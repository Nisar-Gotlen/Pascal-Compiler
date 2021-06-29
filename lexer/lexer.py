from lexer.tokens import Token
from lexer.lexemes import LexemesList


class Lexer:
    def __init__(self, filePath):
        self.filePath = filePath
        self.file = open(self.filePath, "r", encoding="utf-8")
        self.symbol = self.file.read(1)

        self.unaryOperator = {"+", "-"}
        self.relationOperator = {'=', '<>', '<', '>', '<=', '>=', 'in'}
        self.addOperator = {"+", "-", "or"}
        self.mulOperator = {"*", "**", "/", "div", "mod", "and"}
        self.space_symbols = {'', ' ', '\n', '\t', '\0', '\r'}
        self.reserved = {
            "and",
            "downto",
            "if",
            "or",
            "then",
            "array",
            "else",
            "in",
            "packed",
            "to",
            "begin",
            "end",
            "label",
            "procedure",
            "type",
            "case",
            "file",
            "mod",
            "program",
            "until",
            "const",
            "for",
            "nil",
            "record",
            "var",
            "div",
            "function",
            "not",
            "repeat",
            "while",
            "do",
            "goto",
            "of",
            "set",
            "with",
        }
        self.constants = {"false", "true"}
        self.types = {"integer", "boolean", "real", "char"}
        self.functions = {
            "abs", "arctan", "chr", "cos", "eof", "eoln", "exp", "ln", "odd",
            "ord", "pred", "round", "sin", "sqr", "sqrt", "succ", "trunc"
        }
        self.procedures = {
            "get", "new", "dispose", "pack", "page", "put", "read", "readln",
            "reset", "rewrite", "unpack", "write", "writeln"
        }
        self.number_base = {16: '$', 8: '&', 2: '%'}
        self.spaces = {'', ' ', '\n', '\t', '\0', '\r'}
        self.operations_arr = {'+', '-', '*', '/'}
        self.operations_bool = {'>', '<'}

        self.assignments = {":=", "+=", "-=", "*=", "/="}
        self.delimiters = {'.', ',', ':', ';', '(', ')', '[', ']', ".."}

        self.state = ""
        self.line, self.column = 1, 1
        self.buffer, self.unget, self.coordinates = "", "", ""

    def clearBuffer(self):
        self.buffer = ""

    def addBuffer(self):
        self.buffer += self.symbol

    def nextLine(self):
        self.line += 1
        self.column = 0

    def getSymbol(self):

        self.symbol = self.file.read(1)
        self.column += 1

    def setUnget(self, value):
        self.unget = value
        self.col -= 1

    def keepSymbol(self, state=None, keep_coordinates=False):
        if state:
            self.state = state
        if keep_coordinates:
            self.saveCoordinates()
        self.addBuffer()
        self.getSymbol()

    def saveCoordinates(self):
        self.coordinates = f"{self.line} {self.column}"

    def getToken(self, coordinates, type, code, value):
        self.token = Token(coordinates, type, code, value)
        return self.token

    def getCurrLex(self):
        return self.token

    def getValue(self):
        return self.value

    def keepCoordinates(self):
        self.coordinates = f"{self.line}:{self.column}"

    def getNextLexem(self):
        self.clearBuffer()
        while self.symbol or self.buffer:
            if self.state == "":
                if self.symbol in self.space_symbols:
                    if self.symbol == "\n":
                        self.nextLine()
                    self.getSymbol()
                elif self.symbol.isalpha():
                    self.keepSymbol(state=LexemesList.kIdentifier,
                                    keep_coordinates=True)
                elif self.symbol in self.delimiters:
                    self.keepSymbol(state=LexemesList.kDelimiter,
                                    keep_coordinates=True)
                elif self.symbol.isdigit():
                    self.keepSymbol(state=LexemesList.kIntNumber,
                                    keep_coordinates=True)
                elif self.symbol == "{":
                    self.keepSymbol(state=LexemesList.KComment,
                                    keep_coordinates=True)
                elif self.symbol == "'":
                    self.keepSymbol(state=LexemesList.kString,
                                    keep_coordinates=True)

                elif self.symbol in self.unaryOperator or self.symbol in self.relationOperator or self.symbol in self.addOperator or self.symbol in self.mulOperator:
                    self.keepSymbol(state=LexemesList.kOperator,
                                    keep_coordinates=True)
                else:
                    self.keepSymbol(state=LexemesList.kError,
                                    keep_coordinates=True)

            elif self.state == LexemesList.kIdentifier:
                if self.symbol.isdigit() or self.symbol.isalpha(
                ) or self.symbol == "_":
                    self.keepSymbol()
                else:
                    self.state = ""
                    lexeme_state = LexemesList.kIdentifier.value
                    if self.buffer.lower() in self.reserved:
                        lexeme_state = LexemesList.kReserved.value
                    elif self.buffer.lower() in self.constants:
                        lexeme_state = LexemesList.kConstant.value
                    elif self.buffer.lower() in self.types:
                        lexeme_state = LexemesList.kType.value
                    elif self.buffer.lower() in self.functions:
                        lexeme_state = LexemesList.kFunction.value
                    elif self.buffer.lower() in self.procedures:
                        lexeme_state = LexemesList.kProcedure.value

                    elif self.buffer.lower() in self.relationOperator:
                        lexeme_state = LexemesList.kRelationOperator.value
                    elif self.buffer.lower() in self.addOperator:
                        lexeme_state = LexemesList.kAddOperator.value
                    elif self.buffer.lower() in self.mulOperator:
                        lexeme_state = LexemesList.kMulOperator.value
                    return self.getToken(self.coordinates, lexeme_state,
                                         self.buffer, self.buffer)

            elif self.state == LexemesList.kDelimiter:
                self.state = ""
                lexeme_state = LexemesList.kDelimiter.value
                if self.buffer + self.symbol == "(*":
                    self.addBuffer()
                    self.state = LexemesList.KComment
                elif self.buffer + self.symbol in ("..", ":="):
                    self.addBuffer()
                    if self.buffer == ":=":
                        lexeme_state = LexemesList.KAssignment.value
                    self.getSymbol()
                    return self.getToken(self.coordinates, lexeme_state,
                                         self.buffer, self.buffer)
                elif self.buffer == '.':
                    if self.symbol in self.space_symbols:
                        return self.getToken(self.coordinates, lexeme_state,
                                             self.buffer, self.buffer)
                    else:
                        self.state = LexemesList.kError
                        self.keepSymbol()
                else:
                    return self.getToken(self.coordinates, lexeme_state,
                                         self.buffer, self.buffer)

            elif self.state == LexemesList.kOperator:
                if (
                        self.buffer in self.operations_arr
                        or self.buffer in self.operations_bool
                ) and self.symbol == "=" or self.buffer + self.symbol == "**":
                    self.keepSymbol()
                elif self.buffer + self.symbol == "//":
                    self.keepSymbol()
                    self.state == LexemesList.KComment
                else:
                    self.state = ""
                    if self.buffer in self.assignments:
                        lexeme_state = LexemesList.KAssignment.value
                    elif self.buffer in self.unaryOperator:
                        lexeme_state = LexemesList.kUnaryOperator.value
                    elif self.buffer in self.relationOperator:
                        lexeme_state = LexemesList.kRelationOperator.value
                    elif self.buffer in self.addOperator:
                        lexeme_state = LexemesList.kAddOperator.value
                    elif self.buffer in self.mulOperator:
                        lexeme_state = LexemesList.kMulOperator.value
                    return self.getToken(self.coordinates, lexeme_state,
                                         self.buffer, self.buffer)

            elif self.state == LexemesList.KComment:
                if self.symbol == '$' and len(self.buffer) == 1:
                    self.state = LexemesList.kDirective
                    self.keepSymbol()
                elif self.buffer[
                        0] == '{' and self.symbol == '}' or self.buffer[:2] == "(*" and self.buffer[
                            len(self.buffer) - 1] + self.symbol == "*)":
                    self.state = ""
                    self.clearBuffer()
                    self.getSymbol()
                elif self.buffer[:2] == "//" and (not self.symbol
                                                  or self.symbol == "\n"):
                    self.state = ""
                    self.clearBuffer()
                    self.newLine()
                    self.getSymbol()
                elif self.symbol == '\n':
                    self.addBuffer()
                    self.newLine()
                    self.getSymbol()
                elif not self.symbol:
                    self.buff = self.buffer.encode("unicode_escape").decode(
                        "utf-8")
                    self.col -= 1
                    self.keepCoordinates()
                    raise Exception(
                        '{self.coordinates}        No end of comment found')
                else:
                    self.keepSymbol()

            elif self.state == LexemesList.kString:
                if self.symbol == '' or self.symbol == '\n':
                    end_of = "file" if self.symbol == '' else "line"
                    raise Exception(
                        f'{self.coordinates}        End of {end_of} was encountered, but "\'" was expected'
                    )
                elif self.symbol != "'":
                    self.keepSymbol()
                else:
                    self.state = ""
                    self.keepSymbol()
                    return self.getToken(self.coordinates,
                                         LexemesList.kString.value,
                                         self.buffer, self.buffer)

            elif self.state == LexemesList.kIntNumber:
                if self.symbol.isdigit():
                    self.keepSymbol()
                elif self.symbol == ".":
                    self.state = LexemesList.kRelNumber
                    self.keepSymbol()
                elif self.symbol.lower() == "e":
                    self.state = LexemesList.kRelNumber_e
                    self.keepSymbol()
                elif self.symbol.isalpha():
                    self.state = LexemesList.kError
                    self.keepSymbol()
                else:
                    self.state = ""
                    if int(self.buffer) <= 2147483647:
                        return self.getToken(self.coordinates,
                                             LexemesList.kIntNumber.value,
                                             self.buffer, int(self.buffer))
                    else:
                        raise Exception(
                            f"{self.coordinates}        Error in integer constant size"
                        )

            elif self.state == LexemesList.kRelNumber:
                if self.symbol.isdigit():
                    self.keepSymbol()
                elif self.symbol.lower() == "e":
                    if self.buffer[len(self.buffer) - 1] != '.':
                        self.state = LexemesList.kRelNumber_e
                        self.keepSymbol()
                    else:
                        self.state = LexemesList.kError
                        self.keepSymbol()
                elif self.buffer[len(self.buffer) -
                                 1] == '.' and self.symbol == '.':
                    self.state = ""
                    self.buffer = self.buffer[:len(self.buffer) - 1]
                    self.setUnget(".")
                    return self.getToken(self.coordinates,
                                         LexemesList.integer.value,
                                         self.buffer, int(self.buffer))
                else:
                    if self.buffer[len(self.buffer) - 1] != '.':
                        self.state = ""
                        if 2.9e-39 <= float(self.buffer) <= 1.7e38:
                            return self.getToken(self.coordinates,
                                                 LexemesList.kRelNumber.value,
                                                 self.buffer,
                                                 float(self.buffer))
                        raise Exception(
                            f"{self.coordinates}        Range check error")
                    self.state = LexemesList.kError
                    self.keepSymbol()

            elif self.state == LexemesList.kRelNumber_e:
                if self.symbol == '+' or self.symbol == '-' or self.symbol.isdigit(
                ):
                    if self.symbol.isdigit():
                        self.state = LexemesList.kRelDegreeNumber
                    else:
                        self.state = LexemesList.kRelFloatNumber
                    self.keepSymbol()
                else:
                    self.state = LexemesList.kError
                    self.keepSymbol()

            elif self.state == LexemesList.kRelFloatNumber:
                if self.symbol.isdigit():
                    self.state = LexemesList.kRelDegreeNumber
                    self.addBuffer()
                    self.getSymbol()
                else:
                    self.state = LexemesList.kError
                    self.keepSymbol()

            elif self.state == LexemesList.kRelDegreeNumber:
                if self.symbol.isdigit():
                    self.keepSymbol()
                else:
                    self.state = ""
                    if 2.9e-39 <= float(self.buffer) <= 1.7e38:
                        return self.getToken(self.coordinates,
                                             LexemesList.kRelNumber.value,
                                             self.buffer, float(self.buffer))
                    else:
                        raise Exception(
                            f"{self.coordinates}        Range check error")

            elif self.state == LexemesList.kError:
                if self.symbol in self.space_symbols or self.symbol in self.delimiters:
                    raise Exception(
                        f'{self.coordinates}        Syntax error  "{self.buffer}"'
                    )
                self.keepSymbol()

        return self.getToken(f"{self.line} {self.column}", "EOF",
                             "End of file", "End of file")
