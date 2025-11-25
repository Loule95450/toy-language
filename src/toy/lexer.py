"""
The lexer module performs the tokenization of the source code.
The best way to approach it is to build it incrementally.

1. Create the Lexer basic structure:
- tokenize()
- is_at_end()
- advance()
- scan_token()
- add_token()

2. Implement the simplest tokens in scan_token(). Single characters:
- operators: +, -, *, /
- parenthesis: (, )
- ;
- white space skipping

3. Implement numbers :
- peek() to look ahead 1 char
- number()
"""

from toy.tokens import Token, TokenType, KEYWORDS


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens: list[Token] = []

    def tokenize(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()

        match c:
            # Single characters
            case "+":
                self.add_token(TokenType.PLUS)
            case "-":
                self.add_token(TokenType.MINUS)
            case "*":
                self.add_token(TokenType.STAR)
            case "/":
                self.add_token(TokenType.SLASH)
            case "(":
                self.add_token(TokenType.LPAREN)
            case ")":
                self.add_token(TokenType.RPAREN)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            # Ignore whitespaces
            # Don't worry about the string, the string() method will handle them
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1

            # One or 2 characters
            case "=":
                (
                    self.add_token(TokenType.EQUAL_EQUAL)
                    if self.match("=")
                    else self.add_token(TokenType.EQUAL)
                )

            case "<":
                (
                    self.add_token(TokenType.LESS_EQUAL)
                    if self.match("=")
                    else self.add_token(TokenType.LESS)
                )

            case ">":
                (
                    self.add_token(TokenType.GREATER_EQUAL)
                    if self.match("=")
                    else self.add_token(TokenType.GREATER)
                )
            case "!":
                (
                    self.add_token(TokenType.BANG_EQUAL)
                    if self.match("=")
                    else self.add_token(TokenType.BANG)
                )

            # Everything else
            case _:
                if c.isdigit():
                    self.number()
                elif c.isalpha():
                    self.identifier()
                else:
                    raise SyntaxError(
                        f"Unexpected character. character: '{c}', line: {self.line}"
                    )

    def number(self) -> None:
        # We continue to advance until we reach a non-digit character
        while self.peek().isdigit():
            self.advance()

        # Is it a float?
        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()

        # Here we'll have the full number in self.source[self.start : self.current]
        self.add_token(TokenType.NUMBER)

    def identifier(self) -> None:
        # We move until we reach a non-alphanumeric character or _
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()

        text = self.source[self.start : self.current]
        token_type = KEYWORDS.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self):
        # We advance the current position and return the previous character
        # mark the current - 1 as "consumed"
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, token_type: TokenType, literal=None) -> None:
        text = self.source[self.start : self.current]
        lexeme = literal if literal is not None else text
        self.tokens.append(Token(token_type, lexeme, self.line))

    def peek(self) -> str:
        # We look ahead one character (current)
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self) -> str:
        # We look ahead two characters (current + 1)
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True
