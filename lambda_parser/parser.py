import re
from collections import deque

from node.nodes import *
from node.binary_operators import *


class LambdaParser:
    def __init__(self):
        self.function_parts_dict = dict()

        self.primary_tokenizer = re.compile(r"([()+\-*/^.])|\s+").split

        self.variable_re_pattern = re.compile(r"""(?P<var>[a-z])                         # Single character
                                                  """, re.VERBOSE)
        self.number_re_pattern = re.compile(r"""(?P<num>\d+)                             # Number literal
                                                """, re.VERBOSE)

    def __l_par(self, t_stack):
        pass

    def _rec_parse(self, t_stack):
        if len(t_stack) < 1 or t_stack[0] == ")":
            return None
        token = t_stack.popleft()

        if token == "(":
            result = self._appl_parse(t_stack)
            if len(t_stack) == 0 or t_stack[0] != ")":
                raise ValueError("Bad parentheses.")
            t_stack.popleft()
            return result
        elif token == "^":
            try:
                args = t_stack.popleft()
                for char in args:
                    if not self.variable_re_pattern.fullmatch(char):
                        raise ValueError("Bad function arguments.")
                if t_stack.popleft() != ".":
                    raise ValueError("Bad function formatting.")
            except IndexError:
                raise ValueError("Bad function.")
            body = self._appl_parse(t_stack)
            if body is None:
                raise ValueError("Bad function body.")

            return FunctionNode(args, body)
        elif token in ["+", "-", "*", "/"]:
            left = self._rec_parse(t_stack)
            right = self._rec_parse(t_stack)

            if token == "+":
                return OperatorPlusNode(left, right)
            elif token == "-":
                return OperatorMinusNode(left, right)
            elif token == "*":
                return OperatorMultiplyNode(left, right)
            elif token == "/":
                return OperatorDivideNode(left, right)
        else:
            variable_match = self.variable_re_pattern.fullmatch(token)
            if not variable_match:
                number_match = self.number_re_pattern.fullmatch(token)
                if not number_match:
                    raise ValueError("Bad input.")
                return NumberNode(number_match.groupdict()["num"])
            return VariableNode(variable_match.groupdict()["var"])

    def _appl_parse(self, t_stack):
        func = self._rec_parse(t_stack)
        if func is None:
            raise ValueError("Bad input.")
        arg = self._rec_parse(t_stack)
        if arg is None:
            return func

        result = ApplicationNode(func, arg)
        while len(t_stack) > 0 and t_stack[0] != ")":
            result = ApplicationNode(result, self._rec_parse(t_stack))
        return result

    def parse(self, expression):
        check_parentheses(expression)

        tokens = deque(filter(None, self.primary_tokenizer(expression)))
        print(f"Primary tokens: {list(tokens)}")

        result = self._appl_parse(tokens)
        print(f"{result}")
        return result


def check_parentheses(expression):
    parentheses_stack = 0
    for symbol in expression:
        if symbol == "(":
            parentheses_stack += 1
        elif symbol == ")":
            if parentheses_stack > 0:
                parentheses_stack -= 1
            else:
                raise ValueError("Bad parentheses.")
    else:
        if parentheses_stack > 0:
            raise ValueError("Bad parentheses.")
