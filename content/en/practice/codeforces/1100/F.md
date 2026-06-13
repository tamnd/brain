---
title: "CF 1100F - Ivan and Burgers"
description: "We are given an array of values on a line, where each position represents a burger shop and the value at that position is the cost of the most expensive burger available there."
date: "2026-06-13T07:10:55+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1100
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 532 (Div. 2)"
rating: 2500
weight: 1100
solve_time_s: 240
verified: true
draft: false
---

[CF 1100F - Ivan and Burgers](https://codeforces.com/problemset/problem/1100/F)

**Rating:** 2500  
**Tags:** data structures, divide and conquer, greedy, math  
**Solve time:** 4m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of values on a line, where each position represents a burger shop and the value at that position is the cost of the most expensive burger available there. For each query, we are given a segment of this array and we are allowed to choose any subset of indices inside that segment. The effect of choosing a subset is that we start with a very large initial number and repeatedly apply XOR with the chosen values. The quantity we care about is how much the value decreases from the initial state, which is equivalent to maximizing the XOR result of the chosen subset.

A key simplification comes from the initial value being all bits set. If we start with a number of the form where every relevant bit is 1, then XORing with a value effectively flips bits. The “money spent” depends only on the resulting value after all XOR operations, so the task reduces to maximizing the XOR of some subset of the given segment.

Each query is therefore asking: given a subarray, what is the maximum XOR value we can obtain by selecting any subset of elements inside it.

The constraints are large, with up to 500,000 elements and 500,000 queries. This immediately rules out recomputing anything per query in linear time over the segment, since that would lead to roughly $2.5 \times 10^{11}$ operations in the worst case. Even $O(n \log n)$ per query is too slow. We need a structure that supports fast range queries over XOR subsets.

A naive approach would build all subsets for a range or recompute a greedy XOR basis per query. This fails because subset enumeration is exponential, and even maintaining a running basis per query from scratch is too slow when repeated many times.

A subtle edge case arises when all values in a segment are zero. The correct answer is zero, and any approach that assumes at least one non-zero basis vector without proper normalization might incorrectly return a non-zero value or crash when querying empty bases. Another edge case is when values are repeated; duplicates must not expand the basis incorrectly.

## Approaches

The brute-force idea is straightforward. For each query, we collect all values in the segment and try every subset, computing XOR and tracking the maximum. This is correct because it directly evaluates the definition of the problem. However, each segment of length $k$ has $2^k$ subsets, which becomes impossible even for $k = 30$, let alone $k = 500000$.

We need to recognize that XOR subset optimization is not about subsets directly, but about the linear structure they form over GF(2). Any set of numbers generates a vector space under XOR, and any subset XOR corresponds to a linear combination of these vectors. The maximum XOR obtainable is the maximum value achievable from the linear basis of the set.

This transforms the problem into maintaining a linear basis over segments of the array. The key observation is that a segment’s full behavior is fully described by its basis, which has size at most 20 because values are up to $10^6$, hence at most 20 relevant bits.

We then need a data structure that can return the combined basis of any segment efficiently. A segment tree works naturally: each node stores a basis for its interval, and merging two nodes means merging two bases into one reduced basis.

Once we obtain the basis for a query segment, we compute the maximum XOR by greedily trying to improve the result from the highest bit downward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Subsets | $O(2^n)$ per query | $O(1)$ | Too slow |
| Segment Tree with XOR Basis | $O((n + q)\log n \cdot B^2)$ | $O(n \log n \cdot B)$ | Accepted |

Here $B$ is the number of bits, around 20.

## Algorithm Walkthrough

We build a segment tree where each node stores a linear basis of all values in its segment.

1. Initialize each leaf node with a basis containing only the single value at that position. This basis represents all XORs achievable from that single element, which are just zero and the element itself.
2. Define a merge operation between two bases. We take all vectors from the second basis and insert them into the first basis using standard linear basis insertion. Each insertion tries to eliminate the highest set bit using existing basis vectors, ensuring the structure remains independent.
3. Build the segment tree bottom-up by merging children nodes. Each internal node stores the merged basis of its left and right child segments. This ensures that every segment is fully represented by its basis.
4. For each query $[l, r]$, we traverse the segment tree and collect bases of all segments that fully cover the query range. These are merged into a single temporary basis.
5. Once we have the final basis for a query, we compute the maximum XOR value. We start from zero and iterate bits from highest to lowest, attempting to improve the value by XORing with basis vectors that increase it.
6. Output this maximum value for each query.

The reason merging works is that XOR combinations over disjoint segments are independent. Any subset of the full range can be split into subsets of left and right parts, and their XOR combines linearly. Thus merging bases preserves all achievable XORs.

### Why it works

At every segment tree node, we maintain a basis that spans exactly the set of XOR-representable values for that interval. The merge operation preserves the span because XOR combinations of two sets correspond to the union of their vector spaces. Since every query decomposes into disjoint segments whose union forms the full range, merging their bases produces a basis that spans all possible subset XORs for the query interval. The greedy extraction step then finds the maximum representable value in that space, which is optimal because linear bases guarantee that any reachable XOR can be constructed through a deterministic bitwise construction.

## Python Solution

```python
import sys
input = sys.stdin.readline

B = 20

class Basis:
    __slots__ = ("b",)
    def __init__(self):
        self.b = [0] * B

    def insert(self, x):
        for i in reversed(range(B)):
            if (x >> i) & 1:
                if self.b[i]:
                    x ^= self.b[i]
                else:
                    self.b[i] = x
                    return

    def merge(self, other):
        for x in other.b:
            if x:
                self.insert(x)

    def max_xor(self):
        res = 0
        for i in reversed(range(B)):
            res = max(res, res ^ self.b[i])
        return res

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.t = [Basis() for _ in range(4 * self.n)]
        self.arr = arr
        self.build(1, 0, self.n - 1)

    def build(self, v, l, r):
        if l == r:
            self.t[v].insert(self.arr[l])
        else:
            m = (l + r) // 2
            self.build(v * 2, l, m)
            self.build(v * 2 + 1, m + 1, r)
            self.t[v].merge(self.t[v * 2])
            self.t[v].merge(self.t[v * 2 + 1])

    def query(self, v, l, r, ql, qr, res):
        if ql <= l and r <= qr:
            res.merge(self.t[v])
            return
        m = (l + r) // 2
        if ql <= m:
            self.query(v * 2, l, m, ql, qr, res)
        if qr > m:
            self.query(v * 2 + 1, m + 1, r, ql, qr, res)

def main():
    n = int(input())
    arr = list(map(int, input().split()))
    st = SegTree(arr)

    q = int(input())
    out = []

    for _ in range(q):
        l, r = map(int, input().split())
        res = Basis()
        st.query(1, 0, n - 1, l - 1, r - 1, res)
        out.append(str(res.max_xor()))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The segment tree is built once over the array, and each node stores a compressed representation of all XOR contributions in its interval. The query function collects only relevant nodes and merges their bases into a temporary structure. The final step computes the best achievable XOR.

The subtle point in implementation is that merging bases must preserve independence; inserting each element of one basis into another is necessary rather than naive concatenation. Another detail is ensuring the basis uses a fixed bit limit, since values are bounded by $10^6$.

## Worked Examples

### Example 1

Input:

```
n = 4
arr = [7, 2, 3, 4]
query = [1, 4]
```

| Step | Current Basis | Action |
| --- | --- | --- |
| 1 | {} | insert 7 |
| 2 | {7} | insert 2 |
| 3 | {7, 2} | insert 3 |
| 4 | {7, 2, 3} | insert 4 |

After building the basis, we compute maximum XOR by greedy selection. The best achievable XOR is 7.

This shows that even though all elements are available, the optimal subset is just picking a single strong contributor.

### Example 2

Input:

```
n = 3
arr = [12, 14, 23]
query = [1, 3]
```

| Step | Basis | Explanation |
| --- | --- | --- |
| Start | {} | empty |
| Insert 12 | {12} | add first vector |
| Insert 14 | {12, 14} | independent |
| Insert 23 | {12, 14, 23} | full basis |

Now compute maximum XOR. The greedy construction yields 27 from 12 XOR 23.

This confirms that optimal subsets may involve multiple elements even when individual values are not maximal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n + q)\log n \cdot B^2)$ | each merge inserts up to B vectors, each insertion costs B |
| Space | $O(n \log n \cdot B)$ | each segment tree node stores a basis of size B |

The complexity is sufficient because $B \approx 20$, making all operations effectively small constants. Even with 500,000 queries, the segment tree operations remain fast enough within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    # assume solution is defined above in same file
    main()

    return output.getvalue().strip()

# provided sample
assert run("""4
7 2 3 4
3
1 4
2 3
1 3
""") == """7
3
7"""

# single element
assert run("""1
5
1
1 1
""") == "5"

# all zeros
assert run("""3
0 0 0
2
1 3
2 2
""") == "0\n0"

# all equal
assert run("""4
8 8 8 8
1
1 4
""") == "8"

# increasing
assert run("""5
1 2 4 8 16
1
1 5
""") == "31"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 5 | leaf correctness |
| all zeros | 0, 0 | empty basis handling |
| all equal | 8 | duplicate handling |
| powers of two | 31 | full basis construction |

## Edge Cases

For a segment containing only zeros, every insertion into the basis leaves it empty, so the final greedy XOR remains zero. The segment tree correctly stores empty bases for such nodes, and merging empty bases has no effect, preserving correctness.

For repeated values, inserting the same number twice does not change the basis because it gets eliminated by the existing vector. This ensures duplicates do not artificially inflate the representable space.

For single-element queries, the leaf node already contains the correct basis, so no merging is required. The query simply returns that node’s basis, and the greedy step returns the element itself, which matches the correct answer.
