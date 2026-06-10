---
title: "CF 1497A - Meximization"
description: "We are given an array of nonnegative integers and we want to reorder it to maximize the sum of MEX values over all prefixes. A prefix is any initial segment of the array. The MEX of a set is the smallest nonnegative integer not present in that set."
date: "2026-06-10T21:48:12+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1497
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 708 (Div. 2)"
rating: 800
weight: 1497
solve_time_s: 378
verified: false
draft: false
---

[CF 1497A - Meximization](https://codeforces.com/problemset/problem/1497/A)

**Rating:** 800  
**Tags:** brute force, data structures, greedy, sortings  
**Solve time:** 6m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of nonnegative integers and we want to reorder it to maximize the sum of **MEX** values over all prefixes. A prefix is any initial segment of the array. The **MEX** of a set is the smallest nonnegative integer not present in that set. For example, the MEX of `{0, 1, 3}` is `2`, because `0` and `1` are present but `2` is missing.

The input contains multiple test cases. Each test case provides the array size `n` (up to 100) and the array elements themselves (all between 0 and 100). The small size of `n` implies that an algorithm with O(n²) complexity can run comfortably under 1 second, but we should aim for something simpler and more direct because the problem has a clear greedy structure.

Non-obvious edge cases include arrays missing `0`, arrays where all elements are equal, or arrays where some numbers appear multiple times. For instance, if the array is `[2, 2, 3]`, a naive approach might try to start with the largest elements to maximize MEX, but this fails because MEX is very sensitive to missing small numbers. The correct output should prioritize starting from `0` if it exists.

## Approaches

A brute-force approach would try every permutation of the array, compute the MEX for each prefix, and sum them up. This works in principle, but the number of permutations is `n!` which explodes even for `n=10`, making this completely impractical.

The key observation is that MEX grows only when we include the smallest missing number. So, to maximize the sum of prefix MEXes, we should first include all distinct numbers starting from `0` upwards, in order. Once the first occurrence of each number `0,1,2,...` is placed, the MEX of the prefix grows incrementally.

After the first occurrences, the remaining elements can be appended in any order, as they no longer increase MEX. This simple greedy strategy produces a correct and efficient solution because the MEX at each prefix is determined entirely by the set of numbers already placed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all permutations) | O(n!) | O(n) | Too slow |
| Greedy by first occurrences | O(n + max(a)) | O(max(a)) | Accepted |

## Algorithm Walkthrough

1. Count the occurrences of each number in the array. We need to know which numbers are present at least once.
2. Initialize an empty result array.
3. Loop from `0` upwards and append the first occurrence of each number that exists in the array. For each appended number, decrease its count. This ensures that the prefix MEX increases steadily by 1 at each step.
4. Once all numbers from `0` up to the maximum present have been handled once, append the remaining numbers in any order. They do not contribute to increasing MEX but complete the array.
5. Output the result array.

**Why it works**: At each step, we guarantee that the MEX of the current prefix is maximized by including the smallest missing number first. Once the prefix contains all numbers from `0` to `k-1`, the MEX becomes `k`. Appending duplicates afterwards cannot increase the MEX, so placing them at the end is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    count = [0] * 102  # numbers are 0..100
    for x in a:
        count[x] += 1
    
    result = []
    # step 1: include each number once to increase MEX
    for i in range(102):
        if count[i]:
            result.append(i)
            count[i] -= 1
    
    # step 2: append remaining numbers in any order
    for i in range(102):
        while count[i]:
            result.append(i)
            count[i] -= 1
    
    print(' '.join(map(str, result)))
```

The first loop ensures that each prefix grows the MEX optimally. The second loop handles leftover numbers. The array `count` is large enough to cover all input numbers and prevents index errors. Boundary handling is implicit because all numbers are ≤100.

## Worked Examples

**Sample 1:**

Input array: `[4, 2, 0, 1, 3, 3, 7]`

| Step | Action | Result Array | MEX of Prefix |
| --- | --- | --- | --- |
| 1 | Append 0 | [0] | 1 |
| 2 | Append 1 | [0,1] | 2 |
| 3 | Append 2 | [0,1,2] | 3 |
| 4 | Append 3 | [0,1,2,3] | 4 |
| 5 | Append 4 | [0,1,2,3,4] | 5 |
| 6 | Append 7 | [0,1,2,3,4,7] | 5 |
| 7 | Append remaining 3 | [0,1,2,3,4,7,3] | 5 |

This sequence matches the sample output and confirms the greedy logic.

**Sample 2:**

Input array: `[2, 2, 8, 6, 9]`

| Step | Action | Result Array | MEX of Prefix |
| --- | --- | --- | --- |
| 1 | Append 0 (missing) | skip | MEX=0 |
| 2 | Append 1 (missing) | skip | MEX=0 |
| 3 | Append 2 | [2] | 0 |
| 4 | Append remaining numbers 2,6,8,9 | [2,6,8,9,2] | 1 |

Here MEX increases only when necessary; duplicates are added at the end.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + max(a)) | Counting and iterating up to 101 numbers |
| Space | O(max(a)) | Count array for numbers 0..100 |

With n ≤100 and numbers ≤100, the algorithm performs at most 200 iterations per test case, well within the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        count = [0] * 102
        for x in a:
            count[x] += 1
        result = []
        for i in range(102):
            if count[i]:
                result.append(i)
                count[i] -= 1
        for i in range(102):
            while count[i]:
                result.append(i)
                count[i] -= 1
        print(' '.join(map(str, result)))
    return output.getvalue().strip()

# provided samples
assert run("3\n7\n4 2 0 1 3 3 7\n5\n2 2 8 6 9\n1\n0\n") == "0 1 2 3 4 7 3\n2 6 8 9 2\n0", "samples"

# custom cases
assert run("1\n5\n0 0 0 0 0\n") == "0 0 0 0 0", "all equal zeros"
assert run("1\n4\n1 1 1 1\n") == "1 1 1 1", "all equal nonzero, MEX=0"
assert run("1\n3\n0 2 1\n") == "0 1 2", "small array consecutive numbers"
assert run("1\n6\n0 1 2 4 5 6\n") == "0 1 2 4 5 6", "missing 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 0 0 0` | `0 0 0 0 0` | Duplicates of 0, MEX grows once |
| `1 1 1 1` | `1 1 1 1` | Missing 0, MEX remains 0 initially |
| `0 2 1` | `0 1 2` | Small consecutive numbers |
| `0 1 2 4 5 6` | `0 1 2 4 5 6` | Non-consecutive, missing number 3 |

## Edge Cases

If `0` is missing entirely, the MEX of the first prefix is `0`, and no prefix can start with MEX > 0. For example, `[1,1,2]` results in `[1,2,1]`. If all elements are the same, the MEX increases only once (if 0 is present) and stays constant afterwards. The algorithm handles these correctly because it always checks for first occurrences starting from `0` and appends remaining elements afterwards.
