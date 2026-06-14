---
title: "CF 1075A - The King's Race"
description: "We are given an $n times n$ grid. One king starts at the bottom-left corner $(1,1)$ and the other starts at the top-right corner $(n,n)$. A coin is placed at $(x,y)$, and both kings try to reach it as fast as possible."
date: "2026-06-15T06:54:50+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1075
codeforces_index: "A"
codeforces_contest_name: "Lyft Level 5 Challenge 2018 - Final Round (Open Div. 2)"
rating: 800
weight: 1075
solve_time_s: 144
verified: true
draft: false
---

[CF 1075A - The King's Race](https://codeforces.com/problemset/problem/1075/A)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 2m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an $n \times n$ grid. One king starts at the bottom-left corner $(1,1)$ and the other starts at the top-right corner $(n,n)$. A coin is placed at $(x,y)$, and both kings try to reach it as fast as possible. They move like a chess king, so in one move they can go to any of the eight neighboring cells, including diagonals.

The key quantity in this problem is the minimum number of moves a king needs to reach a target cell. Because diagonal movement is allowed, the king effectively reduces both row and column differences simultaneously when possible. This makes the distance between two cells equal to the Chebyshev distance:

$$\text{dist}((a,b),(c,d)) = \max(|a-c|, |b-d|)$$

The white king moves first, then black, alternating turns. Each move takes exactly one step of distance for the king that moves. The winner is whoever reaches $(x,y)$ first.

The constraints allow $n$ up to $10^{18}$, so any simulation of movement step by step is impossible. We must compute distances in constant time.

A subtle edge case is when a king starts on the coin. If $x,y = 1,1$, white wins immediately before black moves. If $x,y = n,n$, black wins immediately. Any solution must handle these instant wins correctly.

Another edge case is parity: even if black is closer in absolute distance, white may still win if black needs one more move but plays second.

## Approaches

A brute-force simulation would move both kings step by step, always choosing any shortest move toward the coin. Each king would need $O(n)$ moves in the worst case, and each move is constant time, leading to $O(n)$ per king. Since $n$ can be $10^{18}$, this is completely infeasible.

The key observation is that optimal play is deterministic: both kings always move along a shortest path, so their arrival times are fully determined by their initial distances to $(x,y)$. The only remaining subtlety is turn order.

We compute:

- $d_w = \max(|x-1|, |y-1|)$
- $d_b = \max(|n-x|, |n-y|)$

White arrives at time $2 \cdot d_w$ or more precisely $2 \cdot d_w$ turns of the game timeline, but since white moves first, his effective arrival turn is $2d_w - 1$.

Black arrives at turn $2d_b$.

So comparison reduces to:

$$2d_w - 1 < 2d_b$$

If true, white wins, otherwise black wins.

This reduces the entire problem to computing two Chebyshev distances and comparing them with a small parity shift.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(n)$ | $O(1)$ | Too slow |
| Distance + Parity Comparison | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute the white king’s distance to the coin using the Chebyshev metric. This represents the minimum number of moves required if white plays optimally.
2. Compute the black king’s distance to the coin in the same way, starting from $(n,n)$.
3. Convert both distances into “turns when the coin is reached.” White reaches on turns $1,3,5,\dots$, so his arrival turn is $2d_w - 1$. Black reaches on turns $2,4,6,\dots$, so his is $2d_b$.
4. Compare these two values. If white’s arrival turn is strictly smaller, white wins. Otherwise black wins.

The reason step 3 is valid is that both players reduce their distance by exactly one per move, and no move can reduce more than one unit of Chebyshev distance.

### Why it works

The key invariant is that each king’s distance to the target decreases by exactly one per move under optimal play, and no alternative strategy can reduce it faster. Since move order is fixed (white always starts), the only asymmetry is a one-move advantage for white. Converting distances into turn indices captures this advantage exactly, so the comparison of $2d_w - 1$ and $2d_b$ fully determines the winner.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    x, y = map(int, input().split())

    dw = max(abs(x - 1), abs(y - 1))
    db = max(abs(n - x), abs(n - y))

    white_turn = 2 * dw - 1
    black_turn = 2 * db

    if white_turn < black_turn:
        print("White")
    else:
        print("Black")

if __name__ == "__main__":
    solve()
```

The white and black distances are computed using the Chebyshev metric because kings can move diagonally, which reduces both coordinates simultaneously. The conversion to turn indices is crucial: white’s first move gives him a one-step advantage in the alternating sequence, which is captured by subtracting one in his final arrival time.

The comparison is strict because if both arrive on the same turn, black is considered to win due to moving second.

## Worked Examples

### Example 1

Input:

```
4
2 3
```

| Quantity | Value |
| --- | --- |
| $d_w$ | 2 |
| $d_b$ | 2 |
| White turn | 3 |
| Black turn | 4 |

White reaches earlier, so he wins.

This shows a case where both kings are equally far in raw distance, but move order gives white the advantage.

### Example 2

Input:

```
5
3 5
```

| Quantity | Value |
| --- | --- |
| $d_w$ | 2 |
| $d_b$ | 2 |
| White turn | 3 |
| Black turn | 4 |

Even though the target is closer to the top-right region, white still reaches earlier due to move order, reinforcing that only relative turn timing matters, not geometric bias.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a few arithmetic operations are performed |
| Space | $O(1)$ | No auxiliary data structures are used |

The solution easily satisfies the constraints since it performs constant-time computation regardless of $n$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    x, y = map(int, input().split())

    dw = max(abs(x - 1), abs(y - 1))
    db = max(abs(n - x), abs(n - y))

    white_turn = 2 * dw - 1
    black
```
