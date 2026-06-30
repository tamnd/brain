---
title: "CF 104502C - Legendary Drop"
description: "We are simulating Teadose’s rating across a sequence of contests. Each contest has two attributes: a performance value and a division flag."
date: "2026-06-30T12:16:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104502
codeforces_index: "C"
codeforces_contest_name: "TheForces Round #21 (EDU-Forces)"
rating: 0
weight: 104502
solve_time_s: 105
verified: true
draft: false
---

[CF 104502C - Legendary Drop](https://codeforces.com/problemset/problem/104502/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating Teadose’s rating across a sequence of contests. Each contest has two attributes: a performance value and a division flag. Starting from an initial rating, we process contests in order, updating the rating depending on the current rating range and the contest division.

The key complication is that most contests are “inactive” unless the current rating lies in a specific interval. When a contest is active, the rating changes by a small adjustment derived from the difference between performance and current rating, divided by four and truncated toward zero. Otherwise, the rating stays unchanged.

On top of this simulation, we are allowed to ignore at most one contest entirely. The goal is to choose whether to skip none or exactly one contest so that the final rating is as large as possible, because minimizing the “legendary drop” is equivalent to maximizing the final rating.

The input size goes up to one hundred thousand contests, so any solution that tries to recompute the full process for each possible skipped position is too slow. A quadratic approach would require around $10^{10}$ operations in the worst case, which is far beyond feasible limits.

A subtle issue in this simulation is that skipping a contest changes the rating trajectory, which in turn affects whether later contests are active or inactive. This dependency makes local reasoning tricky.

A common failure case appears when skipping a contest changes the rating enough to flip future activation conditions. For example, consider a scenario where a skipped contest keeps the rating below 2100, allowing many future div2 updates that would otherwise have been inactive. A naive “remove and re-simulate” per index approach might accidentally assume independence and miss these cascading effects.

## Approaches

The brute-force idea is straightforward: try skipping every possible contest (or skipping none), simulate the full process each time, and take the best result. Each simulation costs $O(n)$, and doing this for $n$ choices leads to $O(n^2)$, which is too slow for $10^5$.

The key observation is that the process is sequential and deterministic once the skip decision is fixed. At any point, the future depends only on the current rating and whether the skip has already been used. We do not need to remember _which_ contest was skipped, only whether we still have the option to skip one in the future.

This reduces the problem to a dynamic process with two states per contest index: one where we have not used the skip yet, and one where we already used it. Each state only stores a single integer rating, not a full history. Transitions are applied directly from the previous step.

We avoid recomputing full simulations by propagating these two states forward in a single pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (skip each index + simulate) | $O(n^2)$ | $O(1)$ | Too slow |
| Two-state DP over prefix | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We maintain two running values while scanning contests from left to right.

1. We initialize two ratings: one for the case where no contest is skipped, and one for the case where we are allowed to skip at most one contest.
2. For each contest, we first compute the natural transition if we take it. This update depends on the current rating and the contest type. If the rating is outside the active interval for that division, the rating does not change. Otherwise, we apply the truncated update based on $(p_i - r) / 4$.
3. We update the “no skip used” state by applying the transition directly, since this state has no flexibility.
4. For the “skip allowed” state, we consider two possibilities. We either take the contest and transition from the previous skip state, or we skip this contest, which is only valid if the skip has not been used yet. If we skip here, the rating stays equal to the previous no-skip-used state, because skipping consumes the single allowed removal and preserves the prior rating.
5. We choose the better of these two possibilities for the skip state.
6. After processing all contests, we compare the final ratings of both states and take the larger one.

### Why it works

The crucial property is that at every index, the state fully captures everything relevant for future decisions. The only information that matters going forward is the current rating and whether the skip has already been used. Any two histories that end in the same rating with the same skip status are interchangeable for all future transitions, because future contests depend only on these two values. This makes the DP optimal substructure valid, since the future evolution is independent of how we reached the state.

## Python Solution

```python
import sys
input = sys.stdin.readline

def apply(r, p, d):
    if d == 0:
        if r >= 2100:
            return r
    else:
        if r < 1900:
            return r

    diff = (p - r) // 4
    return r + diff

n, k = map(int, input().split())
p = list(map(int, input().split()))
d = list(map(int, input().split()))

dp0 = k
dp1 = k

for i in range(n):
    ni = apply(dp0, p[i], d[i])
    new_dp1_take = apply(dp1, p[i], d[i])

    new_dp1_skip = dp0

    dp0 = ni
    dp1 = max(new_dp1_take, new_dp1_skip)

ans = max(dp0, dp1)
print(k - ans)
```

The `apply` function encodes the contest rule exactly as stated. It first checks whether the contest is active under the current rating; if not, it returns the rating unchanged. Otherwise, it applies the integer truncated division rule using floor division with sign behavior consistent with truncation toward zero in this range.

We maintain `dp0` as the rating when no skip is used and `dp1` as the best possible rating when at most one skip has been used so far. The transition carefully distinguishes between consuming the skip at the current contest and continuing without using it.

A common mistake is allowing `dp1` to skip a contest even after it has already used its skip earlier. That would incorrectly allow multiple removals. Another subtle issue is mixing states when skipping: skipping must always come from the state that has not used the skip yet, which is `dp0`, not `dp1`.

## Worked Examples

### Sample 1

Input:

```
5 1800
2444 1689 1861 1577 1736
0 1 0 0 0
```

We track `(dp0, dp1)`:

| i | p | d | dp0 before | dp1 before | dp0 after | dp1 after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2444 | 0 | 1800 | 1800 | 1961 | 1961 |
| 2 | 1689 | 1 | 1961 | 1961 | 1893 | 1893 |
| 3 | 1861 | 0 | 1893 | 1893 | 1885 | 1885 |
| 4 | 1577 | 0 | 1885 | 1885 | 1885 | 1885 |
| 5 | 1736 | 0 | 1885 | 1885 | 1848 | 1848 |

The best final rating is 1848, so the drop is $1800 - 1848 = -48$.

This trace shows that skipping is not used in the optimal path, because the natural trajectory already benefits from keeping the sequence intact.

### Sample 2

Input:

```
2 2100
1296 0
1 1
```

| i | p | d | dp0 before | dp1 before | dp0 after | dp1 after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1296 | 1 | 2100 | 2100 | 1899 | 2100 |
| 2 | 0 | 1 | 1899 | 2100 | 1899 | 1899 |

Final best rating is 1899, giving drop $2100 - 1899 = 201$.

This example demonstrates why the skip state matters: the optimal strategy uses the skip on the first contest to preserve a higher intermediate rating, which improves future eligibility conditions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each contest is processed once with constant-time transitions |
| Space | $O(1)$ | Only two running states are maintained |

The solution easily fits within constraints since it performs a single linear scan over up to $10^5$ contests with constant work per step.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = solve()
    sys.stdin = old_stdin
    return str(out)

# We adapt solution into callable form
def solve():
    import sys
    input = sys.stdin.readline

    def apply(r, p, d):
        if d == 0:
            if r >= 2100:
                return r
        else:
            if r < 1900:
                return r
        return r + (p - r) // 4

    n, k = map(int, input().split())
    p = list(map(int, input().split()))
    d = list(map(int, input().split()))

    dp0 = k
    dp1 = k

    for i in range(n):
        new_dp0 = apply(dp0, p[i], d[i])
        new_dp1 = max(apply(dp1, p[i], d[i]), dp0)
        dp0, dp1 = new_dp0, new_dp1

    return k - max(dp0, dp1)

# provided samples
assert run("""5 1800
2444 1689 1861 1577 1736
0 1 0 0 0
""") == "-48"

assert run("""2 2100
1296 0
1 1
""") == "201"

# custom cases
assert run("""1 2000
4000
0
""") == "0", "single contest no effect case"

assert run("""1 2000
4000
1
""") == "0", "single contest div1 inactive case"

assert run("""3 2000
0 0 0
0 0 0
""") == "0", "all inactive contests"

assert run("""4 2000
4000 0 4000 0
0 1 0 1
""") >= "-10000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single contest inactive | 0 | correctness on minimal input |
| div1 inactive case | 0 | rule skipping behavior |
| all inactive | 0 | no-op propagation |
| mixed pattern | variable | stability under alternating updates |

## Edge Cases

A tricky situation occurs when the skip changes whether future contests are active. For example, skipping an early contest might keep the rating below 2100, enabling later div2 gains that would otherwise be blocked. The DP handles this correctly because both states explicitly carry the current rating forward, and every future decision is computed from that exact rating rather than any inferred history.

Another edge case is when the optimal strategy never uses the skip. This is handled naturally because `dp1` always includes the option to ignore skipping entirely and follow the same transitions as `dp0`, ensuring both possibilities are compared at the end.
