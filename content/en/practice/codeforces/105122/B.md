---
title: "CF 105122B - Bishop Paths"
description: "We are given an $n times n$ chessboard and a bishop placed on a starting square. The bishop can move any number of cells in a single move, but only along diagonals."
date: "2026-06-27T19:37:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105122
codeforces_index: "B"
codeforces_contest_name: "XXVI Interregional Programming Olympiad, Vologda SU, 2024"
rating: 0
weight: 105122
solve_time_s: 87
verified: false
draft: false
---

[CF 105122B - Bishop Paths](https://codeforces.com/problemset/problem/105122/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an $n \times n$ chessboard and a bishop placed on a starting square. The bishop can move any number of cells in a single move, but only along diagonals. The task is not just to decide whether the bishop can reach a target square, but to count how many distinct shortest-move routes exist from the start to the destination.

A shortest route here means a path that uses the minimum possible number of diagonal moves. Since a bishop move is a straight-line diagonal slide, the only possible path lengths are zero moves if we start already at the destination, one move if both squares lie on the same diagonal, or two moves if the bishop must detour through an intermediate square that is diagonally aligned with both endpoints.

The board size can be as large as $10^9$, which immediately rules out any simulation over the grid. Any solution must work purely with coordinate geometry rather than traversal. Every decision depends only on arithmetic relations between coordinates.

A first subtlety is that bishops are restricted by color parity. On a chessboard, a bishop always stays on squares with the same value of $x + y \bmod 2$. If the start and end squares differ in parity, no sequence of moves can ever connect them, regardless of board size.

A second edge case is when the start and end are identical. The correct answer is exactly one path of length zero, even though no moves are performed.

A third situation that often causes mistakes is when two different two-move decompositions seem possible. Since a bishop move is a full diagonal segment, there may be up to two distinct intermediate squares that connect the start diagonal and the target diagonal.

## Approaches

A direct simulation would attempt to explore all possible bishop moves from the starting square and track all shortest paths to the destination. From any position, the bishop has up to four diagonal directions, and each direction allows up to $O(n)$ landing positions. Even if we restrict ourselves to shortest paths, the state space becomes a graph with $O(n^2)$ nodes and dense diagonal connectivity. A BFS would conceptually work, but $n$ can be $10^9$, so enumeration of nodes or edges is impossible.

The key observation is that bishop movement structure collapses the entire problem into a small set of geometric cases. Either the destination lies on one of the two diagonals through the start, or it does not. If it does, there is exactly one shortest path. If it does not but the squares share parity, the shortest route must be exactly two moves, and any valid path is fully determined by choosing a square that lies simultaneously on a diagonal from the start and a diagonal from the destination.

This reduces the problem to finding intersection points of two diagonal lines. Each bishop move corresponds to choosing either the line $x - y = c$ or $x + y = c$, so intermediate squares are intersections of one diagonal from the start with one diagonal from the end. There are at most two such intersections, and we only need to count how many are valid integer points inside the board.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force BFS over board | $O(n^2)$ | $O(n^2)$ | Too slow |
| Geometric case analysis | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Check whether the start and end squares are identical. If they are, the bishop already satisfies the requirement without moving, so there is exactly one valid path.
2. Compute the color parity of both squares using $(x + y) \bmod 2$. If these differ, return zero since no bishop move sequence can cross color classes.
3. Check whether both squares lie on the same diagonal. This happens if either $x_1 - y_1 = x_2 - y_2$ or $x_1 + y_1 = x_2 + y_2$. If this holds, the bishop can go directly in one move, and there is exactly one such path.
4. Otherwise, the minimum number of moves is two. Any valid path must go through an intermediate square that is reachable from both endpoints in one diagonal move.
5. Construct up to two candidate intermediate squares by intersecting diagonals:

The first candidate comes from solving $x - y = x_1 - y_1$ and $x + y = x_2 + y_2$.

The second candidate comes from solving $x + y = x_1 + y_1$ and $x - y = x_2 - y_2$.
6. For each candidate, compute $x = \frac{(sum \pm diff)}{2}$, $y = sum - x$, and check that both coordinates are integers and lie within the board bounds.
7. Count how many of these candidate intermediate squares are valid. Each valid midpoint corresponds to exactly one distinct shortest path.

### Why it works

Every shortest two-move path must consist of a first move from the start to some square on one of its diagonals, and a second move from that square to the target. The only squares reachable in both steps are exactly the intersection points of the diagonal lines defined by the endpoints. Since each diagonal pair intersects in at most one point, the total number of candidate intermediate squares is at most two, and each corresponds to a unique path decomposition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    x1, y1 = map(int, input().split())
    x2, y2 = map(int, input().split())

    if x1 == x2 and y1 == y2:
        print(1)
        return

    if (x1 + y1) % 2 != (x2 + y2) % 2:
        print(0)
        return

    if x1 - y1 == x2 - y2 or x1 + y1 == x2 + y2:
        print(1)
        return

    def valid(x, y):
        return 1 <= x <= n and 1 <= y <= n

    count = 0

    s1 = x1 + y1
    d1 = x1 - y1
    s2 = x2 + y2
    d2 = x2 - y2

    if (s2 + d1) % 2 == 0:
        x = (s2 + d1) // 2
        y = s2 - x
        if valid(x, y):
            count += 1

    if (s1 + d2) % 2 == 0:
        x = (s1 + d2) // 2
        y = s1 - x
        if valid(x, y):
            count += 1

    print(count)

if __name__ == "__main__":
    solve()
```

The solution is structured around early exits for the zero-move and one-move cases, since these dominate when coordinates align. The parity check removes all impossible cases before any geometric construction, avoiding unnecessary arithmetic.

The two candidate midpoints come directly from solving the system of diagonal equations. The integer check is implicit through even-sum validation, since diagonal intersections require consistent parity. Each candidate is then validated against board boundaries, since the algebraic intersection might lie outside the $n \times n$ grid even though the infinite diagonal lines intersect there.

## Worked Examples

### Example 1

Consider a small board where the start is $(1,1)$ and the target is $(3,3)$ on an $n = 5$ board.

| Step | Position | Same diagonal | Action |
| --- | --- | --- | --- |
| Start | (1,1) | - | compute parity |
| Target | (3,3) | yes | reachable in 1 move |

Both points satisfy $x - y = 0$, so the bishop can move directly.

This confirms a single shortest path exists.

### Example 2

Take start $(1,3)$, target $(3,1)$, with $n = 5$.

| Step | Computation | Result |
| --- | --- | --- |
| Parity | (1+3) % 2 = (3+1) % 2 | same |
| Same diagonal | false | need 2 moves |
| Candidate 1 | (s2 + d1)/2 = (4 + -2)/2 | x = 1 |
| Candidate 2 | (s1 + d2)/2 = (4 + 2)/2 | x = 3 |

Both intermediate points $(1,1)$ and $(3,3)$ lie inside the board.

This shows there are exactly two distinct shortest paths, one passing through each midpoint.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only constant arithmetic operations and checks are performed |
| Space | $O(1)$ | No auxiliary structures are used |

The constraints allow $n$ up to $10^9$, but the solution depends only on coordinate algebra, so execution time remains constant regardless of board size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue() if False else capture(inp)

def capture(inp):
    import sys, io
    backup = sys.stdout
    sys.stdout = io.StringIO()
    sys.stdin = io.StringIO(inp)
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = backup
    return out.strip()

# sample-like cases
assert capture("5\n1 1\n3 3\n") == "1"
assert capture("5\n1 3\n3 1\n") == "2"

# same cell
assert capture("10\n4 4\n4 4\n") == "1"

# unreachable parity
assert capture("8\n1 1\n2 3\n") == "0"

# direct diagonal
assert capture("100\n2 7\n10 15\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| same cell | 1 | zero-move case |
| parity mismatch | 0 | unreachable configuration |
| same diagonal | 1 | one-move case |
| two intersections | 2 | full two-path case |

## Edge Cases

When the start and end coincide, the algorithm immediately returns one before any geometric reasoning. This avoids incorrectly counting diagonal intersections that would otherwise suggest intermediate squares.

When the parity differs, the computation stops early because all subsequent algebraic intersections would still represent squares of incorrect color, making any path impossible regardless of board geometry.

When both squares lie on the same diagonal, both candidate midpoint formulas may produce endpoints or invalid points. The early diagonal check prevents counting spurious intermediate constructions and correctly fixes the answer to one.
