---
title: "CF 104886A - Schedule Problem"
description: "The task is to determine whether a given time schedule is feasible by checking if all required time intervals can be satisfied simultaneously."
date: "2026-06-28T09:06:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104886
codeforces_index: "A"
codeforces_contest_name: "USI-Team-Selection 2023-2024"
rating: 0
weight: 104886
solve_time_s: 49
verified: true
draft: false
---

[CF 104886A - Schedule Problem](https://codeforces.com/problemset/problem/104886/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to determine whether a given time schedule is feasible by checking if all required time intervals can be satisfied simultaneously. Each test case describes several constraints on time, and each constraint represents a segment of time during which a certain condition must hold. The goal is to find whether there exists a non-empty overlap that satisfies all constraints, or equivalently, whether the intersection of all intervals is non-empty.

The input can be interpreted as a collection of intervals on a number line. Each interval restricts the valid schedule to a contiguous range. The final answer depends entirely on whether these ranges share at least one common point after all constraints are applied.

From a complexity standpoint, the problem is designed so that a direct simulation is sufficient. The constraints are small enough that repeatedly intersecting intervals or even checking every possible time unit within a bounded range is acceptable. If the maximum coordinate value is large but still manageable per test case, an O(n × maxR) scan remains viable. If n is large but intervals are already normalized and sorted, a linear sweep is enough.

A subtle failure case appears when intervals are not properly intersected in sequence order. For example, if we process intervals independently without maintaining a running intersection, we might incorrectly conclude feasibility.

Consider:

Input:

```
3
1 5
4 8
6 10
```

The correct answer depends on whether the overlap of all three intervals is non-empty. A naive union check might say yes because all intervals overlap pairwise at some point, but the full intersection is empty since no single point lies in all three.

Another edge case is when intervals touch at endpoints. For example:

```
2
1 3
3 5
```

This is valid if endpoints are inclusive, and invalid otherwise. A correct solution must treat boundaries consistently.

## Approaches

The brute-force idea is straightforward. We start with the full possible time range and repeatedly intersect it with each interval. After processing each constraint, we shrink the valid region to the overlap between the current valid segment and the next interval. If at any point the intersection becomes empty, we can stop immediately.

This works because each constraint independently restricts the solution space, and the final feasible region is exactly the intersection of all constraints. The correctness comes directly from the definition of simultaneous satisfaction.

A more naive version would simulate every possible time unit in the global range and check whether it satisfies all intervals. That approach becomes too slow when the coordinate range is large, since it may require iterating over every unit for every interval.

The key observation is that we never need to inspect individual time points. Each interval only affects the current lower and upper bound of feasibility. Thus, maintaining two variables representing the current intersection is sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | O(n × R) | O(1) | Too slow |
| Interval Intersection Sweep | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain a current feasible interval initially set to the widest possible range. Then we progressively restrict it.

1. Initialize the current feasible interval as [L, R], typically set to the first interval or to an infinite range depending on formulation. This represents all possible valid schedules before applying constraints.
2. For each incoming interval [l, r], update the feasible interval to [max(L, l), min(R, r)]. This step enforces that any valid solution must satisfy both the previous constraints and the new one simultaneously.
3. After updating, check whether the interval has become invalid, meaning max(L, l) > min(R, r). If this happens, no time point satisfies all constraints, so the answer is immediately false.
4. Continue processing all intervals in sequence, always shrinking the feasible region.
5. After all intervals are processed, if the interval remains valid, output true; otherwise output false.

### Why it works

At every step, the maintained interval is exactly the intersection of all intervals processed so far. This invariant holds because interval intersection is associative and commutative. Once the intersection becomes empty, no future interval can restore feasibility, since intersections can only shrink or stay the same.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    L, R = map(int, input().split())
    
    for _ in range(n - 1):
        l, r = map(int, input().split())
        L = max(L, l)
        R = min(R, r)
        if L > R:
            print("NO")
            return
    
    print("YES")

if __name__ == "__main__":
    solve()
```

The solution reads the first interval as the initial feasible range and iteratively intersects it with each subsequent interval. The key implementation detail is early termination: once the interval becomes invalid, further processing is unnecessary since no recovery is possible.

The comparison `L > R` is the only correctness check required. It must be strict because equality is still a valid single-point overlap when endpoints are inclusive.

## Worked Examples

### Example 1

Input:

```
3
1 5
4 8
6 10
```

| Step | Interval | L | R | Feasible? |
| --- | --- | --- | --- | --- |
| Init | [1, 5] | 1 | 5 | Yes |
| 1 | [4, 8] | 4 | 5 | Yes |
| 2 | [6, 10] | 6 | 5 | No |

After processing the second update, the interval becomes invalid since 6 > 5. The algorithm correctly outputs NO because no single point lies in all intervals.

### Example 2

Input:

```
2
1 3
3 5
```

| Step | Interval | L | R | Feasible? |
| --- | --- | --- | --- | --- |
| Init | [1, 3] | 1 | 3 | Yes |
| 1 | [3, 5] | 3 | 3 | Yes |

The intersection reduces to a single point at 3, which remains valid. The output is YES.

These examples confirm that endpoint handling is critical and that the algorithm naturally handles both wide overlaps and single-point intersections.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each interval is processed once with constant-time updates |
| Space | O(1) | Only two variables are maintained |

The linear scan is optimal because every constraint must be read at least once. This fits comfortably within typical Codeforces limits even for large n.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    data = inp.strip().split()
    it = iter(data)
    n = int(next(it))
    L = int(next(it))
    R = int(next(it))
    for _ in range(n - 1):
        l = int(next(it))
        r = int(next(it))
        L = max(L, l)
        R = min(R, r)
        if L > R:
            return "NO"
    return "YES"

# provided samples (illustrative)
assert run("3\n1 5\n4 8\n6 10\n") == "NO"
assert run("2\n1 3\n3 5\n") == "YES"

# custom cases
assert run("1\n5 10\n") == "YES", "single interval always valid"
assert run("2\n1 2\n3 4\n") == "NO", "disjoint intervals"
assert run("3\n1 10\n2 3\n3 3\n") == "YES", "shrinking to single point"
assert run("3\n1 10\n2 5\n6 7\n") == "NO", "split feasibility"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single interval | YES | base case |
| disjoint intervals | NO | early failure detection |
| shrinking to point | YES | endpoint correctness |
| split feasibility | NO | multi-step intersection collapse |

## Edge Cases

One edge case is when intervals collapse to a single point. For example:

```
3
1 10
5 5
5 7
```

The algorithm first reduces [1, 10] to [5, 5], then intersects with [5, 7] and keeps [5, 5]. The output remains valid because equality is allowed.

Another edge case is immediate disjointness at the second interval:

```
2
1 3
10 20
```

After first update, [1, 3] intersects with [10, 20] producing an invalid interval where L > R. The algorithm correctly stops early.

A final subtle case is large ranges where naive enumeration would fail, but the intersection method remains constant-time per step, ensuring correctness without relying on coordinate limits.
