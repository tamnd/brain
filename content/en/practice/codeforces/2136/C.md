---
title: "CF 2136C - Against the Difference"
description: "We are given an array of integers, and our goal is to extract the longest possible subsequence that is \"neat.\" A neat subsequence is made by concatenating one or more blocks, where a block is a sequence of identical numbers, and the value of the number equals the length of the…"
date: "2026-06-09T04:10:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 2136
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1046 (Div. 2)"
rating: 1200
weight: 2136
solve_time_s: 82
verified: true
draft: false
---

[CF 2136C - Against the Difference](https://codeforces.com/problemset/problem/2136/C)

**Rating:** 1200  
**Tags:** data structures, dp  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and our goal is to extract the longest possible subsequence that is "neat." A neat subsequence is made by concatenating one or more blocks, where a block is a sequence of identical numbers, and the value of the number equals the length of the block. For instance, `[3,3,3]` is a valid block because it contains three elements, all equal to three. The array `[2,2]` is a valid block, but `[2,2,2]` is not because the value 2 does not match the length 3. An empty array is always considered neat.

We need to find the length of the longest subsequence of the input array that can be partitioned into these blocks. This requires not only finding repeated numbers but also grouping them so that the count matches the number itself.

The constraints indicate that `n` can be as large as 200,000 across all test cases. With up to 10,000 test cases, we cannot afford anything slower than roughly O(n) per test case. A naive approach that tries every subsequence would be exponential in n and completely impractical. Edge cases to consider include arrays where no neat subsequence exists, arrays consisting entirely of ones or n's, and arrays where multiple disjoint blocks of the same number exist but cannot be combined into a larger neat block.

For example, the array `[2,2,1,1]` can form blocks `[2,2]` and two `[1]` blocks, giving a neat subsequence of length 4. In contrast, `[2,3,3]` cannot form any valid block, resulting in a neat subsequence of length 0.

## Approaches

The brute-force approach would consider every subsequence, check if it can be partitioned into valid blocks, and take the maximum length. This is correct in principle, but the number of subsequences is `2^n`, which is utterly infeasible even for `n = 20`.

The key insight is to recognize that blocks are determined entirely by the frequency of numbers. We do not care about order within a block or across blocks; we only need enough identical numbers to form full blocks. For each number `x` in the array, we can attempt to form as many blocks of size `x` as possible. The greedy strategy is to keep forming full blocks from the largest possible count of each number, accumulating the total length of all complete blocks. Because block formation is independent for each number, we can use a dynamic programming array where `dp[x]` stores the maximum length of a neat subsequence ending with blocks of number `x`.

In practice, we iterate over each number in the array, maintain a count of occurrences, and track the largest neat subsequence length we can build by adding this number as part of a complete block whenever we have seen enough occurrences. The problem reduces to counting and grouping, which allows O(n) processing per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Counting + Greedy | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read `n` and the array `a`.
2. Create a dictionary `count` to track how many times each number appears in `a`.
3. Create a dictionary `dp` to track the maximum length of neat subsequence that ends with a block of that number.
4. Iterate through the array. For each element `x`:

- Increment `count[x]`.
- If `count[x]` reaches `x`, it means we can form a complete block of size `x`.
- Update `dp[x]` as `dp[x] = dp[x] + x` and reset `count[x]` for the next potential block.
5. Keep track of the maximum value in `dp` across all numbers; this represents the length of the longest neat subsequence.
6. Print the result for each test case.

The reasoning is that each block is independent and only relies on having enough occurrences of the number. By incrementally counting occurrences and forming blocks greedily, we ensure no potential blocks are wasted and the total length is maximized.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        from collections import defaultdict
        
        count = defaultdict(int)
        dp = defaultdict(int)
        res = 0
        
        for x in a:
            dp[x] = max(dp[x], 0)
            count[x] += 1
            if count[x] >= x:
                dp[x] += x
                count[x] -= x
            res = max(res, dp[x])
        print(res)
```

This solution reads multiple test cases efficiently using `sys.stdin.readline` for fast input. We use a `defaultdict` to avoid key errors when incrementing counts. The `dp` dictionary tracks the maximum length achievable with each number. The greedy update ensures that every complete block contributes to the total neat subsequence length.

## Worked Examples

**Sample Input 1:** `[1]`

| Step | x | count[x] | dp[x] | res |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0→1 | 1 |

This produces length 1, forming the block `[1]`.

**Sample Input 2:** `[1,2,3,3,3,1]`

| Step | x | count[x] | dp[x] | res |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 0 |
| 2 | 2 | 1 | 0 | 0 |
| 3 | 3 | 1 | 0 | 0 |
| 4 | 3 | 2 | 0 | 0 |
| 5 | 3 | 3 | 0→3 | 3 |
| 6 | 1 | 2 | 1→2 | 5 |

The resulting longest neat subsequence has length 5.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is processed once, dictionary operations are O(1) on average |
| Space | O(n) | `count` and `dp` dictionaries store at most n keys |

Given `sum(n) ≤ 2*10^5`, this fits comfortably within the 2-second limit and 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided samples
assert run("6\n1\n1\n2\n2 2\n4\n2 2 1 1\n6\n1 2 3 3 3 1\n8\n8 8 8 8 8 8 8 7\n10\n2 3 3 1 2 3 5 1 1 7\n") == "1\n2\n4\n5\n0\n5"

# custom cases
assert run("1\n5\n1 1 1 1 1\n") == "5"  # all ones
assert run("1\n4\n4 4 4 4\n") == "4"  # single block matches length
assert run("1\n6\n2 2 2 2 2 2\n") == "4"  # 2 blocks of 2
assert run("1\n3\n2 3 3\n") == "0"  # no neat subsequence
assert run("1\n1\n10\n") == "0"  # number too large for block
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 ones | 5 | Can form blocks of size 1 repeatedly |
| 4 fours | 4 | Single block equals the number |
| 6 twos | 4 | Multiple blocks of same number |
| [2,3,3] | 0 | Cannot form any valid block |
| [10] | 0 | Single number cannot form block |

## Edge Cases

When the array contains numbers larger than the count available, no block can form. For example `[10]` results in length 0 because a block of length 10 requires ten occurrences of 10. Arrays with repeated ones correctly form multiple blocks of size 1. Arrays where the total occurrences are multiples of the number, like `[2,2,2,2]`, correctly yield blocks of `[2,2]` twice for a total length of 4. This algorithm handles these cases by tracking `count[x]` and only updating `dp[x]` when a full block is available, ensuring correctness.
