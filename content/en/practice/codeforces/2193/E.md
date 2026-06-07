---
title: "CF 2193E - Product Queries"
description: "We are given an array whose values lie between 1 and n. An element may be reused any number of times, so the only thing that matters is which values are present in the array, not how many times they occur."
date: "2026-06-07T20:51:59+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "number-theory", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 2193
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1076 (Div. 3)"
rating: 1300
weight: 2193
solve_time_s: 155
verified: true
draft: false
---

[CF 2193E - Product Queries](https://codeforces.com/problemset/problem/2193/E)

**Rating:** 1300  
**Tags:** dp, math, number theory, shortest paths  
**Solve time:** 2m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array whose values lie between `1` and `n`. An element may be reused any number of times, so the only thing that matters is which values are present in the array, not how many times they occur.

For every integer `i` from `1` to `n`, we must find the minimum number of chosen array values whose product is exactly `i`. If no such product can be formed, we output `-1`.

A useful way to view the problem is as a multiplicative graph. If a value `k` appears in the array, then from a product `x` we may move to `x * k`, provided the result does not exceed `n`. Every multiplication uses one more selected element.

The total sum of `n` over all test cases is at most `3 · 10^5`. Any solution close to `O(n^2)` is immediately ruled out. We need something around `O(n log n)` across a test case.

Several edge cases are easy to mishandle.

Consider:

```
n = 3
a = [1, 1, 1]
```

The product `1` is obtainable with one chosen element, so the answer for `1` is `1`, not `0`. The statement requires selecting at least one element.

Consider:

```
n = 4
a = [2]
```

The product `4` is obtainable as `2 · 2`, even though the array contains only one occurrence of `2`. Reuse is allowed.

Consider:

```
n = 5
a = [2, 4]
```

The product `3` is impossible. A careless DP that assumes every number can be built from smaller numbers would incorrectly mark it reachable.

## Approaches

The brute-force idea is to treat every product as a state and run a shortest-path search. From a product `x`, try multiplying by every available array value. This is correct because every multiplication corresponds to choosing one more element.

The problem is the number of transitions. If there are `Θ(n)` distinct available values and we examine all of them from every state, the complexity becomes `Θ(n^2)`, which is far too large for `n = 3 · 10^5`.

The key observation is that all products are at most `n`, and every transition has the form

```
x -> x * k
```

where `k` is a value present in the array.

Since `k ≥ 2` for every useful multiplication, the destination is strictly larger than the source. The graph is a DAG whose topological order is simply increasing numerical order.

Let `dp[x]` be the minimum number of selected elements needed to obtain product `x`, assuming we start from the neutral product `1` with cost `0`.

When we process `x`, every available multiplier `k` generates a relaxation:

```
dp[x * k] = min(dp[x * k], dp[x] + 1)
```

Instead of iterating over all available values for every state, we iterate over all possible multipliers `k` up to `n / x` and simply check whether `k` is present in the array.

The total number of examined pairs is

```
Σ floor(n / x)
```

which is `O(n log n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a boolean array `present`, where `present[v]` is true if value `v` appears in the array.
2. Create a DP array initialized with infinity.
3. Set `dp[1] = 0`. This represents the empty product before choosing any elements.
4. Process numbers `x` from `1` to `n` in increasing order.
5. If `dp[x]` is still infinity, skip it because product `x` cannot be formed.
6. For every multiplier `k` from `2` to `⌊n / x⌋`:

If `present[k]` is true, relax

```
dp[x * k] = min(dp[x * k], dp[x] + 1)
```

The multiplication by `k` corresponds to choosing one additional array element.
7. Build the answers.

For `i > 1`, the answer is `dp[i]` if it is finite, otherwise `-1`.

For `i = 1`, the answer is:

```
1  if present[1]
-1 otherwise
```

We cannot output `0` because at least one element must be selected.

### Why it works

The graph contains an edge from `x` to `x * k` whenever value `k` exists in the array. Every edge has cost `1`, and every edge goes to a strictly larger node. Increasing numerical order is therefore a valid topological order.

When processing `x`, `dp[x]` already equals the shortest path length from product `1` to `x`. Relaxing all outgoing edges propagates optimal values to larger products. Since every path corresponds exactly to a sequence of chosen array elements, `dp[i]` becomes the minimum number of selected elements whose product is `i`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        present = [False] * (n + 1)
        for x in a:
            present[x] = True

        INF = 10 ** 9
        dp = [INF] * (n + 1)
        dp[1] = 0

        for x in range(1, n + 1):
            if dp[x] == INF:
                continue

            limit = n // x
            for k in range(2, limit + 1):
                if present[k]:
                    nx = x * k
                    if dp[nx] > dp[x] + 1:
                        dp[nx] = dp[x] + 1

        ans = []

        if present[1]:
            ans.append("1")
        else:
            ans.append("-1")

        for i in range(2, n + 1):
            if dp[i] == INF:
                ans.append("-1")
            else:
                ans.append(str(dp[i]))

        print(" ".join(ans))

solve()
```

The `present` array removes all duplicate values. Since elements may be reused infinitely many times, only existence matters.

The DP starts from product `1` with cost `0`. This is a virtual starting state and is not itself a valid answer. That is why the answer for product `1` is handled separately.

The loop order is crucial. Processing `x` in increasing order works because every transition goes to a larger number. No priority queue or repeated relaxation is needed.

Another subtle point is that multipliers start from `2`. Multiplying by `1` never changes the product and would create self-loops. Such transitions are useless for shortest paths and can be ignored.

## Worked Examples

### Example 1

Input:

```
n = 8
a = [3, 2, 2, 3, 7, 3, 6, 7]
```

Present values are `{2, 3, 6, 7}`.

| x | dp[x] before | Relaxations |
| --- | --- | --- |
| 1 | 0 | dp[2]=1, dp[3]=1, dp[6]=1, dp[7]=1 |
| 2 | 1 | dp[4]=2 |
| 3 | 1 | dp[6] stays 1 |
| 4 | 2 | dp[8]=3 |
| 6 | 1 | no useful update |
| 7 | 1 | no useful update |

Final answers:

```
-1 1 1 2 -1 1 1 3
```

This example shows how repeated use of the same value creates products such as `8 = 2·2·2`.

### Example 2

Input:

```
n = 5
a = [1, 2, 3, 4, 5]
```

| x | dp[x] before | Relaxations |
| --- | --- | --- |
| 1 | 0 | dp[2]=1, dp[3]=1, dp[4]=1, dp[5]=1 |
| 2 | 1 | no improvement |
| 3 | 1 | no improvement |
| 4 | 1 | no improvement |
| 5 | 1 | no improvement |

Since every target already appears in the array, every answer is `1`.

```
1 1 1 1 1
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | The inner loop performs `Σ floor(n / x)` iterations |
| Space | O(n) | `present` and `dp` arrays |

The harmonic-series bound gives roughly `n log n` operations per test case. With the total sum of `n` bounded by `3 · 10^5`, this easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    out = []

    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        present = [False] * (n + 1)
        for x in a:
            present[x] = True

        INF = 10 ** 9
        dp = [INF] * (n + 1)
        dp[1] = 0

        for x in range(1, n + 1):
            if dp[x] == INF:
                continue

            for k in range(2, n // x + 1):
                if present[k]:
                    dp[x * k] = min(dp[x * k], dp[x] + 1)

        ans = []
        ans.append("1" if present[1] else "-1")

        for i in range(2, n + 1):
            ans.append(str(dp[i]) if dp[i] < INF else "-1")

        out.append(" ".join(ans))

    return "\n".join(out)

# provided sample
assert run(
"""6
8
3 2 2 3 7 3 6 7
5
1 2 3 4 5
3
1 1 1
10
2 1 2 1 3 5 5 7 7 7
4
1 1 2 2
1
1
"""
) == (
"""-1 1 1 2 -1 1 1 3
1 1 1 1 1
1 -1 -1
1 1 1 2 1 2 1 3 2 2
1 1 -1 2
1"""
)

# minimum size
assert run(
"""1
1
1
"""
) == "1"

# only value 2
assert run(
"""1
4
2 2 2 2
"""
) == "-1 1 -1 2"

# only ones
assert run(
"""1
5
1 1 1 1 1
"""
) == "1 -1 -1 -1 -1"

# composite reachable through reuse
assert run(
"""1
8
2 3 2 3 2 3 2 3
"""
) == "-1 1 1 2 -1 2 -1 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, [1]` | `1` | Smallest valid instance |
| `n=4, [2,2,2,2]` | `-1 1 -1 2` | Reusing the same value multiple times |
| `n=5, [1,1,1,1,1]` | `1 -1 -1 -1 -1` | Product `1` handling |
| `n=8, only 2 and 3 present` | `-1 1 1 2 -1 2 -1 3` | Multi-step multiplicative paths |

## Edge Cases

Consider:

```
1
3
1 1 1
```

The DP keeps `dp[1] = 0`, but the final answer for product `1` is not taken from the DP. The algorithm checks `present[1]` and outputs `1`, satisfying the requirement that at least one element must be selected.

Consider:

```
1
4
2 2 2 2
```

Processing `x = 1` creates `dp[2] = 1`. Later, processing `x = 2` creates `dp[4] = 2`. The algorithm correctly allows repeated use of the same value even though only one occurrence exists in the array.

Consider:

```
1
5
2 4 4 2 2
```

No transition can ever reach `3` or `5`. Their DP values remain infinity, so the algorithm outputs `-1` for both targets. This prevents unreachable products from being marked as valid.
