from lambda_parser.parser import LambdaParser

parser = LambdaParser()


def test_variable_re_pattern():
    assert parser.variable_re_pattern.fullmatch("x").groupdict() == {"var": "x"}
    assert parser.variable_re_pattern.fullmatch("y").groupdict() == {"var": "y"}
    assert parser.variable_re_pattern.fullmatch(" x ") is None
    assert parser.variable_re_pattern.fullmatch("(x)") is None


def test_binary_operator_re_pattern():
    assert parser.binary_operator_re_pattern.fullmatch("- x y") \
        .groupdict() == {"sign": "-", "left": "x", "right": "y"}
    assert parser.binary_operator_re_pattern.fullmatch("+      x      y") \
        .groupdict() == {"sign": "+", "left": "x", "right": "y"}
