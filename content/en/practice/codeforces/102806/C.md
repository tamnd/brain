---
title: "CF 102806C - \u041d\u043e\u0432\u044b\u0439 \u043a\u043e\u0440\u0430\u0431\u043b\u044c"
description: "We have a rectangular planet divided into cells. Some cells are available for construction and some are blocked. The goal is to build the largest possible ship."
date: "2026-07-26T16:16:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102806
codeforces_index: "C"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2017-2018, \u0427\u0435\u0442\u0432\u0451\u0440\u0442\u0430\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102806
solve_time_s: 61
verified: true
draft: false
---

[CF 102806C - \u041d\u043e\u0432\u044b\u0439 \u043a\u043e\u0440\u0430\u0431\u043b\u044c](https://codeforces.com/problemset/problem/102806/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rectangular planet divided into cells. Some cells are available for construction and some are blocked. The goal is to build the largest possible ship. The ship has the shape of a cross made from five equal squares: one square in the center and one square attached to each of its four sides. If the side length of each square is `k`, the whole cross occupies a `3k × 3k` area, but only the central row block and central column block of that area must be usable.

The input gives the height and width of the grid followed by the grid itself. A `#` cell can be used for construction, while a `.` cell cannot. The output is the maximum value of `k` for which some placement of this cross exists. The statement guarantees that a ship of size at least `1` can always be built.

The grid dimensions can reach `2000 × 2000`, giving up to four million cells. A solution that tries every possible center and expands the cross one layer at a time can approach billions of operations, which is too much for a typical one second limit. We need a method close to linear or near linear in the number of cells. Since the answer is at most `min(n, m) / 3`, a logarithmic factor from binary search is acceptable.

The tricky cases are mostly related to the geometry of the cross. A ship of size `k` is not just a normal `k × k` square, so checking only the center square gives incorrect answers. For example:

```
3 9
...###...
...###...
#########
```

The correct answer is `1`, because the middle row is usable but the vertical part cannot have height `3`. A careless solution that checks only whether there is a `3 × 3` block somewhere would fail.

Another edge case is when the cross touches the border. For example:

```
5 5
..#..
.###.
#####
.###.
..#..
```

The correct answer is `1`. The center square can be placed, but there is not enough space for a larger cross. Implementations that assume the center of a candidate cross must have `k` empty rows and columns around it can accidentally skip valid border placements.

A final common mistake is confusing the size of the whole figure with the size of one square. For a ship of size `k`, the total bounding box is `3k × 3k`, not `k × k`.

## Approaches

The direct approach is to try every possible value of `k`, every possible center position, and check all five squares of the cross. This is correct because the ship definition is exactly the union of those five squares. However, checking a single candidate cross costs `O(k²)`, and there can be `O(nm)` possible centers and `O(min(n,m))` possible sizes. In the worst case this becomes far too large.

The key observation is that for a fixed `k`, we do not need to inspect every cell of every candidate. We only need to answer whether a certain `k × k` square is completely buildable. This can be done in constant time with a two-dimensional prefix sum.

Once we can check a fixed `k`, we can binary search the answer. If a cross of size `k` exists, every smaller size can also be built by taking the central part of that cross. This monotonic property means that the set of possible answers looks like `true, true, ..., true, false, false, ...`, which is exactly what binary search requires.

The brute-force works because it checks the definition directly, but fails because it repeats almost the same area checks many times. Prefix sums remove the repeated work, and binary search removes the need to test every possible size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm · min(n,m)³) in the worst case | O(1) | Too slow |
| Binary Search + Prefix Sums | O(nm log(min(n,m))) | O(nm) | Accepted |

## Algorithm Walkthrough

1. Build a two-dimensional prefix sum array where each position stores the number of usable cells in the rectangle from the top-left corner to that position.

The prefix sum lets us query how many blocked cells are inside any rectangle in constant time. A rectangle is valid for construction exactly when its count of usable cells equals its area.

1. Binary search the side length `k` of one square in the cross.

The lower bound starts at `1` because a solution is guaranteed to exist. The upper bound is `min(n, m) // 3`, because the whole cross occupies three such squares in both dimensions.

1. For a candidate `k`, scan all possible positions of the central `k × k` square.

The center square must have four neighboring `k × k` squares: above, below, left, and right. If all five rectangles contain only usable cells, then a cross of size `k` exists.

1. If the check succeeds, move the binary search upward. Otherwise, move it downward.

A larger cross contains all the requirements of a smaller cross, so failure for one size means every larger size also fails.

1. After binary search finishes, output the largest successful value.

### Why it works

For every tested size `k`, the checking procedure examines exactly the five squares that define a valid ship. The prefix sums give the exact number of usable cells in each square, so a square is accepted if and only if every cell inside it is available.

The binary search is correct because the predicate "a cross of size `k` exists" is monotonic. If a cross of size `k` exists, taking the inner `k' × k'` parts for any smaller `k'` creates a smaller valid cross. If a size fails, no larger size can fit because every larger cross would contain a smaller invalid requirement. Therefore binary search finds the maximum possible size.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    pref = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n):
        row_sum = 0
        for j in range(m):
            if grid[i][j] == '#':
                row_sum += 1
            pref[i + 1][j + 1] = pref[i][j + 1] + row_sum

    def rect_sum(r1, c1, r2, c2):
        return pref[r2][c2] - pref[r1][c2] - pref[r2][c1] + pref[r1][c1]

    def good_square(r, c, k):
        return rect_sum(r, c, r + k, c + k) == k * k

    def check(k):
        for r in range(n - 3 * k + 1):
            for c in range(m - 3 * k + 1):
                if good_square(r, c + k, k):
                    if (good_square(r + k, c, k) and
                        good_square(r + k, c + k, k) and
                        good_square(r + k, c + 2 * k, k) and
                        good_square(r + 2 * k, c + k, k)):
                        return True
        return False

    lo, hi = 1, min(n, m) // 3
    ans = 1

    while lo <= hi:
        mid = (lo + hi) // 2
        if check(mid):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The prefix construction stores counts only for usable cells. This makes the rectangle query independent of the rectangle size, which is the main optimization over checking every cell repeatedly.

The `good_square` function compares the number of usable cells in a candidate square with `k * k`. If they are equal, every cell in that square is available.

The `check` function only iterates over positions where a complete `3k × 3k` bounding box fits. The five calls correspond directly to the five blocks of the cross. Keeping the center square at `(r + k, c + k)` avoids off-by-one errors because the surrounding blocks are naturally offset by exactly `k`.

Python integers do not overflow here, but the multiplication `k * k` is still kept as an integer expression because the prefix values represent cell counts.

## Worked Examples

For the first sample:

```
9 12
...##.###...
...##.###...
.########...
.###########
...#########
...#########
......###...
......###...
......###...
```

A successful placement of size `3` exists.

| Candidate size | Position checked | Result |
| --- | --- | --- |
| 5 | All possible centers | No valid cross |
| 3 | Center block around row 4, column 4 | Valid |
| 4 | All possible centers | No valid cross |

The trace shows why binary search works. Size `3` is possible, but size `4` is not, so the maximum answer is `3`.

For the second sample:

```
6 6
.##...
.##...
######
######
.##...
.##...
```

The largest possible cross has size `1`.

| Candidate size | Position checked | Result |
| --- | --- | --- |
| 1 | Several centers | Valid |
| 2 | All possible centers | Invalid |

The example demonstrates that a large connected area is not enough. The exact five-square shape is required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm log(min(n,m))) | Each binary search step scans the grid and performs constant-time rectangle queries |
| Space | O(nm) | The prefix sum array stores one value per grid cell |

The largest grid has four million cells. The logarithmic number of binary search iterations is small, around eleven for this limit, so the solution stays within the intended limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.getvalue()

assert run("""9 12
...##.###...
...##.###...
.########...
.###########
...#########
...#########
......###...
......###...
......###...
""") == "3\n", "sample 1"

assert run("""6 6
.##...
.##...
######
######
.##...
.##...
""") == "1\n", "sample 2"

assert run("""1 1
#
""") == "1\n", "single cell"

assert run("""3 3
###
###
###
""") == "1\n", "minimum cross"

assert run("""9 9
...###...
...###...
...###...
#########
#########
#########
...###...
...###...
...###...
""") == "3\n", "perfect large cross"

assert run("""9 9
#########
#########
#########
#########
#########
#########
#########
#########
#########
""") == "3\n", "all cells usable"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 × 1` usable grid | `1` | Minimum dimensions |
| Full `3 × 3` grid | `1` | Smallest valid cross |
| Perfect `9 × 9` cross | `3` | Maximum size for a prepared shape |
| Entire grid usable | `3` | Upper bound handling |
| Sample layouts | Sample answers | General correctness |

## Edge Cases

For the border case:

```
5 5
..#..
.###.
#####
.###.
..#..
```

The binary search first tries larger values, but `check(1)` is the only successful call. When checking size `2`, every possible `4 × 4` bounding box requires a missing cell, so the answer remains `1`.

For the false-square case:

```
3 9
...###...
...###...
#########
```

The prefix sums correctly reject a vertical square of size `3`. Although there is a large horizontal region, the four side squares of the cross are not all present, so the algorithm returns `1`.

For the maximum-size situation:

```
9 9
...###...
...###...
...###...
#########
#########
#########
...###...
...###...
...###...
```

The check for `k = 3` finds the five valid `3 × 3` blocks. The next binary search attempt with a larger size fails because the bounding box would exceed the available structure. The returned answer is exactly `3`.
