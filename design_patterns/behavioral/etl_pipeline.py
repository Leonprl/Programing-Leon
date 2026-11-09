import time
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


class DataPipeline(ABC):
    source_type = "source"
    required_fields = ()
    delay = 0.5

    def __init__(self, source):
        self.source = source
        self.data = None

    def run(self):
        self.connect()
        self.data = self.extract()
        print(f"Extracted {len(self.data)} records")
        print(f"Transforming {self.source_type} data...")
        self.data = self.transform(self.data)
        print("Transformation complete")
        self.validate()
        self.load()
        self.cleanup()
        return f"{self.source_type} Pipeline finished"

    @abstractmethod
    def extract(self) -> list:
        pass

    @abstractmethod
    def transform(self, data: list) -> list:
        pass

    def connect(self):
        print(f"Connecting to {self.source_type}: {self.source}")
        time.sleep(self.delay)
        print(f"{self.source_type} connection established")

    def validate(self):
        print("Validating data...")
        for record in self.data:
            for field in self.required_fields:
                if field not in record:
                    raise ValueError(f"Invalid record structure, missing '{field}'")
        print("Validation passed")

    def load(self):
        print("Loading data to destination...")
        time.sleep(self.delay)
        print(f"Loaded {len(self.data)} records successfully")

    def cleanup(self):
        print("Cleaning up resources...")
        self.data = None
        print("Cleanup complete")


class CSVPipeline(DataPipeline):
    source_type = "CSV"
    required_fields = ("id", "name")

    def extract(self):
        print("Extracting data from CSV...")
        return [{"id": 1, "name": "Alice", "age": 30}, {"id": 2, "name": "Bob", "age": 25}]

    def transform(self, data):
        for record in data:
            record["age"] = int(record["age"])
            record["name"] = record["name"].upper()
        return data


class APIPipeline(DataPipeline):
    source_type = "API"
    required_fields = ("user_id", "username")

    def extract(self):
        print("Extracting data from API...")
        return [{"user_id": 101, "username": "charlie", "score": 85},
                {"user_id": 102, "username": "diana", "score": 92}]

    def transform(self, data):
        for record in data:
            record["score"] = int(record["score"])
            record["username"] = record["username"].lower()
            record["grade"] = "A" if record["score"] >= 90 else "B"
        return data


class DatabasePipeline(DataPipeline):
    source_type = "Database"
    required_fields = ("product_id", "price")

    def extract(self):
        print("Extracting data from database...")
        return [{"product_id": 501, "product_name": "Laptop", "price": 1200},
                {"product_id": 502, "product_name": "Mouse", "price": 25}]

    def transform(self, data):
        for record in data:
            record["price"] = float(record["price"])
            record["product_name"] = record["product_name"].title()
            record["tax"] = record["price"] * 0.2
        return data


class XMLPipeline(DataPipeline):
    source_type = "XML"
    required_fields = ("order_id", "amount")

    SAMPLE = """<orders>
        <order><order_id>9001</order_id><customer>eve</customer><amount>59.90</amount></order>
        <order><order_id>9002</order_id><customer>frank</customer><amount>120</amount></order>
    </orders>"""

    def extract(self):
        print("Extracting data from XML...")
        root = ET.fromstring(self.SAMPLE)
        return [{child.tag: child.text for child in order} for order in root]

    def transform(self, data):
        for record in data:
            record["order_id"] = int(record["order_id"])
            record["amount"] = float(record["amount"])
            record["customer"] = record["customer"].capitalize()
        return data


if __name__ == "__main__":
    pipelines = [
        CSVPipeline("data/users.csv"),
        APIPipeline("https://api.example.com/users"),
        DatabasePipeline("postgresql://localhost/mydb"),
        XMLPipeline("data/orders.xml"),
    ]
    for p in pipelines:
        print(f"RUNNING {p.source_type.upper()} PIPELINE")
        print("=" * 70)
        result = p.run()
        print(f"\n{result}\n")
