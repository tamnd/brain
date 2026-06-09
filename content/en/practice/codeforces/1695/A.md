---
title: "CF 1695A - Subrectangle Guess"
description: "We are given a grid containing distinct integers. Michael chooses dimensions h × w, then Joe secretly selects any subrectangle of exactly that size. Michael must name the maximum value inside Joe's chosen rectangle before seeing which rectangle was selected."
date: "2026-06-09T22:42:59+07:00"
tags: ["codeforces", "competitive-programming", "games"]
categories: ["algorithms"]
codeforces_contest: 1695
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 801 (Div. 2) and EPIC Institute of Technology Round"
rating: 800
weight: 1695
solve_time_s: 142
verified: true
draft: false
---

[CF 1695A - Subrectangle Guess](https://codeforces.com/problemset/problem/1695/A)

**Rating:** 800  
**Tags:** games  
**Solve time:** 2m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid containing distinct integers. Michael chooses dimensions `h × w`, then Joe secretly selects any subrectangle of exactly that size. Michael must name the maximum value inside Joe's chosen rectangle before seeing which rectangle was selected.

Since all values are distinct, the entire board has a unique global maximum. Michael can guarantee victory only if every possible `h × w` subrectangle contains that same cell. In that case, regardless of Joe's choice, the maximum inside the chosen rectangle is always the global maximum of the whole board.

The task is to find the smallest possible area `h · w` for which this guarantee is possible.

The dimensions satisfy `n, m ≤ 40`, which is tiny. Even algorithms that try all possible rectangle sizes are easily affordable. There are only `40 × 40 = 1600` possible `(h, w)` pairs per test case, so a direct mathematical solution is more than enough.

A subtle point is that Michael does not need to know which subrectangle Joe chose. He only needs a number that is guaranteed to be the maximum in every possible choice. Because all values are distinct, the only candidate is the global maximum of the entire board.

Consider this grid:

```
1 2
3 4
```

The maximum value `4` is in the bottom-right corner. Choosing `h = 1, w = 1` fails because Joe could select the cell containing `1`, whose maximum is not `4`.

The correct answer is `4`, obtained by choosing the whole board. A careless approach that only checks whether some rectangle contains the maximum would incorrectly return `1`.

Another easy mistake is forgetting that the maximum may lie on an edge.

```
5 1 2
3 4 0
```

The maximum is at position `(1,1)`. The answer is not determined by distance to the center. The rectangle dimensions must be large enough so that every possible placement includes the top-left corner.

## Approaches

The brute-force viewpoint starts by identifying the cell containing the global maximum. Suppose that cell is located at row `r` and column `c` using 1-based indexing.

For every pair `(h, w)`, we could enumerate all possible `h × w` subrectangles and check whether each one contains `(r, c)`. If yes, Michael wins with that choice. We then keep the minimum area.

This is correct because Michael wins exactly when every legal rectangle contains the global maximum cell. The problem is that for every size we would examine many rectangle positions. Although the constraints are small enough that this still passes, it hides the real structure of the problem.

The key observation is that we do not need to enumerate rectangles at all.

For a fixed height `h`, the starting row of a rectangle can be any value from `1` to `n - h + 1`.

For every such rectangle to contain row `r`, two conditions must hold simultaneously:

```
start_row ≤ r
start_row + h - 1 ≥ r
```

The most restrictive starting rows are the smallest possible one and the largest possible one.

The smallest start is `1`, which requires:

```
1 + h - 1 ≥ r
h ≥ r
```

The largest start is `n - h + 1`, which requires:

```
n - h + 1 ≤ r
h ≥ n - r + 1
```

Combining them gives:

```
h ≥ max(r, n - r + 1)
```

Exactly the same reasoning for columns gives:

```
w ≥ max(c, m - c + 1)
```

To minimize area, we choose the smallest valid height and width:

```
h = max(r, n - r + 1)
w = max(c, m - c + 1)
```

The answer is simply `h · w`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²m²) | O(1) | Too slow conceptually, unnecessary |
| Optimal | O(nm) | O(1) | Accepted |

## Algorithm Walkthrough

1. Scan the grid and locate the cell containing the global maximum value.
2. Let its position be `(r, c)` in 1-based indexing.
3. Compute the minimum height that forces every valid rectangle to contain row `r`:

```
h = max(r, n - r + 1)
```

This is the smallest height for which neither the topmost nor the bottommost placement can avoid row `r`.
4. Compute the minimum width that forces every valid rectangle to contain column `c`:

```
w = max(c, m - c + 1)
```
5. Output:

```
h × w
```

### Why it works

Every `h × w` rectangle contains the maximum cell if and only if every legal row interval of length `h` contains row `r` and every legal column interval of length `w` contains column `c`.

The smallest height satisfying this property is `max(r, n-r+1)`. Any smaller height allows either a top placement or a bottom placement that skips row `r`. The same argument holds for the width.

Since height and width are independent, choosing the minimum valid value for each dimension minimizes the area. Every resulting rectangle contains the global maximum cell, so its maximum value is always the same. Michael can always answer correctly.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n, m = map(int, input().split())

    mx = -10**18
    r = c = 0

    for i in range(1, n + 1):
        row = list(map(int, input().split()))
        for j in range(1, m + 1):
            if row[j - 1] > mx:
                mx = row[j - 1]
                r, c = i, j

    h = max(r, n - r + 1)
    w = max(c, m - c + 1)

    print(h * w)
```

The first loop reads the grid while simultaneously locating the global maximum. Since all values are distinct, the maximum cell is unique.

After finding its position `(r, c)`, the formula for the required height and width follows directly from the geometric argument developed above.

Using 1-based indices simplifies the formulas. The quantities `n - r + 1` and `m - c + 1` represent distances to the opposite borders measured inclusively. Taking the maximum chooses the farther side, which determines how large the rectangle must be to become unavoidable.

No additional arrays are needed beyond reading each row.

## Worked Examples

### Example 1

Input:

```
2 3
-7 5 2
0 8 -3
```

The maximum value is `8`.

| Variable | Value |
| --- | --- |
| n | 2 |
| m | 3 |
| r | 2 |
| c | 2 |
| h | max(2, 1) = 2 |
| w | max(2, 2) = 2 |
| Answer | 4 |

The resulting area is `2 × 2 = 4`.

Any `2 × 2` subrectangle must include row 2 and column 2, so it must contain the cell with value `8`.

### Example 2

Input:

```
4 4
2 12 6 10
3 15 16 4
1 13 8 11
14 7 9 5
```

The maximum value is `16`.

| Variable | Value |
| --- | --- |
| n | 4 |
| m | 4 |
| r | 2 |
| c | 3 |
| h | max(2, 3) = 3 |
| w | max(3, 2) = 3 |
| Answer | 9 |

The answer is `3 × 3 = 9`.

This example demonstrates that the optimal rectangle is not necessarily the whole board. It only needs to be large enough that every placement intersects the maximum cell.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | One scan of the grid to locate the maximum |
| Space | O(1) | Only a few variables are stored |

With `n, m ≤ 40`, at most 1600 cells are processed per test case. The solution runs comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n, m = map(int, input().split())

        mx = -10**18
        r = c = 0

        for i in range(1, n + 1):
            row = list(map(int, input().split()))
            for j in range(1, m + 1):
                if row[j - 1] > mx:
                    mx = row[j - 1]
                    r, c = i, j

        ans.append(str(max(r, n - r + 1) *
                       max(c, m - c + 1)))

    print("\n".join(ans))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = old_stdout
    return out.getvalue()

# provided sample
assert run("""3
1 1
3
4 4
2 12 6 10
3 15 16 4
1 13 8 11
14 7 9 5
2 3
-7 5 2
0 8 -3
""") == "1\n9\n4\n"

# minimum size
assert run("""1
1 1
42
""") == "1\n"

# maximum in top-left corner
assert run("""1
2 2
10 1
2 3
""") == "4\n"

# maximum in center of 3x3
assert run("""1
3 3
1 2 3
4 9 5
6 7 8
""") == "4\n"

# maximum in bottom-right corner
assert run("""1
3 4
1 2 3 4
5 6 7 8
9 10 11 12
""") == "12\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 grid | 1 | Smallest possible board |
| Maximum at top-left | 4 | Border position handling |
| Maximum at center of 3×3 | 4 | Interior maximum |
| Maximum at bottom-right | 12 | Opposite corner and inclusive distances |

## Edge Cases

Consider a board where the maximum is in a corner:

```
1
2 2
10 1
2 3
```

The maximum is at `(1,1)`.

The algorithm computes:

```
h = max(1, 2) = 2
w = max(1, 2) = 2
answer = 4
```

Any smaller dimension would allow a rectangle that avoids the corner entirely. The whole board is required.

Now consider a centered maximum:

```
1
3 3
1 2 3
4 9 5
6 7 8
```

The maximum is at `(2,2)`.

The algorithm computes:

```
h = max(2, 2) = 2
w = max(2, 2) = 2
answer = 4
```

Every `2 × 2` rectangle of a `3 × 3` board contains the center cell. A common mistake is assuming the answer must be `3 × 3 = 9`, but the center already becomes unavoidable with area `4`.

Finally, consider a single row:

```
1
1 5
1 2 10 3 4
```

The maximum is at column `3`.

The algorithm gives:

```
h = 1
w = max(3, 3) = 3
answer = 3
```

Every contiguous segment of length 3 in a row of length 5 contains the middle position. The formula naturally handles one-dimensional boards without any special cases.
