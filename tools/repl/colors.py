"""Centralized color scheme for REPL display components."""

from toy.tokens import TokenType


def get_token_color(token_type: TokenType) -> str:
    """Get color for a token type.

    Args:
        token_type: The token type to get color for

    Returns:
        Color name as string for Rich markup
    """
    match token_type:
        # Keywords
        case (
            TokenType.AND
            | TokenType.ELSE
            | TokenType.FALSE
            | TokenType.FN
            | TokenType.FOR
            | TokenType.IF
            | TokenType.NULL
            | TokenType.OR
            | TokenType.PRINT
            | TokenType.RETURN
            | TokenType.TRUE
            | TokenType.VAR
            | TokenType.WHILE
        ):
            return "cyan"
        # Literals
        case TokenType.NUMBER | TokenType.STRING:
            return "yellow"
        # Identifiers
        case TokenType.IDENTIFIER:
            return "green"
        # Operators
        case (
            TokenType.PLUS
            | TokenType.MINUS
            | TokenType.STAR
            | TokenType.SLASH
            | TokenType.BANG
            | TokenType.BANG_EQUAL
            | TokenType.EQUAL
            | TokenType.EQUAL_EQUAL
            | TokenType.GREATER
            | TokenType.GREATER_EQUAL
            | TokenType.LESS
            | TokenType.LESS_EQUAL
        ):
            return "magenta"
        # Delimiters
        case (
            TokenType.LPAREN
            | TokenType.RPAREN
            | TokenType.LBRACE
            | TokenType.RBRACE
            | TokenType.SEMICOLON
            | TokenType.COMMA
        ):
            return "blue"
        # EOF and others
        case _:
            return "white"


# AST node colors
NODE_TYPE_COLOR = "cyan"
NODE_LABEL_COLOR = "yellow"
NODE_UNKNOWN_COLOR = "dim cyan"
