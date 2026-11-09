from abc import ABC, abstractmethod


class OrderComponent(ABC):
    @abstractmethod
    def get_cost(self) -> float:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_base_price(self) -> float:
        pass


class BaseOrder(OrderComponent):
    def __init__(self, base_price: float):
        self.base_price = base_price

    def get_cost(self):
        return self.base_price

    def get_description(self):
        return f"Base price: {self.base_price:.2f}€"

    def get_base_price(self):
        return self.base_price


class OrderDecorator(OrderComponent):
    def __init__(self, order: OrderComponent):
        self._order = order

    def get_cost(self):
        return self._order.get_cost()

    def get_description(self):
        return self._order.get_description()

    def get_base_price(self):
        return self._order.get_base_price()


class ExpressShippingDecorator(OrderDecorator):
    PRICE = 15.00

    def get_cost(self):
        return self._order.get_cost() + self.PRICE

    def get_description(self):
        return self._order.get_description() + f"\nExpress shipping: +{self.PRICE:.2f}€"


class InsuranceDecorator(OrderDecorator):
    RATE = 0.05

    def _insurance(self):
        # insurance is computed on the base price, like in the old code
        return self.get_base_price() * self.RATE

    def get_cost(self):
        return self._order.get_cost() + self._insurance()

    def get_description(self):
        return self._order.get_description() + f"\nInsurance (5%): +{self._insurance():.2f}€"


class GiftWrapDecorator(OrderDecorator):
    PRICE = 5.00

    def get_cost(self):
        return self._order.get_cost() + self.PRICE

    def get_description(self):
        return self._order.get_description() + f"\nGift wrap: +{self.PRICE:.2f}€"


class DiscountDecorator(OrderDecorator):
    def __init__(self, order: OrderComponent, percent: float):
        super().__init__(order)
        if not 0 <= percent <= 100:
            raise ValueError("percent must be between 0 and 100")
        self.percent = percent

    def _discount(self):
        return self._order.get_cost() * self.percent / 100

    def get_cost(self):
        return self._order.get_cost() - self._discount()

    def get_description(self):
        return self._order.get_description() + f"\nDiscount ({self.percent}%): -{self._discount():.2f}€"


class PremiumMemberDecorator(DiscountDecorator):
    def __init__(self, order: OrderComponent):
        super().__init__(order, percent=10)

    def get_description(self):
        return self._order.get_description() + f"\nPremium member (10%): -{self._discount():.2f}€"


if __name__ == "__main__":
    simple = BaseOrder(100.00)
    print(simple.get_description())
    print(f"Total: {simple.get_cost():.2f}€")

    print("\n---\n")

    order = BaseOrder(100.00)
    order = ExpressShippingDecorator(order)
    order = InsuranceDecorator(order)
    order = GiftWrapDecorator(order)
    order = DiscountDecorator(order, percent=15)
    order = PremiumMemberDecorator(order)
    print(order.get_description())
    print(f"Total: {order.get_cost():.2f}€")
