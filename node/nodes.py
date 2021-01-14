

class FunctionNode:
    def __init__(self, args, body, appl):
        self.args = args
        self.body = body
        self.appl = appl

    def __repr__(self):
        return f"(^{self.args}.{self.body}) {self.appl}"


class BinaryOperatorNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        pass

    def result(self):
        pass


class VariableNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.value}"


class NumberNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.value}"
