import pytest
from toy.ast_nodes import *
from toy.interpreter import Interpreter
from toy.lexer import Lexer
from toy.parser import Parser
from toy.tokens import TokenType, Token

def tokenize(source: str) -> list[Token]:
    lexer = Lexer(source)
    return lexer.tokenize()

def parse(source: str) -> list:
    tokens = tokenize(source)
    parser = Parser(tokens)
    return parser.parse()

def evaluate(source: str):
    ast = parse(source)
    interpreter = Interpreter()
    result = None
    for statement in ast:
        if hasattr(statement, "expression"):
            result = interpreter.evaluate(statement.expression)
        else:
            interpreter.execute(statement)
    return result

def test_match_tokenization():
    source = "match x { case 1 => 2 }"
    tokens = tokenize(source)
    # Expected tokens: MATCH IDENTIFIER LBRACE CASE NUMBER ARROW NUMBER RBRACE EOF
    token_types = [t.type for t in tokens]
    assert token_types == [
        TokenType.MATCH, TokenType.IDENTIFIER, TokenType.LBRACE,
        TokenType.CASE, TokenType.NUMBER, TokenType.ARROW, TokenType.NUMBER,
        TokenType.RBRACE, TokenType.EOF
    ]

def test_match_parsing():
    source = "match 1 { case 1 => 2, case 3 => 4 };"
    ast = parse(source)
    # Should be an ExpressionStatement containing MatchExpression
    assert isinstance(ast[0], ExpressionStatement)
    match_expr = ast[0].expression
    assert isinstance(match_expr, MatchExpression)
    assert len(match_expr.cases) == 2
    assert isinstance(match_expr.cases[0], MatchCase)
    assert isinstance(match_expr.cases[0].pattern, Literal)
    assert match_expr.cases[0].pattern.value == 1.0
    assert match_expr.cases[0].body.value == 2.0

def test_match_evaluation_success():
    source = """
    var x = 2;
    match x {
        case 1 => 10,
        case 2 => 20,
        case 3 => 30
    };
    """
    result = evaluate(source)
    assert result == 20.0

def test_match_evaluation_expressions():
    source = """
    match 1 + 1 {
        case 2 => 2 * 2,
        case 3 => 0
    };
    """
    result = evaluate(source)
    assert result == 4.0

def test_match_no_match_error():
    source = """
    match 5 {
        case 1 => 10
    };
    """
    with pytest.raises(RuntimeError, match="No match for value"):
        evaluate(source)
