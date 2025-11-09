import logging
from typing import Tuple

from selenium.common import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """
    BasePage acts as a parent class for all Page Object classes.
    It provides reusable utility methods such as click, send_keys, and waits,
    ensuring code reusability and cleaner test design.
    """

    def __init__(self, driver: WebDriver):
        """
        Initialize the BasePage with a WebDriver instance and configure a logger.
        :param driver: WebDriver instance used for browser interactions.
        """
        self.driver = driver

        # --- Logger Configuration ---
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)  # Default level

        # Prevent duplicate handlers
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                fmt="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.propagate = False  # Prevent messages from propagating to root logger

    def accept_cookies(self) -> None:
        """
        Handle 'Accept All Cookies' pop-up if present.
        """
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@aria-label='We value your privacy']//*[text()='Accept All']"))
            ).click()
            self.logger.info("Accepted cookies successfully")
        except TimeoutException:
            self.logger.info("No cookies pop-up found, continuing test")
        except Exception as e:
            self.logger.error(f"Error while accepting cookies: {e}")


    def click(self, locator: Tuple[str, str]) -> None:
        """
        Wait for an element to be clickable and perform a click action.
        :param locator: Tuple (By.<method>, "locator_string")
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(locator)
            ).click()
            self.logger.info(f"Clicked on element: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to click element {locator}: {e}")

    def send_keys(self, locator: Tuple[str, str], text: str) -> None:
        """
        Wait for an element to be visible and type text into it.
        :param locator: Tuple (By.<method>, "locator_string")
        :param text: The string to send to the input field
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(locator)
            ).send_keys(text)
            self.logger.info(f"Sent keys '{text}' to element: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to send keys to {locator}: {e}")

    def wait_for_element(self, locator: Tuple[str, str], timeout: int = 10) -> None:
        """
        Wait for an element to become visible on the page.
        :param locator: Tuple (By.<method>, "locator_string")
        :param timeout: Maximum wait time in seconds (default: 10)
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            self.logger.info(f"Element became visible: {locator}")
        except Exception as e:
            self.logger.error(f"Element not visible {locator} within {timeout}s: {e}")
