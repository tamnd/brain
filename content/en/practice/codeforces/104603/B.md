---
title: "CF 104603B - Black and white"
description: "We are given an $N times N$ grid where each cell is either usable (black) or forbidden (white). The task is to place as many horizontal dominoes as possible, where each domino covers exactly two adjacent cells in the same row."
date: "2026-06-30T02:53:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104603
codeforces_index: "B"
codeforces_contest_name: "2023 Argentinian Programming Tournament (TAP)"
rating: 0
weight: 104603
solve_time_s: 45
verified: true
draft: false
---

[CF 104603B - Black and white](https://codeforces.com/problemset/problem/104603/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an $N \times N$ grid where each cell is either usable (black) or forbidden (white). The task is to place as many horizontal dominoes as possible, where each domino covers exactly two adjacent cells in the same row. A domino is valid only if both covered cells are black, and no cell can belong to more than one domino.

So the problem is equivalent to choosing as many disjoint horizontal adjacent pairs of black cells as possible across all rows.

The grid size is at most $50 \times 50$, so there are at most 2500 cells. This immediately rules out any exponential search over placements. Even a naive backtracking over all ways to place or not place a domino would be far too large because each row alone could generate exponential choices.

A key observation is that the rows are independent: dominoes never cross rows. So the problem decomposes into solving the same subproblem for each row and summing the results.

A subtle edge case is rows with alternating patterns where greedy pairing can fail if not careful. For example, in a row like `NNNN`, a naive greedy left-to-right pairing produces 2 dominoes correctly, but in patterns like `NNNNN`, careless skipping rules can miscount if implementation does not enforce disjoint usage strictly. Another case is rows with isolated blacks like `NBNBN`, where no domino can be placed despite many black cells.

## Approaches

A brute-force interpretation would consider each possible placement of horizontal dominoes on the grid. This can be seen as selecting edges between adjacent black cells, ensuring no vertex is reused. This is exactly a maximum matching problem on a graph where each cell is a node and edges exist between horizontal neighbors in the same row.

A naive solution would try all subsets of edges and check validity. With up to 2500 cells, even restricting to horizontal edges gives roughly $O(N^2)$ edges, and subsets of edges grow exponentially, around $2^{O(N^2)}$, which is completely infeasible.

The key simplification is structural: edges only exist between $(i, j)$ and $(i, j+1)$. That means each row is an independent path graph broken by white cells. In a path graph, maximum matching is trivial: greedily match consecutive available vertices from left to right.

This reduces the problem from a global matching problem to $N$ independent linear scans.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all domino subsets | $O(2^{N^2})$ | $O(N^2)$ | Too slow |
| Row-wise greedy pairing | $O(N^2)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Process the grid row by row, since dominoes never cross row boundaries. This ensures each decision is confined to independent subproblems.
2. For each row, scan from left to right while tracking whether the previous cell can be paired. We only attempt pairing when we see two consecutive black cells.
3. When we encounter a black cell, check the next cell. If it is also black, place a domino covering both and skip the next position. This guarantees no overlap.
4. If the next cell is white or we are at the end of the row, we cannot place a domino starting at this position, so we move forward.
5. Accumulate the number of placed dominoes for each row into a global total.

### Why it works

Each row forms a path where vertices are cells and edges exist only between consecutive black cells. The maximum number of disjoint edges in a path graph is obtained by greedily selecting the leftmost available edge whenever possible. Any alternative solution that skips a valid pair does not increase future options, because skipping only leaves the same or fewer opportunities for matching further right. This establishes that the greedy construction always produces an optimal matching per row.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    ans = 0

    for _ in range(n):
        row = input().strip()
        i = 0
        while i < n:
            if row[i] == 'N':
                if i + 1 < n and row[i + 1] == 'N':
                    ans += 1
                    i += 2
                else:
                    i += 1
            else:
                i += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the row-wise greedy strategy. We maintain an index `i` and move it forward depending on whether we form a domino or not. When two consecutive `N` cells appear, we immediately consume both and advance by 2 to enforce disjoint usage. Otherwise, we advance by 1.

The key subtlety is that we never reconsider a cell once skipped or used. This is what guarantees correctness: every cell participates in at most one decision, so no overlap is possible.

## Worked Examples

Consider a small grid:

```
N N B N
N N N B
B N N N
N B N N
```

Row-by-row execution:

| Row | i | row[i] | row[i+1] | Action | Dominoes |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | N | N | place | 1 |
| 2 | 2 | B | - | skip | 1 |
| 3 | 0 | N | N | place | 2 |
| 4 | 2 | N | B | skip | 2 |
| 5 | 0 | B | - | skip | 2 |
| 6 | 1 | N | N | place | 3 |
| 7 | 3 | N | - | end | 3 |

This demonstrates how greedy pairing extracts all available adjacent black pairs without conflict.

A second example:

```
N B N B N
N N B N N
B B B B B
N N N N N
N B B B N
```

For this grid:

| Row | Pattern | Dominoes |
| --- | --- | --- |
| 1 | NBNBN | 0 |
| 2 | N N B N N | 1 |
| 3 | BBBBB | 2 |
| 4 | NNNNN | 2 |
| 5 | NBBBN | 1 |

This shows that even dense black rows reduce to simple adjacent pairing, while alternating patterns contribute nothing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N^2)$ | Each cell is visited once across all rows |
| Space | $O(1)$ | Only constant extra variables are used |

The grid has at most 2500 cells, so a single linear scan over all cells is trivial within time limits. The solution runs well under 1 second and uses negligible memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

def solve():
    n = int(input().strip())
    ans = 0
    for _ in range(n):
        row = input().strip()
        i = 0
        while i < n:
            if row[i] == 'N':
                if i + 1 < n and row[i + 1] == 'N':
                    ans += 1
                    i += 2
                else:
                    i += 1
            else:
                i += 1
    print(ans)

# sample-style checks
assert run("5\nBNBNB\nBBNNN\nNNNNN\nBNNNN\nNNBNN\n") == "7"

# minimum size
assert run("1\nN\n") == "0"

# all white
assert run("3\nBBB\nBBB\nBBB\n") == "0"

# full black row
assert run("1\nNNNNN\n") == "2"

# alternating pattern
assert run("1\nNBNBN\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 black | 0 | smallest grid behavior |
| all white | 0 | no placements possible |
| full black row | 2 | maximal greedy pairing |
| alternating pattern | 0 | no adjacent matches |

## Edge Cases

A single-cell grid like `N` has no possible domino placement. The algorithm processes the row, sees no valid pair, and returns 0 correctly.

A completely black row like `NNNNN` is handled by repeatedly matching pairs at indices (0,1) and (2,3), leaving one leftover cell. The scan skips the leftover naturally, producing 2 dominoes.

An alternating pattern like `NBNBN` never triggers a valid adjacent pair, so the algorithm never increments the counter, correctly yielding 0.
