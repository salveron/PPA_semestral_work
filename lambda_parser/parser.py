import re
from collections import deque

from node.nodes import *
from node.binary_operators import *


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


class LambdaParser:
    def __init__(self):
        self.function_parts_dict = dict()

        self.primary_tokenizer = re.compile(r"([()+\-*/^.])|\s+").split

        self.variable_re_pattern = re.compile(r"([a-z])")
        self.number_re_pattern = re.compile(r"(\d+)")

    def __l_par(self, t_stack):
        result = self._appl_parse(t_stack)
        if len(t_stack) == 0 or t_stack[0] != ")":
            raise ValueError("Bad parentheses.")
        t_stack.popleft()
        return result

    def __func(self, t_stack):
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

    def __bin_op(self, t_stack, sign):
        left = self._exp_parse(t_stack)
        right = self._exp_parse(t_stack)

        if sign == "+":
            return OperatorPlusNode(left, right)
        elif sign == "-":
            return OperatorMinusNode(left, right)
        elif sign == "*":
            return OperatorMultiplyNode(left, right)
        elif sign == "/":
            return OperatorDivideNode(left, right)

    def __var_num(self, varnum):
        variable_match = self.variable_re_pattern.fullmatch(varnum)
        if not variable_match:
            number_match = self.number_re_pattern.fullmatch(varnum)
            if not number_match:
                raise ValueError("Bad input.")
            return NumberNode(number_match.group(0))
        return VariableNode(variable_match.group(0))

    def _exp_parse(self, t_stack):
        if len(t_stack) < 1 or t_stack[0] == ")":
            return None
        token = t_stack.popleft()

        if token == "(":
            return self.__l_par(t_stack)
        elif token == "^":
            return self.__func(t_stack)
        elif token in ["+", "-", "*", "/"]:
            return self.__bin_op(t_stack, token)
        else:
            return self.__var_num(token)

    def _appl_parse(self, t_stack):
        func = self._exp_parse(t_stack)
        if func is None:
            raise ValueError("Bad input.")
        arg = self._exp_parse(t_stack)
        if arg is None:
            return func

        result = ApplicationNode(func, arg)
        while len(t_stack) > 0 and t_stack[0] != ")":
            result = ApplicationNode(result, self._exp_parse(t_stack))
        return result

    def parse(self, expression):
        check_parentheses(expression)

        tokens = deque(filter(None, self.primary_tokenizer(expression)))
        print(f"Primary tokens: {list(tokens)}")

        result = self._appl_parse(tokens)
        print(f"{result}")
        return result
