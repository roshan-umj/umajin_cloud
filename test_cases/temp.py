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


test_driver = webdriver.Chrome(executable_path="C:/selenium_browser_drivers/chromedriver.exe")
test_driver.find_element_by_xpath("sdfsdf").clear()

