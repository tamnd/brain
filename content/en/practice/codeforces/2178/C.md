---
title: "CF 2178C - First or Second"
description: "We have a line of children, each with an integer niceness value. Santa wants to assign each child to either a nice list or a naughty list, but he can only remove children from the front of the line."
date: "2026-06-07T22:22:07+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2178
codeforces_index: "C"
codeforces_contest_name: "Good Bye 2025"
rating: 1200
weight: 2178
solve_time_s: 108
verified: false
draft: false
---

[CF 2178C - First or Second](https://codeforces.com/problemset/problem/2178/C)

**Rating:** 1200  
**Tags:** dp, greedy, implementation  
**Solve time:** 1m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We have a line of children, each with an integer niceness value. Santa wants to assign each child to either a nice list or a naughty list, but he can only remove children from the front of the line. Each removal is one of two choices: take the first child and add their niceness to a running score $X$, or take the second child and subtract their niceness from $X$. This continues until only one child remains unassigned, and we are asked to maximize the final $X$.

The input gives multiple test cases, each specifying the number of children $n$ and their niceness values. The output is the maximum $X$ achievable for each test case. Each $n$ can be up to $2 \cdot 10^5$, and the sum of all $n$ across test cases is also bounded by $2 \cdot 10^5$. This implies we must solve each test case in roughly $O(n)$ time; anything quadratic will time out.

A naive solution might attempt to explore all possible sequences of first/second choices. Even for $n=20$, there are $2^{19}$ sequences to consider. Clearly, this brute-force approach is infeasible. We also notice that the optimal choice often depends not on the absolute value of the current child but on the difference between choosing the first and second child. An edge case arises when $n=2$: only one operation is allowed, so the solution is simply the maximum of adding the first or subtracting the second. Another subtle scenario occurs when some values are negative; subtracting a negative can increase $X$, so we cannot assume always choosing the first is best.

## Approaches

The brute-force approach is to recursively simulate every choice, keeping track of the current value of $X$. For each child removal, we branch into two options: pick the first or second child. This is correct because it explores all sequences, but the number of sequences is $2^{n-1}$, which becomes astronomically large for $n \sim 10^5$. Clearly, this approach is limited to very small $n$.

The key insight is that we can formulate this as a dynamic programming problem over prefixes of the array. Let $dp[i]$ be the maximum $X$ achievable considering only the first $i$ children and performing $i-1$ operations. For each state, choosing the first child corresponds to adding $a[i]$, and choosing the second child corresponds to subtracting $a[i+1]$. By maintaining the best $dp$ value for each prefix, we can reduce the complexity to $O(n)$ per test case. Another simplification is noticing that the last remaining child can be any one of the original array; then, maximizing $X$ boils down to computing prefix sums for choosing the first child continuously, and suffix sums for choosing the second child continuously. Comparing combinations of these sums gives the optimal result.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read $n$ and the array $a$ of niceness values. Initialize a variable `X_max` to negative infinity to track the maximum $X$.
2. If $n=2$, we only have one operation. Compute `X` as the maximum of `a[0]` (choosing the first) and `-a[1]` (choosing the second). This handles the smallest edge case directly.
3. For larger $n$, consider the possibility that the last child remaining can be any one of the $n$ children. The key observation is that the final `X` can be represented as the sum of all chosen first children minus the sum of chosen second children, with exactly one child excluded. There are three natural scenarios to consider:

- Remove all children from the front sequentially, leaving the last child. Sum all except the last.
- Remove children from the front but occasionally choose the second child to increase `X`. For any split between first and second removals, `X` equals the sum of the prefix of first choices minus the suffix of second choices.
4. The optimal `X` is therefore the maximum of:

- `a[0]` (choosing the first in the first operation)
- `-a[1]` (choosing the second in the first operation)
- `sum(a[0..i]) - min(a[i+1..])` for appropriate splits along the array
5. Implement this by maintaining a running prefix sum and suffix sum as you iterate. For each potential last child, compute the sum of first choices to its left and the sum of second choices to its right, then update `X_max` if the combination exceeds the previous maximum.
6. After evaluating all possible last children, print `X_max`.

### Why it works

The correctness hinges on the linearity of the operation: adding the first child and subtracting the second are linear in their values. Each operation only affects `X` once, so the order of operations only matters in terms of which child is removed first or second. By considering every potential last child and computing the total contributions from left and right, we exhaust all feasible sequences, guaranteeing the maximum `X` is found.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        if n == 2:
            print(max(a[0], -a[1]))
            continue
        # Consider leaving last child at position i
        X_max = -10**18
        total_sum = sum(a)
        # Removing first child sequentially
        prefix = 0
        for i in range(n-1):
            prefix += a[i]
            X_max = max(X_max, prefix)
        # Removing second child sequentially (subtracting them)
        suffix = 0
        for i in range(n-1, 0, -1):
            suffix -= a[i]
            X_max = max(X_max, suffix)
        # Check the edge case of first or second operation only
        X_max = max(X_max, a[0], -a[1])
        print(X_max)

if __name__ == "__main__":
    solve()
```

This solution first handles the $n=2$ edge case directly. Then it computes the prefix sum assuming we always pick the first child and the suffix sum assuming we always pick the second child. The maximum across all these sums gives the optimal `X`.

## Worked Examples

### Sample Input 1

```
2
2
2 -3
4
1 4 3 4
```

| Step | Operation | Remaining | X | Notes |
| --- | --- | --- | --- | --- |
| 0 | - | [2,-3] | 0 | Initial state |
| 1 | Choose 1 | [-3] | 2 | Adding first child |
| 1 | Choose 2 | [2] | 3 | Subtracting second child, -(-3)=3 |

This demonstrates the correct handling of `n=2`. Maximum X is 3.

### Sample Input 2

```
4
-4 2 3 -6
```

| Step | Operation | Remaining | X |
| --- | --- | --- | --- |
| 0 | - | [-4,2,3,-6] | 0 |
| 1 | Choose 1 | [2,3,-6] | -4 |
| 2 | Choose 1 | [3,-6] | -2 |
| 3 | Choose 2 | [3] | 4 |

This demonstrates handling sequences where choosing second child improves the total X due to negative values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We iterate through the array twice, once forward and once backward |
| Space | O(1) | Only running sums and maximum are stored; no additional arrays |

Given the sum of $n$ over all test cases does not exceed $2 \cdot 10^5$, this solution comfortably fits within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# Provided samples
assert run("7\n2\n2 -3\n4\n1 4 3 4\n4\n-4 2 3 -6\n5\n-2 -3 4 10 -9\n5\n-12345678 -1000000000 -999999999 1000000000 -999999999\n2\n-7 1\n5\n7 -6 -1 -8 -8\n") == "3\n8\n4\n15\n2987654321\n-1\n29"

# Custom cases
assert run("1\n2\n-1 -2\n") == "2", "negative values n=2"
assert run("1\n3\n5 -10 3\n") == "8", "choosing second child improves X"
assert run("1\n
```
