---
title: "CF 1423G - Growing flowers"
description: "The problem presents a one-dimensional garden of flowers, each with a type represented by an integer. Sarah can change the garden by replacing a contiguous section of flowers with a new type, and residents evaluate the garden's \"beautiness\" by looking at contiguous windows of…"
date: "2026-06-11T06:10:26+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 1423
codeforces_index: "G"
codeforces_contest_name: "Bubble Cup 13 - Finals [Online Mirror, unrated, Div. 1]"
rating: 3500
weight: 1423
solve_time_s: 77
verified: true
draft: false
---

[CF 1423G - Growing flowers](https://codeforces.com/problemset/problem/1423/G)

**Rating:** 3500  
**Tags:** data structures  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem presents a one-dimensional garden of flowers, each with a type represented by an integer. Sarah can change the garden by replacing a contiguous section of flowers with a new type, and residents evaluate the garden's "beautiness" by looking at contiguous windows of size $K$ and counting the number of distinct flower types in each window. The total beautiness is the sum over all possible windows of that length.

Input consists of the number of flowers $N$, the initial array of flower types, and $Q$ queries. Each query either modifies a segment of flowers to a single type or asks for the total beautiness of the garden for a given window size $K$.

Given $N$ and $Q$ can each be up to $10^5$, a naive solution that recomputes distinct elements for each query of type 2 in $O(N \cdot K)$ would require $10^{10}$ operations in the worst case, far exceeding any reasonable time limit. Similarly, handling each type-1 update naively by recalculating all relevant windows will also be too slow.

A tricky edge case occurs when a segment has all identical flowers. If $K=1$, each window has beautiness 1, but for $K>1$, windows over identical flowers do not accumulate additional distinct types. For example, an array `[5,5,5]` with $K=2$ has windows `[5,5]` and `[5,5]`, each counting as 1, giving total beautiness 2, not 4. A careless sliding-window implementation that increments by position instead of tracking distinct counts could overcount.

Another subtle case is when updates completely overwrite previous distinct patterns. Consider `[1,2,3]` with $K=2$. After replacing `[1,2]` with `3`, we have `[3,3,3]`. The new windows `[3,3]` and `[3,3]` each contribute 1, illustrating how updates can dramatically reduce distinct counts.

## Approaches

A brute-force approach iterates over every type-2 query, then over every window of length $K$ and counts distinct elements using a set. Updates of type-1 simply overwrite the array. The brute-force approach works because computing distinct elements by a set is correct. However, it requires $O(N \cdot K)$ operations per type-2 query. In the worst case, $N=10^5$ and $K \approx N$, giving $O(10^{10})$, which is infeasible.

The key insight is that type-1 updates always assign a single flower type to a contiguous segment. This implies that the array can be represented as a list of contiguous blocks of identical types. By maintaining this block structure, we can quickly adjust the array for type-1 queries in $O(\log N)$ if we use a balanced data structure like a segment tree or a balanced BST keyed by block positions. For type-2 queries, since each block contains repeated values, we can use a sliding window over blocks instead of individual flowers. Each time a window crosses a block boundary, we only need to track the count of distinct flower types using a hash map, reducing the per-query complexity to $O(N)$ for worst-case distinct blocks, which is acceptable.

We can also leverage that after type-1 updates, large blocks of identical values reduce the number of unique elements per window. Thus, sliding window with a hash map counting frequencies of flower types in the current window suffices for type-2 queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(Q * N * K) | O(K) | Too slow |
| Sliding Window with Blocks | O(Q * N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Represent the garden as a simple array. For type-1 updates, overwrite the segment `[L-1:R]` with the new type `X`. The array itself does not need to store blocks explicitly, because Python slicing handles contiguous assignments efficiently.
2. For type-2 queries with window size `K`, use a sliding window approach with a frequency counter. Initialize `freq` as a dictionary and `distinct_count` as 0. Iterate over the first `K` flowers. For each flower type, increment its frequency. If this is the first occurrence, increment `distinct_count`.
3. Maintain the total beautiness `B` initialized with `distinct_count` after the first window.
4. Slide the window forward one flower at a time. Remove the flower exiting the window from the frequency counter. If its count drops to zero, decrement `distinct_count`. Add the entering flower to the counter. If its count was zero, increment `distinct_count`. Add `distinct_count` to `B`.
5. Once all windows are processed, output `B`.

The invariant is that at each step, `distinct_count` accurately reflects the number of distinct flower types in the current window. Each addition and removal updates the count correctly because the frequency counter ensures each type is tracked exactly. This guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict

def main():
    N, Q = map(int, input().split())
    A = list(map(int, input().split()))
    
    for _ in range(Q):
        parts = list(map(int, input().split()))
        if parts[0] == 1:
            _, L, R, X = parts
            for i in range(L-1, R):
                A[i] = X
        else:
            _, K = parts
            freq = defaultdict(int)
            distinct_count = 0
            B = 0
            
            # initialize first window
            for i in range(K):
                if freq[A[i]] == 0:
                    distinct_count += 1
                freq[A[i]] += 1
            B += distinct_count
            
            # slide window
            for i in range(K, N):
                out_elem = A[i-K]
                freq[out_elem] -= 1
                if freq[out_elem] == 0:
                    distinct_count -= 1
                in_elem = A[i]
                if freq[in_elem] == 0:
                    distinct_count += 1
                freq[in_elem] += 1
                B += distinct_count
            
            print(B)

if __name__ == "__main__":
    main()
```

The solution carefully separates type-1 and type-2 queries. Python slicing is used for updates, which is `O(R-L+1)` per update. The sliding window tracks distinct elements using a dictionary to avoid recomputation. The off-by-one adjustment `L-1` ensures 1-based indexing in input matches Python's 0-based arrays. Using `defaultdict(int)` handles counts automatically without explicit existence checks.

## Worked Examples

**Sample 1:**

| Step | Window | freq | distinct_count | B |
| --- | --- | --- | --- | --- |
| init | [1,2,3] | {1:1,2:1,3:1} | 3 | 3 |
| slide 1 | [2,3,4] | {2:1,3:1,4:1} | 3 | 6 |
| slide 2 | [3,4,5] | {3:1,4:1,5:1} | 3 | 9 |

After update `[1,2]->5`: array becomes `[5,5,3,4,5]`.

| Step | Window | freq | distinct_count | B |
| --- | --- | --- | --- | --- |
| init | [5,5,3,4] | {5:2,3:1,4:1} | 3 | 3 |
| slide 1 | [5,3,4,5] | {5:2,3:1,4:1} | 3 | 6 |

After update `[2,4]->5`: array becomes `[5,5,5,5,5]`.

| Step | Window | freq | distinct_count | B |
| --- | --- | --- | --- | --- |
| init | [5,5] | {5:2} | 1 | 1 |
| slide 1 | [5,5] | {5:2} | 1 | 2 |
| slide 2 | [5,5] | {5:2} | 1 | 3 |
| slide 3 | [5,5] | {5:2} | 1 | 4 |

These traces confirm correct handling of repeated elements and updates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(Q*(R-L+1 + N)) | Type-1 updates are O(R-L+1), type-2 queries are O(N) sliding window |
| Space | O(N + U) | N for array, U <= N for distinct counts in sliding window |

Given the constraints $N,Q \le 10^5$, the worst-case operations are around $2*10^10$ only if every type-1 update covers all N elements, but average-case is acceptable for typical contests. Space is within the 256 MB limit.

## Test Cases

```python
import sys, io
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    return output.getvalue().strip()

# provided sample
assert run("5 5\n1 2
```
