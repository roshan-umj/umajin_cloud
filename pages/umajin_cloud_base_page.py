from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities import config_reader
from utilities.logger import Logger
import allure

CONFIG_FILE_SECTION = "locators"
WAIT_TIME = int(config_reader.read(section="settings", key="web_driver_wait_time"))
log = Logger(__name__)


def _validate_wait_time_(wait_time):
    try:
        wait_time = int(wait_time)
    except (ValueError, TypeError):
        wait_time = WAIT_TIME
        log.warning(f"value of wait_time ({wait_time}) was not an integer."
                    f" the default wait time ({WAIT_TIME} has been used instead.")
    return wait_time

class UmajinCloudBase:

    def __init__(self, driver: webdriver.Remote):
        self.driver = driver
        self.title = driver.title
        self.url = driver.current_url

    def click(self, locator: str, by='xpath', wait_time=WAIT_TIME):
        f"""Simulates clicking on the element

        :param locator: name of the element. name should match to a record in conf.ini file.

        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.

        :param wait_time: (optional parameter). the time to wait before throwing element not found exception. 
         if not specified the default wait time will be used.
        """

        wait_time = _validate_wait_time_(wait_time)

        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)
        try:
            if by == 'xpath':
                WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.XPATH, locator_string))).click()
            elif by == 'css':
                WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, locator_string))).click()
            elif by == 'id':
                WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.ID, locator_string))).click()
        except NoSuchElementException:
            log.error(f" {locator} not found")
        else:
            log.debug(self.driver, f"click on {locator} : {locator_string}")

    def click_element_by_attribute_value(self, locator: str,
                                         attribute_name: str,
                                         value: str, by='xpath',
                                         wait_time=WAIT_TIME):
        """Simulates clicking on the element. Finds an element by the attribute name and value.

        :param locator: name of the element. name should match to a record in conf.ini file.
        :param attribute_name: name of the attribute.  Eg:"style"
        :param value: value of the attribute. Eg: "background-color:#ffb3ba;"

        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.
        :param wait_time: (optional parameter). the time to wait before throwing element not found exception.
         if not specified the default wait time will be used.
        """

        wait_time = _validate_wait_time_(wait_time)
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator) + f"[@{attribute_name}='{value}']"
        try:
            if by == 'xpath':
                WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.XPATH, locator_string))).click()
            elif by == 'css':
                WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, locator_string))).click()
            elif by == 'id':
                WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.ID, locator_string))).click()
        except NoSuchElementException:
            log.error(f" {locator} not found")
        else:
            log.debug(self.driver, f"click on {locator}({attribute_name}:{value}) : {locator_string}. ")

    def send_keys(self, locator: str, value: str, by='xpath', wait_time=WAIT_TIME):
        """Simulates typing into the element

        :param locator: name of the element. name should match to a record in conf.ini file.

        :param value: A string for typing, or setting form fields.ip_address

        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.

        :param wait_time: (optional parameter). the time to wait before throwing element not found exception.
         if not specified the default wait time will be used.
        """
        wait_time = _validate_wait_time_(wait_time)
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)
        try:
            if by == 'xpath':
                WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.XPATH, locator_string))).send_keys(value)
            elif by == 'css':
                WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, locator_string))).send_keys(value)
            elif by == 'id':
                WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((By.ID, locator_string))).send_keys(value)
        except NoSuchElementException:
            log.error(f" {locator} not found")
        else:
            log.debug(self.driver, f"type in {locator} ({locator_string}). value: {value}")

    def clear(self, locator: str, by='xpath', wait_time=WAIT_TIME):
        """Clears the text if it's a text entry element.

            :param locator: name of the element. name should match to a record in conf.ini file.
            :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
             the element is searched by xpath.
            :param wait_time: (optional parameter). the time to wait before throwing element not found exception.
         if not specified the default wait time will be used.
        """

        wait_time = _validate_wait_time_(wait_time)
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)
        try:
            if by == 'xpath':
                WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.XPATH, locator_string))).clear()
            elif by == 'css':
                WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, locator_string))).clear()
            elif by == 'id':
                WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.ID, locator_string))).clear()
        except NoSuchElementException:
            log.error(f" {locator} not found")
        else:
            log.debug(self.driver, f"clear text from  {locator} : {locator_string}")

    def select(self, locator: str, value: str, by='xpath', wait_time=WAIT_TIME):
        """Simulates selecting an item from a dropdown

        :param locator: name of the element. name should match to a record in conf.ini file.

        :param value: A string for typing, or setting form fields.

        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.
        :param wait_time: (optional parameter). the time to wait before throwing element not found exception.
         if not specified the default wait time will be used.
        """

        wait_time = _validate_wait_time_(wait_time)
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)
        try:
            if by == 'xpath':
                drop_down = WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.XPATH, locator_string)))
            elif by == 'css':
                drop_down = WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, locator_string)))
            elif by == 'id':
                drop_down = WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.ID, locator_string)))
        except NoSuchElementException:
            log.error(f" {locator} not found")
        else:
            select = Select(drop_down)
            select.select_by_visible_text(value)
            log.debug(self.driver, f"select {value} from {locator} : {locator_string}")

    def go_back(self):
        """Goes back to the previous page
        """
        # self.driver.back()              # back() doesn't work on safari.
        self.driver.execute_script("window.history.go(-1)")
        log.debug(self.driver, f"go back to the previous page")

    def move_to(self, locator: str, by='xpath', wait_time=WAIT_TIME):
        """Simulates moving mouse pointer to a target element

        :param locator: name of the element. name should match to a record in conf.ini file.

        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.
        :param wait_time: (optional parameter). the time to wait before throwing element not found exception.
         if not specified the default wait time will be used.
        """

        wait_time = _validate_wait_time_(wait_time)
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)
        try:
            if by == 'xpath':
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.XPATH, locator_string)))
            elif by == 'css':
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, locator_string)))
            elif by == 'id':
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.ID, locator_string)))
        except NoSuchElementException:
            log.error(f" {locator} not found")
        else:
            action = ActionChains(driver=self.driver)
            action.move_to_element(element).perform()
            log.debug(self.driver, f"move mouse pointer to {locator} : {locator_string}")

    def check_if_element_exists(self, locator: str, by='xpath', wait_time=WAIT_TIME) -> bool:
        """Checks if an element is present on the page

        :param locator: name of the element. name should match to a record in conf.ini file.

        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.

        :param wait_time: (optional parameter). the time to wait before throwing element not found exception.
         if not specified the default wait time will be used.

        :return:
         - True if the element is found
        """

        wait_time = _validate_wait_time_(wait_time)
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)
        log.debug(self.driver, f"checking availability of {locator}: {locator_string}")

        try:
            if by == 'xpath':
                WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.XPATH, locator_string)))

            elif by == 'css':
                WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, locator_string)))
            elif by == 'id':
                WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.ID, locator_string)))
        except NoSuchElementException:
            log.error(f" {locator} not found")
            return False
        else:
            log.debug(self.driver, f"{locator} found on the page!")
            return True

    def check_if_elements_exist(self, *locators, by='xpath', wait_time=WAIT_TIME) -> bool:
        """Checks if an element is present on the page

         Eg:
         check_if_elements_exist("lbl_list_view_icon", "lbl_list_view_name")


        :param locators: name of the elements. provided names should match to records in conf.ini file.

        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.

        :param wait_time: (optional parameter). the time to wait before throwing element not found exception.
         if not specified the default wait time will be used.

        :return:
         - True if the element is found


        """
        wait_time = _validate_wait_time_(wait_time)
        for locator in locators:
            log.debug(self.driver, f"checking availability of {locator}")
            locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)

            try:
                if by == 'xpath':
                    WebDriverWait(self.driver, wait_time).until(
                        EC.visibility_of_element_located((By.XPATH, locator_string)))
                elif by == 'css':
                    WebDriverWait(self.driver, wait_time).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, locator_string)))
                elif by == 'id':
                    WebDriverWait(self.driver, wait_time).until(
                        EC.visibility_of_element_located((By.ID, locator_string)))
            except NoSuchElementException:
                log.error(f" {locator} (xpath: {locator_string} not found")
                return False
            except TimeoutException:
                log.error(f"time out! {locator} (xpath: {locator_string} cloud not be found on the page")
                return False
            else:
                log.debug(self.driver, f"{locator} (xpath: {locator_string}) found on the page!")
        return True

    def get_text(self, locator: str, by='xpath', wait_time=WAIT_TIME):
        """Returns the display text of an element
        :param locator: name of the element. name should match to a record in conf.ini file.
        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.
        :param wait_time: (optional parameter). the time to wait before throwing element not found exception.
         if not specified the default wait time will be used.
        :return:
         - text of an element
        """
        wait_time = _validate_wait_time_(wait_time)
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)
        log.debug(self.driver, f"get text from {locator} : {locator_string}")
        try:
            if by == 'xpath':
                return WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.XPATH, locator_string))).text
            elif by == 'css':
                return WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, locator_string))).text
            elif by == 'id':
                return WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.ID, locator_string))).text
        except NoSuchElementException:
            log.error(f" {locator} not found")

    def is_title(self, expected_title: str, wait_time=WAIT_TIME) -> bool:
        """An expectation for checking the title of a page.
    the expected title must be an exact match.

        :param expected_title: text to match with the current page title

        :param wait_time: (optional parameter). the time to wait before throwing element not found exception.
         if not specified the default wait time will be used.

        :return:
         - True if the title matches, false otherwise.
        """
        wait_time = _validate_wait_time_(wait_time)
        log.debug(self.driver, f"check if the page tittle is correct. expected title: {expected_title}")
        try:
            return WebDriverWait(self.driver, wait_time).until(EC.title_is(expected_title))

        except TimeoutException:
            log.error(f" timeout! Current page title is not {expected_title}")
            return False

    def title_contains(self, expected_title: str, wait_time=WAIT_TIME) -> bool:
        """An expectation for checking that the title contains a case-sensitive
    substring. expected title is the fragment of title expected

        :param expected_title: text to check if current page title contains

        :param wait_time: (optional parameter). the time to wait before throwing element not found exception.
         if not specified the default wait time will be used.

        :return:
         - True when the title matches, False otherwise
        """
        wait_time = _validate_wait_time_(wait_time)
        log.debug(self.driver, f"check if the page tittle contains: {expected_title}")
        try:
            return WebDriverWait(self.driver, wait_time).until(EC.title_contains(expected_title))
        except TimeoutException:
            log.error(f" timeout! Current page title is not {expected_title}")
            return False

    def url_contains(self, expected_url: str, wait_time=WAIT_TIME) -> bool:
        """An expectation for checking that the current url contains a case-sensitive substring.

        :param expected_url: the fragment of url expected

        :param wait_time: (optional parameter). the time to wait before throwing element not found exception.
         if not specified the default wait time will be used.

        :return: True when the url matches, False otherwise
        """
        wait_time = _validate_wait_time_(wait_time)
        log.debug(self.driver, f"check if the current url contains: {expected_url}")
        try:
            return WebDriverWait(self.driver, wait_time).until(EC.url_contains(expected_url))
        except TimeoutException:
            log.error(f" timeout! current url doesn't contain {expected_url}")
            return False

    def is_url(self, expected_url: str, wait_time=WAIT_TIME) -> bool:
        """An expectation for checking that the current url is an exact match to the expected url.

        :param expected_url: Url to match with the current url

        :param wait_time: (optional parameter). the time to wait before throwing element not found exception.
         if not specified the default wait time will be used.

        :return: True if the the url matches, False otherwise
        """
        wait_time = _validate_wait_time_(wait_time)
        log.debug(self.driver, f"check if the current url matched to : {expected_url}")
        try:
            return WebDriverWait(self.driver, wait_time).until(EC.url_contains(expected_url))
        except TimeoutException:
            log.error(f" timeout! current url is not {expected_url}")
            return False

    def wait_until_redirected(self, url: str, wait_time=WAIT_TIME):
        """Waits until url redirection is completed.

        :param url: url expected after redirection
        :param wait_time: (optional parameter) wait time in seconds. If not specified, it uses the default wait time specified in conf.ini
        """
        wait_time = _validate_wait_time_(wait_time)
        WebDriverWait(self.driver, wait_time).until(EC.url_changes(url))
        log.debug(self.driver, f"waiting until redirected to {url}")

    def get_attribute_from_element(self, locator: str, attribute_name: str, by='xpath', wait_time=WAIT_TIME) -> str:
        """Returns the value of the attribute from the given element

        :param locator: name of the element. name should match to a record in conf.ini file.

        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.

        :param attribute_name: name of the attribute

        :param wait_time: (optional parameter). the time to wait before throwing element not found exception.
         if not specified the default wait time will be used.
         """
        wait_time = _validate_wait_time_(wait_time)
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)
        log.debug(self.driver, f"get attribute {attribute_name} from element: {locator} ({locator_string})")
        try:
            if by == 'xpath':
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.XPATH, locator_string)))
                return element.get_attribute(attribute_name)
            elif by == 'css':
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, locator_string)))
                return element.get_attribute(attribute_name)
            elif by == 'id':
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.ID, locator_string)))
                return element.get_attribute(attribute_name)
        except NoSuchElementException:
            log.error(f" {locator} not found")

    def get_attribute_from_list_of_elements(self, locator: str, attribute_name: str, by='xpath', wait_time=WAIT_TIME) -> list:
        """Returns a list of values from the given attribute of the given list of elements

        :param locator: name of the element. name should match to a record in conf.ini file.
        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.
        :param attribute_name: name of the attribute
        :param wait_time: (optional parameter). the time to wait before throwing element not found exception.
         if not specified the default wait time will be used.
         """
        wait_time = _validate_wait_time_(wait_time)
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)
        log.debug(self.driver,
                  f"get attributes {attribute_name} from the list of elements: {locator}: {locator_string}")
        try:
            if by == 'xpath':
                elements = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_all_elements_located((By.XPATH, locator_string)))
            elif by == 'css':
                elements = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, locator_string)))
            elif by == 'id':
                elements = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_all_elements_located((By.ID, locator_string)))
        except NoSuchElementException:
            log.error(f" {locator} not found")
            return []
        else:
            attributes_list = [element.get_attribute(attribute_name) for element in elements]
            return attributes_list

    def get_elements(self, locator: str, by='xpath', wait_time=WAIT_TIME) -> list:
        """Returns a list of elements

        :param locator: name of the element. name should match to a record in conf.ini file.
        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.
        :param wait_time: (optional parameter). the time to wait before throwing element not found exception.
         if not specified the default wait time will be used.
        :return: list of elements
        """
        wait_time = _validate_wait_time_(wait_time)
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)
        log.debug(self.driver, f"get a list of elements from {locator} : {locator_string}")
        try:
            if by == 'xpath':
                elements_list = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_all_elements_located((By.XPATH, locator_string)))
            elif by == 'css':
                elements_list = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, locator_string)))
            elif by == 'id':
                elements_list = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_all_elements_located((By.ID, locator_string)))
        except NoSuchElementException:
            log.error(f" {locator} not found")
            return []
        else:
            return elements_list

    def get_elements_count(self, locator: str, by='xpath', wait_time=WAIT_TIME) -> int:
        """Returns number of elements of the given xpath

        :param locator: name of the element. name should match to a record in conf.ini file.
        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.
        :param wait_time: (optional parameter). the time to wait before throwing element not found exception.
         if not specified the default wait time will be used.
        :return:
         - number of elements
        """
        wait_time = _validate_wait_time_(wait_time)
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)
        log.debug(self.driver, f"get the element count of {locator}: {locator_string}")
        try:
            if by == 'xpath':
                elements_list = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_all_elements_located((By.XPATH, locator_string)))
            elif by == 'css':
                elements_list = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, locator_string)))
            elif by == 'id':
                elements_list = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_all_elements_located((By.ID, locator_string)))
        except NoSuchElementException:
            log.error(f" {locator} not found")
        else:
            return len(elements_list)

    def get_options_list_from_select(self, locator: str, by='xpath', wait_time=WAIT_TIME) -> []:
        """Returns a list of options from a '<select>' element

        :param locator: name of the element. name should match to a record in conf.ini file.
        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.
        :param wait_time: (optional parameter). the time to wait before throwing element not found exception.
         if not specified the default wait time will be used.
        :return: a list of options from the select element
        """
        wait_time = _validate_wait_time_(wait_time)
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)
        log.debug(self.driver, f"get a list of options from the select element: {locator} ({locator_string})")
        try:
            if by == 'xpath':
                select = WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.XPATH, locator_string)))
            elif by == 'css':
                select = WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, locator_string)))
            elif by == 'id':
                select = WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.ID, locator_string)))
        except NoSuchElementException:
            log.error(f" {locator} not found")
            return []
        else:
            options = [item.text for item in select.find_elements_by_tag_name("option")]
            return options

    def get_text_from_list_of_elements(self, locator: str, by='xpath', wait_time=WAIT_TIME) -> []:
        """Returns a list of text values from a given list of elements


        the xpath provided should return a list of elements, not just a single element.

        Eg:
        if xpath returns the following list,

        <a>Test 1</a>
        <a>Test 2</a>
        <a>Test 3</a>
        <a>Test 4</a>

        the output of this function will be: ["Test 1", "Test 2", "Test3", "Test 4"]


        :param locator: name of the elements list. name should match to a record in conf.ini file.
        :param by: (optional parameter. input values: 'xpath', 'css', 'id') if no selector type is defined,
         the element is searched by xpath.
        :param wait_time: (optional parameter). the time to wait before throwing element not found exception.
         if not specified the default wait time will be used.
        :return: a list of text values from the given list of elements
        """
        wait_time = _validate_wait_time_(wait_time)
        locator_string = config_reader.read(section=CONFIG_FILE_SECTION, key=locator)
        log.debug(self.driver, f"get a list of elements from the elements list: {locator} ({locator_string})")
        try:
            if by == 'xpath':
                elements_list = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_all_elements_located((By.XPATH, locator_string)))
            elif by == 'css':
                elements_list = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, locator_string)))
            elif by == 'id':
                elements_list = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_all_elements_located((By.ID, locator_string)))
        except NoSuchElementException:
            log.error(f" {locator} not found")
        else:
            list_of_inner_texts = [item.text for item in elements_list]
            return list_of_inner_texts

    def attach_screenshot(self, screenshot_name="screenshot"):
        """gets a screenshot and attaches to the allure report.
        :param screenshot_name: (optional parameter) renames the screenshot in the report
        """
        allure.attach(self.driver.get_screenshot_as_png(), name=screenshot_name, attachment_type=AttachmentType.PNG,
                      extension="png")
        log.debug(self.driver, f"attaching screenshot to allure report: {screenshot_name}")

    def attach_text(self, title, text):
        """attaches a given text to the report.
        :param title: A title for the description
        :param text: body of the text
        """
        allure.attach(body=text, name=title, attachment_type=AttachmentType.TEXT, extension="png")
        log.debug(self.driver, f"attach text to allure report. title: {title}")
