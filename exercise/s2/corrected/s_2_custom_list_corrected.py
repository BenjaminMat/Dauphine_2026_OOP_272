import unittest

"""
**Instructions:**
    Your task is to create a `List` class that simulates the basic functionalities of a list in Python.
    This implementation will help you understand how Python lists can contain elements of different types.

    Implement the `List` class with the following methods:
    - `__init__(self)`: The constructor that initializes an empty dictionary and a counter set to 0.
    - `append(self, element)`: Adds an element to the end of the list.
    - `get_index(self, value)`: Returns the index of the first occurrence of the given value.
    - `pop(self, index)`: Removes and returns the element at the specified index.
    - `remove(self, value)`: Removes the first occurrence of the given value.
    

    Your class should have the following attributes:
    - `_elements`: A dictionary containing the elements of the list.
    - `_count`: A counter to keep track of the number of elements.

    Once your implementation is complete, run the provided unit tests.
    Make sure all tests pass. If not, review your implementation.

    **Tips:**
    - Use the `_elements` dictionary to store the elements, with the keys being the indices and the values being the
      elements of the list.
    - Update the `_count` each time you add or remove an element.
    - For `remove` and `get_index`, you will need to iterate through the dictionary to find the value.
    - To delete an element from your dict you can use the following code : del self._elements[index]


**Implementation:**
Complete the `List` class below:
Run the unit tests below to check your implementation:
"""


class List:
    def __init__(self):
        self._elements = {}
        self._count = 0

    def append(self, element):
        self._elements[self._count] = element
        self._count += 1

    def get_index(self, value):
        for index, element in self._elements.items():
            if element == value:
                return index
        return -1

    def pop(self, index):
        if index < 0 or index >= self._count:
            raise IndexError("Out of bond Index")
        element = self._elements[index]

        for i in range(index, self._count - 1):
            self._elements[i] = self._elements[i + 1]

        del self._elements[self._count - 1]
        self._count -= 1

        return element

    def remove(self, value):
        index = self.get_index(value)
        if index == -1:
            return

        for i in range(index, self._count - 1):
            self._elements[i] = self._elements[i + 1]

        del self._elements[self._count - 1]
        self._count -= 1


class Testlist(unittest.TestCase):
    def setUp(self):
        # Set up a new instance of the list class before each test
        self.list = List()

    def test_append(self):
        # Test the append method
        self.list.append(1)
        self.list.append("two")
        self.list.append([3, 4])
        self.assertEqual(self.list._elements, {0: 1, 1: "two", 2: [3, 4]})
        self.assertEqual(self.list._count, 3)

    def test_get_index(self):
        # Test the get_index method
        self.list.append(1)
        self.list.append(2)
        self.list.append(3)
        self.list.append(2)
        self.assertEqual(self.list.get_index(2), 1)
        self.assertEqual(self.list.get_index(4), -1)

    def test_pop(self):
        # Test the pop method
        self.list.append(1)
        self.list.append(2)
        self.list.append(3)
        element = self.list.pop(1)
        self.assertEqual(element, 2)
        self.assertEqual(self.list._elements, {0: 1, 1: 3})
        self.assertEqual(self.list._count, 2)

    def test_remove(self):
        # Test the remove method
        self.list.append(1)
        self.list.append(2)
        self.list.append(1)
        self.list.remove(1)
        self.assertEqual(self.list._elements, {0: 2, 1: 1})
        self.assertEqual(self.list._count, 2)


def run_tests():
    # Run all the tests with verbosity set to 2 for more detailed output
    unittest.main(argv=[''], verbosity=2, exit=False)

if __name__ == '__main__':
    run_tests()