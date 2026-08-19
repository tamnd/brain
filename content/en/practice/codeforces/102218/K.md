---
title: "CF 102218K - K-th Missing Digit"
description: "We are given two positive integers (A) and (B), each potentially containing up to one million decimal digits. Their product is written as a decimal string (P), except that exactly one digit has been replaced by . The task is to recover that missing digit."
date: "2026-08-20T03:38:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102218
codeforces_index: "K"
codeforces_contest_name: "2019, XI Annual Programming Contest by ESCOM-IPN"
rating: 0
weight: 102218
solve_time_s: 304
verified: false
draft: false
---

[CF 102218K - K-th Missing Digit](https://codeforces.com/problemset/problem/102218/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 4s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two positive integers (A) and (B), each potentially containing up to one million decimal digits. Their product is written as a decimal string (P), except that exactly one digit has been replaced by `*`. The task is to recover that missing digit. The missing digit is guaranteed to be nonzero.

The first line gives the lengths of (A), (B), and (P). The next two lines contain (A) and (B), and the last line contains the partially known decimal representation of (A \times B). The answer is the single decimal digit that must replace `*`.

The crucial constraint is the number of digits, not the numerical value of the integers. (A) and (B) can each have (10^6) digits, so constructing either integer with ordinary machine arithmetic is impossible. Even a single grade-school multiplication would require on the order of (10^{12}) digit operations. Trying all nine possible missing digits and checking the resulting product would multiply that cost by nine.

The input itself can contain up to roughly two million digits, so an algorithm that scans the strings a constant number of times is appropriate. An algorithm requiring multiplication, conversion to a built-in integer type, or quadratic work on the digit strings is not suitable. Python's arbitrary-precision integers do not change this conclusion, because the input integers can be far larger than practical native representations and converting million-digit decimal strings is itself unnecessary work.

There are two edge cases that commonly cause mistakes. First, the missing digit can be (9). For example,

```
1 1 2
9
1
1*
```

gives (A \times B = 9), so the answer is `9`. A method that only computes a result modulo (9) and returns the residue directly would return `0`, which is forbidden but mathematically equivalent modulo (9). The guarantee that the missing digit is nonzero tells us to interpret residue (0) as digit (9).

The second edge case is a missing digit at either end of the product. For example,

```
2 2 3
10
10
*00
```

has product `100`, so the missing digit is `1`. A method that tries to infer the digit using only neighboring characters or treats the star as an internal digit can fail here. The modular argument does not depend on the position of the star, so the same calculation works for the first, last, or any middle position.

## Approaches

The direct approach is to try every possible nonzero digit from (1) through (9), replace `*` with that digit, and test whether the resulting string equals (A \times B). This is correct because the missing digit is guaranteed to be one of those nine values, so testing all possibilities must find the answer.

The problem is the multiplication. With up to (10^6) digits in both (A) and (B), ordinary long multiplication takes (O(10^{12})) digit operations for one candidate. Testing nine candidates still leaves roughly (9 \times 10^{12}) operations in the worst case. More sophisticated large-integer multiplication could reduce that asymptotically, but the problem has a much simpler property that avoids multiplication altogether.

The key observation is that decimal numbers preserve their value modulo (9) when their digits are summed. For any decimal number (X),

[
X \equiv \sum \text{digits}(X) \pmod 9.
]

Since (P = A \times B), we can compute

[
P \bmod 9 = (A \bmod 9)(B \bmod 9) \bmod 9.
]

We can calculate (A \bmod 9) and (B \bmod 9) by scanning their digits, without ever constructing the enormous integers. We can also calculate the contribution of every known digit of (P), leaving only the unknown digit (x).

Suppose the sum of the known digits in (P) is (S). Then

[
x + S \equiv A \times B \pmod 9.
]

Thus

[
x \equiv (A \times B - S) \pmod 9.
]

This gives a residue from (0) through (8). If it is (1) through (8), that is exactly the missing digit. If it is (0), the missing digit must be (9), because the problem explicitly rules out (0).

The brute-force method works because every candidate can be checked against the exact product, but fails when the operands contain millions of digits. The observation that decimal digit sums preserve values modulo (9) lets us replace enormous multiplication with three linear scans.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(AB)) for grade-school multiplication, repeated at most 9 times | (O(A+B+P)) | Too slow |
| Optimal | (O(A+B+P)) | (O(1)) besides input strings | Accepted |

Here (A), (B), and (P) in the complexity expressions denote the numbers of digits, not the numerical values of the integers.

## Algorithm Walkthrough

1. Read the three lengths and the strings representing (A), (B), and the partially known product (P). The lengths are not needed for the mathematics, but reading them follows the input format.
2. Compute (A \bmod 9) by scanning every digit of (A) and repeatedly applying `remainder = (remainder + digit) % 9`. The same calculation is performed for (B). This works because a decimal place has value (10^k), and (10 \equiv 1 \pmod 9), so every power of (10) is also congruent to (1).
3. Multiply the two remainders modulo (9). The result is the remainder that the complete product (P) must have.
4. Scan (P), adding every known digit modulo (9) while ignoring `*`. Call the resulting value `known`.
5. Compute the missing digit's residue as `(product_mod - known) % 9`. The modulo operation handles the case where the subtraction is negative.
6. If the resulting residue is zero, output `9`; otherwise output the residue itself. The residue zero corresponds to both digit `0` and digit `9`, and the statement rules out `0`.

### Why it works

The invariant is that every processed decimal string has the same remainder modulo (9) as the sum of its processed digits. After scanning (A) and (B), we know their exact residues modulo (9), so their product residue is known from modular multiplication. After scanning the known digits of (P), the only contribution missing from its digit sum is the unknown digit (x). Hence (x + S) must have exactly the product's remainder modulo (9). The computed residue identifies (x) uniquely among the allowed digits (1,\ldots,9), because only (0) and (9) share residue zero and (0) is forbidden.

## Python Solution

```python
import sys
input = sys.stdin.readline

def digit_mod_9(s):
    remainder = 0
    for ch in s:
        if ch != '\n':
            remainder = (remainder + ord(ch) - ord('0')) % 9
    return remainder

def solve():
    a_len, b_len, p_len = map(int, input().split())

    A = input().strip()
    B = input().strip()
    P = input().strip()

    a_mod = digit_mod_9(A)
    b_mod = digit_mod_9(B)

    product_mod = (a_mod * b_mod) % 9

    known_mod = 0
    for ch in P:
        if ch != '*':
            known_mod = (known_mod + ord(ch) - ord('0')) % 9

    missing = (product_mod - known_mod) % 9

    if missing == 0:
        missing = 9

    print(missing)

if __name__ == "__main__":
    solve()
```

The `digit_mod_9` function performs the digit-sum calculation described in the first part of the algorithm. Keeping the remainder reduced modulo (9) means the variable never grows beyond a single digit.

The two calls on `A` and `B` provide the residues of the operands. Multiplying those residues gives the residue of the actual product without constructing that product.

The final scan skips the `*` and accumulates the residues of all known product digits. Subtracting this from the product residue isolates the missing digit modulo (9).

The `% 9` operation after subtraction is necessary because Python can produce a negative intermediate result before taking the modulo. The final conversion from `0` to `9` is also essential. Returning the residue directly would fail whenever the actual missing digit is (9).

There is no integer conversion and no large-number multiplication. Python's arbitrary-precision arithmetic is used only for tiny values below (9^2), so integer overflow is not an issue.

## Worked Examples

For the first sample, the input is:

```
1 1 2
3
8
2*
```

The calculation proceeds as follows.

| Variable | State |
| --- | --- |
| (A \bmod 9) | (3) |
| (B \bmod 9) | (8) |
| Product modulo (9) | (3 \times 8 \bmod 9 = 6) |
| Known product digit sum modulo (9) | (2) |
| Missing digit modulo (9) | (6 - 2 = 4) |
| Answer | `4` |

The actual product is (3 \times 8 = 24). The modular calculation reaches the same missing digit without computing that product explicitly. The invariant is visible here because (2 + 4 = 6), which matches the product's remainder modulo (9).

For the second sample, the input is:

```
2 2 3
10
10
*00
```

The trace is:

| Variable | State |
| --- | --- |
| (A \bmod 9) | (1) |
| (B \bmod 9) | (1) |
| Product modulo (9) | (1) |
| Known product digit sum modulo (9) | (0) |
| Missing digit modulo (9) | (1) |
| Answer | `1` |

Here the star is the first character of the product. Its position has no effect on the method because every decimal digit contributes its value modulo (9), regardless of its place value. The product is `100`, and its residue is (1), so the missing leading digit must be `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(A+B+P)) | Each input number and the product string is scanned once. |
| Space | (O(A+B+P)) | The input strings are stored, while the algorithm itself uses (O(1)) additional space. |

The total input size is at most a few million characters, so a constant number of linear scans is appropriate even under the very tight time limit. The algorithm never allocates a representation of the full product and uses only a few small integer variables beyond the input strings, which also keeps memory usage comfortably within the stated limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_io():
    input = sys.stdin.readline

    a_len, b_len, p_len = map(int, input().split())
    A = input().strip()
    B = input().strip()
    P = input().strip()

    a_mod = 0
    for ch in A:
        a_mod = (a_mod + ord(ch) - ord('0')) % 9

    b_mod = 0
    for ch in B:
        b_mod = (b_mod + ord(ch) - ord('0')) % 9

    product_mod = (a_mod * b_mod) % 9

    known_mod = 0
    for ch in P:
        if ch != '*':
            known_mod = (known_mod + ord(ch) - ord('0')) % 9

    answer = (product_mod - known_mod) % 9
    if answer == 0:
        answer = 9

    print(answer)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve_io()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

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

# Minimum-size operands, 1 * 9 = 9
assert run("""1 1 1
1
9
*
""") == "9", "minimum size and missing digit 9"

# Missing digit is 9 and appears in the middle
# 99 * 1 = 99
assert run("""2 1 2
99
1
9*
""") == "9", "residue zero must map to digit 9"

# Missing digit is the first product digit
# 12 * 8 = 96
assert run("""2 1 2
12
8
*6
""") == "9", "leading missing digit"

# All digits equal, product 111 * 3 = 333
assert run("""3 1 3
111
3
3*3
""") == "3", "all-equal digits"

# Larger boundary-style values:
# 999999 * 9 = 8999991
assert run("""6 1 7
999999
9
8*99991
""") == "9", "large values and missing digit 9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1`, `9`, `*` | `9` | Minimum size and the special residue-zero case |
| `99`, `1`, `9*` | `9` | A missing final digit equal to `9` |
| `12`, `8`, `*6` | `9` | A missing first digit |
| `111`, `3`, `3*3` | `3` | Repeated equal digits |
| `999999`, `9`, `8*99991` | `9` | Larger operands and boundary-scale arithmetic |

## Edge Cases

A missing digit equal to (9) is the most subtle case. Consider:

```
1 1 1
1
9
*
```

The product is `9`, whose remainder modulo (9) is zero. The known digit contribution is also zero because there are no known product digits. The algorithm computes `missing = 0`, then converts that residue to `9`. This is correct because `0` is prohibited by the input guarantee.

A star at the beginning of the product requires no special positional handling. For:

```
2 1 2
12
8
*6
```

the product is `96`. We have (12 \equiv 3 \pmod 9) and (8 \equiv 8 \pmod 9), giving product residue (3 \times 8 \equiv 6). The known digit is `6`, so the missing digit has residue (6-6\equiv0). The only allowed digit with that residue is `9`, giving the correct product `96`.

A star at the end behaves identically. For:

```
1 1 2
3
8
2*
```

the product residue is (6), while the known digit `2` contributes (2). The missing digit is (4), so the algorithm prints `4`.

Large operands are handled without ever multiplying them. If (A) contains one million digits and (B) contains one million digits, the algorithm only maintains two residues in the range (0) through (8) while scanning the input. The same reasoning applies to a product string containing nearly two million digits. This is precisely the scale at which the modular approach succeeds and explicit multiplication fails.
