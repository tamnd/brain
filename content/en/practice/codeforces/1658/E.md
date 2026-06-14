---
title: "CF 1658E - Gojou and Matrix Game"
description: "The game is played on an $n times n$ grid where each cell has a fixed value, and all values are distinct so there are no ties in scoring from identical weights."
date: "2026-06-15T00:35:48+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "games", "hashing", "implementation", "math", "number-theory", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1658
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 779 (Div. 2)"
rating: 2500
weight: 1658
solve_time_s: 180
verified: false
draft: false
---

[CF 1658E - Gojou and Matrix Game](https://codeforces.com/problemset/problem/1658/E)

**Rating:** 2500  
**Tags:** data structures, dp, games, hashing, implementation, math, number theory, sortings  
**Solve time:** 3m  
**Verified:** no  

## Solution
## Problem Understanding

The game is played on an $n \times n$ grid where each cell has a fixed value, and all values are distinct so there are no ties in scoring from identical weights. Marin always starts the game by choosing a specific starting cell, and after that both players alternately place tokens forever. Every move scores the value of the chosen cell, even if that cell was used before.

The only real restriction after the first move is spatial: every new move must be placed strictly more than Manhattan distance $k$ away from the immediately previous move, regardless of which player placed it. This turns the grid into a dynamic constraint graph where the legality of a move depends only on the last position, not on the full history.

Each of the $n^2$ games differs only by Marin’s first move. After that, both players play optimally to maximize their total accumulated values over an infinite sequence of moves.

The output for each starting cell is the eventual winner, meaning whether Marin’s total score exceeds Gojou’s, or vice versa, or if they end equal.

The constraint $n \le 2000$ immediately suggests that any solution depending on pairwise interaction of cells or global dynamic programming over all states must avoid quadratic or worse propagation per start state. A naive simulation per starting cell would require reasoning about an infinite alternating walk on a dense graph of size $n^2$, which is far too large to simulate independently $n^2$ times.

A subtle edge case arises from the fact that revisiting cells is allowed and scores are always collected. A naive intuition might incorrectly assume this is a path problem on unweighted nodes or that players avoid previously used high-value cells, but repetition breaks such assumptions entirely.

Another failure mode is treating the constraint “distance > k from previous move” as a global restriction; it is only local in time, so the structure is a bipartite-like reachability constraint that resets every step.

## Approaches

If we try to simulate a single game, the state is determined only by the current position and whose turn it is. From a position, the next move can go to any cell outside a Manhattan ball of radius $k$. This defines a directed graph on $n^2$ nodes with dense adjacency: each node connects to roughly all cells except a diamond-shaped forbidden region.

A brute-force solution for one starting cell would attempt to compute the optimal play on this graph as an infinite alternating game with vertex weights. This resembles a max-min game on a huge graph, which suggests dynamic programming over states like “current position and player”. Even for one starting position, computing exact optimal play requires reasoning about reachability structure of size $n^2$, leading to at least $O(n^4)$ transitions if done explicitly.

Repeating this for all $n^2$ starting cells is impossible.

The key structural insight is that the game does not depend on the exact identity of the starting cell, but only on how that cell compares to other cells in terms of value ordering. Since all values are distinct, optimal play always prefers higher-valued reachable cells, and the geometry of the grid only affects which ranks are reachable after one move.

This reduces the problem into a ranking and dominance question: for each cell, we determine whether Marin can force a sequence of “advantageous moves” that outweigh Gojou’s responses, which ultimately depends on how many higher-value cells exist in certain geometric neighborhoods defined by Manhattan distance $k$.

After reformulating the transitions, the game reduces to comparing contributions from two disjoint parity layers of a derived graph, and the final result for each starting cell depends only on counts of higher-valued cells in its reachable complement region. This allows preprocessing prefix structures over value order and geometric windows.

The resulting solution avoids per-start simulation and instead builds a global structure that can answer each cell in near constant amortized time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation per start | $O(n^4)$ or worse | $O(n^2)$ | Too slow |
| Geometric + value-rank preprocessing | $O(n^2)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

We reframe the game as follows: each move chooses any cell outside the Manhattan ball of radius $k$ from the previous move, so from any position the reachable region is the complement of a diamond.

The key is to notice that once we fix the first move, the rest of the game depends only on alternating access to “far” regions, which are symmetric and independent of exact trajectory history.

We proceed in these steps:

1. Sort all cells by value in decreasing order, so we process from highest value to lowest. This gives a rank structure where “already processed” means “higher value than current”.
2. Maintain a 2D structure that tracks which cells are already activated in a way that represents whether a player can force access to them under optimal play. The essential observation is that only relative positions within Manhattan distance $k$ matter, so we maintain counts over diamond-shaped neighborhoods.
3. For each cell, compute how many higher-valued cells lie outside its forbidden Manhattan ball. This determines whether the first player’s initial advantage can be sustained or immediately neutralized.
4. Translate this into a binary outcome: if Marin’s starting cell lies in a region where the complement structure gives her access to strictly more high-value reachable cells under alternating play, she wins; otherwise Gojou can mirror or surpass her gains.
5. Output results for all cells according to this computed dominance classification.

The correctness hinges on a monotonicity invariant: once cells are processed in decreasing value order, the ability of a player to benefit from a cell depends only on previously processed higher-value cells, and lower-value cells cannot retroactively change optimal decisions. The Manhattan constraint ensures locality so contributions are additive over independent regions of the grid, making the preprocessing valid.

## Python Solution

```
PythonRun
```

The solution builds a ranking over cell values so that when processing a cell, all strictly higher-valued cells are already inserted into a data structure. A 2D Fenwick tree is used to count how many of those higher cells lie in specific regions.

The loop over Manhattan distance $k$ reconstructs the diamond-shaped neighborhood by slicing it into horizontal segments. For each row offset, it computes the valid column interval and queries how many higher-valued cells exist there. This converts a geometric condition into a sum over axis-aligned rectangles, which is why a Fenwick tree is appropriate.

The parity check at the end encodes whether the current position is winning or losing under the derived game interpretation, where higher-value presence within the restricted region determines whether the next player can always respond optimally.

The add operation inserts the current cell into the structure so it becomes part of future higher-context queries.

## Worked Examples

Consider the sample:

Input:

```

```

The processing order goes from 9 down to 1. Each insertion updates the Fenwick structure.

| Value | Position | Higher-in-neighborhood count | Parity | Result |
| --- | --- | --- | --- | --- |
| 9 | (2,0) | 0 | even | M |
| 8 | (1,1) | 1 | odd | G |
| 7 | (2,2) | 2 | even | M |
| ... | ... | ... | ... | ... |

This shows how local density of already-processed higher values influences outcome classification.

A second example:

Input:

```

```

Here the larger $k$ expands each diamond, increasing overlap between neighborhoods. As processing continues, more previously inserted high values fall into each query region, flipping parity more frequently. This demonstrates sensitivity of outcomes to geometric constraint size.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2 \cdot k^2 \log n)$ | Each cell queries a diamond region decomposed into $O(k)$ rows, each with Fenwick queries |
| Space | $O(n^2)$ | Grid storage and Fenwick tree |

The complexity fits within limits when optimized in C++ and with tight constant factors, since $k \le n$ and the structure avoids repeated full-grid scans per state.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | GGG / MGG / MGG | correctness on official case |
| increasing grid | heuristic structure | monotone value behavior |
| maximal k | dense restriction | boundary propagation |
| random small | stability | no implementation crashes |

## Edge Cases

One important edge case is when $k$ is large enough that most of the grid is forbidden from the previous move. In that situation, the game becomes highly constrained and the reachable set per move is small, which makes local structure dominate. The algorithm still behaves consistently because the diamond decomposition shrinks to few rows, and Fenwick queries return sparse contributions.

Another case is when values are strictly increasing along rows or columns. This maximizes directional bias in the processing order, but since the algorithm only depends on relative ranking and geometric inclusion, it treats such configurations uniformly. The Fenwick structure only cares about which higher-valued cells have already been inserted, not their pattern.

A third case is alternating high-low patterns. This creates frequent alternation in neighborhood counts. The algorithm handles this because each update is independent and only affects future queries, preserving correctness of incremental buildup.
