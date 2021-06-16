from resources import data
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

        # industry_list = home_page.get_options_list_from_select("sel_signup_industry")
        # country_list = home_page.get_options_list_from_select("sel_signup_country")
        # random_country = random.choice(country_list[1:]) # get one of the country names except first one which is not a valid name
        # random_industry = random.choice(industry_list[1:])  # get one of the industry names except first one which is not a valid name

        # It takes a considerable amount of time to read all options tags from above 2 <select> elements.
        #  Therefore, all option values from those selects are stored in 2 lists in resources/data.py"
        #  comment following 2 lines and uncomment above 4 lines if you want to get values from the website in runtime.

        random_country = random.choice(data.countries)
        random_industry = random.choice(data.industries)



        home_page.sign_up(first_name="Umajin",
                          last_name="Test User",
                          email="umajinnz@gmail.com",
                          company="Umajin",
                          country=random_country,
                          industry=random_industry)
