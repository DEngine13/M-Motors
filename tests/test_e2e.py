import pytest
from playwright.sync_api import Page, expect

# Fixture to facilitate test writing
@pytest.fixture(scope="session")
def live_server_url():
    return "http://127.0.0.1:8000"


class TestE2EVisitorJourney:
    """Test the complete visitor journey"""

    # Testing if the catalog loads
    def test_catalog_loads(self, page: Page, live_server_url):
        page.goto(live_server_url)
        expect(page.locator("h1")).to_contain_text("Catalog")

    # Testing if the filters on the catalog work (filter: type == "sale" as example)
    def test_filter_vehicles(self, page: Page, live_server_url):
        page.goto(live_server_url)
        page.select_option("select[name='type']", "sale")
        page.click("button:has-text('Filter')")
        expect(page.get_by_text("vehicle(s) found")).to_be_visible

    # Testing if the vehicle details page is visible
    def test_view_vehicle_detail(self, page: Page, live_server_url):
        page.goto(live_server_url)
        page.click(".card >> nth=0")
        expect(page.locator("table")).to_be_visible()

    # Testing the entire signing up flow: get tot the sign up page, create the user and get redirected to the catalog page
    def test_signup_flow(self, page: Page, live_server_url):
        # Using time to create unique usernames based on the timestamp
        import time
        username = f"teste2e_{int(time.time())}"
        page.goto(f"{live_server_url}/account/signup/")
        page.fill("input[name='first_name']", "Test")
        page.fill("input[name='last_name']", "E2E")
        page.fill("input[name='username']", username)
        page.fill("input[name='email']", f"{username}@test.com")
        page.fill("input[name='phone']", "06 00 00 00 00")
        page.fill("textarea[name='address']", "1 rue du Test")
        page.fill("input[name='password1']", "SecureE2E2026!")
        page.fill("input[name='password2']", "SecureE2E2026!")
        page.click("button[type='submit']")
        page.wait_for_url("**/", timeout=5000)
        expect(page.locator("h1")).to_contain_text("Catalog")