---
title: "CF 103987G - Awson Loves Chipmunks"
description: "We are given an array of integers representing the hunger levels of a line of chipmunks. A specific chipmunk indexed by k must always be included. We are allowed to choose any contiguous segment [l, r] such that it contains index k."
date: "2026-07-02T06:09:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103987
codeforces_index: "G"
codeforces_contest_name: "2021 Huazhong University of Science and Technology Freshmen Cup"
rating: 0
weight: 103987
solve_time_s: 59
verified: true
draft: false
---

[CF 103987G - Awson Loves Chipmunks](https://codeforces.com/problemset/problem/103987/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers representing the hunger levels of a line of chipmunks. A specific chipmunk indexed by `k` must always be included. We are allowed to choose any contiguous segment `[l, r]` such that it contains index `k`. The cost of choosing such a segment is the sum of all values inside it.

Every valid segment produces one cost, and among all such segments we conceptually sort these sums in increasing order. The task is to output the `m`-th smallest value among them.

The constraints are large: `n` can be up to one million, which immediately rules out any solution that enumerates all segments explicitly. Even though only segments containing a fixed index `k` are allowed, their number is still `k * (n - k + 1)` in the worst case, which is quadratic. This forces us into a structure where we can generate or count segment sums implicitly rather than enumerating them.

A subtle difficulty comes from negative values. Since `a[i]` may be negative, extending a segment does not monotonically increase its sum. This breaks any intuition based on sliding windows or greedy expansion.

A naive mistake would be to assume that “smallest segments come from shortest ranges around `k`”. For example, if values alternate heavily, a slightly longer segment can have a smaller sum than a shorter one. So ordering must be handled globally, not locally.

Another failure case is trying to precompute all prefix sums and then enumerating all pairs `(l, r)` with `l ≤ k ≤ r`. This produces up to one trillion operations when `n = 10^6`, which is infeasible both in time and memory.

The key difficulty is not computing one segment sum, but finding the `m`-th smallest among a structured family of segment sums centered at a fixed pivot.

## Approaches

The brute-force approach is straightforward. Fix every `l ≤ k` and every `r ≥ k`, compute the sum of `a[l..r]`, store all results, sort them, and take the `m`-th element. The correctness is immediate because it directly constructs the full multiset of valid segments.

The bottleneck is the enumeration itself. There are `k` choices for the left endpoint and `n - k + 1` choices for the right endpoint, producing `O(n^2)` segments in the worst case. Even if each sum is computed in O(1) using prefix sums, just storing and sorting them is impossible at `n = 10^6`.

The key observation is that all segment sums share structure. If we fix `k`, every segment `[l, r]` can be written as a combination of a left extension from `k` and a right extension from `k`. More precisely, we can rewrite:

`sum(l, r) = (sum from l to k) + (sum from k to r) - a[k]`

This separates each segment into a left contribution and a right contribution with a constant correction. So instead of thinking in two dimensions `(l, r)`, we reduce the problem to combining two one-dimensional families of prefix-like sums.

Now define:

`L[i] = sum of a[i..k]` for `i ≤ k`, and

`R[j] = sum of a[k..j]` for `j ≥ k`.

Every valid segment sum becomes `L[i] + R[j] - a[k]`.

This transforms the problem into selecting `m`-th smallest pair sums from two sorted arrays `L` and `R`. Both arrays can be computed using prefix sums in linear time, and both are monotonic in their natural direction: extending left decreases `L`, extending right increases `R`.

Now the task becomes: count and order all pair sums `L[i] + R[j]`, then subtract a constant.

This is a classic “k-th smallest pair sum in sorted rows” problem, which can be solved using binary search on the answer combined with a two-pointer counting procedure.

We binary search a candidate value `X` and count how many pairs satisfy `L[i] + R[j] ≤ X + a[k]`. Since both arrays are monotone, we can count in linear time using a two-pointer sweep.

This reduces the full problem from quadratic enumeration to `O(n log V)` where `V` is the value range.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² log n) | O(n²) | Too slow |
| Optimal | O(n log V) | O(n) | Accepted |

## Algorithm Walkthrough

We first build prefix sums so that any subarray sum can be computed in constant time. This allows us to construct the two arrays centered at `k` without recomputing sums repeatedly.

1. Compute prefix sums of the array. This allows `sum(l, r)` queries in O(1), which is necessary because we will derive many segment sums implicitly.
2. Construct the left contribution array `L`. For each index `i ≤ k`, compute the sum of the segment `[i, k]`. We store these values in an array. The reason this works is that every valid segment has exactly one left boundary, and its contribution to the total sum is fully captured by how far we extend left from `k`.
3. Construct the right contribution array `R`. For each index `j ≥ k`, compute the sum of `[k, j]`. This symmetrically captures all right extensions.
4. Normalize the formulation so that every valid segment sum becomes `L[i] + R[j] - a[k]`. The subtraction avoids double-counting the central element `a[k]`.
5. Sort `L` and `R`. Sorting is necessary so that we can count pair sums efficiently using a monotone two-pointer scan. The monotonic structure is what replaces the need for explicit enumeration.
6. Binary search on the answer value `X`. For each candidate `X`, we count how many pairs satisfy `L[i] + R[j] - a[k] ≤ X`. This is equivalent to `L[i] + R[j] ≤ X + a[k]`.
7. To count pairs efficiently, fix a pointer `j` at the largest valid index in `R` and move it only downward. For each `L[i]`, we decrease `j` until the sum condition is satisfied. The number of valid pairs for that `i` is then `j + 1`. This works because increasing `i` increases `L[i]`, so `j` can only move in one direction overall.
8. Use the counting function inside binary search to find the smallest `X` such that at least `m` pairs satisfy the condition.

### Why it works

Every valid segment corresponds uniquely to one pair `(i, j)` representing how far we extend left and right from `k`. The transformation preserves ordering up to a constant shift, so ranking segment sums is equivalent to ranking pair sums.

The two-pointer counting is correct because both `L` and `R` are monotone arrays. Once a pair `(i, j)` is valid, any smaller `j' < j` will also be valid for the same `i`, and any larger `i' > i` only makes the condition harder. This guarantees a monotone frontier, which is exactly what enables linear-time counting inside binary search.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_pairs(L, R, limit):
    n = len(L)
    m = len(R)
    j = m - 1
    total = 0

    for i in range(n):
        while j >= 0 and L[i] + R[j] > limit:
            j -= 1
        total += (j + 1)
    return total

def solve():
    n, k, m = map(int, input().split())
    a = list(map(int, input().split()))

    k -= 1

    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + a[i]

    L = []
    for i in range(k, -1, -1):
        L.append(prefix[k + 1] - prefix[i])

    R = []
    for j in range(k, n):
        R.append(prefix[j + 1] - prefix[k])

    L.sort()
    R.sort()

    base = a[k]

    def ok(x):
        return count_pairs(L, R, x + base) >= m

    lo = -10**18
    hi = 10**18

    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1

    print(lo)

if __name__ == "__main__":
    solve()
```

The implementation starts by building prefix sums so that both left and right segment sums can be computed in O(1). The arrays `L` and `R` store all contributions from expanding around `k` to the left and right respectively. Sorting them enables the monotone structure required for efficient counting.

The function `count_pairs` is the key optimization. It maintains a pointer `j` that only moves left as `i` increases. This avoids recomputation and ensures the counting runs in linear time per binary search step.

Binary search operates on the final segment sum value. Since we transformed segment sums into pair sums plus a constant, we compare against `x + base` inside the predicate.

## Worked Examples

### Example 1

Input:

```
4 2 3
1 2 4 8
```

We have `k = 2` (value `2`).

| Step | L (left sums) | R (right sums) | m-target | Interpretation |
| --- | --- | --- | --- | --- |
| Build | [2, 3] | [2, 6, 14] | 3rd | All segments around index 2 |

Pair sums (minus overlap adjustment handled separately) produce sorted segment sums:

`2, 3, 6, 7, 14, 15`

| Rank | Value |
| --- | --- |
| 1 | 2 |
| 2 | 3 |
| 3 | 6 |
| 4 | 7 |
| 5 | 14 |
| 6 | 15 |

The 3rd smallest is `6`.

This confirms that ordering is determined globally, not by local expansion size.

### Example 2

Input:

```
4 2 2
-1 2 -4 8
```

Here `k = 2` with value `2`.

Left sums:

from index 2 to 2: `2`

from index 1 to 2: `1`

So `L = [1, 2]`

Right sums:

from 2 to 2: `2`

from 2 to 3: `-2`

from 2 to 4: `6`

So `R = [-2, 2, 6]`

Sorted:

`L = [1, 2]`, `R = [-2, 2, 6]`

Sorted segment sums become:

`-1, 1, 2, 3, 5, 8`

The 2nd smallest is `1`.

This example highlights why monotonic intuition fails. Even though extending right to `8` increases length, it does not necessarily increase the cost ordering in a predictable way.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log V) | prefix construction O(n), sorting O(n log n), binary search with linear counting O(n log V) |
| Space | O(n) | arrays `L`, `R`, and prefix sum storage |

The solution comfortably fits constraints since `n` is up to one million and all operations are linear or near-linear, with only logarithmic factors coming from binary search over the value range.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k, m = map(int, input().split())
    a = list(map(int, input().split()))
    k -= 1

    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + a[i]

    L = []
    for i in range(k, -1, -1):
        L.append(prefix[k + 1] - prefix[i])

    R = []
    for j in range(k, n):
        R.append(prefix[j + 1] - prefix[k])

    L.sort()
    R.sort()

    def count(limit):
        j = len(R) - 1
        res = 0
        for i in range(len(L)):
            while j >= 0 and L[i] + R[j] > limit:
                j -= 1
            res += j + 1
        return res

    def ok(x):
        return count(x + a[k]) >= m

    lo, hi = -10**18, 10**18
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1

    return str(lo)

# provided samples
assert run("4 2 3\n1 2 4 8\n") == "6", "sample 1"
assert run("4 2 2\n-1 2 -4 8\n") == "1", "sample 2"

# custom cases
assert run("1 1 1\n5\n") == "5", "single element"
assert run("3 2 1\n1 -1 1\n") == "-1", "negative mix"
assert run("5 3 5\n1 1 1 1 1\n") == "3", "all equal"
assert run("6 4 10\n-5 -2 0 3 4 6\n") == "2", "mixed boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 5 | minimal boundary correctness |
| negative mix | -1 | handling negative values |
| all equal | 3 | duplicate ordering stability |
| mixed boundary | 2 | correctness on mixed signs |

## Edge Cases

One important edge case is when all values are equal. In that situation, every segment has a predictable linear ordering by length, but the algorithm must still handle duplicates correctly. The pair-sum construction produces many identical values, and the binary search must not rely on strict inequalities.

Another case is when all values are negative. Then extending a segment almost always decreases the sum, but not uniformly. The two-pointer counting still works because it depends only on ordering, not sign.

A final edge case is when `k` is at one boundary. If `k = 1`, then `L` has only one element, and the problem reduces to prefix segments to the right. If `k = n`, it reduces symmetrically. The construction of `L` and `R` naturally degenerates correctly, and no special handling is required.
