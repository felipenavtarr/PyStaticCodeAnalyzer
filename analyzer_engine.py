import re
import ast


def is_blank_line(line):
    return not line.strip()


def is_s001(line):
    max_char_per_line = 79
    return len(line) > max_char_per_line


def is_s002(line):
    tab_size = 4
    return (len(line) - len(line.lstrip())) % tab_size != 0


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
    if re.match(pattern, line) and line.lstrip().split(' ')[1] == '':
        return line.split()[0]
    return None


def is_snake_case(x):
    snake_case_pattern = r'^[_a-z][_a-z0-9]*$'
    return re.match(snake_case_pattern, x)


def is_camel_case(x):
    camel_case_pattern = r'^[A-Z][a-z0-9]*[A-Za-z0-9]*$'
    return re.match(camel_case_pattern, x)


class AstChecker(ast.NodeVisitor):

    def __init__(self, errors_prev):
        self.errors = errors_prev

    def get_errors(self):
        for k, v in self.errors.items():
            self.errors[k] = sorted(v)

        return dict(sorted(self.errors.items()))

    def update_errors(self, num_line, error):
        if num_line in self.errors.keys():
            self.errors[num_line].append(error)
        else:
            self.errors.update({num_line: [error]})

    # S008
    def visit_ClassDef(self, node):
        if not is_camel_case(node.name):
            self.update_errors(node.lineno, ('S008', f"in column {node.col_offset + 1}:"
                                                     f" Class name '{node.name}' should use CamelCase"))
        self.generic_visit(node)

    # S009 & S010 & S011 & S012
    def visit_FunctionDef(self, node):
        # S009
        if not is_snake_case(node.name):
            self.update_errors(node.lineno, ('S009', f"in column {node.col_offset + 1}:"
                                                     f" Function name '{node.name}' should use snake_case"))

        # S010
        for item in node.args.args:
            if not is_snake_case(item.arg):
                self.update_errors(item.lineno, ('S010', f"in column {item.col_offset + 1}:"
                                                         f" Argument name '{item.arg}' should be snake_case"))

        # S011
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        name = target.id
                    elif isinstance(target, ast.Attribute):
                        name = target.attr
                    if not is_snake_case(name):
                        self.update_errors(target.lineno, ('S011', f"in column {target.col_offset + 1}:"
                                                                   f" Variable '{name}' in function "
                                                                   f"should be snake_case"))

        # S012
        for item in node.args.defaults:
            if isinstance(item, (ast.List, ast.Dict, ast.Set)):
                self.update_errors(item.lineno, ('S012', f"in column {item.col_offset + 1}:"
                                                         f" The default argument value is mutable"))
                break

        self.generic_visit(node)


class Analyzer:
    """Analyzes a file object.
    Has only one static method, scan(file)
    """
    @staticmethod
    def scan(file) -> dict[int, list[tuple]]:
        """ Analyze the file object passed as argument.
        :param file: the file object to analyze 
        :return: a dictionary whose keys are the line numbers and values a list of tuples each containing the error
        code and a descriptive message
        """
        errors_found = {}

        blanks = 0
        for i, line in enumerate(file, start=1):
            if is_blank_line(line):
                blanks += 1
                continue

            errors_in_line = []

            if is_s001(line):
                errors_in_line.append(('S001', 'Too long'))
            if is_s002(line):
                errors_in_line.append(('S002', 'Indentation is not a multiple of four'))
            if is_s003(line):
                errors_in_line.append(('S003', 'Unnecessary semicolon'))
            if is_s004(line):
                errors_in_line.append(('S004', 'At least two spaces required before inline comments'))
            if is_s005(line):
                errors_in_line.append(('S005', 'TODO found'))
            if blanks > 2:
                errors_in_line.append(('S006', 'More than two blank lines used before this line'))
            error_s007 = check_s007(line)
            if error_s007:
                errors_in_line.append(('S007', f"Too many spaces after '{error_s007}'"))

            blanks = 0

            if errors_in_line:
                errors_found[i] = errors_in_line

        file.seek(0)
        tree = ast.parse(file.read())
        ast_checker = AstChecker(errors_found)
        ast_checker.visit(tree)

        return ast_checker.get_errors()
