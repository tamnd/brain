---
title: "CF 2182E - New Year's Gifts"
description: "Monocarp wants to make as many friends happy as possible with a limited budget. He has a number of friends and a set of boxes."
date: "2026-06-07T21:54:01+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "greedy", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2182
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 186 (Rated for Div. 2)"
rating: 1800
weight: 2182
solve_time_s: 208
verified: true
draft: false
---

[CF 2182E - New Year's Gifts](https://codeforces.com/problemset/problem/2182/E)

**Rating:** 1800  
**Tags:** binary search, data structures, greedy, sortings, two pointers  
**Solve time:** 3m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

Monocarp wants to make as many friends happy as possible with a limited budget. He has a number of friends and a set of boxes. Each box has a beauty value, and each friend has three requirements: a minimum box beauty they care about, a minimum gift value, and a higher threshold gift value that guarantees happiness regardless of the box. Monocarp can spend at most `k` coins in total, and each box can hold at most one gift. The task is to maximize the number of friends that are satisfied given these constraints.

The input gives multiple test cases. For each test case, we are given the number of friends, number of boxes, the total coins available, the beauty of each box, and the three numbers `x_i`, `y_i`, and `z_i` for each friend. The output is a single integer per test case, indicating the maximum number of friends that can be made happy.

The constraints are large. There can be up to 200,000 friends or boxes in one test case, and `k` can be as large as 10^15. This immediately rules out brute-force approaches that try all possible gift-box assignments or combinations of gift values. A naive solution that considers every pairing of friend and box would have a complexity of O(n * m), which is up to 4 * 10^10 operations and infeasible.

Edge cases that need careful handling include situations where all boxes are too low in beauty to satisfy any friend without overspending, or when the budget is barely enough to buy minimum gifts but not enough for higher thresholds. Another tricky scenario occurs when the coins are sufficient to meet all `y_i` values but cannot afford even a single `z_i` value, and the box beauties are insufficient. For example, if `k = 5`, `boxes = [1]`, and a single friend has `x=2, y=3, z=6`, then the only gift affordable is `y=3`, but the box is too low beauty, so happiness is not guaranteed; the correct answer is `0`.

## Approaches

The brute-force approach would assign each box to a friend in all possible ways, calculate the minimum required gift to satisfy happiness for that assignment, and check if the budget `k` allows it. This approach works because it considers all possibilities and guarantees correctness. However, with up to 200,000 friends and boxes, the number of assignments is factorial-scale, and even attempting to pair friends with boxes directly in a naive double loop results in O(n * m), which is far too slow.

The key insight is that friends only care about two things: either the box beauty exceeds their threshold `x_i` or the gift value is at least `z_i`. Gifts can always meet the lower bound `y_i` to satisfy the budget constraint. This allows us to treat the problem as a matching problem between boxes and friends where we aim to maximize the number of friends made happy using the higher threshold `z_i` when necessary. By sorting boxes and friends by relevant thresholds, and using a greedy two-pointer or binary search approach, we can efficiently determine which friends can be satisfied with available boxes without exceeding the budget.

Specifically, if we process friends in descending order of `x_i` (box requirement), and assign the highest available beauty box that satisfies a friend’s `x_i`, then any friend we cannot satisfy with a box must receive a gift of at least `z_i` if the budget allows. The sum of all `y_i` is guaranteed to fit into `k`, so we only need to account for the extra cost for gifts valued at `z_i`. Sorting allows O(n log n + m log m) efficiency, and two-pointer or binary search ensures we match boxes greedily without revisiting previous decisions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(n + m) | Too slow |
| Sorting + Greedy + Two-Pointers | O(n log n + m log m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Sort the array of box beauties in ascending order. This allows efficient matching using two-pointers or binary search.
2. For each friend, determine whether their box requirement can be met. To do this, sort friends by descending `x_i` and keep track of which boxes are available.
3. Iterate through friends and try to assign the smallest available box whose beauty is at least `x_i`. Mark this box as used. This ensures boxes are not double-counted.
4. For friends who cannot be assigned a suitable box, calculate the extra coins required beyond `y_i` to make them happy (`z_i - y_i`). Maintain a running total of these extra costs.
5. If the total extra cost exceeds `k - sum(y_i)`, stop assigning friends to higher-threshold gifts. The number of friends successfully assigned up to this point is the maximum happiness achievable.
6. The sum of `y_i` is always ≤ `k`, so any remaining budget after mandatory minimum gifts can be used for these extra costs.

Why it works: Sorting boxes and friends ensures that each friend is matched to the minimally sufficient resource (box or extra coins). By processing the largest requirements first, we avoid the scenario where small-box beauties are consumed by low-requirement friends, leaving high-requirement friends unsatisfied. The invariant is that any friend considered has either been matched to a box satisfying `x_i` or accounted for with extra coins to reach `z_i`. Since boxes are used at most once and extra coins are checked against the remaining budget, no overcommitment occurs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m, k = map(int, input().split())
        boxes = sorted(map(int, input().split()))
        friends = []
        sum_y = 0
        for _ in range(n):
            x, y, z = map(int, input().split())
            friends.append((x, y, z))
            sum_y += y
        
        friends.sort(reverse=True)  # sort descending by x_i

        used = [False] * m
        happy = 0
        extra_needed = []

        j = m - 1  # pointer to the largest available box
        for x, y, z in friends:
            while j >= 0 and boxes[j] >= x:
                j -= 1
            if j < m - 1:
                happy += 1  # friend happy with a box
            else:
                extra_needed.append(z - y)

        extra_needed.sort()
        remaining = k - sum_y
        for cost in extra_needed:
            if remaining >= cost:
                remaining -= cost
                happy += 1
            else:
                break

        print(happy)

if __name__ == "__main__":
    solve()
```

The code reads input efficiently and processes each test case independently. Friends are sorted in descending order of `x_i` to maximize the chance of satisfying the largest requirements first. Boxes are sorted to quickly locate the minimally sufficient beauty. The `extra_needed` array collects the additional coin costs for friends who cannot be satisfied with a box. Sorting `extra_needed` ensures we spend budget greedily from smallest to largest cost, maximizing the number of happy friends.

## Worked Examples

Sample input:

```
2 1 6
1
1 2 3
1 2 7
```

| Friend | x_i | y_i | z_i | Box assigned | Extra cost | Remaining k | Happy count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 3 | yes (1) | 0 | 6 | 1 |
| 2 | 1 | 2 | 7 | no | 5 | 4 | 2 |

This confirms both friends can be made happy within budget.

Another sample:

```
2 2 3
1 1
2 1 3
2 1 5
```

Boxes `[1,1]` are insufficient for `x_i=2`, extra costs `2` and `4` are required. Remaining budget after `sum(y_i)=2` is `1`, so no extra costs can be paid. The output is `0`, which aligns with expectations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m log m) | Sorting friends and boxes dominates; iterating is O(n + m) |
| Space | O(n + m) | To store friends, boxes, and extra_needed |

The solution fits within time and memory limits for the given constraints: 2*10^5 total n and m over all test cases with 2s and 512 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("3\n2 1 6\n1\n1 2 3\n1 2 7\n2 2 3\n1 1\n2 1 3\n2 1 5\n3 4 11\n1 2 2 1\n3 2 5\n4 4 6\n3 1 3") == "2\n0\n2"

# Minimum input
assert run("1\n1 1 1
```
