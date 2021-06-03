from configparser import ConfigParser


def read(section, key):
    """Reads data from conf.ini file in the given section"

    :param section: section name from the conf.ini
    :param key: relevant key to get data
    :return: value of the given key

    """
    config_file = "configuration_data\\conf.ini"
    config = ConfigParser()
    config.read(filenames=config_file)
    return config.get(section=section, option=key)
