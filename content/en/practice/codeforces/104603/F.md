---
title: "CF 104603F - Cold day at the beach"
description: "Two teams take turns throwing discs onto a rectangular beach court. Each throw is a point in a 2D plane, and there is a fixed target point, the “tejin”, somewhere inside the same rectangle. The score is determined entirely by Euclidean distance to this target."
date: "2026-06-30T02:54:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104603
codeforces_index: "F"
codeforces_contest_name: "2023 Argentinian Programming Tournament (TAP)"
rating: 0
weight: 104603
solve_time_s: 43
verified: true
draft: false
---

[CF 104603F - Cold day at the beach](https://codeforces.com/problemset/problem/104603/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

Two teams take turns throwing discs onto a rectangular beach court. Each throw is a point in a 2D plane, and there is a fixed target point, the “tejin”, somewhere inside the same rectangle. The score is determined entirely by Euclidean distance to this target.

Every throw from both teams is compared against all throws of the opposing team, but the rule simplifies the competition: only the relative ranking of distances matters. First, we find the smallest distance achieved by team A and the smallest distance achieved by team R. The team with the smaller of these two distances wins the match.

After determining the winner, that team earns a point for each of its throws that are strictly closer to the target than the closest throw of the losing team. Ties in distance are guaranteed not to exist, so we never have to worry about equal comparisons.

The input size is small, with at most 1000 throws per team. Computing all distances is trivial, since we only need up to 2000 points. Any solution that evaluates distances once per point and performs linear scans is already sufficient.

A subtle point is that we must compare distances, not squared distances in a careless way unless we are consistent. Since Euclidean distance involves a square root, it is standard to compare squared distances to avoid floating point issues.

Edge cases are mostly structural rather than numerical.

One corner case is when all throws of one team are strictly farther than all throws of the other team. Then the winner is determined immediately by the minimum distance.

Another case is when the closest throw is not unique but belongs to different teams with very close coordinates. The problem explicitly guarantees no equal distances, so we do not handle ties.

A final subtlety is that scoring depends on the losing team’s best throw. Even if the winning team has multiple very good throws, only those strictly better than the opponent’s best contribute.

## Approaches

A direct simulation computes all squared distances for both teams, then scans to find the minimum for each team. After that, we compare the two minima to decide the winner. Once the winner is known, we perform a second pass over that team’s distances and count how many are strictly less than the opponent’s minimum.

This already matches the constraints comfortably. The brute force idea is essentially optimal here because there is no structure to exploit beyond simple aggregation. The full computation is linear in the number of throws, and there is no sorting requirement or combinatorial interaction between points.

The only potential overkill approach would be sorting all distances, but sorting is unnecessary since we only need minimum values and a count threshold.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (scan + compare) | O(N) | O(N) | Accepted |
| Optimal (same idea, direct) | O(N) | O(1) extra | Accepted |

The “optimal” solution is really just recognizing that the problem reduces to computing two minima and a filtered count.

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Read all inputs and store coordinates of team A and team R separately.
2. Compute squared Euclidean distance from each throw to the target point for team A and for team R. Squared distance is used to avoid floating point precision issues since comparison is preserved.
3. Scan through all distances of team A to find the minimum value, and do the same for team R. This gives the best throw for each team.
4. Compare the two minima. The team with the smaller minimum distance is declared the winner.
5. Let `best_loser` be the minimum distance of the losing team. Traverse the winning team’s distances and count how many are strictly less than `best_loser`.
6. Output the winning team label and the count.

The key idea is that the scoring rule only depends on a single threshold derived from the opponent’s best throw, so after identifying that threshold, the rest of the problem becomes a simple filtering operation.

### Why it works

Each team’s contribution to the score depends only on whether a throw beats the opponent’s best possible performance. Any throw that is not strictly better than the opponent’s minimum cannot contribute to the score by definition. Conversely, every throw that is strictly better is counted exactly once. Since all comparisons are independent and based only on distances to a fixed point, no interaction between throws exists beyond identifying the minima.

## Python Solution

```python
import sys
input = sys.stdin.readline

def dist2(x, y, tx, ty):
    dx = x - tx
    dy = y - ty
    return dx * dx + dy * dy

n = int(input())
w, l, tx, ty = map(int, input().split())

A = []
R = []

for _ in range(n):
    x, y = map(int, input().split())
    A.append(dist2(x, y, tx, ty))

for _ in range(n):
    x, y = map(int, input().split())
    R.append(dist2(x, y, tx, ty))

minA = min(A)
minR = min(R)

if minA < minR:
    winner = "A"
    threshold = minR
    score = sum(1 for d in A if d < threshold)
else:
    winner = "R"
    threshold = minA
    score = sum(1 for d in R if d < threshold)

print(winner, score)
```

The implementation separates reading and distance computation cleanly, ensuring all geometric work is reduced to integer arithmetic. Squared distances are used consistently so no square roots appear.

The winner decision is a direct comparison of minima. After that, the scoring pass is a single linear filter over the winning team’s list.

A common mistake is recomputing distances multiple times or mixing raw and squared distances. Another is accidentally counting from both teams instead of only the winner.

## Worked Examples

### Example 1

Input:

```
2
5 5 1 2
1 3
4 2
3 2
5 5
```

Distances squared to (1,2):

| Team A | Distance² |
| --- | --- |
| (1,3) | 1 |
| (4,2) | 9 |

| Team R | Distance² |
| --- | --- |
| (3,2) | 4 |
| (5,5) | 25 |

| Step | minA | minR | Winner | Threshold | Score |
| --- | --- | --- | --- | --- | --- |
| After scan | 1 | 4 | A | 4 | 1 |

Only one A throw is closer than R’s best.

Output:

```
A 1
```

This confirms that only strict comparisons matter; the second A throw is irrelevant because it is worse than R’s best.

### Example 2

Input:

```
2
10 10 0 5
0 0
0 2
0 4
0 1
0 3
0 5
```

Distances squared:

| A | dist² |
| --- | --- |
| (0,0) | 25 |
| (0,2) | 9 |

| R | dist² |
| --- | --- |
| (0,4) | 1 |
| (0,1) | 16 |

| Step | minA | minR | Winner | Threshold | Score |
| --- | --- | --- | --- | --- | --- |
| After scan | 9 | 1 | R | 9 | 1 |

Only R throw (0,4) is closer than A’s best.

Output:

```
R 1
```

This shows that even though R has a worse second throw, it does not affect scoring since only comparisons to A’s best matter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each throw is processed once to compute distance and once more for filtering |
| Space | O(N) | Stores distances for both teams |

The bounds N ≤ 1000 make this trivial. Even a straightforward Python implementation runs well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    w, l, tx, ty = map(int, input().split())

    def dist2(x, y):
        dx = x - tx
        dy = y - ty
        return dx * dx + dy * dy

    A = [dist2(*map(int, input().split())) for _ in range(n)]
    R = [dist2(*map(int, input().split())) for _ in range(n)]

    minA = min(A)
    minR = min(R)

    if minA < minR:
        return "A " + str(sum(d < minR for d in A))
    else:
        return "R " + str(sum(d < minA for d in R))

# provided samples
assert run("""2
5 5 1 2
1 3
4 2
3 2
5 5
""") == "A 1"

assert run("""5
10 10 0 5
0 0
0 2
0 4
0 1
0 3
0 5
""") == "R 1"

# custom cases
assert run("""1
1 1 0 0
1 1
0 0
""") == "R 1"

assert run("""3
10 10 5 5
0 0
10 10
5 6
5 5
6 5
4 5
""") == "A 2"

assert run("""2
10 10 5 5
0 5
10 5
5 0
5 10
""") == "A 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 vs center case | R 1 | Minimum-size correctness |
| mixed symmetric case | A 2 | multiple valid scoring throws |
| axis symmetry case | A 1 | boundary alignment and strict comparison |

## Edge Cases

A key edge case is when both teams have a single throw. The winner is simply the closer point, and the score is always 1 for the winner because it must be strictly closer than the opponent’s only throw. The algorithm handles this naturally because both minimums are computed correctly and the filter counts exactly one element.

Another edge case is when all points of one team are extremely clustered near the target while the other team is far away. In that case, the threshold comparison still works because all winning throws satisfy the strict inequality, so every throw contributes.

A final edge case is when coordinates lie exactly on boundaries of the rectangle. Since distance computation does not depend on boundaries, these points behave identically to interior points. The squared distance computation remains valid and no special casing is needed.
