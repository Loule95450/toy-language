from toy.tokens import Token
from dataclasses import dataclass
from typing import Any

@dataclass
class ASTNode:
    pass

@dataclass
class Expression(ASTNode):
    pass

@dataclass
class Literal(Expression):
    """Un literal est une valeur pouvant représenter n'importe quel type de données"""
    value: Any | None

@dataclass
class Binary(Expression):
    """Une expression binaire est une expression qui prend deux arguments"""
    left: Expression
    operator: Token
    right: Expression

@dataclass
class Unary(Expression):
    operator: Token
    right: Expression