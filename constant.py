import keyword
import builtins

PYENV = r'#! /usr/bin/env -S python3 -u'

# Helper
INDENT = 4

# Import Statements
SYS_IMPORT = 'import sys'
GLOB_IMPORT = 'import glob'
OS_IMPORT = 'import os'
SUBPROCESS_IMPORT = 'import subprocess'

# Subset 0
ECHO = r'^echo '
ASSIGN = r'^[a-zA-Z]+[0-9]*=[^=]+$'
VARIABLE = r'\$\{?[a-zA-Z]+[0-9]*\}?'

# Subset 1
GLOB = r'\*|\?|\[|\][^\s]*'
FOR = r'^for '
DO = r'^do$'
DONE = r'^done$'
THEN = r'^then$'
FI = r'^fi$'
EXIT = r'^exit [0-9]*$'
CD = r'cd .*'
READ = r'^read [a-zA-Z]+[0-9]*'

PROCESS = r'^[a-zA-Z]+[0-9]*'

# Subset 2
ARGS = r'\$[0-9]+'
TEST = r'test [^&|]+$'
IF = r'^if '
ELIF = r'^elif '
ELSE = r'^else$'

# Builtins / Keywords
KEYWORDS = keyword.kwlist
BUILTINS = dir(builtins)

SHELL_BUILTINS = ['exit', 'read', 'cd', 'test',
                  'echo', 'for', 'do', 'done', 'then', 'if', 'elif', 'else', 'fi', '#']


# Test Options
COMPARE_OPTIONS = {'-eq': '==', '-ne': '!=',
                   '-gt': '>', '-ge': '>=', '-lt': '<', '-le': '<=', '=': '=='}
