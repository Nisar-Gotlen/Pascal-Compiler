from lexer.lexemes import LexemesList
from simplest_expr.BinarOpNode import BinarOpNode
from simplest_expr.IdentNode import IdentNode
from simplest_expr.NumberNode import NumberNode


class ExprParser():
    def __init__(self, lexer):
        self.lexer = lexer

    def ParseExpr(self):

        token = self.lexer.getCurrLex()
        left = self.ParseTerm()
        oper_lexeme = self.lexer.getCurrLex()
        while oper_lexeme.getValue() == '+' or oper_lexeme.getValue() == '-':
            self.lexer.getNextLexem()
            right = self.ParseTerm()
            left = BinarOpNode(oper_lexeme.getValue(), left, right)
            oper_lexeme = self.lexer.getCurrLex()
        return left

    def ParseTerm(self):
        left = self.ParseFactor()
        oper_lexeme = self.lexer.getCurrLex()
        while oper_lexeme.getValue() == '*' or oper_lexeme.getValue() == '/':
            self.lexer.getNextLexem()
            right = self.ParseTerm()
            left = BinarOpNode(oper_lexeme.getValue(), left, right)
            oper_lexeme = self.lexer.getCurrLex()
        return left

    def ParseFactor(self):
        token = self.lexer.getCurrLex()
        self.lexer.getNextLexem()
        if token.getType() == LexemesList.kIntNumber.value or token.getType(
        ) == LexemesList.kRelNumber.value:
            return NumberNode(token)
        if token.getType() == LexemesList.kIdentifier.value:
            return IdentNode(token)
        if token.getValue() == "(":
            left = self.ParseExpr()
            token = self.lexer.getCurrLex()
            if token.getValue() != ")":
                raise Exception(f"{token.getCoord()}        ')' was expected")
            self.lexer.getNextLexem()
            return left
        raise Exception(
            f'{token.getCoord()}        Unexpected "{token.getCode()}"')
