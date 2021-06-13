
from common_imports_for_tests import *
from pages.project_list import ProjectList


@pytest.fixture(scope="function")
def navigate_to_page_under_test(request):
    request.cls.driver.get(urls.project_list)


@pytest.mark.usefixtures("navigate_to_page_under_test")
class Test_ProjectList(BaseTest):

    @allure.story(test_cases.get_test_case("test_project_list_views").story)
    @allure.title(test_cases.get_test_case("test_project_list_views").display_name)
    @allure.severity(test_cases.get_test_case("test_project_list_views").severity)
    def test_project_list_views(self):
        # ----------- Grid View --------------
        project_list = ProjectList(self.driver)
        project_list.switch_view("grid")
        project_list.attach_screenshot(screenshot_name="Grid View Screenshot")

        # get a list of projects and attach the list to the report
        grid_view_projects_list = project_list.get_list_of_projects_from_grid_view()
        project_names_list = ""
        for project in grid_view_projects_list:
            project_names_list += f"{project.name} (Id: {project.id})\n"
        project_list.attach_text(title="Project list - From Grid View", text=project_names_list)

        # ----------- List View --------------
        project_list.switch_view("list")
        project_list.attach_screenshot(screenshot_name="List View Screenshot")
        list_view_projects_list = project_list.get_list_of_projects_from_list_view()
        project_names_list = ""
        for project in list_view_projects_list:
            project_names_list += f"{project.name} (Id: {project.id})\n"
        project_list.attach_text(title="Project list - From List View", text=project_names_list)




    @allure.story(test_cases.get_test_case("test_sign_out").story)
    @allure.title(test_cases.get_test_case("test_sign_out").display_name)
    @allure.severity(test_cases.get_test_case("test_sign_out").severity)
    def test_sign_out(self):
        project_list = ProjectList(self.driver)
        login_page = project_list.sign_out()
        assert login_page.check_if_element_exists("lbl_logout_successful_msg"), "Could not locate log out successful message on the login page after logging out "
