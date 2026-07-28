---
title: "CF 102741H - E. Gadd's Ghost Zapper"
description: "We have a set of zapper positions on a one dimensional hallway and a set of ghost positions on the same line. Each ghost must be removed by choosing one zapper. If a ghost is at distance d from the chosen zapper, the energy spent is d²."
date: "2026-07-29T00:47:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102741
codeforces_index: "H"
codeforces_contest_name: "UTPC Contest 9-25-20 Div. 1"
rating: 0
weight: 102741
solve_time_s: 61
verified: true
draft: false
---

[CF 102741H - E. Gadd's Ghost Zapper](https://codeforces.com/problemset/problem/102741/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a set of zapper positions on a one dimensional hallway and a set of ghost positions on the same line. Each ghost must be removed by choosing one zapper. If a ghost is at distance `d` from the chosen zapper, the energy spent is `d²`. The goal is to find the minimum total energy needed when every ghost is assigned to its cheapest possible zapper. The answer must be printed modulo `10^9 + 7`. The original problem constraints allow up to `10^5` zappers and `10^5` ghosts, with coordinates up to `10^7`.

The large input sizes immediately rule out checking every ghost against every zapper. A direct solution would perform `n * m` distance calculations. With both values equal to `100000`, that becomes `10^10` calculations, which is far beyond what a normal competitive programming time limit allows. We need to exploit the fact that all positions lie on a line.

The key structure is that the nearest zapper to a ghost must be one of the two zappers surrounding it after sorting. If a ghost lies between two neighboring zappers, moving farther away from either one only increases the distance. If the ghost lies outside the entire range of zappers, the closest zapper is simply the nearest endpoint. This means the problem can be reduced to sorting and binary searching.

Several edge cases can break an implementation that only considers the common case.

If a ghost is exactly on a zapper, the energy contribution is zero.

Example input:

```
2 1
5
10
5
```

The correct output is:

```
0
```

A careless solution that uses a strict comparison and ignores equality may incorrectly choose another zapper and add a positive cost.

If all zappers are on one side of every ghost, only the closest extreme zapper should be used.

Example input:

```
2 2
10
20
0
5
```

The correct output is:

```
125
```

The first ghost contributes `(10 - 0)² = 100` and the second contributes `(10 - 5)² = 25`. An implementation that assumes every ghost has a zapper on both sides may access invalid indices or compute the wrong neighbor.

Duplicate zapper positions are another case worth handling.

Example input:

```
3 2
7
7
7
7
8
```

The correct output is:

```
1
```

All duplicate zappers behave as a single location. A solution that tries to use unique positions is fine, but a solution that mishandles equal values during binary search can incorrectly skip the exact match.

## Approaches

The brute force solution is straightforward. For every ghost, iterate over every zapper, compute the squared distance, and keep the minimum. It is correct because every possible assignment for that ghost is examined.

The problem is the amount of work. With `n` zappers and `m` ghosts, this performs `n * m` comparisons and distance calculations. At the maximum input size, this reaches `10^10` operations, which is too slow.

The important observation is that the positions are one dimensional. After sorting the zapper locations, the closest zapper to a ghost is always found near the ghost's insertion point in the sorted array. We do not need to inspect all zappers.

For a ghost position `x`, binary search gives the first zapper whose position is at least `x`. This zapper is the closest candidate on the right. The previous zapper, if it exists, is the closest candidate on the left. Any other zapper on the right is farther than this first right candidate, and any other zapper on the left is farther than this first left candidate. We only need to compare those two.

The brute force works because it checks every possible zapper. The observation that only neighboring zappers matter reduces each ghost query from linear time to logarithmic time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Optimal | O(n log n + m log n) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Read all zapper positions and sort them.

Sorting creates an ordered structure where binary search can quickly locate the zappers around any ghost position.
2. For each ghost position, perform a binary search on the sorted zappers to find the first index `i` where `zappers[i] >= ghost`.

This divides the possible nearest zappers into two candidates. The zapper at index `i` is the closest possible one on the right, while the zapper at `i - 1` is the closest possible one on the left.
3. Check the valid candidates.

If `i` is inside the array, compute the cost using `zappers[i]`. If `i - 1` is nonnegative, compute the cost using `zappers[i - 1]`. Keep the smaller squared distance.
4. Add the minimum cost for this ghost to the running answer.

Apply the modulo after additions to keep the integer size manageable.

Why it works:

For any ghost position, consider the sorted zappers around it. Every zapper farther to the left than the immediate left neighbor has a greater distance, and every zapper farther to the right than the immediate right neighbor also has a greater distance. The nearest zapper must be one of those two neighbors. The algorithm always checks exactly those candidates, so every ghost receives the minimum possible energy cost. Summing those independent minimum costs gives the minimum total energy.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n, m = map(int, input().split())

    zappers = []
    for _ in range(n):
        zappers.append(int(input()))

    zappers.sort()

    ans = 0

    for _ in range(m):
        x = int(input())

        left = 0
        right = n

        while left < right:
            mid = (left + right) // 2
            if zappers[mid] >= x:
                right = mid
            else:
                left = mid + 1

        best = 10**30

        if left < n:
            d = zappers[left] - x
            best = d * d

        if left > 0:
            d = zappers[left - 1] - x
            best = min(best, d * d)

        ans = (ans + best) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The sorted list of zappers is the main data structure. The binary search implementation finds the lower bound, meaning the first position containing a value greater than or equal to the current ghost location.

The variable `left` after the search is not the left neighbor, it is the insertion position. If it equals `n`, there is no zapper on the right side. If it is zero, there is no zapper on the left side. These two boundary checks prevent invalid array access.

Python integers do not overflow, so the squared distances are safe even though a coordinate difference can be up to `10^7`. In languages with fixed width integers, the multiplication should be done using a wider type.

## Worked Examples

Sample 1:

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

The sorted zappers are `[1, 4, 7, 11]`.

| Ghost | Lower bound index | Candidates | Minimum cost | Running answer |
| --- | --- | --- | --- | --- |
| 2 | 1 | 4, 1 | 1 | 1 |
| 9 | 3 | 11, 7 | 4 | 5 |
| 6 | 2 | 7, 4 | 1 | 6 |
| 15 | 4 | 11 | 16 | 22 |

The trace shows why only two candidates are needed. For the ghost at position `9`, checking the zappers at `7` and `11` is enough because every other zapper is farther away.

Sample 2:

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

| Ghost | Lower bound index | Candidates | Minimum cost | Running answer |
| --- | --- | --- | --- | --- |
| 7 | 1 | 10, 5 | 4 | 4 |
| 0 | 0 | 5 | 25 | 29 |
| 5 | 0 | 5, none | 0 | 29 |
| 100 | 2 | 10 | 8100 | 8129 |

This example exercises both extremes. Ghosts outside the zapper range only have one valid nearest candidate.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m log n) | Sorting zappers costs O(n log n), and each of the m ghosts performs one binary search. |
| Space | O(n) | The sorted zapper positions are stored. |

The solution handles `10^5` zappers and `10^5` ghosts because the expensive work is performed once during sorting, followed by efficient logarithmic queries.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    data = inp.split()
    it = iter(data)

    n = int(next(it))
    m = int(next(it))

    zappers = [int(next(it)) for _ in range(n)]
    zappers.sort()

    ans = 0
    mod = 10**9 + 7

    for _ in range(m):
        x = int(next(it))

        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if zappers[mid] >= x:
                hi = mid
            else:
                lo = mid + 1

        best = 10**30

        if lo < n:
            d = zappers[lo] - x
            best = d * d

        if lo > 0:
            d = zappers[lo - 1] - x
            best = min(best, d * d)

        ans = (ans + best) % mod

    return str(ans) + "\n"

assert solve("""4 4
4
1
11
7
2
9
6
15
""") == "22\n", "sample 1"

assert solve("""2 4
10
5
7
0
5
100
""") == "8129\n", "sample 2"

assert solve("""1 1
0
0
""") == "0\n", "minimum size"

assert solve("""3 3
5
5
5
0
5
10
""") == "50\n", "all equal zappers"

assert solve("""2 3
10
20
0
5
30
""") == "250\n", "outside boundaries"

assert solve("""3 2
1
10000000
5000000
5000001
9999999
""") == "2\n", "large coordinates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single zapper and ghost at the same location | 0 | Exact match handling |
| Multiple identical zappers | 50 | Duplicate positions |
| Ghosts outside the zapper range | 250 | Left and right boundary cases |
| Large coordinate values | 2 | Correct squared distance handling |

## Edge Cases

For an exact match, such as:

```
2 1
5
10
5
```

the binary search returns the index of `5`. The algorithm compares that candidate and finds distance zero, so the contribution is zero.

For ghosts outside the available range:

```
2 2
10
20
0
5
```

the first ghost gets insertion index `0`, so only the zapper at `10` is checked. The second ghost also gets insertion index `0`, giving the correct costs `100` and `25`.

For duplicate zappers:

```
3 2
7
7
7
7
8
```

sorting keeps all copies together. The binary search finds one of the equal positions, and the distance calculation still returns the minimum value. The duplicates do not require any special handling because they represent identical choices.
