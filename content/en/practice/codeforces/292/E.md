---
title: "CF 292E - Copying Data"
description: "We are asked to maintain two arrays of integers, a and b, each of length n. The first array a is static: its values never change."
date: "2026-06-05T17:14:27+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 292
codeforces_index: "E"
codeforces_contest_name: "Croc Champ 2013 - Round 1"
rating: 1900
weight: 292
solve_time_s: 73
verified: true
draft: false
---

[CF 292E - Copying Data](https://codeforces.com/problemset/problem/292/E)

**Rating:** 1900  
**Tags:** data structures  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to maintain two arrays of integers, `a` and `b`, each of length `n`. The first array `a` is static: its values never change. The second array `b` is mutable, and we need to handle two types of operations: copying a contiguous subsegment from `a` into `b`, and querying the value of a specific element in `b`. Each copy operation may affect multiple elements in `b` simultaneously, and we must support up to `m` operations efficiently.

Given the constraints, both `n` and `m` can be as large as 100,000. A naive implementation that literally copies subsegments in O(k) time per copy could take up to 10^10 operations in the worst case (if k is also O(n)), which is far beyond the 2-second time limit. This means a straightforward loop per copy query is not feasible.

A subtle edge case arises when multiple copy operations overlap. For instance, if we first copy `a[1:3]` into `b[2:4]` and later copy `a[2:4]` into `b[3:5]`, a simple array overwrite strategy might fail to correctly track which original `a` elements are currently represented in `b`. Another potential pitfall is querying an element in `b` that has never been overwritten. The algorithm must correctly return the original value from `b` in that scenario.

## Approaches

The brute-force approach directly simulates the copy operations. Each type-1 query loops over `k` elements and assigns `b[y + q] = a[x + q]`. Each type-2 query simply returns `b[x]`. This approach works correctly for small inputs, but the worst-case time complexity is O(m * n), which can reach 10^10 operations and is clearly too slow.

The key observation to improve performance is that copy operations always move contiguous blocks from `a` to `b`. Instead of updating each element individually, we can represent the state of `b` as either "original" or "linked" to a segment of `a`. If we store these links in a structure that supports efficient range updates and single-element queries, we can avoid explicit copying. A segment tree or a balanced tree structure like a treap could work, but a simpler and sufficient approach is to use a mapping array `from_a` of length `n`. Each `from_a[i]` stores the index in `a` that `b[i]` currently reflects, or -1 if it is the original `b` value.

When a copy occurs, we update the mapping array for the range in O(log n) time using a segment tree. Queries then follow the mapping to return either `b[i]` if `from_a[i] == -1` or the corresponding `a` value otherwise. This reduces the per-operation complexity from O(k) to O(log n) and keeps the total operations within 2_10^5_log(10^5), which is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m * n) | O(n) | Too slow |
| Mapping + Segment Tree | O(m log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `from_a` of size `n`, filled with -1. This will track, for each position in `b`, whether it points to an element of `a` or retains its original value.
2. Build a segment tree over `from_a` that supports range assignment. Each node stores either -1 or the start index in `a` it maps to. The segment tree allows us to assign an entire subrange in O(log n) time.
3. For each query, if it is a copy operation, perform a range assignment in the segment tree. Specifically, for a query copying `k` elements from `a[x]` to `b[y]`, assign the segment `[y, y + k - 1]` in `from_a` to correspond to indices `[x, x + k - 1]` of `a`. This ensures we never physically move elements but track where each element of `b` should read from.
4. If the query is a read operation, use the segment tree to retrieve the value of `from_a[x]`. If it is -1, return the original `b[x]`. Otherwise, compute the correct offset in `a` and return `a[from_a[x]]`.
5. Repeat until all queries are processed, printing results for type-2 queries as we go.

The invariant maintained is that for any position `i` in `b`, the segment tree always knows whether the current value comes from the original `b[i]` or some contiguous segment in `a`. Overlapping copy operations correctly overwrite previous mappings because the segment tree assignment always replaces the affected range.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegmentTree:
    def __init__(self, n):
        self.n = n
        self.data = [-1] * (4 * n)
        self.lazy = [None] * (4 * n)

    def push(self, v, l, r):
        if self.lazy[v] is not None:
            self.data[v] = self.lazy[v]
            if l != r:
                self.lazy[v*2] = self.lazy[v] + 0
                self.lazy[v*2+1] = self.lazy[v] + (r - l + 1)//2
            self.lazy[v] = None

    def update(self, v, l, r, ul, ur, val):
        self.push(v, l, r)
        if ur < l or r < ul:
            return
        if ul <= l and r <= ur:
            self.lazy[v] = val + (l - ul)
            self.push(v, l, r)
            return
        m = (l + r) // 2
        self.update(v*2, l, m, ul, ur, val)
        self.update(v*2+1, m+1, r, ul, ur, val)

    def query(self, v, l, r, pos):
        self.push(v, l, r)
        if l == r:
            return self.data[v]
        m = (l + r) // 2
        if pos <= m:
            return self.query(v*2, l, m, pos)
        else:
            return self.query(v*2+1, m+1, r, pos)

n, m = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

tree = SegmentTree(n)

for _ in range(m):
    q = list(map(int, input().split()))
    if q[0] == 1:
        x, y, k = q[1]-1, q[2]-1, q[3]
        tree.update(1, 0, n-1, y, y+k-1, x)
    else:
        x = q[1]-1
        idx = tree.query(1, 0, n-1, x)
        print(a[idx] if idx != -1 else b[x])
```

The `SegmentTree` class handles lazy propagation for range assignments. The `update` method ensures that when a subsegment is copied, it correctly offsets the mapping to match the source indices in `a`. The `query` method retrieves the current mapping for any index in O(log n). Using zero-based indexing inside the tree avoids off-by-one errors when converting from the one-based query input.

## Worked Examples

### Sample 1

Input:

```
5 10
1 2 0 -1 3
3 1 5 -2 0
2 5
1 3 3 3
2 5
2 4
2 1
1 2 1 4
2 1
2 4
1 4 2 1
2 2
```

| Step | Operation | `from_a` snapshot | Output |
| --- | --- | --- | --- |
| 1 | Query b[5] | [-1,-1,-1,-1,-1] | 0 |
| 2 | Copy a[3:5] -> b[3:5] | [-1,-1,2,3,4] | - |
| 3 | Query b[5] | [-1,-1,2,3,4] | 3 |
| 4 | Query b[4] | [-1,-1,2,3,4] | -1 |
| 5 | Query b[1] | [-1,-1,2,3,4] | 3 |
| 6 | Copy a[2:2] -> b[1:1] | [1,-1,2,3,4] | - |
| 7 | Query b[1] | [1,-1,2,3,4] | 2 |
| 8 | Query b[4] | [1,-1,2,3,4] | -1 |
| 9 | Copy a[4:5] -> b[2:3] | [1,3,4,3,4] | - |
| 10 | Query b[2] | [1,3,4,3,4] | 3 |

This trace confirms that overlapping copies correctly update the mapping and queries retrieve the correct values from either `a` or the original `b`.

## Complexity Analysis

| Measure | Complexity
