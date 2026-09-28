"""
Session 1 -- Procedural version (plain dicts + functions).
Same domain and same portfolio output as finacial_asset_oop.py.
"""
from datetime import date

AS_OF = date(2026, 9, 25)

# Data: an asset is a plain dict, and its "type" is just a string.
def create_equity(ticker, price, currency, eps):
    return {"type": "equity", "ticker": ticker, "price": price,
            "currency": currency, "eps": eps}

def create_bond(ticker, price, currency, maturity_date, coupon_rate):
    # price quoted in % of par: 97 means 97% of nominal
    return {"type": "bond", "ticker": ticker, "price": price,
            "currency": currency, "maturity_date": maturity_date,
            "coupon_rate": coupon_rate}

def create_etf(ticker, price, currency, expense_ratio):  # NEW for ETF
    return {"type": "etf", "ticker": ticker, "price": price,
            "currency": currency, "expense_ratio": expense_ratio}


# Behavior: functions live apart from the data they are valid for.
def compute_pe_ratio(asset):
    # Only meaningful for an equity, but nothing stops you passing a bond.
    if asset["eps"] is None or asset["eps"] <= 0:
        return None  # undefined -- returning 0 would rank it as the cheapest stock
    return asset["price"] / asset["eps"]


def compute_ttm(asset, as_of):
    return (asset["maturity_date"] - as_of).days / 365  # ACT/365 fixed


def get_description(asset):
    header = f"{asset['ticker']} / price = {asset['price']} {asset['currency']}"
    # PAIN POINT 1: every function whose behaviour depends on the asset type needs its own if/elif on a string.
    # What "an equity" means is scattered across all such functions: adding a type means finding and editing each one.
    if asset["type"] == "equity":
        pe = compute_pe_ratio(asset)
        pe_txt = "n/a" if pe is None else f"{pe:.2f}"
        return f"Equity : {header} / P/E = {pe_txt}"
    elif asset["type"] == "bond":
        return (f"Bond : {header} / coupon = {asset['coupon_rate']:.2%}"
                f" / maturity = {asset['maturity_date']}")
    elif asset["type"] == "etf":  # EDITED for ETF: an existing, already-tested function
        return f"ETF : {header} / TER = {asset['expense_ratio']:.4%}"
    else:
        return f"FinancialAsset : {header}"


def market_value(asset, quantity):
    if asset["type"] == "bond":
        return quantity * asset["price"] / 100  # quantity = nominal, price in % of par
    # The else branch is a hand-made "default rule": ETF needed no edit here. The OOP version gets the same thing from inheritance.
    return quantity * asset["price"]


if __name__ == "__main__":
    aapl = create_equity("AAPL", 230, "USD", 6.1)
    ust = create_bond("UST 2030", 97, "USD", date(2030, 12, 31), 0.0405)
    spy = create_etf("SPY", 560, "USD", 0.000945)

    # a position = (asset, quantity); a bond quantity is a nominal amount
    portfolio = [(aapl, 100), (ust, 50_000), (spy, 20)]

    print("--- Portfolio ---")
    for asset, qty in portfolio:
        print(get_description(asset))
    total = sum(market_value(asset, qty) for asset, qty in portfolio)
    print(f"Total market value = {total:,.2f} USD")  # all USD here; mixing currencies needs FX
    print(f"TTM {ust['ticker']} = {compute_ttm(ust, AS_OF):.2f} years")

    print("\n--- Pain points, live ---")
    # PAIN POINT 2: nothing ties a function to the data it is valid for.
    # Both an equity and a bond are "a dict", so a type checker cannot tell
    # them apart: the mistake surfaces at runtime, far from where it was made.
    try:
        compute_pe_ratio(ust)
    except KeyError as err:
        print(f"compute_pe_ratio(bond) -> KeyError: {err}")

    # PAIN POINT 3: the type is a free-form string, so a typo is not an error.
    msft = {"type": "Equity", "ticker": "MSFT", "price": 420,
            "currency": "USD", "eps": 12.4}
    print(get_description(msft), "  <- 'Equity' != 'equity': P/E silently lost")


# ---------------------------------------------------------------------------
# The best procedural fix for PAIN POINT 1: replace if/elif with a table
# mapping each type to its function.
#
#     DESCRIBE = {"equity": describe_equity, "bond": describe_bond, ...}
#     DESCRIBE[asset["type"]](asset)
#
# Now keep one such table per operation, keep them all in sync, and bundle
# each type's data with its row of functions... You have rebuilt classes by
# hand. Python stores exactly this: each class holds a dict of its functions
# (look at Equity.__dict__), and asset.get_description() looks the function
# up on the object's class.
# ---------------------------------------------------------------------------