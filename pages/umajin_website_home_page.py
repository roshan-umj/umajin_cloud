from pages.common_imports import *

log = Logger(__name__)


class HomePage(UmajinCloudBase):
    def __init__(self, driver):
        super().__init__(driver=driver)
        self.driver = driver

    def sign_up (self, first_name: str, last_name: str, email: str, company: str, country: str, industry: str):
        """inserts user details into the sign up form and clicks the signup button

        :param first_name: first name of the user
        :param last_name: last name of the user
        :param email: email address
        :param company: name of the company
        :param country: name of the country. this should match to one of the items from the 'country' dropdown
        :param industry: name of the industry. this should match to one of the items from the 'industry' dropdown

        """
        self.send_keys(locator="txt_signup_firstname", value=first_name)
        self.send_keys(locator="txt_signup_lastname", value=last_name)
        self.send_keys(locator="txt_signup_email", value=email)
        self.send_keys(locator="txt_signup_company", value=company)
        self.send_keys(locator="sel_signup_country", value=country)
        self.send_keys(locator="sel_signup_industry", value=industry)
        self.click(locator="btn_signup_submit")

        log.info(self.driver, f"sign up the user: {first_name} {last_name}")

