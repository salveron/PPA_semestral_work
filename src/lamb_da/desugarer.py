from lamb_da.parser import *


class LambdaDesugarer:
    """Class for "desugaring" lambda calculus expressions.

    To desugar, pass a valid lambda calculus expression to the desugar method. This method will parse the passed
    string (see LambdaParser class in the parser module), then expand the reserved literals and functions
    from the node.nodes.symbolic_functions dictionary and finally expand the multi-argument functions
    to fit the pure lambda calculus definitions. The final result of desugaring is a tree of nodes that can be
    easily represented as a string with a help of nodes' __repr__ and __str__ methods.
    """

    def __init__(self, symbolic_functions):
        self.parser = LambdaParser(symbolic_functions)

    def _expand(self, root):
        # if the node is ApplicationNode, recursively expand its two parts
        if isinstance(root, ApplicationNode):
            return ApplicationNode(self._expand(root.func), self._expand(root.arg))

        # if the node is FunctionNode, recursively expand only its body
        elif isinstance(root, FunctionNode):
            return FunctionNode(root.args, self._expand(root.body))

        # if the node is an Operator, call the node's expand method (returns a string to be parsed),
        # then parse it and recursively expand the resulting tree
        elif isinstance(root, UnaryOperatorNode) \
                or isinstance(root, BinaryOperatorNode):
            return self._expand(self.parser.parse(root.expand()))

        # if the node is a Literal, check if it is a symbolic function. If true, parse the expression from the
        # dictionary, otherwise use its expand method
        elif isinstance(root, LiteralNode):
            if root.value in self.parser.symbolic_functions:
                return self._expand(self.parser.parse(self.parser.symbolic_functions[root.value]))
            else:
                return self._expand(self.parser.parse(root.expand()))

        # if the node is VariableNode, then just pass it outside
        else:
            return root

    def _expand_multi_arg_fns(self, root, a_stack):
        # expanding an ApplicationNode
        if isinstance(root, ApplicationNode):
            # expand the argument to be applied (with a new independent stack)
            appl_arg = self._expand_multi_arg_fns(root.arg, deque())
            a_stack.appendleft(appl_arg)

            # expand the function for the application
            result = self._expand_multi_arg_fns(root.func, a_stack)

            # if the function did not consume the argument, recreate the ApplicationNode
            if len(a_stack) > 0 and a_stack[0] == appl_arg:
                appl_arg = a_stack.popleft()
                return ApplicationNode(result, appl_arg)

            # else, return the result of the recursive expansion
            return result

        # expanding a FunctionNode
        elif isinstance(root, FunctionNode):
            # if the function has multiple arguments, get the first argument and pass the others to the recursive call
            if len(root.args) > 1:

                first_arg, next_args = root.args[0], root.args[1:]

                # if there are arguments for application, create a FunctionNode inside an ApplicationNode
                if len(a_stack) > 0:
                    appl_arg = a_stack.popleft()
                    body = self._expand_multi_arg_fns(FunctionNode(next_args, root.body), a_stack)
                    return ApplicationNode(FunctionNode(first_arg, body), appl_arg)
                # else, create a single FunctionNode with a recursively expanded body
                else:
                    body = self._expand_multi_arg_fns(FunctionNode(next_args, root.body), a_stack)
                    return FunctionNode(first_arg, body)

            # if the function has only one argument, recursively expand its body and create
            # an Application + FunctionNode or just a FunctionNode
            else:
                if len(a_stack) > 0:
                    appl_arg = a_stack.popleft()
                    body = self._expand_multi_arg_fns(root.body, a_stack)
                    return ApplicationNode(FunctionNode(root.args, body), appl_arg)
                return FunctionNode(root.args, self._expand_multi_arg_fns(root.body, a_stack))

        # if the Node is neither ApplicationNode nor FunctionNode, just pass it outside
        else:
            return root

    def desugar(self, expression):
        # parse the string to create a tree of nodes
        root = self.parser.parse(expression)
        print(f"After parsing: {root}")

        # then expand the reserved literals (T, F or numbers) and symbolic functions (e.g. zero function)
        root = self._expand(root)
        print(f"After expansion: {root}")

        # finally, expand multi-argument functions to have a pure lambda calculus expression
        result = self._expand_multi_arg_fns(root, deque())
        print(f"After multi-argument function expansion: {result}")
        print("-------------------------------------------------------------------------------------------------------")
        return result
