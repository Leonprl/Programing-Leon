import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")


class ConfigManager:
    _instance = None

    def __init__(self, path=CONFIG_PATH):
        with open(path, "r") as f:
            self._config = json.load(f)

    @classmethod
    def get_instance(cls, path=CONFIG_PATH):
        if cls._instance is None:
            cls._instance = cls(path)
        return cls._instance

    def get(self, key, default=None):
        value = self._config
        for part in key.split("."):
            if not isinstance(value, dict) or part not in value:
                return default
            value = value[part]
        return value


def connect_database():
    config = ConfigManager.get_instance()
    print(f"Connecting to database at {config.get('database.host')}:{config.get('database.port')}")


def send_email(to: str, subject: str):
    config = ConfigManager.get_instance()
    print(f"Sending email from {config.get('email.sender')} via {config.get('email.smtp_host')}")


def process_payment(amount: float):
    config = ConfigManager.get_instance()
    print(f"Processing {amount}€ in {config.get('payment.environment')} mode")


def start_application():
    config = ConfigManager.get_instance()
    print(f"Starting {config.get('app.name')} (debug={config.get('app.debug')})")


if __name__ == "__main__":
    start_application()
    connect_database()
    send_email("user@test.com", "Welcome")
    process_payment(99.99)

    print(ConfigManager.get_instance() is ConfigManager.get_instance())
