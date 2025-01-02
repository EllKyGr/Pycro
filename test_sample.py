"""This is a sample code to test regex statements from python3.yaml syntax file
   for Micro text editor, and customize colorschemes suited for the user.
   Currently using an extended version or darcula.micro renamed pyrcula.micro"""
import time
from sys import exit as ex
from typing import Any
from collections.abc import Callable

# Variable assignment
SLOT = 5
a_word = "Hi"

# Multi-assignment
one, two, three = [1, 2, 3]

# Type Hint
link: str = "https://google.com"
five: int = 5
n_list: list[int] = [4, 5, 6]
piece: list[int] = n_list[:2]
ant: tuple = tuple(n_list)
empty_dict: dict[int, str] = {}

# f-string
greeting: str = input("Enter your name: ")
print(f"Hello, {greeting}!")  # NOTE: It will highlight even if no 'f' present

# Variable and literal comparison
True is False
False is not None
"True" != None
False is "Right"
one = three
one == two
one != two
one > two
one < two
one >= two
one <= two

# Arithmetic
first_n = int = 5
second_n = int = 10
first_n + second_n
first_n += 2
second_n -= 3
MULTI = first_n * second_n
DIV = second_n / first_n

# Data Structures NOTE: As of December 30th 2024 any DT with variables won't change
# to the expected color scheme within the presence of strings (or quotes for that matter)
# floats and integers work as expected
alpha: list[Any] = ["a", "b", "c", "d", ant, five, n_list, empty_dict]
a_list: list = [five, empty_dict, ant, 5.5, 4_505.8]
# After ':' treats the expression as type instead of var
numbers = {1: five, 2: empty_dict, 3: ant}
a_set = {1, DIV, 2, 4, 5.5}
# String presence changes to default the color for variables
a_tuple = (1, alpha, a_list, 2.5, "string")

# Flow control
for idx, value in enumerate(alpha):
    print(idx, value, flush=True)
    time.sleep(1)

numbers = {1: 4, 2: 5, 3: 6}

for number, content in numbers.items():
    print(f"Entry: {number}\tValue: {content}")

while two < 10:
    print(two)
    two += 1

five = 5
ten = 10

if five >= ten or ten < 20:
    print(five * ten)


# Class creation
class Cat:
    """Dummy text"""

    def __init__(self, name: str, race: str, age: int = 8) -> None:
        """Dummy text"""
        self.name = name
        self.race = race

    @property
    def output_name(self) -> str:
        """Dummy text"""
        print(f"{self.name} is the cat name!")

        return self.name

    def cats_race(self) -> str:
        """Dummy text"""
        print(f"{self.name} is a {self.race}!")
        return self.race


bubbles: Cat = Cat("Bubbles", "Mixed")
print(f"Say hello to {bubbles.name}!", end=" ")
bubbles.output_name()
bubbles.cats_race()

with open("test.py", "r") as file:
    data: list = file.readlines()
    lines: int = len(content)
    print(f"Total number of lines is {lines}")
