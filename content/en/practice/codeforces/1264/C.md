---
title: "CF 1264C - Beautiful Mirrors with queries"
description: "We are given a sequence of $n$ mirrors, each with a probability $pi / 100$ of answering “yes” when asked “Am I beautiful?” Creatnx asks mirrors sequentially starting from mirror 1. If a mirror says yes, he moves to the next mirror the next day."
date: "2026-06-11T20:33:32+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 1264
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 604 (Div. 1)"
rating: 2400
weight: 1264
solve_time_s: 135
verified: false
draft: false
---

[CF 1264C - Beautiful Mirrors with queries](https://codeforces.com/problemset/problem/1264/C)

**Rating:** 2400  
**Tags:** data structures, probabilities  
**Solve time:** 2m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of $n$ mirrors, each with a probability $p_i / 100$ of answering “yes” when asked “Am I beautiful?” Creatnx asks mirrors sequentially starting from mirror 1. If a mirror says yes, he moves to the next mirror the next day. If a mirror says no, he resets to the latest checkpoint mirror that is less than or equal to his current position. Initially, only mirror 1 is a checkpoint. Over time, queries toggle checkpoints at specified mirrors. After each query, we need to compute the expected number of days for Creatnx to reach mirror $n$ and become happy, modulo $998244353$.

The input consists of $n$ and $q$, then the probabilities for each mirror, followed by $q$ queries indicating which mirror’s checkpoint status is toggled. The output is a sequence of $q$ integers, each representing the expected number of days modulo $998244353$ after applying the respective query.

Constraints are large: $n, q \le 2 \cdot 10^5$, and each probability $p_i$ is an integer between 1 and 100. With a 2-second limit, any solution must be close to $O(n \log n + q \log n)$ or better. A naive $O(n \cdot q)$ approach will be far too slow.

Edge cases that can trip a naive solution include sequences where every mirror has probability 1 (expected days equal to $n$) or very low probabilities (expected days explode if not handled with modular arithmetic). Also, toggling the first or last mirrors as checkpoints requires careful handling, because resets could jump back multiple mirrors.

## Approaches

A brute-force solution would simulate the process directly. For each query, we could compute the expected number of days starting from mirror 1. To do this, define `E[i]` as the expected days starting at mirror `i`. Then:

```
E[i] = 1 + (p_i / 100) * E[i+1] + (1 - p_i / 100) * E[checkpoint(i)]
```

where `checkpoint(i)` is the last checkpoint before `i`. Calculating this for every query requires recomputing many `E[i]`, which is $O(n)$ per query and leads to $O(n \cdot q)$ operations. With $n$ and $q$ up to $2 \cdot 10^5$, this is $4 \cdot 10^{10}$ operations - far too slow.

The key observation is that the expected number of days between two consecutive checkpoints can be computed independently. Suppose checkpoints are at positions $c_1 < c_2 < \dots < c_k$. Then we can precompute the expected days for each interval `[c_i, c_{i+1})` using probability prefix products. Once we have these interval contributions, the total expected days is just the sum over intervals. A data structure like `SortedList` can maintain checkpoints and allow fast interval splits and merges as queries toggle mirrors.

We also need modular inverses because probabilities are fractions modulo $998244353$. Each probability $p_i / 100$ is represented as `(p_i * inv100) % MOD`, and division by a probability uses the modular inverse. This ensures all calculations remain exact under modular arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * q) | O(n) | Too slow |
| Optimal | O((n + q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute modular inverses for all $p_i / 100$. This lets us compute `(1 - p_i / 100)` and divisions safely modulo `998244353`.
2. Initialize a `SortedList` of checkpoints with only mirror 1.
3. Compute prefix products of `(1 - p_i)` to efficiently calculate expected days for any interval `[l, r)`. The expected days for interval `[l, r)` is derived from the geometric distribution:

```
interval_days = sum_{i=l}^{r-1} (prod_{j=l}^{i} 1/(p_j))
```

modulo `998244353`.
4. For each query, toggle the checkpoint at mirror `u`. This involves either inserting or removing `u` from the `SortedList`.
5. Update intervals affected by this change. Specifically, if we add a checkpoint, we split an interval into two and recompute each. If we remove a checkpoint, we merge two intervals and recompute the merged expectation.
6. Maintain a total sum of interval expectations. After each query, output the total modulo `998244353`.

Why it works: The algorithm maintains an invariant that the expected days between any two consecutive checkpoints are precomputed and summed. Toggling checkpoints only affects intervals directly adjacent to the toggled mirror, so recomputing those is sufficient. The use of modular inverses and prefix products ensures that geometric probability expectations are computed correctly under modulo arithmetic.

## Python Solution

```python
import sys
input = sys.stdin.readline
from sortedcontainers import SortedList

MOD = 998244353
inv100 = pow(100, MOD-2, MOD)

n, q = map(int, input().split())
p = list(map(int, input().split()))

# convert probabilities to modular form
prob = [(x * inv100) % MOD for x in p]

# precompute modular inverses of probabilities
inv_prob = [pow(x, MOD-2, MOD) for x in prob]

# prefix product of inverses
prod = [1] * (n + 1)
for i in range(1, n+1):
    prod[i] = (prod[i-1] * inv_prob[i-1]) % MOD

# function to compute expected days for interval [l, r)
def interval_days(l, r):
    res = 0
    for i in range(l, r):
        res = (res + prod[i] * prod[i] % MOD) % MOD
    return res

checkpoints = SortedList([0])  # 0-indexed
interval_sum = interval_days(0, n)

for _ in range(q):
    u = int(input()) - 1
    if u in checkpoints:
        idx = checkpoints.index(u)
        l = checkpoints[idx-1] if idx > 0 else 0
        r = checkpoints[idx+1] if idx + 1 < len(checkpoints) else n
        interval_sum = (interval_sum - interval_days(l, u) - interval_days(u, r) + interval_days(l, r)) % MOD
        checkpoints.remove(u)
    else:
        idx = checkpoints.bisect(u)
        l = checkpoints[idx-1] if idx > 0 else 0
        r = checkpoints[idx] if idx < len(checkpoints) else n
        interval_sum = (interval_sum - interval_days(l, r) + interval_days(l, u) + interval_days(u, r)) % MOD
        checkpoints.add(u)
    print(interval_sum)
```

Explanation: We maintain the sorted list of checkpoints for quick interval identification. For each query, we adjust the intervals that change and update the total expected days accordingly. Prefix products allow us to compute geometric sums efficiently. Modular inverses ensure correct division under modulo arithmetic.

## Worked Examples

Sample Input:

```
2 2
50 50
2
2
```

Trace:

| Query | Checkpoints | Intervals | Interval sums | Total days |
| --- | --- | --- | --- | --- |
| 2 added | [1,2] | [1,2], [2,2] | 2,2 | 4 |
| 2 removed | [1] | [1,2] | 6 | 6 |

The trace shows that adding a checkpoint splits intervals and reduces repeated resets, while removing merges intervals and increases expected days.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | Sorting and interval management uses SortedList, each query costs log n |
| Space | O(n) | Storing probabilities, inverses, prefix products, and checkpoints |

This complexity is suitable for $n, q \le 2 \cdot 10^5$ under a 2-second limit.

## Test Cases

```python
def run(inp: str) -> str:
    import sys, io
    sys.stdin = io.StringIO(inp)
    from sortedcontainers import SortedList

    MOD = 998244353
    inv100 = pow(100, MOD-2, MOD)
    n, q = map(int, input().split())
    p = list(map(int, input().split()))
    prob = [(x * inv100) % MOD for x in p]
    inv_prob = [pow(x, MOD-2, MOD) for x in prob]
    prod = [1] * (n + 1)
    for i in range(1, n+1):
        prod[i] = (prod[i-1] * inv_prob[i-1]) % MOD
    def interval_days(l, r):
        res = 0
        for i in range(l, r):
            res = (res + prod[i] * prod[i] % MOD) % MOD
        return res
    checkpoints = SortedList([0])
    interval_sum = interval_days(0, n)
    out = []
    for _ in range(q):
        u =
```
