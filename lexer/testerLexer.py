import os.path
from lexer.lexer import Lexer
from simplest_expr.exprParser import ExprParser


class LexExecute:
    def __init__(self, range, path):
        self.range = range
        self.path = path
        self.compileLexer()

    def compileLexer(self):
        if self.range == 1:
            self.compileLexFile()
        elif self.range == 2:
            self.compileLexDir()

    def compileLexFile(self):
        if os.path.isfile(self.path):
            try:
                f = open(self.path[:-4] + 'MyRes.txt', 'w')
                lexer = Lexer(self.path)
                lex = lexer.getNextLexem()
                f.write(lex.getTokens() + '\n')
                while lex.notEOF():
                    lex = lexer.getNextLexem()
                    f.write(lex.getTokens() + '\n')
                f.close()
            except UnicodeDecodeError:
                print(f"{self.path} 'utf-8' codec can't decode byte")
            except Exception as e:
                f.write(str(e) + '\n')
                f.close()

    def compileLexDir(self):
        if os.path.isdir(self.path):
            for file in os.listdir(self.path):
                try:
                    abs_path = os.path.join(self.path, file)
                    self.testFileLexer(file, abs_path)
                except UnicodeDecodeError:
                    print(f"{abs_path} 'utf-8' codec can't decode byte")

    def testFileLexer(self, file, path):
        self.passed = True
        if ('Answer' not in file) and ('MyRes' not in file):
            f = open(path[:-4] + 'MyRes.txt', 'w')
            try:
                lexer = Lexer(path)
                lex = lexer.getNextLexem()
                f.write(lex.getTokens() + '\n')
                while lex.notEOF():
                    lex = lexer.getNextLexem()
                    f.write(lex.getTokens() + '\n')
                f.close()
            except Exception as e:
                f.write(str(e) + '\n')
                f.close()

            fMyRes = open(path[:-4] + 'MyRes.txt', 'r')
            fAnswers = open(path[:-4] + 'Answer.txt', 'r')
            try:
                for line in fAnswers:
                    fMyRes_line = fMyRes.readline()
                    if line != fMyRes_line:
                        self.passed = False
            except Exception:
                pass
            print("{} - {}".format(file, "OK" if self.passed else "WRONG"))
