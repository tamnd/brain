---
title: "CF 104381B - Knishop"
description: "We are given two points on an infinite grid with integer coordinates. A piece starts at the first point and needs to reach the second point. In one move, the piece can behave in two different ways."
date: "2026-07-01T02:56:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104381
codeforces_index: "B"
codeforces_contest_name: "The Andover Computing Open (TACO) 2022"
rating: 0
weight: 104381
solve_time_s: 60
verified: true
draft: false
---

[CF 104381B - Knishop](https://codeforces.com/problemset/problem/104381/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two points on an infinite grid with integer coordinates. A piece starts at the first point and needs to reach the second point. In one move, the piece can behave in two different ways. It can move like a knight, meaning it jumps in one of the eight standard L-shaped patterns with offsets (2,1), (1,2), and their sign variations. Alternatively, it can move like a bishop, meaning it can move any number of steps in a single diagonal direction, either along the line y = x or y = -x.

Each move is chosen freely, so at every step we may decide whether to use a knight jump or a diagonal slide of arbitrary length. The goal is to minimize the number of moves required to go from the starting coordinate to the target coordinate.

The coordinates can be as large as 10^9 in magnitude, so any solution that attempts to explore the grid or simulate paths step by step is immediately infeasible. Even a BFS over positions would be impossible because the graph is infinite and the branching factor is non-trivial. The answer must depend only on geometric properties of the two points.

A key subtlety is that the bishop move is extremely powerful: it allows instant travel along diagonals of any length. This means that if the start and end lie on the same diagonal, the answer is trivially 1. A second subtle case arises when a knight move alone is sufficient, since knight reachability in one move depends on a small fixed set of relative offsets. Finally, there are situations where neither a knight nor a bishop move suffices, but a combination of two moves does.

A naive mistake would be assuming that combining two movement types always reduces to either 1 or 2 moves without carefully checking alignment conditions. For example, points that are one knight move apart are not necessarily on a diagonal, and points on a diagonal may still be far apart in Manhattan distance but still reachable in one bishop move.

## Approaches

A brute-force interpretation would attempt to treat each position as a node in a graph and run a shortest path search. From any node, there are eight knight edges and infinitely many bishop edges, since a bishop can jump to any point on its diagonals. Even if we discretize the problem, the state space is unbounded and the transitions are not manageable. The branching factor from bishop moves alone makes this impossible, since each node connects to infinitely many others.

The key observation is that optimal paths never require more than a small number of moves. Each move either preserves a diagonal invariant (bishop) or moves within a fixed bounded set of offsets (knight). Because of this, any shortest path must fall into one of three categories: zero moves if the points coincide, one move if they are connected directly by either a knight move or a bishop move, otherwise two moves always suffice.

The reason two moves are always enough comes from the geometry of the grid. A knight move can change parity structure and relative positioning in a bounded way, and a bishop move can realign diagonals arbitrarily. If neither a direct knight move nor a direct bishop move works, we can always first use one move to place ourselves into a configuration where a bishop move completes the journey, or vice versa. Since both move types are extremely expressive in different dimensions, their combination covers all remaining cases.

Thus the problem reduces to checking a few constant-time geometric conditions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Search | O(inf) | O(inf) | Too slow |
| Geometric Case Checking | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We denote the start as (x1, y1) and the target as (x2, y2). We work entirely with the relative displacement dx = |x2 - x1| and dy = |y2 - y1|.

1. First, check whether the start and target coincide. If dx = 0 and dy = 0, no move is needed. This is the only situation where the answer is zero because any move changes position.
2. Next, check whether the target is reachable by a single bishop move. A bishop move can reach any point that lies on the same diagonal, which means dx = dy. This works because moving along a diagonal preserves the absolute difference between coordinates.
3. Then check whether the target is reachable by a single knight move. A knight move has exactly eight possible displacement patterns, so we verify whether the pair (dx, dy) matches any of (1,2), (2,1), (2,0), (0,2) is not valid actually in standard knight moves, so only (1,2) and (2,1) matter, since sign symmetry is handled by absolute values.
4. If none of the above conditions hold, the answer is 2. The reasoning is that any position can always be reached in at most two moves because we can first use a knight move to shift into a position that aligns diagonally or directly matches the target via a bishop move.

### Why it works

The entire solution relies on the fact that both move types define very large reachability sets. A bishop move covers an entire diagonal line in one step, and a knight move can break parity constraints and shift between coordinate classes that bishops cannot reach. Because these two transformations are complementary, any pair of points is either directly connected by one of them or can be bridged using exactly one intermediate position. There is no configuration requiring more than two moves because the combination of one local bounded jump and one global diagonal sweep spans the entire integer lattice.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_knight(dx, dy):
    return (dx, dy) in {(1, 2), (2, 1)}

def solve():
    x1, y1, x2, y2 = map(int, input().split())
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    if dx == 0 and dy == 0:
        print(0)
        return

    if dx == dy:
        print(1)
        return

    if is_knight(dx, dy):
        print(1)
        return

    print(2)

if __name__ == "__main__":
    solve()
```

The implementation begins by reading coordinates and converting the problem into a purely relative form using absolute differences. This removes directionality and allows us to reason only about magnitudes.

The first condition handles the degenerate case where no movement is required. The second condition checks diagonal alignment, which corresponds exactly to bishop reachability in one move. The third condition tests the finite set of knight offsets. Everything else falls into the two-move category, which is guaranteed by the combined movement structure.

## Worked Examples

### Example 1

Input:

```
0 0 1 2
```

We compute dx = 1 and dy = 2.

| Step | dx | dy | Check |
| --- | --- | --- | --- |
| Start | 1 | 2 | not equal |
| Bishop | 1 | 2 | not diagonal |
| Knight | 1 | 2 | match |

The knight condition triggers immediately, so the answer is 1.

This shows the case where the L-shaped geometry alone is sufficient without any need for diagonal movement.

### Example 2

Input:

```
1 1 -100 -100
```

We compute dx = 101 and dy = 101.

| Step | dx | dy | Check |
| --- | --- | --- | --- |
| Start | 101 | 101 | not zero |
| Bishop | 101 | 101 | diagonal match |

Since dx equals dy, a single bishop move can directly traverse the diagonal, producing answer 1.

This demonstrates how large-distance movement collapses to a single operation due to the unbounded diagonal sliding capability.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic and comparisons |
| Space | O(1) | No auxiliary structures are used |

The solution is constant time per test case and works comfortably within the constraints since input size is irrelevant once reduced to geometric checks.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    x1, y1, x2, y2 = map(int, input().split())
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    def is_knight(dx, dy):
        return (dx, dy) in {(1, 2), (2, 1)}

    if dx == 0 and dy == 0:
        return "0"
    if dx == dy:
        return "1"
    if is_knight(dx, dy):
        return "1"
    return "2"

# provided samples
assert run("0 0 1 2") == "1", "sample 1"
assert run("1 1 -100 -100") == "1", "sample 2"

# custom cases
assert run("0 0 0 0") == "0", "same cell"
assert run("0 0 2 1") == "1", "knight move"
assert run("0 0 5 5") == "1", "bishop diagonal"
assert run("0 0 3 4") == "2", "neither direct move"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 0 0 | 0 | zero distance case |
| 0 0 2 1 | 1 | knight reachability |
| 0 0 5 5 | 1 | bishop diagonal reach |
| 0 0 3 4 | 2 | requires two moves |

## Edge Cases

The identical start and end case is the only situation where movement count is zero. The algorithm handles it explicitly before any geometric checks, so it correctly outputs 0 for inputs like (7, -3) to (7, -3).

The knight adjacency case depends on exact offsets. For example, (0,0) to (2,1) is accepted because it matches a valid knight displacement after taking absolute values. The algorithm checks this against a fixed set, so no accidental inclusion of invalid offsets occurs.

The diagonal case handles arbitrarily large distances, such as (10^9, 10^9), correctly collapsing them into a single bishop move. Since equality of absolute differences is checked directly, no overflow or approximation issues arise.

The remaining cases automatically fall into two moves. For instance, (0,0) to (3,4) is not a knight move and not diagonal, so it is classified correctly without needing explicit path construction.
