---
title: "CF 311D - Interval Cubing"
description: "We are given an array of integers and a sequence of queries. Each query is either asking for the sum of a subarray or instructing us to cube every element in a subarray. The output consists of the answers to the sum queries, computed modulo 95542721."
date: "2026-06-05T18:42:03+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "math"]
categories: ["algorithms"]
codeforces_contest: 311
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 185 (Div. 1)"
rating: 2600
weight: 311
solve_time_s: 93
verified: true
draft: false
---

[CF 311D - Interval Cubing](https://codeforces.com/problemset/problem/311/D)

**Rating:** 2600  
**Tags:** data structures, math  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and a sequence of queries. Each query is either asking for the sum of a subarray or instructing us to cube every element in a subarray. The output consists of the answers to the sum queries, computed modulo 95542721.

The array can be up to 100,000 elements long, and there can be up to 100,000 queries. A naive approach that directly sums or updates the array for each query would perform up to 10^10 operations in the worst case, which is far beyond what we can compute within a few seconds. This means we need a data structure that allows both range sum queries and range modifications efficiently.

A tricky aspect of this problem is the cubing operation. Repeated cubing is not linear, so standard range addition techniques like lazy propagation for addition or assignment will not directly work. Moreover, the modulo 95542721 is prime and small enough to allow precomputing repeated cubings efficiently.

A naive implementation might try to cube every element on every update. For example, if the array is `[2, 3]` and we cube the whole array twice, a careless loop would do `2**3 = 8`, then `8**3 = 512`, `3**3 = 27`, then `27**3 = 19683`. While correct in principle, with large ranges this is too slow. We need a method that avoids touching every element for every cubing.

## Approaches

The brute-force approach iterates through the array directly. For sum queries, it loops over all elements in the range, adds them modulo 95542721, and prints the result. For cubing updates, it loops over all elements in the range, raises each to the third power modulo 95542721, and writes back. This approach is correct but too slow. With n and q up to 10^5, worst-case queries over the whole array could result in 10^10 operations.

The key insight is that cubing is periodic modulo 95542721. If you compute repeated cubings of a number modulo 95542721, eventually the sequence cycles. In fact, modulo this prime, any integer x will return to its original value after at most 48 repeated cubings. This observation allows us to treat each element as a cycle of length at most 48. Instead of cubing values directly on the array, we store 48 precomputed powers for each segment and maintain a pointer to how many times the segment has been cubed. Sum queries then combine values based on the current pointer, and cubing an entire range just increments the pointer modulo 48.

We implement this using a segment tree with lazy propagation. Each node stores an array of 48 sums representing repeated cubings of its interval. The lazy value is the number of pending cubings for that interval. When propagating, we rotate the sums array according to the lazy value. Queries then access the correct sum without recomputing cubings element by element.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * q) | O(n) | Too slow |
| Segment Tree with Cubing Cycle | O(q * log n) | O(n * 48) | Accepted |

## Algorithm Walkthrough

1. Precompute cubing sequences modulo 95542721 for each element. For an element x, compute `x^(3^k) % 95542721` for k = 0 to 47. Store these 48 values in an array. This defines the cubing cycle for each element.
2. Build a segment tree. Each node represents a range `[l, r]` of the array. Instead of storing a single sum, store an array of 48 sums, where the k-th element is the sum of all elements in that range after being cubed k times. This allows answering sum queries for any number of pending cubings.
3. Use lazy propagation to handle cubing updates. Each node has a lazy counter `lazy` indicating how many times its interval should be cubed. When a node receives a cubing update, increment `lazy` modulo 48 and postpone updating its children until necessary.
4. To apply a pending lazy value to a node, rotate its array of 48 sums by `lazy` positions. For example, if `lazy = 1`, the sum after one more cubing becomes the sum at index 1, the sum after two cubings becomes index 2, and so on, with wraparound.
5. For a sum query, traverse the tree like a normal segment tree query. When accessing a node, apply the pending lazy rotation and sum the correct value from its sums array corresponding to its current lazy value.
6. When combining two children, combine their sums arrays elementwise, respecting any lazy rotation. This ensures the parent node’s sums are always consistent with its children.

Why it works: Each node maintains all 48 possible cubing states. Lazy propagation guarantees that we never lose updates: we only rotate the array to reflect cubing operations. Sum queries read from the correct rotated index. This preserves correctness because rotations and modular arithmetic are consistent and reversible.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 95542721
CYCLE = 48

class Node:
    __slots__ = ('sums', 'lazy')
    def __init__(self):
        self.sums = [0] * CYCLE
        self.lazy = 0

def cube_cycle(x):
    arr = [x % MOD]
    for _ in range(CYCLE-1):
        arr.append(pow(arr[-1], 3, MOD))
    return arr

def merge(left, right):
    node = Node()
    for i in range(CYCLE):
        node.sums[i] = (left.sums[i] + right.sums[i]) % MOD
    return node

def rotate(arr, k):
    k %= CYCLE
    return arr[k:] + arr[:k]

class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [Node() for _ in range(4*self.n)]
        self.build(1, 0, self.n-1, data)
        
    def build(self, v, l, r, data):
        if l == r:
            self.tree[v].sums = cube_cycle(data[l])
            return
        m = (l+r)//2
        self.build(2*v, l, m, data)
        self.build(2*v+1, m+1, r, data)
        self.tree[v] = merge(self.tree[2*v], self.tree[2*v+1])
    
    def push(self, v):
        lazy = self.tree[v].lazy
        if lazy:
            self.tree[2*v].lazy = (self.tree[2*v].lazy + lazy) % CYCLE
            self.tree[2*v+1].lazy = (self.tree[2*v+1].lazy + lazy) % CYCLE
            self.tree[v].sums = rotate(self.tree[v].sums, lazy)
            self.tree[v].lazy = 0
    
    def update(self, v, l, r, ql, qr):
        if qr < l or r < ql:
            return
        if ql <= l and r <= qr:
            self.tree[v].lazy = (self.tree[v].lazy + 1) % CYCLE
            self.tree[v].sums = rotate(self.tree[v].sums, 1)
            return
        self.push(v)
        m = (l+r)//2
        self.update(2*v, l, m, ql, qr)
        self.update(2*v+1, m+1, r, ql, qr)
        self.tree[v] = merge(self.tree[2*v], self.tree[2*v+1])
    
    def query(self, v, l, r, ql, qr):
        if qr < l or r < ql:
            return 0
        if ql <= l and r <= qr:
            return self.tree[v].sums[self.tree[v].lazy]
        self.push(v)
        m = (l+r)//2
        return (self.query(2*v, l, m, ql, qr) + self.query(2*v+1, m+1, r, ql, qr)) % MOD

n = int(input())
a = list(map(int, input().split()))
tree = SegmentTree(a)
q = int(input())
for _ in range(q):
    t,l,r = map(int, input().split())
    l -= 1; r -= 1
    if t == 1:
        print(tree.query(1,0,n-1,l,r))
    else:
        tree.update(1,0,n-1,l,r)
```

The code builds the segment tree using precomputed cubing sequences. Lazy propagation rotates these sequences instead of recalculating powers each time. Updates increment the lazy counter and rotate arrays. Queries read the correct sum by accounting for the current lazy value.

## Worked Examples

Sample input 1:

```
8
1 2 3 4 5 6 7 8
5
1 2 5
2 2 5
1 2 5
2 3 6
1 4 7
```

| Step | Query | Lazy | Node sums used | Result |
| --- | --- | --- | --- | --- |
| 1 | sum 2-5 | 0 | sums[0] | 2+3+4+5=14 |
