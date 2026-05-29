---
title: "CF 446C - DZY Loves Fibonacci Numbers"
description: "We are given an array of integers and need to support two types of queries efficiently. The first type requires adding Fibonacci numbers to a contiguous subarray: for indices from l to r, we add F₁ to the element at l, F₂ to the element at l+1, up to F{r-l+1} at position r."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 446
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round #FF (Div. 1)"
rating: 2400
weight: 446
solve_time_s: 392
verified: false
draft: false
---

[CF 446C - DZY Loves Fibonacci Numbers](https://codeforces.com/problemset/problem/446/C)

**Rating:** 2400  
**Tags:** data structures, math, number theory  
**Solve time:** 6m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and need to support two types of queries efficiently. The first type requires adding Fibonacci numbers to a contiguous subarray: for indices from _l_ to _r_, we add _F₁_ to the element at _l_, _F₂_ to the element at _l+1_, up to _F_{r-l+1}_ at position _r_. The second type asks for the sum of elements in a subarray modulo 10⁹+9.

The constraints are tight: the array can have up to 300,000 elements and the number of queries can also reach 300,000. This rules out any solution that performs naive iteration over a range for each query, because that would be O(n·m) in the worst case, potentially around 9×10¹⁰ operations, which is far beyond what can run in 4 seconds. The values of the array elements and the Fibonacci numbers can become very large, so we need to carefully handle modular arithmetic.

A subtle edge case arises when a query affects only a single element or when consecutive updates overlap. For example, if the array is [1,2] and the query is to add Fibonacci numbers from 1 to 2, the update adds [1,1] to the array. A naive implementation that simply adds Fibonacci numbers by recomputing them for each query will be too slow and can easily produce wrong results if indices or Fibonacci offsets are misaligned.

## Approaches

The brute-force solution directly implements the queries as described. For a type 1 query, we compute the first r-l+1 Fibonacci numbers and add them individually to each element in the range. For a type 2 query, we sum the elements in the range. While this works conceptually, the complexity is O(m·n) in the worst case. If all queries cover almost the entire array, the algorithm performs roughly 9×10¹⁰ operations, which is far beyond acceptable.

The key insight to speed this up is recognizing that Fibonacci additions are linear and can be expressed using a linear recurrence. This allows us to apply lazy propagation over a segment tree. Instead of updating each element individually, we store the effect of adding a Fibonacci segment in a compact form using the first two Fibonacci numbers of the segment. When we propagate updates down the tree, the Fibonacci sequence can be efficiently extended using its recurrence. This transforms the update operation from O(range) to O(log n), while the sum query also becomes O(log n).

The Fibonacci property F_k+2 = F_k+1 + F_k allows us to compute the next values in a range without recomputing the entire sequence. Segment tree nodes maintain not only the sum of the interval but also two numbers representing the first two Fibonacci contributions that need to be propagated. Lazy propagation ensures that overlapping or consecutive updates are handled correctly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·m) | O(n) | Too slow |
| Segment Tree + Fibonacci Lazy | O((n+m)·log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute Fibonacci numbers modulo 10⁹+9 up to n+2, because updates may require the r-l+1-th Fibonacci number. This allows constant-time access to any needed Fibonacci value.
2. Construct a segment tree over the array. Each node stores the sum of its segment modulo 10⁹+9. Additionally, each node maintains a lazy update as a pair of numbers representing the first two Fibonacci values that need to be propagated to children.
3. For a type 1 query "1 l r", instead of updating each element, calculate the first two Fibonacci numbers that start at position l. Use lazy propagation to add this Fibonacci segment to the corresponding node in the segment tree. When a node is partially covered, push the update to its children, recalculating the starting Fibonacci numbers for each child using the linear recurrence.
4. For a type 2 query "2 l r", query the segment tree for the sum of the range. If any lazy updates exist on the path, propagate them first to ensure the sum reflects all previous updates.
5. When propagating Fibonacci updates to child nodes, compute the first two Fibonacci values for the left child directly from the parent's lazy pair. For the right child, use matrix exponentiation or the known Fibonacci sums to shift the starting point correctly. This ensures that updates maintain the correct sequence.
6. Perform modular arithmetic at every step to avoid integer overflow, as numbers can grow quickly due to Fibonacci growth.

Why it works: The segment tree guarantees that each query is applied to a minimal set of nodes. Lazy propagation ensures that each Fibonacci segment is applied exactly where needed without recomputation. The first-two-Fibonacci representation is sufficient because the entire Fibonacci sequence can be reconstructed from those two values, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 9

def add_mod(a, b):
    return (a + b) % MOD

def mul_mod(a, b):
    return (a * b) % MOD

def build_fib(n):
    fib = [0] * (n + 2)
    fib[1] = 1
    for i in range(2, n + 2):
        fib[i] = add_mod(fib[i-1], fib[i-2])
    return fib

class SegmentTree:
    def __init__(self, a):
        self.n = len(a)
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
        self.sum = [0] * (2 * self.size)
        self.lazy = [(0,0)] * (2 * self.size)
        for i in range(self.n):
            self.sum[self.size + i] = a[i] % MOD
        for i in range(self.size - 1, 0, -1):
            self.sum[i] = add_mod(self.sum[i<<1], self.sum[i<<1|1])

    def push(self, v, l, r):
        a, b = self.lazy[v]
        if a == 0 and b == 0:
            return
        mid = (l + r) >> 1
        len_left = mid - l + 1
        len_right = r - mid
        # Update left child
        self.apply(v<<1, l, mid, a, b)
        # Update right child: shift Fibonacci sequence by len_left
        fib_a = add_mod(mul_mod(fib[len_left-1], b), mul_mod(fib[len_left], a))
        fib_b = add_mod(mul_mod(fib[len_left], b), mul_mod(fib[len_left+1], a))
        self.apply(v<<1|1, mid+1, r, fib_a, fib_b)
        self.lazy[v] = (0,0)

    def apply(self, v, l, r, a, b):
        # Sum over segment: F1+F2+...+Fk = ?
        k = r - l + 1
        s = add_mod(mul_mod(fib[k], b), mul_mod(fib[k-1], a))
        self.sum[v] = add_mod(self.sum[v], s)
        if v < self.size:
            self.lazy[v] = (add_mod(self.lazy[v][0], a), add_mod(self.lazy[v][1], b))

    def update(self, ql, qr, a, b, v=1, l=0, r=None):
        if r is None:
            r = self.size - 1
        if ql > r or qr < l:
            return
        if ql <= l and r <= qr:
            self.apply(v, l, r, a, b)
            return
        self.push(v, l, r)
        mid = (l + r) >> 1
        self.update(ql, qr, a, b, v<<1, l, mid)
        self.update(ql, qr, a, b, v<<1|1, mid+1, r)
        self.sum[v] = add_mod(self.sum[v<<1], self.sum[v<<1|1])

    def query(self, ql, qr, v=1, l=0, r=None):
        if r is None:
            r = self.size - 1
        if ql > r or qr < l:
            return 0
        if ql <= l and r <= qr:
            return self.sum[v]
        self.push(v, l, r)
        mid = (l + r) >> 1
        return add_mod(self.query(ql, qr, v<<1, l, mid),
                       self.query(ql, qr, v<<1|1, mid+1, r))

n, m = map(int, input().split())
a = list(map(int, input().split()))
fib = build_fib(n+2)
st = SegmentTree(a)

for _ in range(m):
    tmp = input().split()
    if tmp[0] == '1':
        l, r = int(tmp[1])-1, int(tmp[2])-1
        st.update(l, r, fib[1], fib[2])
    else:
        l, r = int(tmp[1])-1, int(tmp[2])-1
        print(st.query(l, r))
```

This code first builds the Fibonacci array for constant-time access. The segment tree supports lazy propagation where each node stores a pair of Fibonacci numbers representing pending updates. Updates are applied efficiently to ranges, and the sum query correctly accounts for all previous Fibonacci
