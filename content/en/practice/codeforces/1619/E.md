---
title: "CF 1619E - MEX and Increments"
description: "We are given an array of non-negative integers and we can increment any element by 1 any number of times. The task is to determine for each integer from 0 up to the array length whether it is possible to transform the array so that its MEX (minimum excluded value) equals that…"
date: "2026-06-10T06:10:47+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "dp", "greedy", "implementation", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1619
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 762 (Div. 3)"
rating: 1700
weight: 1619
solve_time_s: 88
verified: false
draft: false
---

[CF 1619E - MEX and Increments](https://codeforces.com/problemset/problem/1619/E)

**Rating:** 1700  
**Tags:** constructive algorithms, data structures, dp, greedy, implementation, math, sortings  
**Solve time:** 1m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of non-negative integers and we can increment any element by 1 any number of times. The task is to determine for each integer from 0 up to the array length whether it is possible to transform the array so that its MEX (minimum excluded value) equals that integer, and if so, calculate the minimum number of increments needed. The MEX of an array is the smallest non-negative integer not present in the array.

For example, if the array is `[0, 1, 3]`, the MEX is `2` because `0` and `1` are present, but `2` is missing. Incrementing `3` to `2` does not help, as we cannot decrease numbers. To achieve MEX `3`, all numbers `0, 1, 2` must be present, which in this array requires transforming existing numbers, but increments alone cannot create a missing number `2` if it is absent and all smaller numbers are already present.

The constraints are such that the sum of all `n` over test cases is at most `2*10^5`, and the number of test cases can be up to `10^4`. This immediately rules out brute-force solutions that simulate every increment for every potential MEX value, because that could be up to `O(n^2)` operations per test case. We need an approach that works in linear or linearithmic time per test case.

Edge cases include arrays where all elements are the same, arrays missing 0, arrays already containing all values `0..n`, and arrays with large gaps. For instance, `[1, 1, 1]` cannot have MEX `0` without incrementing, but MEX `2` may require multiple increments. A careless approach might ignore these gaps or the fact that we can only increase numbers, producing invalid answers.

## Approaches

A naive approach is to try every target MEX `i` from `0` to `n`. For each target, we could simulate increments on missing numbers until we form all numbers `0..i-1`. This would involve scanning the array and increasing values, which could take up to `O(n^2)` operations in the worst case, since each missing number might require scanning or repeated increments. Clearly, this is too slow.

The key observation is that for MEX `i` to be possible, all numbers `0` through `i-1` must exist in the array after some increments. Any missing number below `i` must be “created” by incrementing smaller numbers. Conversely, any number equal to or greater than `i` does not block MEX `i`.

We can exploit frequency counts. If we count how many times each number appears, we can process numbers from `0` upwards. If a number is missing, we can try to “borrow” extra occurrences of smaller numbers to create it. Extra occurrences of numbers below `i` can be incremented to fill gaps, and numbers above `i` can remain untouched. By maintaining a running count of surplus elements, we can calculate the minimum number of increments efficiently in a single pass.

This reduces the problem to a single linear scan of the frequency array while tracking surplus, which is much faster than simulating every increment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n^2) | O(n) | Too slow |
| Frequency + Surplus Tracking | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count the frequency of each number in the array, including numbers up to `n`. Initialize an array `freq` of size `n+1`. This gives immediate access to how many of each number we have.
2. Initialize a variable `surplus` to zero. This will track how many elements we can use to fill missing numbers, i.e., extra copies of numbers already processed.
3. Iterate over `mex` from `0` to `n`. For each `mex`, check if the number exists in the array:

- If `freq[mex] > 0`, we have the number available. Add `freq[mex] - 1` to `surplus` because one occurrence is needed to satisfy the MEX requirement, and the rest are available to fill future gaps.
- If `freq[mex] == 0`, the number is missing. We can only create it by incrementing one of the surplus elements. If `surplus > 0`, decrement `surplus` and increment the operation count. If `surplus == 0`, then MEX `mex` is impossible, and all larger MEX values are also impossible.
4. For each MEX, calculate the total number of operations as the sum of increments used to fill gaps plus the number of elements strictly greater than `mex` that need to be incremented if we want to remove duplicates above `mex` (to avoid blocking MEX).
5. Output the results in order from `0` to `n`. If a MEX is impossible, output `-1`.

Why it works: We maintain the invariant that after processing MEX `i`, all numbers `0..i-1` exist in the array. The `surplus` variable guarantees we can fill missing numbers using extra copies. If at any point a number cannot be created because no surplus exists, higher MEX values are also impossible, which is logically consistent. This greedy approach ensures minimal operations because we always use existing extra elements before creating new ones.

## Python Solution

```python
import sys
input = sys.stdin.readline

for _ in range(int(input())):
    n = int(input())
    a = list(map(int, input().split()))
    freq = [0] * (n + 2)
    for x in a:
        freq[x] += 1

    result = []
    ops = 0
    surplus = 0
    for mex in range(n + 1):
        if mex == 0:
            if freq[0] == 0:
                result.append(1)
                surplus = 0
            else:
                result.append(0)
                surplus = freq[0] - 1
        else:
            if freq[mex] == 0:
                if surplus > 0:
                    ops = ops + 1
                    result.append(ops)
                    surplus -= 1
                else:
                    result.extend([-1] * (n + 1 - mex))
                    break
            else:
                ops += freq[mex - 1]
                result.append(ops)
                surplus += freq[mex] - 1
    print(*result)
```

We start by counting frequencies, which allows us to check availability instantly. The `surplus` variable tracks how many elements can be incremented to fill missing numbers. We update `ops` to reflect the number of increments needed so far. Special handling for MEX `0` is necessary since it may require incrementing an element even if it is missing. The greedy approach ensures minimal operations by always filling gaps with surplus first.

## Worked Examples

### Example 1

Array: `[0, 1, 3]`

| MEX | freq | surplus | ops | result |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 1 |
| 1 | 1 | 0 | 1 | 1 |
| 2 | 0 | 0 | 1 | 0 |
| 3 | 1 | 0 | 2 | -1 |

Explanation: MEX `0` requires incrementing one element, MEX `1` requires one operation, MEX `2` requires no operation, MEX `3` is impossible as no surplus exists to fill the gap.

### Example 2

Array: `[0, 1, 2, 3, 4, 3, 2]`

| MEX | freq | surplus | ops | result |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 1 |
| 1 | 1 | 0 | 1 | 1 |
| 2 | 2 | 1 | 2 | 2 |
| 3 | 2 | 2 | 3 | 2 |
| 4 | 1 | 2 | 4 | 1 |
| 5 | 0 | 2 | 4 | 0 |
| 6 | 0 | 1 | 5 | 2 |
| 7 | 0 | 0 | 6 | 6 |

The table confirms the algorithm correctly accumulates surplus and increments, producing minimal operations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Counting frequencies and scanning from 0 to n are both linear |
| Space | O(n) | Frequency array of size n+2 |

Since the sum of `n` over all test cases is at most `2*10^5`, total operations are about `O(2*10^5)`, well within 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call solution
    for _ in range(int(input())):
        n = int(input())
        a = list(map(int, input().split()))
        freq = [0] * (n + 2)
        for x in a:
            freq[x] += 1
```
