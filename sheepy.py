#! /usr/bin/env python3
import constant
import subset0
import subset1
import subset2
import helper
import sys
import re

print(constant.PYENV)
indentLevel = 0
variables = []

#! Handle Comment Cases
with open(sys.argv[1], 'r') as file:
    helper.get_imports(file)
    file.seek(0)
    next(file)

    for line in file:
        line = line.strip()
        ifindent = 0
        commented = ''

        obj = re.search(r'\s*#', line)
        if obj:
            commented = line[obj.start():]
            line = line[:obj.start()]

        if not line:
            print((' ' * constant.INDENT * (indentLevel + ifindent)) + commented)
            continue

        if re.search(constant.DO, line) or re.search(constant.THEN, line):
            indentLevel += 1
            continue

        if re.search(constant.DONE, line) or re.search(constant.FI, line):
            indentLevel -= 1
            continue

        if re.search(constant.ASSIGN, line):
            line = subset0.assign(line, variables)

        if helper.is_external_command(line, variables):
            line = subset1.external_command(line)
            print((' ' * constant.INDENT * indentLevel) + line)
            continue

        if re.search(constant.FOR, line):
            line = subset1.forloop(line)

        if re.search(constant.ECHO, line):
            line = subset0.echo(line)

        if re.search(constant.READ, line):
            line = subset1.read(line)

        if re.search(constant.EXIT, line):
            line = subset1.exit(line)

        if re.search(constant.CD, line):
            line = subset1.cd(line)

        if re.search(constant.ARGS, line):
            line = subset2.args(line)

        if re.search(constant.TEST, line):
            line = subset2.test(line)

        if re.search(constant.WHILE, line):
            line = subset2.while_loop(line)

        if re.search(constant.IF, line):
            line = subset2.if_statement(line)

        if re.search(constant.ELIF, line):
            line = subset2.elif_statement(line)
            indentLevel -= 1

        if re.search(constant.ELSE, line):
            line = 'else:'
            ifindent = -1

        print((' ' * constant.INDENT * (indentLevel + ifindent)) + (line + commented))
