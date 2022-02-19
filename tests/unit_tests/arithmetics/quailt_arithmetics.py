"""Module where equality body tests are created"""

# Quail-test:new
"""
Name: int_equality
Flyable-version: v0.1a1
Description: Test the equality between two integers
"""
# Quail-test:start
15 == 15 # Quail-assert: eq True
10 == 15 # Quail-assert: eq False
0 == 1 # Quail-assert: eq False
1 == -1 # Quail-assert: eq False
# Quail-test:end


# Quail-test:new
"""
Name: addition
Flyable-version: v0.1a1
Description: Test the addition operator
"""
# Quail-test:start
0 + 0  # Quail-assert: eq 0
0 + 1  # Quail-assert: eq 1
1 + 1  # Quail-assert: eq 2
from sys import maxsize

maxsize + 0  # Quail-assert: eq maxsize
0 + maxsize  # Quail-assert: eq maxsize
10000000000000 + 10000000000000   # Quail-assert: eq 20000000000000
# Quail-test:end


# Quail-test:new
"""
Name: subtraction
Flyable-version: v0.1a1
Description: Test the subtraction operator
"""
# Quail-test:start
0 - 0 # Quail-assert: eq 0
0 - 1 # Quail-assert: eq -1
1 - 0 # Quail-assert: eq 1
1 - 1 # Quail-assert: eq 0
1 - -1 # Quail-assert: eq 2
1 - +1 # Quail-assert: eq 0
-1 - -1 # Quail-assert: eq 0
-1 - +1 # Quail-assert: eq -2
+1 - +1 # Quail-assert: eq 0

51004 - 2414423 # Quail-assert: eq -2363419
# Quail-test:end


# Quail-test:new
"""
Name: multiplication
Flyable-version: v0.1a1
Description: Test the multiplication operator
"""
# Quail-test:start

0 * 0 # Quail-assert: eq 0
5 * 0 # Quail-assert: eq 0
1 * -1 # Quail-assert: eq -1
-1 * 1 # Quail-assert: eq -1
-1 * -1 # Quail-assert: eq 1
120 * 32 # Quail-assert: eq 3840
50 * -50 # Quail-assert: eq -2500
-50 * -50 # Quail-assert: eq 2500
# Quail-test:end


# Quail-test:new
"""
Name: division
Flyable-version: v0.1a1
Description: Test the divide operator
"""
# Quail-test:start
0 / 5 # Quail-assert: eq 0.0
1 / 10 # Quail-assert: eq 0.1
1 / 10.0 # Quail-assert: eq 0.1
50 / 50 # Quail-assert: eq 1.0
50.0 / 50 # Quail-assert: eq 1.0
50 / -50 # Quail-assert: eq -1.0
-50 / -50 # Quail-assert: eq 1.0
226 / 25.3 # Quail-assert: eq 8.932806324110672
226 / 25 # Quail-assert: eq 9.04
# Quail-test:end


# Quail-test:new
"""
Name: division_by_zero
Flyable-version: v0.1a1
Description: Test the division by zero
"""
# Quail-test:start
try:
    print(5 / 0)
except ZeroDivisionError:
    print("Division by zero")
try:
    print(0 / 0)
except ZeroDivisionError:
    print("Division by zero")
try:
    print(2 % 0)
except ZeroDivisionError:
    print("Division by zero")
try:
    print(5 // 0)
except ZeroDivisionError:
    print("Division by zero")
# Quail-test:end


# Quail-test:new
"""
Name: modulo
Flyable-version: v0.1a1
Description: Test the modulo operator
"""
# Quail-test:start
print(0 % 2)
print(42 % 2)
print(3 % 2)
print(8 % 6)
print(8 % -6)
print(-8 % 6)
print(-8 % -6)
# Quail-test:end


# Quail-test:new
"""
Name: pow
Flyable-version: v0.1a1
Description: Test the pow operator
"""
# Quail-test:start
print(1 ** 0)
print(16 ** 0)
print(-16 ** 0)
print(2 ** 8)
print(2 ** -8)
print(-2 ** 8)
print(-2 ** -8)
# Quail-test:end


# Quail-test:new
"""
Name: floor_division
Flyable-version: v0.1a1
Description: Test the pow operator
"""
# Quail-test:start
print(0 // 5)
print(1 // 10)
print(1 // 10.0)
print(50 // 50)
print(40.0 // 50)
print(40.0 // 50.0)
print(40 // -50)
print(-40 // -50)
# Quail-test:end
