import sys
import re
import glob
import os


RE_IGNORE_PROG = re.compile(
    "(?:program|\\.wasm$|\\.wasm\\.js$|main\\.js$|"
    "/\\.git$|/\\.git/|"
    "\\.zip$|\\.png$|\\.jpg$|\\.gif$|\\.mem$)")


def get_output_fname(input_fname: str, xor_key: int) -> str:
    output_fname_characters = []
    rel_dir_path_match = re.match('^\\./', input_fname)
    re_prog = re.compile('[a-zA-Z0-9\\-_\\.]')
    for i, c in enumerate(input_fname):
        c2 = str(bytes([c.encode()[0]^xor_key])).strip('b').strip("'")
        if i == 0 and rel_dir_path_match is not None:
            output_fname_characters.append(c)
        elif c != '/' and re_prog.match(c2) is not None:
            output_fname_characters.append(c2)
        else:
            output_fname_characters.append(c)
    return ''.join(output_fname_characters)


def xor_each_byte(input_fname: str, xor_key: int):
    output_fname = get_output_fname(input_fname, xor_key)
    with open(input_fname, 'rb') as f:
        bytes_arr = bytes([b^xor_key for b in f.read()])
    with open(output_fname, 'wb') as f:
        f.write(bytes_arr)


def xor_directory(dir_path: str, xor_key: int):
    dir_path_rec = dir_path + "**" if \
        dir_path.endswith("/") else dir_path + "/**"
    if dir_path_rec[0] != '.' and dir_path_rec[0] != '/':
        dir_path_rec = './' + dir_path_rec
    fnames = glob.glob(dir_path_rec, recursive=True, include_hidden=True)
    for fname in fnames:
        if not RE_IGNORE_PROG.findall(fname):
            if not os.path.isdir(fname):
                xor_each_byte(fname, xor_key)
            else:
                os.mkdir(get_output_fname(fname, xor_key))


if __name__ == "__main__":
    input_fname, xor_key \
        = sys.argv[1], int(sys.argv[2])
    xor_key = abs(xor_key) % 256
    if os.path.isdir(input_fname):
        xor_directory(input_fname, xor_key)
    else:
        xor_each_byte(input_fname, xor_key)
