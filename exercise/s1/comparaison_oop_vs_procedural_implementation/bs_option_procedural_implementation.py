"""
Below a procedural implementation of a BS pricer (without dividend).

 Why OOP might be usefull for option pricing?

 An option is a natural object: it has parameters (S, K, r, T, sigma) and it can answer questions about itself (
 price, delta, theta, ...). Modelling it as a class instead of a set of functions brings several advantages.

 1. Parameters are stored once
    With call.price() and call.delta(), the parameters are given a single time, at construction.
    You cannot price with one set of numbers and compute the Greeks with another, which is easy to do when passing six
    arguments to several separate functions.

 2. Shared logic lives in one place
    d1, d2 and vega are identical for calls and puts, so they sit in the base class. Each subclass only contains what
    really differs (price, delta, theta, rho). A bug fixed in d1 is fixed for every option type.

 3. Calls and puts are handled uniformly (polymorphism)
    Once you have several options, you can loop over them without caring &about their type:

        portfolio = [Call(...), Put(...)]
        total_value = sum(o.price() for o in portfolio)
        total_delta = sum(o.delta() for o in portfolio)

    The functional version needs tuples of parameters plus an option_type
    string, and has to rebuild every computation each time.

 4. The class structure is safer than a string
    option_type="cal" only fails at runtime in the functional version. With classes you pick Call or Put directly.
    With an abstract base class, a new option type must implement price, delta, theta and rho, otherwise Python refuses
    to instantiate it.

 5. Easy to extend
    Adding a new payoff (digital option, etc.) means writing a new subclass without touching existing code.
    In the functional version, every if/elif chain has to be edited, and each edit risks breaking what
    already works.

 6. The code reads like the domain
    put.theta_per_day() says what it means, and everyone understands the structure quickly.

 Caveats
    - For a script pricing two options, plain functions are shorter and easier to test. OOP pays off as the code grows
    (more option types, portfolios, a pricing engine reused in several places).

"""

from math import exp, log, sqrt, erf, pi


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))


def norm_pdf(x: float) -> float:
    return exp(-0.5 * x**2) / sqrt(2.0 * pi)


def d1_d2(S: float, K: float, T: float, r: float, sigma: float):
    d1 = (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return d1, d2


def black_scholes(S: float, K: float, T: float, r: float, sigma: float,
                  option_type: str = "call") -> float:
    if S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
        raise ValueError("S, K, T & sigma must be positive.")

    d1, d2 = d1_d2(S, K, T, r, sigma)

    if option_type.lower() == "call":
        return S * norm_cdf(d1) - K * exp(-r * T) * norm_cdf(d2)
    if option_type.lower() == "put":
        return K * exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)
    raise ValueError("option_type must be 'call' or 'put'.")


def greeks(S: float, K: float, T: float, r: float, sigma: float,
           option_type: str = "call") -> dict:
    if S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
        raise ValueError("S, K, T & sigma must be positive.")

    d1, d2 = d1_d2(S, K, T, r, sigma)
    disc_r = exp(-r * T)

    vega = S * norm_pdf(d1) * sqrt(T)
    theta_common = -S * norm_pdf(d1) * sigma / (2.0 * sqrt(T))

    if option_type.lower() == "call":
        delta = norm_cdf(d1)
        theta = theta_common - r * K * disc_r * norm_cdf(d2)
        rho = K * T * disc_r * norm_cdf(d2)
    elif option_type.lower() == "put":
        delta = norm_cdf(d1) - 1.0
        theta = theta_common + r * K * disc_r * norm_cdf(-d2)
        rho = -K * T * disc_r * norm_cdf(-d2)
    else:
        raise ValueError("option_type must be 'call' or 'put'.")

    return {"delta": delta, "vega": vega, "theta": theta, "rho": rho}


if __name__ == "__main__":
    cases = [
        ("Case 1 (K=250)", 200, 250, 1.0, 0.0365, 0.15),
        ("Case 2 (K=150)", 200, 150, 1.0, 0.0365, 0.15),
    ]

    for name, S, K, T, r, sigma in cases:
        call = black_scholes(S, K, T, r, sigma, "call")
        put = black_scholes(S, K, T, r, sigma, "put")
        g_call = greeks(S, K, T, r, sigma, "call")
        g_put = greeks(S, K, T, r, sigma, "put")

        print(f"{name}")
        print(f"  Call : {call:.4f}")
        print(f"  Put  : {put:.4f}")
        print(f"  Delta call/put : {g_call['delta']:.4f} / {g_put['delta']:.4f}")
        print(f"  Vega (+1 %)          : {g_call['vega'] / 100:.4f}")
        print(f"  Theta call/put (per day) : {g_call['theta'] / 365:.4f} / {g_put['theta'] / 365:.4f}")
        print(f"  Rho call/put (+1 %)  : {g_call['rho'] / 100:.4f} / {g_put['rho'] / 100:.4f}")
        print()

        parity = call - put - (S - K * exp(-r * T))
        print(f"call-put parity : {parity:.2e}")
        print()