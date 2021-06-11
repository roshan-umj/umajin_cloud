from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities import config_reader
from utilities.logger import Logger

CONFIG_FILE_SECTION = "locators"
WAIT_TIME = int(config_reader.read(section="settings", key="web_driver_wait_time"))
log = Logger(__name__)


class UmajinCloudBase:

    def __init__(self, driver: webdriver.Remote):
        self.driver = driver


    def click(self, locator: str, by='xpath'):
        """Simulates clicking on the element

        :param locator: name of the element. name should match to a record in conf.ini file.

        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.
        """
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)
        if by == 'xpath':
            WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.XPATH, locator_string))).click()
        elif by == 'css':
            WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, locator_string))).click()
        elif by == 'id':
            WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.ID, locator_string))).click()

        log.debug(self.driver, f"click on {locator}")

    def send_keys(self, locator: str, value: str, by='xpath'):
        """Simulates typing into the element

        :param locator: name of the element. name should match to a record in conf.ini file.

        :param value: A string for typing, or setting form fields.

        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.
        """
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)

        if by == 'xpath':
            WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.XPATH, locator_string))).send_keys(value)
        elif by == 'css':
            WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, locator_string))).send_keys(value)
        elif by == 'id':
            WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.ID, locator_string))).send_keys(value)

        log.debug(self.driver, f"type in {locator}. value: {value}")

    def select(self, locator: str, value: str, by='xpath'):
        """Simulates selecting an item from a dropdown

        :param locator: name of the element. name should match to a record in conf.ini file.

        :param value: A string for typing, or setting form fields.

        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.
        """
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)
        if by == 'xpath':
            drop_down = WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.XPATH, locator_string)))
        elif by == 'css':
            drop_down = WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, locator_string)))
        elif by == 'id':
            drop_down = WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.ID, locator_string)))

        select = Select(drop_down)
        select.select_by_visible_text(value)

        log.debug(self.driver, "select '{value}' from {locator}")

    def go_back(self):
        """Goes back to the previous page
        """
        self.driver.back()
        log.debug(self.driver, f"go back to the previous page")

    def move_to(self, locator: str, by='xpath'):
        """Simulates moving mouse pointer to a target element

        :param locator: name of the element. name should match to a record in conf.ini file.

        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.

        """
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)
        if by == 'xpath':
            element = WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.XPATH, locator_string)))
        elif by == 'css':
            element = WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, locator_string)))
        elif by == 'id':
            element = WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.ID, locator_string)))

        action = ActionChains(driver=self.driver)
        action.move_to_element(element).perform()
        log.debug(self.driver, f"move mouse pointer to {locator}")

    def check_if_element_exists(self, locator: str, by='xpath') -> bool:
        """Checks if an element is present on the page

        :param locator: name of the element. name should match to a record in conf.ini file.

        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.

        :return:
         - True if the element is found


        """
        log.debug(self.driver, f"checking availability of {locator}")
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)

        try:
            if by == 'xpath':
                WebDriverWait(self.driver, WAIT_TIME).until(
                    EC.visibility_of_element_located((By.XPATH, locator_string)))

            elif by == 'css':
                WebDriverWait(self.driver, WAIT_TIME).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, locator_string)))
            elif by == 'id':
                WebDriverWait(self.driver, WAIT_TIME).until(
                    EC.visibility_of_element_located((By.ID, locator_string)))
        except NoSuchElementException:
            log.error(f" {locator} not found")
            return False
        log.debug(self.driver, f"{locator} found on the page!")
        return True

    def get_text(self, locator: str, by='xpath') -> bool:
        """Returns the display text of an element

        :param locator: name of the element. name should match to a record in conf.ini file.

        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.

        :return:
         - text of an element
        """
        log.debug(self.driver, f"get text from {locator}")
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)

        if by == 'xpath':
            return WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.XPATH, locator_string))).text
        elif by == 'css':
            return WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, locator_string))).text
        elif by == 'id':
            return WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.ID, locator_string))).text

    def get_page_title(self) -> str:
        """Returns the display text of an element

        """
        log.debug(self.driver, f"get page title: {self.driver.title}")
        return self.driver.title

    def get_page_url(self) -> str:
        """Returns the display text of an element

        """
        log.debug(self.driver, f"get page url: {self.driver.current_url}")
        return self.driver.current_url

    def get_elements_count(self, locator: str, by='xpath') -> int:
        """Returns number of elements of the given xpath

        :param locator: name of the element. name should match to a record in conf.ini file.

        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.

        :return:
         - number of elements
        """
        log.debug(self.driver, f"get the element count of {locator}")
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)
        if by == 'xpath':
            select = WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.XPATH, locator_string)))
            options = select.find_elements_by_tag_name("option")
            return len(options)
        elif by == 'css':
            select = WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, locator_string)))
            options = select.find_elements_by_tag_name("option")
            return len(options)
        elif by == 'id':
            select = WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.ID, locator_string)))
            options = select.find_elements_by_tag_name("option")
            return len(options)

    def get_options_list_from_select(self, locator: str, by='xpath') -> []:
        """Returns a list of options from a '<select>' element

        :param locator: name of the element. name should match to a record in conf.ini file.
        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.
        :return: a list of options from the select element
        """
        log.debug(self.driver, f"get a list of options from the select element: {locator}")
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)
        if by == 'xpath':
            select = WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.XPATH, locator_string)))
            options = [item.text for item in select.find_elements_by_tag_name("option")]
            return options

        elif by == 'css':
            select = WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, locator_string)))
            options = [item.text for item in select.find_elements_by_tag_name("option")]
            return options

        elif by == 'id':
            select = WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.ID, locator_string)))
            options = [item.text for item in select.find_elements_by_tag_name("option")]
            return options


    def wait_until_redirected(self, url: str, wait_time: int = WAIT_TIME):
        """Waits until url redirection is completed.

        :param url: url expected after redirection
        :param wait_time: (optional parameter) wait time in seconds. If not specified, it uses the default wait time specified in conf.ini
        """
        WebDriverWait(self.driver, wait_time).until(EC.url_changes(url))
