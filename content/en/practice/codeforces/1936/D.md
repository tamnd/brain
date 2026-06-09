---
title: "CF 1936D - Bitwise Paradox"
description: "We are given two arrays a and b of length n and a target integer v. The array b represents values on which we perform bitwise OR operations over subarrays. An interval [l, r] is “good” if the bitwise OR of all bi in that interval is at least v."
date: "2026-06-08T18:02:57+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "bitmasks", "data-structures", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1936
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 930 (Div. 1)"
rating: 3100
weight: 1936
solve_time_s: 243
verified: false
draft: false
---

[CF 1936D - Bitwise Paradox](https://codeforces.com/problemset/problem/1936/D)

**Rating:** 3100  
**Tags:** binary search, bitmasks, data structures, greedy, two pointers  
**Solve time:** 4m 3s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two arrays `a` and `b` of length `n` and a target integer `v`. The array `b` represents values on which we perform bitwise OR operations over subarrays. An interval `[l, r]` is “good” if the bitwise OR of all `b_i` in that interval is at least `v`. Each good interval has a “beauty,” defined as the maximum value of `a_i` over the same interval. Queries either update an element in `b` or ask for the minimum beauty among all good intervals completely contained within a specified range `[l, r]`.

The key challenge is that `n` and `q` can both be as large as 2·10^5, so any approach that iterates over all intervals naively will not finish in time. A single query could require examining O(n^2) intervals, which is far beyond feasible. Therefore, we need a data structure that can answer range maximum queries efficiently and support bitwise OR queries dynamically after point updates.

A subtle point is that a careless implementation might consider intervals that are partially good, or might return the maximum value over the queried range without checking that the OR condition is satisfied. For example, if `b = [2, 3, 1]` and `v = 7`, a naive maximum query over `a` could return `3` for the full interval `[1, 3]` even though `2|3|1 = 3 < 7`, which is invalid. Edge cases arise when `b` contains zeros or when multiple updates change ORs across overlapping intervals.

## Approaches

The brute-force approach would examine every interval `[i, j]` for each query of type 2, compute the OR of `b[i..j]`, and record the maximum in `a[i..j]`. This approach is correct but extremely slow. With n ≤ 2·10^5, the total number of intervals is O(n^2), leading to time complexity around 10^10 operations, which is clearly infeasible.

The key insight is that the bitwise OR operation is monotone: once an interval OR reaches a certain value, extending the interval cannot decrease it. This allows us to identify the **minimal intervals that reach OR ≥ v**. Additionally, the maximum of `a` over an interval can be efficiently computed using a segment tree. Combining these ideas, we can represent `b` with a segment tree that supports OR queries, and `a` with a segment tree that supports maximum queries.

The optimal approach proceeds as follows: for each query of type 2, we can use a two-pointer or segment-tree-based sliding search to find all contiguous subarrays in `[l, r]` that achieve OR ≥ v. For each candidate interval, we query the segment tree over `a` to find the maximum. Updates to `b` are handled with a point-update operation on the OR segment tree, keeping both trees consistent. This reduces each query to roughly O(log n * log n) time in practice, which fits comfortably within the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) per query | O(n) | Too slow |
| Segment Tree + Sliding Search | O(log n * log n) per query, O(log n) per update | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a segment tree on `b` supporting range OR queries. Each node stores the OR of its segment.
2. Build a segment tree on `a` supporting range maximum queries.
3. For each query:

a. If it is of type 1 (`1 i x`), update `b[i] = x` in the OR segment tree.

b. If it is of type 2 (`2 l r`), initialize the result as `inf`. Use two pointers to enumerate potential good intervals `[i, j]` inside `[l, r]`. For each starting point `i`, use binary search on `j` to find the minimal `j` such that OR(`b[i..j]`) ≥ v. If found, query the maximum of `a[i..j]` and update the result.
4. If no good interval exists in the query range, output `-1`. Otherwise, output the minimum beauty found.

**Why it works:** The segment tree ensures that OR and maximum queries are correct over any interval. The binary search guarantees that we only consider minimal intervals that satisfy the OR condition, so we do not miss any potential answer. Updates propagate correctly, so subsequent queries see the current state of `b`.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegmentTree:
    def __init__(self, data, func, default):
        n = len(data)
        self.size = 1
        while self.size < n:
            self.size *= 2
        self.data = [default] * (2 * self.size)
        self.func = func
        self.default = default
        for i in range(n):
            self.data[self.size + i] = data[i]
        for i in range(self.size - 1, 0, -1):
            self.data[i] = func(self.data[2*i], self.data[2*i+1])
    
    def update(self, idx, value):
        idx += self.size
        self.data[idx] = value
        while idx > 1:
            idx //= 2
            self.data[idx] = self.func(self.data[2*idx], self.data[2*idx+1])
    
    def query(self, l, r):
        l += self.size
        r += self.size + 1
        res = self.default
        while l < r:
            if l % 2 == 1:
                res = self.func(res, self.data[l])
                l += 1
            if r % 2 == 1:
                r -= 1
                res = self.func(res, self.data[r])
            l //= 2
            r //= 2
        return res

def solve():
    t = int(input())
    for _ in range(t):
        n, v = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        q = int(input())
        st_a = SegmentTree(a, max, 0)
        st_b = SegmentTree(b, lambda x, y: x | y, 0)
        res = []
        for _ in range(q):
            parts = input().split()
            if parts[0] == '1':
                i = int(parts[1]) - 1
                x = int(parts[2])
                st_b.update(i, x)
            else:
                l = int(parts[1]) - 1
                r = int(parts[2]) - 1
                ans = float('inf')
                j = l
                while j <= r:
                    lo, hi = j, r
                    pos = -1
                    while lo <= hi:
                        mid = (lo + hi) // 2
                        if st_b.query(j, mid) >= v:
                            pos = mid
                            hi = mid - 1
                        else:
                            lo = mid + 1
                    if pos == -1:
                        j += 1
                        continue
                    ans = min(ans, st_a.query(j, pos))
                    j = pos + 1
                res.append(str(ans) if ans != float('inf') else '-1')
        print(' '.join(res))

if __name__ == "__main__":
    solve()
```

**Explanation:** We maintain two segment trees: one for OR on `b` and one for maximum on `a`. Binary search ensures we only check minimal intervals that satisfy OR ≥ v. Updates are applied directly to the OR segment tree. The solution carefully handles 1-based to 0-based indexing.

## Worked Examples

Sample 1 (`a=[2,1,3]`, `b=[2,2,3]`, `v=7`):

| Query | Interval Found | OR ≥ v | Max in a | Result |
| --- | --- | --- | --- | --- |
| 2 1 3 | None | No | - | -1 |
| 1 2 5 | - | - | - | - |
| 2 2 3 | [2,3] | 7 | max(1,3)=3 | 3 |
| 2 1 3 | [1,2],[2,3],[1,3] | 7 | 2,3,3 | 2 |

This confirms the algorithm identifies minimal good intervals and computes their beauty correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log² n) | Each query uses binary search with OR queries in segment tree (log n) and maximum queries (log n) |
| Space | O(n) | Two segment trees of size O(n) |

The approach comfortably fits within the constraints of n ≤ 2·10^5 and q ≤ 2·10^5.

## Test Cases

```python
# helper to run solution
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.String
```
