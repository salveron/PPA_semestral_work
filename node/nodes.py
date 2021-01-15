
symbolic_functions = {
    "succ": "(^xsz.s (x s z))",
    "pred": "(^xsz. x (^fg.g (f s)) (^g.z) (^m.m))",
    "true": "T",
    "false": "F",
    "zero": "(^x.x (^y.F) T)",
    "Y": "(^f.(^x.f (x x)) (^x.f (x x)))",
    "fac": "Y (^fn. zero n 1 (* n (f (pred n))))",
}


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
        return f"({self.func} {self.arg})"

    def __eq__(self, other):
        return self.func == other.func and self.arg == other.arg


class UnaryOperatorNode:
    sign = None
    re_char = None

    def __init__(self, left):
        self.left = left

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def __eq__(self, other):
        return self.left == other.left

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
            try:
                num = int(self.value)
                return "(^sz." + "s(" * num + "z" + ")" * (num + 1)
            except ValueError:
                return symbolic_functions[self.value]
