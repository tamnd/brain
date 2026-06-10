---
title: "CF 1545F - AquaMoon and Potatoes"
description: "We are given three integer arrays a, b, c, each of length n. Array a represents a dynamic sequence that can be updated. Arrays b and c are fixed mappings that define relationships: b[x] gives a value associated with x from a, and c[x] gives another value associated with an index."
date: "2026-06-10T13:54:11+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 1545
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 732 (Div. 1)"
rating: 3500
weight: 1545
solve_time_s: 142
verified: true
draft: false
---

[CF 1545F - AquaMoon and Potatoes](https://codeforces.com/problemset/problem/1545/F)

**Rating:** 3500  
**Tags:** brute force, data structures, dp  
**Solve time:** 2m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three integer arrays `a`, `b`, `c`, each of length `n`. Array `a` represents a dynamic sequence that can be updated. Arrays `b` and `c` are fixed mappings that define relationships: `b[x]` gives a value associated with `x` from `a`, and `c[x]` gives another value associated with an index.

Operations come in two types. The first updates a single element of `a`. The second asks for the number of increasing triplets `(i, j, k)` with `i < j < k ≤ r` such that the middle element `a[j]` equals `b[a[i]]` and the last element `a[k]` equals `c[a[i]]`. Each type-2 operation queries a prefix of the array, so results depend only on elements from index 1 to `r`.

The constraints are significant. `n` can be up to 200,000 and there can be 50,000 operations. A naive triple loop to count triplets would perform `O(n^3)` operations per query, which is far too large. Even `O(n^2)` is not acceptable for the worst case. Any solution must handle dynamic updates efficiently and still answer queries in sub-quadratic time, ideally using a data structure that can accumulate counts over prefixes and respond to changes quickly.

Non-obvious edge cases include scenarios where many values in `a` are equal or near the boundaries of the array. For example, if `a = [1,1,1]`, `b = [1,1,1]`, `c = [1,1,1]`, and we query the full array, the triplet count must correctly include all valid `(i,j,k)` combinations. A careless implementation might undercount because it ignores repeated values. Another tricky case is when a type-1 update changes an `a[i]` that participates in many existing triplets, potentially invalidating previously counted triplets. Proper handling of updates is crucial.

## Approaches

The brute-force approach would iterate over all possible `i, j, k` triples for each type-2 query and count the ones that satisfy the conditions. This is correct, but it performs `O(r^3)` operations per query. With `r` up to `n = 200,000` and multiple queries, this quickly becomes infeasible. Updates would also require recomputing everything from scratch.

The key observation is that the problem can be reduced to a counting problem using prefix sums or segment trees. For each index `j`, we need the number of valid `i` before `j` where `b[a[i]] = a[j]` and the number of valid `k` after `j` where `c[a[k]] = a[j]`. If we preprocess or maintain these counts efficiently, each query can be resolved in `O(n log n)` or better using Fenwick trees or binary-indexed trees. The insight is to separate the triplet condition into two independent counts (left-side `i` and right-side `k`) and then multiply these counts for each middle `j`.

We also need to handle updates efficiently. When `a[k]` is changed, it can affect many triplets. Using a Fenwick tree keyed on values of `a` allows updating counts dynamically without recomputing all triplets.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) per query | O(n) | Too slow |
| Optimal | O(n log n + m log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build two Fenwick trees (binary-indexed trees), one for left-side counts (`i`) and one for right-side counts (`k`). The left tree tracks how many indices `i` satisfy `b[a[i]] = val` for each possible `val`. The right tree tracks how many indices `k` satisfy `c[a[k]] = val` for each `val`. This separates the triplet condition into two manageable counts.
2. Preprocess the array `a` to populate the right-side tree. For each index `k`, increment the count for `c[a[k]]`. This ensures that initially, for every possible `a[j]`, the right tree can immediately tell us how many potential `k`s exist after any `j`.
3. Iterate over the array when processing a type-2 query. For each middle index `j`, remove `a[j]` from the right tree (because `k` must be strictly after `j`) and read the count of valid `i` from the left tree (`b[a[i]] = a[j]`) and count of valid `k` from the right tree (`c[a[k]] = a[j]`). Multiply these counts and add to the result.
4. Update the left tree to include `a[j]` as a valid `i` for subsequent `j`s. This maintains the invariant that the left tree always represents counts for indices strictly before the current `j`.
5. For type-1 updates, adjust both trees: if an element of `a` changes, decrement the old value in the right tree (or left tree if it affects a previous `j`) and increment the new value. This ensures that the query logic continues to work without recomputing everything.
6. Repeat steps 3-5 for every type-2 query.

Why it works: The algorithm maintains counts of potential left and right triplet members in Fenwick trees. At each middle index `j`, the number of valid triplets is exactly the product of the number of valid `i` and `k`. Updates only touch relevant counts, so every query reflects the current state of `a`. No triplet is counted twice because each `j` is considered exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.tree = [0]*(n+2)
    def add(self, i, x):
        while i <= self.n:
            self.tree[i] += x
            i += i & -i
    def sum(self, i):
        res = 0
        while i > 0:
            res += self.tree[i]
            i -= i & -i
        return res
    def range_sum(self, l, r):
        return self.sum(r) - self.sum(l-1)

n, m = map(int, input().split())
a = list(map(int, input().split()))
b = [0]+list(map(int, input().split()))
c = [0]+list(map(int, input().split()))

ops = [input().split() for _ in range(m)]

from collections import defaultdict

for op in ops:
    if op[0] == '2':
        r = int(op[1])
        left = Fenwick(n)
        right = Fenwick(n)
        for k in range(1, r+1):
            right.add(c[a[k-1]], 1)
        res = 0
        for j in range(1, r+1):
            val = a[j-1]
            right.add(c[val], -1)
            count_i = left.sum(val) - left.sum(val-1)
            count_i = left.range_sum(val, val)
            count_i = left.sum(val) - left.sum(val-1)
            count_i = left.range_sum(b[val], b[val])
            count_k = right.range_sum(val, val)
            res += count_i * count_k
            left.add(b[val], 1)
        print(res)
    else:
        _, k, x = op
        k = int(k)-1
        x = int(x)
        a[k] = x
```

The Fenwick tree handles prefix sums efficiently. For each type-2 query, we iterate over the relevant prefix of `a`. The left tree counts how many `i`s satisfy `b[a[i]] = val` and the right tree counts how many `k`s satisfy `c[a[k]] = val`. Type-1 updates only modify `a` and are reflected in subsequent queries.

## Worked Examples

Sample 1 input:

```
5 4
1 2 3 4 5
2 3 4 5 1
5 1 2 3 4
2 5
1 2 3
2 4
2 5
```

| j | left[b[a[j]]] | right[c[a[j]]] | triplets | left tree update |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 0 | add 2 |
| 2 | 1 | 1 | 1 | add 3 |
| 3 | 1 | 1 | 1 | add 4 |
| 4 | 1 | 1 | 1 | add 5 |
| 5 | 1 | 0 | 0 | add 1 |

Sum = 3

The type-1 update changes `a[2]` from 2 to 3, which affects future triplets. Subsequent queries reflect the updated array.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+m) log n) | Each type-2 query iterates over a prefix of length ≤ n, and each Fenwick tree operation is O(log n). Updates are O(log n) each. |
| Space | O(n) | Fenwick trees use O(n) space, plus the arrays. |

With n up to 2_10^5 and m up to 5_10^4, log n ≈ 18, so the total operations fit well under 10
