"""Module where str body tests are created"""

# Quail-test:new
"""
Name: empty_str_creation
Flyable-version: v0.1a1
Description: Test that the result of "" equals the result of calling str()
"""
# Quail-test:start
litteral_str = ""
litteral_str_by_method = str()
print(litteral_str == litteral_str_by_method)
# print(litteral_str == litteral_str_by_method)
# Quail-test:end


# Quail-test:new
"""
Name: len_str
Flyable-version: v0.1a1
Description: Test that the len function works properly on strings
"""
# Quail-test:start
msg = "hello world!"
print(len(msg))
msg2 = ""
print(len(msg))
print(len(msg2))
# Quail-test:end


# Quail-test:new
"""
Name: concatenation
Flyable-version: v0.1a1
Description: Test the string concatenation functions
"""
# Quail-test:start
world = "World!"
print("Hello " + world + " " + str(42))
print('Hello {} {}'.format(world, 42))
print(f"Hello {world} ")
print("%s %s %s" % ('Hello', world, 22))

from string import Template
new = Template('Hello $world $number')
print(new.substitute(world=world, number=22))

# Quail-test:end


# Quail-test:new
"""
Name: len_str
Flyable-version: v0.1a1
Description: Test that the len function works properly on strings
"""
# Quail-test:start

# Quail-test:end


