#! /usr/bin/env python3
import constant
import subset0
import subset1
import helper
import sys
import re

print(constant.PYENV)
indentLevel = 0

#! Handle Comment Cases
with open(sys.argv[1], 'r') as file:

    helper.get_imports(file)
    file.seek(0)
    next(file)

    for line in file:
        line = line.strip()
        if re.search(constant.DO, line) or re.search(constant.THEN, line):
            indentLevel += 1
            continue

        if re.search(constant.DONE, line) or re.search(constant.FI, line):
            indentLevel -= 1
            continue

        if re.search(constant.ECHO, line):
            line = subset0.echo(line)

        if re.search(constant.ASSIGN, line):
            line = subset0.assign(line)

        if re.search(constant.FOR, line):
            line = subset1.forloop(line)

        if re.search(constant.EXIT, line):
            line = subset1.exit(line)

        print((' ' * constant.INDENT * indentLevel) + line)
