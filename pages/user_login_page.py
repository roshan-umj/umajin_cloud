from pages.common_imports import *
import pages.project_list as project_list
import pages.forgot_password_page as forgot_password_page

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
        log.info(self.driver, "go to login page")
        # the locator should be available under the given section in configuration_data/config.ini
        self.send_keys(locator="txt_username", value=username)
        self.send_keys(locator="txt_password", value=password)
        self.click(locator="btn_sign_in")
        log.info(self.driver, f"attempt to sign in. username: {username} password: {password}")
        return project_list.ProjectList(driver=self.driver)

    def go_to_forgot_password_page(self):
        self.click(locator="btn_forgot_password")
        return forgot_password_page.ForgotPassword(self.driver)

