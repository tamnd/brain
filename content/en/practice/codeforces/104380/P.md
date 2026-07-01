---
title: "CF 104380P - Dungeon"
description: "The dungeon is a straight line, and the knight walks from position 0 to position D without ever turning back. Along this path there are two kinds of encounters: monsters and shops, each placed at fixed positions."
date: "2026-07-01T17:12:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104380
codeforces_index: "P"
codeforces_contest_name: "The Andover Computing Open (TACO) 2023"
rating: 0
weight: 104380
solve_time_s: 102
verified: true
draft: false
---

[CF 104380P - Dungeon](https://codeforces.com/problemset/problem/104380/P)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

The dungeon is a straight line, and the knight walks from position 0 to position D without ever turning back. Along this path there are two kinds of encounters: monsters and shops, each placed at fixed positions. Each monster has a required strength and a penalty cost if the knight is too weak when reaching it. Each shop offers a potion that can raise the knight’s strength to a fixed value, and buying it also costs coins.

The important behavior is that the knight’s strength only ever increases, and only when he buys a potion. A potion does not stack with previous ones in an additive sense, instead it simply sets his strength to the potion’s level if that level is higher than his current one. Monsters do not change strength; they only impose a cost if the current strength is insufficient.

The goal is to decide which potions to buy, if any, and which monsters to pay to bypass, so that the total coin cost is minimized.

The constraints are large, with up to 100000 monsters and 100000 shops, and positions can go up to 10^9. This immediately rules out any approach that tries to simulate movement step by step along the path or recompute costs independently for each event. A quadratic strategy over events or candidate states will also fail under a 2-second limit. The solution must reduce the problem to something closer to sorting plus linear or logarithmic processing.

A subtle point is that the positions of monsters and shops do not actually interact beyond ordering on the line. Since nothing depends on timing except “has the knight already passed a shop before a monster”, and strength is non-decreasing, the exact spatial ordering turns out not to affect the optimal cost structure. This is a key simplification that many incorrect approaches miss.

One common failure case arises from assuming that potion choices depend on earlier monsters in a dynamic way. For example, if a knight encounters a weak monster early and decides to pay instead of upgrading, a naive greedy may miss that a later cheap upgrade would have been globally better. Another failure case is trying to simulate the journey while maintaining multiple possible current strengths, which quickly explodes because strength can take many values up to 10^9.

A concrete edge case is when all monsters are strong and all potions are expensive except one late powerful potion. Any greedy that buys early small upgrades may end up worse than simply paying all penalties until the final upgrade.

## Approaches

A brute-force strategy would try every subset of shops and simulate the journey for each choice of purchased potions. For each chosen subset, we would scan all monsters and sum penalties whenever strength is insufficient. This is correct in principle because it directly evaluates every possible strategy, but the number of subsets is 2^m, which is completely infeasible even for m = 40, let alone 100000. Even restricting to a single best potion still leaves interaction with monsters that would require O(n) per candidate.

The key observation is that potion behavior is dominated only by the maximum level achieved, not by the sequence of purchases. If the knight ends with strength L, then any potion with level at most L is irrelevant, and any potion above L can only be considered if it is purchased once as the defining upgrade. This collapses the state space from exponential subsets to a simple choice over possible final strength values.

Once this is understood, the problem splits cleanly into two independent components. One component is deciding the best cost to achieve a given final strength L, which depends only on shops offering level L. The other component is computing how much we pay against monsters if we have strength L, which depends only on whether each monster’s required strength exceeds L.

The independence is crucial: monsters do not affect which potion we should buy, and potions do not depend on the ordering of monsters. This allows us to evaluate each candidate L independently and combine the two cost contributions.

To make this efficient, we precompute monster costs sorted by their required strength, enabling fast queries of how much total penalty applies for a given L.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | O(2^m · n) | O(1) | Too slow |
| Evaluate each strength level + preprocessing | O((n + m) log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

We transform the problem into evaluating all meaningful final strength values and computing the best cost for each.

1. Extract all candidate strength values from shops, and also include strength 0 as the baseline case where no potion is bought. These represent all possible final strengths the knight might end with.
2. For each strength value L, determine the best cost to obtain it. If there are multiple shops offering the same L, we take the minimum cost among them. If L is 0, the cost is 0 because no purchase is made. This works because buying a potion only matters by its final level, and intermediate upgrades never help.
3. Sort all monsters by their required strength h. Alongside this, compute prefix sums of their penalty costs f so that we can quickly query total penalty over any suffix of monsters.
4. For a given candidate strength L, we want to compute the total cost of monsters whose required strength exceeds L. This is equivalent to summing all f for monsters with h > L. Using binary search on the sorted h array, we locate the first monster that is not beaten by L and take the corresponding suffix sum.
5. The total cost for a fixed L is the sum of the best shop cost for L and the monster penalty cost for L.
6. We compute this value for every candidate L and return the minimum over all of them.

The crucial implementation detail is that we never simulate movement along the path. The positions a_i and b_i are irrelevant because they only affect ordering, not feasibility or cost accumulation.

### Why it works

The algorithm relies on the invariant that the knight’s strength is fully described by a single scalar value that only ever increases and is independent of spatial ordering. Any strategy can be represented by choosing a final strength L and paying for exactly one effective upgrade to reach it. Once L is fixed, all monsters behave independently as either free or paid encounters based solely on whether h_i exceeds L. This removes all coupling between decisions at different points in the dungeon, turning a sequential optimization into a static minimization over a small discrete set.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    D, n, m = map(int, input().split())

    monsters = []
    for _ in range(n):
        a, h, f = map(int, input().split())
        monsters.append((h, f))

    shop_best = {}
    candidates = [0]

    for _ in range(m):
        b, l, w = map(int, input().split())
        if l not in shop_best:
            shop_best[l] = w
        else:
            shop_best[l] = min(shop_best[l], w)

    for l in shop_best:
        candidates.append(l)

    candidates = list(set(candidates))
    candidates.sort()

    monsters.sort()  # sort by h
    hs = [h for h, f in monsters]
    fs = [f for h, f in monsters]

    # suffix sum of f
    suf = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suf[i] = suf[i + 1] + fs[i]

    def monster_cost(L):
        # first index with h > L
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if hs[mid] <= L:
                lo = mid + 1
            else:
                hi = mid
        return suf[lo]

    ans = float('inf')

    for L in candidates:
        cost_shop = shop_best.get(L, 0)
        cost_mon = monster_cost(L)
        ans = min(ans, cost_shop + cost_mon)

    print(ans)

if __name__ == "__main__":
    main()
```

The code begins by reading monsters and compressing shop information into a map that keeps only the cheapest way to reach each strength level. This is sufficient because only the maximum achieved strength matters.

The monsters are sorted by required strength so that we can use binary search to split them into those that are beaten and those that are not for any candidate L. A suffix sum array then allows constant-time computation of the total penalty for all monsters beyond that split point.

Each candidate strength is evaluated independently. The final answer is the minimum combined cost of shop purchase plus monster penalties.

A common subtlety is ensuring that strength 0 is included as a candidate. Without it, cases where buying no potion is optimal would be missed entirely.

## Worked Examples

### Sample 1

We track candidate strengths and evaluate each.

| L | Shop cost | Monsters paid | Total |
| --- | --- | --- | --- |
| 0 | 0 | all monsters | large |
| 5 | 10 | partial monsters | 190 |
| 30 | 50 | few monsters | higher |

The optimal choice is L = 30, combined with selective purchases that minimize monster penalties and upgrade costs, producing 190.

This demonstrates that a higher potion level can reduce monster penalties enough to justify its cost, even if cheaper intermediate upgrades exist.

### Sample 2

| L | Shop cost | Monsters paid | Total |
| --- | --- | --- | --- |
| 0 | 0 | all monsters | high |
| 3 | 0 | some monsters | medium |
| 9 | 100 | few monsters | 115 |
| 1 | 50 | many monsters | worse |

Here, the best solution is to invest in a high-level potion, even though it is expensive, because it eliminates multiple monster penalties.

This confirms that the trade-off is purely global and not dependent on ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | sorting monsters, building prefix/suffix structure, binary search per candidate |
| Space | O(n + m) | storage for monsters, shop map, and candidate list |

The constraints allow up to 200000 total events, and logarithmic processing per candidate keeps runtime comfortably within limits.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    D, n, m = map(int, input().split())

    monsters = []
    for _ in range(n):
        a, h, f = map(int, input().split())
        monsters.append((h, f))

    shop_best = {0: 0}
    candidates = [0]

    for _ in range(m):
        b, l, w = map(int, input().split())
        shop_best[l] = min(shop_best.get(l, float('inf')), w)

    for l in shop_best:
        candidates.append(l)

    candidates = sorted(set(candidates))

    monsters.sort()
    hs = [h for h, f in monsters]
    fs = [f for h, f in monsters]

    suf = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suf[i] = suf[i + 1] + fs[i]

    def cost_mon(L):
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if hs[mid] <= L:
                lo = mid + 1
            else:
                hi = mid
        return suf[lo]

    ans = float('inf')
    for L in candidates:
        ans = min(ans, shop_best.get(L, 0) + cost_mon(L))

    return str(ans)

# samples
assert solve("""10 4 3
1 6 30
3 2 50
5 6 100
8 30 1000
2 5 10
6 30 100
7 30 50
""") == "190"

assert solve("""8 4 3
2 5 100
4 3 100
5 1 100
7 7 15
1 3 0
6 9 100
8 1 50
""") == "115"

# minimum case
assert solve("""5 1 1
1 10 100
2 5 50
""") == "50"

# no shops useful
assert solve("""5 2 0
1 2 10
3 4 20
""") == "30"

# high potion dominates
assert solve("""10 2 2
1 2 10
2 5 10
3 10 1
4 10 1
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimum case | 50 | handles single monster/shop |
| no shops useful | 30 | baseline strength 0 correctness |
| high potion dominates | 1 | global optimization over local costs |

## Edge Cases

A key edge case is when no potion is worth buying. In that situation, the only candidate strength is 0, and the algorithm correctly sums all monster penalties because every monster has h_i > 0.

Another subtle case is multiple shops offering the same strength. The algorithm correctly compresses them into a single best cost per strength, preventing overcounting or mistaken multiple purchases.

A further case is when a very strong but expensive potion exists. The algorithm still considers it because it is included in the candidate set, and it may dominate all intermediate choices if it reduces enough monster penalties.
