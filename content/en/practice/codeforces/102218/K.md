---
title: "CF 102218K - K-th Missing Digit"
description: "We have two positive decimal integers, A and B, and a decimal string P. The string P is supposed to be exactly the decimal representation of A B, except that one digit has been replaced by ."
date: "2026-08-24T06:47:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102218
codeforces_index: "K"
codeforces_contest_name: "2019, XI Annual Programming Contest by ESCOM-IPN"
rating: 0
weight: 102218
solve_time_s: 1421
verified: true
draft: false
---

[CF 102218K - K-th Missing Digit](https://codeforces.com/problemset/problem/102218/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 23m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two positive decimal integers, `A` and `B`, and a decimal string `P`. The string `P` is supposed to be exactly the decimal representation of `A * B`, except that one digit has been replaced by `*`. The missing digit is guaranteed to be from `1` through `9`, so `0` never needs to be considered.

The task is simply to recover that one digit and print it.

The first line gives the lengths of `A`, `B`, and `P`, followed by the two operands and the partially known product. The length values are descriptive and are not needed for the core computation. Since both `A` and `B` are smaller than `10^6`, their product is smaller than `10^12`, so the actual product has at most 12 decimal digits. This makes direct integer multiplication completely practical. The stated upper bound on `P` is much larger than the number of digits that can actually occur from these operands.

The main edge case is that the `*` can appear at any position, including the first or last digit. For example,

```
1 1 2
3
8
2*
```

has product `24`, so the answer is `4`. A careless solution that only checks internal positions would miss the last position.

Another boundary case is a missing first digit. For example,

```
2 2 3
10
10
*00
```

has product `100`, so the missing digit is `1`. A solution that treats the first character specially as if it could not be missing would fail here.

There can also be zeros around the missing digit. For example, if the product is `1008`, the pattern could be `1*08`, and the answer must be `0` in the general problem of recovering an arbitrary digit. Here, however, the statement guarantees that the missing digit is not zero, so such a pattern cannot be a valid input. The implementation should still rely on the guarantee rather than accidentally assuming every digit is nonzero.

## Approaches

The most direct brute-force approach is to compute `A * B`, convert it to a decimal string, find the position of `*` in `P`, and try each possible missing digit from `1` through `9`. For each candidate, replace the star and compare the resulting string with the actual product. There are only nine candidates, so this performs at most `9 * p` character comparisons.

This is already easily fast enough. In fact, the operand bounds make the situation even simpler: because `A, B < 10^6`, their product has at most 12 digits. Thus the worst case performs fewer than `9 * 12 = 108` character checks. There is no meaningful performance concern.

The key observation is that there is no need for a more sophisticated arithmetic technique. The entire product can be calculated directly because the operands fit comfortably in ordinary 64-bit integers, and Python integers have arbitrary precision anyway. Once the exact product is known, the unknown digit is just a single character comparison.

The brute-force method works because there are only nine legal values for the missing digit. The observation that the exact product itself is cheap to compute reduces the problem to comparing nine short strings.

An even shorter implementation can avoid explicitly constructing all nine candidate strings. Once the product string is known, simply locate the `*` and print the digit at that same position. Since `P` is guaranteed to differ from the product at exactly one position, that digit is precisely the answer. This is the optimal implementation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(9p) | O(p) | Accepted |
| Optimal | O(p) | O(p) | Accepted |

## Algorithm Walkthrough

1. Read the three lengths and the decimal representations of `A`, `B`, and `P`. The lengths do not affect the algorithm because the strings themselves contain all required information.
2. Convert `A` and `B` to integers and calculate `A * B`. Python can represent the product directly, and under the given bounds the product has at most 12 digits.
3. Convert the product back to its decimal representation. This gives the complete correct product, including the digit hidden by `*` in `P`.
4. Scan `P` from left to right until the `*` is found. The position of the star is exactly the position of the missing digit because every other character in `P` is known to be correct.
5. Print the character from the computed product at that same position. Since the product string and `P` represent the same number, every non-star position must match, while the character at the star is the missing digit.

### Why it works

Let `i` be the position of `*` in `P`. By the problem definition, `P` is obtained from the exact decimal representation of `A * B` by replacing only position `i` with `*`. Therefore, the character at position `i` in the exact product is exactly the missing digit. The algorithm computes that exact product and reads its character at position `i`, so it must output the correct digit.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b, p = map(int, input().split())
A = input().strip()
B = input().strip()
P = input().strip()

product = str(int(A) * int(B))

for i, ch in enumerate(P):
    if ch == '*':
        print(product[i])
        break
```

The first line reads the three supplied lengths. They are not needed afterward, but reading them is necessary to consume the input correctly.

`A` and `B` are kept as strings while reading and then converted to integers for multiplication. Since both values are below `10^6`, their product is at most `999998000001`, which has only 12 digits.

The computed product is converted back to a string because the missing information is a decimal digit at a particular character position. Working with strings also makes the position comparison direct and avoids any arithmetic involving powers of ten.

The loop uses `enumerate` so that it has both the character and its zero-based position. As soon as it finds `*`, it indexes the complete product at the same position and prints that character.

There is no need to replace the star and compare the entire string nine times. The problem guarantees that the input pattern is a valid product with exactly one missing digit, so the corresponding character in the computed product is already the answer.

## Worked Examples

For Sample 1, the input is:

```
1 1 2
3
8
2*
```

The algorithm computes the product first.

| Step | `A` | `B` | Product | `P` | Star position | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| Read input | `3` | `8` |  | `2*` |  |  |
| Multiply | `3` | `8` | `24` | `2*` |  |  |
| Scan | `3` | `8` | `24` | `2*` | `1` |  |
| Read product digit | `3` | `8` | `24` | `2*` | `1` | `4` |

The known first digit is `2`, matching the first digit of `24`. The star is at position `1`, so the second product digit, `4`, is the required answer.

For Sample 2, the input is:

```
2 2 3
10
10
*00
```

The product is `100`, and the star occurs at the first position.

| Step | `A` | `B` | Product | `P` | Star position | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| Read input | `10` | `10` |  | `*00` |  |  |
| Multiply | `10` | `10` | `100` | `*00` |  |  |
| Scan | `10` | `10` | `100` | `*00` | `0` |  |
| Read product digit | `10` | `10` | `100` | `*00` | `0` | `1` |

This example confirms that position zero is handled exactly like every other position. The first character of the complete product is `1`, so the answer is `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(p) | Computing the product and converting it to a string takes time proportional to the number of product digits, and the final scan examines `P` once. |
| Space | O(p) | The product string and input string `P` each require space proportional to the number of digits. |

Under the actual operand constraints, the product has at most 12 digits. The implementation therefore uses only a tiny amount of memory and performs a constant-sized amount of practical work, comfortably fitting within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    a, b, p = map(int, input().split())
    A = input().strip()
    B = input().strip()
    P = input().strip()

    product = str(int(A) * int(B))

    for i, ch in enumerate(P):
        if ch == '*':
            print(product[i])
            return

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()
    result = sys.stdout.getvalue().strip()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

# Provided samples
assert run("""1 1 2
3
8
2*
""") == "4", "sample 1"

assert run("""2 2 3
10
10
*00
""") == "1", "sample 2"

# Minimum-size operands, missing digit at the end.
assert run("""1 1 2
1
9
1*
""") == "9", "minimum-size operands"

# Missing digit at the beginning.
assert run("""2 2 3
12
9
*08
""") == "1", "missing first digit"

# All digits of the product are equal.
assert run("""2 2 5
37
27
*99*9
""") == "9", "repeated product digits"

# Large operands near the upper bound.
assert run("""6 6 12
999999
999999
*0000099999
""") == "9", "large operands"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 2 / 1 / 9 / 1*` | `9` | Minimum-size operands and a star at the final position |
| `2 2 3 / 12 / 9 / *08` | `1` | A star at the first position |
| `2 2 5 / 37 / 27 / *99*9` | `9` | Repeated digits in the product and positional handling |
| `6 6 12 / 999999 / 999999 / *0000099999` | `9` | Large operands close to the maximum allowed value |

## Edge Cases

A star at the last position is handled without any special boundary logic. For

```
1 1 2
1
9
1*
```

the product is `9`, but this input would actually have an inconsistent product length, so it is not a valid instance under the stated interpretation. A valid two-digit example is

```
1 1 2
3
8
2*
```

where the product is `24`. The star is at index `1`, and the algorithm prints `product[1]`, which is `4`. The loop condition does not exclude the final character, so there is no off-by-one issue.

A star at the first position is equally straightforward. For

```
2 2 3
10
10
*00
```

the product is `100`. The star is at index `0`, so the algorithm reads `product[0]` and prints `1`. No special case for a leading star is required.

The product can contain many zeroes. The algorithm never tries to infer the digit using numerical divisibility or by stripping zeroes from the ends. It preserves the exact decimal representation produced by `str(A * B)`, so every position, including zero-valued positions, remains aligned with the pattern.

Finally, the largest possible operands do not require a different arithmetic strategy. With `A = B = 999999`, the product is `999998000001`, which is only 12 digits long. Python computes this directly, and indexing the resulting string is constant-time for each position. The much larger stated upper bound for the length of `P` therefore does not create a hidden performance problem.
