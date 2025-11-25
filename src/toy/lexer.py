from toy.tokens import KEYWORDS, TokenType, Token

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []
        self.line = 1
        
        self.start = 0
        self.current = 0

    def tokenize(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()
        
        match c:
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
            case "!=":
                self.add_token(TokenType.BANG_EQUAL)
            case "=":
                if self.match("="):
                    self.add_token(TokenType.EQUAL_EQUAL)
                else:
                    self.add_token(TokenType.EQUAL)
            case "<":
                if self.match("="):
                    self.add_token(TokenType.LESS_EQUAL)
                else:
                    self.add_token(TokenType.LESS)
            case ">":
                if self.match("="):
                    self.add_token(TokenType.GREATER_EQUAL)
                else:
                    self.add_token(TokenType.GREATER)
            case "!":
                if self.match("="):
                    self.add_token(TokenType.BANG_EQUAL)
                else:
                    self.add_token(TokenType.BANG)
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
            case _:
                if c.isdigit():
                    self.number()
                elif c.isalpha():
                    self.identifier()
                else:
                    raise SyntaxError(f"Unexpected character {c}, line={self.line}")

    def number(self) -> None:
        while self.peek().isdigit():
            self.advance()
        
        self.add_token(TokenType.NUMBER)

    def identifier(self) -> None:
        # Si on parse var, on aura start=0, current=3
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()
        
        text = self.source[self.start:self.current]
        token_type = KEYWORDS.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def add_token(self, token_type: TokenType, literal: str | None = None):
        text = self.source[self.start:self.current]
        lexeme = literal if literal else text
        self.tokens.append(Token(token_type, lexeme, self.line))

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)
    
    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True