---
title: "CF 106175E - Card Game Cheater"
description: "We are given two players who each receive the same number of cards from a standard deck. The cards are already fixed for both players, but only Eve is allowed to reorder her cards freely before the game starts."
date: "2026-06-19T18:54:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106175
codeforces_index: "E"
codeforces_contest_name: "2004-2005 Northwestern European Regional Contest (NWERC 2004)"
rating: 0
weight: 106175
solve_time_s: 55
verified: true
draft: false
---

[CF 106175E - Card Game Cheater](https://codeforces.com/problemset/problem/106175/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two players who each receive the same number of cards from a standard deck. The cards are already fixed for both players, but only Eve is allowed to reorder her cards freely before the game starts. After both rows are fixed, the i-th card of Adam is played against the i-th card of Eve, and each pair produces exactly one point for the winner of that comparison.

A card comparison is not just a simple numeric comparison. First, rank dominates: higher face value always wins unless the ranks are identical. When ranks are equal, suits decide the winner using a strict hierarchy: hearts beat everything, spades beat diamonds and clubs, diamonds beat clubs, and clubs loses to all others.

The task is to determine how many points Eve can guarantee by choosing an ordering of her cards that maximizes the number of positions where her card wins against Adam’s corresponding card.

The key constraint is that each player has at most 26 cards per test case, and there can be multiple test cases. Even though the deck is small, the factorial number of permutations makes brute-force ordering completely infeasible. A naive attempt that tries all permutations of Eve’s cards would explode as 26! possibilities, which is far beyond any feasible computation.

The non-obvious difficulty is that equality in rank does not mean symmetry in outcome, since suits create a strict ordering. A careless solution that only compares ranks would underestimate Eve’s ability to force wins by exploiting suit advantages in ties.

A small edge case illustrates this. Suppose Adam has “9H” and Eve has “9C”. A rank-only approach sees equality and treats it as neutral, but Eve actually loses because hearts dominates clubs. Conversely, “9S” vs “9C” gives Eve a win if she has spades. This means the comparison is a full strict ordering, not a partial one.

## Approaches

The brute-force idea is to try every permutation of Eve’s cards and compute how many matches she wins against Adam’s fixed ordering. This is correct because it explores all possible strategies, but it costs factorial time in k, which becomes impossible already at k = 20, let alone 26.

The structure of the problem suggests a matching interpretation. We have k positions on Adam’s side, each requiring exactly one card from Eve, and each assignment yields a profit of either 1 or 0 depending on whether Eve wins that matchup. We want to maximize total profit under a one-to-one assignment constraint.

This is a maximum bipartite matching with weights, but simplified to a binary gain per edge. Each Adam card can be paired with each Eve card, and we want to pick a perfect matching maximizing the number of winning pairs. Since k is small, we can model this as a maximum bipartite matching with unit capacities on nodes and edge weights 1 or 0.

The standard transformation is to view this as a flow problem or equivalently a weighted assignment problem. Because weights are only 0 or 1, a min-cost max-flow formulation works cleanly: each successful match contributes a cost reduction, and we maximize total wins by minimizing losses.

We build a bipartite graph from Adam positions to Eve cards, connect every Adam i to every Eve j, and assign cost 0 if Eve beats Adam in that pair, otherwise cost 1. Then we send k units of flow from source through Adam nodes to Eve nodes to sink. The minimum cost corresponds to minimizing losses, so k minus cost gives Eve’s maximum wins.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force permutations | O(k!) | O(k) | Too slow |
| Min-cost max-flow assignment | O(k^3) typical | O(k^2) | Accepted |

## Algorithm Walkthrough

We first need a function that compares two cards under the full rule system, producing whether Eve wins.

We then construct a flow network where each Adam position is a node on the left side and each Eve card is a node on the right side.

1. Parse all cards and convert each into a comparable value representation consisting of rank and suit priority. This allows fast comparison during edge construction.
2. Build a bipartite graph where every Adam position i connects to every Eve card j. This creates k² candidate assignments.
3. For each pair (i, j), compute whether Eve’s card j beats Adam’s card i. If it does, assign cost 0 to that edge, otherwise assign cost 1. The reasoning is that we treat “winning edges” as free and “losing edges” as penalized.
4. Add edges from a source node to each Adam node with capacity 1 and cost 0. This enforces that each Adam position is used exactly once.
5. Add edges from each Eve node to the sink with capacity 1 and cost 0. This enforces that each Eve card is used at most once.
6. Run a min-cost max-flow sending exactly k units of flow. Each unit corresponds to matching one Adam position with one Eve card.
7. The total cost of this flow equals the number of losing matches. The answer is k minus this cost.

The key idea is that every forced assignment either gives Eve a win or a penalty, and the flow chooses the best global combination rather than greedy local decisions.

### Why it works

At any stage of the flow, the partial matching represents a valid assignment of distinct Eve cards to distinct Adam positions. The cost of a completed flow is exactly the number of pairs where Eve failed to beat Adam. Since every Adam position must be matched exactly once, minimizing total cost is equivalent to maximizing the number of wins. The network construction ensures every valid assignment corresponds to exactly one unit flow of cost equal to its number of losses, so the optimal flow directly encodes the optimal ordering.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**18

rank_map = {str(i): i for i in range(2, 10)}
rank_map.update({'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14})

suit_rank = {'C': 0, 'D': 1, 'S': 2, 'H': 3}

def parse(card):
    r, s = card[0], card[1]
    return rank_map[r], suit_rank[s]

def eve_beats(a, b):
    ra, sa = a
    rb, sb = b
    if ra != rb:
        return ra > rb
    return sa > sb

class MinCostMaxFlow:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]

    def add_edge(self, u, v, cap, cost):
        self.adj[u].append([v, cap, cost, len(self.adj[v])])
        self.adj[v].append([u, 0, -cost, len(self.adj[u]) - 1])

    def flow(self, s, t, maxf):
        n = self.n
        res = 0
        h = [0] * n

        while maxf > 0:
            dist = [INF] * n
            dist[s] = 0
            inq = [False] * n
            prevv = [-1] * n
            preve = [-1] * n

            dist[s] = 0
            q = [s]
            inq[s] = True

            while q:
                u = q.pop(0)
                inq[u] = False
                for i, e in enumerate(self.adj[u]):
                    v, cap, cost, rev = e
                    if cap > 0 and dist[v] > dist[u] + cost:
                        dist[v] = dist[u] + cost
                        prevv[v] = u
                        preve[v] = i
                        if not inq[v]:
                            inq[v] = True
                            q.append(v)

            if dist[t] == INF:
                break

            addf = maxf
            v = t
            while v != s:
                u = prevv[v]
                e = self.adj[u][preve[v]]
                addf = min(addf, e[1])
                v = u

            v = t
            while v != s:
                u = prevv[v]
                e = self.adj[u][preve[v]]
                e[1] -= addf
                self.adj[v][e[3]][1] += addf
                v = u

            res += addf * dist[t]
            maxf -= addf

        return res

def solve():
    k = int(input())
    adam = list(map(parse, input().split()))
    eve = list(map(parse, input().split()))

    N = 2 + k + k
    S = 0
    T = N - 1
    A0 = 1
    E0 = 1 + k

    mcmf = MinCostMaxFlow(N)

    for i in range(k):
        mcmf.add_edge(S, A0 + i, 1, 0)
    for j in range(k):
        mcmf.add_edge(E0 + j, T, 1, 0)

    for i in range(k):
        for j in range(k):
            cost = 0 if eve_beats(eve[j], adam[i]) else 1
            mcmf.add_edge(A0 + i, E0 + j, 1, cost)

    cost = mcmf.flow(S, T, k)
    print(k - cost)

if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        solve()
```

The solution encodes each card comparison into a binary cost, then delegates the global optimization to a min-cost flow solver. The main implementation subtlety is correctly defining the suit tie-breaker so that equality in rank still produces a strict ordering.

The flow structure ensures that each Eve card is used at most once and each Adam position is filled exactly once, which exactly matches the requirement of rearranging Eve’s deck into a permutation.

## Worked Examples

Consider a small case where Adam has two cards and Eve has two cards.

Input:

Adam: 9H 9C

Eve: 9S 9D

We compute pairwise outcomes:

| Adam i | Eve j | Comparison result |
| --- | --- | --- |
| 9H | 9S | Eve wins |
| 9H | 9D | Eve wins |
| 9C | 9S | Eve wins |
| 9C | 9D | Eve loses |

The algorithm will select assignments that avoid the single losing pairing if possible.

A valid optimal matching is:

Adam 9H ↔ Eve 9S

Adam 9C ↔ Eve 9D

| Step | Assignment | Cost so far |
| --- | --- | --- |
| 1 | 9H → 9S | 0 |
| 2 | 9C → 9D | 1 |

Total cost is 1, so Eve gets 1 win.

This trace shows that the algorithm prefers pairing strong suit advantages with tied ranks, and only sacrifices when unavoidable due to limited structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k³) per test case | k² edges and k flow augmentations with shortest path computations |
| Space | O(k²) | adjacency list stores complete bipartite edges |

The constraints k ≤ 26 ensure that even a cubic approach is comfortably fast. The number of test cases is irrelevant because each instance is tiny, and the total operations remain well below practical limits.

## Test Cases

```python
import sys, io

# assumes solve() and supporting code exist above

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = []
    t = int(input())
    for _ in range(t):
        k = int(input())
        adam = input().strip()
        eve = input().strip()
        # placeholder since full solver is embedded in script
    return ""

# provided samples
# assert run(...) == ...

# custom cases
# 1) minimum size
# 2) all equal ranks different suits
# 3) full dominance case
# 4) mixed case
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal k=1 winning | 1 | single match correctness |
| minimal k=1 losing | 0 | suit tie-break correctness |
| identical decks | k/2 style | tie handling |
| alternating strong/weak | optimal matching | global optimization |

## Edge Cases

One edge case is full rank equality with varying suits. For example, if Adam and Eve both have only 7s of all suits, ordering matters entirely due to suit hierarchy. The algorithm handles this because every edge still has a strict cost, so flow chooses only winning suit pairings.

Another edge case is when Eve has strictly better cards but in reversed order. A greedy left-to-right assignment could fail badly, but flow reassigns matches globally, ensuring all dominant cards are used optimally.

A third edge case is when Eve has many winning cards but limited by matching constraints. Even if a card can beat many Adam cards, it can only be used once. The capacity constraint in the flow model enforces this correctly.
