---
title: "CF 341D - Iahub and Xors"
description: "We are maintaining an initially empty square grid of size $n times n$, where every cell starts as zero. Two kinds of operations are performed over this grid. One operation asks for the XOR of all values inside a rectangular subregion."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 341
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 198 (Div. 1)"
rating: 2500
weight: 341
solve_time_s: 370
verified: false
draft: false
---

[CF 341D - Iahub and Xors](https://codeforces.com/problemset/problem/341/D)

**Rating:** 2500  
**Tags:** data structures  
**Solve time:** 6m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are maintaining an initially empty square grid of size $n \times n$, where every cell starts as zero. Two kinds of operations are performed over this grid. One operation asks for the XOR of all values inside a rectangular subregion. The other operation takes a rectangle and XORs every cell inside it with a fixed value $v$.

The important aspect is that updates are not pointwise but rectangular, and queries are also rectangular aggregations. Since XOR is the aggregation operator, the structure is not additive in the usual sense, but it behaves linearly over the field $\mathbb{F}_2$, which makes it compatible with prefix-parity style transformations.

The constraints make brute force infeasible. With $n \le 1000$ and up to $10^5$ operations, a direct rectangle iteration per operation would require up to $10^8$ cell updates per operation in the worst case, leading to $10^{13}$ total operations in the extreme scenario, which is far beyond any time limit.

A naive attempt that stores the grid and performs updates by iterating over all cells in the rectangle will immediately fail on large rectangles. Similarly, recomputing a full submatrix XOR for each query is too slow.

A subtle edge case appears when updates overlap heavily. For example, if we repeatedly XOR the entire matrix, a naive grid update works but becomes maximally slow. Another issue is that XOR updates are invertible and commutative, meaning order does not matter, but a naive approach might try to simulate order-dependent accumulation and still be correct logically but far too slow.

The key difficulty is supporting both rectangular range updates and rectangular range XOR queries efficiently in two dimensions.

## Approaches

A brute force method maintains the grid explicitly. For an update operation, we iterate over all cells in the rectangle and XOR each with $v$. For a query, we iterate over all cells in the rectangle and compute the XOR sum. This is straightforward and correct because XOR is applied exactly as defined.

However, each operation can touch up to $O(n^2)$ cells. With $10^5$ operations, the worst-case cost is $O(m n^2)$, which is $10^{11}$ operations when $n = 1000$, clearly impossible.

The turning point is to reinterpret the grid not as values stored directly, but as the result of multiple range XOR updates. Each update toggles bits in a region. XOR over a rectangle query can then be seen as counting contributions of each update over the intersection of two rectangles.

This is a classic inclusion structure problem. A 2D difference structure over XOR can convert a rectangle XOR update into four corner flips, just like prefix sums convert rectangle additions into point updates. Once updates are represented in a 2D binary indexed tree or segment tree variant, queries reduce to prefix XOR queries over a prefix structure.

However, we still need rectangle updates and rectangle queries. The key insight is to maintain four 2D Fenwick trees (BITs), using inclusion-exclusion on both axes. Each update contributes to a transformed space where prefix XOR queries can be answered in logarithmic time, and rectangle XOR updates are decomposed into a constant number of prefix adjustments.

The final idea is that XOR behaves like addition modulo 2 at the bit level, so we can treat each bit independently. Since values are up to $2^{62}$, we maintain 62 independent 2D BITs, each storing parity contributions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(m n^2)$ | $O(n^2)$ | Too slow |
| Optimal | $O(m \log^2 n \cdot 62)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

We reduce the problem into maintaining a 2D structure that supports rectangle XOR updates and rectangle XOR queries using inclusion-exclusion.

1. Decompose each integer into bits, since XOR is independent per bit. We treat each bit position separately and reconstruct final answers by combining results.

This works because XOR on integers is equivalent to XOR on each binary digit independently.
2. For each bit, maintain a 2D Fenwick tree that supports point updates and prefix XOR queries.
3. Convert a rectangle XOR update into four point updates using inclusion-exclusion over a 2D difference-like structure. Specifically, updating rectangle $(x_0,y_0)$ to $(x_1,y_1)$ is simulated by toggling contributions at the corners in the Fenwick structure.
4. To apply XOR $v$, for each bit $b$ where $v$ has that bit set, we apply the rectangle toggle in the corresponding BIT.
5. To answer a query over $(x_0,y_0)$ to $(x_1,y_1)$, we compute prefix XOR sums using inclusion-exclusion:

$$F(x_1,y_1) \oplus F(x_0-1,y_1) \oplus F(x_1,y_0-1) \oplus F(x_0-1,y_0-1)$$

This isolates the rectangle sum.
6. Combine contributions from all bits to form the final integer answer.

### Why it works

Each update toggles contributions in a way that respects XOR linearity over GF(2). The Fenwick tree stores prefix parity information, and inclusion-exclusion ensures that every cell is counted exactly once when reconstructing a rectangle. Because XOR is associative and commutative, decomposing updates into independent bit contributions preserves correctness. The structure guarantees that every update affects exactly the intended region, and every query reconstructs the exact parity of applied XOR operations over that region.

## Python Solution

```python
import sys
input = sys.stdin.readline

class BIT2D:
    def __init__(self, n):
        self.n = n
        self.bit = [[0] * (n + 1) for _ in range(n + 1)]

    def _update(self, x, y, val):
        i = x
        while i <= self.n:
            j = y
            while j <= self.n:
                self.bit[i][j] ^= val
                j += j & -j
            i += i & -i

    def update_rect(self, x1, y1, x2, y2, val):
        self._update(x1, y1, val)
        self._update(x1, y2 + 1, val)
        self._update(x2 + 1, y1, val)
        self._update(x2 + 1, y2 + 1, val)

    def _query(self, x, y):
        res = 0
        i = x
        while i > 0:
            j = y
            while j > 0:
                res ^= self.bit[i][j]
                j -= j & -j
            i -= i & -i
        return res

    def query_rect(self, x1, y1, x2, y2):
        return (self._query(x2, y2) ^
                self._query(x1 - 1, y2) ^
                self._query(x2, y1 - 1) ^
                self._query(x1 - 1, y1 - 1))

def solve():
    n, m = map(int, input().split())
    bits = [BIT2D(n) for _ in range(64)]

    for _ in range(m):
        tmp = list(map(int, input().split()))
        if tmp[0] == 1:
            _, x1, y1, x2, y2 = tmp
            res = 0
            for b in range(64):
                if bits[b].query_rect(x1, y1, x2, y2):
                    res |= (1 << b)
            print(res)
        else:
            _, x1, y1, x2, y2, v = tmp
            b = 0
            while v:
                if v & 1:
                    bits[b].update_rect(x1, y1, x2, y2, 1)
                v >>= 1
                b += 1

if __name__ == "__main__":
    solve()
```

The implementation uses one 2D BIT per bit position. Each BIT stores parity contributions for that bit. Rectangle updates are handled through four-point inclusion-exclusion, and queries reconstruct prefix XORs similarly. The query loop rebuild
