import sys
import re
import glob
import os


RE_IGNORE_PROG = re.compile(
    "(?:program|\\.wasm$|\\.wasm\\.js$|main\\.js$|"
    "/\\.git$|/\\.git/|\\.png$|\\.jpg$|\\.gif$|\\.mem$)")


def merge_files_to_single(dir_path: str, output_fname: str):
    lines = []
    dir_path_rec = dir_path + "**" if \
            dir_path.endswith("/") else dir_path + "/**"
    if dir_path_rec[0] != '.' and dir_path_rec[0] != '/':
        dir_path_rec = './' + dir_path_rec
    print(dir_path_rec)
    fnames = glob.glob(dir_path_rec, recursive=True, include_hidden=True)
    for fname in fnames:
        print(fname)
        if not RE_IGNORE_PROG.findall(fname):
            if not os.path.isdir(fname):
                lines.append('FILE: ' + fname + '\n')
                with open(fname, 'r') as f:
                    for line in f:
                        lines.append('          ' + line)
                    lines.append('\n')
            else:
                lines.append('DIRECTORY: ' + fname + '\n')
    with open(output_fname, 'w') as f:
        for line in lines:
            f.write(line)


if __name__ == "__main__":
    dir_path, output_fname = sys.argv[1], sys.argv[2]
    if os.path.isdir(dir_path):
        merge_files_to_single(dir_path, output_fname)

