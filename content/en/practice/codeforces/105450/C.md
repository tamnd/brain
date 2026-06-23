---
title: "CF 105450C - Sour Straws"
description: "We are given a collection of integer lengths, each representing a sour straw. From these, we want to choose a subset such that when we sort the chosen lengths in nondecreasing order, every smaller element divides every larger element that comes after it."
date: "2026-06-23T17:32:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105450
codeforces_index: "C"
codeforces_contest_name: "UTPC x WiCS Contest 10-25-24 (UT Internal)"
rating: 0
weight: 105450
solve_time_s: 82
verified: false
draft: false
---

[CF 105450C - Sour Straws](https://codeforces.com/problemset/problem/105450/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of integer lengths, each representing a sour straw. From these, we want to choose a subset such that when we sort the chosen lengths in nondecreasing order, every smaller element divides every larger element that comes after it.

In other words, inside the chosen subset, if we take any two elements, the smaller one must be a divisor of the larger one. The task is to find the maximum possible size of such a subset.

The input size is up to 1000 elements, and each value can be as large as 2 × 10^9. This immediately suggests that any solution with cubic behavior or anything involving repeated factorization per pair might be borderline but still potentially acceptable, while anything exponential over subsets is impossible.

A subtle edge case comes from repeated values. Equal values are always valid together because any number divides itself. Another edge case is when no two numbers divide each other, in which case the answer is just 1.

A naive mistake is to think this is a classic longest increasing subsequence problem and try to enforce only ordering, ignoring divisibility. That would fail on cases like [2, 3, 6], where ordering alone is not enough and divisibility structure matters.

## Approaches

The brute-force interpretation is to try every subset and check whether it satisfies the divisibility condition. For a subset of size k, checking validity requires examining all pairs or at least all consecutive pairs after sorting, which is O(k^2). Since there are 2^n subsets, this approach is completely infeasible, growing on the order of 2^1000.

A more structured approach is to recognize that the divisibility condition becomes much easier after sorting the array. Once sorted, the constraint reduces to building the longest chain where each element divides the next one. This turns the problem into a variant of longest path in a directed acyclic graph where edges go from i to j if i < j and l[j] is divisible by l[i].

From here, dynamic programming becomes natural. For each element, we compute the longest valid chain ending at that element. To compute transitions, we only need to consider earlier elements in sorted order that divide it.

The key observation is that divisibility is transitive in a way that supports chaining: if a divides b and b divides c, then a divides c. Sorting ensures we only extend from smaller or equal values to larger ones, which prevents invalid backward transitions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subsets | O(2^n · n) | O(n) | Too slow |
| DP over sorted array | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the list of lengths in nondecreasing order. This ensures that any valid subset can be arranged so that divisibility only needs to be checked forward.
2. Create a DP array where dp[i] represents the maximum size of a valid subset whose largest element is at position i in the sorted array.
3. Initialize every dp[i] to 1, since each element alone forms a valid subset.
4. For each index i from left to right, consider all earlier indices j < i. If l[i] is divisible by l[j], then we can extend any valid subset ending at j by adding l[i]. Update dp[i] = max(dp[i], dp[j] + 1). This step builds all valid chains ending at i.
5. The answer is the maximum value over all dp[i], since the best subset can end at any position.

Why it works comes from the fact that sorting removes the need to consider permutations of the subset. Every valid subset has a canonical form in sorted order, and the DP ensures that every possible last element is considered while preserving divisibility constraints along transitions. The DP state fully captures all valid chains ending at each index, so no optimal solution is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

a.sort()

dp = [1] * n

for i in range(n):
    for j in range(i):
        if a[i] % a[j] == 0:
            dp[i] = max(dp[i], dp[j] + 1)

print(max(dp))
```

The solution begins by sorting the array so that any potential subset can be interpreted as an increasing sequence where only forward divisibility checks are required. The dp array stores the best chain ending at each index. Each transition checks whether the current value can extend a previous valid chain, and the maximum over all dp values gives the final answer.

A common subtlety is handling duplicates. The condition `a[i] % a[j] == 0` naturally allows equal values since a number divides itself, so duplicates correctly chain together.

## Worked Examples

### Example 1

Input:

```
5
2 7 5 4 8
```

Sorted array becomes `[2, 4, 5, 7, 8]`.

| i | a[i] | j considered | valid extensions | dp[i] |
| --- | --- | --- | --- | --- |
| 0 | 2 | - | - | 1 |
| 1 | 4 | 0 | 2 → 4 | 2 |
| 2 | 5 | 0,1 | none | 1 |
| 3 | 7 | 0,1,2 | none | 1 |
| 4 | 8 | 0,1,2,3 | 2 → 8, 4 → 8 | 3 |

The best chain is `[2, 4, 8]`, which confirms the answer 3.

This trace shows how the DP naturally builds chains without needing to explicitly track subsets.

### Example 2

Input:

```
5
10 10 10 10 10
```

Sorted array remains `[10, 10, 10, 10, 10]`.

| i | a[i] | j considered | valid extensions | dp[i] |
| --- | --- | --- | --- | --- |
| 0 | 10 | - | - | 1 |
| 1 | 10 | 0 | 10 → 10 | 2 |
| 2 | 10 | 0,1 | all valid | 3 |
| 3 | 10 | 0,1,2 | all valid | 4 |
| 4 | 10 | 0,1,2,3 | all valid | 5 |

Every element can extend every previous one since equality satisfies divisibility. The DP correctly accumulates a full chain of length 5.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | For each i, we scan all j < i and perform constant-time divisibility checks |
| Space | O(n) | Only the dp array is stored |

With n up to 1000, an O(n^2) solution performs about 10^6 operations, which is well within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    a.sort()

    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if a[i] % a[j] == 0:
                dp[i] = max(dp[i], dp[j] + 1)

    return str(max(dp))

# provided samples
assert run("5\n2 7 5 4 8\n") == "3"
assert run("5\n10 10 10 10 10\n") == "5"

# custom cases
assert run("1\n42\n") == "1", "single element"
assert run("4\n2 3 5 7\n") == "1", "no divisibility"
assert run("4\n1 2 4 8\n") == "4", "perfect chain"
assert run("6\n3 6 7 14 28 2\n") == "4", "mixed chain structure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 1 | minimum size handling |
| primes | 1 | no valid extensions |
| powers of two | 4 | full chain growth |
| mixed | 4 | correct chaining across multiple branches |

## Edge Cases

For a single element input like `[42]`, the DP array is `[1]`, and the result is 1 since no transitions exist.

For `[2, 3, 5, 7]`, sorting does not create any divisibility relations. Every dp[i] stays 1 because no pair satisfies `a[i] % a[j] == 0`. The output correctly remains 1.

For a fully chainable case like `[1, 2, 4, 8]`, sorting keeps the order, and every element extends all previous ones since each divides the next. The DP builds `[1, 2, 3, 4]`, giving the final answer 4.
