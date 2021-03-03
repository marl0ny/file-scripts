#!/usr/bin/python3
"""
Write a c header file from a c source file.
"""

import re
import sys

if len(sys.argv) != 2:
    sys.exit("Usage: python3 -m write_header [C source file]")
else:
    src_file = sys.argv[1]
    if not re.match(r"[a-z0-9_A-Z]+\.[cC]$", src_file):
        sys.exit("Not a C source file.")

def strip_comments(txt):
    n = len(txt)
    new_txt = ''
    in_long_comment = False
    in_short_comment = False
    for i in range(n):
        if i+2 < n:
            if txt[i:i+2] == "/*":
                in_long_comment = True
            if txt[i:i+2] == "//":
                in_short_comment = True
        if i-2 >= 0:
            if in_long_comment and txt[i-2:i] == "*/":
                in_long_comment = False
        if i-1 >= 0:
            if in_short_comment and txt[i-1] == '\n':
                in_short_comment = False
        if not in_short_comment and not in_long_comment:
            new_txt += txt[i]
    return new_txt

def get_structures(txt):
    structures = []
    parenths = []
    in_structure = False
    in_structure_def = False
    structure = ''
    structure_def = ''
    for i in range(len(txt)):
        if i + 6 < len(txt):
            if txt[i:i+6] == 'struct'  and len(parenths) == 0:
                structure_def_match = re.match(
                    'struct[ ]+[a-zA-Z0-9_]*[^a-zA-Z0-9_]',
                    txt[i::])
                start = structure_def_match.start()
                end = structure_def_match.end()
                structure_def = txt[i+start:i+end]
                in_structure_def = True
            if txt[i] == '{' and in_structure_def:
                in_structure = True
                in_structure_def = False
            if (in_structure and txt[i-2:i] == '};' 
                and len(parenths) == 0):
                in_structure = False
                structures.append(structure_def + structure)
                structure = ''
            if in_structure:
                structure += txt[i]
            if txt[i] == '{':
                parenths.append('{')
            if txt[i] == '}':
                parenths.pop()
    return structures


with open(src_file, 'r') as f:
    txt = f.read()
    txt = strip_comments(txt)
    structures = get_structures(txt)
    define_macros = re.findall(r"#define [a-zA-Z_0-9 ^#]*", txt)
    txt = re.sub('#[ ]*[a-zA-Z]*', '', txt)
    txt = txt.replace('\n', '')
    typedefs = re.findall(r"typedef[^;]*;", txt)
    prototypes = re.findall(r"[a-z0-9_]+[ ]+[a-z0-9_]+[ ]*\([^\(\)]*\)[ ]*{", txt)
    prototypes = [p.strip().strip('{') + ';' for p in prototypes]
    h_file = src_file.strip(".c") + ".h"
    h_guard = "__" + src_file.strip(".c").upper() + "__"
    with open(h_file, 'w') as f:
        f.write("#ifdef __cplusplus\nextern \"C\" {\n#endif\n")
        f.write("#ifndef " + h_guard + "\n")
        f.write("#define " + h_guard + "\n\n")
        for d in define_macros:
            f.write(d + '\n')
        f.write('\n')
        for t in typedefs:
            f.write(t + '\n')
        f.write('\n')
        for s in structures:
            f.write(s + '\n\n')
        f.write('\n')
        for p in prototypes:
            f.write(p + "\n")
        f.write("\n#endif\n")
        f.write("#ifdef __cplusplus\n}\n#endif\n")
