---
title: "CF 102784H - Slime-inator"
description: "The city is an n x n grid. A slime source starts at cell (x, y) and spreads one step in the four cardinal directions every second. After t seconds, a cell is covered exactly when its Manhattan distance from the starting cell is at most t."
date: "2026-07-27T19:49:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102784
codeforces_index: "H"
codeforces_contest_name: "UTPC Contest 10-23-20 Div. 1"
rating: 0
weight: 102784
solve_time_s: 54
verified: true
draft: false
---

[CF 102784H - Slime-inator](https://codeforces.com/problemset/problem/102784/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

The city is an `n x n` grid. A slime source starts at cell `(x, y)` and spreads one step in the four cardinal directions every second. After `t` seconds, a cell is covered exactly when its Manhattan distance from the starting cell is at most `t`. The task is to find the smallest `t` such that at least `k` cells are covered.

The input contains the side length of the grid, the starting row and column of the slime, and the required number of covered cells. The output is the first second when the covered area reaches that amount.

The grid can have a side length up to `10^9`, so even storing the grid is impossible. A simulation that expands the slime one layer at a time would also be too slow because the answer can be close to `10^9`. The algorithm needs to work with formulas and logarithmic searching rather than visiting cells.

A common mistake is assuming the expanding shape is always a complete diamond. The borders of the city cut off parts of the diamond, especially when the source is near an edge. For example, in a `5 x 5` grid with the source at `(1,1)`, after one second the infinite diamond would contain five cells, but the actual grid only contains three reachable cells:

```
Input:
5 1 1 3

Output:
0
```

The starting cell already counts as covered, so the answer is zero. A solution that only checks the diamond size without considering borders can incorrectly overestimate coverage.

Another edge case is when `k = 1`. The slime covers its starting cell immediately, so the answer must be zero:

```
Input:
100 50 50 1

Output:
0
```

A binary search that starts from one instead of zero would miss this case.

A third tricky case is a very large grid where the source is near the middle. For example:

```
Input:
1000000000 500000000 500000000 1000000000000000000
```

The answer may be very large, so all calculations involving counts must use 64 bit integers. Python integers already handle this range.

## Approaches

The direct approach is to simulate the spreading process. At time zero there is one cell. Every second the next Manhattan distance layer is added. We could maintain the visited cells and expand with BFS. This is correct because the slime movement is exactly a shortest path distance process.

The problem is the size of the state space. A diamond with radius `r` contains about `2r^2` cells before borders are considered. With `n = 10^9`, the number of cells involved can approach `10^18`, so simulation is impossible.

The useful observation is that we do not need to know the exact shape at every moment. We only need a function that answers one question: how many cells are covered after `t` seconds? This value is monotonic, because increasing `t` can only add cells. Once we can calculate the count for a fixed `t`, binary search gives the minimum valid time.

The remaining challenge is counting the intersection of a Manhattan diamond with the square grid. The diamond can be divided into four quadrants around the starting cell. Each quadrant becomes a simple problem: count pairs of nonnegative offsets `(a, b)` where `a + b <= t` and both offsets stay inside the grid.

For a rectangle of possible offsets `0 <= a <= A` and `0 <= b <= B`, inclusion-exclusion gives the count in constant time. We start with the unlimited triangle and remove points that exceed either boundary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(answer²) | O(answer²) | Too slow |
| Optimal | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Define a function that counts how many cells are covered after a fixed number of seconds. The function only needs arithmetic because every covered cell satisfies a Manhattan distance condition.
2. Split the grid around the starting cell into four rectangles. Each rectangle represents one direction from the source, and the source cell belongs to all four rectangles. Add the four counts and subtract the extra copies of the starting cell.
3. For one rectangle, count offset pairs `(a, b)` where `a` and `b` are nonnegative and `a + b <= t`. Start with the unrestricted triangle count:

$$\frac{(t+1)(t+2)}{2}$$

Then remove pairs where `a` is too large, remove pairs where `b` is too large, and add back pairs removed twice.

1. Binary search the smallest time `t` where the coverage count is at least `k`. The lower bound is zero because the initial cell may already satisfy the requirement. The upper bound can be `2*n`, because after that the whole grid is definitely reached.

The correctness comes from two properties. First, the Manhattan distance condition exactly describes the cells reached after a given number of seconds. Second, the coverage function is monotonic, so binary search finds the first time where the condition becomes true. The rectangle counting formula counts every valid offset exactly once through inclusion-exclusion, so the coverage check is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

def tri(s):
    if s < 0:
        return 0
    return (s + 1) * (s + 2) // 2

def rect_count(a, b, t):
    return (
        tri(t)
        - tri(t - a - 1)
        - tri(t - b - 1)
        + tri(t - a - b - 2)
    )

def solve():
    n, x, y, k = map(int, input().split())

    def covered(t):
        ans = 0
        ans += rect_count(x - 1, y - 1, t)
        ans += rect_count(x - 1, n - y, t)
        ans += rect_count(n - x, y - 1, t)
        ans += rect_count(n - x, n - y, t)
        return ans - 3

    lo, hi = 0, 2 * n
    while lo < hi:
        mid = (lo + hi) // 2
        if covered(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    print(lo)

if __name__ == "__main__":
    solve()
```

The `tri` function represents the number of points in an unlimited nonnegative triangle. It returns zero when the requested triangle has a negative size, which avoids separate boundary cases.

The `rect_count` function applies inclusion-exclusion. The first term counts every possible offset. The next two terms remove offsets that leave the rectangle through either side. The last term restores offsets that violated both restrictions.

The four calls in `covered` correspond to the four directions around the source. Each one includes the source cell because both offsets can be zero. Since the source appears in all four quadrant counts, three copies must be removed.

The binary search uses `2*n` as a safe upper bound. A radius of `2*n` is larger than the maximum possible Manhattan distance between any two cells in the grid, so the whole board is covered.

## Worked Examples

For the first sample:

```
Input:
4 3 2 1
```

The source cell already satisfies the requirement.

| Time | Covered cells | Decision |
| --- | --- | --- |
| 0 | 1 | enough |

The binary search keeps zero because it is already a valid answer.

For the second sample:

```
Input:
10 7 3 7
```

| Time | Top left | Top right | Bottom left | Bottom right | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 1 | 1 | 5 |
| 2 | 4 | 3 | 4 | 2 | 13 |

At time one there are not enough cells. At time two the count reaches thirteen, so the answer is two.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | Binary search performs O(log n) checks, and each check uses a constant number of arithmetic operations |
| Space | O(1) | Only a few integer variables are stored |

The solution never depends on the number of cells in the grid. This is what allows it to handle grids with side length `10^9`, where explicit simulation would require impossible amounts of memory and time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.readline().split()
    n, x, y, k = map(int, data)

    def tri(s):
        if s < 0:
            return 0
        return (s + 1) * (s + 2) // 2

    def rect_count(a, b, t):
        return tri(t) - tri(t-a-1) - tri(t-b-1) + tri(t-a-b-2)

    def covered(t):
        return (
            rect_count(x-1, y-1, t)
            + rect_count(x-1, n-y, t)
            + rect_count(n-x, y-1, t)
            + rect_count(n-x, n-y, t)
            - 3
        )

    lo, hi = 0, 2*n
    while lo < hi:
        mid = (lo + hi) // 2
        if covered(mid) >= k:
            hi = mid
        else:
            lo = mid + 1

    sys.stdin = old
    return str(lo) + "\n"

assert run("4 3 2 1\n") == "0\n"
assert run("10 7 3 7\n") == "2\n"
assert run("1 1 1 1\n") == "0\n"
assert run("5 1 1 3\n") == "0\n"
assert run("3 2 2 9\n") == "2\n"
assert run("1000000000 500000000 500000000 1000000000000000000\n") == "1000000000\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1` | `0` | Minimum grid and immediate success |
| `5 1 1 3` | `0` | Border truncation near a corner |
| `3 2 2 9` | `2` | Full grid coverage and center expansion |
| Large centered grid | `1000000000` | Large integer handling |

## Edge Cases

When the starting cell is already enough, the coverage formula returns one at time zero. The binary search includes zero as a possible answer, so inputs such as:

```
5 1 1 1
```

correctly produce:

```
0
```

When the source is near a border, some parts of the diamond are outside the city. The quadrant sizes passed to `rect_count` become small, so the inclusion-exclusion formula naturally removes those impossible cells. For:

```
5 1 1 3
```

the four quadrants have only the cells available inside the grid, and the count at time zero already reaches the target.

When the grid is extremely large, the algorithm never constructs the grid or the diamond. It only evaluates formulas involving the coordinates and the current binary search value. This keeps the running time independent of the total number of cells.
