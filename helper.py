import constant
import re


def replace_str_index(text, index=0, replacement=''):
    return '%s%s%s' % (text[:index], replacement, text[index+1:])


def get_imports(file):

    next(file)
    sys = False

    for line in file:
        if re.search(constant.EXIT, line):
            sys = True

    if sys:
        print(constant.SYS)
