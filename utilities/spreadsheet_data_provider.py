import openpyexcel
import random


def get_records(workbook_name, sheet_name):
    """reads a spreadsheet and returns a list of data records

    :param workbook_name: name of the work book
    :param sheet_name: name of the sheet in the workbook
    :return: a list of data records from the given spreadsheet and the sheet
    """
    print("Test Starts here")
    workbook = openpyexcel.load_workbook(workbook_name)
    sheet = workbook[sheet_name]
    total_rows = sheet.max_row
    total_cols = sheet.max_column
    records = []

    for row in range(2, total_rows + 1):
        column_data = []
        for column in range(1, total_cols + 1):
            data = sheet.cell(row=row, column=column).value
            column_data.append(data)
        records.append(column_data)
    print(records)
    print(random.choice(records))
    return records


def get_random_record(workbook_name, sheet_name):
    """reads a spreadsheet and returns a list of data records

    :param workbook_name: name of the work book
    :param sheet_name: name of the sheet in the workbook
    :return: a list of data records from the given spreadsheet and the sheet
    """
    print("Test Starts here")
    workbook = openpyexcel.load_workbook(workbook_name)
    sheet = workbook[sheet_name]
    total_rows = sheet.max_row
    total_cols = sheet.max_column
    records = []
    print("Test 1")

    for row in range(2, total_rows + 1):
        column_data = []
        for column in range(1, total_cols + 1):
            data = sheet.cell(row=row, column=column).value
            column_data.append(data)
        records.append(column_data)
    random_record = random.choice(records)
    random_login = {
        "username": random_record[0],
        "password": random_record[1]
    }
    return random_login
