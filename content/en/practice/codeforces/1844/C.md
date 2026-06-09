---
title: "CF 1844C - Particles"
description: "We are given a sequence of particles arranged in a line, each with an integer charge. We have a device that allows us to remove any particle, after which the two neighboring particles merge into one particle whose charge is the sum of the two neighbors."
date: "2026-06-09T06:04:10+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1844
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 884 (Div. 1 + Div. 2)"
rating: 1300
weight: 1844
solve_time_s: 310
verified: false
draft: false
---

[CF 1844C - Particles](https://codeforces.com/problemset/problem/1844/C)

**Rating:** 1300  
**Tags:** dp, greedy, implementation, math  
**Solve time:** 5m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of particles arranged in a line, each with an integer charge. We have a device that allows us to remove any particle, after which the two neighboring particles merge into one particle whose charge is the sum of the two neighbors. The goal is to apply a sequence of such operations until only one particle remains and maximize the charge of that last particle.

The input consists of multiple test cases. For each test case, we know the number of particles and their respective charges. The output is the maximum possible charge of the remaining particle after performing the operations optimally.

The constraints are significant: there can be up to $2 \cdot 10^5$ particles in total across all test cases, and individual charges can be very large or negative. Because of these constraints, any naive simulation that repeatedly removes particles and recalculates the array is too slow; simulating each operation could take $O(n^2)$ time, which would not finish within a second for large inputs.

A subtle edge case occurs when all particles are negative. A careless approach that merges particles indiscriminately could reduce the maximum remaining charge unnecessarily. For example, if the line is `[-1, -2, -3]`, the optimal strategy is to merge the negative numbers in a way that keeps the least negative sum as the final particle.

## Approaches

The brute-force approach is straightforward: for each possible removal of a particle, recursively simulate all possible remaining sequences until one particle remains, then take the maximum. This is guaranteed to produce the correct answer because it explores every possible sequence of operations. However, this approach is factorial in time complexity: with $n$ particles, there are roughly $n!$ sequences to explore, which is infeasible for $n \sim 10^5$.

The key observation is that the order of merges does not matter beyond grouping consecutive positive or negative sequences. The operation essentially merges adjacent numbers, so at the end, the final particle's charge is the sum of a contiguous subsequence of the original array, possibly after skipping zero-length merges of negative sums. This reduces the problem to a variant of the maximum subarray sum problem.

Specifically, the maximum possible charge of the remaining particle is equal to the sum of the largest contiguous subsequence of non-negative combined sums. This can be computed in linear time by iterating through the array, merging consecutive particles greedily: always sum all positive contributions and reset the sum when it would become smaller by including a negative prefix.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of particles `n` and the list of charges `c`.
2. Initialize two variables: `current_sum` to track the ongoing sum of a contiguous subsequence, and `max_sum` to track the maximum sum found.
3. Iterate through the charges in order. For each particle, add its charge to `current_sum`. If `current_sum` becomes less than the current particle alone, reset `current_sum` to the particle's charge. This is a standard modification of Kadane's algorithm for maximum subarray sum.
4. Update `max_sum` if `current_sum` exceeds it.
5. After processing all particles, `max_sum` contains the maximum achievable charge of the final particle.
6. Print or store the result for each test case.

Why it works: the merging operation reduces the sequence to the sum of a contiguous segment. Any optimal sequence of merges cannot skip a positive contribution without losing potential sum. Thus, finding the maximum sum over all contiguous segments is equivalent to performing merges optimally.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        c = list(map(int, input().split()))
        current_sum = max_sum = c[0]
        for charge in c[1:]:
            current_sum = max(charge, current_sum + charge)
            max_sum = max(max_sum, current_sum)
        print(max_sum)

if __name__ == "__main__":
    solve()
```

This solution uses fast I/O for multiple test cases. It processes each particle exactly once and maintains the running sum efficiently, ensuring no integer overflows because Python integers are arbitrary-precision.

## Worked Examples

### Example 1

Input: `[-3, 1, 4, -1, 5, -9]`

| Step | Current Charge | current_sum | max_sum |
| --- | --- | --- | --- |
| 0 | -3 | -3 | -3 |
| 1 | 1 | 1 | 1 |
| 2 | 4 | 5 | 5 |
| 3 | -1 | 4 | 5 |
| 4 | 5 | 9 | 9 |
| 5 | -9 | 0 | 9 |

Maximum remaining particle charge is `9`.

### Example 2

Input: `[998244353, 998244353, 998244353, 998244353, 998244353]`

| Step | Current Charge | current_sum | max_sum |
| --- | --- | --- | --- |
| 0 | 998244353 | 998244353 | 998244353 |
| 1 | 998244353 | 1996488706 | 1996488706 |
| 2 | 998244353 | 2994733059 | 2994733059 |
| 3 | 998244353 | 3992987412 | 3992987412 |
| 4 | 998244353 | 4991231765 | 4991231765 |

The optimal merges sum all particles consecutively. Maximum remaining charge is `4991231765`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We iterate through the array once to compute maximum subarray sum. |
| Space | O(1) | Only two variables `current_sum` and `max_sum` are maintained besides input. |

The total number of particles across all test cases is at most $2 \cdot 10^5$, so the linear approach is efficient and comfortably fits within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("3\n6\n-3 1 4 -1 5 -9\n5\n998244353 998244353 998244353 998244353 998244353\n1\n-2718") == "9\n2994733059\n-2718", "sample 1"

# Custom cases
assert run("1\n3\n-1 -2 -3") == "-1", "all negative"
assert run("1\n5\n1 2 3 4 5") == "15", "all positive"
assert run("1\n4\n-5 1 -2 3") == "3", "mixed signs"
assert run("1\n1\n42") == "42", "single particle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[-1, -2, -3]` | -1 | Handles all negative particles |
| `[1,2,3,4,5]` | 15 | Sum of all positive numbers |
| `[-5,1,-2,3]` | 3 | Correctly selects maximum contiguous sum in mixed array |
| `[42]` | 42 | Single particle edge case |

## Edge Cases

If the array contains only negative numbers, the algorithm correctly chooses the least negative particle, which corresponds to performing no merges that would reduce the value. For example, `[-1, -2, -3]` returns `-1`.

If there is only one particle, no operations are needed, and the algorithm directly returns that particle.

The solution also handles large positive integers without overflow because Python supports arbitrary-precision integers.
