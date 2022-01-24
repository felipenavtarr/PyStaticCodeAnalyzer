import re

messages = {'S001': 'Too long', 'S002': 'Indentation is not a multiple of four', 'S003': 'Unnecessary semicolon',
            'S004': 'At least two spaces required before inline comments', 'S005': 'TODO found',
            'S006': 'More than two blank lines used before this line'}


def is_blank_line(_line):
    # return re.match(r'\s+$', _line)
    return not _line.strip()


def is_s001(_line):
    max_char = 79
    return len(_line) > max_char


def is_s002(_line):
    return (len(_line) - len(_line.lstrip())) % 4 != 0


def is_s003(_line):
    if '#' in _line:
        _line = _line.split('#')[0]
    return _line.rstrip().endswith(';')


def is_s004(_line):
    if '#' in _line:
        left_part = _line.split('#')[0]
        if left_part.rstrip():
            return len(left_part) - len(left_part.rstrip()) < 2
    return None


def is_s005(_line):
    # return '#' in _line and re.search('todo', _line.partition('#')[2], re.IGNORECASE)
    return '#' in _line and 'todo' in _line.split('#')[1].lower()


errors_found = {}

path_to_file = input()
file = open(path_to_file, 'r')

blanks = 0
for i, line in enumerate(file, start=1):
    if is_blank_line(line):
        blanks += 1
        continue

    errors_in_line = []

    if is_s001(line):
        errors_in_line.append('S001')
    if is_s002(line):
        errors_in_line.append('S002')
    if is_s003(line):
        errors_in_line.append('S003')
    if is_s004(line):
        errors_in_line.append('S004')
    if is_s005(line):
        errors_in_line.append('S005')
    if blanks > 2:
        errors_in_line.append('S006')

    blanks = 0

    if errors_in_line:
        errors_found[i] = sorted(errors_in_line)

file.close()

for line, errors in errors_found.items():
    for error in errors:
        print(f'Line {line}: {error} {messages[error]}')
