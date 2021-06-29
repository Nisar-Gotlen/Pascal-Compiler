from lexer.lexer import Lexer
from simplest_expr.exprParser import ExprParser
'''
path = "TestsLexer/test18.txt"
lexer = Lexer(path)
lex = lexer.getNextLexem()
print(lex.getTokens())
while lex.notEOF():
    lex = lexer.getNextLexem()
    print(lex.getTokens())
'''

path = "TestsParser/test4.txt"
lexer = Lexer(path)
lexer.getNextLexem()
res = ExprParser(lexer).ParseExpr()
if res:
    print(res.Print(0))