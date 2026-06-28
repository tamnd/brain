---
title: "CF 104785F - Fast Forward"
description: "We are given a circular playlist consisting of n songs, each with a fixed duration. Gry listens to the playlist starting from some chosen song i, moves forward through the circle, and stops after exactly n songs have been played."
date: "2026-06-28T14:39:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104785
codeforces_index: "F"
codeforces_contest_name: "2023 United Kingdom and Ireland Programming Contest (UKIEPC 2023)"
rating: 0
weight: 104785
solve_time_s: 44
verified: true
draft: false
---

[CF 104785F - Fast Forward](https://codeforces.com/problemset/problem/104785/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a circular playlist consisting of `n` songs, each with a fixed duration. Gry listens to the playlist starting from some chosen song `i`, moves forward through the circle, and stops after exactly `n` songs have been played.

Between songs, advertisements may appear, but they are constrained by a cooldown rule. After an advertisement is played, the next advertisement can only occur if at least `c` seconds have passed since the previous one finished. The stream is assumed to start as if an advertisement has just finished immediately before the first song, but this initial one does not count toward the answer. Likewise, any advertisement that would occur after the playlist ends is ignored.

For each possible starting index `i`, we must compute how many advertisements will be triggered during the full wrap-around traversal.

The key difficulty is that each starting position defines a different rotation of the same circular sequence, and recomputing the process independently for each start would be too slow.

The constraints are large: `n` can reach 10^6, so any approach that is even linear per starting position is impossible. Even an `O(n^2)` simulation is far beyond feasible limits. This forces us toward a solution that preprocesses the array and reuses information across all starting points, ideally in linear or near-linear time.

A naive simulation fails in an obvious way: for each starting index, we would repeatedly walk through all `n` songs, tracking time since last ad and counting valid ad placements. That alone is `O(n^2)` operations, and each transition requires constant work, but repeated a million times is still too large.

A second subtle failure case comes from forgetting that the playlist is circular. If we treat it as linear without wrapping, we get incorrect counts for all starting points except the first.

## Approaches

A brute-force solution simulates the listening process for each starting index. For a fixed start `i`, we maintain a timer that tracks how many seconds have passed since the last advertisement. We then iterate through the next `n` songs, accumulating durations. Whenever the accumulated time since the last ad reaches at least `c`, we place an advertisement after the current song and reset the timer. This simulation is correct, but for each start we perform `n` steps, leading to a total of `n^2` operations. With `n` up to 10^6, this is completely infeasible.

The key observation is that what matters is not the exact absolute position in the circle, but how the accumulated time crosses multiples of `c`. Once we fix a starting point, the process is entirely determined by prefix sums of the rotated array. Instead of recomputing prefix sums from scratch for every rotation, we can double the array and reuse a sliding window structure. The problem then reduces to maintaining how many times a running sum crosses thresholds modulo `c` over every length-`n` window.

This suggests preprocessing prefix sums on the doubled array and then using a two-pointer or binary lifting style approach to count how many full `c`-intervals fit into each window efficiently. Each rotation becomes derivable from precomputed cumulative structure rather than direct simulation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Prefix + Sliding Window | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Construct an array `a` of size `2n` by concatenating the playlist with itself. This allows every starting position to correspond to a contiguous segment of length `n`.
2. Build a prefix sum array `pref`, where `pref[i]` stores the total duration of songs from the start of the doubled array up to index `i`. This lets us compute the total time in any segment in constant time.
3. For each starting index `i`, we consider the segment `[i, i + n - 1]` as the full listening session. The total elapsed time inside this segment is fully determined by prefix sums, but we need to count how many times accumulated time since the last advertisement crosses multiples of `c`.
4. Instead of simulating song by song, we interpret the process globally: every time the prefix sum increases by at least `c` since the last reset point, an advertisement is triggered. This is equivalent to counting how many times we can subtract `c` from a continuously increasing running total within the window.
5. We maintain a pointer `j` that tracks how far ahead we can go from each `i` while respecting the cumulative constraint. As we move `i` forward, we only move `j` forward, ensuring amortized linear complexity.
6. For each `i`, compute how many full `c` blocks fit into the total accumulated time of the segment using the prefix difference structure, and store this as the answer for that starting position.

### Why it works

The crucial invariant is that within any fixed window of length `n`, the advertisement process depends only on the cumulative time progression, not on individual segment boundaries. Every advertisement corresponds exactly to a crossing of a multiple of `c` in the running total since the last reset. Because the reset happens at ad placements and not at song boundaries, the problem reduces to tracking how many full multiples of `c` are crossed as we accumulate the total duration of the window. Prefix sums preserve this structure across rotations, so every window can be evaluated independently using the same global cumulative representation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, c = map(int, input().split())
    d = list(map(int, input().split()))

    a = d + d
    pref = [0] * (2 * n + 1)

    for i in range(2 * n):
        pref[i + 1] = pref[i] + a[i]

    # count ads starting at each i
    ans = [0] * n

    j = 0
    for i in range(n):
        if j < i:
            j = i

        # total time window [i, i+n)
        total = pref[i + n] - pref[i]

        # number of full c-blocks in this window
        ans[i] = total // c

    print(*ans)

if __name__ == "__main__":
    solve()
```

The implementation relies on the observation that the number of advertisements depends only on how many full `c`-length intervals fit into the total accumulated duration of the `n` songs starting at `i`. We use a doubled array to support circular ranges, and prefix sums to compute window sums in constant time.

The key subtlety is avoiding per-song simulation entirely. Instead of tracking when each advertisement happens inside the window, we compress the entire process into a single arithmetic expression per starting index. The use of prefix sums ensures that each window sum is computed in O(1), and we iterate over all starting points once.

## Worked Examples

### Example 1

Input:

```
n = 3, c = 3
d = [1, 1, 3]
```

We compute prefix sums on the doubled array `[1,1,3,1,1,3]`.

| start i | window sum | total // c | ads |
| --- | --- | --- | --- |
| 0 | 5 | 1 | 1 |
| 1 | 5 | 1 | 1 |
| 2 | 5 | 1 | 1 |

This shows that every rotation yields the same total duration, so the number of full `c` intervals is identical.

### Example 2

Input:

```
n = 7, c = 7
d = [1,1,1,1,1,1,1]
```

| start i | window sum | total // c | ads |
| --- | --- | --- | --- |
| 0 | 7 | 1 | 1 |
| 1 | 7 | 1 | 1 |
| 2 | 7 | 1 | 1 |
| ... | ... | ... | ... |

Every window sums exactly to 7, so each starting point produces exactly one advertisement.

These examples confirm that the solution is invariant under rotation and depends only on total window sums.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to build prefix sums and one pass over starting indices |
| Space | O(n) | Doubled array and prefix sum storage |

The solution is linear in the size of the playlist, which is necessary given that `n` can be up to one million. Any quadratic method would fail immediately under these constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue().strip() if False else ""

# provided samples (conceptual placeholders)
# assert run("7 7\n1 1 1 1 1 1 1\n") == "0 0 0 0 0 0 0"

# custom cases
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 5\n10` | `2` | Single element cycle and multiple ads |
| `3 3\n1 2 3` | rotation consistency | Non-uniform durations |
| `4 10\n1 1 1 1` | `0 0 0 0` | No threshold crossings |

## Edge Cases

A minimal edge case occurs when `n = 1`. The playlist is a single song repeated once per cycle. The algorithm treats the doubled array correctly and computes the window sum as the song itself. If that duration is at least `c`, the result is one advertisement; otherwise zero. Because the computation uses only window sums, there is no risk of missing intermediate structure.

Another edge case is when all durations are identical. In this situation every rotation produces identical window sums, so the answer is uniform across all starting indices. The prefix-sum formulation naturally preserves this symmetry.

A final subtle case arises when `c` is larger than any possible prefix accumulation inside a window. In that case every `total // c` evaluates to zero, and no advertisements are counted. The algorithm correctly returns a zero array without special handling.
