import re
import constant
import helper
import subset1


def echo(line: str) -> str:
    """ Translate echo to valid python syntax """
    end = r'\n'

    # Check for -n option
    if line.split()[1] == '-n':
        # Line should now end on empty string
        end = ''
        # Remove the -n
        line = re.sub('^echo -n', 'echo', line)

    # Interpret the variables into valid python syntax
    printString = ' '.join(line.split()[1:])
    printString = variable(printString)

    # If there is globbing in the print, translate it to valid python syntax
    if re.search(constant.GLOB, line):
        printString = subset1.globstr(printString, var=True)

    # Check if it needs to be an f string
    fstring = ''
    # It only needs to be an f string if it has a variable, uses command line arguments or globbing
    if re.search(constant.VARIABLE, line) or re.search(constant.ARGS, line) or re.search(constant.GLOB, line):
        fstring = 'f'

    # Check if quotes are needed
    quotes = ''
    if not printString.startswith('"') and not printString.startswith("'"):
        quotes = "'"
    return f"print({fstring}{quotes}{printString}{quotes}, end='{end}')"


def assign(line: str, variables: list[str]) -> str:
    """ Intepret the assignment of variable's values """
    # Get the value the variable will be assigned
    line = line.split('=')
    assignment = ' '.join(line[1:])

    # If it has globbing, translate to valid python syntax
    if re.search(constant.GLOB, assignment):
        assignment = subset1.globstr(assignment)

    assignment = assignment.replace('"', '')
    assignment = assignment.replace("'", '')

    # Add the new variable to the list of variables in the program
    variables.append(line[0])

    # Check if it is an f string
    fstring = ''
    if re.search(constant.VARIABLE, assignment) or re.search(constant.ARGS, assignment) or re.search(constant.GLOB, assignment):
        fstring = 'f'

    res = line[0] + f" = {fstring}'" + variable(assignment) + "'"
    return res


def variable(line: str) -> str:
    """ Translate access of variable values to valid python syntax """
    # Loop until all variables in the line are translated
    while True:
        mObj = re.search(constant.VARIABLE, line)
        if not mObj:
            break

        # If variable is in format: '$var'
        if '{' not in mObj.group():
            # Replace $ with {
            line = helper.replace_str_index(line, mObj.start(), '{')
            # Insert } after variable
            line = helper.insert_str(line, mObj.end(), '}')
        else:
            # If variable is in format: '${var}'
            # Only need to remove $
            line = helper.replace_str_index(line, mObj.start(), '')

    return line
