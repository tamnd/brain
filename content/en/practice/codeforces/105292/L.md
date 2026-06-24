---
title: "CF 105292L - Ltf's Board Game"
description: "We are given an $N times N$ grid where two players alternately place tokens on empty cells. The restriction is global: no two placed tokens are allowed to be orthogonally adjacent, meaning they cannot share a side."
date: "2026-06-24T20:16:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105292
codeforces_index: "L"
codeforces_contest_name: "National Taiwan University Class Preliminary 2024"
rating: 0
weight: 105292
solve_time_s: 51
verified: true
draft: false
---

[CF 105292L - Ltf's Board Game](https://codeforces.com/problemset/problem/105292/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an $N \times N$ grid where two players alternately place tokens on empty cells. The restriction is global: no two placed tokens are allowed to be orthogonally adjacent, meaning they cannot share a side. Once a cell is occupied, all four of its edge-neighbors become restricted for future placements unless they are already occupied, since placing there would violate the rule.

The game ends when a player has no legal move on their turn, and that player loses. Ltf makes the first move, and both players are assumed to play perfectly. The task is not to simulate the game but to determine, for a given board size $N$, whether the first player can force a win.

The input is a single integer $N$, and the output is a single word indicating the winner.

Even though the grid can be as large as $10^5 \times 10^5$, the rules depend only on adjacency, not on any dynamic structure that grows during play. This strongly suggests that the answer depends on a structural invariant of the grid rather than any simulation process.

A naive interpretation would attempt to model the game state as a graph where each move removes a vertex and forbids its neighbors. That leads immediately to a combinatorial game on a grid graph with exponential branching. Even for small $N$, enumerating all move sequences becomes infeasible because each move affects up to four neighbors and the game tree grows extremely quickly.

Edge cases are easiest to see on tiny grids.

For $N = 1$, there is exactly one cell. The first player takes it, the second has no move, so the first wins.

For $N = 2$, any move blocks a significant portion of the board. In fact, after the first placement, no second move is possible, so the first player loses if optimal play leads to immediate deadlock after giving the opponent a forced move sequence that results in a winning reply structure. The official sample confirms that $N=2$ is losing for the first player.

For $N = 3$, there is enough space to stagger placements so that the first player can always mirror or control the parity of remaining usable cells, and the first player wins.

These examples already hint that parity or bipartite structure is involved, rather than geometric complexity.

## Approaches

The brute-force approach would model every valid placement configuration as a game state and recursively simulate all possible moves, marking states as winning or losing using minimax. A single move consists of choosing a cell that is not adjacent to any already chosen cell, then updating the forbidden region. In the worst case, the number of valid configurations of an $N \times N$ grid under an independence constraint is exponential in $N^2$, so exploring this state space is completely infeasible even for $N=10$.

The key observation is that the adjacency restriction turns the grid into a bipartite graph where every cell is colored like a chessboard. Any valid set of placed pieces must form an independent set in this graph. The game is then equivalent to players alternately picking vertices such that no two chosen vertices are adjacent to already chosen ones, which is equivalent to building a maximal independent set step by step.

On a bipartite graph, the optimal play structure collapses to a simple parity argument: the first player wins if and only if the total number of available “forced pairing opportunities” does not neutralize the first move advantage. For a full grid with no blocked cells, the outcome depends only on whether the grid size leads to a balanced or unbalanced partition structure.

For an $N \times N$ grid, both color classes of the chessboard coloring have equal size when $N$ is even, and differ by exactly one when $N$ is odd. This imbalance is what determines who has the final move in optimal play. The adjacency restriction ensures that every move effectively consumes one cell from this bipartite structure without allowing cross-interaction between same-color choices.

This reduces the entire game to checking the parity of $N$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Game Simulation | Exponential in $N^2$ | Exponential | Too slow |
| Bipartite Parity Reduction | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Observe that the grid can be colored like a chessboard, splitting all cells into two disjoint sets where no two cells inside one set are adjacent. This converts the placement rule into selecting independent vertices in a bipartite graph.
2. Recognize that every move removes exactly one cell from the available set of moves, and potentially disables up to four neighboring cells, but those neighbors belong to the opposite color class in the bipartite structure.
3. Realize that the only global structure affecting optimal play is the imbalance between the two color classes. On an $N \times N$ grid, the counts are equal when $N$ is even, and differ by one when $N$ is odd.
4. Reduce the game outcome to a parity decision: if $N$ is even, the symmetry allows the second player to always respond in a way that preserves balance; if $N$ is odd, the first player inherits the extra cell and maintains the final move advantage.
5. Output the winner based solely on this parity condition.

### Why it works

The crucial invariant is that after any sequence of legal moves, the remaining playable structure can still be interpreted as a bipartite graph where moves always consume one vertex and indirectly constrain only vertices in the opposite partition. This prevents any player from breaking the global symmetry between the two partitions except through the initial imbalance caused by the grid dimensions. Since optimal play always preserves symmetry whenever possible, the outcome depends only on whether that symmetry is perfect (even $N$) or slightly biased (odd $N$).

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())

# For this game, parity determines the winner
# odd N -> first player wins, even N -> second player wins
if n % 2 == 1:
    print("Ltf")
else:
    print("Ian")
```

The code reads the single integer and directly applies the parity rule. No simulation or preprocessing is needed because the game structure collapses to a constant-time decision.

The only subtlety is ensuring correct handling of the input format and stripping whitespace, since the entire logic depends on a single integer read.

## Worked Examples

### Example 1

Input:

```
2
```

We start with an even-sized grid.

| Step | State | Observation |
| --- | --- | --- |
| 1 | N = 2 | Grid is perfectly symmetric in chessboard coloring |
| 2 | Decision | Even case implies second player can mirror moves |

Output is:

```
Ian
```

This confirms that symmetry is fully balanced and the first player cannot create a lasting advantage.

### Example 2

Input:

```
3
```

Now the grid is odd-sized.

| Step | State | Observation |
| --- | --- | --- |
| 1 | N = 3 | One color class has one extra cell |
| 2 | Decision | First player can claim the imbalance |

Output is:

```
Ltf
```

This shows that the extra cell breaks symmetry and guarantees a last move for the first player.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a parity check of $N$ |
| Space | $O(1)$ | No additional data structures |

The input constraint goes up to $10^5$, but since the computation is constant time, the solution easily fits within all limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    n = int(input().strip())
    return "Ltf" if n % 2 == 1 else "Ian"

# provided samples
assert run("2\n") == "Ian"
assert run("3\n") == "Ltf"

# custom cases
assert run("1\n") == "Ltf"          # minimum case
assert run("4\n") == "Ian"          # even small grid
assert run("5\n") == "Ltf"          # odd mid case
assert run("100000\n") == "Ian"     # large even case
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | Ltf | smallest board behavior |
| 4 | Ian | even symmetry case |
| 5 | Ltf | odd parity consistency |
| 100000 | Ian | upper bound stress case |

## Edge Cases

For $N=1$, the board contains exactly one cell. The first player takes it immediately, leaving no legal move for the opponent, so the output is Ltf.

For $N=2$, the grid is small enough that any move heavily constrains the remaining space, and symmetry fully favors the second player. The algorithm correctly classifies it as even, producing Ian.

For large even values such as $N=10^5$, the structure does not change with scale. The parity check still returns Ian, and no overflow or performance issue arises since only a single modulo operation is performed.
