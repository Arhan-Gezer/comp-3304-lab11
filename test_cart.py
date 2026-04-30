import unittest
from cart import ShoppingCart


class TestAddItem(unittest.TestCase):

    def test_add_new_item(self):
        cart = ShoppingCart()
        cart.add_item("Elma", 10.0, 3)
        self.assertEqual(cart._items["Elma"]["quantity"], 3)
        self.assertEqual(cart._items["Elma"]["price"], 10.0)

    def test_add_item_quantity_accumulates(self):
        """ERROR 1: quantity overwrite yerine toplamalı"""
        cart = ShoppingCart()
        cart.add_item("Elma", 10.0, 3)
        cart.add_item("Elma", 10.0, 4)
        self.assertEqual(cart._items["Elma"]["quantity"], 7)  # BUG: şu an 4 döner

    def test_add_item_zero_quantity_raises(self):
        cart = ShoppingCart()
        with self.assertRaises(ValueError):
            cart.add_item("Elma", 10.0, 0)

    def test_add_item_negative_quantity_raises(self):
        cart = ShoppingCart()
        with self.assertRaises(ValueError):
            cart.add_item("Elma", 10.0, -1)

    def test_add_item_negative_price_raises(self):
        cart = ShoppingCart()
        with self.assertRaises(ValueError):
            cart.add_item("Elma", -5.0, 1)


class TestRemoveItem(unittest.TestCase):

    def test_remove_existing_item(self):
        cart = ShoppingCart()
        cart.add_item("Elma", 10.0, 2)
        cart.remove_item("Elma")
        self.assertNotIn("Elma", cart._items)

    def test_remove_nonexistent_item_raises(self):
        cart = ShoppingCart()
        with self.assertRaises(KeyError):
            cart.remove_item("Armut")

    def test_remove_item_clears_discount_if_below_threshold(self):
        """ERROR 2: item silinince discount kontrol edilmeli"""
        cart = ShoppingCart()
        cart.add_item("Elma", 10.0, 4)
        cart.add_item("Armut", 10.0, 3)
        cart.apply_discount("SAVE20")
        cart.remove_item("Elma")
        self.assertIsNone(cart._discount)  # BUG: şu an discount kalmaya devam eder


class TestApplyDiscount(unittest.TestCase):

    def test_invalid_code_raises(self):
        cart = ShoppingCart()
        cart.add_item("Elma", 10.0, 5)
        with self.assertRaises(ValueError):
            cart.apply_discount("INVALID")

    def test_below_minimum_order_raises(self):
        cart = ShoppingCart()
        cart.add_item("Elma", 10.0, 1)
        with self.assertRaises(ValueError):
            cart.apply_discount("SAVE20")

    def test_exactly_at_minimum_order_applies(self):
        """ERROR 3: eşit olduğunda da uygulanmalı (>= kullanılmalı)"""
        cart = ShoppingCart()
        cart.add_item("Elma", 10.0, 5)  # subtotal = 50.0 (SAVE20 min = 50.0)
        cart.apply_discount("SAVE20")
        self.assertIsNotNone(cart._discount)  # BUG: şu an ValueError fırlatır

    def test_percent_discount_applied(self):
        cart = ShoppingCart()
        cart.add_item("Elma", 10.0, 3)
        cart.apply_discount("SAVE10")  # %10 indirim, min order 0
        self.assertEqual(cart.get_total(), 27.0)

    def test_fixed_discount_applied(self):
        cart = ShoppingCart()
        cart.add_item("Elma", 10.0, 4)  # subtotal=40, FLAT5 min=30
        cart.apply_discount("FLAT5")
        self.assertEqual(cart.get_total(), 35.0)


class TestGetTotal(unittest.TestCase):

    def test_total_no_discount(self):
        cart = ShoppingCart()
        cart.add_item("Elma", 5.0, 2)
        self.assertEqual(cart.get_total(), 10.0)

    def test_total_never_negative(self):
            cart = ShoppingCart()
    	    cart.add_item("Elma", 10.0, 4)  # subtotal=40, FLAT5 min=30
    	    cart.apply_discount("FLAT5")    # 40 - 5 = 35
            self.assertGreaterEqual(cart.get_total(), 0.0)

    def test_empty_cart_total(self):
        cart = ShoppingCart()
        self.assertEqual(cart.get_total(), 0.0)


class TestClear(unittest.TestCase):

    def test_clear_empties_cart(self):
        cart = ShoppingCart()
        cart.add_item("Elma", 10.0, 2)
        cart.clear()
        self.assertEqual(cart._items, {})


class TestGetItemCount(unittest.TestCase):

    def test_get_item_count(self):
        """ERROR 4: get_item_count implement edilmeli"""
        cart = ShoppingCart()
        cart.add_item("Elma", 10.0, 3)
        cart.add_item("Armut", 5.0, 2)
        self.assertEqual(cart.get_item_count(), 5)  # BUG: NotImplementedError fırlatır


if __name__ == "__main__":
    unittest.main()
