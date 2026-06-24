---
title: "CF 105244C - Space Expedition"
description: "A space explorer visits a fixed sequence of celestial objects. Each object offers some scientific value if studied, but also consumes two limited resources: energy and time."
date: "2026-06-24T07:31:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105244
codeforces_index: "C"
codeforces_contest_name: "Dynamic Programming, SPbSU 2024, Training 2"
rating: 0
weight: 105244
solve_time_s: 52
verified: true
draft: false
---

[CF 105244C - Space Expedition](https://codeforces.com/problemset/problem/105244/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

A space explorer visits a fixed sequence of celestial objects. Each object offers some scientific value if studied, but also consumes two limited resources: energy and time. The explorer must process the objects in the given order and decide for each one whether to study it or skip it. Once chosen, an object fully consumes its required energy and time.

The goal is to select a subsequence of these objects, respecting the fixed order, such that the total energy used does not exceed K and the total time does not exceed M, while maximizing the total scientific value.

The output is twofold. First, we report the maximum achievable value. Second, we output the indices of the chosen objects in increasing order of visitation.

The constraints are tight enough to suggest a dynamic programming approach. With N up to 100 and both resource limits also at most 100, a state space that tracks how much energy and time have been used per prefix of objects remains small. A naive subset enumeration would require examining all 2^N subsets, which already becomes infeasible at around N=40, and here N reaches 100, so exponential search is immediately ruled out.

A subtle issue arises from the ordering constraint. This is not a standard knapsack where items can be reordered freely, but the decision still depends only on whether to take or skip each item in sequence, which preserves the classic DP structure.

Edge cases appear when no object can be taken within constraints. For example, if K=5 and M=5 and every object requires at least 6 energy or 6 time, no selection is valid. In that case the correct output is a single zero, not an empty sequence or a zero value followed by an empty line. A naive reconstruction approach that always prints a sequence header can easily misformat this case.

Another corner case is when multiple optimal solutions exist. Since any valid sequence is acceptable, the DP does not need to enforce lexicographic ordering, but reconstruction must still be consistent with stored decisions.

## Approaches

The brute-force strategy is to try every subset of objects while preserving order implicitly by checking inclusion masks. For each subset, we sum energy, time, and value, then verify feasibility. This works conceptually because it directly matches the problem definition, but it requires evaluating 2^N subsets. With N=100, this means roughly 10^30 candidates, which is far beyond any computational limit.

The structure of the problem reveals that the only interaction between decisions is through cumulative resource usage. Each object contributes independently to value, energy, and time, and once processed, it does not affect future transitions except through remaining capacity. This independence suggests a dynamic programming formulation over prefixes and resource budgets.

At each object, we decide whether to skip it or take it, and if taken, we reduce both remaining capacities. This leads naturally to a three-dimensional DP over index, energy used, and time used. Since N, K, and M are all at most 100, the total number of states is about one million, and each transitions in constant time, which is efficient.

To reconstruct the chosen sequence, we store decisions during DP transitions, remembering whether a state came from taking or skipping the current item. Backtracking from the final state with maximum value yields the required sequence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^N · N) | O(N) | Too slow |
| Optimal DP | O(N · K · M) | O(N · K · M) | Accepted |

## Algorithm Walkthrough

We define dp[i][j][k] as the maximum value achievable using the first i items while spending exactly j energy and k time, or treating unreachable states as negative infinity.

1. Initialize all dp states as unreachable except dp[0][0][0] which is zero. This represents starting with no items and no resource usage.
2. Iterate over items from 1 to N. For each item, we propagate transitions from all reachable states of the previous layer.
3. For each state dp[i−1][j][k], we first consider skipping the current item. We update dp[i][j][k] with the same value if it improves the result. This preserves feasibility without consuming resources.
4. We also consider taking the current item, provided j + energy[i] ≤ K and k + time[i] ≤ M. We update dp[i][j + F][k + T] with dp[i−1][j][k] + V[i]. This encodes the decision of including the item.
5. Alongside dp updates, we store a parent pointer that records whether a state came from skipping or taking, and from which previous (j, k) it originated.
6. After processing all items, we scan all dp[N][j][k] to find the maximum value and its corresponding state.
7. We reconstruct the path by moving backward through stored parent pointers until reaching i = 0, collecting all indices where the decision was to take the item.

Why it works comes from the fact that every state (i, j, k) summarizes all possible ways to reach exactly that resource usage using the first i items. Any optimal solution must correspond to some valid state in this space, and transitions enumerate all legal decisions without omission or duplication. Since each transition preserves correctness of accumulated value and respects constraints, the maximum over the final layer must be globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, K, M = map(int, input().split())
    items = []
    for _ in range(N):
        v, f, t = map(int, input().split())
        items.append((v, f, t))

    NEG = -10**18
    dp = [[[NEG] * (M + 1) for _ in range(K + 1)] for _ in range(N + 1)]
    parent = [[[-1] * (M + 1) for _ in range(K + 1)] for _ in range(N + 1)]
    take = [[[-1] * (M + 1) for _ in range(K + 1)] for _ in range(N + 1)]

    dp[0][0][0] = 0

    for i in range(1, N + 1):
        v, f, t = items[i - 1]
        for j in range(K + 1):
            for k in range(M + 1):
                if dp[i - 1][j][k] == NEG:
                    continue

                if dp[i][j][k] < dp[i - 1][j][k]:
                    dp[i][j][k] = dp[i - 1][j][k]
                    parent[i][j][k] = (j, k)
                    take[i][j][k] = 0

                nj, nk = j + f, k + t
                if nj <= K and nk <= M:
                    if dp[i][nj][nk] < dp[i - 1][j][k] + v:
                        dp[i][nj][nk] = dp[i - 1][j][k] + v
                        parent[i][nj][nk] = (j, k)
                        take[i][nj][nk] = 1

    best_val = 0
    bj = bk = 0
    for j in range(K + 1):
        for k in range(M + 1):
            if dp[N][j][k] > best_val:
                best_val = dp[N][j][k]
                bj, bk = j, k

    if best_val == 0:
        print(0)
        return

    res = []
    i, j, k = N, bj, bk
    while i > 0:
        pj, pk = parent[i][j][k]
        if take[i][j][k] == 1:
            res.append(i)
        j, k = pj, pk
        i -= 1

    res.reverse()
    print(best_val)
    print(*res)

if __name__ == "__main__":
    solve()
```

The DP table is built layer by layer over items, ensuring that each state only depends on the previous item index. The skip transition copies previous values forward, while the take transition adds value and increases both resource counters.

The parent and take arrays store enough information to reconstruct the chosen subsequence. The reconstruction walks backward from the best final state until reaching the empty prefix, collecting indices where the take flag is set.

A subtle point is that we only initialize dp[0][0][0] and treat all others as unreachable, which prevents invalid partial states from influencing transitions.

## Worked Examples

Consider a small instance with three objects and moderate constraints. Suppose the optimal solution involves taking the first and third objects but skipping the second due to resource pressure.

We track dp states conceptually for one valid path:

| Step | Item | State (energy, time) | Value | Action |
| --- | --- | --- | --- | --- |
| 0 | - | (0, 0) | 0 | start |
| 1 | 1 | (20, 3) | 100 | take |
| 2 | 2 | (20, 3) | 100 | skip |
| 3 | 3 | (30, 7) | 160 | take |

This trace shows how skipping preserves state, allowing later items to be taken when earlier ones would have blocked capacity.

Now consider a case where all items exceed constraints.

Input:

```
2 5 5
10 6 1
20 1 6
```

Here neither item fits alone. The DP never improves from dp[0][0][0], so the best value remains zero and no reconstruction is possible.

| Step | Item | State | Best Value |
| --- | --- | --- | --- |
| 0 | - | (0,0) | 0 |
| 1 | 1 | invalid | 0 |
| 2 | 2 | invalid | 0 |

This confirms that the algorithm correctly avoids selecting infeasible items.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N · K · M) | Each of N items processes all K·M states once with constant transitions |
| Space | O(N · K · M) | Full DP and reconstruction tables store state for each prefix |

The total number of operations is about one million, which fits comfortably within the limits for N, K, M up to 100. Memory usage is also safe since a few million integers fit within the given 512 MiB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return capture(solve)

def capture(func):
    import sys, io
    old = sys.stdout
    sys.stdout = io.StringIO()
    func()
    out = sys.stdout.getvalue()
    sys.stdout = old
    return out.strip()

# minimum case
assert run("""1 10 10
5 3 3
""") == "5\n1"

# no valid items
assert run("""2 5 5
10 6 1
20 1 6
""") == "0"

# choose all items
assert run("""2 10 10
3 4 4
2 3 3
""") == "5\n1 2"

# must skip due to constraints
assert run("""3 10 10
8 6 6
7 6 6
10 4 4
""") == "10\n3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single item fits | value + index | base case correctness |
| no feasible items | 0 | empty solution handling |
| all items fit | full sequence | accumulation correctness |
| selective skipping | partial sequence | DP decision logic |

## Edge Cases

When every item is too expensive in either energy or time, the DP never advances beyond the initial state. The algorithm correctly detects this because the best value remains zero and no parent pointers for taken items exist. The output becomes a single zero, matching the required format.

When multiple optimal paths exist, for example two different subsets yielding the same maximum value under identical constraints, the reconstruction follows whichever transitions were last written into the DP table. Since the problem allows any valid answer, this non-determinism is acceptable and still produces a correct subsequence.

When K or M equals zero, only items with zero resource consumption would be selectable. Since constraints guarantee F ≥ 1 and T ≥ 1, the only possible result is zero value, which the algorithm handles naturally through the initialization state.
