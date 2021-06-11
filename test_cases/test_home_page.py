from common_imports_for_tests import *
from pages.umajin_website_home_page import HomePage
import random

@pytest.fixture(scope="function")
def navigate_to_page_under_test(request):
    request.cls.driver.get(urls.home_page)

@pytest.mark.usefixtures("navigate_to_page_under_test")
class Test_HomePage(BaseTest):

    @allure.story(test_cases.get_test_case("test_sign_up").story)
    @allure.title(test_cases.get_test_case("test_sign_up").display_name)
    @allure.severity(test_cases.get_test_case("test_sign_up").severity)
    def test_sign_up(self):
        home_page = HomePage(self.driver)

        country_list = home_page.get_options_list_from_select("sel_signup_country")
        random_country = random.choice(country_list[1:]) # get one of the country names except first one which is not a valid name

        industry_list = home_page.get_options_list_from_select("sel_signup_industry")
        random_industry = random.choice(industry_list[1:]) # get one of the industry names except first one which is not a valid name

        home_page.sign_up(first_name="Umajin",
                          last_name="Test User",
                          email="umajinnz@gmail.com",
                          company="Umajin",
                          country=random_country,
                          industry=random_industry)
