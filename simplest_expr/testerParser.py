from lexer.lexer import Lexer
from simplest_expr.exprParser import ExprParser
import os.path


class ParseExecute:
    def __init__(self, range, path):
        self.range = range
        self.path = path
        self.compilerParser()

    def compilerParser(self):
        if self.range == 1:
            self.compilerParserFile()
        elif self.range == 2:
            self.compilerParserDirectory()

    def compilerParserFile(self):
        if os.path.isfile(self.path):
            try:
                f = open(self.path[:-4] + 'MyRes.txt', 'w')
                lexer = Lexer(self.path)
                lexer.getNextLexem()
                res = ExprParser(lexer).ParseExpr()
                if res:
                    res = res.Print(0)
                f.write(res)
                f.close()
            except UnicodeDecodeError:
                print(f"{self.path} 'utf-8' codec can't decode byte")
            except Exception as e:
                f.write(str(e))
                f.close()
        else:
            print("ERROR")

    def compilerParserDirectory(self):
        if os.path.isdir(self.path):
            for file in os.listdir(self.path):
                try:
                    abs_path = os.path.join(self.path, file)
                    self.testFileParser(file, abs_path)
                except UnicodeDecodeError:
                    print(f"{abs_path} 'utf-8' codec can't decode byte")

    def testFileParser(self, file, path):
        self.passed = True
        if ('Answer' not in file) and ('MyRes' not in file):
            try:
                f = open(path[:-4] + 'MyRes.txt', 'w')
                lexer = Lexer(path)
                lexer.getNextLexem()
                res = ExprParser(lexer).ParseExpr()
                if res:
                    res = res.Print(0)
                f.write(res)
                f.close()
            except UnicodeDecodeError:
                print(f"{self.path} 'utf-8' codec can't decode byte")
            except Exception as e:
                f.write(str(e))
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
