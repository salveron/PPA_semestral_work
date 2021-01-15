import os

from lambda_.desugarer import *


def main():
    print("\nRunning tests...")

    os.system("pytest")

    print("\nGreetings! Please enter a valid lambda expression, so I can desugar it "
          "(use '^' symbol instead of greek lambda and Ctrl+C to exit):")

    while True:
        try:
            input_str = input()
            LambdaDesugarer().desugar(input_str)
        except ValueError as e:
            print(*e.args, "Please try again:")
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()

