from common_imports_for_tests import *
import pages.user_login_page as login
from utilities import config_reader
from pages.project_list import ProjectList
from utilities import spreadsheet_data_provider

@pytest.fixture(scope="class")
def navigate_to_page_under_test(request):
    print(urls.project_list)
    request.cls.driver.get(urls.project_list)

    # when you try to access the login page, it automatically redirects to the project list because of the cookie used.
    # sign out from the project list to open the login page
    project_list = ProjectList(request.cls.driver)
    project_list.sign_out()

@pytest.mark.usefixtures("navigate_to_page_under_test")
class Test_UserSignIn(BaseTest):

    @allure.story(test_cases.get_test_case("test_availability_of_page_elements").story)
    @allure.title(test_cases.get_test_case("test_availability_of_page_elements").display_name)
    @allure.severity(test_cases.get_test_case("test_availability_of_page_elements").severity)
    def test_availability_of_page_elements(self):
        login_page = login.Login(self.driver)
        assert login_page.check_if_element_exists("lbl_login_page_heading"), "Page heading is not available"
        assert login_page.check_if_element_exists("txt_username"), "Page username input field is not available"
        assert login_page.check_if_element_exists("txt_password"), "Password input field is not available"
        assert login_page.check_if_element_exists("lbl_username"), "Username label is not available"
        assert login_page.check_if_element_exists("lbl_password"), "Password label is not available"
        assert login_page.check_if_element_exists("btn_sign_in"), "Sign in button is not available"
        assert login_page.check_if_element_exists("btn_sign_up"), "Sign up button is not available"
        assert login_page.check_if_element_exists(
            "btn_forgot_password"), "Forgot Password? button is not available"

        assert login_page.get_text(
            "lbl_login_page_heading").strip() == "Umajin Cloud Services", 'Page heading is not matched to "Umajin Cloud Service"'
        assert login_page.get_text(
            "lbl_username") == "Username / Email", 'Failed to match text : "Username / Email" '
        assert login_page.get_text("lbl_password") == "Password", 'Failed to match text : "Password" '
        assert login_page.get_text("btn_sign_in") == "Sign in", 'Failed to match text : "Sign in" '
        assert login_page.get_text("btn_sign_Up") == "Sign Up", 'Failed to match text : "Sign up" '
        assert login_page.get_text("btn_forgot_password") == "Forgot password?", 'Failed to match text : "Forgot password?"'

        assert login_page.is_title("Umajin Cloud"), "login page title is not correct"

    @allure.story(test_cases.get_test_case("test_page_links").story)
    @allure.title(test_cases.get_test_case("test_page_links").display_name)
    @allure.severity(test_cases.get_test_case("test_page_links").severity)
    def test_page_links(self):

        login_page = login.Login(self.driver)

        # check if forgot password link works:
        forgot_password_page = login_page.open_forgot_password_page()
        # reset_password page has the same page title as the login page so checking the url instead of the title:
        assert forgot_password_page.is_url(urls.reset_password_page), \
            f"Forgot password?' link didn't load the expected url: {urls.reset_password_page}"
        forgot_password_page.go_back()

        # check if sign up link works:
        home_page = login_page.open_sign_up_page()
        # sign up link https://www.umajin.com/create_account/ redirects to https://www.umajin.com/#download
        login_page.wait_until_redirected(urls.sign_up_to_download_page)
        assert home_page.is_title("Umajin Home - Umajin"), "On sign up button click: Umajin home page title did not match."
        home_page.go_back()




    @allure.story(test_cases.get_test_case("test_preventing_unsuccessful_login_attempts").story)
    @allure.title(test_cases.get_test_case("test_preventing_unsuccessful_login_attempts").display_name)
    @allure.severity(test_cases.get_test_case("test_preventing_unsuccessful_login_attempts").severity)
    @pytest.mark.parametrize("username, password",
                             spreadsheet_data_provider.get_records(workbook_name="resources/data_sheets/user_credentials.xlsx",
                                                                   sheet_name="invalid_logins"))
    def test_preventing_unsuccessful_login_attempts(self, username, password):
        login_page = login.Login(self.driver)
        login_page.log_in(username, password)
        assert login_page.check_if_element_exists("lbl_login_failed"), "Successful login detected for a invalid user"

    @allure.story(test_cases.get_test_case("test_successful_login").story)
    @allure.title(test_cases.get_test_case("test_successful_login").display_name)
    @allure.severity(test_cases.get_test_case("test_successful_login").severity)
    def test_successful_login(self):

        login_page = login.Login(self.driver)

        user_name = config_reader.read(section="basic_information", key="test_account_username")
        password = config_reader.read(section="basic_information", key="test_account_password")
        project_list = login_page.log_in(user_name, password)

        assert project_list.is_title("Umajin Cloud | Project List"), "Project list title did not match"
        login_page = project_list.sign_out()
        assert login_page.check_if_element_exists('lbl_logout_successful_msg'), \
            "Successful log out message not found in the sign in page after successfully logging out"

