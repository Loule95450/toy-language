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
    """Base class for all expression nodes. Expressions evaluate to a value."""

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
    """Assignment is an expression: it evaluates to the assigned value.
    For example:
        var a = 1;
        var b = a + 2;  // b gets 3
    Here, `a + 2` produces the value 3; changing `a` is just a side effect.
    """

    name: Token
    value: Expression


##############################################################################
# Statements
##############################################################################


@dataclass
class Statement(ASTNode):
    """The main goal of a statement is to **modify** the state of the program. Some examples:
    * Assigning a value to a variable
    * Declaring a function
    * Control flow (if, for, while). This is specific to Toy (not a general rule for PLs)
    *"""

    pass


@dataclass
class ExpressionStatement(Statement):
    """This is just a wrapper around an expression. In our language, everything is a statement."""

    expression: Expression


@dataclass
class VarStatement(Statement):
    name: Token
    initializer: Expression | None

@dataclass
class PrintStatement(Statement):
    expression: Expression
