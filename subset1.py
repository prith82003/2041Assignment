import subprocess
import constant
import re
import helper


def globstr(line: str) -> str:
    globObj = re.search(constant.GLOB, line)

    newGlob = f'sorted(glob.glob("{line[globObj.start():globObj.end()]}"))'
    newline = line[:globObj.start() - 1] + ''.join(newGlob) + \
        line[globObj.end():]
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
    # TODO: Handle Globbing

    return f'subprocess.call({line.split()})'


def exit(line: str) -> str:
    arg = line.split()[1]
    return f'sys.exit({arg})'
