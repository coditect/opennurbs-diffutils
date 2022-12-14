from argparse import ArgumentParser
from pathlib import Path
import subprocess


def makeabs(path):
    return path if path.is_absolute() else Path.cwd() / path


parser = ArgumentParser()
parser.add_argument("old", type=Path)
parser.add_argument("mine", type=Path)
parser.add_argument("theirs", type=Path)
parser.add_argument("dest", type=Path)
args = parser.parse_args()

old = makeabs(args.old)
mine = makeabs(args.mine)
theirs = makeabs(args.theirs)
dest = makeabs(args.dest)

here = Path(__file__).parent

completed = subprocess.run(
    ["poetry", "run", "3dmdiff3", "-m", "-o", dest, mine, old, theirs], cwd=here
)
exit(completed.returncode)
