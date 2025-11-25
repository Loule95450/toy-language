from typing import Any

from toy.ast_nodes import ASTNode, Expression, Literal, Binary, Unary
from toy.tokens import TokenType


class Interpreter:
    def interpret(self, statements: list[ASTNode]):
        for statement in statements:
            self.evaluate(statement)

    def evaluate(self, expression: Expression) -> Any:
        match expression:
            case Literal(value):
                return value

            case Unary(operator, right):
                right_value = self.evaluate(right)
                match operator.type:
                    case TokenType.MINUS:
                        return -right_value
                    case TokenType.BANG:
                        return not right_value

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
                    case TokenType.LESS:
                        return left_value < right_value
                    case TokenType.LESS_EQUAL:
                        return left_value <= right_value
                    case TokenType.GREATER:
                        return left_value > right_value
                    case TokenType.GREATER_EQUAL:
                        return left_value >= right_value

            case _:
                raise NotImplementedError(f"Unsupported expression type: {expression}")
