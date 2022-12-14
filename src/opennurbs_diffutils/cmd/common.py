from argparse import ArgumentParser
from sys import exit, stderr
from colorama import Fore, Style
from ..abstractmodel import Session


def print_version(programName):
    import importlib.metadata

    version = importlib.metadata.version("3dmdiff")
    print(f"{programName} {version}")
    # v2 = importlib.metadata.version("rhino3dm")
    exit()


def checkForArgument(*names, help=None) -> tuple[ArgumentParser, bool]:
    parser = ArgumentParser(add_help=False)
    flag = parser.add_argument(*names, action="store_true", help=help)
    args, _ = parser.parse_known_args()
    return parser, vars(args)[flag.dest]


def checkForVersionArgument(programName) -> ArgumentParser:
    parser, hasVersionArg = checkForArgument(
        "-v", "--version", help="output version info and exit"
    )
    if hasVersionArg:
        print_version(programName)
    return parser


class ConsoleSession(Session):
    def __init__(self):
        self._componentType = None
        self._componentID = None
        self._property = None

    def setContext(self, componentType, componentID, property):
        self._componentType = componentType
        self._componentID = componentID
        self._property = property

    def _context(self):
        if self._componentType:
            ctx = " in "
            if self._property:
                ctx += f"{self._property} property of "
            ctx += f"{self._componentType} {self._componentID}"
            return ctx
        return ""

    def ask(self, question: str) -> bool:
        pass

    def warn(self, message: str) -> None:
        print(
            Fore.YELLOW + "Warning: " + message + self._context() + Style.RESET_ALL,
            file=stderr,
        )

    def fatal(self, message: str) -> None:
        print(
            Fore.RED + "Fatal error: " + message + self._context() + Style.RESET_ALL,
            file=stderr,
        )
        exit(1)


# class InteractiveConsoleSession(ConsoleSession)
