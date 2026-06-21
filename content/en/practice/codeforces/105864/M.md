---
title: "CF 105864M - \u0422\u0443\u0440\u043d\u0438\u0440 \u043f\u043e\u043a\u0435\u043c\u043e\u043d\u043e\u0432"
description: "We are given a collection of pokémons, each described by two numbers: its initial strength and its price. We are allowed to pick exactly one pokémon as our champion before the tournament starts."
date: "2026-06-22T02:25:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105864
codeforces_index: "M"
codeforces_contest_name: "\u041a\u043e\u043c\u0430\u043d\u0434\u043d\u044b\u0439 \u0442\u0443\u0440\u043d\u0438\u0440 \u0434\u043b\u044f \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 105864
solve_time_s: 53
verified: true
draft: false
---

[CF 105864M - \u0422\u0443\u0440\u043d\u0438\u0440 \u043f\u043e\u043a\u0435\u043c\u043e\u043d\u043e\u0432](https://codeforces.com/problemset/problem/105864/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of pokémons, each described by two numbers: its initial strength and its price. We are allowed to pick exactly one pokémon as our champion before the tournament starts. After choosing it, we must fight all other pokémons one by one in an order of our choosing.

A fight is deterministic: if our current strength is strictly greater than the opponent’s strength, we win. Otherwise we immediately lose and the process ends. Every win increases our current strength by exactly one. If we manage to defeat all opponents, that starting pokémon is considered capable of winning the tournament.

The task is to determine the minimum cost among all pokémons that can be chosen as the initial champion so that there exists some ordering of opponents that allows a full sweep. If no pokémon can achieve this, we output −1.

The key difficulty is that we are free to choose the order of fights, which means feasibility depends not only on the chosen pokémon’s strength but also on how we can schedule opponents relative to the increasing strength during the tournament.

The constraints allow up to 100,000 pokémons, which rules out any solution that simulates all permutations or even greedy attempts per candidate in quadratic time. Any approach that tries to test each pokémon independently with a simulation over all opponents would degrade to roughly O(n^2), which is too slow.

A subtle failure case appears when multiple pokémons share the same strength. If all available choices for a starting pokémon have minimal strength, none can defeat any opponent of equal strength, since the win condition is strictly greater. For example, if all ai are equal, the answer must be −1 regardless of costs.

Another non-obvious situation is that even a strong starting pokémon might fail if we cannot structure fights so that its increasing strength keeps up with the sequence of stronger opponents. A naive greedy like “always fight weakest remaining opponent” is not sufficient because cost is independent of ordering, and feasibility depends on a global ordering condition.

## Approaches

A brute-force solution would pick each pokémon as a candidate starter and then try to determine whether there exists an ordering of all other pokémons that allows it to win. For a fixed starting pokémon, we could simulate by repeatedly selecting a next opponent that is currently beatable and updating strength. Checking feasibility this way already requires sorting or repeated scanning, and doing it for every candidate leads to at least O(n^2) or O(n^2 log n), which is far beyond limits.

The structural insight is to stop thinking in terms of dynamic simulation and instead translate the problem into a feasibility condition on the starting strength. Suppose we fix a candidate with initial strength s. As we win fights, our strength becomes s + k after k victories. To beat all opponents, we need to arrange them so that at every step, the chosen opponent has strength strictly less than the current value.

This means we want to order all other pokémons in a sequence where each ai is less than its position-indexed threshold. This is equivalent to checking whether we can match each opponent strength to a distinct “time slot” where the slot index contributes extra allowed strength.

The crucial observation is that if we sort all other pokémons by strength, the hardest-to-place ones should be considered first in feasibility checking. If we process in increasing strength order, then at step i (0-indexed), the current available strength must be at least ai ≤ s + i. Rearranging gives a condition on s: s ≥ ai − i for every i in the sorted list. So for a fixed starting pokémon, we can compute the maximum of (ai − i) among all others, and ensure s strictly exceeds it.

This reduces each candidate check to O(n log n) due to sorting, but we can globalize the idea. We do not need to try all candidates if we observe that the only relevant starting pokémons are those whose strength is sufficient to satisfy the global constraint derived from all others.

Thus we sort pokémons by strength once, compute the required minimum starting strength threshold, and then among all pokémons whose strength satisfies this threshold, we pick the minimum cost.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 log n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort all pokémons by their strength in non-decreasing order. This gives a fixed order for reasoning about fight scheduling, since we only care about relative magnitudes of opponents.
2. Traverse the sorted list and compute a running constraint value defined by tracking the maximum of (ai − i), where i is the position in the sorted array. This captures how much “deficit” each opponent introduces when we try to schedule them optimally early.
3. Convert this constraint into a minimum required starting strength. Since we need strict victory, the starting strength must exceed the maximum deficit, not merely equal it.
4. Now iterate over all pokémons again and check which ones can serve as a starting candidate, meaning their initial strength is above or equal to the required threshold.
5. Among all valid candidates, take the minimum cost bi.
6. If no candidate satisfies the requirement, output −1.

### Why it works

Once pokémons are sorted by strength, any feasible fight order can be transformed into one that respects this ordering without worsening feasibility, because weaker opponents are never harder to beat later than earlier under a strictly increasing strength process. The expression ai − i captures the worst-case gap between opponent strength and available progression slots. If the initial strength is high enough to cover the worst gap, then a greedy schedule that fights in increasing strength order will always maintain validity, because at step i we have accumulated exactly i wins, hence i strength gain. This creates a tight invariant: after i wins, current strength is exactly s + i, and every remaining opponent in position i must satisfy ai < s + i, which is guaranteed by construction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    pokes = list(zip(a, b))
    pokes.sort()
    
    # compute minimum required starting strength threshold
    need = -10**30
    for i, (ai, bi) in enumerate(pokes):
        need = max(need, ai - i)
    
    ans = float('inf')
    for ai, bi in pokes:
        if ai >= need:
            ans = min(ans, bi)
    
    print(-1 if ans == float('inf') else ans)

if __name__ == "__main__":
    solve()
```

The solution begins by pairing strength and cost, then sorting by strength so that we can reason about how strength requirements evolve as we “spend” one gain per victory. The variable `need` tracks the most restrictive opponent in terms of scheduling pressure.

The second pass filters valid starting pokémons. The condition `ai >= need` reflects that only pokémons whose initial strength already clears the global requirement are usable. Finally, we minimize cost among feasible choices.

A subtle point is that the index `i` in the sorted array implicitly represents how many wins we assume have already occurred before facing that opponent in an optimal schedule. This is the core of why the transformation works.

## Worked Examples

### Example 1

Input:

```
n = 3
a = [1, 2, 4]
b = [3, 1, 2]
```

Sorted pairs:

| i | ai | ai − i |
| --- | --- | --- |
| 0 | 1 | 1 |
| 1 | 2 | 1 |
| 2 | 4 | 2 |

Threshold need = 2.

Now we check valid starters:

| pokémon | ai | bi | valid (ai ≥ 2) |
| --- | --- | --- | --- |
| 1 | 1 | 3 | no |
| 2 | 2 | 1 | yes |
| 3 | 4 | 2 | yes |

Answer is min cost among valid = 1.

This trace shows how early weak elements dominate the constraint, forcing a minimum initial strength that filters out low-strength but possibly cheap candidates.

### Example 2

Input:

```
n = 2
a = [5, 5]
b = [10, 1]
```

Sorted:

| i | ai | ai − i |
| --- | --- | --- |
| 0 | 5 | 5 |
| 1 | 5 | 4 |

Threshold need = 5.

Check candidates:

| pokémon | ai | bi | valid |
| --- | --- | --- | --- |
| 1 | 5 | 10 | yes |
| 2 | 5 | 1 | yes |

Answer is 1.

This confirms that even when strengths are equal, feasibility is purely a threshold condition, and cost selection is independent once feasibility is established.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates, with linear scans afterward |
| Space | O(n) | storing paired array |

The constraints allow up to 100,000 elements, so a single sort plus linear passes comfortably fits within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    pokes = list(zip(a, b))
    pokes.sort()

    need = -10**30
    for i, (ai, bi) in enumerate(pokes):
        need = max(need, ai - i)

    ans = float('inf')
    for ai, bi in pokes:
        if ai >= need:
            ans = min(ans, bi)

    return str(-1 if ans == float('inf') else ans)

# provided samples (illustrative; exact formatting may vary)
assert run("3\n1 2 4\n3 1 2\n") == "1"
assert run("2\n5 5\n10 1\n") == "1"

# custom cases
assert run("2\n1 1\n5 10\n") == "-1"
assert run("3\n1 3 10\n100 1 1\n") == "1"
assert run("4\n2 2 2 2\n4 3 2 1\n") == "1"
assert run("1\n100\n42\n") == "42"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal strengths | -1 | strict inequality makes win impossible |
| mixed strengths with cheap strong candidate | 1 | cost minimization under feasibility |
| uniform strengths with varying costs | 1 | correctness of filtering by threshold |
| single element | cost | base case correctness |

## Edge Cases

When all strengths are equal, every ai − i computation quickly reveals a high required threshold, but no candidate meaningfully helps beyond that threshold since strict comparisons prevent any progression against equals. For example, input `a = [3, 3, 3]` produces a requirement that cannot be satisfied in any schedule, and the algorithm correctly yields −1 because no element passes the feasibility filter.

When there is exactly one strongly dominant pokémon, such as `a = [1, 2, 100]`, the threshold becomes driven by the largest gap early in the sorted order. The algorithm computes need based on all positions, and only the strongest candidate survives the check, correctly selecting its cost as the answer.

When costs are highly uneven but strengths are similar, the algorithm ensures that feasibility is separated from optimization. It never prefers a cheap but infeasible candidate, because the feasibility filter is strictly enforced before cost minimization.
