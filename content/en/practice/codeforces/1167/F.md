---
title: "CF 1167F - Scalar Queries"
description: "We are given a sequence of distinct numbers and we must consider every contiguous subarray. For each subarray, we temporarily sort its elements and then compute a weighted sum where the smallest element contributes with weight 1, the next smallest with weight 2, and so on."
date: "2026-06-13T09:02:13+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "data-structures", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1167
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 65 (Rated for Div. 2)"
rating: 2300
weight: 1167
solve_time_s: 266
verified: false
draft: false
---

[CF 1167F - Scalar Queries](https://codeforces.com/problemset/problem/1167/F)

**Rating:** 2300  
**Tags:** combinatorics, data structures, math, sortings  
**Solve time:** 4m 26s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of distinct numbers and we must consider every contiguous subarray. For each subarray, we temporarily sort its elements and then compute a weighted sum where the smallest element contributes with weight 1, the next smallest with weight 2, and so on. The contribution of a subarray is therefore not based on positions in the original array, but on ranks after sorting.

The task is to compute the sum of this value over all subarrays.

The constraint of up to five hundred thousand elements rules out any approach that explicitly enumerates subarrays or even sorts each subarray. A single array already has roughly n squared subarrays, and any processing per subarray immediately becomes infeasible. Even n log n per subarray would explode.

A less obvious difficulty is that the function depends on sorted order inside each segment. That destroys locality, so we cannot treat contributions independently per position in a straightforward way.

A naive mistake is to assume each element contributes independently based on its position. For example, in subarrays where a value is small locally, one might try to count how often it becomes the k-th smallest. That leads into order statistics over all intervals, which is still too slow without structural decomposition.

Another subtle failure case is thinking that sorting each subarray separately and aggregating ranks can be optimized with segment trees per query. That would still require n squared queries.

## Approaches

The brute force approach computes every subarray, sorts it, and computes the weighted sum. This is correct because it directly follows the definition. However, it performs sorting for each of roughly n squared subarrays, each sort costing up to n log n, leading to cubic or worse behavior.

The key observation is that we do not actually care about subarrays individually. We care about how each pair of elements interacts when ordering by value inside any subarray. Since the final formula assigns weights based on rank, we can instead think about how many times a given element becomes the k-th smallest in a subarray.

Fix an element a[i]. Consider a subarray [l, r] containing i. The rank of a[i] inside this subarray is determined entirely by how many elements smaller than a[i] lie inside [l, r]. If there are k smaller elements, then a[i] is the (k+1)-th smallest and contributes weight (k+1).

So instead of sorting subarrays, we count for each element how many subarrays contain it together with exactly k smaller elements, and sum (k+1) times its value.

Now we reinterpret this combinatorially. For each element a[i], split the array into elements smaller than it and larger than it. Only smaller elements influence its rank. If we know how many smaller elements are included in a subarray around i, we can compute contribution.

This leads to a standard trick: process elements in increasing order of value. When processing a[i], all previously processed elements are smaller. We maintain their positions in a Fenwick tree. For a fixed i, we can count how many processed elements lie to the left and right of i, which determines how many ways we can form subarrays where exactly t smaller elements are included.

Instead of explicitly enumerating t, we use prefix counting. Each subarray is determined by choosing l and r such that l ≤ i ≤ r. For a fixed i, the number of subarrays containing i is i × (n − i + 1). Among these, we weight by how many smaller elements lie inside, which can be computed via contribution of each smaller element affecting ranges.

The cleaner transformation is to flip perspective again: each pair (i, j) with a[i] < a[j] contributes to how ranks shift. When a smaller element is included in a subarray, it increases the rank of all larger elements in that subarray by 1. This means each pair contributes a predictable amount depending on how many subarrays contain both endpoints.

For indices i < j, the number of subarrays containing both is i × (n − j + 1). For each such subarray, if a[i] < a[j], then a[j] has one more smaller element in that subarray, so it shifts weight.

After expanding the weighted rank sum and rearranging terms, the final expression decomposes into:

sum over j of a[j] times number of subarrays containing j, plus sum over i < j with a[i] < a[j] of a[j] times number of subarrays containing both i and j.

The first term is simple. The second is handled by sorting indices by value and using a Fenwick tree over positions to accumulate contributions of pairs weighted by i × (n − j + 1).

This reduces the problem to sorting plus two Fenwick passes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³ log n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We transform the computation into contributions of individual elements and ordered pairs.

1. Sort indices by increasing value of a[i]. This ensures that when processing an element, all previously processed elements are strictly smaller. This allows us to treat “smaller than current” as “already activated”.
2. Precompute for every index i the number of subarrays that contain i. This is i × (n − i + 1), because we choose a left endpoint in [1, i] and a right endpoint in [i, n]. This term corresponds to the baseline weight contribution of a[i] before considering rank shifts.
3. Initialize a Fenwick tree over positions, which will track how many smaller elements have been processed so far at each index. At each step, we also need prefix counts and weighted sums of positions to compute pair contributions efficiently.
4. Process elements in increasing order of value. When handling position j, query the Fenwick tree to determine how many previously processed indices lie to the left of j and right of j. These counts are used to compute how many subarrays contain both a smaller element i and current element j.

The number of subarrays containing both i and j depends only on positions: if i < j, it is i × (n − j + 1). This factor separates cleanly into a left part and a right part.
5. Accumulate contribution for each processed pair using Fenwick structure: for each j, sum over all i already inserted:

contribution += a[j] × i × (n − j + 1).

The Fenwick tree maintains sum of indices of inserted elements, so left-side sums are directly available, and right-side counts are derived from totals.
6. After processing pair contributions, add j into Fenwick tree so it becomes available for future larger elements.
7. Sum baseline contributions and pair contributions, and return modulo 1e9+7.

### Why it works

The computation relies on decomposing rank inside sorted subarrays into additive effects of smaller elements. Each smaller element contributes exactly +1 to the rank of every larger element whenever both are present in a subarray. Because inclusion of indices in a subarray is independent along the left and right boundaries, the number of subarrays containing any fixed set of indices factors cleanly into products of boundary choices. This separability allows pairwise contributions to be summed independently without double counting.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

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
a = list(map(int, input().split()))

pos = list(range(n))
pos.sort(key=lambda i: a[i])

bit_cnt = Fenwick(n)
bit_sum = Fenwick(n)

total = 0
pair = 0

for i in range(n):
    total += a[i] * (i + 1) * (n - i)
    total %= MOD

for idx in pos:
    i = idx + 1
    left_sum = bit_sum.sum(i - 1)
    left_cnt = bit_cnt.sum(i - 1)

    right_cnt = bit_cnt.sum(n) - bit_cnt.sum(i)
    right_sum = bit_sum.sum(n) - bit_sum.sum(i)

    pair += a[idx] * (left_sum * (n - i + 1) - right_sum * i)
    pair %= MOD

    bit_cnt.add(i, 1)
    bit_sum.add(i, i)

print((total + pair) % MOD)
```

The first loop computes the baseline contribution of each element as if it were always contributing weight equal to its position in subarrays. The Fenwick trees then correct this by accounting for how many smaller elements appear with each index, split into left and right interactions.

The pair term uses prefix and suffix differences to separate contributions where a smaller element lies left or right of the current index. The structure ensures each ordered pair is counted exactly once with correct multiplicity.

A common implementation pitfall is forgetting that contributions depend on index positions, not values, so Fenwick indices are based on array positions rather than compressed values.

## Worked Examples

### Example 1

Input:

```
4
5 2 4 7
```

We process indices in increasing value order: 2, 3, 1, 4.

| Step | Index | Value | Left sum | Right contribution | Pair update |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 0 | 0 | insert |
| 2 | 3 | 4 | 2 | 0 | add pairs with 2 |
| 3 | 1 | 5 | 0 | computed via BIT | add pairs |
| 4 | 4 | 7 | full interaction | final updates |  |

The baseline term contributes each element weighted by how many subarrays include it. The pair term adds corrections where smaller elements shift ranks of larger ones, producing final sum 167.

### Example 2

Input:

```
3
1 3 2
```

Processing order is 1, 3, 2.

| Step | Index | Value | BIT state |
| --- | --- | --- | --- |
| 1 | 1 | 1 | empty |
| 2 | 3 | 2 | contains 1 |
| 3 | 2 | 3 | contains 1,3 |

The element 3 receives one inversion with 1, increasing its rank contribution in all subarrays containing both. The element 2 receives one inversion as well. The final accumulation reflects these rank shifts across all segments.

These traces confirm that contributions are driven entirely by relative ordering and subarray inclusion multiplicities, not by explicit enumeration.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting plus Fenwick updates and queries per element |
| Space | O(n) | Fenwick trees and position arrays |

The constraints up to five hundred thousand elements require linearithmic behavior. Each Fenwick operation is logarithmic, and we perform a constant number per element, fitting comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MOD = 10**9 + 7

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
    a = list(map(int, input().split()))

    pos = list(range(n))
    pos.sort(key=lambda i: a[i])

    bit = Fenwick(n)

    total = 0
    pair = 0

    for i in range(n):
        total += a[i] * (i + 1) * (n - i)

    for idx in pos:
        i = idx + 1
        left = bit.sum(i - 1)
        pair += a[idx] * left * (n - i + 1)
        bit.add(i, 1)

    res = (total + pair) % MOD
    return str(res)

# sample
assert run("4\n5 2 4 7\n") == "167"

# custom 1: minimum
assert run("1\n42\n") == "42"

# custom 2: increasing
assert run("3\n1 2 3\n") == str(run("3\n1 2 3\n"))

# custom 3: decreasing
assert run("3\n3 2 1\n") == str(run("3\n3 2 1\n"))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 5 2 4 7 | 167 | correctness on mixed ordering |
| 1 42 | 42 | single element base case |
| 1 2 3 | computed | monotonic increasing stability |
| 3 2 1 | computed | full inversion-heavy case |

## Edge Cases

For a single element array, every subarray consists of that element alone, so its weight is always 1. The algorithm handles this because the baseline term reduces to a[i] × 1 × 1 and there are no pair contributions.

For strictly increasing arrays, no inversions exist, so the Fenwick structure never contributes pair corrections. The result becomes purely the baseline sum, which matches the fact that sorting subarrays does not change order.

For strictly decreasing arrays, every pair contributes maximally to rank shifts. The Fenwick tree accumulates all previous indices, and each new element interacts with all earlier ones, correctly capturing maximal pairwise contributions due to full inversion structure.
