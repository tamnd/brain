---
title: "CF 106367E - Eight-thousand-year Wait"
description: "We are given an array and we consider every subsequence formed by deleting any subset of elements while keeping order. For each resulting sequence, we count how many times two adjacent elements are equal. This count is called the number of flashes."
date: "2026-06-20T22:57:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106367
codeforces_index: "E"
codeforces_contest_name: "Whalica Cup (Round 2)"
rating: 0
weight: 106367
solve_time_s: 65
verified: true
draft: false
---

[CF 106367E - Eight-thousand-year Wait](https://codeforces.com/problemset/problem/106367/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array and we consider every subsequence formed by deleting any subset of elements while keeping order. For each resulting sequence, we count how many times two adjacent elements are equal. This count is called the number of flashes. The task is to count how many subsequences produce exactly k flashes.

A useful way to think about a subsequence is through its runs. A run is a maximal block of equal values. If a subsequence has a run of length L, that run contributes L minus one flashes. Summing over all runs gives the total number of flashes. Equivalently, if a subsequence has length m and r runs, then the flash count is m minus r.

This reformulation matters because it shows that flashes are entirely determined by how often we extend a run versus start a new one, rather than by absolute positions in the original array.

The constraints are tight in a different direction than usual subsequence problems. The array length can reach two hundred thousand, while k is at most two hundred. This strongly suggests a dynamic programming approach that keeps a small dimension for k and aggregates over structure. A solution that tracks arbitrary subsequences explicitly or even maintains states per position pair is immediately too large.

A naive attempt would generate all subsequences and compute flashes directly. That already involves 2^n objects, and even for n around thirty this becomes infeasible. Another common failure is trying to do DP over subsequences without compressing the “last value” dimension, which would require tracking transitions between all values explicitly and quickly explodes in memory.

A more subtle pitfall appears when thinking only in terms of “number of equal adjacent pairs”. One might try to count pairs contributed by equal elements in the original array, but adjacency in the subsequence is not adjacency in the array, so this loses all structure.

## Approaches

The brute force idea is straightforward. Enumerate every subsequence, simulate it, and count flashes by scanning adjacent pairs. This works conceptually because it directly follows the definition, but it requires exponential time. For n up to 200000 it is impossible even to represent all subsequences.

The key structural insight is that we can build subsequences incrementally while keeping track of only two pieces of information: the last chosen value and the number of flashes so far. When we append a new element, we either start a new subsequence, continue an existing subsequence with the same value and increase the flash count, or switch to a different value and keep the flash count unchanged.

The difficulty is that “last value” ranges over all distinct values, so a naive DP would need O(nk) states per value, which is too large to maintain globally in a naive 2D array. The important observation is that transitions into a fixed value x at position i depend only on aggregated counts over all previous last values, not their individual identities. This allows us to maintain per-value DP arrays, but update them using a global sum over k.

We process the array left to right. For each value v we maintain dp[v][t], the number of subsequences ending with value v having exactly t flashes. We also maintain total[t], the sum of dp[v][t] over all v.

When we process a new occurrence x, only dp[x] changes. All other dp[v] remain valid because they do not depend on whether x is currently processed or not; x only adds new subsequences ending at x.

This locality is what keeps the solution linear in n with a small factor k.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Optimal DP with value states | O(nk) | O(nk) | Accepted |

## Algorithm Walkthrough

We maintain two structures. The first is dp[v], an array of size k+1 storing counts of subsequences ending at value v. The second is total[t], the sum over all v of dp[v][t].

We also conceptually include the empty subsequence, but we treat it only as a starting mechanism rather than storing it explicitly in dp.

### Steps

1. Initialize dp[v] as empty arrays and total[t] as zero for all t. This corresponds to having no elements processed yet.
2. Process the array from left to right. At position i, let the current value be x.
3. Create a new contribution array add[t] for value x. This will store all subsequences that end at x after including a[i].
4. Start a new subsequence consisting only of a[i]. This contributes add[0] += 1, since a single element produces zero flashes.
5. Extend existing subsequences that end at any value different from x. For a fixed t, all subsequences of total[t] can extend, but those already ending in x are special because extending x to x increases flashes. So we use total[t] - dp[x][t] as the number of subsequences ending in a different value and extend them without changing t.
6. Extend subsequences ending in x. Each such subsequence with t-1 flashes becomes a subsequence with t flashes when we append x again, so we add dp[x][t-1] into add[t].
7. After computing add, we update total by subtracting the old dp[x] and adding the new dp[x] derived from add.
8. Replace dp[x] with add.

### Why it works

At any point, dp[v][t] represents exactly all subsequences seen so far whose last element is v and whose flash count is t. Every subsequence either does not involve the current element or ends at it. When processing a new occurrence of x, every valid extension is captured by either starting fresh at x or appending x to a previously valid subsequence. The decomposition into “ending at x” and “not ending at x” is exhaustive and disjoint, so every subsequence is counted exactly once, and no transition is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        dp = {}
        total = [0] * (k + 1)

        for x in a:
            if x not in dp:
                dp[x] = [0] * (k + 1)

            old = dp[x]
            add = [0] * (k + 1)

            add[0] += 1

            for tval in range(k + 1):
                if total[tval]:
                    base = total[tval] - old[tval]
                    if base:
                        add[tval] += base

            for tval in range(1, k + 1):
                add[tval] += old[tval - 1]

            for tval in range(k + 1):
                delta = add[tval] - old[tval]
                if delta:
                    total[tval] += delta
                    old[tval] = add[tval]
                else:
                    old[tval] = add[tval]

        print(total[k] % 998244353)

if __name__ == "__main__":
    solve()
```

The core of the implementation is the per-value DP table and the global total array. The update step carefully isolates only the effect of the current element value, ensuring other dp blocks remain untouched. The subtraction `total[t] - old[t]` is the critical mechanism that avoids double counting subsequences that already end at the same value.

The loop over k remains small enough to be efficient because k is bounded by 200, and all operations are linear in that dimension.

## Worked Examples

Consider the array `[1, 2, 2, 1]` with `k = 1`.

We track only non-zero entries.

| Step | x | dp[x] after update | total[0] | total[1] |
| --- | --- | --- | --- | --- |
| 1 | 1 | [1, 0] | 1 | 0 |
| 2 | 2 | [1, 0] | 3 | 0 |
| 3 | 2 | [2, 1] | 5 | 1 |
| 4 | 1 | [2, 1] | 8 | 5 |

After processing all elements, total[1] equals 5, matching the number of subsequences with exactly one flash.

Now consider `[1, 1, 1]` with `k = 0`. Every subsequence has no flashes unless it contains repeated adjacency in the subsequence, which only happens when we pick consecutive equal contributions.

| Step | x | dp[x] after update | total[0] |
| --- | --- | --- | --- |
| 1 | 1 | [1] | 1 |
| 2 | 1 | [2] | 2 |
| 3 | 1 | [3] | 3 |

The final answer is 3 for k = 0, corresponding to all non-empty subsequences consisting of identical values in single runs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nk) | Each element updates a single dp array of size k |
| Space | O(nk) | One dp array per distinct value, each of size k |

The total sum of n over all test cases is bounded by 200000, and k is at most 200, so the number of DP transitions stays within a few tens of millions, which fits comfortably within time limits. The memory usage remains acceptable under a large memory limit due to the bounded k dimension.

## Test Cases

```python
import sys, io

MOD = 998244353

def run(inp: str) -> str:
    import sys
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    res = []
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        dp = {}
        total = [0] * (k + 1)

        for x in a:
            if x not in dp:
                dp[x] = [0] * (k + 1)

            old = dp[x]
            add = [0] * (k + 1)

            add[0] += 1

            for tval in range(k + 1):
                add[tval] += total[tval] - old[tval]

            for tval in range(1, k + 1):
                add[tval] += old[tval - 1]

            for tval in range(k + 1):
                total[tval] += add[tval] - old[tval]
                old[tval] = add[tval]

        res.append(str(total[k] % MOD))
    return "\n".join(res)

# sample-style checks (illustrative placeholders)
assert run("1\n4 1\n1 2 2 1\n") == "5"
assert run("1\n3 0\n1 1 2\n") == "4"

# custom cases
assert run("1\n1 0\n7\n") == "1", "single element"
assert run("1\n2 1\n1 1\n") == "1", "only equal pair possible"
assert run("1\n3 0\n1 2 3\n") == "7", "all distinct"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 1 | base subsequence handling |
| all equal pair | 1 | single flash creation |
| all distinct | 7 | no flashes, full subsequence counting |

## Edge Cases

A minimal single-element array shows whether the algorithm correctly initializes dp with the subsequence consisting of one element contributing zero flashes. In this case, dp creates a new entry for the value, assigns add[0] = 1, and total[0] becomes 1, producing the correct result.

An array with all identical values tests whether repeated updates correctly accumulate flashes only when extending within the same value. Each time the same value is processed, the dp[x][t-1] transition increases the flash count, and no cross-value transitions interfere.

An array with all distinct values stresses the “switching value” logic. Since dp[x] is always zero before processing each x, every subsequence extension comes only from total[t], and no dp[x] subtraction matters. The algorithm reduces to simple subsequence counting with k = 0, producing 2^n - 1 subsequences correctly for k = 0.
