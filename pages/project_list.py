from pages.common_imports import *
import pages.user_login_page as login
from utilities import urls


log = Logger(__name__)



class ProjectList(UmajinCloudBase):

    class Project:
        def __init__(self, name, user, project_id, last_modified_date, project_link):
            self.name = name
            self.user = user
            self.id = project_id
            self.last_modified_date = last_modified_date
            self.link = project_link

    def __init__(self, driver):
        super().__init__(driver=driver)
        self.driver = driver
        self.project_list = None

    def sign_out(self):
        """Signs out from the currently logged in account
        """
        self.click(locator="btn_sign_out")
        log.info("Signing out from the currently logged in account", self.driver)
        return login.Login(self.driver)

    def switch_view(self, view: str):
        """Switches between grid view and list view

        :param view: name of the view. Values accepted: 'Grid View' or 'List View'
        """
        if view.lower() == 'list':
            self.click(locator="btn_list_view")
            log.info("Switching the project list to list view", self.driver)
        else:
            self.click(locator="btn_grid_view")
            log.info("Switching the project list to grid view", self.driver)


    def get_list_of_projects_from_grid_view(self):
        """Project list should be in LIST view to run this. Gets a list of project names from the list view

        :return: a list of Project objects. Project object contains name, id, user, last modified date and link properties
        """
        project_details_of_all_projects = self.get_attribute_from_list_of_elements("lst_grid_view_project_list", "data-original-title")
        projects_list = []
        for project in project_details_of_all_projects:
            project_id = project.split("\n")[1].split(",")[1].split(": ")[1]
            new_project = self.Project(
                name=project.split("\n")[0].split(": ")[1],
                user=project.split("\n")[1].split(",")[0].split(": ")[1],
                project_id=project_id,
                last_modified_date=project.split("\n")[2].split(": ", 1)[1],
                project_link=urls.project_link + project_id
            )
            projects_list.append(new_project)
        return projects_list


    def get_list_of_projects_from_list_view(self):
        """Project list should be in GRID view to run this.
        gets a list of project names from get_inner_text_from_elements()
        returns the list of project names as a string
        """
        project_names_list = self.get_text_from_list_of_elements("lst_list_view_project_names_and_links")
        project_links_list = self.get_attribute_from_list_of_elements(
            locator="lst_list_view_project_names_and_links",
            attribute_name="href")
        last_modified_dates_list = self.get_text_from_list_of_elements(locator="lst_list_view_last_modified_dates")
        modified_users_list = self.get_text_from_list_of_elements(locator="lst_list_view_modified_users")
        project_ids_list = self.get_text_from_list_of_elements(locator="lbl_list_view_project_ids")

        projects_list = []
        for index in range(len(project_ids_list)):
            new_project = self.Project(
                name=project_names_list[index],
                user=modified_users_list[index],
                project_id=project_ids_list[index],
                last_modified_date=last_modified_dates_list[index],
                project_link=project_links_list[index]
            )
            projects_list.append(new_project)
        return projects_list
        # print(f"Names: {len(project_names_list)}")
        # print(f"links: {len(project_links_list)}")
        # print(f"Dates: {len(last_modified_dates_list)}")
        # print(f"Users: {len(modified_users_list)}")
        # print(f"IDS: {len(project_ids_list)}")

    def get_projects_count(self, locator: str):
        pass


