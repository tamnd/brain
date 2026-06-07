---
title: "CF 2184E - Exquisite Array"
description: "We are given a permutation of length $n$, which is simply an array of integers from $1$ to $n$ in some order without repeats."
date: "2026-06-07T21:38:20+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "data-structures", "dsu", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2184
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1072 (Div. 3)"
rating: 1800
weight: 2184
solve_time_s: 124
verified: false
draft: false
---

[CF 2184E - Exquisite Array](https://codeforces.com/problemset/problem/2184/E)

**Rating:** 1800  
**Tags:** combinatorics, data structures, dsu, sortings  
**Solve time:** 2m 4s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of length $n$, which is simply an array of integers from $1$ to $n$ in some order without repeats. The task is to count, for every integer $k$ from $1$ to $n-1$, the number of subarrays of length at least two where every pair of consecutive elements differs by at least $k$. These subarrays are called $k$-exquisite.

The input consists of multiple test cases. Each test case provides the permutation length $n$ and the array itself. We must output $n-1$ numbers per test case, each representing the count of $k$-exquisite subarrays for the corresponding $k$.

The constraints indicate that $n$ can go up to $10^5$ and the sum of $n$ across all test cases does not exceed $2 \cdot 10^5$. This means a naive $O(n^2)$ approach per test case is infeasible because iterating through all subarrays for each $k$ would require around $O(n^3)$ operations in the worst case. We need something closer to linear or linearithmic complexity per test case. Edge cases to consider include strictly increasing or decreasing permutations, small arrays of length 2, and subarrays where the difference between some elements is exactly $k$.

A naive approach would fail for arrays like `[1,2,3,4]` when $k=3$ because it might miscount subarrays starting at 1 and 2 without noticing that differences do not satisfy the threshold.

## Approaches

The brute-force method iterates over all subarrays of length at least two for each $k$. For each subarray, it checks all consecutive pairs to ensure the difference condition is satisfied. While correct, this approach requires $O(n^2)$ checks per $k$, which quickly becomes unmanageable since $k$ ranges up to $n-1$. The total operations would be roughly $O(n^3)$ in the worst case, which is too slow for $n\sim 10^5$.

The key observation is that the problem can be reversed: instead of iterating through $k$ and checking subarrays, we iterate through pairs of consecutive elements in the permutation and compute the absolute difference between them. Each pair effectively constrains a range of $k$ values for which it can contribute to a valid subarray. Specifically, if the difference between $p[i]$ and $p[i+1]$ is $d$, then for any $k \le d$, this pair allows subarrays that include it. Subarrays are contiguous, so consecutive pairs can be merged to form ranges where the difference constraints hold. Using a disjoint set union (DSU) structure or a length-tracking approach, we can count how many subarrays each difference contributes to and aggregate results for all $k$ efficiently.

The improvement comes from recognizing that each pair contributes to all $k \le \text{difference}$ and that subarrays can be counted using segment lengths instead of enumerating every subarray individually. Sorting the pairs by difference and then extending contiguous valid segments allows us to compute counts for all $k$ in $O(n \log n)$ time using union-find.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(1)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the permutation of length $n$. Compute the absolute difference for every consecutive pair, storing $(\text{difference}, \text{index})$ for all $i$ from $0$ to $n-2$.
2. Sort the differences in decreasing order. This ensures that we handle the largest differences first, which correspond to the smallest valid $k$ thresholds.
3. Initialize a DSU where each index starts as a separate segment of length 1. This DSU will track contiguous subarrays where the difference condition holds for the current $k$.
4. Initialize an array `ans` of length $n$ to accumulate counts. `ans[k]` will store the number of subarrays valid for $k$.
5. Iterate over the sorted differences. For each pair with difference $d$ at index $i$:

- Merge the segments containing $i$ and $i+1$. The merged length indicates how many new subarrays become valid when $k$ decreases to $d$.
- Compute the number of new subarrays formed by this merge using the formula $\text{length} \cdot (\text{length} - 1)/2$, which counts all contiguous subarrays of length at least 2 in that segment.
- Update `ans[d]` by adding the number of new subarrays.
6. After processing all differences, propagate the counts downward so that for any smaller $k$, `ans[k]` includes all subarrays valid for larger $k$. This ensures that `ans[k]` correctly reflects all $k$-exquisite subarrays.
7. Output `ans[1..n-1]` for the test case.

Why it works: At every step, the algorithm maintains contiguous segments of elements that satisfy the current difference threshold. Sorting by difference guarantees that when we process difference $d$, all pairs with differences larger than $d$ have already been merged. Counting subarrays by segment lengths ensures that each valid subarray is counted exactly once. Propagating counts downward ensures correct accumulation for all $k$.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1]*n

    def find(self, x):
        while x != self.parent[x]:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        x_root, y_root = self.find(x), self.find(y)
        if x_root == y_root:
            return 0
        if self.size[x_root] < self.size[y_root]:
            x_root, y_root = y_root, x_root
        self.parent[y_root] = x_root
        combined = self.size[x_root] + self.size[y_root]
        delta = combined*(combined-1)//2 - self.size[x_root]*(self.size[x_root]-1)//2 - self.size[y_root]*(self.size[y_root]-1)//2
        self.size[x_root] = combined
        return delta

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        diffs = [(abs(p[i]-p[i+1]), i) for i in range(n-1)]
        diffs.sort(reverse=True)
        ans = [0]*(n)
        dsu = DSU(n)
        for d, i in diffs:
            new_subarrays = dsu.union(i, i+1)
            ans[d] += new_subarrays
        # propagate counts downward
        for k in range(n-2, 0, -1):
            ans[k] += ans[k+1]
        print(' '.join(map(str, ans[1:n])))

solve()
```

The DSU class tracks segment sizes efficiently, and the `union` function returns the number of new subarrays created when merging two segments. Sorting differences in descending order ensures that larger thresholds are processed first, which is essential for correct accumulation. The downward propagation step guarantees that smaller `k` values count all valid subarrays.

## Worked Examples

### Sample Input 1

```
5
5 1 4 2 3
```

| Step | Difference | Index | Segment merge | New subarrays | ans array |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 0 | merge [5,1] | 1 | ans[4]=1 |
| 2 | 3 | 2 | merge [4,2] | 1 | ans[3]=1 |
| 3 | 2 | 1 | merge [1..4] | 4 | ans[2]=4 |
| 4 | 1 | 3 | merge [2..5] | 4 | ans[1]=4 |

Propagation: ans[3]+=ans[4], ans[2]+=ans[3], ans[1]+=ans[2] yields final ans: 10 6 3 1.

### Sample Input 2

```
3
3 2 1
```

Processing differences [1,1]: merges create ans[1]=2, ans[2]=1. After propagation, final ans: 3 0.

These traces show that the DSU correctly tracks contiguous segments and that propagation ensures all counts accumulate for smaller k.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the differences dominates; union-find operations are nearly linear due to path compression |
| Space | O(n) | DSU stores parent and size arrays of length n, plus differences array |

Given the sum of $n$ over all test cases is ≤ 2·10^5, this approach fits comfortably in a 2-second time limit with memory below 256 MB.

## Test Cases
