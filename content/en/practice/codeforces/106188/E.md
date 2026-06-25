---
title: "CF 106188E - Screenmaxxing"
description: "We are looking at a wall represented by an n × n grid of tiles. Each tile has one of two colors, gold or silver. The family wants to keep one square region of size k × k visible and make that visible region consist of a single color."
date: "2026-06-25T10:46:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106188
codeforces_index: "E"
codeforces_contest_name: "UTPC x WiCS Contest 11-12-2025"
rating: 0
weight: 106188
solve_time_s: 38
verified: true
draft: false
---

[CF 106188E - Screenmaxxing](https://codeforces.com/problemset/problem/106188/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are looking at a wall represented by an `n × n` grid of tiles. Each tile has one of two colors, gold or silver. The family wants to keep one square region of size `k × k` visible and make that visible region consist of a single color. A tile inside the chosen square can be replaced with the other color, and the goal is to choose the square that needs the fewest replacements.

The input describes the size of the wall, the required visible square size, and the current colors of all tiles. The output is the minimum number of tiles that must be changed so that some `k × k` part of the wall becomes uniform.

The constraints are the key to choosing the algorithm. The wall can have up to `1000 × 1000` tiles, which means there can be one million cells. Trying every possible square and scanning all its cells would require roughly `n² * k²` work in the worst case. With a million cells, that can become around one trillion operations, far beyond what a normal time limit allows. We need a way to evaluate each possible square without rechecking every tile.

The tricky cases are mostly related to squares touching the border and squares that are already uniform. If the whole visible square already has the same color, the answer must be zero.

For example:

```
Input
3 2
GGG
GGG
SSS

Output
0
```

The top two rows contain a uniform `2 × 2` square. A solution that always assumes at least one replacement is needed would fail.

Another case is when the best square is not the first or last possible position:

```
Input
5 3
GGGGG
SSSSS
GGGGG
SSSSS
GGGGG

Output
3
```

The middle `3 × 3` square has six gold and three silver tiles, so changing the three silver tiles is optimal. Checking only corners would miss this answer.

## Approaches

A direct solution is to try every possible top-left corner of a `k × k` square. For each position, we count how many gold and silver tiles it contains. If there are `g` gold tiles and `s` silver tiles, making it all gold costs `s` changes and making it all silver costs `g` changes. The cost of this square is the smaller of the two values.

This approach is correct because it checks every possible visible region. The problem is the amount of repeated work. There are about `(n-k+1)²` possible squares, and each square contains `k²` tiles. In the worst case this becomes `O(n²k²)`, which is too slow for `n = 1000`.

The important observation is that neighboring squares overlap heavily. Moving the square one column to the right removes one column of `k` tiles and adds another column of `k` tiles. There is no reason to recount the entire square.

A two-dimensional prefix sum gives exactly the information we need. We build a matrix where each cell tells how many gold tiles exist in the rectangle from the origin to that cell. Then any rectangle sum can be found in constant time using four prefix values. After that, every candidate square can be evaluated in `O(1)` time, making the full solution `O(n²)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²k²) | O(1) | Too slow |
| Optimal | O(n²) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Read the grid and build a prefix sum array for gold tiles. The value at `(i, j)` stores the number of gold tiles in the rectangle from `(1, 1)` to `(i, j)`. This lets us answer any rectangle query without scanning its cells.
2. Iterate over every possible top-left corner of a `k × k` square. The bottom-right corner is determined from the top-left position and `k`.
3. Use the prefix sum formula to find the number of gold tiles inside the current square. The number of silver tiles is `k * k - gold`.
4. Compute the cost of making this square gold and the cost of making it silver. The smaller value is the number of replacements required for this square.
5. Keep the minimum cost among all squares and print it.

Why it works: the prefix sum does not change the meaning of the grid, it only stores accumulated information. Every possible visible square is examined, and for each one we calculate exactly how many tiles of each color it contains. Since the minimum number of changes for a square is the smaller color count, the minimum over all examined squares is the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    pref = [[0] * (n + 1) for _ in range(n + 1)]

    for i in range(n):
        row_sum = 0
        for j in range(n):
            if grid[i][j] == 'G':
                row_sum += 1
            pref[i + 1][j + 1] = pref[i][j + 1] + row_sum

    ans = k * k

    for i in range(n - k + 1):
        for j in range(n - k + 1):
            x1, y1 = i, j
            x2, y2 = i + k, j + k

            gold = (
                pref[x2][y2]
                - pref[x1][y2]
                - pref[x2][y1]
                + pref[x1][y1]
            )

            silver = k * k - gold
            ans = min(ans, gold, silver)

    print(ans)

if __name__ == "__main__":
    solve()
```

The prefix construction uses one-based indexing internally. This avoids special cases when the rectangle starts at the first row or column because the row and column before the grid are filled with zeros.

The rectangle query subtracts the two rectangles outside the target square and adds back the overlapping part. This is the standard inclusion-exclusion formula for two-dimensional prefix sums.

The loops stop at `n - k + 1` because a square cannot start in a position where its bottom or right edge would go outside the wall. The final answer starts as `k * k` because the worst possible square would require changing every tile.

## Worked Examples

### Sample 1

Input:

```
3 2
GGG
SSG
GGG
```

Trace:

| Top-left | Gold tiles | Silver tiles | Changes |
| --- | --- | --- | --- |
| (0,0) | 2 | 2 | 2 |
| (0,1) | 3 | 1 | 1 |
| (1,0) | 2 | 2 | 2 |
| (1,1) | 3 | 1 | 1 |

The best square requires one replacement, so the answer is `1`.

This demonstrates that the algorithm checks overlapping squares independently and does not assume the first valid-looking square is optimal.

### Sample 2

Input:

```
5 3
GGGGG
SSSSS
GGGGG
SSSSS
GGGGG
```

Trace:

| Top-left | Gold tiles | Silver tiles | Changes |
| --- | --- | --- | --- |
| (0,0) | 6 | 3 | 3 |
| (0,1) | 6 | 3 | 3 |
| (0,2) | 6 | 3 | 3 |
| (1,0) | 3 | 6 | 3 |
| (1,1) | 3 | 6 | 3 |
| (1,2) | 3 | 6 | 3 |
| (2,0) | 6 | 3 | 3 |
| (2,1) | 6 | 3 | 3 |
| (2,2) | 6 | 3 | 3 |

Every possible square needs three changes, so the answer is `3`.

This confirms that the algorithm handles cases where many positions have the same optimal value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Building the prefix sum and checking every possible square both take quadratic time. |
| Space | O(n²) | The prefix sum stores one value for every cell plus the extra border row and column. |

With at most one million cells, an `O(n²)` solution performs around a few million operations and fits comfortably within the limits.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    pref = [[0] * (n + 1) for _ in range(n + 1)]

    for i in range(n):
        cur = 0
        for j in range(n):
            if grid[i][j] == 'G':
                cur += 1
            pref[i + 1][j + 1] = pref[i][j + 1] + cur

    ans = k * k
    for i in range(n - k + 1):
        for j in range(n - k + 1):
            x2, y2 = i + k, j + k
            gold = (
                pref[x2][y2]
                - pref[i][y2]
                - pref[x2][j]
                + pref[i][j]
            )
            ans = min(ans, gold, k * k - gold)

    return str(ans) + "\n"

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = solve()
    sys.stdin = old
    return out

assert run("3 2\nGGG\nSSG\nGGG\n") == "1\n"
assert run("5 3\nGGGGG\nSSSSS\nGGGGG\nSSSSS\nGGGGG\n") == "3\n"

assert run("1 1\nG\n") == "0\n"
assert run("4 4\nGSSG\nSGGS\nSGGS\nGSSG\n") == "8\n"
assert run("3 3\nSSS\nSSS\nSSS\n") == "0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` single tile | `0` | Minimum size and already uniform square |
| All silver `3 × 3` | `0` | All-equal values |
| Mixed full-size square | `8` | Boundary where only one possible square exists |
| Alternating pattern | `1` in sample | Correct prefix rectangle counting |

## Edge Cases

For the already uniform case:

```
Input
3 2
GGG
GGG
SSS
```

The prefix sum reports that the top-left `2 × 2` square contains four gold tiles and zero silver tiles. The algorithm computes `min(0, 4)` as the replacement cost, so the answer is zero.

For the case where the best square touches the border:

```
Input
4 2
GGSS
GGSS
SSGG
SSGG
```

The square starting at `(0,0)` contains only gold tiles and needs no changes. The prefix sum query includes the first row and first column correctly because of the extra zero border, so the answer is found without any special handling.

For the case where the only valid square is the whole grid:

```
Input
3 3
GSS
SGS
SSG
```

There is only one candidate. The prefix sum returns three gold tiles, so changing to all silver costs three while changing to all gold costs six. The algorithm outputs three, which is the correct minimum.
