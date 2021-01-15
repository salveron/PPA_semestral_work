
class FunctionNode:
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def __repr__(self):
        return f"FUNC:(^{self.args}.{self.body})"

    def __str__(self):
        return f"(^{self.args}.{self.body})"

    def __eq__(self, other):
        return self.args == other.args and self.body == other.body


class ApplicationNode:
    def __init__(self, func, arg):
        self.func = func
        self.arg = arg

    def __repr__(self):
        return f"APPL:{self.func} {self.arg}"

    def __str__(self):
        return f"{self.func} {self.arg}" \
            if isinstance(self.func, FunctionNode) \
            else f"({self.func} {self.arg})"

    def __eq__(self, other):
        return self.func == other.func and self.arg == other.arg


class UnaryOperatorNode:
    sign = None
    re_char = None

    def __init__(self, operand):
        self.operand = operand

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def __eq__(self, other):
        return self.operand == other.operand

    def expand(self):
        pass


class BinaryOperatorNode:
    sign = None
    re_char = None

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def expand(self):
        pass


class VariableNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"VAR:{self.value}"

    def __str__(self):
        return f"{self.value}"

    def __eq__(self, other):
        return self.value == other.value


class LiteralNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"LIT:{self.value}"

    def __str__(self):
        return f"{self.value}"

    def __eq__(self, other):
        return self.value == other.value

    def expand(self):
        if self.value == "T":
            return "(^ab.a)"
        elif self.value == "F":
            return "(^ab.b)"
        else:
            num = int(self.value)
            return "(^sz." + "s(" * num + "z" + ")" * (num + 1)
