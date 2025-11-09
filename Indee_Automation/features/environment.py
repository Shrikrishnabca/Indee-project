from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def before_all(context):
    """Runs once before the entire test suite."""
    # chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})

    # Initialize browser instance
    service = Service("./drivers/chromedriver.exe")
    context.driver = webdriver.Chrome(service=service, options=chrome_options)
    context.driver.maximize_window()
    context.driver.implicitly_wait(10)
    print("\n🚀 Browser launched successfully")

def before_scenario(context, scenario):
    """Runs before each scenario."""
    print(f"\n🎯 Starting Scenario: {scenario.name}")

def after_scenario(context, scenario):
    """Runs after each scenario."""
    if scenario.status == "failed":
        # Optional: Take screenshot on failure
        context.driver.save_screenshot(f"screenshots/{scenario.name}.png")
        print(f"❌ Scenario failed: {scenario.name}")
    else:
        print(f"✅ Scenario passed: {scenario.name}")

def after_all(context):
    """Runs once after all tests are done."""
    context.driver.quit()
    print("\n🧹 Browser closed. Test run complete.")
