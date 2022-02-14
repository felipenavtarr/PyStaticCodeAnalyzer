import re


def is_blank_line(line):
    return not line.strip()


def is_s001(line):
    max_char = 79
    return len(line) > max_char


def is_s002(line):
    return (len(line) - len(line.lstrip())) % 4 != 0


def is_s003(line):
    if '#' in line:
        line = line.split('#')[0]
    return line.rstrip().endswith(';')


def is_s004(line):
    if '#' in line:
        left_part = line.split('#')[0]
        if left_part.rstrip():
            return len(left_part) - len(left_part.rstrip()) < 2
    return None


def is_s005(line):
    return '#' in line and 'todo' in line.split('#')[1].lower()


def check_s007(line):
    # pattern = r'^(def|class)\s+\w+\(?\w*\)?:$'
    pattern = r'^\s*(def|class)\s+\w+\(?.*\)?:$'
    if re.match(pattern, line) and len(line.lstrip().split(' ')) > 2:
        return line.split()[0]
    return None


def check_s008(line):
    line_pattern = r'^\s*class\s+\w+(\(\w+\)){0,1}:$'
    name_pattern = r'^[A-Z][a-z0-9]*[A-Za-z0-9]*$'
    if re.match(line_pattern, line):
        right_part = line.split()[1]
        if '(' in right_part:
            class_name = right_part[:right_part.index('(')]
        else:
            class_name = right_part[:-1]
        if not re.match(name_pattern, class_name):
            return class_name
    return None


def check_s009(line):
    line_pattern = r'^\s*def\s+\w+\(.*\):$'
    name_pattern = r'^[_a-z][_a-z0-9]*$'
    if re.match(line_pattern, line):
        right_part = line.split()[1]
        function_name = right_part[:right_part.index('(')]
        if not re.match(name_pattern, function_name):
            return function_name
    return None


class Analyzer:
    """Analyzes a file object.
    Has only one static method, parse(file)
    """
    @staticmethod
    def parse(file) -> dict[int, dict[str, str]]:
        """ Analyze the file object passed as argument.
        :param file: the file object to analyze 
        :return: a dictionary whose keys are the line numbers and values a dictionary with the error code
        and a descriptive message
        """
        errors_found = {}

        blanks = 0
        for i, line in enumerate(file, start=1):
            if is_blank_line(line):
                blanks += 1
                continue

            errors_in_line = {}

            if is_s001(line):
                errors_in_line.update({'S001': 'Too long'})
            if is_s002(line):
                errors_in_line.update({'S002': 'Indentation is not a multiple of four'})
            if is_s003(line):
                errors_in_line.update({'S003': 'Unnecessary semicolon'})
            if is_s004(line):
                errors_in_line.update({'S004': 'At least two spaces required before inline comments'})
            if is_s005(line):
                errors_in_line.update({'S005': 'TODO found'})
            if blanks > 2:
                errors_in_line.update({'S006': 'More than two blank lines used before this line'})
            error_s007 = check_s007(line)
            if error_s007:
                errors_in_line.update({'S007': f"Too many spaces after '{error_s007}'"})
            error_s008 = check_s008(line)
            if error_s008:
                errors_in_line.update({'S008': f"Class name '{error_s008}' should use CamelCase"})
            error_s009 = check_s009(line)
            if error_s009:
                errors_in_line.update({'S009': f"Function name '{error_s009}' should use snake_case"})

            blanks = 0

            if errors_in_line:
                errors_found[i] = dict(sorted(errors_in_line.items()))

        return errors_found
