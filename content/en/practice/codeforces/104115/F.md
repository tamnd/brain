---
title: "CF 104115F - \u041d\u043e \u0432\u044b \u043e\u0431\u043e \u043c\u043d\u0435 \u0441\u043b\u044b\u0448\u0430\u043b\u0438"
description: "There is a row of $n$ chests numbered from 1 to $n$. Exactly one chest $k$ contains treasure, while all others are empty. A pirate starts opening chests but has not yet discovered where the treasure is located."
date: "2026-07-02T01:56:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104115
codeforces_index: "F"
codeforces_contest_name: "Voronezh State University - Sitronics contest, 2022"
rating: 0
weight: 104115
solve_time_s: 40
verified: true
draft: false
---

[CF 104115F - \u041d\u043e \u0432\u044b \u043e\u0431\u043e \u043c\u043d\u0435 \u0441\u043b\u044b\u0448\u0430\u043b\u0438](https://codeforces.com/problemset/problem/104115/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

There is a row of $n$ chests numbered from 1 to $n$. Exactly one chest $k$ contains treasure, while all others are empty. A pirate starts opening chests but has not yet discovered where the treasure is located.

He commits to one of two fixed strategies before starting: either he opens chests from left to right, starting at 1 and moving upward, or he opens from right to left, starting at $n$ and moving downward. He stops immediately when he opens the chest containing the treasure.

We are asked to compute how many chests he will open in the worst case, assuming the treasure is actually at position $k$, but the pirate chooses the better of the two directions in advance to minimize the maximum number of openings needed.

The constraint $n \le 10^9$ rules out any simulation or iterative scanning across the array. Any solution must be constant time, since even a linear scan over $n$ is impossible.

A subtle edge situation happens when the treasure is near one end. For example, if $n = 5, k = 4$, then scanning from the left takes 4 openings, while scanning from the right takes 2 openings (5 → 4). A naive approach that always assumes left-to-right would incorrectly return 4 without comparing both directions. The correct answer depends on proximity to the nearest endpoint.

Another edge case is when $k = 1$ or $k = n$. In both cases, one direction finds the treasure immediately in 1 step, while the other would take $n$ steps. Any solution that averages or combines distances instead of taking a minimum would fail here.

## Approaches

A direct simulation would attempt to follow the pirate’s process literally. If we fix a direction, we count how many chests are opened until reaching $k$. From the left, this is exactly $k$. From the right, this is $n - k + 1$. This approach is correct because it mirrors the process definition precisely, but it becomes irrelevant under large constraints since the input size is huge but the computation per test is trivial.

The key observation is that there are only two possible monotone traversals, and each produces a deterministic cost based purely on the position of $k$. The problem reduces to choosing the smaller of two linear distances: distance from the left boundary and distance from the right boundary. No intermediate structure matters, since there is no branching or randomness in the search process.

Thus, the optimal solution is simply computing both costs and taking the minimum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n) | O(1) | Too slow |
| Direct Formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute how many chests would be opened if the pirate starts from the left. This is exactly $k$, since he opens 1, 2, ..., up to $k$.
2. Compute how many chests would be opened if the pirate starts from the right. This is $n - k + 1$, since he opens $n, n-1, ..., k$.
3. Compare these two values and choose the smaller one, since the pirate will pick the strategy that minimizes his worst-case number of openings given knowledge of $k$.

### Why it works

Each strategy is a deterministic monotone traversal with no skips. The cost depends only on the number of steps required to reach index $k$ from a fixed endpoint. Since both traversals are linear and independent, the optimal choice is always the minimum of their respective distances. There is no interaction between steps, so no adaptive strategy can improve on these two fixed options.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    left = k
    right = n - k + 1
    print(min(left, right))

if __name__ == "__main__":
    solve()
```

The code reads the two integers and computes the two possible search costs directly. The left cost corresponds to counting positions from 1 to $k$, while the right cost corresponds to counting backwards from $n$. The final answer is the minimum of the two.

The only subtlety is remembering that the right-side distance includes the position itself, hence the $+1$. Without it, the count would be off by one whenever $k$ is exactly at an endpoint.

## Worked Examples

### Example 1: $n = 5, k = 4$

| Step | Left Cost | Right Cost | Decision |
| --- | --- | --- | --- |
| Initial | 4 | 2 | Compare |
| Final | 4 | 2 | Choose 2 |

From the left, chests 1 through 4 are opened. From the right, chests 5 and 4 are opened, so the treasure is found in 2 steps. The table confirms that proximity to the right boundary dominates.

### Example 2: $n = 10, k = 3$

| Step | Left Cost | Right Cost | Decision |
| --- | --- | --- | --- |
| Initial | 3 | 8 | Compare |
| Final | 3 | 8 | Choose 3 |

Here the treasure is closer to the left side, so scanning from the start is optimal. This confirms the decision reduces to comparing distances to endpoints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic operations and one comparison |
| Space | O(1) | No auxiliary data structures |

The constraints allow up to $10^9$, but since no iteration depends on $n$, the solution runs instantly even at maximum input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    left = k
    right = n - k + 1
    return str(min(left, right))

# provided samples
assert run("1 1") == "1"
assert run("5 4") == "2"
assert run("10 3") == "3"

# custom cases
assert run("5 1") == "1"   # boundary left
assert run("5 5") == "1"   # boundary right
assert run("6 3") == "3"   # symmetric-ish case
assert run("7 4") == "4"   # center case
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 1 | 1 | left boundary immediate success |
| 5 5 | 1 | right boundary immediate success |
| 6 3 | 3 | balanced small-mid position |
| 7 4 | 4 | central position symmetry |

## Edge Cases

When $k = 1$, the left strategy finds the treasure immediately in one step, while the right strategy would take $n$ steps. The algorithm computes $left = 1$, $right = n$, and correctly returns 1.

When $k = n$, the symmetric situation occurs. The computation yields $left = n$, $right = 1$, and again the minimum is 1.

When $k$ is exactly in the middle, both directions behave similarly but differ by at most one due to parity. For example, $n = 6, k = 3$ gives $left = 3$, $right = 4$. The algorithm selects 3, matching the fact that the left-side traversal reaches it first.

These cases confirm that the solution correctly reduces the process to endpoint distances without missing boundary effects.
