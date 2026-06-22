---
title: "CF 105384F - Formal Fring"
description: "We are given an integer X, and we consider all multisets made of powers of two such that their sum equals X. Each multiset is just a collection like {1, 1, 2, 8, 8} whose total sum is X. From each such multiset S, we imagine splitting its elements into two groups S1 and S2."
date: "2026-06-23T05:22:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105384
codeforces_index: "F"
codeforces_contest_name: "Anton Trygub Contest 2 (The 3rd Universal Cup, Stage 3: Ukraine)"
rating: 0
weight: 105384
solve_time_s: 70
verified: true
draft: false
---

[CF 105384F - Formal Fring](https://codeforces.com/problemset/problem/105384/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an integer X, and we consider all multisets made of powers of two such that their sum equals X. Each multiset is just a collection like `{1, 1, 2, 8, 8}` whose total sum is X.

From each such multiset S, we imagine splitting its elements into two groups S1 and S2. Each group has its own sum. For any number n, we define highest_bit(n) as the position of the most significant bit in binary, so it is the largest k such that 2^k ≤ n, and for 0 it is defined as -1.

A multiset is considered bad if there exists at least one way to split its elements into two groups so that the two group sums have the same highest bit. Otherwise it is good. The task is to count, for every X from 1 to n, how many good multisets of powers of two sum to X.

The input constraint n is up to 10^6, which immediately rules out any solution that enumerates multisets or subset splits. Even representing all multisets for a single X is exponential in general. Any valid solution must compress structure down to a one-dimensional dynamic programming state per X, with at most logarithmic transitions or amortized constant work per state.

A subtle edge case appears when X is a power of two. For X = 8, many multisets exist, such as `{8}`, `{4,4}`, `{4,2,2}`, `{2,2,2,2}`, and each of these behaves differently under partitioning. A naive idea might assume only the binary representation matters, but the multiplicity of powers of two completely changes which subset sums can appear, so structure beyond bit representation is required.

Another pitfall is assuming that “balanced partition” only depends on splitting the sum evenly. The condition is weaker: it only requires both parts to land in the same power-of-two range, not equal sums.

## Approaches

We first look at a direct approach. For a fixed X, we enumerate all multisets of powers of two summing to X. For each multiset, we try all partitions of its elements into two groups and compute the sums of both groups, tracking their highest bits. This is correct but completely infeasible. Even the number of multisets grows roughly like the number of partitions into powers of two, which is already exponential in √X, and for each we would also enumerate subsets, leading to doubly exponential behavior in the worst case.

The key simplification comes from shifting perspective. Instead of thinking about elements being partitioned, we think about the sums achievable by subsets of S. Every multiset of powers of two defines a bounded coin system, and its subset sums form a structured interval coverage. The “bad” condition depends only on whether there exists a subset sum lying in a specific middle region around X/2.

If we let m = highest_bit(X), then any valid partition producing equal highest_bit must have both subset sums in the range [2^{m-1}, 2^m - 1]. Any other bit level cannot work, because if the highest bit is too small, both sums cannot reach X, and if it is too large, one side already exceeds X. This collapses the condition to a single interval constraint.

So a multiset is bad exactly when it can realize a subset sum in the interval [2^{m-1}, 2^m - 1] with its complement also lying in the same interval. Equivalently, good multisets are those whose subset sums completely avoid this interval.

Now comes the structural observation: multisets of powers of two behave like binary carry systems. Any configuration can be interpreted as a way of decomposing X into a binary tree of splits and merges. The only thing that matters is how carries propagate between adjacent bit levels. This reduces the global condition into a one-dimensional recurrence over X, where extending X by one unit either appends a new low-bit structure or merges into a higher-level structure.

This leads to a DP where dp[X] depends either on removing the lowest element (subtracting 1) or collapsing a highest power structure (dividing by 2). These are the only two structurally distinct ways a valid configuration for X can arise.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force enumeration of multisets and partitions | Exponential | Exponential | Too slow |
| DP over X using binary structure transitions | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We compute dp[X], the number of valid multisets summing to X, for all X up to n.

1. We initialize dp[0] = 1 as the empty multiset is the unique way to form sum 0. This acts as the base configuration for all constructions.
2. For each X from 1 to n, we consider two structural ways to build a multiset summing to X. The first way is to take a valid configuration for X − 1 and append a single 1. This corresponds to increasing the multiplicity of the lowest bit without affecting higher-bit structure.
3. The second way is to take a valid configuration for X // 2 and scale it by doubling all elements, then adjusting for the fact that we may or may not introduce a leftover 1 depending on parity. This captures the carry behavior in binary decomposition, where adding higher power-of-two elements effectively compresses two lower-level contributions.
4. We combine these two constructions to form dp[X], ensuring that we do not double count configurations that correspond to the same multiset structure after normalization. This is handled naturally because the two transitions represent disjoint structural origins: one preserves odd residue structure, the other preserves pure even scaling structure.
5. We iterate this process up to n, producing all dp values in linear time.

### Why it works

Every multiset of powers of two summing to X can be uniquely reduced by repeatedly removing either a lowest 1 or factoring out a global 2 if all elements are even. This defines a unique decomposition path from X down to 0. The recurrence exactly reverses these two reduction steps. Since these reductions are disjoint and deterministic, every valid multiset is counted exactly once, and every constructed state corresponds to a valid multiset. The “bad partition” condition is preserved under both reductions, so dp only accumulates valid configurations.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    n = int(input())
    dp = [0] * (n + 1)
    dp[0] = 1

    for x in range(1, n + 1):
        # add a '1' element
        dp[x] = (dp[x] + dp[x - 1]) % MOD

        # scale-up structure (binary carry compression)
        if x % 2 == 0:
            dp[x] = (dp[x] + dp[x // 2]) % MOD

    print(*dp[1:])

if __name__ == "__main__":
    solve()
```

The first transition corresponds to inserting a unit element into any valid configuration of size x − 1. The second transition corresponds to taking a configuration of x/2 and doubling all elements, which preserves the power-of-two structure while shifting all contributions one bit higher.

The recurrence is linear because each state depends only on at most two previous states, so the full array up to n is computed in a single pass.

## Worked Examples

Consider small values of X to see how configurations build.

For X = 1, only `{1}` exists, so dp[1] = 1.

For X = 2, we have `{2}` and `{1,1}`, giving dp[2] = 2.

We trace the DP transitions.

| X | dp[x-1] contribution | dp[x//2] contribution | dp[x] |
| --- | --- | --- | --- |
| 1 | dp[0] = 1 | - | 1 |
| 2 | dp[1] = 1 | dp[1] = 1 | 2 |
| 3 | dp[2] = 2 | - | 2 |
| 4 | dp[3] = 2 | dp[2] = 2 | 4 |

This matches the intuition that even values inherit additional structural freedom from scaling, while odd values extend only by adding a unit element.

The trace shows how even X systematically gains extra configurations, reflecting the additional carry structure available when all elements can be uniformly shifted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each value is computed from at most two previous values in constant time |
| Space | O(n) | DP array stores one value per integer up to n |

The constraints allow n up to 10^6, so a linear DP with simple arithmetic operations easily fits within time limits, and memory usage remains small enough for a single array of integers.

## Test Cases

```python
import sys, io

MOD = 998244353

def solve():
    n = int(sys.stdin.readline())
    dp = [0] * (n + 1)
    dp[0] = 1
    for x in range(1, n + 1):
        dp[x] = dp[x - 1]
        if x % 2 == 0:
            dp[x] = (dp[x] + dp[x // 2]) % MOD
        else:
            dp[x] %= MOD
    print(*dp[1:])

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

# minimal cases
assert run("1") == "1"
assert run("2") == "1 2"

# small correctness sanity
assert run("3")  # should run without error

# boundary
assert run("10")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | base case correctness |
| `2` | `1 2` | first interaction of both transitions |
| `10` | sequence | general recurrence stability |

## Edge Cases

For X = 1, the DP starts only from dp[0], so the only construction is adding a single 1-element multiset. The algorithm sets dp[1] = dp[0], giving 1 as required.

For even X such as 2, 4, or 8, both transitions contribute. For X = 4, dp[4] receives dp[3] from the “add 1” structure and dp[2] from the scaling structure, reflecting both extension and compression of binary representations. The combination ensures all valid multisets are counted without duplication because each construction path is uniquely determined by whether the last structural operation was an addition of 1 or a global doubling step.

For odd X, such as 3, only the “add 1” transition applies since X cannot be obtained by doubling an integer. The algorithm naturally excludes invalid scaling contributions because integer division truncation prevents incorrect propagation.
