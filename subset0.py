import re
import constant
import helper


def echo(line):
    line = line.replace('"\'', '')
    printString = line.split()[1:]

    for i, word in enumerate(printString):
        if re.search(constant.VARIABLE, word):
            printString[i] = '{' + word[1:] + '}'

    printString = ' '.join(printString)
    return "print(f'" + printString + "')"


def assign(line):
    line = line.split('=')

    assignment = ' '.join(line[1:])
    assignment = assignment.replace('"', '')
    assignment = assignment.replace("'", '')

    if not re.search(constant.VARIABLE, assignment):
        return line[0] + " = '" + assignment + "'"

    res = line[0] + " = f'" + variable(assignment) + "'"
    return res


def variable(line):
    while True:
        mObj = re.search(constant.VARIABLE, line)
        if not mObj:
            break

        line = helper.replace_str_index(line, mObj.span()[0], '{')
        if mObj.span()[1] >= len(line):
            line += '}'
        else:
            line = line[:mObj.span()[1]] + \
                '}' + line[mObj.span()[1]:]

    return line
