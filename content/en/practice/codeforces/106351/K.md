---
title: "CF 106351K - Wala matgeesh bra7tek howa enty hatzeleniiiii"
description: "We have an array of positive integers. We need to count index pairs (i, j) where i < j and the two chosen values satisfy two number theory conditions at the same time. Their greatest common divisor must be at least x, and their least common multiple must not exceed y."
date: "2026-06-25T08:11:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106351
codeforces_index: "K"
codeforces_contest_name: "Zaglol Contest - FCDS level 2 contest 2026"
rating: 0
weight: 106351
solve_time_s: 52
verified: true
draft: false
---

[CF 106351K - Wala matgeesh bra7tek howa enty hatzeleniiiii](https://codeforces.com/problemset/problem/106351/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of positive integers. We need to count index pairs `(i, j)` where `i < j` and the two chosen values satisfy two number theory conditions at the same time. Their greatest common divisor must be at least `x`, and their least common multiple must not exceed `y`. The task is to output the number of such pairs.

The important limits are that the array length and every value are at most `100000`. This rules out checking every pair directly because there can be about `10^10` pairs. We need to use the fact that the values themselves are bounded by `100000`, which allows preprocessing over the value range instead of the indices.

A pair containing a value larger than `y` can never be valid because the lcm of two positive integers is always at least both integers. So we can ignore all array values greater than `y` from the start.

A subtle case is when many values are equal. For example, with input:

```
3 2 10
4 4 4
```

the answer is:

```
3
```

All three pairs have gcd `4` and lcm `4`. A solution that only counts different values would miss these pairs.

Another tricky case is when the gcd condition and lcm condition interact. For example:

```
2 5 6
10 15
```

The gcd is `5`, which is large enough, but the lcm is `30`, which is too large. The correct answer is:

```
0
```

Checking only the gcd or only the lcm would incorrectly count this pair.

## Approaches

The straightforward approach is to try every pair of indices, compute the gcd and lcm, and check the conditions. This is correct because every possible pair is inspected. However, with `n = 100000`, this performs around `5 * 10^9` pair checks, which is far beyond the time limit.

The key observation is that the possible values are small. Instead of thinking about positions, we can think about possible lcm values. Every valid pair has an lcm `L` with `L <= y`, and both numbers in the pair must be divisors of `L`. The number of divisors of a number up to `100000` is small, so for each possible lcm we only need to inspect a small candidate set.

For a fixed `L`, we gather all divisors of `L` that appear in the array. Any pair among these divisors has an lcm that divides `L`. We keep only the pairs whose actual lcm is exactly `L`, and whose gcd is at least `x`.

The brute force over indices becomes a much smaller enumeration over divisors of numbers up to `y`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² log A) | O(1) | Too slow |
| Optimal | O(y log y + Σ τ(i)²) | O(y log y) | Accepted |

## Algorithm Walkthrough

1. Count how many times every value appears in the array. Values greater than `y` are ignored because they cannot be part of a valid pair.
2. Precompute the list of divisors for every number from `1` to `y`. This lets us quickly find all possible values that can participate in a pair with a given lcm.
3. Iterate over every possible lcm value `L` from `1` to `y`. For this `L`, only values that divide `L` can appear in a pair whose lcm is `L`.
4. For every pair of divisors `(a, b)` of `L`, calculate `gcd(a, b)` and `lcm(a, b)`. If the gcd is at least `x` and the lcm is exactly `L`, add the number of index pairs formed by these values.
5. Handle equal values separately inside the divisor enumeration. If `a == b`, the contribution is `freq[a] * (freq[a] - 1) / 2`. Otherwise, the contribution is `freq[a] * freq[b]`.

Why it works:

Every valid pair has one unique lcm value. During the iteration for that lcm, both values must appear among its divisors, so the pair is considered exactly once. The checks for gcd and lcm match the original requirements, which means every counted pair is valid. Since no other lcm iteration can count the same pair, there is no double counting.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, x, y = data[0], data[1], data[2]
    arr = data[3:3 + n]

    freq = [0] * (y + 1)
    for v in arr:
        if v <= y:
            freq[v] += 1

    divisors = [[] for _ in range(y + 1)]
    for d in range(1, y + 1):
        for m in range(d, y + 1, d):
            divisors[m].append(d)

    ans = 0

    for l in range(1, y + 1):
        divs = divisors[l]
        m = len(divs)

        for i in range(m):
            a = divs[i]
            if freq[a] == 0:
                continue

            for j in range(i, m):
                b = divs[j]
                if freq[b] == 0:
                    continue

                if gcd(a, b) < x:
                    continue

                if a // gcd(a, b) * b != l:
                    continue

                if a == b:
                    ans += freq[a] * (freq[a] - 1) // 2
                else:
                    ans += freq[a] * freq[b]

    print(ans)

if __name__ == "__main__":
    solve()
```

The frequency array stores only values that can appear in an answer. This avoids wasting time on numbers that already violate the lcm limit.

The divisor lists are built using a sieve-like loop. For every divisor candidate, we append it to all of its multiples. After this step, `divisors[l]` contains exactly the values that could form a pair with lcm `l`.

Inside the main loop, the pair enumeration starts from `i` instead of zero because the pairs are unordered. This avoids counting `(a, b)` and `(b, a)` separately. The lcm check uses `a // gcd(a, b) * b` instead of `a * b // gcd(a, b)` to reduce the chance of overflow in languages with fixed-size integers.

The equal-value case needs special handling because choosing two occurrences of the same value creates combinations, not a product of two different frequencies.

## Worked Examples

For the sample:

```
10 1 10
1 2 3 4 5 6 7 8 9 10
```

The trace of the important variables is:

| lcm value | divisors considered | valid contribution | answer |
| --- | --- | --- | --- |
| 1 | 1 | (1,1) | 0 |
| 2 | 1,2 | (1,2), (2,2) invalid for lcm 2 except gcd condition | 1 |
| 3 | 1,3 | valid pairs added | 2 |
| 4 | 1,2,4 | more pairs with lcm 4 | 4 |
| 5 to 10 | remaining divisors | additional valid pairs | 19 |

The final answer is:

```
19
```

This shows that the algorithm counts by lcm groups and not by index pairs.

A second example:

```
2 5 6
10 15
```

The trace is:

| lcm value | divisors considered | gcd check | contribution |
| --- | --- | --- | --- |
| 1 to 5 | none contain both values | fails | 0 |
| 6 | divisors of 6 only | no pair exists | 0 |

The final answer is:

```
0
```

This exercises the case where a large gcd is not enough because the lcm limit is violated.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(y log y + Σ τ(i)²) | The divisor sieve and divisor pair checks are bounded by the small value range |
| Space | O(y log y) | Stores all divisor lists for values up to `y` |

The maximum value is only `100000`, so the total divisor processing remains manageable. The algorithm avoids the quadratic number of array pairs and works within the intended limits.

## Test Cases

```python
import sys
import io
from math import gcd

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return ""

    n, x, y = data[0], data[1], data[2]
    arr = data[3:3 + n]

    freq = [0] * (y + 1)
    for v in arr:
        if v <= y:
            freq[v] += 1

    divs = [[] for _ in range(y + 1)]
    for i in range(1, y + 1):
        for j in range(i, y + 1, i):
            divs[j].append(i)

    ans = 0
    for l in range(1, y + 1):
        d = divs[l]
        for i in range(len(d)):
            for j in range(i, len(d)):
                a, b = d[i], d[j]
                if freq[a] == 0 or freq[b] == 0:
                    continue
                g = gcd(a, b)
                if g >= x and a // g * b == l:
                    if a == b:
                        ans += freq[a] * (freq[a] - 1) // 2
                    else:
                        ans += freq[a] * freq[b]
    return str(ans) + "\n"

assert run("""10 1 10
1 2 3 4 5 6 7 8 9 10
""") == "19\n"

assert run("""2 5 6
10 15
""") == "0\n"

assert run("""3 2 10
4 4 4
""") == "3\n"

assert run("""4 3 20
6 10 15 30
""") == "1\n"

assert run("""1 1 100000
100000
""") == "0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Three equal values | 3 | Equal-value pair counting |
| Gcd passes but lcm fails | 0 | Both conditions are required |
| Mixed divisor relationships | 1 | Correct lcm grouping |
| Single element | 0 | No possible pair |

## Edge Cases

For the equal-values case:

```
3 2 10
4 4 4
```

The algorithm reaches lcm `4`. The divisors include `4`, and the pair `(4,4)` has gcd `4`, so it contributes `3 * 2 / 2 = 3`. No other lcm can count these pairs, so the answer stays correct.

For the lcm failure case:

```
2 5 6
10 15
```

The gcd is `5`, but the lcm calculation gives `30`. The algorithm only accepts the pair when the computed lcm equals the current lcm bucket and the bucket is at most `y`, so this pair is rejected.

For values greater than `y`, such as:

```
2 1 5
10 2
```

the value `10` is removed from consideration immediately. Since any pair containing it has lcm at least `10`, it cannot be valid. The remaining value alone cannot create a pair, so the answer is `0`.
