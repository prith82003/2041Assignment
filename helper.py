from io import TextIOWrapper
import constant
import re
import subset0


def replace_str_index(text: str, index=0, replacement=''):
    return '%s%s%s' % (text[:index], replacement, text[index+1:])


def replace_substr_index(text: str, start_index=0, end_index=-1, replacement=''):
    return '%s%s%s' % (text[:start_index], replacement, text[end_index:])


def insert_str(line: str, indx: int, insert_str: str) -> str:
    return '%s%s%s' % (line[:indx], insert_str, line[indx:])


def get_imports(file: TextIOWrapper):
    next(file)
    sys = False
    glob = False
    os = False
    ext_command = False

    variables = []

    for line in file:
        line = line.strip()

        if re.search(constant.EXIT, line) or re.search(constant.ARGS, line):
            sys = True

        if re.search(constant.GLOB, line):
            glob = True

        if re.search(constant.CD, line):
            os = True

        if re.search(constant.ASSIGN, line):
            subset0.assign(line, variables)

        if is_external_command(line, variables):
            ext_command = True

    if sys:
        print(constant.SYS_IMPORT)

    if glob:
        print(constant.GLOB_IMPORT)

    if os:
        print(constant.OS_IMPORT)

    if ext_command:
        print(constant.SUBPROCESS_IMPORT)


def is_external_command(line: str, variables: list[str]) -> bool:
    if not line:
        return False

    match = re.search(constant.PROCESS, line)

    if not match:
        return False
    process = line[match.start():match.end()]

    if process not in variables and process not in constant.SHELL_BUILTINS:
        return True

    return False
