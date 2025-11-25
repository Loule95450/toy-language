"""Interactive REPL tool for the Toy language."""

import sys
from io import StringIO
from pathlib import Path

# Keep at the top to resolve toy imports after
project_root = Path(__file__).parent.parent.parent
toy_src = project_root / "src"
sys.path.insert(0, str(toy_src))

from toy.interpreter import Interpreter
from toy.lexer import Lexer
from toy.parser import Parser

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Input, RichLog, TabbedContent, TabPane

from token_panel import TokenPanel
from ast_panel import ASTPanel
from env_panel import EnvPanel


class REPLApp(App):

    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
        ("ctrl+d", "quit", "Quit"),
    ]

    # Animation frames for the rubber duck
    DUCK_FRAMES = [
        [
            "       __",
            "   ___( o)>",
            "   \\ <_. )",
            "    `---'",
        ],
        [
            "       __",
            "   ___( -)>",
            "   \\ <_. )",
            "    `---'",
        ],
    ]

    def __init__(self):
        super().__init__()
        self.title = "Toy Language REPL"

        self.interpreter = Interpreter()
        self.source = ""
        self.input_buffer = ""
        self.executed_count = 0

        # Animation state
        self.first_input = True
        self.duck_frame = 0
        self.duck_timer = None

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal():
            # Left pane: REPL editor
            with Vertical(id="repl-container"):
                yield RichLog(id="repl-output", highlight=True, markup=True)
                yield Input(
                    placeholder="Enter Toy code...",
                    id="repl-input",
                )

            # Right pane: Tabbed info panels
            with Vertical(id="info-container"):
                with TabbedContent():
                    with TabPane("Tokens"):
                        yield TokenPanel()
                    with TabPane("AST"):
                        yield ASTPanel()
                    with TabPane("Environment"):
                        yield EnvPanel()

        yield Footer()

    def on_mount(self) -> None:
        # Display and animate duck
        self._display_duck()
        self.duck_timer = self.set_interval(0.8, self.animate_duck)

        # Initialize panels
        token_panel = self.query_one(TokenPanel)
        ast_panel = self.query_one(ASTPanel)
        env_panel = self.query_one(EnvPanel)

        token_panel.update_tokens([])
        ast_panel.update_ast([])
        env_panel.update_environment(None)

        # Focus the input
        self.query_one("#repl-input", Input).focus()

    def _display_duck(self) -> None:
        output = self.query_one("#repl-output", RichLog)
        frame = self.DUCK_FRAMES[self.duck_frame]

        for line in frame:
            output.write(f"[bold yellow]{line}[/bold yellow]")
        output.write("[bold cyan]  Official Toy REPL[/bold cyan]")
        output.write("")

    def animate_duck(self) -> None:
        # Alternate between frames
        self.duck_frame = 1 - self.duck_frame

        # Clear and redisplay
        output = self.query_one("#repl-output", RichLog)
        output.clear()
        self._display_duck()

    def is_complete(self, source: str) -> bool:
        """Check if the source has balanced braces."""
        return source.count("{") - source.count("}") == 0

    def on_input_submitted(self, event: Input.Submitted) -> None:
        user_input = event.value
        if not user_input.strip():
            return

        event.input.value = ""

        output = self.query_one("#repl-output", RichLog)
        token_panel = self.query_one(TokenPanel)
        ast_panel = self.query_one(ASTPanel)
        env_panel = self.query_one(EnvPanel)

        # Clear welcome message and stop animation on first input
        if self.first_input:
            if self.duck_timer:
                self.duck_timer.stop()
            output.clear()
            self.first_input = False

        # Accumulate input in buffer
        self.input_buffer += user_input + "\n"

        # Check if input is complete (balanced braces)
        if not self.is_complete(self.input_buffer):
            # Show continuation prompt
            output.write(f"[bold yellow]...[/bold yellow] {user_input}")
            return

        # Input is complete, we can name tokenize, parse, and interpret
        output.write(f"[bold green]>>>[/bold green] {user_input}")
        combined_source = self.source + self.input_buffer
        try:
            # Interpret the input
            lexer = Lexer(combined_source)
            tokens = lexer.tokenize()

            parser = Parser(tokens)
            ast = parser.parse()

            # Update the panels
            token_panel.update_tokens(tokens)
            ast_panel.update_ast(ast)

            # Capture interpreter output
            old_stdout = sys.stdout
            sys.stdout = StringIO()

            try:
                # Only execute statements we haven't executed yet
                # It's not so much about perfs, rather avoid print already executed statements
                start_idx = self.executed_count
                self.interpreter.interpret(ast, start_index=start_idx)
                self.source = combined_source

                output_text = sys.stdout.getvalue()
                if output_text:
                    output.write(output_text.rstrip())
                self.executed_count = len(ast)

                env_panel.update_environment(self.interpreter.environment)
            finally:
                sys.stdout = old_stdout

            # Clear buffer after successful execution
            self.input_buffer = ""

        except Exception as e:
            output.write(f"[bold red]Error[/bold red]: {e}")
            # Clear buffer on error
            self.input_buffer = ""
            return


if __name__ == "__main__":
    app = REPLApp()
    app.run()
