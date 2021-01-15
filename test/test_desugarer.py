from lambda_.desugarer import *

desugarer = LambdaDesugarer()


def test_multiple_args_fns():
    stack = deque()

    assert str(desugarer._expand_multi_arg_fns(desugarer.parser.parse("(^xy.(+ x y))"), stack)) == \
           "(^x.(^y.(+ x y)))"
    assert len(stack) == 0
    assert str(desugarer._expand_multi_arg_fns(desugarer.parser.parse("(^xy.(* x y)) 1 2"), stack)) == \
           "((^x.((^y.(* x y)) 2)) 1)"
    assert len(stack) == 0
    assert str(desugarer._expand_multi_arg_fns(desugarer.parser.parse("(^xyz.x y z) 1 2 3"), stack)) == \
           "((^x.((^y.((^z.((x y) z)) 3)) 2)) 1)"
    assert len(stack) == 0
    assert str(desugarer._expand_multi_arg_fns(desugarer.parser.parse("(^xy.(^zt.(z t)) x y) 1 2"), stack)) == \
           "((^x.((^y.((^z.((^t.(z t)) y)) x)) 2)) 1)"
    assert len(stack) == 0
    assert str(desugarer._expand_multi_arg_fns(desugarer.parser.parse("(^xy.(^z.z x y)(^pqr.p q r)) 1 2"), stack)) == \
           "((^x.((^y.((^z.((z x) y)) (^p.(^q.(^r.((p q) r)))))) 2)) 1)"
    assert len(stack) == 0


def test_literals_expanding():
    assert str(desugarer._expand(desugarer.parser.parse("0"))) == "(^sz.z)"
    assert str(desugarer._expand(desugarer.parser.parse("1"))) == "(^sz.(s z))"
    assert str(desugarer._expand(desugarer.parser.parse("2"))) == "(^sz.(s (s z)))"
    assert str(desugarer._expand(desugarer.parser.parse("T"))) == "(^ab.a)"
    assert str(desugarer._expand(desugarer.parser.parse("F"))) == "(^ab.b)"


def test_operators_expanding():
    assert str(desugarer._expand(desugarer.parser.parse("+ x y"))) == "(((^xysz.((x s) ((y s) z))) x) y)"
    assert str(desugarer._expand(desugarer.parser.parse("* x y"))) == "(((^xysz.((x (y s)) z)) x) y)"
    assert str(desugarer._expand(desugarer.parser.parse("and x y"))) == "(((^xy.((x y) (^tf.f))) x) y)"
    assert str(desugarer._expand(desugarer.parser.parse("or x y"))) == "(((^xy.((x (^tf.t)) y)) x) y)"
    assert str(desugarer._expand(desugarer.parser.parse("not x"))) == "((^xtf.((x f) t)) x)"
    assert str(desugarer._expand(desugarer.parser.parse("+ 1 2"))) == \
           "(((^xysz.((x s) ((y s) z))) (^sz.(s z))) (^sz.(s (s z))))"
    assert str(desugarer._expand(desugarer.parser.parse("not T"))) == "((^xtf.((x f) t)) (^ab.a))"


def test_expanding():
    assert str(desugarer._expand(desugarer.parser.parse("(^xyz.x y z) 1 2 3"))) == \
           "((((^xyz.((x y) z)) (^sz.(s z))) (^sz.(s (s z)))) (^sz.(s (s (s z)))))"


# here I started to hate those endless parentheses inside strings and returned to the previous testing format:


def test_substitution():
    assert desugarer.desugar("zero a") == ApplicationNode(FunctionNode("x", ApplicationNode(
        ApplicationNode(VariableNode("x"), FunctionNode("y", FunctionNode("a", FunctionNode("b", VariableNode("b"))))),
        FunctionNode("a", FunctionNode("b", VariableNode("a"))))), VariableNode("a"))
    assert desugarer.desugar("Y") == FunctionNode("f", ApplicationNode(
        FunctionNode("x", ApplicationNode(VariableNode("f"), ApplicationNode(VariableNode("x"), VariableNode("x")))),
        FunctionNode("x", ApplicationNode(VariableNode("f"), ApplicationNode(VariableNode("x"), VariableNode("x"))))))
    assert desugarer.desugar("Y (^xyz.(^ab.a b) x y) 1 2 3") == \
           desugarer.desugar("(^f.(^x.f (x x)) (^x.f (x x))) (^x.(^y.(^z.(^a.(^b.a b) y) x))) 1 2 3")


