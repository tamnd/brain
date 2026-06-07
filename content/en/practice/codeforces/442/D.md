---
title: "CF 442D - Adam and Tree"
description: "The tree starts with a single root vertex. Each operation adds one new leaf to an existing vertex. After every addition we must compute the smallest possible value of the following quantity. We color the edges of the tree."
date: "2026-06-07T15:53:31+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "trees"]
categories: ["algorithms"]
codeforces_contest: 442
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 253 (Div. 1)"
rating: 2600
weight: 442
solve_time_s: 229
verified: false
draft: false
---

[CF 442D - Adam and Tree](https://codeforces.com/problemset/problem/442/D)

**Rating:** 2600  
**Tags:** data structures, trees  
**Solve time:** 3m 49s  
**Verified:** no  

## Solution
## Problem Understanding

The tree starts with a single root vertex. Each operation adds one new leaf to an existing vertex. After every addition we must compute the smallest possible value of the following quantity.

We color the edges of the tree. Edges with the same color must form one connected path, and no vertex may have more than two incident edges of the same color. For any vertex, look at the path from that vertex to the root and count how many different colors appear on that path. The cost of the coloring is the maximum such count over all vertices. We want the minimum possible cost.

The input does not describe a static tree. It describes a sequence of insertions. If `p[i] = v`, then vertex `i + 1` is attached as a new child of `v`. After each insertion we output the optimal cost of the current tree.

The largest difficulty is the constraint `n ≤ 10^6`. A solution that recomputes anything substantial after each insertion is immediately ruled out. Even `O(height)` work per insertion can be dangerous if it happens too often. The total work must stay very close to linear.

There are several easy ways to go wrong.

Consider a root with two leaf children:

```
1
├─2
└─3
```

The answer is `2`, not `1`. One color cannot simultaneously continue into both branches. Any coloring needs one extra color level once a path splits into two equally difficult subtrees.

Now consider a chain:

```
1
└─2
   └─3
      └─4
```

The answer is still `1`. A single color can cover the entire chain. Counting depth or height would incorrectly produce `4`.

Another subtle case is:

```
1
├─2
│  └─4
└─3
```

The answer is `2`, not `3`. Only one branch is deep. The color used on the heavy branch can continue through the root, so the difficulty does not increase unless there are at least two equally difficult branches.

These examples point toward a recursive quantity that depends on the largest child values and on how many children attain that maximum.

## Approaches

The brute force viewpoint is to build the tree after each insertion and recompute the optimal coloring from scratch.

A useful observation is that every color class is a path. When a path reaches a branching vertex, it can continue through at most one child. All other child subtrees must start a new color segment. This leads to a recursive optimization over the tree.

If we compute the optimal value for every node from scratch after every insertion, the worst case becomes quadratic. A tree with one million insertions makes this completely infeasible.

The key insight is that the optimal cost is exactly the Horton-Strahler number of the rooted tree.

Let `f(v)` be the optimal cost contribution of the subtree rooted at `v`.

For a leaf, `f(v) = 1`.

For an internal node, let `m` be the maximum value among its children.

If only one child has value `m`, then the best color path can continue through that child, so:

```
f(v) = m
```

If at least two children have value `m`, then one extra color level is unavoidable:

```
f(v) = m + 1
```

This is precisely the Strahler recurrence.

The dynamic part becomes much easier because a Strahler number can only increase. In a tree with at most `10^6 + 1` vertices, the Strahler number never exceeds `21`, since obtaining value `k` requires at least `2^(k-1)` leaves.

A child value changes only a small number of times during the entire process. This gives an almost linear total update count.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) amortized, with log n ≤ 21 | O(n log n) | Accepted |

## Algorithm Walkthrough

1. For every vertex store its current Strahler value `val[v]`.
2. For every vertex store `mx[v]`, the largest Strahler value among its children.
3. For every vertex maintain how many children currently have each possible value. Since the maximum possible value is at most `21`, a small fixed range is sufficient.
4. When a new leaf is created, its value is `1`.
5. Attach the leaf to its parent. From the parent's perspective, one child of value `1` has appeared.
6. Update the parent's counters and recompute its value.

If `mx` is the largest child value and `cnt[mx]` is the number of children attaining it, then:

```
val = 1                         if mx = 0
val = mx                        if cnt[mx] = 1
val = mx + 1                    if cnt[mx] ≥ 2
```
7. If the parent's value did not change, stop. Nothing above it can change.
8. If the parent's value changed from `old` to `new`, move to its parent. For that ancestor, one child value changed from `old` to `new`.
9. Repeat until either the value remains unchanged or the root is reached.
10. After processing the insertion, output `val[root]`.

The reason this is efficient is that values only increase. A vertex can move through at most about twenty different values during the entire lifetime of the tree, so the total number of propagated updates is small.

### Why it works

The Strahler recurrence exactly captures the coloring constraint.

A color path may continue through at most one child subtree. If there is a unique hardest child, the optimal path continues through it and no extra color level is needed. If there are two or more hardest children, only one of them can inherit the current color path, forcing another color level somewhere below. That increases the required value by one.

The maintained counters always represent the current multiset of child values. Every update modifies exactly one child contribution, so recomputing the parent from these counters preserves the recurrence. Propagating only when a value changes is sufficient because ancestors depend solely on child values. Thus the root value after each insertion is exactly the optimal coloring cost.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    n = int(input())
    p = list(map(int, input().split()))

    max_nodes = n + 2
    MAXR = 22  # Strahler number never exceeds 21 for n <= 1e6

    parent = array('I', [0]) * max_nodes
    val = bytearray(max_nodes)
    mx = bytearray(max_nodes)

    cnt = array('I', [0]) * (max_nodes * MAXR)

    val[1] = 1

    ans = []

    for node, par in enumerate(p, start=2):
        parent[node] = par
        val[node] = 1

        v = par
        old_child = 0
        new_child = 1

        while v:
            base = v * MAXR

            if old_child:
                cnt[base + old_child] -= 1

            cnt[base + new_child] += 1

            if new_child > mx[v]:
                mx[v] = new_child

            old_val = val[v]

            m = mx[v]
            if m == 0:
                new_val = 1
            else:
                new_val = m + (cnt[base + m] >= 2)

            if new_val == old_val:
                break

            val[v] = new_val

            old_child = old_val
            new_child = new_val
            v = parent[v]

        ans.append(str(val[1]))

    sys.stdout.write(" ".join(ans))

if __name__ == "__main__":
```
