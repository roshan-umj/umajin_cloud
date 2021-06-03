from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities import config_reader
import logging
from utilities.logger import Logger

CONFIG_FILE_SECTION = "locators"
WAIT_TIME = int(config_reader.read(section="settings", key="web_driver_wait_time"))
log = Logger(__name__, logging.INFO)


class UmajinCloudBase:

    def __init__(self, driver):
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

        log.logger.info(f"Clicking on an element: {locator}")

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

        log.logger.info(f"Typing in an element: {locator}. Value entered: {value}")

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

        log.logger.info(f"Selecting from an element: {locator}. Selected value: {value}")

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
        log.logger.info(f"Moving mouse pointer to : {locator}")

    def check_if_element_exists(self, locator: str, by='xpath') -> bool:
        """Checks if an element is present on the page

        :param locator: name of the element. name should match to a record in conf.ini file.

        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.

        :return:
         - True if the element is found


        """
        log.logger.info(f"Checking availability of element: {locator}")
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)

        try:
            if by == 'xpath':
                WebDriverWait(self.driver, WAIT_TIME).until(
                    EC.visibility_of_element_located((By.XPATH, locator_string)))

            elif by == 'css':
                self.driver.find_element_by_css_selector(
                    xpath=config_reader.read(section=CONFIG_FILE_SECTION, key=locator))
            elif by == 'id':
                self.driver.find_element_by_id(xpath=config_reader.read(section=CONFIG_FILE_SECTION, key=locator))
        except NoSuchElementException:
            return False
        return True

    def get_text(self, locator: str, by='xpath') -> bool:
        """Returns the display text of an element

        :param locator: name of the element. name should match to a record in conf.ini file.

        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.

        :return:
         - text of an element
        """
        log.logger.info(f"Getting text of element: {locator}")
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
        log.logger.info(f"Getting the page title of : {self.driver}")
        return self.driver.title

    def get_elements_count(self, locator: str, by='xpath') -> int:
        """Returns number of elements of the given xpath

        :param locator: name of the element. name should match to a record in conf.ini file.

        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.

        :return:
         - number of elements
        """
        log.logger.info(f"Getting the element count of : {locator}")
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)
        if by == 'xpath':
            return len(WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.XPATH, locator_string))))
        elif by == 'css':
            return len(WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, locator_string))))
        elif by == 'id':
            return len(WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.ID, locator_string))))

    def get_options_list_from_select(self, locator: str, by='xpath') -> []:
        """Returns a list of options from a '<select>' element

        :param locator: name of the element. name should match to a record in conf.ini file.
        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.
        :return: a list of options from the select element
        """
        log.logger.info(f"Getting the list of from the select: {locator}")
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator) + "/option"
        if by == 'xpath':
            elements = WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.XPATH, locator_string)))
        elif by == 'css':
            elements = WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, locator_string)))
        elif by == 'id':
            elements = WebDriverWait(self.driver, WAIT_TIME).until(
                EC.visibility_of_element_located((By.ID, locator_string)))

        options_list = []
        for element in elements:
            options_list.append(element.text)
        return options_list
