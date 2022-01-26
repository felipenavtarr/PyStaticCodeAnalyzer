from analyzer_engine import Analyzer, messages
import sys
import os

# Filter arguments
files_to_parse = []
for name in sys.argv[1:]:
    if os.path.isfile(name):
        if name.endswith('.py'):
            files_to_parse.append(name)
        else:
            print(f'{name}: not a python file')
    elif os.path.isdir(name):
        for x in os.listdir(name):
            if os.path.splitext(x)[1] == '.py':
                files_to_parse.append(os.path.join(name, x))
    else:
        print(f'{name}: is not a file or a directory')

# Analyze the selected files
for target_path in sorted(files_to_parse, key=os.path.basename):
    with open(target_path, 'r') as file:
        results = Analyzer.parse(file)

    # print results
    if results:
        for line, errors in results.items():
            for error in errors:
                print(f'{target_path}: Line {line}: {error} {messages[error]}')
    else:
        print(f'{target_path}: No errors found')
