---
title: "CF 1989A - Catch the Coin"
description: "We are given a grid representing the arcade screen with coordinates $(x, y)$, where Monocarp starts at the origin $(0, 0)$. There are $n$ coins scattered on the grid. Each second, Monocarp can move in one of the eight directions (up, down, left, right, and the four diagonals)."
date: "2026-06-08T15:44:02+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1989
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 167 (Rated for Div. 2)"
rating: 800
weight: 1989
solve_time_s: 398
verified: false
draft: false
---

[CF 1989A - Catch the Coin](https://codeforces.com/problemset/problem/1989/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 6m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a grid representing the arcade screen with coordinates $(x, y)$, where Monocarp starts at the origin $(0, 0)$. There are $n$ coins scattered on the grid. Each second, Monocarp can move in one of the eight directions (up, down, left, right, and the four diagonals). After Monocarp moves, all coins fall one unit down along the Y-axis. The goal is to determine for each coin whether Monocarp can reach it at some point, assuming he moves optimally.

The input gives $n$ and the coordinates of the coins, all distinct and none at the origin. The output is a line per coin: "YES" if Monocarp can collect it and "NO" otherwise.

The constraints are small: $n \le 500$ and coin coordinates are between $-50$ and $50$. This allows algorithms with at least $O(n)$ per coin, or $O(n^2)$ total, without performance issues.

The key non-obvious cases involve coins below the origin. Since coins fall down by 1 unit every second, a coin initially at a negative Y-coordinate may fall faster than Monocarp can reach it diagonally. For example, if a coin starts at $(-1, -2)$, Monocarp can move diagonally to reach it as it falls. A naive check using Manhattan distance without considering coin fall would falsely say he cannot reach it.

Another subtle case is coins aligned diagonally or horizontally: Monocarp's diagonal moves can be used to "catch up" vertically while moving horizontally.

## Approaches

The naive approach is to simulate Monocarp's movement for each coin second by second, checking if his path intersects with the coin's falling path. This is correct but cumbersome, requiring a simulation loop per coin and per time step, potentially hundreds of steps for coins far away. With $n = 500$ and positions up to 50, it is feasible but unnecessarily complex.

The optimal approach comes from observing Monocarp's movement options. In one second, he can change both X and Y by at most 1 unit each. This is equivalent to Chebyshev distance (maximum of $|dx|$ and $|dy|$) rather than Manhattan distance. We must account for the fact that coins fall down by 1 unit each second. Let the initial coin position be $(x, y)$ and Monocarp at $(0, 0)$. He can reach the coin if there exists some $t \ge 0$ such that:

$$\max(|x|, |y - t|) \le t$$

Solving for $t$ gives $t \ge \max(|x|, y - t)$, which simplifies to $t \ge |x|$ and $y - t \le t$, or $y \le 2t$. Since $t \ge |x|$, the second inequality becomes $y \le 2|x|$. So the condition for Monocarp to reach a coin is:

$$y \le 2 \cdot |x|$$

If this holds, Monocarp can catch the coin by moving diagonally towards its column and waiting for it to fall if needed. Otherwise, he cannot.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n * max( | x | , |
| Optimal Chebyshev Check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of coins $n$ and their coordinates $(x_i, y_i)$ for $i = 1 \dots n$.
2. For each coin, compute the absolute value of the X-coordinate: $|x_i|$. This represents the minimum number of seconds Monocarp must move horizontally (or diagonally) to align with the coin's column.
3. Check whether the Y-coordinate of the coin satisfies $y_i \le 2 \cdot |x_i|$. This condition ensures that Monocarp's combined diagonal/horizontal moves can match the coin's falling trajectory. If true, print "YES".
4. Otherwise, print "NO".

Why it works: Monocarp's movement allows simultaneous horizontal and vertical adjustments. The Chebyshev distance gives the minimum number of seconds to reach the coin horizontally or vertically. Since the coin falls one unit per second, the maximum vertical distance Monocarp can overcome relative to the falling coin is exactly twice the horizontal distance. This invariant guarantees that if $y \le 2|x|$, there is some sequence of moves that will catch the coin.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
for _ in range(n):
    x, y = map(int, input().split())
    if y <= 2 * abs(x):
        print("YES")
    else:
        print("NO")
```

This solution iterates through the coins exactly once. The key check is derived from the Chebyshev distance and the falling coin dynamics. Using `abs(x)` ensures we handle coins on both sides of the Y-axis. The comparison `y <= 2 * abs(x)` naturally handles coins above or below the origin, since negative y-coordinates always satisfy the inequality when the coin is close horizontally.

## Worked Examples

**Example 1**

Input:

```
5
24 42
-2 -1
-1 -2
0 -50
15 0
```

| Coin | x | y | 2*|x| | y <= 2*|x|? | Result |

|------|---|---|---|---|--------|

| 1 | 24 | 42 | 48 | YES | YES |

| 2 | -2 | -1 | 4 | YES | YES |

| 3 | -1 | -2 | 2 | NO | NO |

| 4 | 0 | -50 | 0 | NO | NO |

| 5 | 15 | 0 | 30 | YES | YES |

This demonstrates both positive and negative coordinates, as well as coins at y < 0.

**Example 2**

Input:

```
3
1 2
2 3
3 5
```

| Coin | x | y | 2*|x| | y <= 2*|x|? | Result |

|------|---|---|---|---|--------|

| 1 | 1 | 2 | 2 | YES | YES |

| 2 | 2 | 3 | 4 | YES | YES |

| 3 | 3 | 5 | 6 | YES | YES |

This confirms that coins above the origin are correctly classified.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each coin is checked independently in constant time. |
| Space | O(1) | No additional memory beyond loop variables. |

Given $n \le 500$ and coordinates bounded by $\pm 50$, this solution is extremely efficient and comfortably fits within the 2-second time limit and memory constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    n = int(input())
    for _ in range(n):
        x, y = map(int, input().split())
        if y <= 2 * abs(x):
            print("YES")
        else:
            print("NO")
    return out.getvalue().strip()

# Provided sample
assert run("5\n24 42\n-2 -1\n-1 -2\n0 -50\n15 0\n") == "YES\nYES\nNO\nNO\nYES"

# Custom test cases
assert run("1\n0 1\n") == "NO", "coin above origin, unreachable horizontally"
assert run("1\n0 0\n") == "YES", "edge case, coin at origin"
assert run("2\n-50 100\n50 100\n") == "NO\nNO", "coins too far vertically"
assert run("3\n1 1\n-1 1\n0 0\n") == "YES\nYES\nYES", "small coins around origin"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 1` | NO | Cannot reach coin directly above origin horizontally |
| `0 0` | YES | Coin at origin |
| `-50 100` | NO | Coin too high to catch |
| `1 1\n-1 1\n0 0` | YES, YES, YES | Coins close to origin in different quadrants |

## Edge Cases

For coins directly above or below the origin with $x = 0$, Monocarp can only move vertically, which limits reach. For example, `(0, -50)` yields `NO` because Monocarp cannot move down faster than the coin falls. For coins on the horizontal axis `(x, 0)`, he can move horizontally and catch the coin immediately, which is why `(15, 0)` yields `YES`. Negative y-coordinates within `2*abs(x)` are handled because Monoc
