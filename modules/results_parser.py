import json
from rich.console import Console
from rich.table import Table

class ResultParser:

    def __init__(self, results):
        self.results = results

    def export_html(self, output_file):
        with open("template.html", "r", encoding="utf-8") as file:
            template = file.read()
        
        elements_html = ''
        for index, result in enumerate(self.results):
            elements_html += f'<div class="resultados">' \
                             f'<div class="indice">Resultado {index}</div>' \
                             f'<h5>{result["title"]}</h5>' \
                             f'<p>{result["description"]}</p>' \
                             f'<a href="{result["link"]}">{result["link"]}</a>' \
                             f'</div>'
        report_html = template.replace("{{ results }}", elements_html)

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(report_html)
        print(f"File {output_file} exported successfully.")

    def export_json(self, output_file):
        with open(output_file, "w", encoding="utf-8") as file:
            data = json.dumps(self.results, ensure_ascii=False, indent=4)
            file.write(data)
        print(f"File {output_file} exported successfully.")

    def show_screen(self):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column('#', style="dim")
        table.add_column("Title")
        table.add_column("Description")
        table.add_column("Link")

        for index, result in enumerate(self.results):
            table.add_row(
                str(index),
                result["title"],
                result["description"][0:50] + "...",
                result["link"]
            )

        console.print(table)

