from common_imports_for_tests import *
import pages.user_login_page as login
from pages.project_list import ProjectList
from utilities import spreadsheet_data_provider

@pytest.fixture(scope="class")
def navigate_to_page_under_test(request):
    request.cls.driver.get("https://cloud.umajin.com")
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
        assert login_page.get_text(
            "btn_forgot_password") == "Forgot password?", 'Failed to match text : "Forgot password?" '

        assert login_page.get_page_title() == "Umajin Cloud"

    @allure.story(test_cases.get_test_case("test_sign_up_link").story)
    @allure.title(test_cases.get_test_case("test_sign_up_link").display_name)
    @allure.severity(test_cases.get_test_case("test_sign_up_link").severity)
    def test_sign_up_link(self):
        login_page = login.Login(self.driver)
        login_page.click("btn_sign_up")
        # sign up link https://www.umajin.com/create_account/ redirects to https://www.umajin.com/#download
        login_page.wait_until_redirected("https://www.umajin.com/#download")

        assert self.driver.title == "Umajin Home - Umajin", "On sign up button click: Umajin home page title did not match. "
        self.driver.back()

    @allure.story(test_cases.get_test_case("test_forgot_password_link").story)
    @allure.title(test_cases.get_test_case("test_forgot_password_link").display_name)
    @allure.severity(test_cases.get_test_case("test_forgot_password_link").severity)
    def test_forgot_password_link(self):
        login_page = login.Login(self.driver)
        login_page.click("btn_forgot_password")
        assert self.driver.current_url == "https://cloud.umajin.com/reset_password.php" and self.driver.title == "Umajin Cloud", "'Forgot password?' link page title or url did not match"
        self.driver.back()

    @allure.story(test_cases.get_test_case("test_unsuccessful_login").story)
    @allure.title(test_cases.get_test_case("test_unsuccessful_login").display_name)
    @allure.severity(test_cases.get_test_case("test_unsuccessful_login").severity)
    @pytest.mark.parametrize("username, password",
                             spreadsheet_data_provider.get_records(workbook_name="data_sheets/user_credentials.xlsx",
                                                                   sheet_name="invalid_logins"))
    def test_unsuccessful_login(self, username, password):
        login_page = login.Login(self.driver)
        login_page.log_in(username, password)
        assert login_page.check_if_element_exists("lbl_login_failed"), "Successful login detected for a invalid user"

    @allure.story(test_cases.get_test_case("test_successful_login").story)
    @allure.title(test_cases.get_test_case("test_successful_login").display_name)
    @allure.severity(test_cases.get_test_case("test_successful_login").severity)
    def test_successful_login(self):
        random_login = spreadsheet_data_provider.get_random_record(workbook_name="data_sheets/user_credentials.xlsx",
                                                                   sheet_name="valid_logins")
        login_page = login.Login(self.driver)
        project_list = login_page.log_in(random_login["username"], random_login["password"])
        assert project_list.get_page_title() == "Umajin Cloud | Project List", "Project list title did not match"
        login_page = project_list.sign_out()
        assert login_page.check_if_element_exists('lbl_logout_successful_msg'), "Successful log out message not found in the sign in page after successfully logging out"
