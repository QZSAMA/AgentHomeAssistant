"""Check the actual raycast path, independently of projected DOM lamp buttons."""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    try:
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        page.goto('http://127.0.0.1:8776/')
        page.wait_for_selector('body[data-ready=true]')
        page.wait_for_timeout(300)
        lamp = page.locator('[data-lamp="living-main"]')
        location = lamp.bounding_box()
        before = page.locator('[data-device-toggle="living-main"]').get_attribute('aria-checked')
        # The same on-screen target is now reached by the underlying canvas.
        page.locator('.lamp-label').evaluate_all("els => els.forEach(el => el.style.pointerEvents='none')")
        page.mouse.click(location['x']+location['width']/2, location['y']+location['height']/2)
        page.wait_for_timeout(100)
        after = page.locator('[data-device-toggle="living-main"]').get_attribute('aria-checked')
        assert before != after, 'Canvas raycast must toggle the lamp, without the DOM overlay'
        print('PASS: direct canvas raycast toggles the matching simulated light')
    finally:
        browser.close()
