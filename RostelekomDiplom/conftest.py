import os
import time
from datetime import datetime
import allure
import pytest
from selenium import webdriver as selenium_wd
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://b2c.passport.rt.ru/auth"


@pytest.fixture(scope="session")
def web_driver(request, base_url=BASE_URL):
    s = Service(executable_path=ChromeDriverManager().install())
    chrome_options = Options()
    driver = selenium_wd.Chrome(service=s, options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(5)

    driver.get(base_url)

    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="function", autouse=True)
def test_failed_check(request, web_driver):
    yield
    if request.node.rep_setup.outcome == 'failed':
        print("Test installation failed:", request.node.nodeid)
        allure.attach(web_driver.get_screenshot_as_png(), name="Screenshot_pass",
                      attachment_type=allure.attachment_type.PNG)
    elif request.node.rep_setup.outcome == 'passed':
        if request.node.rep_call.failed:
            allure.attach(web_driver.get_screenshot_as_png(), name="Screenshot_fail",
                          attachment_type=allure.attachment_type.PNG)
            print("Test execution failed:", request.node.nodeid)
