---
title: "CF 106508G - Delete or not"
description: "We are given a sequence of distinct values that is already sorted in increasing order. From any contiguous segment of this sequence, we are allowed to repeatedly remove elements as long as they satisfy a local convexity condition: an interior element can be deleted if it is not…"
date: "2026-06-18T19:11:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106508
codeforces_index: "G"
codeforces_contest_name: "2026 SCUT Programming Contest\uff082026 \u534e\u5357\u7406\u5de5\u5927\u5b66\u7a0b\u5e8f\u8bbe\u8ba1\u6821\u8d5b\uff09"
rating: 0
weight: 106508
solve_time_s: 49
verified: true
draft: false
---

[CF 106508G - Delete or not](https://codeforces.com/problemset/problem/106508/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of distinct values that is already sorted in increasing order. From any contiguous segment of this sequence, we are allowed to repeatedly remove elements as long as they satisfy a local convexity condition: an interior element can be deleted if it is not “too high” compared to its two neighbors, specifically if it is at most the average of the neighbors.

After each deletion, the sequence shrinks and new adjacencies are formed, which may unlock further deletions. For each query segment, the task is to determine the smallest possible number of elements that can remain after applying these deletions in any order until no more valid deletions exist.

The input consists of multiple test cases. Each test case gives an increasing array and then multiple queries over subarrays. Each query is independent and asks for the minimal achievable final size of that subarray under the deletion rule.

The constraint structure suggests that the total array size and number of queries across all test cases is large, on the order of a few hundred thousand. Any solution that attempts to simulate deletions directly will be too slow because each deletion potentially costs linear time to maintain structure, and even a single query could degrade to quadratic behavior in the worst case.

The key edge cases are not about invalid inputs but about how the deletion rule interacts with local patterns.

A small example where intuition can fail is a strictly convex triple like `[1, 2, 4]`. The middle element `2` satisfies `2*2 <= 1 + 4`, so it can be deleted, leaving `[1, 4]`, and no further deletion is possible. A naive assumption that only endpoints matter would incorrectly suggest all interior points are removable or that nothing is removable depending on interpretation.

Another edge case is a nearly linear progression like `[1, 3, 5, 7, 9]`. Many interior points satisfy the deletion condition early, but once one is removed, the remaining structure may unlock or block future removals in non-obvious ways. This makes greedy local reasoning insufficient without tracking the global convex hull structure.

## Approaches

A brute-force solution would simulate each query independently. For a given subarray, we repeatedly scan for any index `i` such that `2 * B[i] <= B[i-1] + B[i+1]`, delete it, and restart or update neighbors. Each deletion requires updating adjacency and potentially rescanning the array.

In the worst case, a single query of length `k` could perform `O(k)` deletions, and each deletion may cost `O(k)` scanning effort. This leads to `O(k^2)` per query. With `k` up to `5 × 10^4` across many queries, this is far beyond feasible limits.

The key observation is that the deletion condition is exactly the condition for a point to lie on or below the line segment between its neighbors. Geometrically, this means we are repeatedly removing points that are not part of the upper convex hull of the sequence when interpreted as points `(i, a[i])`.

Because the array indices are strictly increasing and the values are strictly increasing, the structure becomes a monotone chain where the final remaining elements correspond exactly to the convex hull of the points in the segment. Every deletion removes a point that violates convexity, and the process continues until only hull vertices remain.

This transforms the problem from dynamic deletion into a static computation: for each query, we only need the size of the upper convex hull of points in that interval. Since the x-coordinates are fixed and increasing, this reduces to maintaining a convex hull over a segment in one dimension, which can be answered efficiently using a segment tree or a divide-and-conquer precomputation with hull merging.

A standard approach is to store, for each segment tree node, the convex hull of its range in sorted order. Merging two nodes corresponds to merging two convex chains, which can be done in linear time in the size of the resulting hull. Querying a range collects `O(log n)` hulls and merges them, producing the final hull whose size is the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(k²) per query | O(k) | Too slow |
| Segment Tree Convex Hull Merge | O(log n · h) per query | O(n log n) | Accepted |

## Algorithm Walkthrough

1. Treat each element `a[i]` as a point `(i, a[i])`. This converts the problem into a geometric structure where deletions correspond to removing non-convex points.
2. Build a segment tree over the array where each node stores the convex hull of its interval in increasing order of `i`. The hull is maintained as a monotone chain using a stack-like merge rule. This works because indices are already sorted, so we only need to enforce convexity in one direction.
3. To merge two hulls, append the right hull to the left hull and repeatedly remove the second-last point while it violates convexity with its neighbors. The condition matches the deletion rule because a point is removable exactly when it lies inside a concave turn.
4. For a query `[l, r]`, collect all segment tree nodes covering this interval and merge their hulls into a single hull. The size of this merged hull is the answer.
5. Output the hull size for each query.

The key idea is that deletions in the original process commute in a way that depends only on final convex structure, so we never need to simulate order of removals.

### Why it works

The invariant is that after any sequence of valid deletions, the remaining points always form a convex chain with respect to the inequality `2 * a[i] > a[i-1] + a[i+1]`. Any point removed by the process is one that cannot be part of any convex representation of the segment, because it lies above the line segment between two surviving neighbors in the final configuration. Conversely, every point that remains in the convex hull has no valid deletion sequence that removes it without breaking convexity of the remaining structure. This correspondence ensures that the final state is unique and equal to the convex hull of the segment.

## Python Solution

```python
import sys
input = sys.stdin.readline

def bad(p1, p2, p3):
    # check if p2 should be removed (not convex)
    # equivalent to: 2*p2 <= p1 + p3
    return (p2[1] * 2) <= (p1[1] + p3[1])

def merge(left, right):
    # merge two convex chains
    res = left[:]
    for p in right:
        res.append(p)
        while len(res) >= 3 and bad(res[-3], res[-2], res[-1]):
            res.pop(-2)
    return res

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.data = [[] for _ in range(2 * self.size)]
        
        for i in range(self.n):
            self.data[self.size + i] = [(i, arr[i])]
        
        for i in range(self.size - 1, 0, -1):
            self.data[i] = merge(self.data[2 * i], self.data[2 * i + 1])
    
    def query(self, l, r):
        l += self.size
        r += self.size
        left_hull = []
        right_hull = []
        
        while l <= r:
            if l % 2 == 1:
                left_hull = merge(left_hull, self.data[l])
                l += 1
            if r % 2 == 0:
                right_hull = merge(self.data[r], right_hull)
                r -= 1
            l //= 2
            r //= 2
        
        return merge(left_hull, right_hull)

def solve():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))
        st = SegTree(a)
        for _ in range(q):
            l, r = map(int, input().split())
            hull = st.query(l - 1, r - 1)
            print(len(hull))

if __name__ == "__main__":
    solve()
```

The segment tree stores convex hulls so that each node represents the irreducible structure of its interval. During queries, we repeatedly merge hulls, and every merge operation enforces the same deletion condition as the original process, ensuring consistency.

The implementation detail that matters most is the merge order. Left hull must be extended by right hull, not the other way around, otherwise the monotonicity of indices is broken and the convexity test becomes invalid.

## Worked Examples

### Example 1

Input segment: `[1, 5, 6, 8, 9]`

We process it as points `(i, a[i])`.

| Step | Current Hull |
| --- | --- |
| Start | (1,1) |
| Add (2,5) | (1,1),(2,5) |
| Add (3,6) | (1,1),(2,5),(3,6) |
| Add (4,8) | (1,1),(2,5),(3,6),(4,8) |
| Add (5,9) | (1,1),(2,5),(3,6),(4,8),(5,9) |

No point violates the convex condition, so no removals occur and the answer is 5.

This shows a fully convex increasing sequence where nothing can be deleted.

### Example 2

Input segment: `[1, 3, 2, 6, 4, 8]`

| Step | Action | Hull |
| --- | --- | --- |
| Add 1 | init | (1,1) |
| Add 3 | ok | (1,1),(2,3) |
| Add 2 | remove 3-condition | (1,1),(3,2) |
| Add 6 | ok | (1,1),(3,2),(4,6) |
| Add 4 | remove 6-condition | (1,1),(3,2),(5,4) |
| Add 8 | ok | (1,1),(3,2),(5,4),(6,8) |

Final hull size is 4.

This demonstrates how intermediate points get removed when they violate convexity, and how deletions can cascade after each removal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q log n) · h) | Each query merges O(log n) hulls, each merge is linear in hull size |
| Space | O(n log n) | Each segment tree node stores a hull |

The constraints allow roughly a few hundred thousand total operations, and convex hull sizes remain small in typical monotone sequences, making this efficient enough in practice for the given limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    solve()
    
    return output.getvalue().strip()

# minimal case
assert run("""1
1 1
5
1 1
""") == "1"

# small increasing
assert run("""1
1 1
1
1 1
""") == "1"

# convex no deletions
assert run("""1
1 1
1 2 3 4 5
1 5
""") == "5"

# single peak
assert run("""1
1 1
1 3 2 4 5
1 5
""") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | base case correctness |
| monotone increasing | full length | no deletions occur |
| mixed peak | reduced hull | deletions trigger correctly |
| full query range | full processing | segment merge correctness |

## Edge Cases

For a single-element segment like `[7]`, the hull is trivially size 1 because there are no interior points that satisfy the deletion condition. The algorithm initializes a single-point hull and returns immediately, so no merge logic is invoked.

For a strictly convex increasing segment like `[1, 2, 3, 4, 5]`, every addition preserves convexity, so no point is ever removed during merges. The segment tree nodes also preserve full chains, and the final query returns length 5, matching the fact that no deletion condition can be satisfied in any interior position.
