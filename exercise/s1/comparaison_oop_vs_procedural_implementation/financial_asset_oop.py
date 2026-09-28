"""
Session 1 -- Object-oriented version.
Same domain and same portfolio output as procedural_assets.py.
  * the portfolio loop contains no if/elif on the asset type
  * ETF support was added without editing a single existing line -> extension
  * each method sits next to the data it needs                   -> encapsulation

"""
from datetime import date

AS_OF = date(2026, 9, 25)

class FinancialAsset:
    def __init__(self, ticker: str, price: float, currency: str):
        self.ticker = ticker
        self.price = price
        self.currency = currency

    def get_description(self) -> str:
        return f"{type(self).__name__} : {self.ticker} / price = {self.price} {self.currency}"

    def market_value(self, quantity: float) -> float:
        return quantity * self.price


class Equity(FinancialAsset):
    def __init__(self, ticker: str, price: float, currency: str, eps: float | None):
        super().__init__(ticker, price, currency)
        self.eps = eps

    def calculate_pe_ratio(self) -> float | None:
        # computed on demand, so it can never go stale if the price changes
        if self.eps is None or self.eps <= 0:
            return None
        return self.price / self.eps

    def get_description(self) -> str:
        pe = self.calculate_pe_ratio()
        pe_txt = "n/a" if pe is None else f"{pe:.2f}"
        return f"{super().get_description()} / P/E = {pe_txt}"


class Bond(FinancialAsset):
    def __init__(self, ticker: str, price: float, currency: str, maturity_date: date, coupon_rate: float):
        super().__init__(ticker, price, currency)
        self.maturity_date = maturity_date
        self.coupon_rate = coupon_rate

    def compute_ttm(self, as_of: date) -> float:
        return (self.maturity_date - as_of).days / 365

    def get_description(self) -> str:
        return f"{super().get_description()} / coupon = {self.coupon_rate:.2%} / maturity = {self.maturity_date}"

    def market_value(self, quantity: float) -> float:
         return quantity * self.price / 100


class ETF(FinancialAsset):
    def __init__(self, ticker: str, price: float, currency: str, expense_ratio: float):
        super().__init__(ticker, price, currency)
        self.expense_ratio = expense_ratio

    def get_description(self) -> str:
        return f"{super().get_description()} / TER = {self.expense_ratio:.4%}"

    # no market_value here: FinancialAsset's default rule is inherited


if __name__ == "__main__":
    aapl = Equity("AAPL", 230, "USD", 6.1)
    ust = Bond("UST 2030", 97, "USD", date(2030, 12, 31), 0.0405)
    spy = ETF("SPY", 560, "USD", 0.0025)

    portfolio = [(aapl, 100), (ust, 50_000), (spy, 20)]

    print("--- Portfolio ---")
    for asset, qty in portfolio:
        print(asset.get_description())
    total = sum(asset.market_value(qty) for asset, qty in portfolio)
    print(f"Total market value = {total:,.2f} USD")  # all USD here; mixing currencies needs FX
    print(f"TTM {ust.ticker} = {ust.compute_ttm(AS_OF):.2f} years")

    print("\n--- The same mistakes, OOP side ---")
    try:
        ust.calculate_pe_ratio()  # the IDE flag this line BEFORE running
    except AttributeError as err:
        print(f"bond.calculate_pe_ratio() -> AttributeError: {err}")

    # A typo in a class name fails loudly, on the line with the typo:
    #     msft = Equty("MSFT", 420, "USD", 12.4)   -> NameError
    # whereas {"type": "Equity"} in the procedural version failed silently.