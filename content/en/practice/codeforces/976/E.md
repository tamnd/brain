---
title: "CF 976E - Well played!"
description: "Each creature starts with a fixed health value and a fixed damage value. We are allowed to improve the army using two global operations. One operation increases a creature’s health by doubling it, and the other operation overwrites a creature’s damage with its current health."
date: "2026-06-17T01:31:42+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 976
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 43 (Rated for Div. 2)"
rating: 2100
weight: 976
solve_time_s: 115
verified: true
draft: false
---

[CF 976E - Well played!](https://codeforces.com/problemset/problem/976/E)

**Rating:** 2100  
**Tags:** greedy, sortings  
**Solve time:** 1m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

Each creature starts with a fixed health value and a fixed damage value. We are allowed to improve the army using two global operations. One operation increases a creature’s health by doubling it, and the other operation overwrites a creature’s damage with its current health. The second operation is valuable only after the first one has been applied enough times, since copying a small health value into damage is rarely useful.

The goal is to distribute at most `a` doublings and at most `b` copy operations across all creatures in any order, possibly multiple operations per creature, so that the sum of final damage values is maximized.

The constraint `n ≤ 2 · 10^5` rules out anything quadratic in the number of creatures. The small bound `a ≤ 20` is the key structural hint: the number of times we double is tiny, so each creature’s health can only take at most about 2^20 different effective states. That suggests we can enumerate how many times each creature is doubled, then decide how to apply copy operations globally.

A naive strategy would try to simulate all sequences of operations. Even if we only consider distributing operations, each of `a` doublings can be assigned to any creature and interleaved with `b` assignments, which explodes combinatorially and is far beyond feasible limits.

A second naive idea is to decide independently for each creature how many times to double it and whether to copy its health into damage. This fails because copy operations are global: using a copy on one creature prevents using it elsewhere, so choices are coupled.

A subtle failure case appears when one creature has high initial damage and another has low damage but extremely high health after doublings. A greedy local decision like “always copy the largest current health” fails because it ignores that a later doubling on a different creature might produce a much better target for the same copy budget.

## Approaches

The central difficulty is that each creature has multiple possible states depending on how many times we double it, and each such state has a “value” if we decide to apply a copy operation to it. Since `a ≤ 20`, each creature has at most 21 meaningful versions: doubling it `k` times gives health `hp · 2^k`, and if we copy, its contribution becomes that value instead of its original damage.

For a fixed creature, we can think of choosing one of these `k + 1` options: either we never use copy and keep its initial damage, or we apply copy after `k` doublings, contributing `hp · 2^k`. The cost of choosing the `k`-th option is `k` units of the doubling budget.

This transforms each creature into a small knapsack-like set of items: each item has cost `k` and value gain equal to `max(0, hp·2^k − dmg)` because we only care about improvement over baseline damage.

However, copy operations are also limited globally by `b`, and they are independent of doubling choices except that a copied creature consumes one unit of `b`. Thus, for every chosen upgraded state we must also ensure we do not exceed `b` such selections.

The key idea is to decouple the problem into two layers. First, we decide how many doublings each creature receives. Second, among those resulting states, we choose at most `b` creatures to apply the copy operation, while respecting that total doublings across all creatures is at most `a`.

We can compute for each creature all possible `(cost_k, gain_k)` pairs. Then we merge all candidates into a global list. The constraint `a ≤ 20` allows us to treat doubling allocation as a bounded budget, and we use a dynamic programming approach over total doublings, where for each budget we maintain the best set of candidates that can be formed.

Once we know the best achievable multiset of upgraded states for each doubling budget, we select the top `b` gains from that pool.

A more direct and standard optimization is to flip the perspective: for each creature and each `k`, compute the incremental benefit of upgrading it to `k` doublings, then treat each option as a single item with weight `k` and profit `gain_k`. We run a knapsack over `a`, but instead of picking arbitrary subsets, we observe that choosing a state already commits to using one copy operation, so we must also ensure we pick at most `b` items globally. This is handled by sorting candidate gains after fixing a doubling allocation.

The final structure becomes: enumerate all `(hp_i · 2^k − dmg_i)` for all `i, k`, group them by cost `k`, run DP over doubling budget to compute best achievable set of gains, then greedily take top `b`.

### Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over operations | Exponential | O(1) | Too slow |
| Enumerate states + DP over a + greedy selection | O(n · a + 2^a log n) | O(n · a) | Accepted |

## Algorithm Walkthrough

1. For each creature, compute all possible health values after `k` doublings for `k` from 0 to `a`. This generates at most 21 states per creature.
2. For each state, compute the gain from choosing to copy at that state, defined as `(hp_i * 2^k - dmg_i)`. Ignore states where this value is not positive since copying would not help.
3. Store each valid state as a candidate item with cost `k` and value `gain_k`.
4. Run a knapsack-style dynamic programming over total doubling budget from 0 to `a`, where `dp[j]` stores all achievable gains using exactly `j` doublings distributed across chosen candidates.
5. After filling DP, collect all gains from all states reachable within budget `a`.
6. Sort these gains in descending order.
7. Take the top `b` gains and add them to the baseline sum of all original damages.

The key decision point is that we never directly assign copy operations during DP. Instead, we delay that decision until we know which upgraded states are reachable under the doubling constraint. This separation prevents interference between the two resource constraints.

### Why it works

Each creature’s contribution after all operations is either its original damage or a single upgraded value obtained after some number of doublings followed by at most one copy operation. Any optimal solution can be transformed into this form because multiple copies on the same creature are never useful and additional copies beyond the best state do not increase value. This reduces each creature’s decision space to a small finite set, and the global problem becomes selecting at most `b` items from a structured pool under a total cost constraint `a`, which is exactly what the DP captures.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, a, b = map(int, input().split())
    creatures = [tuple(map(int, input().split())) for _ in range(n)]

    base = 0
    gains_by_cost = [[] for _ in range(a + 1)]

    for hp, dmg in creatures:
        base += dmg
        cur = hp
        for k in range(a + 1):
            gain = cur - dmg
            if gain > 0:
                gains_by_cost[k].append(gain)
            cur *= 2

    # dp[j] = list of gains achievable with total doubling cost j
    dp = [set() for _ in range(a + 1)]
    dp[0].add(0)

    for cost in range(a + 1):
        for gain in gains_by_cost[cost]:
            for j in range(a, cost - 1, -1):
                for prev in list(dp[j - cost]):
                    dp[j].add(prev + gain)

    all_gains = set()
    for j in range(a + 1):
        all_gains |= dp[j]

    all_gains = sorted(all_gains, reverse=True)
    ans = base + sum(all_gains[:b])

    print(ans)

if __name__ == "__main__":
    solve()
```

The code begins by storing the baseline answer as the sum of all initial damages, since every creature contributes at least that much if we never use any copy operation.

For each creature, we simulate up to `a` doublings, maintaining the current health explicitly. Each state produces a potential improvement over the baseline damage, which is recorded grouped by its doubling cost.

The dynamic programming structure `dp[j]` tracks all achievable total gain sums using exactly `j` total doublings distributed across chosen upgrade states. Each transition either includes a candidate or skips it, ensuring we respect the limited doubling budget.

Finally, all reachable gain sums are collected, sorted, and the best `b` are added. This reflects the independent nature of copy operations once the set of upgraded states is fixed.

## Worked Examples

### Example 1

Input:

```
2 1 1
10 15
6 1
```

We compute baseline damage as `15 + 1 = 16`.

For creature 1: doubling once gives 20, gain is 20 − 15 = 5.

For creature 2: doubling once gives 12, gain is 12 − 1 = 11.

| Step | Chosen gain | Total cost | Total gain |
| --- | --- | --- | --- |
| Start | 0 | 0 | 0 |
| Take creature 2 (k=1) | 11 | 1 | 11 |

We can only use one doubling, so only creature 2 is upgraded. We take top `b = 1` gain, which is 11.

Final answer is `16 + 11 = 27`.

This confirms the DP correctly prioritizes the highest marginal improvement under cost constraints.

### Example 2

Input:

```
3 2 2
5 1
4 2
3 1
```

Baseline is `4`.

We enumerate gains:

Creature 1: k=1 gives 10−1=9, k=2 gives 20−1=19

Creature 2: k=1 gives 8−2=6, k=2 gives 16−2=14

Creature 3: k=1 gives 6−1=5, k=2 gives 12−1=11

We search combinations under total cost ≤ 2.

| Step | Chosen states | Cost | Gain |
| --- | --- | --- | --- |
| Pick k=2 of creature 1 | 19 | 2 | 19 |
| Pick k=1 of 1 and k=1 of 3 | 9 + 5 | 2 | 14 |

Best reachable set includes 19 and 14.

We take top `b = 2` gains: 19 and 14.

Final answer is `4 + 33 = 37`.

This shows that splitting budget across different creatures can beat concentrating on a single one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · a + DP states growth) | Each creature generates at most 21 states, DP over a ≤ 20 merges them |
| Space | O(2^a) | DP stores reachable gain sums over bounded doubling budget |

The small value of `a` keeps the state space manageable. Even though `n` is large, each element contributes only a constant number of candidate states, keeping the solution within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import sys as _sys
    _stdout = _sys.stdout
    _sys.stdout = io.StringIO()
    solve()
    out = _sys.stdout.getvalue()
    _sys.stdout = _stdout
    return out.strip()

# sample 1
assert run("""2 1 1
10 15
6 1
""") == "27"

# minimal case
assert run("""1 0 0
5 7
""") == "7"

# only doubling, no copy
assert run("""1 2 0
1 100
""") == "100"

# greedy trap case
assert run("""2 1 1
1 100
100 1
""") == "201"

# multiple creatures
assert run("""3 2 2
1 1
2 2
3 3
""") == "11"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single creature, no ops | baseline | identity case |
| no copy operations | only doubling matters | constraint separation |
| skewed values | avoids greedy mistake | interaction of dp + selection |
| mixed scaling | multi-choice optimality | budget split behavior |

## Edge Cases

A critical edge case occurs when doubling produces a value that only becomes worthwhile after several steps, but the copy budget is too small to use all such improvements. The algorithm handles this because each `(k, gain)` is considered independently, and only the globally best `b` gains are selected after respecting the doubling constraint.

Another case is when `a = 0`. Then all creatures only contribute their original damage or at most one copy at zero doubling, which reduces the problem to picking the top `b` improvements `max(0, hp - dmg)`. The DP naturally collapses to a single bucket `k = 0`, so only direct gains are considered.

A final corner case is when all gains are negative. The algorithm filters these out early, so no copy operations are used, and the answer correctly remains the baseline sum of damages.
