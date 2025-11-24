from toy.lexer import Lexer
from toy.tokens import TokenType, Token


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
