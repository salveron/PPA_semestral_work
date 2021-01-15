from lambda_.parser import *


simplifications_dict = dict()


class LambdaDesugarer:
    def __init__(self):
        self.parser = LambdaParser()

    def _expand_literals(self, root):
        if isinstance(root, ApplicationNode):
            return ApplicationNode(self._expand_literals(root.func), self._expand_literals(root.arg))
        elif isinstance(root, FunctionNode):
            return FunctionNode(root.args, self._expand_literals(root.body))
        elif isinstance(root, BinaryOperatorNode):
            return root.__class__(self._expand_literals(root.left), self._expand_literals(root.right))
        elif isinstance(root, LiteralNode):
            return self.parser.parse(root.expand())
        else:
            return root

    def _substitute_util_expressions(self):
        pass

    def _expand_multi_arg_fns(self, root, a_stack):
        if isinstance(root, ApplicationNode):
            appl_arg = self._expand_multi_arg_fns(root.arg, a_stack)
            a_stack.appendleft(appl_arg)
            result = self._expand_multi_arg_fns(root.func, a_stack)
            if len(a_stack) > 0 and a_stack[0] == root.arg:
                appl_arg = a_stack.popleft()
                return ApplicationNode(result, appl_arg)
            return result

        elif isinstance(root, FunctionNode):
            if len(root.args) > 1:
                first_arg, next_args = root.args[0], root.args[1:]
                if len(a_stack) > 0:
                    appl_arg = a_stack.popleft()
                    body = self._expand_multi_arg_fns(FunctionNode(next_args, root.body), a_stack)
                    return ApplicationNode(FunctionNode(first_arg, body), appl_arg)
                else:
                    body = self._expand_multi_arg_fns(FunctionNode(next_args, root.body), a_stack)
                    return FunctionNode(first_arg, body)
            else:
                if len(a_stack) > 0:
                    appl_arg = a_stack.popleft()
                    body = self._expand_multi_arg_fns(root.body, a_stack)
                    return ApplicationNode(FunctionNode(root.args, body), appl_arg)
                return FunctionNode(root.args, self._expand_multi_arg_fns(root.body, a_stack))

        else:
            return root

    def desugar(self, expression):
        root = self.parser.parse(expression)

        root = self._expand_literals(root)

        result = self._expand_multi_arg_fns(root, deque())
        print(f"After desugaring: {result}")
        return result
