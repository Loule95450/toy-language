from dataclasses import dataclass
from typing import Any

from toy.tokens import Token


@dataclass
class ASTNode:
    """Classe de base pour tous les nœuds de l'AST."""
    pass


##############################################################################
# Expressions
##############################################################################


@dataclass
class Expression(ASTNode):
    """Classe de base pour toutes les expressions."""
    pass


@dataclass
class Literal(Expression):
    """Représente une valeur littérale (nombre, chaîne, etc.)."""
    value: Any | None


@dataclass
class Binary(Expression):
    """Représente une opération binaire (ex: a + b)."""
    left: Expression
    operator: Token
    right: Expression


@dataclass
class Unary(Expression):
    """Représente une opération unaire (ex: -a, !a)."""
    operator: Token
    right: Expression


@dataclass
class Variable(Expression):
    """Représente l'accès à une variable."""
    name: Token


@dataclass
class VariableAssignment(Expression):
    """Représente l'assignation d'une valeur à une variable."""


    name: Token
    value: Expression


##############################################################################
# Statements
##############################################################################


@dataclass
class Statement(ASTNode):
    """Classe de base pour toutes les instructions."""
    pass


@dataclass
class ExpressionStatement(Statement):
    """Instruction qui évalue une expression."""
    expression: Expression


@dataclass
class VarStatement(Statement):
    """Instruction de déclaration de variable."""
    name: Token
    initializer: Expression | None

@dataclass
class PrintStatement(Statement):
    """Instruction d'affichage."""
    expression: Expression
