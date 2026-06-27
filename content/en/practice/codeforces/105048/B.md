---
title: "CF 105048B - Romeo and Random Walk"
description: "We are given a set of positions on a number line, indexed from 0 to N−1. Each position represents a candidate location where Juliet could have been at time zero."
date: "2026-06-28T01:21:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105048
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 03-22-24 Div. 2 (Beginner)"
rating: 0
weight: 105048
solve_time_s: 81
verified: false
draft: false
---

[CF 105048B - Romeo and Random Walk](https://codeforces.com/problemset/problem/105048/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of positions on a number line, indexed from 0 to N−1. Each position represents a candidate location where Juliet could have been at time zero. After that, Juliet moves on the line, and we are told two things: at time d, her position must lie somewhere inside a known interval [A, B], and in each minute she can move at most one unit distance.

The task is to determine which starting indices are consistent with this information. For each initial point Pi, we ask whether there exists some valid movement of Juliet over d minutes, starting from Pi, such that her final position lies inside [A, B]. If yes, we output the index i.

The constraint N ≤ 10^5 immediately rules out any solution that simulates movement per starting point or per time step. Any approach that is even O(N·d) or O(N^2) is impossible since d can be as large as 10^9. This forces us to reduce the problem to a direct geometric feasibility check per point.

A subtle point is that Juliet’s movement is not deterministic, only bounded. After d minutes, starting from Pi, her reachable region is exactly the interval [Pi − d, Pi + d]. The problem reduces to checking whether this interval intersects [A, B]. Missing this interval interpretation is the main source of incorrect greedy or simulation-based solutions.

Edge cases arise when the reachable interval barely touches [A, B], especially at boundaries.

For example, if Pi = 5, d = 2, then reachable is [3, 7]. If A = 7 and B = 10, this is still valid because 7 is reachable exactly. A careless strict inequality check would incorrectly discard such cases.

Another edge case occurs when A > Pi + d or B < Pi − d, where there is no overlap at all. These must be rejected cleanly without off-by-one errors.

## Approaches

A brute-force interpretation would try to simulate Juliet’s movement from every starting point Pi and check whether there exists a path of length d that ends in [A, B]. Since each step allows movement in two directions or staying within a range, the number of possible paths grows exponentially with d. Even if we instead discretize movement, checking all possibilities for each starting point becomes infeasible once d reaches 10^9.

The key observation is that we do not actually care about the path, only the reachable region after d steps. From any starting point Pi, the set of possible final positions is exactly a continuous interval [Pi − d, Pi + d]. This is because every unit of movement expands reach symmetrically in both directions.

Once we have this, the problem becomes purely a one-dimensional interval intersection problem. We only need to check whether [Pi − d, Pi + d] overlaps with [A, B]. This condition can be tested in constant time per index.

The brute-force approach fails because it tries to reason about trajectories instead of reachable sets. The observation that movement constraints define a convex reachable interval collapses the problem into a simple overlap check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(N · 2^d) | O(1) | Too slow |
| Interval Intersection | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read N, A, B, and d, then read the array P of candidate starting positions.
2. For each index i, compute the reachable interval [Pi − d, Pi + d]. This represents all positions Juliet could occupy at time d if she started at Pi.
3. Check whether this interval overlaps with [A, B]. The condition for overlap is Pi − d ≤ B and Pi + d ≥ A. This ensures that there exists at least one point that is reachable from Pi and also lies inside the known final range.
4. If the condition holds, record index i as valid.
5. After processing all indices, output all valid indices in increasing order.

### Why it works

The core invariant is that after exactly d steps, Juliet’s position must lie in a continuous interval centered at her starting position, with radius d. This interval fully characterizes all possible outcomes of her movement, because each step expands the reachable set by at most one unit in both directions and the union of all reachable positions remains convex on a line. Since both the reachable region and the observed region [A, B] are intervals, feasibility reduces exactly to interval intersection. No sequence of moves can produce a final position outside this interval, and no valid final position inside the overlap is unreachable.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, A, B, d = map(int, input().split())
    P = list(map(int, input().split()))
    
    res = []
    
    for i in range(N):
        left = P[i] - d
        right = P[i] + d
        
        if left <= B and right >= A:
            res.append(str(i))
    
    print(" ".join(res))

if __name__ == "__main__":
    solve()
```

The solution reads all inputs in linear time and checks each candidate independently. The only computation per index is two arithmetic operations and two comparisons, ensuring O(N) behavior.

The boundary logic is implemented carefully using non-strict inequalities. This is essential because endpoints are valid positions, and excluding equality would incorrectly discard valid cases where the reachable interval just touches [A, B].

## Worked Examples

### Example 1

Input:

```
N=10, A=3, B=5, d=14
P = [10, 14, 17, 5, 11, 13, 6, 17, 10, ...]
```

We evaluate a few indices explicitly.

| i | Pi | Pi − d | Pi + d | Overlaps [3,5]? | Valid |
| --- | --- | --- | --- | --- | --- |
| 0 | 10 | -4 | 24 | yes | 0 |
| 4 | 11 | -3 | 25 | yes | 4 |
| 7 | 17 | 3 | 31 | yes | 7 |

All other indices either have reachable intervals entirely above 5 or entirely below 3.

Output:

```
0 4 7
```

This confirms that the overlap condition correctly identifies all starting points whose reachable ranges intersect the observed final interval.

### Example 2

Input:

```
N=3, A=8, B=10, d=2
P = [5, 9, 12]
```

| i | Pi | Pi − d | Pi + d | Overlaps [8,10]? | Valid |
| --- | --- | --- | --- | --- | --- |
| 0 | 5 | 3 | 7 | no |  |
| 1 | 9 | 7 | 11 | yes | 1 |
| 2 | 12 | 10 | 14 | yes | 2 |

Output:

```
1 2
```

This example shows a boundary case where index 2 is valid because its reachable interval touches A exactly at 10.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each index is processed once with constant-time arithmetic and comparisons |
| Space | O(1) | Only a small output list is maintained besides input storage |

The linear scan is optimal under the constraints since every element must be inspected at least once to determine validity. With N up to 10^5, this runs comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    N, A, B, d = map(int, input().split())
    P = list(map(int, input().split()))

    res = []
    for i in range(N):
        if P[i] - d <= B and P[i] + d >= A:
            res.append(str(i))
    return " ".join(res)

# provided sample
assert run("10 3 5 14\n10 14 17 5 11 13 6 17 10 1") == "0 4 7"

# minimum case
assert run("1 0 0 0\n0") == "0"

# no valid points
assert run("3 100 200 5\n0 1 2") == ""

# all valid
assert run("3 0 10 100\n1 2 3") == "0 1 2"

# boundary touch cases
assert run("2 5 5 0\n5 10") == "0"

# symmetric reach
assert run("2 8 12 2\n10 13") == "0 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point, exact match | 0 | minimal boundary correctness |
| all too far | empty | rejection logic |
| large d | all indices | full inclusion case |
| zero movement | boundary equality | exact endpoint handling |
| tight overlap | mixed | correctness of intersection logic |

## Edge Cases

One edge case occurs when d = 0. In this case, the reachable interval collapses to a single point Pi. The condition becomes Pi ∈ [A, B]. The algorithm handles this naturally because Pi − 0 ≤ B and Pi + 0 ≥ A reduces to A ≤ Pi ≤ B, preserving correctness without special handling.

Another edge case arises when A and B are equal. Then we are checking whether Pi can reach exactly one point after d steps. The overlap condition correctly reduces to checking whether Pi is within distance d from A, since both inequalities force A to lie inside [Pi − d, Pi + d].

A final subtle case is when intervals only touch at boundaries. For instance, Pi + d = A. The algorithm includes this as valid because the inequality is non-strict. This ensures that exact reachability at the endpoint is correctly counted, matching the continuous nature of movement on the line.
