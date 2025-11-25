from rich.tree import Tree
from textual.widgets import Static

from toy.environment import Environment


class EnvPanel(Static):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.environment = None

    def update_environment(self, environment: Environment | None):
        self.environment = environment
        if not self.environment:
            self.update("No environment")
            return

        # Create simple tree showing only global scope
        tree = Tree("[cyan]Variables[/cyan]")

        if not self.environment.values:
            tree.add("[dim]<empty>[/dim]")
        else:
            self._add_environment_variables(tree, self.environment)

        self.update(tree)

    def _add_environment_variables(self, parent_tree: Tree, env: Environment):
        for name, value in sorted(env.values.items()):
            is_function = self._is_function(value)
            value_repr = self._format_value(value)

            if is_function:
                parent_tree.add(
                    f"[blue]fn[/blue] [cyan]{name}[/cyan] = [yellow]{value_repr}[/yellow]"
                )
            else:
                # Variable: green name
                parent_tree.add(
                    f"[green]{name}[/green] = [yellow]{value_repr}[/yellow]"
                )

    def _is_function(self, value) -> bool:
        try:
            from toy import interpreter as interp_module

            toy_function_class = getattr(interp_module, "ToyFunction", None)
            return toy_function_class is not None and isinstance(
                value, toy_function_class
            )
        except ImportError:
            return False

    def _format_value(self, value) -> str:
        if self._is_function(value):
            params = ", ".join(p.lexeme for p in value.declaration.parameters)
            return f"fn({params})"
        elif isinstance(value, str):
            return repr(value)
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif value is None:
            return "null"
        else:
            return str(value)
