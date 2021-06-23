from pages.common_imports import *
import pages.project_list as project_list
import pages.reset_password_page as reset_password_page
import pages.umajin_website_home_page as home_page

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

    def open_reset_password_page(self):
        """clicks on Forgot Password and open Forgot Password page

        :return: ForgotPassword page object
        """
        self.click(locator="btn_forgot_password")
        return reset_password_page.ResetPassword(self.driver)

    def open_sign_up_page(self):
        """clicks on Sign up and open Sign up page

        :return: HomePage object
        """
        self.click("btn_sign_up")
        return home_page.HomePage(self.driver)
