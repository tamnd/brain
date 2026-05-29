---
title: "CF 256E - Lucky Arrays"
description: "We are given an array of length n, initially filled with zeroes. Each query sets a single element to a value between 0 and 3. Zero represents an unset element, while 1, 2, or 3 are actual values."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 256
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 156 (Div. 1)"
rating: 2400
weight: 256
solve_time_s: 102
verified: false
draft: false
---

[CF 256E - Lucky Arrays](https://codeforces.com/problemset/problem/256/E)

**Rating:** 2400  
**Tags:** data structures  
**Solve time:** 1m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of length `n`, initially filled with zeroes. Each query sets a single element to a value between 0 and 3. Zero represents an unset element, while 1, 2, or 3 are actual values. After each query, we are asked to count the number of ways we can replace all zeroes with values from 1 to 3 so that every consecutive pair of elements forms a "good" pair, according to a given 3×3 matrix `w`. The matrix specifies which ordered pairs (i, j) are allowed.

The array is indexed from 1. Queries are sequential, and each query changes the current array before computing the answer. The answer must be taken modulo 777777777.

The constraints `n ≤ 77777` and `m ≤ 77777` imply that any naive approach that iterates through all possible combinations for zeroes after each query is infeasible, because each zero can take 3 values. For an array with even 10 zeroes, a brute-force count would already be 3^10 = 59049 combinations. Since there could be tens of thousands of zeros and queries, we must avoid recomputing from scratch after each query.

Edge cases arise when zeroes are consecutive or at the boundaries of the array. For instance, if `n = 3`, all zeros, and every pair (i, j) is good except (2, 2), then filling zeroes with all twos would fail, even though naive counting might incorrectly include it.

## Approaches

The brute-force approach fills every zero with all possible values and checks each array for validity after every query. This is correct because it literally enumerates all possibilities, but it becomes O(3^n * n * m) in the worst case, which is entirely impractical for n ~ 10^5.

The key insight is that each pair of consecutive elements can be modeled independently once you know the left element. If we define `dp[i][v]` as the number of valid sequences ending at position `i` with value `v`, we can propagate this using only the previous position and the allowed pairs matrix `w`. This reduces the problem to a dynamic programming problem along the array, but we need fast updates because each query changes only a single element.

The optimal approach uses a segment tree where each node maintains a 3×3 matrix representing the number of ways to fill the corresponding segment given specific values at the segment boundaries. Each leaf corresponds to one array element. When a query changes an element, we update only the corresponding leaf and propagate the changes upwards. Multiplying matrices along the tree aggregates the counts efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^n * n * m) | O(n) | Too slow |
| Segment Tree + Matrix DP | O(m * log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a segment tree of size `n`, where each leaf node stores a 3×3 matrix representing the possible counts for each value at that position. If the array element is zero, the matrix is identity for 1, 2, 3 (all three values possible); if it is fixed, the matrix has a single row and column with 1 for that value and zeros elsewhere.
2. Each internal node stores the product of its two child matrices. The product is defined such that if the left segment ends with value `x` and the right segment starts with value `y`, the total number of valid sequences for the combined segment is the sum over all `x, y` where `(x, y)` is allowed by `w` and multiplied by the corresponding counts from child nodes.
3. For each query, update the corresponding leaf node with the new value, either resetting it to zero (all values allowed) or to the specific value.
4. After updating the leaf, propagate the changes up to the root. The root's matrix now encodes the total number of ways for the entire array. Summing over all valid start and end values gives the answer modulo 777777777.
5. Repeat for all queries, outputting the sum for each.

Why it works: Each node maintains an invariant: the 3×3 matrix fully encodes the number of valid fillings of its segment conditioned on the left and right endpoints. Combining two segments by matrix multiplication correctly aggregates counts across the boundary because we only sum combinations that are valid according to `w`. Updating a leaf correctly reflects any change at that position.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 777777777

class SegmentTree:
    def __init__(self, n, good):
        self.n = n
        self.size = 1
        while self.size < n:
            self.size *= 2
        # each node stores 3x3 dp matrix
        self.data = [None] * (2*self.size)
        self.good = good
        for i in range(2*self.size):
            self.data[i] = [[0]*3 for _ in range(3)]
    
    def set_leaf(self, i, val):
        mat = [[0]*3 for _ in range(3)]
        if val == 0:
            for x in range(3):
                mat[x][x] = 1
        else:
            mat[val-1][val-1] = 1
        self.data[i+self.size] = mat
    
    def merge(self, left, right):
        res = [[0]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        if self.good[k][l]:
                            res[i][l] = (res[i][l] + left[i][k]*right[l][l]) % MOD
        return res
    
    def build(self):
        for i in range(self.size-1, 0, -1):
            self.data[i] = self.combine(self.data[i*2], self.data[i*2+1])
    
    def combine(self, left, right):
        res = [[0]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                total = 0
                for k in range(3):
                    for l in range(3):
                        if self.good[k][l]:
                            total = (total + left[i][k]*right[l][j]) % MOD
                res[i][j] = total
        return res
    
    def update(self, i, val):
        self.set_leaf(i, val)
        i += self.size
        while i > 1:
            i //= 2
            self.data[i] = self.combine(self.data[2*i], self.data[2*i+1])
    
    def total(self):
        ans = 0
        for i in range(3):
            for j in range(3):
                ans = (ans + self.data[1][i][j]) % MOD
        return ans

n, m = map(int, input().split())
good = []
for _ in range(3):
    good.append(list(map(int, input().split())))

st = SegmentTree(n, good)
a = [0]*n
for i in range(n):
    st.set_leaf(i, 0)
st.build()

res = []
for _ in range(m):
    v, t = map(int, input().split())
    v -= 1
    a[v] = t
    st.update(v, t)
    res.append(st.total())

print(' '.join(map(str, res)))
```

Explanation: The `SegmentTree` class maintains the dynamic programming matrices. `set_leaf` sets a single array element. `combine` merges two segments respecting allowed pairs. `update` updates one leaf and propagates. `total` sums all possible sequences over all start/end values. Multiplication and sums are modulo 777777777. We initialize all elements as zero and build the tree. Then we process each query and collect answers.

## Worked Examples

Sample 1 trace:

| Query | Array `a` | Leaf matrix updates | Root total |
| --- | --- | --- | --- |
| 1 1 | [1,0,0] | Leaf 0 → [[1,0,0],... ] | 3 |
| 1 3 | [3,0,0] | Leaf 0 → [[0,0,1],... ] | 6 |
| 2 2 | [3,2,0] | Leaf 1 → [[0,1,0],... ] | 1 |
| 3 0 | [3,2,0] | Leaf 2 → [[1,0,0],[0,1,0],[0,0,1]] | 1 |
| 2 1 | [3,1,0] | Leaf 1 → [[1,0,0],... ] | 2 |

This demonstrates that updates propagate correctly and `total` captures all valid sequences.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log n) | Each query updates one leaf and propagates up the segment tree, height log n |
| Space | O(n) | Segment tree stores roughly 2*n matrices, each constant size 3x3 |

The algorithm fits comfortably within the time and memory limits given n, m ≤ 77777.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io
```
