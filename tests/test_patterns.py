import json
import pytest

from payment_factory import PaymentFactory
from employee_builder import EmployeeBuilder, DeveloperBuilder
from config_manager import ConfigManager
from report_adapter import LegacyReportAdapter, LegacyReportGenerator
from order_decorators import BaseOrder, ExpressShippingDecorator, InsuranceDecorator, GiftWrapDecorator, \
    DiscountDecorator, PremiumMemberDecorator
from report_strategy import ReportGenerator, CSVFormatStrategy, HTMLFormatStrategy
from etl_pipeline import CSVPipeline, XMLPipeline


def test_factory():
    result = PaymentFactory().get_processor("credit_card").process(100, {"card_number": "1" * 16, "cvv": "123"})
    assert result["success"] and result["fee"] == 2.9
    assert not PaymentFactory().get_processor("paypal").process(100, {"email": "nope"})["success"]
    with pytest.raises(ValueError):
        PaymentFactory().get_processor("bitcoin")


def test_builder():
    e = EmployeeBuilder().with_name("John", "Doe").with_email("j@d.com").with_job("IT", "Dev", 1000).build()
    assert e.first_name == "John" and not e.has_laptop
    assert DeveloperBuilder("A", "B", "a@b.com").build().has_admin_rights
    with pytest.raises(ValueError):
        EmployeeBuilder().with_name("John", "Doe").with_email("bad").build()


def test_singleton():
    ConfigManager.reset()
    a = ConfigManager.get_instance()
    b = ConfigManager.get_instance()
    assert a is b
    assert a.get("database.port") == 5432
    assert a.get("nothing.here") is None


def test_adapter():
    out = LegacyReportAdapter(LegacyReportGenerator()).generate({"orders": 12, "avg": 1.5})
    assert json.loads(out) == {"orders": 12, "avg": 1.5}


def test_decorators():
    order = PremiumMemberDecorator(DiscountDecorator(GiftWrapDecorator(InsuranceDecorator(
        ExpressShippingDecorator(BaseOrder(100)))), percent=15))
    assert order.get_cost() == pytest.approx(95.625)


def test_strategy():
    gen = ReportGenerator([{"name": "a", "value": 1}], CSVFormatStrategy())
    assert gen.generate_report() == "name,value\na,1\n"
    gen.set_strategy(HTMLFormatStrategy())
    assert "<td>a</td>" in gen.generate_report()


def test_pipelines():
    for p in (CSVPipeline("x"), XMLPipeline("y")):
        p.delay = 0
        assert p.run().endswith("Pipeline finished")
