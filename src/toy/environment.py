from typing import Any


class Environment:
    """
    Environment class is just a wrapper around a dictionary.
    It stores all the symbols for a given scope (function, block, etc).
    """

    def __init__(self):
        self.values: dict[str, int] = {}

    def define(self, name: str, value: Any) -> None:
        # Here again, it's a language decision.
        # We don't allow re-defining variables!
        if name in self.values:
            raise RuntimeError(f"Variable '{name}' already defined.")

        self.values[name] = value

    def get(self, name: str) -> Any:
        if name in self.values:
            return self.values[name]

        raise RuntimeError(f"Variable '{name}' is not defined.")

    def assign(self, name: str, value: Any) -> None:
        if name in self.values:
            self.values[name] = value
            return

        raise RuntimeError(f"Undefined variable '{name}'.")
