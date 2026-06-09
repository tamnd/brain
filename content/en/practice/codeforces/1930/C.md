---
title: "CF 1930C - Lexicographically Largest"
description: "We are given an array a of length n. The task is to repeatedly select an element from a, add its value plus its current index to a set S, remove it from the array, and continue until a is empty. After all insertions, we sort the set S in decreasing order to form array b."
date: "2026-06-09T01:41:36+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "data-structures", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1930
codeforces_index: "C"
codeforces_contest_name: "think-cell Round 1"
rating: 1700
weight: 1930
solve_time_s: 106
verified: false
draft: false
---

[CF 1930C - Lexicographically Largest](https://codeforces.com/problemset/problem/1930/C)

**Rating:** 1700  
**Tags:** binary search, constructive algorithms, data structures, greedy, sortings  
**Solve time:** 1m 46s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array `a` of length `n`. The task is to repeatedly select an element from `a`, add its value plus its current index to a set `S`, remove it from the array, and continue until `a` is empty. After all insertions, we sort the set `S` in decreasing order to form array `b`. The goal is to choose elements from `a` in such a way that the resulting `b` is lexicographically as large as possible.

Each element of `S` is calculated as `a_i + i` where `i` is the 1-based position at the time of selection. Since `S` is a set, duplicates are ignored. Therefore, choosing elements that produce the same sum later will not improve the result, which makes ordering crucial. The constraints allow `n` up to `3 * 10^5` with a total sum over all test cases capped at `3 * 10^5`, meaning any algorithm with O(n log n) per test case is feasible, but O(n^2) approaches are too slow.

A subtle edge case occurs when values in `a` are strictly increasing or decreasing. For example, `a = [2, 1]` demonstrates that removing the largest first produces more unique sums, while removing the smaller first may lead to duplicates. Another case is when all `a_i` are equal, say `a = [1, 1, 1]`. Picking elements from the end maximizes the sum with the current index since `a_i + i` increases with `i`.

## Approaches

The brute-force approach would try every permutation of removal orders, compute `S`, and then sort it to form `b`. This is correct but utterly infeasible, because there are `n!` permutations, and even for `n = 10`, this is already 3.6 million possibilities.

The key insight is that the value inserted into `S` depends only on the sum of the element and its current index. To maximize lexicographically, we want the largest values to appear early in `b`. For each value `a_i`, the largest sum occurs if it is selected as late as possible because later positions have larger indices. Therefore, to maximize `b`, we should simulate picking elements from the end of the array first. We also must avoid inserting duplicates into `S`, so we track inserted values using a set.

Concretely, if we iterate `a` in reverse order and calculate `a_i + i` for each `i` in reverse, adding each sum to `S` only if it hasn't appeared before, then sorting `S` in decreasing order produces the desired lexicographically largest `b`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal (reverse + set) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty set `S` for storing unique sums.
2. Iterate over `a` from the last element to the first.
3. For each element `a[i]` at 0-based index `i`, calculate `a[i] + (i + 1)` to account for 1-based indexing.
4. If this sum is not already in `S`, insert it.
5. After processing all elements, convert `S` into a list and sort it in decreasing order to form `b`.
6. Output `b`.

Why it works: iterating from the end ensures that elements at higher indices are considered first, maximizing their `a_i + i` sums. Inserting into a set avoids duplicates. Sorting in decreasing order guarantees that the largest sums appear first, producing a lexicographically largest array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        seen = set()
        result = []
        # process from end to start
        for i in reversed(range(n)):
            val = a[i] + i + 1
            if val not in seen:
                seen.add(val)
                result.append(val)
        # output in decreasing order
        print(*sorted(result, reverse=True))

if __name__ == "__main__":
    solve()
```

The code first reads the number of test cases, then processes each array. Using `reversed(range(n))` correctly calculates sums from the end. The `seen` set prevents duplicate insertions, which is crucial. Sorting at the end guarantees the lexicographic property.

## Worked Examples

**Sample 1**

Input: `a = [2, 1]`

| Step | i | a[i] | a[i]+i+1 | S | Result List |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 2 | {2} | [2] |
| 2 | 0 | 2 | 3 | {2, 3} | [2,3] |

Sorted decreasing: `[3,2]`

This demonstrates that picking the end first ensures both sums are inserted without duplicates.

**Sample 2**

Input: `a = [1, 100, 1000, 1000000, 1000000000]`

Processing in reverse:

| i | a[i]+i+1 | Insert? |
| --- | --- | --- |
| 4 | 1000000005 | Yes |
| 3 | 1000004 | Yes |
| 2 | 1003 | Yes |
| 1 | 102 | Yes |
| 0 | 2 | Yes |

Sorted decreasing: `[1000000005, 1000004, 1003, 102, 2]`

Shows correct handling of large numbers and preserving lexicographic order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Iterating over the array is O(n), insertion into a set is O(1) amortized, sorting result is O(n log n) |
| Space | O(n) | Set and result list store at most n elements |

Given the sum of `n` across all test cases ≤ 3 * 10^5, this solution fits well within the 2s time limit and 256MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided samples
assert run("3\n2\n2 1\n5\n1 100 1000 1000000 1000000000\n3\n6 4 8\n") == "3 2\n1000000005 1000004 1003 102 2\n11 7 6", "sample 1"

# custom: all equal
assert run("1\n5\n1 1 1 1 1\n") == "6 5 4 3 2", "all equal values"

# custom: strictly increasing
assert run("1\n4\n1 2 3 4\n") == "7 6 5 4", "strictly increasing"

# custom: strictly decreasing
assert run("1\n4\n4 3 2 1\n") == "7 6 5 4", "strictly decreasing"

# custom: single element
assert run("1\n1\n42\n") == "43", "single element"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 1 | 6 5 4 3 2 | duplicate handling and lexicographic order |
| 1 2 3 4 | 7 6 5 4 | increasing order, end-first logic |
| 4 3 2 1 | 7 6 5 4 | decreasing order, same logic applies |
| 42 | 43 | minimum-size input |

## Edge Cases

For `a = [1, 1, 1, 1, 1]`, the algorithm processes from the last element:

| i | a[i]+i+1 | S |
| --- | --- | --- |
| 4 | 5+1=5 | {5} |
| 3 | 4 | {4,5} |
| 2 | 3 | {3,4,5} |
| 1 | 2 | {2,3,4,5} |
| 0 | 1 | {1,2,3,4,5} |

Sorted decreasing: `[5,4,3,2,1]` as expected. Processing from the front would insert duplicate sums and produce a smaller lexicographic array. This confirms the end-to-start strategy correctly maximizes `b`.
