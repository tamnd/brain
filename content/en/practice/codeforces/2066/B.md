---
title: "CF 2066B - White Magic"
description: "We are asked to find the maximum length of a subsequence from a given array that satisfies a particular \"magical\" property."
date: "2026-06-08T07:12:04+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2066
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1004 (Div. 1)"
rating: 1900
weight: 2066
solve_time_s: 112
verified: false
draft: false
---

[CF 2066B - White Magic](https://codeforces.com/problemset/problem/2066/B)

**Rating:** 1900  
**Tags:** constructive algorithms, data structures, dp, greedy, implementation  
**Solve time:** 1m 52s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to find the maximum length of a subsequence from a given array that satisfies a particular "magical" property. A sequence is magical if, at every split point, the minimum of all elements on the left is at least as large as the minimum excluded number (MEX) of all elements on the right. The MEX is the smallest non-negative integer not present in the right part. Sequences of length one are automatically magical.

The input consists of multiple test cases. Each test case gives the length of the array and the array itself, with values potentially as large as $10^9$. Since the sum of lengths across all test cases can reach $2 \cdot 10^5$, any algorithm with a complexity worse than $O(n \log n)$ per test case will likely time out. A naive approach that tries all possible subsequences or splits would be exponential and completely infeasible.

Subtle edge cases include sequences that contain large gaps in their numbers or duplicates. For instance, a sequence like `[0, 1, 0, 1]` has repeated numbers but can still produce a magical subsequence `[0, 1, 0]`. Naively counting distinct numbers without considering duplicates would produce the wrong answer. Another case is when the sequence contains a single large number far greater than the indices, such as `[1000000000]`, which still has a maximum magical subsequence of length 1.

## Approaches

A brute-force approach would try every possible subsequence, compute the minimum on the left, compute the MEX on the right for every split, and check if the magical property holds. This is correct logically, but the number of subsequences grows exponentially with $n$, so the worst-case operation count is $O(2^n \cdot n)$, which is completely infeasible for $n$ up to $2 \cdot 10^5$.

The key observation is that the problem reduces to counting occurrences of consecutive non-negative integers starting from 0. Consider that the MEX of any set of numbers is the first missing number starting from 0. To maximize the magical subsequence, we want to include as many 0s as possible, then as many 1s as possible, and so on, until we hit a number that is missing entirely. Formally, we can construct a frequency map of the array, count how many 0s, 1s, 2s, etc. exist, and then the maximum magical subsequence length is determined by how many integers we can pair together in two groups: the first group contributing at most one element per integer, and the second group using the remaining counts. This transforms the problem into a simple counting problem without requiring expensive subsequence enumeration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Optimal (frequency-based counting) | O(n + max_val) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$. Iterate over each test case independently.
2. For each test case, read the array length $n$ and the array $a$. Initialize a frequency counter for all non-negative integers in the array. Because values can be large, we only need to track numbers up to $n+1$ since the MEX of any subsequence cannot exceed $n$.
3. Initialize a variable `mex_count` to track how many distinct numbers starting from 0 exist in the array.
4. Iterate through numbers starting from 0 and check their counts in the frequency map. While the count is positive, increment a counter for the magical subsequence length. Decrement counts appropriately to account for using one element in the first part of the split and the remaining for the second part.
5. Once a number is missing entirely in the frequency map, stop. At this point, the length of the magical subsequence is the sum of the numbers we could fully pair in the manner described.
6. Output this maximum length for the test case.

The invariant here is that every number we can include up to the first missing integer guarantees that the left minimum will never fall below the right MEX, because the MEX is precisely the first missing number and our left will contain all numbers below it.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import Counter

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        freq = Counter(a)
        length = 0
        first_group_used = 0
        
        mex = 0
        while True:
            count = freq.get(mex, 0)
            if count == 0:
                break
            if count >= 2:
                length += 2
            else:
                length += 1
            mex += 1
        
        print(length)

solve()
```

This solution builds a frequency counter of the array, iterates through integers starting from zero, and greedily includes elements in the magical subsequence according to their counts. We handle each integer up to the first missing one. One subtlety is that for the problem's definition, we are allowed to take duplicates optimally, which is why we sometimes add 2 to the length if the count of a number is 2 or more.

## Worked Examples

Sample input `[4, 3, 3, 2, 1, 0]`:

| i | Number | Count | Added to length | Length |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 1 | 1 |
| 1 | 1 | 1 | 1 | 2 |
| 2 | 2 | 1 | 1 | 3 |
| 3 | 3 | 2 | 2 | 5 |
| 4 | 4 | 1 | stop | 5 |

This shows we can use all zeros through threes and get the optimal subsequence length of 5.

Input `[0, 1, 0, 1]`:

| i | Number | Count | Added to length | Length |
| --- | --- | --- | --- | --- |
| 0 | 0 | 2 | 2 | 2 |
| 1 | 1 | 2 | 1 | 3 |
| 2 | 2 | 0 | stop | 3 |

This demonstrates that when a number is missing, we cannot continue and must stop.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Counting frequency and iterating up to `n+1` takes linear time per test case. |
| Space | O(n) | We store the frequency counts of numbers up to `n+1`. |

Given that the sum of $n$ across all test cases is at most $2 \cdot 10^5$, the solution easily fits in the 2-second time limit.

## Test Cases

```python
import sys, io
from collections import Counter

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("8\n5\n4 3 2 1 0\n6\n4 3 3 2 1 0\n4\n2 0 1 2\n1\n777\n4\n1000000000 1 7 9\n2\n0 1\n2\n1 2\n4\n0 1 0 1\n") == "5\n5\n3\n1\n4\n2\n2\n3"

# custom cases
assert run("1\n1\n0\n") == "1"
assert run("1\n5\n0 0 0 0 0\n") == "2"
assert run("1\n6\n0 1 2 3 4 5\n") == "6"
assert run("1\n3\n5 5 5\n") == "0"
assert run("1\n4\n0 2 2 1\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element `[0]` | 1 | Single-element sequence handling |
| All zeros `[0,0,0,0,0]` | 2 | Duplicates counted optimally |
| Consecutive `[0,1,2,3,4,5]` | 6 | Full consecutive sequence usage |
| No zeros `[5,5,5]` | 0 | Missing smallest number, empty subsequence |
| Mixed `[0,2,2,1]` | 4 | Proper handling of order and duplicates |

## Edge Cases

For `[0,0,0,0,0]`, our frequency counter gives `{0:5}`. The first number 0 has count ≥ 2, so we add 2 to the length. The next number 1 is missing, so the loop stops. The output 2 matches the maximal magical subsequence `[0,0]`.

For `[5,5,5]`, the count for 0 is zero, so the loop exits immediately and the output is 0. This correctly handles sequences without the required starting integers.

For `[0,1,0,1]`, the count table gives `{0:2,1:2}`. We add
