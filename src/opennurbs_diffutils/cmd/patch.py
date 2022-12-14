from argparse import ArgumentParser
from pathlib import Path
import sys
from typing import TextIO

import rhino3dm

from ..abstractmodel import Session
from ..adapter3dm import File3dmDelta
from .common import ConsoleSession, checkForVersionArgument

PROGRAM_NAME = "3dmpatch"


def readPatch(input: TextIO, session: Session) -> File3dmDelta:
    delta = File3dmDelta()
    # try:
    delta.read(input)
    return delta
    # except ParseError as e:
    #     session.fatal(f"Error on line {e.lineNumber}: {e.__context__.args[0]}")


def main():
    parser = ArgumentParser(
        prog=PROGRAM_NAME,
        usage="%(prog)s [options] [originalfile [patchfile]]",
        description="Apply a delta to an openNURBS model",
        parents=[checkForVersionArgument(PROGRAM_NAME)],
    )
    parser.add_argument(
        "originalfile", type=Path, nargs="?", help="The model to be patched"
    )
    parser.add_argument(
        "patchfile",
        type=Path,
        nargs="?",
        default="-",
        help="The file containing the delta",
    )
    parser.add_argument("-o", "--output", type=Path, metavar="FILE")
    parser.add_argument("-R", "--reverse", action="store_true")
    args = parser.parse_args()

    # Consider implementing:
    # -f, --force               Assume that the user knows exactly what he or she is doing, and do not ask any questions
    # -r, --reject-file         Use reject-file as the reject file name
    # -s, --quiet, --silent     Work silently unless an error occurs
    # -t, --batch               Do not ask any questions
    # -T, --set-time            Set the modification and access times of patched files from timestamps given in context diff headers, assuming that the context diff headers use local time
    # --verbose                 Print more diagnostics than usual
    # -Z, --set-utc             Set the modification and access times of patched files from timestamps given in context diff headers, assuming that the context diff headers use UTC

    session = ConsoleSession()

    if str(args.patchfile) == "-":
        delta = readPatch(sys.stdin, session)
        # Return stdin to the terminal in case we need interactive input
        sys.stdin = open("/dev/tty", "r")
    else:
        with open(args.patchfile, "r", encoding="utf-8") as file:
            delta = readPatch(file, session)

    if args.reverse:
        delta = delta.reverse()

    inputPath = args.originalfile if args.originalfile else delta.files[0].path
    model = rhino3dm.File3dm.Read(str(inputPath))
    if model is None:
        session.fatal(f"Failed to read file {inputPath}")

    delta.apply(model, session)

    outputPath = args.output if args.output else inputPath

    success = model.Write(str(outputPath), 6)  # Hard-coded to v6 for now
    if not success:
        session.fatal(f"Failed to write to file {outputPath}")
