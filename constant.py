PYENV = r"#! /usr/bin/env -S python3 -u"

# Helper
INDENT = 4
SYS = 'import sys'

# Subset 0
ECHO = r'^echo'
ASSIGN = r'^[^=]+=[^=]+$'
VARIABLE = r'\$[^\$ ]+'

# Subset 1
GLOB = r'\*|\?|\[|\]'
FOR = r'^for'
DO = r'^do$'
DONE = r'^done$'
THEN = r'^then$'
FI = r'^fi$'
EXIT = '^exit [0-9]*$'
