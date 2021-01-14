from lambda_parser.parser import LambdaParser
from node.nodes import *
from node.binary_operators import *

parser = LambdaParser()


def test_parser_varnum():
    assert parser.parse("x") == VariableNode("x")
    assert parser.parse("1") == NumberNode("1")
    assert parser.parse("   x   ") == VariableNode("x")
    assert parser.parse("   1   ") == NumberNode("1")
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


def test_parser_binop():
    assert parser.parse("+ x y") == OperatorPlusNode(VariableNode("x"), VariableNode("y"))
    assert parser.parse("- x y") == OperatorMinusNode(VariableNode("x"), VariableNode("y"))
    assert parser.parse("* x y") == OperatorMultiplyNode(VariableNode("x"), VariableNode("y"))
    assert parser.parse("/ x y") == OperatorDivideNode(VariableNode("x"), VariableNode("y"))
    assert parser.parse("    +     x        y     ") == OperatorPlusNode(VariableNode("x"), VariableNode("y"))
    assert parser.parse(" + x (- y 1)") == OperatorPlusNode(VariableNode("x"), OperatorMinusNode(VariableNode("y"), NumberNode("1")))
    assert parser.parse("+ (*  x  3) (/ y z)") == OperatorPlusNode(OperatorMultiplyNode(VariableNode("x"), NumberNode("3")), OperatorDivideNode(VariableNode("y"), VariableNode("z")))


def test_parser_func():
    assert parser.parse("(^x.x)") == \
           FunctionNode("x", VariableNode("x"))
    assert parser.parse("     (     ^   x   .   x    )    ") == \
           FunctionNode("x", VariableNode("x"))
    assert parser.parse("(^x.(^y.y) x) 1") == \
           ApplicationNode(FunctionNode("x", ApplicationNode(FunctionNode("y", VariableNode("y")), VariableNode("x"))),
                           NumberNode("1"))
    assert parser.parse("(^x  .(^  y  .  y  )  (^   z  .  z) ) 1") == \
           ApplicationNode(FunctionNode("x", ApplicationNode(FunctionNode("y", VariableNode("y")),
                                                             FunctionNode("z", VariableNode("z")))), NumberNode("1"))
    assert parser.parse("(^xyz.(x y z)) 1 2 3") == \
           ApplicationNode(ApplicationNode(ApplicationNode(FunctionNode("xyz", ApplicationNode(ApplicationNode(
               VariableNode("x"), VariableNode("y")), VariableNode("z"))),
               NumberNode("1")), NumberNode("2")), NumberNode("3"))
    assert parser.parse("(^xy.(^z.(+ x (/ y 2))) 1000 (^t.t)) 4 5") == \
           ApplicationNode(ApplicationNode(FunctionNode("xy", ApplicationNode(ApplicationNode(
               FunctionNode("z", OperatorPlusNode(VariableNode("x"), OperatorDivideNode(VariableNode("y"), NumberNode("2")))),
               NumberNode("1000")), FunctionNode("t", VariableNode("t")))), NumberNode("4")), NumberNode("5"))


def test_invalid_inputs():
    bad_things = ["Bad parentheses.",
                  "Bad function arguments.",
                  "Bad function formatting.",
                  "Bad function.",
                  "Bad input."]

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
