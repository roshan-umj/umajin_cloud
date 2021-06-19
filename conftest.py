from pathlib import Path

import pytest
import json
import allure
import os

import selenium.common.exceptions as selenium_exceptions
from selenium import webdriver
from utilities import config_reader
from utilities import urls
import utilities.logger
from allure_commons.types import AttachmentType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

logger = utilities.logger.Logger(logger_name="test setup")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep

# if environment variable is set up for browsers (eg: in jenkins) use that.
#      otherwise, use browser settings from conf.ini:

@pytest.fixture(params=str(os.getenv("Browsers")).strip().split(",") if os.getenv("Browsers") else config_reader.read(section="settings", key="browsers").strip().split(","), scope="class")
def get_browser(request):
    # if environment variable is set up for selenium grid ip and port (eg: in jenkins) use that.
    #      otherwise, use browser settings from conf.ini:
    if os.getenv('Selenium_grid'):
        selenium_grid_hub_ip_and_port = os.getenv('Selenium_grid')
    else:
        selenium_grid_hub_ip_and_port = config_reader.read(section="settings", key="selenium_grid_hub_ip_and_port")
    remote_url = f"http://{selenium_grid_hub_ip_and_port}/wd/hub"
    if request.param == "chrome":
        try:
            capabilities = DesiredCapabilities.CHROME
            driver = webdriver.Remote(
                command_executor=remote_url,
                desired_capabilities=capabilities
            )
        except:
            logger.error(f"{request.param} browser cloud not be initialized."
                         f" Please make sure selenium grid/ local browser drivers are configured correctly")
    elif request.param == "firefox":
        try:
            capabilities = DesiredCapabilities.FIREFOX
            driver = webdriver.Remote(
                command_executor=remote_url,
                desired_capabilities=capabilities
            )
        except:
            logger.error(f"{request.param} browser cloud not be initialized."
                         f" Please make sure selenium grid/ local browser drivers are configured correctly")
    elif request.param == "edge":
        try:
            capabilities = DesiredCapabilities.EDGE
            driver = webdriver.Remote(
                command_executor=remote_url,
                desired_capabilities=capabilities
            )
        except:
            logger.error(f"{request.param} browser cloud not be initialized."
                         f" Please make sure selenium grid/ local browser drivers are configured correctly")

    elif request.param == "safari":
        try:
            capabilities = DesiredCapabilities.SAFARI
            driver = webdriver.Remote(
                command_executor=remote_url,
                desired_capabilities=capabilities
            )
        except:
            logger.error(f"{request.param} browser cloud not be initialized."
                         f" Please make sure selenium grid/ local browser drivers are configured correctly")

    try:
        logger.info(driver, f"initializing {driver.name}")
        request.cls.driver = driver
        # getting the url in advance to set a cookie to bypass the login
        driver.get(urls.base_url)

        # setting a cookie to bypass login - get from env. variables if it's set. otherwise get from conf.ini
        if os.getenv("Server"):
            if os.getenv("Server") == "test":
                cookie_json = config_reader.read(section="settings", key="cookie_test")
            else:
                cookie_json = config_reader.read(section="settings", key="cookie_live")
        else:
            config_settings_server = config_reader.read(section="settings", key="server").lower()
            if config_settings_server == "test":
                cookie_json = config_reader.read(section="settings", key="cookie_test")
            else:
                cookie_json = config_reader.read(section="settings", key="cookie_live")

        driver.add_cookie(json.loads(cookie_json))
        logger.info(driver, f"cookie has been set to bypass login")



        yield driver
        driver.quit()
        logger.info(driver, f"{driver.name} closed")

    except UnboundLocalError:
        logger.exception(f"Failed to initialize browser instance: '{request.param}'. Please check the configurations.")
    except selenium_exceptions.UnableToSetCookieException:
        logger.error(f"Failed to set cookie on {driver.name}")


@pytest.fixture()
def add_logs_on_failure(request, get_browser):
    yield
    item = request.node
    driver = get_browser
    if item.rep_call.failed:
        allure.attach(driver.get_screenshot_as_png(), name="failure_screenshot", attachment_type=AttachmentType.PNG)


@pytest.fixture(scope="session")
def setup_on_session_start(request):

    # create a  brand new log file for each session:
    log_file_name = config_reader.read(section="settings", key="log_file_name")
    with open(file=f"logs/{log_file_name}", mode="w"):
        pass


@pytest.fixture(scope="function")
def change_test_dir(request):
    os.chdir(request.fspath.dirname)
    yield
    os.chdir(request.config.invocation_dir)
