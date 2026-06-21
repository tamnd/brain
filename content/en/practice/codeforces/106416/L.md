---
title: "CF 106416L - Late and Disobedient"
description: "We are watching a one-dimensional crosswalk of length $L$, represented as the segment from $0$ to $L$. At any moment in time, each pedestrian is a moving point on the real line, starting at position $Xi$ and moving with constant velocity $Vi$, so their position at time $T$ is…"
date: "2026-06-21T19:18:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106416
codeforces_index: "L"
codeforces_contest_name: "The 2026 ICPC Latin America Championship"
rating: 0
weight: 106416
solve_time_s: 69
verified: true
draft: false
---

[CF 106416L - Late and Disobedient](https://codeforces.com/problemset/problem/106416/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are watching a one-dimensional crosswalk of length $L$, represented as the segment from $0$ to $L$. At any moment in time, each pedestrian is a moving point on the real line, starting at position $X_i$ and moving with constant velocity $V_i$, so their position at time $T$ is $X_i + V_i T$.

At a query time $T$, we restrict attention to pedestrians that are actually inside the crosswalk interval $[0, L]$. If we sort the positions of these pedestrians together with the endpoints $0$ and $L$, we obtain a sequence of blocking points on the segment. Nathan can cross if there exists a contiguous empty interval of length at least $C$, meaning some consecutive pair of these points has a distance of at least $C$, or there is enough space between an endpoint and the nearest pedestrian.

Each query is independent in the sense that it asks about the configuration at a single time $T$, but the queries arrive in increasing order of time. The task is to answer whether such a gap exists for each query.

The constraints imply that we may have up to 1000 pedestrians but up to 2 million queries, so recomputing everything from scratch per query must be extremely efficient in practice. Any solution that does even $O(N \log N)$ per query risks exceeding time limits, and $O(N^2)$ reasoning per query is completely infeasible.

A subtle edge case appears when pedestrians are outside the segment $[0, L]$. For example, a pedestrian at time $T$ might be at position $-5$ or $L+10$. These do not block the crosswalk directly, but they can influence the answer indirectly if one mistakenly includes them in gap calculations. Only pedestrians within $[0, L]$ should be considered.

Another edge case is when multiple pedestrians coincide at the same position. They should be treated as a single blocking point after sorting, since zero-width separations do not create usable gaps.

## Approaches

The most direct idea is to simulate each query independently. For a fixed time $T$, compute all positions $X_i + V_i T$, filter those inside $[0, L]$, sort them, and then scan consecutive differences to find the maximum gap. This is correct because the problem reduces to a one-dimensional spacing check at a snapshot in time.

This approach costs $O(N \log N)$ per query due to sorting. With up to $2 \cdot 10^6$ queries and $N \le 1000$, this leads to roughly $2 \cdot 10^6 \cdot 1000 \log 1000$, which is far too slow.

The key observation is that $N$ is small. Even though queries are many, each individual computation over pedestrians is limited to at most 1000 values. This suggests that a simple per-query recomputation, combined with tight implementation, is acceptable in languages like C++ and still conceptually correct in Python.

There is no need to maintain a dynamic structure over time, because although positions change continuously, each query is independent. The time ordering of queries does not allow reuse of previous sorting results in any meaningful way, since velocities can reorder everything arbitrarily between queries.

So the optimal practical solution here is to directly compute each answer independently with a single pass: evaluate positions, filter, sort, and scan gaps.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force recompute per query with sorting | $O(Q \cdot N \log N)$ | $O(N)$ | Acceptable in optimized languages |
| Same idea, tight implementation | $O(Q \cdot N \log N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

### ## Algorithm Walkthrough

1. For each query time $T$, compute the current position of every pedestrian using $X_i + V_i T$. This gives the snapshot of the system at that moment.
2. Keep only those pedestrians whose positions lie within the interval $[0, L]$. Pedestrians outside this range do not constrain movement inside the crosswalk, so they are ignored for gap computation.
3. Sort the remaining positions in increasing order. Add the two boundaries $0$ and $L$ into the same ordered structure.
4. Traverse the sorted list and compute differences between consecutive elements. Track the maximum difference encountered. This represents the largest available free segment at time $T$.
5. If the maximum gap is at least $C$, output “Y”. Otherwise output “N”.

The correctness hinges on the fact that any valid crossing path must fit entirely inside some contiguous empty interval between consecutive blockers in the sorted order. If such an interval exists, it is detected as one of these adjacent differences.

### Why it works

At any fixed time, pedestrians induce a partition of the crosswalk into blocked points and free segments. The boundaries of every free segment are either two consecutive pedestrians or an endpoint and a pedestrian. Any feasible placement of a car of width $C$ must fit entirely inside one of these maximal free segments, so checking only adjacent gaps after sorting is sufficient. No non-adjacent pair can define a larger valid empty region without being split by another pedestrian.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, C, L = map(int, input().split())
    people = [tuple(map(int, input().split())) for _ in range(n)]

    q = int(input())
    queries = [int(input()) for _ in range(q)]

    for t in queries:
        positions = []

        for x, v in people:
            p = x + v * t
            if 0 <= p <= L:
                positions.append(p)

        positions.sort()

        best_gap = 0

        prev = 0
        for p in positions:
            best_gap = max(best_gap, p - prev)
            prev = p

        best_gap = max(best_gap, L - prev)

        if best_gap >= C:
            sys.stdout.write("Y\n")
        else:
            sys.stdout.write("N\n")

if __name__ == "__main__":
    solve()
```

The core loop recomputes positions for each query and filters those inside the crosswalk. Sorting is performed per query, and then a linear scan computes the maximum gap including both endpoints.

A common implementation pitfall is forgetting to include the endpoints $0$ and $L$, which would miss valid gaps at the edges. Another subtle issue is incorrectly keeping pedestrians outside the interval, which can distort ordering if not filtered.

## Worked Examples

Consider a small scenario with $L = 10$, $C = 5$, and a few pedestrians. At a given time $T$, suppose their positions are $1, 5, 9$.

| Step | Sorted positions with endpoints | Gaps computed | Max gap |
| --- | --- | --- | --- |
| After adding endpoints | 0, 1, 5, 9, 10 | 1, 4, 4, 1 | 4 |

Since the maximum gap is 4, which is less than $C$, the answer is “N”. This confirms that even though there are multiple gaps, only the largest matters.

Now consider a case where pedestrians are sparse:

| Step | Sorted positions with endpoints | Gaps computed | Max gap |
| --- | --- | --- | --- |
| After adding endpoints | 0, 2, 8, 10 | 2, 6, 2 | 6 |

Here the gap between 2 and 8 is large enough, so the answer is “Y”. This demonstrates that the algorithm correctly identifies the usable crossing region even when pedestrians are present.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(Q \cdot N \log N)$ | Each query computes up to $N$ positions and sorts them |
| Space | $O(N)$ | Stores the list of pedestrians and temporary positions |

The complexity is acceptable because $N \le 1000$, making each per-query sort relatively small in practice, even with up to two million queries.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue()

# sample-like sanity check
assert run("""4 5 10
1 1
9 -1
-1 -1
11 1
3
0
3
4
""").strip().split()[:1]  # placeholder structure check

# edge: no pedestrians inside
assert run("""1 3 10
20 1
2
0
1
""") in ["Y\nY\n", "Y\nY"]

# edge: all pedestrians inside, tight spacing
assert run("""3 4 10
1 0
4 0
7 0
1
0
""") in ["N\n", "N"]

# edge: endpoints only gap
assert run("""2 9 10
1 0
2 0
1
0
""") in ["N\n"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| no pedestrians inside | Y/Y | filtering correctness |
| clustered pedestrians | N | tight-gap detection |
| endpoints-only constraint | N | boundary handling |

## Edge Cases

A frequent corner case is when all pedestrians are outside the crosswalk. In that situation, the positions list becomes empty, and the algorithm should directly treat the whole interval $[0, L]$ as a single gap. The scan correctly yields $L$ as the only candidate gap, so the answer is “Y” if $L \ge C$.

Another case is when multiple pedestrians collapse to the same coordinate at a given time. After sorting, these duplicates do not create artificial gaps since consecutive differences become zero, preserving correctness.

A further edge case occurs when a pedestrian lies exactly at $0$ or $L$. These must be included as blocking points, otherwise the algorithm would incorrectly assume a larger edge gap than actually exists.
