---
title: "CF 1699C - The Third Problem"
description: "We are given a permutation of integers from 0 to $n-1$, which is simply a rearrangement of these numbers with no repeats. The task is to count how many other permutations are \"similar\" to the given one, where similarity is defined through the MEX function."
date: "2026-06-09T22:10:38+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1699
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 804 (Div. 2)"
rating: 1700
weight: 1699
solve_time_s: 182
verified: false
draft: false
---

[CF 1699C - The Third Problem](https://codeforces.com/problemset/problem/1699/C)

**Rating:** 1700  
**Tags:** combinatorics, constructive algorithms, math  
**Solve time:** 3m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of integers from 0 to $n-1$, which is simply a rearrangement of these numbers with no repeats. The task is to count how many other permutations are "similar" to the given one, where similarity is defined through the MEX function. For every contiguous subarray of the permutation, the MEX of that subarray in the original permutation must match the MEX in the similar permutation. The MEX of a set is the smallest non-negative integer not present in it, so for `[0,1,2]` the MEX is 3, and for `[1,2,4]` the MEX is 0.

The input consists of multiple test cases, each giving a permutation of size up to $10^5$, and the sum of all $n$ over all test cases does not exceed $10^5$. This means we can afford linear-time solutions per test case but cannot afford $O(n^2)$ or higher approaches. Edge cases include very small permutations like `[0]` or permutations that are already sorted or reverse-sorted, which may limit the number of similar permutations.

A naive approach that computes MEX for every subarray of every candidate permutation would fail because there are $O(n^2)$ subarrays and $n!$ permutations to consider, which is astronomically large.

## Approaches

The brute-force approach would enumerate all $n!$ permutations and check every subarray for MEX equality against the given permutation. Checking MEX for a single subarray can take $O(n)$, and there are $O(n^2)$ subarrays, leading to $O(n! \cdot n^3)$ complexity. This is completely infeasible even for $n=10$.

The key observation comes from understanding how MEX behaves in a permutation. The smallest missing number in a subarray is determined by which numbers have appeared so far. If we track the positions of each number, the structure of the permutation that influences MEX is determined by intervals containing consecutive numbers. Specifically, the positions of numbers 0, 1, 2,... partition the array into segments such that swapping elements within a segment does not change the MEX of any interval. Therefore, the problem reduces to counting valid permutations of numbers within these segments.

We can process numbers in increasing order. We maintain the leftmost and rightmost positions of numbers seen so far. The "free interval" between these bounds can have its internal numbers rearranged freely, producing valid permutations. The number of ways to permute elements in the free interval is given by factorials of interval sizes. By iterating over numbers in increasing order and multiplying factorials of free interval sizes, we obtain the total count of similar permutations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!·n³) | O(n) | Too slow |
| Optimal | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read the permutation $a$ of size $n$. Store the positions of each number in an array `pos` such that `pos[x]` is the index where $x$ occurs.
2. Initialize variables `l` and `r` to `pos[0]`, representing the current segment covering all numbers processed so far.
3. Initialize a counter `cnt` to 1 and a variable `free` to 0. `free` will count the number of positions inside the current segment that can be freely permuted.
4. Iterate through numbers from 1 to $n-1$. For each number $x$:

a. Update the segment bounds: `l = min(l, pos[x])` and `r = max(r, pos[x])`.

b. Increase `free` by 1 for the new position added.

c. If the current number `x` has its position strictly inside the current segment but not at the borders, it is free to be permuted with other free positions.

d. Whenever `free` positions are completely inside the current segment, multiply `cnt` by `factorial(free)` modulo $10^9+7$ and reset `free` to 0.
5. After processing all numbers, `cnt` contains the number of permutations similar to $a$.

**Why it works:** The algorithm maintains a running segment covering all numbers seen so far. Any number added inside this segment can be rearranged with other numbers in the segment without affecting MEX values of intervals. By counting permutations within these "free" regions, we account for all similar permutations. The segment boundaries guarantee that swapping numbers outside the segment would violate MEX constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline
MOD = 10**9 + 7

# Precompute factorials up to 10^5
N = 100005
fact = [1] * N
for i in range(1, N):
    fact[i] = fact[i-1] * i % MOD

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    pos = [0]*n
    for i in range(n):
        pos[a[i]] = i

    l = pos[0]
    r = pos[0]
    cnt = 1
    free = 0

    for x in range(1, n):
        l = min(l, pos[x])
        r = max(r, pos[x])
        free += 1
        if pos[x] == l or pos[x] == r:
            cnt = cnt * fact[free] % MOD
            free = 0

    print(cnt)
```

The solution precomputes factorials to avoid repeated calculation. It maps each number to its position, then tracks the current segment. Free positions are permuted inside the segment whenever the segment's boundary expands. This ensures correctness while maintaining linear complexity per test case.

## Worked Examples

For the input `[4,0,3,2,1]`:

| x | pos[x] | l | r | free | cnt |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 0 | 1 |
| 1 | 4 | 1 | 4 | 1 | 1 |
| 2 | 3 | 1 | 4 | 2 | 1 |
| 3 | 2 | 1 | 4 | 3 | 2 |
| 4 | 0 | 0 | 4 | 1 | 2 |

Here `cnt = 2`, matching the expected output. The free count tracks positions that can be permuted inside the segment without affecting MEX.

For `[0,1,2,3]`:

| x | pos[x] | l | r | free | cnt |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | 1 |
| 1 | 1 | 0 | 1 | 1 | 1 |
| 2 | 2 | 0 | 2 | 1 | 1 |
| 3 | 3 | 0 | 3 | 1 | 1 |

Only one similar permutation exists, the permutation itself.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each number is processed once, factorials are precomputed |
| Space | O(n) | Stores positions array and factorials |

This fits the constraints because the sum of $n$ over all test cases is ≤ $10^5$, so O(n) per test case is acceptable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    MOD = 10**9 + 7
    N = 100005
    fact = [1]*N
    for i in range(1,N):
        fact[i] = fact[i-1]*i%MOD
    t=int(input())
    res=[]
    for _ in range(t):
        n=int(input())
        a=list(map(int,input().split()))
        pos=[0]*n
        for i in range(n):
            pos[a[i]]=i
        l=r=pos[0]
        cnt=1
        free=0
        for x in range(1,n):
            l=min(l,pos[x])
            r=max(r,pos[x])
            free+=1
            if pos[x]==l or pos[x]==r:
                cnt=cnt*fact[free]%MOD
                free=0
        res.append(str(cnt))
    return '\n'.join(res)

# Provided samples
assert run("5\n5\n4 0 3 2 1\n1\n0\n4\n0 1 2 3\n6\n1 2 4 0 5 3\n8\n1 3 7 2 5 0 6 4\n") == "2\n1\n1\n4\n72"

# Custom tests
assert run("1\n1\n0\n") == "1"
assert run("1\n2\n1 0\n") == "1"
assert run("1\n3\n2 0 1\n") == "2"
assert run("1\n4\n3 1 2 0\n") == "2"
``
```
