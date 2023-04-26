import pytest

from model_objects import Product, SpecialOfferType, ProductUnit
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


def test_ten_percent_discount():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 1.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)

    receipt = teller.checks_out_articles_from(cart)

    assert 4.975 == pytest.approx(receipt.total_price(), 0.01)
    assert [] == receipt.discounts
    assert 1 == len(receipt.items)
    receipt_item = receipt.items[0]
    assert apples == receipt_item.product
    assert 1.99 == receipt_item.price
    assert 2.5 * 1.99 == pytest.approx(receipt_item.total_price, 0.01)
    assert 2.5 == receipt_item.quantity

def test_two_for_one_discount():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, toothbrush, 0.99)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 2)

    receipt = teller.checks_out_articles_from(cart)

    assert 0.99 == pytest.approx(receipt.total_price(), 0.01)
    discount = receipt.discounts[0]
    assert -0.99 == discount.discount_amount
    receipt_item = receipt.items[0]
    assert toothbrush == receipt_item.product
    assert 2 == receipt_item.quantity

def test_five_for_amount_discount():
    catalog = FakeCatalog()
    toothpaste = Product("toothpaste", ProductUnit.EACH)
    catalog.add_product(toothpaste, 1.79)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothpaste, 7.49)

    cart = ShoppingCart()
    cart.add_item_quantity(toothpaste, 5)

    receipt = teller.checks_out_articles_from(cart)

    assert 7.49 == pytest.approx(receipt.total_price(), 0.01)
    discount = receipt.discounts[0]
    assert -1.46 == discount.discount_amount
    receipt_item = receipt.items[0]
    assert toothpaste == receipt_item.product
    assert 5 == receipt_item.quantity

def test_three_for_two_discount():
    catalog = FakeCatalog()
    cherry_tomatoes = Product("cherry tomatoes", ProductUnit.EACH)
    catalog.add_product(cherry_tomatoes, 1)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, cherry_tomatoes, 1)

    cart = ShoppingCart()
    cart.add_item_quantity(cherry_tomatoes, 6)

    receipt = teller.checks_out_articles_from(cart)

    assert 4 == pytest.approx(receipt.total_price(), 0.01)
    assert 1 == len(receipt.discounts)
    discount = receipt.discounts[0]
    assert -2 == discount.discount_amount
    receipt_item = receipt.items[0]
    assert cherry_tomatoes == receipt_item.product
    assert 6 == receipt_item.quantity
