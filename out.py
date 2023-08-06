#! /usr/bin/env -S python3 -u
import glob

for i in '1 2 3 4 5 6'.split():
    print(f'{i}', end='\n')
    for file in f'{" ".join(sorted(glob.glob("*")))}'.split():
        print(f'{file}', end='\n')
