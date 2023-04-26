import math

from model_objects import Offer, Product, ProductQuantity, SpecialOfferType, Discount
from receipt import Receipt
from catalog import SupermarketCatalog

class ShoppingCart:

    def __init__(self) -> None:
        self._items: list[ProductQuantity] = []
        self._product_quantities: dict[Product, float] = {}

    @property
    def items(self) -> list[ProductQuantity]:
        return self._items

    def add_item(self, product: Product):
        self.add_item_quantity(product, 1.0)

    @property
    def product_quantities(self) -> dict[Product, float]:
        return self._product_quantities

    def add_item_quantity(self, product: Product, quantity: float):
        self._items.append(ProductQuantity(product, quantity))
        if product in self._product_quantities.keys():
            self._product_quantities[product] = self._product_quantities[product] + quantity
        else:
            self._product_quantities[product] = quantity

    def handle_offers(self, receipt: Receipt, offers: dict[Product, Offer], catalog: SupermarketCatalog):
        for p, quantity in self._product_quantities.items():
            if p in offers:
                offer = offers[p]
                unit_price = catalog.unit_price(p)
                quantity_as_int = int(quantity)
                discount = None
                x = 1

                if offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
                    x = 3
                    if quantity_as_int > 2:
                        discount_amount = round(quantity * unit_price - ((quantity_as_int // x) * 2 * unit_price + quantity_as_int % 3 * unit_price), 2)
                        discount = Discount(p, "3 for 2", -discount_amount)

                elif offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
                    x = 2
                    if quantity_as_int >= 2:
                        total = offer.argument * (quantity_as_int // x) + quantity_as_int % 2 * unit_price
                        discount_n = round(unit_price * quantity - total, 2)
                        discount = Discount(p, f"2 for {offer.argument}", -discount_n)

                elif offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
                    x = 5
                    if quantity_as_int >= 5:
                        discount_total = round(unit_price * quantity - (offer.argument * (quantity_as_int // x) + quantity_as_int % 5 * unit_price), 2)
                        discount = Discount(p, f"{x} for {offer.argument}", -discount_total)

                elif offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
                    discount = Discount(p, f"{offer.argument}% off", -round(quantity * unit_price * offer.argument / 100.0, 2))

                if discount:
                    receipt.add_discount(discount)

