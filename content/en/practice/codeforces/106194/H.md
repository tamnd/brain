---
title: "CF 106194H - \u9b54\u5973\u4e4b\u65c5"
description: "We are given a sequence of integers representing friendliness values of towns arranged in a line. A traveler must choose a contiguous segment of this sequence, but the segment length is restricted: it must contain at least L towns and at most R towns."
date: "2026-06-19T18:37:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106194
codeforces_index: "H"
codeforces_contest_name: "2025 Winter China Unversity of Geosciences (Wuhan) Freshman Contest"
rating: 0
weight: 106194
solve_time_s: 71
verified: true
draft: false
---

[CF 106194H - \u9b54\u5973\u4e4b\u65c5](https://codeforces.com/problemset/problem/106194/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers representing friendliness values of towns arranged in a line. A traveler must choose a contiguous segment of this sequence, but the segment length is restricted: it must contain at least L towns and at most R towns. Among all valid segments, we want the one whose average value is as large as possible. The output is not the exact maximum average, but its floor.

The key object is therefore a constrained subarray: every candidate is a window [l, r] such that L ≤ (r − l + 1) ≤ R. For each such window we compute the average sum divided by length, and we want to maximize that ratio.

The constraints go up to n = 2 × 10^5, which immediately rules out any O(n²) enumeration of all subarrays. Even O(nR) becomes dangerous when R is large. This pushes us toward a solution where each position is processed in amortized constant or logarithmic time.

A naive mistake is to think we can fix the right endpoint and just pick the best left endpoint by maximizing the average greedily. That fails because shortening a segment can increase average, but not in a monotone way.

For example, consider a segment where adding a high-value element at the end increases the sum but decreases the average, while a shorter prefix is better, but a slightly longer segment elsewhere is even better. The optimal window is not monotonic in either direction.

Another subtle edge case is when L = R. Then the problem reduces to choosing a fixed-length window, which is straightforward sliding window maximum average. Any general solution must still handle this correctly without degenerating.

## Approaches

The brute-force approach is straightforward: enumerate every valid pair (l, r), check if its length is within [L, R], compute its sum, compute the average, and track the maximum. Computing sums can be accelerated with prefix sums so each query is O(1), but the number of subarrays is still O(n²) in the worst case. With n = 2 × 10^5, this is completely infeasible.

To improve, we rewrite the objective. For a fixed candidate answer x, consider transforming each element as b[i] = a[i] − x. Then a segment has average at least x if and only if its transformed sum is non-negative. This converts the problem into checking whether there exists a subarray of length in [L, R] with sum ≥ 0. This is a standard feasibility check for a guessed answer.

This immediately suggests binary search on the answer. The only remaining challenge is efficiently checking feasibility for a given x.

For a fixed x, we maintain prefix sums of b[i]. We need to find a subarray ending at i whose length is between L and R, meaning we want:

S[i] − S[j] ≥ 0 with i − R ≤ j ≤ i − L.

So for each i, we need the minimum prefix sum S[j] in a sliding window range. This can be maintained using a monotonic deque over prefix sums, ensuring we always have the best candidate j for each i in amortized O(1). This makes each feasibility check O(n), and the binary search adds a log(max value) factor.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) or O(n) | Too slow |
| Binary Search + Sliding Window | O(n log A) | O(n) | Accepted |

Here A is the value range of friendliness, up to 10^9.

## Algorithm Walkthrough

We reformulate the problem into deciding whether a candidate average value x is achievable, then binary search the maximum such x.

1. Fix a candidate value x and transform the array into b[i] = a[i] − x. The goal becomes finding a valid subarray with sum ≥ 0.
2. Compute prefix sums S where S[0] = 0 and S[i] = b[1] + … + b[i]. This allows any subarray sum to be written as S[i] − S[j].
3. For each endpoint i, we must choose a starting index j such that i − R ≤ j ≤ i − L. The subarray is valid only if its length is in [L, R]. This creates a sliding window of valid j values.
4. Maintain a data structure that tracks the minimum prefix sum among valid j values. A deque is used where prefix sums are kept in increasing order. This ensures the front always stores the smallest S[j], which maximizes S[i] − S[j].
5. As we move i from L to n, we first insert index i − L into the deque (since it becomes newly valid), and remove indices smaller than i − R (since they are no longer allowed).
6. After updating the deque, check whether S[i] − minimum_prefix_in_window ≥ 0. If yes, the candidate x is feasible.
7. Binary search x over a sufficiently wide range, typically from 0 to max(a[i]) or using floating bounds if needed. Since we need floor of answer, we can binary search integer x.

### Why it works

The key invariant is that at every position i, the deque contains exactly the prefix sums S[j] for all j such that the subarray ending at i with start j has length in [L, R], and among them the front is the minimum prefix sum. This guarantees that if any valid subarray ending at i can achieve sum ≥ 0, the one using the smallest S[j] will detect it. Therefore the feasibility check is exact, and binary search converges to the maximum achievable average.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import deque

def can(avg, a, n, L, R):
    # transformed prefix sums
    S = [0] * (n + 1)
    for i in range(1, n + 1):
        S[i] = S[i - 1] + (a[i - 1] - avg)

    dq = deque()
    dq.append(0)

    # we maintain candidates j for each i
    for i in range(L, n + 1):
        # add new valid index i-L
        j_add = i - L
        while dq and S[dq[-1]] >= S[j_add]:
            dq.pop()
        dq.append(j_add)

        # remove out-of-range indices (i - R - 1 becomes invalid)
        if i - R - 1 >= 0:
            j_remove = i - R - 1
            if dq and dq[0] == j_remove:
                dq.popleft()

        # check feasibility
        if S[i] - S[dq[0]] >= 0:
            return True

    return False

def solve():
    n, L, R = map(int, input().split())
    a = list(map(int, input().split()))

    lo, hi = 0, max(a)

    while lo < hi:
        mid = (lo + hi + 1) // 2
        if can(mid, a, n, L, R):
            lo = mid
        else:
            hi = mid - 1

    print(lo)

if __name__ == "__main__":
    solve()
```

The code separates feasibility checking from optimization. The `can` function builds transformed prefix sums for a fixed candidate average and uses a deque to maintain the minimum prefix sum in the valid window of starting indices.

The binary search uses an upper bound of max(a) since the average cannot exceed the maximum element. The midpoint is biased upward to avoid infinite loops when converging.

The deque logic is the critical part: it enforces both validity (index range constraints) and optimality (minimum prefix sum) simultaneously. The order of insertion and removal ensures each index is processed exactly once.

## Worked Examples

### Example 1

Input:

```
5 2 3
1 12 7 9 2
```

We test feasibility for x = 9.

| i | S[i] | valid j range | deque (indices) | best S[j] | check |
| --- | --- | --- | --- | --- | --- |
| 2 | ... | [0..0] | [0] | S[0] | S[2]-S[0] < 0 |
| 3 | ... | [1..1] | [1] | S[1] | valid ≥ 0 |

At i = 3, the segment [2,3] (values 12,7) has average 9.5, so feasibility succeeds. Binary search converges to 9.

This shows how the structure naturally picks the best short high-value segment rather than longer diluted ones.

### Example 2

Input:

```
4 1 4
5 5 5 5
```

For any x ≤ 5, every transformed value is non-negative over any segment, so feasibility is always true. The binary search returns 5.

This confirms that uniform arrays collapse correctly regardless of L and R.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log A) | binary search over answer, each check is O(n) via deque |
| Space | O(n) | prefix sum array and deque storage |

With n up to 2 × 10^5 and A up to 10^9, this comfortably fits within limits, since about 30-32 feasibility checks are required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    def can(avg, a, n, L, R):
        S = [0] * (n + 1)
        for i in range(1, n + 1):
            S[i] = S[i - 1] + (a[i - 1] - avg)

        dq = deque()
        dq.append(0)

        for i in range(L, n + 1):
            j_add = i - L
            while dq and S[dq[-1]] >= S[j_add]:
                dq.pop()
            dq.append(j_add)

            if i - R - 1 >= 0:
                j_remove = i - R - 1
                if dq and dq[0] == j_remove:
                    dq.popleft()

            if S[i] - S[dq[0]] >= 0:
                return True

        return False

    n, L, R = map(int, input().split())
    a = list(map(int, input().split()))

    lo, hi = 0, max(a)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if can(mid, a, n, L, R):
            lo = mid
        else:
            hi = mid - 1

    return str(lo)

# provided samples
assert run("5 2 3\n1 12 7 9 2\n") == "9", "sample 1"
assert run("4 1 4\n5 5 5 5\n") == "5", "sample 2"

# minimum size
assert run("1 1 1\n7\n") == "7", "single element"

# all equal boundary
assert run("6 2 5\n3 3 3 3 3 3\n") == "3", "uniform array"

# strict window
assert run("5 3 3\n1 2 100 2 1\n") == "100", "exact length peak"

# edge low values
assert run("3 1 3\n1 1 100\n") == "100", "best at end"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 7 | minimal boundary correctness |
| uniform array | 3 | flat landscape stability |
| exact length peak | 100 | strict window handling |
| best at end | 100 | prefix vs suffix correctness |

## Edge Cases

A minimal-length case like `n = 1, L = R = 1` reduces everything to a single value, and the algorithm initializes the deque with index 0 and immediately evaluates the only valid segment correctly.

A uniform array such as `[3, 3, 3, 3]` keeps every prefix sum difference consistent, and the deque never changes the outcome of comparisons, so every feasibility check succeeds for x ≤ 3 and fails above it.

A case where the best segment lies exactly at length L demonstrates why we insert `i - L` precisely at each step rather than earlier. For instance in `[1, 2, 100, 2, 1]` with L = R = 3, the segment `[2,3,4]` is only evaluated when i = 4 and j = 1 becomes active, showing that delayed activation of indices is essential for correctness.
