---
title: "CF 104412K - Knockout Spell"
description: "We are given a square grid of size $N times N$, where each cell contains a digit from 0 to 9 representing terrain type. We are also given a fixed size $K$, and we need to examine every possible $K times K$ sub-square inside the grid."
date: "2026-06-30T22:52:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104412
codeforces_index: "K"
codeforces_contest_name: "2023 ICPC Gran Premio de Mexico 2da Fecha"
rating: 0
weight: 104412
solve_time_s: 51
verified: true
draft: false
---

[CF 104412K - Knockout Spell](https://codeforces.com/problemset/problem/104412/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a square grid of size $N \times N$, where each cell contains a digit from 0 to 9 representing terrain type. We are also given a fixed size $K$, and we need to examine every possible $K \times K$ sub-square inside the grid.

A sub-square is considered valid if all four of its corner cells contain the same value. The task is to count how many such $K \times K$ sub-squares exist in the grid.

The input constraints make the grid potentially large, up to $1000 \times 1000$. That immediately rules out any solution that re-checks every $K \times K$ square cell-by-cell in the worst case. A naive check per square would examine $K^2$ cells, leading to $O(N^2 K^2)$, which can reach $10^{12}$ operations when $N = K = 1000$, far beyond feasible limits.

A more subtle issue is overlapping computation. Adjacent $K \times K$ windows share most of their interior, but a naive approach would recompute everything from scratch.

A few edge cases deserve attention.

If $K = N$, there is exactly one square to check, the whole grid. The answer is either 1 or 0 depending on whether the four corners match.

If all values in the grid are identical, every $K \times K$ sub-square is valid, so the answer is $(N-K+1)^2$.

If only one digit appears at corners but interior differs, a naive solution that incorrectly checks all cells instead of only corners would still work logically but waste time; however, a buggy solution might accidentally include interior constraints, which would be wrong since only corners matter.

## Approaches

The brute-force approach is straightforward. We iterate over every possible top-left corner $(i, j)$ of a $K \times K$ sub-square. For each one, we explicitly compare all $K^2$ cells or at least traverse the boundary. Even if we optimize slightly and only check the four corners, the brute-force still needs to do this for $(N-K+1)^2$ positions, which is at most $10^6$. That part is fine. The real cost appears only if we incorrectly verify full squares.

So the key observation is that the condition depends only on four positions: top-left, top-right, bottom-left, bottom-right. Everything else inside the square is irrelevant. This collapses the problem into a constant-time check per position.

Thus, instead of scanning grids or maintaining prefix structures, we simply iterate over all valid starting points and compare four cells.

The problem reduces from a 2D geometric aggregation task to a simple sliding enumeration problem with constant work per window.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (full square check) | $O(N^2 K^2)$ | $O(1)$ | Too slow |
| Corner-only check | $O(N^2)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read $N$ and $K$, then store the grid in a 2D array. This is necessary because we need random access to any cell when checking corners.
2. Iterate over all possible top-left positions of a $K \times K$ square. These positions are $(i, j)$ where $0 \le i \le N-K$ and $0 \le j \le N-K$. These bounds ensure the square stays inside the grid.
3. For each position $(i, j)$, identify its four corners: $(i, j)$, $(i, j+K-1)$, $(i+K-1, j)$, and $(i+K-1, j+K-1)$. These are the only cells that matter for validity.
4. Check whether all four corner values are equal. If they are, increment the answer.
5. After processing all positions, output the accumulated count.

The key design choice is restricting checks to corners only. This is valid because the condition never references interior cells, so any additional computation would be redundant.

### Why it works

Every valid placement is defined entirely by a local condition on four fixed positions. Each $K \times K$ square is uniquely determined by its top-left corner, and the validity predicate depends only on values at fixed offsets from that anchor. Since we evaluate every anchor exactly once and apply the exact condition defining validity, no valid square is missed and no invalid square is counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, K = map(int, input().split())
    grid = [list(map(int, input().split())) for _ in range(N)]
    
    ans = 0
    
    for i in range(N - K + 1):
        for j in range(N - K + 1):
            a = grid[i][j]
            b = grid[i][j + K - 1]
            c = grid[i + K - 1][j]
            d = grid[i + K - 1][j + K - 1]
            if a == b == c == d:
                ans += 1
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the algorithm. The nested loops enumerate all valid top-left corners. The four corner accesses are constant-time array lookups, ensuring the inner loop remains $O(1)$.

The main subtlety is indexing: the bottom-right corner is at $i + K - 1, j + K - 1$, not $i + K, j + K$. Off-by-one errors here are the most common source of bugs.

## Worked Examples

### Example 1

Input:

```
2 2
0 0
0 0
```

| i | j | corners (TL, TR, BL, BR) | equal? | count |
| --- | --- | --- | --- | --- |
| 0 | 0 | (0,0,0,0) | yes | 1 |

This confirms that when all values are identical, the single possible square is valid.

### Example 2

Input:

```
2 2
1 2
1 1
```

| i | j | corners (TL, TR, BL, BR) | equal? | count |
| --- | --- | --- | --- | --- |
| 0 | 0 | (1,2,1,1) | no | 0 |

This shows that even though three cells match, the mismatch at one corner invalidates the square.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N^2)$ | We examine each possible $K \times K$ placement once, and each check is constant time |
| Space | $O(N^2)$ | Storage for the grid |

The grid size of up to $10^6$ cells fits comfortably in memory, and $10^6$ constant-time checks easily pass within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("""2 2
0 0
0 0
""") == "1", "sample 1"

assert run("""2 2
1 2
1 1
""") == "0", "sample 2"

assert run("""5 3
1 5 1 6 1
1 7 8 9 5
1 1 1 1 1
1 2 3 4 1
1 1 1 1 1
""") == "5", "sample 3"

# custom cases
assert run("""3 2
1 1 2
1 1 2
3 3 3
""") == "1", "single valid square"

assert run("""4 3
7 7 7 7
7 1 2 7
7 3 4 7
7 7 7 7
""") == "4", "multiple boundary-valid squares"

assert run("""3 3
9 9 9
9 8 9
9 9 9
""") == "1", "only full grid"

assert run("""3 2
1 2 1
3 4 5
6 7 8
""") == "0", "no matching corners"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3x2 with partial matches | 1 | detects single valid placement |
| 4x3 border structure | 4 | multiple overlapping valid windows |
| full 3x3 with center mismatch | 1 | correctness on full-grid case |
| fully distinct grid | 0 | rejects all invalid windows |

## Edge Cases

When $K = N$, there is exactly one candidate square. The algorithm evaluates a single iteration with $(i, j) = (0, 0)$. It compares the four corners of the entire grid directly and returns 1 only if they match. No out-of-bounds access occurs because $i + K - 1 = N - 1$, which is valid indexing.

When all grid values are identical, every iteration satisfies the condition. The loops run over $(N-K+1)^2$ positions, and each comparison returns true. The final answer equals the number of possible placements, matching the combinatorial count of sub-squares.

When only interior cells differ but corners match, the algorithm still counts correctly because it never inspects interior positions. For example, in a $3 \times 3$ square:

```
1 1 1
1 9 1
1 1 1
```

A $3 \times 3$ window has matching corners (all 1), so it is counted once, regardless of the central 9. This confirms that restricting attention to corners is both sufficient and necessary for correctness.
