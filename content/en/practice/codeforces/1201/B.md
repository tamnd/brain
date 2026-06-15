---
title: "CF 1201B - Zero Array"
description: "We are given a list of numbers, and we repeatedly perform an operation that picks two different positions and reduces both values by one. The goal is to decide whether we can eventually bring every value down exactly to zero using some sequence of such operations."
date: "2026-06-15T17:33:47+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1201
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 577 (Div. 2)"
rating: 1500
weight: 1201
solve_time_s: 305
verified: true
draft: false
---

[CF 1201B - Zero Array](https://codeforces.com/problemset/problem/1201/B)

**Rating:** 1500  
**Tags:** greedy, math  
**Solve time:** 5m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of numbers, and we repeatedly perform an operation that picks two different positions and reduces both values by one. The goal is to decide whether we can eventually bring every value down exactly to zero using some sequence of such operations.

Each operation consumes exactly one unit from two distinct elements. If you think in terms of “units of work”, every operation removes two units in total, but they must come from two different piles at the same time. The question is whether the initial distribution of units across the array can be completely paired off like this until nothing remains.

The constraint on `n` up to $10^5$ with values up to $10^9$ immediately rules out any simulation of operations. Even if we tried to greedily simulate decrements, the total number of operations could be on the order of $10^9$, which is far beyond feasible limits. The solution must instead rely on a structural condition that can be checked in linear time.

A few subtle failure cases appear if we try naive reasoning. For example, one might think that as long as the sum is even, the answer is “YES”. This fails: consider `[1, 1, 1]`, where the sum is 3 (already odd, so rejected), but also `[2, 2, 1, 1]` has sum 6 and seems promising. However, pairing constraints can still make it impossible if one element dominates too much.

Another naive idea is to greedily pair the largest elements until exhausted. This can fail in cases like `[3, 3, 1, 1]`, where greedy pairing works, but in `[4, 1, 1, 1]`, greedy pairing quickly gets stuck even though the structure itself already guarantees impossibility.

So the real difficulty is not simulation but recognizing when a valid pairing structure exists.

## Approaches

Each operation removes one unit from two distinct indices, so the process can be interpreted as pairing individual unit contributions across different indices. Imagine each array element as a stack of unit tokens. We need to match every token with a token from a different stack.

If we expand the array into a multiset of unit tokens, the task becomes: can we pair all tokens such that no pair comes from the same index? This immediately suggests two necessary conditions.

First, the total number of tokens must be even, because each operation removes exactly two units. If the sum is odd, at least one unit will remain unpaired.

Second, no single element can be too large compared to the rest. If one value exceeds the sum of all others, it is impossible to keep pairing its units with distinct elements, because eventually we run out of external tokens to match it with. Formally, if `max(a)` is greater than `sum(a) - max(a)`, then the largest pile cannot be fully matched.

These two conditions are also sufficient. If they hold, we can always construct pairings greedily without getting stuck, because the large piles are always supported by enough smaller piles to absorb their decrements.

The brute-force idea would simulate operations, always picking two nonzero elements and decrementing them until no moves remain or all zeros are reached. This works conceptually but requires potentially $O(\sum a_i)$ operations, which is infeasible when values are large.

The key insight is that we do not need to simulate pairing; we only need to verify feasibility conditions derived from conservation of units and pairing constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(sum a_i) | O(1) | Too slow |
| Mathematical Check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the total sum of the array. This represents the total number of unit removals required across all operations. Since each operation removes exactly 2 units, this sum must be even for any solution to exist.
2. If the total sum is odd, immediately conclude it is impossible. No sequence of operations can remove a single leftover unit.
3. Identify the maximum element in the array. This value represents the most constrained pile, since every unit in it must be paired with a unit from another index.
4. Compute the sum of all remaining elements excluding the maximum. This represents the total available “external capacity” that can be paired against the largest pile.
5. If the maximum element is greater than this remaining sum, return “NO”. This indicates that even if we used every other element optimally, we would still not have enough distinct units to match all units in the largest pile.
6. Otherwise, return “YES”, since both global parity and local feasibility constraints are satisfied.

### Why it works

The process can be seen as constructing edges in a complete matching where each index contributes as many vertices as its value. The constraints ensure that a perfect matching exists without self-pairing.

The parity condition enforces that a perfect matching is even possible in principle. The dominance condition ensures no vertex set is too large to be matched externally. Together, these guarantee that a greedy pairing process can always continue without getting stuck, because at every stage there remains at least one alternative index to pair with any chosen unit from the largest pile.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    total = sum(a)
    mx = max(a)
    
    if total % 2 != 0:
        print("NO")
        return
    
    if mx > total - mx:
        print("NO")
        return
    
    print("YES")

if __name__ == "__main__":
    solve()
```

The code first computes the sum and maximum in a single pass. The parity check is performed before anything else because it is a strict necessary condition. The second check enforces the feasibility of pairing the largest element against all others combined. The order matters only for early exit efficiency, not correctness.

## Worked Examples

### Example 1

Input:

```
4
1 1 2 2
```

| Step | Total Sum | Max | Remaining Sum | Decision |
| --- | --- | --- | --- | --- |
| 1 | 6 | 2 | 4 | continue |
| 2 | even | - | - | continue |
| 3 | max ≤ rest | - | - | YES |

This confirms both conditions are satisfied, so a full pairing is possible.

### Example 2

Input:

```
3
3 1 1
```

| Step | Total Sum | Max | Remaining Sum | Decision |
| --- | --- | --- | --- | --- |
| 1 | 5 | 3 | 2 | stop |
| 2 | odd | - | - | NO |

The sum is odd, so we immediately reject without considering structure further.

These traces show how the algorithm filters impossible cases early using global invariants instead of local simulation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass to compute sum and maximum |
| Space | O(1) | only a few accumulator variables are used |

The constraints allow up to $10^5$ elements, so a single linear scan is optimal and comfortably within limits. No intermediate structures are needed.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    
    total = sum(a)
    mx = max(a)
    
    if total % 2 != 0:
        return "NO"
    if mx > total - mx:
        return "NO"
    return "YES"

# provided sample
assert run("4\n1 1 2 2\n") == "YES"

# all equal small
assert run("2\n1 1\n") == "YES"

# impossible due to dominance
assert run("3\n4 1 1\n") == "NO"

# odd sum
assert run("3\n1 1 1\n") == "NO"

# large valid
assert run("5\n2 2 2 2 2\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 1 | YES | minimal valid case |
| 3 1 1 1 | NO | odd sum rejection |
| 3 4 1 1 | NO | dominance constraint |
| 5 2 2 2 2 2 | YES | uniform large valid case |

## Edge Cases

A key edge case is when one element is exactly equal to the sum of all others. For example, `[4, 1, 1, 2]`. The total sum is 8, which is even, and the maximum is 4 while the remaining sum is also 4. The condition `mx > total - mx` is false, so the algorithm accepts the case. This is correct because the largest pile can be paired exactly with all remaining units without leftovers.

Another subtle case is `[1, 1]`. The sum is 2, even, and the maximum is 1 while the remaining sum is also 1. The algorithm accepts it, matching the single possible operation, which directly reduces both elements to zero.

A case like `[3, 3, 3]` is rejected because the sum is 9, immediately failing parity. Even though the values are balanced, pairing always removes two units, so one unit inevitably remains.
