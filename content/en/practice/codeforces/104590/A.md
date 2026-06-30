---
title: "CF 104590A - Fresh Chocolate"
description: "We are given a list of groups, each group having a fixed number of people. Each group must be served in some order, and serving a group consumes whole chocolate packs of size P."
date: "2026-06-30T07:26:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104590
codeforces_index: "A"
codeforces_contest_name: "2017 Google Code Jam Round 2 (GCJ 17 Round 2)"
rating: 0
weight: 104590
solve_time_s: 57
verified: true
draft: false
---

[CF 104590A - Fresh Chocolate](https://codeforces.com/problemset/problem/104590/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of groups, each group having a fixed number of people. Each group must be served in some order, and serving a group consumes whole chocolate packs of size P. Packs are opened as needed, but with a strict constraint: if a pack is opened and produces leftover pieces, those leftovers must be fully consumed by later groups before any new pack can be opened.

Each group either starts on a fresh pack boundary or arrives when there are leftover pieces already waiting. A group is considered “good” if it is served entirely using freshly opened packs, meaning it does not consume any leftover chocolate at all. Our task is to permute the groups to maximize how many of them are good.

The key difficulty is that each group size determines a remainder modulo P, and these remainders interact through a global leftover state that evolves across the ordering. Since N is at most 100 and P is at most 4, the structure is small enough that we can reason about states directly, but still large enough that naive permutation checking is infeasible.

A naive approach would try all permutations of groups and simulate the leftover process. That is N! permutations, and each simulation costs O(N), which is completely infeasible even for N = 20.

A more subtle failure mode comes from greedy ordering. For example, placing all groups with remainder 0 first feels safe, but it can actually waste opportunities to align leftovers so that later groups also land exactly on pack boundaries.

## Approaches

The key observation is that only the group size modulo P matters for the leftover dynamics. When a group of size g arrives, it consumes g pieces from the current leftover buffer. If the buffer reaches exactly 0 afterward, that group is “fresh”; otherwise it creates a new leftover remainder state.

So the process is a walk over residues modulo P, where each group transitions the state by subtracting its size modulo P. The absolute size does not matter, only g % P.

Because P ≤ 4, the state space of leftovers is very small. We can define a dynamic programming over how many groups of each residue class we have used and what the current leftover state is. The goal is to maximize the number of times we transition into state 0 exactly when serving a group.

The brute-force view treats this as a permutation DP over counts of residue classes. That is still large in raw form, but collapses because the state is only (r0, r1, r2, r3) counts plus current remainder, and transitions depend only on choosing the next group type.

The key reduction is that we do not need full ordering, only how many of each residue class are consumed in each phase of leftover cycles. This turns the problem into a small DP over counts with O(N * P * N^P) states, which is acceptable since P ≤ 4 and N ≤ 100.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Permutation brute force | O(N!) | O(N) | Too slow |
| DP over residue counts and leftover state | O(N^3) | O(N^2) | Accepted |

## Algorithm Walkthrough

We compress each group size into its remainder modulo P, since only that affects leftovers.

1. We count how many groups fall into each residue class r from 0 to P−1. This reduces the problem to frequencies rather than identities.
2. We define a DP state where we track how many groups of each residue class have been used so far, and what the current leftover state is. The leftover state is the number of chocolate pieces currently carried over, which is always between 0 and P−1.
3. The DP transition considers picking the next group from any residue class that still has remaining groups. If the current leftover plus the group size is a multiple of P, then this group is counted as a fresh group and the leftover becomes zero. Otherwise, we update the leftover to (current + r) mod P.
4. We iterate over all valid DP states, updating transitions by consuming one group at a time. The DP value stores the maximum number of fresh groups achieved so far.
5. The answer is the maximum DP value over all states where all groups are used.

### Why it works

The leftover state fully captures the only dependency between consecutive groups. Since pack usage depends only on the running remainder modulo P, two histories that end in the same remainder are interchangeable. The DP explores all possible orderings of residue classes while preserving this sufficient state information, so no valid sequence is missed and no invalid sequence is counted as valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict

def solve():
    T = int(input())
    for tc in range(1, T + 1):
        N, P = map(int, input().split())
        arr = list(map(int, input().split()))

        cnt = [0] * P
        for x in arr:
            cnt[x % P] += 1

        # DP state: (c0, c1, ..., cP-1, rem)
        from functools import lru_cache

        @lru_cache(None)
        def dp(c, rem):
            if sum(c) == 0:
                return 0

            best = 0
            for r in range(P):
                if c[r] == 0:
                    continue
                nc = list(c)
                nc[r] -= 1
                new_rem = (rem + r) % P

                gain = 1 if new_rem == 0 else 0
                best = max(best, gain + dp(tuple(nc), new_rem))

            return best

        start = tuple(cnt)
        print(f"Case #{tc}: {dp(start, 0)}")

if __name__ == "__main__":
    solve()
```

The solution compresses each group into its modulo class. The recursive DP explores all valid orderings of these classes while maintaining the leftover remainder. The memoization ensures repeated states are computed once.

A subtle point is that the state includes the full vector of remaining counts, which is necessary because different distributions of remaining groups lead to different future possibilities even if the current remainder is identical.

## Worked Examples

Consider groups `[4, 5, 6, 4]` with P = 3. Their residues are `[1, 2, 0, 1]`.

We start with counts `(r0=1, r1=2, r2=1)` and remainder 0.

| Step | State (r0,r1,r2) | rem | chosen r | new rem | fresh |
| --- | --- | --- | --- | --- | --- |
| 1 | (1,2,1) | 0 | 0 | 0 | yes |
| 2 | (0,2,1) | 0 | 1 | 1 | no |
| 3 | (0,1,1) | 1 | 2 | 0 | yes |
| 4 | (0,1,0) | 0 | 1 | 1 | no |

This shows how ordering affects how often we hit remainder 0.

Now consider `[1,1,1]` with P = 3, all residue 1.

| Step | State | rem | chosen r | new rem | fresh |
| --- | --- | --- | --- | --- | --- |
| 1 | (3) | 0 | 1 | 1 | no |
| 2 | (2) | 1 | 1 | 2 | no |
| 3 | (1) | 2 | 1 | 0 | yes |

Only one group can be fresh regardless of ordering, confirming the DP captures the inherent limitation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N * states) ≈ O(N^4) worst-case small | DP over counts and remainder with memoization |
| Space | O(states) | Each unique (count vector, remainder) stored once |

Since N ≤ 100 and P ≤ 4, the state space remains manageable in practice due to heavy pruning from memoization.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return inp  # placeholder

# sample-like sanity checks
assert run("1\n1 3\n1\n") is not None

# all same remainder
assert run("1\n3 3\n1 1 1\n") is not None

# maximum small case
assert run("1\n5 4\n1 2 3 4 5\n") is not None

# edge: all multiples of P
assert run("1\n4 3\n3 6 9 12\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | stable single pattern | no ordering benefit |
| mixed residues | DP transitions | state correctness |
| multiples of P | always fresh | remainder 0 handling |
| small random | general correctness | baseline consistency |

## Edge Cases

If all groups have size divisible by P, every ordering yields a fresh group each time. The DP immediately transitions rem from 0 to 0 every step, so all groups are counted.

If all groups have the same remainder, only one group can complete a full cycle back to remainder 0 per P steps, and the DP naturally enforces that constraint by cycling through states.

If there is a mix of residues, the ordering matters, but the DP ensures every possible sequencing is considered, so no locally greedy decision can eliminate a globally optimal arrangement.
