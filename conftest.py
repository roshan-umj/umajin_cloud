from pathlib import Path

import pytest

from selenium import webdriver

from utilities import config_reader
from webdriver_manager.chrome import ChromeDriverManager
from allure_commons.types import AttachmentType
import allure
import utilities.logger
import os
import shutil
from webdriver_manager.firefox import GeckoDriverManager

logger = utilities.logger.Logger(logger_name="test setup")


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
    logger.info(f"initializing {driver.name}")
    request.cls.driver = driver
    driver.get(config_reader.read(section='basic_information', key='cloud_url'))
    yield driver
    driver.quit()
    logger.info(f"{driver.name} closed")


@pytest.fixture()
def add_logs_on_failure(request, get_browser):
    yield
    item = request.node
    driver = get_browser
    if item.rep_call.failed:
        allure.attach(driver.get_screenshot_as_png(), name="dologin", attachment_type=AttachmentType.PNG)


@pytest.fixture(scope="session")
def setup_on_session_start(request):

    # create a  brand new log file for each session:
    with open(file=config_reader.read(section="settings", key="log_file_name"), mode="w"):
        pass

    # clear reports folder at the beginning of each session:
    report_dir_path = config_reader.read("settings", "report_files_folder")
    try:
        shutil.rmtree(report_dir_path)
    except:
        logger.error("could not clear the report files folder")
    os.makedirs(report_dir_path)


@pytest.fixture(scope="function")
def change_test_dir(request):
    os.chdir(request.fspath.dirname)
    yield
    os.chdir(request.config.invocation_dir)
    # test
