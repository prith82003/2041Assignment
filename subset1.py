import subprocess
import constant
import re
import helper


def globstr(line: str, var=False) -> str:
    globObj = re.search(constant.GLOB, line)
    newGlob = ''

    if not var:
        newGlob = f'sorted(glob.glob("{line[globObj.start():globObj.end()]}"))'
    else:
        newGlob = '{' + \
            f'" ".join(sorted(glob.glob("{line[globObj.start():globObj.end()]}")))' + '}'
    newline = helper.replace_substr_index(
        line, globObj.start(), globObj.end(), newGlob)

    return newline


def forloop(line: str) -> str:
    words = line.split()
    iterator = words[1]

    enumerable = ''

    if re.search(constant.GLOB, line):
        enumerable = globstr(' '.join(words[3:]))
    else:
        enumerable = words[3:]

    return f'for {iterator} in {enumerable}:'


def cd(line: str) -> str:
    loc = ' '.join(line.split()[1:])
    return f'os.chdir("{loc}")'


def read(line: str) -> str:
    var = line.split()[1]
    return f'{var} = input()'


def external_command(line: str) -> str:
    if re.search(constant.GLOB, line):
        return f'subprocess.call("{line}", shell=True)'

    return f'subprocess.call({line.split()})'


def exit(line: str) -> str:
    arg = ''
    if len(line.split()) > 1:
        arg = line.split()[1]

    return f'sys.exit({arg})'
