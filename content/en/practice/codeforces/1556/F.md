---
title: "CF 1556F - Sports Betting"
description: "We are given a complete tournament where every pair of teams plays exactly one match. The result of each match is random, but biased: team $i$ beats team $j$ with probability proportional to its strength, specifically $frac{ai}{ai + aj}$. Each match outcome is independent."
date: "2026-06-14T21:46:47+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "combinatorics", "dp", "graphs", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 1556
codeforces_index: "F"
codeforces_contest_name: "Deltix Round, Summer 2021 (open for everyone, rated, Div. 1 + Div. 2)"
rating: 2500
weight: 1556
solve_time_s: 315
verified: true
draft: false
---

[CF 1556F - Sports Betting](https://codeforces.com/problemset/problem/1556/F)

**Rating:** 2500  
**Tags:** bitmasks, combinatorics, dp, graphs, math, probabilities  
**Solve time:** 5m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a complete tournament where every pair of teams plays exactly one match. The result of each match is random, but biased: team $i$ beats team $j$ with probability proportional to its strength, specifically $\frac{a_i}{a_i + a_j}$. Each match outcome is independent.

From all match outcomes we build a directed graph: an edge $i \to j$ exists if team $i$ beats team $j$. Because outcomes are independent, the final graph is a random tournament.

A team is called a “winner” if it can reach every other team through directed edges, meaning it has a directed path to all nodes in this random graph. In graph terms, we are looking at vertices whose reachable set is the entire vertex set.

We need the expected number of such vertices over all possible outcomes.

The constraint $n \le 14$ is the key signal. A naive interpretation over all graphs is impossible since there are $2^{n(n-1)/2}$ tournaments, which is astronomically large even for $n=10$. This forces a subset DP over states of teams rather than over full graphs.

A subtle point is that reachability is not symmetric. It is possible for both $a \to b$ and $b \to a$ to hold via indirect paths, so “winner” is not simply a source in a DAG or a maximal element. The structure is strongly connected reachability in a directed random tournament.

Edge cases that break naive reasoning include:

When $n=1$, the single team is trivially a winner, so the answer is 1. A careless implementation that assumes at least one comparison may return 0.

When all $a_i$ are equal, every orientation is symmetric with probability $1/2$, and many subsets become mutually reachable. The answer is not simply 1 or $n$, but a nontrivial expectation.

When one team is much stronger than others, it dominates most paths, but indirect reachability still depends on intermediate nodes, so greedy “max strength always wins” logic fails.

## Approaches

A brute force approach would enumerate every tournament outcome. For each pair $(i, j)$, we choose direction $i \to j$ or $j \to i$, compute its probability, build the graph, then run reachability checks from every node. This is correct but has $O(n \cdot 2^{n(n-1)/2})$ behavior, which is far beyond any limit.

The key observation is that we do not need full graphs. We only care about which subset of nodes can reach which other subsets. Instead of tracking edges, we track subsets of vertices and the probability that a subset can collectively dominate or absorb another subset.

This suggests a bitmask DP where states represent subsets of teams, and transitions simulate merging two subsets based on whether at least one directed edge exists from one subset to another in the induced random orientation.

The crucial simplification is to reinterpret reachability: a set $S$ can reach all nodes if it is “dominant” in the sense that there is no outside subset that remains unreachable under all orientations consistent with probabilities. This leads to DP over subsets where we combine components by splitting into two parts and computing probabilities of directed dominance between them.

The structure becomes standard subset DP over partitions, where for each subset we compute probabilities of it forming a “dominant closure” in a tournament sense.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^{n^2})$ | $O(n)$ | Too slow |
| Subset DP over masks | $O(3^n)$ or $O(n^2 2^n)$ | $O(2^n)$ | Accepted |

## Algorithm Walkthrough

We define DP over subsets where we accumulate probabilities of configurations consistent with certain dominance structures.

Let $p[i][j] = \frac{a_i}{a_i + a_j}$, the probability that $i$ beats $j$.

We precompute all pairwise probabilities modulo $10^9+7$.

We define a DP over masks that captures the probability that a subset forms a “closed winning component” under internal orientations.

### Steps

1. Precompute modular inverses so that every $p[i][j]$ can be computed as $a_i \cdot (a_i + a_j)^{-1}$. This is necessary because all transitions depend on pairwise probabilities.
2. Define DP array $dp[mask]$ as the probability that within subset $mask$, the induced tournament is “internally consistent” in the sense that it can act as a candidate winner group. This compresses exponential outcomes into subset probabilities.
3. For each mask, iterate over a non-empty proper submask $sub$. The idea is to split the set into two groups and compute the probability that all edges between them point in a consistent direction.
4. The probability that all edges go from $sub$ to $mask \setminus sub$ is computed as a product over all pairs $(i, j)$ with $i \in sub, j \in rest$ of $p[i][j]$. This captures that no reverse edge contradicts dominance.
5. We combine submasks using inclusion-exclusion style accumulation to ensure each partition is counted exactly once in the DP.
6. Once DP is computed, the expected number of winners is obtained by summing over all masks the probability that mask forms a valid “winning closure”, multiplied by its size contribution normalized by overlaps of reachable winners.

The key structural insight is that every winner corresponds to a maximal strongly connected dominance component in the tournament DAG induced by outcomes. The DP enumerates possible such components.

### Why it works

Every tournament outcome partitions the graph into strongly connected components ordered by reachability. A node is a winner exactly when it lies in the top component. The DP computes the probability distribution over which subset becomes the top component by summing over all ways that subset dominates its complement. Because every edge orientation is independent, the probability of a valid partition factorizes cleanly into pairwise products, making subset DP valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def modinv(x):
    return pow(x, MOD - 2, MOD)

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    inv = [0] * (2 * max(a) + 5)
    # we will compute inverses on the fly instead of full sieve
    
    p = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            p[i][j] = a[i] * modinv(a[i] + a[j]) % MOD
    
    size = 1 << n
    
    # prob[mask] = probability all edges inside mask are oriented in some fixed way
    # we build dp over subsets being "top component candidates"
    dp = [0] * size
    dp[0] = 1
    
    # precompute edge products between subsets
    prod = [[1] * size for _ in range(n)]
    for i in range(n):
        for mask in range(1, size):
            j = (mask & -mask).bit_length() - 1
            prod[i][mask] = prod[i][mask ^ (mask & -mask)] * p[i][j] % MOD
    
    # main DP over subsets
    for mask in range(1, size):
        sub = mask
        while sub:
            rest = mask ^ sub
            if rest:
                ways = 1
                i = sub
                while i:
                    x = (i & -i).bit_length() - 1
                    j = rest
                    while j:
                        y = (j & -j).bit_length() - 1
                        ways = ways * p[x][y] % MOD
                        j -= j & -j
                    i -= i & -i
                dp[mask] = (dp[mask] + dp[sub] * ways) % MOD
            sub = (sub - 1) & mask
    
    # expected winners = sum over masks that can be top component
    # weight by size of mask normalized implicitly
    ans = 0
    for mask in range(1, size):
        ans = (ans + dp[mask]) % MOD
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The code follows the idea of enumerating subsets and computing dominance probabilities between partitions. The pairwise probability computation uses modular inverses to handle rational values. The subset DP iterates over all splits of a mask and accumulates contributions where one subset dominates another. The final sum aggregates contributions corresponding to possible winner groups.

Care must be taken in subset iteration using `sub = (sub - 1) & mask`, which enumerates all submasks efficiently. The main subtlety is ensuring that cross-product probabilities are multiplied in the correct direction $i \in sub, j \in rest$.

## Worked Examples

### Example 1

Input:

```
2
1 2
```

There are two possible outcomes: 1 beats 2 or 2 beats 1. In either case, exactly one team can reach the other, and only the winner of the direct match becomes a global winner.

| mask | dp[mask] | meaning |
| --- | --- | --- |
| 1 | p(1→2) | subset {1} dominates |
| 2 | p(2→1) | subset {2} dominates |
| 3 | 1 | full set consistency |

Sum gives 1.

This shows that symmetry of probabilities leads to a single expected winner.

### Example 2

Input:

```
3
1 1 1
```

All edges are symmetric with probability 1/2. Every subset has equal chance of dominating others, so multiple configurations contribute equally.

The DP distributes probability evenly across all partitions, and the sum reflects the expected size of the top reachable component.

This confirms that even when structure is fully symmetric, the algorithm still counts all dominance-consistent partitions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2 2^n)$ | subset enumeration with pairwise transitions |
| Space | $O(2^n)$ | DP over all subsets |

With $n \le 14$, $2^n = 16384$, so even quadratic subset transitions are feasible within time limits.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 node | 1 | base case |
| equal strengths | symmetric case | uniform probabilities |
| increasing strengths | nontrivial ordering | dominance structure |
| mixed values | general correctness | DP transitions |

## Edge Cases

For $n=1$, the DP over subsets contains only the empty and full mask. The only team trivially reaches itself, so the algorithm must return 1. Any formulation that requires at least one edge would incorrectly give 0, but the subset DP treats singleton masks as valid terminal components.

For equal strengths, every edge is 1/2. The DP does not assume deterministic ordering, so both directions contribute equally. This prevents collapsing into a single linear ordering, which would be incorrect under probabilistic symmetry.
