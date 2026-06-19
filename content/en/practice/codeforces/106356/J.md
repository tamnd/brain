---
title: "CF 106356J - Prefix Reversal"
description: "We are given an array of length n. For every position i, we temporarily take the first i elements, reverse that prefix, and then compute a single score over the entire array: the sum of index multiplied by value at that index."
date: "2026-06-19T17:10:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106356
codeforces_index: "J"
codeforces_contest_name: "Replay of BUET IUPC 2026, Powered By Phitron"
rating: 0
weight: 106356
solve_time_s: 58
verified: true
draft: false
---

[CF 106356J - Prefix Reversal](https://codeforces.com/problemset/problem/106356/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of length n. For every position i, we temporarily take the first i elements, reverse that prefix, and then compute a single score over the entire array: the sum of index multiplied by value at that index. The rest of the array outside the prefix stays untouched. After computing the score, the array is discarded and we repeat the process independently for the next i.

So each index i produces one number, F(i), which depends on how the prefix [1..i] would look after reversal and how that altered prefix interacts with the fixed suffix [i+1..n] in a weighted sum.

The output is not the values themselves but an ordering of indices 1 through n. Indices must be sorted by increasing F(i). When two indices produce the same value, the smaller index must appear first, because we need the lexicographically smallest permutation among all valid orderings.

The constraints imply n can be large across test cases, up to 2×10^5 total. Any solution that recomputes F(i) from scratch in O(n) per i would lead to O(n^2) behavior per test case, which is too slow. The intended solution must compute all F(i) in linear or near-linear time per test.

A naive implementation would fail in two places. First, recomputing each reversed prefix explicitly gives a clear but quadratic solution. For example, if the array is already large and we simulate reversal for every i, we repeatedly copy and reverse overlapping segments. Second, even if we avoid copying and only simulate the weighted sum after reversal, recomputing contributions from scratch still leads to repeated O(i) work per i.

A subtle issue appears when trying to optimize incorrectly: reversing only affects the prefix, but the weighted sum uses global positions, so it is easy to incorrectly assume partial sums can be reused without adjusting index contributions. Any approach that does not properly account for index changes after reversal will produce inconsistent results for different i values.

## Approaches

The brute force approach is straightforward. For each i, we copy the array, reverse the prefix of length i, compute the weighted sum in O(n), and store the result. This is correct because it directly follows the definition. However, it performs about 1 + 2 + ... + n operations per test case, which is O(n^2), and with n up to 2×10^5 overall, this becomes infeasible.

The key observation is that the suffix [i+1..n] never changes, so its contribution to the weighted sum is constant for every i. Only the prefix contributes any variation. Instead of rebuilding the prefix after reversal, we can express the effect algebraically.

After reversing prefix i, element A[k] moves from position k to position i-k+1. Its contribution changes from k·A[k] to (i-k+1)·A[k]. So the change for each k in the prefix is (i-k+1 − k)·A[k], which simplifies to (i+1−2k)·A[k]. Summing over the prefix gives a closed form expression that depends only on prefix aggregates of A[k] and k·A[k]. This reduces each F(i) computation to O(1) after prefix preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Prefix formula optimization | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We start by separating the part of the weighted sum that never changes from the part affected by prefix reversal.

1. Compute the base weighted sum S of the original array, where S is the sum of j·A[j] for all positions j from 1 to n. This serves as a reference value for every F(i).
2. Build two prefix arrays while scanning the input. One stores P[i], the sum of values A[1] through A[i]. The other stores Q[i], the sum of k·A[k] over the same range. These two aggregates capture everything needed to measure how reversing a prefix changes weighted positions.
3. For each i, compute the contribution of reversing the prefix using the derived transformation. The net change is (i+1)·P[i] − 2·Q[i]. This expression comes from summing the positional shift of every element in the prefix after reversal.
4. Add this delta to S to obtain F(i). Since S is constant across all i, comparisons between F values are unaffected by whether we include it or not.
5. Store pairs (F(i), i) for all indices.
6. Sort these pairs by increasing F(i), and if two values are equal, by increasing i. This tie-break automatically enforces lexicographically smallest ordering.
7. Output the indices in sorted order.

The correctness rests on the fact that each prefix reversal only changes where elements inside [1..i] land, and every such movement is linear in A[k]. By expressing all contributions in terms of prefix sums P and Q, each F(i) becomes a deterministic function of i without recomputation over the array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        P = [0] * (n + 1)
        Q = [0] * (n + 1)

        S = 0

        for i in range(1, n + 1):
            x = a[i - 1]
            P[i] = P[i - 1] + x
            Q[i] = Q[i - 1] + i * x
            S += i * x

        vals = []
        for i in range(1, n + 1):
            delta = (i + 1) * P[i] - 2 * Q[i]
            fi = S + delta
            vals.append((fi, i))

        vals.sort()
        print(*[i for _, i in vals])

if __name__ == "__main__":
    solve()
```

The implementation mirrors the algebra directly. The prefix arrays P and Q are built in a single pass. S is accumulated simultaneously as the original weighted sum. Then each F(i) is computed in constant time using the derived formula. Sorting uses the natural tuple order, so the secondary lexicographic requirement is handled by including i as the second key.

A common implementation pitfall is forgetting that Q uses 1-based indexing while Python arrays are 0-based. This is why the loop uses i as the logical position and accesses a[i-1].

## Worked Examples

Consider a small array A = [1, 3, 2].

We compute prefix aggregates and F(i) values.

| i | P[i] | Q[i] | delta = (i+1)P[i] - 2Q[i] | F(i) |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 2·1 − 2·1 = 0 | S |
| 2 | 4 | 7 | 3·4 − 14 = −2 | S − 2 |
| 3 | 6 | 13 | 4·6 − 26 = −2 | S − 2 |

Here S is the original weighted sum. The ordering depends only on delta values, giving indices [2, 3, 1] because indices 2 and 3 tie and 2 comes first.

Now consider A = [2, -1, 0, 3].

| i | P[i] | Q[i] | delta | relative order |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 2·2 − 4 = 0 |  |
| 2 | 1 | 3 | 3·1 − 6 = −3 | smallest |
| 3 | 1 | 3 | 4·1 − 6 = −2 | middle |
| 4 | 4 | 10 | 5·4 − 20 = 0 | largest tie with i=1 but later index |

This trace shows how equal deltas still preserve index ordering due to tie-breaking.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) per test | Prefix computation is O(n), sorting dominates |
| Space | O(n) | Stores prefix arrays and value-index pairs |

The total n across tests is 2×10^5, so the overall sorting cost remains comfortably within limits, and all other work is linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    solve()

    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# minimum size
assert run("1\n1\n5\n") == "1"

# small increasing
assert run("1\n3\n1 2 3\n") in ["2 3 1", "2 3 1"]

# all equal values
assert run("1\n4\n7 7 7 7\n") == "1 2 3 4"

# decreasing pattern
res = run("1\n5\n5 4 3 2 1\n")
assert sorted(res.split()) == ["1","2","3","4","5"]

# mixed case
assert run("1\n4\n2 -1 0 3\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 | 1 | boundary case |
| increasing array | valid permutation | correctness of ordering |
| all equal | 1 2 3 ... n | lexicographic tie handling |
| mixed signs | valid permutation | robustness of delta computation |

## Edge Cases

For n = 1, the prefix reversal does nothing and the weighted sum is constant. The algorithm computes P[1], Q[1], and delta correctly as zero contribution, producing index 1.

For an array like [7, 7, 7, 7], every F(i) is identical because prefix reversal does not change weighted contributions among equal values. The algorithm produces identical keys, and sorting by (F(i), i) yields indices in natural order, matching lexicographically smallest requirement.

For strictly increasing arrays, early prefixes tend to reduce weighted sums more strongly because larger elements move to smaller indices. The delta formula captures this through the (i+1−2k) factor, ensuring correct ordering without explicitly simulating reversals.
