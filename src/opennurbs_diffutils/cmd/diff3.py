from argparse import ArgumentParser
from pathlib import Path
import sys
import rhino3dm

from ..adapter3dm import File3dmDelta
from .common import ConsoleSession, checkForVersionArgument

PROGRAM_NAME = "3dmdiff3"


def main():
    parser = ArgumentParser(
        prog=PROGRAM_NAME,
        usage="%(prog)s [options] myfile oldfile yourfile",
        description="Find differences between two openNURBS models with a common ancestor",
        parents=[checkForVersionArgument(PROGRAM_NAME)],
    )
    parser.add_argument("myfile", type=Path)
    parser.add_argument("oldfile", type=Path)
    parser.add_argument("yourfile", type=Path)
    parser.add_argument("-m", "--merge", action="store_true")
    parser.add_argument("-o", "--output", type=Path, metavar="FILE")
    args = parser.parse_args()

    session = ConsoleSession()

    mine = File3dmDelta()
    mine.comparePaths((args.oldfile, args.myfile), session)

    yours = File3dmDelta()
    yours.comparePaths((args.oldfile, args.yourfile), session)

    merged = mine.merge(yours, session)

    if args.merge:
        session = ConsoleSession()
        model = rhino3dm.File3dm.Read(str(args.oldfile))
        if model is None:
            session.fatal(f"Failed to read file {args.oldfile}")

        merged.apply(model, session)

        outputPath = args.output if args.output else args.oldfile

        success = model.Write(str(outputPath), 6)  # Hard-coded to v6 for now
        if not success:
            session.fatal(f"Failed to write to file {args.output}")

    else:
        merged.write(sys.stdout)
