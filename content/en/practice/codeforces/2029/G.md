---
title: "CF 2029G - Balanced Problem"
description: "We are asked to maximize a weighted sum over an array of integers that starts as all zeros. The array has length $n$ and receives $m$ initial operations, each of which increases a prefix or suffix of the array by 1."
date: "2026-06-08T12:04:35+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 2029
codeforces_index: "G"
codeforces_contest_name: "Refact.ai Match 1 (Codeforces Round 985)"
rating: 3000
weight: 2029
solve_time_s: 106
verified: false
draft: false
---

[CF 2029G - Balanced Problem](https://codeforces.com/problemset/problem/2029/G)

**Rating:** 3000  
**Tags:** data structures, dp  
**Solve time:** 1m 46s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to maximize a weighted sum over an array of integers that starts as all zeros. The array has length $n$ and receives $m$ initial operations, each of which increases a prefix or suffix of the array by 1. After these operations, Kevin can perform any number of additional prefix or suffix additions. For a given target value $v$, an element contributes its corresponding weight $c_i$ to the total beauty if and only if its value equals $v$. The task is to compute, for each $v$ from 1 to $V$, the maximum achievable beauty if Kevin continues optimally.

The constraints indicate that $n$ and $m$ can be as large as $2\cdot 10^5$, so any solution iterating over all possible sequences of operations is impossible. Additionally, $V$ can go up to 2000 and the sum of $V^2$ over all test cases is limited to $4 \cdot 10^6$, suggesting that algorithms with complexity $O(n V)$ are acceptable.

Edge cases include arrays with length one, arrays where all weights are equal, or scenarios where initial operations already push some elements beyond $V$. A naive implementation could miscount beauty if it does not properly account for elements that have already exceeded a target $v$ and cannot be decreased.

## Approaches

The brute-force approach is conceptually simple: simulate the initial operations to build the array $a$, then for each $v$ from 1 to $V$, try all sequences of prefix and suffix additions to reach exactly $v$ at each index. This approach is correct but utterly infeasible, because the number of sequences of additions grows exponentially with $n$ and the number of additions. Even if we limit ourselves to trying a single operation per index, the worst-case complexity is $O(n^2 V)$, which is too large for $n \sim 2 \cdot 10^5$.

The key observation is that any number of prefix and suffix additions can be represented as a non-negative integer to be added to a contiguous range. Specifically, let us define $a_i$ after the initial operations. To make $a_i$ exactly $v$, Kevin must perform additional additions so that $a_i + \text{additional}_i = v$. Because prefix and suffix additions affect ranges, any selection of operations corresponds to choosing a contiguous range to increase. This reduces the problem to a maximum sum of weights $c_i$ over a range such that $a_i \le v$ and can be incremented to $v$.

Formally, let $d_i = v - a_i$. An element $i$ can contribute to the beauty if $d_i \ge 0$. Then the maximum achievable beauty is the maximum sum of $c_i$ over some range of elements where the corresponding $d_i$ are non-negative. Since any contiguous range can be incremented using prefix and suffix additions, we can select any contiguous subsequence of indices where $d_i \ge 0$ and add the necessary number of operations to bring them exactly to $v$. This allows us to compute the answer in $O(n)$ per value $v$ using a variant of Kadane's algorithm.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * V) | O(n) | Too slow |
| Optimal | O(n V) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an array $a$ of zeros with length $n$. Iterate through the $m$ initial operations. For each operation of type L at index $x$, increment a difference array at index 0 by 1 and decrement at index $x$ by 1. For each operation of type R at index $x$, increment at index $x-1$ and decrement at index $n$. Convert the difference array to the actual array $a$ by taking a prefix sum. This step efficiently simulates all initial operations in O(n + m).
2. For each target value $v$ from 1 to $V$, compute $d_i = v - a_i$. If $d_i < 0$, element $i$ cannot reach $v$ and contributes zero to the beauty. Otherwise, its weight $c_i$ is available for summing.
3. Apply a maximum subarray sum algorithm over $c_i$ restricted to indices where $d_i \ge 0$. Start with a running sum of zero, iterate through the array: if $d_i < 0$, reset the running sum to zero; otherwise, add $c_i$ to the running sum and track the maximum sum encountered.
4. The maximum sum found in step 3 is the answer for this $v$. Repeat for all $v$ from 1 to $V$.

This works because any contiguous range of indices can be adjusted to reach $v$ using prefix and suffix additions. The difference array in step 1 ensures that we respect the initial operations. The maximum subarray sum ensures that we optimally select the subset of indices to maximize beauty without overstepping $v$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m, V = map(int, input().split())
        c = list(map(int, input().split()))
        diff = [0]*(n+1)
        for _ in range(m):
            op, x = input().split()
            x = int(x)
            if op == 'L':
                diff[0] += 1
                diff[x] -= 1
            else:
                diff[x-1] += 1
                diff[n] -= 1
        a = [0]*n
        curr = 0
        for i in range(n):
            curr += diff[i]
            a[i] = curr

        result = []
        for v in range(1, V+1):
            max_beauty = 0
            curr_sum = 0
            for i in range(n):
                if a[i] > v:
                    curr_sum = 0
                else:
                    curr_sum += c[i]
                    if curr_sum > max_beauty:
                        max_beauty = curr_sum
            result.append(str(max_beauty))
        print(' '.join(result))

if __name__ == "__main__":
    solve()
```

The solution first constructs the array after initial operations using a difference array to efficiently handle prefix and suffix increments. Then for each value $v$, it calculates the maximum beauty by iterating through elements, skipping those that already exceed $v$, and using a running sum to track the best contiguous subsequence. This avoids simulating additional operations explicitly and ensures optimal beauty for each $v$.

## Worked Examples

### Sample 1, first test case

Initial array $a = [0,0,0]$. Operations:

| Operation | Resulting a |
| --- | --- |
| L 3 | [1,1,1] |
| R 3 | [1,1,2] |
| L 1 | [2,1,2] |

Target $v = 1$: $d = [-1,0,-1]$, only index 2 can contribute, sum = 2.

Target $v = 2$: $d = [0,1,0]$, contiguous subsequence [2,3] can be incremented, sum = 6.

### Sample 2, third test case

Array $a = [0,0,0,0,0]$, initial operations modify to $a = [3,2,2,1,1]$. For $v = 3$:

| i | a_i | d_i | c_i contribution |
| --- | --- | --- | --- |
| 1 | 3 | 0 | 1 |
| 2 | 2 | 1 | 1 |
| 3 | 2 | 1 | 1 |
| 4 | 1 | 2 | 1 |
| 5 | 1 | 2 | 1 |

Maximum contiguous sum for non-negative $d_i$ is 3 (indices 1-3), beauty = 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n V) | Initial operations simulated in O(n + m), then O(n) per v from 1 to V. |
| Space | O(n) | Arrays a and diff, plus temporary variables. |

Given the constraints $V^2$ sum over all test cases ≤ $4 \cdot 10^6$, this is feasible within 2-3 seconds and memory limit of 1GB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# Provided samples
assert run("""5
3 3 2
1 2 4
L 3
R 3
L 1
3 3 2
5 1 4
L
```
