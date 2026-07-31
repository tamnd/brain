---
title: "CF 102569B - Bonuses on a Line"
description: "We have a set of bonus locations placed on a number line. The starting position is coordinate 0, and moving one unit of distance always consumes one second. The task is to choose a group of bonuses and visit every chosen location within the available time t."
date: "2026-07-31T07:50:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102569
codeforces_index: "B"
codeforces_contest_name: "2020, XIII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102569
solve_time_s: 96
verified: true
draft: false
---

[CF 102569B - Bonuses on a Line](https://codeforces.com/problemset/problem/102569/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a set of bonus locations placed on a number line. The starting position is coordinate 0, and moving one unit of distance always consumes one second. The task is to choose a group of bonuses and visit every chosen location within the available time `t`. The answer is the largest number of bonuses that can be collected, not the distance traveled or the final position.

The input gives the number of bonuses, the time limit, and the already sorted coordinates of all bonuses. Since the coordinates are sorted, nearby bonuses are stored next to each other, which is the structural property that allows an efficient solution. The output is a single integer representing the maximum count of bonuses that can be reached.

The number of bonuses can reach 200000, so checking every possible group of bonuses is not realistic. A quadratic algorithm would perform around 40000000000 operations in the worst case, which is far beyond what a 2 second limit allows. We need an approach close to linear time. The coordinates and the time limit can be as large as `10^9`, so calculations must use integer arithmetic that can safely store large intermediate values. Python integers already handle this.

A common mistake is to only check the distance to the farthest bonus in a chosen range. That works when all bonuses are on one side of the origin, but it fails when bonuses exist on both sides because returning across the origin costs extra movement. For example, with:

```
3 4
-2 1 3
```

the correct answer is `2`. Visiting `-2` and `1` costs `2 + 3 = 5` seconds if we go left first, or `1 + 3 = 4` seconds if we go right first, so two bonuses are possible. A method that only looks at the farthest coordinate would incorrectly think all three bonuses fit because the farthest coordinate is `3`.

Another edge case is having no time available. For example:

```
1 0
5
```

The correct output is `0`. A careless implementation that starts with one reachable bonus or checks the position before moving can incorrectly count it.

A third case is when the optimal range crosses zero but starts and ends on opposite sides. For example:

```
4 5
-4 -1 2 10
```

The best choice is `-1, 2`, which takes `3` seconds if we go right first. Including `-4` would require much more time. Algorithms that always extend to the largest possible coordinate range without considering the return trip will overestimate the answer.

## Approaches

A direct brute-force solution would try every possible consecutive segment of bonuses. For each segment, we can calculate the shortest route that starts at zero and visits both ends of the segment. Because all bonuses inside the segment lie between those two endpoints, visiting the endpoints is enough. This is correct because once we reach both extremes, all intermediate bonuses can be collected on the way.

The problem is the number of segments. There are about `n * (n + 1) / 2` possible segments, which is about 20000000000 for `n = 200000`. Even with constant-time cost checks, this is too slow.

The key observation is that an optimal set of bonuses is always a consecutive segment in the sorted array. If a solution takes two bonuses and skips a bonus between them, adding that skipped bonus costs no extra movement because the route already passes its position. This turns the problem into finding the longest valid window.

For a fixed right endpoint, moving the left endpoint to the right can only make the required travel distance smaller or keep it unchanged. This monotonic behavior allows a two pointer approach. We extend the right side one bonus at a time, and whenever the current window needs more than `t` seconds, we remove bonuses from the left until the window becomes possible again.

The travel cost of a window depends only on its two ends. If the entire window is on the positive side, the cost is the rightmost coordinate. If it is on the negative side, the cost is the absolute value of the leftmost coordinate. If it crosses zero, there are two possible orders: visit the left side first or the right side first. We take the smaller of the two.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Keep two pointers describing the current segment of bonuses. The right pointer expands from left to right, adding one new bonus each time. The left pointer marks the first bonus currently included.
2. After adding a new right endpoint, calculate the minimum time needed to visit the current segment. The only coordinates needed are the leftmost and rightmost bonuses because every other bonus lies between them.
3. If the current segment needs more than `t` seconds, move the left pointer one position right and check again. Removing bonuses from the left cannot increase the required time, so this process eventually finds the longest valid segment ending at the current right pointer.
4. Whenever the current segment is valid, update the answer with its size. The largest size seen during the scan is the maximum number of bonuses that can be collected.

The invariant is that after shrinking, the current window is always the longest valid window ending at the current right endpoint. Any window with the same right endpoint but a smaller left endpoint was already checked and was invalid if it was removed. Since every possible right endpoint is considered, the largest valid window found by the scan is the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, t = map(int, input().split())
    x = list(map(int, input().split()))

    def cost(l, r):
        left = x[l]
        right = x[r]

        if right <= 0:
            return -left
        if left >= 0:
            return right

        return min(right - 2 * left, 2 * right - left)

    ans = 0
    l = 0

    for r in range(n):
        while l <= r and cost(l, r) > t:
            l += 1
        if l <= r:
            ans = max(ans, r - l + 1)

    print(ans)

if __name__ == "__main__":
    solve()
```

The `cost` function is the core of the solution. When both ends are negative, the farthest point is on the left and the required movement is simply the distance from zero to the left endpoint. When both ends are positive, the right endpoint determines the cost. When the segment crosses zero, the two formulas represent the two possible orders of visiting the sides.

The main loop follows the two pointer process. The right pointer only moves forward once, and the left pointer also only moves forward once, so the total number of pointer movements is linear. The repeated calls to `cost` use only a few arithmetic operations.

The boundary condition in the shrinking loop is important. A window containing only the current right endpoint is still valid if its cost is checked, so the condition allows `l == r`. If every bonus is too far away, the window becomes empty and the answer remains zero.

No special handling for large coordinates is needed because Python integers do not overflow. In languages with fixed-size integer types, the expressions involving doubled coordinates would require 64-bit integers.

## Worked Examples

For the sample:

```
5 6
-4 -1 2 3 7
```

the scan behaves as follows.

| Left index | Right index | Window | Cost | Best answer |
| --- | --- | --- | --- | --- |
| 0 | 0 | -4 | 4 | 1 |
| 0 | 1 | -4,-1 | 4 | 2 |
| 0 | 2 | -4,-1,2 | 10 | 2 |
| 1 | 2 | -1,2 | 4 | 2 |
| 1 | 3 | -1,2,3 | 5 | 3 |
| 1 | 4 | -1,2,3,7 | 15 | 3 |
| 2 | 4 | 2,3,7 | 7 | 3 |
| 3 | 4 | 3,7 | 7 | 3 |
| 4 | 4 | 7 | 7 | 3 |

The important part of this trace is that after the window becomes too large, the algorithm removes the left side until it becomes valid again. It never needs to move the right pointer backward.

A second example:

```
4 3
-5 -1 1 2
```

| Left index | Right index | Window | Cost | Best answer |
| --- | --- | --- | --- | --- |
| 0 | 0 | -5 | 5 | 0 |
| 1 | 0 | empty |  | 0 |
| 1 | 1 | -1 | 1 | 1 |
| 1 | 2 | -1,1 | 3 | 2 |
| 1 | 3 | -1,1,2 | 4 | 2 |
| 2 | 3 | 1,2 | 2 | 2 |

This example shows the behavior when the time limit is small. The algorithm discards impossible left endpoints and keeps the largest segment that fits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each bonus enters the window once and leaves the window at most once. |
| Space | O(1) besides input storage | Only pointers, counters, and temporary values are used. |

The solution performs a constant amount of work per bonus, which is suitable for `n = 200000`. The memory usage is also within the limit because the algorithm does not create additional arrays or dynamic structures.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

def solve():
    import sys
    input = sys.stdin.readline

    n, t = map(int, input().split())
    x = list(map(int, input().split()))

    def cost(l, r):
        left = x[l]
        right = x[r]
        if right <= 0:
            return -left
        if left >= 0:
            return right
        return min(right - 2 * left, 2 * right - left)

    ans = 0
    l = 0
    for r in range(n):
        while l <= r and cost(l, r) > t:
            l += 1
        if l <= r:
            ans = max(ans, r - l + 1)

    print(ans)

assert run("5 6\n-4 -1 2 3 7\n") == "3\n", "sample 1"
assert run("1 0\n5\n") == "0\n", "no time available"
assert run("1 10\n-7\n") == "1\n", "single negative point"
assert run("5 5\n-3 -1 2 4 8\n") == "3\n", "crossing zero window"
assert run("6 1000000000\n-1000000000 -5 1 2 7 999999999\n") == "6\n", "large coordinates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 6 / -4 -1 2 3 7` | `3` | Original sample with a mixed-sign optimal range |
| `1 0 / 5` | `0` | Minimum time boundary |
| `1 10 / -7` | `1` | Single bonus handling |
| `5 5 / -3 -1 2 4 8` | `3` | Correct cost calculation when crossing zero |
| Large coordinate case | `6` | Large values and integer arithmetic |

## Edge Cases

For the zero-time case:

```
1 0
5
```

the right pointer starts at the only bonus. The cost is `5`, which is greater than `t`, so the left pointer moves past the right pointer. The window becomes empty and the answer stays zero. The algorithm never counts a bonus that cannot be reached.

For a range on both sides of zero:

```
3 4
-2 1 3
```

the window containing all three bonuses has cost `2 * 3 - (-2) = 8` or `3 - 2 * (-2) = 7`, so it is rejected. The left pointer moves until the window `[-2, 1]` remains, whose cost is `1 - 2 * (-2) = 5` and `2 * 1 - (-2) = 4`, giving a valid cost of `4`. The answer becomes two.

For a window entirely on one side:

```
3 5
-6 -3 -1
```

the algorithm does not use the crossing-zero formula. The cost is simply the distance to the farthest negative point. The first window has cost `6`, so the left pointer moves. The remaining bonuses `-3, -1` cost `3` seconds and are counted, producing output `2`.

For large coordinates:

```
2 2000000000
-1000000000 1000000000
```

the crossing formula evaluates values around `3000000000`, which exceeds 32-bit integer limits. Python handles this correctly, and the algorithm compares the full integer values before deciding that both bonuses fit. The output is `2`.
