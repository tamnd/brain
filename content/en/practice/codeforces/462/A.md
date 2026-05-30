---
title: "CF 462A - Appleman and Easy Task"
description: "We are given an n×n board, where each cell contains either an 'x' or an 'o'. The task is to check a local property for every cell: whether the number of orthogonally adjacent cells containing 'o' is even."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 462
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 263 (Div. 2)"
rating: 1000
weight: 462
solve_time_s: 62
verified: true
draft: false
---

[CF 462A - Appleman and Easy Task](https://codeforces.com/problemset/problem/462/A)

**Rating:** 1000  
**Tags:** brute force, implementation  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an _n_×_n_ board, where each cell contains either an 'x' or an 'o'. The task is to check a local property for every cell: whether the number of orthogonally adjacent cells containing 'o' is even. Two cells are adjacent if they share a side, so each inner cell has up to four neighbors, edge cells have three or two, and corner cells have two. The output is "YES" if all cells satisfy this property and "NO" otherwise.

The input size constraint is small, _n_ ≤ 100. This is important because it implies we can afford to check every cell and its neighbors directly without worrying about performance. Even in the worst case of a 100×100 board, we would perform at most 100×100×4 = 40,000 operations, which is negligible for a 1-second time limit.

Non-obvious edge cases include very small boards (n=1) where there are no neighbors, and configurations where only boundary cells have 'o's. For instance, a 1×1 board with a single 'o' should output "YES" because it has zero neighbors, which is even. Another edge case is when all cells contain 'o'; each inner cell has four neighbors, which is even, but corner cells have only two neighbors, which is still even, so the board is valid.

## Approaches

The brute-force approach is straightforward: iterate over every cell and count the number of 'o's among its neighbors. If any cell has an odd count, we immediately return "NO". Otherwise, after checking all cells, we return "YES". This works because the board is small enough to allow direct neighbor inspection.

We can formalize the brute-force: for cell (i,j), check (i-1,j), (i+1,j), (i,j-1), (i,j+1) if they exist. Counting neighbors for each cell is O(1), and there are n² cells, so the total time is O(n²). This is acceptable here. There is no faster asymptotic approach needed; the problem's constraints make the brute-force both correct and efficient. The key insight is recognizing that adjacency is strictly local, so we never need to do anything global like graph traversal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n²) | Accepted |
| Optimal | O(n²) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Read the integer n and then read n lines of n characters into a 2D list representing the board. This allows direct access to any cell by row and column indices.
2. Iterate through each cell in the board using two nested loops for rows and columns.
3. For each cell at position (i,j), initialize a counter to zero. This counter will track how many of the four possible neighbors contain 'o'.
4. Check each neighbor: above (i-1,j), below (i+1,j), left (i,j-1), and right (i,j+1). Only check a neighbor if the indices are within bounds of the board. If the neighbor contains 'o', increment the counter.
5. After counting neighbors for the current cell, check if the counter is odd. If it is odd, print "NO" and terminate. This works because a single violation is enough to invalidate the entire board.
6. If the loop completes without finding any cell with an odd count, print "YES". Every cell has satisfied the even adjacency condition.

Why it works: The algorithm examines every cell exactly once and evaluates the property of interest using only its immediate neighbors. Since the problem is local and all relevant information is in the cell's adjacent positions, there are no hidden interactions. Any cell with an odd number of 'o' neighbors is immediately detected, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
board = [input().strip() for _ in range(n)]

for i in range(n):
    for j in range(n):
        count = 0
        if i > 0 and board[i-1][j] == 'o':
            count += 1
        if i < n-1 and board[i+1][j] == 'o':
            count += 1
        if j > 0 and board[i][j-1] == 'o':
            count += 1
        if j < n-1 and board[i][j+1] == 'o':
            count += 1
        if count % 2 != 0:
            print("NO")
            sys.exit()
print("YES")
```

The solution reads the board efficiently with `sys.stdin.readline` to avoid overhead from `input()`. It explicitly checks bounds before accessing neighbors to prevent index errors. Using `sys.exit()` stops computation as soon as a violation is found, which is slightly more efficient than checking a flag after the loop. Counting neighbors directly avoids extra data structures, keeping space complexity minimal.

## Worked Examples

**Sample Input 1**

```
3
xxo
xox
oxx
```

| i | j | Neighbors with 'o' | count % 2 |
| --- | --- | --- | --- |
| 0 | 0 | (0,1),(1,0) none, (1,0) 'x' | 0 |
| 0 | 1 | (0,0)x,(0,2)o,(1,1)x | 1 -> yes? check |
| Actually: |  |  |  |
| (0,1): up n/a, down (1,1)x, left (0,0)x, right (0,2)o → 1 neighbor 'o' → odd → triggers NO? |  |  |  |

Wait sample output is YES, so recheck.

Board:

row0: x x o

row1: x o x

row2: o x x

Compute neighbors:

(0,0): up n/a, down (1,0)x, left n/a, right (0,1)x → 0 → even → OK

(0,1): up n/a, down (1,1)o, left (0,0)x, right (0,2)o → 2 → even → OK

(0,2): up n/a, down (1,2)x, left (0,1)x, right n/a → 0 → even → OK

(1,0): up (0,0)x, down (2,0)o, left n/a, right (1,1)o → 2 → even → OK

(1,1): up (0,1)x, down (2,1)x, left (1,0)x, right (1,2)x → 0 → even → OK

(1,2): up (0,2)o, down (2,2)x, left (1,1)x, right n/a → 1 → odd? Wait sample output is YES, so must recalc:

up (0,2)o →1, down (2,2)x →0, left (1,1)o →1, total 2 → even → OK

(2,0): up (1,0)x, down n/a, left n/a, right (2,1)x → 0 → even → OK

(2,1): up (1,1)o, down n/a, left (2,0)o, right (2,2)x → 2 → even → OK

(2,2): up (1,2)x, down n/a, left (2,1)x, right n/a →0 → even → OK

All even → YES

This demonstrates careful boundary checking is crucial to avoid off-by-one errors.

**Sample Input 2**

```
1
o
```

| i | j | Neighbors with 'o' | count % 2 |
| --- | --- | --- | --- |
| 0 | 0 | none → 0 | 0 → even → OK |

Output: YES. Even with a single-cell board, the algorithm handles it correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Each of the n² cells is visited once, counting up to 4 neighbors each, constant time. |
| Space | O(n²) | The board is stored in memory as a list of n strings of length n. |

The algorithm is well within the 1-second time limit even for the maximum n=100, and memory usage is minimal relative to the 256 MB constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    n = int(input())
    board = [input().strip() for _ in range(n)]
    for i in range(n):
        for j in range(n):
            count = 0
            if i > 0 and board[i-1][j] == 'o':
                count += 1
            if i < n-1 and board[i+1][j] == 'o':
                count += 1
            if j > 0 and board[i][j-1] == 'o':
                count += 1
            if j < n-1 and board[i][j+1] == 'o':
                count += 1
            if count % 2 != 0:
                return "NO"
    return "YES"

# provided samples
assert run("3\nxxo\nxox\noxx\n") == "
```
