from typing import List, Any


def create_table(header: List[Any], rows: List[Any]) -> list:
    """
    Generates a table from the data.
    :param header: list
    :param rows: list
    :return: list
    """
    num_columns = len(rows[0])
    col_widths = [max(len(str(header[i])), *(len(str(row[i])) for row in rows)) for i in range(num_columns)]

    horizontal_border = '+' + '+'.join(['-' * (width + 2) for width in col_widths]) + '+'
    header_row = '|' + '|'.join([' ' + str(header[i]).ljust(col_widths[i]) + ' ' for i in range(num_columns)]) + '|'

    yield horizontal_border
    yield header_row
    yield horizontal_border

    for row in rows:
        yield '|' + '|'.join([' ' + str(row[i]).ljust(col_widths[i]) + ' ' for i in range(num_columns)]) + '|'
        yield horizontal_border


def run_process(process) -> None:
    """
    Starts the process.
    :param process: object
    :return: None
    """
    process.run()
