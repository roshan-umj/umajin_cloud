from pages.umajin_cloud_base_page import UmajinCloudBase
from pages.project_list import ProjectList
import logging
from utilities.logger import Logger

log = Logger(__name__)

class Login(UmajinCloudBase):
    def __init__(self, driver):
        super().__init__(driver=driver)
        self.driver = driver

    def log_in(self, username: str, password: str):
        """inserts user credentials into the login form and clicks the login button

        :param username: username or email address
        :param password: password
        """
        log.info("go to login page")
        # the locator should be available under the given section in configuration_data/config.ini
        self.send_keys(locator="txt_username", value=username)
        self.send_keys(locator="txt_password", value=password)
        self.click(locator="btn_sign_in")
        log.logger.info(f"attempt to sign in. username: {username} password: {password}")
        return ProjectList(driver=self.driver)



