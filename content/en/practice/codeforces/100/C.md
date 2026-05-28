---
title: "CF 100C - A+B"
description: "The task looks trivial at first glance: read two integers and print their sum. The catch is hidden inside the constraints. Each number can contain up to 500 decimal digits, far larger than the range of standard 32-bit or 64-bit integers in many languages."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 100
codeforces_index: "C"
codeforces_contest_name: "Unknown Language Round 3"
rating: 1400
weight: 100
solve_time_s: 87
verified: true
draft: false
---

[CF 100C - A+B](https://codeforces.com/problemset/problem/100/C)

**Rating:** 1400  
**Tags:** *special, implementation  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

The task looks trivial at first glance: read two integers and print their sum. The catch is hidden inside the constraints. Each number can contain up to 500 decimal digits, far larger than the range of standard 32-bit or 64-bit integers in many languages.

We are given two positive integers, each written on its own line without leading zeros. We must output their exact decimal sum, also without leading zeros.

The important constraint is the size of the numbers. A value with 500 digits cannot fit into normal integer types like `int` or `long long` in C++. A direct numeric addition using fixed-size arithmetic would overflow immediately.

The time limit is extremely generous for such small input sizes. Even an algorithm that processes digits one by one is tiny in practice. Since each number has at most 500 digits, an `O(n)` solution where `n` is the number of digits is more than enough.

The main edge cases come from carry propagation.

Consider this input:

```
999
1
```

The correct output is:

```
1000
```

A careless digit-by-digit implementation might forget to append the final carry after processing all positions.

Another subtle case is different lengths:

```
12345
9
```

The correct output is:

```
12354
```

If the shorter number is not padded correctly, indices may go out of bounds or digits may become misaligned.

There is also the smallest possible input:

```
1
1
```

The correct output is:

```
2
```

This checks that the implementation works when there is only a single digit and no complicated carry logic.

In Python, built-in integers already support arbitrary precision, so the whole problem reduces to reading the numbers and printing their sum. Still, understanding why this matters is the core idea of the problem.

## Approaches

The brute-force approach is manual big integer addition. We can store both numbers as strings, process them from right to left, add corresponding digits, keep track of carry, and build the result digit by digit.

This works because decimal addition is local. Each position depends only on the two current digits and the carry from the previous position. Since each number has at most 500 digits, the total number of operations is only a few hundred additions and modulo operations.

The brute-force method is already fast enough. Its complexity is linear in the number of digits, which is tiny here.

The more convenient approach in Python is to rely on Python's arbitrary-precision integers. Python integers automatically expand to hold very large values, so we can directly convert the strings to integers, add them, and print the result.

The manual method exists because many programming languages cannot represent 500-digit numbers natively. Python removes that limitation, which turns the problem into a one-line arithmetic operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Manual digit-by-digit addition | O(n) | O(n) | Accepted |
| Python arbitrary-precision integers | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the first integer as a string from input.
2. Read the second integer as a string from input.
3. Convert both strings into Python integers. Python automatically handles arbitrarily large numbers, so no custom big integer logic is needed.
4. Add the two integers.
5. Print the resulting sum.

Why it works:

Python integers are implemented with arbitrary precision arithmetic internally. Instead of storing values in fixed-size machine words, Python dynamically allocates enough memory to represent very large integers. Because of this, adding two 500-digit numbers produces the mathematically correct result without overflow.

## Python Solution

```python
import sys
input = sys.stdin.readline

a = int(input().strip())
b = int(input().strip())

print(a + b)
```

The program starts by using fast input through `sys.stdin.readline`, which is standard in competitive programming.

The `strip()` calls remove trailing newline characters. Without them, `int()` would still work in Python, but using `strip()` keeps the parsing explicit and clean.

The critical detail is the use of Python's built-in `int` type. Unlike fixed-width integer types in many languages, Python integers automatically grow as needed. This avoids overflow completely, even for 500-digit numbers.

The final `print(a + b)` directly outputs the exact decimal representation of the sum. Python automatically formats the integer without leading zeros.

## Worked Examples

### Example 1

Input:

```
2
3
```

Step trace:

| Step | a | b | Sum |
| --- | --- | --- | --- |
| Read input | 2 | 3 | - |
| Add numbers | 2 | 3 | 5 |
| Output | 2 | 3 | 5 |

This demonstrates the simplest possible case, a single-digit addition without carry propagation.

### Example 2

Input:

```
999
1
```

Step trace:

| Step | a | b | Sum |
| --- | --- | --- | --- |
| Read input | 999 | 1 | - |
| Add numbers | 999 | 1 | 1000 |
| Output | 999 | 1 | 1000 |

This example demonstrates carry propagation across multiple digits. A manual implementation must correctly handle the final carry that creates a new leading digit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Python processes all digits of the numbers during addition |
| Space | O(n) | The integers and result require storage proportional to digit count |

Here, `n` is the number of digits in the larger number. Since the maximum size is only 500 digits, the runtime and memory usage are negligible compared to the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    a = int(input().strip())
    b = int(input().strip())

    print(a + b)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("2\n3\n") == "5\n", "sample 1"

# minimum values
assert run("1\n1\n") == "2\n", "minimum values"

# carry propagation
assert run("999\n1\n") == "1000\n", "final carry"

# different lengths
assert run("12345\n9\n") == "12354\n", "different digit counts"

# very large numbers
assert run(
    "999999999999999999999999999999\n"
    "1\n"
) == "1000000000000000000000000000000\n", "large integer handling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `2` | Smallest valid input |
| `999 1` | `1000` | Carry propagation across all digits |
| `12345 9` | `12354` | Different number lengths |
| Large 30-digit value plus 1 | Large 31-digit result | Arbitrary-precision arithmetic |

## Edge Cases

Consider the input:

```
999
1
```

The algorithm converts both values into Python integers and computes:

```
999 + 1 = 1000
```

The output becomes:

```
1000
```

This case confirms that carry propagation across every digit is handled correctly. A manual implementation might forget the extra leading carry, but Python's integer arithmetic handles it automatically.

Now consider numbers of different lengths:

```
12345
9
```

The addition becomes:

```
12345 + 9 = 12354
```

The output is:

```
12354
```

This verifies that alignment issues do not exist when using arbitrary-precision integers. Python internally manages the digit positions correctly.

Finally, consider the smallest valid input:

```
1
1
```

The program computes:

```
1 + 1 = 2
```

and prints:

```
2
```

This confirms the implementation works even at the lower boundary of the constraints.
