---
title: "CF 102740H - E. Gadd's Ghost Zapper"
description: "We have a long one-dimensional hallway. Some positions contain zapper devices, and some positions contain ghosts. A zapper can remove any ghost, but the energy cost depends on the square of the distance between them."
date: "2026-07-29T01:01:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102740
codeforces_index: "H"
codeforces_contest_name: "UTPC Contest 9-25-20 Div. 2"
rating: 0
weight: 102740
solve_time_s: 100
verified: true
draft: false
---

[CF 102740H - E. Gadd's Ghost Zapper](https://codeforces.com/problemset/problem/102740/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a long one-dimensional hallway. Some positions contain zapper devices, and some positions contain ghosts. A zapper can remove any ghost, but the energy cost depends on the square of the distance between them. Since all zappers can be used independently, every ghost should be handled by whichever zapper is closest to it. The required output is the sum of these minimum squared distances for every ghost, taken modulo (10^9+7).

The input gives the number of zappers and ghosts, followed by their positions along the hallway. Positions are integers and can be as large as (10^7), while both the number of zappers and ghosts can reach (10^5). With (10^5) ghosts and (10^5) zappers, checking every possible pair would require (10^{10}) distance calculations, which is far beyond what a two second limit allows. We need a solution close to (O((n+m)\log n)) or better.

The main edge cases come from the fact that the nearest zapper may not be the first one encountered, and distances can be zero. For example, if the input is:

```
1 1
5
5
```

the answer is `0` because the ghost is already on a zapper. A solution that only checks strictly smaller distances could accidentally miss this case.

Another case is when the ghost lies before the first zapper or after the last zapper:

```
2 2
10
20
0
30
```

The correct answer is `200`, because the ghost at position `0` is distance `10` from the first zapper and the ghost at position `30` is distance `10` from the second zapper. A solution that only searches between two zappers would fail because these ghosts have no zapper on both sides.

A third case is when two zappers are equally close:

```
2 1
4
10
7
```

The answer is `9`, because both zappers are distance `3` away and the cost is (3^2). Any tie-breaking choice is fine as long as the minimum distance is used.

## Approaches

The direct approach is to compare every ghost with every zapper. For each ghost position (x), we compute ((x-z_i)^2) for all zapper positions and keep the smallest value. This is correct because the zapper choices are independent, so each ghost can be optimized separately. However, with (10^5) ghosts and (10^5) zappers, the worst case performs (10^{10}) comparisons and distance computations, which is too slow.

The structure that makes this problem easier is that all objects lie on a line. After sorting the zapper positions, the closest zapper to a ghost must be one of the two zappers surrounding that ghost. Any zapper farther to the left than the nearest left neighbor is even farther away, and the same argument applies to the right side.

This reduces the problem to binary search. For each ghost, we find the first zapper whose position is at least the ghost position. That zapper is the closest candidate on the right. The previous zapper in the sorted array is the closest candidate on the left. We calculate the distance to both candidates when they exist and add the smaller squared distance.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Optimal | O((n+m) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort all zapper positions. The sorted order allows us to locate the closest possible neighbors of any ghost using binary search.
2. For each ghost position, find the insertion position of that ghost in the sorted zapper array. This index points to the first zapper whose position is not smaller than the ghost.
3. Check the zapper at that index if it exists. This is the closest zapper on the right side.
4. Check the zapper immediately before that index if it exists. This is the closest zapper on the left side.
5. Add the smaller of the available squared distances to the answer. Repeat this for every ghost and take the result modulo (10^9+7).

The reason only two zappers need to be checked is the ordering of the line. Suppose a ghost is between two zappers. Moving farther left from the closest left zapper only increases the distance, and moving farther right from the closest right zapper does the same. The same reasoning covers ghosts outside the range of all zappers.

Why it works: after sorting, the binary search position divides all zappers into those left of the ghost and those right of it. The closest element from each group is the only possible optimal choice. Every other zapper in the same group is farther away, so its squared distance cannot be smaller. Since the algorithm evaluates both possible closest neighbors, it always chooses the minimum energy cost for each ghost.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n, m = map(int, input().split())

    zappers = []
    for _ in range(n):
        zappers.append(int(input()))

    ghosts = []
    for _ in range(m):
        ghosts.append(int(input()))

    zappers.sort()

    ans = 0

    for x in ghosts:
        idx = bisect_left(zappers, x)

        best = None

        if idx < n:
            d = x - zappers[idx]
            best = d * d

        if idx > 0:
            d = x - zappers[idx - 1]
            cost = d * d
            if best is None or cost < best:
                best = cost

        ans = (ans + best) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The sorted zapper list is the only structure that needs to be stored because ghosts can be processed independently. The `bisect_left` call returns the first position where the ghost could be inserted without breaking sorting, which gives exactly the first zapper on the right.

The code checks the right candidate before the left candidate, but the order does not affect correctness. The boundary checks are necessary because the insertion position can be zero, meaning there is no left zapper, or it can equal `n`, meaning there is no right zapper.

The squared distance is computed using integers. Python handles large integers automatically, but taking the modulo after every addition keeps the accumulated answer bounded and follows the required output format.

## Worked Examples

For the first example:

```
4 4
4
1
11
7
2
9
6
15
```

After sorting, the zappers become `[1, 4, 7, 11]`.

| Ghost | Binary search index | Left candidate | Right candidate | Chosen cost | Running total |
| --- | --- | --- | --- | --- | --- |
| 2 | 1 | 1 | 4 | 1 | 1 |
| 9 | 3 | 7 | 11 | 4 | 5 |
| 6 | 2 | 4 | 7 | 1 | 6 |
| 15 | 4 | 11 | none | 16 | 22 |

The answer is `22`. The trace shows that every ghost only needs the two neighboring zappers after sorting.

For the second example:

```
2 4
10
5
7
0
5
100
```

The sorted zappers are `[5, 10]`.

| Ghost | Binary search index | Left candidate | Right candidate | Chosen cost | Running total |
| --- | --- | --- | --- | --- | --- |
| 7 | 1 | 5 | 10 | 4 | 4 |
| 0 | 0 | none | 5 | 25 | 29 |
| 5 | 0 | none | 5 | 0 | 29 |
| 100 | 2 | 10 | none | 8100 | 8129 |

The answer is `8129`. This example exercises both outside-range cases and the zero-distance case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+m) log n) | Sorting takes O(n log n), and every ghost performs one binary search |
| Space | O(n) | Only the sorted zapper positions are stored |

The constraints allow around a few million operations, but not billions. Sorting the zappers and performing binary searches keeps the work within the required range for (10^5) positions.

## Test Cases

```python
import sys
import io
from bisect import bisect_left

MOD = 10**9 + 7

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, m = map(int, input().split())
    zappers = [int(input()) for _ in range(n)]
    ghosts = [int(input()) for _ in range(m)]

    zappers.sort()
    ans = 0

    for x in ghosts:
        idx = bisect_left(zappers, x)
        best = None

        if idx < n:
            d = x - zappers[idx]
            best = d * d

        if idx > 0:
            d = x - zappers[idx - 1]
            cost = d * d
            if best is None or cost < best:
                best = cost

        ans = (ans + best) % MOD

    return str(ans)

assert solve("""4 4
4
1
11
7
2
9
6
15
""") == "22"

assert solve("""2 4
10
5
7
0
5
100
""") == "8129"

assert solve("""1 1
5
5
""") == "0"

assert solve("""2 2
10
20
0
30
""") == "200"

assert solve("""3 3
0
10000000
5000000
5000000
5000001
4999999
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single zapper and ghost at the same position | 0 | Zero distance handling |
| Ghosts outside both ends of the zapper range | 200 | Boundary binary search cases |
| Large coordinate range | 2 | Integer distance calculation and large values |
| Two equally close zappers | Correct minimum squared distance | Tie handling |

## Edge Cases

When a ghost is exactly on a zapper, the binary search finds that zapper as the right candidate. The calculated distance is zero, so the algorithm adds no energy. For:

```
1 1
5
5
```

the sorted zapper list is `[5]`, the search index is `0`, and the right candidate gives a cost of `0`.

When a ghost is before all zappers, the search index is `0`, so there is no left candidate. The algorithm uses the first zapper. For:

```
2 2
10
20
0
30
```

the ghost at `0` only checks the zapper at `10`, giving (10^2=100).

When a ghost is after all zappers, the search index becomes the length of the array. The algorithm skips the nonexistent right candidate and uses the final zapper. The ghost at `30` in the same example uses position `20`, also costing (10^2=100).

When a ghost is exactly between two zappers, both candidates are tested. For:

```
2 1
4
10
7
```

the costs are (3^2) and (3^2), so either choice gives the correct minimum of `9`.
