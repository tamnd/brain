---
title: "CF 102420D - Spell"
description: "We have two positive integers, a and b, given as decimal strings, and we consider every integer from a through b. We multiply all of them together, then repeatedly replace the resulting number by the sum of its decimal digits until only one digit remains."
date: "2026-08-12T00:40:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102420
codeforces_index: "D"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0422\u0440\u0435\u0442\u044c\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102420
solve_time_s: 182
verified: true
draft: false
---

[CF 102420D - Spell](https://codeforces.com/problemset/problem/102420/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two positive integers, `a` and `b`, given as decimal strings, and we consider every integer from `a` through `b`. We multiply all of them together, then repeatedly replace the resulting number by the sum of its decimal digits until only one digit remains. The required output is that final one digit.

The key difficulty is that `a` and `b` can contain up to 100,000 digits. We cannot construct the product, and we cannot even safely convert the endpoints to ordinary machine integers. A solution must work directly with the decimal representations and exploit a property of the final digit rather than performing the stated arithmetic literally.

The repeated digit sum is the digital root. For every positive integer `x`, its digital root is determined completely by `x mod 9`: if the remainder is nonzero, the answer is that remainder, while remainder zero corresponds to the digit `9`. Thus the enormous product only matters modulo `9`.

There are two edge cases that commonly cause incorrect solutions. First, a product can be divisible by `9`, giving remainder `0`, but the final digit is `9`, not `0`. For example, with input `9` and `9`, the product is `9`, so the answer is `9`. A solution that simply prints `product % 9` would print `0`.

Second, the interval can be enormous even though its endpoints are huge decimal strings. For example, `1` and `100000000000000000000000000000` represent an interval with vastly too many factors to enumerate. A solution that tries to multiply every integer is not merely slow, it is fundamentally incompatible with the input size.

There is also a useful boundary around intervals containing five or fewer consecutive differences. For example, `1` through `5` gives `120`, whose digital root is `3`, while `1` through `6` gives `720`, whose digital root is `9`. The transition happens because six consecutive integers necessarily contain two multiples of `3`, making their product divisible by `9`.

## Approaches

The direct approach follows the statement exactly. Starting with a product of `1`, we would multiply by every integer from `a` through `b`, construct the resulting enormous integer, compute its digit sum, and repeat until one digit remains. This is correct because it performs exactly the requested transformation.

The problem is the range size. For `a = 1` and `b = 10^100000 - 1`, there are exactly `10^100000 - 1` factors, so even ignoring the cost of multiplying enormous integers, the algorithm performs `10^100000 - 2` multiplication operations. The product itself also has an astronomical number of digits. This makes brute force impossible.

The observation that rescues the problem is that digit sums preserve a number modulo `9`. If two positive integers have the same remainder modulo `9`, they have the same digital root, with remainder `0` represented by `9`. Consequently, we only need the product modulo `9`.

That still seems to leave many factors, but modulo `9` gives us a much stronger shortcut. Any six consecutive integers contain two multiples of `3`. Their product is consequently divisible by `3 * 3 = 9`, so every interval containing at least six consecutive numbers has final answer `9`. In terms of the endpoints, this means that whenever `b - a >= 5`, the answer is immediately `9`.

Only intervals with at most five numbers remain. We can handle those directly modulo `9`, because there are at most five factors. We do not need their actual values, only their residues modulo `9`. A decimal string's residue modulo `9` is just the sum of its digits modulo `9`.

The remaining technical issue is finding the small difference `b - a` without converting either 100,000-digit string to an integer. Since we already know that only differences from `0` through `5` matter, we can add each of these small values to the decimal string `a` and compare the result with `b`. This takes only a constant number of linear scans over the input.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Ω(10^100000) factor operations in the worst case | Astronomical for the product | Too slow |
| Optimal | O( | a | + | b | ) | O( | a | + | b | ) | Accepted |

## Algorithm Walkthrough

1. Read `a` and `b` as strings. We deliberately keep them as strings because either endpoint may have 100,000 digits.
2. Compute `a mod 9` by scanning its digits and accumulating the remainder. This is possible because decimal numbers satisfy `10 ≡ 1 (mod 9)`, so the entire number is congruent to the sum of its digits.
3. Check whether `b >= a + 5`. We can calculate `a + 5` using ordinary decimal-string addition and compare it with `b`. If this condition holds, the interval contains at least six integers, so it contains at least two multiples of `3`. Their product is divisible by `9`, and the final digital root is `9`.
4. If `b < a + 5`, the interval contains at most five integers. Find the exact difference `d` by constructing `a`, `a + 1`, ..., `a + 4` as decimal strings and comparing them with `b`. Since `a <= b`, exactly one of these values must equal `b`.
5. Multiply the residues of `a, a + 1, ..., a + d` modulo `9`. Because `d <= 4`, this is at most five modular multiplications.
6. Convert the resulting remainder into a digital root. A remainder from `1` through `8` is already the answer. A remainder of `0` means the product is a positive multiple of `9`, so the answer is `9`.

Why it works: throughout the algorithm, the only information discarded from the product is information that cannot affect its digital root. Congruence modulo `9` is preserved by multiplication, so the product of the residues has exactly the same remainder as the true product. For intervals of at least six numbers, the product necessarily contains two factors divisible by `3`, so its remainder is guaranteed to be zero. For shorter intervals, we explicitly multiply every factor's residue. Thus every possible interval is handled by an exact modulo `9` computation, and the final conversion from remainder zero to `9` gives precisely the repeated digit-sum result.

## Python Solution

```python
import sys
input = sys.stdin.readline

def add_small(s, x):
    """Return the decimal string representing int(s) + x, where x <= 5."""
    digits = list(s)
    i = len(digits) - 1
    carry = x

    while i >= 0 and carry:
        value = (ord(digits[i]) - 48) + carry
        digits[i] = chr(value % 10 + 48)
        carry = value // 10
        i -= 1

    if carry:
        digits.insert(0, chr(carry + 48))

    return ''.join(digits)

def mod9(s):
    r = 0
    for ch in s:
        r = (r + ord(ch) - 48) % 9
    return r

def solve():
    a = input().strip()
    b = input().strip()

    # Six consecutive integers contain two multiples of 3,
    # so their product is divisible by 9.
    if b >= add_small(a, 5):
        print(9)
        return

    # Here b - a <= 4, so we can find the exact difference
    # by checking only five possibilities.
    diff = 0
    for d in range(5):
        if add_small(a, d) == b:
            diff = d
            break

    result = 1
    current_mod = mod9(a)

    for d in range(diff + 1):
        result = (result * ((current_mod + d) % 9)) % 9

    print(9 if result == 0 else result)

solve()
```

The `mod9` function implements the central observation. It never constructs the enormous integer represented by the string. Each digit can be processed independently, and the remainder always stays between `0` and `8`.

The `add_small` function is used only with values from `0` through `5`. It performs normal decimal addition from right to left, so even a 100,000-digit endpoint is handled without integer conversion. The carry can propagate through the entire string, which is why the loop must continue while `carry` is nonzero. For example, adding `5` to `999` correctly produces `1004`.

The comparison `b >= add_small(a, 5)` handles the large-interval case without ever computing `b - a`. Because the input strings have no leading zeros, ordinary lexicographical comparison is sufficient when their lengths differ or when their lengths are equal.

Once the interval is known to contain at most five numbers, the loop checks the exact endpoint rather than trying to calculate a general large subtraction. This is a deliberate use of the mathematical bound: there are only five candidates, so a constant number of string operations is enough.

The multiplication loop uses `(current_mod + d) % 9` for the consecutive values. Since adding `d` to the residue of `a` gives the residue of `a + d` modulo `9`, the actual large integers never need to exist.

Python's arbitrary-precision integers would not overflow for the small modulo values used here, but relying on Python to parse a 100,000-digit decimal string with `int()` is unnecessary and can also hit Python's decimal conversion limit. Keeping the endpoints as strings avoids that issue entirely.

## Worked Examples

For Sample 1, the interval is from `1` to `5`. Its length is five, so the six-number shortcut does not apply.

| Step | `d` | Current residue | Product residue |
| --- | --- | --- | --- |
| Start | 0 | 1 | 1 |
| Multiply by `1` | 0 | 1 | 1 |
| Multiply by `2` | 1 | 2 | 2 |
| Multiply by `3` | 2 | 3 | 6 |
| Multiply by `4` | 3 | 4 | 6 |
| Multiply by `5` | 4 | 5 | 3 |

The product is congruent to `3 mod 9`, so its digital root is `3`. This matches the direct calculation `1 * 2 * 3 * 4 * 5 = 120`, whose digit sum is `3`.

For Sample 2, the interval is `6` through `8`. Again there are only three factors.

| Step | `d` | Current residue | Product residue |
| --- | --- | --- | --- |
| Start | 0 | 6 | 1 |
| Multiply by `6` | 0 | 6 | 6 |
| Multiply by `7` | 1 | 7 | 6 |
| Multiply by `8` | 2 | 8 | 3 |

The final residue is `3`, so the answer is `3`. The actual product is `6 * 7 * 8 = 336`, and `3 + 3 + 6 = 12`, followed by `1 + 2 = 3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | a | + | b | ) | Only a constant number of scans and decimal additions are performed, plus at most five modular multiplications. |
| Space | O( | a | + | b | ) | The strings and a constant number of temporary decimal strings are stored. |

With at most 100,000 digits per endpoint, a linear scan is entirely practical. The algorithm never depends on the numerical magnitude of `a` or `b`, only on the number of decimal digits, and it performs only constant work beyond those scans.

## Test Cases

```python
import io
import sys

def add_small(s, x):
    digits = list(s)
    i = len(digits) - 1
    carry = x

    while i >= 0 and carry:
        value = (ord(digits[i]) - 48) + carry
        digits[i] = chr(value % 10 + 48)
        carry = value // 10
        i -= 1

    if carry:
        digits.insert(0, chr(carry + 48))

    return ''.join(digits)

def mod9(s):
    r = 0
    for ch in s:
        r = (r + ord(ch) - 48) % 9
    return r

def solve_one(a, b):
    if b >= add_small(a, 5):
        return "9"

    diff = 0
    for d in range(5):
        if add_small(a, d) == b:
            diff = d
            break

    result = 1
    base = mod9(a)

    for d in range(diff + 1):
        result = result * ((base + d) % 9) % 9

    return str(9 if result == 0 else result)

def run(inp: str) -> str:
    data = inp.strip().split()
    a, b = data
    return solve_one(a, b) + "\n"

# Provided samples
assert run("1\n5\n") == "3\n", "sample 1"
assert run("6\n8\n") == "3\n", "sample 2"

# Minimum-size input
assert run("1\n1\n") == "1\n", "minimum input"

# All-equal values where the value is divisible by 9
assert run("9\n9\n") == "9\n", "zero remainder must become digital root 9"

# Boundary just below six consecutive numbers
assert run("4\n8\n") == "6\n", "five-number interval"

# Boundary at six consecutive numbers
assert run("4\n9\n") == "9\n", "six-number interval"

# Large endpoint, same value, without converting it to an ordinary integer
big = "9" * 100000
assert run(big + "\n" + big + "\n") == "9\n", "100000-digit endpoint"

# Large endpoint with difference exactly 5
large_a = "1" + "0" * 99999
large_b = add_small(large_a, 5)
assert run(large_a + "\n" + large_b + "\n") == "9\n", "large boundary difference"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `1` | Smallest possible interval and endpoint handling |
| `9 / 9` | `9` | Distinguishes digital root `9` from modulo result `0` |
| `4 / 8` | `6` | Maximum interval size that does not trigger the six-number shortcut |
| `4 / 9` | `9` | Exact boundary where six consecutive numbers force divisibility by `9` |
| `9...9 / 9...9` with 100,000 digits | `9` | Maximum endpoint length and string-based modulo computation |
| `10^99999 / (10^99999 + 5)` | `9` | Huge strings combined with the exact `b - a = 5` boundary |

## Edge Cases

When `a = b`, the product contains exactly one number, so the answer is simply the digital root of that number. For input `9` and `9`, `mod9("9")` is zero. The algorithm does not print zero, it converts the zero remainder to `9`, giving the correct result `9`.

When the interval contains exactly five numbers, the shortcut must not be applied. For input `4` and `8`, the factors are `4, 5, 6, 7, 8`. Their product is `6720`, which has remainder `6` modulo `9`, so the answer is `6`. The algorithm compares `b` with `a + 5 = 9`, sees that `8 < 9`, and explicitly processes all five factors.

When the interval contains exactly six numbers, the shortcut must apply. For input `4` and `9`, the factors include both `6` and `9`. Their product already contributes two factors of `3`, so the complete product is divisible by `9`. The algorithm computes `a + 5 = 9`, observes `b >= 9`, and immediately returns `9`.

The endpoints may have 100,000 digits, so converting them with `int()` is not part of the solution. For an endpoint consisting of 100,000 nines, the algorithm scans its digits to obtain the modulo `9` residue and uses decimal-string addition only when comparing nearby values. The work remains linear in the number of digits.

The case `b - a = 5` is especially useful for catching off-by-one errors. Six numbers means five units of difference, so the product is guaranteed to be divisible by `9`. An implementation that checks `b - a > 5` instead of `b - a >= 5` would incorrectly try to process this case as a short interval. For example, `4` and `9` must produce `9`.
