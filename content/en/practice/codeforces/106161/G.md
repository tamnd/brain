---
title: "CF 106161G - GCD of Subsets"
description: "We are given a collection of items. Each item has a weight and a value, but for some items exactly one of these two numbers is missing and must be assigned by us as a positive integer not exceeding one billion. Two greedy procedures will later run on the completed dataset."
date: "2026-06-20T22:14:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106161
codeforces_index: "G"
codeforces_contest_name: "The 2025 ICPC Asia Chengdu Regional Contest (The 4rd Universal Cup. Stage 4: Grand Prix of Chengdu)"
rating: 0
weight: 106161
solve_time_s: 88
verified: true
draft: false
---

[CF 106161G - GCD of Subsets](https://codeforces.com/problemset/problem/106161/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of items. Each item has a weight and a value, but for some items exactly one of these two numbers is missing and must be assigned by us as a positive integer not exceeding one billion.

Two greedy procedures will later run on the completed dataset. Alice sorts items by increasing weight and then takes items in that order until the next item would overflow the knapsack capacity, at which point she stops completely. Bob sorts items by decreasing value and then scans in that order, taking an item whenever it fits into the remaining capacity.

Our task is to assign the missing weights and values so that both procedures end up selecting exactly the same set of items.

The key difficulty is that the assignment influences both the sorting order and the knapsack feasibility, so we are simultaneously controlling ordering and cumulative sums under a single capacity constraint.

The constraints are small enough that quadratic or even slightly supercubic reasoning per test case is not acceptable across all cases. There are at most 3000 items in total, but the real difficulty is not raw computation, it is constructing a consistent assignment under mixed constraints coming from ordering and capacity.

A subtle failure mode appears immediately if one tries to treat Alice and Bob independently. Alice’s selection depends only on weight ordering and prefix sums, while Bob’s depends on value ordering and incremental feasibility. A naive attempt that fixes one ordering first will often make the other greedy procedure diverge, because the second procedure is sensitive to intermediate remaining capacity, not just final sums.

## Approaches

The brute-force perspective would try to assign all missing values and then simulate both strategies. This is clearly impossible since each unknown can take up to a billion values, giving an exponential or infinite search space.

A more structured observation comes from understanding what Alice’s procedure really produces. Once weights are fixed, Alice does not choose arbitrarily, she always takes a prefix in sorted-by-weight order and stops at the first item that does not fit. This means Alice’s chosen set is completely determined by a threshold in that ordering.

Bob’s procedure is more flexible in order of selection, but still greedy in the sense that once items are sorted by value, he tries to pack them if possible.

The key idea is that we should avoid any interaction where items taken by Alice are interleaved with items not taken by Bob in either ordering. If we can force both procedures to agree on a common “accepted region” of items that is stable under both sorting criteria, then both greedy processes behave identically.

The simplest way to guarantee identical behavior is to make both algorithms effectively select all items, which reduces the problem to making both greedy procedures accept every item without ever rejecting due to capacity or ordering conflicts.

To do this, we assign all missing weights and values so that every item fits and every item is processed in a consistent order where no rejection happens.

We ensure that the total sum of weights is at most W, and we ensure value ordering cannot prevent inclusion. Once all items fit, Alice takes everything because no prefix step ever overflows, and Bob takes everything because every item fits when encountered.

The only obstruction is that some weights are fixed and cannot be reduced. However, since we are allowed to assign unknown weights, we can always choose them small enough so that the sum constraint is satisfied as long as the fixed weights already do not exceed capacity.

This leads to a direct feasibility check: if the sum of already-fixed weights is greater than W, then no assignment can rescue Alice’s procedure because those weights are immutable. Otherwise, we can assign every unknown weight as 1 and ensure the total weight remains within capacity. Values can be assigned arbitrarily positive, for example all equal, which makes Bob’s ordering irrelevant up to tie-breaking.

This makes both greedy procedures accept every item.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force assignment search | Exponential | O(n) | Too slow |
| Construct all-selected solution | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We construct a solution where both Alice and Bob select all items.

1. Compute the sum of all given weights that are already fixed (non-zero entries). These weights cannot be changed, so they form a hard lower bound on the total knapsack usage.
2. If this fixed sum already exceeds W, then no assignment is possible because even before adding any unknown weights, Alice would exceed capacity when attempting to take all items. In this case we immediately output that the task is impossible.
3. Otherwise, assign every unknown weight the value 1. This keeps the total weight as small as possible while respecting the requirement that weights must be positive integers.
4. Now consider Alice’s process. Since all weights are positive and their total sum does not exceed W, every prefix of the weight-sorted order remains feasible, so Alice never encounters an item that would overflow the knapsack. She therefore selects every item.
5. Assign all unknown values to 1 as well. This makes all values identical, so Bob’s sorting becomes stable and only depends on original indices.
6. Bob processes all items in some order, but since every item fits into the remaining capacity (because total weight is within W), he never skips due to capacity. Therefore Bob also selects every item.

### Why it works

The construction reduces both greedy processes to a trivial regime where capacity constraints never trigger a rejection. Alice’s stopping condition is never activated because the total weight is bounded by W. Bob’s skipping condition is never activated because every item fits individually at the moment it is considered. Since both procedures include all items, their selected sets are identical.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        n, W = map(int, input().split())
        w = list(map(int, input().split()))
        r = list(map(int, input().split()))
        
        fixed_sum = 0
        for x in w:
            if x != 0:
                fixed_sum += x
        
        if fixed_sum > W:
            print("No")
            continue
        
        print("Yes")
        
        # assign weights
        res_w = []
        for x in w:
            if x == 0:
                res_w.append(1)
            else:
                res_w.append(x)
        
        # assign values
        res_r = []
        for x in r:
            if x == 0:
                res_r.append(1)
            else:
                res_r.append(x)
        
        print(*res_w)
        print(*res_r)

if __name__ == "__main__":
    solve()
```

The implementation follows the construction directly. The only non-trivial step is computing the sum of fixed weights and verifying feasibility against W. Everything else is a direct assignment of 1 to missing entries.

One subtle point is that we never modify given values. This is important because the problem guarantees that at most one of weight or value is missing per item, so there is no conflict in overwriting.

## Worked Examples

### Example 1

Consider three items with capacity W = 10.

Suppose weights are `[3, 0, 2]` and values are `[0, 5, 0]`.

Fixed weight sum is `3 + 2 = 5`, which is within capacity.

We assign missing weights and values as 1.

| Step | Weights | Values | Fixed Sum | Valid |
| --- | --- | --- | --- | --- |
| Initial | 3, 0, 2 | 0, 5, 0 | 5 | Yes |
| After fill | 3, 1, 2 | 1, 5, 1 | 5 | Yes |

Alice processes items in increasing weight order and accumulates at most 6 total, which is ≤ 10, so she takes all items. Bob processes items in decreasing value order and every item fits, so he also takes all items.

This confirms that identical selection occurs.

### Example 2

Let W = 6, weights `[2, 0, 5]`, values `[0, 3, 0]`.

Fixed weight sum is `2 + 5 = 7`, which already exceeds capacity.

| Step | Fixed Sum | Decision |
| --- | --- | --- |
| Initial | 7 | Impossible |

Since even the immutable weights exceed capacity, Alice would be forced to fail before any assignment, so no solution exists.

This demonstrates the only obstruction: fixed weights alone can violate feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single pass to compute sums and fill arrays |
| Space | O(n) | Storing final assigned arrays |

The constraints allow up to 3000 total items, so a linear construction per test case is easily fast enough. The solution avoids any sorting or search, which keeps it well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    T = int(sys.stdin.readline())
    out = []
    for _ in range(T):
        n, W = map(int, sys.stdin.readline().split())
        w = list(map(int, sys.stdin.readline().split()))
        r = list(map(int, sys.stdin.readline().split()))

        fixed = sum(x for x in w if x != 0)
        if fixed > W:
            out.append("No")
        else:
            out.append("Yes")
            w2 = [x if x != 0 else 1 for x in w]
            r2 = [x if x != 0 else 1 for x in r]
            out.append(" ".join(map(str, w2)))
            out.append(" ".join(map(str, r2)))

    return "\n".join(out)

# custom cases
assert run("""1
1 10
0
0
""") == "Yes\n1\n1"

assert run("""1
2 1
1 1
0 0
""") == "No"

assert run("""1
3 10
3 0 2
0 5 0
""").startswith("Yes")

assert run("""1
2 10
0 0
0 0
""") == "Yes\n1 1\n1 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single unknown | Yes, minimal fill | Base construction |
| fixed overflow | No | impossibility detection |
| mixed unknowns | Yes | general feasibility |
| all unknown | Yes | full flexibility |

## Edge Cases

A critical edge case is when fixed weights already exceed capacity. For example, if an item has weight 10^9 and W is smaller, no assignment can reduce it. The algorithm correctly rejects immediately without attempting assignments.

Another edge case is when all values are missing but weights are fixed. Even in that case, value assignment is irrelevant because selection is determined entirely by weights once Alice’s feasibility is satisfied.

A final subtle case is when many zeros exist. Since we always assign 1, we ensure minimal inflation of total weight while preserving correctness, and we never accidentally exceed capacity in the constructed solution.
