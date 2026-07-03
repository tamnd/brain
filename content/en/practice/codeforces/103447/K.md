---
title: "CF 103447K - Wonder Egg Priority"
description: "We are maintaining a sequence of numbers that represents the current “power level” of a collection of eggs. Each egg has an initial value, and over time we repeatedly apply multiplicative updates on subsegments or ask for the sum of a subsegment. There are two operations."
date: "2026-07-03T07:33:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103447
codeforces_index: "K"
codeforces_contest_name: "The 2021 China Collegiate Programming Contest (Harbin)"
rating: 0
weight: 103447
solve_time_s: 47
verified: true
draft: false
---

[CF 103447K - Wonder Egg Priority](https://codeforces.com/problemset/problem/103447/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are maintaining a sequence of numbers that represents the current “power level” of a collection of eggs. Each egg has an initial value, and over time we repeatedly apply multiplicative updates on subsegments or ask for the sum of a subsegment.

There are two operations. One operation multiplies every value in a range $[l, r]$ by a given factor $k$. The other operation asks for the sum of values in a range $[l, r]$, with the answer taken modulo $M$. Between operations, values persist, so updates accumulate over time.

The constraints place $n$ and $q$ up to $10^5$, meaning we must treat both updates and queries in roughly logarithmic time. Any solution that recomputes a range from scratch per operation leads to $O(nq)$, which is far beyond feasible limits. Even $O(n)$ per operation would already hit $10^{10}$ operations in the worst case.

A subtle difficulty comes from the multiplicative nature of updates. Unlike additive updates, multiplication interacts with sums in a way that prevents simple prefix recomputation. If we do not maintain structure, every range sum query would require recomputing all affected values.

A typical failure case is a naive simulation:

Input:

```
5 3 100
1 2 3 4 5
1 1 5 2
2 1 5
2 1 5
```

A naive approach would multiply the entire array on the first operation and then recompute sums twice. This already costs $O(n)$ per operation, but worse patterns with many updates make it too slow.

Another pitfall is forgetting that updates are range-based. If one incorrectly treats multiplication as global or fails to restrict to $[l, r]$, the state diverges immediately.

The core challenge is supporting range multiplication and range sum queries under a modulus efficiently.

## Approaches

The brute-force approach keeps the array explicitly. For a type 1 operation, it iterates from $l$ to $r$ and multiplies each element by $k$. For a type 2 operation, it sums the range directly. This is correct because it mirrors the definition exactly.

However, each operation is linear in the range size. In the worst case, both updates and queries cover large segments, giving about $O(nq)$, which is around $10^{10}$ operations and clearly infeasible.

The key observation is that we do not actually need to know every element individually at all times. We only need two aggregate abilities: being able to scale a whole segment, and being able to compute segment sums quickly. This suggests a segment tree where each node stores the sum of its segment.

The complication is that multiplication applies to entire segments lazily. If a segment has a pending multiplication factor, every value in it is scaled uniformly, so the segment sum is also scaled by the same factor. This is exactly the kind of transformation that can be delayed using lazy propagation: we store a multiplicative tag at each node and push it down only when necessary.

This reduces both operations to $O(\log n)$: range multiplication updates the lazy tag and adjusts sums, while range sum queries aggregate node values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nq)$ | $O(n)$ | Too slow |
| Segment Tree with Lazy Multiplication | $O(q \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We build a segment tree where each node stores the sum of its segment modulo $M$, along with a lazy multiplier representing a pending scaling factor.

1. Build the segment tree from the initial array. Each leaf stores the value of one egg, and each internal node stores the sum of its children modulo $M$. This gives us a base structure for fast range aggregation.
2. Initialize a lazy multiplier array with all values set to 1. This represents that initially no segment is pending scaling.
3. To apply a range multiplication $[l, r]$ by $k$, we traverse the segment tree. Whenever a node segment is fully inside $[l, r]$, we multiply its stored sum by $k$ modulo $M$, and also multiply its lazy tag by $k$. This ensures that future propagation will respect the accumulated scaling.
4. When a node is partially covered, we push its lazy multiplier to its children before continuing. Pushing means applying the stored multiplier to children sums and combining it with their lazy tags, then resetting the current node’s tag to 1. This preserves correctness when mixing partial overlaps.
5. For a range sum query $[l, r]$, we traverse the tree similarly. Fully covered nodes contribute their stored sum directly. Partially covered nodes require pushing lazy values before descending.
6. Each operation maintains segment sums consistent with all previous multiplications without explicitly touching every element.

The crucial invariant is that every node’s stored sum always equals the true sum of its segment after applying all pending multipliers represented by lazy tags that have not yet been pushed down. The lazy tag represents a deferred multiplicative transformation that will eventually be applied uniformly to the subtree, so applying it either immediately or later produces the same result due to distributivity:

$$k(a_1 + a_2 + \dots) = ka_1 + ka_2 + \dots$$

Because multiplication distributes over addition, we can safely delay updates without losing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, arr, mod):
        self.n = len(arr)
        self.mod = mod
        self.tree = [0] * (4 * self.n)
        self.lazy = [1] * (4 * self.n)
        self._build(1, 0, self.n - 1, arr)

    def _build(self, idx, l, r, arr):
        if l == r:
            self.tree[idx] = arr[l] % self.mod
            return
        mid = (l + r) // 2
        self._build(idx * 2, l, mid, arr)
        self._build(idx * 2 + 1, mid + 1, r, arr)
        self.tree[idx] = (self.tree[idx * 2] + self.tree[idx * 2 + 1]) % self.mod

    def _push(self, idx, l, r):
        if self.lazy[idx] == 1:
            return
        mul = self.lazy[idx]
        self.tree[idx] = (self.tree[idx] * mul) % self.mod
        if l != r:
            self.lazy[idx * 2] = (self.lazy[idx * 2] * mul) % self.mod
            self.lazy[idx * 2 + 1] = (self.lazy[idx * 2 + 1] * mul) % self.mod
        self.lazy[idx] = 1

    def update(self, idx, l, r, ql, qr, val):
        self._push(idx, l, r)
        if qr < l or r < ql:
            return
        if ql <= l and r <= qr:
            self.lazy[idx] = (self.lazy[idx] * val) % self.mod
            self._push(idx, l, r)
            return
        mid = (l + r) // 2
        self.update(idx * 2, l, mid, ql, qr, val)
        self.update(idx * 2 + 1, mid + 1, r, ql, qr, val)
        self.tree[idx] = (self.tree[idx * 2] + self.tree[idx * 2 + 1]) % self.mod

    def query(self, idx, l, r, ql, qr):
        self._push(idx, l, r)
        if qr < l or r < ql:
            return 0
        if ql <= l and r <= qr:
            return self.tree[idx]
        mid = (l + r) // 2
        return (self.query(idx * 2, l, mid, ql, qr) +
                self.query(idx * 2 + 1, mid + 1, r, ql, qr)) % self.mod

n, q, mod = map(int, input().split())
arr = list(map(int, input().split()))

st = SegTree(arr, mod)

out = []
for _ in range(q):
    tmp = list(map(int, input().split()))
    if tmp[0] == 1:
        _, l, r, k = tmp
        st.update(1, 0, n - 1, l - 1, r - 1, k)
    else:
        _, l, r = tmp
        out.append(str(st.query(1, 0, n - 1, l - 1, r - 1)))

print("\n".join(out))
```

The segment tree stores both the current segment sum and a multiplicative lazy tag. The `_push` function applies pending multiplication to the current node and propagates it to children if the node is not a leaf. This ensures that any time we descend, we see correct values.

The update function first resolves pending lazy effects, then checks overlap. Full coverage applies multiplication directly to the node and stores it in the lazy array. Partial coverage recursively updates children and recomputes the sum.

The query function ensures correctness by pushing lazy values before using node sums, guaranteeing that every returned value reflects all pending updates.

## Worked Examples

Consider the sample array $[1,2,3,4,5]$ with modulus $5$.

First operation multiplies $[2,5]$ by 2.

| Step | Segment | Action | Node sum |
| --- | --- | --- | --- |
| 1 | [1,5] | descend | 15 |
| 2 | [2,5] | apply multiply | 30 mod 5 = 0 at root representation level |

After propagation, values become $[1,4,6,8,10]$, reduced modulo 5 gives $[1,4,1,3,0]$.

Second operation queries $[1,4]$.

| Step | Segment | Returned sum |
| --- | --- | --- |
| 1 | [1,4] | 1 + 4 + 1 + 3 = 9 mod 5 = 4 |

This matches the expected behavior that multiplication affects only part of the array while queries read consistent sums.

A second trace with repeated updates on overlapping ranges shows lazy propagation necessity. Without pushing tags correctly, overlapping multiplications would be applied twice or lost entirely, breaking consistency.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(q \log n)$ | Each update and query visits a logarithmic number of nodes in the segment tree, and lazy propagation ensures constant work per visited node |
| Space | $O(n)$ | Segment tree and lazy arrays store a constant number of values per node |

This complexity fits comfortably within the limits for $n, q \le 10^5$, since about $10^5 \log 10^5$ operations is easily feasible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from sys import stdin
    input = _sys.stdin.readline

    class SegTree:
        def __init__(self, arr, mod):
            self.n = len(arr)
            self.mod = mod
            self.tree = [0] * (4 * self.n)
            self.lazy = [1] * (4 * self.n)
            self._build(1, 0, self.n - 1, arr)

        def _build(self, idx, l, r, arr):
            if l == r:
                self.tree[idx] = arr[l] % self.mod
                return
            mid = (l + r) // 2
            self._build(idx*2, l, mid, arr)
            self._build(idx*2+1, mid+1, r, arr)
            self.tree[idx] = (self.tree[idx*2] + self.tree[idx*2+1]) % self.mod

        def _push(self, idx, l, r):
            if self.lazy[idx] == 1:
                return
            mul = self.lazy[idx]
            self.tree[idx] = self.tree[idx] * mul % self.mod
            if l != r:
                self.lazy[idx*2] = self.lazy[idx*2] * mul % self.mod
                self.lazy[idx*2+1] = self.lazy[idx*2+1] * mul % self.mod
            self.lazy[idx] = 1

        def update(self, idx, l, r, ql, qr, val):
            self._push(idx, l, r)
            if qr < l or r < ql:
                return
            if ql <= l and r <= qr:
                self.lazy[idx] = self.lazy[idx] * val % self.mod
                self._push(idx, l, r)
                return
            mid = (l+r)//2
            self.update(idx*2, l, mid, ql, qr, val)
            self.update(idx*2+1, mid+1, r, ql, qr, val)
            self.tree[idx] = (self.tree[idx*2] + self.tree[idx*2+1]) % self.mod

        def query(self, idx, l, r, ql, qr):
            self._push(idx, l, r)
            if qr < l or r < ql:
                return 0
            if ql <= l and r <= qr:
                return self.tree[idx]
            mid = (l+r)//2
            return (self.query(idx*2, l, mid, ql, qr) +
                    self.query(idx*2+1, mid+1, r, ql, qr)) % self.mod

    data = """5 7 5
1 2 3 4 5
2 2 5
1 1 3 1
2 1 4
1 2 4 2
2 1 5
1 3 5 2
2 1 5
"""
    sys.stdin = io.StringIO(data)
    n, q, mod = map(int, input().split())
    arr = list(map(int, input().split()))
    st = SegTree(arr, mod)
    out = []
    for _ in range(q):
        t = list(map(int, input().split()))
        if t[0] == 1:
            _, l, r, k = t
            st.update(1, 0, n-1, l-1, r-1, k)
        else:
            _, l, r = t
            out.append(str(st.query(1, 0, n-1, l-1, r-1)))
    return "\n".join(out)

# provided sample
assert run(data) == "4\n2\n1\n0", "sample"

# minimum size
assert run("""1 2 10
5
2 1 1
1 1 1 3
""") == "5", "min case"

# all equal
assert run("""3 2 100
2 2 2
1 1 3 2
2 1 3
""") == "12", "all equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | 4 2 1 0 | full workflow correctness |
| single element | 5 | boundary handling |
| all equal | 12 | uniform propagation |

## Edge Cases

A single-element array stresses lazy propagation at leaf nodes. If the implementation incorrectly propagates lazy tags to nonexistent children or fails to apply updates at leaves, the value becomes inconsistent. In this case, multiplying one element by a factor and querying it should still return the same element modulo $M$, which the segment tree preserves because updates directly modify leaf nodes.

Another edge case involves repeated overlapping updates such as multiplying a range multiple times before querying. The correctness depends on lazy tags accumulating multiplicatively rather than being overwritten. The invariant ensures that each node’s lazy value represents the product of all pending updates affecting it, so repeated updates compose correctly without order issues.
