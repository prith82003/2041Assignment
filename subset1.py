import constant
import re
import glob


def globstr(line: str) -> str:
    words = line.split()

    for idx, word in enumerate(words):
        if re.search(constant.GLOB, word):
            globbed = glob.glob(word)
            words[idx] = ' '.join(globbed)

    return ' '.join(words)


def forloop(line: str) -> str:
    if re.search(constant.GLOB, line):
        line = globstr(line)

    words = line.split()
    iterator = words[1]
    enumerable = words[3:]

    return f'for {iterator} in {enumerable}:'


def exit(line):
    arg = line.split()[1]
    return f'sys.exit({arg})'
