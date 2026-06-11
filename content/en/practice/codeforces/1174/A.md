---
title: "CF 1174A - Ehab Fails to Be Thanos"
description: "We are given an array of length 2n, and the task is to reorder it such that the sum of the first n elements differs from the sum of the last n elements. The input provides n and the array values, each between 1 and 10^6."
date: "2026-06-12T01:51:46+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1174
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 563 (Div. 2)"
rating: 1000
weight: 1174
solve_time_s: 108
verified: false
draft: false
---

[CF 1174A - Ehab Fails to Be Thanos](https://codeforces.com/problemset/problem/1174/A)

**Rating:** 1000  
**Tags:** constructive algorithms, greedy, sortings  
**Solve time:** 1m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of length `2n`, and the task is to reorder it such that the sum of the first `n` elements differs from the sum of the last `n` elements. The input provides `n` and the array values, each between `1` and `10^6`. The output is either a valid permutation of the array satisfying the condition or `-1` if no such permutation exists.

The constraints imply that `n` is up to 1000, making the total array length at most 2000. This is small enough to allow sorting or linear scans without concern for time limits. The primary challenge is not performance but finding a permutation that guarantees the sums are unequal.

A key edge case occurs when all array elements are identical. For instance, if `n = 2` and the array is `[5, 5, 5, 5]`, any split into two halves will have equal sums, and the answer must be `-1`. Another subtle case is arrays where the total sum can be split equally in multiple ways, but since we can reorder arbitrarily, a simple heuristic can break symmetry.

## Approaches

The brute-force approach is to generate all `2n!` permutations and check each one by computing the sums of the first and last halves. This is obviously impractical because even for `n = 10`, the number of permutations exceeds `10^7`.

The observation that unlocks a fast solution is that if we sort the array and the first and last elements are not equal, then the sum of the first `n` elements and the sum of the last `n` elements cannot be identical. Sorting separates smaller and larger numbers, ensuring imbalance unless all numbers are equal. This reduces the problem to checking whether all elements are the same. If they are, output `-1`. Otherwise, sort the array and print it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((2n)!) | O(2n) | Too slow |
| Sort & Check | O(n log n) | O(2n) | Accepted |

## Algorithm Walkthrough

1. Read integer `n` and array `a` of length `2n`.
2. Check if all elements in `a` are equal. If true, print `-1` and terminate because no reordering can create unequal sums.
3. Sort the array in non-decreasing order. Sorting ensures that the smallest `n` numbers are in the first half and the largest `n` numbers are in the second half, creating a sum imbalance.
4. Print the sorted array as the valid permutation.

The algorithm works because sorting produces an ordering where the first half is not equal to the second half unless all elements are identical. The invariant is that after sorting, the sum of the first half is strictly less than the sum of the second half unless all values are equal. Checking for equality first ensures we do not produce a false solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

if all(x == a[0] for x in a):
    print(-1)
else:
    a.sort()
    print(' '.join(map(str, a)))
```

The code first reads `n` and the array `a`. The `all` check efficiently determines if all elements are identical. Sorting produces a guaranteed solution in O(n log n). Joining the array into a string ensures correct formatting without extra spaces.

## Worked Examples

### Sample 1

Input:

```
3
1 2 2 1 3 1
```

| Step | a (state) | Reason |
| --- | --- | --- |
| Read input | [1, 2, 2, 1, 3, 1] | initial array |
| Check all equal | False | array has different values |
| Sort | [1, 1, 1, 2, 2, 3] | smallest in first half, largest in second |
| Output | 1 1 1 2 2 3 | sums: first half 3, second half 7 |

This demonstrates that sorting separates sums automatically.

### Sample 2

Input:

```
2
5 5 5 5
```

| Step | a (state) | Reason |
| --- | --- | --- |
| Read input | [5, 5, 5, 5] | initial array |
| Check all equal | True | no permutation can create unequal sums |
| Output | -1 | correct |

This confirms the edge case handling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates, linear scans negligible |
| Space | O(2n) | array storage, no extra structures |

With n ≤ 1000, sorting 2000 elements is trivial. Memory usage is well under the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    if all(x == a[0] for x in a):
        return "-1"
    else:
        a.sort()
        return ' '.join(map(str, a))

# Provided samples
assert run("3\n1 2 2 1 3 1\n") == "1 1 1 2 2 3"
assert run("2\n5 5 5 5\n") == "-1"

# Custom cases
assert run("1\n42 17\n") == "17 42", "minimum size n=1"
assert run("2\n1 2 3 4\n") == "1 2 3 4", "already sorted, sums differ"
assert run("3\n7 7 7 7 7 8\n") == "7 7 7 7 7 8", "one distinct value breaks equality"
assert run("2\n2 2 1 3\n") == "1 2 2 3", "reordering required"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 42 17 | 17 42 | minimum n=1, simple swap |
| 2 1 2 3 4 | 1 2 3 4 | already valid sorted array |
| 3 7 7 7 7 7 8 | 7 7 7 7 7 8 | one distinct value creates imbalance |
| 2 2 2 1 3 | 1 2 2 3 | requires reordering |

## Edge Cases

All-equal input: `2 5 5 5 5`. The algorithm detects uniformity and returns `-1`. Sorting is skipped to avoid invalid output.

Minimum `n = 1`: `1 42 17`. Sorting the two elements ensures sums differ, and the algorithm outputs `17 42`.

Already sorted input: `2 1 2 3 4`. The algorithm preserves order, demonstrating no unnecessary modifications occur when the array already satisfies the sum condition.

One distinct value amon
