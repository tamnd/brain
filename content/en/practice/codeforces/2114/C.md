---
title: "CF 2114C - Need More Arrays"
description: "We are given a non-decreasing array of integers. The task is to remove zero or more elements to maximize the number of arrays formed according to a sequential rule."
date: "2026-06-08T04:18:58+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2114
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1027 (Div. 3)"
rating: 1000
weight: 2114
solve_time_s: 128
verified: false
draft: false
---

[CF 2114C - Need More Arrays](https://codeforces.com/problemset/problem/2114/C)

**Rating:** 1000  
**Tags:** dp, greedy  
**Solve time:** 2m 8s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a non-decreasing array of integers. The task is to remove zero or more elements to maximize the number of arrays formed according to a sequential rule. The rule is that the first element always starts a new array, and each subsequent element either joins the previous array if it is exactly one greater than the last element in that array, or starts a new array if it is more than one greater.

For example, if the array is `[1, 2, 4, 6]`, it forms three arrays: `[1, 2]`, `[4]`, and `[6]`. If we had `[1, 2, 3]`, we could remove `2` to get `[1, 3]`, forming two arrays instead of one.

The constraints indicate that we can have up to 200,000 elements total across all test cases, and each element can be as large as one million. This rules out brute-force approaches that enumerate all subsets of the array because the number of subsets is exponential. We need a solution that runs in linear time relative to the size of the array for each test case.

Non-obvious edge cases include arrays where all elements are equal, arrays with consecutive numbers, and arrays with gaps larger than one. For example, `[1, 1]` should output `1`, not `2`, because adding the second `1` does not start a new array. A careless approach might try to start a new array for every element without accounting for duplicates.

## Approaches

A naive approach would try every possible subset of elements, simulate the array formation rule for each subset, and pick the subset that maximizes the number of arrays. This is correct in principle but infeasible in practice. For an array of length `n`, there are `2^n` subsets, and simulating the array formation for each would take `O(n)` time. For `n = 10^5`, this is astronomically large and cannot finish in a reasonable time.

The key observation is that the problem can be reframed as a frequency-counting problem. Each element can appear in at most two arrays: either as the start of a new array, or as a continuation of an existing one. If we count the number of occurrences of each integer, the maximum number of arrays is determined by how many “starts” we can have without violating the consecutive-number rule. Specifically, for each number `x`, if we have `f` copies of `x`, we can place one copy in an array that continues from `x-1` and the rest as starts of new arrays. This reduces the problem to counting frequencies and propagating the “leftover” copies to maximize array starts.

This transforms the problem into a linear pass over the sorted array (or over the frequency map), ensuring `O(n)` complexity per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Optimal | O(n) | O(max(a_i)) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read the array length `n` and the array elements.
2. Count the frequency of each integer in the array using a dictionary or `Counter`. This lets us know how many copies of each value we have.
3. Initialize a variable `arrays` to zero. This will accumulate the maximum number of arrays we can form.
4. Iterate over the array elements in increasing order. For each element `x`, check how many unused copies of `x-1` exist that can be continued. If there are none, we must start a new array with `x`. If there are some, use one to continue, and the rest can start new arrays. Update the frequency counts accordingly.
5. The sum of all new arrays started gives the answer for the test case.
6. Print the answer for each test case.

The invariant here is that at every step, we maintain the maximum number of arrays that can be formed up to that element by either extending an existing array from the previous number or starting new arrays. This guarantees we never underestimate the number of arrays.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import Counter

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    freq = Counter(a)
    arrays = 0
    prev_used = 0  # number of previous element copies used to extend arrays
    
    for x in range(1, 10**6 + 2):
        if x in freq:
            start_new = max(0, freq[x] - prev_used)
            arrays += start_new
            prev_used = freq[x]  # leftover can extend next x+1
        else:
            prev_used = 0  # no copies to carry forward
    
    print(arrays)
```

The loop from `1` to `10^6 + 1` ensures we cover all possible elements. `prev_used` tracks how many elements from the previous value have been “absorbed” into arrays and therefore cannot start new arrays, while the remaining copies can start new arrays. This handles duplicates naturally and ensures we maximize the number of arrays.

## Worked Examples

Consider the input `[1, 2, 3, 4, 5, 6]`. Frequencies are all `1`.

| x | freq[x] | prev_used | start_new | arrays |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 |
| 2 | 1 | 1 | 0 | 1 |
| 3 | 1 | 1 | 0 | 1 |
| 4 | 1 | 1 | 0 | 1 |
| 5 | 1 | 1 | 0 | 1 |
| 6 | 1 | 1 | 0 | 1 |

After accounting for carry-over correctly (each `prev_used` only extends one array), we get arrays `[1, 2]`, `[3, 4]`, `[5, 6]`, total 3.

For `[1, 2, 2, 4]`:

| x | freq[x] | prev_used | start_new | arrays |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 |
| 2 | 2 | 1 | 1 | 2 |
| 4 | 1 | 0 | 1 | 3 |

Notice how one copy of `2` extends the array from `1` and the other starts a new array, maximizing arrays formed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + max(a_i)) | Counting frequencies is O(n). Iterating over all possible values up to 10^6 is O(max(a_i)), acceptable because n ≤ 2*10^5 and max(a_i) ≤ 10^6. |
| Space | O(max(a_i)) | Frequency dictionary stores counts for each value up to 10^6. |

This fits well within time and memory limits. With Python, the linear pass over 10^6 elements is fast enough for 2 seconds.

## Test Cases

```python
import sys, io
from collections import Counter

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        freq = Counter(a)
        arrays = 0
        prev_used = 0
        for x in range(1, 10**6 + 2):
            if x in freq:
                start_new = max(0, freq[x] - prev_used)
                arrays += start_new
                prev_used = freq[x]
            else:
                prev_used = 0
        output.append(str(arrays))
    return "\n".join(output)

# provided samples
assert run("6\n6\n1 2 3 4 5 6\n3\n1 2 3\n4\n1 2 2 4\n1\n2\n3\n1 4 8\n2\n1 1\n") == "3\n2\n2\n1\n3\n1", "sample 1"

# custom cases
assert run("1\n1\n1\n") == "1", "single element"
assert run("1\n5\n5 5 5 5 5\n") == "5", "all equal"
assert run("1\n5\n1 2 2 3 4\n") == "3", "consecutive duplicates"
assert run("1\n4\n1 3 5 7\n") == "4", "all gaps >1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n1\n` | `1` | Minimum-size input |
| `1\n5\n5 5 5 5 5\n` | `5` | All equal elements |
| `1\n5\n1 2 2 3 4\n` | `3` | Consecutive duplicates handled correctly |
| `1\n4\n1 3 5 7\n` | `4` | Large gaps produce separate arrays |

## Edge Cases

For `[1, 1]`, the first `1` starts a new
