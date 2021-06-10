from pages.common_imports import *
import pages.user_login_page as login


log = Logger(__name__)


class ProjectList(UmajinCloudBase):
    def __init__(self, driver):
        super().__init__(driver=driver)
        self.driver = driver

    def sign_out(self):
        """Signs out from the currently logged in account
        """
        self.click(locator="btn_sign_out")
        log.info(self.driver, "Signing out from the currently logged in account")
        return login.Login(self.driver)

    def switch_view(self, view: str):
        """Switches between grid view and list view

        :param view: name of the view. Values accepted: 'Grid View' or 'List View'
        """
        if view == 'Grid View':
            self.click(locator="btn_grid_view")
            log.info(self.driver, "Switching the project list to grid view")
        else:
            self.click(locator="btn_list_view")
            log.info(self.driver, "Switching the project list to list view")

    def get_projects_count(self, locator: str):
        pass


