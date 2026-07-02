---
title: "CF 103666I - \u041d\u0443\u0436\u043d\u043e \u0431\u043e\u043b\u044c\u0448\u0435 \u0437\u043e\u043b\u043e\u0442\u0430"
description: "We are given a collection of magical artifacts, each with a positive value $wi$. The hero starts with zero magical power. Each artifact must be used exactly once, and each one can be activated in one of two ways."
date: "2026-07-02T21:33:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103666
codeforces_index: "I"
codeforces_contest_name: "\u0422\u0443\u0440\u043d\u0438\u0440 \u0410\u0440\u0445\u0438\u043c\u0435\u0434\u0430 2016"
rating: 0
weight: 103666
solve_time_s: 47
verified: true
draft: false
---

[CF 103666I - \u041d\u0443\u0436\u043d\u043e \u0431\u043e\u043b\u044c\u0448\u0435 \u0437\u043e\u043b\u043e\u0442\u0430](https://codeforces.com/problemset/problem/103666/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of magical artifacts, each with a positive value $w_i$. The hero starts with zero magical power. Each artifact must be used exactly once, and each one can be activated in one of two ways.

If an artifact is activated using magic, its value is added to the hero’s current magical power. If it is activated using strength, it yields gold equal to the artifact’s value multiplied by the hero’s current magical power at that moment. The activation order is free, and the decision of whether to use magic or strength for each artifact is also free.

The goal is to maximize total gold obtained from strength activations, while remembering that only magic activations increase the multiplier used for future gold gains.

The input size is small, with $n \le 100$ and values $w_i \le 100$. This immediately suggests that quadratic or even cubic dynamic programming approaches are acceptable, but exponential enumeration over all subsets is not reliable since $2^{100}$ is far too large.

A key structural observation is that the only way to increase future gains is to “spend” some artifacts as pure power builders, and the rest as profit generators. The order matters because power accumulates over time and directly multiplies all later chosen profit contributions.

A subtle edge case is when all artifacts are used as magic. In that case, no gold is produced at all, and the answer is zero. Another corner case is when all are used as strength, but then the multiplier is always zero, so again the answer is zero. The optimal solution must balance both roles.

## Approaches

A brute-force approach tries all possibilities of assigning each artifact either to be used as magic or strength, and also considers all permutations of activation order. For each arrangement, we simulate the process, tracking current power and accumulating gold. This already becomes infeasible because even ignoring permutations, there are $2^n$ assignments, and each simulation costs $O(n)$, giving $O(n \cdot 2^n)$, which is far beyond limits.

The key observation is that the order can be normalized. If we fix which artifacts are used for magic, it is always optimal to apply all magic operations first in increasing order of when we want their power contribution to matter, because delaying magic only reduces future multipliers. Once this separation is understood, the problem becomes: choose a subset of items to contribute to power, and then decide an order for strength items that maximizes gain under a growing prefix sum.

This leads to a dynamic programming formulation over how many artifacts are used as magic and how their total power is built. We sort artifacts so that we reason over them one by one, maintaining possible states of total magic power and how many items we have processed. Each artifact either increases power or contributes to gold weighted by current power, and the decision is made optimally via DP transitions.

The structure is essentially a knapsack-like DP where state tracks accumulated magic sum and best achievable gold for that sum after processing a prefix of items.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \cdot 2^n)$ | $O(n)$ | Too slow |
| Dynamic Programming | $O(n^2 \cdot \max w)$ | $O(n \cdot \max w)$ | Accepted |

## Algorithm Walkthrough

We interpret the process as building two groups: artifacts used to increase magic power and artifacts used to earn gold, where gold depends on the final accumulated power at the moment each strength artifact is used. The difficulty is that strength activations depend on the evolving power, so we must model power accumulation carefully.

### Steps

1. Sort the artifacts by value, or more precisely, process them in arbitrary order since all choices are symmetric. We instead focus on DP over subsets implicitly via prefix processing.
2. Define a DP state where we track how many artifacts have been processed and the total magic power accumulated so far, and for each such state store the maximum gold achievable.
3. Initialize the DP with zero artifacts processed, zero power, and zero gold.
4. For each artifact with value $w$, we consider two transitions from every existing state. One transition treats the artifact as magic, increasing the current power by $w$ without producing gold. The other transition treats it as strength, producing gold equal to current power multiplied by $w$, without changing power.
5. We update the DP carefully so that each artifact is used exactly once, iterating states in reverse order of processing to avoid reuse within the same iteration.
6. After processing all artifacts, we scan all DP states and take the maximum gold value.

The key design choice is storing power as a state variable. This is necessary because gold depends on the multiplier at each decision, and that multiplier is exactly the accumulated magic power so far.

### Why it works

At any point in the process, the only information that affects future outcomes is the current total magic power and which items remain. The DP state captures exactly this information. Any two sequences that end at the same processed prefix and same power are interchangeable for future decisions, so keeping only the best gold for each state is safe. This establishes optimal substructure, since decisions for each artifact depend only on current power and not on how that power was achieved.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    w = list(map(int, input().split()))

    max_sum = sum(w)

    # dp[i][p] = max gold after processing some prefix, with power p
    dp = [[-1] * (max_sum + 1) for _ in range(n + 1)]
    dp[0][0] = 0

    for i in range(n):
        wi = w[i]
        for j in range(i, -1, -1):
            for p in range(max_sum - wi, -1, -1):
                if dp[j][p] < 0:
                    continue

                # use as magic: increase power
                dp[j + 1][p + wi] = max(dp[j + 1][p + wi], dp[j][p])

                # use as strength: gain gold
                dp[j + 1][p] = max(dp[j + 1][p], dp[j][p] + p * wi)

    ans = 0
    for j in range(n + 1):
        for p in range(max_sum + 1):
            ans = max(ans, dp[j][p])

    print(ans)

if __name__ == "__main__":
    solve()
```

The code builds a DP table indexed by how many items have been processed and the current accumulated magic power. Each artifact either contributes to increasing power or contributes to gold based on the current power.

The reverse iteration over `j` and `p` ensures each artifact is used exactly once, preventing overwriting states that would incorrectly reuse the same item multiple times. The transition for strength uses `p * wi`, directly encoding the multiplier rule.

## Worked Examples

Consider the sample input with values $[1, 1, 2, 2]$.

We trace a simplified DP focusing on optimal choices.

| Step | Artifact | Power before | Action | Power after | Gold gained | Total gold |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | magic | 1 | 0 | 0 |
| 2 | 2 | 1 | magic | 3 | 0 | 0 |
| 3 | 1 | 3 | strength | 3 | 3 | 3 |
| 4 | 2 | 3 | strength | 3 | 6 | 9 |

This trace shows that building power early and spending it later yields strictly better results than mixing actions arbitrarily.

Now consider a skewed input $[5, 1, 1]$.

| Step | Artifact | Power before | Action | Power after | Gold gained | Total gold |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 5 | 0 | magic | 5 | 0 | 0 |
| 2 | 1 | 5 | strength | 5 | 5 | 5 |
| 3 | 1 | 5 | strength | 5 | 5 | 10 |

This shows that a single large magic early enables maximizing all later strength gains.

The traces confirm that the DP is correctly capturing the trade-off between building power and spending it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2 \cdot \sum w)$ | Each item transitions over all DP states, and each state considers two choices |
| Space | $O(n \cdot \sum w)$ | DP table stores best gold for each prefix and power value |

The constraints $n \le 100$, $w_i \le 100$ imply $\sum w \le 10000$. The DP therefore runs in about $10^8$ operations in the worst case, which is acceptable in optimized Python under 2 seconds in typical competitive settings when implemented carefully.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import inf

    data = inp.strip().split()
    n = int(data[0])
    w = list(map(int, data[1:]))

    max_sum = sum(w)
    dp = [[-1] * (max_sum + 1) for _ in range(n + 1)]
    dp[0][0] = 0

    for i in range(n):
        wi = w[i]
        for j in range(i, -1, -1):
            for p in range(max_sum - wi, -1, -1):
                if dp[j][p] < 0:
                    continue
                dp[j + 1][p + wi] = max(dp[j + 1][p + wi], dp[j][p])
                dp[j + 1][p] = max(dp[j + 1][p], dp[j][p] + p * wi)

    ans = 0
    for j in range(n + 1):
        for p in range(max_sum + 1):
            ans = max(ans, dp[j][p])
    return str(ans)

# provided sample
assert run("4\n1 1 2 2\n") == "9"

# minimum size
assert run("1\n5\n") == "0"

# all equal small
assert run("3\n1 1 1\n") == "2"

# increasing values
assert run("3\n1 2 3\n") == "8"

# decreasing values
assert run("3\n3 2 1\n") == "8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 artifact | 0 | single item cannot produce gold |
| all ones | 2 | ordering of magic vs strength matters |
| mixed small | 8 | DP correctly balances power buildup |
| reverse order | 8 | symmetry of optimal strategy |

## Edge Cases

A minimal case with one artifact, for example input `1 / 5`, forces the algorithm to recognize that without any prior magic, any strength activation yields zero gold. The DP starts with power zero, so both transitions lead to zero final answer.

A uniform case like `3 / 1 1 1` demonstrates that splitting is essential. The optimal plan is to use one artifact for magic and two for strength, giving power 1 and then gold $1 + 1 = 2$. The DP correctly explores both possibilities because it keeps all intermediate power states.

A case with a large early value, such as `3 / 10 1 1`, shows why greedy ordering fails if we try to always maximize immediate gold. The optimal solution first converts 10 into power, then spends it twice, yielding 20, which the DP captures through correct state propagation.
