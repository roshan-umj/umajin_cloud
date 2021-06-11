import pytest
from utilities import config_reader

@pytest.mark.usefixtures("add_logs_on_failure", "get_browser", "setup_on_session_start")
class BaseTest:
    pass