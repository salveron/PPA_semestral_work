import re
from collections import deque

from node.nodes import *
from node.binary_operators import *


class LambdaParser:
    def __init__(self):
        self.function_parts_dict = dict()

        self.primary_tokenizer = re.compile("([()])").split

        self.variable_re_pattern = re.compile("""(?P<var>[a-z])                         # Single character
                                                 """, re.VERBOSE)
        self.number_re_pattern = re.compile("""(?P<num>\d+)                             # Number literal
                                                """, re.VERBOSE)
        self.binary_operator_re_pattern = re.compile("""(?P<sign>[+\-*/])               # Operator
                                                        (?P<left>.+?)                   # Left operand
                                                        (?P<right>.*?)                  # Right operand
                                                        """, re.VERBOSE)
        self.function_re_pattern = re.compile("""\^                                     # Lambda symbol
                                                 (?P<fn_args>.+?)                       # Lambda function arguments
                                                 \.                                     # Dot character
                                                 (?P<fn_body>.*?)                       # Lambda function body
                                                 """, re.VERBOSE)
        self.application_re_pattern = re.compile("""(?P<first>.+?)                      # First part of application 
                                                                                        # (function)
                                                    [ ]                                 # Application space character
                                                    (?P<second>.*?)                     # Second part of application
                                                                                        # (argument(-s))
                                                    """, re.VERBOSE)

    def check_function(self, function):
        match = self.function_re_pattern.fullmatch(function)
        if not match:
            raise ValueError(f"The function {function} does not match with the expected pattern.")

        args = match.groupdict()["fn_args"]
        body = match.groupdict()["fn_body"]

        for char in args:
            if not self.variable_re_pattern.fullmatch(char):
                raise ValueError(f"Bad lambda argument {char}.")

        return args, body

    def check_binary_operator(self, expression):
        match = self.binary_operator_re_pattern.fullmatch(expression)
        if not match:
            raise ValueError(f"The expression {expression} does not match with the expected pattern.")

        sign = match.groupdict()["sign"]
        left = match.groupdict()["left"]
        right = match.groupdict()["right"]

        return sign, left, right

    def tokenize(self, t_list):
        pass

    def _rec_parse(self, t_stack):
        if len(t_stack) < 1:
            raise ValueError("Bad number of tokens on stack.")
        token = t_stack.popleft()

        if token == "(":
            result = self._rec_parse(t_stack)
            right_par = t_stack.popleft() if len(t_stack) > 0 else None
            if right_par != ")":
                raise ValueError("Bad parentheses.")
            return result
        elif token.startswith("^"):
            args, body = self.check_function(token)
            if body == "":
                body = self._rec_parse(t_stack)

            return FunctionNode(args, body, None)  # TODO
        elif any([token.startswith(op) for op in ("+", "-", "*", "/")]):
            sign, left, right = self.check_binary_operator(token)
            if right == "":
                right = self._rec_parse(t_stack)

            if sign == "+":
                return OperatorPlusNode(left, right)
            elif sign == "-":
                return OperatorMinusNode(left, right)
            elif sign == "*":
                return OperatorMultiplyNode(left, right)
            elif sign == "/":
                return OperatorDivideNode(left, right)
        else:
            variable_match = self.variable_re_pattern.fullmatch(token)
            if not variable_match:
                number_match = self.number_re_pattern.fullmatch(token)
                if not number_match:
                    raise ValueError(f"The token {token} is neither function, nor binary operator expression, "
                                     f"nor variable, nor number")
                return NumberNode(number_match.groupdict()["num"])
            return VariableNode(variable_match.groupdict()["var"])

    def parse(self, expression):
        tokens = list(map(lambda x: " ".join(x.strip().split()),
                          filter(None, self.primary_tokenizer(expression))))

        print(f"Tokens: {tokens}")

        if len(tokens) == 0:
            return

        try:
            root = self._rec_parse(deque(tokens))
            print(root)
        except ValueError as e:
            print(*e.args)
