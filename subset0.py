import re
import constant
import helper


def echo(line: str) -> str:
    line = line.replace('"', '')
    line = line.replace("'", '')

    printString = ' '.join(line.split()[1:])
    printString = variable(printString)

    fstring = ''
    if re.search(constant.VARIABLE, line) or re.search(constant.ARGS, line):
        fstring = 'f'

    return f"print({fstring}'{printString}')"


def assign(line: str, variables: list[str]) -> str:
    line = line.split('=')

    assignment = ' '.join(line[1:])
    assignment = assignment.replace('"', '')
    assignment = assignment.replace("'", '')
    variables.append(line[0])

    if not re.search(r'\$[a-zA-Z0-9]+', assignment):
        return line[0] + " = '" + assignment + "'"

    res = line[0] + " = f'" + variable(assignment) + "'"
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
