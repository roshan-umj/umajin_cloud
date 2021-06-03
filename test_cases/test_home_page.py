import time

import allure
import pytest
import random

from pages.umajin_website_home_page import HomePage
from pages.user_login_page import Login
from pages.project_list import ProjectList
from test_cases.base_test import BaseTest


@pytest.fixture(scope="class")
def navigate_to_project_list(request):
    login_page = Login(request.cls.driver)
    login_page.click("btn_sign_up")


@pytest.mark.usefixtures("navigate_to_project_list")
class Test_HomePage(BaseTest):

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Cloud Login Test")
    def test_sign_up(self):
        home_page = HomePage(self.driver)

        country_list = home_page.get_options_list_from_select("sel_signup_country")
        random_country = random.choice(country_list[1:])

        industry_list = home_page.get_options_list_from_select("sel_signup_industry")
        random_industry = random.choice(country_list[1:])


        home_page.sign_up(first_name="Umajin",
                          last_name="Test User",
                          email="umajinnz@gmail.com",
                          company="Umajin",
                          country=random_country,
                          industry=random_industry)
        time.sleep(10)

    def test_sign_out(self):
        project_list = ProjectList(self.driver)
        project_list.sign_out()
