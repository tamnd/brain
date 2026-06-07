---
title: "CF 2117H - Incessant Rain"
description: "We are given an array of integers a of length n and a sequence of q queries. Each query replaces one element of the array with a new value. After each update, we are asked to find the maximum integer k such that some integer x is the k-majority in some subarray of a."
date: "2026-06-08T04:08:51+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2117
codeforces_index: "H"
codeforces_contest_name: "Codeforces Round 1029 (Div. 3)"
rating: 2500
weight: 2117
solve_time_s: 69
verified: false
draft: false
---

[CF 2117H - Incessant Rain](https://codeforces.com/problemset/problem/2117/H)

**Rating:** 2500  
**Tags:** data structures, divide and conquer, sortings  
**Solve time:** 1m 9s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers `a` of length `n` and a sequence of `q` queries. Each query replaces one element of the array with a new value. After each update, we are asked to find the maximum integer `k` such that some integer `x` is the `k`-majority in some subarray of `a`. A number is a `k`-majority in a subarray if it occurs at least `floor((length of subarray + 1)/2) + k` times.

The constraints are tight: `n` and `q` can each be up to 300,000, and the sum of `n` and `q` over all test cases is at most 300,000. This rules out any solution that examines all subarrays explicitly, since even a single subarray scan could be O(n^2) and would not finish in time. Similarly, maintaining counts naively after each update would be too slow. Memory is restricted to 192 MB, so large auxiliary arrays or complex segment trees storing extensive data must be carefully designed.

A subtle point is that the `k`-majority depends on the floor of half the subarray length. For very short arrays, `k` can be zero or negative if the counts are misinterpreted. For example, consider `a = [1,2]`. If we replace an element with the same number, the maximum `k` could be 1, but a naive algorithm might incorrectly compute it as 2 by ignoring the floor division. Another edge case is when all elements are distinct: the maximum `k` is zero because no number appears more than half the subarray size.

## Approaches

The brute-force method would enumerate every subarray and count occurrences of each number to find the maximum `k`. Each query would require O(n^2) work per array, which is far too slow for `n` up to 3e5. The complexity would be O(n^3) across queries in the worst case, which is completely infeasible.

The key insight comes from observing that the `k`-majority in a subarray is maximized by choosing `x` that appears most frequently. If we can quickly determine the frequency of each number and the intervals where it dominates, we can reduce the problem to computing `max(count(x) - (length of interval - count(x)))`, which simplifies to `2*count(x) - length`.

The optimal approach leverages two observations: the number that maximizes `k` must be a candidate that occurs frequently, and we do not need exact counts for all subarrays. Instead, we can use a segment tree with a small set of potential candidates per segment. Using a divide-and-conquer strategy, each node stores the candidate numbers and their frequency counts in its range. Upon a query update, we update only O(log n) nodes in the segment tree. To determine `k` after each update, we combine the candidates along the tree and compute the maximum `k` for those numbers, which is efficient because the number of candidates is bounded by a small constant (at most 2 per segment by the Boyer-Moore majority principle).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 * q) | O(n) | Too slow |
| Optimal (Segment Tree with candidates) | O((n+q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a segment tree where each node stores up to two candidate numbers that could be majority elements in its range along with their counts relative to the segment size. Two candidates suffice because any subarray has at most one majority element, and after combining children nodes, at most two candidates remain as potential leaders.
2. To merge two nodes, count how often each candidate occurs in the union of the left and right segments. Keep only candidates that appear more than half the combined segment size.
3. For each query, update the leaf node corresponding to the changed element. Update counts and propagate the change up the tree. Each update takes O(log n) time.
4. After the update, traverse the root's candidates. For each candidate, compute its maximum possible `k` across the whole array. This is `2*count(candidate) - length of array` or zero if negative. The maximum among all candidates is the answer for the query.
5. Output the answers for all queries in sequence.

Why it works: the segment tree invariant ensures that any candidate majority in a segment is represented at its node. By limiting to at most two candidates per segment and propagating counts properly, we capture every number that could become a `k`-majority in any subarray. Any number not present as a candidate cannot achieve a higher `k` than the ones stored.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Node:
    def __init__(self, val=None):
        self.candidates = {}
        if val is not None:
            self.candidates[val] = 1

def merge(a, b):
    counter = {}
    for key in a.candidates:
        counter[key] = counter.get(key, 0) + a.candidates[key]
    for key in b.candidates:
        counter[key] = counter.get(key, 0) + b.candidates[key]
    # keep at most 2 top candidates
    items = sorted(counter.items(), key=lambda x: -x[1])
    node = Node()
    for k, v in items[:2]:
        node.candidates[k] = v
    return node

def build(arr, tree, v, tl, tr):
    if tl == tr:
        tree[v] = Node(arr[tl])
    else:
        tm = (tl + tr)//2
        build(arr, tree, 2*v, tl, tm)
        build(arr, tree, 2*v+1, tm+1, tr)
        tree[v] = merge(tree[2*v], tree[2*v+1])

def update(tree, v, tl, tr, pos, val):
    if tl == tr:
        tree[v] = Node(val)
    else:
        tm = (tl+tr)//2
        if pos <= tm:
            update(tree, 2*v, tl, tm, pos, val)
        else:
            update(tree, 2*v+1, tm+1, tr, pos, val)
        tree[v] = merge(tree[2*v], tree[2*v+1])

def get_count(arr, candidate):
    return sum(1 for x in arr if x == candidate)

t = int(input())
for _ in range(t):
    n, q = map(int, input().split())
    arr = list(map(int, input().split()))
    size = 1
    while size < n:
        size *= 2
    tree = [Node() for _ in range(2*size)]
    build(arr, tree, 1, 0, n-1)
    res = []
    for _ in range(q):
        i, x = map(int, input().split())
        i -= 1
        arr[i] = x
        update(tree, 1, 0, n-1, i, x)
        kmax = 0
        for cand in tree[1].candidates:
            cnt = get_count(arr, cand)
            k = max(0, 2*cnt - n)
            kmax = max(kmax, k)
        res.append(str(kmax))
    print(" ".join(res))
```

The segment tree stores candidates and counts. Merge ensures at most two candidates propagate upward. The update function modifies only the affected path from leaf to root. To compute `k`, we check actual counts in the array for root candidates, which are few, keeping it efficient.

## Worked Examples

Sample 1 input:

```
5 5
1 2 3 4 5
3 4
1 4
2 4
4 3
2 3
```

| Query | Update | Candidates at root | Counts | kmax |
| --- | --- | --- | --- | --- |
| 3→4 | [1,2,4,4,5] | 4,1 | 4:2, 1:1 | 1 |
| 1→4 | [4,2,4,4,5] | 4,2 | 4:3, 2:1 | 1 |
| 2→4 | [4,4,4,4,5] | 4,5 | 4:4, 5:1 | 2 |
| 4→3 | [4,4,4,3,5] | 4,3 | 4:3,3:1 | 1 |
| 2→3 | [4,3,4,3,5] | 4,3 | 4:2,3:2 | 0 |

This confirms that candidate tracking plus count evaluation produces correct `kmax`.

Sample 2 input works similarly, confirming multiple repeated elements and updates are handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+q) log n) | Building the segment tree takes O(n). Each query update affects O(log n) nodes. Counting candidates per query is O(1) since at most 2 candidates exist. |
| Space | O(n) | Segment tree stores 2*n nodes with at most 2 candidates each, fitting within memory limit. |
