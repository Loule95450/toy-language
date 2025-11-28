
from toy.lexer import Lexer
from toy.parser import Parser
from toy.interpreter import Interpreter
from toy.tokens import TokenType, Token
from toy.ast_nodes import *
import pytest

def evaluate(source: str):
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    result = None
    for statement in ast:
        if hasattr(statement, "expression"):
            result = interpreter.evaluate(statement.expression)
        else:
            interpreter.execute(statement)
    return result

def test_boolean_literals():
    assert evaluate("true;") is True
    assert evaluate("false;") is False

def test_null_literal():
    assert evaluate("null;") is None

def test_string_literal():
    assert evaluate('"hello";') == "hello"

def test_logical_and():
    assert evaluate("true and true;") is True
    assert evaluate("true and false;") is False
    assert evaluate("false and true;") is False
    assert evaluate("false and false;") is False

def test_logical_or():
    assert evaluate("true or true;") is True
    assert evaluate("true or false;") is True
    assert evaluate("false or true;") is True
    assert evaluate("false or false;") is False

def test_logical_short_circuit():
    # If short-circuit works, the second part shouldn't be evaluated (if it has side effects, we can't easily test it with evaluate unless we mock or use print/var)
    # Using variable assignment to test short circuit
    source = """
    var a = 1;
    false and (a = 2);
    a;
    """
    assert evaluate(source) == 1

    source2 = """
    var b = 1;
    true or (b = 2);
    b;
    """
    assert evaluate(source2) == 1
