"""Token display utilities and widgets."""

from textual.widgets import Static
from rich.text import Text

from toy.tokens import Token, TokenType
from colors import get_token_color


class TokenPanel(Static):
    """Widget to display tokenization results."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tokens = []

    def update_tokens(self, tokens: list[Token]):
        self.tokens = tokens
        if not self.tokens:
            self.update("No tokens to display")
            return

        # Render tokens as bordered chips/tags
        result = Text()
        line = 1
        # Format line number with zero padding
        result.append(f"{line:02} | ")
        for token in self.tokens:
            if token.type == TokenType.EOF:
                continue

            if token.line != line:
                line = token.line
                result.append(f"\n{line:02} | ")

            color = get_token_color(token.type)
            # Create chip with brackets and colored background
            title = token.type
            if token.type != token.lexeme:
                title = f"{token.type} {token.lexeme}"

            chip = Text(f" {title} ", style=f"bold {color}")
            result.append("[", style=f"dim {color}")
            result.append(chip)
            result.append("]", style=f"dim {color}")

        self.update(result)
