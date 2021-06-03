import pytest

from selenium import webdriver

from utilities import config_reader
from webdriver_manager.chrome import ChromeDriverManager
from allure_commons.types import AttachmentType
import allure
import os
from webdriver_manager.firefox import GeckoDriverManager

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture(params=["chrome"], scope="class")
def get_browser(request):
    if request.param == "chrome":
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    if request.param == "firefox":
        driver = webdriver.Firefox(executable_path="c:/selenium_browser_drivers/geckodriver.exe")
    request.cls.driver = driver
    driver.get(config_reader.read(section='basic_information', key='cloud_url'))
    yield driver
    driver.quit()


@pytest.fixture()
def add_logs_on_failure(request, get_browser):
    yield
    item = request.node
    driver = get_browser
    if item.rep_call.failed:
        allure.attach(driver.get_screenshot_as_png(), name="dologin", attachment_type=AttachmentType.PNG)

@pytest.fixture(scope="function")
def change_test_dir(request):
    os.chdir(request.fspath.dirname)
    yield
    os.chdir(request.config.invocation_dir)
    # test


