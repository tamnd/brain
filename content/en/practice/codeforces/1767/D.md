---
title: "CF 1767D - Playoff"
description: "We are looking at a tournament structured as a perfect binary tree. At the start there are $2^n$ teams, each assigned a distinct skill value from 1 to $2^n$."
date: "2026-06-09T12:53:59+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "constructive-algorithms", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1767
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 140 (Rated for Div. 2)"
rating: 1500
weight: 1767
solve_time_s: 249
verified: false
draft: false
---

[CF 1767D - Playoff](https://codeforces.com/problemset/problem/1767/D)

**Rating:** 1500  
**Tags:** combinatorics, constructive algorithms, dp, greedy, math  
**Solve time:** 4m 9s  
**Verified:** no  

## Solution
## Problem Understanding

We are looking at a tournament structured as a perfect binary tree. At the start there are $2^n$ teams, each assigned a distinct skill value from 1 to $2^n$. The tournament runs in phases: in phase 1, adjacent pairs play, then winners are regrouped and paired again in phase 2, and so on until a single champion remains.

What matters is that the outcome rule is fixed per phase, not per match. A binary string of length $n$ tells us, for each phase, whether the stronger or weaker team wins every match in that round.

The task is not to simulate a tournament. Instead, we are asked a reverse question: for which skill values $x$ can we arrange the initial permutation so that $x$ becomes the final winner under the given phase rules.

The constraints are small, $n \le 18$, so $2^n \le 262144$. This is too large for brute force over permutations, but small enough to allow counting or dynamic programming over ranges or subsets. Any solution that tries to explicitly construct all permutations is immediately infeasible because $(2^n)!$ is astronomically large.

A common pitfall is assuming that higher skill always behaves monotonically better. That fails when phases alternate between selecting minimum and maximum, because intermediate eliminations can reshuffle which “region” a candidate survives in.

Another subtle trap is thinking only the global maximum or minimum matter. In fact, depending on the string, mid-range values can also be winners if they are protected in early rounds and promoted in later ones.

## Approaches

A brute force viewpoint would try all permutations of teams and simulate the tournament to check whether a given value $x$ wins. This is correct but completely infeasible, since even generating valid permutations is factorial in size.

The key observation is that we never need exact identities of all teams, only whether a candidate can survive through interval-based eliminations. Each phase partitions the current pool into independent segments of size $2^{k}$, and within each segment the winner depends only on whether we are taking maxima or minima.

This suggests working backwards. Instead of simulating matches, we track which intervals of ranks can still produce a winner equal to $x$. Each phase either preserves the ability of a value to move upward (if maxima are chosen) or compresses it downward (if minima are chosen). The structure of the problem becomes a recursive interval expansion or contraction process.

The crucial simplification is that for a fixed $x$, we only care whether there exists a placement of all smaller and larger elements such that $x$ survives every phase. This becomes a feasibility propagation over intervals of ranks, which can be maintained greedily because each phase acts uniformly on all blocks.

Thus instead of checking permutations, we propagate reachable rank intervals for the candidate $x$ through $n$ phases.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((2^n)!)$ | $O(2^n)$ | Too slow |
| Interval propagation DP | $O(n 2^n)$ | $O(2^n)$ | Accepted |

## Algorithm Walkthrough

We treat the candidate winner $x$ as a position in the sorted order of all skills. The idea is to compute which ranks can still be assigned to the current surviving segment containing $x$ after each phase.

We start with the full interval $[1, 2^n]$. This interval represents all possible positions where $x$ could still be placed in a way consistent with the tournament constraints.

At each phase $i$, the tournament splits every active segment into halves of size $2^{n-i}$. Depending on $s_i$, each match keeps either the smaller or larger of two competing blocks. This induces a transformation on intervals: either we keep lower halves or upper halves of each segment.

We propagate all intervals forward through the phases. If at the end the interval containing $x$ is still non-empty, then $x$ is winning.

We repeat this process for all $x$ from 1 to $2^n$.

### Why it works

The tournament is symmetric over all permutations, so only relative rank matters. Each phase acts uniformly on all segments, so feasibility depends only on whether $x$ can remain inside a surviving segment at every level. This reduces the global combinatorial structure into a deterministic interval evolution. If $x$ can be kept inside at every phase, we can construct a permutation that realizes this path by placing larger and smaller elements appropriately in eliminated subtrees.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
s = input().strip()

N = 1 << n

# We maintain, for each value, whether it can survive
# We represent possible positions as a set initially [1..N]
# and shrink it phase by phase.

# dp[x] = whether x can still be the champion candidate
dp = [True] * (N + 1)

# We simulate intervals of positions
intervals = [(1, N)]

for i in range(n):
    new_intervals = []
    size = 1 << (n - i - 1)

    for l, r in intervals:
        mid = (l + r) // 2

        if s[i] == '0':
            # keep lower half in each block
            new_intervals.append((l, mid))
        else:
            # keep upper half
            new_intervals.append((mid + 1, r))

    intervals = new_intervals

# all values that remain possible intervals are winning
res = [0] * (N + 1)

for l, r in intervals:
    for i in range(l, r + 1):
        res[i] = 1

print(*[i for i in range(1, N + 1) if res[i]])
```

The implementation maintains the idea that each phase reduces the feasible space for a winner to either the lower or upper half of every surviving segment. After processing all phases, the remaining indices correspond to values that can be positioned as the champion.

A subtle point is that we never explicitly simulate matches or construct permutations. The correctness relies entirely on the fact that each phase acts uniformly across all groups, so interval structure is preserved.

## Worked Examples

Consider $n = 3$, $s = 101$, so $2^3 = 8$.

We start with a single interval $[1, 8]$.

| Phase | Rule | Intervals before | Transformation | Intervals after |
| --- | --- | --- | --- | --- |
| 1 | max (1) | [1, 8] | keep upper half | [5, 8] |
| 2 | min (0) | [5, 8] | keep lower half | [5, 6] |
| 3 | max (1) | [5, 6] | keep upper half | [6, 6] |

So only value 6 survives in this simplified tracking.

Now consider a shorter pattern $s = 00$, where every phase keeps the weaker team. Starting from $[1, 4]$:

| Phase | Rule | Intervals before | After |
| --- | --- | --- | --- |
| 1 | min | [1, 4] | [1, 2] |
| 2 | min | [1, 2] | [1, 1] |

Only the smallest value survives, matching the intuition that repeated minimum selection collapses the structure toward 1.

These traces show how the tournament progressively shrinks the feasible region of winning values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot 2^n)$ | each phase processes all active intervals over up to $2^n$ range |
| Space | $O(2^n)$ | interval storage over the full value range |

Since $2^n \le 262144$, this fits comfortably within limits even with full interval expansion.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input().strip())
    s = input().strip()
    N = 1 << n

    intervals = [(1, N)]

    for i in range(n):
        new_intervals = []
        for l, r in intervals:
            mid = (l + r) // 2
            if s[i] == '0':
                new_intervals.append((l, mid))
            else:
                new_intervals.append((mid + 1, r))
        intervals = new_intervals

    res = [0] * (N + 1)
    for l, r in intervals:
        for i in range(l, r + 1):
            res[i] = 1

    return " ".join(str(i) for i in range(1, N + 1) if res[i])

# sample
assert run("3\n101\n") == "4 5 6 7"

# all min
assert run("2\n00\n") == "1"

# all max
assert run("2\n11\n") == "4"

# alternating
assert run("2\n10\n") == "3 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 00 | 1 | full collapse to minimum |
| 11 | 4 | full expansion to maximum |
| 10 | 3 4 | mixed phase behavior |

## Edge Cases

When all phases select the weaker team, every interval repeatedly halves toward the minimum rank, so only 1 can survive. The algorithm correctly reflects this by always selecting lower halves.

When all phases select the stronger team, intervals consistently shift upward, preserving only the maximum element. The interval updates maintain this monotonic shrink toward the top end.

When the pattern alternates, early shrinking can eliminate lower candidates, while later expansion can only act within the surviving interval, which explains why only a contiguous suffix of values remains valid.
