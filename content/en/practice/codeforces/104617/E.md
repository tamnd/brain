---
title: "CF 104617E - Cone Coloring"
description: "We are given a line of colored dyes, each dye having a positive integer value that represents how “beautiful” it is."
date: "2026-06-29T18:22:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104617
codeforces_index: "E"
codeforces_contest_name: "UTPC Contest 09-22-23 Div. 2 (Beginner)"
rating: 0
weight: 104617
solve_time_s: 74
verified: true
draft: false
---

[CF 104617E - Cone Coloring](https://codeforces.com/problemset/problem/104617/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of colored dyes, each dye having a positive integer value that represents how “beautiful” it is. We want to choose a subset of these dyes to maximize the total beauty sum, but with one restriction: we are not allowed to pick two dyes that are next to each other in the original line.

In more concrete terms, this is a sequence of numbers, and we must select a subset of indices such that no two selected indices are consecutive. The goal is to maximize the sum of the selected values.

The input size can go up to 100,000 elements. A solution that tries all subsets of indices is impossible because the number of subsets is exponential. Even a quadratic approach that checks all pairs would be too slow at this scale. The constraints strongly suggest a linear or near-linear dynamic programming solution where each element is processed once and we reuse previously computed results.

A few edge cases deserve attention. If there is only one dye, the answer is simply that dye’s value.

For example, input:

```
1
7
```

The correct output is:

```
7
```

A naive approach that assumes at least two elements and initializes DP incorrectly might return 0 or crash.

If all values are equal, say:

```
4
5 5 5 5
```

The optimal strategy is to pick alternating elements, giving 5 + 5 = 10. Any greedy approach that always picks locally optimal adjacent choices can fail if it does not properly enforce global spacing.

Another subtle case arises when a very large value is surrounded by two medium values. For example:

```
3
1 100 1
```

The correct answer is 100, not 2 or 101 depending on flawed greedy logic. This shows why local decisions like “always take the bigger of adjacent elements” are incorrect.

## Approaches

A brute-force solution would try every subset of indices and check whether it is valid (no two consecutive picks), then compute its sum. This works conceptually because it directly enforces the constraint, but it requires iterating over all subsets of size 2^N. Even if we improve slightly by generating subsets with backtracking and pruning adjacent picks, the worst case still explores an exponential number of states, which becomes infeasible long before N reaches even 40.

The structure of the problem suggests that the decision at position i depends only on whether we take i or skip it. If we take i, then i-1 cannot be taken. If we skip i, then we inherit the best result up to i-1. This creates a simple optimal substructure over prefixes of the array.

Let dp[i] represent the maximum beauty sum we can achieve using only the first i dyes. For each position i, we have two choices: either we do not take b[i], in which case we keep dp[i-1], or we take b[i], in which case we must add it to dp[i-2]. This gives a direct recurrence and reduces the problem to a linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^N) | O(N) | Too slow |
| Dynamic Programming | O(N) | O(N) (or O(1)) | Accepted |

## Algorithm Walkthrough

We process the array from left to right while maintaining the best possible answer for each prefix.

1. Define dp[0] = 0, since with no elements we cannot pick anything.
2. Define dp[1] = b[0], since with one element we either take it or have nothing better.
3. For each index i from 2 to N - 1, compute dp[i] as follows:

We compare skipping the current element versus taking it. Skipping gives dp[i-1]. Taking it gives dp[i-2] + b[i]. We choose the maximum of these two.
4. After processing all elements, dp[N-1] contains the answer.

A more memory-efficient version keeps only the last two DP states instead of the full array.

### Why it works

At each index i, any valid selection over the prefix [0..i] must fall into exactly one of two categories: it either includes i or it does not. If it includes i, then i-1 is forbidden, and the remaining contribution must come from an optimal solution over [0..i-2]. If it excludes i, then the best possible value is exactly the optimal solution over [0..i-1]. These two cases cover all possibilities without overlap, so taking the maximum preserves optimality at every prefix. Because every prefix solution is built from smaller optimal prefixes, no later decision can invalidate earlier optimal choices.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    b = list(map(int, input().split()))
    
    if n == 1:
        print(b[0])
        return
    
    prev2 = 0
    prev1 = b[0]
    
    for i in range(1, n):
        cur = max(prev1, prev2 + b[i])
        prev2 = prev1
        prev1 = cur
    
    print(prev1)

if __name__ == "__main__":
    solve()
```

The implementation compresses the DP array into two variables. `prev1` represents dp[i-1], and `prev2` represents dp[i-2]. At each step, we compute whether taking the current value plus `prev2` beats skipping it and keeping `prev1`.

The single-element case is handled explicitly to avoid referencing an uninitialized dp state. Without this, `prev2 + b[i]` would be invalid for i = 1.

## Worked Examples

### Example 1

Input:

```
5
5 10 9 10 7
```

| i | b[i] | skip (dp[i-1]) | take (dp[i-2] + b[i]) | dp[i] |
| --- | --- | --- | --- | --- |
| 0 | 5 | - | 5 | 5 |
| 1 | 10 | 5 | 10 | 10 |
| 2 | 9 | 10 | 14 | 14 |
| 3 | 10 | 14 | 20 | 20 |
| 4 | 7 | 20 | 21 | 21 |

The table shows how the decision at each index balances immediate gain against skipping for future benefit. The final answer is 21, achieved by selecting indices 1, 3, and 4? Actually indices 1 and 3 give 20, but the optimal is indices 0, 1, 3? That violates adjacency, so correct selection is 0, 1 is invalid. The actual optimal structure is 5 + 9 + 7 is invalid due to adjacency constraints. The DP correctly resolves this by enforcing prefix optimality rather than explicit subset construction.

### Example 2

Input:

```
3
1 100 1
```

| i | b[i] | skip | take | dp[i] |
| --- | --- | --- | --- | --- |
| 0 | 1 | - | 1 | 1 |
| 1 | 100 | 1 | 100 | 100 |
| 2 | 1 | 100 | 2 | 100 |

The optimal strategy selects the middle element only. The DP correctly avoids the temptation to combine both ends.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each element is processed once with O(1) transitions |
| Space | O(1) | Only two rolling DP variables are stored |

The linear scan easily fits within the constraints for N up to 100,000, and constant memory usage ensures no overhead from large arrays.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return str(solve_output(inp)).strip()

def solve_output(inp: str):
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline())
    b = list(map(int, sys.stdin.readline().split()))
    
    if n == 1:
        return b[0]
    
    prev2 = 0
    prev1 = b[0]
    
    for i in range(1, n):
        cur = max(prev1, prev2 + b[i])
        prev2 = prev1
        prev1 = cur
    
    return prev1

# provided sample
assert solve_output("5\n5 10 9 10 7\n") == 21

# minimum size
assert solve_output("1\n7\n") == 7

# all equal
assert solve_output("4\n5 5 5 5\n") == 10

# alternating high values
assert solve_output("5\n10 1 10 1 10\n") == 30

# increasing sequence
assert solve_output("5\n1 2 3 4 5\n") == 9
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 7 | base case handling |
| all equal | 10 | alternating optimal selection |
| alternating highs | 30 | correct skipping structure |
| increasing | 9 | non-greedy optimal DP behavior |

## Edge Cases

For a single-element array like:

```
1
7
```

the algorithm sets `prev1 = b[0]` and never enters the loop. The output is directly 7, which matches the correct answer because the only valid subset contains that element.

For a case with alternating high values like:

```
5
10 1 10 1 10
```

the DP evolves as follows: starting from 10, then 10, then 20, then 20, then 30. At each step, skipping or taking is evaluated globally, so the algorithm correctly selects all three 10s while avoiding adjacent picks.
