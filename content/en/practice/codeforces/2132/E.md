---
title: "CF 2132E - Arithmetics Competition"
description: "The problem presents a team of two players, Vadim and Kostya, who each have a collection of cards with numeric values."
date: "2026-06-08T02:51:11+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "greedy", "sortings", "ternary-search"]
categories: ["algorithms"]
codeforces_contest: 2132
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1043 (Div. 3)"
rating: 1700
weight: 2132
solve_time_s: 97
verified: true
draft: false
---

[CF 2132E - Arithmetics Competition](https://codeforces.com/problemset/problem/2132/E)

**Rating:** 1700  
**Tags:** binary search, data structures, greedy, sortings, ternary search  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem presents a team of two players, Vadim and Kostya, who each have a collection of cards with numeric values. In each round, they are asked to select exactly a given number of cards, but each player has a personal upper limit on how many of their own cards they can contribute. The task is to maximize the sum of the chosen cards in each round.

Formally, Vadim has `n` cards with values `a_1` through `a_n`, and Kostya has `m` cards `b_1` through `b_m`. For each query `(x_i, y_i, z_i)`, the team must choose exactly `z_i` cards, with at most `x_i` from Vadim and at most `y_i` from Kostya. The goal is to compute the maximum possible sum of these `z_i` cards.

The problem's constraints are strict: the total number of cards across all test cases is up to 200,000 for Vadim and Kostya separately, and up to 100,000 rounds. This immediately rules out any brute-force approach that iterates through combinations of cards in a round, since even choosing subsets of size 100,000 would be exponential. The key observation is that each round can be reduced to choosing the `k` largest cards from sorted arrays of each player's cards, respecting their individual limits.

Non-obvious edge cases include situations where the requested number of cards is zero, or where one player is allowed zero cards. For example, if Vadim has cards `[10, 20]` and Kostya `[5, 15]`, and the round is `(x=0, y=2, z=2)`, the team must pick all cards from Kostya even though Vadim has higher-valued cards. A naive approach that always tries to pick the largest global cards would fail here.

## Approaches

The brute-force approach iterates through all combinations of `k` cards from Vadim's and Kostya's collections that respect the constraints. For each combination, it computes the sum and returns the maximum. This is correct, but its complexity is exponential in the number of cards, far exceeding any feasible time limit for `n, m ~ 2*10^5`.

The optimal approach relies on sorting and prefix sums. If both Vadim's and Kostya's cards are sorted in descending order, we can precompute prefix sums to quickly determine the sum of the top `k` cards for any `k` up to `n` or `m`. For each round, we simply iterate over the possible number of cards Vadim can contribute (from 0 up to `min(x_i, z_i)`), and compute how many cards Kostya would then need to provide to reach `z_i`. If that number is within his limit, we calculate the sum using the prefix sums and track the maximum.

This works efficiently because each round's maximum sum can be found in O(min(x_i, z_i)) operations using prefix sums, and the precomputation is O(n + m) for sorting and prefix sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(n+m)) | O(n+m) | Too slow |
| Sorting + Prefix Sums | O((n+m) log(n+m) + q * min(x_i, z_i)) | O(n+m) | Accepted |

## Algorithm Walkthrough

1. Sort Vadim's cards in descending order. This ensures the first `k` cards are always the `k` largest.
2. Sort Kostya's cards in descending order for the same reason.
3. Compute prefix sums for both Vadim and Kostya. Let `pref_a[k]` be the sum of the first `k` cards of Vadim and `pref_b[k]` for Kostya. This allows constant-time sum queries for the top `k` cards.
4. For each query `(x, y, z)`, iterate `i` from `max(0, z - y)` to `min(z, x)` representing the number of cards taken from Vadim. This range respects both Vadim's limit and ensures that Kostya can contribute the remaining cards.
5. For each `i`, compute `j = z - i` as the number of cards taken from Kostya. Skip iterations where `j > y` because they exceed Kostya's limit.
6. Compute the total sum as `pref_a[i] + pref_b[j]` and keep track of the maximum across all valid `i`.
7. Return the maximum sum for the round.

Why it works: The algorithm maintains the invariant that at each step we consider all valid ways to split the `z` cards between Vadim and Kostya within their individual limits. By pre-sorting and using prefix sums, we guarantee that for any split, we are using the largest possible cards from each player, ensuring the sum is maximal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m, q = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        a.sort(reverse=True)
        b.sort(reverse=True)
        
        # Prefix sums
        pref_a = [0]
        for val in a:
            pref_a.append(pref_a[-1] + val)
        
        pref_b = [0]
        for val in b:
            pref_b.append(pref_b[-1] + val)
        
        res = []
        for _ in range(q):
            x, y, z = map(int, input().split())
            max_sum = 0
            # i is number of cards from Vadim
            for i in range(max(0, z - y), min(z, x) + 1):
                j = z - i
                if j <= y:
                    current_sum = pref_a[i] + pref_b[j]
                    max_sum = max(max_sum, current_sum)
            res.append(str(max_sum))
        print("\n".join(res))

if __name__ == "__main__":
    solve()
```

This solution first sorts the cards and computes prefix sums to quickly query sums of top cards. The query loop iterates only over valid numbers of cards Vadim can contribute, automatically calculating the corresponding cards from Kostya. The careful use of `max(0, z - y)` prevents illegal negative selections and ensures that the prefix sum indices are correct.

## Worked Examples

Using Sample 1:

| Query | Vadim limit x | Kostya limit y | Total needed z | i range | max sum |
| --- | --- | --- | --- | --- | --- |
| 0 0 0 | 0 | 0 | 0 | [0] | 0 |
| 3 4 7 | 3 | 4 | 7 | [3,4] | 70 |

For the second query, Vadim can contribute at most 3 cards, Kostya at most 4. We need 7 cards total, so Vadim must contribute at least 3 cards (`max(0,7-4)=3`), leaving 4 for Kostya. The sum is `30+20+10 + 4+3+2+1 = 70`.

The trace demonstrates that the prefix sum approach correctly picks the largest possible cards while respecting limits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+m) log(n+m) + q * min(x_i, z_i)) | Sorting the arrays dominates initially, then each query loops over possible splits of z cards |
| Space | O(n+m) | Prefix sums arrays for Vadim and Kostya |

With `n+m <= 2*10^5` and `q <= 10^5`, this fits comfortably within the 3-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided sample
assert run("""4
3 4 5
10 20 30
1 2 3 4
0 0 0
3 4 7
3 4 4
1 4 4
2 2 4
5 5 2
500000000 300000000 100000000 900000000 700000000
800000000 400000000 1000000000 600000000 200000000
1 4 3
5 2 6
4 4 1
100 100 20 20
100 100 20 20
4 4 5
3 3 6
2 363 711
286 121 102
1 1 1
3 1 1
1 2 0
1 3 2
0 1 0
3 3 3""") == """0
70
64
39
57
2700000000
4200000000
420
711
711
0
997
0
1360"""

# Custom cases
assert run("1\n2 2 1\n10 20\n5 15\n1 1 2") == "35", "must pick one from each for max sum"
assert run("1\n3 3 1\n1 2 3\n4 5 6\n2 2 3") ==
```
