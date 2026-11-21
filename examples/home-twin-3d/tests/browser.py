"""Exercise the local 3D demo through its real rendered controls.

Run after starting the preview server:
    python tests/browser.py --base-url http://127.0.0.1:8776

No server is started here, and no external website or real device is contacted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import expect, sync_playwright


ROOT = Path(__file__).resolve().parents[1]
IDS = ("living-main", "dining-pendant", "studio-main", "studio-desk")
NAMES = {
    "living-main": "客厅主灯",
    "dining-pendant": "餐厅吊灯",
    "studio-main": "电竞房主灯",
    "studio-desk": "电竞房桌面灯",
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:8776")
    parser.add_argument("--channel", help="Optional installed Chromium channel, e.g. chrome")
    args = parser.parse_args()
    base = args.base_url.rstrip("/")
    target = urlparse(base)
    if target.hostname not in {"127.0.0.1", "localhost", "::1"}:
        parser.error("This test is restricted to a local preview server")

    previews = ROOT / "previews"
    previews.mkdir(exist_ok=True)
    report = {"base_url": base, "checks": [], "screenshots": [], "page_errors": [], "console_errors": [], "external_requests": [], "failed_requests": []}

    def mark(name: str) -> None:
        report["checks"].append(name)
        print(f"PASS {name}", flush=True)

    def optional_url(url: str) -> bool:
        path = urlparse(url).path
        return path.startswith("/neonplan-preview/") or path == "/exports/wuhan-neonplan-import.json"

    def watch(page) -> None:
        page.on("pageerror", lambda error: report["page_errors"].append(str(error)))
        page.on("console", lambda message: report["console_errors"].append(message.text) if message.type == "error" else None)

        def request_seen(request) -> None:
            parsed = urlparse(request.url)
            if parsed.scheme in {"http", "https"} and (parsed.scheme, parsed.netloc) != (target.scheme, target.netloc):
                report["external_requests"].append(request.url)

        def request_failed(request) -> None:
            if not optional_url(request.url):
                report["failed_requests"].append({"url": request.url, "failure": request.failure})

        def response_seen(response) -> None:
            if response.status >= 400 and not optional_url(response.url):
                report["failed_requests"].append({"url": response.url, "status": response.status})

        page.on("request", request_seen)
        page.on("requestfailed", request_failed)
        page.on("response", response_seen)

    def ready(page) -> None:
        page.wait_for_selector('body[data-ready="true"]', timeout=45000)
        page.wait_for_load_state("networkidle")
        expect(page.locator("#loading")).to_be_hidden()
        expect(page.locator("#error")).to_be_hidden()
        page.wait_for_timeout(700)

    def switch(page, device_id: str):
        return page.locator(f'[data-device-toggle="{device_id}"]')

    def switch_states(page):
        return {device_id: switch(page, device_id).get_attribute("aria-checked") for device_id in IDS}

    def state_is(page, expected: dict[str, bool]) -> None:
        for device_id, on in expected.items():
            expect(switch(page, device_id)).to_have_attribute("aria-checked", str(on).lower())
        expect(page.locator("#on-count")).to_have_text(str(sum(expected.values())))

    def rendered_hash(page, selector="#scene") -> str:
        page.wait_for_timeout(300)
        return hashlib.sha256(page.locator(selector).screenshot()).hexdigest()

    def capture(page, filename: str) -> None:
        page.wait_for_timeout(500)
        page.screenshot(path=str(previews / filename), full_page=True)
        report["screenshots"].append(filename)

    with sync_playwright() as playwright:
        launch = {"headless": True, "args": ["--use-angle=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"]}
        if args.channel:
            launch["channel"] = args.channel
        browser = playwright.chromium.launch(**launch)
        try:
            context = browser.new_context(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
            page = context.new_page()
            watch(page)
            page.goto(base, wait_until="networkidle")
            ready(page)
            assert "未连接设备" in page.locator(".demo-badge").inner_text()
            state_is(page, dict.fromkeys(IDS, True))
            for device_id in IDS:
                expect(switch(page, device_id)).to_have_attribute("role", "switch")
            capture(page, "desktop.png")
            mark("desktop loads as an explicitly simulated 3D home")

            before = rendered_hash(page)
            switch(page, "living-main").click()
            state_is(page, {"living-main": False, "dining-pendant": True, "studio-main": True, "studio-desk": True})
            assert rendered_hash(page) != before, "Switch changed the UI but not the rendered lighting"
            page.locator('[data-device-select="living-main"]').click()
            expect(page.locator("#selected-name")).to_have_text(NAMES["living-main"])
            slider = page.locator("#brightness")
            slider.focus()
            slider.press("End")
            expect(slider).to_have_value("100")
            slider.press("ArrowLeft")
            expect(slider).to_have_value("99")
            expect(page.locator("#brightness-value")).to_contain_text("99")
            expect(switch(page, "living-main")).to_have_attribute("aria-checked", "true")
            slider.press("Home")
            expect(slider).to_have_value("0")
            expect(switch(page, "living-main")).to_have_attribute("aria-checked", "false")
            switch(page, "living-main").focus()
            page.keyboard.press("Space")
            expect(slider).to_have_value("99")
            mark("switches, keyboard dimming, zero brightness, and remembered brightness")

            page.locator('[data-scene="movie"]').click()
            expect(page.locator('[data-scene="movie"]')).to_have_attribute("aria-pressed", "true")
            state_is(page, {"living-main": True, "dining-pendant": False, "studio-main": False, "studio-desk": True})
            page.locator("#lighting-mode").click()
            expect(page.locator("#lighting-mode")).to_have_attribute("aria-pressed", "true")
            capture(page, "night.png")
            page.locator('[data-scene="away"]').click()
            state_is(page, dict.fromkeys(IDS, False))
            page.locator('[data-scene="home"]').click()
            state_is(page, dict.fromkeys(IDS, True))
            mark("home, movie, away scenes and night display")

            page.locator("#lighting-mode").click()
            expect(page.locator("#lighting-mode")).to_have_attribute("aria-pressed", "false")
            for view in ("living", "studio", "bedroom", "top"):
                prior = rendered_hash(page)
                page.locator(f'[data-view="{view}"]').click()
                expect(page.locator(f'[data-view="{view}"]')).to_have_attribute("aria-pressed", "true")
                page.wait_for_timeout(800)
                assert rendered_hash(page) != prior, f"Camera did not change for {view}"
            capture(page, "top.png")
            for selector in ("#cutaway", "#cad-overlay", "#room-label-toggle"):
                prior = rendered_hash(page, "#viewport")
                control = page.locator(selector)
                original = control.is_checked()
                control.set_checked(not original)
                assert rendered_hash(page, "#viewport") != prior, f"Display option has no visible effect: {selector}"
                control.set_checked(original)
            mark("camera presets, wall cutaway, CAD overlay, and room labels")

            lamp = page.locator('[data-lamp="dining-pendant"]')
            expect(lamp).to_be_visible()
            lamp.click()
            expect(switch(page, "dining-pendant")).to_have_attribute("aria-checked", "false")
            expect(page.locator("#selected-name")).to_have_text(NAMES["dining-pendant"])
            lamp.focus()
            page.keyboard.press("Enter")
            expect(switch(page, "dining-pendant")).to_have_attribute("aria-checked", "true")
            mark("projected lamp buttons toggle and select the matching device")

            page.locator('[data-view="overview"]').click()
            page.wait_for_timeout(800)
            before_states = switch_states(page)
            bounds = page.locator("#scene").bounding_box()
            assert bounds
            start_x, start_y = bounds["x"] + bounds["width"] * .43, bounds["y"] + bounds["height"] * .64
            page.mouse.move(start_x, start_y)
            page.mouse.down()
            page.mouse.move(start_x + 140, start_y + 35, steps=12)
            page.mouse.up()
            page.wait_for_timeout(400)
            assert switch_states(page) == before_states, "Canvas drag must never toggle a lamp"
            page.locator("#scene").focus()
            prior = rendered_hash(page)
            page.keyboard.press("ArrowLeft")
            page.keyboard.press("+")
            assert rendered_hash(page) != prior, "Canvas keyboard controls did not change the view"
            assert switch_states(page) == before_states
            mark("canvas drag and keyboard camera controls do not toggle devices")

            page.locator("#source-open").click()
            expect(page.locator("#source-dialog")).to_be_visible()
            page.keyboard.press("Escape")
            expect(page.locator("#source-dialog")).to_be_hidden()
            page.locator("#source-open").click()
            page.locator("#source-close").click()
            expect(page.locator("#source-dialog")).to_be_hidden()
            mark("source dialog opens and closes by button and Escape")

            page.locator("#design-open").click()
            expect(page.locator("#design-dialog")).to_be_visible()
            reference = page.locator("#design-dialog img")
            expect(reference).to_be_visible()
            assert reference.evaluate("image => image.complete && image.naturalWidth > 0"), "Designer reference image did not load"
            assert urlparse(reference.evaluate("image => image.currentSrc")).netloc == target.netloc, "Designer reference must be served locally"
            page.keyboard.press("Escape")
            expect(page.locator("#design-dialog")).to_be_hidden()
            page.locator("#design-open").click()
            page.locator("#design-close").click()
            expect(page.locator("#design-dialog")).to_be_hidden()
            mark("designer reference dialog uses a local image and closes with button and Escape")

            page.locator('[data-device-select="studio-desk"]').focus()
            page.keyboard.press("Enter")
            slider.focus()
            slider.press("End")
            for _ in range(7):
                slider.press("ArrowLeft")
            expect(slider).to_have_value("93")
            expected_states = switch_states(page)
            page.reload(wait_until="networkidle")
            ready(page)
            assert switch_states(page) == expected_states
            expect(page.locator("#selected-name")).to_have_text(NAMES["studio-desk"])
            expect(page.locator("#brightness")).to_have_value("93")
            mark("selection and simulated brightness persist after reload")

            expect(page.locator("#designer-mode")).to_be_checked()
            expect(page.locator("body")).to_have_attribute("data-designer", "true")
            page.locator('[data-view="living"]').click()
            page.wait_for_timeout(800)
            remembered_states = switch_states(page)
            remembered_scene = page.locator("#current-scene").inner_text()
            for cycle in range(3):
                styled = rendered_hash(page)
                page.locator("#designer-mode").uncheck()
                expect(page.locator("body")).to_have_attribute("data-designer", "false")
                plain = rendered_hash(page)
                assert styled != plain, f"Designer mode did not visibly change the model on cycle {cycle + 1}"
                assert switch_states(page) == remembered_states
                expect(page.locator("#selected-name")).to_have_text(NAMES["studio-desk"])
                expect(page.locator("#brightness")).to_have_value("93")
                assert page.locator("#current-scene").inner_text() == remembered_scene
                page.locator("#designer-mode").check()
                expect(page.locator("body")).to_have_attribute("data-designer", "true")
                assert rendered_hash(page) != plain
                assert switch_states(page) == remembered_states
                expect(page.locator("#selected-name")).to_have_text(NAMES["studio-desk"])
                expect(page.locator("#brightness")).to_have_value("93")
                expect(page.locator("[data-lamp]")).to_have_count(4)
                expect(page.locator("#scene")).to_have_count(1)
                expect(page.locator('[data-view="living"]')).to_have_attribute("aria-pressed", "true")
            assert not report["page_errors"], report["page_errors"]
            assert not report["console_errors"], report["console_errors"]
            page.locator('[data-view="top"]').click()
            page.wait_for_timeout(800)
            recreated_lamp = page.locator('[data-lamp="studio-desk"]')
            recreated_lamp.click()
            expect(switch(page, "studio-desk")).to_have_attribute("aria-checked", "false")
            recreated_lamp.click()
            expect(page.locator("#brightness")).to_have_value("93")
            mark("three designer-mode rebuild cycles preserve state, selection, dimming, and working single lamp handlers")

            page.locator('[data-scene="home"]').click()
            for view in ("living", "studio", "bedroom"):
                page.locator(f'[data-view="{view}"]').click()
                page.wait_for_timeout(800)
                capture(page, f"designer-{view}.png")
            page.locator('[data-view="studio"]').click()
            page.wait_for_timeout(800)
            cutaway_hash = rendered_hash(page)
            page.locator("#cutaway").uncheck()
            assert rendered_hash(page) != cutaway_hash, "Full walls must visibly restore the scene height"
            capture(page, "designer-full-walls.png")
            page.locator("#cutaway").check()
            page.locator('[data-view="overview"]').click()
            page.wait_for_timeout(800)
            capture(page, "desktop.png")
            mark("designer living, studio, bedroom, and full-wall views render without errors")

            with page.expect_download() as download_info:
                page.locator("#export-mapping").click()
            export_file = previews / "tested-entity-mapping.json"
            download_info.value.save_as(str(export_file))
            mapping = json.loads(export_file.read_text(encoding="utf-8"))
            assert mapping["mode"] == "simulation" and mapping["connected"] is False
            assert len(mapping["devices"]) == 4 and all(item["entityId"] is None for item in mapping["devices"])
            mark("downloaded mapping declares disconnected simulation and no bound entities")

            mobile_context = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=1, is_mobile=True, has_touch=True)
            mobile = mobile_context.new_page()
            watch(mobile)
            mobile.goto(base, wait_until="networkidle")
            ready(mobile)
            assert mobile.evaluate("document.documentElement.scrollWidth <= window.innerWidth"), "Mobile has horizontal overflow"
            expect(mobile.locator("[data-view]")).to_have_count(5)
            view_rectangles = mobile.locator("[data-view]").evaluate_all("buttons => buttons.map(button => {const r=button.getBoundingClientRect();return {view:button.dataset.view,left:r.left,right:r.right,top:r.top,bottom:r.bottom};})")
            assert all(rect["left"] >= 0 and rect["right"] <= 390 for rect in view_rectangles), f"Mobile camera buttons are clipped: {view_rectangles}"
            for view in ("living", "studio", "bedroom", "top", "overview"):
                mobile.locator(f'[data-view="{view}"]').click()
                expect(mobile.locator(f'[data-view="{view}"]')).to_have_attribute("aria-pressed", "true")
            mobile.locator("#designer-mode").uncheck()
            expect(mobile.locator("body")).to_have_attribute("data-designer", "false")
            state_is(mobile, dict.fromkeys(IDS, True))
            mobile.locator("#designer-mode").check()
            expect(mobile.locator("body")).to_have_attribute("data-designer", "true")
            mark("all five mobile camera buttons fit and designer mode remains operable")
            mobile.locator('[data-scene="away"]').click()
            state_is(mobile, dict.fromkeys(IDS, False))
            switch(mobile, "studio-main").click()
            expect(switch(mobile, "studio-main")).to_have_attribute("aria-checked", "true")
            mobile.locator('[data-view="top"]').click()
            mobile.wait_for_timeout(700)
            mobile.locator('[data-lamp="living-main"]').click()
            expect(switch(mobile, "living-main")).to_have_attribute("aria-checked", "true")
            mobile.locator('[data-scene="home"]').click()
            mobile.locator('[data-view="overview"]').click()
            mobile.evaluate("window.scrollTo(0,0)")
            capture(mobile, "mobile.png")
            assert mobile.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
            mark("390×844 mobile layout has no horizontal overflow and remains operable")
            mobile_context.close()
            context.close()

            assert not report["page_errors"], report["page_errors"]
            assert not report["console_errors"], report["console_errors"]
            assert not report["external_requests"], report["external_requests"]
            assert not report["failed_requests"], report["failed_requests"]
            mark("no page errors, external requests, or failed required resources")
            report["status"] = "passed"
        except Exception as error:
            report["status"] = "failed"
            report["failure"] = str(error)
            try:
                page.screenshot(path=str(previews / "failure.png"), full_page=True)
            except Exception:
                pass
            raise
        finally:
            (previews / "browser-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            browser.close()
    print(json.dumps({"status": report["status"], "checks": len(report["checks"]), "screenshots": report["screenshots"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
