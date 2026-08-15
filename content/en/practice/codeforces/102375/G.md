---
title: "CF 102375G - \u0415\u0441\u0442\u044c \u043b\u0438 \u0434\u0435\u043b\u0438\u0442\u0435\u043b\u044c?"
description: "We are given one nonempty decimal string, with no leading zero. The string is not necessarily interpreted in base 10. We may choose a base (B), provided every digit appearing in the string is a valid digit in that base."
date: "2026-08-15T18:00:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102375
codeforces_index: "G"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438 \u0438 \u041c\u043e\u0441\u043a\u0432\u044b ICPC 2019"
rating: 0
weight: 102375
solve_time_s: 306
verified: false
draft: false
---

[CF 102375G - \u0415\u0441\u0442\u044c \u043b\u0438 \u0434\u0435\u043b\u0438\u0442\u0435\u043b\u044c?](https://codeforces.com/problemset/problem/102375/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 6s  
**Verified:** no  

## Solution
## Problem Understanding

We are given one nonempty decimal string, with no leading zero. The string is not necessarily interpreted in base 10. We may choose a base (B), provided every digit appearing in the string is a valid digit in that base. Interpreting the same sequence of digits in base (B) produces some integer (D).

Our task is to choose (B) and a proper divisor (X) of (D), with (1 < X < D), such that both (B) and (X) are at most (10^9). If no such pair exists, we print (-1).

The length can reach (3\cdot10^6), so the input itself is already millions of characters long. Any solution that repeatedly scans the whole string, tries many bases, or performs integer factorization on the resulting enormous number is unsuitable. We want essentially one linear pass over the digits. The useful fact is that the sum of all digits is at most (9\cdot3\cdot10^6=27\cdot10^6), which is far below (10^9). This gives us a small enough candidate for both the base and the divisor.

There are several small cases where blindly applying the main construction fails. For input `1`, the represented value is always (1), regardless of the base, so there cannot be a proper divisor and the correct answer is `-1`. For input `4`, the digit sum is (4), but choosing the sum as the divisor would give (X=D=4), which is not a proper divisor. The correct answer can be `10 2`. For input `10`, the digit sum is (1), so the construction based on the digit sum cannot use (X=1). Nevertheless, base (10) gives (D=10), and (X=2) works. These cases explain why the final algorithm separates strings of length one and the case where the digit sum is one.

## Approaches

A direct approach would try a base (B), construct the corresponding number (D), and search for a divisor (X). Even choosing only among all (10^9) possible bases already gives at least (10^9) candidates. Evaluating one base from a string of length (n) requires processing its digits, so merely examining every possible base costs at least (10^9n) digit operations. At the maximum length this is at least (3\cdot10^{15}) operations, before doing any factorization. Factoring (D) is even worse because (D) can have millions of decimal digits.

The brute force works because testing a candidate base and divisor is straightforward, but it fails because the space of possible bases is huge and the represented number is enormous. The key observation is that we do not need to know (D) explicitly at all.

For a number written in base (B), reducing it modulo (B-1) replaces every power of (B) by (1), because (B\equiv1\pmod{B-1}). Thus, if the digits are (a_0,a_1,\ldots,a_{n-1}), then

[
D=\sum a_iB^i\equiv\sum a_i\pmod{B-1}.
]

Let the digit sum be (S). If we choose

[
B=S+1,
]

then (B-1=S), so (D\equiv S\equiv0\pmod S). Consequently (X=S) is automatically a divisor of (D).

This is the central construction. Since (S) is at least every individual digit, (B=S+1) is a valid base. Since (S\le27\cdot10^6), both (B) and (X) are comfortably below (10^9).

For a string of length at least two and (S\ge2), (X=S) is also strictly smaller than (D). The leading digit is at least one, so (D\ge B=S+1>S=X).

The only remaining situation with at least two digits is (S=1). Since the first digit is nonzero, the string must be `100...0`. Choosing (B=10) gives (D=10^{n-1}), and (X=2) is a proper divisor. Finally, a one-digit string represents exactly that digit, independently of the base. Such a number has a proper divisor only when the digit itself is composite, which among the allowed digits means (4,6,8,9).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | At least (O(10^9n)), plus factorization | Potentially enormous | Too slow |
| Optimal | (O(n)) | (O(1)) besides the input string | Accepted |

## Algorithm Walkthrough

1. Read the digit string and compute its length and digit sum (S). Only the sum is needed for the main construction, so there is no reason to build the potentially enormous number (D).
2. If the string has one digit, handle it separately. A one-digit representation always has value equal to that digit, regardless of the base. If the digit is (4,6,) or (8), choose (B=10) and (X=2). If the digit is (9), choose (B=10) and (X=3). For (1,2,3,5,7), the number is prime, so print (-1).
3. If the string has at least two digits and (S=1), the string is necessarily `100...0`. Choose (B=10) and (X=2). The represented value is (10^{n-1}), which is divisible by (2) and is greater than (2).
4. Otherwise (n\ge2) and (S\ge2). Set (X=S) and (B=S+1). The base is valid because every digit is at most (S), hence strictly less than (B).
5. Output (B) and (X). Since (S\le27\cdot10^6), both values satisfy the (10^9) limit. Also, (D>X), because (D\ge B=S+1).

### Why it works

The invariant behind the main construction is (B\equiv1\pmod{B-1}). For (B=S+1), this becomes (B\equiv1\pmod S). Every positional power (B^k) is consequently congruent to (1) modulo (S), so the whole represented number satisfies (D\equiv S\equiv0\pmod S). Thus (X=S) always divides (D).

The construction also satisfies all bounds. The digit sum is at most (27\cdot10^6), so (B=S+1\le27,000,001) and (X=S\le27,000,000). Because (S) is at least the maximum digit, every digit is valid in base (B). For strings of length at least two, (D\ge B>X), so the divisor is proper. The special cases cover exactly the situations where (S) cannot serve as a valid proper divisor.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(s: str) -> str:
    n = len(s)
    digit_sum = sum(ord(c) - 48 for c in s)

    if n == 1:
        d = ord(s[0]) - 48

        if d in (4, 6, 8):
            return "10 2"
        if d == 9:
            return "10 3"
        return "-1"

    if digit_sum == 1:
        return "10 2"

    return f"{digit_sum + 1} {digit_sum}"

s = input().strip()
print(solve(s))
```

The first pass computes the digit sum without converting the entire string into an integer. Converting a string with up to three million digits into an integer would be unnecessary and, in many Python environments, subject to additional conversion limits.

The one-digit branch is separate because the positional base has no effect when there is only one digit. For example, `4` represents (4) in every valid base, so we must actually ask whether (4) itself has a proper divisor.

For a multi-digit string whose digit sum is one, the first digit must be one and every other digit must be zero. The fixed construction (B=10,X=2) works because the represented number is a positive power of ten.

In the general branch, `digit_sum + 1` is the base and `digit_sum` is the divisor. The code never calculates (D), which is the main implementation advantage. Python integers are therefore only used for tiny values bounded by (27\cdot10^6+1), regardless of the input length.

There are no overflow concerns in Python, and even in a language with fixed-width integers the constructed (B) and (X) are easily within 32-bit signed integer range. The string is scanned once, so the implementation also avoids any hidden quadratic behavior.

## Worked Examples

### Sample 1

For input `1`, the only represented value is (1).

| Input | Length | Digit sum | Chosen base | Chosen divisor | Result |
| --- | --- | --- | --- | --- | --- |
| `1` | 1 | 1 | none | none | `-1` |

The one-digit case is handled before the general construction. Since (1) has no divisor greater than one, no answer exists.

### Sample 2

For input `4`, the value is (4) in every valid base.

| Input | Length | Digit sum | Chosen base | Chosen divisor | Result |
| --- | --- | --- | --- | --- | --- |
| `4` | 1 | 4 | 10 | 2 | `10 2` |

The output means that the digit string `4` is interpreted as (D=4) in base (10), and (2) is a proper divisor of (4). The digit sum construction is deliberately not used here because it would select (X=4=D).

### Sample 3

For input `19`, the digit sum is (10), so the general construction gives (B=11) and (X=10).

In base (11),

[
D=1\cdot11+9=20,
]

and (20) is divisible by (10).

| Input | Length | Digit sum | Base (B) | Divisor (X) | Value (D) |
| --- | --- | --- | --- | --- | --- |
| `19` | 2 | 10 | 11 | 10 | 20 |

The congruence gives (D\equiv10\equiv0\pmod{10}), exactly as predicted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | The string is scanned once to compute its digit sum. |
| Space | (O(n)) for the input, (O(1)) auxiliary | No representation of (D) or other large structures is created. |

With (n\le3\cdot10^6), a single linear pass is appropriate. The algorithm performs only simple arithmetic on each character and never factors or constructs the potentially millions-of-digits-long value (D), so the constraints are easily within the intended range.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve(s: str) -> str:
    n = len(s)
    digit_sum = sum(ord(c) - 48 for c in s)

    if n == 1:
        d = ord(s[0]) - 48

        if d in (4, 6, 8):
            return "10 2"
        if d == 9:
            return "10 3"
        return "-1"

    if digit_sum == 1:
        return "10 2"

    return f"{digit_sum + 1} {digit_sum}"

def run(inp: str) -> str:
    s = inp.strip()
    return solve(s)

# Provided samples
assert run("1\n") == "-1", "sample 1"
assert run("4\n") == "10 2", "sample 2"
assert run("19\n") == "11 10", "sample 3, another valid answer"

# Minimum-size prime digit
assert run("2\n") == "-1", "single-digit prime"

# Single-digit composite at the upper boundary
assert run("9\n") == "10 3", "single-digit composite"

# All digits equal
assert run("2222\n") == "9 8", "all-equal digits"

# Digit sum exactly 1, including the two-digit boundary
assert run("10\n") == "10 2", "sum-one boundary"

# Maximum possible length
s = "1" + "0" * (3_000_000 - 1)
assert run(s) == "10 2", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2` | `-1` | Single-digit prime case |
| `9` | `10 3` | Single-digit composite at the largest digit |
| `2222` | `9 8` | Repeated digits and the main (B=S+1) construction |
| `10` | `10 2` | The exact boundary where the digit sum is one |
| `1` followed by (2,999,999) zeros | `10 2` | Maximum input length and linear processing |

## Edge Cases

For input `1`, the algorithm immediately enters the one-digit branch. Its value is (1) in every possible base, so there is no (X>1) with (X<D). The output is correctly `-1`.

For input `4`, the one-digit branch recognizes (4) as composite and chooses (X=2). Base (10) is valid because the digit (4) is smaller than (10), and the represented value remains (4). Thus `10 2` satisfies (2<4) and (2\mid4).

For input `9`, the algorithm uses (X=3) instead of (2), because (3\mid9). The output `10 3` represents (D=9), so the divisor is proper.

For input `10`, the digit sum is (1), making the main construction impossible because it would require (X=1). The special branch chooses (B=10), giving (D=10), and (X=2) is a proper divisor. The same reasoning works for every input of the form `100...0` with at least two digits.

For an input such as `2222`, the digit sum is (8), so the algorithm chooses (B=9) and (X=8). The represented value is

[
2\cdot9^3+2\cdot9^2+2\cdot9+2=1622,
]

and (1622) is divisible by (8). The congruence argument gives this without ever constructing (D).

For the maximum-size input consisting of `1` followed by (2,999,999) zeros, the digit sum is still (1). The algorithm therefore does not attempt to process the enormous represented number. It returns `10 2` immediately after the linear digit-sum pass, and the represented value is (10^{2,999,999}), which is certainly divisible by (2) and greater than (2).
