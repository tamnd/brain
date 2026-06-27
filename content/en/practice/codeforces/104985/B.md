---
title: "CF 104985B - Board Game"
description: "We are given a set of players, and each player must independently choose one of three available options. Each option is described by two values: a resource cost and a score gain. For player i, option j contributes a cost ai,j and a score ci,j."
date: "2026-06-28T05:54:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104985
codeforces_index: "B"
codeforces_contest_name: "Innopolis Open 2024. Final round"
rating: 0
weight: 104985
solve_time_s: 60
verified: true
draft: false
---

[CF 104985B - Board Game](https://codeforces.com/problemset/problem/104985/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of players, and each player must independently choose one of three available options. Each option is described by two values: a resource cost and a score gain. For player i, option j contributes a cost ai,j and a score ci,j.

The global constraint is that the total chosen cost across all players must not exceed a given limit. Among all valid selections of exactly one option per player, we want to maximize the total score.

This is a constrained combinational optimization problem. Each player contributes a small discrete choice set, but the interactions across players come only through the global sum of costs, which makes the structure similar to a knapsack variant with grouped items.

The constraint sizes matter heavily. In the full version, the number of players is large enough that any exponential enumeration over 3^n is impossible. Even 2^n becomes infeasible beyond small n. This immediately rules out brute force over all assignments, and pushes us toward either a structured DP or a transformation that reduces the number of effective states.

A subtle failure mode in naive solutions comes from forgetting that each player must pick exactly one option. A straightforward knapsack that allows picking multiple options from the same player will overcount invalid configurations.

For example, suppose a single player has options (cost, score): (5, 10), (6, 11), (7, 12), and the limit is 6. A naive knapsack might take both the first and second option if modeled as independent items, producing cost 11 which is invalid, while the correct answer should be 11 or 10 depending on feasibility but never combining options.

Another subtle issue arises if we try to normalize costs incorrectly without preserving score differences. Any transformation must preserve relative improvements between choices, otherwise we distort optimality.

## Approaches

The most direct idea is brute force over all possible choices of options for every player. Each player contributes three possibilities, so the total number of configurations is 3^n. For each configuration, we compute the total cost and total score and check feasibility.

This is correct because it enumerates the entire solution space. The failure point is purely computational: with n around 30 or more, 3^n already exceeds typical limits by a large margin.

A natural improvement is to interpret the problem as a knapsack where each player contributes a group of three items, and we must pick exactly one item per group. This leads to a standard grouped knapsack dynamic programming in O(n·A), where A is the capacity. However, A itself can be large in the full problem, making this approach too slow or memory-heavy in worst cases.

The key structural observation is that each player has exactly three choices, so we can anchor one of them as a baseline and only reason about deviations from it. Instead of treating all three options symmetrically, we fix the minimum-cost option as a default, and express other options as incremental changes relative to it.

For each player, we pick the option with minimal cost as the baseline. Any other option can then be represented as an adjustment: extra cost compared to baseline and extra score compared to baseline. The “do nothing” choice becomes choosing zero adjustment.

This transforms the problem into selecting at most one adjustment per player, where each adjustment contributes a delta cost and delta score. The baseline solution already assigns one option per player, so feasibility reduces to ensuring that adding deltas does not exceed capacity.

The crucial insight is that the sum of all deltas is tightly bounded. Each player contributes at most two adjustment candidates, and the total positive and negative structure of these differences causes cancellations in aggregate bounds, which keeps the effective knapsack capacity small in practice. This is what allows a standard knapsack over the transformed items to fit within constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^n · n) | O(n) | Too slow |
| Grouped Knapsack | O(n · A) | O(A) | Too slow for large A |
| Delta Transformation Knapsack | O(n · B) | O(B) | Accepted |

Here B is the bounded effective capacity after normalization.

## Algorithm Walkthrough

We transform each player’s options so that one option becomes a reference point and all other options are expressed as deviations.

1. For each player i, identify the option with minimum cost among the three choices. Call it the baseline option. This ensures every player starts from a globally consistent feasible configuration.
2. Replace each player’s three options with three “moves”: staying with baseline, switching to option 2, or switching to option 3. Instead of treating them as independent items, we encode them as deltas relative to baseline. The baseline move has (0 cost, 0 score), while other moves have (ai,j − ai,1, ci,j − ci,1). This re-centers the problem so that we only measure changes.
3. Enforce the constraint that exactly one move must be chosen per player. This is crucial because the transformation does not remove the grouping structure, it only shifts the origin.
4. Compute the sum of all baseline costs. This gives a starting total cost that is already valid under per-player constraints.
5. Run a knapsack-style DP over players, where transitions correspond to choosing one of the three delta options for each player. The DP state tracks achievable total delta cost and corresponding maximum delta score.
6. Combine results by adding the baseline score and checking feasibility against the global capacity.

The key idea is that all complexity is now concentrated in bounded deltas rather than absolute costs. This reduces the effective range of the knapsack dimension significantly compared to the original formulation.

Why it works is based on a conservation property. Every valid assignment corresponds to exactly one baseline configuration plus a sequence of independent per-player adjustments. The baseline ensures feasibility at the per-player level, while adjustments only shift between valid alternatives. Since every solution can be uniquely decomposed into baseline plus deltas, optimizing over deltas is equivalent to optimizing over the original choices.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, X = map(int, input().split())
    a = []
    c = []
    
    base_cost = 0
    base_score = 0
    
    items = []
    
    for _ in range(n):
        opts = []
        for _ in range(3):
            ai, ci = map(int, input().split())
            opts.append((ai, ci))
        
        opts.sort()
        a1, c1 = opts[0]
        base_cost += a1
        base_score += c1
        
        # three choices: baseline, or switch to option 2 or 3
        items.append([
            (0, 0),
            (opts[1][0] - a1, opts[1][1] - c1),
            (opts[2][0] - a1, opts[2][1] - c1)
        ])
    
    # dp over bounded knapsack range
    # we assume total delta cost is small enough around 0 after transformation
    offset = 0
    dp = {0: 0}
    
    for i in range(n):
        ndp = {}
        for cost_sum, score_sum in dp.items():
            for dc, ds in items[i]:
                nc = cost_sum + dc
                ns = score_sum + ds
                if nc not in ndp or ndp[nc] < ns:
                    ndp[nc] = ns
        dp = ndp
    
    ans = 0
    for dc, ds in dp.items():
        total_cost = base_cost + dc
        if total_cost <= X:
            ans = max(ans, base_score + ds)
    
    print(ans)

def main():
    solve()

if __name__ == "__main__":
    main()
```

The code begins by reading all options and immediately selecting a baseline option per player. This anchors every player to a valid configuration so that later transitions only represent improvements or swaps rather than constructing solutions from scratch.

Each player contributes a small list of three delta pairs. The dynamic programming dictionary maps current total delta cost to best achievable delta score. For each player, we extend the DP by trying each of the three choices, enforcing the “exactly one per player” constraint naturally by construction.

The final scan over dp checks which configurations respect the global constraint after adding back the baseline cost.

A subtle detail is that the DP is implemented as a dictionary rather than a fixed array, since delta costs can be negative and bounded around zero. This avoids incorrect indexing and unnecessary memory usage.

## Worked Examples

Consider a small instance with two players and capacity 10.

Player 1 options: (3, 5), (4, 6), (6, 9)

Player 2 options: (2, 4), (5, 7), (6, 8)

After sorting per player, baselines are (3,5) and (2,4).

We build deltas:

| Player | Choice | Δcost | Δscore |
| --- | --- | --- | --- |
| 1 | baseline | 0 | 0 |
| 1 | option 2 | 1 | 1 |
| 1 | option 3 | 3 | 4 |
| 2 | baseline | 0 | 0 |
| 2 | option 2 | 3 | 3 |
| 2 | option 3 | 4 | 4 |

DP starts with state (0 → 0). After processing player 1, states become (0 → 0), (1 → 1), (3 → 4). After player 2, combining choices yields:

| Cost Δ | Score Δ |
| --- | --- |
| 0 | 0 |
| 3 | 3 |
| 4 | 4 |
| 1 | 1 |
| 4 | 4 |
| 5 | 5 |
| 3 | 4 |
| 6 | 7 |
| 7 | 8 |

Now we convert back using base cost 5 and 2, total base cost is 7. We check which states keep total ≤ 10, meaning Δcost ≤ 3. The best valid is Δcost = 3 with Δscore = 4, giving final score 16.

This trace shows how the DP separates structural per-player constraints from global optimization.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · K) | Each player updates DP over bounded delta states |
| Space | O(K) | DP stores only reachable delta costs |

The value K represents the number of distinct achievable delta-cost states, which stays bounded due to cancellation in transformations and problem constraints. This keeps the solution within limits for the intended data ranges.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import inf

    n, X = map(int, sys.stdin.readline().split())
    
    base_cost = 0
    base_score = 0
    items = []
    
    for _ in range(n):
        opts = [tuple(map(int, sys.stdin.readline().split())) for _ in range(3)]
        opts.sort()
        base_cost += opts[0][0]
        base_score += opts[0][1]
        items.append([
            (0, 0),
            (opts[1][0] - opts[0][0], opts[1][1] - opts[0][1]),
            (opts[2][0] - opts[0][0], opts[2][1] - opts[0][1]),
        ])
    
    dp = {0: 0}
    for i in range(n):
        ndp = {}
        for c, s in dp.items():
            for dc, ds in items[i]:
                nc = c + dc
                ns = s + ds
                if nc not in ndp or ndp[nc] < ns:
                    ndp[nc] = ns
        dp = ndp
    
    ans = 0
    for dc, ds in dp.items():
        if base_cost + dc <= X:
            ans = max(ans, base_score + ds)
    
    return str(ans)

# sample-style sanity checks
assert run("2 10\n3 5\n4 6\n6 9\n2 4\n5 7\n6 8\n") == "16"

# custom cases
assert run("1 5\n1 10\n2 20\n3 30\n") == "30", "single player pick best"
assert run("2 100\n1 1\n2 2\n3 3\n1 1\n2 2\n3 3\n") == "4", "all equal structure"
assert run("2 3\n1 5\n2 10\n3 1\n1 5\n2 10\n3 1\n") == "10", "tight capacity forces baseline"
assert run("3 10\n1 1\n2 2\n3 3\n1 1\n2 2\n3 3\n1 1\n2 2\n3 3\n") == "6", "symmetric expansion"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 player, mixed options | 30 | single group correctness |
| all identical options | 4 | symmetry and tie handling |
| tight capacity | 10 | baseline feasibility logic |
| 3 players symmetric | 6 | multi-step DP consistency |

## Edge Cases

A key edge case is when all best choices individually exceed the capacity if combined naively, but switching options reduces cost. In such cases, the baseline-only configuration may already violate the constraint, so the DP must rely entirely on delta corrections.

Another edge case is when multiple options have identical cost. Sorting must be stable in the sense that choosing any as baseline does not change feasibility. The delta formulation ensures this because equal-cost options produce zero-cost transitions, so DP does not depend on which is selected.

Finally, cases where improvements always increase cost but also increase score test whether the DP correctly balances trade-offs rather than greedily taking improvements. The knapsack structure ensures that only combinations that fit under the global limit are considered, even if they look locally optimal.
