---
title: "CF 105920L - Fyreflies"
description: "We are given several hidden positions on a number line from 1 to 100000. These positions represent locations of firefly groups. We do not know the positions, and multiple groups may exist at different points."
date: "2026-06-21T15:34:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105920
codeforces_index: "L"
codeforces_contest_name: "Soy Cup #1: Firefly"
rating: 0
weight: 105920
solve_time_s: 50
verified: true
draft: false
---

[CF 105920L - Fyreflies](https://codeforces.com/problemset/problem/105920/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several hidden positions on a number line from 1 to 100000. These positions represent locations of firefly groups. We do not know the positions, and multiple groups may exist at different points.

The only operation allowed is to choose a coordinate x and receive a response equal to the total distance from x to all hidden positions. Each response is a sum of absolute differences between x and every hidden point. The goal is to identify at least one of the hidden positions using at most 40 such queries per test case.

The important structural detail is that the response function behaves like a convex function over integers. As we move x along the line, the total distance decreases until we reach the “center” of the distribution of points and then increases. This center corresponds to a median of the multiset of hidden positions. Any median position is guaranteed to be one of the actual coordinates in this problem because all points are integers on a discrete line.

The constraints imply that n can be as large as 10000 per test case, and there can be up to 1000 test cases, but the sum of n is bounded. The coordinate range is fixed at 100000. This means we cannot afford any approach that tries to reconstruct all points explicitly or queries every position. Instead, each test must be solved with logarithmic querying in the coordinate space, using the structure of the absolute distance function.

A naive misunderstanding is to assume we can directly “invert” a single query. One query only gives a global aggregate and does not reveal local structure. Another subtle failure case appears if one assumes the minimum response point is unique in all cases. When all points are identical, every query returns the same coordinate as the answer, and binary search must still converge correctly without relying on slope noise.

## Approaches

A brute-force mindset would try to probe every coordinate x from 1 to 100000 and compute the response. This would clearly identify the minimum of the function, and that minimum corresponds to a median position. However, this requires 100000 queries per test case, which is far beyond the 40-query limit, so it fails immediately even before considering multiple test cases.

The key observation is that the function f(x) defined as the sum of absolute distances has a predictable discrete derivative. If we look at how f changes when moving from x to x+1, each hidden point contributes +1 if it lies at or to the left of x, and contributes -1 if it lies to the right of x. This transforms the difference f(x+1) − f(x) into a quantity that directly encodes how many points lie on each side of x.

This means we can recover the prefix count of points up to x using only two evaluations of the function. Once we can evaluate how many hidden points are ≤ x, we can binary search for the smallest x such that this count reaches at least (n+1)/2, which is the median position. That coordinate must coincide with one of the hidden firefly locations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force scanning all x | O(100000) queries | O(1) | Too slow |
| Binary search using slope recovery | O(log 100000) queries | O(1) | Accepted |

## Algorithm Walkthrough

We rely on the fact that we can compute prefix counts using differences of the distance function.

1. We define a function f(x) that queries the interactor and returns the sum of distances to all hidden points. We treat this as a black box evaluation.
2. For any x, we compute f(x) and f(x+1). From these two values, we compute the number of hidden points less than or equal to x using the identity count_le(x) = (f(x+1) − f(x) + n) / 2. This works because each point contributes either +1 or -1 to the difference depending on which side of x it lies.
3. We binary search over the coordinate range [1, 100000] to find the smallest x such that count_le(x) is at least (n+1)//2. This ensures we reach the median threshold.
4. During binary search, each midpoint requires two queries, one at mid and one at mid+1, so we carefully ensure we do not exceed the 40-query limit.
5. Once binary search converges, we output that coordinate as the answer.

The reason this works is that the function f(x) is convex and its discrete derivative changes monotonically from negative to positive as x passes the sorted list of hidden points. The prefix count extracted from the difference is monotone, which makes binary search valid. The median threshold guarantees that we land on a point that is actually occupied by at least one firefly group, not just a geometric center between them.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())

        def query(x):
            print("?", x)
            sys.stdout.flush()
            return int(input())

        def pref_le(x):
            fx = query(x)
            fx1 = query(x + 1)
            return (fx1 - fx + n) // 2

        lo, hi = 1, 100000
        target = (n + 1) // 2

        while lo < hi:
            mid = (lo + hi) // 2
            if pref_le(mid) >= target:
                hi = mid
            else:
                lo = mid + 1

        print("!", lo)
        sys.stdout.flush()

if __name__ == "__main__":
    solve()
```

The solution is built around converting a global distance query into a local structural signal. The function pref_le reconstructs how many hidden points lie to the left of a position using only two interactive calls. This is the critical transformation that turns the problem into a standard binary search over a monotone predicate.

The binary search is over the coordinate domain rather than over indices because we do not have access to the sorted list of positions. Each decision step is valid because the prefix count is monotone in x, so once we pass the median threshold we never go back below it.

The query function is isolated to ensure flushing happens immediately after every interaction, which is required to avoid idleness errors in interactive problems.

## Worked Examples

Since this is interactive, we simulate the idea using a fixed hidden array.

Assume hidden positions are [1, 5, 10, 8, 9, 6, 13], so n = 7 and median is position 8.

We show how binary search would conceptually proceed.

| step | lo | hi | mid | pref_le(mid) | decision |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 100000 | 50000 | small (7) | go left |
| 2 | 1 | 50000 | 25000 | small | go left |
| 3 | 1 | 25000 | 12500 | small | go left |
| ... | ... | ... | ... | ... | ... |
| k | 1 | 10 | 5 | 3 | go right |
| k+1 | 6 | 10 | 8 | 4 | stop |

At x = 8, the prefix count reaches at least 4, which is (n+1)//2 = 4, so the search stabilizes at 8.

This trace demonstrates that we never need to locate all points explicitly. We only need enough resolution to identify the median threshold crossing.

A second scenario is when all points are equal, say [42, 42, 42]. Every query returns a symmetric linear function centered at 42. The prefix count jumps from 0 to 7 at x = 42, so binary search converges exactly to 42 without ambiguity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log 100000) per test | Each binary search step uses constant interactive queries |
| Space | O(1) | No additional storage beyond variables |

The coordinate range is fixed and small enough for logarithmic search to fit easily within 40 queries per test case. Since each step uses two queries, around 15 to 17 steps are sufficient, staying within the limit.

## Test Cases

Because this is an interactive problem, we simulate a local oracle that answers distance queries.

```python
import sys, io

def make_solver(hidden):
    def run(inp: str) -> str:
        data = inp.strip().split()
        t = int(data[0])
        idx = 1
        out_lines = []

        for _ in range(t):
            n = int(data[idx]); idx += 1

            def f(x):
                return sum(abs(v - x) for v in hidden)

            def pref_le(x):
                fx = f(x)
                fx1 = f(x + 1)
                return (fx1 - fx + n) // 2

            lo, hi = 1, 100000
            target = (n + 1) // 2

            while lo < hi:
                mid = (lo + hi) // 2
                if pref_le(mid) >= target:
                    hi = mid
                else:
                    lo = mid + 1

            out_lines.append(str(lo))

        return "\n".join(out_lines)

    return run

# custom tests
run = make_solver([5])
assert run("1\n1\n") == "5"

run = make_solver([1, 5, 10])
assert run("1\n3\n") == "5"

run = make_solver([42, 42, 42])
assert run("1\n3\n") == "42"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point | same value | base correctness |
| multiple spread points | median selection | correctness of median logic |
| all equal points | that value | stability under flat function |

## Edge Cases

When all hidden points are identical, the function f(x) becomes a simple V-shaped function centered at that coordinate. The prefix reconstruction still works because the difference f(x+1) − f(x) jumps from negative to positive exactly at that point. The binary search therefore converges without oscillation.

When n is even, there are two medians in the classical sense, but both correspond to valid coordinates among the hidden points in this problem setup. The algorithm targets the lower median via (n+1)//2, ensuring deterministic convergence to a valid answer.

When all points lie near the boundary 1 or 100000, the binary search still behaves correctly because queries remain within bounds and the monotonicity of the prefix function is preserved even at edges.
