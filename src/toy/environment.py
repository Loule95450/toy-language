from typing import Any


class Environment:
    """Gère la portée des variables et stocke leurs valeurs."""


    def __init__(self):
        self.values: dict[str, int] = {}

    def define(self, name: str, value: Any) -> None:
        """Définit une nouvelle variable dans l'environnement courant."""
        if name in self.values:
            raise RuntimeError(f"Variable '{name}' already defined.")

        self.values[name] = value

    def get(self, name: str) -> Any:
        """Récupère la valeur d'une variable."""
        if name in self.values:
            return self.values[name]

        raise RuntimeError(f"Variable '{name}' is not defined.")

    def assign(self, name: str, value: Any) -> None:
        """Met à jour la valeur d'une variable existante."""
        if name in self.values:
            self.values[name] = value
            return

        raise RuntimeError(f"Undefined variable '{name}'.")
