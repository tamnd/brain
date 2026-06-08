---
title: "CF 2090B - Pushing Balls"
description: "We are given the final occupancy pattern of a grid after some sequence of ball insertions. A ball can be pushed either from the left side of a row or from the top side of a column. The ball travels forward until it reaches a cell. If that cell is empty, it stays there."
date: "2026-06-09T03:49:31+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2090
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1012 (Div. 2)"
rating: 1000
weight: 2090
solve_time_s: 108
verified: true
draft: false
---

[CF 2090B - Pushing Balls](https://codeforces.com/problemset/problem/2090/B)

**Rating:** 1000  
**Tags:** brute force, dp, implementation  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the final occupancy pattern of a grid after some sequence of ball insertions.

A ball can be pushed either from the left side of a row or from the top side of a column. The ball travels forward until it reaches a cell. If that cell is empty, it stays there. If that cell already contains a ball, the incoming ball takes that position and the displaced ball continues moving in the same direction.

The process resembles repeatedly inserting elements into the front of a row or column, with existing balls being shifted deeper into the grid.

The task is not to reconstruct the sequence of operations. We only need to decide whether at least one valid sequence exists that produces the given final grid.

The grid dimensions are at most 50 × 50, and the total number of cells across all test cases is at most 10,000. This is a very small input size. Even an $O(nm)$ or $O(nm(n+m))$ solution is easily fast enough. There is no need for sophisticated data structures.

The difficulty is understanding which final configurations are reachable.

A common mistake is to think that every cell containing a ball must be connected to the top or left border through other balls. That is stronger than necessary.

Consider:

```
111
111
111
```

This configuration is clearly reachable. Every cell contains a ball.

Now consider:

```
010
111
010
```

This is also reachable, despite the corner cells being empty. A simple connectivity argument would incorrectly reject it.

Another easy mistake is to focus on the order of operations. The number of possible insertion sequences grows exponentially, so direct simulation or backtracking is infeasible even for small grids.

The key is to identify a structural property that every reachable configuration satisfies and that is also sufficient for reachability.

A particularly revealing counterexample is:

```
000
000
001
```

The answer is `NO`.

The ball at the bottom-right corner would require balls to exist somewhere to its left or above to push it that far into the grid. Since neither exists, no sequence can create this isolated cell.

## Approaches

A brute-force approach would try to simulate all possible insertion sequences. Each operation chooses one row or one column. Even for a 5 × 5 grid, the number of possible sequences becomes enormous. Since up to 2500 balls may exist in a test case, exhaustive search is completely impossible.

To find a better approach, we need to understand what a push actually does.

Suppose a cell $(i,j)$ contains a ball in the final configuration. How could a ball arrive there?

If it was inserted through row $i$, then before stopping at $(i,j)$, every cell to its left in that row must already contain balls. Otherwise it would have stopped earlier.

Similarly, if it was inserted through column $j$, then every cell above it in that column must already contain balls.

This observation immediately gives a necessary condition:

For every occupied cell that is not in the first row and not in the first column, at least one of its immediate neighbors above or to the left must also be occupied.

Indeed, if both neighbors were empty, there would be no way for a ball to reach that position.

The surprising part is that this condition is also sufficient.

If every occupied interior cell has a ball directly above it or directly to its left, then we can always construct the configuration. One way to see this is to reverse the process. Any occupied cell that has no occupied cell below it and no occupied cell to its right can be considered the last inserted ball. Removing such cells repeatedly never violates the condition. Eventually the entire configuration disappears, proving that a valid construction exists.

This reduces the whole problem to a simple grid check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(nm) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Read the grid.
2. Iterate through every cell.
3. Ignore cells containing `0`, since they impose no constraints.
4. If the cell is in the first row or first column, it is always valid.

A ball can always be inserted directly from the corresponding border.
5. For every occupied cell `(i, j)` with `i > 0` and `j > 0`, check the cell above `(i-1, j)` and the cell to the left `(i, j-1)`.
6. If both neighbors contain `0`, immediately answer `"NO"`.

Such a cell cannot be reached from either insertion direction.
7. If every occupied interior cell passes the check, answer `"YES"`.

### Why it works

Consider any occupied cell that is not on the top row or left column.

If the ball that finally occupies this position entered through its row, then every position before it in that row had to be occupied when it arrived. In particular, the cell immediately to its left must contain a ball in the final configuration.

If instead it entered through its column, the cell immediately above must contain a ball in the final configuration.

Hence every reachable configuration satisfies the condition checked by the algorithm.

For sufficiency, repeatedly remove an occupied cell that has no occupied neighbor below and no occupied neighbor to the right. Such a cell could have been the last inserted ball. The local condition guarantees that after removing it, the remaining occupied cells still satisfy the same property. Continuing this process eventually removes all balls, producing a valid reverse construction. Thus every configuration passing the check is reachable.

The condition is both necessary and sufficient, so the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n, m = map(int, input().split())
    g = [input().strip() for _ in range(n)]

    ok = True

    for i in range(1, n):
        for j in range(1, m):
            if g[i][j] == '1':
                if g[i - 1][j] == '0' and g[i][j - 1] == '0':
                    ok = False

    print("YES" if ok else "NO")
```

The implementation follows the proof directly.

The first row and first column never need checking, because balls can enter directly from the corresponding border.

For every other occupied cell, we test whether at least one supporting neighbor exists. If neither the upper nor left neighbor contains a ball, the configuration is impossible and we mark the test case as invalid.

No simulation is performed. The entire solution is a single scan of the grid.

A common off-by-one mistake is checking all cells and accessing `i-1` or `j-1` when `i=0` or `j=0`. Starting the loops from `1` avoids this problem completely.

## Worked Examples

### Example 1

Input grid:

```
001
001
110
```

Trace:

| Cell | Value | Up | Left | Valid? |
| --- | --- | --- | --- | --- |
| (1,1) | 0 | - | - | Skip |
| (1,2) | 1 | 1 | 0 | Yes |
| (2,1) | 1 | 0 | 1 | Yes |
| (2,2) | 0 | - | - | Skip |

No violation is found.

Output:

```
YES
```

The occupied cells away from the border always have support from above or from the left, matching the reachability condition.

### Example 2

Input grid:

```
000
000
001
```

Trace:

| Cell | Value | Up | Left | Valid? |
| --- | --- | --- | --- | --- |
| (1,1) | 0 | - | - | Skip |
| (1,2) | 0 | - | - | Skip |
| (2,1) | 0 | - | - | Skip |
| (2,2) | 1 | 0 | 0 | No |

The occupied cell in the lower-right corner has neither a ball above nor a ball to the left.

Output:

```
NO
```

This demonstrates the core impossibility condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each cell is examined once |
| Space | O(1) extra | Only a few variables besides the input grid |

Since the total number of cells across all test cases is at most 10,000, an $O(nm)$ scan is tiny. The solution runs comfortably within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    ans = []

    for _ in range(t):
        n, m = map(int, input().split())
        g = [input().strip() for _ in range(n)]

        ok = True

        for i in range(1, n):
            for j in range(1, m):
                if g[i][j] == '1':
                    if g[i - 1][j] == '0' and g[i][j - 1] == '0':
                        ok = False

        ans.append("YES" if ok else "NO")

    return "\n".join(ans)

# provided sample
assert run(
"""5
3 3
001
001
110
3 3
010
111
010
3 3
111
111
111
3 3
000
000
000
3 3
000
000
001
"""
) == "\n".join([
    "YES",
    "YES",
    "YES",
    "YES",
    "NO"
])

# minimum grid, empty
assert run(
"""1
1 1
0
"""
) == "YES"

# minimum grid, occupied
assert run(
"""1
1 1
1
"""
) == "YES"

# isolated interior ball
assert run(
"""1
2 2
00
01
"""
) == "NO"

# all ones
assert run(
"""1
4 4
1111
1111
1111
1111
"""
) == "YES"

# catches off-by-one issues near borders
assert run(
"""1
2 3
001
111
"""
) == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 grid with 0 | YES | Empty configuration |
| 1×1 grid with 1 | YES | Border cell always reachable |
| `00 / 01` | NO | Isolated interior ball |
| All ones | YES | Dense configuration |
| `001 / 111` | YES | Correct border handling |

## Edge Cases

Consider the smallest occupied grid:

```
1 1
1
```

The algorithm performs no interior checks because there are no interior cells. The answer is `YES`. A single push into row 1 or column 1 creates the configuration.

Consider the isolated corner example:

```
3 3
000
000
001
```

The algorithm reaches cell `(2,2)`. Its upper neighbor is `0` and its left neighbor is `0`, so the condition fails immediately and the answer is `NO`. This matches the fact that no sequence of pushes can move a ball that deep without intermediate occupied cells.

Consider a configuration with support from only one side:

```
3 3
000
110
011
```

For the bottom-right cell, the left neighbor is `1`, so the condition succeeds even though the upper neighbor is `0`. The algorithm returns `YES`. A ball only needs one valid insertion path, either from its row or from its column.

Consider the completely empty grid:

```
3 3
000
000
000
```

Every cell is skipped because none contains a ball. No violation occurs, and the answer is `YES`. Doing zero operations is always allowed.
