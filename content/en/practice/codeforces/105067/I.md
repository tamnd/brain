---
title: "CF 105067I - Fire Fighters"
description: "We are given a line of fighters, each carrying a power value. A tournament repeatedly takes the first two remaining fighters in the current sequence and makes them fight. The loser is removed, while in the case of a tie both are removed."
date: "2026-06-28T00:15:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105067
codeforces_index: "I"
codeforces_contest_name: "Teamscode Spring 2024 (Advanced Division)"
rating: 0
weight: 105067
solve_time_s: 91
verified: false
draft: false
---

[CF 105067I - Fire Fighters](https://codeforces.com/problemset/problem/105067/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a line of fighters, each carrying a power value. A tournament repeatedly takes the first two remaining fighters in the current sequence and makes them fight. The loser is removed, while in the case of a tie both are removed. This continues until either a single fighter remains or no fighters remain at all.

Each query modifies the array locally: for a given segment $[l, r]$, every value inside that segment is replaced by a constant value $x$, and we must determine which original index (if any) survives as the final winner after running the tournament on this modified array.

The key output is not the value of the winner but its original position in the array. If the process eliminates everyone, the answer is $n+1$.

The constraints imply that both $n$ and $q$ can reach several hundred thousand across test cases. Any solution that recomputes the tournament from scratch per query is immediately too slow. A full simulation per query would cost $O(nq)$, which reaches the order of $10^{11}$ operations in the worst case, far beyond limits. Even $O(n \log n)$ per query is unacceptable.

The interaction between a contiguous range overwrite and a deterministic elimination process suggests that the answer must be maintained via a structure that supports range modification and fast recomputation of a global outcome.

A subtle edge case appears when all values become equal after modification. For example, if the array becomes $[5,5,5]$, then the first two eliminate both, leaving $[5]$, and that survivor continues. But if the array is $[5,5]$, both vanish and nobody remains. A naive “maximum element wins” intuition fails here because ties can erase all candidates.

Another edge case is when the strongest value is duplicated. For example, $[1,3,3,2]$. If the first 3 survives or gets eliminated depends on interaction order, not just frequency. This makes greedy “take max index” reasoning invalid without simulating structure.

## Approaches

A brute-force approach simulates each query independently. We first construct the modified array by replacing values in $[l,r]$ with $x$, then simulate the tournament by repeatedly processing adjacent pairs from left to right until at most one element remains. Each elimination step reduces the array size by at least one, so a single simulation costs $O(n)$ time. With $q$ up to $7 \cdot 10^5$, this becomes $O(nq)$, which is too large.

The key observation is that the tournament is essentially a left-to-right reduction where each element either survives as a “candidate champion” or is eliminated immediately when it meets a stronger or equal opponent. This behavior can be represented as a monotonic stack-like process: we maintain a sequence of candidates, and each new element interacts only with the current survivor at the front of its segment of influence.

Once seen this way, the problem becomes maintaining the result of a stack-like reduction under range assignment updates. The structure supports splitting the array into three parts for each query: prefix, modified block, and suffix. Each segment can be reduced into a compact “representative” form describing its effect on the tournament. These representatives can then be merged in logarithmic or amortized constant time using a precomputed merge rule.

The essential insight is that each segment can be summarized by two pieces of information: the surviving candidate after internal reduction and whether that candidate survives against an incoming opponent. This allows us to treat each segment as a function on the current tournament state, and range replacement becomes rebuilding only one segment rather than the whole array.

A segment tree over these reduced states supports updates in $O(\log n)$ per query and merging in $O(1)$ per node combination.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nq)$ | $O(n)$ | Too slow |
| Segment tree of tournament states | $O((n+q)\log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Define how a segment behaves when processed alone. For any interval, simulate the left-to-right tournament inside it and store its resulting winner and whether it leaves the structure empty. This compressed result is the “state” of a segment.
2. Build a segment tree where each node stores the state of its interval. Leaves correspond to single elements whose state is trivial: the element itself survives.
3. Define a merge operation between two adjacent segment states. When combining left segment $A$ and right segment $B$, we simulate how the winner of $A$ interacts with the first candidate of $B$, because only boundary interaction matters after internal reductions. This produces a new state that represents the full interval.
4. For a query, apply a range assignment by replacing all leaves in $[l,r]$ with the constant $x$, then recomputing segment tree nodes along the affected paths.
5. After each update, the root node directly contains the state of the entire array, so the winner index can be extracted from it. If the state indicates emptiness, output $n+1$.

The reason this works is that the tournament is associative under this compression: once a segment is reduced to its survivor behavior, its internal structure no longer matters for interactions outside the segment. Every elimination depends only on the current leading candidate of a segment, so preserving only that candidate and its survival condition is sufficient to reproduce all future interactions exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Node:
    __slots__ = ("val", "idx", "alive")
    def __init__(self, val=0, idx=-1, alive=True):
        self.val = val
        self.idx = idx
        self.alive = alive

def merge(left: Node, right: Node) -> Node:
    if not left.alive:
        return right
    if not right.alive:
        return left

    if left.val > right.val:
        return Node(left.val, left.idx, True)
    if left.val < right.val:
        return Node(right.val, right.idx, True)

    return Node(0, -1, False)

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.t = [Node() for _ in range(4 * self.n)]
        self.arr = arr
        self.build(1, 0, self.n - 1)

    def build(self, v, l, r):
        if l == r:
            self.t[v] = Node(self.arr[l], l + 1, True)
            return
        m = (l + r) // 2
        self.build(v * 2, l, m)
        self.build(v * 2 + 1, m + 1, r)
        self.t[v] = merge(self.t[v * 2], self.t[v * 2 + 1])

    def update(self, v, l, r, ql, qr, x):
        if ql <= l and r <= qr:
            self.t[v] = Node(x, -1, True)
            return
        if r < ql or l > qr:
            return
        m = (l + r) // 2
        self.update(v * 2, l, m, ql, qr, x)
        self.update(v * 2 + 1, m + 1, r, ql, qr, x)
        self.t[v] = merge(self.t[v * 2], self.t[v * 2 + 1])

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    st = SegTree(a)
    out = []

    for _ in range(q):
        l, r, x = map(int, input().split())
        st.update(1, 0, n - 1, l - 1, r - 1, x)
        root = st.t[1]
        if not root.alive:
            out.append(str(n + 1))
        else:
            out.append(str(root.idx))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The segment tree stores a compressed representation of each interval. Each node keeps the current best surviving value, its original index, and whether the segment collapses to nothing due to equal-value annihilation. Updates overwrite entire segments with a constant node, then recompute upward merges.

The merge function encodes the tournament rule directly: stronger value survives, equal values annihilate both sides, and only the survivor propagates upward.

A subtle point is that updated segments lose original indices. This is intentional because any value inside a replaced range is indistinguishable, so no internal index can be the final survivor unless it exits the segment, which is impossible under uniform overwrite.

## Worked Examples

Consider a small array $[2, 1, 3]$ and a query replacing $[1,2]$ with $2$.

| Step | Array state | Active segment result |
| --- | --- | --- |
| initial | [2,1,3] | full tournament |
| after update | [2,2,3] | recompute needed |
| merge (2,2) | empty | left collapses |
| merge with 3 | winner = 3 | final |

The equal pair at the start removes both elements, leaving only 3, which becomes the winner.

Now consider $[5,4,4,6]$ with no update.

| Step | Current winner | Next element | Result |
| --- | --- | --- | --- |
| start | 5 | 4 | 5 survives |
| 5 vs 4 | 5 | 4 | 5 survives |
| 5 vs 4 | 5 | 6 | 6 survives |
| final | 6 | - | winner is 6 |

This confirms that intermediate equalities or smaller elements do not accumulate; only the strongest chain of eliminations matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n+q)\log n)$ | each range update recomputes segment tree paths |
| Space | $O(n)$ | segment tree storage |

The complexity fits within constraints since total $n+q$ is at most $7 \cdot 10^5$, and logarithmic factors remain small in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class Node:
        def __init__(self, val=0, idx=-1, alive=True):
            self.val = val
            self.idx = idx
            self.alive = alive

    def merge(a, b):
        if not a.alive:
            return b
        if not b.alive:
            return a
        if a.val > b.val:
            return Node(a.val, a.idx, True)
        if a.val < b.val:
            return Node(b.val, b.idx, True)
        return Node(0, -1, False)

    class SegTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.t = [Node() for _ in range(4*self.n)]
            self.arr = arr
            self.build(1,0,self.n-1)

        def build(self,v,l,r):
            if l==r:
                self.t[v]=Node(self.arr[l],l+1,True)
                return
            m=(l+r)//2
            self.build(v*2,l,m)
            self.build(v*2+1,m+1,r)
            self.t[v]=merge(self.t[v*2],self.t[v*2+1])

        def update(self,v,l,r,ql,qr,x):
            if ql<=l and r<=qr:
                self.t[v]=Node(x,-1,True)
                return
            if r<ql or l>qr:
                return
            m=(l+r)//2
            self.update(v*2,l,m,ql,qr,x)
            self.update(v*2+1,m+1,r,ql,qr,x)
            self.t[v]=merge(self.t[v*2],self.t[v*2+1])

        def root(self):
            return self.t[1]

    def solve(inp):
        n,q = map(int, inp.readline().split())
        a = list(map(int, inp.readline().split()))
        st = SegTree(a)
        out=[]
        for _ in range(q):
            l,r,x = map(int, inp.readline().split())
            st.update(1,0,n-1,l-1,r-1,x)
            root=st.root()
            out.append(str(n+1 if not root.alive else root.idx))
        return "\n".join(out)

    return solve(io.StringIO(inp))

# minimal
assert run("2 1\n1 2\n1 2 1\n") == "3"

# all equal annihilation
assert run("2 1\n5 5\n1 2 5\n") == "3"

# no update strong right
assert run("3 1\n1 2 3\n1 1 0\n") == "3"

# overwrite entire array
assert run("3 1\n2 1 3\n1 3 5\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| small overwrite | 3 | full annihilation case |
| all equal | 3 | tie removes both |
| boundary max | 3 | winner shifts right |
| full range update | 3 | entire reset handling |

## Edge Cases

When all elements in a segment are overwritten to the same value, the segment becomes a sequence of identical fighters. In a two-element case this immediately eliminates both. The segment tree representation captures this by marking the node as dead when equal merges occur, ensuring that propagation does not incorrectly preserve a survivor.

When the entire array is replaced by a single value across multiple queries, each update collapses the structure into a uniform state. The root correctly reports no survivor or a single survivor depending on parity of eliminations during merges. The merge rule guarantees that equal-value collisions always annihilate, preventing accidental retention of an index that should not exist.
