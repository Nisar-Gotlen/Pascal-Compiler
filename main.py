from lexer.lexer import Lexer
from simplest_expr.exprParser import ExprParser
import os.path
'''
path = "TestsLexer"

for file in os.listdir(path):
    try:
        if 'Answer' in file:
            continue
        abs_path = os.path.join(path, file)
        f = open('TestsLexer/' + file[:-4] + 'Answer.txt', 'w')
        lexer = Lexer(abs_path)
        lex = lexer.getNextLexem()
        f.write(lex.getTokens() + '\n')
        while lex.notEOF():
            lex = lexer.getNextLexem()
            f.write(lex.getTokens() + '\n')
    except Exception as e:
        f.write(str(e) + '\n')
'''
'''
path = "TestsLexer/test2.txt"
lexer = Lexer(path)
lex = lexer.getNextLexem()
print(lex.getTokens())
while lex.notEOF():
    lex = lexer.getNextLexem()
    print(lex.getTokens())
'''
path = "TestsParser"
'''
lexer = Lexer(path)
lexer.getNextLexem()
res = ExprParser(lexer).ParseExpr()
if res:
    print(res.Print(0))
'''
for file in os.listdir(path):
    try:
        if 'Answer' in file:
            continue
        abs_path = os.path.join(path, file)
        f = open('TestsParser/' + file[:-4] + 'Answer.txt', 'w')
        lexer = Lexer(abs_path)
        lex = lexer.getNextLexem()
        res = ExprParser(lexer).ParseExpr()
        f.write(res.Print(0))
    except Exception as e:
        f.write(str(e))
