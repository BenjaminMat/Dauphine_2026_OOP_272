from datetime import datetime

class FinancialAsset:
    def __init__(self, ticker: str, price : float, currency: str):
        self.ticker = ticker
        self.price = price
        self.currency = currency

    def get_description(self):
        print(f"FinancialAsset : ticker = {self.ticker} / price = {self.price} {self.currency}")


class Equity(FinancialAsset):
    def __init__(self, ticker: str, price: float, currency: str, eps: float):
        super().__init__(ticker, price, currency)
        self.eps = eps
        self.pe = self.calculate_pe_ratio()

    def calculate_pe_ratio(self) -> float :
        if self.eps is None or self.eps <= 0:
            return 0  # P/E not meaningful with non-positive/unknown EPS
        return self.price / self.eps

    def get_description(self):
        print(f"Equity : ticker = {self.ticker} / price = {self.price} {self.currency} / pe = {self.pe}")


class Bond(FinancialAsset):
    def __init__(self, ticker: str, price : float, currency: str, maturity_date : datetime, coupon_rate: float):
        super().__init__(ticker,price,currency)
        self.maturity_date: datetime = maturity_date
        self.coupon_rate: float = coupon_rate

    def compute_ttm(self):
        today = datetime.now()
        delta = self.maturity_date - today
        return delta.days / 365



if __name__ == '__main__':
    financial_asset_1 = FinancialAsset("AAPL", 230, "USD")
    financial_asset_1.get_description()

    equity = Equity('AAPL', 230, 'USD', 6.1)  # create an Equity Asset object
    equity.get_description()  # call the method defined in the Parent class
    print(f"PE ratio for {equity.ticker} : {round(equity.calculate_pe_ratio(), 2)}")

    bond_maturity = datetime(2030, 12, 31)
    bond = Bond("US10YT", 97, "USD", bond_maturity, 0.0405)
    print(f"ttm for bond {round(bond.compute_ttm(), 2)}")
