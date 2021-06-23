import random
from utilities import config_reader
from utilities import spreadsheet_data_provider
from common_imports_for_tests import *
import pages.profile_page as profile

from utilities.enums import ProfileColors


@pytest.fixture(scope="function")
def navigate_to_page_under_test(request):
    request.cls.driver.get(urls.profile_page)


def is_in_change_success_messages(page_obj, text):
    """checks if the given text in available in a list of success messages received after saving the project.

        :return: True if the text is found in the list of messages
    """
    success_messages = page_obj.get_text_from_list_of_elements("lbl_profile_change_success_alert")
    for text in success_messages:
        return True
    return False


@pytest.mark.usefixtures("navigate_to_page_under_test")
class Test_ProfilePage(BaseTest):
    @allure.story(test_cases.get_test_case("test_changing_profile").story)
    @allure.title(test_cases.get_test_case("test_changing_profile").display_name)
    @allure.severity(test_cases.get_test_case("test_changing_profile").severity)
    @pytest.mark.serial
    def test_changing_profile(self):
        profile_page = profile.ProfilePage(self.driver)

        random_profile_data = spreadsheet_data_provider.get_random_record(
            workbook_name="resources/data_sheets/random_data.xlsx",
            sheet_name="user_profile_data")
        random_name = random_profile_data[2]  # index 2 contains full name
        random_password = random_profile_data[6]  # index 6 contains a random password
        random_color = random.choice(list(ProfileColors)).value
        random_profile_photo = f"resources/profile_pictures/{random.randint(1, 9)}.png"
        password = config_reader.read(section="basic_information", key="test_account_password")

        # test changing only profile color
        profile_page.change_profile(color=random_color)
        assert is_in_change_success_messages(profile_page, "Your avatar color has been changed."), \
            "Avatar color change alert did not appear"

        # test changing only profile name
        profile_page.change_profile(name=random_name)
        assert is_in_change_success_messages(profile_page, "Your name has been updated."), \
            "Name change alert did not appear"

        # test changing only profile picture
        profile_page.change_profile(profile_photo=random_profile_photo)
        assert is_in_change_success_messages(profile_page, "Your user image has been changed."), \
            "Profile photo change alert did not appear"

        # test changing only profile name
        profile_page.change_profile(current_password=password, new_password=random_password)
        assert is_in_change_success_messages(profile_page, "Your password has been updated."), \
            "Password change alert did not appear"

        # reset password back to the default password
        profile_page.reset_password_to_default(current_password=random_password)
