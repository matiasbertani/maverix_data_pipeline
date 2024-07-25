import inquirer
from rich.console import Console

from src.use_cases import (
    FullTransformation,
    UseCase,
)


class TerminalUserInterface:

    options = {
        "Transformación completa": "full_transformation",
        "Salir": "exit",
    }

    uses_cases = {
        "full_transformation": FullTransformation,
    }

    def __init__(self):
        self.menu = [
            inquirer.List(
                'choice',
                message="¿Qué deseas hacer?",
                choices=self.options.keys(),
            ),
        ]
        self.console = Console()

    def start(self):

        while True:
            answers = inquirer.prompt(self.menu)

            choice = self.options.get(answers['choice'])

            if choice == "exit":
                break

            print(f"Seleccionaste {choice}")
            use_case: UseCase = self.uses_cases.get(choice)
            use_case.execute()

        self.console.print("Saliendo...", style="red")
