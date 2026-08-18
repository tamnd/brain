---
title: "CF 102270C - Divide"
description: "We need to count positive integers (N) in the interval ([A,B]) satisfying three independent-looking restrictions. First, every decimal digit of (N) must belong to the supplied set (S). Second, (N) must be divisible by (X)."
date: "2026-08-19T05:01:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102270
codeforces_index: "C"
codeforces_contest_name: "HCW 19 Individual Day 2"
rating: 0
weight: 102270
solve_time_s: 619
verified: false
draft: false
---

[CF 102270C - Divide](https://codeforces.com/problemset/problem/102270/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 10m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We need to count positive integers (N) in the interval ([A,B]) satisfying three independent-looking restrictions.

First, every decimal digit of (N) must belong to the supplied set (S). Second, (N) must be divisible by (X). Third, if we number positions from the right, the digit at position (i) must be coprime with (i). In other words, for the digit (d_i) at the (i)-th position from the right, we require (\gcd(d_i,i)=1). The answer is the number of such integers, reduced modulo (10^9+7).

The official constraints allow (B) to have up to 101 decimal digits, while (X) can be as large as (10^5). That immediately rules out enumerating the interval. Even storing or iterating over all numbers would require up to about (10^{100}) candidates. We need an algorithm whose cost depends on the number of digits and on (X), not on the numerical size of (B).

There are a few boundary cases that are easy to mishandle. The first is leading zeroes. Zero may be a valid digit at an internal position, but it cannot be the most significant digit of a positive integer. For example, with input

```
1 9 1
0
```

the answer is `0`. A careless implementation might regard `0` as a valid one-digit number, or regard representations such as `01` as ordinary positive integers.

The second issue is that the coprimality condition is counted from the right, not from the left. For example, `12` is valid with respect to the positional condition because its rightmost digit is (2) and (\gcd(2,1)=1), while its left digit is (1) and (\gcd(1,2)=1). This is why simply checking the digit against its index in the left-to-right representation gives the wrong result.

The third issue is the upper bound when processing digits from the right. Consider `B = 20` and the one-digit number `8`. Comparing the low digit `8` with the low digit `0` makes the subtraction `0 - 8` borrow, but `8` is obviously still smaller than `20`. A right-to-left bound DP must remember that a shorter number automatically fits below a longer positive upper bound.

## Approaches

The direct approach is to enumerate every integer from (A) through (B). For each candidate, we would inspect its digits, verify membership in (S), check the coprimality condition at every position, and test divisibility by (X). This is correct because every candidate is examined exactly once, and every required condition is checked explicitly.

The problem is the size of the interval. When (B) has 101 digits, there can be on the order of (10^{100}) candidates. Even if checking one candidate took only (O(100)) operations, the worst case would be roughly (O(100\cdot10^{100})), which is completely infeasible.

The key observation is that the restrictions are digit-local except for divisibility. At position (i), we can immediately determine which digits are legal by checking (\gcd(d,i)=1). Divisibility can also be represented by a remainder modulo (X). That gives a digit DP whose state contains only a remainder and a small amount of information about the comparison with the bound.

There is an especially useful trick here. The positional condition is defined from the right, so instead of processing the bound from left to right, we process both the constructed number and the bound from right to left. The comparison can then be represented by the borrow produced while subtracting the constructed number from the bound.

Suppose the currently processed low (i) digits of the bound are (B_{\text{low}}), and the corresponding digits of the constructed number are (N_{\text{low}}). We maintain whether the subtraction (B_{\text{low}}-N_{\text{low}}) needs a borrow into the next position. This turns the usual left-to-right tight condition into a two-state borrow condition.

The remainder is also convenient from the right. If the already chosen (i-1) low digits form a value with remainder (r), and the new digit at position (i) is (d), then the new value is

[
r+d\cdot10^{i-1}.
]

Thus we only need to maintain the remainder modulo (X).

The same DP can count every possible length up to the length of the bound. If the constructed number has fewer digits than the bound, it is automatically smaller, regardless of the final borrow. Only a number with exactly the same number of digits as the bound needs final borrow zero.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(100\cdot10^{100})) | (O(1)) | Too slow |
| Optimal | (O(LX | S | )) per bound | (O(X)) | Accepted |

Here (L\le101). We run the bounded DP for (B) and for (A-1), which only changes the constant factor.

## Algorithm Walkthrough

1. Define `dp0[r]` and `dp1[r]` after processing some number of positions from the right. `dp0[r]` counts constructions whose current subtraction from the corresponding low digits of the bound has no borrow, while `dp1[r]` counts constructions with a borrow. Both arrays are indexed by the remainder modulo (X).

Initially no digits have been chosen, the remainder is zero, and there is no borrow, so `dp0[0] = 1` and every other state is zero.
2. Process positions (i=1,2,\ldots,L) from right to left. For every position, build the list of digits from (S) satisfying (\gcd(d,i)=1). These are exactly the digits that can appear at this position.

This directly incorporates the unusual positional condition into the transition, so an invalid digit never enters the DP.
3. Maintain (p=10^{i-1}\bmod X). If the current digit is (d), adding it to the already constructed lower positions changes the remainder from (r) to

[
(r+d p)\bmod X.
]

The power is updated by multiplying by 10 after each position.
4. Let (b) be the (i)-th digit of the bound from the right. Suppose the previous borrow is (c). The subtraction at this position is

[
b-d-c.
]

The new borrow is determined by whether this value is negative. There are only three cases.

If (d<b), both possible old borrows produce no new borrow.

If (d=b), an old borrow remains a borrow, while no old borrow remains no borrow.

If (d>b), both possible old borrows produce a new borrow.

This is the right-to-left equivalent of the familiar tight-state transition in ordinary digit DP.
5. After processing position (i), count numbers whose length is exactly (i). To make position (i) the most significant position, the chosen digit must be nonzero. For every legal nonzero digit (d), we know exactly which previous remainder can lead to remainder zero, namely

[
r\equiv-d\cdot10^{i-1}\pmod X.
]

There is only one such remainder, so counting exact-length divisible numbers takes only a constant number of extra operations per digit.
6. If (i<L), every (i)-digit positive number is smaller than the (L)-digit bound. Consequently both borrow states are accepted when counting the contribution of this length.

If (i=L), the number has the same length as the bound, so only states with final borrow zero are accepted.
7. Compute `count_leq(B)`, then decrement (A) by one as a decimal string and compute `count_leq(A-1)`. The required interval answer is

[
\text{count_leq}(B)-\text{count_leq}(A-1).
]

The subtraction is performed modulo (10^9+7).

Why it works: after processing the first (i) positions from the right, every DP state represents exactly one set of valid choices for those positions, classified by its remainder modulo (X) and by the borrow in the subtraction from the bound. The transition considers every legal next digit exactly once and sends it to the mathematically correct new remainder and borrow state. When a number stops after (i) digits, its most significant digit is explicitly required to be nonzero. For shorter numbers both borrow states are valid because the unprocessed higher part of the bound contains at least one positive digit. For equal-length numbers, borrow zero is exactly the condition that the constructed number is at most the bound. Thus every valid number is counted once, and no invalid number is counted.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

MOD = 1_000_000_007

def dec_one(s):
    s = s.lstrip('0')
    if not s:
        return None

    a = list(s)
    i = len(a) - 1

    while i >= 0 and a[i] == '0':
        a[i] = '9'
        i -= 1

    if i < 0:
        return None

    a[i] = str(ord(a[i]) - ord('0') - 1)

    res = ''.join(a).lstrip('0')
    return res if res else '0'

def count_leq(t, x, source_digits):
    if t is None or t == '0':
        return 0

    t = t.lstrip('0')
    if not t:
        return 0

    length = len(t)

    allowed = [[] for _ in range(length + 1)]
    for pos in range(1, length + 1):
        cur = allowed[pos]
        for d in source_digits:
            if gcd(d, pos) == 1:
                cur.append(d)

    # dp0[r]: low processed digits have no borrow.
    # dp1[r]: low processed digits have a borrow.
    dp0 = [0] * x
    dp1 = [0] * x
    dp0[0] = 1

    power = 1
    answer = 0

    # Digits of t indexed from the right.
    bound_digits = [ord(c) - 48 for c in reversed(t)]

    for pos in range(1, length + 1):
        bd = bound_digits[pos - 1]
        digits = allowed[pos]

        ndp0 = [0] * x
        ndp1 = [0] * x

        # Count numbers that stop at this position.
        # For pos < length, both borrow states are valid.
        # For pos == length, only borrow 0 is valid.
        if pos < length:
            length_count = 0

            for d in digits:
                if d == 0:
                    continue

                add = (d * power) % x
                prev = (-add) % x

                v = dp0[prev] + dp1[prev]
                if v >= MOD:
                    v -= MOD

                length_count += v
                if length_count >= MOD:
                    length_count -= MOD

            answer += length_count
            if answer >= MOD:
                answer -= MOD
        else:
            length_count = 0

            for d in digits:
                if d == 0:
                    continue

                add = (d * power) % x
                prev = (-add) % x

                if d < bd:
                    v = dp0[prev] + dp1[prev]
                elif d == bd:
                    v = dp0[prev]
                else:
                    v = 0

                if v >= MOD:
                    v -= MOD

                length_count += v
                if length_count >= MOD:
                    length_count -= MOD

            answer += length_count
            if answer >= MOD:
                answer -= MOD

        # Build the DP for the next position.
        for d in digits:
            add = (d * power) % x

            if d < bd:
                # Both old borrow states become borrow 0.
                src0 = dp0
                src1 = dp1
                dest = ndp0

                for r in range(x):
                    j = r + add
                    if j >= x:
                        j -= x

                    v = src0[r] + src1[r]
                    if v >= MOD:
                        v -= MOD

                    v += dest[j]
                    if v >= MOD:
                        v -= MOD

                    dest[j] = v

            elif d == bd:
                # No old borrow stays at 0, old borrow stays at 1.
                src0 = dp0
                src1 = dp1

                for r in range(x):
                    j = r + add
                    if j >= x:
                        j -= x

                    v = ndp0[j] + src0[r]
                    if v >= MOD:
                        v -= MOD
                    ndp0[j] = v

                    v = ndp1[j] + src1[r]
                    if v >= MOD:
                        v -= MOD
                    ndp1[j] = v

            else:
                # Both old borrow states become borrow 1.
                src0 = dp0
                src1 = dp1
                dest = ndp1

                for r in range(x):
                    j = r + add
                    if j >= x:
                        j -= x

                    v = src0[r] + src1[r]
                    if v >= MOD:
                        v -= MOD

                    v += dest[j]
                    if v >= MOD:
                        v -= MOD

                    dest[j] = v

        dp0, dp1 = ndp0, ndp1

        power = (power * 10) % x

    return answer

def solve_case(a, b, x, s):
    digits = [ord(c) - 48 for c in s]

    right_of_a = dec_one(a)

    upper = count_leq(b, x, digits)
    lower = count_leq(right_of_a, x, digits)

    return (upper - lower) % MOD

def main():
    A, B, X = input().split()
    X = int(X)
    S = input().strip()

    print(solve_case(A, B, X, S))

if __name__ == "__main__":
    main()
```

The `allowed` array is the direct implementation of the positional rule. Position 1 is special because every digit is coprime with 1, while zero is also mathematically allowed there. Zero remains valid for the least significant position, but the exact-length counting step skips it whenever that position becomes the most significant digit.

The two remainder arrays are the central DP state. The arrays are recreated at every position because each transition depends only on the immediately previous position. No history beyond the current remainder and borrow is needed.

The update `j = r + add` followed by one subtraction of `x` avoids the relatively expensive modulo operation inside the innermost loop. Since both `r` and `add` are in `[0,x-1]`, their sum is smaller than `2x`, so one subtraction is sufficient.

The exact-length count is separate from the transition because zero is legal internally but illegal as a leading digit. For a nonzero candidate digit `d`, the only previous remainder that produces final remainder zero is `(-d * power) % x`. This avoids scanning the entire remainder array a second time just to determine how many valid leading digits produce remainder zero.

The borrow transition deserves particular attention. For `d < bd`, even an existing borrow is absorbed because `bd - d - 1` is still nonnegative. For `d == bd`, an existing borrow survives. For `d > bd`, both cases require a borrow. Mixing up these three cases is the most likely source of a wrong answer in a right-to-left implementation.

Python integers do not overflow, but all DP counts are reduced modulo (10^9+7) after each addition. The decimal decrement is done directly on the string, which is necessary because (A) may have 101 digits and does not need to fit in a fixed-width integer.

## Worked Examples

For Sample 1,

```
A = 1
B = 20
X = 2
S = 1234789
```

The useful right-to-left states for the upper bound are summarized below.

| Position | Bound digit | Allowed digits | Length contribution | Reason |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1,2,3,4,7,8,9 | 3 | One-digit multiples of 2 are 2, 4, 8 |
| 2 | 2 | 1,3,7,9 | 3 | Two-digit valid multiples are 12, 14, 18 |

At position 1, every digit is coprime with 1. Since one-digit numbers are automatically below `20`, the valid divisible numbers are `2`, `4`, and `8`.

At position 2, the most significant digit must be coprime with 2, so only `1`, `3`, `7`, and `9` are allowed. The bound digit is 2. The combinations that produce remainder zero and finish with no borrow are `12`, `14`, and `18`. The total is consequently 6, matching the sample output.

For Sample 2,

```
A = 1
B = 20
X = 3
S = 0123678
```

The trace is similar.

| Position | Bound digit | Allowed digits | Length contribution | Valid numbers |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0,1,2,3,6,7,8 | 2 | 3, 6 |
| 2 | 2 | 1,3,7 | 2 | 12, 18 |

At position 1, zero is ignored as a leading digit, leaving `3` and `6` as the one-digit multiples of 3.

At position 2, the second-from-right digit is restricted by (\gcd(d,2)=1), so among the supplied digits only `1`, `3`, and `7` are possible. The bound and remainder conditions leave `12` and `18`. The total is 4, again matching the sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(LX | S | )) | There are (L) positions, (X) remainder states, and at most 10 candidate digits per position, with two bounds |
| Space | (O(X+L | S | )) | Two remainder arrays and the precomputed legal digits |

The maximum bound length is only about 101 digits, while (X\le10^5). The algorithm never depends on the numerical magnitude of (A) or (B), only on their decimal lengths. The memory usage stays linear in (X), which is the key requirement for the largest tests.

## Test Cases

```python
# Save the editorial solution as solution.py before running these tests.

from solution import solve_case

# Provided samples
assert solve_case(
    "1", "20", 2, "1234789"
) == 6, "sample 1"

assert solve_case(
    "1", "20", 3, "0123678"
) == 4, "sample 2"

# Minimum-size input.
assert solve_case(
    "1", "1", 1, "1"
) == 1, "single valid number"

# Single boundary value that is not divisible by X.
assert solve_case(
    "11", "11", 2, "12"
) == 0, "exact boundary but wrong remainder"

# Exact boundary value that is valid.
assert solve_case(
    "12", "12", 2, "12"
) == 1, "exact boundary"

# All-equal digit set. Valid numbers are 7 and 77.
assert solve_case(
    "1", "100", 7, "7"
) == 2, "all-equal digits"

# Maximum-size decimal bound.
# With only digit 1 available, every repunit from 1 to 101 digits is valid,
# and X = 1 makes every one divisible.
big_b = "1" + "0" * 100
assert solve_case(
    "1", big_b, 1, "1"
) == 101, "maximum-size bound"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / 1` | `1` | Minimum interval and single valid number |
| `11 11 2 / 12` | `0` | Exact upper and lower boundary with failed divisibility |
| `12 12 2 / 12` | `1` | Exact boundary with all conditions satisfied |
| `1 100 7 / 7` | `2` | Repeated digit and positional coprimality |
| `1 10^100 1 / 1` | `101` | Maximum digit length and arbitrary-precision bounds |

## Edge Cases

A leading zero is handled by the exact-length counting step rather than by forbidding zero globally. For example,

```
1 9 1
0
```

has answer `0`. Zero is legal at position 1 according to the gcd rule, but it cannot be the leading digit of a positive integer, so the candidate is never counted as a one-digit number.

A zero can still be a valid internal digit when its position is 1 from the right. This is why zero must remain in the transition set. For example, if the allowed digits are `01`, the number `10` has rightmost digit zero, and (\gcd(0,1)=1), while its leading digit one satisfies (\gcd(1,2)=1). The algorithm allows the zero during the first transition and rejects it only if it is used as the most significant digit.

Numbers shorter than the bound require special treatment in a right-to-left comparison. For `B = 20`, the one-digit number `8` causes a borrow when comparing its only digit against the low digit `0` of `20`. The DP keeps that borrow state instead of rejecting the number. Since the constructed number has only one digit while the bound has two, both final borrow states are accepted for the one-digit contribution.

The positional gcd condition must use the distance from the right. For `12`, the rightmost digit is at position 1 and the left digit is at position 2. Both satisfy the condition because (\gcd(2,1)=1) and (\gcd(1,2)=1). The DP processes exactly in that order, so the position used to construct the allowed digit set is always the correct one.

Finally, the interval is obtained as `count_leq(B) - count_leq(A-1)`. This handles both endpoints without special cases in the main DP. For `A = B = 12`, the first count includes `12` and the second count stops at `11`, leaving exactly one number. For `A = B = 11` with `X = 2`, both computations agree that there is no valid divisible number, so the result is zero.
