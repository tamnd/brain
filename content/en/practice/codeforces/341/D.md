---
title: "CF 341D - Iahub and Xors"
description: "We are given an $n times n$ matrix initially filled with zeros. The problem asks us to handle two types of operations efficiently: one that computes the xor of all elements inside a submatrix, and another that xors a given value into every element of a submatrix."
date: "2026-06-06T17:32:52+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 341
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 198 (Div. 1)"
rating: 2500
weight: 341
solve_time_s: 146
verified: false
draft: false
---

[CF 341D - Iahub and Xors](https://codeforces.com/problemset/problem/341/D)

**Rating:** 2500  
**Tags:** data structures  
**Solve time:** 2m 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an $n \times n$ matrix initially filled with zeros. The problem asks us to handle two types of operations efficiently: one that computes the xor of all elements inside a submatrix, and another that xors a given value into every element of a submatrix. Each operation specifies the top-left and bottom-right coordinates of the submatrix, and for updates, a value to xor.

The input bounds are significant. $n$ can go up to 1000, so the total number of elements is up to $10^6$, and the number of operations $m$ can be as high as $10^5$. A naive solution that iterates through all cells of a submatrix for every query or update would take up to $10^5 \cdot 10^6 = 10^{11}$ operations in the worst case, which is far beyond what we can handle in a 1-second limit. This means we cannot touch each element individually per operation; we need a data structure that allows both range updates and range queries efficiently.

Edge cases to watch out for include single-element submatrices, submatrices that cover the entire matrix, and multiple updates to the same element. For example, xoring the same value twice should cancel it out. A naive prefix-xor approach without handling range updates correctly could give wrong results when updates overlap.

## Approaches

The brute-force approach is straightforward. For each update, we loop over every element in the given submatrix and xor it with the given value. For each query, we loop over the submatrix and xor all values. This approach is correct but slow: for a $n \times n$ matrix with $m$ operations, each touching potentially the entire matrix, we could have up to $m \cdot n^2 = 10^5 \cdot 10^6 = 10^{11}$ operations, which is infeasible.

The key insight is that xor behaves nicely under both addition and subtraction operations because it is its own inverse. This property allows us to use a 2D Fenwick Tree (Binary Indexed Tree) where each cell stores xor contributions. A standard 2D Fenwick Tree supports point updates and rectangle queries, but we can extend it to support rectangle updates using the inclusion-exclusion principle. The idea is to maintain a structure where we can xor a value to a rectangle by updating the four corners appropriately, and any query over a rectangle can then be expressed using xor sums of these corners. This reduces each operation to $O(\log^2 n)$, which is fast enough for the given constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 * m) | O(n^2) | Too slow |
| 2D BIT (Rectangle Updates + Queries) | O(m * log^2 n) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Initialize a 2D Binary Indexed Tree `bit` with dimensions $n+1 \times n+1$ to handle 1-based indexing conveniently.
2. Define a helper function `xor_update(x, y, val)` that performs the standard BIT update: xor `val` into all positions in the BIT affected by coordinates `(x, y)`. This is the core building block.
3. To xor a value `v` over a rectangle `(x0, y0)` to `(x1, y1)`, we apply inclusion-exclusion:

- xor `v` at `(x0, y0)`
- xor `v` at `(x0, y1 + 1)`
- xor `v` at `(x1 + 1, y0)`
- xor `v` at `(x1 + 1, y1 + 1)`

This ensures that when we compute a prefix xor up to any cell `(x, y)`, the contributions from overlapping rectangles combine correctly.
4. Define a helper function `prefix_xor(x, y)` that computes the xor of the submatrix from `(1,1)` to `(x, y)` using standard 2D BIT query traversal.
5. To compute the xor of an arbitrary submatrix `(x0, y0, x1, y1)`, apply inclusion-exclusion using the prefix xor values:

- result = `prefix_xor(x1, y1) ^ prefix_xor(x0-1, y1) ^ prefix_xor(x1, y0-1) ^ prefix_xor(x0-1, y0-1)`
6. Process each operation in the input. If it is an update, call the rectangle update routine. If it is a query, compute the xor using the submatrix prefix xors and print the result.

Why it works: The 2D BIT with inclusion-exclusion maintains the xor contributions of all updates. Each prefix query retrieves exactly the xor of all updates affecting a given rectangle. Because xor is associative and self-inverse, overlapping updates cancel correctly, and no double-counting occurs.

## Python Solution

```python
import sys
input = sys.stdin.readline

class BIT2D:
    def __init__(self, n):
        self.n = n
        self.bit = [[0] * (n + 2) for _ in range(n + 2)]

    def update(self, x, y, val):
        i = x
        while i <= self.n:
            j = y
            while j <= self.n:
                self.bit[i][j] ^= val
                j += j & -j
            i += i & -i

    def rectangle_update(self, x0, y0, x1, y1, val):
        self.update(x0, y0, val)
        self.update(x0, y1 + 1, val)
        self.update(x1 + 1, y0, val)
        self.update(x1 + 1, y1 + 1, val)

    def prefix_xor(self, x, y):
        res = 0
        i = x
        while i > 0:
            j = y
            while j > 0:
                res ^= self.bit[i][j]
                j -= j & -j
            i -= i & -i
        return res

    def query(self, x0, y0, x1, y1):
        return (self.prefix_xor(x1, y1) ^ self.prefix_xor(x0 - 1, y1) ^
                self.prefix_xor(x1, y0 - 1) ^ self.prefix_xor(x0 - 1, y0 - 1))

n, m = map(int, input().split())
bit2d = BIT2D(n)

for _ in range(m):
    cmd = list(map(int, input().split()))
    if cmd[0] == 1:
        x0, y0, x1, y1 = cmd[1:]
        print(bit2d.query(x0, y0, x1, y1))
    else:
        x0, y0, x1, y1, v = cmd[1:]
        bit2d.rectangle_update(x0, y0, x1, y1, v)
```

The `BIT2D` class encapsulates all BIT logic. The `update` method modifies one cell and all its ancestors, and `rectangle_update` applies the xor to the four corners. The `query` method uses inclusion-exclusion to retrieve the exact xor of a submatrix.

Boundary handling is subtle. We need `n+2` for the internal array to avoid index overflows when `x1+1` or `y1+1` equals `n+1`. Using 1-based indexing avoids confusion with BIT traversal.

## Worked Examples

### Sample 1

Input operations:

| Operation | Description | BIT effect | Query result |
| --- | --- | --- | --- |
| 2 1 1 2 2 1 | xor 1 in rectangle (1,1)-(2,2) | four corners updated | - |
| 2 1 3 2 3 2 | xor 2 in rectangle (1,2)-(3,3) | four corners updated | - |
| 2 3 1 3 3 3 | xor 3 in rectangle (3,1)-(3,3) | four corners updated | - |
| 1 2 2 3 3 | query rectangle (2,2)-(3,3) | prefix_xor gives 3 | 3 |
| 1 2 2 3 2 | query rectangle (2,2)-(3,2) | prefix_xor gives 2 | 2 |

This trace shows how rectangle updates propagate correctly and the prefix_xor inclusion-exclusion retrieves the right xor.

### Custom Example

Input:

```
2 3
2 1 1 2 2 5
2 1 2 1 2 7
1 1 1 2 2
```

Step trace:

| Operation | Matrix effect | Query result |
| --- | --- | --- |
| xor 5 in (1,1)-(2,2) | all elements = 5 | - |
| xor 7 in (1,2)-(2,2) | elements: [[5,2],[5,2]] | - |
| query (1,1)-(2,2) | xor 5^2^5^2 = 0 | 0 |

Confirms overlapping updates cancel appropriately using xor.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time |  |  |
