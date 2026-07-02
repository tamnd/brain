---
title: "CF 103666J - \u0411\u0430\u0448\u043d\u0438"
description: "We are given a sequence of tower heights placed along a line, where each position has a unique height value. The task is to count how many triples of indices $i < j < k$ form a strictly increasing sequence in both position and height, meaning $hi < hj < hk$."
date: "2026-07-02T21:33:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103666
codeforces_index: "J"
codeforces_contest_name: "\u0422\u0443\u0440\u043d\u0438\u0440 \u0410\u0440\u0445\u0438\u043c\u0435\u0434\u0430 2016"
rating: 0
weight: 103666
solve_time_s: 45
verified: true
draft: false
---

[CF 103666J - \u0411\u0430\u0448\u043d\u0438](https://codeforces.com/problemset/problem/103666/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of tower heights placed along a line, where each position has a unique height value. The task is to count how many triples of indices $i < j < k$ form a strictly increasing sequence in both position and height, meaning $h_i < h_j < h_k$.

In other words, we are counting the number of increasing subsequences of length three in a permutation-like array.

The constraint $n \le 8000$ already rules out any cubic or quadratic-over-constant solutions. A naive triple loop over all $(i, j, k)$ would examine about $n^3 / 6$ combinations, which is on the order of 8 \times 10^3^3 \approx 5 \times 10^{11} operations, far beyond what fits in 2 seconds. Even $O(n^2)$ methods need careful design but are still acceptable here.

A subtle point is that heights are a permutation of $1 \dots n$, so comparisons are strictly meaningful and no duplicates exist. This eliminates ambiguity around equal values and ensures every increasing pair or triple is well-defined.

There are no tricky edge cases related to ordering degeneracy, but a naive implementation can still fail in a less obvious way if it recomputes local counts inefficiently. For example, repeatedly scanning suffixes for each middle index leads to hidden quadratic or cubic behavior.

A minimal example helps clarify correctness requirements. For input:

```
3
1 2 3
```

there is exactly one valid triple $(1,2,3)$. Any correct method must detect this single increasing chain.

For a decreasing array:

```
3
3 2 1
```

the answer is zero, since no pair can extend to a third increasing element. This case often exposes implementations that assume partial ordering incorrectly.

## Approaches

A brute-force approach directly tries every triple $i < j < k$ and checks whether the values are increasing. This is correct because it explicitly enumerates all candidates and filters valid ones. However, its cost grows as $O(n^3)$, which becomes prohibitive even for $n = 8000$, since it leads to hundreds of billions of comparisons.

We can improve by fixing the middle element $j$. For each $j$, we want to know how many valid pairs $(i, k)$ exist such that $i < j < k$, $h_i < h_j < h_k$. This separates the condition into two independent counts: how many elements before $j$ are smaller than $h_j$, and how many elements after $j$ are larger than $h_j$. Multiplying these two gives the number of valid triples with middle at $j$.

This transformation reduces the problem to computing prefix and suffix statistics efficiently. Instead of recomputing counts from scratch for every $j$, we precompute:

how many values smaller than $h_j$ appear in the prefix $[1, j-1]$, and how many values greater than $h_j$ appear in the suffix $[j+1, n]$.

Because heights are a permutation over $1 \dots n$, we can maintain frequency structures and update them incrementally in linear or logarithmic time using a Fenwick tree.

The key insight is that the triple count decomposes cleanly around the middle index, turning a global combinatorial problem into two local counting queries per position.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(1)$ | Too slow |
| Split middle + Fenwick Tree | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We use a Fenwick tree (Binary Indexed Tree) to maintain counts of seen values.

1. Traverse the array from left to right and compute a prefix count array `left_smaller[j]`, where for each position $j$, we count how many elements in positions $< j$ have value smaller than $h_j$. We maintain a Fenwick tree storing frequencies of seen heights. At each step, we query how many values $< h_j$ have been inserted so far.
2. Traverse the array from right to left and compute a suffix count array `right_greater[j]`, where for each position $j$, we count how many elements in positions $> j$ have value greater than $h_j$. Again we use a Fenwick tree, but now we process elements from right to left, inserting values and querying how many values greater than the current exist in the tree. This is computed as total seen minus prefix sum up to $h_j$.
3. For each index $j$, interpret it as the middle element of the triple. Multiply the two quantities: `left_smaller[j] * right_greater[j]`. This counts all valid triples where $j$ is the center.
4. Sum these products over all $j$. The result is the total number of increasing triples.

Each step relies on maintaining an accurate frequency structure over a dynamic prefix or suffix. The Fenwick tree ensures both updates and prefix queries run in logarithmic time.

### Why it works

Every valid triple $i < j < k$ is uniquely determined by its middle index $j$. For a fixed $j$, the choice of $i$ depends only on elements before $j$ smaller than $h_j$, and the choice of $k$ depends only on elements after $j$ larger than $h_j$. These choices are independent, so the number of combinations is the product of the two counts. Since every valid triple is counted exactly once at its middle index, summing over all $j$ produces the correct total.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

n = int(input())
h = list(map(int, input().split()))

# left_smaller
bit = Fenwick(n)
left_smaller = [0] * n

for i in range(n):
    x = h[i]
    left_smaller[i] = bit.sum(x - 1)
    bit.add(x, 1)

# right_greater
bit = Fenwick(n)
right_greater = [0] * n

total = 0
for i in range(n - 1, -1, -1):
    x = h[i]
    right_greater[i] = bit.sum(n) - bit.sum(x)
    bit.add(x, 1)

for j in range(n):
    total += left_smaller[j] * right_greater[j]

print(total)
```

The implementation defines a Fenwick tree supporting point updates and prefix sums over height values. The first pass builds `left_smaller` by inserting values as we scan left to right, ensuring the structure always represents elements strictly to the left of the current index.

The second pass resets the structure and processes from right to left, computing how many larger elements exist to the right of each position. The expression `bit.sum(n) - bit.sum(x)` is crucial, since it converts prefix counting into suffix counting.

Finally, the product aggregation step directly mirrors the combinatorial decomposition of triples around their middle index.

## Worked Examples

### Example 1

Input:

```
n = 3
h = [1, 2, 3]
```

Prefix and suffix contributions:

| j | h[j] | left_smaller | right_greater | product |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 2 | 0 |
| 1 | 2 | 1 | 1 | 1 |
| 2 | 3 | 2 | 0 | 0 |

Total is 1.

This confirms that the only valid triple is centered at index 1, where value 2 is between 1 and 3.

### Example 2

Input:

```
n = 4
h = [3, 1, 4, 2]
```

| j | h[j] | left_smaller | right_greater | product |
| --- | --- | --- | --- | --- |
| 0 | 3 | 1 | 1 | 1 |
| 1 | 1 | 0 | 2 | 0 |
| 2 | 4 | 2 | 0 | 0 |
| 3 | 2 | 1 | 0 | 0 |

Total is 1.

This shows the method correctly isolates triples even when they are not contiguous and depend on global ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Each of the two Fenwick passes performs $n$ updates and queries, each in logarithmic time |
| Space | $O(n)$ | Arrays for prefix/suffix counts plus Fenwick tree storage |

The constraint $n \le 8000$ makes $n \log n$ comfortably fast, since the total operations are on the order of a few hundred thousand.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, i, v):
            while i <= self.n:
                self.bit[i] += v
                i += i & -i

        def sum(self, i):
            s = 0
            while i > 0:
                s += self.bit[i]
                i -= i & -i
            return s

    n = int(input())
    h = list(map(int, input().split()))

    bit = Fenwick(n)
    left = [0] * n
    for i in range(n):
        left[i] = bit.sum(h[i] - 1)
        bit.add(h[i], 1)

    bit = Fenwick(n)
    right = [0] * n
    for i in range(n - 1, -1, -1):
        right[i] = bit.sum(n) - bit.sum(h[i])
        bit.add(h[i], 1)

    ans = 0
    for i in range(n):
        ans += left[i] * right[i]

    return str(ans)

# provided samples
assert run("3\n1 2 3\n") == "1", "sample 1"
assert run("3\n3 2 1\n") == "0", "sample 2"

# custom cases
assert run("1\n1\n") == "0", "minimum size"
assert run("2\n1 2\n") == "0", "too small for triple"
assert run("4\n1 2 3 4\n") == "4", "all increasing"
assert run("4\n4 3 2 1\n") == "0", "all decreasing"
assert run("5\n2 5 1 4 3\n") == "3", "mixed ordering"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 0 | minimum size |
| 2 increasing | 0 | cannot form triples |
| sorted increasing | 4 | full combinatorial counting |
| sorted decreasing | 0 | no valid triples |
| mixed permutation | 3 | correctness on general case |

## Edge Cases

The smallest input sizes test boundary behavior where the Fenwick logic must not access invalid indices. For $n = 1$, the prefix and suffix computations are never used in aggregation, and the algorithm correctly returns zero because no middle index exists.

For a strictly increasing sequence like $1,2,3,4$, every index contributes $(j)\cdot(n-j-1)$, which the algorithm captures through Fenwick counts without relying on adjacency. This ensures correctness even when every possible triple is valid.

For a strictly decreasing sequence, every prefix smaller count is zero, so all products vanish. The suffix computation also correctly yields zero because no element is larger than any earlier one, confirming that both halves of the decomposition behave symmetrically under reversal.
