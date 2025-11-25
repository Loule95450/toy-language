from typing import Any


class Environment:


    def __init__(self):
        self.values: dict[str, int] = {}

    def define(self, name: str, value: Any) -> None:

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
