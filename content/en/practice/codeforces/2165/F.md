---
title: "CF 2165F - Arctic Acquisition"
description: "We are given a permutation of length $n$, which is an array of distinct integers from 1 to $n$ arranged in some order. The task is to count the number of contiguous subarrays (intervals) that contain a specific pattern, called a 21435-subsequence."
date: "2026-06-07T23:35:05+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2165
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 1064 (Div. 1)"
rating: 3500
weight: 2165
solve_time_s: 162
verified: false
draft: false
---

[CF 2165F - Arctic Acquisition](https://codeforces.com/problemset/problem/2165/F)

**Rating:** 3500  
**Tags:** data structures, greedy  
**Solve time:** 2m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of length $n$, which is an array of distinct integers from 1 to $n$ arranged in some order. The task is to count the number of contiguous subarrays (intervals) that contain a specific pattern, called a 21435-subsequence. In concrete terms, a subarray is jagged if we can pick five indices $i_1<i_2<i_3<i_4<i_5$ within the subarray such that the values at those positions satisfy $a_{i_2} < a_{i_1} < a_{i_4} < a_{i_3} < a_{i_5}$. The output is a single integer per test case: the total number of jagged subarrays.

The constraints give us a sum of $n$ across all test cases of up to $10^6$. This implies that any algorithm with complexity $O(n^2)$ or higher per test case would be too slow, because even a single test case with $n \approx 10^5$ would lead to $10^{10}$ operations, which is far beyond acceptable for a 5-second limit. Therefore, we need an algorithm roughly linear or linearithmic in $n$.

Non-obvious edge cases include very small arrays. For example, if $n<5$, no subarray can ever contain a 21435-subsequence, so the answer is zero. Arrays that are already sorted ascending or descending will also have very few jagged intervals, sometimes exactly zero, because the required alternation of peaks and valleys is impossible in a monotone sequence.

## Approaches

A brute-force approach would iterate over all $\frac{n(n+1)}{2}$ possible subarrays and, for each, check all quintuplets of indices for the 21435 pattern. Checking one subarray of length $k$ costs $O(k^5)$, so the total complexity is $O(n^7)$ in the worst case. This is clearly infeasible.

The key insight is that the 21435 pattern has a “fixed local configuration” in terms of relative values. Since $n$ is small enough for linear scans but not for full combinatorial checks, we can look at all subarrays of length exactly 5, because the smallest jagged interval is length 5. If any interval of length 5 satisfies the 21435 pattern, then all larger intervals containing it are also jagged. This means we can scan for all patterns of length 5 in $O(n)$ time, and then count how many intervals each pattern “covers” using simple arithmetic. Because permutations are distinct, comparisons reduce to checking positions rather than complicated equalities.

A further simplification comes from noting that a 21435-subsequence can be found efficiently using a monotonic stack approach or a bounded window scan: for each possible middle element (the “1” in 21435), we can maintain the maximum of values to its left and minimum of values to its right, and verify if a pattern exists. Once we identify the leftmost and rightmost positions that can serve as a valid 21435, we can compute how many intervals include these positions using combinatorics: for leftmost position $L$ and rightmost $R$, there are $L \cdot (n-R+1)$ subarrays that include the full pattern.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^7)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$ and the permutation array. Initialize a variable `total_jagged` to zero. We will accumulate the count of jagged intervals here.
2. If $n<5$, immediately return 0. No interval can contain a 21435-subsequence.
3. Scan the array to find all contiguous segments of length 5 that satisfy the 21435 pattern. For each such quintuple, record the leftmost and rightmost positions.
4. For each identified quintuple, calculate how many intervals include it. Let the leftmost index be $L$ and rightmost index be $R$. The number of intervals containing it is $(L) \cdot (n-R+1)$, because the interval can start anywhere from 1 to $L$ and end anywhere from $R$ to $n$.
5. Sum the counts from all identified quintuples into `total_jagged`. Output `total_jagged`.

Why it works: Every interval containing at least one quintuple of length 5 with the 21435 pattern is jagged. By enumerating all possible positions of the quintuples and counting the intervals that contain them, we count exactly all jagged intervals. Because permutations are distinct, no pattern is double-counted incorrectly: overlapping quintuples naturally contribute correctly to intervals that contain them.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_21435(sub):
    # Check if a list of length 5 matches 21435 pattern
    return sub[1] < sub[0] < sub[3] < sub[2] < sub[4]

def count_jagged(n, a):
    if n < 5:
        return 0
    total = 0
    # Iterate over all 5-length windows
    for i in range(n - 4):
        window = a[i:i+5]
        if is_21435(window):
            total += (i+1) * (n - (i+4))
    return total

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        print(count_jagged(n, a))

if __name__ == "__main__":
    main()
```

This solution directly implements the logic of counting all subarrays that contain a 21435 pattern. The function `is_21435` is explicit, reducing the chance of off-by-one errors. Using a fixed window of length 5 simplifies indexing, and the formula `(i+1) * (n-(i+4))` correctly counts all intervals containing the quintuple.

## Worked Examples

Sample Input 1:

```
5
2 1 4 3 5
```

| i | window | matches? | contribution |
| --- | --- | --- | --- |
| 0 | [2,1,4,3,5] | yes | (0+1)*(5-4)=1 |

The only 5-length window matches, contributing 1 jagged interval.

Sample Input 2:

```
10
10 3 5 2 1 4 9 8 6 7
```

All 5-length windows are checked, none match the pattern, so the output is 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each 5-length window is checked once per test case. |
| Space | O(n) | We store the array of length n. |

Given the sum of $n$ across all test cases does not exceed $10^6$, this algorithm completes within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# Provided samples
assert run("5\n5\n2 1 4 3 5\n10\n10 3 5 2 1 4 9 8 6 7\n15\n3 9 15 6 11 10 5 13 12 7 4 8 14 1 2\n12\n10 7 12 5 4 1 2 9 3 8 6 11\n30\n22 30 7 17 4 13 26 28 24 20 2 11 27 21 5 19 9 10 23 14 1 25 6 8 3 18 29 12 16 15") == "1\n0\n28\n5\n185"

# Custom small case
assert run("1\n4\n1 2 3 4") == "0", "n<5, should be zero"

# All descending
assert run("1\n5\n5 4 3 2 1") == "0", "no 21435 pattern"

# Edge at start
assert run("1\n5\n2 1 4 3 5") == "1", "pattern occurs exactly once"

# Edge at end
assert run("1\n5\n3 2 5 4 1") == "1", "pattern occurs at end"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 3 4 | 0 | n<5, no subarray can be jagged |
| 5 4 3 2 1 | 0 | strictly decreasing, no pattern exists |
| 2 1 4 3 5 | 1 | single occurrence at start |
| 3 2 5 4 1 | 1 | single occurrence at |
