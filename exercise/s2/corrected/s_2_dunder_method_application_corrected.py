"""
### SOLUTION

### Part 1 - FinancialAsset
You are given a class `FinancialAsset` that represents a financial asset with a ticker, a price and a currency.
The class already has a method `get_description()` that returns a description of the asset.

#### Your Tasks:
1. **Implement the `__str__` Method**: `__str__` should return a readable description of the asset.
    Before writing it, check whether an existing method already builds that string: reuse it, don't duplicate it.

2. **Implement the `__eq__` Method**: two `FinancialAsset` objects are equal if they have the same `ticker`
    and the same `currency`. The price is NOT part of the comparison: AAPL quoted at 150 USD and AAPL quoted
    at 200 USD are the same instrument, observed at two different moments.
    If the other object is not a `FinancialAsset`, return `NotImplemented` (not `False`): Python will then
    try the reflected comparison and, if nothing matches, `==` will return `False` on its own.

3. **Implement the `__hash__` Method**: as soon as you define `__eq__`, Python sets `__hash__` to `None`,
    so your assets can no longer be put in a `set` or used as `dict` keys (try it before implementing!).
    Rule: two objects that are equal must have the same hash. Hash the attributes used in `__eq__`.

### What to Check:
- `str(asset)` returns the description.
- `==` and `!=` behave as described above (you never implement `__ne__`: Python derives it from `__eq__`).
- A set of assets keeps a single entry per (ticker, currency).
"""
import unittest


class FinancialAsset:
    def __init__(self, ticker, price, currency):
        self.ticker: str = ticker
        self.price: float = price
        self.currency: str = currency

    def get_description(self):
        return f'The ticker for this asset is {self.ticker} and its price is {self.price} {self.currency}'

    def __str__(self):
        return self.get_description()

    def __repr__(self):
        return f"FinancialAsset(ticker={self.ticker}, price={self.price}, currency={self.currency}"

    def __eq__(self, other):
        if isinstance(other, FinancialAsset):
            return self.ticker == other.ticker and self.currency == other.currency
        return NotImplemented

    def __hash__(self):
        # Equal objects must have equal hashes -> hash exactly the attributes used in __eq__.
        # Never include price: two equal assets with different prices would get different hashes.
        return hash((self.ticker, self.currency))


"""
### Part 2 - InstrumentList
You are given a class `InstrumentList` that represents a collection of `FinancialAsset` objects.
Implement two special methods, `__add__` and `__sub__`, to add an asset to the collection and remove one from it.

**Implement the `__add__` Method** (`instrument_list + asset`):
    - Returns a NEW `InstrumentList` containing the existing assets plus `asset`.
    - The original `InstrumentList` must be left unchanged.
    - If `asset` is not a `FinancialAsset`, raise a `TypeError`.

**Implement the `__sub__` Method** (`instrument_list - asset`):
    - Returns a NEW `InstrumentList` without the assets equal to `asset`.
      "Equal" means equal in the sense of your `__eq__` from Part 1 (same ticker and currency, whatever the price).
    - If no asset is equal to `asset`, the new list has the same content as the original one.
    - The original `InstrumentList` must be left unchanged.
    - If `asset` is not a `FinancialAsset`, raise a `TypeError`.

**Hint:** `self.instruments.append(...)` modifies the list in place. Think about what that means for the
original object, and build a new Python list instead.
"""


class InstrumentList:
    def __init__(self, list_of_instrument):
        self.instruments: list[FinancialAsset] = list_of_instrument

    def __add__(self, other):
        if not isinstance(other, FinancialAsset):
            raise TypeError(f"Can only add a FinancialAsset to an InstrumentList, not {type(other).__name__}")
        # self.instruments + [other] builds a NEW list: the original InstrumentList is untouched.
        # (self.instruments.append(other) would mutate self, and every alias of it.)
        return InstrumentList(self.instruments + [other])

    def __sub__(self, other):
        if not isinstance(other, FinancialAsset):
            raise TypeError(f"Can only subtract a FinancialAsset from an InstrumentList, not {type(other).__name__}")
        # != relies on __eq__ (Python derives __ne__ from it), so any quote of the same
        # instrument (same ticker and currency, whatever the price) is removed.
        # If nothing matches, the new list simply contains the same assets.
        return InstrumentList([asset for asset in self.instruments if asset != other])


"""
UNIT TESTS
"""


class TestFinancialAsset(unittest.TestCase):
    def test_str_method(self):
        asset = FinancialAsset("AAPL", 150.0, "USD")
        self.assertEqual(str(asset), 'The ticker for this asset is AAPL and its price is 150.0 USD')

    def test_eq_method_same_ticker_and_currency(self):
        asset1 = FinancialAsset("AAPL", 150.0, "USD")
        asset2 = FinancialAsset("AAPL", 200.0, "USD")
        self.assertTrue(asset1 == asset2)
        self.assertFalse(asset1 != asset2)

    def test_eq_method_different_ticker(self):
        asset1 = FinancialAsset("AAPL", 150.0, "USD")
        asset2 = FinancialAsset("MSFT", 150.0, "USD")
        self.assertFalse(asset1 == asset2)
        self.assertTrue(asset1 != asset2)

    def test_eq_method_different_currency(self):
        asset1 = FinancialAsset("AAPL", 150.0, "USD")
        asset2 = FinancialAsset("AAPL", 150.0, "EUR")
        self.assertFalse(asset1 == asset2)

    def test_eq_method_different_object(self):
        asset = FinancialAsset("AAPL", 150.0, "USD")
        self.assertFalse(asset == "Not a FinancialAsset object")
        self.assertIs(asset.__eq__("Not a FinancialAsset object"), NotImplemented)

    def test_hash_method(self):
        quotes = {
            FinancialAsset("AAPL", 150.0, "USD"),
            FinancialAsset("AAPL", 151.2, "USD"),
            FinancialAsset("AAPL", 139.0, "EUR"),
        }
        self.assertEqual(len(quotes), 2)


class TestInstrumentList(unittest.TestCase):
    def setUp(self):
        self.asset1 = FinancialAsset("AAPL", 150.0, "USD")
        self.asset2 = FinancialAsset("MSFT", 250.0, "USD")
        self.asset3 = FinancialAsset("NVDA", 120.0, "USD")
        self.instrument_list = InstrumentList([self.asset1, self.asset2])

    def test_add_method(self):
        new_list = self.instrument_list + self.asset3
        self.assertIn(self.asset3, new_list.instruments)
        self.assertEqual(len(new_list.instruments), 3)

    def test_add_method_returns_new_object(self):
        new_list = self.instrument_list + self.asset3
        self.assertIsNot(new_list, self.instrument_list)
        self.assertEqual(len(self.instrument_list.instruments), 2)

    def test_add_method_invalid_type(self):
        with self.assertRaises(TypeError):
            _ = self.instrument_list + "Not a FinancialAsset object"

    def test_sub_method(self):
        new_list = self.instrument_list - self.asset1
        self.assertNotIn(self.asset1, new_list.instruments)
        self.assertEqual(len(new_list.instruments), 1)

    def test_sub_method_uses_eq(self):
        # A new quote of AAPL (different object, different price) is the same instrument: it must be removed
        new_list = self.instrument_list - FinancialAsset("AAPL", 999.0, "USD")
        self.assertEqual(len(new_list.instruments), 1)
        self.assertEqual(new_list.instruments[0].ticker, "MSFT")

    def test_sub_method_returns_new_object(self):
        new_list = self.instrument_list - self.asset1
        self.assertIsNot(new_list, self.instrument_list)
        self.assertEqual(len(self.instrument_list.instruments), 2)

    def test_sub_method_non_existing_asset(self):
        new_list = self.instrument_list - self.asset3  # asset3 is not in the list
        self.assertEqual(new_list.instruments, self.instrument_list.instruments)
        self.assertEqual(len(new_list.instruments), 2)

    def test_sub_method_invalid_type(self):
        with self.assertRaises(TypeError):
            _ = self.instrument_list - "Not a FinancialAsset object"


def run_tests():
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == "__main__":
    run_tests()