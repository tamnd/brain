---
title: "CF 106106B - \u041c\u0438\u0441\u0442\u0435\u0440 \u041c\u0438\u0441\u0438\u043a\u0441"
description: "We have a set of golf holes placed on a coordinate plane. A player starts the ball at a point suggested by a Meeseeks. The only allowed movement consists of two shots: first the ball can move only to the left, and then it can move only downward."
date: "2026-06-25T11:40:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106106
codeforces_index: "B"
codeforces_contest_name: "\u0423\u0440\u0430\u043b\u044c\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e \u042e\u043d\u0438\u043e\u0440\u044b 2024"
rating: 0
weight: 106106
solve_time_s: 36
verified: true
draft: false
---

[CF 106106B - \u041c\u0438\u0441\u0442\u0435\u0440 \u041c\u0438\u0441\u0438\u043a\u0441](https://codeforces.com/problemset/problem/106106/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a set of golf holes placed on a coordinate plane. A player starts the ball at a point suggested by a Meeseeks. The only allowed movement consists of two shots: first the ball can move only to the left, and then it can move only downward. The lengths of the two shots can be any non-negative values.

For a starting position `(a, b)`, the final position after these two shots can be any hole whose coordinates satisfy `x <= a` and `y <= b`. The order of the shots does not change this condition, because the first shot only decreases the x-coordinate and the second shot only decreases the y-coordinate.

The input gives up to `100000` holes and up to `100000` suggestions. For every suggestion we must answer whether at least one hole is reachable.

The bounds immediately rule out checking every suggestion against every hole. A direct solution would need up to `10^10` coordinate comparisons, which is far beyond what a typical two second limit allows. We need to preprocess the holes so each query can be answered in logarithmic time.

The main edge cases come from the direction of movement. A hole with a larger x-coordinate or a larger y-coordinate cannot be reached even if the other coordinate is suitable. For example:

```
Input
2
5 5
10 1
3
6 6
9 2
4 10
```

The first query should output `YES` because `(5,5)` is below and to the left of `(6,6)`. The second query should output `NO` because `(5,5)` has a smaller x-coordinate but the other hole `(10,1)` is too far right. A careless solution that only checks one coordinate would incorrectly accept it.

Another common mistake is forgetting that the starting point itself can be a valid destination. For example:

```
Input
1
7 4
1
7 4
```

The answer is `YES`, because both shot lengths can be zero. Solutions that require a strictly smaller coordinate fail on this case.

Duplicate holes are also possible. For example:

```
Input
3
2 3
2 3
5 1
1
2 3
```

The answer is `YES`. The duplicates do not change the logic, but an implementation that removes points incorrectly while preprocessing can accidentally lose valid information.

## Approaches

The brute-force approach is straightforward. For every suggestion `(a, b)`, scan all holes and check whether there exists a hole `(x, y)` with `x <= a` and `y <= b`. This is correct because it tests exactly the reachability condition. However, with `n` holes and `q` queries, the worst case performs `n * q` comparisons. With both values equal to `100000`, this becomes `10^10` operations, which is too slow.

The structure of the condition gives us the faster approach. Every query asks whether a point exists in the lower-left rectangle ending at `(a, b)`. Instead of searching this rectangle every time, we can preprocess the holes into a form where the answer is just a comparison.

Sort all holes by their x-coordinate. While moving from left to right, maintain the largest y-coordinate among all holes seen so far. For any possible x-boundary, this value tells us the highest hole that can still be reached horizontally. A query `(a, b)` only needs to know whether among holes with `x <= a` there is one with maximum y at least `b`.

This converts the problem into a prefix maximum query. After sorting the holes, we store arrays of x-coordinates and the corresponding maximum y-values. Each query uses binary search to find the last hole with `x <= a`, then checks the stored maximum y.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Optimal | O((n + q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort all holes by their x-coordinate. If two holes have the same x-coordinate, their relative order does not matter because they will all become part of the same prefix.
2. Build a prefix maximum array. For each position in the sorted holes, store the largest y-coordinate among all holes from the beginning up to that position. This value represents the highest reachable hole among all holes whose x-coordinate is not larger than the current x-coordinate.
3. For every Meeseeks suggestion `(a, b)`, use binary search on the sorted x-coordinates to find the last index containing a hole with `x <= a`. All holes after that index are impossible to reach because their x-coordinate is too large.
4. If no such index exists, there is no hole to the left of the starting point, so the answer is `NO`. Otherwise, compare the prefix maximum y-coordinate at that index with `b`. If it is at least `b`, some reachable hole exists and the answer is `YES`.

Why it works: after sorting by x, every prefix contains exactly the holes that satisfy the horizontal requirement. The stored maximum y in that prefix represents the best possible vertical position among those holes. If even the highest y is below the query's y-coordinate, every hole in the prefix is too low. If the maximum reaches the query's y-coordinate, that hole satisfies both coordinates and can be reached.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    holes = []

    for _ in range(n):
        x, y = map(int, input().split())
        holes.append((x, y))

    holes.sort()

    xs = []
    pref_y = []

    best = 0
    for x, y in holes:
        xs.append(x)
        best = max(best, y)
        pref_y.append(best)

    q = int(input())
    ans = []

    import bisect

    for _ in range(q):
        a, b = map(int, input().split())

        idx = bisect.bisect_right(xs, a) - 1

        if idx >= 0 and pref_y[idx] >= b:
            ans.append("YES")
        else:
            ans.append("NO")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The sorting step prepares the points for prefix processing. After sorting, every prefix ending at index `i` contains exactly the holes with x-coordinate at most `xs[i]`.

The `pref_y` array stores the strongest vertical option available for each prefix. Keeping only the maximum y is enough because a query does not care which hole provides it, only whether some hole reaches high enough.

For each query, `bisect_right` finds the first position where `a` could be inserted while keeping the x-array sorted. Subtracting one gives the last valid hole with `x <= a`. The comparison with `pref_y[idx]` handles the vertical requirement.

The binary search boundary is the easiest place to make a mistake. Using `bisect_right` instead of `bisect_left` is necessary because holes exactly on the starting x-coordinate are reachable.

## Worked Examples

Consider:

```
Input
3
1 3
3 1
4 4
5
1 3
4 2
2 1
2 2
3 3
```

After sorting, the holes are already ordered.

| Query | Last x <= a | Maximum y in prefix | Result |
| --- | --- | --- | --- |
| (1,3) | 0 | 3 | YES |
| (4,2) | 2 | 4 | YES |
| (2,1) | 0 | 3 | YES |
| (2,2) | 0 | 3 | YES |
| (3,3) | 1 | 3 | YES |

The prefix maximum shows that once a hole with high enough y has appeared, all later queries with larger x can still use it.

A query that exercises the impossible case:

```
Input
2
10 1
20 2
3
5 5
15 2
25 3
```

| Query | Last x <= a | Maximum y in prefix | Result |
| --- | --- | --- | --- |
| (5,5) | none | none | NO |
| (15,2) | 0 | 1 | NO |
| (25,3) | 1 | 2 | NO |

The trace demonstrates why both coordinates matter. Even though the first two queries have holes with smaller x-values, their y-values are not large enough.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | Sorting costs O(n log n), and each query uses one binary search. |
| Space | O(n) | The sorted coordinates and prefix maxima store information for all holes. |

The solution only performs a logarithmic amount of work per query, so `100000` holes and `100000` queries easily fit within the limits.

## Test Cases

```python
import sys
import io
import bisect

def solve(inp: str) -> str:
    data = io.StringIO(inp)
    input = data.readline

    n = int(input())
    holes = [tuple(map(int, input().split())) for _ in range(n)]

    holes.sort()

    xs = []
    pref = []
    best = 0

    for x, y in holes:
        xs.append(x)
        best = max(best, y)
        pref.append(best)

    q = int(input())
    res = []

    for _ in range(q):
        a, b = map(int, input().split())
        idx = bisect.bisect_right(xs, a) - 1
        res.append("YES" if idx >= 0 and pref[idx] >= b else "NO")

    return "\n".join(res)

assert solve("""3
1 3
3 1
4 4
5
1 3
4 2
2 1
2 2
3 3
""") == """YES
YES
YES
YES
YES"""

assert solve("""3
10 1
20 2
30 3
4
5 5
15 2
25 3
35 3
""") == """NO
NO
NO
YES"""

assert solve("""1
7 4
3
7 4
8 4
6 5
""") == """YES
YES
NO"""

assert solve("""4
2 3
2 3
5 1
10 10
4
2 3
5 2
9 9
11 11
""") == """YES
YES
NO
NO"""

assert solve("""5
1 1
2 2
3 3
4 4
5 5
3
0 0
5 5
3 4
""") == """NO
YES
NO"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| First sample-style case | All YES | Normal reachable queries |
| Increasing coordinates | Mixed answers | Checks x and y conditions together |
| Single hole | YES, YES, NO | Handles minimum size and zero-length shots |
| Duplicate holes | Correct duplicate handling | Prevents preprocessing mistakes |
| Diagonal points | Boundary failures | Catches incorrect inequality handling |

## Edge Cases

For the first edge case:

```
2
5 5
10 1
1
9 2
```

The algorithm sorts the holes and finds that only `(5,5)` belongs to the prefix with `x <= 9`. The maximum y in that prefix is `5`, which is at least `2`, so the answer is `YES`.

For the same data with query `(9,6)`, the prefix maximum is still `5`, but now it is below the required y-coordinate. The algorithm returns `NO`, correctly rejecting a point that is horizontally reachable but vertically too high.

For the zero-distance movement case:

```
1
7 4
1
7 4
```

Binary search finds the hole because `x <= a` is true when the values are equal. The prefix maximum y is also equal to `b`, so the answer is `YES`.

For duplicate holes:

```
3
2 3
2 3
5 1
1
2 3
```

Both copies of `(2,3)` appear at the beginning after sorting. The prefix maximum becomes `3`, and the query succeeds. The algorithm does not depend on uniqueness, so duplicates require no special handling.
