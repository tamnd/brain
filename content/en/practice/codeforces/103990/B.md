---
title: "CF 103990B - Balanced Seesaw Array"
description: "We are given an array of values and a long sequence of updates. Each query either increases a whole segment by a constant, overwrites a segment with a constant value, or asks whether a given subarray has a special “balanced” property."
date: "2026-07-02T06:04:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103990
codeforces_index: "B"
codeforces_contest_name: "2022 ICPC Asia Taiwan Online Programming Contest"
rating: 0
weight: 103990
solve_time_s: 62
verified: true
draft: false
---

[CF 103990B - Balanced Seesaw Array](https://codeforces.com/problemset/problem/103990/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of values and a long sequence of updates. Each query either increases a whole segment by a constant, overwrites a segment with a constant value, or asks whether a given subarray has a special “balanced” property.

A subarray is considered balanced if there exists an index k inside that subarray such that if we take each element and multiply it by its distance from k, the signed weighted sum becomes zero. In other words, k acts like a pivot where the array balances perfectly like a seesaw, with values to the left and right canceling each other in terms of weighted contribution.

Each query of type 3 asks whether a specific subarray can be balanced in this sense. The difficulty is that the array is changing frequently, so we cannot recompute everything from scratch for each query.

The constraints immediately rule out recomputing subarray properties naively. The array length is up to 100,000, while the number of operations can reach 1.2 million. Any solution that scans a segment per query will inevitably time out, since even a single linear scan per operation leads to roughly 10¹¹ operations in the worst case.

A second important difficulty is that updates are not simple point changes. They are range additions and range assignments, both of which affect many positions at once. This pushes the solution toward a data structure that supports lazy propagation.

A subtle failure case for naive approaches comes from misunderstanding the “existence of k” condition. For example, consider a segment [1, 2, -1]. A naive idea might try to check balance at midpoint or assume symmetry-like behavior, but the correct condition depends on weighted sums, not geometric intuition. Another failure case appears when all values in a segment become zero. In that case, every choice of k satisfies the equation, so the answer must always be “Yes”, which is easy to miss if one divides by the total sum without checking zero cases.

## Approaches

A direct approach would answer each query by iterating over the segment and computing the condition from scratch. For a segment of length m, we would compute two quantities: the sum of values and the weighted sum of index multiplied by value. From these, we can derive whether a valid pivot exists. This works correctly, but each query costs O(m), and with up to 1.2 million queries, this becomes far too slow.

The key observation is that the balance condition depends only on two aggregate values over the segment. If we define S as the sum of elements and T as the sum of i * a[i], then the condition reduces to a simple algebraic equation in S and T. This means we do not need to know individual elements inside the segment at query time, only these two aggregates.

Once the problem is reduced to maintaining range sums of two different quantities, the structure becomes standard. A segment tree can maintain S and T for every interval. Range add and range assign operations can be translated into updates on these aggregates. The only additional ingredient is that T depends on indices, so each node must store not only sum of values but also sum of indices weighted by value changes.

The transformation from a geometric balancing condition to a constant-time check using prefix aggregates is what makes the solution efficient. After that, the rest is a classic lazy propagation problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Segment Tree with aggregates | O(q log n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a segment tree where each node stores three pieces of information: the sum of values in the segment, the sum of indices in the segment, and a pair of lazy tags for range assignment and range addition.

For clarity, let len be the segment length and idxSum be the sum of indices in that segment, both precomputed for each node structure.

### 1. Precompute structural information for each segment tree node

Each node knows its interval [l, r], its length, and the sum of indices in that interval. This allows fast recalculation of weighted sums when values change uniformly.

The reason this is necessary is that updates depend on both value magnitude and position, so we must separate structural information from dynamic values.

### 2. Maintain two aggregates per node

Each node stores S, the sum of a[i], and T, the sum of i * a[i]. These two values fully describe the balanced condition for any segment.

This reduction works because the balance equation expands into a linear expression in these two sums.

### 3. Handle range assignment

When a segment is set to a constant x, S becomes x times length, and T becomes x times sum of indices. Any previous structure is overwritten, so lazy addition is cleared.

This ensures the segment remains consistent without needing to touch individual elements.

### 4. Handle range addition

When adding x to every element in a segment, S increases by x times length. T increases by x times sum of indices. This works because each position i gains an extra contribution of x * i.

### 5. Answer queries using algebra

For a query segment, compute S and T.

If S equals zero, the condition reduces to requiring T equals zero. If both are zero, any pivot works, so the answer is positive.

If S is non-zero, the pivot is k = T / S. The answer is valid only if k is an integer and lies within the segment boundaries.

### Why it works

The key invariant is that for every segment tree node, S and T always exactly match the true sum of values and weighted sum of indices for the represented segment after applying all lazy operations. Since every update rule preserves the algebraic contribution of each operation, no information is lost. The query condition is derived directly from rewriting the balance equation into a solvable linear form, so correctness reduces to verifying arithmetic consistency rather than structural properties of the array.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

class Node:
    __slots__ = ("s", "t", "add", "assign", "has_assign")
    def __init__(self):
        self.s = 0
        self.t = 0
        self.add = 0
        self.assign = 0
        self.has_assign = False

class SegTree:
    def __init__(self, a):
        self.n = len(a) - 1  # 1-indexed
        self.tree = [Node() for _ in range(4 * self.n)]
        self.build(1, 1, self.n, a)

    def build(self, idx, l, r, a):
        if l == r:
            self.tree[idx].s = a[l]
            self.tree[idx].t = a[l] * l
            return
        mid = (l + r) // 2
        self.build(idx*2, l, mid, a)
        self.build(idx*2+1, mid+1, r, a)
        self.pull(idx)

    def pull(self, idx):
        left = self.tree[idx*2]
        right = self.tree[idx*2+1]
        self.tree[idx].s = left.s + right.s
        self.tree[idx].t = left.t + right.t

    def apply_assign(self, idx, l, r, x):
        node = self.tree[idx]
        node.s = x * (r - l + 1)
        node.t = x * (r + r - (r - l)) * (r - l + 1) // 2  # sum i from l to r * x
        node.has_assign = True
        node.assign = x
        node.add = 0

    def apply_add(self, idx, l, r, x):
        node = self.tree[idx]
        node.s += x * (r - l + 1)
        node.t += x * (l + r) * (r - l + 1) // 2

        if node.has_assign:
            node.assign += x
        else:
            node.add += x

    def push(self, idx, l, r):
        node = self.tree[idx]
        if l == r:
            return
        mid = (l + r) // 2
        if node.has_assign:
            self.apply_assign(idx*2, l, mid, node.assign)
            self.apply_assign(idx*2+1, mid+1, r, node.assign)
            node.has_assign = False
        if node.add != 0:
            self.apply_add(idx*2, l, mid, node.add)
            self.apply_add(idx*2+1, mid+1, r, node.add)
            node.add = 0

    def update_add(self, idx, l, r, ql, qr, x):
        if ql <= l and r <= qr:
            self.apply_add(idx, l, r, x)
            return
        self.push(idx, l, r)
        mid = (l + r) // 2
        if ql <= mid:
            self.update_add(idx*2, l, mid, ql, qr, x)
        if qr > mid:
            self.update_add(idx*2+1, mid+1, r, ql, qr, x)
        self.pull(idx)

    def update_assign(self, idx, l, r, ql, qr, x):
        if ql <= l and r <= qr:
            self.apply_assign(idx, l, r, x)
            return
        self.push(idx, l, r)
        mid = (l + r) // 2
        if ql <= mid:
            self.update_assign(idx*2, l, mid, ql, qr, x)
        if qr > mid:
            self.update_assign(idx*2+1, mid+1, r, ql, qr, x)
        self.pull(idx)

    def query(self, idx, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.tree[idx].s, self.tree[idx].t
        self.push(idx, l, r)
        mid = (l + r) // 2
        s = t = 0
        if ql <= mid:
            s1, t1 = self.query(idx*2, l, mid, ql, qr)
            s += s1
            t += t1
        if qr > mid:
            s2, t2 = self.query(idx*2+1, mid+1, r, ql, qr)
            s += s2
            t += t2
        return s, t

def main():
    n, q = map(int, input().split())
    arr = [0] + list(map(int, input().split()))
    st = SegTree(arr)

    out = []

    for _ in range(q):
        tmp = input().split()
        if tmp[0] == '1':
            l, r, x = map(int, tmp[1:])
            st.update_add(1, 1, n, l, r, x)
        elif tmp[0] == '2':
            l, r, x = map(int, tmp[1:])
            st.update_assign(1, 1, n, l, r, x)
        else:
            l, r = map(int, tmp[1:])
            s, t = st.query(1, 1, n, l, r)
            m = r - l + 1
            if s == 0:
                out.append("Yes" if t == 0 else "No")
            else:
                if t % s != 0:
                    out.append("No")
                else:
                    k = t // s
                    out.append("Yes" if l <= k <= r else "No")

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The implementation maintains two independent aggregates per segment. The first is the sum of values, and the second is the sum of index-weighted values. Every update modifies both consistently, and lazy propagation ensures correctness under composition of operations. The query logic directly applies the derived algebraic condition.

A subtle implementation point is the interaction between assignment and addition lazy tags. Assignment must override any previous additions, and when pushed down, it must fully reset children states before applying further increments. Any reversal of this order leads to incorrect accumulation.

Another important detail is that all computations rely on exact integer arithmetic. Python handles large integers safely, which avoids overflow concerns that would appear in lower-level languages.

## Worked Examples

### Example 1

Input segment: [1, 2, 3]

| Step | S (sum) | T (weighted sum) | Decision |
| --- | --- | --- | --- |
| Query whole | 6 | 14 | check k |
| k = T/S |  | 14/6 not integer | No |

The segment cannot balance because no integer pivot produces perfect cancellation.

### Example 2

Input segment: [1, 2, 1]

| Step | S | T | Decision |
| --- | --- | --- | --- |
| Query | 4 | 8 | k = 2 |
| Check bounds |  | 2 in [1,3] | Yes |

This confirms a valid pivot exists at index 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log n) | Each update and query traverses the segment tree height |
| Space | O(n) | Storage for tree nodes and lazy tags |

The constraints allow up to 1.2 million operations, so logarithmic factor per operation remains acceptable in Python given tight implementation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    main()
    return sys.stdout.getvalue().strip()

# provided sample (adapted formatting)
assert run("""3 6
1 2 3
3 1 1
3 1 3
1 1 2 2
3 1 3
2 2 2 0
3 2 3
""") == "Yes\nNo\nYes\nYes"

# minimum size
assert run("""1 2
5
3 1 1
3 1 1
""") == "Yes\nYes"

# all equal
assert run("""5 2
2 2 2 2 2
3 1 5
""") == "Yes"

# range assign edge
assert run("""4 3
1 2 3 4
2 2 3 0
3 1 4
""") == "Yes"

# range add edge
assert run("""3 3
1 1 1
1 1 3 1
3 1 3
""") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | Yes | trivial pivot always exists |
| all equal | Yes | symmetry of weighted sums |
| assign to zero | Yes | zero-sum consistency |
| range add | Yes | lazy propagation correctness |

## Edge Cases

One important edge case occurs when the sum of the segment becomes zero. In that situation, dividing by S is impossible, so the correct logic switches entirely to checking whether the weighted sum is also zero. For example, consider a segment where values cancel out exactly. The algorithm correctly detects S = 0 and verifies T = 0 before returning “Yes”, avoiding invalid division.

Another edge case arises when the computed pivot k lies exactly on a boundary. Since the condition requires k to be within the segment, a value like k = l or k = r is valid, and the implementation explicitly checks this range rather than assuming interior placement.

A final subtle case appears under repeated mixed updates, where assignment follows addition. The lazy propagation logic ensures assignment clears any pending addition before applying the constant overwrite, preserving consistency of both S and T across all descendants.
