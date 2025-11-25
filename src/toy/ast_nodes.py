from toy.tokens import Token
from dataclasses import dataclass
from typing import Any

@dataclass
class ASTNode:
    pass

####################
# Expressions
####################

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
    """Une expression unaire est une expression qui prend un argument"""
    operator: Token
    right: Expression

####################
# Statements
####################

@dataclass
class Statement(ASTNode):
    pass

@dataclass
class ExpressionStatement(Statement):
    expression: Expression

@dataclass
class VarStatement(Statement):
    name: Token
    initializer: Expression | None