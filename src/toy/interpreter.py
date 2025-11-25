from typing import Any

from toy.ast_nodes import ASTNode, Expression, Literal, Binary
from toy.tokens import TokenType


class Interpreter:
    def interpret(self, statements: list[ASTNode]):
        for statement in statements:
            self.evaluate(statement)

    def evaluate(self, expression: Expression) -> Any:
        match expression:
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

            case _:
                raise NotImplementedError(f"Unsupported expression type: {expression}")
