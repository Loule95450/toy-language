from dataclasses import dataclass
from enum import auto, StrEnum


class TokenType(StrEnum):
    """Énumération des types de tokens."""
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    COMMA = auto()
    MINUS = auto()
    PLUS = auto()
    SLASH = auto()
    STAR = auto()

    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()

    AND = auto()
    ELSE = auto()
    FALSE = auto()
    FN = auto()
    FOR = auto()
    IF = auto()
    NULL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()
    MATCH = auto()
    CASE = auto()
    ARROW = auto()

    EOF = auto()

@dataclass
class Token:
    """Représente un token avec son type, son lexème et sa ligne."""
    type: TokenType
    lexeme: str
    line: int

KEYWORDS = {
    "and": TokenType.AND,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "fn": TokenType.FN,
    "for": TokenType.FOR,
    "if": TokenType.IF,
    "null": TokenType.NULL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
    "match": TokenType.MATCH,
    "case": TokenType.CASE,
}
