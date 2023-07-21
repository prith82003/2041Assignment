#! /usr/bin/env -S python3 -u
import sys
a = 'hello '
b = 'world'

test = f'{a}{b}'

str = f'Sentence: {a} {b}'

for file in ['constant.py', 'sheepy.py', 'subset1.py', 'subset0.py', 'helper.py', 'out.py', 'test.py']:
    print(f'{file}')

sys.exit(1)
