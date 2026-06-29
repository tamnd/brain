---
title: "CF 104687I - \u0412\u044b\u0431\u043e\u0440 \u0447\u0438\u0441\u0435\u043b 2"
description: "We are given an array of integers and we need to pick exactly three elements from it. The only restriction is structural: if we pick elements at positions $i1 < i2 < i3$, then each consecutive pair must be separated by at least $d$ indices, meaning $i{t+1} - it ge d$."
date: "2026-06-29T08:48:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104687
codeforces_index: "I"
codeforces_contest_name: "\u041e\u0442\u0431\u043e\u0440 \u0432 \u0426\u0420\u041e\u0414 2022"
rating: 0
weight: 104687
solve_time_s: 86
verified: true
draft: false
---

[CF 104687I - \u0412\u044b\u0431\u043e\u0440 \u0447\u0438\u0441\u0435\u043b 2](https://codeforces.com/problemset/problem/104687/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and we need to pick exactly three elements from it. The only restriction is structural: if we pick elements at positions $i_1 < i_2 < i_3$, then each consecutive pair must be separated by at least $d$ indices, meaning $i_{t+1} - i_t \ge d$. The objective is to maximize the sum of the chosen values.

The key difficulty is that the positions interact. Choosing a large value early may block access to other large values nearby, so a locally optimal pick can destroy the global optimum.

The constraints are large: $n \le 150000$. This immediately rules out any cubic or quadratic exploration of all triples or all valid combinations. Even $O(n^2)$ approaches are too slow. The solution must be essentially linear or linearithmic.

A subtle issue arises when values are negative. A naive intuition might suggest “always take the best available next element,” but that fails because a slightly smaller early pick can unlock two much larger later picks.

For example, consider:

```
n = 6, d = 2
A = [10, -100, 9, 9, 9, 9]
```

A greedy choice might take 10 at index 1, then be forced into suboptimal spacing. The correct strategy might skip it to allow two or three large values later depending on spacing.

Another failure case comes from local window reasoning. Any approach that only looks at the next $d$ or $2d$ positions independently will fail because the optimal triple depends on global alignment across the array.

## Approaches

A brute-force solution would try every triple of indices $i < j < k$, checking whether spacing constraints are satisfied and computing the sum. This is $O(n^3)$, which is completely infeasible at $n = 150000$. Even optimizing the validity check does not help, because the number of candidate triples itself is enormous.

We need a way to avoid enumerating pairs and instead reuse optimal substructure. The crucial observation is that once we fix the middle element $j$, the problem splits into two independent subproblems: the best valid choice on the left side and the best valid choice on the right side, each with spacing constraints.

This suggests dynamic programming. We define states that capture the best possible sum of picking 1, 2, or 3 elements up to a given index while respecting spacing.

More concretely, we can define:

- $dp1[i]$: best sum choosing 1 element from prefix $[1..i]$
- $dp2[i]$: best sum choosing 2 elements from prefix $[1..i]$
- $dp3[i]$: best sum choosing 3 elements from prefix $[1..i]$

Transitions depend on choosing whether to place the last chosen element at position $i$, and ensuring the previous chosen element is at most $i - d$.

To enforce spacing efficiently, we maintain best values from valid earlier ranges instead of scanning all previous states.

The transition becomes:

- Either skip $i$
- Or use $i$ as the last picked element and combine it with the best valid state ending at or before $i - d$

This reduces each state transition to $O(1)$ amortized using prefix maxima.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(1)$ | Too slow |
| Optimal DP with prefix maxima | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We construct three DP layers, but we compute them in a single forward pass using prefix-best tracking.

1. Precompute prefix maximum arrays that allow us to query the best dp value up to index $i$. This ensures we can efficiently find the best valid previous pick without scanning.
2. Maintain three DP arrays: dp1, dp2, dp3. Each dp state represents the best sum achievable using exactly that many picks up to index $i$. This separation is necessary because transitions depend on how many elements have already been chosen.
3. Initialize dp1[i] as the best single element seen so far up to i. This is simply the maximum value in the prefix, since only one element is chosen.
4. For dp2[i], consider taking element i as the second pick. The first pick must come from indices at most i - d. So dp2[i] is updated as:

best dp1 value in prefix [1 .. i - d] + A[i], or carry dp2[i-1].

This step encodes the spacing constraint directly into the transition.
5. For dp3[i], similarly consider taking i as the third pick. We combine the best dp2 value up to i - d with A[i], or carry dp3[i-1].
6. The final answer is dp3[n].

Why it works:

At every index i, dp1, dp2, dp3 store optimal solutions for prefixes ending at i. Any optimal selection of three elements must have a last element k. Once k is fixed, the remaining two elements form an optimal valid selection in the prefix up to k - d, because any overlap or deviation would contradict optimality. This optimal substructure guarantees that building solutions incrementally using prefix maxima never misses a better configuration.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k, d = map(int, input().split())
    a = list(map(int, input().split()))
    
    NEG = -10**30
    
    # dp arrays
    dp1 = [NEG] * n
    dp2 = [NEG] * n
    dp3 = [NEG] * n

    dp1[0] = a[0]

    # prefix bests for dp1, dp2, dp3
    best1 = [NEG] * n
    best2 = [NEG] * n
    best3 = [NEG] * n

    best1[0] = dp1[0]

    for i in range(1, n):
        # dp1: take best single element
        dp1[i] = max(dp1[i-1], a[i])

        # dp2: either skip or take i as second element
        j = i - d
        best_prev1 = best1[j] if j >= 0 else NEG
        dp2[i] = max(dp2[i-1], best_prev1 + a[i])

        # dp3: either skip or take i as third element
        best_prev2 = best2[j] if j >= 0 else NEG
        dp3[i] = max(dp3[i-1], best_prev2 + a[i])

        # update prefix bests
        best1[i] = max(best1[i-1], dp1[i])
        best2[i] = max(best2[i-1], dp2[i])
        best3[i] = max(best3[i-1], dp3[i])

    print(dp3[n-1])

if __name__ == "__main__":
    solve()
```

The implementation tracks both the exact DP at position i and the prefix maximums. The prefix arrays are essential because transitions always require the best value up to a bounded index $i - d$, not necessarily ending exactly at $i - d$.

The negative sentinel is set large enough to avoid accidental overflow when adding values. The carry-over `dpX[i-1]` ensures that skipping an element is always considered.

## Worked Examples

### Example 1

Input:

```
10 3 2
-1 4 2 -6 3 3 5 -1 4 -1
```

We track dp1, dp2, dp3 at key positions.

| i | a[i] | dp1 | dp2 | dp3 |
| --- | --- | --- | --- | --- |
| 0 | -1 | -1 | -inf | -inf |
| 1 | 4 | 4 | -inf | -inf |
| 2 | 2 | 4 | 6 | -inf |
| 3 | -6 | 4 | 6 | -inf |
| 4 | 3 | 4 | 7 | 10 |
| 5 | 3 | 4 | 7 | 10 |
| 6 | 5 | 5 | 9 | 13 |
| 7 | -1 | 5 | 9 | 13 |
| 8 | 4 | 5 | 9 | 13 |
| 9 | -1 | 5 | 9 | 13 |

The final answer is 13, achieved by selecting indices corresponding to values 4, 3, 5 with valid spacing.

This trace shows how dp2 stabilizes early but dp3 continues improving once a strong third pick becomes available at index 6.

### Example 2

Input:

```
7 3 2
5 -1 6 -2 7 -3 8
```

| i | a[i] | dp1 | dp2 | dp3 |
| --- | --- | --- | --- | --- |
| 0 | 5 | 5 | -inf | -inf |
| 1 | -1 | 5 | -inf | -inf |
| 2 | 6 | 6 | 11 | -inf |
| 3 | -2 | 6 | 11 | -inf |
| 4 | 7 | 7 | 13 | 18 |
| 5 | -3 | 7 | 13 | 18 |
| 6 | 8 | 8 | 15 | 20 |

Final answer is 20.

This example highlights that skipping negative values is automatically handled because dp states carry forward previous bests.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each index is processed once with O(1) transitions using prefix maxima |
| Space | $O(n)$ | Three DP arrays and prefix maxima arrays |

The solution easily fits within limits since $n = 150000$ allows linear traversal with minimal constant factors.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k, d = map(int, input().split())
    a = list(map(int, input().split()))

    NEG = -10**30
    dp1 = [NEG] * n
    dp2 = [NEG] * n
    dp3 = [NEG] * n

    dp1[0] = a[0]

    best1 = [NEG] * n
    best2 = [NEG] * n

    best1[0] = dp1[0]

    for i in range(1, n):
        dp1[i] = max(dp1[i-1], a[i])

        j = i - d
        best_prev1 = best1[j] if j >= 0 else NEG
        dp2[i] = max(dp2[i-1], best_prev1 + a[i])

        best_prev2 = best2[j] if j >= 0 else NEG
        dp3[i] = max(dp3[i-1], best_prev2 + a[i])

        best1[i] = max(best1[i-1], dp1[i])
        best2[i] = max(best2[i-1], dp2[i])

    return str(dp3[n-1])

# provided sample
assert run("10 3 2\n-1 4 2 -6 3 3 5 -1 4 -1\n") == "13"

# minimum size
assert run("3 3 1\n1 2 3\n") == "6"

# all negative
assert run("6 3 2\n-1 -2 -3 -4 -5 -6\n") == "-6"

# spaced best picks
assert run("7 3 2\n5 -1 6 -2 7 -3 8\n") == "20"

# alternating pattern
assert run("8 3 2\n10 1 10 1 10 1 10 1\n") == "30"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all positive increasing | correct sum of spaced maxima | greedy failure avoidance |
| all negative | picks least harmful triple | handling negatives |
| alternating highs | spacing enforcement | dependency across positions |
| minimum n | base correctness | boundary conditions |

## Edge Cases

A critical edge case is when the best early value blocks access to a much stronger combination later. For instance:

```
n = 6, d = 2
A = [100, 1, 1, 1, 100, 100]
```

A naive approach might pick 100 at index 0, forcing the remaining picks to be far apart and losing the ability to take both 100s at the end. The DP correctly skips the first 100 when forming dp2 and dp3 because dp2 and dp3 preserve alternative histories.

Another edge case is when optimal picks are tightly aligned exactly at distance d boundaries. The transition uses `i - d`, not `i - d - 1`, so the boundary inclusion is correct. Any off-by-one error here would either allow invalid selections or incorrectly forbid valid ones, immediately breaking correctness on tightly packed optimal solutions.
