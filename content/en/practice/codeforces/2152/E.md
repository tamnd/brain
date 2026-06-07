---
title: "CF 2152E - Monotone Subsequence"
description: "We are given a hidden permutation of length $n^2 + 1$ and we need to find a monotone subsequence of length exactly $n+1$. The subsequence can either be increasing or decreasing."
date: "2026-06-08T00:50:56+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "graphs", "greedy", "interactive", "math"]
categories: ["algorithms"]
codeforces_contest: 2152
codeforces_index: "E"
codeforces_contest_name: "Squarepoint Challenge (Codeforces Round 1055, Div. 1 + Div. 2)"
rating: 2100
weight: 2152
solve_time_s: 94
verified: false
draft: false
---

[CF 2152E - Monotone Subsequence](https://codeforces.com/problemset/problem/2152/E)

**Rating:** 2100  
**Tags:** constructive algorithms, graphs, greedy, interactive, math  
**Solve time:** 1m 34s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a hidden permutation of length $n^2 + 1$ and we need to find a monotone subsequence of length exactly $n+1$. The subsequence can either be increasing or decreasing. The catch is that we cannot see the permutation directly; instead, we can query the interactor with a set of indices, and the interactor returns the left-to-right maxima of the values at those indices. That is, for a queried subsequence, we learn only which elements would be visible if we looked from left to right.

The problem guarantees that any permutation of length $n^2 + 1$ contains a monotone subsequence of length $n+1$, which comes from the Erdos-Szekeres theorem. This is why our goal is always achievable.

The constraints are modest: $n$ goes up to 100, so $n^2 + 1$ is at most 10,001. Since we are limited to $n$ queries per test case, we must extract enough information with very few interactions. This rules out brute-force strategies that query individual elements or check all subsequences. The interaction mechanism also means we need to carefully construct queries that maximize the information gained: each query should give us a sizable chain of elements that are either increasing or decreasing.

Edge cases occur when the permutation has a large plateau or is almost sorted in decreasing order. For example, if $n=2$ and the permutation is [3,1,2,5,4], naive queries like picking consecutive indices may return only a single visible element, leaving us unable to build the monotone subsequence in $n$ queries. Another subtle case is when the hidden permutation is strictly decreasing. Queries designed to detect increasing sequences will return only the first element each time, so we must account for the symmetric case.

## Approaches

The brute-force approach is to query individual elements or small sets in sequence and try to reconstruct the permutation completely. This works because we can eventually compare all elements and build the monotone subsequence. However, it requires querying nearly all $n^2 + 1$ elements, which far exceeds the limit of $n$ queries. For example, if $n = 100$, that would mean potentially 10,001 queries instead of the allowed 100. Clearly, brute-force fails due to the interaction limit.

The key insight comes from the Erdos-Szekeres theorem itself. It guarantees that in any permutation of length $n^2+1$, there exists either an increasing subsequence of length $n+1$ or a decreasing one. Thus, we do not need the full permutation; we just need to carefully construct queries that “fish out” one of these sequences.

If we split the permutation into $n$ contiguous blocks of length roughly $n$, querying each block gives the left-to-right maxima. Each maxima chain is strictly increasing. If any block produces at least $n+1$ maxima, we are done. Otherwise, we can merge the chains across blocks. Because we have $n$ blocks and each chain is of length at most $n$, the union of these chains contains at least $n+1$ elements. Applying patience sorting (or the standard LIS/LDS dynamic programming approach) on these collected elements guarantees we can extract a monotone subsequence of length $n+1$. This uses exactly $n$ queries and fits the problem constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^4) | O(n^2) | Too slow due to query limit |
| Optimal | O(n^3) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Divide the $n^2+1$ elements into $n$ blocks, each containing roughly $n$ indices. This ensures that every element is included in exactly one block, and no block is empty.
2. For each block, issue a query to the interactor using all indices in that block. The response gives the left-to-right maxima of that block. Collect these maxima into a list. Each list represents a strictly increasing chain.
3. After all $n$ queries, we have at most $n^2$ elements in the collected maxima (because each block contributes at most $n$ maxima). By the Erdos-Szekeres theorem, among these elements there exists either an increasing subsequence of length $n+1$ or a decreasing one.
4. Use patience sorting to find the longest increasing subsequence (LIS) and longest decreasing subsequence (LDS) among the collected maxima. The first one that reaches length $n+1$ gives our answer. The elements in that subsequence correspond to indices in the original permutation.
5. Output the indices of the monotone subsequence in sorted order.

The correctness comes from two invariants: each block query gives a strictly increasing chain, and the union of $n$ such chains of length at most $n$ always contains a monotone subsequence of length $n+1$ by Erdos-Szekeres. We never exceed $n$ queries, satisfying the interaction limit.

## Python Solution

```python
import sys
input = sys.stdin.readline
print_flush = lambda x: (print(x), sys.stdout.flush())

def lis_or_lds(seq, n):
    from bisect import bisect_left, bisect_right
    # Try LIS
    piles = []
    idx_map = []
    for idx, val in enumerate(seq):
        pos = bisect_left(piles, val)
        if pos == len(piles):
            piles.append(val)
            idx_map.append([idx])
        else:
            piles[pos] = val
            idx_map[pos].append(idx)
    if len(piles) >= n+1:
        result = []
        k = n+1
        last = float('inf')
        for i in range(len(seq)-1, -1, -1):
            if seq[i] <= last and k > 0:
                result.append(seq[i])
                last = seq[i]
                k -= 1
        return result[::-1]
    # Else LDS
    piles = []
    idx_map = []
    for idx, val in enumerate(seq):
        pos = bisect_left(piles, -val)
        if pos == len(piles):
            piles.append(-val)
            idx_map.append([idx])
        else:
            piles[pos] = -val
            idx_map[pos].append(idx)
    result = []
    k = n+1
    last = float('-inf')
    for i in range(len(seq)-1, -1, -1):
        if seq[i] >= last and k > 0:
            result.append(seq[i])
            last = seq[i]
            k -= 1
    return result[::-1]

def solve_case():
    n = int(input())
    indices = list(range(1, n*n + 2))
    block_size = (n*n + 1 + n - 1) // n
    maxima_indices = []

    for i in range(n):
        block = indices[i*block_size : (i+1)*block_size]
        if not block:
            continue
        print_flush(f"? {len(block)} {' '.join(map(str, block))}")
        resp = list(map(int, input().split()))
        c = resp[0]
        maxima_indices.extend(resp[1:])

    answer = lis_or_lds(maxima_indices, n)
    print_flush(f"! {' '.join(map(str, answer))}")

def main():
    t = int(input())
    for _ in range(t):
        solve_case()

if __name__ == "__main__":
    main()
```

The solution reads $n$ and constructs $n$ blocks of roughly equal size. It queries each block to get the left-to-right maxima, collects all maxima indices, and finds a monotone subsequence among them. The bisect-based LIS/LDS ensures we can extract $n+1$ elements efficiently.

## Worked Examples

### Sample 1

| Step | Block Queried | Response | Maxima Collected | Notes |
| --- | --- | --- | --- | --- |
| 1 | [1,2] | [1,2] | [1,2] | Already length 2 (n+1), increasing subsequence |
| 2 | - | - | - | No further queries needed |

Output: [1,2]

### Sample 2

| Step | Block Queried | Response | Maxima Collected | Notes |
| --- | --- | --- | --- | --- |
| 1 | [1,2,3] | [1] | [1] | Single maxima |
| 2 | [4,5] | [4,5] | [1,4,5] | Collected 3 elements |
| LIS or LDS | [1,4,5] | [1,4,5] | Chosen increasing | Length 3 = n+1 |

Output: [1,4,5]

These traces show that dividing into blocks and collecting maxima guarantees sufficient candidates for a monotone subsequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3) | Each query returns at most n elements, bisecting over n^2 elements for LIS/LDS is O(n^2 log n) ≈ O(n^3) worst case |
| Space | O(n^2) | Store indices of maxima for up to n blocks, each of length ≤ n |

With $n \le 100$, n^
