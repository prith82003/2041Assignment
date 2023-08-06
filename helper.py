from io import TextIOWrapper
import constant
import re
import subset0


def replace_str_index(text: str, index=0, replacement=''):
    """ Replace a string or character at a specific index in list """
    return '%s%s%s' % (text[:index], replacement, text[index+1:])


def replace_substr_index(text: str, start_index=0, end_index=-1, replacement=''):
    """ Replace a substring from start to end index """
    return '%s%s%s' % (text[:start_index], replacement, text[end_index:])


def insert_str(line: str, indx: int, insert_str: str) -> str:
    """ Insert a string into a specific index """
    return '%s%s%s' % (line[:indx], insert_str, line[indx:])


def get_imports(file: TextIOWrapper):
    """ Print all the imports needed for a bash file """
    next(file)
    sys = False
    glob = False
    os = False
    ext_command = False
    stat = False

    variables = []

    for line in file:
        line = line.strip()

        # If any command requiring that library is required, set that library as required
        if re.search(constant.EXIT, line) or re.search(constant.ARGS, line) or re.search(constant.NUM_ARGS, line):
            sys = True

        if re.search(constant.GLOB, line):
            glob = True

        if re.search(constant.CD, line):
            os = True

        if re.search(constant.ASSIGN, line):
            subset0.assign(line, variables)

        if re.search(constant.TEST, line) and not set(line.split()).intersection(constant.COMPARE_OPTIONS):
            stat = True
            os = True

        if is_external_command(line, variables):
            ext_command = True

    # Print all the imports required
    if sys:
        print(constant.SYS_IMPORT)

    if glob:
        print(constant.GLOB_IMPORT)

    if os:
        print(constant.OS_IMPORT)

    if ext_command:
        print(constant.SUBPROCESS_IMPORT)

    if stat:
        print(constant.STAT_IMPORT)


def is_external_command(line: str, variables: list[str]) -> bool:
    """ Return if given line contains external command """
    if not line:
        return False

    # Get the first word of the line
    match = re.search(constant.PROCESS, line)

    if not match:
        return False
    process = match.group()

    # If the process is not a variable or a shell builtin/keyword that should be
    # directly translated, return true as an external command
    if process not in variables and process not in constant.SHELL_BUILTINS:
        return True

    return False
