---
title: "CF 1405A - Permutation Forgery"
description: "We are asked to manipulate permutations of integers from 1 to n. Each permutation has a “fingerprint,” which is the sorted list of sums of every pair of consecutive elements."
date: "2026-06-11T08:04:26+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1405
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 668 (Div. 2)"
rating: 800
weight: 1405
solve_time_s: 114
verified: false
draft: false
---

[CF 1405A - Permutation Forgery](https://codeforces.com/problemset/problem/1405/A)

**Rating:** 800  
**Tags:** constructive algorithms  
**Solve time:** 1m 54s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to manipulate permutations of integers from 1 to n. Each permutation has a “fingerprint,” which is the sorted list of sums of every pair of consecutive elements. The task is to take a given permutation and produce another, different permutation with the same fingerprint. The permutations must remain valid, meaning all integers from 1 to n appear exactly once.

The input consists of multiple test cases. Each test case provides the length of the permutation and the permutation itself. The output is a permutation for each test case that differs from the input but has the same fingerprint. The constraints are modest: n is at most 100 and the number of test cases is at most 668. These limits indicate that an algorithm with quadratic or even slightly worse complexity per test case will run efficiently, since 100² is only 10,000 operations per case, and 668×10,000 is well under 10 million operations overall.

A subtle point arises with very small permutations. For n = 2, the only permutation different from [1, 2] is [2, 1], but that’s still valid because it produces the same sum for its only pair. For n > 2, the input permutation may be sorted, reversed, or random, but we need a guaranteed systematic way to produce a different permutation without violating the fingerprint property.

## Approaches

A brute-force approach would try all n! permutations of length n and compute the fingerprint for each, checking if it matches the original. This is correct in principle, but completely impractical. For n = 10, that’s 3,628,800 possibilities; for n = 100, n! is astronomically large. Even with n = 8, the number of checks would be too high to run multiple test cases efficiently.

The key insight is that the fingerprint depends only on the sums of adjacent elements. Reversing the permutation preserves every adjacent sum, just in a different order. For example, the sums of [a, b, c, d] are [a+b, b+c, c+d], and for [d, c, b, a] they become [d+c, c+b, b+a], which contains exactly the same numbers, possibly in a different order. Since the fingerprint is sorted, the order does not matter. Reversing any permutation of length at least 2 guarantees a different permutation with the same fingerprint.

This observation reduces the problem from factorial complexity to linear time. We simply read the permutation, reverse it, and output it. This handles all sizes n ≥ 2, respects the constraints, and is trivial to implement.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Reverse Permutation | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases t. This defines how many permutations we need to process.
2. For each test case, read the integer n and the permutation p of length n.
3. Reverse the array p to produce a new permutation p'. This works because reversing preserves all adjacent sums in some order, which is sufficient for the sorted fingerprint.
4. Output the reversed permutation. No additional checks are necessary, as n ≥ 2 guarantees that the reversed permutation is different from the original.

Why it works: Reversing preserves every sum of adjacent elements in the permutation. The sorting step in the fingerprint removes order sensitivity, so the fingerprint of the reversed array matches the original. For n ≥ 2, the reversal is always different from the original permutation, satisfying the distinctness condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    p = list(map(int, input().split()))
    p.reverse()
    print(" ".join(map(str, p)))
```

The solution reads input efficiently using `sys.stdin.readline` and processes multiple test cases. The permutation is reversed in place using `list.reverse()`, which avoids extra memory allocation. Finally, the reversed list is printed space-separated. Off-by-one errors are avoided because `reverse()` handles the full array and the join operation correctly converts integers to strings.

## Worked Examples

For the first sample input:

| Step | p | Action | Output |
| --- | --- | --- | --- |
| 1 | [1, 2] | Reverse | [2, 1] |
| 2 | Compute F(p') implicitly | [2+1] = [3] | Matches original |

The algorithm successfully produces [2, 1], fingerprint [3], different from input.

For the second sample input:

| Step | p | Action | Output |
| --- | --- | --- | --- |
| 1 | [2, 1, 6, 5, 4, 3] | Reverse | [3, 4, 5, 6, 1, 2] |
| 2 | Compute F(p') implicitly | [3+4,4+5,5+6,6+1,1+2] = [7,9,11,7,3] | Sorted: [3,7,7,9,11] |

The fingerprint matches the original. Reversal guarantees distinctness.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n) | Each reversal and output takes linear time per test case. |
| Space | O(n) | Storing the permutation array and its reversed version. |

The constraints t ≤ 668 and n ≤ 100 ensure at most 66,800 operations, well within the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        p.reverse()
        print(" ".join(map(str, p)))
    return out.getvalue().strip()

# Provided samples
assert run("3\n2\n1 2\n6\n2 1 6 5 4 3\n5\n2 4 3 1 5\n") == "2 1\n3 4 5 6 1 2\n5 1 3 4 2", "samples"

# Custom test cases
assert run("1\n2\n2 1\n") == "1 2", "minimum n=2"
assert run("1\n3\n1 2 3\n") == "3 2 1", "small n=3"
assert run("1\n4\n4 3 2 1\n") == "1 2 3 4", "reversed sorted"
assert run("1\n5\n5 4 3 2 1\n") == "1 2 3 4 5", "max n=5 small test"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n2\n1 2 | 2 1 | Minimum permutation length |
| 3\n1 2 3 | 3 2 1 | Small permutation, reversal correctness |
| 4\n4 3 2 1 | 1 2 3 4 | Already reversed, ensures output differs |
| 5\n5 4 3 2 1 | 1 2 3 4 5 | Moderate size reversal |

## Edge Cases

For n = 2, the input [1,2] is reversed to [2,1]. The fingerprint [3] is identical, and the permutation is different, satisfying the problem requirements. For a larger, sorted permutation like [1,2,3,4,5], the reversal [5,4,3,2,1] produces the same sorted fingerprint [3,5,7,9] and differs from the original. In all cases, reversing is sufficient to satisfy both the fingerprint and distinctness constraints.
