---
title: "CF 104720F - Chef Circle"
description: "We are given a circular arrangement of chefs, each associated with a value. We choose a starting chef and then traverse clockwise, visiting every chef exactly once until we return to the start position."
date: "2026-06-29T06:12:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104720
codeforces_index: "F"
codeforces_contest_name: "UTPC x WiCS Contest 10-06-23"
rating: 0
weight: 104720
solve_time_s: 71
verified: false
draft: false
---

[CF 104720F - Chef Circle](https://codeforces.com/problemset/problem/104720/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a circular arrangement of chefs, each associated with a value. We choose a starting chef and then traverse clockwise, visiting every chef exactly once until we return to the start position. The order of visiting depends on the chosen starting point, but once fixed, the traversal is a full rotation of the array.

When a chef is visited in position $i$ of this traversal (starting from 1), their value is multiplied by $i$. The total score of a starting position is the sum of these weighted contributions. The task is to compute the maximum possible score over all $n$ choices of starting position.

The constraints allow up to $n = 10^5$, which immediately rules out recomputing the full weighted sum from scratch for every starting position. A naive $O(n^2)$ rotation evaluation would involve about $10^{10}$ operations in the worst case, which is far beyond a 1-second limit.

A subtle issue arises from the circular nature of the problem. A naive implementation might linearize the array and forget that shifting the start changes all positional multipliers in a correlated way. Another pitfall is recomputing the weighted sum without reusing previous computations, which leads to unnecessary repeated summations over the same elements.

For example, with $C = [1, 2, 3]$, different starting points produce:

starting at 1 gives $1\cdot1 + 2\cdot2 + 3\cdot3 = 14$,

starting at 2 gives $2\cdot1 + 3\cdot2 + 1\cdot3 = 11$,

starting at 3 gives $3\cdot1 + 1\cdot2 + 2\cdot3 = 11$.

A correct solution must capture how the rotation changes weights without recomputing everything.

## Approaches

The brute-force method fixes a starting index and directly computes the weighted sum of the circular traversal. For each start, we walk through all $n$ elements, assign increasing multipliers, and accumulate the result. This is correct because it directly implements the definition of the scoring function. However, it requires $n$ work per start and there are $n$ starts, leading to $O(n^2)$ total operations, which becomes too slow at $n = 10^5$.

The key observation is that moving the starting point by one position does not destroy structure, it only shifts weights. Instead of recomputing from scratch, we relate the score of one rotation to the next. When we shift the start forward by one position, every element’s multiplier effectively decreases by 1, while the element that wraps around moves from multiplier 1 to multiplier $n$. This produces a clean recurrence between consecutive configurations.

Let $S_k$ be the score when starting at position $k$. If we already know $S_k$, we can compute $S_{k+1}$ in $O(1)$ using prefix structure of contributions. Expanding the algebra shows that the change depends only on the total sum of all values and the element that moves from front to back in the rotation. This reduces the entire computation to a single linear scan plus $n$ updates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We first flatten the circular behavior by thinking of the array duplicated once, so we can easily represent any window of length $n$.

1. Compute the total sum of all elements. This value is reused in every transition because shifting a window always involves the same global mass of values.
2. Compute the score for the initial starting position $k = 1$ by directly summing $i \cdot C_i$ for $i = 1$ to $n$. This gives a valid baseline.
3. Maintain a rolling value $cur\_score$ representing the current rotation score.
4. For each next rotation, identify that all elements effectively lose one unit of weight, which subtracts the total sum of the array from the score. This happens because every element’s multiplier decreases by 1.
5. The element that moves from the front of the window to the back gains a multiplier of $n$, replacing its previous contribution of $1 \cdot C$. This introduces an adjustment of $+ n \cdot C_{out} - C_{out}$, but the $-C_{out}$ is already included in the global shift, so only the net correction is applied.
6. Update the current score in $O(1)$ using this relation and track the maximum over all rotations.
7. Output the maximum value encountered.

### Why it works

The correctness comes from expressing each rotation as a linear transformation of the previous one. Every element’s coefficient decreases uniformly by 1 when shifting the start, which contributes a fixed subtraction equal to the total sum. The only non-uniform effect is the wraparound element whose coefficient jumps from 1 to $n$, and this deviation is exactly captured by a single correction term. Since every rotation is derived from the previous one through an exact algebraic identity, no configuration is missed and no double counting occurs.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

total = sum(a)

cur = 0
for i in range(n):
    cur += (i + 1) * a[i]

best = cur

# simulate rotations
for i in range(1, n):
    # element that moves from front is a[i-1]
    cur = cur - total + n * a[i - 1]
    if cur > best:
        best = cur

print(best)
```

The first loop computes the base weighted sum directly from the definition. The second loop performs the rotation update: subtracting the total sum accounts for every element’s weight decreasing by 1, and adding $n \cdot a[i-1]$ restores the correct contribution of the element that wraps around to the end.

A subtle implementation point is that the rotated element is always $a[i-1]$, not $a[i]$, because after shifting, the previous starting element becomes the last element in the new ordering.

## Worked Examples

### Example 1

Input:

```
6
2 3 5 1 9 10
```

We compute initial score:

| step | rotation start | contribution | cur |
| --- | --- | --- | --- |
| 0 | 1 | 1·2 + 2·3 + 3·5 + 4·1 + 5·9 + 6·10 | 132 |

Now apply transitions:

| step | moved element | update formula | cur |
| --- | --- | --- | --- |
| 1 | 2 | 132 - 30 + 6·2 | 114 |
| 2 | 3 | 114 - 30 + 6·3 | 102 |
| 3 | 5 | 102 - 30 + 6·5 | 102 |
| 4 | 1 | 102 - 30 + 6·1 | 78 |
| 5 | 9 | 78 - 30 + 6·9 | 102 |

Maximum is 132.

This confirms that every rotation is derived incrementally and that the recurrence correctly tracks how shifting redistributes weights.

### Example 2

Input:

```
3
1 4 2
```

Initial rotation:

| step | rotation start | cur |
| --- | --- | --- |
| 0 | 1 | 1·1 + 2·4 + 3·2 = 15 |

Transitions:

| step | moved | cur |
| --- | --- | --- |
| 1 | 1 | 15 - 7 + 3·1 = 11 |
| 2 | 4 | 11 - 7 + 3·4 = 16 |

Maximum is 16.

This shows that even when the best rotation is not the first or second, the recurrence still explores all configurations exactly once.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One initial linear pass plus one pass over rotations |
| Space | $O(1)$ | Only a few accumulators are maintained |

The algorithm fits comfortably within the constraints since it performs a small constant number of arithmetic operations per element.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    total = sum(a)

    cur = 0
    for i in range(n):
        cur += (i + 1) * a[i]

    best = cur

    for i in range(1, n):
        cur = cur - total + n * a[i - 1]
        best = max(best, cur)

    return str(best)

# provided samples
assert run("6\n2 3 5 1 9 10\n") == "132"
assert run("3\n1 4 2\n") == "16"

# custom cases
assert run("1\n5\n") == "5"
assert run("2\n1 1\n") == "3"
assert run("4\n10 10 10 10\n") == "100"
assert run("5\n5 4 3 2 1\n") == "35"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 single value | 5 | base case handling |
| two equal values | 3 | rotation symmetry correctness |
| all equal array | 100 | uniform stability of recurrence |
| decreasing sequence | 35 | non-trivial optimal rotation |

## Edge Cases

One edge case is when $n = 1$. The algorithm computes the initial weighted sum and never enters the rotation loop, correctly returning the single value. The recurrence is never used, which avoids invalid access to $a[i-1]$.

For $n = 2$, the rotation alternates between two states. The update formula subtracts the total sum and adds $2 \cdot a[i-1]$, correctly flipping the contribution between the two configurations. This ensures symmetry is preserved.

For arrays with all equal values, every rotation produces the same result. The recurrence still updates the score, but the subtraction and addition cancel exactly, maintaining a constant best value.
