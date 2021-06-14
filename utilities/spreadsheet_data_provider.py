import openpyexcel
import random


def get_records(workbook_name, sheet_name):
    """reads a spreadsheet and returns a list of data records

    :param workbook_name: name of the work book
    :param sheet_name: name of the sheet in the workbook
    :return: a list of data records from the given spreadsheet and the sheet
    """
    workbook = openpyexcel.load_workbook(workbook_name)
    sheet = workbook[sheet_name]
    total_rows = sheet.max_row
    total_cols = sheet.max_column
    records = []

    # staring from the second row to skip the headings
    for row in range(2, total_rows + 1):
        column_data = []
        for column in range(1, total_cols + 1):
            data = sheet.cell(row=row, column=column).value
            column_data.append(data)
        records.append(column_data)
    return records


def get_random_record(workbook_name, sheet_name):
    """reads a spreadsheet and returns a random record as a list object

    :param workbook_name: name of the work book
    :param sheet_name: name of the sheet in the workbook
    :return: a random record from the excel sheet
    """
    return random.choice(get_records(workbook_name, sheet_name))
