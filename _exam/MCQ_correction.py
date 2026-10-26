"""
=======================================================
MCQ Correction - Object-Oriented Programming in Python
=======================================================
"""

import math
import sys
from statistics import NormalDist


# =============================================================================
# 1. OOP FUNDAMENTALS
# =============================================================================


"""Q1 - What are the pillars of OOP in Python?

Correct answer: A (Encapsulation), B (Inheritance), C (Polymorphism).

- Encapsulation: bundle data and the methods acting on it in one unit.
- Inheritance: a class reuses and extends another class.
- Polymorphism: different classes answer the same method call in their own way.
- Compilation is not an OOP concept.
"""


"""Q2 - Relationship between a class and an object?
Correct answer: "A class is a blueprint; an object is a specific instance created from it."

The class defines BOTH the data (attributes) and the behaviour (methods).
Each object is a concrete instance with its own attribute values.
"""
class Asset:                      # the blueprint
    def __init__(self, ticker):
        self.ticker = ticker

a = Asset("AAPL")                 # two instances of the same blueprint
b = Asset("MSFT")
print(type(a).__name__, a.ticker, b.ticker)


"""Q3 - When is __init__ executed?
Correct answer: "Automatically, each time a new instance is created with ClassName(...)."

ClassName(...) creates the object, then Python calls __init__ on it to
initialise its attributes. It does not run when the class statement is read.
"""
class Asset:
    def __init__(self):
        print("__init__ called")

print("class defined, nothing printed yet")
obj_1 = Asset()                           # __init__ runs here
obje_2 = Asset()                           # and again here


"""Q4 - What does this code print?

Correct answer: "Ticker Symbol: MSFT"
`self` is the instance itself, passed implicitly by Python:
a.display_ticker() is equivalent to FinancialAsset.display_ticker(a).
"""
class FinancialAsset:
    def __init__(self, ticker):
        self.ticker = ticker

    def display_ticker(self):
        print(f'Ticker Symbol: {self.ticker}')

a = FinancialAsset('MSFT')
a.display_ticker()


# =============================================================================
# 2. PEP 8 NAMING CONVENTIONS
# =============================================================================


"""Q5 - Select every line that follows PEP 8 naming conventions.
Correct answers:
  RISK_FREE_RATE = 0.0365   (module-level constant)  -> UPPER_SNAKE_CASE
  def calculate_ytm(self):                           -> lower_snake_case
  
Wrong:
  def computeVolatility(prices):   camelCase is not PEP 8 for functions.
  self.MaturityDate = ...          CapWords is reserved for classes;  attributes use lower_snake_case.

"""


"""Q6 - Correct PEP 8 name for a Black-Scholes pricer class?
Correct answer: BlackScholesPricer
Classes use CapWords (PascalCase): no underscores, each word capitalised.
"""

class BlackScholesPricer:
    pass


# =============================================================================
# 3. ENCAPSULATION AND NAME MANGLING
# =============================================================================

"""Q7 - What happens when this code runs?

Correct answer: it prints 500.

Inside the class body of Account, `self.__balance` is renamed by Python to `self._Account__balance` (name mangling). 
get_balance is also defined in Account, so it uses the same mangled name and finds the attribute.
SavingsAccount inherits __init__ and get_balance, so it works.
"""
class Account:
    def __init__(self, balance):
        self.__balance = balance

    def get_balance(self):
        return self.__balance

class SavingsAccount(Account):
    pass

acct = SavingsAccount(500)
print(acct.get_balance())
print(acct.__dict__)              # shows the real name: _Account__balance



"""Q8 - Which expressions run WITHOUT error outside the class?

Correct answers:
  acc.owner                               public attribute
  acc._balance                            single underscore = convention only
  acc._BankAccount__transaction_history   the mangled name works
  acc.add_transaction("x")                public method, may use the private list

Fails:
  acc.__transaction_history               the real name is mangled, so AttributeError.

Python has no real private attributes: mangling prevents accidents, not deliberate access.
"""
class BankAccount:
    def __init__(self, owner, initial_balance):
        self.owner = owner
        self._balance = initial_balance
        self.__transaction_history = []

    def add_transaction(self, transaction):
        self.__transaction_history.append(transaction)

acc = BankAccount("Someone", 1000)

print(acc.owner)
print(acc._balance)
try:
    print(acc.__transaction_history)
except AttributeError as e:
    print("AttributeError:", e)
print(acc._BankAccount__transaction_history)
acc.add_transaction("x")
print(acc._BankAccount__transaction_history)


# =============================================================================
# 4. OPERATOR OVERLOADING (__add__, __sub__)
# =============================================================================


"""Shared definitions for Q9, Q10 and Q11 (identical to the MCQ)."""
class FinancialInstrument:
    def __init__(self, symbol, price, currency):
        self.ticker = symbol
        self.price = price
        self.currency = currency

class BankAccount:
    def __init__(self, name, balance, currency):
        self.name = name
        self.balance = balance
        self.currency = currency

    def __add__(self, other):
        if isinstance(other, BankAccount) and other.currency == self.currency:
            self.balance = self.balance + other.balance
            return self.balance

        if isinstance(other, FinancialInstrument) and other.currency == self.currency:
            self.balance = self.balance + other.price
            return self.balance

    def __sub__(self, other):
        if isinstance(other, BankAccount) and other.currency == self.currency:
            self.balance = self.balance - other.balance
            return self.balance

        if isinstance(other, FinancialInstrument) and other.currency == self.currency:
            self.balance = self.balance - other.price
            return self.balance



"""Q9 - What is printed? """
acc1 = BankAccount('Account 1', 1200, 'USD')
acc2 = BankAccount('Account 2', 800, 'USD')
x = acc1 + acc2
y = acc1 - acc2
print(x, y, acc1.balance)

"""
Correct answer: 2000 1200 1200

- acc1 + acc2: 1200 + 800 = 2000, and acc1.balance is now 2000 (mutation).
- acc1 - acc2: 2000 - 800 = 1200 (NOT 400, because acc1 already changed).
- acc1.balance ends at 1200.
"""


"""Q10 - What is printed by acc1 + acc3?"""
acc1 = BankAccount('Account 1', 1200, 'USD')
acc3 = BankAccount('Account 3', 500, 'EUR')
print(acc1 + acc3)

"""
Correct answer: None

Currencies differ (USD vs EUR), so neither `if` is true. A function that reaches its end without a `return` returns None.
"""

"""Q11 - What is printed?"""

acc = BankAccount('Main', 1000, 'USD')
bond = FinancialInstrument('T 5 15/09/2045', 300, 'USD')
print(acc - bond)
print(acc + bond)

"""
Correct answer: 700 then 1000
The balance is mutated at each step:
1000 - 300 = 700, then 700 + 300 = 1000.
A BankAccount can be combined with a FinancialInstrument (uses its price).
"""



# =============================================================================
# 5. EQUALITY, HASHING AND STRING REPRESENTATION
# =============================================================================


"""Q12- No __eq__ is defined. What is printed?

Correct answer: False True

Without __eq__, == falls back to eq object implementation.
Python’s default behavior is to treat two objects as equal only if they are the same object (store at the same place 
in the memory), not if they hold the same data.
a and b are two distinct objects with the same content -> False.
a == a is the same object -> True.
"""
class Asset:
    def __init__(self, ticker):
        self.ticker = ticker

a = Asset('AAPL')
b = Asset('AAPL')
print(a == b, a == a)


"""Q13 - What does this code print?

Correct answer: 2

A set uses __hash__ to find the bucket and __eq__ to detect duplicates.
The two 'AAPL' objects have the same hash and compare equal, so only one is
kept. Remaining: AAPL and MSFT.
Rule: if you define __eq__, define a consistent __hash__ too.
"""
class FinancialAsset:
    def __init__(self, ticker):
        self.ticker = ticker

    def __eq__(self, other):
        if isinstance(other, FinancialAsset):
            return self.ticker == other.ticker
        return False

    def __hash__(self):
        return hash(self.ticker)

assets = {
    FinancialAsset('AAPL'),
    FinancialAsset('AAPL'),
    FinancialAsset('MSFT'),
}
print(len(assets))


"""Q14 - What do the three print statements output?

Correct answer: AAPL @ 178 / Px('AAPL', 178) / AAPL @ 178

- print(x) and f"{x}" use __str__ (readable output for users).
- repr(x) uses __repr__ (unambiguous output for developers).
- The default __format__ falls back to str(), hence the f-string result.
"""
class Px:
    def __init__(self, t, p):
        self.t, self.p = t, p

    def __str__(self):
        return f"{self.t} @ {self.p}"

    def __repr__(self):
        return f"Px('{self.t}', {self.p})"

x = Px('AAPL', 178)
print(x)
print(repr(x))
print(f"{x}")


# =============================================================================
# 6. INHERITANCE
# =============================================================================

"""Q15 - What does this code print?

Correct answer: True False

Inheritance is an "is-a" relationship that goes one way:
a Bond IS a FinancialAsset, but a plain FinancialAsset is not a Bond.
"""
class FinancialAsset:
    def __init__(self, symbol, price):
        self.symbol = symbol
        self.price = price

class Bond(FinancialAsset):
    def __init__(self, symbol, price, face_value, maturity_date):
        super().__init__(symbol, price)
        self.face_value = face_value
        self.maturity_date = maturity_date

asset = FinancialAsset("USD", 1.0)
bond = Bond('T 5 15/09/2045', 100, 100_000_000, '2045-09-15')
print(isinstance(bond, FinancialAsset), isinstance(asset, Bond))



"""Q16 - Given the classes below, what happens?

Correct answer: the first line prints a number; the second raises AttributeError: 'Call' object has no 
attribute 'rho_per_1pct'.

- vega() is defined in Option, so Call inherits it.
- rho() and rho_per_1pct() exist only in Put. Call and Put are siblings,
  so Call cannot see them. The error is raised when the attribute is looked
  up, before the call parentheses matter.
"""
class Option:
    def __init__(self, s, k, r, ttm, sigma):
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

class Put(Option):
    def price(self):
        d1, d2 = self.d1(), self.d2()
        return self.K * math.exp(-self.r * self.T) * NormalDist().cdf(-d2) - self.S * NormalDist().cdf(-d1)

    def rho(self):
        return -self.T * self.K * math.exp(-self.r * self.T) * NormalDist().cdf(-self.d2())

    def rho_per_1pct(self):
        return 0.01 * self.rho()

call = Call(s=200, k=250, r=0.0365, ttm=1.0, sigma=0.15)
print(round(call.vega(), 4))
try:
    print(call.rho_per_1pct())
except AttributeError as e:
    print("AttributeError:", e)


"""Q17 - What happens when this code runs?

Correct answer: AttributeError: 'Equity' object has no attribute 'price'

Equity.__init__ OVERRIDES the parent's __init__ and never calls super().__init__(...), so self.ticker and self.price 
are never set.
Creating the object works; pe() fails when it reads self.price.
Fix: call super().__init__(ticker, price) inside Equity.__init__.
"""
class FinancialAsset:
    def __init__(self, ticker, price):
        self.ticker = ticker
        self.price = price

class Equity(FinancialAsset):
    def __init__(self, ticker, price, eps):
        self.eps = eps

    def pe(self):
        return self.price / self.eps

try:
    print(Equity('AAPL', 230, 6.1).pe())
except AttributeError as e:
    print("AttributeError:", e)


# =============================================================================
# 7. MULTIPLE INHERITANCE AND THE MRO
# =============================================================================


"""Q18 - What does this code print?

Correct answer: Method in BaseClass1

Python searches the Method Resolution Order (MRO) from left to right:
[DerivedClass, BaseClass1, BaseClass2, object]. The first match wins.
"""
class BaseClass1:
    def method(self):
        print("Method in BaseClass1")

class BaseClass2:
    def method(self):
        print("Method in BaseClass2")

class DerivedClass(BaseClass1, BaseClass2):
    pass

DerivedClass().method()
print([c.__name__ for c in DerivedClass.__mro__])


"""Q19 - Each method prints BEFORE calling super(). Output?

Correct answer: D B C A

The MRO of D is D -> B -> C -> A. super() means "the NEXT class in the MRO", not "the parent". 
So B's super() goes to C (not A), and A is called only once (the "diamond" problem solved by C3 linearization).
Each class prints, then delegates: D B C A.
"""
class A:
    def method(self):
        print("A")

class B(A):
    def method(self):
        print("B")
        super().method()

class C(A):
    def method(self):
        print("C")
        super().method()

class D(B, C):
    def method(self):
        print("D")
        super().method()

D().method()
print([c.__name__ for c in D.__mro__])



"""Q20 - Each method calls super() BEFORE printing. Output?
Correct answer: A C B D
Same call chain as Q19 (D -> B -> C -> A), but each class prints AFTER the
delegated call returns. The deepest class prints first, and the output
unwinds in reverse MRO order: A, C, B, D.
"""
class A:
    def method(self):
        print("A")

class B(A):
    def method(self):
        super().method()
        print("B")

class C(A):
    def method(self):
        super().method()
        print("C")

class D(B, C):
    def method(self):
        super().method()
        print("D")

D().method()

