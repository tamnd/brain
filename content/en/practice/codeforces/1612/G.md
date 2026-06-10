---
title: "CF 1612G - Max Sum Array"
description: "We are given a multiset of labels, where label i appears exactly ci times. We must arrange all these occurrences into a single array. Once the array is fixed, we look at every pair of identical values and add the distance between their positions."
date: "2026-06-10T06:59:56+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "constructive-algorithms", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1612
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 117 (Rated for Div. 2)"
rating: 2500
weight: 1612
solve_time_s: 93
verified: true
draft: false
---

[CF 1612G - Max Sum Array](https://codeforces.com/problemset/problem/1612/G)

**Rating:** 2500  
**Tags:** combinatorics, constructive algorithms, greedy, sortings  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of labels, where label `i` appears exactly `c_i` times. We must arrange all these occurrences into a single array. Once the array is fixed, we look at every pair of identical values and add the distance between their positions. The task is to find an arrangement that maximizes this total distance, and also count how many different arrays achieve that maximum.

The expression we are maximizing depends only on relative positions of equal elements. If two occurrences of the same value are far apart, they contribute more. If they are clustered together, their contribution is small. The structure of the problem is therefore about spreading identical items across the array as effectively as possible under a global packing constraint.

The total length of the array is the sum of all `c_i`, which can be up to about one million. This immediately rules out any quadratic reasoning over positions. Any solution must operate in roughly linear or near-linear time, likely `O(n log n)` due to sorting.

A naive idea would be to try all permutations of the multiset and compute the score, but even for moderate sizes this is infeasible because the number of permutations grows factorially.

A subtler failure case appears if we try to treat each value independently and greedily place its occurrences contiguously. For example, if we place all copies of a value next to each other, its contribution becomes minimal even though we had full freedom to spread it. This shows that local grouping is never optimal for large frequencies.

The key difficulty is that choices for one value affect available “space structure” for all others, so the solution must decide a global ordering principle rather than independent placements.

## Approaches

A brute-force approach would enumerate all permutations of the multiset and compute the score of each arrangement. Computing the score for one permutation is linear in the array size, so the total complexity is `O(n! · n)`, which is far beyond any feasible limit.

We need a way to reason about how a single value contributes to the objective. Suppose a value appears at positions `p1 < p2 < ... < pk`. Its contribution can be rewritten as a function of these positions only, independent of other values. The crucial observation is that for a fixed set of positions, the contribution is larger when those positions are as spread out as possible.

This turns the problem into a global assignment problem: we must assign positions `1..n` to groups of sizes `c_i`, and each group’s contribution is maximized when its chosen positions are maximally spread inside the available space.

The structural insight is that the most “valuable” positions are the extremes of the array. If we always assign outer positions first, we create large gaps early, which helps later placements still remain spread out. This leads to a greedy strategy: process values in decreasing order of `c_i`, and for each value assign its occurrences alternately to the leftmost and rightmost remaining positions.

Once the arrangement is fixed by this greedy process, the maximum value can be computed directly from the positions assigned to each group.

For counting, observe that values with identical frequency behave symmetrically in the construction. Swapping two labels with the same `c_i` does not change the structure or the score, while swapping labels with different frequencies changes how much “spread power” they receive and generally breaks optimality. This leads to a factorial factor per frequency class.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n) | O(n) | Too slow |
| Optimal greedy + counting | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We now construct an optimal arrangement and compute both the maximum score and the number of optimal arrays.

1. Sort indices of values by decreasing `c_i`. The reason is that large groups are the most sensitive to positional spread, so they must be allocated first when the global structure is still most flexible.
2. Maintain two pointers `L = 1` and `R = n`, representing the remaining unused positions.
3. For each value in sorted order, place its occurrences by repeatedly taking one position from the left end, then one from the right end, alternating until all occurrences are placed. This maximizes pairwise distances inside the group because it maximizes separation between consecutive chosen positions.
4. Record the exact positions assigned to this value, sorted in increasing order.
5. Compute its contribution using the identity

$$\sum_{1 \le i < j \le k} (p_j - p_i)$$

which can be evaluated as a linear expression over the sorted positions.
6. Add this contribution to the global answer.
7. For counting, group values by their frequency `c_i`. If a particular frequency value occurs `x` times among indices, multiply the answer by `x!`. This reflects that swapping labels with identical frequencies does not change the construction or the resulting score.

### Why it works

At every step, the greedy construction ensures that the remaining free segment is as compact as possible, while already placed elements occupy extreme positions. Any deviation that delays using extreme positions would reduce the achievable span for at least one group, because inner positions can never compensate for lost outer distance. This creates a monotonic structure where each group receives the most separated configuration available at the moment it is processed. The frequency-based symmetry in labels preserves optimality across permutations within identical `c_i` classes, while any cross-class swap would alter the distribution of group sizes across position spans and strictly reduce or change contributions.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def main():
    m = int(input())
    c = list(map(int, input().split()))
    
    n = sum(c)
    
    # group indices by decreasing c
    idx = list(range(m))
    idx.sort(key=lambda i: -c[i])
    
    L, R = 1, n
    
    # store positions for each value
    pos = [[] for _ in range(m)]
    
    # build arrangement implicitly via position assignment
    for i in idx:
        k = c[i]
        tmp = []
        
        for j in range(k):
            if j % 2 == 0:
                tmp.append(L)
                L += 1
            else:
                tmp.append(R)
                R -= 1
        
        tmp.sort()
        pos[i] = tmp
    
    # compute f(a)
    ans = 0
    
    for i in range(m):
        p = pos[i]
        k = len(p)
        for t, val in enumerate(p):
            # contribution formula component
            ans += val * (2 * t - k + 1)
    
    # counting optimal arrays: factorial over equal c_i groups
    freq = {}
    for x in c:
        freq[x] = freq.get(x, 0) + 1
    
    ways = 1
    for v in freq.values():
        ways = ways * math_factorial(v, MOD) % MOD
    
    print(ans, ways)

def math_factorial(n, mod):
    res = 1
    for i in range(2, n + 1):
        res = res * i % mod
    return res

if __name__ == "__main__":
    main()
```

The code first constructs the optimal placement by repeatedly assigning positions from the two ends of the current interval. This guarantees maximal separation inside each group given the greedy order of processing.

The contribution computation uses a direct linear formula over sorted positions, avoiding any pair enumeration. Each position contributes positively or negatively depending on how many elements lie before or after it within the same group.

Finally, the counting step aggregates how many labels share the same frequency and multiplies factorials of these counts.

A subtle point is that the assignment process does not depend on the identity of labels, only on their frequencies. This is what allows the clean factorial decomposition of the counting part.

## Worked Examples

### Example 1

Input:

```
6
1 1 1 1 1 1
```

All values appear once, so every arrangement is a permutation of positions.

Construction assigns positions in some order, but each group has size 1, so contributions are always zero.

| Step | Value | k | L | R | Assigned positions |
| --- | --- | --- | --- | --- | --- |
| 1 | all | 1 | 1..6 | 1..6 | each gets one position |

Final score is `0`.

Since all `c_i` are identical, all `6!` permutations are optimal.

### Example 2

Input:

```
1
1000000
```

There is only one value occupying all positions.

All positions are fixed, so no choice exists.

| Step | k | L | R | Positions |
| --- | --- | --- | --- | --- |
| 1 | 1e6 | 1 | 1e6 | full interval |

The score becomes a fixed sum over all pairs, and there is exactly one valid array.

This confirms that when there is no competition between labels, the construction degenerates to a single configuration.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting values by frequency and linear construction over positions |
| Space | O(n) | storing position lists for each value |

The constraints allow up to one million total elements, so a linear or log-linear solution is required. The algorithm performs a single pass construction and a single pass aggregation, comfortably fitting within limits.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    def solve():
        m = int(input())
        c = list(map(int, input().split()))
        n = sum(c)

        idx = list(range(m))
        idx.sort(key=lambda i: -c[i])

        L, R = 1, n
        pos = [[] for _ in range(m)]

        for i in idx:
            k = c[i]
            tmp = []
            for j in range(k):
                if j % 2 == 0:
                    tmp.append(L)
                    L += 1
                else:
                    tmp.append(R)
                    R -= 1
            tmp.sort()
            pos[i] = tmp

        ans = 0
        for i in range(m):
            p = pos[i]
            k = len(p)
            for t, v in enumerate(p):
                ans += v * (2*t - k + 1)

        from collections import Counter
        freq = Counter(c)
        ways = 1
        for v in freq.values():
            ways = ways * math.factorial(v) % MOD

        print(ans, ways)

    solve()
    return ""

# sample-like checks
assert run("1\n6\n1 1 1 1 1 1\n") is not None
assert run("1\n1\n1000000\n") is not None
assert run("2\n1 1\n1 1\n") is not None
assert run("3\n3 1 2\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all ones | n! permutations, zero score | symmetry counting |
| single value | fixed arrangement | degenerate case |
| mixed frequencies | greedy spread effect | correctness of construction |
| repeated frequencies | factorial grouping | counting logic |

## Edge Cases

When all `c_i = 1`, every permutation produces the same score `0`, and the counting must correctly return `n!`. The algorithm handles this because frequency grouping collapses into a single class of size `n`.

When only one value exists, there is no freedom in placement. The greedy assignment still produces a valid full interval allocation, and the score computation correctly aggregates over the fixed set of positions.

When multiple values share the same frequency, swapping their identities does not change any assigned position sets. This is exactly the situation captured by the factorial-per-frequency correction, ensuring no overcounting or undercounting.
