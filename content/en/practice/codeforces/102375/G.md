---
title: "CF 102375G - \u0415\u0441\u0442\u044c \u043b\u0438 \u0434\u0435\u043b\u0438\u0442\u0435\u043b\u044c?"
description: "We are given a decimal string of digits, but those digits are not necessarily meant to be interpreted in base 10. We may choose a base (B), as long as every digit in the string is valid in that base."
date: "2026-08-14T03:28:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102375
codeforces_index: "G"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438 \u0438 \u041c\u043e\u0441\u043a\u0432\u044b ICPC 2019"
rating: 0
weight: 102375
solve_time_s: 154
verified: false
draft: false
---

[CF 102375G - \u0415\u0441\u0442\u044c \u043b\u0438 \u0434\u0435\u043b\u0438\u0442\u0435\u043b\u044c?](https://codeforces.com/problemset/problem/102375/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 34s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a decimal string of digits, but those digits are not necessarily meant to be interpreted in base 10. We may choose a base (B), as long as every digit in the string is valid in that base. If the digits are (a_{N-1}\ldots a_1a_0), the represented number is

[
D=a_{N-1}B^{N-1}+a_{N-2}B^{N-2}+\cdots+a_1B+a_0.
]

We need to choose (B) and a proper divisor (X) of (D), with both values between 2 and (10^9). The number (D) itself may be enormously large, because the input contains up to (3\cdot10^6) digits, so constructing it as an integer is impossible.

The decisive constraint is the length of the input. With three million digits, an algorithm that examines many possible bases or divisors cannot work. We need essentially one or a few linear scans over the string. The bound (10^9) on (B) and (X) is generous enough for values derived from the digit sum, because the largest possible digit sum is only (9\cdot3\cdot10^6=27\cdot10^6).

There are two small cases that a careless solution can mishandle. For input `1`, the represented value is always 1, regardless of the base, so there is no proper divisor and the answer is `-1`. For input `4`, the value is always 4, but it does have the proper divisor 2, so the answer exists, for example `10 2`. A solution that assumes every one-digit input is impossible would fail here.

Another special case is a multi-digit string whose digit sum is 1, such as `10` or `1000`. The main construction below would try to use (X=1), which is forbidden. For `10`, choosing (B=4) gives (D=4), so (X=2) works. The same construction works for every string of the form `100...0`.

## Approaches

A direct approach would try bases one by one. For every candidate base (B), we would evaluate the polynomial represented by the digit string and then search for a divisor. Even ignoring the divisor search, there can be (10^9) possible bases. Evaluating a length-(N) string for each base costs (O(N)), giving roughly (10^9N) digit operations, which reaches about (3\cdot10^{15}) operations at the maximum input size. Trying every pair ((B,X)) is even worse, with up to (10^{18}) pairs.

The useful observation is that the value of the polynomial becomes very simple modulo a number related to the base. Suppose the sum of all digits is (S), and choose

[
X=S,\qquad B=S+1.
]

Then (B\equiv1\pmod S). Consequently every power of (B) is also congruent to 1 modulo (S), so

[
D\equiv a_{N-1}+a_{N-2}+\cdots+a_0=S\equiv0\pmod S.
]

Thus (S) automatically divides (D). We have converted the problem from finding a divisor of a huge number into simply computing the digit sum.

For (S\ge2) and (N\ge2), the construction is always valid. Since (S) is at least every individual digit, (B=S+1) is strictly larger than every digit and is a legal base. Also (S\le27\cdot10^6), so both (B) and (X) are safely below (10^9). Finally, because there are at least two digits and (B) is a valid base, (D>B>S), so (X=S) is a proper divisor rather than the whole number.

The only remaining case for (N\ge2) is (S=1). Since the first digit is nonzero, this means the input is exactly `100...0`. Choosing (B=4) makes the represented number (D=4^{N-1}). For (N\ge2), this is at least 4 and is divisible by (X=2).

For a one-digit input, changing the base does not change the value at all. The value is simply that digit. Among digits 1 through 9, the composite ones are 4, 6, 8, and 9. They have proper divisors 2, 2, 2, and 3 respectively. The remaining digits have no proper divisor, so the answer is `-1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(10^9N)) or worse | (O(N)) | Too slow |
| Optimal | (O(N)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read the digit string and compute its digit sum (S) in one pass. We only need the sum, not the enormous number represented by the string.
2. If the string has one digit, inspect that digit directly. For 4, 6, and 8 output base 10 and divisor 2. For 9 output base 10 and divisor 3. For 1, 2, 3, 5, and 7 output `-1`, because those values have no proper divisor.
3. If there are at least two digits and (S=1), output (B=4) and (X=2). The input must be `100...0`, so its value in base 4 is (4^{N-1}), which is at least 4 and divisible by 2.
4. If there are at least two digits and (S\ge2), set (X=S) and (B=S+1). The choice is designed so that (B\equiv1\pmod X), making every power of (B) equal to 1 modulo (X).
5. Since every digit is at most (S), the base (B=S+1) is valid. The largest possible sum is (27\cdot10^6), so both (B) and (X) are below (10^9).
6. The represented number satisfies

[
D\equiv\sum a_i=S\equiv0\pmod S,
]

and (D>S) because the string has at least two digits. Thus the pair is valid.

### Why it works

The central invariant is that when (B=S+1), every power (B^k) is congruent to 1 modulo (S). The entire base-(B) number therefore collapses modulo (S) to its digit sum. Choosing the divisor equal to that digit sum makes the remainder zero. The special (S=1) case is handled separately because 1 cannot be used as a divisor, while one-digit inputs are handled separately because changing the base cannot change their numerical value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(s: str) -> str:
    n = len(s)
    digits = [ord(c) - 48 for c in s]
    total = sum(digits)

    if n == 1:
        d = digits[0]

        if d == 4 or d == 6 or d == 8:
            return "10 2"
        if d == 9:
            return "10 3"

        return "-1"

    if total == 1:
        return "4 2"

    x = total
    b = total + 1
    return f"{b} {x}"

s = input().strip()
print(solve(s))
```

The first line of `solve` computes the digit sum without converting the input to an integer. Python integers can be arbitrarily large, but constructing a three-million-digit integer would still be unnecessary and expensive.

For a one-digit input, the code handles the four composite digits explicitly. Base 10 is valid for every input digit from 1 through 9, so there is no need to search for a base.

For a multi-digit input with digit sum 1, the only possible form is `100...0`. The pair `4 2` is valid even for the shortest such string, `10`, because its value in base 4 is exactly 4.

For all remaining inputs, `total` is at least 2. The code outputs `total + 1` as the base and `total` as the divisor. There is no overflow issue in Python, and the maximum value of `total` is only 27 million.

The check that the base is valid follows directly from (S\ge d_i) for every digit (d_i), giving (B=S+1>d_i). No conversion of the whole string to the represented number is performed.

## Worked Examples

### Sample 1

For the input `1`, the string has one digit, so its value is 1 in every valid base.

| Input | Length | Digit sum | Case | Output |
| --- | --- | --- | --- | --- |
| `1` | 1 | 1 | One-digit prime/value 1 | `-1` |

There is no integer (X) with (1<X<1), so no solution exists. This exercises the smallest possible input and the special one-digit branch.

### Sample 2

For the input `4`, the value is 4 regardless of the base. Since 4 is composite, divisor 2 works.

| Input | Length | Digit | Proper divisor | Base | Output |
| --- | --- | --- | --- | --- | --- |
| `4` | 1 | 4 | 2 | 10 | `10 2` |

In base 10, the digit `4` represents (D=4), and (2\mid4) with (2<4). This demonstrates why one-digit composite inputs must not be rejected.

### Sample 3

For `19`, the digit sum is (S=10). The general construction chooses (X=10) and (B=11).

| Input | Length | Digit sum (S) | (B=S+1) | (X=S) | (D) | Output |
| --- | --- | --- | --- | --- | --- | --- |
| `19` | 2 | 10 | 11 | 10 | (1\cdot11+9=20) | `11 10` |

The sample uses the different valid pair `11 2`, but the problem allows any valid pair. Our pair works because (20) is divisible by 10 and (10<20).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N)) | The string is scanned once to compute its digit sum. |
| Space | (O(N)) | The input string itself occupies (O(N)) memory; the algorithm uses only (O(1)) additional space. |

With (N\le3\cdot10^6), a single linear scan is exactly the intended scale. The algorithm never constructs (D), whose number of bits could be proportional to (N\log B), and never enumerates bases or divisors.

## Test Cases

```python
import sys
import io

def solve(s: str) -> str:
    n = len(s)
    total = sum(ord(c) - 48 for c in s)

    if n == 1:
        d = ord(s[0]) - 48

        if d == 4 or d == 6 or d == 8:
            return "10 2"
        if d == 9:
            return "10 3"

        return "-1"

    if total == 1:
        return "4 2"

    return f"{total + 1} {total}"

def run(inp: str) -> str:
    return solve(inp.strip())

assert run("1") == "-1", "sample 1"
assert run("4") == "10 2", "sample 2"
assert run("19") == "11 10", "sample 3, any valid answer is accepted"

assert run("2") == "-1", "one-digit prime"
assert run("9") == "10 3", "one-digit composite"
assert run("10") == "4 2", "digit sum equals 1"
assert run("99") == "19 18", "general digit-sum construction"

large = "9" * 3_000_000
assert run(large) == "27000001 27000000", "maximum input length"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2` | `-1` | One-digit prime value |
| `9` | `10 3` | One-digit composite value at the upper digit boundary |
| `10` | `4 2` | Special case with digit sum 1 |
| `99` | `19 18` | Normal digit-sum construction |
| Three million `9` digits | `27000001 27000000` | Maximum input length and the (10^9) bounds |

The third sample has a different expected output from the official sample because this problem accepts any valid pair. For `19`, both `11 2` and `11 10` are correct.

## Edge Cases

The input `1` is the smallest possible string. Its represented value is 1 for every base, so no proper divisor exists. The one-digit branch detects that the value is not one of 4, 6, 8, or 9 and returns `-1`.

The input `4` demonstrates the opposite one-digit situation. The value remains 4 regardless of the base, and 2 is a proper divisor. The algorithm outputs `10 2`, where base 10 is valid because the only digit is 4.

The input `10` has two digits but digit sum 1. Using the general formula would produce (X=1), which is forbidden. The special branch instead chooses (B=4) and (X=2). The represented value is (1\cdot4+0=4), so (2) is a valid proper divisor.

For a maximum-length input consisting entirely of 9s, the digit sum is (27,000,000). The algorithm chooses (X=27,000,000) and (B=27,000,001). Both are below (10^9), and every digit is less than the base. Since (B\equiv1\pmod X), the represented number is divisible by (X) regardless of its enormous size.

The boundary condition (D>X) also deserves explicit attention. For every multi-digit input in the general case, the leading digit is positive, so the represented value contains at least one positive multiple of (B). Hence (D\ge B), and because (B=S+1), we get (D>S=X). The divisor can never accidentally equal the whole represented number.
