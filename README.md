# BI-PPA semestral work by Nikita Mortuzaiev

This is a **Lambda Calculus** "desugarer" program written in **Python 3.8.5**. 
The desugaring is a process of removing symbolic functions from a lambda calculus 
expression, expanding Church numbers, bool literals, arithmetical and logical 
operators and multi-argument functions to fit the pure Lambda Calculus definition.

### Syntax of input expressions

To write a lambda function, use parentheses and `^` symbol instead of Greek lambda.
For example: `(^x.x)` is an equivalent for `λx.x`.

To write an operator expression, type an operator and then its operands (all separated
by spaces). For example: `+ x y`, `and T F`, `not a` and so on.

To use an application, type two or more application parts separated by a space: `x y`, 
`(^x.x) 1`, `x y z t` (which is equivalent for `(((x y) z) t)`).

To use a symbolic function, check the `symbolic_functions` dictionary in `node.nodes`
module. You can easily extend this dictionary with custom definitions. To do this,
type a symbolic function name as an item key and its definition as its value. You
can check existing symbolic functions expansions in the provided tests modules.

### Installation and running

To run, clone this repository and type this:

`python main.py`

The application is written in the pure python with the usage of `re` module, so no 
additional libraries need to be installed.