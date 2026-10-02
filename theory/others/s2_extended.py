"""
Table of contents :

        ## Encapsulation in Python - Part 2
        ## Inheritance in Python - Part 2
        ## Dunder Methods


## Encapsulation in Python - Part 2

    Encapsulation is one of the fundamental principles of object-oriented programming. It involves bundling data
    (attributes) and the methods that manipulate them into a single unit (the class) and controlling access to this
    data from outside the class.

    **Definition/Concept: Public and Private attributes in Python:**
        Unlike languages like Java or C++, Python does not have a strict mechanism to define attributes or methods
        as "private" or "public." Instead, Python follows a naming convention to indicate the developer's intention
        regarding the usage of attributes and methods.

        *Public Attributes and Methods:**
          Named normally, without an underscore.
          Example: `self.attribute`, `def method(self):`
          These are considered part of the class's public interface.

        *"Private" Attributes and Methods (by convention):**
          Prefixed with a single underscore `_`.
          Example: `self._attribute`, `def _method(self):`
          This indicates that these elements are intended for internal use and should not be accessed directly from
          outside the class. This convention is based on trust; technically, these elements remain accessible.

        *Name Mangling for Attributes and Methods:**
          Prefixed with a double underscore `__` (without an underscore at the end).
          Example: `self.__attribute`, `def __method(self):`
          Python applies "name mangling", i.e. it automatically changes of the attribute / method to include the class
          name making access from outside more difficult but not impossible.

    **Why:**
        Encapsulation helps in controlling access to data, providing flexibility to modify the internal implementation
        without affecting the code that uses the class, preventing accidental modifications to internal data, and
        improving code clarity by distinguishing between the public interface and implementation details.

    **When to use it:**
        Use encapsulation when you want to protect the internal state of an object and ensure that only the intended
        methods or functions can modify it.
        Use public methods (getters/setters) to control access to internal data if needed.
        Follow naming conventions (`_attribute` for internal use, `__attribute` for name mangling) to clearly indicate
        the intended use of attributes and methods.

    **Important Points to Remember:**
        Encapsulation in Python is based on conventions rather than strict restrictions.
        Attributes and methods prefixed with a single underscore `_` are considered internal to the class.
        The double underscore `__` triggers name mangling, making external access more difficult but not impossible.
        Encapsulation is a matter of design and programming discipline in Python.
"""

import datetime as dt

class BankAccount:
    def __init__(self, owner: str, initial_balance: float):
        self.owner = owner  # Public
        self._balance = initial_balance  # "Private" by convention
        self.__transaction_history = []  # "Private" with name mangling

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            self.__add_transaction(f"Deposit of {amount} at {dt.datetime.now()}")
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            self.__add_transaction(f"Withdrawal of {amount} at {dt.datetime.now()}")
            return True
        return False

    def get_balance(self):
        return self._balance

    def __add_transaction(self, transaction):
        self.__transaction_history.append(transaction)


# Usage
account = BankAccount("Someone", 1000)
print(account.owner)  # Access to a public attribute
account.deposit(500)
# The following line are possible but not recommended:
print(account._balance)  # Access to a "private" attribute by convention
# Alternative
print(account.get_balance())  # Using a public method to access the balance

# print(account.__transaction_history)  # This will raise an AttributeError
print(account._BankAccount__transaction_history)  # Access to the attribute with name mangling


"""
## Inheritance in Python - Reminder

    ** Definition/Concept ** 
        Inheritance is a pillar of Object-Oriented Programming (OOP). It allows a class to inherit features 
        (methods and properties) from another class. The class being inherited from is known as the parent class, 
        superclass or base class, and the class that inherits is known as the child class, subclass or derived class.

## Multiple Inheritance in Python

    **Definition/Concept:**
        Python supports multiple inheritance, which means that a class can inherit from multiple parent classes.
        This allows a derived class to combine functionalities from several base classes.

    ** Syntax of Multiple Inheritance:**
        Python uses a straightforward syntax to define multiple inheritance by listing all parent classes
        in the parentheses after the class name.

"""


class BaseClass1:
    def method(self):
        print("Method in BaseClass1")


class BaseClass2:
    def method(self):
        print("Method in BaseClass2")


class DerivedClass(BaseClass1, BaseClass2):
    pass


derived_class = DerivedClass()
derived_class.method()
# Outputs:
# Method in DerivedClass
# Method in BaseClass1
# Method in BaseClass2

"""
    **Practical Benefits of Multiple Inheritance:**
        Combining Functionality:
            Multiple inheritance allows a class to combine functionalities from different classes into one.
        Code Reuse from Multiple Sources:
            Useful when a class needs to inherit behaviors from several unrelated classes.
        Implementing Complex Designs:
            Enables creating more flexible and adaptable class structures.
"""


class BaseClass1Modified:
    def method_from_base_class_1_modified(self):
        print("Method from BaseClass1Modified")


class BaseClass2Modified:
    def method_from_base_class_2_modified(self):
        print("Method from BaseClass2Modified")


class DerivedClassModified(BaseClass1Modified, BaseClass2Modified):
    pass


derived_class_2 = DerivedClassModified()
derived_class_2.method_from_base_class_1_modified()
derived_class_2.method_from_base_class_2_modified()

"""
    **Method Resolution Order (MRO) in Detail**
        The Method Resolution Order (MRO) is crucial for understanding how Python handles inheritance, especially 
        multiple inheritance.
        
        The MRO defines the order in which Python searches for methods and attributes in a class hierarchy.
        
        This is particularly important in multiple inheritance scenarios where multiple parent classes may define 
        the same method.
        
        Python uses the C3 Linearization Algorithm to determine the MRO. This algorithm ensures that:
            - Subclasses appear before their parent classes.
            - The order of parent classes declared is preserved.
            - The MRO is monotonic (a class always appears before its parents).
            
        In practice, To compute MRO for a given class, the following steps are applied:
            1. Start with: [each parent's MRO] + [list of parents declared]
            2. Repeatedly take the FIRST class that:
                - Is a HEAD of some list (first element)
                - Does NOT appear in the TAIL (remaining elements) of ANY list
            3. Remove it from all lists and repeat until empty
        
        Understanding the MRO is crucial to:
            - Avoid name conflicts in multiple inheritance.
            - Understand the order in which methods are executed.
            - Design coherent and predictable class hierarchies.
"""

# Visualizing MRO:
# You can visualize the MRO of a class using the mro() method or the __mro__ attribute:
print(DerivedClass.mro())  # Displays the MRO for class DerivedClass
# output : [<class '__main__.DerivedClass'>, <class '__main__.BaseClass1'>, <class '__main__.BaseClass2'>, <class 'object'>]

# Detailed Example of Method Resolution: Example to illustrate how the MRO works:
class A:
    def method(self):
        print("Method in A")


class B(A):
    def method(self):
        print("Method in B")


class C(A):
    def method(self):
        print("Method in C")


class D(B, C):
    pass


d = D()
print(D.__mro__)
d.method()

"""
# 4. Using super()

# Definition/Concept:
# The super() function is a powerful tool in Python for managing inheritance elegantly and flexibly.

# 4.1 Definition and Utility:

# Purpose of super():
# super() allows calling methods from the parent class in a derived class. It is particularly useful for:
# - Extending the behavior of a parent method without completely rewriting it.
# - Ensuring proper management of multiple inheritance.
"""


# 4.2 Basic Syntax:
class Parent:
    def method(self):
        print("Method in Parent")


class Child(Parent):
    def method(self):
        super().method()  # Calls the method from the parent class
        print("Method in Child")


child = Child()
child.method()


# Outputs:
# Method in Parent
# Method in Child


# In the case of multiple inheritance, super() follows the order defined by the MRO:
class A:
    def method(self):
        print("Method in A")


class B(A):
    def method(self):
        print("Method in B")
        super().method()


class C(A):
    def method(self):
        print("Method in C")
        super().method()


class D(B, C):
    def method(self):
        print("Method in D")
        super().method()


d = D()
d.method()


# Outputs:
# Method in D
# Method in B
# Method in C
# Method in A

# Managing Parent Method Calls in Multiple Inheritance
# Direct Call to a Parent Class Method:  In some cases, you might want to call a specific parent class method directly
# rather than following the MRO:
class A:
    def method(self):
        print("Method in A")


class B:
    def method(self):
        print("Method in B")


class C(A, B):
    def method(self):
        print("Method in C")
        A.method(self)  # Direct call to A's method
        B.method(self)  # Direct call to B's method


c = C()
c.method()
# Outputs:
# Method in C
# Method in A
# Method in B



"""
** Dunder methods**

## 1 - Overall definition
    **Definition/Concept**
        "Dunder" is short for "Double underscore" (__). Dunder methods are a set of predefined methods you can use to 
        enrich your classes in Python. You've already seen these special methods in previous class with the
        `__init__` method

    **Why**
        Dunder methods allow you to emulate the behavior of built-in types. For instance, to get the length of a 
        string you can call `len('string')`. But an empty class definition doesn't support this behavior out of the box.

   **When to use it**
        Use dunder methods when you want to define operator behavior on your custom classes or want to mimic built-in 
        Python behavior.

You can find a list of dunder methods in the additional resources directory 

## 2 - Use built-in functions for classes by implementing dunder methods

    **Definition/Concept**
        The dunder method for specifying the behavior of built-in Python functions like `len` or `str` involves 
        implementing specific, predefined methods within your class using double underscores (__). 
        Such methods include `__len__`, `__str__`, and others, which Python calls when built-in functions of the same 
        name are used on instances of your class. 

    **Why**
        Implementing these dunder methods enables your custom objects to behave similarly to built-in Python objects, 
        thereby making your classes more intuitive and easy to use for other developers. This can also help your 
        objects to adhere to established Python conventions and idioms. For instance, if you define a `__len__` method,
         developers will know they can use the `len()` function on instances of your class.

    **When to use it**
        Utilize dunder methods when:
        - You want your custom objects to have idiomatic behavior similar to built-in Python types (e.g., allowing the
         use of functions like `len()` and `str()` on your objects).
        - You are creating a class where the logical implementation of such methods makes sense. For example, if your 
        class represents a collection of objects, implementing `__len__` would be intuitive.
        - You want to create objects that can be used interchangeably with built-in types or that can take advantage 
        of Python's rich set of built-in functions.

    **How to implement it**
        - Define methods in your class with names matching the dunder methods, ensuring they accept the correct 
        parameters and return values that adhere to Python’s data model.
        - By defining these methods, you allow instances of your class to be used with `len(instance)` and `
        str(instance)`, providing behavior similar to built-in Python objects.
        - Always refer to the Python data model documentation to understand the expected behavior and return values 
        of these methods to ensure compatibility and idiomatic usage.

By adhering to this approach, you ensure that your custom classes are not only user-friendly but also adhere to the 
principles and conventions that Python developers expect.
"""

"""
Example of dunder method : __len__
    __len__(self) determines the “length” of your object, which allows you to use the len(obj) syntax.
    If we do not implement the dunder method, len(instrument_list) will return the following : Error: object of 
    type 'InstrumentList' has no len()
"""

class FinancialAsset:
    def __init__(self, ticker):
        self.ticker = ticker

    def display_ticker(self):
        print(f'Ticker Symbol: {self.ticker}')

class InstrumentList:
    def __init__(self, list_of_instrument):
        self.instruments: list[FinancialAsset] = list_of_instrument


class InstrumentListWithDunder:
    def __init__(self, list_of_instrument):
        self.instruments: list[FinancialAsset] = list_of_instrument

    def __len__(self):
        return len(self.instruments)


asset1 = FinancialAsset('AAPL')  # create a Financial Asset object
asset2 = FinancialAsset('MSFT')  # create a Financial Asset object

#instrument_list = InstrumentList([asset1, asset2])
instrument_list_0 = InstrumentList([asset1, asset2])
instrument_list_1 = InstrumentListWithDunder([asset1, asset2])
print(len(instrument_list_1))

"""
## 3.2.1 -The __str__() method
    **Definition/Concept**:
        The `__str__()` method in Python is another "dunder" method associated with a class. It is meant to return a 
        string representation of an object which is intended to be informative and easily readable for end-users.

    **Why**:
        - To offer a "user-friendly" string representation of an object that can be used in various contexts like
         printing the object.
        - It is beneficial when you want a simple description of the object rather than an exhaustive or technical one, 
          as given by `__repr__()`.
        - The primary goal of the `__str__()` method is readability over unambiguity. 

    **When to use it**:
        - When you want to provide an intuitive and user-friendly string representation of an object for display 
        purposes, especially in user-facing applications.
        - When you are implementing print statements or logs where the technical details of an object 
        are not necessary.
        - When you call the built-in `str()` function on an object or use format string methods, the `__str__()` 
        method gets invoked. So, it's helpful to define it when you anticipate such use-cases for your custom objects.
"""


class FinancialAssetWithStrDunder:
    def __init__(self, ticker, price, currency):
        self.ticker: str = ticker
        self.price: float = price
        self.currency: str = currency

    def __str__(self):
        return f'The ticker for this asset is {self.ticker} and its price is {self.price} {self.currency}'


asset_str_dunder_example = FinancialAssetWithStrDunder('AAPL', 178, 'USD')
print(str(asset_str_dunder_example))

"""
## 3.2.2 - The __repr__() Method
    **Definition/Concept**:
        The `__repr__()` method in Python is a dunder method associated with a class.  
        It should return a string that looks like a valid Python expression and could be used to recreate an object with 
        the same properties.  Ideally, using `eval(repr(obj))` should produce an object equivalent to `obj`.

    **Why**:
        - To provide an "official" string representation of an object that is useful for debugging and development. 
        - The output of `__repr__()` is intended to be unambiguous and helps developers understand the properties of 
        the object.
        - While both `__str__()` and `__repr__()` methods in a class provide string representations, the former is for 
        end-users and should be readable, while the latter is primarily for developers and debugging.

    **When to use it**:
        - When you want to provide a detailed and unambiguous string representation of an object for debugging and
         logging.
        - When you want to ensure that there's a clear way to recreate the object from its string representation.

    Benefits of __repr__() when implementing complex Python framework:
        Traceability: In complex financial simulations or optimizations, you might be dealing with hundreds of 
                    instrument objects. If something goes wrong, having a clear __repr__() output can help you trace 
                    back to the exact instrument causing the issue.

        Reproducibility: Sometimes you may need to send the state of your system (the exact instruments and their 
                    properties) to someone else for verification, testing, or audit purposes. With a clear __repr__() 
                    method, you can recreate the exact state of objects with ease.

        Logging: When logging system activities, having a clear representation of the objects being processed can be 
                useful for future reference or debugging.
"""


class FinancialAssetWithDunderRepr:
    def __init__(self, ticker, price, currency):
        self.ticker: str = ticker
        self.price: float = price
        self.currency: str = currency

    def __str__(self):
        return f'The ticker for this asset is {self.ticker} and its price is {self.price} {self.currency}'

    def __repr__(self):
        return f"FinancialAssetWithDunderRepr('{self.ticker}', {str(self.price)}, '{self.currency}')"


asset_str_dunder_example = FinancialAssetWithDunderRepr('AAPL', 178, 'USD')
print(repr(asset_str_dunder_example))

assetExampleEval = eval(repr(asset_str_dunder_example))
# eval() convert an "official" string representation of an object to the object. Here we create a new object.
print(str(asset_str_dunder_example))  # This new object is an instance of FinancialAssetWithDunderRepr

"""
## 3.3 - Operator overloading

    Built-in operator does not work on custom classes. For example, if we try to use "+" or any other operator such as
    "-", "*", "/", ">", ... this will raise a TypeError as the behavior for these operators are not implemented for the
    object. If we want to use built-in operator for custom objects we need to use dunder methods.
    The only exception is the "=" operator. If we don't implement the dunder method to specify the behavior of the
    equal operator for custom objects, python will check for object identity (i.e., both objects are the
    same instance). Thus even though each attributes of 2 objects are equal the "=" will return false

    Implementing dunder methods referring to built-in operator is called operator overloading. 
    **Definition/Concept**: 
        It is the ability of one operation, such as addition or multiplication, to behave in one way or more 
        according to the data or objects being operated upon.

    **Why**: 
        Operator overloading is used to make programming more intuitive and the code more user friendly,
        behaving like they would with built-in types.

    **_When to use `Operator Overloading`_**: 
        Operator overloading is used when you want to specify more than one meaning to an operator or apply specific 
        operation

    You will find below example of operator overloading. 
"""

"""
Example of operator overloading for "+" and "-" operator
Here the operator overloading is realized by implementing the following method : __add__ and __sub__

When we try to add up an object to a BankAccount type object with the "+" operator the __add__ method is called. 
The method checks if the object we try to add up to the first element of the addition is a BankAccount instance. If it's
the case it modify the current balance of the first element and return the updated amount. If it's not the case, 
it will not perform any operation. 

When implementing dunder method for operator overloading, we can specify multiply behavior which will depend on the 
type of the object. If we look at the __sub__ method, the object we try to subtract the first element with could be a 
BankAccount instance or a FinancialInstrument with the same currency than the bank account. If it's the case it modify 
the current balance of the first element and return the updated amount. If it's not the case, it will not perform any 
operation. 
"""

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

        if isinstance(other, FinancialInstrument) and other.ticker == self.currency:
            self.balance = self.balance - other.price
            return self.balance


acc1 = BankAccount('Account 1', 1200, 'USD')
acc2 = BankAccount('Account 2', 800, 'USD')

print(acc1 + acc2)  # 2000
print(acc1 - acc2)
acc1.__sub__(acc2 )# 400

asset = FinancialInstrument('USD', 300, 'USD')
print(acc1 - asset)

"""
Example of the dunder method __eq__()
**Definition/Concept**:  
    The `__eq__()` method in Python is another "dunder" method associated with a class. It is used to define   
    how two objects should be compared for equality. It is invoked when using the `==` operator between two objects.

**Why**:  
    - To define what it means for two instances of a class to be considered equal.  
    - It is beneficial when equality should depend on the values or attributes of objects rather than their   
      identity in memory.  
    - The primary goal of the `__eq__()` method is to provide meaningful value-based equality between objects.  
    - When `__eq__()` is implemented, it is important to consider `__hash__()` as well: if two objects are equal,   
      they must have the same hash value in order to be safely used as keys in dictionaries or as elements of sets.

**When to use it**:  
    - When you want to compare custom objects based on their attributes or values rather than their identity.  
    - When you want expressions such as `object1 == object2` to perform a meaningful comparison for your class.  
    - When objects need to participate correctly in collections such as lists, sets, or dictionaries.  
    - When you implement `__eq__()`, you must consider whether the object should also be hashable and, if so,   
      implement `__hash__()` consistently with `__eq__()`.  
    - If an object is mutable and its equality-relevant attributes can change, it is generally safer not to make   
      it hashable, because changing those attributes after insertion into a set or dictionary can make the object   
      difficult to find or remove.
"""

class FinancialAssetWithNoDunderEq:
    def __init__(self, ticker):
        self.ticker: str = ticker


print('test equality for object with no __eq__() implementation')
asset = FinancialAssetWithNoDunderEq('AAPL')
asset1 = FinancialAssetWithNoDunderEq('AAPL')
print(f'is object with same attributes equal : {asset == asset1}')  # false


class FinancialAssetWithDunderEq:
    def __init__(self, ticker):
        self.ticker: str = ticker

    def __eq__(self, other):
        # First, ensure that the other object is an instance of the same class
        if isinstance(other, FinancialAssetWithDunderEq):
            return self.ticker == other.ticker
        return False

    def __hash__(self):
        return hash(self.ticker)


asset_eq_dunder_example = FinancialAssetWithDunderEq('AAPL')
asset_eq_dunder_example1 = FinancialAssetWithDunderEq('AAPL')
asset_eq_dunder_example2 = FinancialAssetWithDunderEq('MSFT')
print('__eq__() example')
print(f'asset_eq_dunder_example = FinancialAssetWithDunderEq("AAPL") //'
      f' asset_eq_dunder_example1 = FinancialAssetWithDunderEq("AAPL") //'
      f' asset_eq_dunder_example2 = FinancialAssetWithDunderEq("MSFT")')
print(' ')
print(f'asset_eq_dunder_example == "AAPL": {asset_eq_dunder_example == "AAPL"}')  # False
print(
    f'asset_eq_dunder_example == asset_eq_dunder_example1: {asset_eq_dunder_example == asset_eq_dunder_example1}')  # true
print(
    f'asset_eq_dunder_example == asset_eq_dunder_example2 : {asset_eq_dunder_example == asset_eq_dunder_example2}')  # false



"""
## List comprehension

**Definition/Concept**
    List comprehension is a concise way to create lists in Python. It consists of an expression followed by a `for`
    loop inside square brackets `[]` or '{}. This allows you to generate a new list / dict by applying an expression to 
    each item in an existing list (or other iterable).

    Syntax:     [expression for item in iterable if condition] for creating a list
                {expression which generate a dict for item in iterable if condition} for creating a dict

**Why to use it**
1. **Conciseness:** List comprehensions can make your code more compact and easier to read by reducing the number
                    of lines of code.
2. **Readability:** When used appropriately, list comprehensions can make your intention clear, emphasizing the
                    transformation or filtering of data.
3. **Performance:** In some cases, using list comprehension can be faster than equivalent loops due to internal
                    optimizations in Python.

**When to use it**
1. **Simple Transformations:** When you want to apply a simple transformation to each element in a sequence.
                                For instance, squaring each number in a list or converting each string in a list to
                                uppercase.
2. **Filtering:** When you want to select only certain items from an iterable based on some condition.
                  For example, getting only the even numbers from a list.
3. **Flattening:** When dealing with lists of lists or nested iterables and you want to flatten them.
                    For example, flattening a 2D matrix into a 1D list.

4. **Avoid Overcomplication:** While list comprehensions are powerful, they shouldn't be overused.
                                If the logic becomes too complex, it might be clearer to use traditional loops instead
                                to maintain readability.

It's essential to strike a balance. If a list comprehension becomes hard to read or understand, it might be better
to revert to a more traditional for-loop structure.
"""

"""
Example : simple transformation using list comprehension
"""

import math
from datetime import datetime, timedelta

prices = [100.5, 102.3, 98.7, 105.6]

log_returns_with_for_loop = []
for i in range(1, len(prices)):
    log_return = math.log(prices[i] / prices[i - 1])
    log_returns_with_for_loop.append(log_return)

#[expression for item in iterable if condition] for creating a list
log_returns = [math.log(prices[i] / prices[i - 1]) for i in range(1, len(prices))]
print('same output for log_returns: ' + str(log_returns == log_returns_with_for_loop))

"""
Example : filtering  using list comprehension
"""
daily_returns = {datetime.today() - timedelta(days=5): 0.02,
                 datetime.today() - timedelta(days=4): -0.01,
                 datetime.today() - timedelta(days=3): 0.03,
                 datetime.today() - timedelta(days=2): -0.015,
                 datetime.today() - timedelta(days=1): 0.04}

profitable_days_with_for_loop = []
non_profitable_days_with_for_loop = []
for k, v in daily_returns.items():
    if v > 0:
        profitable_days_with_for_loop.append((k, v))
    elif v < 0:
        non_profitable_days_with_for_loop.append((k, v))

    #[expression for item in iterable if condition] for creating a list
profitable_days = [(k, v) for k, v in daily_returns.items() if v > 0]  # filtering example
non_profitable_days = [(k, v) for k, v in daily_returns.items() if v < 0]  # filtering example

print('same output for profitable_days: ' + str(profitable_days == profitable_days_with_for_loop))
print('same output for non_profitable_days: ' + str(non_profitable_days == non_profitable_days_with_for_loop))

"""
Example : flattening using list comprehension
"""

list_of_list = [
    [1, 0.5, 0.3],
    [0.5, 1, 0.4],
    [0.3, 0.4, 1]
]

flat_list_with_for_loop = []
for sublist in list_of_list:
    for item in sublist:
        flat_list_with_for_loop.append(item)

flat_list = [item for sublist in list_of_list for item in sublist]

print('same output for flat_list: ' + str(flat_list == flat_list_with_for_loop))


