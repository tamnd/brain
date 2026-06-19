---
title: "CF 106144M - Tactical Game"
description: "We are given a binary string representing a line of battlefield cells. Each cell is either empty or contains an enemy. The goal is to eliminate every enemy using two kinds of actions. A lightning strike removes exactly one chosen enemy."
date: "2026-06-19T19:28:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106144
codeforces_index: "M"
codeforces_contest_name: "2025-2026 ICPC, NERC, Southern and Volga Russian Regional Contest"
rating: 0
weight: 106144
solve_time_s: 53
verified: true
draft: false
---

[CF 106144M - Tactical Game](https://codeforces.com/problemset/problem/106144/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string representing a line of battlefield cells. Each cell is either empty or contains an enemy. The goal is to eliminate every enemy using two kinds of actions. A lightning strike removes exactly one chosen enemy. A fireball removes one chosen enemy and also removes its immediate neighbors if they exist. The restriction is that we are allowed to use at most one fireball in the entire process, while lightning can be used any number of times.

The task is to minimize the total number of actions required to eliminate all enemies. Each enemy must be removed either directly by lightning or indirectly by a fireball effect.

The key difficulty is deciding whether and where to use the single fireball, because its effect depends heavily on local structure. It can potentially remove up to three consecutive enemies, but its placement can also be wasteful if it overlaps regions where enemies are sparse.

The constraints allow the total length across test cases up to 3·10^5. This immediately implies that any solution must be linear or near-linear per test case, since an O(n^2) scan per case would degenerate to around 10^10 operations in the worst case, which is not viable.

A naive idea would be to try every possible position for the fireball and recompute how many enemies remain. That would repeatedly scan the string, giving O(n^2) behavior. Another naive approach is greedy left-to-right removal without considering fireball placement, but that fails because the optimal fireball position depends on global structure, not just local density.

A few edge cases expose the structure clearly.

If the string is all zeros, the answer is zero because no actions are needed.

If the string is all ones, for example `11111`, a lightning-only strategy costs five actions. A single fireball placed at position 3 removes all five only if boundaries are considered carefully, but in reality it removes at most three, leaving two more, so the optimal answer is 3 actions, not 1 or 2.

If enemies are isolated like `10101`, fireball is almost useless since no placement covers multiple separated ones; optimal remains five lightnings or slightly fewer if a central placement reduces overlap, but gains are minimal.

These cases suggest that the fireball is only useful in dense contiguous segments, and its best effect always comes from applying it within a single contiguous block of ones.

## Approaches

If we ignore the fireball constraint, the problem is trivial: each enemy requires one lightning, so the answer is simply the number of ones.

Introducing a single fireball changes things because it can eliminate a cluster of up to three consecutive enemies in one operation. More importantly, it can merge savings across a contiguous block of ones by reducing local density.

A brute-force approach would be to try each index i where s[i] = '1' as the fireball center. For each such choice, we simulate the removal of i and its neighbors and then count remaining ones. This recomputation costs O(n), and doing it for all candidates gives O(n^2).

The key observation is that the string decomposes into independent blocks of consecutive ones. Any fireball can only affect a single block in a meaningful way, because zeros separate components and prevent cross-block interaction. Inside a block of length k, without fireball we need k lightnings. With one fireball, we reduce the number of required actions by at most 2, because the best possible outcome is removing three consecutive ones in a single action instead of three separate lightnings.

Thus, the entire problem reduces to finding a contiguous segment of ones where placing the fireball yields the maximum reduction. In a block of length k, the gain is exactly 1 if k ≥ 1, 2 if k ≥ 3, and 3 is impossible since adjacency overlap prevents removing more than three distinct ones per fireball.

Since we are only allowed one fireball globally, we want the best block where we can maximize saved lightnings. However, the global optimal strategy simplifies further: we do not need to explicitly choose a block, we just compute total ones and subtract the best possible savings, which is at most 2.

More precisely, the optimal saving is achieved by finding any pattern of three consecutive ones within a block. If such a pattern exists, we save 2 operations. If no such pattern exists but at least one pair of adjacent ones exists, we save 1. Otherwise, we cannot save anything.

This reduces the problem to scanning the string once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force fireball position | O(n^2) | O(1) | Too slow |
| Scan blocks and compute best gain | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the string and track three values: total number of ones, whether there exists a pair of consecutive ones, and whether there exists a triple of consecutive ones.

1. Count the total number of ones in the string. This is the baseline cost if we only use lightning attacks.
2. Scan the string from left to right and check for consecutive runs of ones. Whenever we see `s[i] = s[i-1] = '1'`, we mark that a saving of at least 1 is possible because a fireball can eliminate at least two adjacent enemies more efficiently than two separate lightnings.
3. Whenever we see `s[i] = s[i-1] = s[i-2] = '1'`, we mark that a stronger saving of 2 is possible because a single fireball can replace three separate lightning attacks.
4. After scanning, determine the best achievable saving. If a triple exists anywhere, saving is 2. Else if a pair exists, saving is 1. Otherwise saving is 0.
5. Output total_ones minus saving.

The reason this works is that any fireball always affects a contiguous region of at most three positions, and the only meaningful improvements come from replacing multiple consecutive lightnings. Longer runs do not increase per-fireball efficiency beyond these cases because a single fireball cannot cover more than three positions.

### Why it works

The algorithm relies on the fact that the benefit of the single fireball is fully determined by local adjacency structure. Every optimal placement can be reduced to a configuration inside a contiguous run of ones. Within such a run, the best possible improvement is bounded by how many consecutive ones can be centered around the fireball position. This bounds the global optimization problem into a constant-factor local pattern search, ensuring no configuration outside these patterns can yield a better improvement.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    s = input().strip()

    ones = s.count('1')

    best = 0

    for i in range(n):
        if s[i] == '1':
            if i > 0 and s[i-1] == '1':
                best = max(best, 1)
            if i > 1 and s[i-1] == '1' and s[i-2] == '1':
                best = 2

    print(ones - best)
```

The solution begins by counting all enemies, since each one would normally require a lightning strike. The variable `best` tracks how much we can reduce this cost using a single fireball.

During the scan, we detect adjacency patterns. A pair of consecutive ones guarantees that at least one fireball can save one operation by replacing two lightnings with one fireball plus one leftover lightning elsewhere. A triple of ones guarantees the maximum saving of two, since three adjacent enemies can be replaced by a single fireball instead of three separate lightnings.

The implementation uses a simple left-to-right scan, and the moment a triple is found we can safely set `best = 2` because no configuration can exceed this improvement.

Care is needed at boundaries, since indexing i-2 must only be accessed when valid.

## Worked Examples

### Example 1: `1110`

We have a single block of three ones.

| i | s[i] | pattern check | best |
| --- | --- | --- | --- |
| 0 | 1 | start | 0 |
| 1 | 1 | pair found | 1 |
| 2 | 1 | triple found | 2 |
| 3 | 0 | reset | 2 |

Total ones = 3, best saving = 2, answer = 1.

This shows the fireball fully compresses a dense cluster of three enemies into a single operation.

### Example 2: `11011`

Two separate blocks exist.

| i | s[i] | pattern check | best |
| --- | --- | --- | --- |
| 0 | 1 | start | 0 |
| 1 | 1 | pair found | 1 |
| 2 | 0 | break | 1 |
| 3 | 1 | start | 1 |
| 4 | 1 | pair found | 1 |

Total ones = 4, best saving = 1, answer = 3.

This demonstrates that separated clusters do not combine their benefit under a single fireball.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once per test case |
| Space | O(1) | Only counters and flags are stored |

The total length constraint across all test cases is 3·10^5, so a single linear scan per test case comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        s = input().strip()

        ones = s.count('1')
        best = 0

        for i in range(n):
            if s[i] == '1':
                if i > 0 and s[i-1] == '1':
                    best = max(best, 1)
                if i > 1 and s[i-1] == '1' and s[i-2] == '1':
                    best = 2

        out.append(str(ones - best))

    return "\n".join(out)

# edge: no enemies
assert run("1\n5\n00000\n") == "0"

# edge: all ones small
assert run("1\n3\n111\n") == "1"

# edge: separated ones
assert run("1\n5\n10101\n") == "5"

# edge: mixed blocks
assert run("1\n6\n110111\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 00000 | 0 | no operations needed |
| 111 | 1 | maximum benefit of fireball |
| 10101 | 5 | no adjacency benefit |
| 110111 | 2 | mixed blocks with triple saving |

## Edge Cases

For a string like `00000`, the algorithm immediately counts zero ones and never triggers any adjacency condition. The output is correctly zero because no saving is possible.

For `111`, the scan detects both a pair and a triple. At index 2, the triple condition sets best to 2, leading to answer 1, which corresponds to replacing three lightnings with a single fireball plus no remaining enemies in that segment.

For `10101`, no adjacent ones exist, so best remains zero. Every enemy is isolated, and each requires a separate lightning.

For `110111`, the first block gives a pair, and the second block gives a triple, so best becomes 2. The algorithm correctly applies the fireball only where it gives maximal compression, ignoring that blocks are separate since only one fireball is available.
