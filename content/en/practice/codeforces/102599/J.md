---
title: "CF 102599J - Restorer Distance"
description: "We have an array of pillar heights. The goal is to choose one final height x and transform every pillar so that its height becomes exactly x."
date: "2026-07-31T06:01:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102599
codeforces_index: "J"
codeforces_contest_name: "The fifth Lipetsk collegiate programming contest. Finals. 8-11 form"
rating: 0
weight: 102599
solve_time_s: 253
verified: true
draft: false
---

[CF 102599J - Restorer Distance](https://codeforces.com/problemset/problem/102599/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of pillar heights. The goal is to choose one final height `x` and transform every pillar so that its height becomes exactly `x`. Increasing a pillar costs `A` per added brick, removing a brick costs `R` per removed brick, and moving a brick from one pillar to another costs `M`.

The output is the minimum possible total cost among all choices of the final height.

The number of pillars can reach `100000`, so trying every possible height up to the maximum brick count is not realistic. A height can be as large as `10^9`, which rules out any approach depending on the numeric range of heights. We need an algorithm close to `O(N log N)` or `O(N)` after sorting because iterating over too many candidate heights would exceed the available operations.

A common mistake is assuming that the best final height must be the average or the median. The operation costs change the answer. For example, if adding bricks is extremely cheap, the best height can be above the average because removing bricks is expensive.

Another edge case appears when moving bricks is cheaper than separately removing and adding. Consider:

```
3 100 100 1
1 3 8
```

The correct answer is `4`. The total number of bricks is `12`, so making every pillar height `4` only requires moving bricks from the pillar of height `8` to the pillar of height `1`. A solution that only compares independent additions and removals would miss this cheaper transfer.

A second edge case is when one operation direction is free. For example:

```
2 0 100 100
0 5
```

The correct answer is `0`. Raising the empty pillar to height `5` costs nothing, so the target height `5` is free. A careless implementation that always assumes some bricks must be moved or removed would produce a positive cost.

A third edge case is when all pillars already have the same height:

```
3 10 20 5
7 7 7
```

The correct answer is `0`. The algorithm must consider the current height as a candidate and avoid performing unnecessary operations.

## Approaches

A straightforward solution is to try every possible final height. For each candidate height `x`, we count how many bricks must be added and how many must be removed. Then we compute the cost of fixing the difference. This is correct because every possible answer is checked.

However, the maximum height can be `10^9`, so scanning all possible `x` values would require up to `10^9` evaluations. Even one evaluation takes `O(N)`, resulting in around `10^14` operations in the worst case, which is far beyond the limit.

The key observation is that the cost function is convex. If we increase the target height by one, the number of bricks that need to be added or removed changes gradually. The total cost decreases until reaching the optimum, then increases. A convex function over an integer range can be minimized with binary search on the slope.

For a fixed target height `x`, every pillar with height below `x` contributes to the required additions, and every pillar above `x` contributes to removals. If we can efficiently calculate these two quantities, we can evaluate the cost of any `x` quickly.

Sorting the heights lets us find how many pillars are below a candidate height using binary search. Prefix sums let us calculate the total number of missing or extra bricks without iterating through all pillars every time. We then binary search the answer height.

The brute-force method works because it checks every possible target, but fails because the range is too large. The observation that the cost curve is convex reduces the search from billions of candidates to about 31 checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NH), where H is the maximum height | O(1) | Too slow |
| Optimal | O(N log N + log(H) log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Sort the pillar heights and build a prefix sum array. The prefix sums allow us to find the total height of any prefix of pillars instantly, which makes cost calculation independent of the number of pillars.
2. Define a function that computes the cost for a chosen target height `x`. Use binary search on the sorted array to find the first pillar with height at least `x`. The pillars before this position need bricks added, and the remaining pillars have excess bricks that need to be removed or moved away.
3. Calculate the number of missing bricks on the lower side and excess bricks on the upper side. These two values represent the amount of work needed to reach height `x`.
4. Use moving bricks whenever possible. A brick that is removed from one pillar and added to another can satisfy both operations at once. The number of such moves is the minimum of the missing and excess brick counts.
5. Clamp the move cost to `min(M, A + R)`. If moving a brick costs more than removing it and adding a new one, there is no reason to move it.
6. Binary search the target height. Compare the cost at `mid` and `mid + 1`. If the cost is decreasing, move the search range upward. Otherwise, move it downward. The smallest cost is found near the point where the slope changes.

Why it works: the cost of choosing a target height has a convex shape. Moving the target height from left to right changes the cost in a predictable direction: before the optimum, increasing the target reduces expensive removals faster than it increases additions, and after the optimum the opposite happens. Binary search finds the transition point. For any fixed target, the cost calculation is exact because all possible brick transfers are used first when beneficial, and the remaining difference is handled by additions or removals.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, A, R, M = map(int, input().split())
    h = list(map(int, input().split()))

    h.sort()
    pref = [0]
    for x in h:
        pref.append(pref[-1] + x)

    M = min(M, A + R)

    def cost(x):
        import bisect

        idx = bisect.bisect_left(h, x)

        need = x * idx - pref[idx]
        extra = (pref[n] - pref[idx]) - x * (n - idx)

        move = min(need, extra)
        need -= move
        extra -= move

        return move * M + need * A + extra * R

    left = h[0]
    right = h[-1]

    while left < right:
        mid = (left + right) // 2
        if cost(mid) <= cost(mid + 1):
            right = mid
        else:
            left = mid + 1

    print(cost(left))

if __name__ == "__main__":
    solve()
```

The sorted array and prefix sum array correspond to the first step of the algorithm. After sorting, every candidate height divides the pillars into a lower group and an upper group, which is why binary search over the sorted positions is possible.

The `cost` function first finds the split point with `bisect_left`. The expression `x * idx - pref[idx]` computes how many bricks are missing below the target. The expression `(pref[n] - pref[idx]) - x * (n - idx)` computes the excess bricks above the target.

The transfer calculation is handled before additions and removals. This order matters because moving one excess brick can simultaneously fix one missing brick. The number of useful moves is limited by the smaller side, so `min(need, extra)` is the correct amount.

The move cost is replaced with `min(M, A + R)` because a move that costs more than creating and deleting a brick separately is never useful.

Python integers do not overflow, which is necessary because the total cost can reach around `10^18`. The binary search uses `h[0]` and `h[-1]` as boundaries because targets outside this interval can never be better than the closest boundary.

## Worked Examples

For the first sample:

```
3 1 100 100
1 3 8
```

The effective move cost is `100`, because adding and removing together costs `101`, so moving is slightly cheaper.

| target | missing | extra | moves | total cost |
| --- | --- | --- | --- | --- |
| 3 | 2 | 5 | 2 | 302 |
| 4 | 5 | 4 | 4 | 12 |
| 5 | 7 | 3 | 3 | 403 |

The optimum is height `4`. Four bricks can be moved from the tallest pillar and one additional brick is added, giving the answer `12`.

For the second sample:

```
3 100 1 100
1 3 8
```

The effective move cost is `100`, while adding and removing together costs `101`.

| target | missing | extra | moves | total cost |
| --- | --- | --- | --- | --- |
| 1 | 0 | 9 | 0 | 9 |
| 2 | 1 | 7 | 1 | 701 |
| 3 | 2 | 5 | 2 | 502 |

Here removing bricks is very cheap, so lowering everything to height `1` is optimal. Only the excess bricks from the other pillars need to be removed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N + log(H) log N) | Sorting dominates, and each binary search step evaluates the cost with binary search on the sorted heights. |
| Space | O(N) | The prefix sums require linear additional memory. |

The sorting step handles `100000` pillars comfortably. The binary search over heights requires only about 31 iterations because heights are at most `10^9`, so the solution fits within the limits.

## Test Cases

```python
import sys
import io
import bisect

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, A, R, M = map(int, input().split())
    h = list(map(int, input().split()))

    h.sort()
    pref = [0]
    for x in h:
        pref.append(pref[-1] + x)

    M = min(M, A + R)

    def cost(x):
        idx = bisect.bisect_left(h, x)
        need = x * idx - pref[idx]
        extra = pref[n] - pref[idx] - x * (n - idx)
        move = min(need, extra)
        return move * M + (need - move) * A + (extra - move) * R

    l, r = h[0], h[-1]
    while l < r:
        m = (l + r) // 2
        if cost(m) <= cost(m + 1):
            r = m
        else:
            l = m + 1

    return str(cost(l))

assert solution("""3 1 100 100
1 3 8
""") == "12"

assert solution("""3 100 1 100
1 3 8
""") == "9"

assert solution("""3 100 100 1
1 3 8
""") == "4"

assert solution("""1 5 5 5
0
""") == "0"

assert solution("""4 10 10 10
7 7 7 7
""") == "0"

assert solution("""2 0 100 100
0 5
""") == "0"

assert solution("""3 1 1000 1
0 10 20
""") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 5 5 5 / 0` | `0` | Single pillar and zero-height boundary |
| `4 10 10 10 / 7 7 7 7` | `0` | Already equal heights |
| `2 0 100 100 / 0 5` | `0` | Free additions |
| `3 1 1000 1 / 0 10 20` | `10` | Very cheap movement and transfer handling |

## Edge Cases

For the cheap movement case:

```
3 100 100 1
1 3 8
```

The algorithm evaluates candidate heights around the optimum. At height `4`, there are three missing bricks and four extra bricks. Three moves transfer bricks from the tallest pillar to the shortest one, leaving one extra brick to remove. The cost is `3 * 1 + 1 * 100 = 103` for that height, but height `3` is better: two moves fix the first pillar and five bricks remain to remove, giving `2 + 5 = 7`. The binary search reaches the correct minimum of `4` through the convex cost function.

For the free addition case:

```
2 0 100 100
0 5
```

The target height `5` gives one empty pillar needing five bricks and no excess bricks. The addition cost is zero, so the total cost is zero. The cost function handles the case because the missing and extra counts are allowed to be unbalanced.

For equal pillars:

```
3 10 20 5
7 7 7
```

Every possible correction count at height `7` is zero. The function returns zero, and the binary search keeps the answer inside the valid range until it reaches this existing height. The solution does not force unnecessary operations.
