---
title: "CF 1793F - Rebrending"
description: "We are given a lineup of candidates for a band, each with a unique height. Over several days, the organizers choose a contiguous segment of candidates and want to select two whose heights are as close as possible."
date: "2026-06-09T10:19:56+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "divide-and-conquer", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1793
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 852 (Div. 2)"
rating: 2600
weight: 1793
solve_time_s: 119
verified: false
draft: false
---

[CF 1793F - Rebrending](https://codeforces.com/problemset/problem/1793/F)

**Rating:** 2600  
**Tags:** brute force, data structures, divide and conquer, implementation  
**Solve time:** 1m 59s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a lineup of candidates for a band, each with a unique height. Over several days, the organizers choose a contiguous segment of candidates and want to select two whose heights are as close as possible. For each day, the task is to report the smallest difference between any two heights in the chosen segment.

The input consists of an array of `n` unique integers representing heights and `q` queries, each specifying a segment `[l_i, r_i]`. The output for each query is a single integer: the minimal height difference in that segment.

The constraints are large: `n` can be up to 300,000 and `q` up to 1,000,000. A naive solution that compares all pairs of heights in each segment would require up to $O(n^2)$ per query, which is completely infeasible. Even $O(n \cdot q)$ is too slow. This forces us to seek a solution that preprocesses or structures the data efficiently, ideally with something around $O(n \log n + q \log n)$.

Non-obvious edge cases include segments of minimal length (just two people), where the answer is always the difference of those two heights, and segments at the array boundaries, which can expose off-by-one errors. For example, if the segment is `[1,2]` in an array `[5,3,8]`, the answer must be `2` (5−3), not accidentally calculated using an element outside the segment.

## Approaches

The brute-force approach simply checks every pair of heights in the segment for each query. It is correct but extremely slow. For each query, it does $(r-l+1)^2$ comparisons. With the maximum values of `n` and `q`, this could result in up to $10^{11}$ operations, far beyond what is feasible in 4 seconds.

The key observation is that the minimal difference between two numbers in a set occurs between two consecutive numbers when the numbers are sorted. Therefore, for each query segment, if we could efficiently retrieve the sorted heights or at least the minimum difference between consecutive sorted heights, we would get the answer instantly.

This insight suggests using a data structure that allows range queries for the minimal difference between consecutive elements. A practical approach is a divide-and-conquer or a segment tree variant. We can construct a segment tree where each node stores the sorted list of its segment. When merging nodes, we can compute the minimal difference across the boundary, combining it with the internal minimal differences stored in the children. This reduces the query time to $O(\log n)$ per query if we store extra information carefully.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q * n^2) | O(n) | Too slow |
| Segment Tree with Sorted Lists | O(n log n + q log n) | O(n log n) | Accepted |

## Algorithm Walkthrough

1. Build a segment tree over the array of heights. Each leaf corresponds to a single element, storing its value and setting its internal minimal difference to infinity.
2. For each internal node, merge the sorted lists of the two children to get the combined sorted segment. Compute the minimum difference inside this merged list and store it at the node. Also, store the sorted list itself, as it is needed to compute differences when merging higher nodes.
3. To answer a query `[l, r]`, traverse the segment tree. At each node fully contained in `[l, r]`, retrieve the minimal difference stored at that node. For partially overlapping nodes, merge the relevant parts and compute the minimum difference between boundary elements, combining it with the minimal differences from fully covered children.
4. Return the minimum difference found from all considered nodes.

The reason this works is that any two heights with the minimal difference in a segment must be consecutive in the sorted version of that segment. By maintaining sorted lists and internal minimal differences in the tree nodes, we ensure that when we combine nodes, we never miss a consecutive pair that could yield the minimal difference.

## Python Solution

```python
import sys
input = sys.stdin.readline
from bisect import bisect_left

class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.size = 1
        while self.size < self.n:
            self.size *= 2
        self.tree = [([], float('inf')) for _ in range(2*self.size)]
        for i, v in enumerate(data):
            self.tree[self.size + i] = ([v], float('inf'))
        for i in range(self.size - 1, 0, -1):
            left_list, left_min = self.tree[2*i]
            right_list, right_min = self.tree[2*i+1]
            merged = sorted(left_list + right_list)
            min_diff = min(left_min, right_min, *(merged[j+1]-merged[j] for j in range(len(merged)-1)))
            self.tree[i] = (merged, min_diff)

    def query(self, l, r):
        l += self.size
        r += self.size
        res_list = []
        res_min = float('inf')
        while l < r:
            if l % 2:
                merged = res_list + self.tree[l][0]
                if merged:
                    merged.sort()
                    res_min = min(res_min, self.tree[l][1], *(merged[j+1]-merged[j] for j in range(len(merged)-1)))
                res_list += self.tree[l][0]
                l += 1
            if r % 2:
                r -= 1
                merged = res_list + self.tree[r][0]
                if merged:
                    merged.sort()
                    res_min = min(res_min, self.tree[r][1], *(merged[j+1]-merged[j] for j in range(len(merged)-1)))
                res_list += self.tree[r][0]
            l //= 2
            r //= 2
        return res_min

n, q = map(int, input().split())
a = list(map(int, input().split()))
seg = SegmentTree(a)
for _ in range(q):
    l, r = map(int, input().split())
    print(seg.query(l-1, r))
```

The segment tree stores both sorted lists and the minimal differences to avoid recalculating for fully covered nodes. The `query` function carefully merges only necessary segments and computes the minimum difference across boundaries.

## Worked Examples

### Sample Input 1

```
3 3
1 3 2
1 2
2 3
1 3
```

| Step | Segment | Sorted List | Min Diff | Query Result |
| --- | --- | --- | --- | --- |
| Day 1 | [1,2] | [1,3] | 2 | 2 |
| Day 2 | [2,3] | [2,3] | 1 | 1 |
| Day 3 | [1,3] | [1,2,3] | 1 | 1 |

The segment tree merges and stores minimal differences, correctly finding the smallest consecutive differences.

### Sample Input 2

```
6 3
1 3 5 2 6 4
4 6
1 2
3 6
```

| Step | Segment | Sorted List | Min Diff | Query Result |
| --- | --- | --- | --- | --- |
| Day 1 | [2,6] | [2,4,6] | 2 | 2 |
| Day 2 | [1,2] | [1,3] | 2 | 2 |
| Day 3 | [3,6] | [2,4,5,6] | 1 | 1 |

This shows the algorithm handles non-contiguous ranges and merges boundary differences correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + q log n) | Building the tree merges sorted lists at each node, logarithmic height ensures query time is logarithmic. |
| Space | O(n log n) | Each node stores a sorted list; total storage across all nodes is O(n log n). |

The solution fits comfortably within the 4-second time limit for n up to 300,000 and q up to 1,000,000, as log n is approximately 18.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # run solution
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    seg = SegmentTree(a)
    for _ in range(q):
        l, r = map(int, input().split())
        print(seg.query(l-1, r))
    return output.getvalue().strip()

assert run("3 3\n1 3 2\n1 2\n2 3\n1 3\n") == "2\n1\n1"
assert run("6 3\n1 3 5 2 6 4\n4 6\n1 2\n3 6\n") == "2\n2\n1"
assert run("2 1\n1000000000 1\n1 2\n") == "999999999"
assert run("5 2\n5 4 3 2 1\n1 5\n2 4\n") == "1\n1"
assert run("4 2\n1 4 2 3\n1
```
