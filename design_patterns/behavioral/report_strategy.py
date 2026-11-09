import json
from abc import ABC, abstractmethod


class ReportFormatStrategy(ABC):
    extension = ""

    @abstractmethod
    def format(self, data: list) -> str:
        pass


class PDFFormatStrategy(ReportFormatStrategy):
    extension = ".pdf"

    def format(self, data):
        report = "PDF REPORT\n" + "=" * 50 + "\n"
        for item in data:
            report += f"| {item['name']:20} | {item['value']:10} |\n"
        report += "=" * 50 + "\nEnd of PDF Report"
        return report


class ExcelFormatStrategy(ReportFormatStrategy):
    extension = ".xlsx"

    def format(self, data):
        report = "EXCEL REPORT\n" + "-" * 50 + "\nName\tValue\n"
        for item in data:
            report += f"{item['name']}\t{item['value']}\n"
        report += "-" * 50 + "\n"
        return report


class CSVFormatStrategy(ReportFormatStrategy):
    extension = ".csv"

    def format(self, data):
        report = "name,value\n"
        for item in data:
            report += f"{item['name']},{item['value']}\n"
        return report


class JSONFormatStrategy(ReportFormatStrategy):
    extension = ".json"

    def format(self, data):
        return json.dumps(data, indent=2)


class HTMLFormatStrategy(ReportFormatStrategy):
    extension = ".html"

    def format(self, data):
        rows = "\n".join(f"  <tr><td>{i['name']}</td><td>{i['value']}</td></tr>" for i in data)
        return f"<table>\n  <tr><th>Name</th><th>Value</th></tr>\n{rows}\n</table>"


class ReportGenerator:
    def __init__(self, data, strategy: ReportFormatStrategy = None):
        self.data = data
        self.strategy = strategy

    def set_strategy(self, strategy: ReportFormatStrategy):
        self.strategy = strategy

    def generate_report(self):
        if self.strategy is None:
            raise ValueError("no format strategy set")
        return self.strategy.format(self.data)

    def save_report(self, filename):
        path = filename + self.strategy.extension
        with open(path, "w") as f:
            f.write(self.generate_report())
        return path


if __name__ == "__main__":
    data = [
        {"name": "Sales Q1", "value": 15000},
        {"name": "Sales Q2", "value": 18000},
        {"name": "Sales Q3", "value": 22000},
        {"name": "Sales Q4", "value": 25000},
    ]
    generator = ReportGenerator(data)

    for title, strategy in [("PDF", PDFFormatStrategy()), ("CSV", CSVFormatStrategy()),
                            ("JSON", JSONFormatStrategy()), ("HTML (new)", HTMLFormatStrategy())]:
        print(f"=== {title} FORMAT ===")
        generator.set_strategy(strategy)
        print(generator.generate_report())
        print("\n" + "=" * 60 + "\n")

    generator.set_strategy(CSVFormatStrategy())
    print("saved to", generator.save_report("sales_report"))
