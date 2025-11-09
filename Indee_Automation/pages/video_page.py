import time
from typing import Tuple
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage


class VideoPage(BasePage):
    """
    Page Object Model for the Indee Demo Video Page.
    Handles all interactions related to video playback, volume control,
    resolution change, tab switching, and logout.
    """
    # Element
    PROJECT_TITLE: Tuple[str, str] = (By.XPATH, "//*[text()='Test automation project']")
    DETAILS_TAB: Tuple[str, str] = (By.XPATH, "//a[@id='detailsSection']")
    VIDEOS_TAB: Tuple[str, str] = (By.XPATH, "//a[@id='videosSection']")
    PLAY_BTN: Tuple[str, str] = (By.XPATH, "//button[@aria-label='Play Video']")
    PAUSE_BTN: Tuple[str, str] = (By.XPATH, "//div[@class='jw-reset jw-button-container']/div[@aria-label='Pause']")
    REPLAY_BUTTON: Tuple[str, str] = (By.XPATH, "//div[@class='jw-reset jw-button-container']/div[@aria-label='Play']")
    SETTINGS_BTN: Tuple[str, str] = (By.XPATH, "//*[@aria-label='Settings' and @role='button']")
    VOLUME_ICON: Tuple[str, str] = (By.XPATH, "//div[@aria-label='Mute button']")
    VOLUME_SLIDER: Tuple[str, str] = (By.XPATH, "//*[@class='jw-horizontal-volume-container']")
    LOGOUT_ICON: Tuple[str, str] = (By.XPATH, "//button[@id='signOutSideBar']")

    def __init__(self, driver: WebDriver):
        """
        Initialize VideoPage with WebDriver. Logger is inherited from BasePage.
        :param driver: WebDriver instance (Chrome, Edge, etc.)
        """
        super().__init__(driver)

    def verify_video_page_loaded(self) -> bool:
        """
        Verify that the video project page is loaded successfully.
        Waits for DOM ready state and key elements on the page.
        :return: True if loaded, False otherwise.
        """
        try:
            WebDriverWait(self.driver, 15).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            self.logger.info("✅ DOM is fully loaded.")

            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.DETAILS_TAB)
            )
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.VIDEOS_TAB)
            )
            self.logger.info("✅ Video project page loaded successfully.")
            return True

        except Exception as e:
            self.logger.error(f"❌ Video project page did not load correctly: {e}")
            return False

    def switch_to_details_tab(self) -> None:
        """Switch to the 'Details' tab on the video page."""
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.DETAILS_TAB)
            )

            # Scroll element into view (centered)
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            time.sleep(0.3)  # allow UI to repaint

            # Hover over the tab
            ActionChains(self.driver).move_to_element(element).perform()
            time.sleep(0.1)  # wait for any hover effects

            element.click()
            self.logger.info("✅ Switched to Details tab.")
            time.sleep(2)
        except Exception as e:
            self.logger.error(f"❌ Failed to switch to details tab: {e}")

    def switch_to_videos_tab(self) -> None:
        """Switch to the 'Videos' tab on the video page."""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.VIDEOS_TAB)
            ).click()
            self.logger.info("✅ Switched to Videos tab.")
        except Exception as e:
            self.logger.error(f"❌ Failed to switch to videos tab: {e}")

    def play_video(self) -> None:
        """Play the selected video."""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.PLAY_BTN)
            ).click()
            self.logger.info("▶️ Video started playing.")
            time.sleep(5)
        except Exception as e:
            self.logger.error(f"❌ Failed to play video: {e}")

    def pause_video_after_10_sec(self) -> None:
        """Play the video and pause it once elapsed time reaches max_seconds (default 10)."""
        try:
            # Switch to iframe where video is playing
            iframe = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "video_player"))
            )
            self.driver.switch_to.frame(iframe)
            self.logger.info("✅ Switched to iframe 'video_player'")

            # Wait for the video to start (elapsed time visible)
            elapsed_locator = (By.XPATH, "//*[contains(@class, 'jw-text-elapsed')]")
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(elapsed_locator)
            )

            # Poll until time exceeds 10 seconds
            start_time = time.time()
            while True:
                elapsed_text = self.driver.find_element(*elapsed_locator).text.strip()  # e.g., '0:11'
                if ":" in elapsed_text:
                    mins, secs = elapsed_text.split(":")
                    elapsed_sec = int(mins) * 60 + int(secs)
                else:
                    elapsed_sec = int(elapsed_text) if elapsed_text.isdigit() else 0

                if elapsed_sec >= 10:
                    self.logger.info(f"⏱️ Video reached {elapsed_sec} sec, attempting to pause.")
                    break

                # Safety: if more than 30 sec passed in real-time, break
                if time.time() - start_time > 30:
                    self.logger.warning("⏳ Timeout waiting for 10 seconds playback.")
                    break

                time.sleep(0.5)

            # Locate and click Pause button
            pause_btn = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(self.PAUSE_BTN)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pause_btn)
            ActionChains(self.driver).move_to_element(pause_btn).pause(0.3).click().perform()

            self.logger.info("⏸️ Video paused successfully.")

            # Switch back to main content
            self.driver.switch_to.default_content()
            self.logger.info("🔙 Switched back to main page from iframe.")

            time.sleep(2)

        except Exception as e:
            self.logger.error(f"❌ Failed to pause video: {e}")
            # Always switch back even on failure
            try:
                self.driver.switch_to.default_content()
            except:
                pass
            raise

    def pause_video(self) -> None:
        """Pause the currently playing video."""
        try:
            # --- Switch to the iframe ---
            iframe = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "video_player"))
            )
            self.driver.switch_to.frame(iframe)
            self.logger.info("Switched to video iframe 'video_player'")

            # --- Wait for the pause button inside iframe ---
            element = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.PAUSE_BTN)
            )

            # --- Hover over the element ---
            ActionChains(self.driver).move_to_element(element).perform()
            time.sleep(0.2)

            # --- Click using JS (more reliable for video controls) ---
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.info("⏸️ Video paused successfully inside iframe")
            time.sleep(2)  # optional wait for video state to stabilize

            # --- Switch back to main content ---
            self.driver.switch_to.default_content()
            self.logger.info("Switched back to main page")

        except Exception as e:
            self.logger.error(f"❌ Failed to pause video inside iframe: {e}")
            raise

    def replay_video(self) -> None:
        """Replay or continue the paused video."""
        try:
            # Step 1: Switch to iframe
            iframe = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "video_player"))
            )
            self.driver.switch_to.frame(iframe)
            self.logger.info("✅ Switched to iframe 'video_player' for replay")

            # Step 2: Wait for replay/continue button to appear
            element = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(self.REPLAY_BUTTON)
            )

            # Step 3: Scroll into view and hover before click
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            ActionChains(self.driver).move_to_element(element).pause(0.3).click().perform()
            self.logger.info("🔁 Clicked on 'Continue Watching' / Replay button.")

            # Step 4: Wait to confirm video has started playing again
            try:
                elapsed_locator = (By.XPATH, "//*[contains(@class, 'jw-text-elapsed')]")
                start_time = self.driver.find_element(*elapsed_locator).text.strip()
                time.sleep(3)
                new_time = self.driver.find_element(*elapsed_locator).text.strip()

                if start_time != new_time:
                    self.logger.info("▶️ Video successfully replayed and playing.")
                else:
                    self.logger.warning("⚠️ Replay clicked, but playback not detected.")
            except Exception:
                self.logger.warning("ℹ️ Could not verify playback progress (elapsed time not found).")

            # Step 5: Switch back to main content
            self.driver.switch_to.default_content()
            self.logger.info("🔙 Switched back to main page from iframe after replay.")

        except Exception as e:
            self.logger.error(f"❌ Failed to replay video: {e}")
            try:
                self.driver.switch_to.default_content()
            except:
                pass

    def adjust_volume(self, level: int = 50) -> None:
        """
        Adjust video volume directly using JavaScript inside iframe 'video_player'.
        :param level: Volume percentage (0–100)
        """
        try:
            # Step 1: Switch to iframe
            iframe = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "video_player"))
            )
            self.driver.switch_to.frame(iframe)
            self.logger.info("✅ Switched to iframe 'video_player'.")

            # Step 2: Ensure JW Player container or <video> is present
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "video"))
            )
            self.logger.info("🎬 Video element located successfully inside iframe.")

            # Step 3: Adjust volume directly via JS (most reliable)
            js_script = f"""
            const vid = document.querySelector('video');
            if (vid) {{
                vid.volume = {level / 100};
                return vid.volume * 100;
            }} else {{
                return -1;
            }}
            """
            actual_volume = self.driver.execute_script(js_script)

            if actual_volume >= 0:
                self.logger.info(f"🔊 Volume successfully set to {actual_volume:.0f}%")
            else:
                self.logger.warning("⚠️ Video element not found in DOM, could not adjust volume.")

            time.sleep(1)

        except Exception as e:
            self.logger.error(f"❌ Failed to adjust volume: {e}")

        finally:
            try:
                self.driver.switch_to.default_content()
                self.logger.info("🔙 Switched back to main page from iframe.")
            except Exception:
                pass

    def change_resolution(self, resolution: str = "720p") -> None:
        """
        Change video resolution using JW Player settings safely.
        :param resolution: Desired quality (e.g., '1080p', '720p', '480p')
        """
        try:
            # Step 1: Switch to iframe where player is loaded
            iframe = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "video_player"))
            )
            self.driver.switch_to.frame(iframe)
            self.logger.info("✅ Switched to iframe 'video_player'.")

            # Step 2: Hover over and click settings icon (gear icon)
            settings_icon = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(self.SETTINGS_BTN)
            )
            ActionChains(self.driver).move_to_element(settings_icon).pause(0.3).click().perform()
            self.logger.info("⚙️ Opened JW Player settings menu.")

            # Step 3: Wait for quality options to appear
            quality_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//button[normalize-space(text())='{resolution}']")
                )
            )

            # Step 4: Scroll into view and click desired resolution
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", quality_option)
            ActionChains(self.driver).move_to_element(quality_option).pause(0.2).click().perform()
            self.logger.info(f"✅ Resolution changed successfully to {resolution}.")

            # Step 5: Optional — click outside to close settings
            ActionChains(self.driver).move_by_offset(50, 0).click().perform()
            self.logger.info("✅ Closed settings menu after resolution change.")

            # Step 6: Switch back to main page
            self.driver.switch_to.default_content()
            self.logger.info("🔙 Switched back to main page from iframe.")

        except Exception as e:
            self.logger.error(f"❌ Failed to change resolution: {e}")
            try:
                self.driver.switch_to.default_content()
            except:
                pass
            raise

    def pause_and_exit(self) -> None:
        """Pause the video and navigate back to the previous screen."""
        try:
            self.pause_video()
            self.logger.info("⏸️ Video paused using pause_video().")

            time.sleep(1)
            self.driver.back()
            self.logger.info("🔙 Navigated back to the previous screen using driver.back().")

        except Exception as e:
            self.logger.error(f"❌ Failed to pause and exit video: {e}")

    def logout(self) -> None:
        """
        Clicks the Sign Out icon (sidebar logout) with hover and verifies redirection to login screen.
        """
        try:
            # Wait for the logout <a> container to appear
            logout_container = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "signOutSideBar"))
            )
            self.logger.info("👀 Logout sidebar icon located.")

            # Hover over the logout area
            ActionChains(self.driver).move_to_element(logout_container).pause(0.4).perform()
            self.logger.info("🖱️ Hovered over the Sign Out area.")

            # Now target the actual <button> inside the container
            logout_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#signOutSideBar button"))
            )

            # Click using JavaScript (more reliable for sidebar buttons)
            self.driver.execute_script("arguments[0].click();", logout_button)
            self.logger.info("🚪 Clicked on the Sign Out icon (Logout).")

            # Wait for redirection to login page
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//input[@placeholder='Enter your PIN here']")
                )
            )
            self.logger.info("✅ Logout successful — redirected to Login page.")

        except Exception as e:
            self.logger.error(f"❌ Logout failed: {e}")
            raise
