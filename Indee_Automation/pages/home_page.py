import time
from typing import Tuple

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage


class HomePage(BasePage):
    """
    Page Object Model class for the Indee Demo Home Page.
    Handles verification of page load and navigation to specific projects.
    Inherits utility methods and logger from BasePage.
    """
    # Elements
    ALL_TILES_HEADER: Tuple[str, str] = (By.XPATH, "//*[text()=' All Titles ']")
    TEST_AUTOMATION_PROJECT: Tuple[str, str] = (By.XPATH, "//*[text()='Test automation project']")

    def __init__(self, driver: WebDriver):
        """
        Initialize the HomePage with WebDriver instance.
        Logger is inherited from BasePage.
        :param driver: WebDriver instance (e.g., Chrome, Edge)
        """
        super().__init__(driver)

    def verify_home_page_loaded(self) -> bool:
        """
        Verify that the Home page is loaded successfully.
        Waits for the 'All Titles' header or home page element to be visible.
        :return: True if page loaded successfully, False otherwise.
        """
        try:
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.ALL_TILES_HEADER)
            )
            self.logger.info("✅ Home page loaded successfully.")
            return True
        except Exception as e:
            self.logger.error(f"❌ Home page did not load correctly: {e}")
            return False

    def open_project(self) -> None:
        """
        Opens a specific project from the Home page by its visible name.
        """
        try:
            # Ensure home page is ready before proceeding
            if not self.verify_home_page_loaded():
                raise Exception("Home page not ready. Cannot select project.")

            locator: Tuple[str, str] = (By.XPATH, "//*[@aria-label='Title - Test automation project, ']")

            # Wait for the project tile and click it
            element = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(locator)
            )

            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            time.sleep(0.3)  # 300ms pause to ensure scroll completes

            # Hover over the element
            ActionChains(self.driver).move_to_element(element).perform()
            time.sleep(0.1)  # tiny pause after hover
            self.logger.info(f"Hovered over project tile:")

            element.click()

            self.logger.info(f"✅ Opened project")

            # Optional: Wait until project navigation completes
            WebDriverWait(self.driver, 10).until_not(
                EC.presence_of_element_located(locator)
            )
            self.logger.info("ℹ️ Navigated to the project details page successfully.")

        except Exception as e:
            self.logger.error(f"❌ Failed to open Test automation project: {e}")
