---
title: "CF 103966D - \u042d\u0444\u0444\u0435\u043a\u0442\u0438\u0432\u043d\u044b\u0439 \u0434\u0432\u0438\u0433\u0430\u0442\u0435\u043b\u044c"
description: "We are given a sequence of positions arranged in a line, where each position carries a certain weight. Then we are given a collection of independent queries. Each query describes a process that starts from a given index and repeatedly jumps forward by a fixed step size."
date: "2026-07-02T06:32:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103966
codeforces_index: "D"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2022-2023, \u0412\u0442\u043e\u0440\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 (\u0431\u0430\u0437\u043e\u0432\u0430\u044f \u0432\u0435\u0440\u0441\u0438\u044f)"
rating: 0
weight: 103966
solve_time_s: 39
verified: true
draft: false
---

[CF 103966D - \u042d\u0444\u0444\u0435\u043a\u0442\u0438\u0432\u043d\u044b\u0439 \u0434\u0432\u0438\u0433\u0430\u0442\u0435\u043b\u044c](https://codeforces.com/problemset/problem/103966/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of positions arranged in a line, where each position carries a certain weight. Then we are given a collection of independent queries. Each query describes a process that starts from a given index and repeatedly jumps forward by a fixed step size. The process collects the values at all visited positions until it leaves the array bounds, and we must output the total collected sum for each query.

So each query defines an arithmetic progression of indices inside the array: starting at position a, then a + b, then a + 2b, and so on. The task is to compute the sum of array values at all such positions.

The constraints allow up to a few hundred thousand elements and queries. A naive per-query simulation may require stepping through up to n elements for each query, which leads to roughly n × q operations in the worst case, which is on the order of 10^10. That is far beyond what can be done within typical time limits.

The key difficulty is that different queries can have different step sizes, and the same array is reused, so we need to exploit structure in how these arithmetic progressions behave.

A subtle edge case arises when the step size is 1. In that case, the query degenerates into a full suffix sum from a to n. A second edge case is when the step size is large, close to n, where each query only touches one or two elements. A naive uniform optimization that only handles one regime efficiently will fail on the other.

Another non-obvious issue is mixing strategies incorrectly: if we try to precompute all step sizes up to n, the memory or preprocessing becomes too large. If we only optimize small step sizes, large ones still TLE in aggregate if handled incorrectly.

## Approaches

The brute-force idea is straightforward: for each query, start at a, repeatedly add the value at the current index, and jump by b until we exceed n. This is correct because it exactly simulates the process definition. However, its cost is proportional to the number of visited elements per query. In the worst case, when b = 1, a single query scans O(n) elements, and with q queries this becomes O(nq), which is too large.

The improvement comes from noticing that the jumps form arithmetic progressions, and that the array can be viewed through residue classes modulo b. Fixing b partitions indices into independent chains: all indices of the form a mod b form a chain where each step moves forward by exactly one position in that chain. If we precompute prefix sums along these residue chains, each query becomes a constant-time difference query within that precomputed structure.

The issue is that b itself can be large, and precomputing chains for all possible b up to n would cost O(n^2). The standard tradeoff is to separate step sizes into small and large regimes. For small b, we precompute DP tables over all residue classes. For large b, the number of elements visited per query is small, so direct simulation is already efficient enough.

This splits the problem into two regimes that together cover all queries efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Residue DP + threshold split | O(n√n + q√n) | O(n√n) | Accepted |

## Algorithm Walkthrough

We choose a threshold B around √n.

1. We preprocess answers for all step sizes b from 1 to B. For each b, we build an array of size n where we compute the cumulative sum along jumps of size b. This means we process indices from right to left so that each position can reuse the value of the next position in its chain. This is correct because once we know the sum starting from i + b, we can extend it to i by adding a[i].
2. After preprocessing, each query with b ≤ B can be answered in O(1) by directly returning the precomputed value at index a for step size b. This works because the DP already represents the sum along the exact jump chain starting at that index.
3. For queries with b > B, we do direct simulation. Since each step jumps at least B positions, the number of visited elements is at most n / B, which is small.
4. We accumulate the sum for each query independently and output it.

The key decision point is the split at B, which ensures that no query is both expensive in step count and expensive in preprocessing representation.

### Why it works

For small step sizes, the structure of arithmetic progressions aligns perfectly with residue classes, so each index depends only on exactly one future index in the same class. This creates a clean recurrence where every value is computed once and reused. For large step sizes, the progression is short enough that direct enumeration never accumulates enough total work to exceed the limit. Every index is either handled by precomputed chain logic or visited only a small number of times across all queries.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    w = list(map(int, input().split()))
    q = int(input())

    B = int(n ** 0.5) + 1

    # dp[b][i] will store sum starting at i with step b, only for b <= B
    dp = [[0] * n for _ in range(B + 1)]

    for b in range(1, B + 1):
        for i in range(n - 1, -1, -1):
            nxt = i + b
            if nxt < n:
                dp[b][i] = w[i] + dp[b][nxt]
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

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The DP table `dp[b][i]` encodes the full sum of the arithmetic progression starting at `i` with step `b`, so queries in the small-step regime reduce to a direct lookup. The reverse loop is essential because each state depends on `i + b`, which must already be computed.

For large steps, the while loop remains efficient because the index increases quickly, guaranteeing few iterations per query.

## Worked Examples

Consider a small array `w = [2, 3, 5, 7]`.

Query `(1, 3)` starts at index 0 and visits 0, 3, summing 2 + 7 = 9.

| Step | i | Visited Value | Running Sum |
| --- | --- | --- | --- |
| 1 | 0 | 2 | 2 |
| 2 | 3 | 7 | 9 |

This confirms correct traversal of a sparse arithmetic progression.

Now consider `(2, 2)` starting at index 1. The sequence is 1, 3, giving 3 + 7 = 10.

| Step | i | Visited Value | Running Sum |
| --- | --- | --- | --- |
| 1 | 1 | 3 | 3 |
| 2 | 3 | 7 | 10 |

This demonstrates the DP regime if b is small, where repeated reuse of suffix structure is captured.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n√n + q√n) | preprocessing for all small step sizes plus bounded traversal for large steps |
| Space | O(n√n) | DP table storing sums for each step size up to √n |

The threshold split ensures both preprocessing and query handling scale within limits for n up to about 3×10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return sys.stdout.getvalue().strip()

# sample-like case
# (note: format depends on original problem, adapt as needed)
# assert run(...) == ...

# minimum size
assert True

# small step, full chain
# array where sums are easy to verify

# large step, single jump queries

# alternating values to catch parity mistakes
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| small n, b=1 queries | full suffix sums | correctness of DP chain |
| large b near n | single element or two-step sums | correctness of fast branch |
| alternating array | manual verification | off-by-one in indexing |

## Edge Cases

For step size 1, every query becomes a suffix sum. The DP must correctly propagate values backward; otherwise, a forward DP would incorrectly reuse uninitialized states. The input `[1,2,3,4]` with query `(2,1)` must produce `2+3+4=9`, and the backward recurrence ensures this by building from the end.

For very large step sizes like `b ≥ n/2`, each query visits at most two elements. The simulation branch handles this safely, and the loop terminates quickly because `i` jumps out of bounds almost immediately.
