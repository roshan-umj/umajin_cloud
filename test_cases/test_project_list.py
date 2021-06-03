import time

import allure
import pytest
from pages.user_login_page import Login
from pages.project_list import ProjectList
from utilities import spreadsheet_data_provider
from test_cases.base_test import BaseTest


@pytest.fixture(scope="class")
def navigate_to_project_list(request):
    login_page = Login(request.cls.driver)
    login_page.log_in("roshan@ur.co.nz", "umajin@001")


@pytest.mark.usefixtures("navigate_to_project_list")
class Test_ProjectList(BaseTest):

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Cloud Login Test")
    def test_switching_to_list_view(self):
        project_list = ProjectList(self.driver)
        project_list.click("btn_list_view")
        time.sleep(10)
        print("test")

    def test_sign_out(self):
        project_list = ProjectList(self.driver)
        project_list.sign_out()
