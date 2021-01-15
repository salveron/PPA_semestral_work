from node.nodes import BinaryOperatorNode


class OperatorPlusNode(BinaryOperatorNode):
    sign = "+"
    re_char = "\+"

    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        return f"+ {self.left} {self.right}"

    def __str__(self):
        return f"(+ {self.left} {self.right})"

    def expand(self):
        return f"{self.left} (^abc.b (a b c)) {self.right}"


class OperatorMultiplyNode(BinaryOperatorNode):
    sign = "*"
    re_char = "\*"

    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        return f"* {self.left} {self.right}"

    def __str__(self):
        return f"(* {self.left} {self.right})"

    def expand(self):
        return f"{self.left} (^xyz.x (y z)) {self.right}"


class OperatorAndNode(BinaryOperatorNode):
    sign = "and"
    re_char = "(?:and)"

    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        return f"and {self.left} {self.right}"

    def __str__(self):
        return f"(and {self.left} {self.right})"

    def expand(self):
        return f"{self.left} (^xy. x y (^tf. f)) {self.right}"


class OperatorOrNode(BinaryOperatorNode):
    sign = "or"
    re_char = "(?:or)"

    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        return f"or {self.left} {self.right}"

    def __str__(self):
        return f"(or {self.left} {self.right})"

    def expand(self):
        return f"{self.left} (^xy. x (^tf. t) y) {self.right}"


class OperatorXorNode(BinaryOperatorNode):
    sign = "xor"
    re_char = "(?:xor)"

    def __init__(self, left, right):
        super().__init__(left, right)

    def __repr__(self):
        return f"xor {self.left} {self.right}"

    def __str__(self):
        return f"(xor {self.left} {self.right})"

    def expand(self):
        return f"{self.left} (^xy. x (y (^tf. f)(^tf. t)) y) {self.right}"


binary_operators = [
    OperatorPlusNode,
    OperatorMultiplyNode,
    OperatorAndNode,
    OperatorOrNode,
    OperatorXorNode,
]
