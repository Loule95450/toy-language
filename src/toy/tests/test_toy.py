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


def interpret(source: str):
    ast = parse(source)
    interpreter = Interpreter()
    interpreter.interpret(ast)
    return interpreter



def test_lexer_tokenize():
    source = """3 + 2; 
    var a = 1; """
    tokens = tokenize(source)
    assert tokens == [

        Token(TokenType.NUMBER, "3", 1),
        Token(TokenType.PLUS, "+", 1),
        Token(TokenType.NUMBER, "2", 1),
        Token(TokenType.SEMICOLON, ";", 1),

        Token(TokenType.VAR, "var", 2),
        Token(TokenType.IDENTIFIER, "a", 2),
        Token(TokenType.EQUAL, "=", 2),
        Token(TokenType.NUMBER, "1", 2),
        Token(TokenType.SEMICOLON, ";", 2),
        Token(TokenType.EOF, "", 2),
    ]



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

def test_parse_if_statement():
    ast = parse("""if (1 == 2) {
                        print 3;
                    } else {
                        print 4;
                    }""")

    assert ast == [
        IfStatement(
            condition=Binary(Literal(1.0), Token(TokenType.EQUAL_EQUAL, "==", 1), Literal(2.0)),
            then_branch=BlockStatement([PrintStatement(Literal(3.0))]),
            else_branch=BlockStatement([PrintStatement(Literal(4.0))]),
        )
    ]

def test_block_environment_scope():
    source = """
    var a = 1;
    var b = 2;
    {
        var a = 2;
        var c = 3;
        b = 10;
    }
    """
    interpreter = interpret(source)

    # The block scope doesn't affect the global a variable
    assert interpreter.environment.get("a") == 1.0

    # The b variable is properly resolved in the block scope from the outer scope
    assert interpreter.environment.get("b") == 10.0

    # The c variable is not defined in the global scope
    with pytest.raises(RuntimeError):
        interpreter.environment.get("c")

def test_while_statement(capsys):
    source = """
    var i = 0;
    while (i < 5) {
        print i;
        i = i + 1;
    }
    """
    interpret(source)
    captured = capsys.readouterr()
    assert captured.out == "0.0\n1.0\n2.0\n3.0\n4.0\n"