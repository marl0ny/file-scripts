import sys
import re
import os


RE_DIR_PROG = re.compile("^DIRECTORY:")
RE_FILE_PROG = re.compile("^FILE:")
RE_LINE_PROG = re.compile("^ {10,}")


def get_files_from_merged(merged_file: str):
    lines = []
    with open(merged_file, 'r') as f:
        for line in f:
            lines.append(line)
    for i, line in enumerate(lines):
        if RE_DIR_PROG.findall(line):
            os.mkdir(line.strip("DIRECTORY:").strip('\n').strip(' '))
        if RE_FILE_PROG.findall(line):
            j = i + 1 if (i + 1) < len(lines) else i
            fname_mode = line.strip("FILE:").strip('\n').strip(' ')
            fname, mode = fname_mode.split('\t')
            with open(fname, "w") as f:
                while RE_LINE_PROG.findall(lines[j]) and j < len(lines):
                    f.write(lines[j][10:])
                    j += 1
            os.chmod(fname,int(mode))


if __name__ == "__main__":
    merged_file = sys.argv[1]
    get_files_from_merged(merged_file)

