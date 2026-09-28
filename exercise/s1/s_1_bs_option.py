import math
from statistics import NormalDist


class Option:
    def __init__(self, s: float, k: float, r: float, ttm: float, sigma: float):
        self.S = s
        self.K = k
        self.r = r
        self.T = ttm
        self.sigma = sigma

    def d1(self):
        return ((math.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T)
                / (self.sigma * math.sqrt(self.T)))
    def d2(self):
        return self.d1() - self.sigma * math.sqrt(self.T)

    def vega(self):
        return self.S * NormalDist().pdf(self.d1()) * math.sqrt(self.T)


class Call(Option):
    def price(self):
        d1, d2 = self.d1(), self.d2()
        return self.S * NormalDist().cdf(d1) - self.K * math.exp(-self.r * self.T) * NormalDist().cdf(d2)

    def delta(self):
        return NormalDist().cdf(self.d1())

    def rho(self):
        return self.T * self.K * math.exp(-self.r * self.T) * NormalDist().cdf(self.d2())

    def theta(self):
        d1, d2 = self.d1(), self.d2()
        return (-(self.S * NormalDist().pdf(d1) * self.sigma) / (2 * math.sqrt(self.T))
                -self.r * self.K * math.exp(-self.r * self.T) * NormalDist().cdf(d2))

    def theta_per_day(self):
        return self.theta() / 365.0


class Put(Option):
    def price(self):
        d1, d2 = self.d1(), self.d2()
        return self.K * math.exp(-self.r * self.T) * NormalDist().cdf(-d2) - self.S * NormalDist().cdf(-d1)

    def delta(self):
        return NormalDist().cdf(self.d1()) - 1.0

    def rho(self):
        return -self.T * self.K * math.exp(-self.r * self.T) * NormalDist().cdf(-self.d2())

    def rho_per_1pct(self):
        return 0.01 * self.rho()

    def theta(self):
        d1, d2 = self.d1(), self.d2()
        return (-(self.S * NormalDist().pdf(d1) * self.sigma) / (2 * math.sqrt(self.T)) + self.r * self.K *
                math.exp(-self.r * self.T) * NormalDist().cdf(-d2))

    def theta_per_day(self):
        return self.theta() / 365.0


if __name__ == "__main__":
    call = Call(s=200, k=250, r=0.0365, ttm=1.0, sigma=0.15)
    put  = Put (s=200, k=250, r=0.0365, ttm=1.0, sigma=0.15)

    call_2 = Call(s=200, k=150, r=0.0365, ttm=1.0, sigma=0.15)
    put_2 = Put(s=200, k=150, r=0.0365, ttm=1.0, sigma=0.15)

    print(f"Call price: {call.price():.4f}")
    print(f"Put  price: {put.price():.4f}")

    print(f"Call Δ: {call.delta():.4f}")
    print(f"Put  Δ: {put.delta():.4f}")

    print(f"Vega  : {call.vega():.4f}")

    print(f"Call ρ: {call.rho():.4f}")
    print(f"Put  ρ: {put.rho():.4f}")

    print(f'Call θ per year: {call.theta():.4f}; θ/day: {call.theta_per_day():.4f}')
    print(f"Put  θ per year: {put.theta():.4f}; θ/day: {put.theta_per_day():.4f}")

    # Put-Call parity (q=0): C - P = S - K e^{-rT}
    lhs = call.price() - put.price()
    rhs = call.S - call.K * math.exp(-call.r * call.T)
    print(f"Put-Call parity -> {lhs:.4f} - {rhs:.4f} = {lhs - rhs:.8f} ")