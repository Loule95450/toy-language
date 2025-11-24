from toy.ast_nodes import ASTNode, Expression
from toy.tokens import Token, TokenType

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> list[ASTNode]:
        statements = []
        while not self.is_at_end():
            statements.append(self.parse_expression())

        return statements

    ####################
    # Parsing
    ####################
 
    def parse_expression(self) -> Expression:
        return self.parse_term()

    def parse_term(self) -> Expression:
        left = self.parse_primary()

    def parse_primary(self) -> Expression:
        if self.match(TokenType.NUMBER):
            return Literal(float(self.previous().lexeme))

    ####################
    # Utils
    ####################

    def match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check(self, token_type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]