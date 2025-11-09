from typing import Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object for the Indee Demo Login Page.
    Handles login actions and brand selection after sign-in.
    Inherits common utilities (click, send_keys, waits, logging) from BasePage.
    """
    # URL for the application
    URL: str = "https://indeedemo-fyc.watch.indee.tv/"

    # Elements
    PIN_FIELD: Tuple[str, str] = (By.XPATH, "//input[@placeholder='Enter your PIN here']")
    SIGN_IN_BTN: Tuple[str, str] = (By.XPATH, "//button[@id='sign-in-button']")

    # Brand selection tiles
    DEFAULT_BRAND_CARD: Tuple[str, str] = (By.XPATH, "//button[@aria-label='All Titles']")
    INDEE_BRAND_CARD: Tuple[str, str] = (By.XPATH, "//button[@aria-label='indee brand2']")

    def __init__(self, driver: WebDriver):
        """
        Initialize the LoginPage class with the WebDriver instance.
        The logger is inherited from BasePage.
        :param driver: WebDriver instance (Chrome, Edge, etc.)
        """
        super().__init__(driver)  # logger already initialized in BasePage

    def open(self) -> None:
        """
        Opens the Indee Demo login page and maximizes the browser window.
        """
        try:
            self.driver.get(self.URL)
            self.driver.maximize_window()
            self.logger.info(f"Opened login page: {self.URL}")
            self.accept_cookies()
        except Exception as e:
            self.logger.error(f"Failed to open login page: {e}")

    def verify_signin_page_displayed(self) -> bool:
        """
        Verifies that the Sign-In page is displayed.
        Waits for presence of PIN input or Sign-In button.
        :return: True if displayed, False otherwise.
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.any_of(
                    EC.visibility_of_element_located(self.PIN_FIELD),
                    EC.visibility_of_element_located(self.SIGN_IN_BTN)
                )
            )
            self.logger.info("✅ Sign-In page is displayed successfully.")
            return True
        except Exception as e:
            self.logger.error(f"❌ Sign-In page not visible: {e}")
            return False

    def sign_in(self, pin: str, brand_name: str = "default") -> None:
        """
        Enters PIN and performs sign-in.
        Optionally selects a brand if the brand page appears.
        :param pin: The login PIN.
        :param brand_name: Brand to select ('default' or 'indee').
        """
        try:
            # Step 1: Enter PIN and click Sign-In
            self.send_keys(self.PIN_FIELD, pin)
            self.click(self.SIGN_IN_BTN)
            self.logger.info("PIN entered and Sign-In button clicked.")

            # Step 2: Brand selection logic
            brand_name = brand_name.strip().lower()
            if brand_name == "default":
                locator = self.DEFAULT_BRAND_CARD
            elif brand_name == "indee":
                locator = self.INDEE_BRAND_CARD
            else:
                raise ValueError(f"Unknown brand name: {brand_name}. Use 'default' or 'indee'.")

            # Step 3: Wait for brand card and click it
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(locator)
            ).click()

            self.logger.info(f"✅ Brand '{brand_name}' selected successfully.")

        except Exception as e:
            self.logger.error(f"❌ Sign-in or brand selection failed: {e}")
