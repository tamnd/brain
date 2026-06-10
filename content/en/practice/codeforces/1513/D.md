---
title: "CF 1513D - GCD and MST"
description: "We are asked to compute the minimum spanning tree (MST) of a weighted graph constructed from an array of positive integers."
date: "2026-06-10T18:46:27+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dsu", "graphs", "greedy", "number-theory", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1513
codeforces_index: "D"
codeforces_contest_name: "Divide by Zero 2021 and Codeforces Round 714 (Div. 2)"
rating: 2000
weight: 1513
solve_time_s: 144
verified: true
draft: false
---

[CF 1513D - GCD and MST](https://codeforces.com/problemset/problem/1513/D)

**Rating:** 2000  
**Tags:** constructive algorithms, dsu, graphs, greedy, number theory, sortings  
**Solve time:** 2m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to compute the minimum spanning tree (MST) of a weighted graph constructed from an array of positive integers. Each array element corresponds to a vertex, and edges exist either between adjacent elements with a fixed weight `p` or between any pair of vertices `(i, j)` if the greatest common divisor (GCD) of all elements from `a[i]` to `a[j]` equals the minimum in that subarray. The weight of such an edge is the minimum value of the subarray. The goal is not to explicitly construct all edges, but to compute the MST weight efficiently.

The constraints show that `n` can be up to 2·10^5 per test case, and the sum of `n` over all test cases is also 2·10^5. This means any approach with O(n^2) time per test case is immediately infeasible because it would require roughly 4·10^10 operations. We need an algorithm close to linear or linearithmic in `n`.

A subtle edge case occurs when all array elements are equal or smaller than `p`. For example, if `n = 3`, `p = 5`, and `a = [3, 3, 3]`, naive adjacency processing might try to create edges between non-adjacent vertices unnecessarily or miss cheaper edges. Similarly, if the array has a single small element surrounded by larger ones, greedy connections must correctly identify that connecting through this small element can reduce the MST cost below `p` per edge.

## Approaches

The brute-force approach is to literally generate all candidate edges. For every pair `(i, j)` you compute the GCD of `a[i..j]` and the minimum in that range. If they are equal, add an edge with weight `min(a[i..j])`. Adjacent vertices always get an edge of weight `p`. After generating edges, run Kruskal's or Prim's algorithm to compute the MST. This is correct because it follows the problem rules exactly, but it is O(n^2 log n) in the worst case for edge generation and sorting, which is far too slow for `n = 2·10^5`.

The key insight is that we do not need all edges. Any edge with weight greater than `p` is never cheaper than using the adjacent `p` edges in an MST. Therefore, we can restrict attention to edges where `min(a[i..j]) < p`. For those, consider each element `a[k]` as a candidate to connect contiguous ranges where it is the minimum and divides all elements in that range. This transforms the problem into a greedy construction: start from the smallest elements, and extend left and right while the GCD remains divisible by that element. These ranges give edges we can add to the MST using a disjoint-set union (DSU). This allows us to avoid explicit GCD computation for all pairs and reduces the problem to roughly sorting the array and performing union-find operations, giving O(n log n) complexity per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 log n) | O(n^2) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `n`, `p`, and the array `a`.
2. Initialize a disjoint-set union (DSU) structure for the `n` elements. This will track which vertices are already connected in the MST.
3. Create a list of indices `idx` sorted by the corresponding array values `a[i]`. This allows us to process potential minimums in increasing order.
4. Initialize `mst_weight = 0` and `edges_used = 0`. These will accumulate the MST total weight and track how many edges we have added.
5. Iterate through the sorted indices. For each `i`:

- Skip if `a[i] >= p` because such edges are never cheaper than the fixed `p` edges.
- Try extending to the left: while the previous element exists, is not yet connected in DSU, and is divisible by `a[i]`, union them and add `a[i]` to `mst_weight`.
- Similarly, extend to the right, unioning adjacent divisible elements.
- Each union corresponds to adding an MST edge, so increment `edges_used`.
6. After processing all small elements, there may be remaining unconnected pairs. For every adjacent pair `(i, i+1)` not in the same DSU component, union them and add `p` to `mst_weight`.
7. Print `mst_weight` for the test case.

Why it works: By processing array elements from smallest to largest, we ensure that whenever we create an MST edge, it is the cheapest possible for that component. Divisibility guarantees that the GCD condition is satisfied for contiguous ranges. Remaining adjacent edges with weight `p` handle cases where no smaller element can connect two vertices, ensuring the MST is complete.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
    
    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    
    def union(self, x, y):
        x_root, y_root = self.find(x), self.find(y)
        if x_root == y_root:
            return False
        self.parent[y_root] = x_root
        return True

def solve():
    t = int(input())
    for _ in range(t):
        n, p = map(int, input().split())
        a = list(map(int, input().split()))
        dsu = DSU(n)
        idx = sorted(range(n), key=lambda i: a[i])
        mst_weight = 0
        edges_used = 0
        
        for i in idx:
            if a[i] >= p:
                break
            j = i - 1
            while j >= 0 and a[j] % a[i] == 0 and dsu.union(i, j):
                mst_weight += a[i]
                edges_used += 1
                j -= 1
            j = i + 1
            while j < n and a[j] % a[i] == 0 and dsu.union(i, j):
                mst_weight += a[i]
                edges_used += 1
                j += 1

        for i in range(n - 1):
            if dsu.union(i, i + 1):
                mst_weight += p
                edges_used += 1

        print(mst_weight)

if __name__ == "__main__":
    solve()
```

The code first defines a DSU with path compression for efficient union and find. Sorting the indices ensures we process the cheapest potential MST edges first. The left-right extensions union contiguous divisible elements, which corresponds to edges satisfying the GCD condition. Finally, remaining adjacent edges of weight `p` guarantee a connected MST.

## Worked Examples

Sample Input 1:

```
n = 2, p = 5
a = [10, 10]
```

| Step | Action | DSU parent | MST weight | Edges used |
| --- | --- | --- | --- | --- |
| 1 | Sort indices by value | [0, 1] | 0 | 0 |
| 2 | i=0, a[i]=10 >= p, skip | [0,1] | 0 | 0 |
| 3 | Connect remaining adjacent pair (0,1) with p=5 | [0,0] | 5 | 1 |

Output is `5`.

Sample Input 2:

```
n = 2, p = 5
a = [3, 3]
```

| Step | Action | DSU parent | MST weight | Edges used |
| --- | --- | --- | --- | --- |
| 1 | Sort indices by value | [0,1] | 0 | 0 |
| 2 | i=0, a[i]=3 < p | union left/right not needed | [0,0] | 3 |
| 3 | No remaining edges needed | - | - | - |

Output is `3`.

These traces show that small elements are used greedily for GCD-based connections, and remaining adjacency edges handle the rest.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting indices takes O(n log n), union-find with path compression is almost linear. |
| Space | O(n) | DSU stores parent array, and index array uses O(n) |

Given the constraint sum of n ≤ 2·10^5, this algorithm runs efficiently within 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("4\n2 5\n10 10\n2 5\n3 3\n4 5\n5 2 4 9\n8 8\n5 3 3 6 10 100 9 15\n") == "5\n3\n12\n46"

# Custom cases
assert run("1\n2 1\n1 1\n") == "1", "minimum values, p=1"
assert run("1\n3 10\n5 5
```
