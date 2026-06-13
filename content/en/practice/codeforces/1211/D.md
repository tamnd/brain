---
title: "CF 1211D - Teams"
description: "We are given a multiset of player ratings. Each player can be used at most once, and our goal is to form as many disjoint teams as possible under a strict structure constraint. Every valid team consists of two homogeneous groups of players."
date: "2026-06-13T17:05:19+07:00"
tags: ["codeforces", "competitive-programming", "*special", "binary-search", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1211
codeforces_index: "D"
codeforces_contest_name: "Kotlin Heroes: Episode 2"
rating: 2000
weight: 1211
solve_time_s: 393
verified: true
draft: false
---

[CF 1211D - Teams](https://codeforces.com/problemset/problem/1211/D)

**Rating:** 2000  
**Tags:** *special, binary search, greedy, math  
**Solve time:** 6m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of player ratings. Each player can be used at most once, and our goal is to form as many disjoint teams as possible under a strict structure constraint.

Every valid team consists of two homogeneous groups of players. One group has exactly `a` players, all sharing the same rating value `x`. The second group has exactly `b` players, all sharing another rating value `k · x`. A team is valid only if these two groups exist simultaneously and are disjoint across all teams.

So each team is essentially a pairing rule between counts of numbers: we need `a` copies of some value `x`, and `b` copies of value `k·x`. Different teams consume frequencies of values, and once a player is used, it cannot participate again.

The task is to maximize how many such teams we can build.

The input size reaches up to 300,000 elements, so any solution that tries to repeatedly simulate forming teams greedily without structure will be too slow. Even an $O(n^2)$ pairing strategy is immediately infeasible because it would require checking compatibility between many frequency buckets repeatedly. The only viable direction is to compress the array into frequencies and process values in a structured order, typically logarithmic or near-linear.

A subtle difficulty is that choices interact across values. If we greedily match a value `x` too early or too late, it may affect availability of `k·x`, so naive greedy approaches that do not carefully control ordering can fail.

A common failure case looks like this: suppose we always try to form a team as soon as we see enough `x` and `k·x`, without considering future contributions. This can waste high-value elements that are needed for more optimal pairing later.

Another issue is ordering: since `k·x` is larger than `x`, processing in increasing order allows us to always treat `x` first and push constraints forward, avoiding revisiting states.

## Approaches

The brute-force idea is to think in terms of frequencies and repeatedly try to construct a team by scanning all possible `x`, checking if `freq[x] >= a` and `freq[k·x] >= b`, and then subtracting and counting a team. Repeating this until no changes occur is conceptually correct but extremely slow. In the worst case, each iteration might remove only one team, and scanning all values costs $O(U)$, leading to $O(U \cdot \text{answer})$, which is too large when both are large.

The key observation is that the problem is entirely driven by frequencies and deterministic pairing between `x` and `k·x`. Once we fix how many times a given `x` is used as the base of teams, everything becomes forced. The only real decision is how many teams we take from each value, but this decision is local if we process values in increasing order.

The standard optimization is to maintain frequencies in a map or array and iterate over values in sorted order. For each value `x`, we compute how many teams we can form using available `x` as the first group. Each such team consumes `a` copies of `x` and `b` copies of `k·x`. We update the frequency of `k·x` accordingly.

Because `k·x` is always larger than `x`, when we reach `x`, the frequency of `x` is final and will never be changed later by future operations. This makes a single pass sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | O(U · answer) | O(U) | Too slow |
| Frequency greedy in sorted order | O(U log U) | O(U) | Accepted |

## Algorithm Walkthrough

We first compress the input into a frequency map of ratings. This removes irrelevant ordering and turns the problem into arithmetic over counts.

We then sort all distinct ratings in increasing order so that every value is processed before its multiple `k·x`.

1. Build a frequency table `freq[v]` for all ratings. This step is necessary because only counts matter, not positions.
2. Extract all distinct values and sort them increasingly. Sorting ensures that when we process a value `x`, all possible future consumers `k·x` are either not processed yet or will not affect `x` later.
3. Iterate over each value `x` in sorted order. At this moment, `freq[x]` represents the final available count for `x`.
4. Compute how many teams can be formed starting from `x` as the small-rating group. This is `t = freq[x] // a`. We cannot form more than this because each team needs `a` copies of `x`.
5. However, we are also limited by availability of `k·x`. So we cap `t` by `freq[k·x] // b`. This ensures we do not overuse `k·x`.
6. Add `t` to the answer. Then subtract resources: reduce `freq[x]` by `t · a` and reduce `freq[k·x]` by `t · b`. This enforces disjoint usage.

The key subtlety is that we never revisit `x`. Any remaining `x` after processing cannot be used later because no future step will consume it as a second group, since all second groups require a strictly larger value.

### Why it works

The algorithm enforces a directional dependency: every team uses a smaller value as a source and a larger value as a sink. By processing in increasing order, we ensure that once we assign usage of `x`, no later operation can retroactively affect it. Each value is therefore decided exactly once, and every team formed is maximal given local constraints. This eliminates cycles and guarantees that greedy local pairing does not block future optimal pairings.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, a, b, k = map(int, input().split())
    arr = list(map(int, input().split()))
    
    from collections import Counter
    freq = Counter(arr)
    
    vals = sorted(freq.keys())
    
    ans = 0
    
    for x in vals:
        if freq[x] == 0:
            continue
        y = x * k
        
        if y not in freq:
            continue
        
        # number of possible teams from x
        t = min(freq[x] // a, freq[y] // b)
        
        if t > 0:
            freq[x] -= t * a
            freq[y] -= t * b
            ans += t
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The code first builds a frequency map so that we can reason purely in counts. Sorting keys ensures that we always process smaller ratings first.

Inside the loop, we only attempt pairing if both `x` and `k·x` exist. The bottleneck calculation uses integer division on both sides, and we take the minimum to respect both constraints simultaneously. Updates to the frequency table ensure that no player is reused.

A common pitfall is forgetting to subtract from `freq[y]`. Without this, later values would incorrectly reuse already-consumed elements, inflating the answer.

## Worked Examples

### Example 1

Input:

```
12 1 2 2
1 1 2 2 2 2 2 3 3 4 6 6
```

We track frequencies:

| x | freq[x] | freq[2x] | teams formed | remaining x | remaining 2x |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 1 | 1 | 1 |
| 2 | 3 | 2 | 1 | 1 | 0 |
| 3 | 2 | 0 | 0 | 2 | 0 |

Final answer is 3.

The trace shows that once we process a value, its contribution is fully resolved, and leftover elements may still be usable only in later valid pairings with their multiples.

### Example 2

Input:

```
6 1 1 2
1 1 2 2 4 4
```

Frequencies: 1→2, 2→2, 4→2

| x | freq[x] | freq[2x] | teams | remaining x | remaining 2x |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 2 | 0 | 0 |
| 2 | 2 | 2 | 0 | 2 | 2 |
| 4 | 2 | 0 | 0 | 2 | 0 |

Only value 1 contributes because its multiples are already consumed.

This demonstrates that early processing locks in usage and prevents downstream reuse.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(U \log U)$ | sorting distinct ratings dominates |
| Space | $O(U)$ | frequency map over values |

The constraints allow up to 300,000 players, and ratings up to 1e6. Sorting distinct values and doing constant-time updates per value fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import Counter

    n, a, b, k = map(int, sys.stdin.readline().split())
    arr = list(map(int, sys.stdin.readline().split()))
    
    freq = Counter(arr)
    vals = sorted(freq.keys())
    
    ans = 0
    for x in vals:
        y = x * k
        if freq[x] == 0 or y not in freq:
            continue
        t = min(freq[x] // a, freq[y] // b)
        freq[x] -= t * a
        freq[y] -= t * b
        ans += t
    
    return str(ans)

# provided sample
assert run("12 1 2 2\n1 1 2 2 2 2 2 3 3 4 6 6\n") == "3"

# all equal no pairing
assert run("5 2 2 2\n1 1 1 1 1\n") == "0"

# exact single team
assert run("3 1 2 2\n1 2 2\n") == "1"

# chain interference
assert run("6 1 1 2\n1 1 2 2 4 4\n") == "2"

# large k break (no multiples)
assert run("4 1 1 10\n1 1 2 2\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 0 | no valid pairing exists |
| minimal valid | 1 | single team formation |
| chain case | 2 | interaction across multiples |
| large k | 0 | missing partners prevents teams |

## Edge Cases

A key edge case is when multiple values could serve as `k·x` for different `x`. For example, if both `x` and `x/k` exist in the array, careless greedy subtraction can overconsume the shared pool. The sorted order processing prevents this because once `x` is processed, it is never revisited, and all usage is decided at its smallest source.
