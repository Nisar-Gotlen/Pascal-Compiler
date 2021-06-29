from simplest_expr.node import Node


class BinarOpNode(Node):
    def __init__(self, oper_lex, left, right):
        self.oper = oper_lex
        self.left = left
        self.right = right

    def Print(self, space):
        right = self.right.Print(space + 1)
        left = self.left.Print(space + 1)
        return '    ' * space + str(
            self.oper) + '\n' + str(left) + '\n' + str(right)
