---
title: "CF 103785B - Poku's Vacation"
description: "We are given a number of identical bricks and we want to build a staircase using them. Each stair has a positive integer height, and the staircase must strictly increase from one step to the next."
date: "2026-07-02T08:50:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103785
codeforces_index: "B"
codeforces_contest_name: "CodeBrew : Freshers Contest 2022"
rating: 0
weight: 103785
solve_time_s: 49
verified: true
draft: false
---

[CF 103785B - Poku's Vacation](https://codeforces.com/problemset/problem/103785/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a number of identical bricks and we want to build a staircase using them. Each stair has a positive integer height, and the staircase must strictly increase from one step to the next. The goal is to use at most the available bricks while maximizing how many distinct steps we can build.

The key output is not the exact configuration of the staircase but only the maximum number of steps possible under the constraint that step heights must increase and the total number of bricks used cannot exceed the given limit.

The constraint structure is important: if there are up to $n$ bricks, a naive construction might try arbitrary increasing sequences, but the requirement of strictly increasing heights immediately forces a minimal-cost structure if we want to maximize the number of steps.

A first subtle point is that there are no “hidden choices” in an optimal construction. If we decide to build $k$ steps, the smallest possible total number of bricks occurs when the staircase is as tight as possible: $1, 2, 3, \ldots, k$. Any deviation from this increases total cost and reduces feasibility.

Edge cases worth considering include very small inputs and exact boundary matches of triangular numbers. For example, if $n = 1$, the answer is clearly 1. If $n = 3$, we can build $1 + 2 = 3$ giving 2 steps, but if $n = 2$, we can only build one step because two steps would require 3 bricks.

A naive mistake would be to assume that any increasing sequence is equally efficient or to try arbitrary greedy increments without recognizing that the minimal structure is forced.

## Approaches

The brute-force idea is straightforward: simulate building stairs one by one, always increasing the next stair height by at least one, while tracking how many bricks have been used. At each step, we try to add the next stair and stop when we exceed $n$. This is correct because it always constructs the minimal possible staircase for a given number of steps.

However, this directly reveals the inefficiency. In the worst case, if $n$ is large, we may iterate up to $k \approx \sqrt{2n}$ steps, and each step is constant work, so it is already efficient enough for typical constraints. But conceptually, this brute process hides the key structure: the sum of the first $k$ integers.

The observation is that the optimal staircase must always use the smallest possible increasing sequence, which reduces the problem to finding the largest $k$ such that:

$$1 + 2 + 3 + \cdots + k \le n$$

This is a triangular sum:

$$\frac{k(k+1)}{2} \le n$$

So the problem becomes solving a simple inequality. This can be done either mathematically using the quadratic formula or iteratively by accumulating values until the limit is exceeded. The iterative approach is simpler and avoids floating-point precision issues.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(√n) | O(1) | Accepted |
| Mathematical / Iterative Optimal | O(√n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start with the smallest possible stair height, which is 1. This ensures we minimize total brick usage for any fixed number of stairs.
2. Maintain three variables: the current stair height, the total bricks used so far, and the number of stairs constructed.
3. Try to add the next stair by increasing the height by 1 each time. This is forced because any smaller increase would violate strict ordering.
4. Before adding a stair, check whether adding its required number of bricks would exceed the limit $n$. If it does, stop immediately.
5. Otherwise, include the stair, update the total sum of used bricks, increment the stair count, and continue.
6. Repeat until no further stair can be added without exceeding the available bricks.

Why it works: the construction always builds the lexicographically smallest strictly increasing sequence of positive integers of a given length. For any fixed number of stairs $k$, this sequence minimizes total cost. Since the cost grows monotonically with $k$, the first value of $k$ that violates the constraint is exactly where the maximum valid solution ends. This establishes that the greedy incremental construction is both necessary and sufficient for optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

cnt = 0
add = 1
total = 0

while total + add <= n:
    total += add
    add += 1
    cnt += 1

print(cnt)
```

The solution maintains three variables that mirror the construction process. The variable `add` represents the height of the next stair, starting from 1 and increasing by 1 each iteration. The variable `total` tracks how many bricks have been used so far, ensuring we never exceed the budget `n`. The variable `cnt` counts how many stairs have been successfully built.

The loop condition `total + add <= n` is critical because it ensures we only commit to a stair if it can be fully supported by the remaining bricks. This avoids overshooting and removes the need for backtracking.

A common off-by-one risk here is updating `total` before checking feasibility; the correct approach is to check first, then commit.

## Worked Examples

### Example 1: n = 5

| Step | add | total before | total after | cnt |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 |
| 2 | 2 | 1 | 3 | 2 |
| 3 | 3 | 3 | 6 (stop) | 2 |

We stop before adding 3 because it would exceed 5. The result is 2 stairs. This confirms that the algorithm halts exactly at the triangular boundary.

### Example 2: n = 10

| Step | add | total before | total after | cnt |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 |
| 2 | 2 | 1 | 3 | 2 |
| 3 | 3 | 3 | 6 | 3 |
| 4 | 4 | 6 | 10 | 4 |
| 5 | 5 | 10 | stop | 4 |

Here we reach exactly 10 at 4 stairs. The algorithm correctly uses all bricks without violating constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(√n) | Each step increases `add` by 1, and the loop runs until the sum exceeds n, which happens after about √(2n) iterations |
| Space | O(1) | Only a constant number of variables are maintained |

The complexity is comfortably within limits even for large values of $n$, since the number of iterations grows only with the square root of the input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    cnt = 0
    add = 1
    total = 0
    while total + add <= n:
        total += add
        add += 1
        cnt += 1
    return str(cnt)

# provided samples (conceptual, as not explicitly given)
assert run("1\n") == "1"
assert run("3\n") == "2"

# custom cases
assert run("0\n") == "0", "minimum edge"
assert run("2\n") == "1", "cannot form second stair"
assert run("6\n") == "3", "exact triangular number"
assert run("10\n") == "4", "perfect staircase"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 | 0 | minimum boundary handling |
| 2 | 1 | early stopping correctness |
| 6 | 3 | exact triangular number case |
| 10 | 4 | perfect full staircase case |

## Edge Cases

For $n = 1$, the algorithm starts with `add = 1` and checks `0 + 1 <= 1`, so it builds exactly one stair and stops afterward because the next add would be 2, which already exceeds the remaining budget. This confirms correct handling of minimal input.

For $n = 2$, the first stair is added, giving `total = 1`, and the next candidate is `add = 2`. Since `1 + 2 > 2`, the loop stops immediately, producing exactly one stair. This shows that the algorithm does not overestimate feasibility.

For triangular boundaries like $n = 6$, the sequence builds exactly $1 + 2 + 3 = 6$, and the next attempt would be 4, which correctly fails. This demonstrates that equality is handled safely because the condition uses `<=`, allowing exact fits to be included.
