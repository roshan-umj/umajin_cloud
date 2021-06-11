from configparser import ConfigParser, NoSectionError
import logging, os

def read(section, key):
    """Reads data from conf.ini file in the given section"

    :param section: section name from the conf.ini
    :param key: relevant key to get data
    :return: value of the given key

    """
    config_file = "configuration_data/conf.ini"
    config = ConfigParser()
    try:
        config.read(filenames=config_file)
        return config.get(section=section, option=key)
    except NoSectionError:
        logging.error(f"Could not read data from the config file: {config_file}. Make sure the test is running from the "
                  f"root directory. Current directory is {os.getcwd()}")
