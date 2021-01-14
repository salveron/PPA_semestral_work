from node.nodes import BinaryOperatorNode


class OperatorPlusNode(BinaryOperatorNode):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        return f"( + {self.left} {self.right} )"

    def result(self):
        return self.left + self.right


class OperatorMinusNode(BinaryOperatorNode):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        return f"( - {self.left} {self.right} )"

    def result(self):
        return self.left - self.right


class OperatorMultiplyNode(BinaryOperatorNode):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        return f"( * {self.left} {self.right} )"

    def result(self):
        return self.left * self.right


class OperatorDivideNode(BinaryOperatorNode):
    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        return f"( / {self.left} {self.right} )"

    def result(self):
        return self.left / self.right
