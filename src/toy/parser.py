

from toy.ast_nodes import *
from typing import Callable
from toy.tokens import Token, TokenType


class Parser:
    """Analyseur syntaxique qui transforme les tokens en AST."""
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current = 0

    def parse(self) -> list[ASTNode]:
        """Point d'entrée pour analyser les tokens et produire une liste d'instructions."""
        statements = []
        while not self.is_at_end():
            statements.append(self.parse_declaration())
        return statements

    def parse_declaration(self) -> Statement:
        """Analyse une déclaration (variable ou instruction)."""

        if self.match(TokenType.VAR):
            return self.parse_var_declaration()
        if self.match(TokenType.FN):
            return self.parse_function_declaration()

        return self.parse_statement()

    ##########################################################################
    # Parsing statements
    ##########################################################################

    def parse_var_declaration(self) -> Statement:
        """Analyse une déclaration de variable."""
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.parse_expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")

        return VarStatement(name, initializer)

    def parse_function_declaration(self) -> Statement:
        name = self.consume(TokenType.IDENTIFIER, "Expect function name.")
        self.consume(TokenType.LPAREN, "Expect '(' after function name.")

        parameters = []
        if not self.check(TokenType.RPAREN):
            parameters.append(
                self.consume(TokenType.IDENTIFIER, "Expect parameter name.")
            )
            while self.match(TokenType.COMMA):
                parameters.append(
                    self.consume(TokenType.IDENTIFIER, "Expect parameter name.")
                )

        self.consume(TokenType.RPAREN, "Expect ')' after parameters.")
        self.consume(TokenType.LBRACE, "Expect '{' before function body.")

        body = []
        while not self.check(TokenType.RBRACE):
            body.append(self.parse_declaration())

        self.consume(TokenType.RBRACE, "Expect '}' after function body.")
        return FunctionDeclarationStatement(name, parameters, body)

    def parse_statement(self) -> Statement:
        """Analyse une instruction (autre que déclaration)."""
        if self.match(TokenType.PRINT):
            return self.parse_print_statement()
        if self.match(TokenType.IF):
            return self.parse_if_statement()
        if self.match(TokenType.WHILE):
            return self.parse_while_statement()
        if self.match(TokenType.FOR):
            return self.parse_for_statement()
        if self.match(TokenType.LBRACE):
            return self.parse_block_statement()
        if self.match(TokenType.RETURN):
            return self.parse_return_statement()

        return self.parse_expression_statement()


    def parse_print_statement(self) -> Statement:
        """Analyse une instruction d'affichage."""
        expr = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return PrintStatement(expr)

    def parse_if_statement(self) -> Statement:
        """Analyse une instruction conditionnelle."""
        self.consume(TokenType.LPAREN, "Expect '(' after 'if'")
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN, "Expect ')' after 'if'")
        then_branch = self.parse_statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.parse_statement()

        return IfStatement(condition, then_branch, else_branch)

    def parse_while_statement(self) -> Statement:
        """Analyse une instruction conditionnelle."""
        self.consume(TokenType.LPAREN, "Expect '(' after 'while'")
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN, "Expect ')' after 'while'")

        body = self.parse_statement()
        return WhileStatement(condition, body)

    def parse_for_statement(self) -> Statement:
        """Analyse une instruction conditionnelle."""
        self.consume(TokenType.LPAREN, "Expect '(' after 'for'.")

        initializer = None
        if self.match(TokenType.SEMICOLON):
            pass
        elif self.match(TokenType.VAR):
            initializer = self.parse_var_declaration()
        else:
            initializer = self.parse_expression_statement()

        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment = None
        if not self.check(TokenType.RPAREN):
            increment = self.parse_expression()
        self.consume(TokenType.RPAREN, "Expect ')' after for clauses.")

        body = self.parse_statement()

        if increment is not None:
            body = BlockStatement([body, ExpressionStatement(increment)])

        if condition is None:
            condition = Literal(True)

        body = WhileStatement(condition, body)

        if initializer is not None:
            body = BlockStatement([initializer, body])

        return body

    def parse_return_statement(self) -> Statement:
        keyword = self.previous()

        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.parse_expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return ReturnStatement(keyword, value)

    def parse_block_statement(self) -> BlockStatement:
        """Analyse une instruction de bloc."""
        statements = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            statements.append(self.parse_declaration())
        self.consume(TokenType.RBRACE, "Expect '}' after block.")
        return BlockStatement(statements)

    def parse_expression_statement(self) -> Statement:
        """Analyse une instruction d'expression."""
        expr = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return ExpressionStatement(expr)

    ##########################################################################
    # Parsing expressions
    ##########################################################################

    def parse_expression(self) -> Expression:
        """Analyse une expression."""
        return self.parse_assignment()

    def parse_assignment(self) -> Expression:
        """Analyse une assignation."""
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
        """Analyse une égalité."""
        return self.binary_left(
            self.parse_comparison,
            [
                TokenType.EQUAL_EQUAL,
                TokenType.BANG_EQUAL,
            ],
        )

    def parse_comparison(self) -> Expression:
        """Analyse une comparaison."""
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
        """Analyse un terme (addition/soustraction)."""
        return self.binary_left(self.parse_factor, [TokenType.PLUS, TokenType.MINUS])

    def parse_factor(self) -> Expression:
        """Analyse un facteur (multiplication/division)."""
        return self.binary_left(self.parse_unary, [TokenType.STAR, TokenType.SLASH])

    def parse_unary(self) -> Expression:
        """Analyse une opération unaire."""
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.parse_unary()
            return Unary(operator, right)

        return self.parse_primary()

    def parse_primary(self) -> Expression:
        """Analyse une expression primaire (littéral, variable, parenthèses)."""
        if self.match(TokenType.NUMBER):
            return Literal(float(self.previous().lexeme))

        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())

        if self.match(TokenType.LPAREN):
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression.")
            return expr

        if self.match(TokenType.MATCH):
            return self.parse_match_expression()

        raise SyntaxError(
            f"Unexpected token. token: {self.peek().lexeme}, line: {self.peek().line}"
        )

    def parse_match_expression(self) -> Expression:
        """Analyse une expression match."""
        # 'match' keyword is already consumed
        subject = self.parse_expression()
        self.consume(TokenType.LBRACE, "Expect '{' after match subject.")

        cases = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            self.consume(TokenType.CASE, "Expect 'case' before match pattern.")
            pattern = self.parse_expression()
            self.consume(TokenType.ARROW, "Expect '=>' after match pattern.")
            body = self.parse_expression()
            cases.append(MatchCase(pattern, body))

            if self.match(TokenType.COMMA):
                pass
        
        self.consume(TokenType.RBRACE, "Expect '}' after match cases.")
        return MatchExpression(subject, cases)

    ##########################################################################
    # Utils
    ##########################################################################

    def binary_left(
        self,
        operand_fn: Callable[[], Expression],
        operators: list[TokenType],
    ) -> Expression:
        """Helper pour analyser les opérations binaires associatives à gauche."""
        left = operand_fn()

        while self.match(*operators):
            operator = self.previous()
            right = operand_fn()
            left = Binary(left, operator, right)

        return left

    def is_at_end(self) -> bool:
        """Vérifie si on a atteint la fin des tokens."""
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        """Retourne le token courant sans avancer."""
        return self.tokens[self.current]

    def match(self, *types: TokenType) -> bool:
        """Vérifie si le token courant correspond à un type donné et avance."""
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def previous(self) -> Token:
        """Retourne le token précédent."""
        return self.tokens[self.current - 1]

    def check(self, token_type: TokenType) -> bool:
        """Vérifie le type du token courant sans avancer."""

        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def advance(self) -> Token:
        """Avance au token suivant."""
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def consume(self, token_type: TokenType, error_message: str) -> Token:
        """Consomme le token attendu ou lève une erreur."""
        if self.check(token_type):
            return self.advance()
        raise SyntaxError(f"{error_message} at line {self.peek().line}")

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
