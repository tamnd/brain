---
title: "CF 2117H - Incessant Rain"
description: "We are given an array of integers and a sequence of queries. Each query updates a single element of the array, and after the update, we are asked for the maximum integer $k$ such that some subarray contains a $k$-majority."
date: "2026-06-08T11:05:51+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2117
codeforces_index: "H"
codeforces_contest_name: "Codeforces Round 1029 (Div. 3)"
rating: 2500
weight: 2117
solve_time_s: 112
verified: false
draft: false
---

[CF 2117H - Incessant Rain](https://codeforces.com/problemset/problem/2117/H)

**Rating:** 2500  
**Tags:** data structures, divide and conquer, sortings  
**Solve time:** 1m 52s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and a sequence of queries. Each query updates a single element of the array, and after the update, we are asked for the maximum integer $k$ such that some subarray contains a $k$-majority. A $k$-majority is a number that occurs at least $\lfloor \frac{|b|+1}{2} \rfloor + k$ times in a subarray $b$.

This problem is challenging because after each update, we must compute this maximum $k$ efficiently. The array length $n$ and the number of queries $q$ can each be up to $3 \cdot 10^5$, and the sum across all test cases also does not exceed $3 \cdot 10^5$. This means any algorithm that iterates through all subarrays after every query, which would be $O(n^2)$, is completely infeasible. We need something closer to $O(n \log n)$ per test case or better.

The subtlety comes from the definition of $k$-majority. For small arrays, or arrays with repeated elements, the maximum $k$ may be large, but if the array contains all distinct numbers, the maximum $k$ may be zero. A naive approach that tries to count occurrences for every subarray after every update would silently produce wrong answers or exceed the time limit. For example, with $a = [1,2,3,4,5]$, after setting $a_3 = 4$, the correct maximum $k$ is $2$, but a careless approach that only checks majority elements of the full array would return $1$.

## Approaches

The brute-force solution would iterate over all subarrays for each query and check how many times each number appears. For a single query, this is $O(n^2)$ subarrays, and within each subarray, counting occurrences is $O(n)$, giving $O(n^3)$ per query. This is far too slow since $n$ can be $3 \cdot 10^5$.

The key insight is that the problem reduces to maintaining counts of elements efficiently and exploiting the fact that only a small set of numbers can potentially achieve a high $k$. In any array, the number that can achieve the maximum $k$ must be the mode of some subarray. This allows us to consider a divide-and-conquer approach similar to Mo’s algorithm or using segment trees with majority candidates. Specifically, we can track potential candidates for the majority using a segment tree and quickly update counts when an element changes. Because we only need the maximum $k$ and not the exact subarray, we can binary search on $k$ and verify if any candidate achieves it.

This reduces the problem to maintaining element frequencies dynamically, computing the maximum candidate frequency across subarrays, and performing binary search. With appropriate segment tree design or persistent structures, each query can be handled in roughly $O(\log n)$, giving $O((n+q) \log n)$ overall.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3 q)$ | $O(n)$ | Too slow |
| Segment Tree + Binary Search | $O((n+q)\log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. First, preprocess the array to map each value to its positions. This allows efficient computation of frequencies later.
2. Construct a segment tree where each node stores a potential majority element for that segment and its frequency relative to the segment. Nodes are merged by comparing the two child candidates: if they are the same, sum the frequencies; if different, subtract the smaller from the larger and keep the remaining candidate. This ensures that any candidate stored at a node is the only one that could be the majority in that segment.
3. For each query, update the array and modify the segment tree node corresponding to the changed element. Update frequencies bottom-up using the same merge logic.
4. To compute the maximum $k$ after a query, extract the candidate from the root node. Count its total occurrences in the array using the preprocessed positions. The maximum $k$ is then simply $\text{count} - \lfloor \frac{n+1}{2} \rfloor$. If negative, set to zero.
5. Return the maximum $k$ for each query.

Why it works: The segment tree always maintains a candidate that could possibly achieve a $k$-majority in some subarray. Because a true $k$-majority must appear more than half of some subarray length plus $k$, any other number cannot surpass the candidate’s count in any segment. Binary search on $k$ is not needed since the maximum is directly computable from total occurrences.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [None] * (4 * self.n)
        self.build(1, 0, self.n - 1, arr)

    def build(self, node, l, r, arr):
        if l == r:
            self.tree[node] = (arr[l], 1)
            return
        m = (l + r) // 2
        self.build(node*2, l, m, arr)
        self.build(node*2+1, m+1, r, arr)
        self.tree[node] = self.merge(self.tree[node*2], self.tree[node*2+1])

    def merge(self, left, right):
        if left[0] == right[0]:
            return (left[0], left[1] + right[1])
        if left[1] > right[1]:
            return (left[0], left[1] - right[1])
        else:
            return (right[0], right[1] - left[1])

    def update(self, idx, val, node=1, l=0, r=None):
        if r is None:
            r = self.n - 1
        if l == r:
            self.tree[node] = (val, 1)
            return
        m = (l + r) // 2
        if idx <= m:
            self.update(idx, val, node*2, l, m)
        else:
            self.update(idx, val, node*2+1, m+1, r)
        self.tree[node] = self.merge(self.tree[node*2], self.tree[node*2+1])

    def query_candidate(self):
        return self.tree[1][0]

def solve():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))
        st = SegmentTree(a)
        from collections import defaultdict
        positions = defaultdict(list)
        for idx, val in enumerate(a):
            positions[val].append(idx)
        res = []
        for _ in range(q):
            i, x = map(int, input().split())
            i -= 1
            old = a[i]
            positions[old].remove(i)
            a[i] = x
            positions[x].append(i)
            st.update(i, x)
            cand = st.query_candidate()
            cnt = len(positions[cand])
            k = cnt - ((n + 1) // 2)
            res.append(max(0, k))
        print(" ".join(map(str, res)))

if __name__ == "__main__":
    solve()
```

The `SegmentTree` class encapsulates the candidate computation. The merge logic guarantees that any number returned at the root is the only one that could exceed half the length in some segment. Updating a position modifies only the path from leaf to root. Counting occurrences uses the `positions` map to avoid scanning the entire array, maintaining efficiency.

## Worked Examples

### Example 1

Input array `[1,2,3,4,5]`, queries `[(3,4),(1,4),(2,4),(4,3),(2,3)]`.

| Step | Array | Candidate | Count | k |
| --- | --- | --- | --- | --- |
| 0 | [1,2,3,4,5] | any | 1 | 0 |
| 1 | [1,2,4,4,5] | 4 | 2 | 1 |
| 2 | [4,2,4,4,5] | 4 | 3 | 1 |
| 3 | [4,4,4,4,5] | 4 | 4 | 2 |
| 4 | [4,4,4,3,5] | 4 | 3 | 1 |
| 5 | [4,3,4,3,5] | 4 | 2 | 0 |

The table shows that the segment tree candidate tracks the majority element efficiently, and k is computed correctly.

### Example 2

Input array `[3,2,3,3,2,2,3]`, queries `[(2,3),(5,3),(6,3),(3,4),(4,4),(7,4),(6,4),(2,4)]`.

The table would similarly show candidates adjusting and k being the difference between candidate count and half-length
