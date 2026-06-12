---
title: "CF 911D - Inversion Counting"
description: "We are given a permutation of integers from 1 to n, meaning every number in that range appears exactly once in some order. An inversion is a pair of positions where a larger index holds a smaller number than a smaller index, effectively a local \"disorder."
date: "2026-06-13T00:29:39+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 911
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 35 (Rated for Div. 2)"
rating: 1800
weight: 911
solve_time_s: 275
verified: true
draft: false
---

[CF 911D - Inversion Counting](https://codeforces.com/problemset/problem/911/D)

**Rating:** 1800  
**Tags:** brute force, math  
**Solve time:** 4m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of integers from 1 to _n_, meaning every number in that range appears exactly once in some order. An inversion is a pair of positions where a larger index holds a smaller number than a smaller index, effectively a local "disorder." For example, in the permutation [4, 1, 3, 2], the number 1 at index 2 is smaller than the 4 at index 1, forming an inversion.

The task is to process multiple queries, each reversing a subsegment of the permutation. After each reversal, we do not need the exact count of inversions but only whether it is odd or even.

The constraints are subtle. The permutation length _n_ is up to 1500, which is small enough to do operations quadratic in _n_ if needed. However, the number of queries _m_ is very large, up to 2·10^5. This combination immediately rules out any solution that recomputes inversions from scratch after each query, since even an O(n^2) inversion count per query would require roughly 4.5·10^11 operations in the worst case. We need an approach that handles queries in O(1) or O(n) at worst.

Edge cases arise from very short segments or segments of length one. Reversing a segment of length 1 should not change the inversion count at all. A permutation already in increasing or decreasing order requires careful handling to ensure the parity flips are computed correctly. For example, reversing the whole permutation of size 2 switches a single inversion, flipping the parity from even to odd.

## Approaches

The brute-force approach is straightforward: after reading the permutation, we could iterate over every pair of indices for each query and count inversions. This works because the inversion definition is explicit, but it becomes impractical as soon as we have more than a few thousand queries because each count would be O(n^2).

The key insight that unlocks an efficient solution comes from focusing on parity rather than exact inversion counts. Consider what happens when we reverse a subarray of length _k_. Each pair of elements in the subarray swaps their relative order exactly once. There are _k·(k-1)/2_ pairs in a segment of length _k_. Therefore, the parity of the number of inversions in the segment flips if and only if _k·(k-1)/2_ is odd. This reduces each query to computing whether this simple arithmetic value is odd or even, which can be done in constant time.

We do not need to track which specific elements swap; the invariant is that the parity of the overall inversion count changes only when the number of element pairs in the reversed segment is odd. This observation transforms a problem that seems inherently O(n^2) per query into an O(1) per query parity update.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m·n^2) | O(n) | Too slow |
| Optimal | O(n^2 + m) | O(n) | Accepted |

## Algorithm Walkthrough

1. First, count the initial number of inversions in the permutation. This is done by iterating through all pairs `(i, j)` with `i > j` and checking if `a[i] < a[j]`. Store the parity only: even or odd.
2. For each query with segment `[l, r]`, compute the length of the segment as `k = r - l + 1`.
3. Compute the number of pairs within the segment, which is `k * (k - 1) / 2`. Check whether this number is odd or even. If odd, flip the current parity of inversions. If even, leave the parity unchanged.
4. Output "odd" or "even" based on the updated parity.

Why it works: The parity of inversions in the permutation is affected only by swaps that reverse order within the segment. Each pair in the reversed segment contributes exactly one swap to the inversion count. Thus, the only relevant information for the query is whether the number of such pairs is odd or even, which guarantees the parity update is correct for any permutation and any query length.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
m = int(input())

# compute initial inversion parity
parity = 0  # 0 = even, 1 = odd
for i in range(n):
    for j in range(i):
        if a[i] < a[j]:
            parity ^= 1  # flip parity

for _ in range(m):
    l, r = map(int, input().split())
    k = r - l + 1
    if (k * (k - 1) // 2) % 2 == 1:
        parity ^= 1
    print("odd" if parity else "even")
```

The first double loop computes the initial parity correctly. Using XOR with 1 flips the parity whenever a swap contributes an odd number. The query processing is constant time: compute the length, compute the number of pairs, check parity, and flip. There are no off-by-one errors since we compute `k = r - l + 1` correctly for inclusive indices.

## Worked Examples

Sample Input 1:

```
3
1 2 3
2
1 2
2 3
```

| Step | Segment Length k | Pairs k*(k-1)/2 | Flip? | Parity | Output |
| --- | --- | --- | --- | --- | --- |
| Initial | - | - | - | 0 | - |
| Query 1 [1,2] | 2 | 1 | Yes | 1 | odd |
| Query 2 [2,3] | 2 | 1 | Yes | 0 | even |

This demonstrates the parity flips correctly for minimal segments.

Sample Input 2:

```
4
1 2 4 3
4
2 4
1 3
1 4
3 3
```

| Step | Segment Length k | Pairs k*(k-1)/2 | Flip? | Parity | Output |
| --- | --- | --- | --- | --- | --- |
| Initial | - | - | - | 1 | - |
| Query 1 [2,4] | 3 | 3 | Yes | 0 | even |
| Query 2 [1,3] | 3 | 3 | Yes | 1 | odd |
| Query 3 [1,4] | 4 | 6 | No | 1 | odd |
| Query 4 [3,3] | 1 | 0 | No | 1 | odd |

The table shows that single-element reversals do not affect parity and larger even-length reversals may not flip parity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2 + m) | Initial inversion parity takes O(n^2), each query is O(1) |
| Space | O(n) | Store the permutation array only |

With n ≤ 1500 and m ≤ 2·10^5, the O(n^2) initial step is roughly 2.25·10^6 operations, which is acceptable. Query processing in O(1) each is 2·10^5 operations, well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    n = int(input())
    a = list(map(int, input().split()))
    m = int(input())
    parity = 0
    for i in range(n):
        for j in range(i):
            if a[i] < a[j]:
                parity ^= 1
    for _ in range(m):
        l, r = map(int, input().split())
        k = r - l + 1
        if (k * (k - 1) // 2) % 2 == 1:
            parity ^= 1
        output.append("odd" if parity else "even")
    return "\n".join(output)

# provided samples
assert run("3\n1 2 3\n2\n1 2\n2 3\n") == "odd\neven", "sample 1"
assert run("4\n1 2 4 3\n4\n2 4\n1 3\n1 4\n3 3\n") == "even\nodd\nodd\nodd", "sample 2"

# custom cases
assert run("1\n1\n1\n1 1\n") == "even", "single element"
assert run("2\n2 1\n1\n1 2\n") == "even", "two element swap flips parity"
assert run("5\n5 4 3 2 1\n3\n1 5\n2 4\n3 3\n") == "even\nodd\nodd", "descending with mixed queries"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "1\n1\n1\n1 1\n" | even | Single element segment should not flip parity |
| "2\n2 1\n1\n1 2\n" | even | Two elements reversed flips parity from initial odd |
| "5\n5 4 3 2 1\n3\n1 5\n2 4\n3 3\n" | even, odd, odd | Large initial inversions, mixed-length |
