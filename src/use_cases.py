from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn

from src import (
    FinalReport,
    ManagementReport,
    NxPortfolio,
    PreTransformedReport,
)


class UseCase:

    def execute(self):
        raise NotImplementedError


class FullTransformation(UseCase):

    @staticmethod
    def execute():
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.1f}%",
            TimeElapsedColumn(),
        ) as progress:

            task = progress.add_task("[cyan]Iniciando tranformacíon...", total=7)

            progress.update(task, description="[cyan]Leyendo Gestiones...", advance=1)
            management_report = ManagementReport()

            progress.update(task, description="[cyan]Leyendo cartera Nx...", advance=1)
            nx_portfolio = NxPortfolio()

            progress.update(task, description="[cyan]Transformando reporte...", advance=1)
            transformed_report = PreTransformedReport(management_report, nx_portfolio).transform()

            progress.update(task, description="[cyan]Generando reporte final...", advance=1)
            final_report = FinalReport(transformed_report)
            final_report.generate()

            progress.update(task, description="[cyan]Escribiendo verificación...", advance=1)
            final_report.write_verification()

            progress.update(task, description="[cyan]Validando reporte...", advance=1)
            final_report.validate()

            progress.update(task, description="[cyan]Guardando reporte...", advance=1)
            final_report.save()
