from pages.common_imports import *

log = Logger(__name__)


class ForgotPassword(UmajinCloudBase):
    def __init__(self, driver):
        super().__init__(driver=driver)
        self.driver = driver
