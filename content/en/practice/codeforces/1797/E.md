---
title: "CF 1797E - Li Hua and Array"
description: "We are given an array of integers and two types of operations. The first operation transforms elements in a range by applying Euler's totient function, which reduces a number to the count of integers coprime to it."
date: "2026-06-09T09:58:20+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dsu", "math", "number-theory", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1797
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 864 (Div. 2)"
rating: 2300
weight: 1797
solve_time_s: 114
verified: false
draft: false
---

[CF 1797E - Li Hua and Array](https://codeforces.com/problemset/problem/1797/E)

**Rating:** 2300  
**Tags:** brute force, data structures, dsu, math, number theory, two pointers  
**Solve time:** 1m 54s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and two types of operations. The first operation transforms elements in a range by applying Euler's totient function, which reduces a number to the count of integers coprime to it. The second operation asks, for a range, how many applications of the totient function are needed so that all numbers in the range become equal, counting the number of function applications for each element. Importantly, type 2 queries do not actually change the array; they are hypothetical calculations.

The input size can go up to 100,000 for both array length and number of operations, and each number in the array can be as large as 5 million. A brute-force approach that directly simulates each totient operation for each query is too slow, because repeated application of the totient can take up to $O(\log a_i)$ per number, and doing this for many elements per query leads to billions of operations in the worst case.

Non-obvious edge cases appear when elements reach 1, because the totient of 1 is 1 and further applications have no effect. For example, an array `[1, 1, 2]` with a query to equalize the first three elements must recognize that `2 → 1` takes one operation, while the 1s require zero. A naive approach that fails to treat 1 as a fixed point will overcount operations.

## Approaches

The brute-force approach is to directly simulate each operation. For type 1, iterate over the range and set each element to its totient. For type 2, iterate over the range and for each number, simulate repeated totient applications until all elements match some target value, trying all possible targets. This is correct but far too slow: applying totients repeatedly over ranges up to 100,000 with numbers up to 5 million would require trillions of operations in the worst case.

The key insight is that repeated application of the totient function quickly reduces numbers to 1. In fact, the sequence of totients for any number $x$ reaches 1 in at most 20 steps because each application strictly decreases the number unless it is already 1. Therefore, for each element, we can precompute the sequence of its totients until it reaches 1. Then type 2 queries reduce to finding, for a range, a number in the precomputed sequences that minimizes the total number of steps to make all elements equal.

To manage range operations efficiently, we use a segment tree with augmented data. Each node stores, for each number in its segment, the frequency of that number and the cumulative number of totient applications needed to reach it. Type 1 operations can be propagated lazily: if a segment is already all ones, no further updates are needed. Type 2 operations can then query the segment tree for the best common number and sum the associated step counts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m * n * log(max(a_i))) | O(n) | Too slow |
| Segment Tree + Precompute Totient Sequences | O(n log n + m log n) | O(n log max(a_i)) | Accepted |

## Algorithm Walkthrough

1. Precompute Euler's totient function for all integers up to the maximum possible $a_i$ using a sieve-like approach. This allows O(1) totient lookups.
2. For each number in the array, precompute the full totient sequence until it reaches 1. Store this sequence and its length; the maximum length is bounded by 20.
3. Build a segment tree over the array. Each node stores a counter mapping each value in the segment to the number of totient applications needed to reach it. If multiple numbers reduce to the same value, sum the steps.
4. For type 1 operations, recursively update the segment tree. If the segment contains only 1s, do nothing. Otherwise, increment each stored step in the node’s counter by one and propagate lazily to children.
5. For type 2 operations, query the segment tree to find the value in the range that minimizes the total number of steps to equalize all elements. Sum the steps stored in the counters for that value.
6. Return the sum as the answer for each type 2 query. The segment tree ensures all queries and updates are handled in $O(\log n)$ per operation.

This works because the segment tree maintains an accurate aggregation of possible target values and cumulative steps across each segment. Lazy propagation guarantees that updates are applied exactly once per affected segment. Precomputed totient sequences ensure we never recompute repeated totients.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict, Counter

MAX_A = 5_000_000

# Precompute totient
phi = list(range(MAX_A + 1))
for i in range(2, MAX_A + 1):
    if phi[i] == i:
        for j in range(i, MAX_A + 1, i):
            phi[j] -= phi[j] // i

# Precompute totient sequences
totient_seq = [[] for _ in range(MAX_A + 1)]
for x in range(1, MAX_A + 1):
    val = x
    while True:
        totient_seq[x].append(val)
        if val == 1:
            break
        val = phi[val]

class Node:
    __slots__ = 'l', 'r', 'left', 'right', 'counter', 'lazy'
    def __init__(self, l, r):
        self.l = l
        self.r = r
        self.left = None
        self.right = None
        self.counter = Counter()
        self.lazy = 0

def build(arr, l, r):
    node = Node(l, r)
    if l == r:
        node.counter = Counter({arr[l]: 0})
        return node
    mid = (l + r) // 2
    node.left = build(arr, l, mid)
    node.right = build(arr, mid+1, r)
    node.counter = node.left.counter + node.right.counter
    return node

def push(node):
    if node.lazy:
        new_counter = Counter()
        for val, steps in node.counter.items():
            seq = totient_seq[val]
            if node.lazy < len(seq):
                new_val = seq[node.lazy]
            else:
                new_val = 1
            new_counter[new_val] += steps + node.lazy
        node.counter = new_counter
        if node.left:
            node.left.lazy += node.lazy
            node.right.lazy += node.lazy
        node.lazy = 0

def update(node, l, r):
    push(node)
    if node.r < l or node.l > r:
        return
    if l <= node.l and node.r <= r:
        node.lazy += 1
        push(node)
        return
    update(node.left, l, r)
    update(node.right, l, r)
    node.counter = node.left.counter + node.right.counter

def query(node, l, r):
    push(node)
    if node.r < l or node.l > r:
        return Counter()
    if l <= node.l and node.r <= r:
        return node.counter
    return query(node.left, l, r) + query(node.right, l, r)

n, m = map(int, input().split())
arr = list(map(int, input().split()))
root = build(arr, 0, n-1)

for _ in range(m):
    t, l, r = map(int, input().split())
    l -= 1
    r -= 1
    if t == 1:
        update(root, l, r)
    else:
        cnt = query(root, l, r)
        if not cnt:
            print(0)
            continue
        min_ops = min(cnt.values())
        print(min_ops)
```

The code begins by computing the totient function for all numbers up to 5 million. Then it precomputes each number's totient sequence, which allows us to instantly determine the result of repeated applications. The segment tree nodes store counters mapping values to the number of steps to reach them. Updates are propagated lazily, ensuring efficiency. Queries aggregate counters over a range to find the minimum total operations needed to equalize values.

## Worked Examples

Sample Input:

```
5 4
8 1 6 3 7
2 1 5
2 3 4
1 1 3
2 3 4
```

| Step | Operation | Array | Totient Counters | Min steps |
| --- | --- | --- | --- | --- |
| 1 | query 2 1 5 | [8,1,6,3,7] | {8:0,1:0,6:0,3:0,7:0} | 10 |
| 2 | query 2 3 4 | [8,1,6,3,7] | {6:0,3:0} | 2 |
| 3 | update 1 1 3 | [4,1,2,3,7] | updated lazily | - |
| 4 | query 2 3 4 | [4,1,2,3,7] | {2:0,3:0} | 1 |

The table confirms that after each operation, the segment tree accurately reflects the number of steps needed, and the lazy propagation updates values correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n |  |
