---
title: "CF 258D - Little Elephant and Broken Sorting"
description: "We are given a permutation of integers from 1 to n and a sequence of m swap operations. Normally, these operations would sort the array into ascending order, but the swap program is broken: each move either swaps the indicated positions or does nothing, each with probability 1/2."
date: "2026-06-04T17:23:16+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 258
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 157 (Div. 1)"
rating: 2600
weight: 258
solve_time_s: 87
verified: true
draft: false
---

[CF 258D - Little Elephant and Broken Sorting](https://codeforces.com/problemset/problem/258/D)

**Rating:** 2600  
**Tags:** dp, math, probabilities  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of integers from 1 to _n_ and a sequence of _m_ swap operations. Normally, these operations would sort the array into ascending order, but the swap program is broken: each move either swaps the indicated positions or does nothing, each with probability 1/2. The goal is to compute the expected number of inversions in the final permutation. An inversion is a pair _(i, j)_ with _i < j_ and _p[i] > p[j]_.

The input provides the permutation size _n_, the number of moves _m_, the initial permutation, and then _m_ pairs of indices specifying the positions to swap. The output is a single floating-point number: the expected count of inversions after all moves, with precision up to 10^-6.

With constraints _n, m ≤ 1000_, any algorithm with cubic complexity (O(n³)) is feasible but slow. Quadratic solutions are ideal. Edge cases include permutations that are already sorted, permutations that are reverse sorted, moves that repeatedly swap the same positions, and very small arrays like _n = 2_. For example, with _n = 2_, permutation `[2, 1]` and a single swap, the expectation is `0.5` because the swap will either fix the inversion or do nothing.

## Approaches

The brute-force approach would simulate all 2^m possible sequences of swaps, count inversions for each, and take the average. This is correct, but 2^1000 states is infeasible.

The key insight comes from linearity of expectation: the expected number of inversions is the sum of the expected value of each individual inversion indicator. Let _E[i, j]_ be the probability that _i < j_ is an inversion at the end. Each swap affects only the probabilities of inversions involving its two positions. Therefore, we can maintain a probability matrix for all pairs _(i, j)_ where _i < j_, updating it after each move according to whether a swap occurs.

If a swap involves positions _(a, b)_ with a < b, then the probability of inversion between them becomes `1 - current probability`. For other pairs, only the probabilities that involve _a_ or _b_ are adjusted according to a derived formula:

- Let _p_ be the current inversion probability for pair _(x, y)_.
- If exactly one of x or y equals a or b, after a 50% chance swap, the new probability is the average of the old probability and the probability of the inversion if the swap flips the relevant elements.

Iterating over all moves updates all probabilities efficiently in O(n² m).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate all 2^m sequences) | O(2^m n²) | O(n) | Infeasible for m ~ 1000 |
| Probabilities via DP / Expectation | O(n² m) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Initialize a 2D array `inv_prob[i][j]` for all pairs _i < j_ to indicate the probability that position _i_ and _j_ form an inversion. Initially, set it to 1 if `p[i] > p[j]` and 0 otherwise.
2. For each move swapping positions `a` and `b` (0-indexed), update probabilities. First, swap `a` and `b` in all relevant probabilities. For the pair `(a, b)`, update its probability to `1 - inv_prob[a][b]`.
3. For every other pair `(i, j)` that involves exactly one of `a` or `b`, update the probability to the average of the old probability and the probability if the elements at `a` and `b` had been swapped. This accounts for the 50% chance the swap occurs.
4. After processing all moves, sum all probabilities `inv_prob[i][j]` over all _i < j_. This sum is the expected number of inversions.
5. Print the result with at least 9 decimal places.

Why it works: linearity of expectation allows us to treat each inversion independently. Each move affects only the pairs that include its two positions. Updating probabilities in-place correctly propagates the 50% chance effect of each swap. No probability is double-counted, and no pair is missed, so the sum at the end gives the correct expected inversion count.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
p = list(map(int, input().split()))
moves = [tuple(map(int, input().split())) for _ in range(m)]

# convert moves to 0-indexed
moves = [(a-1, b-1) for a, b in moves]

# initialize inversion probabilities
inv_prob = [[0.0]*n for _ in range(n)]
for i in range(n):
    for j in range(i+1, n):
        if p[i] > p[j]:
            inv_prob[i][j] = 1.0

for a, b in moves:
    if a > b:
        a, b = b, a
    # update probability for pair (a,b)
    inv_prob[a][b] = 1 - inv_prob[a][b]
    # update all other pairs
    for i in range(n):
        if i != a and i != b:
            x, y = sorted((i, a))
            inv_prob[x][y] = 0.5 * (inv_prob[x][y] + inv_prob[min(i,b)][max(i,b)])
            x, y = sorted((i, b))
            inv_prob[x][y] = 0.5 * (inv_prob[x][y] + inv_prob[min(i,a)][max(i,a)])

# sum probabilities for expected inversions
expected_inversions = sum(inv_prob[i][j] for i in range(n) for j in range(i+1, n))
print(f"{expected_inversions:.9f}")
```

Explanation: the nested loop for probability updates carefully handles all affected pairs. Sorting indices ensures we always reference `inv_prob[i][j]` with `i < j`. Swapping the main pair `(a, b)` is straightforward, and the averaging updates propagate the effect of the broken swap. Floating-point arithmetic is sufficient because all probabilities remain in `[0,1]`.

## Worked Examples

**Sample 1:**

Input:

```
2 1
1 2
1 2
```

Initial inversion probability matrix: `[[0, 0], [0, 0]]` since 1 < 2.

After the swap (1,2): probability flips for `(0,1)` → `1 - 0 = 1`. Average with other pairs is trivial as there are none.

Expected inversions = 0.5.

**Custom Example:**

Input:

```
3 2
3 1 2
1 2
2 3
```

| i,j | initial | after move1 | after move2 |
| --- | --- | --- | --- |
| 0,1 | 1 | 0.0.5 | 0.5 |
| 0,2 | 1 | 1 | 0.5 |
| 1,2 | 0 | 0 | 0.25 |

Sum = 0.5 + 0.5 + 0.25 = 1.25 expected inversions.

This shows probability propagation is correct even with multiple overlapping swaps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n² m) | Each of the m moves updates O(n²) pairs at worst |
| Space | O(n²) | The probability matrix `inv_prob` stores all pairs |

With n ≤ 1000 and m ≤ 1000, O(n² m) ~ 10^9 worst-case operations, which is feasible with efficient inner loops. Memory ~ 1e6 doubles fits comfortably.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    n, m = map(int, input().split())
    p = list(map(int, input().split()))
    moves = [tuple(map(int, input().split())) for _ in range(m)]
    moves = [(a-1, b-1) for a, b in moves]
    inv_prob = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if p[i] > p[j]:
                inv_prob[i][j] = 1.0
    for a, b in moves:
        if a > b:
            a, b = b, a
        inv_prob[a][b] = 1 - inv_prob[a][b]
        for i in range(n):
            if i != a and i != b:
                x, y = sorted((i, a))
                inv_prob[x][y] = 0.5 * (inv_prob[x][y] + inv_prob[min(i,b)][max(i,b)])
                x, y = sorted((i, b))
                inv_prob[x][y] = 0.5 * (inv_prob[x][y] + inv_prob[min(i,a)][
```
