messages = {'S001': 'Too long', 'S002': 'Indentation is not a multiple of four', 'S003': 'Unnecessary semicolon',
            'S004': 'At least two spaces required before inline comments', 'S005': 'TODO found',
            'S006': 'More than two blank lines used before this line'}


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


class Analyzer:
    """Analyzes a file object.
    Has only one static method, parse(file)
    """
    @staticmethod
    def parse(file):
        """ Analyze the file object passed as argument.
        :param file: the file object to analyze 
        :return: a dictionary whose keys are the line numbers and values a list with the error codes in that line
        """
        errors_found = {}

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

        return errors_found
