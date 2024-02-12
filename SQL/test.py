# data = [[1,2,3], [4,5,6]]

# new_data = [i for item in data for i in item ]

# print(new_data)


# import ast

# # Example Python literal
# python_literal = "{'key1': 123, 'key2': [4, 5, 6]}"

# # Example input as a string
# input_string = "[1, 2, 3, [4, 5, 6], 'hello', 'world', " + python_literal + "]"

# # Using ast.literal_eval to evaluate the updated input string as a Python literal
# result = ast.literal_eval(input_string)

# for item in result:
#   print(item, "   ", type(item))
# # Printing the result and its type
# print(result)
# print(type(result))

import re

# Example strings
strings = ["I have 3 apples", "The price is $5.99", "Room 123 is on the 4th floor", "The product code is ABC123XYZ"]

# Applying the substitution to each string
for string in strings:
    result = re.sub(r"\b\d+\b", "", string).strip()
    print(f"Original: {string} => Result: {result}")