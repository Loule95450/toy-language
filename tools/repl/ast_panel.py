"""Custom widgets for the Inspect tool."""

from rich.tree import Tree
from textual.widgets import Static

from toy.ast_nodes import ASTNode
from toy import ast_nodes as ast_module
from colors import NODE_TYPE_COLOR, NODE_LABEL_COLOR


class ASTPanel(Static):
    """Widget to display AST tree structure."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ast = None

    def update_ast(self, ast: list[ASTNode]):
        """Update the displayed AST.

        Args:
            ast: Root AST node from the parser
        """
        self.ast = ast
        if not self.ast:
            self.update("No AST to display")
            return

        tree = Tree("Program")

        for node in self.ast:
            self._add_node(tree, node)

        self.update(tree)

    def _format_label(self, node_type: str, detail: str = "") -> str:
        label = f"[{NODE_TYPE_COLOR}]{node_type}[/{NODE_TYPE_COLOR}]"
        if detail:
            label += f" {detail}"
        return label

    def _add_node(self, parent_tree: Tree, node: ASTNode):
        node_name = node.__class__.__name__
        branch = parent_tree.add(self._format_label(node_name))

        # Helper to check if node matches a type (returns False if type doesn't exist)
        def is_type(class_name: str) -> bool:
            cls = getattr(ast_module, class_name, None)
            return cls is not None and isinstance(node, cls)

        match node:
            # Expressions
            case _ if is_type("Binary"):
                branch.label = self._format_label(
                    node_name, f"({node.operator.lexeme})"
                )
                self._add_node(branch, node.left)
                self._add_node(branch, node.right)

            case _ if is_type("Unary"):
                branch.label = self._format_label(
                    node_name, f"({node.operator.lexeme})"
                )
                self._add_node(branch, node.right)

            case _ if is_type("Literal"):
                branch.label = self._format_label(node_name, repr(node.value))

            case _ if is_type("Variable"):
                branch.label = self._format_label(node_name, f"'{node.name.lexeme}'")

            case _ if is_type("VariableAssignment"):
                branch.label = self._format_label(node_name, f"'{node.name.lexeme}'")
                self._add_node(branch, node.value)

            case _ if is_type("FunctionCall"):
                self._add_node(branch, node.callee)
                for arg in node.arguments:
                    self._add_node(branch, arg)

            # Statements
            case _ if is_type("ExpressionStatement"):
                self._add_node(branch, node.expression)

            case _ if is_type("VarStatement"):
                branch.label = self._format_label(node_name, f"'{node.name.lexeme}'")
                if node.initializer:
                    self._add_node(branch, node.initializer)

            case _ if is_type("PrintStatement"):
                self._add_node(branch, node.expression)

            case _ if is_type("IfStatement"):
                cond_tree = branch.add(
                    f"[{NODE_LABEL_COLOR}]condition[/{NODE_LABEL_COLOR}]"
                )
                self._add_node(cond_tree, node.condition)
                then_tree = branch.add(f"[{NODE_LABEL_COLOR}]then[/{NODE_LABEL_COLOR}]")
                self._add_node(then_tree, node.then_branch)
                if node.else_branch:
                    else_tree = branch.add(
                        f"[{NODE_LABEL_COLOR}]else[/{NODE_LABEL_COLOR}]"
                    )
                    self._add_node(else_tree, node.else_branch)

            case _ if is_type("WhileStatement"):
                cond_tree = branch.add(
                    f"[{NODE_LABEL_COLOR}]condition[/{NODE_LABEL_COLOR}]"
                )
                self._add_node(cond_tree, node.condition)
                body_tree = branch.add(f"[{NODE_LABEL_COLOR}]body[/{NODE_LABEL_COLOR}]")
                self._add_node(body_tree, node.body)

            case _ if is_type("BlockStatement"):
                for stmt in node.statements:
                    self._add_node(branch, stmt)

            case _ if is_type("FunctionDeclarationStatement"):
                params_str = ", ".join(p.lexeme for p in node.parameters)
                branch.label = self._format_label(
                    node_name, f"'{node.name.lexeme}({params_str})'"
                )
                for stmt in node.body:
                    self._add_node(branch, stmt)

            case _ if is_type("ReturnStatement"):
                if node.value:
                    self._add_node(branch, node.value)

            case _:
                # Unknown/unimplemented node - keep default label
                pass
