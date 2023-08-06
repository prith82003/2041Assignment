import constant
import re
import helper
import subset0


def globstr(line: str, var=False) -> str:
    """ Convert globbing to valid python syntax """
    newline = line
    i = 0

    # To be safe in case infinite loop occurs
    while i < 1000:
        globObj = re.search(constant.GLOB, newline)
        newGlob = ''

        if not globObj:
            break

        # To offset since capture begins before glob string
        offset = 0
        if globObj.group()[0] not in ['*', '[', ']', '?']:
            offset = 1

        # Translate the glob to python syntax as either list or joined string
        if not var:
            newGlob = f'sorted(glob.glob("{newline[globObj.start() + offset:globObj.end()]}"))'
        else:
            newGlob = '{' + \
                f'" ".join(sorted(glob.glob("{newline[globObj.start() + offset:globObj.end()]}")))' + '}'

        # Replace the substring in the line which contains the globbing with the python version
        newline = helper.replace_substr_index(
            newline, globObj.start() + offset, globObj.end(), newGlob)
        i += 1

    return newline


def forloop(line: str) -> str:
    """ Converts for into valid python syntax """
    words = line.split()

    # Gets the iterator variable
    iterator = words[1]

    # Gets the variable that is being enumerated over
    enumerable = words[3:]
    enumerable = ' '.join(enumerable)

    fstring = ''
    if re.search(constant.VARIABLE, enumerable) or re.search(constant.ARGS, enumerable) or re.search(constant.GLOB, enumerable):
        fstring = 'f'

    # If it is a glob statement, translate
    if re.search(constant.GLOB, line):
        enumerable = globstr(' '.join(words[3:]), True)

    # Add quotes if necessary
    quotes = ''
    if not enumerable.startswith('"') and not enumerable.startswith("'"):
        quotes = "'"

    # Interpret variables in condition
    enumerable = subset0.variable(enumerable)

    # Split the enumerable so that words are iterated over
    return f"for {iterator} in {fstring}{quotes}{enumerable}{quotes}.split():"


def cd(line: str) -> str:
    """ Translate cd into valid python syntax """
    # Get location and chdir into it
    loc = ' '.join(line.split()[1:])
    return f'os.chdir("{loc}")'


def read(line: str) -> str:
    """ Read input from stdin """
    var = line.split()[1]
    return f'{var} = input()'


def external_command(line: str) -> str:
    """ Call external command in valid python syntax """
    # If it has glob statement
    if re.search(constant.GLOB, line):
        return f'subprocess.call("{line}", shell=True)'

    return f'subprocess.call({line.split()})'


def exit(line: str) -> str:
    """ Convert exit to valid python syntax """
    arg = ''

    # Get exit code if any
    if len(line.split()) > 1:
        arg = line.split()[1]

    # Exit with code
    return f'sys.exit({arg})'
