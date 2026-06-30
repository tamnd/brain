---
title: "CF 104491A - Easy Problem"
description: "We are given a row of chickens indexed from left to right. Each chicken has a capacity limit, meaning it can only eat up to a certain number of grains."
date: "2026-06-30T12:27:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104491
codeforces_index: "A"
codeforces_contest_name: "43rd Petrozavodsk Programming Camp (2022 Summer) Day 7. HSE Koresha Contest"
rating: 0
weight: 104491
solve_time_s: 88
verified: false
draft: false
---

[CF 104491A - Easy Problem](https://codeforces.com/problemset/problem/104491/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a row of chickens indexed from left to right. Each chicken has a capacity limit, meaning it can only eat up to a certain number of grains. Alongside this, there are several feeders, and each feeder covers a continuous segment of chickens and contains a fixed number of grains.

The twist is in how feeders are filtered for each chicken. For a fixed chicken index $i$, we only keep feeders whose segment includes $i$. All other feeders are ignored completely. Among the remaining feeders, we consider how many total grains can be used, but each chicken still cannot exceed its own capacity.

So for every chicken $i$, we imagine a world where only feeders covering $i$ exist. In that world, we want the total number of grains contributed by those feeders, but capped by the per-chicken capacity constraint.

The output is a list of $n$ values, one per chicken, describing the total usable grains for that chicken under this filtering rule.

The constraints are tight enough that a quadratic approach over chickens and feeders would be too slow. With $n, m \le 10^5$ per test case and total sums bounded across tests, any solution must be close to linear or $O((n + m)\log n)$. A naive per-chicken scan over all feeders would perform up to $10^{10}$ operations in worst case, which is not viable.

A subtle point arises from overlap behavior. A feeder contributes to multiple chickens, but for each chicken independently we decide whether it is included or not. This means the contribution of a feeder is “locally global”: it depends only on whether the index lies in its segment.

A naive mistake is to assume we must recompute sums from scratch for each chicken. Another mistake is to forget that a feeder excluded for one index may still be included for a nearby index, so we cannot globally pre-delete feeders.

## Approaches

A brute-force solution fixes a chicken $i$, then iterates over all feeders and sums $c_j$ for those whose interval $[l_j, r_j]$ contains $i$. This is correct because it directly follows the rule. However, each query costs $O(m)$, and doing this for all $n$ chickens leads to $O(nm)$, which reaches $10^{10}$ operations in the worst case.

The key observation is that for a fixed chicken $i$, a feeder contributes if and only if $l_j \le i \le r_j$. We can rewrite this as: all feeders active at $i$ are exactly those whose interval covers $i$. So each feeder contributes its weight to a continuous range of indices, namely from $l_j$ to $r_j$. This is the classical “range adds, point queries” structure.

Instead of recomputing for every $i$, we reverse the perspective. Each feeder adds $c_j$ to every index in its interval. Therefore we want to compute, for every position $i$, the sum of all $c_j$ over feeders covering it. This becomes a difference array or prefix sum accumulation problem.

Once we compute this base array of total coverage sums, we must respect chicken capacities. Each chicken cannot eat more than $a_i$, so the final answer is simply $\min(a_i, \text{coverage}[i])$.

This converts the problem into two linear passes over difference arrays.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Optimal (difference array) | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

We compute how many grains are available at each position if we apply all feeders as range additions, then clamp by capacities.

1. Initialize an array `diff` of size $n+2$ with zeros. This array will store range updates in compressed form. The idea is that instead of updating every position in a range, we mark where a contribution starts and ends.
2. For each feeder $(l_j, r_j, c_j)$, add $c_j$ at `diff[l_j]` and subtract $c_j$ at `diff[r_j + 1]`. This encodes that the contribution is active only between $l_j$ and $r_j$. The subtraction ensures the effect stops after the range ends.
3. Build a prefix sum over `diff` to recover the actual coverage array `cover[i]`. At each index $i$, `cover[i]` equals the sum of all active feeder contributions at that point. This works because every range update contributes a +c at its start and a -c after its end, so prefix accumulation reconstructs the correct overlap sum.
4. For each chicken $i$, compute the final answer as $\min(a_i, cover[i])$. This enforces the per-chicken capacity constraint.
5. Output all answers for the test case.

### Why it works

Each feeder contributes $c_j$ to exactly the indices in its interval. The difference array ensures that every such interval is counted exactly once during prefix summation. No contribution is lost or double-counted because every addition has a matching cancellation after the interval ends. The resulting prefix sum at position $i$ equals the sum of all feeders covering $i$, which is exactly the quantity required before applying the capacity limit. Since capacity is independent per index, clamping does not interfere with correctness of other positions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        diff = [0] * (n + 2)

        for _ in range(m):
            l, r, c = map(int, input().split())
            diff[l] += c
            diff[r + 1] -= c

        cur = 0
        res = [0] * n

        for i in range(1, n + 1):
            cur += diff[i]
            res[i - 1] = min(a[i - 1], cur)

        print(*res)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the algorithm exactly. The `diff` array is sized $n+2$ to safely handle the $r+1$ update without bounds checks. The prefix accumulation variable `cur` avoids recomputing prefix sums repeatedly. Each position is processed once, ensuring linear performance per test case.

A common pitfall is forgetting that indexing is 1-based in input but 0-based in Python arrays. This solution consistently shifts only when writing into `res`, keeping `diff` aligned with 1-based logic for clarity.

## Worked Examples

### Example 1

Consider a small setup with three chickens and two feeders.

Input interpretation:

Feeder 1 covers chickens 1 to 2 with 3 grains, feeder 2 covers chickens 2 to 3 with 2 grains. Capacities are $a = [2, 5, 2]$.

We build the difference array step by step.

| Step | Operation | diff array (1..3) | cur | cover[i] | answer |
| --- | --- | --- | --- | --- | --- |
| init | start | [0,0,0,0] | 0 | - | - |
| F1 | +3 at 1, -3 at 3 | [3,0,-3,0] | - | - | - |
| F2 | +2 at 2, -2 at 4 | [3,2,-3,-2] | - | - | - |
| i=1 | prefix | - | 3 | 3 | min(2,3)=2 |
| i=2 | prefix | - | 5 | 5 | min(5,5)=5 |
| i=3 | prefix | - | 2 | 2 | min(2,2)=2 |

This shows how overlapping feeders accumulate naturally through prefix sums, and capacities only clamp after full aggregation.

### Example 2

A case with non-overlapping feeders highlights independence.

Suppose $n=4$, capacities $a=[1,10,1,10]$, feeders: $[1,1,5]$, $[3,4,7]$.

| i | cur coverage | capacity | result |
| --- | --- | --- | --- |
| 1 | 5 | 1 | 1 |
| 2 | 0 | 10 | 0 |
| 3 | 7 | 1 | 1 |
| 4 | 7 | 10 | 7 |

Each segment influences only its own interval, and positions outside receive zero due to no active feeders.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) per test case | Each feeder is processed once, and each position is visited once during prefix computation |
| Space | O(n) | Difference array and result array of size proportional to n |

The total constraints guarantee that the sum of all $n$ and $m$ across test cases is at most $10^5$, so this linear approach is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out_lines = []
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        diff = [0] * (n + 2)

        for _ in range(m):
            l, r, c = map(int, input().split())
            diff[l] += c
            diff[r + 1] -= c

        cur = 0
        res = []
        for i in range(1, n + 1):
            cur += diff[i]
            res.append(str(min(a[i - 1], cur)))

        out_lines.append(" ".join(res))

    return "\n".join(out_lines)

# sample-like tests
assert run("""1
3 2
2 5 2
1 2 3
2 3 2
""") == "2 5 2"

# minimum size
assert run("""1
1 1
10
1 1 5
""") == "5"

# no feeders
assert run("""1
3 0
1 2 3
""") == "0 0 0"

# full overlap
assert run("""1
4 2
1 1 1 1
1 4 10
2 3 5
""") == "1 1 1 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single small overlap | 2 5 2 | correctness of overlap accumulation |
| n=1 case | 5 | boundary handling for r+1 |
| no feeders | 0 0 0 | empty update handling |
| full overlap mix | 1 1 1 1 | capacity clamping dominance |

## Edge Cases

A minimal single-chicken case with a single feeder tests whether the r+1 subtraction breaks array bounds. For input $n=1$, $l=r=1$, the update writes to `diff[2]`, which is valid because the array is sized $n+2$. The prefix sum produces the correct coverage, and clamping ensures the final value equals $\min(a_1, c_1)$.

A case with no feeders ensures the prefix sum remains zero everywhere. The algorithm correctly outputs zeros regardless of capacities, since no range updates ever activate.

A fully overlapping set of feeders tests accumulation correctness. Every index receives the sum of all feeder values, and the final min operation ensures that even very large overlaps are capped independently per position, confirming that per-index independence is preserved.
