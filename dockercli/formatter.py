"""
Helper functions to format output for CLI.
"""
from tabulate import tabulate


def format_data(data):
    """
    Uses tabulate to format the iterable.
    :return: string (multiline)
    """
    if isinstance(data, list) and len(data) > 1:
        if isinstance(data[0], tuple):
            text = tabulate(data)
            return text.split('\n')
        elif isinstance(data[0], dict):
            data = flatten_rows(data)
            data = truncate_rows(data)
            text = tabulate(data, headers='keys')
            return text.split('\n')
        elif isinstance(data[0], basestring):
            data = truncate_rows(data)
            text = tabulate(data)
            return text.split('\n')
    return data


def format_struct(data, spaces=1, indent=0, lines=None):

    if lines is None:
        lines = []

    if isinstance(data, dict):
        data = [(k, data[k]) for k in sorted(data.keys())]

    def add_item_to_line(current_item, current_line, is_last_item):
        """ Helper to add item to end of line """
        current_indent = ' ' * indent
        current_line = current_indent + \
                       current_line + \
                       '{0}'.format(current_item)
        if is_last_item:
            lines.append(current_line)
        else:
            current_line += ': '
        return current_line

    for row in data:
        line = ''
        l = len(row)
        for i in range(l):
            if isinstance(row[i], dict):
                lines.append(line)
                lines = format_struct(row[i], spaces, indent + 1, lines)
                indent -= 1
            elif isinstance(row[i], list):
                if is_plain_list(row[i]):
                    item = ', '.join(map(lambda x: '{0}'.format(x), row[i]))
                    line = add_item_to_line(item, line, i == (l - 1))
                else:
                    lines.append(line)
                    lines = format_struct(row[i], spaces, indent + 1, lines)
                    indent -= 1
            else:
                line = add_item_to_line(row[i], line, i == (l - 1))

    return lines


def is_plain_list(lst):
    """
    Check if all items in list are strings or numbers
    :param lst:
    :return: boolean
    """
    for item in lst:
        if not isinstance(item, basestring) and \
                not isinstance(item, (int, long, float, complex)):
            return False
    return True

def flatten_rows(rows):
    """
    Transform all list or dict values in a dict into comma-separated strings.
    :param rows: iterable of dictionaries
    :return:
    """

    for row in rows:
        for k in row.iterkeys():
            if isinstance(row[k], list):
                row[k] = ', '.join(row[k])
            elif isinstance(row[k], dict):
                row[k] = ', '.join(["{0}: {1}".format(x, y)
                                    for x, y in row[k].iteritems()])
    return rows


def truncate_rows(rows, length=25):
    """
    Truncate every string value in a dictionary up to a certain length.
    :param rows: iterable of dictionaries
    :param length: int
    :return:
    """

    def trimto(str):
        if isinstance(str, basestring):
            return str[:length+1]
        return str

    result = []
    for row in rows:
        if isinstance(row, dict):
            result.append({k: trimto(v) for k, v in row.iteritems()})
        elif isinstance(row, basestring):
            result.append((trimto(row),))
        else:
            result.append(row)
    return result