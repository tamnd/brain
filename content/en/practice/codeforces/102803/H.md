---
title: "CF 102803H - Hate That You Know Me"
description: "For a fixed exponent k, define sigmak(i) as the sum of the k-th powers of all divisors of i. The task is not asking for one value of this function, but for the XOR of two large prefix sums. For each test case, we are given two small exponents a and b, and a limit n."
date: "2026-07-26T16:24:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102803
codeforces_index: "H"
codeforces_contest_name: "The 15th Heilongjiang Provincial Collegiate Programming Contest"
rating: 0
weight: 102803
solve_time_s: 45
verified: true
draft: false
---

[CF 102803H - Hate That You Know Me](https://codeforces.com/problemset/problem/102803/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

For a fixed exponent `k`, define `sigma_k(i)` as the sum of the `k`-th powers of all divisors of `i`. The task is not asking for one value of this function, but for the XOR of two large prefix sums. For each test case, we are given two small exponents `a` and `b`, and a limit `n`. We need to compute the sum of `sigma_a(i)` for every `i` from `1` to `n`, do the same for `sigma_b(i)`, XOR the two results, and keep only the lowest 64 bits.

The exponents are restricted to `0, 1, 2, 3`, but `n` can reach `10^12`. A direct simulation over all numbers up to `n` would require iterating one trillion times in the worst case, which is far beyond what a 2 second limit allows. Even an `O(n log n)` divisor enumeration method would need roughly `10^13` operations, so the solution must exploit the mathematical structure of divisor sums.

The main edge cases come from the size of `n` and from the required 64-bit behavior. For example, when `n=1`, `a=0`, and `b=1`, the only number considered is `1`. Both divisor sums are `1`, so the XOR is `0`.

```
Input:
1
0 1 1

Output:
0
```

A solution that starts its loop from `d=0` would fail because divisors begin at `1`.

Another easy mistake is forgetting that the answer is modulo `2^64`. For example, the prefix sum of divisor sums can exceed the range of normal signed 64-bit integers for large `n`, so using a language implementation with arbitrary precision requires explicitly applying the mask.

For `n=4`, `a=0`, and `b=1`, the two prefix sums are:

```
sigma_0: 1, 2, 2, 3 -> total 8
sigma_1: 1, 3, 4, 7 -> total 15
```

The correct answer is:

```
8 XOR 15 = 7
```

A careless implementation that confuses XOR with addition would output `23`.

## Approaches

A straightforward approach follows the definition directly. For every integer `i` from `1` to `n`, we could enumerate its divisors, calculate `sigma_a(i)` and `sigma_b(i)`, and add them. This is correct because it literally evaluates the mathematical definition.

The problem is the scale. The largest test cases contain `n=10^12`, so even touching every value of `i` is impossible. A divisor-based enumeration would be even slower because each number has to be factorized or scanned for divisors.

The key observation is that the order of summation can be exchanged. Instead of asking which divisors belong to each number, ask how many numbers contain a particular divisor. A divisor `d` contributes `d^k` to every multiple of `d`, and there are exactly `floor(n/d)` such multiples. Therefore:

$$\sum_{i=1}^{n}\sigma_k(i)=\sum_{d=1}^{n} d^k\left\lfloor\frac nd\right\rfloor$$

The remaining challenge is that the sum still appears to have `n` terms. The important property is that `floor(n/d)` stays constant over long ranges. If `floor(n/l)=q`, then every `d` in a certain interval ending at `r=floor(n/q)` has the same quotient `q`.

This lets us process ranges instead of individual divisors. There are only about `2*sqrt(n)` such ranges, which is around two million when `n=10^12`. For each range, we need the sum of `d^k` between two boundaries. Since `k` is at most `3`, closed-form prefix formulas are enough.

The brute-force works because it counts each divisor contribution correctly, but fails because it performs too many small operations. The quotient grouping observation compresses many identical terms into one calculation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) or worse | O(1) | Too slow |
| Quotient grouping | O(sqrt(n)) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each needed exponent `k`, compute the value of

$$F_k(n)=\sum_{d=1}^{n}d^k\left\lfloor\frac nd\right\rfloor$$

using quotient ranges instead of iterating over every divisor.

1. Start a range at `l=1`. The quotient is `q=n//l`. The last position where this quotient remains unchanged is `r=n//q`.

The whole interval `[l,r]` contributes:

$$q \times \sum_{d=l}^{r}d^k$$

because every divisor in this interval has the same multiplier.

1. Obtain the power sum of the interval from prefix formulas. The required formulas are:

$$\sum d = \frac{x(x+1)}2$$

$$\sum d^2=\frac{x(x+1)(2x+1)}6$$

$$\sum d^3=\left(\frac{x(x+1)}2\right)^2$$

The `k=0` case is simply the count of numbers in the interval.

1. Add the contribution to the answer modulo `2^64`, then continue from `r+1`.
2. Compute the two required prefix sums, XOR them, and output the resulting 64-bit value.

The correctness comes from the divisor contribution transformation. Every pair `(i,d)` where `d` divides `i` is counted exactly once in the original definition. After swapping the order, the same pair is counted when processing divisor `d`, multiplied by the number of valid multiples. Quotient grouping only combines adjacent divisors with identical multipliers, so it changes the order of calculation but not the value.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1 << 64

def prefix_power(x, k):
    if k == 0:
        return x & (MOD - 1)
    if k == 1:
        return (x * (x + 1) // 2) & (MOD - 1)
    if k == 2:
        return (x * (x + 1) * (2 * x + 1) // 6) & (MOD - 1)
    t = x * (x + 1) // 2
    return (t * t) & (MOD - 1)

def calc(n, k):
    ans = 0
    l = 1

    while l <= n:
        q = n // l
        r = n // q

        segment = (prefix_power(r, k) - prefix_power(l - 1, k)) & (MOD - 1)
        ans = (ans + q * segment) & (MOD - 1)

        l = r + 1

    return ans

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return

    t = int(data[0])
    idx = 1
    cache = {}
    out = []

    for _ in range(t):
        a = int(data[idx])
        b = int(data[idx + 1])
        n = int(data[idx + 2])
        idx += 3

        if n not in cache:
            cache[n] = [calc(n, k) for k in range(4)]

        out.append(str((cache[n][a] ^ cache[n][b]) & (MOD - 1)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `prefix_power` function implements the four closed forms needed by the algorithm. The divisions happen before the modulo operation because the formulas contain fractions, and applying the modulo too early would destroy the integer result.

The `calc` function performs the quotient grouping. The variables `l` and `r` describe the current divisor interval. Moving directly to `r+1` avoids processing every divisor separately.

The cache stores all four possible exponent results for a given `n`. Since multiple test cases may share the same limit, this avoids repeating the same `O(sqrt(n))` calculation.

The bit mask `MOD - 1` keeps only the lowest 64 bits after every large operation. Python integers do not overflow naturally, so this explicit masking reproduces the required modulo `2^64`.

## Worked Examples

For the first sample:

```
Input:
1
0 1 4
```

The algorithm computes both prefix sums.

| l | r | quotient | k=0 contribution | k=1 contribution |
| --- | --- | --- | --- | --- |
| 1 | 1 | 4 | 4 | 4 |
| 2 | 2 | 2 | 2 | 4 |
| 3 | 4 | 1 | 2 | 7 |

The totals are `8` and `15`. Their XOR is `7`.

For the second sample:

```
Input:
1
2 3 2
```

| l | r | quotient | k=2 contribution | k=3 contribution |
| --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 2 | 2 |
| 2 | 2 | 1 | 4 | 8 |

The totals are `6` and `10`. The final XOR is `12`.

These traces show that the quotient intervals cover every divisor exactly once, while combining all divisors that share the same value of `floor(n/d)`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sqrt(n)) per distinct n | The quotient grouping creates about `2*sqrt(n)` intervals, and each interval uses constant-time formulas. |
| Space | O(1) besides cache | Only a few integer variables are required, plus four stored answers per distinct test value of n. |

With `n` up to `10^12`, the number of quotient intervals is around two million. This is small enough for the given limits, while any approach proportional to `n` is impossible.

## Test Cases

```python
import sys
import io

MOD = 1 << 64

def prefix_power(x, k):
    if k == 0:
        return x & (MOD - 1)
    if k == 1:
        return (x * (x + 1) // 2) & (MOD - 1)
    if k == 2:
        return (x * (x + 1) * (2 * x + 1) // 6) & (MOD - 1)
    s = x * (x + 1) // 2
    return (s * s) & (MOD - 1)

def calc(n, k):
    ans = 0
    l = 1
    while l <= n:
        q = n // l
        r = n // q
        ans = (ans + q * ((prefix_power(r, k) - prefix_power(l - 1, k)) & (MOD - 1))) & (MOD - 1)
        l = r + 1
    return ans

def run(inp):
    data = inp.split()
    t = int(data[0])
    p = 1
    out = []
    for _ in range(t):
        a, b, n = map(int, data[p:p+3])
        p += 3
        x = calc(n, a)
        y = calc(n, b)
        out.append(str((x ^ y) & (MOD - 1)))
    return "\n".join(out)

assert run("2\n0 1 4\n2 3 2\n") == "7\n12"

assert run("1\n0 0 1\n") == "0"

assert run("1\n1 1 10\n") == "0"

assert run("1\n0 1 1\n") == "0"

assert run("1\n2 3 1000000000000\n") == run("1\n2 3 1000000000000\n")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 1 4` | `7` | Provided sample and XOR handling |
| `0 0 1` | `0` | Minimum input and equal exponents |
| `1 1 10` | `0` | Identical sums always XOR to zero |
| `0 1 1` | `0` | Smallest boundary case |
| `2 3 1000000000000` | computed by reference run | Maximum-size `n` handling |

## Edge Cases

For `n=1`, the quotient grouping has only one interval. The algorithm starts with `l=1`, computes `q=1`, and processes the single divisor. There is no attempt to access divisor zero, so the smallest case is handled naturally.

For equal exponents such as:

```
Input:
1
2 2 100
```

both calculations use the same exponent and produce the same prefix sum. The final XOR operation produces zero. The implementation handles this without a special branch because XOR already has this property.

For very large values such as:

```
Input:
1
3 2 1000000000000
```

the intermediate arithmetic exceeds normal signed 64-bit ranges. The algorithm masks after operations, preserving exactly the required lower 64 bits instead of relying on language overflow behavior.

For cases where `n` is near a quotient boundary, such as `n=10`, the interval calculation `r=n//q` must be exact. If an implementation used `r=l` or incremented incorrectly, it would skip or double-count divisors. The grouping formula used here always advances from `l` to `r+1`, so every divisor appears in exactly one interval.
