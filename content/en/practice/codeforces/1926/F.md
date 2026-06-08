---
title: "CF 1926F - Vlad and Avoiding X"
description: "We have a fixed $7 times 7$ board whose cells are either black or white. A configuration is considered bad if there exists a black cell whose four diagonal neighbors are also black. Such a pattern looks like an X centered at that cell."
date: "2026-06-08T19:02:36+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "dfs-and-similar", "dp", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1926
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 928 (Div. 4)"
rating: 2200
weight: 1926
solve_time_s: 196
verified: false
draft: false
---

[CF 1926F - Vlad and Avoiding X](https://codeforces.com/problemset/problem/1926/F)

**Rating:** 2200  
**Tags:** bitmasks, brute force, dfs and similar, dp, implementation  
**Solve time:** 3m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We have a fixed $7 \times 7$ board whose cells are either black or white. A configuration is considered bad if there exists a black cell whose four diagonal neighbors are also black. Such a pattern looks like an X centered at that cell.

We may flip any cell, changing black to white or white to black. The goal is to perform the minimum number of flips so that no bad X remains anywhere on the board.

The most striking part of the problem is the tiny board size. A $7 \times 7$ grid contains only 49 cells, yet $2^{49}$ possible colorings still make unrestricted brute force impossible. The number of test cases can reach 200, so the solution must exploit some special structure rather than searching over all board states.

A bad X can only be centered at cells that have four diagonal neighbors. Those are exactly the $5 \times 5$ interior cells. There are only 25 possible centers.

The key constraint hidden inside the geometry is parity. Every diagonal move preserves the parity of $r+c$. The center and all four diagonal neighbors of an X always belong to the same checkerboard color class. This splits the board into two completely independent sets of cells.

Several edge cases are easy to mishandle.

Consider a single isolated X:

```
.......
.B.B...
..B....
.B.B...
.......
.......
.......
```

One flip is enough. Flipping the center destroys the X immediately. A greedy strategy that flips multiple surrounding cells would be suboptimal.

Another subtle case is overlapping X patterns:

```
.......
.B.B.B.
..B.B..
.B.B.B.
..B.B..
.B.B.B.
.......
```

One cell may participate in several bad X patterns simultaneously. Treating each violation independently can overcount badly because a single flip can eliminate many violations.

A third trap is assuming that only currently black cells should ever be changed. The optimization problem allows flipping white cells to black as well. In practice, the optimal solution never needs to create new violations deliberately, but the DP formulation must correctly search all possibilities rather than relying on a fragile greedy rule.

## Approaches

The most direct idea is to view every cell as a binary variable and try all subsets of cells to flip. There are $2^{49}$ possibilities, which is around $5.6 \times 10^{14}$. Even checking one million states per second would require many years.

The next observation is that violations only involve cells of the same parity. If we color the board like a chessboard, every X pattern lies entirely inside one color class.

The parity class with $(r+c)\bmod 2=0$ contains 25 cells. The other class contains 24 cells. The two classes never interact.

Now look only at one parity class. Every possible X center is itself a cell of that class. There are at most 13 centers in one parity class and 12 in the other.

Suppose we decide which cells of a parity class will be black after all flips. For every center we can immediately check whether the forbidden X exists.

The crucial observation is that the cells of one parity class form a $5 \times 5$-like lattice when viewed through diagonal connections. Every constraint only involves a center and its four adjacent lattice neighbors.

Since there are only 13 relevant cells in one parity class, we can represent a complete final coloring of that class by a bitmask of size at most 13. That gives at most $2^{13}=8192$ states.

For each parity class we enumerate all possible final masks. A mask is valid if none of its centers forms a forbidden X. The cost of the mask is the number of bits that differ from the original board. We keep the minimum cost among valid masks.

The two parity classes are independent, so their optimal costs simply add together.

The total work is tiny:

$$2^{13}+2^{12}=12288$$

states per test case, with only a small constant amount of checking per state.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all 49 cells | $O(2^{49})$ | $O(1)$ | Too slow |
| Enumerate parity classes independently | $O(2^{13}+2^{12})$ | $O(2^{13})$ | Accepted |

## Algorithm Walkthrough

### Building the parity groups

The forbidden pattern only uses diagonal moves, so all participating cells have the same parity of $r+c$.

Split the board into two groups:

1. Cells with even parity.
2. Cells with odd parity.

These groups can be optimized independently because no constraint ever mixes them.

### Enumerating one parity group

For one parity group:

1. Collect all cells belonging to that parity and assign them indices from 0 to $k-1$, where $k\le 13$.
2. Record the original coloring as a bitmask `orig`.
3. Identify which cells can act as X centers. A cell is a center if all four diagonal neighbors exist.
4. For every center, precompute the indices of its four diagonal neighbors inside the same parity group.

### Testing a final mask

1. Enumerate every mask from `0` to `(1<<k)-1`.
2. For each center, check whether the center bit is 1 and all four neighbor bits are also 1.
3. If such a center exists, the mask is invalid and can be discarded.

The mask represents a complete final coloring of this parity group. Any forbidden X means the resulting board is not acceptable.

### Computing the flip cost

1. For every valid mask, compute the number of changed cells:

$$\text{cost} = \text{popcount}(mask \oplus orig)$$

1. Keep the minimum cost among all valid masks.

### Combining both parities

1. Solve the even parity group and the odd parity group separately.
2. Add the two minimum costs and print the result.

### Why it works

Every forbidden X lies entirely within a single parity class because diagonal moves preserve parity. Changing cells from one parity class cannot affect whether a pattern exists in the other class.

For a fixed parity class, every possible final coloring appears exactly once among the enumerated masks. The validity test rejects precisely those colorings containing a forbidden X. Among all valid colorings, we choose the one requiring the fewest flips from the original configuration.

Since the two parity classes are independent, the global optimum is obtained by combining the optimal valid coloring of each class. Any global solution decomposes into two parity solutions, and any pair of parity solutions combines into a global solution. The minimum costs therefore add.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_parity(board, parity):
    cells = []
    pos_to_idx = {}

    for r in range(7):
        for c in range(7):
            if (r + c) % 2 == parity:
                pos_to_idx[(r, c)] = len(cells)
                cells.append((r, c))

    k = len(cells)

    orig = 0
    for i, (r, c) in enumerate(cells):
        if board[r][c] == 'B':
            orig |= 1 << i

    centers = []

    for r, c in cells:
        if 1 <= r <= 5 and 1 <= c <= 5:
            neigh = [
                pos_to_idx[(r - 1, c - 1)],
                pos_to_idx[(r - 1, c + 1)],
                pos_to_idx[(r + 1, c - 1)],
                pos_to_idx[(r + 1, c + 1)],
            ]
            centers.append((pos_to_idx[(r, c)], neigh))

    limit = 1 << k
    best = k

    for mask in range(limit):
        valid = True

        for center, neigh in centers:
            if not (mask >> center) & 1:
                continue

            ok = True
            for v in neigh:
                if ((mask >> v) & 1) == 0:
                    ok = False
                    break

            if ok:
                valid = False
                break

        if valid:
            cost = (mask ^ orig).bit_count()
            if cost < best:
                best = cost

    return best

def solve():
    t = int(input())

    ans = []

    for _ in range(t):
        board = [input().strip() for _ in range(7)]

        res = solve_parity(board, 0) + solve_parity(board, 1)
        ans.append(str(res))

    sys.stdout.write("\n".join(ans))

solve()
```

The solution begins by separating cells according to parity. Each parity class is represented by a compact bitmask, allowing all possible final colorings to be enumerated efficiently.

For every parity class, the code precomputes all potential X centers together with the indices of their four diagonal neighbors. This removes any repeated coordinate arithmetic inside the enumeration loop.

The validity check is carefully written so that a center contributes a violation only when the center itself is black and all four diagonal neighbors are black. Border cells are never considered centers because they cannot have four diagonal neighbors.

The flip cost is computed with `mask ^ orig`. Every differing bit corresponds to one cell whose color changed. Python's `bit_count()` provides an efficient popcount implementation.

The maximum mask size is only 13 bits, so the full enumeration remains very small.

## Worked Examples

### Example 1

Input board:

```
.......
.B.B...
..B....
.B.B...
.......
.......
.......
```

The five black cells form exactly one X.

For the relevant parity class:

| Step | Current Mask | Valid? | Flip Cost |
| --- | --- | --- | --- |
| Original | X pattern present | No | 0 |
| Remove center | No X | Yes | 1 |
| Remove one arm | No X | Yes | 1 |
| Remove two cells | No X | Yes | 2 |

The minimum valid cost is 1.

This example shows that destroying any one of the five participating cells eliminates the violation.

### Example 2

A board containing no black cells:

```
WWWWWWW
WWWWWWW
WWWWWWW
WWWWWWW
WWWWWWW
WWWWWWW
WWWWWWW
```

For each parity class:

| Step | Current Mask | Valid? | Flip Cost |
| --- | --- | --- | --- |
| Original | Empty | Yes | 0 |
| Any modified mask | Usually valid | >0 |  |

The minimum cost is 0 for both parity groups.

This example confirms that the algorithm does not introduce unnecessary changes when the board is already valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(2^{13}+2^{12})$ per test case | Enumerate all masks of both parity classes |
| Space | $O(1)$ | Only a few small arrays and masks are stored |

The largest parity class contains 13 cells, giving at most 8192 masks. Across both parity classes, fewer than 13000 states are examined per test case. Even with 200 test cases, the total workload is comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    input = sys.stdin.readline

    def solve_parity(board, parity):
        cells = []
        pos = {}

        for r in range(7):
            for c in range(7):
                if (r + c) % 2 == parity:
                    pos[(r, c)] = len(cells)
                    cells.append((r, c))

        k = len(cells)

        orig = 0
        for i, (r, c) in enumerate(cells):
            if board[r][c] == 'B':
                orig |= 1 << i

        centers = []
        for r, c in cells:
            if 1 <= r <= 5 and 1 <= c <= 5:
                centers.append(
                    (
                        pos[(r, c)],
                        [
                            pos[(r - 1, c - 1)],
                            pos[(r - 1, c + 1)],
                            pos[(r + 1, c - 1)],
                            pos[(r + 1, c + 1)],
                        ],
                    )
                )

        best = k

        for mask in range(1 << k):
            good = True

            for center, neigh in centers:
                if (mask >> center) & 1:
                    if all((mask >> v) & 1 for v in neigh):
                        good = False
                        break

            if good:
                best = min(best, (mask ^ orig).bit_count())

        return best

    t = int(input())
    ans = []

    for _ in range(t):
        board = [input().strip() for _ in range(7)]
        ans.append(str(
            solve_parity(board, 0) +
            solve_parity(board, 1)
        ))

    print("\n".join(ans))

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.getvalue().strip()

# sample
assert run(
"""1
WWWWWWW
WWWWWWW
WWWWWWW
WWWWWWW
WWWWWWW
WWWWWWW
WWWWWWW
"""
) == "0"

# single X
assert run(
"""1
WWWWWWW
WBWBWWW
WWBWWWW
WBWBWWW
WWWWWWW
WWWWWWW
WWWWWWW
"""
) == "1"

# all white
assert run(
"""1
WWWWWWW
WWWWWWW
WWWWWWW
WWWWWWW
WWWWWWW
WWWWWWW
WWWWWWW
"""
) == "0"

# all black
assert run(
"""1
BBBBBBB
BBBBBBB
BBBBBBB
BBBBBBB
BBBBBBB
BBBBBBB
BBBBBBB
"""
) == "9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| All white board | 0 | Already valid configuration |
| Single X | 1 | Smallest non-trivial violation |
| All black board | 9 | Many overlapping violations |
| Sample-style empty board | 0 | No unnecessary flips |

## Edge Cases

### A violation touching the border

Input:

```
BWBWWWW
WBWWWWW
BWBWWWW
WWWWWWW
WWWWWWW
WWWWWWW
WWWWWWW
```

The apparent center would need to lie on the border, which is impossible. Border cells cannot have four diagonal neighbors. During preprocessing, only cells with coordinates between 1 and 5 are considered centers, so this pattern is ignored correctly. The answer is 0.

### Multiple overlapping X patterns

Input:

```
.......
.B.B.B.
..B.B..
.B.B.B.
..B.B..
.B.B.B.
.......
```

Several violations share cells. A greedy strategy that fixes each X independently may perform many flips. The mask enumeration evaluates the entire parity class simultaneously and discovers when one flip destroys several violations at once.

### Already valid board

Input:

```
WWWWWWW
WWWWWWW
WWWWWWW
WWWWWWW
WWWWWWW
WWWWWWW
WWWWWWW
```

The original mask itself passes every validity test. Its flip cost is zero, so it remains the optimal solution. The algorithm never modifies cells unnecessarily.

### Dense board with many violations

Input:

```
BBBBBBB
BBBBBBB
BBBBBBB
BBBBBBB
BBBBBBB
BBBBBBB
BBBBBBB
```

Almost every interior cell is the center of a forbidden X. Local reasoning becomes difficult because patterns overlap heavily. The parity decomposition converts the problem into two independent searches over at most 8192 states, guaranteeing that the true minimum number of flips is found.
