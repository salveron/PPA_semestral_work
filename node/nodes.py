

class FunctionNode:
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def __repr__(self):
        return f"FUNC:(^{self.args}.{self.body})"

    def __eq__(self, other):
        return self.args == other.args and self.body == other.body


class ApplicationNode:
    def __init__(self, func, arg):
        self.func = func
        self.arg = arg

    def __repr__(self):
        return f"APPL:{self.func} {self.arg}"

    def __eq__(self, other):
        return self.func == other.func and self.arg == other.arg


class BinaryOperatorNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        pass

    def result(self):
        pass

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right


class VariableNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"VAR:{self.value}"

    def __eq__(self, other):
        return self.value == other.value


class NumberNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NUM:{self.value}"

    def __eq__(self, other):
        return self.value == other.value
