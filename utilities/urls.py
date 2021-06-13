from utilities import config_reader
home_page = f"https://www.{config_reader.read(section='settings', key='domain')}"
# home_page = "https://www.umajin.com/"

server = config_reader.read(section="settings", key="server")
if server == "test":
    base_url = f"https://cloudtest.{config_reader.read(section='settings', key='domain')}/"
    # base_url = https://cloudtest.umajin.com
else:
    base_url = f"https://cloud.{config_reader.read(section='settings', key='domain')}/"
    # base_url = https://cloud.umajin.com/

project_list = base_url + "index.php"
sign_up_to_download_page = home_page + "#download"
rest_password_page = base_url + "reset_password.php"
project_link = base_url + "index.php?view=dashboard&projectid="