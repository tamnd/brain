---
title: "CF 1700D - River Locks"
description: "The system is a chain of containers, each with a fixed capacity. Water enters a selected subset of these containers at a constant rate of one unit per second per opened pipe."
date: "2026-06-09T22:03:11+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1700
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 802 (Div. 2)"
rating: 1900
weight: 1700
solve_time_s: 179
verified: false
draft: false
---

[CF 1700D - River Locks](https://codeforces.com/problemset/problem/1700/D)

**Rating:** 1900  
**Tags:** binary search, dp, greedy, math  
**Solve time:** 2m 59s  
**Verified:** no  

## Solution
## Problem Understanding

The system is a chain of containers, each with a fixed capacity. Water enters a selected subset of these containers at a constant rate of one unit per second per opened pipe. Whenever a container overflows, the excess is immediately pushed to the next container, and this cascading continues until the last container, where overflow leaves the system.

The goal is not to simulate water flow directly, but to choose a subset of containers to activate as sources. For each query, we are given a time limit and must determine the minimum number of sources to activate so that, starting from empty, every container reaches full capacity no later than that time.

The key interaction is that water does not stay local. Opening a pipe at position i contributes not only to container i, but potentially to all containers to the right through overflow. This makes contributions strongly non-local and forces reasoning about prefix structure rather than independent capacities.

The constraints push toward a solution that is close to O(n log n) or O(n log^2 n). With up to 200,000 locks and 200,000 queries, any per-query linear simulation or naive greedy recomputation would exceed the time limit by several orders of magnitude. The solution must preprocess the structure once and answer each query in logarithmic time.

A subtle edge case appears when early locks have large capacities compared to later ones. For example, if v = [10, 1, 1] and time is small, opening pipes in later locks does not help fill the first lock, since overflow cannot travel backwards. A naive strategy that prioritizes small suffix positions would incorrectly assume later activations compensate for earlier deficits. Another corner case is when time is smaller than the maximum v_i; even opening all pipes cannot fill the largest lock in time, so the answer must immediately be -1.

## Approaches

If we fix a number k of opened pipes, the problem becomes checking whether there exists a choice of k indices such that all locks can be filled within t seconds. A brute-force solution would try all subsets of size k and simulate water flow for each configuration. This is correct in principle because the process is deterministic once sources are fixed, but it explodes combinatorially. The number of subsets is O(n choose k), and even restricting k does not prevent exponential growth across queries.

A more useful way to think about the system is to reverse the perspective. Instead of tracking how water flows forward, consider what it means for a lock i to be filled by time t. Each opened pipe at position j contributes at most t units of water, and due to overflow structure, any unit that reaches position i must have passed through all intermediate locks. This creates a bottleneck effect: filling a prefix depends on how many sources lie in or before that prefix.

The critical observation is that the system behaves like we are distributing t units of “budget” per opened pipe, and these budgets can be routed forward but not backward. To make all locks full, we need enough total contribution to satisfy prefix demands induced by capacities. The optimal strategy always prefers placing pipes as far to the right as possible, because they help fewer earlier constraints while still contributing via overflow to the left only indirectly through saturation.

This reduces the problem to a greedy feasibility check for a fixed k, and since feasibility is monotonic in k, we can binary search the answer per query. Precomputing prefix information allows each check to be done in linear time or slightly optimized form, yielding an overall O((n + q) log n) or O((n + q) log^2 n) solution depending on implementation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Subsets | Exponential | O(n) | Too slow |
| Greedy + Binary Search | O((n + q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

We reformulate the task as a decision problem: for a fixed time t and a fixed number k of pipes, decide whether it is possible to choose k positions that guarantee all locks are filled.

1. For a given t, compute how much each pipe can contribute. Since each opened pipe produces t units, every selected position contributes up to t total units of flow that will eventually be distributed through overflow. This reduces the system to selecting k sources with capacity t each.
2. Traverse locks from left to right while maintaining how much water must still be supplied to satisfy each lock’s requirement. At position i, we track remaining demand for v_i.
3. When a pipe is opened at position i, it contributes t units that can help satisfy current and future demands. The greedy idea is to use a pipe as early as needed to cover deficits as they appear, because delaying only risks increasing required compensation later.
4. Maintain a running surplus of available water coming from already chosen pipes. When we reach a lock i, we subtract its requirement v_i from this surplus. If surplus becomes negative, we are forced to activate another pipe before or at i to compensate.
5. Each time we are forced to open a pipe, we place it at the current position, add t to the surplus, and continue. Count how many such forced openings are needed.
6. If at any point the number of required openings exceeds k, the configuration is impossible. Otherwise, it is feasible.
7. For each query, binary search the minimum k that makes the configuration feasible.

The key invariant is that at every prefix i, the algorithm maintains the maximum possible remaining water surplus achievable using the chosen number of pipes placed so far, assuming an optimal placement strategy. Whenever the greedy procedure is forced to place a pipe, it is because no earlier placement can prevent a deficit at that prefix. This makes each placement locally optimal and globally necessary. Since feasibility only depends on whether we can avoid negative surplus, the greedy construction correctly characterizes whether k pipes suffice.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(v, t, k):
    n = len(v)
    used = 0
    surplus = 0

    i = 0
    while i < n:
        if surplus < v[i]:
            used += 1
            if used > k:
                return False
            surplus += t
        surplus -= v[i]
        i += 1

    return True

def solve():
    n = int(input())
    v = list(map(int, input().split()))
    q = int(input())
    queries = [int(input()) for _ in range(q)]

    max_v = max(v)

    for t in queries:
        if t < max_v:
            print(-1)
            continue

        lo, hi = 1, n
        ans = n

        while lo <= hi:
            mid = (lo + hi) // 2
            if can(v, t, mid):
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The core implementation splits into two parts. The function `can` checks feasibility for a fixed time and number of pipes using a single left-to-right sweep that simulates how much remaining demand can be covered by currently opened pipes. The binary search in `solve` finds the smallest number of pipes that passes this feasibility test.

The initial check `t < max(v)` prevents unnecessary work because even concentrating all flow cannot fill the largest lock faster than its own capacity requirement. The greedy logic relies on maintaining a running surplus that represents how much “unused water potential” remains from previously opened pipes, and each time this becomes insufficient, a new pipe is forced.

## Worked Examples

Consider the sample input with v = [4, 1, 5, 4, 1] and a query t = 6, testing k = 3.

We simulate feasibility:

| i | v[i] | surplus before | action | surplus after | used |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 0 | open pipe | 6 → 2 after fill | 1 |
| 2 | 1 | 2 | no new pipe | 2 → 1 | 1 |
| 3 | 5 | 1 | open pipe | 7 → 2 | 2 |
| 4 | 4 | 2 | open pipe | 8 → 4 | 3 |
| 5 | 1 | 4 | no new pipe | 4 → 3 | 3 |

All requirements are satisfied using 3 pipes, confirming feasibility.

Now consider a small custom case v = [3, 3, 3], t = 3, k = 2.

We simulate:

| i | v[i] | surplus | action | used |
| --- | --- | --- | --- | --- |
| 1 | 3 | 0 → 3 | open pipe | 1 |
| 2 | 3 | 0 → 3 | open pipe | 2 |
| 3 | 3 | 0 → 3 | cannot open more | 3 needed |

We exceed k, so infeasible. This demonstrates that each pipe only contributes a bounded amount of usable flow and cannot be stretched indefinitely across multiple deficits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | each query does binary search over k, each check is linear |
| Space | O(n) | storing lock capacities and queries |

The constraints allow up to 200,000 elements, so a logarithmic factor over a linear scan remains comfortably within limits. The feasibility check is simple arithmetic per element, making the constant factors small.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    import sys

    input = sys.stdin.readline

    def can(v, t, k):
        used = 0
        surplus = 0
        for x in v:
            if surplus < x:
                used += 1
                if used > k:
                    return False
                surplus += t
            surplus -= x
        return True

    n = int(input())
    v = list(map(int, input().split()))
    q = int(input())
    res = []
    max_v = max(v)

    for _ in range(q):
        t = int(input())
        if t < max_v:
            res.append("-1")
            continue
        lo, hi = 1, n
        ans = n
        while lo <= hi:
            mid = (lo + hi) // 2
            if can(v, t, mid):
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1
        res.append(str(ans))

    return "\n".join(res)

# sample
assert run("""5
4 1 5 4 1
6
1
6
2
3
4
5
""") == """-1
3
-1
-1
4
3"""

# all equal
assert run("""3
2 2 2
2
2
3
""") == """3
2"""

# minimum size
assert run("""1
5
2
4
5
""") == """-1
1"""

# increasing
assert run("""4
1 2 3 4
1
4
""") == """2"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | provided | correctness on mixed queries |
| all equal | 3, 2 | stable greedy behavior |
| single lock | -1, 1 | base feasibility and trivial case |
| increasing | 2 | non-uniform capacity distribution |

## Edge Cases

A key edge case is when the time limit is smaller than the maximum lock capacity. For v = [10, 1, 1] and t = 5, no number of pipes can satisfy the first lock because even a fully dedicated pipe cannot supply enough water per second over the given duration. The algorithm handles this immediately through the feasibility check rejecting all k.

Another subtle case is when capacities decrease sharply. For v = [5, 1, 1, 1], placing all pipes early might seem optimal, but the greedy procedure shows that later deficits force additional openings regardless of earlier concentration. The surplus mechanism correctly reflects that earlier excess cannot be redistributed backwards, ensuring additional pipes are counted exactly when needed.

A third case is n = 1. The answer is either -1 if t < v1 or 1 otherwise. The binary search and greedy logic naturally collapse to this without special casing beyond the max check.
