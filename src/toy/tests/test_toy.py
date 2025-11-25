from toy.interpreter import Interpreter
from toy.parser import Parser
from toy.lexer import Lexer
from toy.tokens import TokenType, Token
from toy.ast_nodes import Binary, Literal


def test_lexer_tokenize():
    source = "3 + 2"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    assert tokens == [
        Token(TokenType.NUMBER, "3", 1),
        Token(TokenType.PLUS, "+", 1),
        Token(TokenType.NUMBER, "2", 1),
        Token(TokenType.EOF, "", 1),
    ]


def test_lexer_tokenize_ignored_chars():
    source = "2\t * 3\n / 4"
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    assert tokens == [
        Token(TokenType.NUMBER, "2", 1),
        Token(TokenType.STAR, "*", 1),
        Token(TokenType.NUMBER, "3", 1),
        Token(TokenType.SLASH, "/", 2),
        Token(TokenType.NUMBER, "4", 2),
        Token(TokenType.EOF, "", 2),
    ]

def test_parse_term():
    source = "3 + 2"
    lexer = Lexer(source)

    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    assert ast == [
        Binary(
            Literal(3.0),
            Token(TokenType.PLUS, "+", 1),
            Literal(2.0),
        ),
    ]

def test_parse_factor():
    source = "3 + 2 * 4"
    lexer = Lexer(source)

    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    assert ast == [
        Binary(
            Literal(3.0),
            Token(TokenType.PLUS, "+", 1),
            Binary(
                Literal(2.0),
                Token(TokenType.STAR, "*", 1),
                Literal(4.0),
            ),
        ),
    ]

def test_evaluate_factor():
    source = "3 + 2 * 4"  # 3 + (2 * 4)

    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()

    result = None
    for statement in ast:
        result = interpreter.evaluate(statement)
    assert result == 11.0

def test_evaluate_comparison():
    source = "3 * 2 > 4" # (3 * 2) > 4
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()

    result = None
    for statement in ast:
        result = interpreter.evaluate(statement)
    assert result == True

def test_parse_comparison_equality():
    source = "3 > 2 == 4" # (3 > 2) == 4
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    assert ast == [
        Binary(
            Binary(
                Literal(3.0),
                Token(TokenType.GREATER, ">", 1),
                Literal(2.0),
            ),
            Token(TokenType.EQUAL_EQUAL, "==", 1),
            Literal(4.0),
        ),
    ]