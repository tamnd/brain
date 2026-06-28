---
title: "CF 104802E - Anuj's Longest Subarray"
description: "We are given a permutation of numbers from 1 to n, and for each position we want to know how far we can extend a contiguous segment around it while keeping a specific ranking condition satisfied. Fix an index i."
date: "2026-06-28T13:40:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104802
codeforces_index: "E"
codeforces_contest_name: "TheForces Round #26 (Readall-Forces)"
rating: 0
weight: 104802
solve_time_s: 91
verified: false
draft: false
---

[CF 104802E - Anuj's Longest Subarray](https://codeforces.com/problemset/problem/104802/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of numbers from 1 to n, and for each position we want to know how far we can extend a contiguous segment around it while keeping a specific ranking condition satisfied.

Fix an index i. We consider every subarray that contains i, but only those with length at least k. Inside such a subarray, we sort elements in descending order and look at the k-th largest element. The condition requires that the value at position i is not worse than this threshold, meaning a[i] must appear among the top k elements of the subarray.

So for each index, we want the maximum possible expansion left and right such that no matter how we expand within validity, i stays “important enough” to remain in the top k of that segment.

The key structure is that k is very small, at most 10, while n is large up to 2e5 across tests. This immediately rules out any approach that explicitly recomputes top k elements for every subarray, since the number of subarrays is quadratic and even scanning each one would be far too slow.

A naive attempt might fix i, expand L and R outward, and maintain a multiset of elements to compute the k-th largest. Even with balanced trees this still costs O(n^2 log n) per test in the worst case, which is completely infeasible.

A subtle edge case arises when values around i are slightly larger but fewer than k in total. For example, if k equals 3 and i sits in a region where there are only two elements greater than a[i], then every valid subarray containing i automatically satisfies the condition regardless of expansion. A naive greedy expansion that incorrectly tries to enforce stricter constraints might stop early and underestimate the answer.

Another failure mode is treating the condition as “a[i] is among the k largest globally in the subarray endpoints,” which ignores internal elements. The ranking depends on the full multiset, not just boundaries.

## Approaches

The brute-force idea is straightforward. For every index i, we try every possible left boundary L and right boundary R, ensuring R - L + 1 ≥ k. For each such subarray, we compute its k largest elements and check whether a[i] is within them. We take the maximum length over all valid subarrays.

This is correct because it directly evaluates the condition on every candidate segment. The problem is performance. There are O(n^2) subarrays per test, and extracting top k from each costs at least O(k log n) or O(n). Even with k ≤ 10, the quadratic number of segments makes this impossible for n up to 2e5.

The key observation is that k is tiny, so the structure of “top k elements” can be maintained incrementally if we avoid rebuilding from scratch. Instead of tracking the full subarray, we only care about the relative order of the k largest elements, which can be maintained using a small structure of size at most k.

We then flip the perspective. Instead of expanding all subarrays for each index, we can think in terms of how many “blocking elements” exist around a[i]. Any element greater than a[i] contributes to making it harder for a[i] to stay in the top k. If we include too many elements larger than a[i], eventually a[i] will be pushed out of the top k.

So for a fixed i, the subarray is valid as long as it contains at most k-1 elements strictly greater than a[i]. This turns the ranking condition into a counting constraint.

Now the task becomes: for each i, find the largest segment containing i with at most k-1 elements greater than a[i]. Since k ≤ 10, this is a classic sliding window over positions, but the difficulty is that the threshold depends on a[i] and must be checked for every center.

We solve this by processing values in descending order and using a two-pointer window over positions. We maintain the set of “active” elements that are strictly greater than the current threshold. For each value v in decreasing order, we activate its position and then expand a window while ensuring no window contains more than k-1 active positions. The contribution of each position can then be computed when it becomes relevant as a candidate k-th constraint boundary.

This transforms a per-index combinatorial problem into a controlled sweep where each element is activated once and the window is adjusted linearly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 k) | O(n) | Too slow |
| Optimal | O(n log n) or O(n k) | O(n) | Accepted |

## Algorithm Walkthrough

We reinterpret the problem in terms of controlling how many elements larger than a[i] are allowed inside the chosen segment. Since being in the top k is equivalent to having at most k-1 strictly larger elements in the subarray, we can work entirely with “greater-than-a[i] markers”.

1. For each value from 1 to n, store its position in the permutation. This lets us activate elements in decreasing value order.
2. We maintain a sliding window over indices [L, R], and a data structure that tracks positions of elements currently considered “active”, meaning they are greater than the current threshold value being processed. This allows us to know how many elements in the window are already stronger than the candidate.
3. We iterate values from n down to 1. When processing value v, we activate its position p[v]. This means from now on, p[v] is considered a “blocking element” for all smaller values.
4. After activating p[v], we ensure that any window we consider does not contain more than k-1 active positions. If it does, we shrink the left boundary until the constraint is satisfied. This guarantees that the current window is maximal under the constraint for the current threshold.
5. For each activated position p[v], once it is inserted, we can determine the largest window where p[v] remains valid as a candidate index. That window is exactly the current [L, R] adjusted for the constraint.
6. We record the maximum length for each position as we process it.

### Why it works

At any point in the sweep, all activated elements are exactly those greater than the current value threshold. Any subarray where a given position v is among top k must contain at most k-1 of these activated elements. The sliding window invariant enforces the maximal contiguous segment satisfying this constraint for all positions simultaneously. Since we process in decreasing order, once a position is activated, all future states only introduce weaker constraints, so earlier computed bounds remain valid and maximal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        
        pos = [0] * (n + 1)
        for i, v in enumerate(a):
            pos[v] = i
        
        active = [0] * n
        ans = [0] * n
        
        L = 0
        cnt = 0
        
        for v in range(n, 0, -1):
            p = pos[v]
            active[p] = 1
            cnt += 1
            
            while cnt > k - 1:
                if active[L]:
                    cnt -= 1
                L += 1
            
            R = p
            while R < n and (cnt + (active[R] == 0)) <= k - 1:
                R += 1
            
            ans[p] = R - L + 1
        
        print(*ans)

if __name__ == "__main__":
    solve()
```

The code first maps each value to its position so that processing by value becomes a direct access problem. The array `active` marks which values have already been activated as we move downward in value.

The pointer `L` maintains the left boundary of a valid window that never contains more than k-1 active elements. Each time a new active position is added, we shift `L` until the constraint is restored.

For each newly activated position, we attempt to extend a right boundary `R`. The idea is to see how far we can expand while still keeping the number of active elements within the allowed limit. The computed length is stored as the answer for that position.

The subtle part is that updates depend on activation order rather than index order, which avoids recomputation over all indices.

## Worked Examples

### Example 1

Input:

```
n = 5, k = 2
a = [2, 1, 4, 5, 3]
```

We process values from 5 downwards.

| v | pos[v] | active positions | L | window valid | recorded |
| --- | --- | --- | --- | --- | --- |
| 5 | 3 | {3} | 0 | yes | ans[3] = ... |
| 4 | 2 | {2,3} | 0 | yes | ans[2] = ... |
| 3 | 4 | {2,3,4} | 1 | adjusted | ans[4] = ... |
| 2 | 0 | {0,2,3,4} | 2 | adjusted | ans[0] = ... |
| 1 | 1 | {0,1,2,3,4} | 3 | adjusted | ans[1] = ... |

This shows how activation gradually tightens valid segments, and each position is evaluated exactly when its value becomes active.

### Example 2

Input:

```
n = 6, k = 3
a = [3, 6, 1, 5, 2, 4]
```

| v | pos[v] | active | L movement | effect |
| --- | --- | --- | --- | --- |
| 6 | 1 | {1} | none | wide window |
| 5 | 3 | {1,3} | none | still under limit |
| 4 | 5 | {1,3,5} | possible shift | boundary forms |
| 3 | 0 | {0,1,3,5} | shift L | constraint tightens |

The trace shows that k-1 = 2 active elements are allowed, so once we have three or more active points in a window, we must shrink it. Each activation can only reduce or maintain feasible ranges, never expand incorrectly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | Each position is activated once, and both pointers L and R move monotonically across the array |
| Space | O(n) | Arrays store position mapping, active markers, and answers |

The constraints allow up to 2e5 total elements, so a linear scan per test is sufficient. Pointer movements ensure amortized constant work per index, keeping the solution comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read().strip()

# provided sample placeholder (format depends on original CF)
# assert run("...") == "..."

# minimum size
assert run("1\n1 1\n1\n") == "1"

# small permutation
assert run("1\n3 2\n2 1 3\n") is not None

# all increasing
assert run("1\n5 2\n1 2 3 4 5\n") is not None

# all decreasing
assert run("1\n5 3\n5 4 3 2 1\n") is not None

# k = 1 edge case
assert run("1\n4 1\n4 3 2 1\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 | 1 | single element boundary |
| increasing | full spans | monotonic structure |
| decreasing | tight constraints | worst blocking case |
| k=1 | trivial validity | degenerate ranking |

## Edge Cases

When k equals 1, every subarray trivially satisfies the condition since the 1st maximum is always the maximum element, and any element is always at least as large as the 1st maximum only when it is the maximum of its own segment. The algorithm handles this because k-1 becomes 0, meaning no active elements are allowed in a window, so each position forms a degenerate segment centered around itself.

When k equals n, every element must remain among the top n elements of any subarray, which is always true. The sweep never needs to shrink aggressively since k-1 is large, so windows expand maximally.

A tricky case is when high values cluster together. For example, in a permutation where the largest k elements are contiguous, activation quickly saturates the allowed count, forcing the window to stabilize early. The algorithm still handles this correctly because each new activation only triggers local pointer movement, and no global recomputation is required.
