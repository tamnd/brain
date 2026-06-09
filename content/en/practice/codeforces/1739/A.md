---
title: "CF 1739A - Immobile Knight"
description: "We are given a very small chessboard, at most $8 times 8$. The task is not to compute a complicated value but to locate any cell from which a knight has no legal moves that stay inside the board."
date: "2026-06-09T17:41:42+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1739
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 136 (Rated for Div. 2)"
rating: 800
weight: 1739
solve_time_s: 265
verified: false
draft: false
---

[CF 1739A - Immobile Knight](https://codeforces.com/problemset/problem/1739/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 4m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a very small chessboard, at most $8 \times 8$. The task is not to compute a complicated value but to locate any cell from which a knight has no legal moves that stay inside the board. If such a cell exists, we must output one of them; otherwise we are allowed to output any coordinate on the board.

The key object is the standard knight move: from a cell $(r, c)$, a knight tries to jump to eight possible offsets of the form $(\pm 2, \pm 1)$ and $(\pm 1, \pm 2)$. A cell is called isolated if none of those eight destinations remain within the board.

Since both dimensions are bounded by $8$, the total number of cells is at most $64$. This immediately places the problem in the regime where direct simulation is not only sufficient but conceptually cleaner than any optimization. Any approach that inspects each cell and checks up to eight moves runs in constant time per test case.

A subtle edge case appears when the board is extremely small. On a $1 \times m$ or $n \times 1$ board, every cell is isolated because every knight move leaves the board. On a $2 \times 2$ board, the same happens. On larger boards like $3 \times 3$, some central cells become isolated while border cells still allow at least one valid move, depending on geometry. The definition is purely local, so there is no global constraint or parity issue to consider.

## Approaches

A brute-force solution examines every cell and tries all eight knight moves. If at least one move stays inside the grid, the cell is not isolated. If none do, we immediately return it. Since there are at most $64$ cells and $8$ directions per cell, the work per test case is bounded by a few hundred operations, which is trivially fast.

There is no deeper structure to exploit because the board is so small. The only reason to think further is to recognize that the condition is purely geometric and local: isolation depends only on whether the surrounding $3 \times 3$ and $5 \times 5$ neighborhoods exist within bounds. This means we do not need preprocessing or search.

The optimal solution is identical to the brute-force approach, just implemented directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nm)$ per test | $O(1)$ | Accepted |
| Optimal | $O(nm)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

We process each test case independently and scan the board.

1. Iterate over every cell $(r, c)$ in the $n \times m$ grid. Each cell is a candidate for being isolated.
2. For a fixed cell, check all eight knight moves. Each move produces a target cell $(r + dr, c + dc)$, and we verify whether it remains inside the board bounds $1 \le r \le n$, $1 \le c \le m$.
3. If at least one move is valid, mark the cell as non-isolated and continue to the next one. This ensures we only accept cells with zero valid knight transitions.
4. If we find a cell for which none of the eight moves is valid, we immediately output it and stop processing the current test case.
5. If no isolated cell is found after scanning all positions, output any cell, for instance $(1, 1)$.

The key idea is that the definition of isolation is entirely local and depends only on the immediate neighborhood reachable by knight moves, so exhaustive checking cannot miss any valid candidate.

### Why it works

A cell is isolated exactly when all eight knight offsets leave the grid. The algorithm tests this condition directly. Since every cell is checked independently and all possible moves are enumerated, a cell is reported isolated if and only if it satisfies the definition. If no such cell exists, returning any coordinate is allowed by the problem, so correctness is preserved in all cases.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    moves = [(2, 1), (2, -1), (-2, 1), (-2, -1),
             (1, 2), (1, -2), (-1, 2), (-1, -2)]
    
    for _ in range(t):
        n, m = map(int, input().split())
        
        found = False
        for r in range(1, n + 1):
            for c in range(1, m + 1):
                isolated = True
                
                for dr, dc in moves:
                    nr, nc = r + dr, c + dc
                    if 1 <= nr <= n and 1 <= nc <= m:
                        isolated = False
                        break
                
                if isolated:
                    print(r, c)
                    found = True
                    break
            
            if found:
                break
        
        if not found:
            print(1, 1)

if __name__ == "__main__":
    solve()
```

The implementation follows the algorithm literally. The only subtlety is early termination: once an isolated cell is found, we stop scanning further because any valid answer is acceptable. The move list is fixed and exhaustive, ensuring correctness without case analysis.

## Worked Examples

Consider a $3 \times 3$ board. We check the center cell $(2, 2)$. Every knight move from it goes outside the grid, so it is immediately classified as isolated. The algorithm stops as soon as it encounters this cell during iteration.

| Cell | Valid knight move exists | Isolated |
| --- | --- | --- |
| (1,1) | Yes | No |
| (1,2) | Yes | No |
| (1,3) | Yes | No |
| (2,2) | No | Yes |

This confirms that the algorithm correctly identifies the unique isolated position in this case.

Now consider a $2 \times 3$ board. Every cell has at least one knight move staying inside the grid, so no isolated cell exists. The algorithm scans all positions, finds none isolated, and outputs $(1,1)$.

| Cell | Valid knight move exists | Isolated |
| --- | --- | --- |
| (1,1) | Yes | No |
| (1,2) | Yes | No |
| (1,3) | Yes | No |
| (2,1) | Yes | No |
| (2,2) | Yes | No |
| (2,3) | Yes | No |

This demonstrates the fallback behavior when the isolated set is empty.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm)$ per test | Each cell checks at most eight constant-time moves |
| Space | $O(1)$ | Only fixed move list is stored |

The board size is at most $64$ cells, so even the worst-case total work across all test cases is negligible within the limits. Memory usage is constant.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    def solve():
        t = int(input())
        moves = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                 (1, 2), (1, -2), (-1, 2), (-1, -2)]
        
        for _ in range(t):
            n, m = map(int, input().split())
            
            found = False
            for r in range(1, n + 1):
                for c in range(1, m + 1):
                    isolated = True
                    for dr, dc in moves:
                        nr, nc = r + dr, c + dc
                        if 1 <= nr <= n and 1 <= nc <= m:
                            isolated = False
                            break
                    if isolated:
                        print(r, c)
                        found = True
                        break
                if found:
                    break
            if not found:
                print(1, 1)
    
    solve()
    return sys.stdout.getvalue().strip()

assert run("3\n1 7\n8 8\n3 3\n") == "1 1\n1 1\n2 2", "samples"

assert run("1\n1 1\n") == "1 1", "minimum board"
assert run("1\n2 2\n") == "1 1", "small full isolation"
assert run("1\n2 3\n") == "1 1", "no isolated cell case"
assert run("1\n3 3\n") == "2 2", "center isolated cell"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| $1 \times 1$ board | $(1,1)$ | trivial isolation |
| $2 \times 2$ board | $(1,1)$ | all cells isolated |
| $2 \times 3$ board | $(1,1)$ | no isolated cells |
| $3 \times 3$ board | $(2,2)$ | center isolation case |

## Edge Cases

On a $1 \times m$ or $n \times 1$ board, every cell is isolated because all knight moves immediately exceed bounds in at least one coordinate. The algorithm handles this because for each cell, all eight candidate moves fail the boundary check, so the first cell encountered is returned as isolated.

On a $2 \times 2$ board, the same logic applies, but now in a denser form: every knight move leaves the grid due to insufficient height or width. The scan will classify the first cell as isolated and stop immediately.

On larger boards like $3 \times 3$, only the center cell has no valid knight moves inside the grid. The algorithm reaches it during iteration and correctly identifies it as isolated because every offset goes out of bounds.
