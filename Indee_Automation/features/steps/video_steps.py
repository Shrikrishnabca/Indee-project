import time

from behave import given, when, then

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.video_page import VideoPage


@given("I open the Indee video platform")
def step_open(context):
    context.login_page = LoginPage(context.driver)
    context.home_page = HomePage(context.driver)
    context.video_page = VideoPage(context.driver)
    context.login_page.open()


@when("I log in using the provided PIN")
def step_login(context):
    context.login_page.sign_in("WVMVHWBS")


@when('I navigate to "Test Automation Project"')
def step_navigate_project(context):
    context.home_page.open_project()


@when('I switch to the "Details" tab')
def step_details(context):
    context.video_page.verify_video_page_loaded()
    context.video_page.switch_to_details_tab()


@when('I return to the "Videos" tab')
def step_videos(context):
    context.video_page.switch_to_videos_tab()


@when('I play the video for 10 seconds and pause it')
def step_play(context):
    context.video_page.play_video()
    context.video_page.pause_video_after_10_sec()

@when('I replay the video using the "Continue Watching" button')
def step_replay(context):
    context.video_page.replay_video()


@when('I set the video volume to 50 percent')
def step_volume(context):
    context.video_page.adjust_volume(level=50)


@when('I change the video resolution to 480p and back to 720p')
def step_resolution(context):
    context.video_page.change_resolution(resolution="480p")
    context.video_page.change_resolution(resolution="720p")


@when('I pause the video and exit to the main screen')
def step_exit(context):
    context.video_page.pause_and_exit()


@then("I log out successfully")
def step_logout(context):
    context.video_page.logout()
    time.sleep(5)
    assert context.login_page.verify_signin_page_displayed() == True
    context.driver.quit()

