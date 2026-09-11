from playwright.sync_api import sync_playwright

def check_map():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        console_logs = []
        page_errors = []

        page.on("console", lambda msg: console_logs.append(f"{msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: page_errors.append(str(err)))

        print("Navigating to /map...")
        page.goto("http://localhost:5000/map")
        page.wait_for_timeout(2000)

        print("--- Console logs on /map ---")
        for log in console_logs:
            print(log)

        print("--- Page errors on /map ---")
        for err in page_errors:
            print(err)

        browser.close()

if __name__ == "__main__":
    check_map()
