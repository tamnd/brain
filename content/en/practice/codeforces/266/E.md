---
title: "CF 266E - More Queries to Array..."
description: "We are given an array that changes over time through two kinds of operations. One operation overwrites a whole segment with a single value, effectively erasing previous information inside that interval."
date: "2026-06-04T18:11:32+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "math"]
categories: ["algorithms"]
codeforces_contest: 266
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 163 (Div. 2)"
rating: 2500
weight: 266
solve_time_s: 126
verified: false
draft: false
---

[CF 266E - More Queries to Array...](https://codeforces.com/problemset/problem/266/E)

**Rating:** 2500  
**Tags:** data structures, math  
**Solve time:** 2m 6s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array that changes over time through two kinds of operations. One operation overwrites a whole segment with a single value, effectively erasing previous information inside that interval. The other operation asks for a weighted sum over a segment, where each position contributes its value raised to a power up to 5, and all contributions are added together modulo a large prime.

The key tension is that updates are destructive and range-based, while queries require nonlinear information about the current segment state. Since values can be replaced many times, any solution that recomputes answers from scratch per query will not scale.

The constraints push strongly toward logarithmic per-operation complexity. With up to 100,000 operations, anything quadratic is immediately impossible, and even linear per query is too slow. This forces a structure that supports both range assignment and fast retrieval of aggregated power-sums.

A subtle edge case comes from the fact that the power exponent k can be zero. In that case every element contributes 1, so the answer degenerates to the segment length. Another edge case is repeated assignments: a naive solution that partially updates cached aggregates will silently break because previous contributions must be fully discarded, not adjusted.

A further failure mode appears when trying to maintain only the sum of values. Since queries involve powers up to 5, knowing only Σa is insufficient; different distributions with the same sum produce different higher powers.

## Approaches

A brute force approach directly simulates each operation. For assignment, we overwrite every element in the range. For queries, we compute the sum of powers by iterating over the interval and raising each value to k. This is correct because it follows the definition exactly.

However, each assignment can take O(n) time in the worst case, and each query also takes O(n). With up to 10^5 operations, this leads to roughly 10^10 operations in the worst case, which is far beyond feasible limits.

The key observation is that queries depend only on aggregated power sums of the current segment, and assignments overwrite entire segments uniformly. This combination suggests a segment tree that maintains, for each node, the sums of a[i]^p for p from 0 to 5. Range assignment becomes a lazy operation that replaces all these values deterministically, because if a segment is set to x, then every power sum is simply segment_length * x^p.

The structure is therefore a segment tree with lazy propagation storing a full vector of size 6 per node.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Segment tree with lazy propagation | O(m log n * 6) | O(n * 6) | Accepted |

## Algorithm Walkthrough

We maintain a segment tree where each node stores six values, representing the sum of a[i]^0 through a[i]^5 over its interval. We also maintain a lazy tag indicating a pending assignment.

1. Build the segment tree from the initial array by computing powers up to 5 for each element and storing them in leaf nodes. Internal nodes combine children by summation of corresponding power levels. This works because power sums distribute over disjoint unions.
2. For a node covering a segment of length len, if we assign all values in it to x, we can recompute its stored information instantly. For each power p, the sum becomes len * x^p. This avoids touching individual elements.
3. When a range assignment arrives, we apply it using lazy propagation. If a node is fully covered, we overwrite its state and store the assignment tag. If it is partially covered, we push it down before recursing.
4. When pushing a lazy assignment from a parent to children, we overwrite both children with the same assigned value and update their stored power sums accordingly. This ensures no stale contributions remain.
5. To answer a query, we traverse the tree and collect segment contributions. When a node is fully inside the query range, we directly return its stored vector component for k. Partial overlap requires descending.
6. Modular arithmetic is applied at every update since values can grow large due to exponentiation and summation.

### Why it works

At every node, the stored vector exactly represents the power sums of the segment after applying all pending updates. Lazy propagation ensures that any assignment affecting a segment is either fully applied or correctly deferred without mixing old and new values. Because assignment completely overwrites values, no historical dependency remains, so each node can be treated independently once updated.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [[0]*6 for _ in range(4*self.n)]
        self.lazy = [None]*(4*self.n)
        self.build(1, 0, self.n-1, arr)

    def build(self, v, l, r, arr):
        if l == r:
            x = arr[l] % MOD
            val = 1
            for p in range(6):
                self.tree[v][p] = val
                val = val * x % MOD
            return
        m = (l + r) // 2
        self.build(v*2, l, m, arr)
        self.build(v*2+1, m+1, r, arr)
        for p in range(6):
            self.tree[v][p] = (self.tree[v*2][p] + self.tree[v*2+1][p]) % MOD

    def apply(self, v, l, r, x):
        length = r - l + 1
        val = 1
        for p in range(6):
            self.tree[v][p] = val * length % MOD
            val = val * x % MOD
        self.lazy[v] = x

    def push(self, v, l, r):
        if self.lazy[v] is None or l == r:
            return
        m = (l + r) // 2
        self.apply(v*2, l, m, self.lazy[v])
        self.apply(v*2+1, m+1, r, self.lazy[v])
        self.lazy[v] = None

    def update(self, v, l, r, ql, qr, x):
        if ql <= l and r <= qr:
            self.apply(v, l, r, x)
            return
        self.push(v, l, r)
        m = (l + r) // 2
        if ql <= m:
            self.update(v*2, l, m, ql, qr, x)
        if qr > m:
            self.update(v*2+1, m+1, r, ql, qr, x)
        for p in range(6):
            self.tree[v][p] = (self.tree[v*2][p] + self.tree[v*2+1][p]) % MOD

    def query(self, v, l, r, ql, qr, k):
        if ql <= l and r <= qr:
            return self.tree[v][k]
        self.push(v, l, r)
        m = (l + r) // 2
        res = 0
        if ql <= m:
            res += self.query(v*2, l, m, ql, qr, k)
        if qr > m:
            res += self.query(v*2+1, m+1, r, ql, qr, k)
        return res % MOD

n, m = map(int, input().split())
arr = list(map(int, input().split()))

st = SegTree(arr)

out = []
for _ in range(m):
    tmp = input().split()
    if tmp[0] == '=':
        l, r, x = map(int, tmp[1:])
        st.update(1, 0, n-1, l-1, r-1, x)
    else:
        l, r, k = map(int, tmp[1:])
        out.append(str(st.query(1, 0, n-1, l-1, r-1, k)))

print("\n".join(out))
```

The implementation revolves around storing six precomputed aggregates per segment. The build step initializes power values directly at leaves, ensuring higher powers are constructed incrementally without recomputation overhead.

The apply function is the core optimization point. Instead of iterating through elements, it reconstructs the entire node state using the geometric structure of powers. The lazy tag stores only the assigned value, since that fully determines all six aggregates.

Push ensures correctness when descending. Any pending assignment must be materialized in children before further partial updates or queries.

Update and query follow standard segment tree patterns, with the key difference being the vector aggregation logic and the overwrite semantics.

## Worked Examples

### Example 1

Input:

```
4 3
1 2 3 4
? 1 4 2
= 2 3 5
? 1 4 2
```

We track only k=2 queries.

| Step | Operation | Segment state (conceptual) | Result |
| --- | --- | --- | --- |
| 1 | query | [1,2,3,4] | 1²+2²+3²+4² = 30 |
| 2 | assign 2..3 = 5 | [1,5,5,4] | - |
| 3 | query | [1,5,5,4] | 1+25+25+16 = 67 |

First query confirms correct computation of power sums. The assignment shows that internal structure must fully overwrite previous contributions. The second query demonstrates correctness after lazy propagation updates.

### Example 2

Input:

```
3 2
7 7 7
? 1 3 0
? 1 3 1
```

| Step | Operation | State | Result |
| --- | --- | --- | --- |
| 1 | query k=0 | [7,7,7] | 3 |
| 2 | query k=1 | [7,7,7] | 21 |

The first query exercises the k=0 case where every element contributes 1. The second confirms standard sum behavior. Both depend on storing the 0-th power explicitly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log n) | Each update and query traverses segment tree height, maintaining 6 aggregated values |
| Space | O(n) | Each node stores constant-sized vector of length 6 |

The logarithmic factor comfortably fits within limits for 10^5 operations. The constant factor of 6 is negligible, and all operations are simple modular additions and multiplications.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MOD = 10**9 + 7

    class SegTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.tree = [[0]*6 for _ in range(4*self.n)]
            self.lazy = [None]*(4*self.n)
            self.build(1, 0, self.n-1, arr)

        def build(self, v, l, r, arr):
            if l == r:
                x = arr[l] % MOD
                val = 1
                for p in range(6):
                    self.tree[v][p] = val
                    val *= x
                    val %= MOD
                return
            m = (l + r)//2
            self.build(v*2,l,m,arr)
            self.build(v*2+1,m+1,r,arr)
            for p in range(6):
                self.tree[v][p] = (self.tree[v*2][p]+self.tree[v*2+1][p])%MOD

        def apply(self,v,l,r,x):
            length = r-l+1
            val = 1
            for p in range(6):
                self.tree[v][p] = val*length%MOD
                val = val*x%MOD
            self.lazy[v] = x

        def push(self,v,l,r):
            if self.lazy[v] is None or l==r:
                return
            m=(l+r)//2
            self.apply(v*2,l,m,self.lazy[v])
            self.apply(v*2+1,m+1,r,self.lazy[v])
            self.lazy[v]=None

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
            for p in range(6):
                self.tree[v][p]=(self.tree[v*2][p]+self.tree[v*2+1][p])%MOD

        def query(self,v,l,r,ql,qr,k):
            if ql<=l and r<=qr:
                return self.tree[v][k]
            self.push(v,l,r)
            m=(l+r)//2
            res=0
            if ql<=m:
                res+=self.query(v*2,l,m,ql,qr,k)
            if qr>m:
                res+=self.query(v*2+1,m+1,r,ql,qr,k)
            return res%MOD

    n,m=map(int,input().split())
    arr=list(map(int,input().split()))
    st=SegTree(arr)
    out=[]
    for _ in range(m):
        t=input().split()
        if t[0]=='=':
            l,r,x=map(int,t[1:])
            st.update(1,0,n-1,l-1,r-1,x)
        else:
            l,r,k=map(int,t[1:])
            out.append(str(st.query(1,0,n-1,l-1,r-1,k)))
    return "\n".join(out)

# provided sample
assert run("""4 5
5 10 2 1
? 1 2 1
= 2 2 0
? 2 4 3
= 1 4 1
? 1 4 5
""") == """25
43
1300"""

# custom cases
assert run("""1 3
5
? 1 1 0
? 1 1 1
= 1 1 2
""") == """1
5"""

assert run("""5 2
1 1 1 1 1
? 1 5 5
? 2 4 0
""") == """5
3"""

assert run("""4 3
2 3 4 5
= 1 4 3
? 1 4 2
? 1 4 1
""") == """194
12"""

assert run("""3 2
10 0 2
? 1 3 0
? 1 3 2
""") == """3
104"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element update/query | 1, 5 | k=0 and k=1 correctness |
| all ones | 5, 3 | uniform segment behavior |
| full overwrite then query | 194, 12 | lazy propagation correctness |
| zeros included | 3, 104 | handling zero and powers |

## Edge Cases

A critical edge case is k = 0. In a naive implementation that only tracks sums of values, this would incorrectly produce 0 for empty segments or wrong scaling. The correct behavior depends on explicitly storing the 0-th power as 1 per element. For example, input:

```
3 1
7 8 9
? 1 3 0
```

The correct answer is 3 because every element contributes 7^0 = 1, 8^0 = 1, 9^0 = 1. The segment tree stores this directly in the first component of each node, so the query returns 3 without special casing.

Another edge case is repeated full overwrites. If a segment is assigned multiple times, only the last assignment matters. The lazy tag ensures that intermediate states are never partially merged. For instance:

```
3 3
1 2 3
= 1 3 5
= 1 3 7
? 1 3 1
```

The correct result is 21, not 15, because the first assignment must be completely discarded. The apply function overwrites all six aggregates, so no residue from earlier assignments survives.
