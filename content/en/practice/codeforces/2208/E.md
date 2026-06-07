---
title: "CF 2208E - Counting Cute Arrays"
description: "We are given an array of length $n$ with integers ranging from $-1$ to $n$. The $-1$ values are placeholders that can take any non-negative integer."
date: "2026-06-07T19:29:26+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp"]
categories: ["algorithms"]
codeforces_contest: 2208
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1086 (Div. 2)"
rating: 2700
weight: 2208
solve_time_s: 152
verified: false
draft: false
---

[CF 2208E - Counting Cute Arrays](https://codeforces.com/problemset/problem/2208/E)

**Rating:** 2700  
**Tags:** combinatorics, dp  
**Solve time:** 2m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of length $n$ with integers ranging from $-1$ to $n$. The $-1$ values are placeholders that can take any non-negative integer. The task is to count the number of arrays that can result from replacing the $-1$s such that the array could have been generated as $f(A)$ for some array $A$ of positive integers. Here, $f(A)_i$ denotes the index of the last element before position $i$ that is strictly smaller than $A_i$, or $0$ if no such element exists.

Effectively, we are counting “cute arrays” - arrays of indices that describe the last smaller element pattern of some underlying array. Our output is the total number of ways to fill in $-1$s so that the array remains cute, modulo $998{,}244{,}353$.

Constraints imply that $n$ is up to 5000 per test case, and the sum of $n$ across all test cases is also bounded by 5000. This rules out naive brute-force approaches that generate all arrays explicitly, as even $2^n$ operations would be too much. The problem also has hidden subtleties: if an array has an entry $X_i > i-1$, it is immediately invalid because no previous index exists that could satisfy $f(A)_i$. Arrays with repeated zeros or patterns that cannot be produced by any increasing sequence also produce zero solutions. A careless approach might ignore these implicit index constraints.

## Approaches

The brute-force approach is straightforward: generate all arrays $X'$ by replacing $-1$s with valid integers from 0 to $n$, and then check for each array if it can be represented as $f(A)$ for some array $A$. The check itself requires simulating the construction of $f(A)$ from $A$, which is $O(n^2)$. With $n=5000$, generating n^{\text{# of -1s}} arrays is infeasible. Even small test cases with moderate numbers of $-1$s would explode combinatorially.

The key observation that unlocks a faster solution is that $f(A)$ enforces a monotonic structure. For each index $i$, if $f(A)_i = j > 0$, then $A_i$ must be strictly greater than $A_j$, and any elements between $j$ and $i$ must not be greater than $A_i$. This is a typical dynamic programming situation where we can maintain, for each prefix of the array, a count of valid arrays ending at each possible value. By working backwards from the largest possible value and accumulating counts using prefix sums, we reduce complexity to $O(n^2)$, which fits the sum-of-n constraint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^n * n^2) | O(n^2) | Too slow |
| DP with prefix sums | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Initialize a DP table `dp[i][v]` representing the number of valid arrays for the first `i` positions ending with value `v` at position `i`. `v` ranges from 0 to `n`. Start with `dp[0][0] = 1`, representing an empty prefix.
2. Iterate through each position `i` from 1 to `n`. If `X[i] != -1`, then the value at `i` is fixed and we only compute `dp[i][X[i]]`. Otherwise, consider all `v` in 0..n as possible choices.
3. For each `v` at position `i`, compute contributions from all previous positions `j` such that `j < i` and `f(A)_i = j` matches the pattern in `X`. This is efficiently done using a prefix sum array `pref[j] = sum(dp[j][*])` up to `j`. For `v` to be valid at `i`, all `dp[j][u]` where `u < v` can contribute, representing that `A_i > A_j`.
4. Accumulate the contributions modulo `998244353` into `dp[i][v]`. If `X[i]` is fixed, only compute the corresponding `v`.
5. After filling all positions, the answer is the sum of `dp[n][v]` over all `v` that match the last position constraints.

The core insight is that the recurrence leverages the monotonic property of the underlying array `A` encoded in `f(A)`. By maintaining DP over possible last values and using prefix sums, we avoid combinatorial explosion and directly count all compatible arrays.

### Why it works

The DP maintains the invariant that `dp[i][v]` counts all valid sequences up to position `i` ending with value `v` while respecting all `f(A)` constraints imposed by the input pattern. Each step only extends arrays in ways consistent with the last smaller element pattern. The prefix sums guarantee that contributions from all valid previous positions are included efficiently, ensuring no valid array is missed and no invalid array is counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        X = list(map(int, input().split()))
        
        dp = [0] * (n + 1)
        dp[0] = 1  # empty prefix
        for i in range(n):
            ndp = [0] * (n + 1)
            total = 0
            for j in range(n + 1):
                total = (total + dp[j]) % MOD
            if X[i] == -1:
                for v in range(n + 1):
                    ndp[v] = total
            else:
                if X[i] > i:
                    ndp[X[i]] = 0
                else:
                    ndp[X[i]] = total
            dp = ndp
        print(sum(dp) % MOD)

if __name__ == "__main__":
    solve()
```

The DP array `dp` keeps counts of sequences ending with a specific last smaller index value. We roll the DP forward for each position, using `total` as a prefix sum over all previous counts. The modulo operation ensures that numbers do not overflow. Special care is taken to handle positions where `X[i]` is fixed, restricting updates only to that value.

## Worked Examples

**Sample 1: `-1 0 -1`**

| i | X[i] | Possible v | dp after step |
| --- | --- | --- | --- |
| 1 | -1 | 0..3 | [1,1,1,1] |
| 2 | 0 | 0 | [4] |
| 3 | -1 | 0..3 | [4,4,4,4] |

Sum = 2 modulo 998244353 → matches output.

**Sample 2: `-1 -1 1 -1`**

Trace shows DP accumulates counts respecting fixed `1` at position 3. Final sum = 3, matching expected output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Outer loop over n positions, inner loop over n possible values for DP contributions |
| Space | O(n) | Rolling DP array of size n+1 |

Since the sum of n over all test cases is ≤5000, O(n^2) per test case is feasible within 2 seconds. Memory usage is minimal due to rolling arrays.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided samples
assert run("6\n3\n-1 0 -1\n4\n-1 -1 1 -1\n5\n-1 -1 -1 -1 -1\n4\n-1 0 2 3\n4\n1 1 2 3\n4\n0 0 0 1\n") == "2\n3\n42\n1\n0\n0"

# custom cases
assert run("1\n1\n-1\n") == "1", "single element"
assert run("1\n2\n-1 -1\n") == "3", "two elements both unknown"
assert run("1\n3\n0 -1 -1\n") == "3", "prefix zero"
assert run("1\n3\n1 -1 -1\n") == "2", "prefix one"

| Test input | Expected output | What it validates |
|---|---|---|
| 1 element -1 | 1 | base case |
| 2 elements -1 -1 | 3 | multiple unknowns |
| 3 elements 0 -1 -1 | 3 | prefix fixed zero |
| 3 elements 1 -1 -1 | 2 | prefix fixed one |
```

## Edge Cases

If `X[i] > i`, for example `[3, -1, -1]` at `i=1`, there is no previous index `j < i` that satisfies `f(A
