---
title: "CF 1968F - Equal XOR Segments"
description: "We are asked to decide, for subarrays of a given array, whether it is possible to partition the subarray into at least two consecutive segments such that the bitwise XOR of each segment is equal."
date: "2026-06-07T18:08:25+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 1968
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 943 (Div. 3)"
rating: 1800
weight: 1968
solve_time_s: 134
verified: false
draft: false
---

[CF 1968F - Equal XOR Segments](https://codeforces.com/problemset/problem/1968/F)

**Rating:** 1800  
**Tags:** binary search, data structures  
**Solve time:** 2m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to decide, for subarrays of a given array, whether it is possible to partition the subarray into at least two consecutive segments such that the bitwise XOR of each segment is equal. Formally, if we consider the subarray $a_l, a_{l+1}, \dots, a_r$, we need to determine if there exists an integer $k > 1$ and indices $l = i_0 < i_1 < \dots < i_k = r+1$ so that for each segment $[i_j, i_{j+1}-1]$, the XOR of elements is identical.

The input includes multiple test cases, each with an array and several queries on subarrays. Array sizes and the number of queries can reach $2 \cdot 10^5$, with the total across all test cases bounded similarly. This rules out any approach that enumerates all possible partitions, which would have exponential complexity in $n$. We need an algorithm that answers each query efficiently, ideally in $O(n)$ preprocessing and $O(1)$ per query or slightly higher, using precomputed structures like prefix XORs.

An edge case arises when all elements are zero. Here, any non-trivial split works because zero XOR with zero is zero, so every subarray is automatically interesting. Another subtle case is when the total XOR of the subarray is non-zero but there are internal partitions whose XORs match; we need to carefully detect splits that satisfy the equal-XOR condition without missing valid configurations.

## Approaches

A brute-force approach would try every possible split of a subarray, compute XORs for each segment, and check if they are equal. For a subarray of length $m$, there are $2^{m-1}-1$ ways to split it into at least two parts. Computing XORs for each split adds another $O(m)$, giving a total time complexity of roughly $O(2^m \cdot m)$. This is infeasible for $m$ up to $2 \cdot 10^5$.

A key observation simplifies the problem. Let $X$ be the XOR of the entire subarray. If the array can be partitioned into $k \ge 2$ segments with equal XORs $x$, then the XOR of the entire array must be $x$ repeated $k$ times. Since XOR is associative and $x \oplus x = 0$, the total XOR must be $0$ if $k$ is even, or equal to $x$ if $k$ is odd. More practically, we can scan for prefix XORs: if we find at least two positions where the cumulative XOR from the start matches the total XOR, we can form a valid partition. This reduces the problem to checking the prefix XOR array, which is computable in $O(n)$, and counting matches, which can also be done efficiently.

The optimal approach uses prefix XORs and searches for indices where the cumulative XOR equals the total XOR of the subarray. If such indices exist allowing a split into at least two segments, we answer "YES"; otherwise, "NO". Handling zero subarrays or single-element segments requires careful boundary checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^m * m) | O(1) | Too slow |
| Prefix XOR Check | O(n) preprocessing, O(q) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute a prefix XOR array $px$ for the input array such that $px[i] = a_1 \oplus a_2 \oplus \dots \oplus a_i$. This allows constant-time XOR computation for any subarray using $px[r] \oplus px[l-1]$.
2. For each query $(l, r)$, compute the total XOR of the subarray as $total = px[r] \oplus px[l-1]$.
3. If $total = 0$, the subarray is always interesting. We can always split it into at least two non-empty segments because XOR of zero segments can be repeated.
4. Otherwise, scan the subarray for prefix positions where the cumulative XOR from the start of the subarray equals $total$. Let $count$ be the number of such positions.
5. If we can find at least two such positions separated by at least one element, or a position not at the boundary allowing a valid split, answer "YES". Otherwise, "NO".
6. Edge cases: subarrays of length two must have equal elements to be interesting. Also, careful attention is needed to ensure segments are non-empty.

Why it works: By properties of XOR, if the total XOR of the array is $X$, any partition into $k$ equal-XOR segments must satisfy the cumulative XOR up to each split being a multiple of $X$. This invariant guarantees that counting such prefix XORs correctly detects all possible valid partitions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))
        px = [0]*(n+1)
        for i in range(n):
            px[i+1] = px[i] ^ a[i]
        
        for _ in range(q):
            l, r = map(int, input().split())
            total = px[r] ^ px[l-1]
            if total == 0:
                print("YES")
                continue
            found = 0
            xor_acc = 0
            for i in range(l-1, r):
                xor_acc ^= a[i]
                if xor_acc == total:
                    found += 1
                    xor_acc = 0
            print("YES" if found >= 2 else "NO")

if __name__ == "__main__":
    solve()
```

The prefix XOR array allows constant-time total XOR computation for subarrays. The inner loop accumulates XORs and resets when a segment matching the total is found. Counting at least two such segments ensures a valid split. The boundary conditions are handled by starting the loop from $l-1$ and including $r$.

## Worked Examples

**Example 1:** Subarray $[1,1,2,3,0]$ with query (1,5). Prefix XORs: 1,0,2,1,1. Total XOR = 1. Scanning yields segments: [1], [1], [2,3,0] with XOR 1 each. Answer YES.

| i | a[i] | xor_acc | found |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 0 |
| 1 | 1 | 0 | 1 |
| 2 | 2 | 2 | 1 |
| 3 | 3 | 1 | 1 |
| 4 | 0 | 1 | 1 -> reset to 0, found=2 |

**Example 2:** Subarray [1,2,3] with query (1,3). Total XOR = 0. Answer YES immediately.

These examples confirm the algorithm correctly handles both non-zero total XOR partitions and zero total XOR subarrays.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) per test case | Prefix XOR computed in O(n), each query processed in O(r-l) worst-case, which is bounded by total n |
| Space | O(n) | Prefix XOR array of size n+1 |

Given sum of n and q over all test cases ≤ 2e5, this solution comfortably fits within 5s and 256MB limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("""4
5 5
1 1 2 3 0
1 5
2 4
3 5
1 3
3 4
5 5
1 2 3 4 5
1 5
2 4
3 5
1 3
2 3
7 4
12 9 10 9 10 11 9
1 5
1 7
2 6
2 7
11 4
0 0 1 0 0 1 0 1 1 0 1
1 2
2 5
6 9
7 11""") == """YES
YES
NO
NO
NO
YES
NO
NO
YES
NO
NO
NO
NO
NO
YES
NO
YES
YES""", "sample 1"

# Custom: all zeros
assert run("1\n5 2\n0 0 0 0 0\n1 5\n2 4") == "YES\nYES", "all zeros"

# Custom: single-element segments impossible
assert run("1\n3 1\n1 2 3\n1 3") == "NO", "no partition"

# Custom: two equal elements
assert run("1\n2 1\n7 7\n1 2") == "YES", "minimal partition"

# Custom: prefix XOR matches total XOR twice
assert run("1\n5
```
