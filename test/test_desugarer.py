from lambda_.desugarer import LambdaDesugarer, deque

desugarer = LambdaDesugarer()


def test_multiple_args_fns():
    stack = deque()

    assert str(desugarer._expand_multi_arg_fns(desugarer.parser.parse("(^xy.(+ x y))"), stack)) == \
           "(^x.(^y.(+ x y)))"
    assert len(stack) == 0
    assert str(desugarer._expand_multi_arg_fns(desugarer.parser.parse("(^xy.(* x y)) 1 2"), stack)) == \
           "(^x.(^y.(* x y)) 2) 1"
    assert len(stack) == 0
    assert str(desugarer._expand_multi_arg_fns(desugarer.parser.parse("(^xyz.x y z) 1 2 3"), stack)) == \
           "(^x.(^y.(^z.((x y) z)) 3) 2) 1"
    assert len(stack) == 0
    assert str(desugarer._expand_multi_arg_fns(desugarer.parser.parse("(^xy.(^zt.(z t)) x y) 1 2"), stack)) == \
           "(^x.(^y.(^z.(^t.(z t)) y) x) 2) 1"
    assert len(stack) == 0
    assert str(desugarer._expand_multi_arg_fns(desugarer.parser.parse("(^xy.(^z.z x y)(^pqr.p q r)) 1 2"), stack)) == \
           "(^x.(^y.(^z.((z x) y)) (^p.(^q.(^r.((p q) r))))) 2) 1"
    assert len(stack) == 0


def test_literals_expanding():
    assert str(desugarer._expand_literals(desugarer.parser.parse("0"))) == "(^sz.z)"
    assert str(desugarer._expand_literals(desugarer.parser.parse("1"))) == "(^sz.(s z))"
    assert str(desugarer._expand_literals(desugarer.parser.parse("2"))) == "(^sz.(s (s z)))"
    assert str(desugarer._expand_literals(desugarer.parser.parse("T"))) == "(^ab.a)"
    assert str(desugarer._expand_literals(desugarer.parser.parse("F"))) == "(^ab.b)"
    assert str(desugarer._expand_literals(desugarer.parser.parse("+ 2 1"))) == "(+ (^sz.(s (s z))) (^sz.(s z)))"
    assert str(desugarer._expand_literals(desugarer.parser.parse("(^xyz.x y z) 1 2 3"))) == \
           "(((^xyz.((x y) z)) (^sz.(s z)) (^sz.(s (s z)))) (^sz.(s (s (s z)))))"


