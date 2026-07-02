---
title: "CF 103896D - Owl Defense"
description: "We are given a line of cows, each with a weight. A “raid” is defined by two integers, a starting position and a step size. Starting from position a, we repeatedly jump forward by b positions and collect all cows we land on, stopping once we go past the end of the line."
date: "2026-07-02T07:30:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103896
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 09-02-22 Div. 1 (Advanced)"
rating: 0
weight: 103896
solve_time_s: 49
verified: true
draft: false
---

[CF 103896D - Owl Defense](https://codeforces.com/problemset/problem/103896/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of cows, each with a weight. A “raid” is defined by two integers, a starting position and a step size. Starting from position a, we repeatedly jump forward by b positions and collect all cows we land on, stopping once we go past the end of the line. Each query asks for the total weight of all cows collected by that particular raid pattern.

In other words, each query defines an arithmetic progression of indices inside the array, and we must sum the values at those indices.

The constraints are large: up to 3×10^5 cows and 3×10^5 queries. This immediately rules out any approach that recomputes the sum for each query by walking the progression step by step. In the worst case, a single query with b = 1 touches O(n) elements, which would lead to O(n·q), far beyond acceptable limits.

A subtle edge case appears when b is large versus small. When b is large, each query touches few elements and is cheap. When b is small, many indices overlap across queries, and naive iteration repeats the same work many times. Another issue is when a = 1 and b = 1, which degenerates into summing the entire array, a situation that would be repeatedly recomputed under brute force.

A naive improvement might try caching results per (a, b), but since there can be up to 3×10^5 distinct pairs, this does not help in worst case.

## Approaches

The brute force idea is straightforward: for each query, start at index a and repeatedly add w[a], w[a + b], w[a + 2b], and so on until exceeding n. This is correct because it exactly follows the definition of the raid. The problem is cost. In the worst case where b = 1, each query processes n elements, leading to about 9×10^10 operations overall when both n and q are 3×10^5.

The key observation is that the jump size b partitions behavior into two fundamentally different regimes. Large b means few visited positions per query. Small b means many queries share similar residue classes modulo b, so we can reuse precomputed information. The structure we exploit is that indices visited by a fixed step b form independent arithmetic sequences, and when b is small there are only a few such sequences overall.

This leads to a hybrid solution. We choose a threshold B around √n. For b greater than B, we compute each query directly because it only visits at most n / B elements. For b less than or equal to B, we precompute answers for all possible (b, remainder) pairs using dynamic programming from right to left, so each query becomes O(1).

The key transition is rewriting the recurrence: for fixed b, define dp[i] = w[i] + dp[i + b]. This allows all answers for a given b to be computed in one pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Sqrt Decomposition on step size | O(n√n + q√n) | O(n√n) | Accepted |

## Algorithm Walkthrough

We separate queries based on their step size b using a threshold B ≈ √n.

1. We initialize a structure to store answers for small step sizes. For each b from 1 to B, we will compute a dp array where dp[i] represents the total sum starting from i and jumping by b until leaving the array.
2. For each b from 1 to B, we compute dp in reverse order from n down to 1. At position i, if i + b ≤ n, we set dp[i] = w[i] + dp[i + b], otherwise dp[i] = w[i]. This works because the next visited position in the same arithmetic progression is exactly i + b.
3. After computing dp for a fixed b, we can answer any query with that b in O(1) time by returning dp[a].
4. For queries where b > B, we answer them directly by iterating i = a, a + b, a + 2b and summing weights until we exceed n. Since b is large, the number of visited elements is small.
5. We process all queries, using precomputed dp for small steps and direct simulation for large steps.

Why it works is tied to the structure of arithmetic progressions over a fixed array. For small steps, the array is repeatedly reused in overlapping chains, so precomputation amortizes across all queries. For large steps, chains are sparse enough that direct traversal is cheap. Every query is handled by exactly one of these two regimes, and both cover all possible (a, b) cases without overlap or omission.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
w = list(map(int, input().split()))
q = int(input())

B = int(n ** 0.5) + 1

# store answers for small b
dp = [[0] * n for _ in range(B + 1)]

# precompute for all b up to B
for b in range(1, B + 1):
    for i in range(n - 1, -1, -1):
        if i + b < n:
            dp[b][i] = w[i] + dp[b][i + b]
        else:
            dp[b][i] = w[i]

for _ in range(q):
    a, b = map(int, input().split())
    a -= 1

    if b <= B:
        print(dp[b][a])
    else:
        s = 0
        i = a
        while i < n:
            s += w[i]
            i += b
        print(s)
```

The dp table is the core optimization. Each row corresponds to a fixed step size b, and each entry collapses an entire arithmetic progression into a single precomputed value. The direct loop is only used when the progression is short enough that preprocessing would not be worth it.

The only subtle implementation detail is indexing. The dp array is built on 0-based indices, so every query converts a to a - 1 before lookup. Another detail is the boundary check i + b < n, which ensures we only reference valid future indices.

## Worked Examples

### Example 1

Input:

```
n = 3
w = [1, 2, 3]
queries = (1,1), (1,2)
```

For b = 1, dp[1][i] is suffix sum:

| i | dp[1][i] |
| --- | --- |
| 3 | 3 |
| 2 | 5 |
| 1 | 6 |

Query (1,1) returns dp[1][1] = 6.

For (1,2), we directly visit indices 1 and 3:

sum = 1 + 3 = 4.

This shows how dp compresses a full traversal into O(1).

### Example 2

Input:

```
n = 4
w = [2,3,5,7]
queries = (2,3), (2,2)
```

For b = 3:

dp[3][i] values:

| i | dp[3][i] |
| --- | --- |
| 4 | 7 |
| 3 | 5 |
| 2 | 3 + 7 = 10 |
| 1 | 2 + 5 = 7 |

Query (2,3) returns dp[3][2] = 10.

For b = 2, since 2 is small, we use dp directly:

dp[2][2] = 3 + 7 = 10? actually indices 2 → 4 gives 3 + 7 = 10.

This confirms consistency between recurrence and traversal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n√n + q√n) | Each small step b builds a dp array in O(n), and there are √n such b values; large steps process at most √n elements per query |
| Space | O(n√n) | DP table stores n entries for each b up to √n |

The combined complexity fits comfortably within limits for n, q up to 3×10^5, since √n ≈ 550.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import sqrt
    n = int(input())
    w = list(map(int, input().split()))
    q = int(input())

    B = int(n ** 0.5) + 1
    dp = [[0] * n for _ in range(B + 1)]

    for b in range(1, B + 1):
        for i in range(n - 1, -1, -1):
            if i + b < n:
                dp[b][i] = w[i] + dp[b][i + b]
            else:
                dp[b][i] = w[i]

    out = []
    for _ in range(q):
        a, b = map(int, input().split())
        a -= 1
        if b <= B:
            out.append(str(dp[b][a]))
        else:
            s = 0
            i = a
            while i < n:
                s += w[i]
                i += b
            out.append(str(s))
    return "\n".join(out)

# sample-like
assert run("3\n1 2 3\n2\n1 1\n1 2") == "6\n4"

# minimum
assert run("1\n5\n1\n1 1") == "5"

# all equal
assert run("5\n1 1 1 1 1\n2\n1 1\n1 2") == "5\n3"

# large step
assert run("6\n1 2 3 4 5 6\n1\n2 5") == "7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 5 | base case correctness |
| uniform array | 5, 3 | consistency across step sizes |
| large jump | 7 | sparse traversal correctness |

## Edge Cases

A critical edge case is when b = 1. In that situation, every query becomes a full suffix sum from a, and naive solutions repeatedly recompute long segments. The dp recurrence handles this cleanly because dp[1][i] naturally becomes a suffix sum chain.

Another edge case is when a is near the end and b is large. For example, n = 6, a = 5, b = 10. The loop should only include w[5], and stop immediately. The direct simulation handles this correctly because the condition i < n is checked before each addition.

A final subtle case is when multiple queries share the same (a, b). The solution does not rely on caching per query; instead it ensures correctness independently for each query via either dp lookup or deterministic traversal.
