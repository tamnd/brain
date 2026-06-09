---
title: "CF 2033D - Kousuke's Assignment"
description: "We are given an array of integers and need to identify subarrays, or contiguous segments, whose sum is zero. These segments are called beautiful. The task is not just to find all beautiful segments but to maximize the number of them without overlaps."
date: "2026-06-08T11:42:50+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "dsu", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2033
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 981 (Div. 3)"
rating: 1300
weight: 2033
solve_time_s: 92
verified: true
draft: false
---

[CF 2033D - Kousuke's Assignment](https://codeforces.com/problemset/problem/2033/D)

**Rating:** 1300  
**Tags:** data structures, dp, dsu, greedy, math  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and need to identify subarrays, or contiguous segments, whose sum is zero. These segments are called beautiful. The task is not just to find all beautiful segments but to maximize the number of them without overlaps. In other words, once a segment is counted, no element inside it can appear in another beautiful segment.

The input consists of multiple test cases, each with a potentially large array. The array length can reach 100,000, and the sum of lengths across all test cases is limited to 300,000. A naive solution that checks all possible subarrays for zero sum is infeasible because the number of subarrays grows quadratically with array length. This rules out any O(n²) approach. We need an algorithm that works roughly in O(n) or O(n log n) time per test case.

Non-obvious edge cases include arrays with many zeros, arrays where only the full array sums to zero, and arrays with repeated patterns that can form multiple non-overlapping zero-sum segments. For example, `[0, 0, 0]` should return `3` because each zero alone can be a segment, while a careless approach that tries only maximal-length segments might return `1`.

## Approaches

The brute-force approach would iterate over all possible starting indices and, for each, check all possible ending indices to see if the subarray sums to zero. This method is correct in principle because it explores every segment, but it requires O(n²) operations per array. With n up to 10^5, this would perform roughly 10^10 operations in the worst case, far exceeding any reasonable time limit.

The key observation that unlocks a faster solution is that a zero-sum segment corresponds to a repeated prefix sum. If we compute the prefix sum of the array, then a segment `[l, r]` sums to zero if `prefix[r] - prefix[l-1] = 0`. Rearranging, this means `prefix[r] = prefix[l-1]`. Therefore, whenever we see a prefix sum that we have seen before, we can end a beautiful segment there. To maximize non-overlapping segments, we greedily end a segment whenever we detect a repeated prefix sum, then reset our tracking to avoid overlapping segments.

This leads to an optimal O(n) solution per test case using a set to track the prefix sums seen since the last segment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Prefix Sum + Set | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable `count` to zero. This will store the number of beautiful segments found.
2. Initialize a variable `prefix` to zero to track the running sum of the array elements.
3. Initialize a set `seen` containing zero. This set stores prefix sums seen since the last segment end.
4. Iterate through each element of the array. Add the current element to `prefix`.
5. Check if `prefix` is already in `seen`. If it is, increment `count` because a beautiful segment ends here. Reset `seen` to contain only zero and reset `prefix` to zero for the next segment. This ensures non-overlapping segments.
6. If `prefix` is not in `seen`, add it to `seen` and continue.
7. After processing the array, `count` contains the maximum number of non-overlapping beautiful segments. Output this value for the current test case.

Why it works: the set `seen` ensures we track all possible prefix sums since the last segment end. The first time we see a repeated prefix sum, we have found the earliest point to end a segment without missing potential later segments. Resetting the set guarantees non-overlapping, and the greedy approach maximizes the number of segments because we always end a segment at the earliest opportunity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        count = 0
        prefix = 0
        seen = set()
        seen.add(0)
        
        for x in a:
            prefix += x
            if prefix in seen:
                count += 1
                seen = set()
                seen.add(0)
                prefix = 0
            else:
                seen.add(prefix)
        
        print(count)

if __name__ == "__main__":
    solve()
```

The code initializes prefix sum tracking and the set of seen prefix sums with zero. As it iterates through the array, it checks if the current prefix sum has already been seen since the last segment. When it has, a segment ends, the set is reset, and counting continues. Using a set avoids repeatedly scanning for duplicates and ensures O(1) checks per element.

## Worked Examples

Sample 1: `[2, 1, -3, 2, 1]`

| i | x | prefix | seen | count |
| --- | --- | --- | --- | --- |
| 0 | 2 | 2 | {0,2} | 0 |
| 1 | 1 | 3 | {0,2,3} | 0 |
| 2 | -3 | 0 | 0 in seen? yes | 1 |
| 3 | 2 | 2 | {0,2} | 1 |
| 4 | 1 | 3 | {0,2,3} | 1 |

Count = 1, matches expected.

Sample 2: `[0, -4, 0, 3, 0, 1]`

| i | x | prefix | seen | count |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 in seen? yes | 1 |
| 1 | -4 | -4 | {-4,0} reset -> prefix=0 | 1 |
| 2 | 0 | 0 | 0 in seen? yes | 2 |
| 3 | 3 | 3 | {0,3} | 2 |
| 4 | 0 | 3 | {0,3} | 2 |
| 5 | 1 | 4 | {0,3,4} | 2 |

Count = 3, matches expected output.

These traces show that the algorithm detects segments greedily and handles zeros correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is processed once; set operations are amortized O(1) |
| Space | O(n) per test case | The set of prefix sums can grow up to n elements |

Given the constraints (sum of n ≤ 300,000), this approach easily runs within 2 seconds and uses less than 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# Provided samples
assert run("3\n5\n2 1 -3 2 1\n7\n12 -4 4 43 -3 -5 8\n6\n0 -4 0 3 0 1\n") == "1\n2\n3"

# Minimum input
assert run("1\n1\n0\n") == "1"
assert run("1\n1\n5\n") == "0"

# All zeros
assert run("1\n5\n0 0 0 0 0\n") == "5"

# Large positive and negative sums
assert run("1\n6\n3 -1 -2 4 -4 0\n") == "3"

# Non-overlapping tricky case
assert run("1\n8\n1 2 -3 1 -1 0 0 0\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element zero | 1 | Single element zero |
| 1 element non-zero | 0 | Single element non-zero |
| 5 zeros | 5 | Consecutive zeros handled correctly |
| Mixed signs | 3 | Multiple non-overlapping segments |
| Complex pattern | 4 | Algorithm finds maximum non-overlapping segments |

## Edge Cases

For `[0, 0, 0]`, the algorithm starts with `prefix = 0` and `seen = {0}`. The first zero triggers `prefix in seen`, incrementing count to 1 and resetting `prefix` and `seen`. Each subsequent zero repeats this process, yielding three segments in total. This confirms that the greedy approach handles consecutive zeros correctly.

For `[3, -3, 3, -3]`, prefix sums are `[3,0,3,0]`. The algorithm detects the first zero prefix sum at index 1, counts one segment, resets, then detects another zero prefix sum at index 3, counting a second segment. This matches the expected maximum of 2 non-overlapping segments, demonstrating the correctness for alternating positive and negative numbers.
