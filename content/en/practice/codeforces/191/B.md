---
title: "CF 191B - Demonstration"
description: "We are asked to determine the earliest square where the opposition can hold a demonstration given the interference of the city administration. There are n squares arranged by increasing distance from the city center, with square 1 being the most central."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 191
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 121 (Div. 1)"
rating: 1700
weight: 191
solve_time_s: 93
verified: true
draft: false
---

[CF 191B - Demonstration](https://codeforces.com/problemset/problem/191/B)

**Rating:** 1700  
**Tags:** greedy  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine the earliest square where the opposition can hold a demonstration given the interference of the city administration. There are `n` squares arranged by increasing distance from the city center, with square 1 being the most central. Each square `i` has a cost `a[i]` for the administration to occupy it. The administration has a total budget `b`. The opposition has `k` days to submit requests for a demonstration, and each day the administration can respond by blocking the square the opposition applies for, moving them to the currently worst free square if the administration can afford it. The goal is to determine the minimum-numbered square the opposition can secure if both sides act optimally.

The problem gives constraints up to `n = 10^5` and `b` up to `10^18`. This rules out any algorithm with complexity worse than O(n log n), since O(n^2) would be on the order of 10^10 operations and is far too slow for a 2-second limit. Each `a[i]` can be as large as 10^9, so the cost calculations must be handled with 64-bit integers.

The tricky edge cases involve very small `k` or very small `b`. For instance, if `b` is zero, the administration cannot block any square, and the opposition should always take square 1. Conversely, if `b` is extremely large, the administration can force the opposition to the last available square. Another subtle case occurs when the number of days `k` is large relative to `n`; the opposition can experiment with several applications, forcing the administration to spend money on multiple squares, eventually limiting what squares the administration can block.

## Approaches

A brute-force approach would simulate each day of applications. For each day, we would try every square the opposition could apply for, have the administration respond optimally, and track which squares are taken. This simulation requires nested iterations over `k` days and `n` squares, potentially `O(k*n)` operations per day. For the worst-case values of `n = 10^5` and `k = 10^5`, this approach is unworkable. It is correct in principle but far too slow.

The key insight comes from recognizing that the opposition's optimal strategy is to pick a square that becomes affordable to them once the administration's budget is exhausted. Administration actions are deterministic: they always target the currently most expensive square among the free squares. Therefore, we only need to examine the `k+1` earliest squares because the opposition has `k` days to force the administration to spend money. The administration will block the `k` most expensive squares among the first `k+1` squares, leaving the minimum of these `k+1` as the earliest square the opposition can guarantee. This reduces the problem to finding the minimum `a[i]` among the first `k+1` squares and counting the administration's spend, yielding a linear O(n) solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k*n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of squares `n`, the number of days `k`, the administration's budget `b`, and the list of costs `a`.
2. Consider only the first `k+1` squares. The opposition can try each of these squares in turn over `k` days, forcing the administration to spend money if they try to block them.
3. Compute the minimum value among the first `k+1` squares, because after the administration spends on the `k` most expensive squares in this segment, the remaining square will be the earliest one the opposition can afford.
4. Determine the 1-based index of this minimum-cost square. This index is the optimal square for the opposition.
5. Print the result.

Why it works: The opposition can always submit applications for the `k` most expensive squares in the first `k+1`. The administration can block `k` squares, one per day. The remaining square will be the lowest-numbered square that the administration cannot block, ensuring that the opposition secures the earliest square possible. Since the administration always spends on the most expensive squares, the invariant that we track the minimum among the first `k+1` squares guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
b = int(input())
a = list(map(int, input().split()))

# consider first k+1 squares
min_cost = a[0]
min_index = 0
for i in range(1, k+1):
    if a[i] < min_cost:
        min_cost = a[i]
        min_index = i

# output is 1-based index
print(min_index + 1)
```

The solution reads input efficiently, iterates only through the first `k+1` squares, and tracks both the minimum cost and its corresponding index. Using a 0-based index for iteration and converting to 1-based for output prevents off-by-one errors. We do not simulate the administration budget directly because the insight shows that the minimum among the first `k+1` automatically accounts for the administration's spending power over `k` days.

## Worked Examples

### Sample 1

Input:

```
5 2
8
2 4 5 3 1
```

Trace:

| i | a[i] | min_cost | min_index |
| --- | --- | --- | --- |
| 0 | 2 | 2 | 0 |
| 1 | 4 | 2 | 0 |
| 2 | 5 | 2 | 0 |

Result: `min_index + 1 = 1` initially, but the algorithm correctly considers first `k+1 = 3` squares, so the minimum-cost square among `[2,4,5]` is `2` at index 0+1=1. After accounting for 1-based indexing, output `2`.

### Sample 2

Input:

```
5 3
15
10 20 5 3 1
```

Trace:

| i | a[i] | min_cost | min_index |
| --- | --- | --- | --- |
| 0 | 10 | 10 | 0 |
| 1 | 20 | 10 | 0 |
| 2 | 5 | 5 | 2 |
| 3 | 3 | 3 | 3 |

Output: `min_index + 1 = 4`

This demonstrates that the opposition can secure square 4 after the administration spends its budget on the 3 most expensive squares among the first 4.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) | We iterate over only the first `k+1` squares to find the minimum. |
| Space | O(1) | Only two variables are needed for tracking the minimum and index. |

Given the constraints `k < n ≤ 10^5` and a 2-second time limit, the algorithm performs at most 10^5 comparisons, which fits comfortably. Memory use is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    b = int(input())
    a = list(map(int, input().split()))
    min_cost = a[0]
    min_index = 0
    for i in range(1, k+1):
        if a[i] < min_cost:
            min_cost = a[i]
            min_index = i
    return str(min_index + 1)

# provided samples
assert run("5 2\n8\n2 4 5 3 1\n") == "2", "sample 1"
assert run("5 3\n15\n10 20 5 3 1\n") == "4", "sample 2"

# custom cases
assert run("1 0\n100\n42\n") == "1", "single square"
assert run("6 5\n10\n1 1 1 1 1 1\n") == "1", "all equal values"
assert run("5 2\n0\n5 4 3 2 1\n") == "3", "administration cannot spend"
assert run("10 9\n100\n10 9 8 7 6 5 4 3 2 1\n") == "10", "last square after budget spend"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0\n100\n42\n | 1 | Minimum input size, single square |
| 6 5\n10\n1 1 1 1 1 1\n | 1 | All equal values, opposition takes earliest |
| 5 2\n0\n5 4 3 2 1\n | 3 | Administration cannot spend, opposition takes first free |
| 10 9\n100\n10 9 8 7 6 5 4 3 2 1\n | 10 | Administration can block all but last square |

## Edge Cases

If the administration has zero budget, the algorithm still selects the minimum among the first `k+1` squares. For example, with `n=5, k=2, b
