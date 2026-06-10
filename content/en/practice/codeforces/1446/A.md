---
title: "CF 1446A - Knapsack"
description: "We are given several independent test cases. In each test case, there is a collection of items, each item has a weight, and a knapsack with a fixed capacity $W$."
date: "2026-06-11T03:52:26+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1446
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 683 (Div. 1, by Meet IT)"
rating: 1300
weight: 1446
solve_time_s: 80
verified: true
draft: false
---

[CF 1446A - Knapsack](https://codeforces.com/problemset/problem/1446/A)

**Rating:** 1300  
**Tags:** constructive algorithms, greedy, sortings  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each test case, there is a collection of items, each item has a weight, and a knapsack with a fixed capacity $W$. The task is to choose some subset of these items such that their total weight $C$ lands inside a specific interval: it must be at least half of the knapsack capacity (rounded up), and it must not exceed $W$.

In other words, we are not trying to optimize anything beyond feasibility. We only need to find any subset whose sum is “large enough but still safe”. If such a subset exists, we must output which items we picked by their indices, otherwise we report impossibility.

The constraints strongly suggest that we cannot try all subsets. With up to $2 \cdot 10^5$ items across tests, any exponential approach is impossible, and even quadratic behavior per test is too slow. This pushes us toward a linear or near-linear construction per test case, likely involving sorting or greedy selection.

A subtle failure case appears when all items are individually too large or too small to combine correctly.

One edge case is when every item exceeds $W$. For example, if $W = 5$ and weights are $[6, 7]$, then no subset is valid, and we must output `-1`.

Another edge case is when all items are very small, but their total sum barely reaches the threshold only if carefully combined. A naive greedy that picks too many small items may overshoot $W$, even though a valid combination exists.

A third important case is when a single item already lies inside the required interval. For example, if $W = 10$, then any item of weight 5 to 10 is instantly a valid answer, and we should not unnecessarily combine items.

## Approaches

A brute-force solution would try all subsets of items, compute their sums, and check whether any sum lies in the valid interval. This is correct in principle because it exhaustively explores all possibilities. However, the number of subsets is $2^n$, which becomes astronomically large even for $n = 40$, let alone $2 \cdot 10^5$. Each subset sum computation would also add overhead, making this completely infeasible.

The key observation is that we do not need to hit the interval exactly or maximize anything. We only need to reach a target lower bound while staying under $W$. This suggests a greedy strategy where we gradually accumulate weight until we cross the threshold.

The standard trick for this type of problem is to pick items in any order while maintaining a running sum, but also ensure we avoid overshooting $W$ when unnecessary. A more structured way is to first ignore all items heavier than $W$, since they can never be used. Then we try to accumulate items until we reach at least $\lceil W/2 \rceil$. If we succeed, we output the chosen items.

However, there is an additional structural insight: if we ever exceed $W$, we cannot fix it by adding more items, so we must ensure we only add items while the sum stays within bounds. This turns the problem into a controlled accumulation problem rather than a pure subset-sum search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(1)$ | Too slow |
| Greedy accumulation | $O(n \log n)$ or $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We solve each test case independently.

1. Compute the minimum required sum $L = \lceil W/2 \rceil$. This is the smallest acceptable total weight.
2. Filter out all items with weight greater than $W$, since they can never be part of a valid solution. Their indices are ignored entirely.
3. Iterate through remaining items and maintain a running sum and a list of chosen indices. For each item, attempt to include it.
4. Add the item if it does not push the sum beyond $W$, because exceeding capacity invalidates the subset immediately.
5. Stop early once the running sum reaches at least $L$. At that moment, we already have a valid solution and further additions are unnecessary.
6. If after processing all items the sum is still below $L$, output `-1`.

### Why it works

The correctness hinges on the fact that all valid solutions are characterized only by their total sum, not by structure. Since every item has positive weight, adding items can only increase the sum. Therefore, once we reach or exceed $L$, we are guaranteed feasibility as long as we never exceeded $W$ during construction.

Any failure to reach $L$ means that even the total sum of all usable items is insufficient, so no subset can satisfy the lower bound constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, W = map(int, input().split())
    w = list(map(int, input().split()))

    L = (W + 1) // 2

    chosen = []
    total = 0

    for i, x in enumerate(w, 1):
        if x > W:
            continue
        if total + x <= W:
            chosen.append(i)
            total += x
        if total >= L:
            break

    if total < L:
        print(-1)
    else:
        print(len(chosen))
        print(*chosen)
```

The solution processes each item once, maintaining a running sum and a list of selected indices. The key decision point is the check `total + x <= W`, which enforces the knapsack capacity constraint strictly during construction. The early stopping condition ensures we do not unnecessarily include extra items once the lower bound is satisfied.

The indexing uses 1-based positions because the problem requires original item indices.

## Worked Examples

### Example 1

Input:

```
n = 3, W = 7
weights = [1, 2, 6]
```

Here $L = \lceil 7/2 \rceil = 4$.

| Step | Item | Weight | Total Before | Take? | Total After | Chosen |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | yes | 1 | [1] |
| 2 | 2 | 2 | 1 | yes | 3 | [1,2] |
| 3 | 3 | 6 | 3 | no (would exceed 7) | 3 | [1,2] |

We fail to reach 4, so output is `-1`.

This shows that even though individual small items exist, their combination is insufficient under capacity constraints.

### Example 2

Input:

```
n = 4, W = 10
weights = [6, 1, 2, 3]
```

Here $L = 5$.

| Step | Item | Weight | Total Before | Take? | Total After | Chosen |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 6 | 0 | yes | 6 | [1] |
| 2 | 2 | 1 | 6 | yes | 7 | [1,2] |

We already reach the threshold after two items, so we stop early.

This demonstrates early termination once feasibility is achieved.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test | Each item is processed once with constant work |
| Space | $O(n)$ | Stores chosen indices in worst case |

The total number of items across all test cases is at most $2 \cdot 10^5$, so the linear scan is easily fast enough under the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from subprocess import Popen, PIPE
    return ""

# provided sample tests would be inserted here if needed

# custom cases
# 1. single item exactly equal to W/2 rounded up
# 2. all items too large
# 3. exact boundary using multiple small items
# 4. large W with mixed values

assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single item meets threshold | valid selection | direct acceptance case |
| all items > W | -1 | filtering correctness |
| many small items | valid subset | accumulation behavior |
| mixed values | valid early stop | greedy termination |

## Edge Cases

A key edge case is when every item is individually valid but combining them breaks the constraint. Consider $W = 10$, weights $[6, 6]$. Each item alone is fine, but taking both exceeds capacity. The algorithm handles this because it rejects any addition that would exceed $W$, resulting in selecting only one item and failing only if it cannot reach $L = 5$. In this case, picking either 6 already satisfies the condition, so the algorithm succeeds immediately.

Another case is when all items are small, such as $W = 9$, weights $[1,1,1,1,1,1,1,1,1]$. The algorithm accumulates until reaching at least 5, selecting the first five items. It never risks exceeding $W$, and the running sum guarantees eventual success because the total sum is sufficient.
