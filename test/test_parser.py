from lambda_.parser import LambdaParser
from node.nodes import *
from node.unary_operators import *
from node.binary_operators import *

# don't need any symbolic functions here
parser = LambdaParser(dict())


def test_parser_varnum():
    assert parser.parse("x") == VariableNode("x")
    assert parser.parse("1") == LiteralNode("1")
    assert parser.parse("   x   ") == VariableNode("x")
    assert parser.parse("   1   ") == LiteralNode("1")
    assert parser.parse("((((((((((x))))))))))") == VariableNode("x")
    assert parser.parse("x") == VariableNode("x")
    assert parser.parse("x") == VariableNode("x")


def test_parser_appl():
    assert parser.parse("x y") == ApplicationNode(VariableNode("x"), VariableNode("y"))
    assert parser.parse("(x y)") == ApplicationNode(VariableNode("x"), VariableNode("y"))
    assert parser.parse("   (    x    y    )   ") == ApplicationNode(VariableNode("x"), VariableNode("y"))
    assert parser.parse("x y z") == ApplicationNode(ApplicationNode(VariableNode("x"), VariableNode("y")), VariableNode("z"))
    assert parser.parse("(x y) z") == ApplicationNode(ApplicationNode(VariableNode("x"), VariableNode("y")), VariableNode("z"))
    assert parser.parse("x y z w") == ApplicationNode(ApplicationNode(ApplicationNode(VariableNode("x"), VariableNode("y")), VariableNode("z")), VariableNode("w"))
    assert parser.parse("(x y) (z w)") == ApplicationNode(ApplicationNode(VariableNode("x"), VariableNode("y")), ApplicationNode(VariableNode("z"), VariableNode("w")))


def test_parser_bin_op():
    assert parser.parse("+ x y") == OperatorPlusNode(VariableNode("x"), VariableNode("y"))
    assert parser.parse("* x y") == OperatorMultiplyNode(VariableNode("x"), VariableNode("y"))
    assert parser.parse("and x y") == OperatorAndNode(VariableNode("x"), VariableNode("y"))
    assert parser.parse("or x y") == OperatorOrNode(VariableNode("x"), VariableNode("y"))
    assert parser.parse("xor x y") == OperatorXorNode(VariableNode("x"), VariableNode("y"))
    assert parser.parse("not x") == OperatorNotNode(VariableNode("x"))
    assert parser.parse("    +     x        y     ") == OperatorPlusNode(VariableNode("x"), VariableNode("y"))
    assert parser.parse(" + x (* y 1)") == OperatorPlusNode(VariableNode("x"), OperatorMultiplyNode(VariableNode("y"), LiteralNode("1")))
    assert parser.parse("and (or  x  y) (xor a b)") == OperatorAndNode(OperatorOrNode(VariableNode("x"), VariableNode("y")),
                                                                       OperatorXorNode(VariableNode("a"), VariableNode("b")))


def test_parser_func():
    assert parser.parse("(^x.x)") == \
           FunctionNode("x", VariableNode("x"))
    assert parser.parse("     (     ^   x   .   x    )    ") == \
           FunctionNode("x", VariableNode("x"))
    assert parser.parse("(^x.(^y.y) x) 1") == \
           ApplicationNode(FunctionNode("x", ApplicationNode(FunctionNode("y", VariableNode("y")), VariableNode("x"))),
                           LiteralNode("1"))
    assert parser.parse("(^x  .(^  y  .  y  )  (^   z  .  z) ) 1") == \
           ApplicationNode(FunctionNode("x", ApplicationNode(FunctionNode("y", VariableNode("y")),
                                                             FunctionNode("z", VariableNode("z")))), LiteralNode("1"))
    assert parser.parse("(^xyz.(x y z)) 1 2 3") == \
           ApplicationNode(ApplicationNode(ApplicationNode(FunctionNode("xyz", ApplicationNode(ApplicationNode(
               VariableNode("x"), VariableNode("y")), VariableNode("z"))),
                                                           LiteralNode("1")), LiteralNode("2")), LiteralNode("3"))
    assert parser.parse("(^xy.(^z.(+ x (* y 2))) 1000 (^t.t)) 4 5") == \
           ApplicationNode(ApplicationNode(FunctionNode("xy", ApplicationNode(ApplicationNode(
               FunctionNode("z", OperatorPlusNode(VariableNode("x"), OperatorMultiplyNode(VariableNode("y"), LiteralNode("2")))),
               LiteralNode("1000")), FunctionNode("t", VariableNode("t")))), LiteralNode("4")), LiteralNode("5"))


def test_invalid_inputs():
    bad_things = ["Bad parentheses.",
                  "Bad function arguments.",
                  "Bad function formatting.",
                  "Bad function.",
                  "Bad input.",
                  "Bad unary operator.",
                  "Bad binary operator."]

    def _helper(expression):
        try:
            parser.parse(expression)
            assert False
        except ValueError as e:
            assert e.args[0] in bad_things

    _helper(")")
    _helper("(")
    _helper("(^t2.t)")
    _helper("(^t+t)")
    _helper("(^)")
    _helper("^t")
    _helper("(^t.)")
    _helper("(^t.((())))")
    _helper("[]")
    _helper("N")
    _helper("$%@#$'")
    _helper("()()x()()")
    _helper("(()x())")
