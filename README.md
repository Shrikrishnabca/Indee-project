Automated end-to-end testing framework for Indee’s video player web application.
This framework is built using Python, Selenium WebDriver, and BDD (Behave) for clear, human-readable test scenarios.

Features

✅ Page Object Model (POM) based structure

✅ BDD Framework (Behave) integration

✅ Handles iframes, hover actions, and JS execution

✅ Automates video interactions:

Play / Pause / Replay

Volume Adjustment

Resolution Change

Time-based pause at 10 sec

✅ Includes robust logging and exception handling

✅ Supports cross-browser execution


Project Structure

Indee_Automation/
├── features/
│   ├── video_playback.feature      # BDD Scenarios
│   └── steps/
│       └── video_steps.py          # Step Definitions
│
├── pages/
│   └── video_page.py               # Page Object for Video Page
│
├── tests/
│   └── conftest.py                 # Pytest Fixtures (if used)
│
├── drivers/
│   └── chromedriver.exe            # Browser driver (keep version matched)
│
├── logs/
│   └── test_run.log                # Execution logs
│
├── behave.ini                      # Behave configuration
├── requirements.txt                # Dependencies
└── README.md                       # Project documentation


⚙️ Installation

Clone the repository

git clone https://github.com/<your-username>/Indee_Automation.git
cd Indee_Automation


Create a virtual environment

python -m venv venv
source venv/Scripts/activate     # For Windows
# or
source venv/bin/activate         # For macOS/Linux
