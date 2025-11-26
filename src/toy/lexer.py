

from toy.tokens import Token, TokenType, KEYWORDS

class Lexer:
    """Analyseur lexical qui transforme le code source en tokens."""
    def __init__(self, source: str) -> None:
        self.source = source
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens: list[Token] = []

    def tokenize(self) -> list[Token]:
        """Transforme le code source en une liste de tokens."""
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", self.line))
        return self.tokens

    def scan_token(self):
        """Analyse le prochain caractère et génère le token correspondant."""
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
            case "{":
                self.add_token(TokenType.LBRACE)
            case "}":
                self.add_token(TokenType.RBRACE)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
            case "=":
                if self.match('='):
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
        """Analyse un nombre (entier ou flottant)."""

        while self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()


        self.add_token(TokenType.NUMBER)

    def identifier(self) -> None:
        """Analyse un identifiant ou un mot-clé."""
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()

        text = self.source[self.start : self.current]
        token_type = KEYWORDS.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)

    def is_at_end(self) -> bool:
        """Vérifie si on a atteint la fin du code source."""
        return self.current >= len(self.source)

    def advance(self):
        """Avance d'un caractère et retourne le caractère consommé."""

        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, token_type: TokenType, literal=None) -> None:
        """Ajoute un token à la liste des tokens."""
        text = self.source[self.start : self.current]
        lexeme = literal if literal is not None else text
        self.tokens.append(Token(token_type, lexeme, self.line))

    def peek(self) -> str:
        """Retourne le caractère courant sans avancer."""
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self) -> str:
        """Retourne le caractère suivant sans avancer."""
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def match(self, expected: str) -> bool:
        """Vérifie si le caractère courant correspond à celui attendu et avance si c'est le cas."""
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True
