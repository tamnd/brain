---
title: "CF 1538A - Stone Game"
description: "We are given a row of stones, each with a distinct integer power. Polycarp can remove stones only from either end of the row. His goal is to remove both the stone with the minimum power and the stone with the maximum power in as few moves as possible."
date: "2026-06-10T14:51:29+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1538
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 725 (Div. 3)"
rating: 800
weight: 1538
solve_time_s: 360
verified: false
draft: false
---

[CF 1538A - Stone Game](https://codeforces.com/problemset/problem/1538/A)

**Rating:** 800  
**Tags:** brute force, dp, greedy  
**Solve time:** 6m  
**Verified:** no  

## Solution
## Problem Understanding

We are given a row of stones, each with a distinct integer power. Polycarp can remove stones only from either end of the row. His goal is to remove both the stone with the minimum power and the stone with the maximum power in as few moves as possible. Each test case provides the number of stones and their powers in order. The output for each case is the minimum number of moves needed to remove both extreme stones.

The constraints are small: at most 100 stones per test case and at most 100 test cases. This means an algorithm that is quadratic in `n` would still run in under 2 seconds, but we can also aim for a linear scan solution per test case. The small bounds also allow us to reason carefully about edge cases like when the minimum and maximum stones are at the same end, or when one is at the first position and the other is at the last.

Non-obvious edge cases include situations where removing stones from the same end is optimal, for example when the min and max are both near the left or both near the right. A careless approach that always removes one from each end might produce a suboptimal answer. For instance, if `a = [1, 3, 2]`, removing from opposite ends could take three moves, but removing both from the left takes only two.

## Approaches

A brute-force approach would be to simulate all sequences of removing stones from either end and track the first time both extreme stones are removed. There are `2^(n)` possible sequences of left/right choices, which is clearly infeasible even for `n = 100`. While the brute-force is conceptually correct, it is too slow.

The key insight comes from noticing that we only care about the positions of the minimum and maximum stones. Let `l_min` and `l_max` denote the 1-based indices of the smallest and largest stones from the left. Let `r_min` and `r_max` denote the distance from the right end (or equivalently, `n - l + 1`). Then the problem reduces to choosing one of four strategies:

1. Remove both stones from the left end. The number of moves is the larger of `l_min` and `l_max`.
2. Remove both stones from the right end. The number of moves is the larger of `r_min` and `r_max`.
3. Remove the minimum from the left and the maximum from the right. Moves are `l_min + r_max`.
4. Remove the maximum from the left and the minimum from the right. Moves are `l_max + r_min`.

The answer is the minimum among these four quantities. This observation avoids simulating moves entirely and runs in linear time per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For a given array `a` of length `n`, scan once to find the indices of the minimum and maximum stones. Keep them as `l_min` and `l_max`, 1-based.
2. Compute the distances from the right end as `r_min = n - l_min + 1` and `r_max = n - l_max + 1`.
3. Compute the four candidate numbers of moves:

- `from_left = max(l_min, l_max)` for taking both from the left.
- `from_right = max(r_min, r_max)` for taking both from the right.
- `min_left_max_right = l_min + r_max` for min from left and max from right.
- `max_left_min_right = l_max + r_min` for max from left and min from right.
4. The answer is the minimum of these four values.

Why it works: The invariant is that no matter what sequence of removals we choose, any optimal solution will remove the extreme stones either by taking them from the same end or from opposite ends. Considering these four configurations exhausts all possibilities. The algorithm never underestimates the number of moves because it explicitly calculates the moves required to remove both extremes.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    l_min = l_max = -1
    min_val, max_val = min(a), max(a)
    
    for i in range(n):
        if a[i] == min_val:
            l_min = i + 1
        if a[i] == max_val:
            l_max = i + 1
            
    r_min = n - l_min + 1
    r_max = n - l_max + 1
    
    ans = min(
        max(l_min, l_max),
        max(r_min, r_max),
        l_min + r_max,
        l_max + r_min
    )
    print(ans)
```

The code first reads the number of test cases. For each array, it finds the positions of the minimum and maximum elements. Distances from the right end are computed so that we can evaluate the four strategies. The final answer is the minimum among them. Care must be taken with 1-based indexing to match the formula for right-end distances.

## Worked Examples

For the input:

```
5
5
1 5 4 3 2
```

We compute `l_min = 1`, `l_max = 2`, `r_min = 5`, `r_max = 4`.

| Strategy | Moves |
| --- | --- |
| Left end | max(1,2) = 2 |
| Right end | max(5,4) = 5 |
| Min left, max right | 1 + 4 = 5 |
| Max left, min right | 2 + 5 = 7 |

Minimum moves = 2. This shows that removing both from the left is optimal.

For the input:

```
8
2 1 3 4 5 6 8 7
```

`l_min = 2`, `l_max = 7`, `r_min = 7`, `r_max = 2`.

| Strategy | Moves |
| --- | --- |
| Left end | max(2,7) = 7 |
| Right end | max(7,2) = 7 |
| Min left, max right | 2 + 2 = 4 |
| Max left, min right | 7 + 7 = 14 |

Minimum moves = 4. Here taking min from left and max from right is optimal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Linear scan to find min and max positions |
| Space | O(1) | Only a few integer variables needed |

With `t` up to 100 and `n` up to 100, the total number of operations is under 10^4, which is negligible for a 2-second limit. Memory usage is minimal and well below 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    # copy solution here
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        l_min = l_max = -1
        min_val, max_val = min(a), max(a)
        for i in range(n):
            if a[i] == min_val:
                l_min = i + 1
            if a[i] == max_val:
                l_max = i + 1
        r_min = n - l_min + 1
        r_max = n - l_max + 1
        ans = min(max(l_min, l_max), max(r_min, r_max), l_min + r_max, l_max + r_min)
        print(ans)
    return out.getvalue().strip()

# Provided samples
assert run("5\n5\n1 5 4 3 2\n8\n2 1 3 4 5 6 8 7\n8\n4 2 3 1 8 6 7 5\n4\n3 4 2 1\n4\n2 3 1 4\n") == "2\n4\n5\n3\n2"

# Custom cases
assert run("1\n2\n1 2\n") == "2"  # minimum input
assert run("1\n3\n3 1 2\n") == "2"  # max at start, min in middle
assert run("1\n4\n4 1 2 3\n") == "2"  # both extremes at ends
assert run("1\n5\n5 4 3 2 1\n") == "2"  # both extremes at opposite ends
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 stones: `1 2` | 2 | Minimum input size, straightforward left/right removal |
| 3 stones: `3 1 2` | 2 | Maximum at start, minimum in middle |
| 4 stones: `4 1 2 3` | 2 | Both extremes near opposite ends, confirms min/max calculation |
| 5 stones |  |  |
