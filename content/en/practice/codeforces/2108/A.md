---
title: "CF 2108A - Permutation Warm-Up"
description: "We are given a permutation of the numbers from 1 to n, and we measure how far each element moves away from its original position. For each position i, we take the absolute difference between the value sitting there and i itself, and sum this over the entire array."
date: "2026-06-08T04:43:26+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2108
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1022 (Div. 2)"
rating: 800
weight: 2108
solve_time_s: 69
verified: true
draft: false
---

[CF 2108A - Permutation Warm-Up](https://codeforces.com/problemset/problem/2108/A)

**Rating:** 800  
**Tags:** combinatorics, greedy, math  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of the numbers from 1 to n, and we measure how far each element moves away from its original position. For each position i, we take the absolute difference between the value sitting there and i itself, and sum this over the entire array. This produces a single integer score for that permutation.

The task is not to compute this value for a single permutation, but to consider all possible permutations of length n and determine how many different total scores can appear.

The key object is not the permutations themselves but the set of achievable values of a distance-like measure. Each permutation rearranges the same multiset of integers, so the sum is constrained by how much displacement is possible globally.

The constraints allow n up to 500 with multiple test cases. Any solution that explicitly enumerates permutations is impossible because even for n = 10, the number of permutations is already 3,628,800. This rules out brute force generation entirely. The solution must rely on structural properties of how these absolute differences can vary.

A subtle edge case appears at very small n. When n = 1, there is only one permutation and the value is always 0, so the answer must be 1, not 0. When n = 2, only two values are possible, 0 and 2, which shows that the function does not necessarily produce consecutive integers but still forms a structured set.

## Approaches

A brute force idea is straightforward: generate every permutation, compute the sum of absolute differences, insert results into a set, and return its size. This is correct because it directly follows the definition. However, it requires iterating over n! permutations and computing an O(n) sum for each, leading to O(n · n!) operations. This becomes infeasible almost immediately beyond n = 10.

The crucial observation is that we are not studying permutations individually but the range of possible total displacement values. The expression ∑|p_i − i| is known as the total displacement or Spearman footrule distance from identity. A key structural fact is that swapping elements affects the sum in controlled increments, and the set of achievable values turns out to form all even numbers up to a maximum value, with some parity constraints depending on n.

More precisely, the minimum value is 0 (identity permutation), and the maximum value is achieved by reversing the array. Intermediate values can be obtained by gradually correcting the reversed permutation using swaps that adjust the total cost in predictable steps. The parity of the sum depends on whether n is even or odd, but regardless, the number of distinct values turns out to depend only on n and follows a simple quadratic expression in n.

The final closed form can be derived by analyzing how far we can move elements symmetrically. Each swap between positions contributes a controlled change in the sum, and the reachable set fills all integers of a certain parity range between 0 and the maximum value. Counting those values reduces to counting arithmetic progression lengths, which yields the final formula:

For even n:

the number of distinct values is n² / 4 + 1

For odd n:

the number of distinct values is (n² + 3) / 4

This simplifies to a unified expression:

⌊n² / 4⌋ + 1

Thus the problem reduces to a constant-time computation per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · n!) | O(n!) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read n for each test case. This defines the permutation size and determines the entire structure of possible values.
2. Compute n × n. This represents the scale of total displacement capacity, since each position contributes at most O(n) to the sum.
3. Divide this value by 4 using integer division. This corresponds to counting how many distinct “steps” fit into the full achievable range of values, which is symmetric around the identity permutation.
4. Add 1 to include the zero displacement permutation. This ensures the identity permutation’s value is counted.

Each step corresponds directly to compressing the structure of permutation distances into a single arithmetic range. The only non-trivial step is recognizing that the reachable values form a contiguous set within a parity class.

### Why it works

The function f(p) measures total displacement from the identity permutation. Swapping two elements changes the sum in a controlled and incremental way, and any permutation can be transformed into any other through a sequence of swaps. The key structural property is that these swaps allow us to realize every feasible total displacement within a fixed interval, but only stepping in increments consistent with parity constraints. As a result, the set of achievable values forms an arithmetic progression starting at 0, ending at the maximum displacement, and including exactly one parity class. Counting elements in this progression reduces to computing its length, which depends only on n.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    print(n * n // 4 + 1)
```

The code directly implements the derived closed form. The multiplication n * n is safe for n up to 500, since the result fits comfortably within Python integers. Integer division by 4 captures the density of achievable values in the range. The +1 accounts for the zero-value permutation.

The solution avoids any permutation construction and relies entirely on the structural result that the number of distinct values depends only on n.

## Worked Examples

### Example 1

Input:

n = 2

We evaluate all permutations:

| permutation | f(p) |
| --- | --- |
| [1, 2] | 0 |
| [2, 1] | 2 |

The distinct values are {0, 2}.

For n = 2, formula gives 2² // 4 + 1 = 1 + 1 = 2.

This confirms that even at minimal non-trivial size, the values are not contiguous integers but still follow the arithmetic structure.

### Example 2

Input:

n = 3

| permutation | f(p) |
| --- | --- |
| [1, 2, 3] | 0 |
| [1, 3, 2] | 2 |
| [2, 1, 3] | 2 |
| [2, 3, 1] | 4 |
| [3, 1, 2] | 4 |
| [3, 2, 1] | 4 |

Distinct values are {0, 2, 4}, so answer is 3.

Formula gives 9 // 4 + 1 = 2 + 1 = 3.

This shows that only even values appear and that the range is fully filled.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is a single arithmetic computation |
| Space | O(1) | No auxiliary structures beyond variables |

The computation is constant time per test case, which is easily within limits even for the maximum t = 100.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        out.append(str(n * n // 4 + 1))
    return "\n".join(out)

# provided samples
assert run("5\n2\n3\n8\n15\n43\n") == "2\n3\n17\n57\n463"

# minimum size
assert run("1\n1\n") == "1"

# small even/odd comparison
assert run("2\n2\n3\n") == "2\n3"

# larger boundary
assert run("1\n500\n") == str(500 * 500 // 4 + 1)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n = 1 | 1 | single permutation edge case |
| n = 2,3 | 2,3 | smallest non-trivial structure |
| n = 500 | 62501 | maximum constraint handling |

## Edge Cases

For n = 1, there is only one permutation. The algorithm computes 1 * 1 // 4 + 1 = 1, which correctly counts the only achievable value 0.

For n = 2, the computation gives 4 // 4 + 1 = 2. The two permutations produce values 0 and 2, matching the prediction.

For large n such as 500, the formula still applies directly without overflow issues in Python. The structure does not depend on enumeration or combinatorial generation, so performance remains constant.

These cases confirm that both minimal and maximal inputs are handled uniformly by the same arithmetic expression.
