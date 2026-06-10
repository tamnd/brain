---
title: "CF 1450B - Balls of Steel"
description: "We are given several steel balls placed at distinct coordinates on a plane. A charged ball acts like a magnet with radius measured in Manhattan distance."
date: "2026-06-11T03:47:30+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "geometry", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1450
codeforces_index: "B"
codeforces_contest_name: "Codeforces Global Round 12"
rating: 1000
weight: 1450
solve_time_s: 709
verified: true
draft: false
---

[CF 1450B - Balls of Steel](https://codeforces.com/problemset/problem/1450/B)

**Rating:** 1000  
**Tags:** brute force, geometry, greedy  
**Solve time:** 11m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several steel balls placed at distinct coordinates on a plane. A charged ball acts like a magnet with radius measured in Manhattan distance. When we charge a ball, every ball whose Manhattan distance from it is at most `k` instantly moves onto the charged ball's position.

The goal is to make all balls occupy one position. We may perform any number of charging operations. For each test case we must determine the minimum number of operations required, or report that it cannot be done.

The constraints are unusually small. Each test case contains at most 100 points, and there are at most 100 test cases. Even an `O(n²)` or `O(n³)` solution is easily fast enough. With `n = 100`, an `O(n²)` algorithm performs only 10,000 distance checks per test case.

The first edge case is when all points already lie within distance `k` of some point. For example:

```
3 3
6 7
8 8
6 9
```

Every point is within distance 3 of every other point. Charging any ball gathers all balls immediately, so the answer is `1`, not `0`. The problem asks for the minimum number of operations needed to make all balls coincide, and initially they are distinct.

Another subtle case occurs when points form a connected chain but no single point can reach all others:

```
4 1
0 0
0 1
0 2
0 3
```

Each point is close to its neighbors, but there is no point whose distance to every other point is at most 1. A careless solution might assume repeated operations can gradually merge everything. They cannot. The correct answer is `-1`.

A third edge case is `k = 0`. Since all coordinates are distinct, no ball can attract any other ball. The answer is always `-1`.

## Approaches

A brute-force simulation would try sequences of charging operations and track how points move. Such a search quickly becomes complicated because the state changes after every operation, and the number of possible sequences grows exponentially.

The key observation is that the answer is never greater than one.

Suppose all balls eventually end up at some position. That final position must be one of the original ball locations. Balls never create new coordinates. Every movement copies the position of a charged ball.

Consider the last operation in a successful sequence. At that moment, every remaining ball must move onto the charged ball's position. Therefore every ball must already be within distance `k` of that charged ball.

Since moving balls only changes their positions to existing ball positions, if some original ball can attract every other original ball directly, then one operation is enough. If no such ball exists, no sequence of operations can create one later.

This reduces the entire problem to checking whether there exists a point whose Manhattan distance to every other point is at most `k`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| State-space simulation | Exponential | Exponential | Too slow |
| Check every candidate center | O(n²) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read all points of the test case.
2. For every point `i`, treat it as a possible gathering point.
3. Compute the Manhattan distance from point `i` to every other point.
4. If all distances are at most `k`, then charging point `i` gathers all balls in a single operation. Output `1`.
5. If no point satisfies this condition, output `-1`.

### Why it works

Assume a successful sequence exists. Look at the final operation. The charged ball has some position `P`, which is one of the original ball coordinates. Every ball that becomes part of the final merged position must be within distance `k` of `P` at that moment.

Since all positions throughout the process are copied from original ball locations, the final gathering point must correspond to an original point. If that original point cannot directly attract some other original point, then there is no way to make that point participate in the final merge. Thus a solution exists if and only if some original point is within distance `k` of every original point.

When such a point exists, one operation immediately gathers all balls. Otherwise no sequence can succeed.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n, k = map(int, input().split())
    pts = [tuple(map(int, input().split())) for _ in range(n)]

    possible = False

    for x1, y1 in pts:
        ok = True

        for x2, y2 in pts:
            if abs(x1 - x2) + abs(y1 - y2) > k:
                ok = False
                break

        if ok:
            possible = True
            break

    print(1 if possible else -1)
```

The outer loop tests every point as a potential gathering center. The inner loop verifies whether every other point lies within Manhattan distance `k`.

The early `break` statements are useful but not required. As soon as one distance exceeds `k`, that candidate can no longer work. As soon as one valid candidate is found, the answer is known.

The Manhattan distance must be computed as:

```
abs(x1 - x2) + abs(y1 - y2)
```

Using Euclidean distance or squared distance would solve a different problem.

## Worked Examples

### Example 1

Input:

```
3 3
6 7
8 8
6 9
```

| Candidate | Distances to others | Valid |
| --- | --- | --- |
| (6,7) | 3, 2 | Yes |
| (8,8) | 3, 3 | Yes |
| (6,9) | 2, 3 | Yes |

The first candidate already reaches every point, so the answer is `1`.

This example demonstrates that only one successful center is needed. We do not need to search for a better answer because `1` is already minimal.

### Example 2

Input:

```
4 1
0 0
0 1
0 2
0 3
```

| Candidate | Farthest distance | Valid |
| --- | --- | --- |
| (0,0) | 3 | No |
| (0,1) | 2 | No |
| (0,2) | 2 | No |
| (0,3) | 3 | No |

No point can reach all others with radius 1.

The answer is `-1`.

This example demonstrates why connectivity is not enough. Nearby points cannot gradually pull the entire chain together.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Check every pair of points |
| Space | O(1) excluding input storage | Only a few variables are used |

With `n ≤ 100`, at most 10,000 distance computations are performed per test case. Even with 100 test cases this is easily within the time limit.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n, k = map(int, input().split())
        pts = [tuple(map(int, input().split())) for _ in range(n)]

        possible = False

        for x1, y1 in pts:
            ok = True
            for x2, y2 in pts:
                if abs(x1 - x2) + abs(y1 - y2) > k:
                    ok = False
                    break
            if ok:
                possible = True
                break

        ans.append("1" if possible else "-1")

    return "\n".join(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# sample
assert run(
"""3
3 2
0 0
3 3
1 1
3 3
6 7
8 8
6 9
4 1
0 0
0 1
0 2
0 3
"""
) == "-1\n1\n-1"

# minimum size, impossible
assert run(
"""1
2 0
0 0
1 0
"""
) == "-1"

# minimum size, possible
assert run(
"""1
2 1
0 0
1 0
"""
) == "1"

# center point exists
assert run(
"""1
5 2
0 0
1 0
0 1
1 1
0 2
"""
) == "1"

# far separated points
assert run(
"""1
3 1
0 0
100 100
200 200
"""
) == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two points, k = 0 | -1 | No attraction possible |
| Two points, k = 1 | 1 | Smallest successful case |
| Cluster with central point | 1 | Valid gathering center exists |
| Widely separated points | -1 | Impossible configuration |
| Official sample | -1 1 -1 | Matches statement |

## Edge Cases

Consider:

```
1
2 0
0 0
1 0
```

The distance between the points is 1, which exceeds `k = 0`. The algorithm checks both points and rejects both candidates. It outputs `-1`.

Consider:

```
1
2 5
0 0
3 2
```

The Manhattan distance is exactly 5. Since the condition is distance at most `k`, both points qualify. The algorithm correctly outputs `1`.

Consider the chain:

```
1
4 1
0 0
0 1
0 2
0 3
```

The middle points appear promising because they are close to their neighbors. The algorithm computes distances to every point, discovers a distance of 2 to one endpoint, rejects each candidate, and outputs `-1`.

Consider a case where one point dominates:

```
1
5 10
0 0
1 1
2 2
3 3
4 4
```

The point `(0,0)` has Manhattan distance at most 8 from every other point. The algorithm accepts it immediately and outputs `1`. This confirms the early exit logic is correct.
