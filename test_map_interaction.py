from playwright.sync_api import sync_playwright

def test_map_interaction():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("http://localhost:5000/map")
        page.wait_for_timeout(1000)

        while page.locator(".marker-cluster").count() > 0:
            page.locator(".marker-cluster").first.click()
            page.wait_for_timeout(500)

        page.screenshot(path="map_unclustered.png")

        markers = page.locator(".leaflet-interactive").all()
        print(f"Found {len(markers)} interactive markers")

        if markers:
            markers[0].click()
            page.wait_for_timeout(500)
            page.screenshot(path="map_popup.png")

        browser.close()

if __name__ == "__main__":
    test_map_interaction()
