"""Read-only Home Assistant REST connectivity probe (Python standard library)."""

from __future__ import annotations

import argparse
import http.client
import ipaddress
import json
import os
import re
import socket
import ssl
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, HTTPSHandler, ProxyHandler, Request, build_opener


TIMEOUT_SECONDS = 5
MAX_RESPONSE_BYTES = 1024 * 1024
ENTITY_PATTERN = re.compile(r"[a-z_][a-z0-9_]*\.[a-z0-9_]+", re.ASCII)
VERSION_PATTERN = re.compile(
    r"[0-9]{4}\.(?:0?[1-9]|1[0-2])\.[0-9]+(?:(?:a|b|rc)[0-9]+|\.dev[0-9]+)?",
    re.ASCII,
)


class InputError(ValueError):
    """A fixed reason, never the original invalid argument or setting."""


class SafeArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise InputError("invalid_arguments")


class NoRedirect(HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        # Reject before urllib parses an untrusted Location header.
        raise HTTPError(req.full_url, code, msg, headers, fp)

    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302
    http_error_308 = http_error_302


def make_report() -> dict:
    return {
        "scope": "ha_rest_probe",
        "status": "failed",
        "exit_code": 2,
        "ha_version": None,
        "checks": [],
    }


def validate_settings(raw_url: str, token: str, entities: list[str]) -> str:
    """Reject every invalid input before constructing a network transport."""
    if not raw_url:
        raise InputError("missing_hass_url")
    if not token:
        raise InputError("missing_hass_token")
    if not all(33 <= ord(character) <= 126 for character in token):
        raise InputError("invalid_hass_token")
    # urlsplit strips several controls; inspect the original value first.
    if any(ord(character) <= 32 or ord(character) >= 127 for character in raw_url):
        raise InputError("invalid_hass_url")
    if any(character in raw_url for character in "\\%?#"):
        raise InputError("invalid_hass_url")
    try:
        parts = urlsplit(raw_url)
        hostname = parts.hostname
        port = parts.port
        if (
            parts.scheme not in {"http", "https"}
            or not hostname
            or parts.username is not None
            or parts.password is not None
            or parts.path not in {"", "/"}
            or parts.query
            or parts.fragment
            or parts.netloc.endswith(":")
            or port == 0
        ):
            raise ValueError
        if ":" in hostname:
            ipaddress.IPv6Address(hostname)
        elif re.fullmatch(r"[0-9.]+", hostname):
            ipaddress.IPv4Address(hostname)
        else:
            labels = hostname.removesuffix(".").split(".")
            if len(hostname) > 253 or not all(
                re.fullmatch(r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?", label)
                for label in labels
            ):
                raise ValueError
    except ValueError:
        raise InputError("invalid_hass_url") from None
    if any(
        len(entity) > 255 or not ENTITY_PATTERN.fullmatch(entity) or token in entity
        for entity in entities
    ):
        raise InputError("invalid_entity_id")
    return raw_url.removesuffix("/")


def error_reason(error: Exception) -> str:
    if isinstance(error, HTTPError):
        if 300 <= error.code < 400:
            return "redirect_blocked"
        if error.code in {401, 403}:
            return "authentication_failed"
        if error.code == 404:
            return "endpoint_not_found"
        return "http_error"
    cause = error.reason if isinstance(error, URLError) else error
    if isinstance(cause, (socket.timeout, TimeoutError)):
        return "timeout"
    if isinstance(cause, ssl.SSLError):
        return "tls_error"
    return "network_error"


def get_json(opener, base_url: str, token: str, path: str) -> tuple[object, str | None]:
    request = Request(
        base_url + path,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        method="GET",
    )
    try:
        with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
            payload = response.read(MAX_RESPONSE_BYTES + 1)
            if len(payload) > MAX_RESPONSE_BYTES:
                return None, "invalid_response"
    except (OSError, URLError, http.client.HTTPException) as error:
        reason = error_reason(error)
        if isinstance(error, HTTPError):
            error.close()
        return None, reason
    try:
        return json.loads(payload), None
    except (ValueError, UnicodeError, RecursionError):
        return None, "invalid_response"


def add_check(report: dict, name: str, reason: str, passed: bool, entity_id: str | None = None) -> None:
    check = {"name": name, "status": "passed" if passed else "failed", "reason": reason}
    if entity_id is not None:
        check["entity_id"] = entity_id
    report["checks"].append(check)


def probe(base_url: str, token: str, entities: list[str]) -> dict:
    report = make_report()
    report["exit_code"] = 1
    opener = build_opener(
        ProxyHandler({}), NoRedirect(), HTTPSHandler(context=ssl.create_default_context())
    )
    api, reason = get_json(opener, base_url, token, "/api/")
    if reason is None and (not isinstance(api, dict) or api.get("message") != "API running."):
        reason = "invalid_response"
    add_check(report, "api", reason or "api_available", reason is None)
    if reason:
        return report
    config, reason = get_json(opener, base_url, token, "/api/config")
    version = config.get("version") if isinstance(config, dict) else None
    if reason is None and (
        not isinstance(version, str)
        or not VERSION_PATTERN.fullmatch(version)
        or token in version
    ):
        reason = "invalid_response"
    add_check(report, "config", reason or "config_available", reason is None)
    if reason:
        return report
    report["ha_version"] = version
    for entity_id in entities:
        state, reason = get_json(opener, base_url, token, f"/api/states/{entity_id}")
        if reason is None:
            if (
                not isinstance(state, dict)
                or state.get("entity_id") != entity_id
                or not isinstance(state.get("state"), str)
                or not state["state"].strip()
                or not isinstance(state.get("attributes"), dict)
            ):
                reason = "invalid_response"
            elif state["state"].strip().casefold() in {"unknown", "unavailable"}:
                reason = "entity_unavailable"
        add_check(report, "entity_state", reason or "entity_available", reason is None, entity_id)
    if all(check["status"] == "passed" for check in report["checks"]):
        report["status"] = "passed"
        report["exit_code"] = 0
    return report


def render_report(report: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(report, ensure_ascii=True))
        return
    print(
        f"scope={report['scope']} status={report['status']} "
        f"exit_code={report['exit_code']} ha_version={report['ha_version'] or 'not_available'}"
    )
    for check in report["checks"]:
        target = f" {check['entity_id']}" if "entity_id" in check else ""
        print(f"{check['name']}{target}: {check['status']} ({check['reason']})")


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    parser = SafeArgumentParser(
        description="Read-only HA REST probe; no Hermes or device-action verification.",
        allow_abbrev=False,
    )
    parser.add_argument("--entity-id", action="append", default=[], metavar="DOMAIN.OBJECT")
    parser.add_argument("--json", action="store_true", help="Emit a structured, sanitized report.")
    try:
        options = parser.parse_args(arguments)
        token = os.environ.get("HASS_TOKEN", "")
        base_url = validate_settings(os.environ.get("HASS_URL", ""), token, options.entity_id)
    except InputError as error:
        report = make_report()
        add_check(report, "input", str(error), False)
    else:
        report = probe(base_url, token, options.entity_id)
    render_report(report, "--json" in arguments)
    return report["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
