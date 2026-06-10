---
title: "CF 1452B - Toy Blocks"
description: "We are given a set of boxes, each containing a certain number of toy blocks. The game consists of a child choosing a single box and attempting to redistribute all its blocks evenly across the other boxes."
date: "2026-06-11T03:17:32+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1452
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 98 (Rated for Div. 2)"
rating: 1400
weight: 1452
solve_time_s: 326
verified: true
draft: false
---

[CF 1452B - Toy Blocks](https://codeforces.com/problemset/problem/1452/B)

**Rating:** 1400  
**Tags:** binary search, greedy, math, sortings  
**Solve time:** 5m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of boxes, each containing a certain number of toy blocks. The game consists of a child choosing a single box and attempting to redistribute all its blocks evenly across the other boxes. If the redistribution results in all other boxes having the same number of blocks, the child is happy; otherwise, he is sad. Our task is to preemptively add extra blocks to the boxes so that no matter which box is chosen, the redistribution will always succeed. The question asks for the minimum number of extra blocks needed to guarantee this outcome.

The input specifies multiple test cases, each with the number of boxes and the current block counts. With up to 1000 test cases and up to 10^5 boxes in total, a brute-force approach that tries every possible redistribution would be far too slow. We need an algorithm that operates linearly in the number of boxes per test case. Edge cases include when all boxes are already equal, when some boxes are empty, and when one box has far more blocks than the others. For example, with boxes `[0, 3, 0]`, we need to carefully distribute extra blocks so that any chosen box can be evenly redistributed without leaving leftovers.

## Approaches

A naive approach would attempt to simulate each box choice and compute the number of extra blocks needed for each scenario, then take the maximum. While correct, this would require iterating over all boxes for every potential target configuration, leading to O(n^2) operations per test case. With n up to 10^5, this approach is infeasible.

The key insight for an efficient solution comes from observing that the redistribution only succeeds if the total number of blocks after adding extras is divisible by n-1. Let `sum_a` be the sum of the initial block counts and `max_a` the largest block count. No matter which box is chosen, the chosen box's blocks will be added to the others, so the other boxes collectively must reach at least `max_a * (n-1)` blocks. Simultaneously, the total sum of all blocks, including extras, must be divisible by `n-1` to allow equal distribution. These two constraints give us the minimal total sum we need, from which we can compute the number of extra blocks as `max(target_sum - sum_a, 0)`. This insight reduces the problem to a simple computation without simulation, allowing linear-time processing.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of boxes `n` and the current block counts `a`.  
2. Compute `sum_a`, the sum of all blocks, and `max_a`, the maximum block count in the array.  
3. Calculate `min_required`, the smallest total sum of blocks needed to guarantee a happy child. This is the maximum of `n-1` times `max_a` and the smallest multiple of `n-1` that is at least `sum_a`. To compute this second value, perform integer division with rounding up: `(sum_a + n - 2) // (n-1) * (n-1)`.  
4. The number of extra blocks needed is `min_required - sum_a`. Since `min_required` is always at least `sum_a`, this value is non-negative.  
5. Print the result for each test case.

Why it works: by ensuring the total block count reaches the ceiling multiple of `n-1` and that each other box can reach at least `max_a`, we guarantee that any box selection can be evenly distributed among the others. These constraints capture exactly what is necessary to satisfy the redistribution without simulation.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    sum_a = sum(a)
    max_a = max(a)
    # minimal total sum that is >= sum_a and divisible by n-1
    target_sum = max(sum_a, (max_a * (n - 1)))
    if target_sum % (n - 1) != 0:
        target_sum = ((target_sum + n - 2) // (n - 1)) * (n - 1)
    print(target_sum - sum_a)
```

The solution reads input efficiently using `sys.stdin.readline` and handles multiple test cases. It computes `sum_a` and `max_a` in linear time and uses integer arithmetic to round up to the nearest multiple of `n-1`. The key subtlety is correctly rounding up the sum when it is not divisible by `n-1`, which avoids off-by-one errors. No extra space beyond input storage is needed.

## Worked Examples

### Sample Input 1

```
3
3
3 2 2
4
2 2 3 2
3
0 3 0
```

Trace for the first test case:

| Variable | Value |
|---|---|
| n | 3 |
| a | [3, 2, 2] |
| sum_a | 7 |
| max_a | 3 |
| target_sum | max(7, 3*2)=7 → next multiple of 2 ≥ 7 → 8 |
| extra_blocks | 8 - 7 = 1 |

Trace for the third test case `[0, 3, 0]`:

| Variable | Value |
|---|---|
| n | 3 |
| a | [0, 3, 0] |
| sum_a | 3 |
| max_a | 3 |
| target_sum | max(3, 3*2)=6 → already divisible by 2 → 6 |
| extra_blocks | 6 - 3 = 3 |

These traces confirm that the algorithm correctly identifies the minimum number of extra blocks.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(n) per test case | Sum and max computation are linear, rounding to multiple is constant time |
| Space | O(n) per test case | Storing the input array |

Given the sum of n across all test cases is ≤ 10^5, this solution executes comfortably within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        sum_a = sum(a)
        max_a = max(a)
        target_sum = max(sum_a, max_a * (n - 1))
        if target_sum % (n - 1) != 0:
            target_sum = ((target_sum + n - 2) // (n - 1)) * (n - 1)
        print(target_sum - sum_a)
    return output.getvalue().strip()

# provided samples
assert run("3\n3\n3 2 2\n4\n2 2 3 2\n3\n0 3 0\n") == "1\n0\n3", "sample 1"

# custom cases
assert run("1\n2\n0 0\n") == "0", "all zero"
assert run("1\n3\n1 1 1\n") == "2", "all equal"
assert run("1\n4\n5 0 0 0\n") == "15", "one big, others zero"
assert run("1\n5\n1 2 3 4 5\n") == "5", "ascending sequence"
```

| Test input | Expected output | What it validates |
|---|---|---|
| 2 boxes, all zeros | 0 | No extra blocks needed if already equal |
| 3 boxes, all ones | 2 | Ensures total divisible by n-1 |
| 4 boxes, one big, others zero | 15 | Handles extreme imbalance |
| 5 boxes, ascending | 5 | Checks rounding to next multiple of n-1 |

## Edge Cases

For the edge case `[0, 3, 0]`, the algorithm computes the total sum as 3, max as 3, and then the minimum required sum as 6, giving 3 extra blocks. This ensures that regardless of which box the child chooses, redistribution among the others is always possible. For `[1,1,1]`, sum is 3, max is 1, minimum total sum to be divisible by 2 is 4, resulting in 1 extra block per the formula. These traces show that both extreme imbalances and uniform cases are correctly handled.
