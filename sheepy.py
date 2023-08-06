#! /usr/bin/env python3
import constant
import subset0
import subset1
import subset2
import helper
import sys
import re

# Print Header
print(constant.PYENV)
indentLevel = 0
variables = []

with open(sys.argv[1], 'r') as file:
    # Print all the imports
    helper.get_imports(file)
    file.seek(0)
    next(file)

    # Iterate through each line of file
    for line in file:
        line = line.strip()
        line = line.replace(';', '')

        # Unindent if 'elif' or 'else'
        ifindent = 0

        # Keep track of commented section of line
        commented = ''

        # Search for # to check comment
        obj = re.search(r'\s(?!\s*[\$]\s*)\s*#\s*', line)
        if obj:
            commented = line[obj.start():]
            line = line[:obj.start()]

        # If line is empty, print only comment and continue to next line
        if not line:
            print((' ' * constant.INDENT * (indentLevel + ifindent)) + commented)
            continue

        # If Do/Then or Done/Fi Indent or Unindent line as necessary, continue to next line
        if re.search(constant.DO, line) or re.search(constant.THEN, line):
            indentLevel += 1
            continue

        if re.search(constant.DONE, line) or re.search(constant.FI, line):
            indentLevel -= 1
            continue

        # Regex search for each case
        if re.search(constant.ASSIGN, line):
            # Hold the partially translated variable back in line
            line = subset0.assign(line, variables)

        # Continue to translate line
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

        # Once line is fully translated, print it
        # The ' ' is multiplied by the indent level and then by 4, to indent to correct level
        # Then the translated line is printed, followed by the comment
        print((' ' * constant.INDENT * (indentLevel + ifindent)) + (line + commented))
