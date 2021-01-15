import re
from collections import deque

from node.nodes import *
from node.unary_operators import *
from node.binary_operators import *


def check_parentheses(expression):
    """Simple parentheses check function.

    Counts the difference between the numbers of left and right brackets, raises an exception if the difference
    becomes less than zero (there was a single right parenthesis) or if final difference is greater than zero
    (there was a single left parenthesis).
    """

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
    """Class for parsing lambda calculus expressions.

    To parse, pass a valid lambda calculus expression to the parse method. This method will tokenize the passed string
    using the standard Python re module and then start the recursion to create a tree of nodes. For more information
    about different nodes, see the node package.
    """

    def __init__(self):
        # simple split function that splits by regular expression matches
        self.tokenizer = re.compile("([()^.TF]|" +
                                    "|".join([op.re_char for op in unary_operators]) +
                                    "|".join([op.re_char for op in binary_operators]) +
                                    ")|\s+").split

        # patterns to match lambda calculus variables, numbers, True/False literals or reserved functions from the
        # node.nodes.simplifications_dict dictionary (these reserved functions are represented as literals to be then
        # easily expanded by a desugarer)
        self.variable_re_pattern = re.compile("([a-z])")
        self.literal_re_pattern = re.compile("(\d+|[TF]|" +
                                             "|".join([func for func in simplifications_dict.keys()]) +
                                             ")")

    def __l_par(self, t_stack):
        # if the token is a left parenthesis, then recursively parse the expression after it. If the next token after
        # expression is not a right parenthesis, raise an error exception

        result = self._appl_parse(t_stack)
        if len(t_stack) == 0 or t_stack[0] != ")":
            raise ValueError("Bad parentheses.")
        t_stack.popleft()
        return result

    def __func(self, t_stack):
        # if the token is a function, then get its arguments, then check for the dot token,
        # then parse the function body and create a node. In case of errors, raise an exception

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

    def __un_op(self, t_stack, operator):
        # if the token is an unary operator, recursively parse its operand and create a node

        left = self._exp_parse(t_stack)
        for op_node in unary_operators:
            if op_node.sign == operator:
                return op_node(left)
        raise ValueError("Bad unary operator.")

    def __bin_op(self, t_stack, operator):
        # if the token is a binary operator, get its operands and create a node

        left = self._exp_parse(t_stack)
        right = self._exp_parse(t_stack)
        for op_node in binary_operators:
            if op_node.sign == operator:
                return op_node(left, right)
        raise ValueError("Bad binary operator.")

    def __var_num(self, varnum):
        # in case of variable or literal, create a node if the token matches the defined pattern

        variable_match = self.variable_re_pattern.fullmatch(varnum)
        if not variable_match:
            number_match = self.literal_re_pattern.fullmatch(varnum)
            if not number_match:
                raise ValueError("Bad input.")
            return LiteralNode(number_match.group(0))
        return VariableNode(variable_match.group(0))

    def _exp_parse(self, t_stack):
        """Method for parsing non-application expressions.

        Application expressions are parsed by _appl_parse method that calls this one twice to get both
        parts of an application. This method uses a stack of tokens to create an expression tree and calls private
        helper methods for different token types.
        """

        if len(t_stack) == 0 or t_stack[0] == ")":
            return None
        token = t_stack.popleft()

        if token == "(":
            return self.__l_par(t_stack)
        elif token == "^":
            return self.__func(t_stack)
        elif token in [op.sign for op in unary_operators]:
            return self.__un_op(t_stack, token)
        elif token in [op.sign for op in binary_operators]:
            return self.__bin_op(t_stack, token)
        else:
            return self.__var_num(token)

    def _appl_parse(self, t_stack):
        """Method for parsing application expressions.

        Calls the _exp_parse method twice to get two arts of an application, then creates an ApplicationNode if
        both parts are nodes or returns a first part if the second part is not defined. If the stack is not empty
        at the end, creates ApplicationNodes to empty it.
        """

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
        # check if the expression has a valid parentheses sequence
        check_parentheses(expression)

        # tokenize the input string
        tokens = deque(filter(None, self.tokenizer(expression)))

        # parse as an application by default
        return self._appl_parse(tokens)
