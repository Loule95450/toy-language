import sys

from toy.interpreter import Interpreter
from toy.lexer import Lexer
from toy.parser import Parser


interpreter = Interpreter()


def run_file(path: str) -> None:
    with open(path, "r") as f:
        source = f.read()
    run(source)


def run(source: str) -> None:
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        interpreter.interpret(ast)

    except (SyntaxError, RuntimeError) as e:
        print(f"Error: {e}")


def repl() -> None:
    print("Toy Language REPL")
    print("Type 'exit' to quit\n")

    while True:
        try:
            line = input(">>> ")
            if line.strip() == "exit":
                break

            run(line)
        except (EOFError, KeyboardInterrupt):
            break


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        repl()
