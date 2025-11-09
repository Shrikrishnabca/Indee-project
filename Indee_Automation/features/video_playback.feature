Feature: Automate Indee video platform

  Scenario: Automate video playback and controls
    Given I open the Indee video platform
    When I log in using the provided PIN
    And I navigate to "Test Automation Project"
    And I switch to the "Details" tab
    And I return to the "Videos" tab
    And I play the video for 10 seconds and pause it
    And I replay the video using the "Continue Watching" button
    And I set the video volume to 50 percent
    And I change the video resolution to 480p and back to 720p
    And I pause the video and exit to the main screen
    Then I log out successfully
