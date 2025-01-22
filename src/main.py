import os

from lamb_da.desugarer import *


def main():
    symbolic_functions = {
        "succ": "(^xsz.s (x s z))",
        "pred": "(^xsz. x (^fg.g (f s)) (^g.z) (^m.m))",
        "true": "T",
        "false": "F",
        "zero": "(^x.x (^y.F) T)",
        "Y": "(^f.(^x.f (x x)) (^x.f (x x)))",
    }

    print("\nRunning tests...")

    os.system("pytest")

    print("\nGreetings! To start off, please enter your custom symbolic functions using this format: "
          "<name>: <definition> (for example, true: (^ab.a)).\n\nPredefined symbolic functions are:")

    for key, val in symbolic_functions.items():
        print(f"    {key}: {val}")

    print("\nUse the '^' symbol instead of the greek lambda, and when you are done, print \"done\" (use Ctrl+C to exit):")

    symb_fn_pattern = re.compile("(?P<name>.+?): (?P<definition>.+)")
    while True:
        print("> ", end="")
        try:
            input_str = input()
        except KeyboardInterrupt:
            return

        if input_str == "done":
            break

        match = symb_fn_pattern.fullmatch(input_str)
        if not match:
            print("Your input is wrong. Please try again:")
            continue
        name, definition = match.groupdict()["name"], match.groupdict()["definition"]
        try:
            LambdaParser(dict()).parse(definition)
        except ValueError as e:
            print(f"Your function definition is not correct. Please try again (error message: {e.args[0]}):")
            continue

        symbolic_functions[name] = definition

    print("\nNow enter a valid lambda expression, so I can desugar it "
          "(use Ctrl+C to exit):")

    while True:
        print("> ", end="")
        try:
            input_str = input()
            LambdaDesugarer(symbolic_functions).desugar(input_str)
        except ValueError as e:
            print(*e.args, "Please try again:")
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()

