import sys
stdin_fileno=sys.stdin

for line in stdin_fileno:
    if 'exit'==line.strip():
        print('Found exit. Terminating the program')
        exit(0)
    else:
        print('Message from sys.stdin: ---> {} <---'.format(line))