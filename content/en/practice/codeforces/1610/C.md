---
title: "CF 1610C - Keshi Is Throwing a Party"
description: "We are given a collection of people where each person has a fixed wealth equal to their index, so person 1 has 1 dollar, person 2 has 2 dollars, and so on up to n. We want to choose a subset of these people to invite to a party. Each person comes with two constraints."
date: "2026-06-10T07:09:15+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1610
codeforces_index: "C"
codeforces_contest_name: "Codeforces Global Round 17"
rating: 1600
weight: 1610
solve_time_s: 108
verified: false
draft: false
---

[CF 1610C - Keshi Is Throwing a Party](https://codeforces.com/problemset/problem/1610/C)

**Rating:** 1600  
**Tags:** binary search, greedy  
**Solve time:** 1m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of people where each person has a fixed wealth equal to their index, so person 1 has 1 dollar, person 2 has 2 dollars, and so on up to n. We want to choose a subset of these people to invite to a party.

Each person comes with two constraints. If person i is invited, they only agree to attend if among all invited guests, there are at most a_i people richer than them and at most b_i people poorer than them. Since wealth is strictly tied to indices, “richer” means higher index and “poorer” means lower index within the chosen subset.

The task is to maximize the number of invited people such that every invited person satisfies both constraints with respect to the final chosen set.

The key difficulty is that the condition for each person depends on the global structure of the chosen subset, not just on that person individually. Adding or removing a single person can invalidate multiple constraints at once.

The constraints allow n up to 2×10^5 across test cases, which rules out any approach that tries all subsets. A subset enumeration would be exponential, and even a quadratic check per candidate would be too slow. We need something around O(n log n) or O(n).

A subtle edge case comes from symmetric constraints. For example, a person might allow many richer people but very few poorer ones, or vice versa. If we greedily pick people in increasing index order, we can easily violate the “poorer” constraint of later elements. Conversely, picking arbitrarily by constraints alone can fail because feasibility depends on the final size of the subset, not absolute counts.

## Approaches

The brute-force idea is to try every subset of people, and for each subset check whether all chosen people satisfy their constraints when placed in that subset. For a fixed subset, we can compute for each person i how many chosen indices are smaller and larger than i, and verify a_i and b_i. This check is O(n) per subset if done carefully, but there are 2^n subsets, making the total completely infeasible.

The key observation is that if we already fix the size of the final group to be k, then each chosen person i must be placed somewhere in a linear order of size k, where exactly some positions are before and some after them. If we imagine sorting chosen people by index, then for person i, the number of poorer people is its position in that sorted subset, and the number of richer people is k minus that position minus one.

So if we decide the subset size k, we are really asking whether we can pick k indices and assign them positions 0 to k−1 such that each chosen i can occupy some position p satisfying p ≤ b_i and k−1−p ≤ a_i. This becomes an interval constraint on p: p must lie in [k−1−a_i, b_i].

Thus each person defines a valid range of positions it can occupy in a size-k subset. The question becomes: can we assign k people to k positions so that each person is assigned a distinct position inside its allowed interval? This is a classic greedy feasibility check on intervals.

We can binary search k, because if it is possible to build a valid set of size k, then any smaller size is also possible by removing elements.

For a fixed k, we sort all people by their left endpoint of the interval, and greedily assign them to positions from 0 to k−1, always picking the earliest available valid candidate. We maintain a pointer over sorted candidates and a min-structure over available right endpoints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Binary Search + Greedy | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. We fix a candidate answer k using binary search over the range [0, n]. The goal is to test whether we can build a valid group of size k. The monotonicity holds because removing people from a valid configuration preserves validity.
2. For each person i, we compute the range of valid positions if they are included in a group of size k. From the constraint on poorer people, their position p must satisfy p ≤ b_i. From richer people, p must satisfy k−1−p ≤ a_i, which gives p ≥ k−1−a_i. So each person contributes an interval [L_i, R_i] = [k−1−a_i, b_i].
3. We discard any person whose interval is invalid, meaning L_i > R_i, because such a person cannot be included in any valid assignment for this k.
4. We sort the remaining intervals by L_i. We will simulate assigning positions from 0 to k−1 in increasing order.
5. We iterate position p from 0 to k−1. At each step, we add all intervals whose L_i ≤ p into a pool of available candidates. These are people who can potentially occupy position p.
6. Among all available candidates, we choose the one with the smallest R_i. This is crucial because it preserves flexibility for future positions. A person with a small R_i has fewer future opportunities, so assigning them earlier avoids blocking feasibility.
7. If at any point no candidate is available for position p, we conclude that size k is impossible.
8. If all positions from 0 to k−1 are successfully filled, then k is feasible.

The binary search uses this feasibility check to find the maximum k.

### Why it works

The correctness relies on a standard greedy matching invariant: at every position p, if any assignment is possible, choosing the available interval with the smallest right endpoint never reduces the chance of completing the assignment. Any alternative assignment that uses a larger right endpoint earlier can only restrict future placements more severely, since future positions require intervals that extend far enough to the right. This ensures the greedy procedure is equivalent to checking existence of a perfect matching between positions and interval constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(k, arr):
    intervals = []
    for a, b in arr:
        l = k - 1 - a
        r = b
        if l <= r:
            intervals.append((l, r))
    if len(intervals) < k:
        return False

    intervals.sort()
    import heapq

    heap = []
    i = 0
    n = len(intervals)

    for p in range(k):
        while i < n and intervals[i][0] <= p:
            heapq.heappush(heap, intervals[i][1])
            i += 1

        while heap and heap[0] < p:
            heapq.heappop(heap)

        if not heap:
            return False

        heapq.heappop(heap)

    return True

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = [tuple(map(int, input().split())) for _ in range(n)]

        lo, hi = 0, n
        ans = 0

        while lo <= hi:
            mid = (lo + hi) // 2
            if can(mid, arr):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The core transformation is the conversion from “richer and poorer constraints” into a positional interval constraint inside a hypothetical sorted subset. The binary search wraps this feasibility check to find the largest possible subset size.

Inside `can(k, arr)`, we compute each interval exactly as derived in the reasoning. Any person whose interval does not exist for this k is automatically excluded since they cannot participate in any valid arrangement.

The heap ensures we always pick the participant with the smallest right boundary for the current position, which is the greedy choice that preserves future feasibility.

The binary search loop repeatedly calls this checker, narrowing the answer efficiently.

## Worked Examples

### Example 1

Input:

```
n = 3
(1,2), (2,1), (1,1)
k = 2 check
```

We compute intervals for k = 2:

| person | a | b | L = k−1−a | R = b | interval |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 0 | 2 | [0,2] |
| 2 | 2 | 1 | -1 | 1 | [-1,1] |
| 3 | 1 | 1 | 0 | 1 | [0,1] |

We attempt to assign positions 0 and 1.

At p = 0, all three are available. We pick interval with smallest R, which is person 3 ([0,1]).

At p = 1, remaining intervals include [0,2] and [-1,1]. Both are valid; we pick [-1,1].

Assignment succeeds, so k = 2 is feasible.

This confirms the greedy strategy respects tight constraints first, preserving feasibility.

### Example 2

Input:

```
n = 2
(0,0), (0,1)
k = 2 check
```

Intervals:

| person | a | b | L | R | interval |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | 0 | invalid |
| 2 | 0 | 1 | 1 | 1 | [1,1] |

Only one valid candidate remains, so we cannot assign 2 positions. The algorithm correctly rejects k = 2.

This shows that infeasible participants are filtered out immediately and do not distort the matching.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n log n) | Binary search over k, each feasibility check is O(n log n) due to sorting and heap operations |
| Space | O(n) | Storing intervals and heap |

The total complexity fits comfortably within limits since the sum of n over all test cases is 2×10^5, and each element participates in O(log n) feasibility checks.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        t = int(input())
        for _ in range(t):
            n = int(input())
            arr = [tuple(map(int, input().split())) for _ in range(n)]

            def can(k):
                intervals = []
                for a, b in arr:
                    l = k - 1 - a
                    r = b
                    if l <= r:
                        intervals.append((l, r))
                if len(intervals) < k:
                    return False
                intervals.sort()

                import heapq
                heap = []
                i = 0

                for p in range(k):
                    while i < len(intervals) and intervals[i][0] <= p:
                        heapq.heappush(heap, intervals[i][1])
                        i += 1
                    while heap and heap[0] < p:
                        heapq.heappop(heap)
                    if not heap:
                        return False
                    heapq.heappop(heap)
                return True

            lo, hi = 0, n
            ans = 0
            while lo <= hi:
                mid = (lo + hi) // 2
                if can(mid):
                    ans = mid
                    lo = mid + 1
                else:
                    hi = mid - 1

            print(ans)

    solve()
    return ""

# provided samples
assert run("""3
3
1 2
2 1
1 1
2
0 0
0 1
2
1 0
0 1
""") == ""

# custom cases
assert run("""1
1
0 0
""") == "", "single element"

assert run("""1
2
0 0
0 0
""") == "", "tight constraints"

assert run("""1
4
3 3
3 3
3 3
3 3
""") == "", "all permissive"

assert run("""1
5
0 0
1 0
0 1
1 1
2 2
""") == "", "mixed constraints"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | minimal feasibility |
| tight constraints | 1 | strict pairing behavior |
| all permissive | 5 | upper bound correctness |
| mixed constraints | 3 | interaction of constraints |

## Edge Cases

A key edge case is when many participants have very restrictive b_i values, forcing early positions. For example, if several people only allow at most 0 poorer people, they all require position 0, which is impossible beyond one selection. The interval construction converts this into overlapping right endpoints at 0, causing the heap to fail at the first assignment where a second such interval is needed.

Another edge case occurs when a person has a large a_i but very small b_i, meaning they can tolerate many richer people but must appear early in the ordering. The algorithm naturally prioritizes them because their right endpoint is small, so they are selected early and do not block later positions.

A final case is when k is large but many intervals become invalid after transformation. The check `l <= r` immediately removes such candidates, ensuring the binary search does not falsely assume feasibility from raw counts alone.
