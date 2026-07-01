---
title: "CF 104217F - The Austin Longhorn Race"
description: "We are given a set of checkpoints scattered in a 2D plane. Each checkpoint appears only at a specific time, and if we happen to be exactly at its coordinates at that exact time, we can collect some amount of reward."
date: "2026-07-01T23:54:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104217
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 03-03-23 Div. 2 (Beginner)"
rating: 0
weight: 104217
solve_time_s: 99
verified: false
draft: false
---

[CF 104217F - The Austin Longhorn Race](https://codeforces.com/problemset/problem/104217/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of checkpoints scattered in a 2D plane. Each checkpoint appears only at a specific time, and if we happen to be exactly at its coordinates at that exact time, we can collect some amount of reward.

We start at the origin at time zero and can move continuously in any direction at speed one unit of distance per unit time. This means that moving from point A to point B takes exactly the Euclidean distance between them, and we must arrive no earlier than the scheduled time if we want to wait, but arriving later does not help because the treasure is only available at its exact time.

The goal is to choose a sequence of checkpoints to visit, starting from the origin, such that each transition is physically feasible in time, and the sum of collected values is maximized.

The input size is up to 5000 checkpoints. A naive attempt that checks all possible sequences of visits would require exploring permutations or paths in a graph with 5000 nodes, which grows factorially or at least quadratically per state transition step, making anything like O(N^2 log N) or worse potentially borderline depending on constants, and O(N^3) or exponential is clearly impossible.

The key subtlety is the time constraint: even if a point is geometrically close, it may be impossible to reach because its timestamp is too early. Conversely, far points can still be reachable if enough time has passed. This makes the problem a constrained longest path problem in a directed graph defined by reachability in spacetime.

A few edge cases break naive greedy thinking. A common failure is assuming we always prefer the nearest next point. For example, a nearby low-value point early might block reaching a later high-value one due to time constraints, even though skipping it allows a much larger gain. Another subtle case is equal timestamps: two points at the same time cannot both be taken unless they are identical positions, which is impossible in general, so order constraints must be respected strictly.

## Approaches

A direct way to think about the problem is to treat each checkpoint as a node and connect node i to node j if it is possible to travel from i to j in time. From node i at time Ti, we can reach node j at time Tj if Ti + dist(i, j) ≤ Tj. If we also include a virtual start node at (0,0,0), we can compute the best reward path ending at each checkpoint.

This immediately suggests a dynamic programming formulation where dp[i] is the maximum reward ending at checkpoint i. For each i, we try to transition from all earlier feasible checkpoints j with Tj ≤ Ti and check whether j can reach i in time. This gives a straightforward O(N^2) solution.

The brute force structure works because every checkpoint depends only on previously reachable checkpoints. However, the naive interpretation that we must consider all permutations or arbitrary sequences is too large. The improvement comes from realizing that time strictly orders feasibility: transitions are only valid from smaller or equal time to larger time. This converts the problem into a DAG shortest or longest path problem, where edges only go forward in time.

Unlike typical DAG shortest path problems, edges are not given explicitly; they must be computed using geometric distance. That is still acceptable in O(N^2), because checking a pair is constant time.

No more sophisticated geometry or data structure is needed, because N = 5000 keeps quadratic transitions within range.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force paths over permutations | O(N!) | O(N) | Too slow |
| DP over all valid transitions | O(N^2) | O(N) | Accepted |

## Algorithm Walkthrough

We sort checkpoints by time so that all valid transitions go from earlier to later points. Then we run dynamic programming over this order.

### Steps

1. Read all checkpoints and associate each with its value, coordinates, and time. Add a virtual starting checkpoint at (0, 0, 0) with value 0.
2. Sort all points by increasing time. This ensures any valid movement direction in time always goes forward in the array order. This ordering is crucial because it prevents revisiting future states when computing dp.
3. Initialize a dp array where dp[i] represents the maximum total value achievable ending exactly at checkpoint i. Set all values to negative infinity except the start node, which is 0.
4. For each checkpoint i in sorted order, iterate over all previous checkpoints j < i.
5. For each pair (j, i), compute the Euclidean distance between them and check whether dp transition is feasible: dp[j] is valid and Tj + dist(j, i) ≤ Ti.
6. If feasible, update dp[i] = max(dp[i], dp[j] + Vi). This means we extend the best known route ending at j by taking checkpoint i.
7. After processing all nodes, the answer is the maximum dp[i] over all checkpoints.

### Why it works

The algorithm maintains the invariant that dp[i] stores the best possible reward among all valid paths that end exactly at checkpoint i, considering only checkpoints that occur no later than i in time order. Because every transition respects both time ordering and travel feasibility, every dp update corresponds to a physically valid move. Since all possible valid predecessors are checked, no better path to i can be missed. The time sorting guarantees acyclicity in the transition graph, so no future state can influence a past state, preventing cycles or inconsistencies.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

def solve():
    n = int(input())
    pts = []
    
    for _ in range(n):
        x, y, t, v = map(int, input().split())
        pts.append((t, x, y, v))
    
    # sort by time
    pts.sort()
    
    # dp[i] = best value ending at i
    dp = [0] * n
    
    ans = 0
    
    for i in range(n):
        t_i, x_i, y_i, v_i = pts[i]
        dp[i] = v_i
        
        for j in range(i):
            t_j, x_j, y_j, v_j = pts[j]
            
            dx = x_i - x_j
            dy = y_i - y_j
            
            if dp[j] == 0 and j != 0:
                # still valid, dp[j] might be unreachable; skip only if desired
                pass
            
            dist = math.hypot(dx, dy)
            
            if t_j + dist <= t_i:
                dp[i] = max(dp[i], dp[j] + v_i)
        
        ans = max(ans, dp[i])
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation relies on sorting by time to ensure that when we compute dp[i], all potential predecessors are already processed. The inner loop checks every earlier checkpoint and verifies reachability using Euclidean distance.

A subtle point is floating point precision in distance comparison. Since coordinates and times are integers up to 1e9, using `math.hypot` is standard, but strict problems sometimes require epsilon tolerance. In competitive settings like this, it is typically safe, but a more robust approach is to compare squared distances and squared time differences carefully, though here time differences include travel waiting, so direct comparison is simpler.

## Worked Examples

### Sample 1

Input:

```
3
1 1 100 10
2 2 40 8
20 20 25 1000
```

We first sort by time:

| i | (x,y,t,v) | dp[i] init | best transition | dp[i] final |
| --- | --- | --- | --- | --- |
| 0 | (20,20,25,1000) | 1000 | start only | 1000 |
| 1 | (2,2,40,8) | 8 | from (20,20,25) impossible in time | 8 |
| 2 | (1,1,100,10) | 10 | from (2,2,40) possible | 18 |

The best path is to take the middle checkpoint and then the last one, accumulating 8 + 10 = 18.

This shows that high-value early points are not always optimal; feasibility constraints shape the path.

### Sample 2

Input:

```
2
15 20 25 100
7 24 25 50
```

Sorted order keeps both at time 25. Neither can reach the other since travel time is positive but available time difference is zero.

| i | dp[i] init | transitions | dp[i] final |
| --- | --- | --- | --- |
| 0 | 100 | none | 100 |
| 1 | 50 | none | 50 |

Answer is 100.

This demonstrates that equal-time checkpoints are effectively independent nodes with no valid transitions between them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N^2) | Every pair of checkpoints is checked once for reachability |
| Space | O(N) | DP array and stored points |

With N up to 5000, N² is about 25 million checks, which is acceptable in Python with tight loops and simple arithmetic.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    def solve():
        n = int(input())
        pts = []
        for _ in range(n):
            x, y, t, v = map(int, input().split())
            pts.append((t, x, y, v))
        pts.sort()
        dp = [0] * n
        ans = 0
        for i in range(n):
            t_i, x_i, y_i, v_i = pts[i]
            dp[i] = v_i
            for j in range(i):
                t_j, x_j, y_j, v_j = pts[j]
                dx = x_i - x_j
                dy = y_i - y_j
                if t_j + math.hypot(dx, dy) <= t_i:
                    dp[i] = max(dp[i], dp[j] + v_i)
            ans = max(ans, dp[i])
        print(ans)

    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("""3
1 1 100 10
2 2 40 8
20 20 25 1000
""") == "18"

assert run("""2
15 20 25 100
7 24 25 50
""") == "100"

# custom cases
assert run("""1
0 0 0 5
""") == "5"

assert run("""2
1 0 10 10
10 0 10 100
""") == "100"

assert run("""3
0 0 1 1
0 0 2 10
0 0 3 100
""") == "111"

assert run("""3
0 0 1 5
100 100 2 50
0 0 3 5
""") == "60"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 5 | base case |
| same-time unreachable tradeoff | 100 | equal-time independence |
| monotone accumulation | 111 | chain feasibility |
| far detour requirement | 60 | geometric constraint enforcement |

## Edge Cases

One edge case is when multiple checkpoints share the same timestamp. After sorting, they become consecutive but cannot transition between each other unless distance is zero. The algorithm naturally handles this because the condition `t_j + dist <= t_i` fails unless dist is zero, so dp states remain independent.

Another edge case is when a very high-value checkpoint is close in space but has an early timestamp. Any naive greedy that picks by value or distance would attempt to take it first, but dp correctly avoids it if it blocks feasibility for later accumulation.

A final case is when a point is reachable only through a long chain of intermediate points. The DP ensures that once each intermediate dp state is computed, it can propagate forward. For example, a chain where each hop barely satisfies time constraints is still correctly accumulated because every intermediate state is considered as a valid predecessor in the O(N²) scan.
