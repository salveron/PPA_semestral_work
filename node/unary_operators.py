from node.nodes import UnaryOperatorNode


class OperatorNotNode(UnaryOperatorNode):
    sign = "not"
    re_char = "(?:not)"

    def __init__(self, operand):
        super().__init__(operand)

    def __repr__(self):
        return f"not {self.operand}"

    def __str__(self):
        return f"(not {self.operand})"

    def expand(self):
        return f"(^xtf.x f t) {self.operand}"


unary_operators = [
    OperatorNotNode,
]
