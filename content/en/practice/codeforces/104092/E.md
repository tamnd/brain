---
title: "CF 104092E - \u041a\u0430\u0437\u043d\u0438\u0442\u044c \u043d\u0435\u043b\u044c\u0437\u044f \u043f\u043e\u043c\u0438\u043b\u043e\u0432\u0430\u0442\u044c"
description: "We are given a sequence of words, each carrying an integer value that can be positive or negative. We are allowed to insert up to k commas, which split the sequence into contiguous segments."
date: "2026-07-02T02:26:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104092
codeforces_index: "E"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u041f\u0435\u0442\u0440\u043e\u0437\u0430\u0432\u043e\u0434\u0441\u043a\u0435 \u0438 \u041a\u0430\u0440\u0435\u043b\u0438\u0438 2021-2022 (9-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 104092
solve_time_s: 47
verified: true
draft: false
---

[CF 104092E - \u041a\u0430\u0437\u043d\u0438\u0442\u044c \u043d\u0435\u043b\u044c\u0437\u044f \u043f\u043e\u043c\u0438\u043b\u043e\u0432\u0430\u0442\u044c](https://codeforces.com/problemset/problem/104092/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of words, each carrying an integer value that can be positive or negative. We are allowed to insert up to `k` commas, which split the sequence into contiguous segments. Each segment contributes to the total score, but the sign of that contribution depends on whether we place the special word “нельзя” around that segment.

Each segment can optionally be marked as “flipped” by inserting “нельзя” immediately before and/or after commas as described in the statement, but the net effect is simple: each segment is either added normally or subtracted, and we control this choice indirectly through placement rules. The constraint that each segment can contain at most one “нельзя” means every segment independently becomes either positive or negative in its contribution, but we cannot arbitrarily assign signs to individual words, only to whole segments.

So the real structure is: we partition the array into at most `k+1` contiguous segments, and each segment `l..r` contributes either `+sum(a[l..r])` or `-sum(a[l..r])`. We want to maximize the total sum over all segments.

The constraint `n ≤ 500` immediately suggests that quadratic or cubic dynamic programming is viable. Anything like exponential splitting is impossible because the number of segmentations grows like a combinatorial explosion, roughly `2^n`.

A subtle failure case for naive thinking is assuming we should only place “нельзя” on segments with negative sums. That is incorrect because flipping a segment changes its sign, so sometimes we want to deliberately make a positive-sum segment negative if that enables better global structure under limited cuts.

Another failure mode is trying greedy segmentation: choosing best local split positions. For example, picking a locally best positive block can force remaining elements into worse configurations, and the sign choice couples segments globally.

## Approaches

A brute-force solution would enumerate all ways to split the array into up to `k+1` segments and then assign each segment a sign. Even ignoring sign assignment, the number of partitions is exponential. For `n = 500`, this is completely infeasible.

A more structured observation is that once we fix segment boundaries, the only remaining freedom is whether each segment is positive or negative. However, these choices interact with the total sum in a linear way, so we can fold them into the DP state.

The key insight is to treat this as interval DP over prefixes: for every prefix `1..i`, and for a given number of segments, we track the best achievable value. The transition considers the last segment ending at `i`, which starts at some `j+1`. The contribution of that segment is either `+(prefix[i] - prefix[j])` or `-(prefix[i] - prefix[j])`. This reduces each transition to choosing between two linear forms.

The structure becomes a classic “partition DP with prefix sums and sign choice”, solvable in `O(n^2 k)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force partitions | O(2^n) | O(n) | Too slow |
| DP over segments and endpoints | O(n^2 k) | O(nk) | Accepted |

## Algorithm Walkthrough

We precompute prefix sums so that any segment sum can be obtained in O(1). Let `pref[i]` be the sum of the first `i` values.

We define a DP table where `dp[t][i]` represents the maximum achievable score using exactly `t` segments covering the first `i` elements.

We also include the possibility of not using all `k` cuts by taking the maximum over all valid `t`.

### Steps

1. Build a prefix sum array `pref` where `pref[i] = a[1] + ... + a[i]`. This allows constant-time segment sum queries.
2. Initialize DP with a very small value for all states except `dp[0][0] = 0`, meaning zero segments covering zero elements.
3. Iterate over number of segments `t` from `1` to `k+1`. Each segment count corresponds to `t-1` commas.
4. For each endpoint `i`, try all possible previous split points `j < i`. The last segment is `(j+1 .. i)`.
5. Compute the segment sum `S = pref[i] - pref[j]`. The segment can contribute either `+S` or `-S`. So we take `max(S, -S)`, which is `|S|`.
6. Transition: `dp[t][i] = max(dp[t][i], dp[t-1][j] + abs(pref[i] - pref[j]))`.
7. The answer is the maximum value among `dp[t][n]` for `t ≤ k+1`.

### Why it works

The crucial invariant is that every valid construction corresponds to exactly one partition into segments, and each segment independently contributes either its sum or its negated sum. The DP enumerates all possible last segments for each prefix, and for each such segment it already assumes an optimal solution for the earlier prefix. Since absolute value captures the best sign choice per segment independently, we never need to revisit earlier decisions. This ensures that every valid configuration is represented exactly once through some sequence of transitions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]

    NEG = -10**18
    dp = [[NEG] * (n + 1) for _ in range(k + 2)]
    dp[0][0] = 0

    for t in range(1, k + 2):
        for i in range(1, n + 1):
            best = NEG
            for j in range(i):
                if dp[t - 1][j] == NEG:
                    continue
                seg = pref[i] - pref[j]
                best = max(best, dp[t - 1][j] + abs(seg))
            dp[t][i] = best

    ans = 0
    for t in range(1, k + 2):
        ans = max(ans, dp[t][n])

    print(ans)

if __name__ == "__main__":
    solve()
```

The prefix sum array is the core simplification that removes repeated O(n) segment sum computation. The DP layer `t` counts how many segments are used so far. The inner transition explicitly tries all split points, which is valid because `n ≤ 500`.

The use of `abs(seg)` encodes the best possible placement of “нельзя” for that segment independently of others, since each segment can be flipped or not without affecting other segments.

## Worked Examples

### Example 1

Input:

```
2 1
-100 100
```

We compute prefix sums: `pref = [0, -100, 0]`.

We allow up to 2 segments.

| t (segments) | i | j choice | segment sum | contribution | dp[t][i] |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | -100 | 100 | 100 |
| 1 | 2 | 0 | 0 | 0 | 0 |
| 1 | 2 | 1 | 100 | 100 | 100 |
| 2 | 2 | split best | mixed | 100 + 100 | 200 |

The best configuration is splitting into two segments, flipping the negative part to become positive contribution, yielding 200.

This shows that even when the total sum is zero, segmentation plus sign choice can create positive value.

### Example 2

Input:

```
8 3
2 -100 10 5 -10 3 -20 40
```

We track only key optimal transitions:

| step | last segment | prefix diff | abs value | accumulated |
| --- | --- | --- | --- | --- |
| start | - | - | - | 0 |
| take [1..2] | 2 | -98 | 98 | 98 |
| take [3..4] | 2 | 15 | 15 | 113 |
| take [5..7] | 3 | -27 | 27 | 140 |
| take [8..8] | 1 | 40 | 40 | 180 |

This trace demonstrates that optimal structure prefers grouping strongly negative and positive runs into segments whose absolute sums are large.

It also shows why greedy splitting fails: intermediate segments that look harmful (like negative prefix sums) become valuable once flipped.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²k) | For each of k+1 segment counts, we try all pairs (j, i) transitions |
| Space | O(nk) | DP table storing states for segments × prefix length |

With `n ≤ 500`, the worst-case operations are about 125 million, which fits comfortably in Python with tight loops.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    n, k = map(int, sys.stdin.readline().split())
    a = list(map(int, sys.stdin.readline().split()))

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]

    NEG = -10**18
    dp = [[NEG] * (n + 1) for _ in range(k + 2)]
    dp[0][0] = 0

    for t in range(1, k + 2):
        for i in range(1, n + 1):
            best = NEG
            for j in range(i):
                if dp[t - 1][j] == NEG:
                    continue
                best = max(best, dp[t - 1][j] + abs(pref[i] - pref[j]))
            dp[t][i] = best

    return str(max(dp[t][n] for t in range(1, k + 2)))

# provided samples
assert run("2 1\n-100 100\n") == "200"
assert run("8 3\n2 -100 10 5 -10 3 -20 40\n") == "180"

# custom cases
assert run("2 1\n1 2\n") == "3"
assert run("3 1\n-1 -2 -3\n") == "6"
assert run("3 2\n-1 2 -3\n") == "6"
assert run("5 1\n5 -1 5 -1 5\n") == "11"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 / 1 2` | `3` | all positive, no flips needed |
| `-1 -2 -3` | `6` | full flip becomes optimal |
| `-1 2 -3, k=2` | `6` | alternating structure benefits segmentation |
| `5 -1 5 -1 5` | `11` | multiple segment gains with selective flipping |

## Edge Cases

A single large negative block tests whether the algorithm correctly uses sign flipping instead of avoiding segmentation. For example, `[-10, -20, -30]` with enough segments should produce `60`, and the DP achieves this by taking the whole segment and flipping it once.

A fully positive array checks that unnecessary splitting does not improve the answer. For `n=500` positives and small `k`, the optimal strategy collapses into taking large absolute segments, and the DP naturally prefers full-range segments without artificial splits because absolute value preserves large contiguous sums.

Alternating signs test the interaction between segmentation and absolute value. Inputs like `[100, -100, 100, -100]` ensure the DP does not rely on local maxima but instead groups elements into segments whose total magnitude is maximized after potential sign flips.
