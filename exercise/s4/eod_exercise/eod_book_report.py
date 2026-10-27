"""
EXERCISE - Refactoring a procedural script with OOP
===================================================

The script below produces an end-of-day (EOD) report for a small multi-asset book:
two US equities, a Euro Stoxx 50 future and a French government bond (OAT).
Input data (instruments, prices, trades, FX rate, price corrections) lives in the data/ folder next to the script.

Objective: reshape it with the OOP concepts seen in class so that it could live in a production codebase, be tested,
and be extended to new instruments easily.

Deliverables
------------
1. A refactored version of the script.
2. The refactored code must print the same numbers as the original report.
3. (Optional) A short note (max 1 page) explaining, for each design choice, what you changed
   and why it is better.

Constraints
-----------
- Each class should have one clear responsibility (no single "All-in class").
- Importing your module must not run anything: no print, no file written.

Things worth looking at
-----------------------
- How data is represented (dicts, tuples).
- Calculations or branches that are repeated.
- Code copied around several functions.
- Values that are derived from other values.
- Hard-coded numbers.
- How errors are reported.
- Where the state lives and who modifies it.
- The different input formats.

Bonus: once refactored, add a new instrument type.
How many places in your code did you have to touch? How many in the original?
"""

# =============================================================================
#  eod_book_report.py - EOD report for the multi-asset book
# =============================================================================
import csv
import math
import os
import statistics
import time
from datetime import datetime

# -----------------------------------------------------------------------------
# static data (read from the data/ folder next to this script)
# -----------------------------------------------------------------------------
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

INSTRUMENTS = {}
with open(os.path.join(DATA_DIR, "instruments.csv")) as f:
    for row in csv.DictReader(f):
        INSTRUMENTS[row["ticker"]] = {"type": row["type"], "ccy": row["ccy"]}
        if row["multiplier"]:
            INSTRUMENTS[row["ticker"]]["multiplier"] = int(row["multiplier"])
        # bonds: price in % of par, qty = nominal

with open(os.path.join(DATA_DIR, "prices.csv")) as f:
    PRICES_CSV = f.read()

# trades entered by the desk in the blotter: date|ticker|side|qty|price
with open(os.path.join(DATA_DIR, "blotter_trades.txt")) as f:
    BLOTTER_TRADES = [line.strip() for line in f if line.strip()]

# trades received from the broker: unsigned quantity, side given separately
with open(os.path.join(DATA_DIR, "broker_trades.csv")) as f:
    BROKER_TRADES = list(csv.DictReader(f))

with open(os.path.join(DATA_DIR, "fx_rates.csv")) as f:
    FX_RATES = {row["pair"]: float(row["rate"]) for row in csv.DictReader(f)}
EURUSD = FX_RATES["EURUSD"]

# corrected closes received from the exchange after the batch has run
with open(os.path.join(DATA_DIR, "price_corrections.csv")) as f:
    PRICE_CORRECTIONS = {row["ticker"]: float(row["close"]) for row in csv.DictReader(f)}

# -----------------------------------------------------------------------------
# global state
# -----------------------------------------------------------------------------
PORTFOLIO = {}
CALL_COUNTS = {"get_last_price": 0, "compute_volatility": 0}
_VOL_CACHE = {}
TRADE_LOG_FILE = "trades_log.txt"


# -----------------------------------------------------------------------------
# loading
# -----------------------------------------------------------------------------
def load_prices(csv_text):
    t0 = time.time()
    prices = {}
    lines = csv_text.strip().split("\n")
    for line in lines[1:]:
        parts = line.split(",")
        d = datetime.strptime(parts[0], "%Y-%m-%d")
        ticker = parts[1]
        px = float(parts[2])
        if ticker not in prices:
            prices[ticker] = []
        prices[ticker].append((d, px))
    print(f"[TIMER] load_prices took {time.time() - t0:.6f}s")
    return prices


def parse_blotter_trade(line):
    parts = line.split("|")
    qty = float(parts[3])
    if parts[2] == "SELL":
        qty = -qty
    return {
        "date": datetime.strptime(parts[0], "%Y-%m-%d"),
        "ticker": parts[1],
        "qty": qty,
        "price": float(parts[4]),
    }


def parse_broker_trade(d):
    qty = float(d["q"])
    if d["side"] == "S":
        qty = -qty
    return {
        "date": datetime.fromisoformat(d["ts"]),
        "ticker": d["sym"],
        "qty": qty,
        "price": float(d["px"]),
    }


# -----------------------------------------------------------------------------
# booking
# -----------------------------------------------------------------------------
def book_trade(trade):
    ticker = trade["ticker"]
    qty = trade["qty"]
    px = trade["price"]
    if ticker not in INSTRUMENTS:
        raise ValueError(f"Unknown instrument: {ticker}")
    if px <= 0:
        raise ValueError(f"Invalid price for {ticker}: {px}")
    if qty == 0:
        raise ValueError(f"Zero quantity for {ticker}")

    if ticker not in PORTFOLIO:
        PORTFOLIO[ticker] = {
            "qty": 0.0,
            "avg_price": 0.0,
            "realized_pnl": 0.0,  # in instrument currency
            "type": INSTRUMENTS[ticker]["type"],
            "ccy": INSTRUMENTS[ticker]["ccy"],
        }
    pos = PORTFOLIO[ticker]
    old_qty = pos["qty"]

    if old_qty == 0 or (old_qty > 0) == (qty > 0):
        # opening or increasing the position: weighted average entry price
        pos["avg_price"] = (pos["avg_price"] * old_qty + px * qty) / (old_qty + qty)
        pos["qty"] = old_qty + qty
    else:
        # reducing, closing or flipping: realize PnL on the closed quantity
        closed_qty = min(abs(qty), abs(old_qty)) * (1 if old_qty > 0 else -1)
        if pos["type"] == "equity":
            pos["realized_pnl"] += closed_qty * (px - pos["avg_price"])
        elif pos["type"] == "future":
            pos["realized_pnl"] += closed_qty * (px - pos["avg_price"]) * INSTRUMENTS[ticker]["multiplier"]
        elif pos["type"] == "bond":
            pos["realized_pnl"] += closed_qty * (px - pos["avg_price"]) / 100
        new_qty = old_qty + qty
        if new_qty == 0:
            pos["avg_price"] = 0.0
        elif (new_qty > 0) != (old_qty > 0):
            pos["avg_price"] = px  # position flipped: the remainder is a new position
        pos["qty"] = new_qty

    with open(TRADE_LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - BOOKED - {trade}\n")


def book_all_trades():
    t0 = time.time()
    for line in BLOTTER_TRADES:
        book_trade(parse_blotter_trade(line))
    for d in BROKER_TRADES:
        book_trade(parse_broker_trade(d))
    print(f"[TIMER] book_all_trades took {time.time() - t0:.6f}s")


# -----------------------------------------------------------------------------
# pricing
# -----------------------------------------------------------------------------
def get_last_price(prices, ticker):
    CALL_COUNTS["get_last_price"] += 1
    return prices[ticker][-1][1]


def compute_exposure(ticker, pos):
    # market value for cash instruments, notional for futures (instrument currency)
    if pos["type"] == "equity":
        return pos["qty"] * pos["last_price"]
    elif pos["type"] == "future":
        return pos["qty"] * pos["last_price"] * INSTRUMENTS[ticker]["multiplier"]
    elif pos["type"] == "bond":
        return pos["qty"] * pos["last_price"] / 100
    else:
        raise ValueError(f"Unknown instrument type: {pos['type']}")


def compute_unrealized_pnl(ticker, pos):
    if pos["type"] == "equity":
        pnl = pos["qty"] * (pos["last_price"] - pos["avg_price"])
    elif pos["type"] == "future":
        pnl = pos["qty"] * (pos["last_price"] - pos["avg_price"]) * INSTRUMENTS[ticker]["multiplier"]
    elif pos["type"] == "bond":
        pnl = pos["qty"] * (pos["last_price"] - pos["avg_price"]) / 100
    else:
        raise ValueError(f"Unknown instrument type: {pos['type']}")
    if pos["ccy"] == "USD":
        pnl = pnl / EURUSD
    return pnl


def mark_to_market(prices):
    t0 = time.time()
    for ticker in PORTFOLIO:
        pos = PORTFOLIO[ticker]
        pos["last_price"] = get_last_price(prices, ticker)
        exposure = compute_exposure(ticker, pos)
        if pos["ccy"] == "USD":
            exposure = exposure / EURUSD
        pos["exposure_eur"] = exposure
    print(f"[TIMER] mark_to_market took {time.time() - t0:.6f}s")


def update_price(ticker, new_price):
    # used when the exchange sends a corrected close after the batch has run
    pos = PORTFOLIO[ticker]
    pos["last_price"] = new_price
    exposure = compute_exposure(ticker, pos)
    if pos["ccy"] == "USD":
        exposure = exposure / EURUSD
    pos["exposure_eur"] = exposure


# -----------------------------------------------------------------------------
# risk and performance attribution
# -----------------------------------------------------------------------------
def compute_returns(price_list):
    returns = []
    for i in range(1, len(price_list)):
        returns.append(price_list[i] / price_list[i - 1] - 1)
    return returns


def compute_volatility(ticker, prices):
    CALL_COUNTS["compute_volatility"] += 1
    if ticker in _VOL_CACHE:
        return _VOL_CACHE[ticker]
    closes = [p[1] for p in prices[ticker]]
    rets = compute_returns(closes)
    vol = statistics.stdev(rets) * math.sqrt(252)
    _VOL_CACHE[ticker] = vol
    return vol


def compute_max_drawdown(ticker, prices):
    closes = [p[1] for p in prices[ticker]]
    peak = closes[0]
    max_dd = 0.0
    for c in closes:
        if c > peak:
            peak = c
        dd = (peak - c) / peak
        if dd > max_dd:
            max_dd = dd
    return max_dd


def compute_portfolio_daily_pnl(prices):
    # daily PnL in EUR of the CURRENT positions, held constant over the history
    first_ticker = next(iter(prices))
    n = len(prices[first_ticker])  # all tickers share the same dates
    daily_pnl = []
    for i in range(1, n):
        total = 0.0
        for ticker in PORTFOLIO:
            pos = PORTFOLIO[ticker]
            move = prices[ticker][i][1] - prices[ticker][i - 1][1]
            if pos["type"] == "equity":
                pnl = pos["qty"] * move
            elif pos["type"] == "future":
                pnl = pos["qty"] * move * INSTRUMENTS[ticker]["multiplier"]
            elif pos["type"] == "bond":
                pnl = pos["qty"] * move / 100
            else:
                raise ValueError(f"Unknown instrument type: {pos['type']}")
            if pos["ccy"] == "USD":
                pnl = pnl / EURUSD
            total += pnl
        daily_pnl.append(total)
    return daily_pnl


def compute_pnl_max_drawdown(daily_pnl):
    # largest peak-to-trough fall of the cumulative PnL, in EUR
    cumulative = 0.0
    peak = 0.0
    max_dd = 0.0
    for p in daily_pnl:
        cumulative += p
        if cumulative > peak:
            peak = cumulative
        if peak - cumulative > max_dd:
            max_dd = peak - cumulative
    return max_dd


def compute_risk(prices):
    t0 = time.time()
    risk = {}
    for ticker in PORTFOLIO:
        risk[ticker] = {
            "vol": compute_volatility(ticker, prices),
            "max_dd": compute_max_drawdown(ticker, prices),
        }
    daily_pnl = compute_portfolio_daily_pnl(prices)
    risk["PORTFOLIO"] = {
        "pnl_vol": statistics.stdev(daily_pnl) * math.sqrt(252),
        "pnl_max_dd": compute_pnl_max_drawdown(daily_pnl),
    }
    print(f"[TIMER] compute_risk took {time.time() - t0:.6f}s")
    return risk


# -----------------------------------------------------------------------------
# report
# -----------------------------------------------------------------------------
def print_report(risk, as_of):
    t0 = time.time()
    width = 95
    print("=" * width)
    print(f"EOD REPORT - as of {as_of:%Y-%m-%d}")
    print("=" * width)
    print(
        f"{'Ticker':<10}{'Qty':>10}{'Avg px':>10}{'Last px':>10}"
        f"{'Exposure (EUR)':>19}{'Unreal. (EUR)':>18}{'Real. (EUR)':>18}"
    )
    total_exposure = 0.0
    total_unrealized = 0.0
    total_realized = 0.0
    for ticker in PORTFOLIO:
        pos = PORTFOLIO[ticker]
        unrealized = compute_unrealized_pnl(ticker, pos)
        realized = pos["realized_pnl"]
        if pos["ccy"] == "USD":
            realized = realized / EURUSD
        total_exposure += pos["exposure_eur"]
        total_unrealized += unrealized
        total_realized += realized
        print(
            f"{ticker:<10}{pos['qty']:>10,.0f}{pos['avg_price']:>10.2f}{pos['last_price']:>10.2f}"
            f"{pos['exposure_eur']:>19,.2f}{unrealized:>18,.2f}{realized:>18,.2f}"
        )
    print("-" * width)
    print(f"{'TOTAL':<40}{total_exposure:>19,.2f}{total_unrealized:>18,.2f}{total_realized:>18,.2f}")
    print()
    print(f"{'Ticker':<10}{'Ann. vol':>12}{'Max DD':>12}")
    for ticker in PORTFOLIO:
        r = risk[ticker]
        print(f"{ticker:<10}{r['vol']:>12.2%}{r['max_dd']:>12.2%}")
    print()
    print(f"Portfolio annualised PnL vol (EUR): {risk['PORTFOLIO']['pnl_vol']:,.2f}")
    print(f"Portfolio PnL max drawdown (EUR):   {risk['PORTFOLIO']['pnl_max_dd']:,.2f}")
    print(f"Call counts: {CALL_COUNTS}")
    print(f"[TIMER] print_report took {time.time() - t0:.6f}s")


# -----------------------------------------------------------------------------
# run
# -----------------------------------------------------------------------------
prices = load_prices(PRICES_CSV)
book_all_trades()
mark_to_market(prices)
for ticker in PRICE_CORRECTIONS:
    update_price(ticker, PRICE_CORRECTIONS[ticker])
risk = compute_risk(prices)
print_report(risk, prices["AAPL"][-1][0])
