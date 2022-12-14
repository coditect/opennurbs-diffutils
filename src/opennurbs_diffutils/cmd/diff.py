from argparse import ArgumentParser
from pathlib import Path
import sys

from ..adapter3dm import File3dmDelta
from .common import ConsoleSession, checkForArgument, checkForVersionArgument

PROGRAM_NAME = "3dmdiff"


def main():
    versionParser = checkForVersionArgument(PROGRAM_NAME)
    gitOptionParser, useGit = checkForArgument(
        "--git", help="expect arguments provided to GIT_EXTERNAL_DIFF"
    )

    if useGit:
        procedure = gitExternalDiff
        usage = "%(prog)s --git path oldfile oldhex oldmode newfile newhex newmode"
    else:
        procedure = standardDiff
        usage = "%(prog)s [options] fromfile tofile"

    parser = ArgumentParser(
        prog=PROGRAM_NAME,
        usage=usage,
        description="Find differences between two openNURBS models",
        parents=[versionParser, gitOptionParser],
    )
    procedure(parser)


def gitExternalDiff(parser: ArgumentParser):
    parser.add_argument("path", type=Path)
    parser.add_argument("oldFile", type=Path)
    parser.add_argument("oldHex", type=str)
    parser.add_argument("oldMode", type=str)
    parser.add_argument("newFile", type=Path)
    parser.add_argument("newHex", type=str)
    parser.add_argument("newMode", type=str)
    args = parser.parse_args()

    session = ConsoleSession()

    delta = File3dmDelta()
    delta.comparePaths((args.oldFile, args.newFile), session)
    delta.files[0].label(f"a/{args.path}")
    delta.files[1].label(f"b/{args.path}")
    delta.write(sys.stdout)


def standardDiff(parser: ArgumentParser):
    parser.add_argument("fromfile", type=Path)
    parser.add_argument("tofile", type=Path)
    parser.add_argument(
        "-q", "--brief", action="store_true", help="output only whether files differ"
    )
    parser.add_argument(
        "-s",
        "--report-identical-files",
        action="store_true",
        help="report when two files are the same",
    )
    parser.add_argument(
        "--label", action="append", default=[], help="use LABEL instead of file name"
    )
    args = parser.parse_args()

    session = ConsoleSession()

    delta = File3dmDelta()
    delta.comparePaths((args.fromfile, args.tofile), session)

    if len(args.label) >= 1:
        delta.files[0].label(args.label[0])

    if len(args.label) >= 2:
        delta.files[1].label(args.label[1])

    if delta.hasDifferences:
        if args.brief:
            print(f"Files {delta.files[0].path} and {delta.files[1].path} differ")
        else:
            delta.write(sys.stdout)
        sys.exit(1)
    elif args.report_identical_files:
        print(f"Files {delta.files[0].path} and {delta.files[1].path} are identical")
