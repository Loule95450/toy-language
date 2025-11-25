"""The interpreter walks the AST and executes the statements"""

from typing import Any

from toy.ast_nodes import (
    Statement,
    Expression,
    Literal,
    Binary,
    Unary,
    VarStatement,
    Variable,
    ExpressionStatement,
    VariableAssignment,
    PrintStatement,
)
from toy.environment import Environment
from toy.tokens import TokenType


class Interpreter:
    def __init__(self) -> None:
        self.environment = Environment()

    def interpret(self, statements: list[Statement], start_index: int = 0) -> None:
        """Execute multiple statements for their side effects (used by REPL/file execution).

        start_index: index of the first statement to execute (useful for a REPL, debugger, etc)
        """
        for statement in statements[start_index:]:
            self.execute(statement)

    def execute(self, stmt: Statement) -> None:
        """Execute a statement for its side effects. Statements don't return values."""
        match stmt:
            case ExpressionStatement(expression):
                self.evaluate(expression)

            case VarStatement(name, initializer):
                value = None
                if initializer is not None:
                    value = self.evaluate(initializer)
                self.environment.define(name.lexeme, value)

            case PrintStatement(expression):
                value = self.evaluate(expression)
                print(value)

            case _:
                raise ValueError(f"Unknown statement: {stmt}")

    def evaluate(self, expr: Expression) -> Any:
        """Evaluate an expression and return its value."""
        match expr:
            # Expressions
            case Literal(value):
                return value
            case Binary(left, operator, right):
                left_value = self.evaluate(left)
                right_value = self.evaluate(right)

                match operator.type:
                    # One character operators
                    case TokenType.PLUS:
                        return left_value + right_value
                    case TokenType.MINUS:
                        return left_value - right_value
                    case TokenType.STAR:
                        return left_value * right_value
                    case TokenType.SLASH:
                        return left_value / right_value

                    # One or 2 character operators
                    case TokenType.EQUAL_EQUAL:
                        return left_value == right_value
                    case TokenType.BANG_EQUAL:
                        return left_value != right_value
                    case TokenType.GREATER:
                        return left_value > right_value
                    case TokenType.GREATER_EQUAL:
                        return left_value >= right_value
                    case TokenType.LESS:
                        return left_value < right_value
                    case TokenType.LESS_EQUAL:
                        return left_value <= right_value

                    case _:
                        raise ValueError(f"Unknown operator: {operator}")

            case Unary(operator, right):
                right_value = self.evaluate(right)

                match operator.type:
                    case TokenType.MINUS:
                        return -right_value
                    case TokenType.BANG:
                        return not right_value
                    case _:
                        raise ValueError(f"Unknown operator: {operator}")

            case Variable(value):
                return self.environment.get(value.lexeme)

            case VariableAssignment(name, value):
                value = self.evaluate(value)
                self.environment.assign(name.lexeme, value)
                return value

            case _:
                raise ValueError(f"Unknown expression: {expr}")
