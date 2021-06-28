from lexer.lexer import Lexer

path = "Tests/test18.txt"
lexer = Lexer(path)
lex = lexer.getNextLexem()
print(lex.getTokens())
while lex.notEOF():
    lex = lexer.getNextLexem()
    print(lex.getTokens())