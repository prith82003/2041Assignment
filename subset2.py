import re
import constant
import helper


def args(line: str) -> str:
    """ Convert the accessing of command line arguments to valid python """
    # Looop over for all arguments in line
    while True:
        mObj = re.search(constant.ARGS, line)
        if not mObj:
            break

        # If special argument variable, handle seperately then continue to next
        if mObj.group() == '$#' or mObj.group() == '${#}':
            line = helper.replace_substr_index(
                line, mObj.start(), mObj.end(), '{len(sys.argv[1:])}')
            continue

        if mObj.group() == '$@' or mObj.group() == '${@}':
            line = helper.replace_substr_index(
                line, mObj.start(), mObj.end(), '{" ".join(sys.argv[1:])}')
            continue

        # Get the argument number
        argv = re.search(r'\d+', mObj.group()).group()

        # Replace the substring of the original line with updated python syntax
        line = helper.replace_substr_index(
            line, mObj.start(), mObj.end(), '{' + f'sys.argv[{int(argv)}]' + '}')

    return line


def test(line: str) -> str:
    """ Convert test to valid python syntax """
    # Loop over for all tests in line
    while True:
        # Get the current test and its conditions
        mObj = re.search(constant.TEST, line)
        if not mObj:
            break

        # Get all the seperate words in the test
        match = mObj.group().split()[1:]

        # Check if result needs to be inverted ('!')
        invert = ''
        if match[0] == '!':
            match = match[1:]
            invert = 'not'

        # Check if the next word is an object that is being compared
        first_option = ''
        if not match[0].startswith('-'):
            first_option = match[0]
            match = match[1:]

        # Get the compare type
        compare = match[0]
        match = match[1:]

        # The rest of the string should be joined together
        # to become the other object that is being compared
        cmpObj = ' '.join(match[0:])

        # If the test option is a comparison
        if compare in constant.COMPARE_OPTIONS:
            # Convert to python syntax
            compare = constant.COMPARE_OPTIONS[compare]
            # Replace the substring with valid python syntax
            line = helper.replace_substr_index(
                line, mObj.start(), mObj.end(), f"{invert} '{first_option}' {compare} '{cmpObj}'")
        else:
            # If its a different type of test call helper
            line = extra_tests(line)

    return line


def extra_tests(line: str) -> str:
    """ Handles the Extra Test Cases """

    mObj = re.search(constant.TEST, line)
    test = mObj.group()

    option = test.split()[1]
    obj = test.split()[2]

    # Depending on the case, convert the test option
    # to its python equivalent by calling a function
    if option == '-a' or option == '-e':
        line = helper.replace_substr_index(
            line, mObj.start(), mObj.end(), f'os.access("{obj}", os.F_OK)')
    elif option == '-b':
        line = helper.replace_substr_index(
            line, mObj.start(), mObj.end(), f'stat.S_ISBLK(os.lstat("{obj}").st_mode)')
        pass
    elif option == '-c':
        line = helper.replace_substr_index(
            line, mObj.start(), mObj.end(), f'stat.S_ISCHR(os.lstat("{obj}").st_mode)')
        pass
    elif option == '-d':
        line = helper.replace_substr_index(
            line, mObj.start(), mObj.end(), f'os.path.isdir("{obj}")')
    elif option == '-f':
        line = helper.replace_substr_index(
            line, mObj.start(), mObj.end(), f'os.path.isfile("{obj}")')
    elif option == '-g':
        line = helper.replace_substr_index(
            line, mObj.start(), mObj.end(), f'stat.ST_GID(os.lstat("{obj}").st_mode)')
        pass
    elif option == '-h' or option == '-L':
        line = helper.replace_substr_index(
            line, mObj.start(), mObj.end(), f'stat.S_IFLNK(os.lstat("{obj}").st_mode)')
    elif option == '-k':
        line = helper.replace_substr_index(
            line, mObj.start(), mObj.end(), f'stat.S_ISVTX(os.lstat("{obj}").st_mode)')
    elif option == '-p':
        line = helper.replace_substr_index(
            line, mObj.start(), mObj.end(), f'stat.S_ISFIFO(os.lstat("{obj}").st_mode)')
        pass
    elif option == '-r':
        line = helper.replace_substr_index(
            line, mObj.start(), mObj.end(), f'os.access("{obj}", os.R_OK)')
        pass
    elif option == '-s':
        # Check if obj exists and not empty using python syntax
        line = helper.replace_substr_index(line, mObj.start(), mObj.end(
        ), f"os.path.exists('{obj}'') and os.stat('{obj}').st_size > 0")
    elif option == '-S':
        line = helper.replace_substr_index(
            line, mObj.start(), mObj.end(), f'stat.S_ISSOCK(os.lstat("{obj}").st_mode)')
    elif option == '-u':
        line = helper.replace_substr_index(
            line, mObj.start(), mObj.end(), f'stat.S_ISUID(os.lstat("{obj}").st_mode)')
    elif option == '-w':
        line = helper.replace_substr_index(
            line, mObj.start(), mObj.end(), f'os.access("{obj}", os.W_OK)')
    elif option == '-x':
        line = helper.replace_substr_index(
            line, mObj.start(), mObj.end(), f'os.access("{obj}", os.X_OK)')
    elif option == '-O':
        # Owner
        pass
    elif option == '-G':
        # Group
        pass
    elif option == '-N':
        # Modified
        pass

    return line


def while_loop(line: str) -> str:
    """ Convert while to python syntax """
    condition = line.split()[1:]
    return f'while {condition}:'


def if_statement(line: str) -> str:
    """ Converts if to valid python syntax """
    condition = ' '.join(line.split()[1:])
    return f'if {condition}:'


def elif_statement(line: str) -> str:
    """ Converts if to valid python syntax """
    condition = ' '.join(line.split()[1:])
    return f'elif {condition}:'
