---
title: "CF 931A - Friends Meeting"
description: "Two people stand on a number line at integer coordinates $a$ and $b$. They want to end up at the same integer position, and each of them can move one step left or right any number of times. The twist is that movement cost is not linear."
date: "2026-06-17T02:58:27+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 931
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 468 (Div. 2, based on Technocup 2018 Final Round)"
rating: 800
weight: 931
solve_time_s: 68
verified: true
draft: false
---

[CF 931A - Friends Meeting](https://codeforces.com/problemset/problem/931/A)

**Rating:** 800  
**Tags:** brute force, greedy, implementation, math  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

Two people stand on a number line at integer coordinates $a$ and $b$. They want to end up at the same integer position, and each of them can move one step left or right any number of times.

The twist is that movement cost is not linear. If a person makes $k$ total moves, their tiredness is $1 + 2 + \dots + k$, which equals $k(k+1)/2$. The order of moves does not matter, only how many steps a person takes in total.

The task is to choose a meeting point $x$, move both people to $x$, and minimize the sum of their tiredness values.

The constraints are very small, with positions up to 1000. This immediately suggests that even an $O(n)$ or $O(n^2)$ scan over all possible meeting points is feasible without concern for performance. The real difficulty is not computational, but recognizing how movement cost behaves.

A naive mistake here is to assume that since both can move freely, the answer depends on some midpoint-like behavior only. Another mistake is to think direction matters; it does not, because moving left or right has identical cost structure, only the count of steps matters.

A subtle edge case is when both meet far away from both initial points. Even if both move, it might still be optimal compared to only one person moving, because splitting distance can reduce quadratic cost growth.

## Approaches

A direct approach is to try every possible meeting position $x$. For each $x$, compute how far each person must move: $|a-x|$ and $|b-x|$. If a person moves $d$ steps, their cost is $d(d+1)/2$. Summing both costs gives the total tiredness for that meeting point.

Since $a$ and $b$ are at most 1000, valid meeting points also lie within a small range around them. Any point outside $[\min(a,b), \max(a,b)]$ only increases both distances simultaneously and cannot improve the solution.

The brute-force method checks all candidate $x$ in this interval, computes the cost, and takes the minimum. This is correct because the problem reduces to a one-dimensional convex search over integer points.

The key insight is that the cost function is quadratic in distance, so while each individual cost grows faster than linearly, the sum over both agents still forms a simple unimodal function over the integer line. That guarantees the minimum occurs near the segment between $a$ and $b$, and exhaustive checking over that small region is sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all x | O(1000) | O(1) | Accepted |
| Optimal (same idea, bounded scan) | O(1000) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two integers $a$ and $b$, representing starting positions of the two friends. We will evaluate possible meeting points on the integer line.
2. Compute the search range as all integer points between $\min(a,b)$ and $\max(a,b)$. Any optimal meeting point must lie in this interval because moving outside increases both distances simultaneously.
3. Initialize an answer variable with a very large number. This will track the minimum total tiredness observed across all candidate meeting points.
4. Iterate over every integer point $x$ in the chosen range. Each $x$ is treated as a potential meeting location.
5. For each $x$, compute the distance each friend must travel: $d_1 = |a-x|$ and $d_2 = |b-x|$. These distances fully determine tiredness.
6. Convert each distance into tiredness using the triangular number formula $d(d+1)/2$, then sum both values. This gives total cost for meeting at $x$.
7. Update the answer with the minimum over all computed values.
8. Output the final minimum tiredness.

### Why it works

For any fixed meeting point, each participant’s cost depends only on the number of steps they take, not the path. Since cost is strictly increasing and convex in distance, spreading movement away from the segment between $a$ and $b$ never helps both simultaneously. Thus the optimal solution must lie within the interval connecting the two starting points. Exhaustively checking all integer points in this bounded region guarantees the global minimum is found.

## Python Solution

```python
import sys
input = sys.stdin.readline

def cost(d):
    return d * (d + 1) // 2

a = int(input())
b = int(input())

lo = min(a, b)
hi = max(a, b)

ans = float('inf')

for x in range(lo, hi + 1):
    total = cost(abs(a - x)) + cost(abs(b - x))
    ans = min(ans, total)

print(ans)
```

The function `cost` encodes the triangular number formula, which is the only nonlinear part of the computation. The loop considers every feasible meeting point and evaluates the exact cost for both participants.

The use of `min(a,b)` and `max(a,b)` avoids unnecessary checks outside the segment where both distances increase together, which would only produce worse results.

## Worked Examples

### Example 1

Input:

```
3
4
```

| x | d1 = |3-x| | d2 = |4-x| | cost(d1) | cost(d2) | total |

|---|---|---|---|---|---|

| 3 | 0 | 1 | 0 | 1 | 1 |

| 4 | 1 | 0 | 1 | 0 | 1 |

The minimum occurs at either endpoint, since the points are adjacent. This confirms that when distance is minimal, concentrating movement on one person is optimal.

### Example 2

Input:

```
1
5
```

| x | d1 | d2 | cost(d1) | cost(d2) | total |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 4 | 0 | 10 | 10 |
| 2 | 1 | 3 | 1 | 6 | 7 |
| 3 | 2 | 2 | 3 | 3 | 6 |
| 4 | 3 | 1 | 6 | 1 | 7 |
| 5 | 4 | 0 | 10 | 0 | 10 |

The best meeting point is the midpoint $x=3$, showing how splitting distance minimizes quadratic cost.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | a-b |
| Space | O(1) | Only a few variables are used regardless of input size |

The constraint range ensures that at most 1000 candidate points are checked, which is trivial under a 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    def cost(d):
        return d * (d + 1) // 2

    a = int(sys.stdin.readline())
    b = int(sys.stdin.readline())

    lo, hi = min(a, b), max(a, b)
    ans = float('inf')

    for x in range(lo, hi + 1):
        ans = min(ans, cost(abs(a - x)) + cost(abs(b - x)))

    return str(ans)

# provided samples
assert run("3\n4\n") == "1"

# custom cases
assert run("1\n2\n") == "1", "adjacent points"
assert run("1\n5\n") == "6", "midpoint optimal split"
assert run("10\n10\n") == "0", "same point (invalid per statement but robustness)"
assert run("2\n9\n") == "10", "larger span case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3,4 | 1 | basic adjacency |
| 1,5 | 6 | midpoint optimality |
| 10,10 | 0 | degenerate equality handling |
| 2,9 | 10 | wider interval correctness |

## Edge Cases

A key edge situation is when both friends are already close. For input:

```
3
4
```

the algorithm checks only $x=3$ and $x=4$. At $x=3$, costs are $0$ and $1$, total $1$. At $x=4$, symmetric result $1$. The loop ensures both endpoints are considered, so no missed optimum occurs due to off-by-one range errors.

Another important case is when the optimal meeting point lies strictly between the two positions. For:

```
1
5
```

the loop evaluates all points from 1 to 5, including $x=3$, where costs are $3$ and $3$. The sum $6$ is correctly identified as minimal. This confirms that restricting the search to the segment is sufficient and no external point is needed.
