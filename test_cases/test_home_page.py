import allure
import pytest
import random
import utilities.test_cases as test_cases
from pages.umajin_website_home_page import HomePage
from pages.user_login_page import Login
from test_cases.base_test import BaseTest


@pytest.fixture(scope="class")
def navigate_to_project_list(request):
    login_page = Login(request.cls.driver)
    login_page.click("btn_sign_up")


@pytest.mark.usefixtures("navigate_to_project_list")
class Test_HomePage(BaseTest):

    @allure.story(test_cases.get_test_case("test_sign_up").story)
    @allure.title(test_cases.get_test_case("test_sign_up").display_name)
    @allure.severity(test_cases.get_test_case("test_sign_up").severity)
    def test_sign_up(self):
        home_page = HomePage(self.driver)

        country_list = home_page.get_options_list_from_select("sel_signup_country")
        random_country = random.choice(country_list[1:])

        industry_list = home_page.get_options_list_from_select("sel_signup_industry")
        random_industry = random.choice(industry_list[1:])

        home_page.sign_up(first_name="Umajin",
                          last_name="Test User",
                          email="umajinnz@gmail.com",
                          company="Umajin",
                          country=random_country,
                          industry=random_industry)
