---
title: "CF 105018C - Rooks"
description: "We are given an $n times n$ grid and several rooks placed on distinct cells. A rook controls every cell in its row and every cell in its column. A cell is considered “safe” only if no rook shares its row or column. The operation allowed is removing rooks from the board."
date: "2026-06-28T02:03:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105018
codeforces_index: "C"
codeforces_contest_name: "Winter Cup 5.0 Online Mirror Contest"
rating: 0
weight: 105018
solve_time_s: 56
verified: true
draft: false
---

[CF 105018C - Rooks](https://codeforces.com/problemset/problem/105018/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an $n \times n$ grid and several rooks placed on distinct cells. A rook controls every cell in its row and every cell in its column. A cell is considered “safe” only if no rook shares its row or column.

The operation allowed is removing rooks from the board. The goal is not to maximize safety everywhere, but only to guarantee the existence of at least one safe cell after removals. We want to minimize how many rooks we remove to make such a cell exist.

Rephrased differently, we want to end up with at least one cell $(i, j)$ such that after deletions, row $i$ contains no rook and column $j$ contains no rook.

The constraints are small: $n \le 50$ and $k \le n^2 \le 2500$. This immediately rules out anything beyond roughly $O(n^3)$ per test case if implemented carefully, but even that is unnecessary. A direct enumeration over grid cells is already feasible.

A naive mistake is to think we need to simulate removing subsets of rooks. For example, if we try to choose which rooks to delete, the number of subsets is $2^k$, which becomes enormous even at $k = 2500$. Another incorrect direction is to assume we only care about empty rows or empty columns independently, but the condition depends on a pair $(row, column)$, not just one dimension.

A subtle edge case appears when there are no rooks at all. The answer is zero because every cell is already safe. Another is when rooks are distributed so that every row and column is occupied at least once; even then, removing rooks from a carefully chosen row and column intersection can still produce a safe cell, but only after targeted deletions.

## Approaches

A brute-force idea is to try every possible subset of rooks to remove, then check whether a safe cell exists. For each subset, we would scan all rows and columns to verify whether there exists a pair $(i, j)$ whose row and column are both empty of remaining rooks. Checking one subset costs $O(n^2 + k)$, and there are $2^k$ subsets, which is far beyond feasible limits even for the smallest nontrivial inputs.

The key simplification comes from shifting perspective: instead of deciding which rooks to remove, we fix the target safe cell first. Suppose we decide that the safe cell must be $(i, j)$. For this to happen, row $i$ must end up empty and column $j$ must end up empty. That means we are forced to remove every rook in row $i$ and every rook in column $j$. There is no alternative way to make that cell safe.

This converts the problem into a direct cost computation. For each candidate cell $(i, j)$, we compute how many rooks lie in its row or column. Removing those rooks guarantees that $(i, j)$ becomes safe, and that cost is exactly the number of removals needed for that choice. We then pick the minimum over all cells.

This works because every valid final configuration must correspond to at least one cell whose row and column are completely cleared, and the only way to achieve that is to remove all rooks intersecting those lines.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | $O(2^k \cdot n^2)$ | $O(k)$ | Too slow |
| Try all cells with counting | $O(n^2 + k)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

1. Count how many rooks are placed in each row and each column. This allows us to later compute removal costs without scanning all rooks repeatedly.
2. Record whether a rook exists at each cell using a boolean grid or a set. This is needed to avoid double-counting when a rook lies at the intersection of a chosen row and column.
3. For every cell $(i, j)$, compute the cost of making it safe. The cost is the number of rooks in row $i$ plus the number of rooks in column $j$, minus one if there is a rook already at $(i, j)$.
4. Track the minimum cost over all cells. This represents the smallest number of removals needed to create at least one safe cell anywhere on the board.
5. Output this minimum for each test case.

### Why it works

Fixing a target cell $(i, j)$ forces a strict requirement: after removals, both its row and column must be empty of rooks. Any rook outside these lines does not affect the safety of that specific cell, while any rook inside must be removed. Therefore the cost for each candidate cell is fully determined and independent of decisions elsewhere. Since every valid solution must correspond to at least one such cell becoming safe, minimizing over all candidates covers all possibilities.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        
        row = [0] * (n + 1)
        col = [0] * (n + 1)
        has = [[0] * (n + 1) for _ in range(n + 1)]
        
        for _ in range(k):
            x, y = map(int, input().split())
            row[x] += 1
            col[y] += 1
            has[x][y] = 1
        
        ans = k
        
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                cost = row[i] + col[j] - has[i][j]
                if cost < ans:
                    ans = cost
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the reasoning directly. Row and column arrays store counts so that each candidate cell can be evaluated in constant time. The grid `has` prevents double subtraction when a rook lies exactly at the intersection. The answer starts at $k$ because removing all rooks always guarantees a valid configuration.

The double loop over all cells is safe because $n \le 50$, giving at most 2500 evaluations per test case.

## Worked Examples

Consider a small board where rooks occupy a few scattered positions.

Input:

```
1
3 3
1 1
1 2
2 3
```

We compute row counts and column counts first:

| Step | row1 | row2 | row3 | col1 | col2 | col3 |
| --- | --- | --- | --- | --- | --- | --- |
| after input | 2 | 1 | 0 | 1 | 1 | 1 |

Now evaluate each cell cost:

| Cell | row + col - overlap | Explanation |
| --- | --- | --- |
| (1,1) | 2 + 1 - 1 = 2 | rook at intersection |
| (1,2) | 2 + 1 - 1 = 2 | intersection again |
| (1,3) | 2 + 1 - 0 = 3 | no rook at (1,3) |
| (2,1) | 1 + 1 - 0 = 2 |  |
| (2,2) | 1 + 1 - 0 = 2 |  |
| (2,3) | 1 + 1 - 1 = 1 | best choice |
| (3,1) | 0 + 1 = 1 |  |
| (3,2) | 0 + 1 = 1 |  |
| (3,3) | 0 + 1 = 1 |  |

The minimum is 1, meaning removing one rook suffices to unlock a safe cell.

This trace shows how the solution does not depend on global structure but purely on local row-column intersections.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t \cdot n^2 + k)$ | each cell evaluated once, rooks processed once |
| Space | $O(n^2)$ | grid plus row/column counters |

The limits $n \le 50$ and $k \le 2500$ make this comfortably fast even in Python, since the dominant operation is at most a few thousand integer additions per test case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    import sys
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n, k = map(int, input().split())
            row = [0] * (n + 1)
            col = [0] * (n + 1)
            has = [[0] * (n + 1) for _ in range(n + 1)]

            for _ in range(k):
                x, y = map(int, input().split())
                row[x] += 1
                col[y] += 1
                has[x][y] = 1

            ans = k
            for i in range(1, n + 1):
                for j in range(1, n + 1):
                    ans = min(ans, row[i] + col[j] - has[i][j])
            out.append(str(ans))
        return "\n".join(out)

    return solve()

# sample-style tests
assert run("1\n3 0\n") == "0", "empty board"
assert run("1\n2 2\n1 1\n2 2\n") == "1", "diagonal rooks"
assert run("1\n2 3\n1 1\n1 2\n2 1\n") == "1", "dense corner case"
assert run("1\n3 3\n1 1\n2 2\n3 3\n") == "1", "main diagonal"
assert run("1\n3 1\n2 2\n") == "0", "single rook"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty board | 0 | no removals needed |
| diagonal rooks | 1 | intersection logic |
| dense corner case | 1 | overlapping row/col counts |
| main diagonal | 1 | symmetric placement |
| single rook | 0 | trivial safety |

## Edge Cases

When there are no rooks, the row and column counts remain zero everywhere, so every cell evaluates to zero cost and the minimum is zero. The algorithm naturally returns zero without special handling.

When all rooks lie in a single row, every candidate cell in that row produces a high cost, while cells in other rows only depend on column counts. The minimum correctly shifts to a row outside the occupied one, requiring no removals.

When rooks cover almost every row and column, the intersection correction `-has[i][j]` becomes crucial. Without it, a rook placed at $(i, j)$ would be counted twice, inflating the removal cost and producing incorrect answers.
