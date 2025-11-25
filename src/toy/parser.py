"""This parser implements a recursive descent parser for the language.

The grammar can be found in @README.md#grammar.

Recursive descent reads the tokens like a human would do:
1. Each grammar rule becomes a parse_* method (e.g., parse_expression(), parse_term(), parse_factor())
2. Each method consumes tokens and returns an AST node
3. Methods call each other following the grammar structure

Example: parsing "3 + 2 * 5"
- parse_expression() calls parse_term() => gets Literal(3)
- Sees PLUS, so continues: calls parse_term() again
- parse_term() calls parse_factor() => gets Literal(2)
- Sees STAR (higher precedence!), so continues: calls parse_factor() => gets Literal(5)
- parse_term() returns Binary(2, *, 5)
- parse_expression() returns Binary(3, +, Binary(2, *, 5))

Result: 3 + (2 * 5) — multiplication grouped first due to grammar structure.
"""

from _ast import Assign
from typing import Callable

from toy.ast_nodes import (
    ASTNode,
    Binary,
    Literal,
    Unary,
    VarStatement,
    Expression,
    Statement,
    ExpressionStatement,
    Variable,
    VariableAssignment,
    PrintStatement,
)
from toy.tokens import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current = 0

    def parse(self) -> list[ASTNode]:
        statements = []
        while not self.is_at_end():
            statements.append(self.parse_declaration())
        return statements

    def parse_declaration(self) -> Statement:
        """In Toy, everything is a statement!"""
        if self.match(TokenType.VAR):
            return self.parse_var_declaration()

        return self.parse_statement()

    ##########################################################################
    # Parsing statements
    ##########################################################################

    def parse_var_declaration(self) -> Statement:
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

        # Here's a language design decision. We authorize a variable to be declared without an initializer.
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.parse_expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")

        return VarStatement(name, initializer)

    def parse_statement(self) -> Statement:
        """Here we parse every statement that is NOT a variable/function declaration."""
        if self.match(TokenType.PRINT):
            return self.parse_print_statement()

        return self.parse_expression_statement()

    def parse_print_statement(self) -> Statement:
        expr = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return PrintStatement(expr)

    def parse_expression_statement(self) -> Statement:
        expr = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return ExpressionStatement(expr)

    ##########################################################################
    # Parsing expressions
    ##########################################################################

    def parse_expression(self) -> Expression:
        """Entry point to parse an expression. This method will delegate to other parse_* methods."""
        return self.parse_assignment()

    def parse_assignment(self) -> Expression:
        expr = self.parse_equality()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.parse_assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return VariableAssignment(name, value)

            raise SyntaxError(f"Invalid assignment target. token: {equals.lexeme}")

        return expr

    def parse_equality(self) -> Expression:
        return self.binary_left(
            self.parse_comparison,
            [
                TokenType.EQUAL_EQUAL,
                TokenType.BANG_EQUAL,
            ],
        )

    def parse_comparison(self) -> Expression:
        return self.binary_left(
            self.parse_term,
            [
                TokenType.GREATER,
                TokenType.GREATER_EQUAL,
                TokenType.LESS,
                TokenType.LESS_EQUAL,
            ],
        )

    def parse_term(self) -> Expression:
        """A term is an addition or subtraction of factors. Exemple:
        * 4 + 2
        * 10 - 7
        * x + 3
        """
        return self.binary_left(self.parse_factor, [TokenType.PLUS, TokenType.MINUS])

    def parse_factor(self) -> Expression:
        """A factor is a multiplication or division of a primary. Examples:
        * 3 * 4
        * 10 / 2
        """
        return self.binary_left(self.parse_unary, [TokenType.STAR, TokenType.SLASH])

    def parse_unary(self) -> Expression:
        """A unary operator is a primary prefix. Examples:
        * ! (bang)
        * - (minus)
        """
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.parse_unary()
            return Unary(operator, right)

        return self.parse_primary()

    def parse_primary(self) -> Expression:
        """A primary is an atomic expression that cannot be decomposed. Examples:
        * 42
        * "hello"
        * x
        """
        if self.match(TokenType.NUMBER):
            return Literal(float(self.previous().lexeme))

        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())

        # if we have a LPAREN, the order here is:
        # 1. match advances self.current
        # 2. parse_expression will return the expression inside the LPAREN
        # 3. the RPAREN is consumed (everything is already stored inside the BinaryOp ASTNode)
        if self.match(TokenType.LPAREN):
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression.")
            return expr

        raise SyntaxError(
            f"Unexpected token. token: {self.peek().lexeme}, line: {self.peek().line}"
        )

    ##########################################################################
    # Utils
    ##########################################################################

    def binary_left(
        self,
        operand_fn: Callable[[], Expression],
        operators: list[TokenType],
    ) -> Expression:
        """Factorize a binary operation parsing"""
        left = operand_fn()

        while self.match(*operators):
            operator = self.previous()
            right = operand_fn()
            left = Binary(left, operator, right)

        return left

    def is_at_end(self) -> bool:
        """Returns True if we've reached the end of the input."""
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        """Returns the current token without advancing the parser."""
        return self.tokens[self.current]

    def match(self, *types: TokenType) -> bool:
        """If the current token matches, we advance the parser and return True."""
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def check(self, token_type: TokenType) -> bool:
        """Check if the current token matches the given token type.
        DOES NOT advance the parser."""
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def advance(self) -> Token:
        """Advance the parser to the next token and return the previous token."""
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def consume(self, token_type: TokenType, error_message: str) -> Token:
        if self.check(token_type):
            return self.advance()
        raise SyntaxError(f"{error_message} at line {self.peek().line}")

    # For debug purpose only (to see the current state of the parser)
    @property
    def current_token(self) -> Token:
        return self.tokens[self.current]

    @property
    def previous_token(self) -> Token | None:
        if self.current <= 0:
            return None
        return self.tokens[self.current - 1]

    @property
    def next_token(self) -> Token | None:
        if self.current >= len(self.tokens) - 1:
            return None
        return self.tokens[self.current + 1]
