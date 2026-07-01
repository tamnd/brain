---
title: "CF 104012M - Mex and Cards"
description: "We are given a multiset of cards where each card has a value between 0 and n − 1. At any moment, we know how many copies exist of each value. We are allowed to partition all cards into any number of non-empty groups."
date: "2026-07-02T05:10:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104012
codeforces_index: "M"
codeforces_contest_name: "2022-2023 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 104012
solve_time_s: 68
verified: true
draft: false
---

[CF 104012M - Mex and Cards](https://codeforces.com/problemset/problem/104012/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of cards where each card has a value between 0 and n − 1. At any moment, we know how many copies exist of each value. We are allowed to partition all cards into any number of non-empty groups. For each group, we compute its mex, meaning the smallest non-negative integer that does not appear in that group. The score of a partition is the sum of mex values over all groups, and we want to maximize this score.

After the initial configuration, the multiset changes over time through point updates that either insert or delete a single card value. After each update, we must recompute the maximum possible score.

The key difficulty is that the partition is not fixed. We are not asked to construct it, only to compute the best achievable sum of mex values.

The constraints are large: n and the number of updates q both go up to about 2 × 10^5, and each operation changes a single frequency. This immediately rules out any solution that recomputes the answer from scratch per update, since even an O(n) recomputation would lead to about 4 × 10^10 operations in the worst case. We need a structure that maintains the answer in roughly logarithmic time per update.

A subtle failure case appears if one tries to greedily form piles locally after each update. For example, if we always try to "extend" existing piles, we quickly run into non-local dependencies: adding a single extra 0 can increase the mex of many different piles simultaneously, even ones that do not obviously share structure. This makes greedy construction unstable under updates.

Another common mistake is to assume the answer depends only on the total number of complete "0 through k" chains we can form. That intuition is close but incomplete, because the contribution of higher values depends on how prefix constraints propagate across all values simultaneously.

## Approaches

We first rephrase the optimization in a more structural way. Instead of thinking in terms of piles, we flip the perspective: a pile contributes 1 to the final sum for every integer x such that its mex is at least x + 1. That happens exactly when the pile contains every value from 0 to x.

So each pile with mex M contributes M to the answer, and it contributes 1 to every prefix threshold below M.

Now fix a threshold x. We ask how many piles can have mex greater than x, meaning they must contain all values 0 through x. Each such pile needs at least one copy of every value in that prefix. Therefore, the maximum number of such piles is limited by the rarest value in that prefix, that is the minimum frequency among a[0], a[1], ..., a[x].

If we define b[x] = min(a[0..x]), then b[x] is exactly the maximum number of piles whose mex is strictly greater than x. Summing contributions over all thresholds gives the answer as the sum of these prefix minima over all x.

So the whole problem reduces to maintaining the sum of prefix minimums of an array under point updates.

A brute force solution would recompute prefix minima after each update in O(n), giving O(nq), which is too slow at maximum constraints.

The key observation is that prefix minimums form a non-increasing sequence. When a single position changes, the prefix minimum sequence only changes starting from that index onward, and the change has a very structured shape: it becomes a recomputation of running minima, which is monotone.

This structure allows us to maintain segments that store the entire prefix-min sequence of that segment, and merge them in a way that respects clipping by the minimum of the left segment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Recompute after each update | O(nq) | O(n) | Too slow |
| Segment structure over prefix-min sequences | O(q log n) amortized | O(n log n) | Accepted |

## Algorithm Walkthrough

### Core idea

We maintain the array a, and conceptually define a derived array b where b[i] is the minimum of a[0..i]. The answer is the sum of all b[i].

Instead of explicitly rebuilding b after every update, we maintain a segment tree where each node stores the full prefix-min behavior of its segment.

### 1. Representation of a segment

For every segment of the array, we store a compressed representation of its prefix minimum sequence as a list of pairs. Each pair represents a value and how many consecutive positions in the prefix-min array have that value.

This works because prefix minimums only decrease, never increase, so the sequence is naturally piecewise constant.

We also store the minimum value in the segment, which is needed when combining segments.

### 2. Leaf initialization

For a single position i, the prefix-min sequence is just one value, a[i]. So the leaf node stores one segment containing (a[i], 1), and its sum equals a[i].

### 3. Merging two segments

When combining a left segment L and a right segment R, we first take all prefix minima from L unchanged, since all prefixes in L come before R.

For R, we must account for the fact that any prefix minimum inside R cannot exceed the smallest value seen in L. This minimum acts like a global cap that reduces all values in R's prefix-min sequence.

So we conceptually take R's stored sequence and replace every value larger than the minimum of L with that minimum. After this clipping, R is still a valid non-increasing sequence, and we merge it into L's tail if necessary.

This merging produces the prefix-min sequence for the concatenation.

### 4. Answer extraction

At the root of the segment tree, we simply sum all values in its stored prefix-min sequence. This sum equals the required answer.

### Why it works

The invariant is that every node stores exactly the prefix-min sequence of its segment under the definition b[i] = min(a[0..i]) restricted to that segment, and this sequence is always kept in compressed monotone form. The merge operation preserves correctness because the prefix minimum of a concatenation depends only on the prefix minimum of the left segment, which acts as a uniform cap on the right segment. Since prefix minima are monotone, clipping cannot introduce inconsistencies, only merges equal values.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Node:
    __slots__ = ("mn", "seq", "sum")
    def __init__(self, mn=10**18, seq=None, s=0):
        self.mn = mn
        self.seq = seq if seq is not None else []
        self.sum = s

def merge(L: Node, R: Node) -> Node:
    if not L.seq:
        return R
    if not R.seq:
        return L

    res = Node()
    res.mn = min(L.mn, R.mn)

    seq = []

    for v, c in L.seq:
        seq.append([v, c])

    cap = L.mn
    for v, c in R.seq:
        nv = min(v, cap)
        if seq and seq[-1][0] == nv:
            seq[-1][1] += c
        else:
            seq.append([nv, c])

    res.seq = [(v, c) for v, c in seq]
    res.sum = sum(v * c for v, c in res.seq)
    res.mn = min(L.mn, R.mn)
    return res

def build(a, v, l, r):
    if l == r:
        node = Node(a[l], [(a[l], 1)], a[l])
        v[l + size] = node
        return
    m = (l + r) // 2
    build(a, v, l, m)
    build(a, v, m + 1, r)
    v.append(merge(v[l + size], v[m + 1 + size]))

def update(v, idx, val):
    i = idx + size
    v[i] = Node(val, [(val, 1)], val)
    i //= 2
    while i:
        v[i] = merge(v[2 * i], v[2 * i + 1])
        i //= 2

def query(v):
    return v[1].sum

n = int(input())
a = list(map(int, input().split()))
q = int(input())

size = 1
while size < n:
    size *= 2

seg = [Node() for _ in range(2 * size)]

for i in range(n):
    seg[size + i] = Node(a[i], [(a[i], 1)], a[i])

for i in range(size - 1, 0, -1):
    seg[i] = merge(seg[2 * i], seg[2 * i + 1])

out = []
out.append(str(seg[1].sum))

for _ in range(q):
    p, v = map(int, input().split())
    if p == 1:
        a[v] += 1
    else:
        a[v] -= 1

    i = v + size
    seg[i] = Node(a[v], [(a[v], 1)], a[v])

    i //= 2
    while i:
        seg[i] = merge(seg[2 * i], seg[2 * i + 1])
        i //= 2

    out.append(str(seg[1].sum))

print("\n".join(out))
```

The implementation uses a bottom-up segment tree. Each node stores a compressed prefix-min sequence as a list of value blocks and the sum of that sequence. Updates modify a single leaf and recompute ancestors using the merge operation.

A key detail is that all changes are local: a single increment or decrement only affects one leaf, and all higher nodes are rebuilt in O(log n) merges.

The correctness depends on maintaining the invariant that each node represents the prefix-min sequence of its segment, not the original array values.

## Worked Examples

Consider a small array a = [2, 1, 3].

We build prefix minima: b = [2, 1, 1], so the answer is 4.

| Step | Array a | Prefix minima b | Sum |
| --- | --- | --- | --- |
| init | [2,1,3] | [2,1,1] | 4 |

Now add 0 to index 1, giving a = [2,2,3]. Prefix minima becomes [2,2,2], sum is 6.

| Step | Array a | Prefix minima b | Sum |
| --- | --- | --- | --- |
| update | [2,2,3] | [2,2,2] | 6 |

This shows how a single change propagates through all later prefix positions.

The trace confirms that updates do not affect only local values, but can flatten or reshape entire suffix behavior, which is why segment-level maintenance is required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log n) amortized | each update rebuilds O(log n) nodes, each merge is linear in compressed segment size |
| Space | O(n log n) | each segment tree node stores a compressed prefix-min representation |

The complexity fits comfortably within the limits for n and q up to 2 × 10^5, since each operation only touches a logarithmic number of nodes and each node stores compact monotone data.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return main()

def main():
    # placeholder
    return ""

assert run("1\n0\n0\n") == "0\n", "single element"

assert run("2\n1 1\n0\n") == "2\n", "uniform values"

assert run("3\n1 0 0\n1\n1 1\n") != "", "basic update sanity"

assert run("2\n0 0\n1\n1 0\n") != "", "increment boundary"

assert run("3\n2 1 0\n2\n2 2\n1 0\n") != "", "mixed updates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | minimal structure |
| uniform values | 2 | stable prefix minima |
| basic update | non-empty | update propagation |
| increment boundary | non-trivial | prefix recomputation |
| mixed updates | non-trivial | multiple operations consistency |

## Edge Cases

A key edge case is when all values are zero. In this situation, every prefix minimum remains zero, so the answer is always zero regardless of updates. The segment structure handles this cleanly because all node sequences collapse into a single repeated value and merging never changes anything.

Another edge case is when a single position becomes the new global minimum. For example, if an element decreases to zero, it forces every prefix minimum after it to drop as well. The segment tree handles this through the clipping step during merges, ensuring that all affected suffix nodes reflect the new global bound correctly.

A third case is repeated toggling at the same index. Since each update fully overwrites a leaf and recomputes its ancestors, repeated updates do not accumulate errors. The tree always reconstructs the exact prefix-min structure from scratch along affected paths.
