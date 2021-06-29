from simplest_expr.node import Node


class IdentNode(Node):
    def __init__(self, node):
        self.node = node

    def Print(self, space):
        return ('    ' * space + str(self.node.getValue()))