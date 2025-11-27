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

@dataclass
class FunctionCall(Expression):
    callee: Expression
    arguments: list[Expression]


@dataclass
class MatchCase(ASTNode):
    """Représente un cas dans une expression match."""
    pattern: Expression
    body: Expression


@dataclass
class MatchExpression(Expression):
    """Représente une expression match."""
    subject: Expression
    cases: list[MatchCase]

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


@dataclass
class IfStatement(Statement):
    """Instruction conditionnelle."""
    condition: Expression
    then_branch: Statement
    else_branch: Statement | None

@dataclass
class WhileStatement(Statement):
    """Instruction conditionnelle."""
    condition: Expression
    body: Statement

@dataclass
class ForStatement(Statement):
    """Instruction conditionnelle."""
    initializer: Statement
    condition: Expression
    body: Statement

@dataclass
class BlockStatement(Statement):
    """Instruction qui contient plusieurs instructions."""
    statements: list[Statement]


@dataclass
class FunctionDeclarationStatement(Statement):
    """Instruction de déclaration de fonction."""
    name: Token
    parameters: list[Token]
    body: BlockStatement


@dataclass
class ReturnStatement(Statement):
    """Instruction de retour."""
    keyword: Token
    value: Expression | None