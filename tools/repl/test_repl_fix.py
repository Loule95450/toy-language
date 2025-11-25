"""Test script to verify REPL doesn't redisplay output."""

import sys
from pathlib import Path
from io import StringIO

# Add src to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from toy.interpreter import Interpreter
from toy.lexer import Lexer
from toy.parser import Parser


def test_repl_no_redisplay():
    """Simulate REPL behavior to verify output is not redisplayed."""
    interpreter = Interpreter()
    source = ""
    executed_count = 0

    print("Testing REPL behavior...")
    print("=" * 50)

    # First input: print 1
    print("\n>>> print 1")
    source += "print 1\n"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    old_stdout = sys.stdout
    sys.stdout = StringIO()
    start_idx = executed_count
    interpreter.interpret(ast, start_index=start_idx)
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    executed_count = len(ast)

    print(f"Output: {output.rstrip()}")
    assert output.strip() == "1", f"Expected '1', got '{output.strip()}'"

    # Second input: print 2
    print("\n>>> print 2")
    source += "print 2\n"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    old_stdout = sys.stdout
    sys.stdout = StringIO()
    start_idx = executed_count
    interpreter.interpret(ast, start_index=start_idx)
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    executed_count = len(ast)

    print(f"Output: {output.rstrip()}")
    assert output.strip() == "2", f"Expected '2', got '{output.strip()}' (should NOT include '1')"

    # Third input: print 3
    print("\n>>> print 3")
    source += "print 3\n"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    old_stdout = sys.stdout
    sys.stdout = StringIO()
    start_idx = executed_count
    interpreter.interpret(ast, start_index=start_idx)
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    executed_count = len(ast)

    print(f"Output: {output.rstrip()}")
    assert output.strip() == "3", f"Expected '3', got '{output.strip()}' (should NOT include '1' or '2')"

    # Test with variables (verify state persists)
    print("\n>>> var x = 10")
    source += "var x = 10\n"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    old_stdout = sys.stdout
    sys.stdout = StringIO()
    start_idx = executed_count
    interpreter.interpret(ast, start_index=start_idx)
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    executed_count = len(ast)

    print(f"Output: {output.rstrip() if output else '(no output)'}")

    print("\n>>> print x")
    source += "print x\n"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    old_stdout = sys.stdout
    sys.stdout = StringIO()
    start_idx = executed_count
    interpreter.interpret(ast, start_index=start_idx)
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    executed_count = len(ast)

    print(f"Output: {output.rstrip()}")
    assert output.strip() == "10", f"Expected '10', got '{output.strip()}'"

    print("\n" + "=" * 50)
    print("✓ All tests passed! Output is not being redisplayed.")
    print("✓ Interpreter state persists across inputs.")


if __name__ == "__main__":
    test_repl_no_redisplay()
