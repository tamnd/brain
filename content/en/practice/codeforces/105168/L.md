---
title: "CF 105168L - Terabyte Connection"
description: "We are given a set of independent file chunks that behave like delayed-start tasks. Each chunk becomes available for connection at a specific moment $pi$, and once we start downloading that chunk, it takes exactly $ti$ seconds to finish."
date: "2026-06-27T09:07:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105168
codeforces_index: "L"
codeforces_contest_name: "2024 Fujian Normal University Programming Contest"
rating: 0
weight: 105168
solve_time_s: 53
verified: true
draft: false
---

[CF 105168L - Terabyte Connection](https://codeforces.com/problemset/problem/105168/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of independent file chunks that behave like delayed-start tasks. Each chunk becomes available for connection at a specific moment $p_i$, and once we start downloading that chunk, it takes exactly $t_i$ seconds to finish. We are allowed to start downloading a chunk only after its connection time, and we do not need to download chunks sequentially in any particular order; each chunk progresses independently once it is “available” to begin.

Two quantities must be computed for each test case. The first is the earliest time when all chunks have become connected at least once, which is simply the last arrival moment among all $p_i$. The second is the earliest time when all chunks have fully finished downloading, assuming that each chunk starts downloading immediately at its connection time.

The input size can reach $2 \cdot 10^5$ chunks per test file across test cases. This immediately rules out any approach that simulates time second by second or maintains a time-based simulation. Even $O(n^2)$ reasoning per test case would be too slow; we need an $O(n)$ scan per test case.

A subtle issue appears if one interprets the problem as requiring scheduling decisions. Since chunks do not compete for bandwidth or resources, there is no interaction between them. Each chunk is effectively an independent interval starting at $p_i$ and ending at $p_i + t_i$. The only global quantities are the maximum start time and the maximum end time.

Edge cases arise when multiple chunks share the same connection time, or when a chunk with a small $p_i$ has a very large $t_i$. For example, if we have $p = [1, 100]$ and $t = [1000, 1]$, the earliest full connection is 100, but the final completion time is 1001. A naive incorrect approach might mistakenly assume that the last connection time dominates completion, ignoring long downloads that started earlier.

## Approaches

A brute-force interpretation would simulate each chunk independently over time, advancing a timeline and tracking when each chunk becomes active and completes. One could imagine iterating time from the smallest $p_i$ to the largest completion moment and updating states as chunks start and finish. This is correct conceptually because each chunk’s lifecycle is straightforward, but it is completely infeasible in the worst case. If $p_i$ and $t_i$ are large, the time axis spans up to $10^9$, and even compressing events still leaves $O(n \log n)$ or worse overhead if we attempt event simulation.

The key observation is that there is no interaction between chunks. Each chunk contributes exactly two values: its start moment $p_i$ and its finish moment $p_i + t_i$. The global answer for connection completion is simply the maximum of all start times, since that is the last moment any chunk becomes available. The global answer for finishing is the maximum of all computed completion times, since each chunk runs independently.

Once this is recognized, the problem reduces to a single linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(max(p_i + t_i)) | O(n) | Too slow |
| Linear Scan | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently and compute two maxima in a single pass over the chunks.

1. Initialize two variables $P = 0$ and $F = 0$, which will track the maximum connection time and maximum finishing time respectively. These represent global aggregations over independent intervals.
2. For each chunk $i$, read $p_i$ and $t_i$. Update $P$ as $P = \max(P, p_i)$. This step ensures we always retain the latest moment any chunk becomes available.
3. Compute the finishing time of the current chunk as $p_i + t_i$, and update $F = \max(F, p_i + t_i)$. This captures the fact that each chunk contributes a candidate completion moment independent of others.
4. After processing all chunks, output $P$ and $F$.

The ordering of updates does not matter because each chunk is independent; we are only aggregating extrema over a set of derived values.

### Why it works

Each chunk defines a deterministic interval $[p_i, p_i + t_i]$. The moment all chunks are connected is the maximum left endpoint among these intervals. The moment all chunks are finished is the maximum right endpoint. Since there is no dependency or shared resource constraint, no chunk can delay another, and no reordering affects any interval. The problem therefore reduces exactly to computing maxima over interval endpoints, which is invariant under any processing order.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    P = 0
    F = 0
    for _ in range(n):
        p, ti = map(int, input().split())
        P = max(P, p)
        F = max(F, p + ti)
    print(P, F)
```

The solution maintains two accumulators during a single pass. The first accumulator tracks the latest connection moment, and the second tracks the latest completion moment formed by adding duration to each start time.

The only subtle implementation detail is ensuring that addition $p + t$ is computed per chunk before taking the maximum. Any attempt to separate these operations or reuse partial values across iterations would break correctness.

## Worked Examples

### Example 1

Input:

```
n = 3
chunks = (1,1), (3,2), (2,3)
```

We track $P$ and $F$ step by step.

| Chunk | p | t | p + t | P | F |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 2 | 1 | 2 |
| 2 | 3 | 2 | 5 | 3 | 5 |
| 3 | 2 | 3 | 5 | 3 | 5 |

Final result is $P = 3$, $F = 5$.

This trace shows that early starting chunks do not determine completion time; instead, long-running chunks dominate $F$, while the last connection time determines $P$.

### Example 2

Input:

```
n = 4
chunks = (10,1), (2,100), (7,3), (5,50)
```

| Chunk | p | t | p + t | P | F |
| --- | --- | --- | --- | --- | --- |
| 1 | 10 | 1 | 11 | 10 | 11 |
| 2 | 2 | 100 | 102 | 10 | 102 |
| 3 | 7 | 3 | 10 | 10 | 102 |
| 4 | 5 | 50 | 55 | 10 | 102 |

Final result is $P = 10$, $F = 102$.

This example demonstrates that a chunk with a very early start but large duration can dominate the final finishing time even though it does not affect the connection maximum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each chunk is processed once with constant work |
| Space | O(1) | Only two running maxima are stored |

The total $n$ across test cases is bounded by $2 \cdot 10^5$, so the solution performs a single linear scan overall, which easily fits within typical time limits for 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        P = 0
        F = 0
        for _ in range(n):
            p, ti = map(int, input().split())
            P = max(P, p)
            F = max(F, p + ti)
        out.append(f"{P} {F}")
    return "\n".join(out)

# provided sample
assert run("""1
3
1 1
3 2
2 3
""") == "3 5"

# minimum size
assert run("""1
1
5 7
""") == "5 12"

# all equal
assert run("""1
3
4 4
4 4
4 4
""") == "4 8"

# mixed values
assert run("""1
4
10 1
2 100
7 3
5 50
""") == "10 102"

# large dominance of early finish
assert run("""1
2
1 1000
999 1
""") == "999 1001"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single chunk | trivial max behavior | base case correctness |
| identical chunks | stability under duplicates | no ordering dependence |
| mixed values | long duration dominates F | correctness of p+t aggregation |
| skewed starts | separation of P and F | independent maxima behavior |

## Edge Cases

Consider a case where the earliest chunk has the longest download time:

```
1
2
1 1000
999 1
```

Processing proceeds as follows. Initially $P = 0$, $F = 0$. After the first chunk, $P = 1$, $F = 1001$. After the second chunk, $P = 999$, $F = 1001$. The final answer is $P = 999$, $F = 1001$.

This confirms that a chunk contributing the maximum finish time does not need to be the last one to connect. The algorithm correctly separates the two independent extrema: one over start points and one over computed end points.
