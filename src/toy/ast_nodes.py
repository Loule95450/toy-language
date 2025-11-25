from dataclasses import dataclass
from typing import Any

from toy.tokens import Token


@dataclass
class ASTNode:
    pass


##############################################################################
# Expressions
##############################################################################


@dataclass
class Expression(ASTNode):
    pass


@dataclass
class Literal(Expression):
    value: Any | None


@dataclass
class Binary(Expression):
    left: Expression
    operator: Token
    right: Expression


@dataclass
class Unary(Expression):
    operator: Token
    right: Expression


@dataclass
class Variable(Expression):
    name: Token


@dataclass
class VariableAssignment(Expression):


    name: Token
    value: Expression


##############################################################################
# Statements
##############################################################################


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

@dataclass
class PrintStatement(Statement):
    expression: Expression
