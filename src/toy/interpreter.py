

from pygments.token import String
from typing import Any

from toy.ast_nodes import *
from toy.environment import Environment
from toy.tokens import TokenType


class Interpreter:
    """Exécute le programme en parcourant l'AST."""
    def __init__(self) -> None:
        self.environment = Environment()

    def interpret(self, statements: list[Statement], start_index: int = 0) -> None:
        """Point d'entrée pour exécuter une liste d'instructions."""
        for statement in statements[start_index:]:
            self.execute(statement)

    def execute(self, stmt: Statement) -> None:
        """Exécute une instruction spécifique."""
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

            case IfStatement(condition, then_branch, else_branch):
                condition_value = self.evaluate(condition)
                if condition_value:
                    self.execute(then_branch)
                else:
                    self.execute(else_branch)

            case WhileStatement(condition, body):
                while self.evaluate(condition):
                    self.execute(body)

            case BlockStatement(statements):
                self.execute_block(statements)

            case _:
                raise ValueError(f"Unknown statement: {stmt}")

    def evaluate(self, expr: Expression) -> Any:
        """Évalue une expression et retourne sa valeur."""
        match expr:
            case Literal(value):
                return value
            case Binary(left, operator, right):
                left_value = self.evaluate(left)
                right_value = self.evaluate(right)

                match operator.type:

                    case TokenType.PLUS:
                        return left_value + right_value
                    case TokenType.MINUS:
                        return left_value - right_value
                    case TokenType.STAR:
                        return left_value * right_value
                    case TokenType.SLASH:
                        return left_value / right_value
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

    def execute_block(self, statements: list[Statement]) -> None:
        """Exécute une liste d'instructions dans un bloc."""
        previous = self.environment
        env = Environment(self.environment)
        
        try:
            self.environment = env
            for statement in statements:
                self.execute(statement)
        except RuntimeError as e:
            raise e
        finally:
            self.environment = previous