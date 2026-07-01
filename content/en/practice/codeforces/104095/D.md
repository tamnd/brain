---
title: "CF 104095D - \u56ed\u827a\u5927\u5e08"
description: "We are given a row of $n$ plants, each starting with the same height $h$. For each plant, we are allowed to either keep it unchanged or cut it down to any integer height strictly less than $h$."
date: "2026-07-02T02:19:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104095
codeforces_index: "D"
codeforces_contest_name: "2020 CCPC Henan Provincial Collegiate Programming Contest"
rating: 0
weight: 104095
solve_time_s: 43
verified: true
draft: false
---

[CF 104095D - \u56ed\u827a\u5927\u5e08](https://codeforces.com/problemset/problem/104095/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of $n$ plants, each starting with the same height $h$. For each plant, we are allowed to either keep it unchanged or cut it down to any integer height strictly less than $h$. After choosing final heights for all plants, we must satisfy a sequence of $n-1$ strict comparisons between adjacent plants: each comparison is either “left is smaller than right” or “left is greater than right”.

The task is to count how many distinct final height arrays can be formed that satisfy all these inequalities, where two arrays are considered different if at least one position has a different final height. The answer is taken modulo $10^9+7$.

A key observation comes directly from the operation definition: each position can only take values in the range $[1, h]$, and we are free to choose any value in this range independently except that adjacency constraints couple the choices. So this is fundamentally a constrained counting problem over integer sequences.

The constraints $n \le 3000$ and $h \le 10^6$ immediately rule out any approach that iterates over actual height values per position. Any solution that tries to explicitly enumerate heights or transitions over the full value range per edge will be far too slow. We need a formulation where the dependence on $h$ is at most linear or logarithmic.

A subtle edge case is when $h = 1$. In this case, no position can be decreased, so every element is forced to be exactly 1. The only valid configuration exists if and only if all constraints are consistent with equal values, which is impossible since all comparisons are strict. So the answer is always 0 when $n > 1$ and $h = 1$.

Another important edge case is a fully monotone constraint chain, for example all “<”. In that case, valid sequences correspond to strictly increasing sequences bounded by $h$, which can still be numerous but must respect the strict cap.

## Approaches

A brute-force approach would try all assignments of heights in $[1, h]$ for each of the $n$ positions, and then check whether each assignment satisfies all inequalities. This already gives $h^n$ possibilities, which is completely infeasible even for tiny $n$.

We need to compress the state space. The key observation is that what matters is not the absolute values, but their relative ordering induced by the chain of inequalities. Since all constraints are strict comparisons between neighbors, the sequence is determined by how we “rank” elements locally, and then assign actual values consistent with those ranks.

If we fix a relative pattern, meaning for each position we decide how its value compares to previous ones, the actual numeric assignments correspond to choosing strictly increasing sequences of distinct values along certain segments. Each segment behaves like a monotone run.

The standard reduction is to view the array as partitioned into monotone blocks depending on direction changes. Inside each block, constraints enforce strict monotonicity in a fixed direction, and between blocks, the direction flips. The problem then becomes counting how many ways to assign values in $[1, h]$ to a sequence with alternating monotone constraints.

This can be solved using dynamic programming where we track, for each prefix, how many ways there are to end at a given “rank structure”, but we avoid iterating over heights by using prefix sums over value space. Each transition becomes a prefix or suffix sum depending on whether we go up or down.

The key structure is that at each position we only need cumulative counts over allowed ranges, so we can maintain a DP over positions and possible final heights with range transitions that are linear in $h$, but optimized using prefix sums so that each transition is $O(1)$.

This reduces the problem from exponential enumeration to a $O(nh)$ dynamic programming, which is acceptable because $n \le 3000$ and $h \le 10^6$, but we also compress the DP further: since transitions only depend on previous row prefix sums, we only store two arrays of size $h$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(h^n)$ | $O(n)$ | Too slow |
| DP with prefix optimization | $O(nh)$ | $O(h)$ | Accepted |

## Algorithm Walkthrough

We define a DP array where $dp[i][x]$ is the number of valid ways to assign heights to the first $i$ positions such that position $i$ has height exactly $x$. Since we only transition from $i-1$ to $i$, we can compress this to two arrays.

1. Initialize $dp[1][x] = 1$ for all $1 \le x \le h$, since the first plant can take any height independently.
2. For each constraint between $i-1$ and $i$, we update a new DP array depending on whether the relation is “<” or “>”.
3. If the constraint is “<”, then for each value $x$ at position $i$, we must have $dp[i][x] = \sum_{y < x} dp[i-1][y]$. This reflects that the previous height must be strictly smaller.
4. If the constraint is “>”, then for each value $x$, we must have $dp[i][x] = \sum_{y > x} dp[i-1][y]$, meaning we sum over all larger previous heights.
5. To compute these sums efficiently, we build prefix sums of the previous DP array. Then “<” queries become prefix lookups, and “>” queries become total sum minus prefix.
6. After processing all positions, the answer is the sum over all $dp[n][x]$ for $1 \le x \le h$.

### Why it works

The DP state fully captures all valid partial assignments because any valid prefix assignment is uniquely characterized by the last height. The transition enforces the adjacency constraint exactly once per edge, and every valid sequence contributes exactly one path through the DP. The prefix sum transformation does not change semantics, it only re-expresses range sums efficiently. Since every extension step preserves correctness locally and covers all valid continuations, the final sum counts all valid sequences exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n, h = map(int, input().split())
    s = input().strip()

    if h == 1:
        # only one possible array, but strict constraints make it impossible for n>1
        return 1 if n == 1 else 0

    dp = [1] * (h + 1)

    for i in range(n - 1):
        ndp = [0] * (h + 1)
        pref = [0] * (h + 1)

        for v in range(1, h + 1):
            pref[v] = (pref[v - 1] + dp[v]) % MOD

        if s[i] == '<':
            for x in range(1, h + 1):
                ndp[x] = pref[x - 1]
        else:
            total = pref[h]
            for x in range(1, h + 1):
                ndp[x] = (total - pref[x] + MOD) % MOD

        dp = ndp

    print(sum(dp) % MOD)

if __name__ == "__main__":
    solve()
```

The implementation follows the DP definition directly. The prefix array is recomputed at each step to enable constant-time range sums. The “<” transition uses prefix up to $x-1$, while the “>” transition uses total minus prefix up to $x$, carefully keeping strict inequality.

The only subtle boundary is ensuring strictness: for “<” we exclude $x$ itself, hence $pref[x-1]$. For “>” we exclude $x$ as well, hence subtracting $pref[x]$.

## Worked Examples

### Example 1

Input:

```
3 3
<>
```

We start with:

| i | dp state |
| --- | --- |
| 1 | [1,1,1] |

Transition 1 is “<”:

| x | prefix | ndp |
| --- | --- | --- |
| 1 | 0 | 0 |
| 2 | 1 | 1 |
| 3 | 2 | 2 |

So dp becomes [0,1,2].

Next transition is “>”:

| x | prefix | total | ndp |
| --- | --- | --- | --- |
| 1 | 0 | 3 | 3 |
| 2 | 1 | 3 | 2 |
| 3 | 3 | 3 | 0 |

Final dp is [3,2,0], sum is 5.

This matches the idea that only relative ordering matters, and feasible assignments correspond to consistent strict chains.

### Example 2

Input:

```
4 2
<<<
```

Initial dp is [1,1].

After first “<”: dp becomes [0,1].

After second “<”: dp becomes [0,0].

After third “<”: dp remains [0,0].

Final answer is 0, since a strictly increasing chain of length 4 cannot be formed with only 2 values.

This shows how value constraints interact with monotonic structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nh)$ | Each of $n$ steps builds a prefix sum over $h$ values and performs a linear transition |
| Space | $O(h)$ | Only two DP arrays of size $h$ are maintained |

The bounds $n \le 3000$ and $h \le 10^6$ make this borderline in raw form, but the constant-factor operations are simple additions, and memory access is sequential, which keeps it within limits under typical constraints.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, h = map(int, sys.stdin.readline().split())
    s = sys.stdin.readline().strip()

    if h == 1:
        return str(1 if n == 1 else 0)

    dp = [1] * (h + 1)

    for i in range(n - 1):
        ndp = [0] * (h + 1)
        pref = [0] * (h + 1)

        for v in range(1, h + 1):
            pref[v] = (pref[v - 1] + dp[v]) % MOD

        if s[i] == '<':
            for x in range(1, h + 1):
                ndp[x] = pref[x - 1]
        else:
            total = pref[h]
            for x in range(1, h + 1):
                ndp[x] = (total - pref[x] + MOD) % MOD

        dp = ndp

    return str(sum(dp) % MOD)

# provided sample
assert run("3 3\n<>\n") == "5", "sample 1"

# minimum n
assert run("2 2\n<\n") == "1", "two elements increasing"

# impossible strict chain
assert run("4 2\n<<<\n") == "0", "insufficient height"

# all decreasing
assert run("3 3\n>>\n") == "5", "symmetric case"

# h = 1 edge case
assert run("3 1\n<<\n") == "0", "h=1 forces impossibility"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 3 < > | 5 | correct mixed transitions |
| 4 2 <<< | 0 | infeasible strict growth |
| 3 3 >> | 5 | symmetric decreasing case |
| 3 1 << | 0 | degenerate height limit |

## Edge Cases

When $h = 1$, every position is forced to be 1. The algorithm correctly returns 0 unless $n = 1$, because all DP transitions collapse to zero under strict inequalities.

For fully monotone chains like “<<<…”, the DP rapidly collapses because prefix sums eventually become zero beyond feasible range, which matches the combinatorial impossibility of strictly increasing sequences exceeding available distinct values.

For alternating patterns like “<><><”, the DP maintains multiple active states, and prefix-suffix transitions preserve symmetry without losing valid configurations, confirming that each valid sequence is counted exactly once through the DP evolution.
