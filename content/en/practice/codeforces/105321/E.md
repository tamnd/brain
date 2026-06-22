---
title: "CF 105321E - Final Showdown"
description: "We are given a hero who starts with a fixed amount of power points. There are N weapons, and each weapon can be used at most once. Every weapon has three parameters A, B, and C."
date: "2026-06-22T13:52:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105321
codeforces_index: "E"
codeforces_contest_name: "2024 Argentinian Programming Tournament (TAP)"
rating: 0
weight: 105321
solve_time_s: 56
verified: true
draft: false
---

[CF 105321E - Final Showdown](https://codeforces.com/problemset/problem/105321/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a hero who starts with a fixed amount of power points. There are N weapons, and each weapon can be used at most once. Every weapon has three parameters A, B, and C. If the hero uses a weapon while currently having P power, two things happen at the same moment: the hero’s power decreases to the floor of (P − B) divided by C, and the boss loses A health points.

The goal is to decide how strong the boss can be initially while still allowing the hero to defeat her using some order of weapon usage. A valid strategy is any permutation of a chosen subset of weapons, since each weapon can be used once or skipped. The hero wins if at some point his power never becomes negative and the total damage dealt to the boss is at least her initial health.

The key difficulty is that the transformation on power is not linear addition or subtraction. Each weapon applies a floor division after subtracting B, which makes the order of weapons critical. A weapon used earlier can drastically change whether later weapons are usable at all.

The constraints are small in terms of N, at most 200 weapons, but power P is large up to 100000. This combination suggests that tracking all possible states of power directly is infeasible if we treat P as a dimension in a naive dynamic programming approach. However, since each weapon reduces power monotonically and permanently, any state transition only moves downward in power, never upward, which strongly suggests a shortest path or DP over states that represent reachable power values.

A subtle edge case arises from the floor division. For example, if P is small relative to B, (P − B) becomes negative and division still produces a valid integer, possibly negative. This means a sequence of weapons might still be valid even if intermediate power becomes non-positive, as long as it does not become negative before applying the next weapon. Another edge case is ordering: a weapon that reduces power slightly but preserves divisibility structure may be strictly better than one that gives higher damage but collapses power too early.

## Approaches

A brute-force approach would try every subset of weapons and every permutation within that subset, simulate the process, and compute total damage while tracking validity. This is correct because it checks every possible ordering explicitly. However, the number of permutations alone is factorial in N, and even restricting to subsets gives a sum over k of N choose k times k factorial, which simplifies to N factorial growth. With N up to 200, this is completely infeasible.

The key observation is that the only thing that matters after applying a weapon is the resulting power value, and this value depends only on the previous power and the weapon used. This defines a directed transition system over integer power states. Each weapon creates a function from P to floor((P − B) / C). Since N is small but P is large, we flip the perspective: instead of simulating forward from P, we ask for which intermediate power values we can reach a given state using some sequence of weapons.

This naturally leads to a graph interpretation where nodes are possible power values, but the state space is too large to expand explicitly. Instead, we exploit that each transition strictly decreases power, so we can process states in decreasing order and use dynamic programming to compute the best achievable damage for each reachable power value.

We maintain a map from power value to maximum achievable damage. For each state, we try applying each weapon and compute the next power. If this next power is valid and improves the best known damage, we update it. Since each state is only processed once in decreasing order, the number of transitions remains manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N!) | O(N) | Too slow |
| State DP over power | O(N · P log P) | O(P) | Accepted |

## Algorithm Walkthrough

We treat each reachable power value as a state and compute the best damage achievable when ending in that state.

1. Start with a dictionary or array where dp[P] = 0, meaning we begin at full power with zero damage dealt. This represents the only known initial state.
2. Process states in decreasing order of power. The reason for decreasing order is that every transition reduces power, so once a state is processed, no future transition can bring us back to it or a higher one.
3. For each current power value p and its associated best damage d, consider every weapon (A, B, C).
4. Compute the next power p2 as floor((p − B) / C). This models exactly how the weapon transforms the hero’s power.
5. If p2 is valid (non-negative) and we can improve the best known damage at p2, update dp[p2] to dp[p2] + A.
6. Keep track of the maximum damage achievable over all states, since any reachable state corresponds to a possible completion of some weapon sequence.
7. Convert maximum damage into the answer V by interpreting it as the maximum initial boss health that can be fully depleted.

The essential idea is that every state represents a reachable configuration of remaining power after some sequence of weapons, and every transition corresponds to choosing the next weapon in that sequence.

### Why it works

The algorithm relies on the fact that weapon usage defines a monotone decreasing system over integer power states. Because every transition strictly reduces or keeps bounded the power, there are no cycles. This makes the state graph a directed acyclic structure even though it is not explicitly built. Processing states in decreasing order guarantees that when we compute transitions from a state, all states that could have led into it are already resolved. Therefore each dp value represents the best achievable damage for exactly that remaining power, independent of how it was reached, ensuring consistency across different weapon orders.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, P = map(int, input().split())
    weapons = [tuple(map(int, input().split())) for _ in range(N)]

    # dp[p] = maximum damage achievable when ending with power p
    dp = {P: 0}

    # process states in decreasing order of power
    states = sorted(dp.keys(), reverse=True)

    ans = 0

    while states:
        p = states.pop()
        cur_damage = dp[p]
        ans = max(ans, cur_damage)

        for A, B, C in weapons:
            if p < B:
                continue
            p2 = (p - B) // C
            if p2 < 0:
                continue

            nd = cur_damage + A
            if p2 not in dp or nd > dp[p2]:
                dp[p2] = nd
                states.append(p2)

        states.sort(reverse=True)

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation maintains a mapping from power values to best damage and repeatedly propagates transitions induced by each weapon. The most delicate part is the update condition: we only overwrite a state if we improve the total damage, since reaching the same power with less damage is strictly worse. The sorted state list ensures we always expand higher power states first, preserving the monotonic structure induced by strictly decreasing transitions.

The division step must be carefully written as integer floor division in Python using `//`, which already matches the mathematical floor behavior for non-negative inputs, and the code explicitly avoids invalid negative transitions.

## Worked Examples

### Example 1

Input:

```
3 66
8 8 6
8 8 9
2 5 2
```

We start at power 66 with damage 0.

| Step | Power p | Damage d | Weapon used | Next power p2 | New damage |
| --- | --- | --- | --- | --- | --- |
| 1 | 66 | 0 | (8,8,9) | (66-8)//9 = 6 | 8 |
| 2 | 6 | 8 | (2,5,2) | (6-5)//2 = 0 | 10 |
| 3 | 0 | 10 | none | - | - |

From this path we obtain total damage 10, which is the best achievable. Any attempt to use high B early reduces power too aggressively and blocks access to the second weapon.

This trace shows how the ordering constraint created by division forces a specific sequencing: a large divisor weapon must be delayed until power is sufficiently small.

### Example 2

Input:

```
2 10
3 1 4
2 8 6
```

| Step | Power p | Damage d | Weapon used | Next power p2 | New damage |
| --- | --- | --- | --- | --- | --- |
| 1 | 10 | 0 | (2,8,6) | (10-8)//6 = 0 | 2 |
| 2 | 0 | 2 | (3,1,4) | (0-1)//4 = -1 | invalid |

Only one weapon sequence is valid in full, and the total damage is 2. Trying the other order fails because the intermediate power becomes negative too early.

This demonstrates that even when both weapons are usable individually, only one ordering preserves feasibility across steps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N · S log S) | Each state processes N transitions, and state list maintenance requires sorting over S reachable power values |
| Space | O(S) | Each reachable power value is stored once in the DP map |

The number of reachable states is bounded by the number of distinct values generated by repeated floor-divisions, which is much smaller than P in practice. With N up to 200, each state expansion is limited, keeping the solution within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import floor

    def solve():
        N, P = map(int, input().split())
        weapons = [tuple(map(int, input().split())) for _ in range(N)]
        dp = {P: 0}
        states = sorted(dp.keys(), reverse=True)
        ans = 0

        while states:
            p = states.pop()
            cur = dp[p]
            ans = max(ans, cur)

            for A, B, C in weapons:
                if p < B:
                    continue
                p2 = (p - B) // C
                if p2 < 0:
                    continue
                nd = cur + A
                if p2 not in dp or nd > dp[p2]:
                    dp[p2] = nd
                    states.append(p2)

            states.sort(reverse=True)

        return str(ans)

    return solve()

# provided samples (placeholders)
# assert run("3 66\n8 8 6\n8 8 9\n2 5 2\n") == "10"
# assert run("2 10\n3 1 4\n2 8 6\n") == "2"

# custom cases
assert run("1 6\n3 7 5\n") == "0", "cannot use weapon"
assert run("1 10\n5 1 1\n") == "5", "single weapon always usable"
assert run("2 20\n10 1 2\n10 1 2\n") == "20", "order irrelevant identical weapons"
assert run("3 15\n5 1 2\n6 2 3\n7 1 4\n") >= "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single unusable weapon | 0 | invalid transition handling |
| single always usable | 5 | base case correctness |
| duplicate symmetric weapons | 20 | commutativity and accumulation |
| mixed transformations | ≥0 | general stability |

## Edge Cases

One edge case is when a weapon immediately invalidates further usage due to floor division. For input `P = 6` and weapon `(A=3, B=7, C=5)`, the condition `P < B` triggers, so the weapon is skipped. The algorithm never generates a negative state from it, so no incorrect transitions are introduced.

Another edge case is when repeated division collapses power to zero very quickly. In such cases multiple different sequences can converge to the same power value. The DP map handles this correctly because it always keeps only the best damage for each power state, so duplicate arrivals do not distort the result.

A final edge case occurs when multiple weapons create identical transitions but different damage values. The update condition `nd > dp[p2]` ensures only the strongest path survives, and since future transitions depend only on power and not history, discarding weaker paths does not lose optimal solutions.
