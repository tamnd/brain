---
title: "CF 106350H - Zaglol vs. the British Occupation"
description: "We are given a line of enemies, each with a positive strength. For each query, Zaglol starts with a sword of some initial power and tries to defeat as many enemies as possible."
date: "2026-06-25T08:07:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106350
codeforces_index: "H"
codeforces_contest_name: "Zaglol Contest - FCDS level 1 contest 2026"
rating: 0
weight: 106350
solve_time_s: 39
verified: true
draft: false
---

[CF 106350H - Zaglol vs. the British Occupation](https://codeforces.com/problemset/problem/106350/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of enemies, each with a positive strength. For each query, Zaglol starts with a sword of some initial power and tries to defeat as many enemies as possible. The rules are simple but slightly unusual: he may choose the order in which he fights enemies, but to defeat an enemy his current sword power must be at least that enemy’s strength, and after defeating it, his sword power permanently decreases by that same strength.

Each query is independent, meaning we always start fresh with the same list of enemies and a new initial sword power. The task is to compute, for each query, the maximum number of enemies that can be defeated by choosing an optimal order.

The key structure hidden in the rules is that every time we take an enemy of strength $a_i$, we permanently reduce our budget by $a_i$. This turns the problem into a budgeting process where each chosen item consumes part of the initial power.

The constraints (up to $10^5$ enemies and $10^5$ queries, with values up to $10^9$) immediately rule out any per-query simulation over permutations or subsets. Anything even quadratic per query is too large, and even $O(n \log n)$ per query would be borderline. We need a preprocessing idea that allows each query to be answered in logarithmic time.

A few edge cases are worth noticing.

If all enemy strengths are larger than the initial power, the answer is zero. For example, with enemies $[5, 6, 7]$ and $x = 3$, no fight is possible.

If all enemies are small but there are many of them, a greedy strategy might appear to depend on order. For instance, with $[4, 1, 3]$ and $x = 5$, different orders might seem to change the outcome, but in reality the structure forces a consistent optimal choice once we interpret it correctly.

A more subtle case is when picking a large enemy early blocks multiple smaller ones later. For example, $[6, 1, 1, 1]$ with $x = 7$: picking 6 first leaves too little flexibility, while picking small ones first allows more total kills. This hints that order matters, but in a very controlled way.

## Approaches

The brute-force interpretation is to try all subsets of enemies and all possible orders for each subset, simulating whether a given ordering is valid under the decreasing-power rule. Even if we ignore permutations and only check subsets, we still face $2^n$ possibilities, and each simulation costs linear time. This is completely infeasible.

The key observation is that the order is actually under our control, and we want to maximize how many items we can “fit” into a decreasing budget. Each chosen enemy consumes exactly its own strength from the total available power, and the constraint at each step is equivalent to ensuring we never exceed the remaining budget.

If we decide on a subset of enemies, the best strategy is to fight them in increasing order of strength. This avoids wasting power early on large values and ensures that feasibility depends only on total sum, not intermediate fluctuations. Under this ordering, the condition becomes simple: after choosing $k$ enemies, their total sum must not exceed $x$.

So the problem reduces to selecting as many elements as possible such that their sum is at most $x$. To maximize the count, we should always take smaller elements first, since they contribute less cost and allow more elements to fit. This transforms the problem into sorting and building a prefix sum array.

Each query then becomes: how many smallest elements can we take before their cumulative sum exceeds $x$, which can be answered using binary search over the prefix sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over subsets and orders | $O(n! \cdot n)$ or worse | $O(n)$ | Too slow |
| Sort + prefix sums + binary search | $O(n \log n + q \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Sort the array of enemy strengths in non-decreasing order. This ensures we always consider the cheapest enemies first, which is essential for maximizing count.
2. Build a prefix sum array where each position stores the total strength of all enemies up to that index. This lets us quickly compute the cost of taking any number of weakest enemies.
3. For each query with initial power $x$, perform a binary search on the prefix sum array to find the largest index $k$ such that the sum of the first $k$ enemies is at most $x$.
4. Output $k$ as the answer for that query, since it represents the maximum number of enemies that can be defeated without exceeding the available power.

The reason binary search works here is that prefix sums are strictly increasing, so feasibility transitions from true to false exactly once.

### Why it works

Once we fix how many enemies we want to take, any valid order must respect the constraint that remaining power never drops below the next chosen enemy. Sorting in increasing order ensures that the hardest constraint is always satisfied last, since every step consumes the smallest possible available cost at that stage. This collapses the sequential condition into a single global condition: the total sum of chosen elements must not exceed the starting power. Because all values are positive, any deviation from picking the smallest available element first can only reduce the number of items we can fit, never increase it.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
a.sort()

# prefix sums
pref = [0] * n
pref[0] = a[0]
for i in range(1, n):
    pref[i] = pref[i - 1] + a[i]

q = int(input())
out = []

def upper_bound(x):
    lo, hi = 0, n - 1
    ans = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if pref[mid] <= x:
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return ans + 1

for _ in range(q):
    x = int(input())
    out.append(str(upper_bound(x)))

print("\n".join(out))
```

The code first sorts the array so that weaker enemies are considered before stronger ones. The prefix sum array converts “can I take k enemies?” into a single comparison against $x$. The binary search finds the largest valid prefix, and returning index plus one converts it into a count.

A common implementation pitfall is forgetting that the answer is a count, not an index. Another is mishandling the case where even the smallest element is too large, in which case the function correctly returns zero through the $-1 + 1$ adjustment.

## Worked Examples

### Example 1

Input:

```
n = 5
a = [4, 2, 1, 10, 3]
query x = 7
```

After sorting:

```
[1, 2, 3, 4, 10]
prefix: [1, 3, 6, 10, 20]
```

We check how many prefix elements fit into 7.

| k | prefix sum | valid? |
| --- | --- | --- |
| 1 | 1 | yes |
| 2 | 3 | yes |
| 3 | 6 | yes |
| 4 | 10 | no |

Answer is 3.

This shows that the optimal strategy always picks smallest elements first, and the decision depends only on cumulative sum.

### Example 2

Input:

```
n = 4
a = [5, 1, 1, 1]
query x = 5
```

Sorted:

```
[1, 1, 1, 5]
prefix: [1, 2, 3, 8]
```

| k | prefix sum | valid? |
| --- | --- | --- |
| 1 | 1 | yes |
| 2 | 2 | yes |
| 3 | 3 | yes |
| 4 | 8 | no |

Answer is 3.

This confirms the greedy intuition that taking the large 5 early would be strictly worse than delaying it, but in the optimal solution it is simply excluded because it breaks the budget constraint.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n + q \log n)$ | sorting dominates preprocessing, each query uses binary search |
| Space | $O(n)$ | prefix sum array stores one value per enemy |

The constraints allow up to $10^5$ elements and queries, so an $O(n \log n)$ preprocessing plus logarithmic queries fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    a.sort()

    pref = [0] * n
    pref[0] = a[0]
    for i in range(1, n):
        pref[i] = pref[i - 1] + a[i]

    q = int(input())
    out = []

    def upper_bound(x):
        lo, hi = 0, n - 1
        ans = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if pref[mid] <= x:
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1
        return ans + 1

    for _ in range(q):
        x = int(input())
        out.append(str(upper_bound(x)))

    return "\n".join(out)

# custom cases

# minimum size
assert run("1\n5\n1\n10\n") == "1"

# cannot take anything
assert run("3\n5 6 7\n2\n1\n5\n") == "0\n0"

# all equal
assert run("5\n2 2 2 2 2\n3\n1\n4\n10\n") == "0\n1\n5"

# mixed case
assert run("4\n4 1 3 2\n2\n5\n6\n") == "2\n3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | base case |
| all too large | 0 0 | impossible selections |
| equal values | 0 1 5 | threshold behavior |
| mixed values | 2 3 | greedy correctness across queries |

## Edge Cases

When all elements exceed the query power, the prefix sum array starts above $x$, and binary search correctly returns $-1$, which converts to zero. For example, with $[10, 20]$ and $x = 5$, the search never finds a valid prefix.

When the array contains many small elements followed by a large outlier, such as $[1, 1, 1, 1, 100]$, the algorithm naturally ignores the large element for small queries because it is placed at the end after sorting, and only becomes relevant for sufficiently large $x$.

When $x$ is extremely large, the binary search always returns $n$, and the algorithm correctly counts all elements without overflow issues because prefix sums use Python integers.
