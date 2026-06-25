---
title: "CF 106369G - Not So Close"
description: "The problem asks us to place condo units on an r by c rectangular grid. A condo occupies one grid square, and two condos are not allowed to be placed in squares that touch each other. Touching includes all eight directions: horizontal, vertical, and diagonal neighbors."
date: "2026-06-25T08:20:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106369
codeforces_index: "G"
codeforces_contest_name: "2023 UCF Local Programming Contest"
rating: 0
weight: 106369
solve_time_s: 37
verified: true
draft: false
---

[CF 106369G - Not So Close](https://codeforces.com/problemset/problem/106369/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem asks us to place condo units on an `r` by `c` rectangular grid. A condo occupies one grid square, and two condos are not allowed to be placed in squares that touch each other. Touching includes all eight directions: horizontal, vertical, and diagonal neighbors.

The task is to count how many different valid placement sets exist. Two placements are different if at least one square contains a condo in one arrangement but not the other. The empty arrangement is also valid. The answer can be very large, so it must be printed modulo `10^9 + 7`.

The input contains only two integers, the number of rows and columns of the grid. The number of rows is small, at most 10, while the number of columns can reach 1000. This asymmetry is the main clue. A solution depending exponentially on the number of rows is practical, but one depending exponentially on the number of columns is impossible. Since a grid with 1000 columns cannot be handled by trying all column choices, we need to process the grid one column at a time.

A useful way to think about the limit `r <= 10` is that one column has only `2^r` possible occupancy patterns. For ten rows this is only 1024 masks, and after removing invalid masks with vertically adjacent condos, the number becomes even smaller. This makes a state compression approach feasible. A naive search over every square would have `2^(r*c)` possibilities, which is astronomically large even for a small grid.

The tricky cases are mostly caused by forgetting one of the forbidden neighbor directions.

For example, a single column with two rows:

```
Input:
2 1
```

The correct output is:

```
3
```

The possible arrangements are empty, top square occupied, or bottom square occupied. A careless solution that only checks horizontal conflicts might count both squares occupied and incorrectly return 4.

Another common mistake is ignoring diagonal conflicts. For example:

```
Input:
2 2
```

The correct output is:

```
5
```

The only non-empty valid arrangements contain exactly one condo, because every pair of squares in a 2 by 2 grid touches. A solution that only prevents side-by-side and vertical neighbors would incorrectly allow diagonal pairs.

The smallest grid also needs attention:

```
Input:
1 1
```

The correct output is:

```
2
```

There are two possibilities: build nothing or build one condo. Implementations that initialize the dynamic programming array incorrectly can accidentally return zero.

# Approaches

The direct approach is to consider every square independently and decide whether to place a condo there. For a grid with `r * c` squares, this gives `2^(r*c)` possible arrangements. The method is logically correct because it examines every possible set of placements and keeps only valid ones, but it becomes unusable immediately. Even a grid with only 10 rows and 20 columns would already have `2^200` possibilities.

The reason brute force fails is not that the grid has no structure. The important observation is that the interaction between columns is limited. When we decide the contents of one column, the only information needed about previous columns is the previous column's occupancy pattern. We do not need to remember the whole history.

A column can be represented as a bitmask. Bit `i` is one if row `i` contains a condo in that column. First, we discard masks with two adjacent set bits because those represent vertically touching condos inside the same column.

Then we process columns from left to right. For every pair of consecutive column masks, we check whether they conflict. Two columns conflict if a condo appears in the same row, one row above, or one row below in the neighboring column. If they do not conflict, the two columns can appear consecutively in a valid arrangement.

The brute force works because every complete placement is a sequence of column choices. It fails because the number of sequences is huge. The observation that only adjacent columns affect each other lets us replace the full history with a small dynamic programming state.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(r*c)) | O(r*c) | Too slow |
| Optimal | O(c * S^2) | O(S) | Accepted |

Here, `S` is the number of valid column masks. For `r = 10`, `S` is only 144.

# Algorithm Walkthrough

1. Generate every possible column mask from `0` to `2^r - 1`. Keep only masks where no two neighboring rows are both occupied. These are the only possible states for a single column because vertical touching is forbidden inside one column.
2. Precompute which pairs of valid masks can be placed next to each other. Two masks are compatible when they have no occupied rows in common and no occupied rows shifted by one position. The shifts represent diagonal touching between neighboring columns.
3. Initialize the dynamic programming value of every valid mask for the first column as `1`. Each mask represents one possible first-column arrangement.
4. Process the remaining columns one by one. For every current column mask, add the number of ways to reach it from every compatible mask in the previous column. The previous columns do not matter anymore because all future conflicts only involve the current last column.
5. Sum all dynamic programming values after the final column. Every possible final column state represents a complete valid grid arrangement.

Why it works: the invariant is that after processing any number of columns, `dp[mask]` equals the number of valid arrangements of those processed columns where the last column has exactly the occupancy pattern `mask`. The transition only allows pairs of columns that do not violate any touching rule, so it never creates an invalid arrangement. Every valid arrangement has a unique sequence of column masks, and each transition in that sequence is considered, so every valid arrangement is counted exactly once.

# Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10 ** 9 + 7

def solve():
    r, c = map(int, input().split())

    masks = []
    for mask in range(1 << r):
        if (mask & (mask << 1)) == 0:
            masks.append(mask)

    n = len(masks)

    transitions = [[] for _ in range(n)]
    for i in range(n):
        a = masks[i]
        for j in range(n):
            b = masks[j]
            if (a & b) == 0 and (a & (b << 1)) == 0 and (a & (b >> 1)) == 0:
                transitions[i].append(j)

    dp = [1] * n

    for _ in range(1, c):
        ndp = [0] * n
        for prev in range(n):
            value = dp[prev]
            if value:
                for nxt in transitions[prev]:
                    ndp[nxt] += value
                    if ndp[nxt] >= MOD:
                        ndp[nxt] -= MOD
        dp = ndp

    print(sum(dp) % MOD)

if __name__ == "__main__":
    solve()
```

The first part builds the list of legal column states. The check `(mask & (mask << 1)) == 0` removes masks with vertically adjacent occupied squares. Shifting the mask by one row is enough because only consecutive rows can touch vertically.

The transition construction compares every pair of valid states. The expression `(a & b)` catches condos directly beside each other horizontally. The two shifted comparisons catch diagonal neighbors. The masks are indexed rather than stored directly in the dynamic programming array, which keeps transitions compact.

The dynamic programming loop starts with one column already processed. Every state has one way to exist as the first column, including the empty state. Each following column creates a new array because the previous values must represent exactly the previous column, avoiding accidental mixing of states from different iterations.

Python integers do not overflow, but the modulo operation is still required after additions because the answer grows exponentially. The final sum includes every possible ending column state, including the empty column.

# Worked Examples

There are no official samples available in the statement, so the following traces use small constructed cases.

For `r = 1`, `c = 3`, the grid is a single row. Adjacent cells cannot both contain condos, so the answer follows the independent choices of three positions.

Input:

```
1 3
```

| Column | Current mask states | DP values |
| --- | --- | --- |
| 1 | 0, 1 | 1, 1 |
| 2 | 0, 1 | 2, 1 |
| 3 | 0, 1 | 3, 2 |

The final sum is `3 + 2 = 5`. These arrangements are empty, each single position, and the two non-adjacent pairs. The trace demonstrates that the DP keeps only the previous column information while still counting all possibilities.

For a grid where diagonal conflicts matter:

Input:

```
2 2
```

The valid masks are `00`, `01`, and `10`.

| Column | Previous state | New state | Added value |
| --- | --- | --- | --- |
| 1 | start | 00 | 1 |
| 1 | start | 01 | 1 |
| 1 | start | 10 | 1 |
| 2 | 00 | 00 | 1 |
| 2 | 00 | 01 | 1 |
| 2 | 00 | 10 | 1 |
| 2 | 01 | 00 | 1 |
| 2 | 10 | 00 | 1 |

The final count is `5`: empty, or one of the four cells. The transitions correctly reject all pairs of non-empty masks because every pair of cells in a 2 by 2 grid touches.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(c * S^2) | Each column transition checks compatible pairs of valid masks. |
| Space | O(S^2) | The transition lists plus two dynamic programming arrays are stored. |

For `r <= 10`, the number of valid masks is very small, so even 1000 columns can be processed easily. The algorithm avoids dependence on the total number of cells and fits comfortably within the intended limits.

# Test Cases

```python
import sys, io

MOD = 10 ** 9 + 7

def solution(inp):
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    r, c = map(int, sys.stdin.readline().split())

    masks = []
    for mask in range(1 << r):
        if (mask & (mask << 1)) == 0:
            masks.append(mask)

    n = len(masks)
    trans = [[] for _ in range(n)]

    for i, a in enumerate(masks):
        for j, b in enumerate(masks):
            if (a & b) == 0 and (a & (b << 1)) == 0 and (a & (b >> 1)) == 0:
                trans[i].append(j)

    dp = [1] * n
    for _ in range(c - 1):
        ndp = [0] * n
        for i, val in enumerate(dp):
            for j in trans[i]:
                ndp[j] = (ndp[j] + val) % MOD
        dp = ndp

    ans = str(sum(dp) % MOD)
    sys.stdin = old_stdin
    return ans

assert solution("1 1\n") == "2", "minimum grid"
assert solution("2 2\n") == "5", "all cells touch in a 2x2 grid"
assert solution("1 5\n") == "13", "single row Fibonacci case"
assert solution("2 1\n") == "3", "vertical boundary case"
assert solution("3 3\n") == "35", "small multi-row grid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `2` | Smallest possible grid and empty placement handling |
| `2 2` | `5` | Diagonal conflict handling |
| `1 5` | `13` | One-dimensional reduction |
| `2 1` | `3` | Vertical adjacency boundary |
| `3 3` | `35` | General profile DP behavior |

# Edge Cases

For the input:

```
2 1
```

the generated masks are `00`, `01`, and `10`. Since there is only one column, there are no horizontal transitions to consider. The answer is the number of valid single-column masks, which is 3. The algorithm handles this because the initial dynamic programming array already represents the complete grid when `c = 1`.

For the input:

```
2 2
```

the algorithm creates the same three column states. When checking transitions, every pair of non-empty states is rejected because either the rows overlap or the shifted masks overlap diagonally. Only transitions involving the empty state remain, giving five total arrangements. This catches implementations that forget diagonal checks.

For the input:

```
1 5
```

the only states are empty and occupied. The transition allows an occupied state only after an empty state, because two adjacent columns cannot both contain condos. The DP produces the sequence of independent sets on a line, ending with 13 arrangements.

For the input:

```
1 1
```

the initial state array contains two possibilities. Since no transitions are needed, the final answer is simply the sum of the initial states. This confirms that the empty arrangement and the single-condo arrangement are both counted.
