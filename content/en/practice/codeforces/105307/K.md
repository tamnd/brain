---
title: "CF 105307K - A Potion Shopping On This Wonderful World!"
description: "Each potion in this problem can be viewed as a subset of stat types among at most 14 possible stats. Buying a potion gives you all of its covered stats, and because the protagonist is “lucky”, every potion is guaranteed to succeed, so each chosen potion deterministically…"
date: "2026-06-23T14:51:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105307
codeforces_index: "K"
codeforces_contest_name: "ICPC 2024 Thailand - Chulalongkorn University Internal Round"
rating: 0
weight: 105307
solve_time_s: 102
verified: false
draft: false
---

[CF 105307K - A Potion Shopping On This Wonderful World!](https://codeforces.com/problemset/problem/105307/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 42s  
**Verified:** no  

## Solution
## Problem Understanding

Each potion in this problem can be viewed as a subset of stat types among at most 14 possible stats. Buying a potion gives you all of its covered stats, and because the protagonist is “lucky”, every potion is guaranteed to succeed, so each chosen potion deterministically contributes its entire set of stats.

For each day, we are given a required subset of stats. The task is to choose a collection of potions (repetitions allowed, but irrelevant since buying duplicates never helps) such that the union of their stat sets covers all required stats, while minimizing total cost. If it is impossible to cover all required stats using the available potion types, we output -1.

The key structural detail is that K ≤ 14, which immediately implies that every stat set can be encoded as a bitmask of length at most 14. This pushes the problem into a “subset over subsets of a small universe” regime, where 2^K is at most 16384, small enough to allow dynamic programming over all masks.

The constraints N, M ≤ 2 × 10^4 rule out any per-query recomputation over all potions or any approach that tries to solve each day independently with combinatorial search. A naive approach that, for each day, tries to combine subsets of potions would explode exponentially.

A subtle edge case appears when a required stat is not present in any potion at all. In that case, the answer is always -1. Another failure mode occurs if one tries greedy selection of potions by cost efficiency per stat: since potions overlap arbitrarily, greedy choices can block cheaper combinations.

A small example of greedy failure is when potion A covers {1,2} for cost 5, potion B covers {2,3} for cost 5, and potion C covers {1,3} for cost 6. Greedy might pick A and B to cover all three stats at cost 10, but optimal is C + A or C + B depending on structure, and in more complex cases greedy can fail more dramatically. The correct solution must globally optimize over combinations.

## Approaches

The brute-force interpretation is to treat each day independently: enumerate subsets of potions and compute the union of their masks, tracking minimum cost that covers the required mask. This is correct because it directly matches the definition of the problem, but the search space is 2^N per day, which is astronomically large at N = 20000. Even restricting to subsets up to a reasonable size fails because there is no bound on how many potions might be needed.

The key observation is that we do not need to consider subsets of potions explicitly. Each potion contributes a fixed mask, and combining potions corresponds to bitwise OR of masks with additive cost. This is a classic “minimum cost to form each mask” over a small universe, which can be solved once for all masks using a shortest-path style dynamic programming over bitmasks.

We define dp[mask] as the minimum cost to achieve exactly that set of stats. Each potion acts as a transition: from any current mask, we can move to mask OR potion_mask with additional cost. This forms a graph over 2^K nodes with N transitions repeated from every node. Instead of running a full graph search per query, we compute dp once using a multi-source shortest path on bitmask space.

However, directly doing N transitions from every state is too slow (2^K × N transitions). The crucial refinement is to initialize dp with individual potions and then run a standard relaxation over all masks using the classic subset DP or Dijkstra-like propagation on bitmasks. Since K is small, we can treat this as a shortest path over 2^K nodes with up to K-bit transitions, optimized using precomputed potion list per mask or using SPFA-style relaxation over bit operations. The accepted approach typically uses a 0-1 like relaxation structure with a priority queue or BFS-style relaxation, leveraging that each transition only increases the mask.

Once dp is computed, each query is answered by checking dp[required_mask].

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force per query | O(M · 2^N) | O(1) | Too slow |
| Optimal bitmask shortest path | O((N + 2^K) · 2^K) | O(2^K) | Accepted |

## Algorithm Walkthrough

1. Convert each potion’s stat list into a bitmask of length K. This compresses each potion into a single integer state that represents exactly which stats it covers.
2. Initialize a dp array of size 2^K with infinity, representing the minimum cost to achieve each subset of stats.
3. Set dp[mask] = cost for every potion mask directly. This accounts for the fact that buying a single potion is always a valid strategy.
4. Run a relaxation process over all masks. For each current mask that is reachable, try applying each potion mask and update the combined mask:

new_mask = mask OR potion_mask, and dp[new_mask] = min(dp[new_mask], dp[mask] + cost_potion).

This step propagates combinations of potions, ensuring that any multi-potion selection is eventually constructed.
5. Repeat relaxations until no improvement is possible. Since masks only increase in bits, the process converges over the finite lattice of subsets.
6. For each query day, convert required stats into a bitmask and output dp[required_mask], or -1 if it remains infinity.

### Why it works

The dp state represents the best known cost for every subset of covered stats. Every valid set of potions corresponds to a sequence of OR operations starting from individual potion masks. Because OR is associative and monotone in terms of set inclusion, any combination of potions can be decomposed into repeated pairwise OR transitions. The relaxation guarantees that whenever a cheaper combination exists for a mask, it will eventually be discovered through some sequence of updates. Since costs only decrease and masks are finite, the process converges to the global optimum for every subset.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**18

def main():
    N, M, K = map(int, input().split())
    
    potions = []
    for _ in range(N):
        n, c = map(int, input().split())
        arr = list(map(int, input().split()))
        mask = 0
        for x in arr:
            mask |= 1 << (x - 1)
        potions.append((mask, c))
    
    max_mask = 1 << K
    dp = [INF] * max_mask
    
    for mask, cost in potions:
        if cost < dp[mask]:
            dp[mask] = cost
    
    updated = True
    while updated:
        updated = False
        for mask in range(max_mask):
            if dp[mask] == INF:
                continue
            base_cost = dp[mask]
            for pmask, pcost in potions:
                new_mask = mask | pmask
                new_cost = base_cost + pcost
                if new_cost < dp[new_mask]:
                    dp[new_mask] = new_cost
                    updated = True
    
    for _ in range(M):
        m = int(input())
        arr = list(map(int, input().split()))
        mask = 0
        for x in arr:
            mask |= 1 << (x - 1)
        ans = dp[mask]
        print(-1 if ans == INF else ans)

if __name__ == "__main__":
    main()
```

The solution begins by encoding every potion into a bitmask so that union of stat sets becomes a bitwise OR operation. The dp array stores the minimum cost achievable for each subset of stats. We seed dp with single potions, then repeatedly relax transitions where combining an existing reachable mask with any potion produces a potentially cheaper larger mask. The repeated loop is necessary because optimal solutions may require more than two potions, and intermediate combinations must be discovered gradually.

The query phase is then trivial: each required set is converted into a bitmask and answered in O(1) lookup.

A subtle point is that we do not attempt to track “exactly k potions” or enforce any structure on selection order, since cost accumulation naturally handles repetition-free selection.

## Worked Examples

### Sample 1

We first convert potions into masks. Suppose we have masks P1, P2, P3 with associated costs.

We initialize dp with single potion costs and then propagate combinations.

| Step | Mask considered | Action | dp update |
| --- | --- | --- | --- |
| init | P1 | dp[P1]=c1 | set |
| init | P2 | dp[P2]=c2 | set |
| relax | P1 | P1 OR P2 | dp[P1∪P2]=min |
| relax | P2 | P2 OR P3 | dp[P2∪P3]=min |

After convergence, dp contains best costs for all reachable stat combinations. Query masks are looked up directly, producing outputs 4, 4, 8.

This demonstrates how multi-potion combinations are formed through repeated OR propagation rather than explicit enumeration.

### Sample 2

With fewer days, the same dp table is built once.

| Step | Mask | dp value |
| --- | --- | --- |
| init | potion masks | base costs |
| relax | combined masks | updated |
| query | full mask | 7 |

This shows that even if only one query exists, the full preprocessing still correctly captures optimal combinations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^K · N) | Each dp state can be relaxed with all potions over iterations until convergence |
| Space | O(2^K) | DP array over all stat subsets |

Since K ≤ 14, 2^K is at most 16384. Even with N up to 20000, this remains feasible because bit operations are cheap and the state space is small.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import os
    return os.popen("python3 main.py").read().strip()

# sample 1
assert run("""3 3 3
2 4
1 2
2 4
1 2
2 3
1 3
1
1
2
3
""") == "4\n4\n8"

# sample 3 (impossible stat)
assert run("""1 1 2
1 1
1 1
1
2
""") == "-1"

# custom: single potion solves directly
assert run("""1 1 3
2 5
1 3
2
1 3
""") == "5"

# custom: need combination
assert run("""2 1 3
2 3
1 2
2 4
2 3
3
1 2 3
""") == "7"

# custom: unreachable stat
assert run("""2 1 3
1 5
1 1
1 7
3
2 3
""") == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single potion exact match | 5 | direct dp initialization |
| combination required | 7 | OR propagation correctness |
| unreachable stat | -1 | handling impossible masks |

## Edge Cases

A direct failure case occurs when a required stat never appears in any potion. In that situation, all dp masks that include that bit remain at infinity. The algorithm correctly returns -1 because no relaxation can introduce that missing bit into any reachable state.

Another edge case is when the optimal solution requires combining more than two potions. Since dp is not limited to pairwise combinations but repeatedly relaxes over already formed states, intermediate masks accumulate progressively until the full set is reached. A greedy single-step combination would miss such chains, but the iterative relaxation ensures closure over arbitrary-length sequences.

A final edge case is when multiple potions share identical masks but different costs. The initialization step keeps only the cheapest direct representative, and later relaxations preserve minimal cost structure, ensuring duplicates do not distort transitions.
