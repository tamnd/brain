---
title: "CF 258C - Little Elephant and LCM"
description: "We are given an array a. For every position i, we must choose an integer bi such that 1 ≤ bi ≤ ai. A sequence b is called good when its least common multiple is equal to its maximum element."
date: "2026-06-04T17:29:36+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "combinatorics", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 258
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 157 (Div. 1)"
rating: 2000
weight: 258
solve_time_s: 231
verified: true
draft: false
---

[CF 258C - Little Elephant and LCM](https://codeforces.com/problemset/problem/258/C)

**Rating:** 2000  
**Tags:** binary search, combinatorics, dp, math  
**Solve time:** 3m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array `a`. For every position `i`, we must choose an integer `b_i` such that `1 ≤ b_i ≤ a_i`.

A sequence `b` is called good when its least common multiple is equal to its maximum element.

Instead of directly counting good sequences, it is more useful to think about the value that both quantities must share. If

$$\operatorname{lcm}(b_1,\dots,b_n)=\max(b_1,\dots,b_n)=m,$$

then every chosen value must divide `m`, otherwise the LCM would become larger than `m`. At the same time, at least one position must contain exactly `m`, otherwise the maximum would be smaller than `m`.

The task is to count all valid sequences `b` satisfying the upper bounds imposed by `a`, modulo $10^9+7$.

The constraints completely determine the shape of the solution. We have up to $10^5$ positions, and every `a_i` is at most $10^5$. Any algorithm that processes positions and values together in a quadratic way is impossible. Even $10^5 \times 10^5$ operations would be far beyond the limit. The small value bound of $10^5$ is the key observation. It suggests counting how many array elements fall into value ranges and then iterating over possible maximum values.

Several edge cases are easy to mishandle.

Consider

```
1
1
```

The only possible sequence is `[1]`. Its LCM and maximum are both `1`, so the answer is `1`. Any formula involving "proper divisors" must treat `1` carefully because it has no proper positive divisors.

Consider

```
2
2 2
```

The good sequences are

```
(1,1)
(1,2)
(2,1)
(2,2)
```

for a total of `4`. A common mistake is to count only sequences whose maximum equals `2`, forgetting that maximum `1` is also possible.

Consider

```
2
1 100000
```

The first position is forced to be `1`. The second position can be many values. Any approach that assumes all positions have similar freedom will overcount. The contribution of each candidate maximum depends on how many indices can actually reach it.

## Approaches

The most direct approach is to enumerate every possible sequence `b`, compute its LCM and maximum, and check whether they match.

This is correct because it literally follows the definition. Unfortunately, even when all `a_i = 10`, there are already $10^n$ possible sequences. With $n = 10^5$, brute force is hopeless.

The next idea is to fix the common value

$$m=\operatorname{lcm}(b)=\max(b).$$

For a fixed `m`, every selected value must be a divisor of `m`. Also, at least one selected value must be exactly `m`.

Now the problem becomes counting assignments under divisor constraints.

Suppose we know all divisors of `m` in increasing order:

$$d_1 < d_2 < \dots < d_k=m.$$

For a position whose limit is `x`, the number of allowed choices equals the number of divisors of `m` that do not exceed `x`.

This converts the problem into a product of counts.

The remaining challenge is evaluating these products efficiently for every `m ≤ 100000`.

The crucial observation is that the count of divisors not exceeding `x` changes only when `x` crosses a divisor of `m`.

If

$$d_r \le x < d_{r+1},$$

then exactly `r` divisors of `m` are available.

Instead of processing every array position separately, we count how many `a_i` fall into each interval between consecutive divisors. Since all values are at most `100000`, a prefix-frequency array lets us obtain these counts in constant time.

The total number of divisor appearances among all integers up to `100000` is

$$\sum_{i=1}^{100000}\tau(i)\approx 1.17\times10^6,$$

which is easily manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in `n` | O(n) | Too slow |
| Optimal | O(M log M) where `M = max(a)` | O(M log M) | Accepted |

## Algorithm Walkthrough

1. Read the array and compute a frequency table of values.
2. Build a prefix-count array `pref`, where `pref[x]` equals the number of indices with `a_i ≤ x`.
3. Precompute the divisor list for every integer up to `100000` using a divisor sieve.
4. Let `m` be the candidate value of both the LCM and the maximum.
5. Obtain the sorted divisors of `m`:

$$d_1<d_2<\dots<d_k=m.$$
6. For every interval

$$[d_r,\ d_{r+1}-1],$$

count how many array elements fall inside it:

$$E_r = \text{pref}[d_{r+1}-1] - \text{pref}[d_r-1].$$

Every such position has exactly `r` available divisors of `m`.
7. Multiply

$$\prod_{r=1}^{k-1} r^{E_r}.$$

This counts choices for all positions whose upper bounds are below `m`.
8. Let

$$C=n-\text{pref}[m-1].$$

These are exactly the positions with `a_i ≥ m`.

Each of them may use any of the `k` divisors of `m`.
9. Among those assignments, subtract the ones that never use the divisor `m`.

The number of valid assignments is

$$k^C-(k-1)^C.$$

This is a standard inclusion-exclusion step.
10. Multiply the result of step 7 by the result of step 9 and add it to the global answer.
11. Repeat for every `m` from `1` to `100000`.

### Why it works

Fix a value `m`.

Every good sequence whose LCM and maximum equal `m` must satisfy two conditions. Every element must divide `m`, otherwise the LCM exceeds `m`. At least one element must equal `m`, otherwise the maximum is smaller than `m`.

The interval decomposition counts exactly how many divisors of `m` are available at each position. The product over intervals counts all assignments using divisors of `m`. The factor

$$k^C-(k-1)^C$$

keeps precisely those assignments where at least one position uses the divisor `m`.

Every good sequence contributes to exactly one value of `m`, namely its common LCM and maximum. Different values of `m` generate disjoint sets of sequences. Summing all contributions counts every good sequence exactly once.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

MOD = 1000000007
MAXV = 100000

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    freq = [0] * (MAXV + 1)
    for x in a:
        freq[x] += 1

    pref = [0] * (MAXV + 1)
    for i in range(1, MAXV + 1):
        pref[i] = pref[i - 1] + freq[i]

    divisors = [[] for _ in range(MAXV + 1)]
    for d in range(1, MAXV + 1):
        for multiple in range(d, MAXV + 1, d):
            divisors[multiple].append(d)

    max_tau = max(len(divisors[i]) for i in range(1, MAXV + 1))

    pw = [None] * (max_tau + 1)
    pw[0] = array('I', [0] * (n + 1))

    for base in range(1, max_tau + 1):
        arr = array('I', [0] * (n + 1))
        arr[0] = 1
        for e in range(1, n + 1):
            arr[e] = (arr[e - 1] * base) % MOD
        pw[base] = arr

    ans = 0

    for m in range(1, MAXV + 1):
        ds = divisors[m]
        k = len(ds)

        cur = 1

        for r in range(1, k):
            left = ds[r - 1]
            right = ds[r] - 1

            cnt = pref[right] - pref[left - 1]
            cur = (cur * pw[r][cnt]) % MOD

        c = n - pref[m - 1]

        add = pw[k][c]
        if k > 1:
            add -= pw[k - 1][c]

        cur = (cur * add) % MOD
        ans += cur

    print(ans % MOD)

if __name__ == "__main__":
    solve()
```

The frequency array and prefix array allow us to answer range-count queries in constant time. Every interval between consecutive divisors becomes a simple subtraction of two prefix values.

The divisor sieve is the standard

$$O(M \log M)$$

construction. Each integer is inserted into the divisor list of its multiples.

The power table is indexed by divisor rank rather than by value. The number of divisors of any number up to `100000` never exceeds `128`, so only a small number of bases must be precomputed. This avoids performing more than a million modular exponentiations inside the main loop.

The most delicate part is the factor

$$k^C-(k-1)^C.$$

It counts assignments where at least one position uses the divisor `m`. Forgetting this subtraction counts many sequences whose maximum is actually smaller than `m`.

Another subtle case is `m = 1`. Then `k = 1`, and the subtraction term should be zero. The code handles this separately.

## Worked Examples

### Sample 1

Input:

```
4
1 4 3 2
```

After sorting conceptually, the upper bounds are distributed as:

| Value | Count |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |

For `m = 2`:

Divisors are `[1, 2]`.

| Interval | Available divisor count | Elements in interval |
| --- | --- | --- |
| [1,1] | 1 | 1 |
| ≥ 2 | handled by C | 3 |

Thus

$$1^1 \cdot (2^3-1^3)=7.$$

For `m = 3`:

| Interval | Available divisor count | Elements |
| --- | --- | --- |
| [1,2] | 1 | 2 |
| ≥ 3 | handled by C | 2 |

Contribution:

$$1^2 \cdot (2^2-1^2)=3.$$

For `m = 4`:

Divisors `[1,2,4]`.

| Interval | Count |
| --- | --- |
| [1,1] | 1 |
| [2,3] | 2 |
| ≥4 | 1 |

Contribution:

$$1^1\cdot2^2\cdot(3^1-2^1)=4.$$

Adding all contributions gives `15`.

This example demonstrates that different values of `m` contribute independently and are simply summed.

### Example 2

Input:

```
2
2 2
```

For `m = 1`:

| Quantity | Value |
| --- | --- |
| C | 2 |
| Contribution | $1^2 = 1$ |

For `m = 2`:

| Quantity | Value |
| --- | --- |
| C | 2 |
| Contribution | $2^2-1^2=3$ |

Total answer:

$$1+3=4.$$

The four counted sequences are exactly

```
(1,1)
(1,2)
(2,1)
(2,2)
```

which confirms the inclusion-exclusion step.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M log M) | Divisor sieve plus processing all divisor occurrences |
| Space | O(M log M) | Storage of divisor lists and power tables |

Here `M = 100000`.

The total number of divisor occurrences up to `100000` is roughly `1.17 million`, which keeps the main loop comfortably within the limits. The memory usage also fits within the 256 MB constraint.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    from array import array

    MOD = 1000000007
    MAXV = 100000

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    freq = [0] * (MAXV + 1)
    for x in a:
        freq[x] += 1

    pref = [0] * (MAXV + 1)
    for i in range(1, MAXV + 1):
        pref[i] = pref[i - 1] + freq[i]

    divisors = [[] for _ in range(MAXV + 1)]
    for d in range(1, MAXV + 1):
        for m in range(d, MAXV + 1, d):
            divisors[m].append(d)

    max_tau = max(len(divisors[i]) for i in range(1, MAXV + 1))

    pw = [None] * (max_tau + 1)
    pw[0] = array('I', [0] * (n + 1))

    for base in range(1, max_tau + 1):
        arr = array('I', [0] * (n + 1))
        arr[0] = 1
        for e in range(1, n + 1):
            arr[e] = (arr[e - 1] * base) % MOD
        pw[base] = arr

    ans = 0

    for m in range(1, MAXV + 1):
        ds = divisors[m]
        k = len(ds)

        cur = 1

        for r in range(1, k):
            cnt = pref[ds[r] - 1] - pref[ds[r - 1] - 1]
            cur = (cur * pw[r][cnt]) % MOD

        c = n - pref[m - 1]

        add = pw[k][c]
        if k > 1:
            add -= pw[k - 1][c]

        ans = (ans + cur * add) % MOD

    return str(ans) + "\n"

# provided sample
assert run("4\n1 4 3 2\n") == "15\n"

# minimum size
assert run("1\n1\n") == "1\n"

# all equal
```
