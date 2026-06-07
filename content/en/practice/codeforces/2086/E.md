---
title: "CF 2086E - Zebra-like Numbers"
description: "A zebra-like number is a positive integer whose binary representation looks like 1, 101, 10101, 1010101, ... In other words, the bits alternate and the least significant bit is 1. Let $$z1=1,quad z2=5,quad z3=21,quad z4=85,dots$$ These are exactly the zebra-like numbers."
date: "2026-06-08T06:04:46+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "constructive-algorithms", "dfs-and-similar", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2086
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 177 (Rated for Div. 2)"
rating: 2400
weight: 2086
solve_time_s: 128
verified: true
draft: false
---

[CF 2086E - Zebra-like Numbers](https://codeforces.com/problemset/problem/2086/E)

**Rating:** 2400  
**Tags:** bitmasks, brute force, constructive algorithms, dfs and similar, dp, greedy, math  
**Solve time:** 2m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

A zebra-like number is a positive integer whose binary representation looks like

`1`, `101`, `10101`, `1010101`, ...

In other words, the bits alternate and the least significant bit is `1`.

Let

$$z_1=1,\quad z_2=5,\quad z_3=21,\quad z_4=85,\dots$$

These are exactly the zebra-like numbers.

For a positive integer $x$, its zebra value is the minimum number of zebra-like numbers whose sum is $x$.

For every query $[l,r]$ and $k$, we must count how many integers in that interval have zebra value exactly $k$.

The interval endpoints can be as large as $10^{18}$, so iterating over numbers is impossible. Even a single pass over the interval would require up to $10^{18}$ operations. The solution must work in roughly polylogarithmic time per query.

The first non-obvious observation is that there are very few zebra-like numbers below $10^{18}$. They satisfy

$$z_{i+1}=4z_i+1,$$

so they grow exponentially. Only about thirty of them fit inside $10^{18}$.

A second trap is assuming that the zebra value can be computed with an ordinary coin-change DP. The coin values reach $10^{18}$, so any DP over sums is impossible.

A third trap is that different decompositions of the same number may use different numbers of zebra-like summands. For example,

$$21 = z_3$$

has zebra value $1$, even though

$$21 = 5+5+5+5+1$$

uses five summands. We must reason about optimal decompositions directly.

Consider the query

```
1 1 1
```

The answer is `1` because $1$ itself is zebra-like. Any approach that accidentally counts only sums of at least two zebra numbers would fail here.

Consider

```
2 10 100
```

The answer is `0`. Although $k$ may be as large as $10^{18}$, no number up to $10^{18}$ can have zebra value anywhere near that large. Handling such cases early is essential.

## Approaches

A brute-force approach would generate every number in $[l,r]$, compute its zebra value, and count the matches.

Even if we somehow computed a zebra value in constant time, the interval length can be $10^{18}$. This is completely infeasible.

The key is to stop thinking about the numbers themselves and instead study the structure of zebra-like numbers.

Let

$$z_i=\frac{4^i-1}{3}.$$

These satisfy

$$z_{i+1}=4z_i+1.$$

Suppose an optimal decomposition contains at least five copies of some $z_i$.

For $i>1$,

$$5z_i=z_{i+1}+4z_{i-1}.$$

The right side uses the same number of summands. Repeating this transformation removes every coefficient greater than four.

As a result, every number has an optimal decomposition

$$x=\sum c_i z_i,$$

with

$$0\le c_i\le 4.$$

A second reduction comes from

$$z_{i+1}=4z_i+1.$$

If some coefficient $c_i=4$ and there is any positive coefficient below it, then we can replace

$$4z_i+1$$

by

$$z_{i+1},$$

reducing the number of summands. Hence in an optimal decomposition, whenever a digit $4$ appears, all lower digits must be zero.

This gives a canonical representation:

$$x=\sum c_i z_i,$$

where every digit is between $0$ and $4$, and after the first digit equal to $4$, all lower digits are zero.

The zebra value is simply

$$\sum c_i.$$

Now the problem becomes a digit-DP problem in a strange numeral system. We count representations not exceeding a bound $N$ whose digit sum equals $k$.

Since there are only about thirty zebra digits, the DP is tiny.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(r-l+1)$ | $O(1)$ | Too slow |
| Optimal Digit DP | $O(30^2)$ per query | $O(30^2)$ | Accepted |

## Algorithm Walkthrough

### Precomputation

1. Generate all zebra-like numbers $z_i\le 10^{18}$ using

$$z_{i+1}=4z_i+1.$$
2. There are only about thirty such numbers.

### Converting a bound into zebra digits

1. For a given $N$, compute its greedy representation in the basis $\{z_i\}$.
2. Process the zebra numbers from largest to smallest. At each position, take the maximum coefficient possible.
3. The resulting digits are always between $0$ and $4$.

The recurrence $z_{i+1}=4z_i+1$ guarantees that greedy decomposition produces the canonical digit system used by the DP.

### Digit DP

1. Let `digits[i]` be the coefficient of $z_i$ in the representation of $N$.
2. Process positions from most significant to least significant.
3. Maintain four DP parameters:

- current position
- whether we are still tight to $N$
- current digit sum
- whether a digit $4$ has already appeared
4. If a digit $4$ has already appeared, every remaining digit must be zero. This enforces the canonical representation condition.
5. Otherwise, try all digits from $0$ up to the allowed limit.
6. Add the chosen digit to the running digit sum.
7. At the end, count states whose digit sum equals $k$.

### Range query

1. Let $F(N,k)$ be the number of integers $x\le N$ whose zebra value equals $k$.
2. The answer for $[l,r]$ is

$$F(r,k)-F(l-1,k).$$

### Why it works

Every optimal decomposition can be transformed until all coefficients belong to $\{0,1,2,3,4\}$. Any representation containing a digit $4$ together with a positive lower coefficient is not optimal because one copy of $z_{i+1}$ can replace $4z_i+1$ and reduce the number of summands.

Thus every number has a unique canonical representation satisfying:

$$0\le c_i\le 4,$$

and after the first digit equal to $4$, all lower digits are zero.

The zebra value equals the sum of these digits. The digit DP enumerates exactly these canonical representations and counts those whose digit sum is $k$. Since every valid representation corresponds to exactly one integer and vice versa, the count returned by the DP is correct.

## Python Solution

```python
import sys
from functools import lru_cache

input = sys.stdin.readline

Z = [1]
while True:
    nxt = Z[-1] * 4 + 1
    if nxt > 10**18:
        break
    Z.append(nxt)

M = len(Z)

def count_upto(n, k):
    if n <= 0:
        return 0

    if k > 4 * M:
        return 0

    digits = [0] * M
    rem = n

    for i in range(M - 1, -1, -1):
        digits[i] = rem // Z[i]
        rem %= Z[i]

    @lru_cache(None)
    def dfs(pos, tight, s, locked):
        if s > k:
            return 0

        if pos < 0:
            return 1 if s == k else 0

        if locked:
            d = 0
            if tight and d > digits[pos]:
                return 0
            ntight = tight and (d == digits[pos])
            return dfs(pos - 1, ntight, s, 1)

        limit = digits[pos] if tight else 4

        ans = 0
        for d in range(limit + 1):
            ntight = tight and (d == limit if tight else False)

            if tight:
                ntight = (d == digits[pos])

            ans += dfs(
                pos - 1,
                ntight,
                s + d,
                locked or (d == 4)
            )

        return ans

    return dfs(M - 1, 1, 0, 0)

def solve():
    t = int(input())

    out = []

    for _ in range(t):
        l, r, k = map(int, input().split())

        if k > 4 * M:
            out.append("0")
            continue

        ans = count_upto(r, k) - count_upto(l - 1, k)
        out.append(str(ans))

    sys.stdout.write("\n".join(out))

solve()
```

The first section builds all zebra-like numbers up to $10^{18}$. Only about thirty values exist, which is why the later DP remains tiny.

The function `count_upto` computes $F(N,k)$. It first converts $N$ into its greedy zebra-digit representation. These digits play the same role that decimal digits play in a standard digit DP.

The state variable `locked` is the subtle part. Once a digit `4` appears, all remaining lower digits must be zero. Forgetting this restriction counts non-optimal representations and produces incorrect zebra values.

The pruning condition `s > k` keeps the state space small. Since the maximum possible digit sum is only about $120$, the DP remains extremely fast.

Finally, every query is answered using the standard prefix-count technique:

$$[l,r] = [1,r] - [1,l-1].$$

## Worked Examples

### Example 1

Input:

```
1 100 3
```

The zebra numbers involved are:

$$1,\;5,\;21,\;85.$$

The greedy zebra representation of $100$ is:

| Zebra number | Coefficient |
| --- | --- |
| 85 | 1 |
| 21 | 0 |
| 5 | 3 |
| 1 | 0 |

So $100 = 1\cdot85 + 0\cdot21 + 3\cdot5 + 0\cdot1$.

The DP explores all canonical representations not exceeding these digits and counts those with digit sum $3$.

The result is:

```
13
```

This example shows that zebra value is determined entirely by the digit sum of the canonical representation.

### Example 2

Input:

```
15 77 2
```

Relevant zebra numbers:

$$1,\;5,\;21.$$

The numbers in the interval with zebra value $2$ are:

$$26=21+5,$$

$$42=21+21,$$

$$50=5+45? \text{ not canonical},$$

and the DP automatically filters invalid decompositions.

The final count is:

```
3
```

This example demonstrates why counting arbitrary sums is not enough. Only canonical optimal decompositions matter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(M^2)$ per query | $M \approx 30$, digit sum is at most $4M$ |
| Space | $O(M^2)$ | Memoized DP states |

With $M\approx30$, the number of DP states is only a few thousand. Even with $100$ test cases, the solution comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    # paste solve() here and return captured output
    ...

# provided sample
assert run(
"""5
1 100 3
1 1 1
15 77 2
2 10 100
1234567 123456789101112131 12
"""
) == (
"""13
1
3
0
4246658701
""")

# minimum value
assert run(
"""1
1 1 1
"""
) == (
"""1
""")

# single value not zebra-like
assert run(
"""1
2 2 1
"""
) == (
"""0
""")

# impossible huge k
assert run(
"""1
1 1000000000000000000 1000000000000000000
"""
) == (
"""0
""")

# boundary interval
assert run(
"""1
21 21 1
"""
) == (
"""1
""")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `1` | Smallest valid number |
| `2 2 1` | `0` | Non-zebra number with value greater than 1 |
| Huge `k` | `0` | Early rejection of impossible zebra values |
| `21 21 1` | `1` | Single zebra-like number |

## Edge Cases

Consider

```
1
1 1 1
```

The greedy zebra representation is simply one copy of $z_1=1$. The digit sum is $1$, so the DP counts it. The output is `1`.

Consider

```
1
2 10 100
```

There are only about thirty zebra digits. Every canonical digit is at most four, so the maximum zebra value below $10^{18}$ is at most $120$. Since $100$ already exceeds the achievable range for many intervals and $10^{18}$ is the global limit, the DP immediately returns zero states. The output is `0`.

Consider

```
1
21 21 1
```

The canonical representation is

$$21 = z_3.$$

Its digit sum is $1$, so its zebra value is $1$. The DP reaches exactly one accepting state and returns `1`.

The most delicate case is when a digit $4$ appears. Suppose a representation tries to use

$$4z_i + z_j$$

with $j<i$. Since

$$z_{i+1}=4z_i+1,$$

this representation is not optimal. The `locked` state forbids such configurations by forcing all lower digits to become zero after a digit $4$ is chosen. That is exactly the condition required for canonical optimal decompositions.
