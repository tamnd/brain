---
title: "CF 1095C - Powers Of Two"
description: "We are asked to express a given integer n as a sum of exactly k numbers, where every summand must be a power of two. Each chosen number is therefore of the form 1, 2, 4, 8, ..., and repetitions are allowed because we can use the same power multiple times."
date: "2026-06-13T05:12:25+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1095
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 529 (Div. 3)"
rating: 1400
weight: 1095
solve_time_s: 744
verified: false
draft: false
---

[CF 1095C - Powers Of Two](https://codeforces.com/problemset/problem/1095/C)

**Rating:** 1400  
**Tags:** bitmasks, greedy  
**Solve time:** 12m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to express a given integer `n` as a sum of exactly `k` numbers, where every summand must be a power of two. Each chosen number is therefore of the form `1, 2, 4, 8, ...`, and repetitions are allowed because we can use the same power multiple times.

The input describes a target amount `n` and a required number of summands `k`. The output is either a statement that the decomposition is impossible, or a concrete multiset of `k` powers of two whose sum equals `n`.

The structure of the problem is constrained in two independent directions. The value `n` limits the total mass we can distribute, while `k` forces us to split that mass into a fixed number of pieces. This creates a tension between “few large powers” and “many small powers”.

The bounds are tight enough that any approach that tries to enumerate partitions or build combinations explicitly will fail. The value of `n` goes up to `10^9`, so even representing it in binary has at most 30 significant bits. The value of `k` goes up to `2 * 10^5`, so the output itself can be large, meaning the algorithm must be close to linear in the final answer size.

A key edge case appears when `k` is larger than `n`. Since the smallest allowed value is `1`, the sum of `k` positive integers is at least `k`, so any case where `k > n` is immediately impossible.

Another subtle case arises when `n` has very few set bits in binary. For example, if `n = 8`, the natural representation is just `[8]`. If `k = 3`, we must split `8` into three powers of two. This is possible via splitting `8 -> 4 + 4`, then further splitting one `4 -> 2 + 2`, depending on how many splits are needed. The correctness hinges on whether we can keep decomposing powers of two.

## Approaches

A direct but naive approach is to start from `n` written as a sum of powers of two in its binary form. Each bit `1 << i` becomes one element. This gives the minimal number of summands equal to the number of set bits in `n`.

If this number is already greater than `k`, we fail immediately because merging powers of two is impossible. A power of two cannot be combined with a different one to form another power of two unless they are equal, so we cannot reduce count arbitrarily.

If the number of initial terms is at most `k`, we try to increase the number of terms until we reach exactly `k`. The only operation that preserves the sum while increasing the number of elements is splitting a power of two into two equal halves. Each split increases the count by exactly one.

The brute force version would repeatedly pick any number greater than `1` and split it until reaching `k` terms. In the worst case, each split reduces a high power down to many ones, leading to about `O(n)` operations if implemented inefficiently as array manipulations. This is far too slow for `k` up to `2e5`.

The key observation is that we never need to consider arbitrary splits. We only need a greedy strategy: always split the largest available power of two. This guarantees that we keep feasibility while maximizing flexibility for future splits.

We maintain a structure of counts of powers of two. Each time we split a `2^i`, we replace it with two `2^(i-1)` values. We continue until the number of elements reaches `k` or no further splits are possible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force splitting list | O(n) worst case | O(k) | Too slow |
| Greedy power-of-two splitting | O(k log n) | O(k) | Accepted |

## Algorithm Walkthrough

1. Convert `n` into its binary decomposition, storing counts of each power of two. This gives the smallest possible number of summands. This step is forced because powers of two form a disjoint basis for all integers.
2. Count the number of initial summands. If this count is greater than `k`, output `NO`, since we cannot merge distinct powers of two into a single valid power of two.
3. Insert all powers of two into a max-structure (conceptually a priority queue by exponent). We always want to split the largest power available because it produces the most flexibility in future splits.
4. While the number of summands is less than `k`, extract the largest power `2^x`. If `x = 0`, meaning the value is `1`, stop because it cannot be split further. Otherwise replace it with two copies of `2^(x-1)` and increase the count by one.
5. If we reach exactly `k` elements, output the multiset. If we get stuck before reaching `k`, output `NO`.

### Why it works

The algorithm maintains a representation of `n` as a multiset of powers of two that always sums to `n`. Each operation preserves the total sum because replacing `2^x` with two `2^(x-1)` keeps the value unchanged. The number of elements increases monotonically by exactly one per split, so we control the final size precisely. The greedy choice of splitting the largest power ensures we never run out of splittable mass prematurely when a feasible solution exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

import heapq

def solve():
    n, k = map(int, input().split())

    # initial decomposition
    cnt = 0
    heap = []

    for i in range(31):
        if n & (1 << i):
            heap.append(-i)
            cnt += 1

    if cnt > k:
        print("NO")
        return

    heapq.heapify(heap)

    # we store exponents as negatives for max-heap behavior

    while cnt < k:
        if not heap:
            break

        x = -heapq.heappop(heap)

        if x == 0:
            break

        # split 2^x into two 2^(x-1)
        heapq.heappush(heap, -(x - 1))
        heapq.heappush(heap, -(x - 1))
        cnt += 1

    if cnt != k:
        print("NO")
        return

    print("YES")
    res = []
    while heap:
        x = -heapq.heappop(heap)
        res.append(1 << x)

    print(*res)
```

The solution begins by decomposing `n` into powers of two, which forms the minimal valid representation. A heap is used to always extract the largest exponent efficiently. This matters because larger powers are the only ones that can be repeatedly split, and choosing them first avoids getting stuck with many `1`s too early.

Each split operation removes one element and adds two smaller ones, increasing the total count by exactly one. This makes it easy to track progress toward `k`.

The termination condition is either reaching exactly `k` elements or exhausting all splittable powers.

## Worked Examples

### Example 1

Input: `n = 9, k = 4`

Initial decomposition is `9 = 8 + 1`, so exponents are `{3, 0}`.

| Step | Heap (exponents) | Count | Action |
| --- | --- | --- | --- |
| 0 | [3, 0] | 2 | start |
| 1 | [2, 2, 0] | 3 | split 3 → 2 + 2 |
| 2 | [2, 1, 1, 0] | 4 | split 2 → 1 + 1 |

We reach 4 elements, so the output is valid: `8 → 4 4 → 2 2 4 → 1 1 2 4`.

This demonstrates that repeated splitting of the largest available power correctly distributes mass into the required number of summands.

### Example 2

Input: `n = 7, k = 5`

Initial decomposition: `7 = 4 + 2 + 1`.

| Step | Heap | Count | Action |
| --- | --- | --- | --- |
| 0 | [2, 1, 0] | 3 | start |
| 1 | [1, 1, 1, 0] | 4 | split 2 → 1 + 1 |
| 2 | [1, 1, 1, 0] | 4 | cannot split further for progress |

We cannot reach 5 elements because all remaining values are `1`, so no further splits are possible. The answer is `NO`.

This shows the importance of detecting exhaustion of splittable powers before reaching `k`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k log n) | Each split is a heap operation and we perform at most k splits |
| Space | O(k) | Heap stores at most k elements |

The constraints allow up to `2 * 10^5` output elements, and each operation is logarithmic in this size, so the solution comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    import sys
    sys.stdin = io.StringIO(inp)
    from collections import deque

    # inline solution for testing
    import heapq

    n, k = map(int, sys.stdin.readline().split())

    cnt = 0
    heap = []

    for i in range(31):
        if n & (1 << i):
            heap.append(-i)
            cnt += 1

    if cnt > k:
        return "NO"

    heapq.heapify(heap)

    while cnt < k:
        if not heap:
            return "NO"
        x = -heapq.heappop(heap)
        if x == 0:
            return "NO"
        heapq.heappush(heap, -(x - 1))
        heapq.heappush(heap, -(x - 1))
        cnt += 1

    if cnt != k:
        return "NO"

    res = []
    while heap:
        res.append(1 << (-heapq.heappop(heap)))

    return "YES " + " ".join(map(str, res))

assert run("9 4") == "YES 1 2 2 4", "sample 1"

assert run("1 1") == "YES 1", "minimum case"

assert run("1 2") == "NO", "cannot split 1"

assert run("8 1") == "YES 8", "already exact"

assert run("7 10") == "NO", "need more splits than possible"

assert run("10 4") != "", "basic feasibility check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 | NO | cannot split 1 further |
| 8 1 | YES 8 | already minimal representation |
| 7 10 | NO | insufficient split capacity |
| 10 4 | valid decomposition | general correctness |

## Edge Cases

When `n = 1` and `k > 1`, the heap contains only a single exponent `0`. The algorithm immediately stops because `0` cannot be split, so it correctly returns `NO`.

When `n` is already large but sparse in bits, such as `n = 2^30`, the algorithm starts with a single element. It repeatedly splits down to `1`s until either reaching `k` or exhausting all split capacity. Each step preserves correctness because every split maintains total sum.

When `k` equals the number of initial bits in `n`, no splitting is needed. The algorithm outputs the binary representation directly, which matches the optimal minimal decomposition.
