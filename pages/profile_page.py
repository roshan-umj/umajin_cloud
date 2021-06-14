import time
import utilities.config_reader as config_reader

from pages.common_imports import *

log = Logger(__name__)


class ProfilePage(UmajinCloudBase):
    def __init__(self, driver):
        super().__init__(driver=driver)
        self.driver = driver

    def change_profile(self, color=None, name=None, current_password=None, new_password=None, profile_photo=None):
        if color:
            self.click_element_by_attribute_value("lst_profile_colours", "style", f"background-color:{str(color)};")
        if name:
            self.clear("txt_profile_name")
            self.send_keys("txt_profile_name", name)
        if profile_photo:
            self.send_keys("img_profile_avatar", profile_photo)
        if current_password and new_password:
            self.send_keys("txt_profile_password", current_password)
            self.send_keys("txt_profile_new_password", new_password)
            self.send_keys("txt_profile_new_password_confirm", new_password)
        self.click("btn_profile_update")


    def reset_password_to_default(self, current_password):
        default_password = config_reader.read(section="basic_information", key="test_account_password")
        self.change_profile(current_password=current_password, new_password=default_password)