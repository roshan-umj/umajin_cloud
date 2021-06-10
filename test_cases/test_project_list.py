
from common_imports_for_tests import *
from pages.project_list import ProjectList


@pytest.fixture(scope="function")
def navigate_to_page_under_test(request):
    request.cls.driver.get("https://cloud.umajin.com/index.php?")


@pytest.mark.usefixtures("navigate_to_page_under_test")
class Test_ProjectList(BaseTest):

    @allure.story(test_cases.get_test_case("test_switching_to_list_view").story)
    @allure.title(test_cases.get_test_case("test_switching_to_list_view").display_name)
    @allure.severity(test_cases.get_test_case("test_switching_to_list_view").severity)
    def test_switching_to_list_view(self):
        project_list = ProjectList(self.driver)
        project_list.click("btn_list_view")

    @allure.story(test_cases.get_test_case("test_sign_out").story)
    @allure.title(test_cases.get_test_case("test_sign_out").display_name)
    @allure.severity(test_cases.get_test_case("test_sign_out").severity)
    def test_sign_out(self):
        project_list = ProjectList(self.driver)
        login_page = project_list.sign_out()
        login_page.check_if_element_exists("lbl_logout_successful_msg")
