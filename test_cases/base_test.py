import pytest

@pytest.mark.usefixtures("add_logs_on_failure", "get_browser")
class BaseTest:
    pass