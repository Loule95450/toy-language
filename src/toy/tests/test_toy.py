import pytest
from toy.ast_nodes import (
    Binary,
    Literal,
    Unary,
    VarStatement,
    ExpressionStatement,
    VariableAssignment,
)
from toy.interpreter import Interpreter
from toy.lexer import Lexer
from toy.parser import Parser
from toy.tokens import TokenType, Token


def tokenize(source: str) -> list[Token]:
    """Tokenize source code."""
    lexer = Lexer(source)
    return lexer.tokenize()


def parse(source: str) -> list:
    """Parse source code into AST."""
    tokens = tokenize(source)
    parser = Parser(tokens)
    return parser.parse()


def evaluate(source: str):
    """Evaluate source code and return result."""
    ast = parse(source)
    interpreter = Interpreter()
    result = None
    for statement in ast:
        if hasattr(statement, "expression"):
            result = interpreter.evaluate(statement.expression)
        else:
            interpreter.execute(statement)
    return result


# Lexer tests
def test_lexer_tokenize():
    source = """3 + 2; 
    var a = 1; """
    tokens = tokenize(source)
    assert tokens == [
        # Line 1
        Token(TokenType.NUMBER, "3", 1),
        Token(TokenType.PLUS, "+", 1),
        Token(TokenType.NUMBER, "2", 1),
        Token(TokenType.SEMICOLON, ";", 1),
        # Line 2
        Token(TokenType.VAR, "var", 2),
        Token(TokenType.IDENTIFIER, "a", 2),
        Token(TokenType.EQUAL, "=", 2),
        Token(TokenType.NUMBER, "1", 2),
        Token(TokenType.SEMICOLON, ";", 2),
        Token(TokenType.EOF, "", 2),
    ]


# Parser tests
def test_parse_term():
    ast = parse("3 + 2;")
    assert ast == [
        ExpressionStatement(
            Binary(
                Literal(3.0),
                Token(TokenType.PLUS, "+", 1),
                Literal(2.0),
            )
        ),
    ]


def test_parse_factor():
    ast = parse("3 + 2 * 4;")
    assert ast == [
        ExpressionStatement(
            Binary(
                Literal(3.0),
                Token(TokenType.PLUS, "+", 1),
                Binary(
                    Literal(2.0),
                    Token(TokenType.STAR, "*", 1),
                    Literal(4.0),
                ),
            )
        ),
    ]


def test_parse_factor_with_parenthesis():
    ast = parse("(3 + 2) * 4;")
    assert ast == [
        ExpressionStatement(
            Binary(
                Binary(
                    Literal(3.0),
                    Token(TokenType.PLUS, "+", 1),
                    Literal(2.0),
                ),
                Token(TokenType.STAR, "*", 1),
                Literal(4.0),
            )
        )
    ]


def test_parse_unary():
    ast = parse("-3 + !2;")
    assert ast == [
        ExpressionStatement(
            Binary(
                Unary(
                    Token(TokenType.MINUS, "-", 1),
                    Literal(3.0),
                ),
                Token(TokenType.PLUS, "+", 1),
                Unary(
                    Token(TokenType.BANG, "!", 1),
                    Literal(2.0),
                ),
            )
        )
    ]


def test_parse_comparison_operators():
    ast = parse("3 > 2;")
    assert ast == [
        ExpressionStatement(
            Binary(
                Literal(3.0),
                Token(TokenType.GREATER, ">", 1),
                Literal(2.0),
            )
        )
    ]


def test_parse_equality_operators():
    ast = parse("3 == 2;")
    assert ast == [
        ExpressionStatement(
            Binary(
                Literal(3.0),
                Token(TokenType.EQUAL_EQUAL, "==", 1),
                Literal(2.0),
            )
        )
    ]


def test_parse_comparison_with_equality():
    # Test precedence: comparison binds tighter than equality
    ast = parse("3 > 2 == 4;")  # (3 > 2) == 4
    assert ast == [
        ExpressionStatement(
            Binary(
                Binary(
                    Literal(3.0),
                    Token(TokenType.GREATER, ">", 1),
                    Literal(2.0),
                ),
                Token(TokenType.EQUAL_EQUAL, "==", 1),
                Literal(4.0),
            )
        )
    ]


def test_parse_var_declaration():
    ast = parse("var a = 1;")
    assert ast == [
        VarStatement(
            Token(TokenType.IDENTIFIER, "a", 1),
            Literal(1.0),
        )
    ]


def test_parse_var_assignment():
    ast = parse("var a = 1; a = 2;")
    assert ast == [
        VarStatement(
            Token(TokenType.IDENTIFIER, "a", 1),
            Literal(1.0),
        ),
        ExpressionStatement(
            VariableAssignment(
                Token(TokenType.IDENTIFIER, "a", 1),
                Literal(2.0),
            )
        ),
    ]


# Interpreter tests
@pytest.mark.parametrize(
    "source,expected",
    [
        ("3 + 2 * 4;", 11.0),  # Precedence: 3 + (2 * 4)
        ("3 + 2 > 4;", True),  # Comparison: 5 > 4
        ("3 + 2 == 5;", True),  # Equality: 5 == 5
        ("3 + 2 == 4;", False),  # Equality: 5 == 4
        ("-2 + 3;", 1),  # Unary: 1
        ("var a = 1; a + 1;", 2),  # VariableAssignment: 2
    ],
)
def test_evaluate_expressions(source, expected):
    assert evaluate(source) == expected
