---
title: "CF 2146A - Equal Occurrences"
description: "We are given a non-decreasing array of integers, and we want to find a subsequence whose elements all appear the same number of times. A subsequence can skip elements but cannot change their order."
date: "2026-06-08T01:25:39+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2146
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1052 (Div. 2)"
rating: 800
weight: 2146
solve_time_s: 72
verified: true
draft: false
---

[CF 2146A - Equal Occurrences](https://codeforces.com/problemset/problem/2146/A)

**Rating:** 800  
**Tags:** brute force, greedy, implementation  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a non-decreasing array of integers, and we want to find a subsequence whose elements all appear the same number of times. A subsequence can skip elements but cannot change their order. For example, from `[1, 1, 4, 4, 4]`, the subsequence `[1, 1, 4, 4]` is balanced because `1` and `4` appear exactly twice each. The task is to determine the length of the longest such balanced subsequence.

The constraints are moderate: each array has at most 100 elements, and there are up to 500 test cases. This suggests that an algorithm with roughly O(n²) operations per test case will run comfortably within the time limit. The small size also allows us to consider solutions based on counting frequencies without worrying about high complexity optimizations.

A subtle edge case arises when all elements are the same. For `[3, 3, 3, 3, 3]`, the whole array is already balanced. Another is when every element is distinct, such as `[1, 2, 3]`; the balanced subsequence here is any single element or all elements if each occurs once, which works because each element appears exactly once. A naive approach that tries to form subsequences without looking at frequencies might produce incorrect results in these scenarios.

## Approaches

The brute-force method is to generate all subsequences and check if they are balanced. For each subsequence, count the occurrences of each element and compare them. This is correct because it exhaustively considers every possibility. However, the number of subsequences grows exponentially (2ⁿ), making this approach infeasible even for n=20.

A better approach leverages the fact that elements are sorted and uses frequency counts. First, count how many times each distinct number appears. Then, the longest balanced subsequence is obtained by choosing a number k of occurrences that all elements can support. For instance, if the frequencies are `[3, 5, 2]`, we can pick k=2 because all numbers appear at least twice, forming a subsequence of length `2 * 3 = 6`. Iterating through all possible k from 1 to the maximum frequency of any element allows us to find the largest balanced subsequence efficiently.

The key insight is that a balanced subsequence's length is the number of chosen occurrences times the number of distinct numbers that can supply at least that many occurrences. Sorting the frequency counts simplifies finding the maximum length, because we only need to check frequencies that exist in the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2ⁿ * n) | O(n) | Too slow |
| Optimal | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases t. For each test case, read n and the array a.
2. Count the occurrences of each distinct number. Since the array is sorted, we can do this in one pass. Store the counts in a list `freq`.
3. Initialize `max_len` to 0. This will hold the length of the longest balanced subsequence.
4. For each possible count k from 1 to the maximum frequency:

a. Count how many elements in `freq` are greater than or equal to k. Call this `num_elements`.

b. The candidate subsequence length is `k * num_elements`. Update `max_len` if this is larger than the current `max_len`.
5. After iterating through all k, output `max_len` for this test case.

The invariant is that at each step, we only consider counts k that can be supplied by at least one element. By iterating over all possible k, we ensure we do not miss the optimal subsequence length. Because we compute `num_elements` for each k, we correctly account for only the elements that can participate in a balanced subsequence of that size.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    freq = []
    count = 1
    for i in range(1, n):
        if a[i] == a[i-1]:
            count += 1
        else:
            freq.append(count)
            count = 1
    freq.append(count)
    
    max_len = 0
    max_freq = max(freq)
    
    for k in range(1, max_freq + 1):
        num_elements = sum(1 for f in freq if f >= k)
        max_len = max(max_len, k * num_elements)
    
    print(max_len)
```

The first section reads input efficiently and counts frequencies using a simple linear scan. The `freq` list contains how many times each unique number appears. The iteration over possible k values ensures we consider all subsequences where each number appears the same number of times. Counting elements with at least k occurrences ensures the subsequence remains balanced.

## Worked Examples

**Sample 1:** `[1, 1, 4, 4, 4]`

| Step | freq | max_freq | k | num_elements | candidate length | max_len |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | [2,3] | 3 | 1 | 2 | 2 | 2 |
|  |  |  | 2 | 2 | 4 | 4 |
|  |  |  | 3 | 1 | 3 | 4 |

The algorithm correctly selects k=2 and both numbers to form a balanced subsequence of length 4.

**Sample 2:** `[1,2]`

| Step | freq | max_freq | k | num_elements | candidate length | max_len |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | [1,1] | 1 | 1 | 2 | 2 | 2 |

Both numbers appear once, so the whole array is balanced, giving a maximum length of 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Counting frequencies is O(n). For each k up to max frequency (≤ n), we scan freq (≤ n) to compute num_elements. |
| Space | O(n) | Store the frequency of each distinct number. |

With n ≤ 100, O(n²) operations per test case is roughly 10,000 operations, well within the 1-second limit. The solution uses only a linear array to store frequencies.

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
        freq = []
        count = 1
        for i in range(1, n):
            if a[i] == a[i-1]:
                count += 1
            else:
                freq.append(count)
                count = 1
        freq.append(count)
        max_len = 0
        max_freq = max(freq)
        for k in range(1, max_freq + 1):
            num_elements = sum(1 for f in freq if f >= k)
            max_len = max(max_len, k * num_elements)
        print(max_len)
    return output.getvalue().strip()

# Provided samples
assert run("4\n5\n1 1 4 4 4\n2\n1 2\n15\n1 1 1 1 1 2 2 2 2 3 3 3 4 4 5\n5\n3 3 3 3 3") == "4\n2\n9\n5"

# Custom cases
assert run("2\n1\n1\n3\n2 2 2") == "1\n3"  # minimum-size, all equal
assert run("1\n5\n1 2 3 4 5") == "5"  # all distinct
assert run("1\n6\n1 1 2 2 3 3") == "6"  # perfect balance
assert run("1\n7\n1 1 1 2 2 3 3") == "6"  # uneven counts
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1` | `1` | Single-element array |
| `2 2 2` | `3` | All-equal elements, full array balanced |
| `1 2 3 4 5` | `5` | All distinct, each count 1 |
| `1 1 2 2 3 3` | `6` | Already perfectly balanced |
| `1 1 1 2 2 3 3` | `6` | Must exclude one occurrence of `1` to balance |

## Edge Cases

For an array with all distinct elements, such as `[1, 2, 3]`, `freq = [1,1,1]`. Iterating over k=1, num_elements=3, candidate length=3, which matches the array length. The algorithm correctly returns 3.

For an array with all identical elements `[5,5,5,5]`, `freq=[4
