from argparse import ArgumentParser
from pathlib import Path
import subprocess

# path old-file old-hex old-mode new-file new-hex new-mode

parser = ArgumentParser()
parser.add_argument("path", type=Path)
parser.add_argument("old_file", type=Path)
parser.add_argument("old_hex", type=str)
parser.add_argument("old_mode", type=str)
parser.add_argument("new_file", type=Path)
parser.add_argument("new_hex", type=str)
parser.add_argument("new_mode", type=str)
args = parser.parse_args()

old_file = args.old_file if args.old_file.is_absolute() else Path.cwd() / args.old_file
new_file = args.new_file if args.new_file.is_absolute() else Path.cwd() / args.new_file

# print(old_file)
# print(new_file)

here = Path(__file__).parent
# print(here)

subprocess.run(["poetry", "run", "3dmdiff", old_file, new_file], cwd=here)
