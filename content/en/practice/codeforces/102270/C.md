---
title: "CF 102270C - Divide"
description: "We need to count positive integers (N) in the inclusive range ([A,B]) that satisfy three independent-looking restrictions. First, (N) must be divisible by (X). Second, every decimal digit of (N) must belong to the set described by the string (S)."
date: "2026-08-17T18:24:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102270
codeforces_index: "C"
codeforces_contest_name: "HCW 19 Individual Day 2"
rating: 0
weight: 102270
solve_time_s: 319
verified: false
draft: false
---

[CF 102270C - Divide](https://codeforces.com/problemset/problem/102270/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We need to count positive integers (N) in the inclusive range ([A,B]) that satisfy three independent-looking restrictions.

First, (N) must be divisible by (X). Second, every decimal digit of (N) must belong to the set described by the string (S). Third, if a digit is in position (i), counted from the right starting at (1), then that digit (d) must satisfy (\gcd(d,i)=1).

The last condition is the unusual part. For example, the units digit is always unrestricted by the gcd condition because every digit is coprime with (1). At position (2), only odd digits can occur. At position (3), digits divisible by (3) are forbidden. At position (5), both (0) and (5) are forbidden. A zero digit is especially easy to mishandle: zero is valid at position (1), since (\gcd(0,1)=1), but it is invalid at every position greater than (1).

The bounds are the real reason a direct enumeration is impossible. (B) can contain up to (101) decimal digits because the largest allowed value can be (10^{100}), while (X) can be as large as (10^5). We cannot iterate through the integers in the interval, and we cannot even enumerate all valid digit strings. The solution has to work with the remainder modulo (X), giving a digit DP with roughly (O(100X)) states per layer.

There are several boundary cases that are easy to get wrong. Consider

```
1 20 2
02
```

The only candidate using the available digits near the upper boundary is (20), but it is invalid because its tens digit is (2), and (\gcd(2,2)=2). The correct answer is (0). An implementation that checks only whether digits belong to (S) would incorrectly count it.

Now consider

```
10 10 2
01
```

The answer is (1), because (10) is divisible by (2), its units digit is (0) and (\gcd(0,1)=1), and its tens digit is (1) and (\gcd(1,2)=1). An implementation that simply rejects zero digits would miss this case.

A second subtle case is a single digit:

```
1 1 1
0
```

The answer is (0), because the only allowed digit is zero, but the problem counts positive natural numbers, so (0) itself must not be included. This is why the DP must distinguish the units digit being zero from a complete one-digit number being zero.

Finally, the upper bound may have more digits than many valid numbers. For example, when (B=10^{100}), every valid number with fewer than (101) digits is automatically smaller than (B). Treating leading zeros as actual digits would incorrectly apply the position-gcd condition to those nonexistent leading positions.

## Approaches

The brute-force approach is straightforward. Iterate through every integer from (A) to (B), reject it if it is not divisible by (X), inspect its digits, and verify both the digit-set restriction and the gcd condition for every position. This is correct because every candidate is checked directly.

Its problem is the size of the interval. When (A=1) and (B) is close to (10^{100}), there are essentially (10^{100}) candidates. Even checking a single digit of each candidate would require an impossible number of operations. Converting the integers to strings also does not change the fundamental complexity.

The useful observation is that we never need the value of a partially constructed number, only its remainder modulo (X). At most (10^5) different remainders exist. The gcd condition also depends only on the position and the chosen digit, so for position (i) we can precompute exactly which digits are legal.

There is another structural detail that makes the position direction convenient. We process digits from right to left. After processing positions (1) through (i), the remainder is simply

[
r=\sum_{j=1}^{i} d_j10^{j-1}\pmod X.
]

When a new digit is placed at position (i+1), its contribution is known immediately as (d10^i\pmod X). More importantly, if we are comparing a fixed-length number with a bound, the newly added digit is more significant than every digit already processed. If it differs from the corresponding bound digit, it completely determines whether the number is smaller or larger. If it is equal, the comparison result of the lower positions is retained.

This gives a digit DP with the remainder as its main state and a three-valued comparison state for the boundary length.

We also avoid doing a separate digit DP for every possible length. We maintain the number of valid strings of each length incrementally. When a new most significant digit is added, all old digits keep exactly the same positions counted from the right, so their validity does not change. The new digit only has to satisfy the condition for its new position.

The two approaches can be summarized as follows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O((B-A+1)\log B)) | (O(\log B)) | Too slow |
| Optimal digit DP | (O(LX D)) | (O(X)) | Accepted |

Here (L\le101) is the number of digits involved and (D\le10) is the number of available decimal digits. The optimal method performs a constant number of such DP passes for the two range boundaries.

## Algorithm Walkthrough

1. Convert the digit string (S) into an array of allowed digits. For every position (i) from (1) through the maximum required length, build the list of digits (d) satisfying both (d\in S) and (\gcd(d,i)=1). This moves the gcd test out of the main DP loops.
2. Maintain a DP array indexed by the remainder modulo (X). While constructing digits from right to left, `dp[r]` represents the number of possible lower digit sequences whose numerical value modulo (X) is (r).
3. Initialize position (1) using every allowed digit, including zero. Zero must remain in this state because it is a perfectly valid units digit of a larger number, as in (10).
4. Extend the DP from position (i) to position (i+1). The new digit is the new most significant digit, so it must be nonzero. Its contribution to the remainder is (d10^i\bmod X). Consequently, a state with remainder (r) moves to

[
(r+d10^i)\bmod X.
]

Because the newly added digit is the most significant digit, requiring it to be nonzero guarantees that the resulting string represents a number with exactly (i+1) digits.

1. Store `dp[0]` after each extension as the number of valid positive integers of that exact length divisible by (X). For length (1), handle zero separately because the initial DP contains zero as a possible units digit but zero is not a positive integer.
2. To handle a bound such as (B), only its exact digit length needs special treatment. Every valid number with fewer digits is automatically smaller than (B). The previously computed exact-length counts can handle all those shorter numbers.
3. For the exact length of the bound, add a comparison state with three values: smaller, equal, and larger. Process the number from right to left. When the newly added digit is smaller than the corresponding digit of the bound, the complete comparison becomes smaller. When it is larger, the comparison becomes larger. When it is equal, the previous comparison remains unchanged.
4. At the end of the boundary DP, sum the remainder-zero states whose comparison is smaller or equal. This gives the number of valid integers of exactly the same length as the bound that do not exceed it.
5. Define `count_leq(B)` as the sum of all exact-length counts below the length of (B), plus the boundary DP result for the length of (B). Similarly compute `count_leq(A-1)` and subtract the two values modulo (10^9+7).
6. Subtracting one from a decimal string is done directly on the string. This is necessary because (A) and (B) may be larger than any built-in 64-bit integer.

### Why it works

The main invariant is that after processing position (i), every DP state represents exactly the valid choices for positions (1) through (i), grouped only by their remainder modulo (X) and, for a boundary DP, by their comparison with the corresponding suffix of the bound.

The position condition is checked exactly when a digit is introduced, so every stored sequence satisfies the gcd requirement. The remainder transition is the standard positional-value formula, so state (0) contains exactly the numbers divisible by (X). Requiring every newly added most significant digit to be nonzero gives every positive integer exactly one representation, with no leading-zero duplicates.

For the boundary DP, adding a new more significant digit correctly overrides the comparison of all less significant digits whenever it differs from the bound. Thus the final comparison state is exactly the usual numerical comparison between the constructed number and the bound. Combining all shorter lengths with the exact-length boundary count consequently counts every valid number up to the bound exactly once.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

MOD = 1_000_000_007

def dec_string(s):
    """Return s - 1 for a non-negative decimal string."""
    s = s.lstrip('0') or '0'
    if s == '0':
        return '-1'

    a = list(s)
    i = len(a) - 1

    while a[i] == '0':
        a[i] = '9'
        i -= 1

    a[i] = chr(ord(a[i]) - 1)
    res = ''.join(a).lstrip('0')
    return res or '0'

def prepare_digits(s, max_len):
    digits = [ord(c) - 48 for c in s]

    valid = [[] for _ in range(max_len + 1)]
    for pos in range(1, max_len + 1):
        valid[pos] = [d for d in digits if gcd(d, pos) == 1]

    return valid

def exact_counts(max_len, x, valid):
    """
    counts[len] = number of valid positive numbers with exactly len digits
    that are divisible by x.
    """
    counts = [0] * (max_len + 1)

    # Position 1 is the units digit. Zero is allowed here because it can
    # be the last digit of a multi-digit number.
    dp = [0] * x
    for d in valid[1]:
        dp[d % x] += 1

    # A one-digit number itself cannot be zero.
    c = 0
    for d in valid[1]:
        if d != 0 and d % x == 0:
            c += 1
    counts[1] = c % MOD

    power = 10 % x

    for pos in range(2, max_len + 1):
        ndp = [0] * x

        # Position pos is the most significant digit, so it must be nonzero.
        shifts = []
        for d in valid[pos]:
            if d != 0:
                shifts.append((d * power) % x)

        for shift in shifts:
            if shift == 0:
                for r in range(x):
                    ndp[r] += dp[r]
            else:
                cut = x - shift
                for r in range(cut):
                    ndp[r + shift] += dp[r]
                for r in range(cut, x):
                    ndp[r - cut] += dp[r]

        for r in range(x):
            ndp[r] %= MOD

        dp = ndp
        counts[pos] = dp[0]

        power = (power * 10) % x

    return counts

def boundary_count(bound, x, valid):
    """
    Count valid positive numbers with exactly len(bound) digits,
    divisible by x, and <= bound.
    """
    if bound == '0':
        return 0

    n = len(bound)

    # Relation:
    # 0 = smaller, 1 = equal, 2 = larger.
    less = [0] * x
    equal = [0] * x
    greater = [0] * x

    bound_digit = ord(bound[-1]) - 48

    # Start with the units digit. Zero is allowed here because the final
    # number may have more digits.
    for d in valid[1]:
        r = d % x
        if d < bound_digit:
            less[r] += 1
        elif d == bound_digit:
            equal[r] += 1
        else:
            greater[r] += 1

    if n == 1:
        # Only nonzero digits represent positive one-digit numbers.
        ans = 0
        for d in valid[1]:
            if d == 0:
                continue
            r = d % x
            if d <= bound_digit and r == 0:
                ans += 1
        return ans % MOD

    power = 10 % x

    for pos in range(2, n + 1):
        ndp_less = [0] * x
        ndp_equal = [0] * x
        ndp_greater = [0] * x

        bd = ord(bound[n - pos]) - 48

        for d in valid[pos]:
            if d == 0:
                continue

            shift = (d * power) % x

            if d < bd:
                # The new, more significant digit makes the whole number
                # smaller, regardless of the old comparison.
                if shift == 0:
                    for r in range(x):
                        ndp_less[r] += less[r] + equal[r] + greater[r]
                else:
                    cut = x - shift
                    for r in range(cut):
                        ndp_less[r + shift] += less[r] + equal[r] + greater[r]
                    for r in range(cut, x):
                        ndp_less[r - cut] += less[r] + equal[r] + greater[r]

            elif d > bd:
                # The new digit makes the whole number larger.
                if shift == 0:
                    for r in range(x):
                        ndp_greater[r] += less[r] + equal[r] + greater[r]
                else:
                    cut = x - shift
                    for r in range(cut):
                        ndp_greater[r + shift] += less[r] + equal[r] + greater[r]
                    for r in range(cut, x):
                        ndp_greater[r - cut] += less[r] + equal[r] + greater[r]

            else:
                # Equal new digit preserves the previous comparison.
                if shift == 0:
                    for r in range(x):
                        ndp_less[r] += less[r]
                        ndp_equal[r] += equal[r]
                        ndp_greater[r] += greater[r]
                else:
                    cut = x - shift

                    for r in range(cut):
                        nr = r + shift
                        ndp_less[nr] += less[r]
                        ndp_equal[nr] += equal[r]
                        ndp_greater[nr] += greater[r]

                    for r in range(cut, x):
                        nr = r - cut
                        ndp_less[nr] += less[r]
                        ndp_equal[nr] += equal[r]
                        ndp_greater[nr] += greater[r]

        for r in range(x):
            ndp_less[r] %= MOD
            ndp_equal[r] %= MOD
            ndp_greater[r] %= MOD

        less = ndp_less
        equal = ndp_equal
        greater = ndp_greater

        power = (power * 10) % x

    return (less[0] + equal[0]) % MOD

def count_leq(bound, x, valid, counts):
    if bound == '-1' or bound == '0':
        return 0

    n = len(bound)

    ans = 0

    # Every positive number with fewer digits is automatically below bound.
    for length in range(1, n):
        ans += counts[length]
        if ans >= MOD:
            ans -= MOD

    ans += boundary_count(bound, x, valid)
    return ans % MOD

def solve():
    A, B, X = input().split()
    X = int(X)
    S = input().strip()

    max_len = max(len(A), len(B))

    valid = prepare_digits(S, max_len)
    counts = exact_counts(max_len, X, valid)

    A_minus_one = dec_string(A)

    right = count_leq(B, X, valid, counts)
    left = count_leq(A_minus_one, X, valid, counts)

    print((right - left) % MOD)

if __name__ == "__main__":
    solve()
```

The first helper performs decimal subtraction without converting the value to an integer. This matters because the input can exceed the machine integer range.

`prepare_digits` precomputes the position-dependent digit restrictions. At position (1), zero remains in the list because it can be the units digit of a multi-digit number. The nonzero requirement is applied only when a digit becomes the most significant digit.

`exact_counts` is the unrestricted length DP. Its state contains only the remainder modulo (X). The initial state contains zero because a number such as (10) needs zero at position (1). From position (2) onward, the newly added leading digit is forced to be nonzero. The remainder is updated by adding the new digit times the appropriate power of ten.

The boundary DP uses the same right-to-left construction but adds three arrays for the comparison relation. The key implementation detail is that a new digit is more significant than all previously processed digits. Thus a digit smaller than the bound digit sends every previous comparison state to `less`, while a larger digit sends every state to `greater`. Only an equal digit preserves the old comparison.

The transitions use `shift` rather than constructing an integer. Since the DP is processed from right to left, adding a digit is just a cyclic shift of the remainder array. The code avoids `% X` inside the innermost transition by splitting the array at `X - shift`. This matters because the innermost loops execute millions of times.

The DP values are reduced modulo (10^9+7) once after each position rather than after every addition. During one position, at most ten previous values are added into one cell, so the temporary Python integers remain small enough for this optimization.

Finally, `count_leq(B) - count_leq(A-1)` converts the two prefix counts into the requested inclusive range. The subtraction is performed modulo (10^9+7), so a negative intermediate result is handled correctly by Python's `%` operator.

## Worked Examples

For the first sample,

```
1 20 2
1234789
```

the available digits are (1,2,3,4,7,8,9). The valid numbers in the interval are (2,4,8,12,14,18).

The important state evolution for the boundary (20) is shown below.

| Position from right | Bound digit | Possible leading digit behavior | Relevant remainder-zero numbers |
| --- | --- | --- | --- |
| 1 | 0 | Units digit can be (1,2,3,4,7,8,9), but zero is unavailable | (2,4,8) |
| 2 | 2 | Tens digit must be nonzero and coprime with (2) | (12,14,18) |
| Final | 2 | Equal state is allowed, smaller state is allowed | (2,4,8,12,14,18) |

The one-digit numbers (2,4,8) are divisible by (2). For two digits, the tens digit has to be odd because position (2) requires coprimality with (2), leaving (12,14,18) among the numbers not exceeding (20). The answer is consequently (6).

For the second sample,

```
1 20 3
0123678
```

the available digits are (0,1,2,3,6,7,8).

| Position from right | Bound digit | Position-valid digits from S | Numbers contributing to the answer |
| --- | --- | --- | --- |
| 1 | 0 | (0,1,2,3,6,7,8) | (3,6) |
| 2 | 2 | (1,2,7,8) | (12,18) |
| Final | 2 | Numbers divisible by (3) and at most (20) | (3,6,12,18) |

At position (2), digits (3) and (6) are rejected because they are not coprime with (2). The resulting valid multiples of (3) are (3,6,12,18), giving the required answer (4).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(LXD)) | There are at most (L\le101) positions, (X\le10^5) remainders, and at most (D=10) digit transitions. A constant number of DP passes handles the two boundaries. |
| Space | (O(X)) | Each DP keeps only the current and next remainder arrays. The exact-length counts require only (O(L)) additional memory. |

With (L) bounded by about one hundred and (X) bounded by (10^5), the state space is controlled by roughly (10^7) remainder-position combinations. The implementation keeps only a few arrays of length (X), so memory usage stays well below the 512 MB limit.

## Test Cases

```python
import sys
import io
from math import gcd

MOD = 1_000_000_007

def dec_string(s):
    s = s.lstrip('0') or '0'
    if s == '0':
        return '-1'

    a = list(s)
    i = len(a) - 1

    while a[i] == '0':
        a[i] = '9'
        i -= 1

    a[i] = chr(ord(a[i]) - 1)
    return ''.join(a).lstrip('0') or '0'

def solve_instance(inp: str) -> str:
    data = inp.split()
    A, B, Xs, S = data
    X = int(Xs)

    max_len = max(len(A), len(B))

    digits = [ord(c) - 48 for c in S]
    valid = [[] for _ in range(max_len + 1)]

    for p in range(1, max_len + 1):
        valid[p] = [d for d in digits if gcd(d, p) == 1]

    counts = [0] * (max_len + 1)

    dp = [0] * X
    for d in valid[1]:
        dp[d % X] += 1

    counts[1] = sum(
        1 for d in valid[1]
        if d != 0 and d % X == 0
    ) % MOD

    power = 10 % X

    for p in range(2, max_len + 1):
        ndp = [0] * X

        for d in valid[p]:
            if d == 0:
                continue

            shift = (d * power) % X

            if shift == 0:
                for r in range(X):
                    ndp[r] += dp[r]
            else:
                cut = X - shift
                for r in range(cut):
                    ndp[r + shift] += dp[r]
                for r in range(cut, X):
                    ndp[r - cut] += dp[r]

        for r in range(X):
            ndp[r] %= MOD

        dp = ndp
        counts[p] = dp[0]
        power = (power * 10) % X

    def boundary(bound):
        if bound in ('0', '-1'):
            return 0

        n = len(bound)

        less = [0] * X
        equal = [0] * X
        greater = [0] * X

        bd = int(bound[-1])

        for d in valid[1]:
            r = d % X
            if d < bd:
                less[r] += 1
            elif d == bd:
                equal[r] += 1
            else:
                greater[r] += 1

        if n == 1:
            return sum(
                1 for d in valid[1]
                if d != 0 and d <= bd and d % X == 0
            ) % MOD

        power = 10 % X

        for p in range(2, n + 1):
            nl = [0] * X
            ne = [0] * X
            ng = [0] * X

            bd = int(bound[n - p])

            for d in valid[p]:
                if d == 0:
                    continue

                shift = (d * power) % X

                if d < bd:
                    for r in range(X):
                        v = less[r] + equal[r] + greater[r]
                        nr = r + shift
                        if nr >= X:
                            nr -= X
                        nl[nr] += v

                elif d > bd:
                    for r in range(X):
                        v = less[r] + equal[r] + greater[r]
                        nr = r + shift
                        if nr >= X:
                            nr -= X
                        ng[nr] += v

                else:
                    for r in range(X):
                        nr = r + shift
                        if nr >= X:
                            nr -= X
                        nl[nr] += less[r]
                        ne[nr] += equal[r]
                        ng[nr] += greater[r]

            for r in range(X):
                nl[r] %= MOD
                ne[r] %= MOD
                ng[r] %= MOD

            less, equal, greater = nl, ne, ng
            power = (power * 10) % X

        return (less[0] + equal[0]) % MOD

    def count_leq(bound):
        if bound in ('0', '-1'):
            return 0

        n = len(bound)
        ans = sum(counts[1:n]) % MOD
        ans += boundary(bound)
        return ans % MOD

    left = count_leq(dec_string(A))
    right = count_leq(B)

    return str((right - left) % MOD)

assert solve_instance(
    "1 20 2\n1234789\n"
) == "6", "sample 1"

assert solve_instance(
    "1 20 3\n0123678\n"
) == "4", "sample 2"

assert solve_instance(
    "1 1 1\n1\n"
) == "1", "single valid number"

assert solve_instance(
    "10 10 2\n01\n"
) == "1", "zero is valid at position 1"

assert solve_instance(
    "20 20 2\n02\n"
) == "0", "digit 2 is invalid at position 2"

assert solve_instance(
    "111 111 3\n1\n"
) == "1", "equal boundaries and repeated digits"

assert solve_instance(
    "2 4 1\n1234\n"
) == "3", "inclusive boundary"

assert solve_instance(
    "1 " + "1" + "0" * 100 + " 1\n1\n"
) == "100", "maximum length"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / 1` | `1` | Minimum-size range and exact equality |
| `10 10 2 / 01` | `1` | Zero is allowed at position (1) |
| `20 20 2 / 02` | `0` | Gcd restriction at position (2) |
| `111 111 3 / 1` | `1` | Equal lower and upper bounds |
| `2 4 1 / 1234` | `3` | Inclusive range boundaries |
| `1 10^100 1 / 1` | `100` | Maximum decimal length |

## Edge Cases

For

```
10 10 2
01
```

the DP starts with both units digits (0) and (1). The zero state is retained because position (1) permits it. When position (2) is added, digit (1) is allowed and becomes the nonzero most significant digit. The resulting number is (10), whose remainder modulo (2) is zero. The answer is (1).

For

```
20 20 2
02
```

the units digit (0) is valid, but the only possible tens digit is (2). Position (2) requires (\gcd(2,2)=1), which is false, so the transition creating the tens digit (2) is never inserted into the DP. The final answer is (0).

For

```
1 1 1
1
```

the boundary DP has one position. Digit (1) is equal to the bound digit, has remainder zero modulo (1), and is nonzero. The equal state contributes one number, so the answer is (1).

For the maximum-length test

```
1 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 1
1
```

the upper bound is (10^{100}). The only permitted digit is (1), so the valid numbers are exactly the strings consisting entirely of (1), with lengths from (1) through (100). The number (10^{100}) itself contains zeroes and cannot be represented using (S). The DP records one divisible number for each of the first (100) lengths, giving (100).

## Edge Cases

The distinction between a lower-position zero and a leading zero is another source of duplicate-counting bugs. For the number (102), the zero in the middle is an actual digit at position (2), but it is invalid because (\gcd(0,2)=2). For the number (10), the zero is at position (1), where it is valid. The DP handles both situations because position validity is checked using the actual position from the right, while the nonzero restriction is applied only when a new most significant digit is introduced.

The range subtraction also handles the smallest possible lower bound correctly. If (A=1), then (A-1=0), and `count_leq(0)` returns zero because the DP counts only positive integers. Consequently the prefix difference becomes exactly the number of valid integers from (1) through (B), with no special adjustment required elsewhere.
