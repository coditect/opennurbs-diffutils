class ParseError(Exception):
    "An error that occurs while parsing a delta"

    def __init__(self, lineNumber):
        self.lineNumber = lineNumber
