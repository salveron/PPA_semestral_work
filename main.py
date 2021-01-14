from lambda_parser.parser import *


def main():
    print("Greetings! Please enter a valid lambda expression, so I can desugar it "
          "(use '^' symbol instead of greek lambda and Ctrl+C to exit):")

    while True:
        try:
            input_str = input()

            LambdaParser().parse(input_str)
        # except ExpressionError as e:
        #     print(f"Invalid expression \"{e.args[0]}\". Please try again:")
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()

