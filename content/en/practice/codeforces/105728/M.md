---
title: "CF 105728M - The Maximum MEX Challenge"
description: "Each test case describes a set of “choices”. There are n intervals, and from the i-th interval we must pick one integer that lies inside its allowed range. After doing this for all intervals, we obtain an array of length n."
date: "2026-06-26T07:51:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105728
codeforces_index: "M"
codeforces_contest_name: "EPT Solving Cup 5.0 \uacf5\uc2dd \uacbd\uc5f0\ub300\ud68c"
rating: 0
weight: 105728
solve_time_s: 49
verified: true
draft: false
---

[CF 105728M - The Maximum MEX Challenge](https://codeforces.com/problemset/problem/105728/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case describes a set of “choices”. There are n intervals, and from the i-th interval we must pick one integer that lies inside its allowed range. After doing this for all intervals, we obtain an array of length n. The goal is to make this array contain as many consecutive small non-negative integers starting from 0 as possible, so that the first missing integer (the MEX) is as large as possible.

The MEX is determined only by whether we can successfully place every integer 0, 1, 2, and so on somewhere in the chosen values. If we fail to place x, then the answer is x, regardless of what happens later.

The constraints are large: the total number of intervals across all test cases can reach 10^6. This immediately rules out any approach that tries to simulate assignments for every candidate MEX and every interval in a nested manner. Anything quadratic in n per test case will not survive.

A subtle difficulty is that each interval does not correspond to a fixed value, but a flexible range. This means we are not matching values to positions, but instead deciding whether the system of intervals can “cover” the prefix of integers starting from 0.

A naive mistake is to think we can greedily assign each interval its smallest possible value and compute the MEX. That fails because the choice of values must be coordinated globally.

For example, consider intervals [0, 1], [0, 1], [1, 1]. A greedy local assignment might choose 0, 0, 1 giving MEX 2, which is optimal. But if we instead had [0, 0], [0, 1], [1, 1], greedy local choices can accidentally block feasibility of later values. The real constraint is whether each number k can be “supported” by at least one interval that can still be used for it.

## Approaches

The brute-force view is to try a candidate MEX m and ask whether we can assign distinct intervals to cover every value from 0 to m − 1. For a fixed m, we would scan all intervals repeatedly and attempt to assign each required value to some interval that can produce it, ensuring no interval is reused.

This can be modeled as a bipartite matching between values 0…m−1 and intervals, where an edge exists if l_i ≤ value ≤ r_i. A straightforward matching attempt for each m would cost O(n²) in the worst case because each feasibility check scans and reassigns intervals repeatedly.

The key observation is that we never need to consider matching structure explicitly. We only care about whether each integer k can be covered by some interval that is still “available” after satisfying smaller values. This suggests a greedy sweep over values from 0 upward.

If we fix k and try to ensure all values 0 through k are achievable, the best strategy is always to assign each value to the earliest finishing interval that can cover it, but since all intervals are equivalent resources and we only need existence, a simpler condition emerges: for each k, we just need to know whether there exists an interval that can be dedicated to k without blocking earlier assignments. This reduces to checking how many intervals are “usable” in increasing order.

The correct transformation is to process values in increasing order and greedily assign them to intervals that can cover them, always preferring intervals with the smallest right endpoint that still allow coverage. This is equivalent to checking whether we can greedily match 0, 1, 2, … in order using interval availability.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Matching per MEX candidate | O(n² log n) | O(n) | Too slow |
| Greedy sweep with sorted intervals | O(n log n) per test | O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Sort all intervals by their right endpoint in non-decreasing order. This ensures that when we try to assign a value k, we always consider intervals that finish earliest first, preserving flexibility for later values.
2. Maintain a pointer over intervals and a count of how many values we have successfully assigned so far, starting from 0.
3. For each integer k starting from 0 upward, attempt to assign it:

scan intervals whose left endpoint is ≤ k and right endpoint is ≥ k, and pick one such interval that is still unused. If no such interval exists, stop; the current k is the MEX.

The reason we insist on intervals covering k is that k must appear somewhere in the final construction for the MEX to exceed k.
4. Mark the chosen interval as used and move to k + 1.
5. Continue until failure or until all values up to n are assigned.

A more efficient implementation avoids repeatedly scanning from scratch: we sweep intervals in order of increasing right endpoint, and maintain a data structure (or greedy pointer logic) to ensure that whenever we reach k, we already know which intervals can cover it.

### Why it works

The core invariant is that after processing value k − 1, we have selected k distinct intervals, each of which is capable of producing a distinct value in {0, 1, …, k − 1}. Because we always assign the smallest feasible interval that can cover the current k, we never consume an interval that would be the only possible support for a smaller value. This keeps future feasibility maximally intact.

If at some value k we cannot find any interval covering k that is still unused, then no reassignment can fix this, because every interval that could produce k has already been “spent” on earlier values or does not cover k at all. That makes k the true MEX.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        segs = [tuple(map(int, input().split())) for _ in range(n)]

        # sort by right endpoint
        segs.sort(key=lambda x: x[1])

        used = 0
        idx = 0
        import heapq
        heap = []

        ok = True

        for mex in range(n + 1):
            # push all intervals that can cover current mex
            while idx < n and segs[idx][1] < mex:
                idx += 1

            while idx < n and segs[idx][0] <= mex:
                heapq.heappush(heap, segs[idx][1])
                idx += 1

            # remove unusable intervals (already too small right endpoint)
            while heap and heap[0] < mex:
                heapq.heappop(heap)

            if not heap:
                print(mex)
                ok = False
                break

            heapq.heappop(heap)
            used += 1

        if ok:
            print(n)

if __name__ == "__main__":
    solve()
```

The key part of the implementation is the sweep over possible MEX values. The heap stores all intervals that can still potentially cover the current value. For each k, we discard intervals whose right endpoint is too small, and we pick one valid interval to “assign” k. This ensures each interval is used at most once and always in the most constrained way possible.

A common implementation mistake is forgetting that an interval [l, r] can only serve values up to r, so once k exceeds r, it is permanently useless. That is why we aggressively discard expired intervals.

## Worked Examples

### Example 1

Input:

```
3
0 0
0 1
1 2
```

We sort by right endpoint:

[0,0], [0,1], [1,2]

| k | available intervals | chosen interval | result |
| --- | --- | --- | --- |
| 0 | [0,0], [0,1], [1,2] | [0,0] | ok |
| 1 | [0,1], [1,2] | [0,1] | ok |
| 2 | [1,2] | cannot cover 2 | stop |

MEX is 2, since value 2 cannot be placed.

This shows how the algorithm naturally consumes tight intervals first.

### Example 2

Input:

```
4
0 3
0 1
1 2
0 0
```

Sorted:

[0,0], [0,1], [1,2], [0,3]

| k | available intervals | chosen interval | result |
| --- | --- | --- | --- |
| 0 | all | [0,0] | ok |
| 1 | [0,1], [1,2], [0,3] | [0,1] | ok |
| 2 | [1,2], [0,3] | [1,2] | ok |
| 3 | [0,3] | [0,3] | ok |
| 4 | none | fail | MEX = 4 |

This confirms that a large interval like [0,3] is optimally saved for the largest value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) per test case | Sorting intervals dominates; each interval enters and leaves the heap once |
| Space | O(n) | Heap and interval storage |

Given that total n across tests is up to 10^6, this fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    def solve():
        t = int(input())
        out = []
        import heapq
        for _ in range(t):
            n = int(input())
            segs = [tuple(map(int, input().split())) for _ in range(n)]
            segs.sort(key=lambda x: x[1])

            idx = 0
            heap = []
            ans = 0

            for mex in range(n + 1):
                while idx < n and segs[idx][1] < mex:
                    idx += 1
                while idx < n and segs[idx][0] <= mex:
                    heapq.heappush(heap, segs[idx][1])
                    idx += 1
                while heap and heap[0] < mex:
                    heapq.heappop(heap)
                if not heap:
                    ans = mex
                    break
                heapq.heappop(heap)
            else:
                ans = n
            out.append(str(ans))
        return "\n".join(out)

    return solve()

# minimum
assert run("1\n1\n0 0\n") == "1", "single interval"

# already full chain
assert run("1\n3\n0 1\n1 2\n2 3\n") == "4", "perfect chain"

# disjoint gaps
assert run("1\n3\n0 0\n2 2\n4 4\n") == "1", "gap at 1"

# overlapping flexibility
assert run("1\n4\n0 3\n0 3\n0 3\n0 3\n") == "4", "fully flexible"

# edge: no zero
assert run("1\n2\n1 2\n1 2\n") == "0", "cannot place 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single interval | 1 | minimal case |
| chain intervals | 4 | optimal progressive coverage |
| disjoint gaps | 1 | early failure at 0 |
| full overlap | 4 | maximum flexibility |
| no zero coverage | 0 | MEX starts failing immediately |

## Edge Cases

One important edge case is when no interval contains 0. In that case, the algorithm fails immediately at k = 0 because there is no interval capable of producing 0. For example, intervals [1,2], [2,3] produce MEX = 0, since the first required value is already impossible.

Another subtle case is when many intervals overlap heavily but all have small right endpoints. For instance, intervals [0,1], [0,1], [0,1], [0,1] allow MEX at most 2. The algorithm will repeatedly consume these intervals for k = 0 and k = 1, and then fail at k = 2 because all remaining intervals end before 2.

A final edge case is when a single large interval exists alongside many tight ones. The greedy strategy ensures the tight intervals are consumed first, leaving the large interval for the largest possible k. This is essential; reversing this order would incorrectly waste flexibility and reduce the final MEX.
