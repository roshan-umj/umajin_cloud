import utilities.spreadsheet_data_provider as dp
import utilities.logger as log

logger = log.Logger(__name__)

class TestCase:
    def __init__(self, test_case_id, page_name, story, display_name, description, severity, done, comments):
        self.id = test_case_id
        self.page_name = page_name
        self.story = story
        self.display_name = display_name
        self.description = description
        self.severity = severity
        self.done = done
        self.comments = comments


# reading test_coverage.xlsx and get test case data from it:

try:
    records = dp.get_records("resources/data_sheets/test_coverage.xlsx", "test_cases")
    test_cases = []
    for record in records:
        tc = TestCase(
            test_case_id=record[2],
            page_name=record[0],
            story=record[1],
            display_name=record[3],
            description=record[4],
            severity=record[5],
            done=record[6],
            comments=record[7]
        )
        test_cases.append(tc)
except FileNotFoundError:
    logger.error("Failed to data from test_coverage.xlsx")

def get_test_case(test_case_function_name) -> TestCase:
    for test_case in test_cases:
        if test_case.id == test_case_function_name:
            return test_case
