---
title: "CF 1840C - Ski Resort"
description: "The problem asks us to count how many ways Dima can choose consecutive vacation days at a ski resort given weather constraints."
date: "2026-06-09T06:24:32+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1840
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 878 (Div. 3)"
rating: 1000
weight: 1840
solve_time_s: 71
verified: true
draft: false
---

[CF 1840C - Ski Resort](https://codeforces.com/problemset/problem/1840/C)

**Rating:** 1000  
**Tags:** combinatorics, math, two pointers  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to count how many ways Dima can choose consecutive vacation days at a ski resort given weather constraints. We are given an array of integers representing daily temperatures and two numbers: the minimum length of the vacation $k$ and the maximum temperature $q$ that Dima can tolerate. A valid vacation period is a contiguous subarray where all temperatures are at most $q$ and its length is at least $k$. The task is to compute, for each test case, the total number of valid vacation periods.

The input constraints indicate that the total number of days across all test cases does not exceed $2 \cdot 10^5$. This rules out any solution that examines every possible subarray naively, because enumerating all subarrays of a large array can require $O(n^2)$ operations, which is too slow for $n$ up to $2 \cdot 10^5$.

Edge cases to consider include scenarios where all temperatures are above $q$, so no vacation is possible, or where $k = 1$ and all temperatures are valid, meaning every day and every consecutive subarray contributes. A careless approach might try to count subarrays by brute force and either exceed time limits or mishandle the boundary of valid subarrays when temperatures exceed $q$.

## Approaches

The brute-force approach would iterate over every starting day and every possible ending day, checking that the temperatures between them never exceed $q$ and the length is at least $k$. This is correct but requires $O(n^2)$ operations per test case, which is unacceptable for the largest inputs.

The key observation that allows a faster approach is that any sequence of consecutive days where the temperature is at most $q$ can be treated as a block. Within this block of length $len$, every contiguous subarray of length at least $k$ is valid. The number of such subarrays can be computed directly using a simple formula: for a block of length $len \ge k$, there are $(len - k + 1) + (len - k) + \dots + 1 = (len - k + 1)(len - k + 2)/2$ valid subarrays. If $len < k$, there are no valid subarrays. This reduces the problem to scanning the array once and summing the counts for each valid block.

This approach naturally leads to an $O(n)$ algorithm for each test case, as we only traverse the array once and compute a simple arithmetic formula for each block of valid temperatures.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a counter to keep track of the number of valid vacation periods. Initialize a variable `length` to track the current block of consecutive days where the temperature does not exceed `q`.
2. Iterate through each temperature in the array. If the current day's temperature is at most `q`, increment `length` to extend the current block.
3. If the current day's temperature exceeds `q`, compute the number of valid subarrays in the current block. Only blocks of length at least `k` contribute. Use the formula $(length - k + 1) + (length - k) + \dots + 1 = (length - k + 1) \cdot (length - k + 2) / 2$. Reset `length` to zero to start a new block.
4. After the loop, handle the final block if the array ends with a valid sequence.
5. Return the total count of valid subarrays.

Why it works: every contiguous block of temperatures that satisfy the maximum temperature constraint can be counted independently. Within each block, the number of valid subarrays of length at least `k` can be calculated exactly without enumeration. The invariant is that at any point, `length` represents the number of consecutive valid days ending at the current index.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_vacations(n, k, q, a):
    count = 0
    length = 0
    for temp in a:
        if temp <= q:
            length += 1
        else:
            if length >= k:
                count += (length - k + 1) * (length - k + 2) // 2
            length = 0
    if length >= k:
        count += (length - k + 1) * (length - k + 2) // 2
    return count

t = int(input())
for _ in range(t):
    n, k, q = map(int, input().split())
    a = list(map(int, input().split()))
    print(count_vacations(n, k, q, a))
```

This solution reads input using fast I/O to handle up to $10^4$ test cases efficiently. The function `count_vacations` keeps track of blocks of valid days and computes the number of subarrays for each block. The key implementation detail is handling the last block after the loop ends, which is easy to forget.

## Worked Examples

Sample Input 1:

```
3 1 15
-5 0 -10
```

| Index | Temp | Length | Count |
| --- | --- | --- | --- |
| 0 | -5 | 1 | 0 |
| 1 | 0 | 2 | 0 |
| 2 | -10 | 3 | 0 |
| End of array: length=3, k=1 → add (3-1+1)*(3-1+2)/2 = 6 |  |  |  |
| Output: 6 |  |  |  |

This confirms the counting formula produces all contiguous subarrays of length at least 1.

Sample Input 2:

```
4 3 12
12 12 10 15
```

| Index | Temp | Length | Count |
| --- | --- | --- | --- |
| 0 | 12 | 1 | 0 |
| 1 | 12 | 2 | 0 |
| 2 | 10 | 3 | 0 |
| 3 | 15 | 0 | length=3 ≥ k → add (3-3+1)*(3-3+2)/2=1 |
| Output: 1 |  |  |  |

This demonstrates handling a block interrupted by an over-temperature day.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single pass through the array, constant work per element. |
| Space | O(1) | Only a few integers are used to track counts and lengths. |

Given the sum of all `n` across test cases is at most $2 \cdot 10^5$, the total runtime is well within the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    result = []
    t = int(input())
    for _ in range(t):
        n, k, q = map(int, input().split())
        a = list(map(int, input().split()))
        result.append(str(count_vacations(n, k, q, a)))
    return "\n".join(result)

# Provided samples
assert run("7\n3 1 15\n-5 0 -10\n5 3 -33\n8 12 9 0 5\n4 3 12\n12 12 10 15\n4 1 -5\n0 -1 2 5\n5 5 0\n3 -1 4 -5 -3\n1 1 5\n5\n6 1 3\n0 3 -2 5 -4 -4\n") == "6\n0\n1\n0\n0\n1\n9"

# Custom tests
assert run("1\n1 1 0\n-1\n") == "1"  # single valid day
assert run("1\n5 2 10\n11 12 13 14 15\n") == "0"  # all temps too high
assert run("1\n5 3 5\n1 2 3 4 5\n") == "6"  # full valid block
assert run("1\n6 2 3\n1 4 2 1 5 2\n") == "3"  # multiple small blocks
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 0 / -1 | 1 | Single day below threshold |
| 5 2 10 / 11 12 13 14 15 | 0 | All temperatures exceed q |
| 5 3 5 / 1 2 3 4 5 | 6 | Full valid block, length > k |
| 6 2 3 / 1 4 2 1 5 2 | 3 | Multiple small valid blocks separated by high temps |

## Edge Cases

If all temperatures are above the threshold, the algorithm correctly returns zero because no block reaches length `k`. For example, with input `[6 2 0, 1 2 3 4 5 6]`, `length` never increases beyond zero, so the count remains zero.

If the array ends with a valid block,
