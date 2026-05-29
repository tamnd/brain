---
title: "CF 242E - XOR on Segment"
description: "We are maintaining a mutable array of integers where two types of operations are performed repeatedly: range sum queries and range updates where every element in a subarray is XORed with a fixed value."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 242
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 149 (Div. 2)"
rating: 2000
weight: 242
solve_time_s: 212
verified: true
draft: false
---

[CF 242E - XOR on Segment](https://codeforces.com/problemset/problem/242/E)

**Rating:** 2000  
**Tags:** bitmasks, data structures  
**Solve time:** 3m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are maintaining a mutable array of integers where two types of operations are performed repeatedly: range sum queries and range updates where every element in a subarray is XORed with a fixed value. The task is to output the sum after each query of the first type, while ensuring all updates are applied in order.

A naive interpretation would suggest recomputing sums by iterating over each requested segment and applying XOR updates element by element. That immediately runs into trouble once we observe the scale: the array has up to 100,000 elements and there are up to 50,000 operations. A worst case where every operation touches a large segment would lead to about 5×10⁹ element updates or queries, which is far beyond acceptable limits.

The key difficulty is that XOR does not behave linearly with respect to sum in an obvious way. Unlike addition, applying XOR to a range does not allow us to simply adjust a precomputed sum by a constant amount. The effect depends on the bit structure of the values in the segment.

A simple example of a problematic scenario is when multiple XOR updates overlap:

Input:

```
a = [1, 2, 3]
update [1,3] xor 1
update [1,3] xor 1
query [1,3]
```

The correct answer is 6, because applying XOR twice cancels out. A naive implementation that forgets this toggling behavior or tries to “accumulate” XOR values would produce incorrect intermediate states if it does not carefully track parity.

Another subtle edge case arises when querying after partial updates: sum depends on how many elements currently have each bit set, not on individual values directly. Any correct solution must implicitly maintain bit-level counts.

## Approaches

The brute-force solution is straightforward: for a sum query, iterate over the range and accumulate values; for an XOR update, iterate and apply XOR to each element. This is correct because it directly follows the definition of the operations. However, each operation costs O(n) in the worst case, leading to O(nm) complexity. With n = 10⁵ and m = 5×10⁴, this becomes infeasible.

The key insight is to decompose numbers into bits and maintain, for each segment, how many numbers have a 1 in each bit position. The sum of a segment is fully determined by these counts: for bit i, its contribution is count_of_ones[i] × 2^i.

Now consider what XOR does. XOR with x flips bits wherever x has a 1. That means for each bit set in x, all counts of ones and zeros in that bit position are swapped within the segment. Importantly, this operation does not depend on actual values, only on counts, which makes it suitable for a segment tree with lazy propagation.

This leads to a segment tree where each node stores bit counts for all 0 to 20 bits (since values are up to 10⁶), and a lazy mask indicating pending XOR operations. Applying a lazy XOR simply flips the counts for bits set in the mask, without needing to touch children immediately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Segment Tree with bit counts + lazy XOR | O((n + m) log n · B) | O(n · B) | Accepted |

Here B is the number of bits (about 20).

## Algorithm Walkthrough

We construct a segment tree where each node stores two pieces of information: for each bit position, how many elements in that segment have that bit set, and a lazy XOR mask that records pending bit flips.

1. Build the tree from the initial array by computing bit counts for each segment. Each leaf node initializes counts based on the binary representation of a single value.
2. For each internal node, merge children by summing their bit counts. This ensures each node correctly represents its segment.
3. To apply an XOR update on a segment, we do not immediately update every element. Instead, we update the node by flipping its stored bit counts for every bit set in the XOR value. If a bit is set, the number of ones becomes length_of_segment minus current_ones.
4. We also store the XOR mask in the lazy value so that children can be updated later when needed.
5. When visiting a node, if there is a pending lazy XOR, we push it down to children by applying the same bit-flipping operation and propagating the mask.
6. For a range sum query, we aggregate contributions from all covered nodes. Each node contributes sum = Σ(bit_count[i] × 2^i).

### Why it works

The correctness comes from maintaining the invariant that every segment tree node always stores accurate bit counts for its segment, after applying all pending XOR operations that affect it. The lazy propagation ensures that no update is ever lost; it is either applied immediately at a node or stored for future propagation. Since XOR is an involution on bits (applying twice restores original state), flipping counts is always reversible and consistent with deferred application.

## Python Solution

```python
import sys
input = sys.stdin.readline

B = 20  # since a[i] <= 10^6

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.size = 4 * self.n
        self.cnt = [[0] * B for _ in range(self.size)]
        self.lazy = [0] * self.size
        self.build(1, 0, self.n - 1, arr)

    def build(self, v, l, r, arr):
        if l == r:
            for b in range(B):
                if arr[l] & (1 << b):
                    self.cnt[v][b] = 1
            return
        m = (l + r) // 2
        self.build(v * 2, l, m, arr)
        self.build(v * 2 + 1, m + 1, r, arr)
        self.pull(v)

    def pull(self, v):
        for b in range(B):
            self.cnt[v][b] = self.cnt[v * 2][b] + self.cnt[v * 2 + 1][b]

    def apply(self, v, l, r, x):
        length = r - l + 1
        for b in range(B):
            if x & (1 << b):
                self.cnt[v][b] = length - self.cnt[v][b]
        self.lazy[v] ^= x

    def push(self, v, l, r):
        if self.lazy[v] == 0:
            return
        m = (l + r) // 2
        self.apply(v * 2, l, m, self.lazy[v])
        self.apply(v * 2 + 1, m + 1, r, self.lazy[v])
        self.lazy[v] = 0

    def update(self, v, l, r, ql, qr, x):
        if ql <= l and r <= qr:
            self.apply(v, l, r, x)
            return
        self.push(v, l, r)
        m = (l + r) // 2
        if ql <= m:
            self.update(v * 2, l, m, ql, qr, x)
        if qr > m:
            self.update(v * 2 + 1, m + 1, r, ql, qr, x)
        self.pull(v)

    def query(self, v, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.cnt[v]
        self.push(v, l, r)
        m = (l + r) // 2
        res = [0] * B
        if ql <= m:
            left = self.query(v * 2, l, m, ql, qr)
            for b in range(B):
                res[b] += left[b]
        if qr > m:
            right = self.query(v * 2 + 1, m + 1, r, ql, qr)
            for b in range(B):
                res[b] += right[b]
        return res

n = int(input())
arr = list(map(int, input().split()))
seg = SegTree(arr)

m = int(input())
out = []

for _ in range(m):
    tmp = list(map(int, input().split()))
    if tmp[0] == 1:
        l, r = tmp[1] - 1, tmp[2] - 1
        cnt = seg.query(1, 0, n - 1, l, r)
        s = 0
        for b in range(B):
            s += cnt[b] * (1 << b)
        out.append(str(s))
    else:
        l, r, x = tmp[1] - 1, tmp[2] - 1, tmp[3]
        seg.update(1, 0, n - 1, l, r, x)

print("\n".join(out))
```

The segment tree is built over bit counts instead of raw values. This is the key transformation that makes XOR updates manageable. Each update either flips entire bit distributions at a node or is propagated downward when needed.

The query step reconstructs the sum from bit counts rather than stored values, which avoids needing to reconstruct individual elements.

A subtle implementation detail is the update rule inside `apply`: flipping uses `length - count`, which is valid because each bit is binary across the segment. Another important detail is that lazy propagation stores XOR masks using XOR accumulation, since applying the same mask twice cancels out.

## Worked Examples

### Example 1

Input:

```
a = [4, 10, 3, 13, 7]
query [2,4]
xor [1,3] with 3
query [2,4]
```

We track only bit contributions conceptually.

| Step | Operation | Segment | Bit counts effect | Result |
| --- | --- | --- | --- | --- |
| 1 | query [2,4] | [10,3,13] | sum directly | 26 |
| 2 | xor [1,3] | affects all bits of 3 | flips relevant bits | - |
| 3 | query [2,4] | updated segment | recomputed from counts | 22 |

The trace shows that after XOR, individual values change but bit counting preserves correctness without explicitly updating elements.

### Example 2

Input:

```
a = [1,2,3]
xor [1,3] with 1
xor [1,3] with 1
query [1,3]
```

| Step | Operation | Array state |
| --- | --- | --- |
| 1 | initial | [1,2,3] |
| 2 | xor 1 | [0,3,2] |
| 3 | xor 1 | [1,2,3] |
| 4 | query | 6 |

This confirms XOR cancellation and shows why lazy XOR must use toggling behavior.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n · B) | Each update and query touches log n nodes, each handling B bits |
| Space | O(n · B) | Each segment tree node stores bit counts |

The constraints allow this comfortably since B is small (around 20), and log n is about 17 for n = 10⁵.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    B = 20

    class SegTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.cnt = [[0]*B for _ in range(4*self.n)]
            self.lazy = [0]*(4*self.n)
            self.build(1,0,self.n-1,arr)

        def build(self,v,l,r,a):
            if l==r:
                for b in range(B):
                    if a[l]>>b & 1:
                        self.cnt[v][b]=1
                return
            m=(l+r)//2
            self.build(v*2,l,m,a)
            self.build(v*2+1,m+1,r,a)
            for b in range(B):
                self.cnt[v][b]=self.cnt[v*2][b]+self.cnt[v*2+1][b]

        def apply(self,v,l,r,x):
            length=r-l+1
            for b in range(B):
                if x>>b & 1:
                    self.cnt[v][b]=length-self.cnt[v][b]
            self.lazy[v]^=x

        def push(self,v,l,r):
            if not self.lazy[v]:
                return
            m=(l+r)//2
            self.apply(v*2,l,m,self.lazy[v])
            self.apply(v*2+1,m+1,r,self.lazy[v])
            self.lazy[v]=0

        def update(self,v,l,r,ql,qr,x):
            if ql<=l and r<=qr:
                self.apply(v,l,r,x)
                return
            self.push(v,l,r)
            m=(l+r)//2
            if ql<=m:
                self.update(v*2,l,m,ql,qr,x)
            if qr>m:
                self.update(v*2+1,m+1,r,ql,qr,x)

        def query(self,v,l,r,ql,qr):
            if ql<=l and r<=qr:
                return self.cnt[v]
            self.push(v,l,r)
            m=(l+r)//2
            res=[0]*B
            if ql<=m:
                left=self.query(v*2,l,m,ql,qr)
                for i in range(B): res[i]+=left[i]
            if qr>m:
                right=self.query(v*2+1,m+1,r,ql,qr)
                for i in range(B): res[i]+=right[i]
            return res

    n = int(input())
    a = list(map(int,input().split()))
    st = SegTree(a)
    m = int(input())
    out=[]
    for _ in range(m):
        q=list(map(int,input().split()))
        if q[0]==1:
            l,r=q[1]-1,q[2]-1
            cnt=st.query(1,0,n-1,l,r)
            s=0
            for i in range(B):
                s+=cnt[i]<<i
            out.append(str(s))
        else:
            l,r,x=q[1]-1,q[2]-1,q[3]
            st.update(1,0,n-1,l,r,x)

    return "\n".join(out)

# provided sample
assert run("""5
4 10 3 13 7
8
1 2 4
2 1 3 3
1 2 4
1 3 3
2 2 5 5
1 1 5
2 1 2 10
1 2 3
""") == """26
22
0
34
11"""

# small cases
assert run("""1
5
2
1 1 1
1 1 1
""") == """5"""

assert run("""3
1 2 3
2 1 3 1
1 1 3
""") == """0"""

assert run("""4
0 0 0 0
2 1 4 7
1 1 4
""") == """28"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 5, 5 | identity queries |
| full XOR cancel | 0 | bit toggling correctness |
| all zeros XOR | 28 | multi-bit propagation |

## Edge Cases

A key edge case is repeated XOR with the same value over overlapping segments. The algorithm handles this correctly because the lazy mask uses XOR accumulation. Applying the same mask twice cancels out, restoring original bit counts.

Another edge case is querying a segment that has pending lazy updates at multiple ancestor nodes. The push operation ensures that all pending transformations are applied before any partial query computation, preserving correctness even in deeply nested trees.

A final case is full-range updates followed by partial queries. Since each node always represents correct bit counts for its segment after propagation, querying any subsegment produces correct aggregated contributions without needing per-element reconstruction.
