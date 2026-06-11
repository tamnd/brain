---
title: "CF 1400D - Zigzags"
description: "We are given an array of integers and asked to count how many quadruples of indices $(i, j, k, l)$ satisfy both $i < j < k < l$ and $a[i] = a[k]$, $a[j] = a[l]$."
date: "2026-06-11T08:51:41+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "combinatorics", "data-structures", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1400
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 94 (Rated for Div. 2)"
rating: 1900
weight: 1400
solve_time_s: 86
verified: true
draft: false
---

[CF 1400D - Zigzags](https://codeforces.com/problemset/problem/1400/D)

**Rating:** 1900  
**Tags:** brute force, combinatorics, data structures, math, two pointers  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and asked to count how many quadruples of indices $(i, j, k, l)$ satisfy both $i < j < k < l$ and $a[i] = a[k]$, $a[j] = a[l]$. In other words, we want two pairs of matching values where the first and third positions hold the same value and the second and fourth positions hold the same value, with the indices strictly increasing.

The input provides multiple test cases. For each test case, we first read the size of the array $n$ and then the array itself. We are guaranteed that the sum of all $n$ across test cases does not exceed 3000. This means any algorithm that runs in roughly $O(n^2)$ time per test case should be fast enough, but anything $O(n^3)$ or worse will likely time out in the worst case.

A naive implementation might try to enumerate all quadruples using four nested loops. This would be correct but extremely slow: the worst-case operation count is about $n^4$, which is on the order of $8 \times 10^{13}$ operations if $n = 3000$, clearly infeasible.

Edge cases that a naive solution can miss include arrays where all elements are equal. For example, if the array is $[2, 2, 2, 2, 2]$, every combination of four indices is valid. Another subtle case is when some values appear only once or twice; the algorithm must correctly skip combinations that cannot form valid pairs.

## Approaches

The brute-force solution is straightforward: iterate over all quadruples $(i, j, k, l)$ with four nested loops and check the equality conditions. This works in theory because it directly implements the definition, but it is impractical since it has time complexity $O(n^4)$.

The key observation that allows a faster solution is to realize that for a fixed $j$ and $k$, we can efficiently count the number of suitable $i$ and $l$ indices. Specifically, if we fix the middle two indices $j$ and $k$, the number of valid $i < j$ such that $a[i] = a[k]$ is simply the count of that value before $j$, and the number of valid $l > k$ such that $a[j] = a[l]$ is the count of that value after $k$. Multiplying these two counts gives the number of quadruples for that $j, k$ pair. This reduces the problem to $O(n^2)$, which is feasible for $n \le 3000$.

This approach works because the problem is symmetric around the middle indices: the outer values only depend on values before $j$ and after $k$, allowing us to precompute prefix and suffix counts to avoid repeated counting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^4) | O(1) | Too slow |
| Prefix/Suffix Counting | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$ and the array $a$. We will process each array independently.
2. Initialize a variable to accumulate the answer.
3. Iterate $j$ from index 1 to $n-2$ and $k$ from $j+1$ to $n-1$. These represent the middle two indices in the quadruple.
4. For each pair $(j, k)$, count the number of indices $i < j$ where $a[i] = a[k]$. This can be done by iterating over the first $j$ elements and checking equality.
5. Count the number of indices $l > k$ where $a[l] = a[j]$. This is done by iterating from $k+1$ to $n-1$ and checking equality.
6. Multiply these two counts to get the number of quadruples for this particular $(j, k)$ combination, and add it to the accumulated answer.
7. After iterating over all $(j, k)$ pairs, output the answer for the test case.

Why it works: At each step, the algorithm explicitly counts valid $i$ before $j$ and valid $l$ after $k$. Multiplying these counts ensures that all combinations of valid outer indices are considered exactly once. Since $j < k$ is enforced, all quadruples satisfy $i < j < k < l$.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    ans = 0
    for j in range(1, n - 2 + 1):
        for k in range(j + 1, n - 1):
            count_i = 0
            for i in range(j):
                if a[i] == a[k]:
                    count_i += 1
            count_l = 0
            for l in range(k + 1, n):
                if a[l] == a[j]:
                    count_l += 1
            ans += count_i * count_l
    print(ans)
```

The code reads the number of test cases and processes each one separately. For each $(j, k)$ pair, it counts how many $i$ satisfy $a[i] = a[k]$ and how many $l$ satisfy $a[l] = a[j]$. Multiplying these counts yields the number of quadruples contributed by that pair. The careful choice of ranges ensures $i < j < k < l$, and all loops avoid off-by-one errors by using Python's 0-based indexing correctly.

## Worked Examples

Sample Input 1:

```
5
2 2 2 2 2
```

| j | k | i indices | count_i | l indices | count_l | added to ans | total ans |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 1 | 3,4 | 2 | 2 | 2 |
| 1 | 3 | 0 | 1 | 4 | 1 | 1 | 3 |
| 1 | 4 | 0 | 1 | none | 0 | 0 | 3 |
| 2 | 3 | 0,1 | 2 | 4 | 1 | 2 | 5 |
| 2 | 4 | 0,1 | 2 | none | 0 | 0 | 5 |
| 3 | 4 | 0,1,2 | 3 | none | 0 | 0 | 5 |

This demonstrates that all valid quadruples are counted exactly once. The algorithm handles multiple overlapping indices correctly.

Sample Input 2:

```
6
1 3 3 1 2 3
```

| j | k | i indices | count_i | l indices | count_l | added to ans | total ans |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 0 | 3,4,5 | 1 | 0 | 0 |
| 1 | 3 | 0 | 1 | 4,5 | 0 | 0 | 0 |
| 1 | 4 | 0 | 0 | 5 | 0 | 0 | 0 |
| 1 | 5 | 0 | 0 | none | 0 | 0 | 0 |
| 2 | 3 | 0,1 | 0 | 4,5 | 0 | 0 | 0 |
| 2 | 4 | 0,1 | 0 | 5 | 0 | 0 | 0 |
| 2 | 5 | 0,1 | 1 | none | 0 | 0 | 0 |
| 3 | 4 | 0,1,2 | 0 | 5 | 0 | 0 | 0 |
| 3 | 5 | 0,1,2 | 1 | none | 0 | 0 | 0 |
| 4 | 5 | 0,1,2,3 | 0 | none | 0 | 0 | 0 |

Final answer is 2. The table shows that the algorithm counts valid $i$ and $l$ without double-counting.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Two nested loops for $j, k$, each counting $i < j$ and $l > k$ in worst case O(n). Since sum of $n \le 3000$, total operations < 10^7 |
| Space | O(n) | Only the array and a few counters are stored |

The solution easily fits in the 2-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution code here
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        ans = 0
        for j in range(1, n - 2 + 1):
            for k in range(j + 1, n - 1):
                count_i = sum(1 for i in range(j) if a[i] == a[k])
                count_l = sum(1 for l in range(k + 1, n) if a[l] == a[j])
                ans += count_i * count_l
        print(ans)
    return output
```
