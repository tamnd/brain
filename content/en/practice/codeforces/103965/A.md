---
title: "CF 103965A - Mood Balance"
description: "We are given a sequence of integers. Think of them as daily “changes” to some running value that starts at zero. As we go from left to right, we maintain a running sum. Each element either increases or decreases this running sum."
date: "2026-07-02T06:34:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103965
codeforces_index: "A"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2022-2023, \u041f\u0435\u0440\u0432\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 103965
solve_time_s: 37
verified: true
draft: false
---

[CF 103965A - Mood Balance](https://codeforces.com/problemset/problem/103965/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers. Think of them as daily “changes” to some running value that starts at zero. As we go from left to right, we maintain a running sum. Each element either increases or decreases this running sum.

The task is to determine the highest value this running sum ever reaches while processing the array from left to right.

So if the array is interpreted as increments and decrements of a score, we are asked: what is the maximum score achieved at any prefix boundary.

The output is a single integer: the maximum prefix sum over the whole array.

The constraints in this problem are not large enough to require anything beyond a single linear scan. That already rules out any solution that tries to recompute prefix sums repeatedly or uses nested loops, because those would turn into quadratic behavior and are unnecessary.

A subtle edge case appears when all values are negative. In that case, the running sum starts at zero and never improves, so the answer should remain zero. Any solution that assumes at least one positive prefix increase will fail here. For example, input `[-3, -2, -5]` must produce `0`, not `-3`.

Another edge case is when the maximum prefix sum occurs at the first element. For example `[5, -10, 1]` should return `5`. A naive implementation that only checks after full accumulation or forgets to consider intermediate prefixes can miss this.

## Approaches

A brute-force approach would compute the sum of every prefix separately and take the maximum. For each index i, we sum from 0 to i. This works correctly because it directly follows the definition of prefix sums. However, recomputing the sum for each prefix leads to a total of roughly n + (n-1) + ... + 1 operations, which is O(n²). With typical constraints up to 10^5, this becomes far too slow.

The key observation is that prefix sums are incremental. Instead of recomputing from scratch, we can maintain a running sum while scanning the array once. Each new element updates the current sum, and we immediately compare it with the best value seen so far. This reduces the problem from repeated recomputation to a single pass accumulation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force prefix recomputation | O(n²) | O(1) | Too slow |
| Single pass running sum | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start with two variables: `current_sum = 0` and `best = 0`. The initial best is zero because we are allowed to consider the starting state before any element is applied.
2. Iterate through the array from left to right. At each position, add the current element to `current_sum`. This simulates applying the next “mood change” or “increment”.
3. After updating `current_sum`, compare it with `best`. If `current_sum` is larger, replace `best` with it. This step ensures we always remember the highest prefix value encountered so far.
4. Continue until the end of the array. The final value of `best` is the answer.

### Why it works

The running sum at position i is exactly the prefix sum of the first i elements. Every possible prefix sum is evaluated exactly once during the scan. Since the maximum of a set is preserved under incremental comparison, tracking the maximum seen so far guarantees that no candidate prefix is missed. There is no dependence between non-adjacent prefixes beyond the accumulated sum, so no additional structure is required.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

current_sum = 0
best = 0

for x in a:
    current_sum += x
    if current_sum > best:
        best = current_sum

print(best)
```

The implementation is a direct translation of the scan described above. The only subtle decision is initializing `best` to zero rather than negative infinity. This reflects that the running sum starts before any elements are taken, so the empty prefix is valid.

## Worked Examples

### Example 1

Input:

`[1, -2, 3]`

| Step | Element | Current Sum | Best |
| --- | --- | --- | --- |
| 0 | start | 0 | 0 |
| 1 | 1 | 1 | 1 |
| 2 | -2 | -1 | 1 |
| 3 | 3 | 2 | 2 |

This demonstrates how the maximum can occur after a later positive rebound, not necessarily at the beginning.

### Example 2

Input:

`[-1, -2, -3]`

| Step | Element | Current Sum | Best |
| --- | --- | --- | --- |
| 0 | start | 0 | 0 |
| 1 | -1 | -1 | 0 |
| 2 | -2 | -3 | 0 |
| 3 | -3 | -6 | 0 |

This confirms that the algorithm correctly preserves zero when all prefixes decrease.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once with constant-time updates |
| Space | O(1) | Only two running variables are maintained |

The linear scan is optimal because every element must be read at least once, and no additional structure is required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    current_sum = 0
    best = 0
    for x in a:
        current_sum += x
        best = max(best, current_sum)
    return str(best)

# provided samples (illustrative)
assert run("3\n1 -2 3\n") == "2"

# all negative
assert run("3\n-1 -2 -3\n") == "0"

# all positive
assert run("4\n1 2 3 4\n") == "10"

# alternating
assert run("5\n1 -1 1 -1 1\n") == "1"

# single element
assert run("1\n5\n") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all negative | 0 | empty-prefix handling |
| all positive | sum | full accumulation correctness |
| alternating | 1 | correct intermediate max |
| single element | value itself | boundary condition |

## Edge Cases

For an input consisting entirely of negative numbers, the running sum continuously decreases. Since the algorithm always compares against zero initialized best, it correctly returns zero. For example `[-4, -2, -7]` produces `0` because no prefix exceeds the empty prefix.

For a single-element array, the first update immediately sets both current and best to that value if it is positive, or keeps best at zero if negative. This matches the idea that we always compare against the starting state before processing any elements.
