from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    @abstractmethod
    def validate(self, details: dict) -> bool:
        pass

    @abstractmethod
    def fee(self, amount: float) -> float:
        pass

    def process(self, amount: float, details: dict) -> dict:
        # same flow for every payment method, only the rules change
        if not self.validate(details):
            return {"success": False, "error": f"Invalid details for {self.name}"}
        fee = round(self.fee(amount), 2)
        return {"success": True, "method": self.name, "amount": round(amount + fee, 2), "fee": fee}


class CreditCardProcessor(PaymentProcessor):
    name = "credit_card"

    def validate(self, details):
        card = details.get("card_number")
        cvv = details.get("cvv")
        return bool(card) and len(card) == 16 and bool(cvv) and len(cvv) == 3

    def fee(self, amount):
        return amount * 0.029


class BankTransferProcessor(PaymentProcessor):
    name = "bank_transfer"

    def validate(self, details):
        iban = details.get("iban")
        return bool(iban) and len(iban) >= 15

    def fee(self, amount):
        return 1.50


class PayPalProcessor(PaymentProcessor):
    name = "paypal"

    def validate(self, details):
        email = details.get("email")
        return bool(email) and "@" in email

    def fee(self, amount):
        return amount * 0.034 + 0.30


class PaymentFactory:
    _processors = {
        "credit_card": CreditCardProcessor,
        "bank_transfer": BankTransferProcessor,
        "paypal": PayPalProcessor,
    }

    @classmethod
    def register(cls, name, processor_class):
        # new payment methods are added here, process() never changes
        cls._processors[name] = processor_class

    def get_processor(self, payment_type: str) -> PaymentProcessor:
        if payment_type not in self._processors:
            raise ValueError(f"Unknown payment type: {payment_type}")
        return self._processors[payment_type]()


# example: adding Apple Pay without touching the other classes
class ApplePayProcessor(PaymentProcessor):
    name = "apple_pay"

    def validate(self, details):
        return bool(details.get("device_token"))

    def fee(self, amount):
        return amount * 0.015


PaymentFactory.register("apple_pay", ApplePayProcessor)


if __name__ == "__main__":
    factory = PaymentFactory()

    processor = factory.get_processor("credit_card")
    print(processor.process(100.0, {"card_number": "1234567890123456", "cvv": "123"}))

    processor = factory.get_processor("bank_transfer")
    print(processor.process(100.0, {"iban": "FR7630006000011234567890189", "bic": "BNPAFRPP"}))

    processor = factory.get_processor("paypal")
    print(processor.process(100.0, {"email": "leon"}))

    print(factory.get_processor("apple_pay").process(100.0, {"device_token": "abc"}))
