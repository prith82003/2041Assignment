import re
import constant
import helper
import subset1


def echo(line: str) -> str:
    line = line.replace('"', '')
    line = line.replace("'", '')

    printString = ' '.join(line.split()[1:])

    printString = variable(printString)

    if re.search(constant.GLOB, line):
        printString = subset1.globstr(printString, var=True)

    fstring = ''
    if re.search(constant.VARIABLE, line) or re.search(constant.ARGS, line) or re.search(constant.GLOB, line):
        fstring = 'f'

    return f"print({fstring}'{printString}')"


def assign(line: str, variables: list[str]) -> str:
    line = line.split('=')

    assignment = ' '.join(line[1:])

    if re.search(constant.GLOB, assignment):
        assignment = subset1.globstr(assignment)

    assignment = assignment.replace('"', '')
    assignment = assignment.replace("'", '')
    variables.append(line[0])

    fstring = ''
    if re.search(constant.VARIABLE, assignment) or re.search(constant.ARGS, assignment) or re.search(constant.GLOB, assignment):
        fstring = 'f'

    res = line[0] + f" = {fstring}'" + variable(assignment) + "'"
    return res


def variable(line: str) -> str:
    while True:
        mObj = re.search(constant.VARIABLE, line)
        if not mObj:
            break

        if '{' not in mObj.group():
            line = helper.replace_str_index(line, mObj.start(), '{')
            line = helper.insert_str(line, mObj.end(), '}')
        else:
            line = helper.replace_str_index(line, mObj.start(), '')

    return line
