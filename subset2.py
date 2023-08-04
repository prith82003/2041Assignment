import re
import constant
import helper


def args(line: str) -> str:
    while True:
        mObj = re.search(constant.ARGS, line)
        if not mObj:
            break

        argv = re.search(r'\d+', mObj.group()).group()

        line = helper.replace_str_index(line, mObj.start(), '{')
        line = helper.replace_substr_index(
            line, mObj.start(), mObj.end(), '{' + f'sys.argv[{int(argv)}]' + '}')

    return line


def test(line: str) -> str:
    while True:
        mObj = re.search(constant.TEST, line)
        if not mObj:
            break

        match = mObj.group().split()[1:]

        invert = ''
        if match[0] == '!':
            match = match[1:]
            invert = 'not'

        first_option = ''
        if not match[0].startswith('-'):
            first_option = match[0]
            match = match[1:]

        compare = match[0]
        match = match[1:]

        cmpObj = ' '.join(match[0:])

        if compare in constant.COMPARE_OPTIONS:
            compare = constant.COMPARE_OPTIONS[compare]
            line = helper.replace_substr_index(
                line, mObj.start(), mObj.end(), f"{invert} '{first_option}' {compare} '{cmpObj}'")
        else:
            line = extra_tests(line)

    return line


def extra_tests(line: str) -> str:
    mObj = re.search(constant.TEST, line).group()
    test = mObj.group()

    option = test.split()[1]
    obj = test.split()[2]

    if option == '-a' or option == '-e':
        line = helper.replace_substr_index(
            line, mObj.start(), mObj.end(), f'os.access({obj}, os.F_OK)')
    elif option == '-b':
        # Block Special
        pass
    elif option == '-c':
        # Character Special
        pass
    elif option == '-d':
        line = helper.replace_substr_index(
            line, mObj.start(), mObj.end(), f'os.path.isdir({obj})')
    elif option == '-f':
        line = helper.replace_substr_index(
            line, mObj.start(), mObj.end(), f'os.path.isfile({obj})')
    elif option == '-g':
        # Group ID
        pass
    elif option == '-h' or option == '-L':
        # Symbolic Link
        pass
    elif option == '-k':
        # Sticky Bit
        pass
    elif option == '-p':
        # Pipe
        pass
    elif option == '-r':
        # Readable
        pass
    elif option == '-s':
        # Check if obj exists and not empty using python syntax
        line = helper.replace_substr_index(
            line, mObj.start(), mObj.end(), f"os.path.exists({obj}) and os.stat({obj}).st_size > 0")
    elif option == '-S':
        # Socket
        pass
    elif option == '-t':
        # Open in terminal
        pass
    elif option == '-u':
        # setuid bit
        pass
    elif option == '-w':
        # Write Perms
        pass
    elif option == '-x':
        # Executable
        pass
    elif option == '-O':
        # Owner
        pass
    elif option == '-G':
        # Group
        pass
    elif option == '-N':
        # Modified
        pass
    elif option == 'nt':
        # newwer than
        pass

    return line


def while_loop(line: str) -> str:
    condition = line.split()[1:]
    return f'while {condition}:'


def if_statement(line: str) -> str:
    condition = ' '.join(line.split()[1:])
    return f'if {condition}:'


def elif_statement(line: str) -> str:
    condition = ' '.join(line.split()[1:])
    return f'elif {condition}:'
