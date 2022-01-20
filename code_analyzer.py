MAX_CHAR = 79
CODE = 'S001'
MESSAGE = 'Line too long'

path_to_file = input()
file = open(path_to_file, 'r')
for i, line in enumerate(file, start=1):
    if len(line) > MAX_CHAR:
        print(f'Line {i}: {CODE} {MESSAGE}')
file.close()
