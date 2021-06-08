from pathlib import Path

import pytest

from selenium import webdriver

from utilities import config_reader
from webdriver_manager.chrome import ChromeDriverManager
from allure_commons.types import AttachmentType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
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


@pytest.fixture(params=["firefox", "chrome", "safari"], scope="class")
def get_browser(request):
    selenium_grid_hub_ip_and_port = config_reader.read(section="settings", key="selenium_grid_hub_ip_and_port")
    remote_url = f"http://{selenium_grid_hub_ip_and_port}/wd/hub"
    if request.param == "chrome":
        # uncomment/comment the following lines to switch between local execution and selenium grid
        # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        driver = webdriver.Remote(
            command_executor=remote_url,
            desired_capabilities=DesiredCapabilities.CHROME
        )
    elif request.param == "firefox":
        # uncomment/comment the following lines to switch between local execution and selenium grid
        # driver = webdriver.Firefox(executable_path="c:/selenium_browser_drivers/geckodriver.exe")
        driver = webdriver.Remote(
            command_executor=remote_url,
            desired_capabilities=DesiredCapabilities.FIREFOX
        )
    elif request.param == "edge":
        # uncomment/comment the following lines to switch between local execution and selenium grid
        # driver = webdriver.Edge(executable_path="c:/selenium_browser_drivers/edgedriver.exe")
        caps = DesiredCapabilities.EDGE
        driver = webdriver.Remote(
            command_executor=remote_url,
            desired_capabilities=caps
        )
    elif request.param == "safari":
        caps = DesiredCapabilities.SAFARI
        driver = webdriver.Remote(
            command_executor=remote_url,
            desired_capabilities=caps
        )
    logger.info(driver, f"initializing {driver.name}")
    request.cls.driver = driver

    # getting the url in advance to set a cookie to bypass the login
    driver.get(config_reader.read(section='basic_information', key='cloud_url'))
    driver.add_cookie({"name": "token", "domain": ".umajin.com", "value": "edad609473489327d8fb0b0f55903b5b"})
    logger.info(driver, f"cookie has been set to bypass login")

    yield driver
    driver.quit()
    logger.info(driver, f"{driver.name} closed")


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
    log_file_name = config_reader.read(section="settings", key="log_file_name")
    with open(file=f"logs/{log_file_name}", mode="w"):
        pass

    # DISABLED FOR NOW - doesn't support parallel testing. ------clear reports folder at the beginning of each session:
    # report_dir_path = config_reader.read("settings", "report_files_folder")
    # try:
    #     shutil.rmtree(report_dir_path)
    # except:
    #     logger.error("could not clear the report files folder")
    # os.makedirs(report_dir_path)


    yield
    allure.attach.file("data_sheets/test_coverage.xlsx", name="test_coverage_details.xlsx", extension="xlsx")


@pytest.fixture(scope="function")
def change_test_dir(request):
    os.chdir(request.fspath.dirname)
    yield
    os.chdir(request.config.invocation_dir)
