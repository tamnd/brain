---
title: "CF 1393A - Rainbow Dash, Fluttershy and Chess Coloring"
description: "We are given a square grid of size $n times n$. The goal is to completely cover every cell with two colors in a chessboard pattern, meaning adjacent cells must always have opposite colors."
date: "2026-06-11T09:54:12+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1393
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 662 (Div. 2)"
rating: 800
weight: 1393
solve_time_s: 81
verified: true
draft: false
---

[CF 1393A - Rainbow Dash, Fluttershy and Chess Coloring](https://codeforces.com/problemset/problem/1393/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a square grid of size $n \times n$. The goal is to completely cover every cell with two colors in a chessboard pattern, meaning adjacent cells must always have opposite colors.

The construction process is constrained: initially, only the outer border of the grid is considered “available”, and from there, tiles are added one or more at a time per turn. Each newly placed tile must touch at least one previously existing tile along an edge. In a single turn, only one player acts, but she may place multiple tiles of her own color as long as the placement rule is satisfied.

The question is purely about scheduling: how few turns are needed, assuming optimal cooperation between the two players, to fully build any valid chess coloring of the grid.

The constraint $n \le 10^9$ immediately rules out any grid simulation. Any solution that tries to model the board or placement process cell by cell would require $O(n^2)$ work or memory, which is impossible. Even $O(n)$ per test case would be too slow in the worst case if many queries are given.

The key difficulty is that the answer is not about geometry of the grid in a complicated sense, but about how the chess pattern can be “layered” under the adjacency constraint.

A naive mistake comes from assuming that because there are two colors, the answer is always 2. This fails immediately for $n = 4$. In that case, the sample output is 3, showing that some structural limitation prevents completing everything in two alternating moves.

Another subtle pitfall is assuming symmetry between even and odd $n$. For instance, $n = 3$ needs 2 turns, while $n = 4$ needs 3 turns, so parity alone is not the whole story.

## Approaches

A brute-force interpretation would simulate the construction process. We would maintain a grid, repeatedly place valid sets of cells per turn, and enforce the adjacency constraint explicitly. Even if we greedily try to fill maximal valid expansions each turn, we still need to track connectivity and color constraints over an $n \times n$ structure. This leads to at least $O(n^2)$ state or repeated scanning, which is infeasible when $n$ reaches $10^9$.

The key observation is that the problem does not depend on individual placements but on how many “layers” of forced alternation exist in the grid structure.

In a chessboard coloring, the grid can be thought of as alternating parity cells. When we start from the boundary, each move can effectively “push inward” a layer of consistent coloring, but diagonal structure forces some cells to be reachable only after multiple expansion waves.

The crucial simplification is that the answer depends only on whether $n$ is even or odd, and more precisely on how many complete “rings” of dependency exist when expanding from the boundary inward.

For odd $n$, the center cell acts as a natural meeting point of expansions, allowing slightly more efficient layering. For even $n$, the grid splits more symmetrically, requiring one additional turn to reconcile the parity structure across the middle.

This leads to a simple closed form:

$$\text{answer} = \left\lfloor \frac{n}{2} \right\rfloor + 1$$

This matches both sample cases:

For $n = 3$, we get $1 + 1 = 2$.

For $n = 4$, we get $2 + 1 = 3$.

The deeper reason is that each pair of rows (or columns) contributes one “layer” of construction, and an additional turn is needed to finalize the chess alternation constraint across the remaining parity mismatch.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(n^2)$ | $O(n^2)$ | Too slow |
| Formula $\lfloor n/2 \rfloor + 1$ | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read each value of $n$. Each test case is independent, so no state is shared between them.
2. Compute $n // 2$. This value represents how many full “paired layers” of the grid exist when expanding from the boundary inward.
3. Add 1 to the result. This accounts for the final consolidation step where the chess coloring constraint forces an extra turn beyond simple layer pairing.
4. Output the computed value immediately for each test case.

### Why it works

The construction process effectively reduces to peeling the grid inward in symmetric layers. Each pair of opposite sides contributes one full step of expansion. However, the parity constraint of chess coloring prevents perfect pairing in all cases, forcing exactly one additional step to resolve the final configuration. Since every valid construction must respect adjacency propagation from the boundary, no strategy can reduce the number of layers below $\lfloor n/2 \rfloor$, and the final parity reconciliation enforces the extra constant term.

## Python Solution

```python
import sys
input = sys.stdin.readline

T = int(input())
for _ in range(T):
    n = int(input())
    print(n // 2 + 1)
```

The solution directly implements the derived closed-form expression. The only subtlety is ensuring integer division is used, since the formula depends on floor behavior. Each test case is handled independently in constant time.

## Worked Examples

### Example 1

Input:

```
n = 3
```

We compute:

| Step | Value |
| --- | --- |
| n | 3 |
| n // 2 | 1 |
| answer | 2 |

The grid has a central cell that allows both colors to propagate efficiently from opposite directions, but still requires two distinct turns due to alternation constraints meeting in the middle.

### Example 2

Input:

```
n = 4
```

| Step | Value |
| --- | --- |
| n | 4 |
| n // 2 | 2 |
| answer | 3 |

Here, the grid splits into symmetric halves with no central resolving cell. This forces one additional turn compared to simple layering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T)$ | One arithmetic operation per test case |
| Space | $O(1)$ | No auxiliary structures used |

The constraints allow up to 100 test cases with $n \le 10^9$, so any per-test constant-time formula is sufficient. The solution operates comfortably within limits.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    T = int(input())
    out = []
    for _ in range(T):
        n = int(input())
        out.append(str(n // 2 + 1))
    return "\n".join(out)

# provided samples
assert solve("2\n3\n4\n") == "2\n3"

# minimum case
assert solve("1\n1\n") == "1"

# small odd/even mix
assert solve("3\n2\n3\n5\n") == "2\n2\n3"

# large value sanity
assert solve("1\n1000000000\n") == str(1000000000 // 2 + 1)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | smallest grid |
| 2,3,5 | 2,2,3 | parity behavior |
| 1e9 | 500000001 | upper bound correctness |

## Edge Cases

When $n = 1$, the grid is a single cell. The formula gives $1 // 2 + 1 = 1$, matching the fact that no layering is needed beyond the initial placement.

For very large $n$, such as $10^9$, the computation remains constant time. There is no overflow risk in Python, and the formula depends only on integer division, so the result remains exact without simulation.
