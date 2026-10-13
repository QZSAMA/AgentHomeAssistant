"""Offline contract tests for the standalone, read-only HA REST probe."""

from __future__ import annotations

import json
import contextlib
import http.server
import importlib.util
import io
import os
from pathlib import Path
import socket
import ssl
import subprocess
import sys
import threading
import unittest
from unittest import mock
import urllib.error
from urllib.request import HTTPSHandler, ProxyHandler


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "ha_probe.py"
TOKEN = "PRIVATE_TOKEN_DO_NOT_PRINT_abc123"

SPEC = importlib.util.spec_from_file_location("standalone_ha_probe", SCRIPT)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)


class FixtureHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.server.requests.append((self.command, self.path, dict(self.headers)))
        status, payload, headers = self.server.routes.get(self.path, (404, {}, {}))
        body = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        for name, value in headers.items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        self.server.requests.append((self.command, self.path, dict(self.headers)))
        self.send_response(405)
        self.end_headers()

    def log_message(self, format, *args):
        pass


class ProbeBehaviorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), FixtureHandler)
        cls.worker = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.worker.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.worker.join(timeout=5)

    def setUp(self):
        self.server.requests = []
        self.server.routes = {
            "/api/": (200, {"message": "API running."}, {}),
            "/api/config": (200, {"version": "2026.10.1", "location_name": TOKEN}, {}),
            "/api/states/input_boolean.aha_poc_light": (
                200,
                {"entity_id": "input_boolean.aha_poc_light", "state": "off", "attributes": {"private": TOKEN}},
                {},
            ),
            "/api/states/input_boolean.aha_poc_fan": (
                200,
                {"entity_id": "input_boolean.aha_poc_fan", "state": "on", "attributes": {}},
                {},
            ),
        }

    def run_probe(self, args=None, settings=None):
        environment = {"HASS_URL": self.base_url, "HASS_TOKEN": TOKEN}
        environment.update(settings or {})
        stdout, stderr = io.StringIO(), io.StringIO()
        with mock.patch.object(os, "environ", environment):
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                code = PROBE.main(["--json", *(args or [])])
        self.assertEqual(stderr.getvalue(), "")
        self.assertNotIn(TOKEN, stdout.getvalue())
        report = json.loads(stdout.getvalue())
        self.assertEqual(report["exit_code"], code)
        self.assertEqual(report["scope"], "ha_rest_probe")
        self.assertEqual(report["status"], "passed" if code == 0 else "failed")
        return code, report

    def test_default_probe_reads_only_api_and_config(self):
        code, report = self.run_probe()
        self.assertEqual(code, 0)
        self.assertEqual(report["ha_version"], "2026.10.1")
        self.assertEqual([item[1] for item in self.server.requests], ["/api/", "/api/config"])
        self.assertTrue(all(item[0] == "GET" for item in self.server.requests))
        self.assertTrue(all(item[2].get("Authorization") == f"Bearer {TOKEN}" for item in self.server.requests))

    def test_repeated_entity_flags_check_only_requested_entities(self):
        code, report = self.run_probe([
            "--entity-id", "input_boolean.aha_poc_light", "--entity-id", "input_boolean.aha_poc_fan"
        ])
        self.assertEqual(code, 0)
        self.assertEqual([item[1] for item in self.server.requests], [
            "/api/", "/api/config", "/api/states/input_boolean.aha_poc_light", "/api/states/input_boolean.aha_poc_fan"
        ])
        self.assertEqual([item["entity_id"] for item in report["checks"] if item["name"] == "entity_state"],
                         ["input_boolean.aha_poc_light", "input_boolean.aha_poc_fan"])
        self.assertNotIn("attributes", json.dumps(report))
        self.assertFalse(any("state" in item for item in report["checks"]))

    def test_missing_settings_fail_before_network(self):
        for settings, reason in [
            ({"HASS_URL": ""}, "missing_hass_url"),
            ({"HASS_TOKEN": ""}, "missing_hass_token"),
        ]:
            with self.subTest(reason=reason):
                code, report = self.run_probe(settings=settings)
                self.assertEqual(code, 2)
                self.assertEqual(report["checks"][0]["reason"], reason)
                self.assertEqual(self.server.requests, [])

    def test_invalid_urls_are_rejected_before_network(self):
        invalid_urls = [
            "example.test", "ftp://example.test", "file:///etc/passwd", "https://", "http://user:pass@example.test",
            "http://example.test/path", "http://example.test?token=private", "http://example.test#fragment",
            "http://example.test:", "http://example.test:0", "http://example.test:65536", "http://example.test:bad",
            "http://[::1", "http://[]", "http://exa mple.test", "http://example.test\n", "http://exa\tmple.test",
            " http://example.test", "http://example.test\\other", "http://example.test/%2f", "http://%65xample.test",
            "http://example.test?", "http://example.test#", "http://example.test\x00", "http://example..test",
            "http://[::1]evil", "http://[::1]evil:8123", "http://[::1]:abc",
        ]
        with mock.patch.object(PROBE, "build_opener", create=True) as transport:
            for value in invalid_urls:
                with self.subTest(value=repr(value)):
                    code, report = self.run_probe(settings={"HASS_URL": value})
                    self.assertEqual(code, 2)
                    self.assertEqual(report["checks"][0]["reason"], "invalid_hass_url")
            transport.assert_not_called()

    def test_valid_root_urls_reach_the_transport(self):
        for value in [
            "http://localhost", "http://localhost:8123/", "https://ha.example.test/",
            "http://192.0.2.1:8123", "http://[::1]:8123/", "http://[::ffff:192.0.2.1]",
        ]:
            with self.subTest(value=value):
                opener = mock.Mock()
                opener.open.side_effect = urllib.error.URLError(TOKEN)
                with mock.patch.object(PROBE, "build_opener", return_value=opener):
                    code, report = self.run_probe(settings={"HASS_URL": value})
                self.assertEqual(code, 1)
                self.assertEqual(report["checks"][0]["reason"], "network_error")
                self.assertEqual(opener.open.call_count, 1)

    def test_entity_domain_may_start_with_underscore(self):
        entity_id = "_domain.aha_lab_light"
        self.server.routes[f"/api/states/{entity_id}"] = (
            200, {"entity_id": entity_id, "state": "off", "attributes": {}}, {}
        )
        code, report = self.run_probe(["--entity-id", entity_id])
        self.assertEqual(code, 0)
        self.assertEqual(report["checks"][-1]["entity_id"], entity_id)

    def test_entity_containing_token_is_not_reflected_or_requested(self):
        entity_id = "input_boolean.aha_lab_light"
        for token in [entity_id, "aha_lab"]:
            with self.subTest(token=token):
                code, report = self.run_probe(["--entity-id", entity_id], {"HASS_TOKEN": token})
                self.assertEqual(code, 2)
                self.assertEqual(report["checks"][0]["reason"], "invalid_entity_id")
                self.assertNotIn(token, json.dumps(report))
        self.assertEqual(self.server.requests, [])

    def test_invalid_entities_are_all_validated_before_network(self):
        for value in ["", "light", ".kitchen", "light.", "LIGHT.kitchen", "light.kitchen/../../config", "light.kitchen?x=y",
                      "light.kitchen#x", "light.kitchen\n", "light.kit chen", "light.%20", "light.kitchen.other", "light." + "a" * 256]:
            with self.subTest(value=repr(value)):
                code, report = self.run_probe(["--entity-id", "input_boolean.aha_poc_light", "--entity-id", value])
                self.assertEqual(code, 2)
                self.assertEqual(report["checks"][0]["reason"], "invalid_entity_id")
        self.assertEqual(self.server.requests, [])

    def test_invalid_token_cannot_inject_authorization_headers(self):
        for token in ["bad\ntoken", "bad\rtoken", " badtoken", "badtoken ", "bad token", "bad\x00token"]:
            with self.subTest(token=repr(token)):
                code, report = self.run_probe(settings={"HASS_TOKEN": token})
                self.assertEqual(code, 2)
                self.assertEqual(report["checks"][0]["reason"], "invalid_hass_token")
        self.assertEqual(self.server.requests, [])

    def test_invalid_arguments_never_echo_values(self):
        for args in [["--token", TOKEN], ["--entity-id"], ["--unknown=" + TOKEN], ["--js"]]:
            with self.subTest(args=args):
                code, report = self.run_probe(args)
                self.assertEqual(code, 2)
                self.assertEqual(report["checks"][0]["reason"], "invalid_arguments")
        self.assertEqual(self.server.requests, [])

    def test_http_errors_use_fixed_reasons_without_bodies(self):
        for status, reason in [(401, "authentication_failed"), (403, "authentication_failed"), (404, "endpoint_not_found"),
                               (429, "http_error"), (500, "http_error")]:
            with self.subTest(status=status):
                self.server.requests = []
                self.server.routes["/api/"] = (status, {"private": TOKEN}, {})
                code, report = self.run_probe()
                self.assertEqual(code, 1)
                self.assertEqual(report["checks"][0]["reason"], reason)
                self.assertEqual(len(self.server.requests), 1)

    def test_redirects_are_not_followed_or_sent_bearer_credentials(self):
        for status in [301, 302, 303, 307, 308]:
            with self.subTest(status=status):
                self.server.requests = []
                self.server.routes["/api/"] = (status, {"private": TOKEN}, {"Location": self.base_url + "/credential-sink?token=" + TOKEN})
                code, report = self.run_probe()
                self.assertEqual(code, 1)
                self.assertEqual(report["checks"][0]["reason"], "redirect_blocked")
                self.assertEqual([item[1] for item in self.server.requests], ["/api/"])

    def test_network_errors_are_sanitized_and_never_retried(self):
        for failure, reason in [
            (urllib.error.URLError(TOKEN), "network_error"),
            (urllib.error.URLError(socket.timeout(TOKEN)), "timeout"),
            (socket.timeout(TOKEN), "timeout"),
            (urllib.error.URLError(ssl.SSLError(TOKEN)), "tls_error"),
            (ssl.SSLError(TOKEN), "tls_error"),
        ]:
            with self.subTest(failure=type(failure).__name__):
                opener = mock.Mock()
                opener.open.side_effect = failure
                with mock.patch.object(PROBE, "build_opener", return_value=opener, create=True):
                    code, report = self.run_probe()
                self.assertEqual(code, 1)
                self.assertEqual(report["checks"][0]["reason"], reason)
                self.assertEqual(opener.open.call_count, 1)
                self.assertEqual(opener.open.call_args.kwargs["timeout"], 5)
                self.assertEqual(opener.open.call_args.args[0].get_method(), "GET")

    def test_malformed_redirect_locations_are_rejected_without_parsing(self):
        for status in [301, 302, 303, 307, 308]:
            for location in ["http://[bad-ipv6", "http://[::1]evil", "file:///private/" + TOKEN]:
                with self.subTest(status=status, location=location):
                    self.server.requests = []
                    self.server.routes["/api/"] = (status, {}, {"Location": location})
                    code, report = self.run_probe()
                    self.assertEqual(code, 1)
                    self.assertEqual(report["checks"][0]["reason"], "redirect_blocked")
                    self.assertEqual([item[1] for item in self.server.requests], ["/api/"])

    def test_https_opener_uses_certificate_validating_context(self):
        opener = mock.Mock()
        opener.open.side_effect = urllib.error.URLError(TOKEN)
        with mock.patch.object(PROBE, "build_opener", return_value=opener, create=True) as factory:
            self.run_probe(settings={"HASS_URL": "https://example.test"})
        self.assertTrue(factory.called, "The probe must construct a secure HTTPS transport.")
        handlers = factory.call_args.args
        https = next(item for item in handlers if isinstance(item, HTTPSHandler))
        self.assertTrue(https._context.check_hostname)
        self.assertEqual(https._context.verify_mode, ssl.CERT_REQUIRED)

    def test_environment_proxies_are_disabled(self):
        opener = mock.Mock()
        opener.open.side_effect = urllib.error.URLError(TOKEN)
        with mock.patch.object(PROBE, "build_opener", return_value=opener, create=True) as factory:
            self.run_probe(settings={"HTTP_PROXY": "http://private-proxy.invalid:8000", "HTTPS_PROXY": "http://private-proxy.invalid:8000"})
        self.assertTrue(factory.called, "The probe must explicitly configure its HTTP transport.")
        proxies = next((item for item in factory.call_args.args if isinstance(item, ProxyHandler)), None)
        self.assertIsNotNone(proxies)
        self.assertEqual(proxies.proxies, {})

    def test_malformed_api_payload_is_failure(self):
        for payload in [b"not json " + TOKEN.encode(), [], None, {}, {"message": [TOKEN]}, {"message": TOKEN}]:
            with self.subTest(payload=type(payload).__name__):
                self.server.routes["/api/"] = (200, payload, {})
                code, report = self.run_probe()
                self.assertEqual(code, 1)
                self.assertEqual(report["checks"][0]["reason"], "invalid_response")

    def test_empty_non_utf8_and_deep_payloads_are_structured_failures(self):
        for status, payload in [
            (204, b""), (200, b"\xff"), (200, b"[" * 2000 + b"]" * 2000),
        ]:
            with self.subTest(status=status, size=len(payload)):
                self.server.routes["/api/"] = (status, payload, {})
                code, report = self.run_probe()
                self.assertEqual(code, 1)
                self.assertEqual(report["checks"][0]["reason"], "invalid_response")

    def test_response_bodies_are_limited_to_one_mebibyte(self):
        payload = json.dumps({"message": "API running."}).encode()
        for size, expected_code in [(1024 * 1024, 0), (1024 * 1024 + 1, 1)]:
            with self.subTest(size=size):
                self.server.routes["/api/"] = (200, payload + b" " * (size - len(payload)), {})
                code, report = self.run_probe()
                self.assertEqual(code, expected_code)
                if code:
                    self.assertEqual(report["checks"][0]["reason"], "invalid_response")

    def test_config_requires_a_safe_home_assistant_version(self):
        for payload in [[], {}, {"version": 12}, {"version": TOKEN}, {"version": "2026.10.1\n"}, {"version": "2026.10.1" + TOKEN}]:
            with self.subTest(payload=payload):
                self.server.routes["/api/config"] = (200, payload, {})
                code, report = self.run_probe()
                self.assertEqual(code, 1)
                self.assertIsNone(report["ha_version"])
                self.assertEqual(report["checks"][-1]["reason"], "invalid_response")

    def test_valid_development_version_is_supported(self):
        for version in ["2026.10.0b1", "2026.10.0rc1", "2026.11.0.dev0"]:
            with self.subTest(version=version):
                self.server.routes["/api/config"] = (200, {"version": version}, {})
                code, report = self.run_probe()
                self.assertEqual(code, 0)
                self.assertEqual(report["ha_version"], version)

    def test_version_equal_to_token_is_not_reflected(self):
        self.server.routes["/api/config"] = (200, {"version": "2026.10.1"}, {})
        code, report = self.run_probe(settings={"HASS_TOKEN": "2026.10.1"})
        self.assertEqual(code, 1)
        self.assertIsNone(report["ha_version"])
        self.assertNotIn("2026.10.1", json.dumps(report))

    def test_unknown_and_unavailable_entities_fail(self):
        for state in ["unknown", "unavailable"]:
            with self.subTest(state=state):
                self.server.routes["/api/states/input_boolean.aha_poc_light"] = (
                    200, {"entity_id": "input_boolean.aha_poc_light", "state": state, "attributes": {}}, {}
                )
                code, report = self.run_probe(["--entity-id", "input_boolean.aha_poc_light"])
                self.assertEqual(code, 1)
                self.assertEqual(report["checks"][-1]["reason"], "entity_unavailable")

    def test_entity_responses_must_match_requested_id_and_state_structure(self):
        invalid_payloads = [
            [], {}, {"entity_id": "input_boolean.aha_poc_fan", "state": "on", "attributes": {}},
            {"entity_id": "input_boolean.aha_poc_light", "state": None, "attributes": {}},
            {"entity_id": "input_boolean.aha_poc_light", "state": "", "attributes": {}},
            {"entity_id": "input_boolean.aha_poc_light", "state": "on", "attributes": []},
            {"entity_id": "input_boolean.aha_poc_light", "state": "on"},
        ]
        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                self.server.routes["/api/states/input_boolean.aha_poc_light"] = (200, payload, {})
                code, report = self.run_probe(["--entity-id", "input_boolean.aha_poc_light"])
                self.assertEqual(code, 1)
                self.assertEqual(report["checks"][-1]["reason"], "invalid_response")

    def test_one_failed_entity_does_not_hide_later_requested_checks(self):
        self.server.routes["/api/states/input_boolean.aha_poc_light"] = (404, {"private": TOKEN}, {})
        code, report = self.run_probe(["--entity-id", "input_boolean.aha_poc_light", "--entity-id", "input_boolean.aha_poc_fan"])
        self.assertEqual(code, 1)
        self.assertEqual([item["status"] for item in report["checks"][-2:]], ["failed", "passed"])

    def test_text_and_json_describe_the_same_results(self):
        _, report = self.run_probe(["--entity-id", "input_boolean.aha_poc_light"])
        self.assertIsInstance(report["ha_version"], str)
        stdout = io.StringIO()
        with mock.patch.dict(os.environ, {"HASS_URL": self.base_url, "HASS_TOKEN": TOKEN}, clear=True):
            with contextlib.redirect_stdout(stdout):
                code = PROBE.main(["--entity-id", "input_boolean.aha_poc_light"])
        self.assertEqual(code, report["exit_code"])
        text = stdout.getvalue()
        for value in [report["scope"], report["status"], report["ha_version"], "input_boolean.aha_poc_light"]:
            self.assertIn(value, text)
        for item in report["checks"]:
            self.assertIn(item["reason"], text)
        self.assertNotIn(TOKEN, text)
        self.assertNotIn(self.base_url, text)

    def test_text_failures_match_json_without_sensitive_details(self):
        for settings in [{"HASS_TOKEN": ""}, {}]:
            with self.subTest(settings=settings):
                opener = mock.Mock()
                opener.open.side_effect = urllib.error.URLError(TOKEN + self.base_url)
                with mock.patch.object(PROBE, "build_opener", return_value=opener):
                    expected_code, report = self.run_probe(settings=settings)
                    environment = {"HASS_URL": self.base_url, "HASS_TOKEN": TOKEN, **settings}
                    stdout, stderr = io.StringIO(), io.StringIO()
                    with mock.patch.object(os, "environ", environment):
                        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                            code = PROBE.main([])
                self.assertEqual(code, expected_code)
                self.assertEqual(stderr.getvalue(), "")
                self.assertIn(f"exit_code={code}", stdout.getvalue())
                self.assertIn(report["checks"][0]["reason"], stdout.getvalue())
                self.assertNotIn(TOKEN, stdout.getvalue())
                self.assertNotIn(self.base_url, stdout.getvalue())

    def test_default_report_remains_unchanged_without_expectations(self):
        code, report = self.run_probe()
        self.assertEqual(code, 0)
        self.assertEqual(report, {
            "scope": "ha_rest_probe", "status": "passed", "exit_code": 0,
            "ha_version": "2026.10.1",
            "checks": [
                {"name": "api", "status": "passed", "reason": "api_available"},
                {"name": "config", "status": "passed", "reason": "config_available"},
            ],
        })

    def test_expected_version_matches(self):
        code, report = self.run_probe(["--expect-version", "2026.10.1"])
        self.assertEqual(code, 0)
        self.assertEqual(report["checks"][-1], {
            "name": "version_expectation", "status": "passed", "reason": "version_matches",
        })
        self.assertEqual([item[1] for item in self.server.requests], ["/api/", "/api/config"])

    def test_expected_version_mismatch_short_circuits_entities(self):
        code, report = self.run_probe([
            "--expect-version", "2026.10.2",
            "--entity-id", "input_boolean.aha_poc_light",
            "--expect-state", "input_boolean.aha_poc_fan=on",
        ])
        self.assertEqual(code, 1)
        self.assertEqual(report["ha_version"], "2026.10.1")
        self.assertEqual(report["checks"][-1], {
            "name": "version_expectation", "status": "failed", "reason": "version_mismatch",
        })
        self.assertNotIn("2026.10.2", json.dumps(report))
        self.assertEqual([item[1] for item in self.server.requests], ["/api/", "/api/config"])

    def test_expected_versions_use_existing_format_and_exact_comparison(self):
        for actual, expected, code in [
            ("2026.10.0b1", "2026.10.0b1", 0),
            ("2026.10.0rc1", "2026.10.0rc1", 0),
            ("2026.11.0.dev0", "2026.11.0.dev0", 0),
            ("2026.1.1", "2026.01.1", 1),
        ]:
            with self.subTest(actual=actual, expected=expected):
                self.server.routes["/api/config"] = (200, {"version": actual}, {})
                actual_code, report = self.run_probe(["--expect-version", expected])
                self.assertEqual(actual_code, code)
                self.assertEqual(
                    report["checks"][-1]["reason"],
                    "version_matches" if code == 0 else "version_mismatch",
                )

    def test_invalid_expected_versions_fail_before_network(self):
        for value in ["", "2026.13.1", "2026.10", "v2026.10.1", " 2026.10.1", "2026.10.1\n", TOKEN]:
            with self.subTest(value=repr(value)):
                code, report = self.run_probe(["--expect-version", value])
                self.assertEqual(code, 2)
                self.assertEqual(report["checks"][0]["reason"], "invalid_expected_version")
        self.assertEqual(self.server.requests, [])

    def test_duplicate_expected_versions_are_rejected_even_if_identical(self):
        for second in ["2026.10.1", "2026.10.2"]:
            with self.subTest(second=second):
                code, report = self.run_probe([
                    "--expect-version", "2026.10.1", "--expect-version", second,
                ])
                self.assertEqual(code, 2)
                self.assertEqual(report["checks"][0]["reason"], "invalid_expected_version")
        self.assertEqual(self.server.requests, [])

    def test_expected_state_selects_entity_and_matches(self):
        code, report = self.run_probe(["--expect-state", "input_boolean.aha_poc_light=off"])
        self.assertEqual(code, 0)
        self.assertEqual(report["checks"][-1], {
            "name": "entity_state", "status": "passed", "reason": "state_matches",
            "entity_id": "input_boolean.aha_poc_light",
        })
        self.assertEqual([item[1] for item in self.server.requests], [
            "/api/", "/api/config", "/api/states/input_boolean.aha_poc_light",
        ])
        self.assertTrue(all(item[0] == "GET" for item in self.server.requests))

    def test_state_mismatch_does_not_skip_later_entities_or_retry(self):
        code, report = self.run_probe([
            "--expect-state", "input_boolean.aha_poc_light=on",
            "--expect-state", "input_boolean.aha_poc_fan=on",
        ])
        self.assertEqual(code, 1)
        self.assertEqual([item["reason"] for item in report["checks"][-2:]], [
            "state_mismatch", "state_matches",
        ])
        self.assertEqual([item[1] for item in self.server.requests], [
            "/api/", "/api/config", "/api/states/input_boolean.aha_poc_light",
            "/api/states/input_boolean.aha_poc_fan",
        ])
        self.assertTrue(all(item[0] == "GET" for item in self.server.requests))

    def test_expected_states_compare_exactly_without_normalizing_response(self):
        for state in ["ON", " on", "on ", "On", TOKEN]:
            with self.subTest(state=state):
                self.server.routes["/api/states/input_boolean.aha_poc_light"] = (
                    200, {"entity_id": "input_boolean.aha_poc_light", "state": state, "attributes": {}}, {}
                )
                code, report = self.run_probe(["--expect-state", "input_boolean.aha_poc_light=on"])
                self.assertEqual(code, 1)
                self.assertEqual(report["checks"][-1]["reason"], "state_mismatch")
                self.assertNotIn(state, json.dumps(report))

    def test_invalid_expected_state_specifications_fail_before_network(self):
        for specification in [
            "", "input_boolean.aha_poc_light", "=on", "input_boolean.aha_poc_light=",
            "input_boolean.aha_poc_light=ON", "input_boolean.aha_poc_light= off",
            "input_boolean.aha_poc_light=off ", "input_boolean.aha_poc_light=off\n",
            "input_boolean.aha_poc_light=true", "input_boolean.aha_poc_light=on=off",
            "input_boolean.aha_poc_light=" + TOKEN,
        ]:
            with self.subTest(specification=repr(specification)):
                code, report = self.run_probe(["--expect-state", specification])
                self.assertEqual(code, 2)
                self.assertEqual(report["checks"][0]["reason"], "invalid_expected_state")
        self.assertEqual(self.server.requests, [])

    def test_expected_state_entities_are_validated_before_any_network(self):
        for entity_id in [
            "invalid", "Light.kitchen", " light.kitchen", "light.kitchen ",
            "light.kitchen/../config", "light." + "x" * 256, TOKEN,
        ]:
            with self.subTest(entity_id=entity_id):
                code, report = self.run_probe([
                    "--expect-version", "2026.10.1",
                    "--expect-state", "input_boolean.aha_poc_light=off",
                    "--expect-state", entity_id + "=on",
                ])
                self.assertEqual(code, 2)
                self.assertEqual(report["checks"][0]["reason"], "invalid_entity_id")
        self.assertEqual(self.server.requests, [])

    def test_duplicate_expected_states_are_rejected_even_if_identical(self):
        for second in ["off", "on"]:
            with self.subTest(second=second):
                code, report = self.run_probe([
                    "--expect-state", "input_boolean.aha_poc_light=off",
                    "--expect-state", "input_boolean.aha_poc_light=" + second,
                ])
                self.assertEqual(code, 2)
                self.assertEqual(report["checks"][0]["reason"], "duplicate_expected_state")
        self.assertEqual(self.server.requests, [])

    def test_expectations_append_only_new_entities_after_explicit_order(self):
        code, report = self.run_probe([
            "--expect-state", "input_boolean.aha_poc_light=off",
            "--entity-id", "input_boolean.aha_poc_fan",
            "--expect-state", "input_boolean.aha_poc_fan=on",
            "--entity-id", "input_boolean.aha_poc_fan",
            "--expect-version", "2026.10.1",
        ])
        self.assertEqual(code, 0)
        self.assertEqual([item[1] for item in self.server.requests], [
            "/api/", "/api/config", "/api/states/input_boolean.aha_poc_fan",
            "/api/states/input_boolean.aha_poc_fan", "/api/states/input_boolean.aha_poc_light",
        ])
        self.assertEqual([item["reason"] for item in report["checks"]], [
            "api_available", "config_available", "version_matches",
            "state_matches", "state_matches", "state_matches",
        ])

    def test_unasserted_entities_keep_the_original_success_reason(self):
        code, report = self.run_probe([
            "--entity-id", "input_boolean.aha_poc_fan",
            "--expect-state", "input_boolean.aha_poc_light=off",
        ])
        self.assertEqual(code, 0)
        self.assertEqual([item["reason"] for item in report["checks"][-2:]], [
            "entity_available", "state_matches",
        ])

    def test_api_and_config_errors_precede_version_expectation(self):
        for path, response, reason in [
            ("/api/", (401, {}, {}), "authentication_failed"),
            ("/api/config", (403, {}, {}), "authentication_failed"),
            ("/api/config", (200, {"version": TOKEN}, {}), "invalid_response"),
        ]:
            with self.subTest(path=path, reason=reason):
                self.setUp()
                self.server.routes[path] = response
                code, report = self.run_probe([
                    "--expect-version", "2026.10.1",
                    "--expect-state", "input_boolean.aha_poc_light=off",
                ])
                self.assertEqual(code, 1)
                self.assertEqual(report["checks"][-1]["reason"], reason)
                self.assertNotIn("version_expectation", [item["name"] for item in report["checks"]])
                self.assertTrue(all(not item[1].startswith("/api/states/") for item in self.server.requests))

    def test_entity_errors_precede_state_expectations(self):
        entity_id = "input_boolean.aha_poc_light"
        for status, payload, reason in [
            (401, {}, "authentication_failed"),
            (404, {}, "endpoint_not_found"),
            (200, {"entity_id": entity_id, "state": "on"}, "invalid_response"),
            (200, {"entity_id": entity_id, "state": None, "attributes": {}}, "invalid_response"),
            (200, {"entity_id": "light.wrong", "state": "on", "attributes": {}}, "invalid_response"),
            (200, {"entity_id": entity_id, "state": "unknown", "attributes": {}}, "entity_unavailable"),
            (200, {"entity_id": entity_id, "state": " Unavailable ", "attributes": {}}, "entity_unavailable"),
        ]:
            with self.subTest(status=status, reason=reason):
                self.server.routes[f"/api/states/{entity_id}"] = (status, payload, {})
                code, report = self.run_probe(["--expect-state", entity_id + "=on"])
                self.assertEqual(code, 1)
                self.assertEqual(report["checks"][-1]["reason"], reason)

    def test_expectation_inputs_and_responses_do_not_reflect_tokens(self):
        cases = [
            (["--expect-version", "2026.10.2"], "2026.10.2", 1, "version_mismatch"),
            (["--expect-version", "2026.10.1"], "2026.10.1", 1, "invalid_response"),
            (["--expect-state", "input_boolean.aha_poc_light=off"], "aha_poc", 2, "invalid_entity_id"),
        ]
        for args, token, expected_code, reason in cases:
            with self.subTest(args=args):
                code, report = self.run_probe(args, {"HASS_TOKEN": token})
                self.assertEqual(code, expected_code)
                self.assertEqual(report["checks"][-1]["reason"], reason)
                self.assertNotIn(token, json.dumps(report))

    def test_expectation_text_matches_json_without_state_or_expected_values(self):
        for args, expected_code, reason in [
            (["--expect-state", "input_boolean.aha_poc_light=off"], 0, "state_matches"),
            (["--expect-state", "input_boolean.aha_poc_light=on"], 1, "state_mismatch"),
            (["--expect-version", "2026.10.2"], 1, "version_mismatch"),
            (["--expect-version", TOKEN], 2, "invalid_expected_version"),
            (["--expect-state", "input_boolean.aha_poc_light=" + TOKEN], 2, "invalid_expected_state"),
        ]:
            with self.subTest(args=args):
                json_code, report = self.run_probe(args)
                self.assertEqual(json_code, expected_code)
                self.assertEqual(report["checks"][-1]["reason"], reason)
                stdout, stderr = io.StringIO(), io.StringIO()
                with mock.patch.object(os, "environ", {"HASS_URL": self.base_url, "HASS_TOKEN": TOKEN}):
                    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                        code = PROBE.main(args)
                self.assertEqual(code, expected_code)
                self.assertEqual(stderr.getvalue(), "")
                expected_lines = [
                    f"scope=ha_rest_probe status={report['status']} exit_code={code} "
                    f"ha_version={report['ha_version'] or 'not_available'}"
                ]
                for item in report["checks"]:
                    target = f" {item['entity_id']}" if "entity_id" in item else ""
                    expected_lines.append(f"{item['name']}{target}: {item['status']} ({item['reason']})")
                self.assertEqual(stdout.getvalue(), "\n".join(expected_lines) + "\n")
                self.assertNotIn(TOKEN, stdout.getvalue())
                self.assertNotIn(self.base_url, stdout.getvalue())
                self.assertNotIn("2026.10.2", stdout.getvalue())
                self.assertTrue(all(set(item) <= {"name", "status", "reason", "entity_id"} for item in report["checks"]))

    def test_isolated_cli_runs_expectations_against_offline_fixture(self):
        environment = {**os.environ, "HASS_URL": self.base_url, "HASS_TOKEN": TOKEN}
        completed = subprocess.run(
            [sys.executable, "-I", "-S", "-B", str(SCRIPT),
             "--expect-version=2026.10.1", "--expect-state=input_boolean.aha_poc_light=off", "--json"],
            env=environment, capture_output=True, text=True, timeout=10, check=False,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stderr, "")
        self.assertNotIn(TOKEN, completed.stdout)
        report = json.loads(completed.stdout)
        self.assertEqual([item["reason"] for item in report["checks"][-2:]], [
            "version_matches", "state_matches",
        ])
        self.assertEqual(len(self.server.requests), 3)
        self.assertTrue(all(item[0] == "GET" for item in self.server.requests))


class ProbeCliTests(unittest.TestCase):
    def run_cli(self, *args: str, settings: dict[str, str] | None = None):
        environment = dict(os.environ)
        environment.pop("HASS_URL", None)
        environment.pop("HASS_TOKEN", None)
        environment.update(settings or {})
        return subprocess.run(
            [sys.executable, "-I", "-S", "-B", str(SCRIPT), *args],
            env=environment,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

    def test_missing_configuration_returns_structured_failure(self):
        completed = self.run_cli("--json")
        self.assertEqual(completed.returncode, 2)
        self.assertTrue(
            completed.stdout.startswith("{"),
            "The HA probe CLI must emit a structured input failure even without configuration.",
        )
        report = json.loads(completed.stdout)
        self.assertEqual(report["scope"], "ha_rest_probe")
        self.assertEqual(report["status"], "failed")
        self.assertEqual(report["exit_code"], 2)
        self.assertEqual(report["checks"][0]["reason"], "missing_hass_url")
        self.assertEqual(completed.stderr, "")

    def test_help_is_available_without_configuration_or_site_packages(self):
        completed = self.run_cli("--help")
        self.assertEqual(completed.returncode, 0)
        self.assertIn("Read-only HA REST probe", completed.stdout)
        self.assertEqual(completed.stderr, "")

    def test_help_describes_the_optional_expectations(self):
        completed = self.run_cli("--help")
        self.assertEqual(completed.returncode, 0)
        self.assertIn("--expect-version", completed.stdout)
        self.assertIn("--expect-state", completed.stdout)
        self.assertEqual(completed.stderr, "")

    def test_missing_expectation_values_are_sanitized_cli_errors(self):
        for flag in ["--expect-version", "--expect-state"]:
            with self.subTest(flag=flag):
                completed = self.run_cli("--json", flag)
                self.assertEqual(completed.returncode, 2)
                self.assertEqual(completed.stderr, "")
                self.assertEqual(json.loads(completed.stdout)["checks"][0]["reason"], "invalid_arguments")


if __name__ == "__main__":
    unittest.main()
