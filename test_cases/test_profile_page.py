import random
from utilities import config_reader
from utilities import spreadsheet_data_provider
from common_imports_for_tests import *
import pages.profile_page as profile

from utilities.enums import ProfileColors


@pytest.fixture(scope="function")
def navigate_to_page_under_test(request):
    request.cls.driver.get(urls.profile_page)


@pytest.mark.usefixtures("navigate_to_page_under_test")
class Test_ProfilePage(BaseTest):
    @allure.story(test_cases.get_test_case("test_changing_profile").story)
    @allure.title(test_cases.get_test_case("test_changing_profile").display_name)
    @allure.severity(test_cases.get_test_case("test_changing_profile").severity)
    def test_changing_profile(self):
        profile_page = profile.ProfilePage(self.driver)

        random_profile_data = spreadsheet_data_provider.get_random_record(workbook_name="resources/data_sheets/random_data.xlsx",
                                                                          sheet_name="user_profile_data")
        random_name = random_profile_data[2]  # index 2 contains full name
        random_password = random_profile_data[6]  # index 6 contains a random password
        random_color = random.choice(list(ProfileColors)).value
        random_profile_photo = f"resources/profile_pictures/{random.randint(1, 9)}.png"
        password = config_reader.read(section="basic_information", key="test_account_password")

        # test changing only profile color
        profile_page.change_profile(color=random_color)
        assert "Your avatar color has been changed." in profile_page.get_text("lbl_profile_change_success_alert"), \
            "Avatar color change alert did not appear"

        # test changing only profile name
        profile_page.change_profile(name=random_name)
        assert "Your name has been updated." in profile_page.get_text("lbl_profile_change_success_alert"), \
            "Name change alert did not appear"

        # test changing only profile picture
        profile_page.change_profile(profile_photo=random_profile_photo)
        assert "Your user image has been changed." in profile_page.get_text("lbl_profile_change_success_alert"), \
            "Profile photo change alert did not appear"

        # test changing only profile name
        profile_page.change_profile(current_password=password, new_password=random_password)
        assert "Your password has been updated." in profile_page.get_text("lbl_profile_change_success_alert"), \
            "Password change alert did not appear"

        # reset password back to the default password
        profile_page.reset_password_to_default(current_password=random_password)
