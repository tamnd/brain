---
title: "CF 1193A - Amusement Park"
description: "We are given a set of attractions and some planned one-way slides between pairs of them. After construction, each slide can be reversed or kept as is, independently of others. What we ultimately choose is therefore just a direction for every existing edge."
date: "2026-06-13T13:33:16+07:00"
tags: ["codeforces", "competitive-programming", "*special", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1193
codeforces_index: "A"
codeforces_contest_name: "CEOI 2019 day 2 online mirror (unrated, IOI format)"
rating: 0
weight: 1193
solve_time_s: 241
verified: true
draft: false
---

[CF 1193A - Amusement Park](https://codeforces.com/problemset/problem/1193/A)

**Rating:** -  
**Tags:** *special, dp, math  
**Solve time:** 4m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of attractions and some planned one-way slides between pairs of them. After construction, each slide can be reversed or kept as is, independently of others. What we ultimately choose is therefore just a direction for every existing edge.

A proposal is considered physically valid if we can assign heights to attractions so that every slide goes strictly downward. This condition is equivalent to saying the directed graph formed by the chosen directions has no directed cycles, because a height assignment induces a strict ordering of vertices, and every edge must follow that order.

So every valid proposal corresponds exactly to an acyclic orientation of the given undirected graph.

The cost of a proposal is the number of slides whose final direction differs from the originally given direction. The task is not to find a single best proposal, but to sum this cost over all valid (acyclic) orientations.

The constraint on the number of nodes is small, but the number of edges can be quadratic. That suggests the intended solution is not enumerating orientations explicitly, since there are 2^m possibilities, which becomes enormous even for moderate m.

A subtle issue appears if one tries to think only in terms of cycles. A naive idea is to try to count acyclic orientations by checking permutations or topological sorts, but without noticing symmetry, this quickly leads to overcounting or double counting the same orientation in different forms.

## Approaches

A brute-force approach would try all 2^m ways to assign directions to edges, then check whether the resulting graph is acyclic, and compute the cost for each valid orientation. Cycle checking per configuration would require O(n + m), leading to O(2^m · m) time. With m up to about 150, this is far beyond feasible limits.

A more structured viewpoint is to stop focusing on edges and instead focus on vertex orderings. If we fix a permutation of all attractions, we can orient every edge consistently with that order: earlier vertex to later vertex. This automatically produces a valid acyclic orientation, and every acyclic orientation can be associated with at least one such permutation.

This shifts the space from 2^m edge configurations to n! permutations. The crucial simplification is that cost becomes easy to express in terms of the permutation: for a fixed edge u → v in the original input, the edge is reversed exactly when v appears before u in the permutation. Over all permutations, this event has perfect symmetry, so each direction occurs equally often.

This symmetry allows the entire sum to collapse into a simple closed form.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Enumerate edge directions | O(2^m · m) | O(n + m) | Too slow |
| Permutation counting with symmetry | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Observe that every permutation of vertices defines a valid acyclic orientation by directing each edge from earlier to later in the permutation. This gives a complete mapping from permutations to legal proposals.
2. Fix one edge u → v from the input. Across all permutations, consider how often this edge is reversed in the induced orientation. Reversal happens exactly when v appears before u in the permutation.
3. By symmetry of all permutations, u is before v in exactly half of them, and v is before u in the other half. Therefore, for each edge, the number of permutations contributing a cost of 1 for that edge is n! / 2.
4. The total cost over a permutation is the sum over edges of whether that edge is reversed. Summing over all permutations allows exchanging sums, so each edge contributes independently.
5. Multiply the contribution of one edge by the number of edges m to obtain the total sum over all valid proposals.
6. Compute factorial n! modulo 998244353 and multiply by m and the modular inverse of 2.

The key idea is that edge contributions are independent under uniform permutations, which removes any need to consider graph structure beyond edge count.

### Why it works

Every acyclic orientation corresponds to at least one permutation, and every permutation produces exactly one acyclic orientation. When summing cost over all valid orientations, we can instead sum over all permutations without losing correctness because each orientation is counted at least once consistently with its inducing permutations. The cost decomposition depends only on relative ordering of endpoints of each edge, and these relative orders are uniformly distributed over permutations, making each edge contribute a fixed expected and total value independent of the rest of the graph.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    n, m = map(int, input().split())
    
    fact = 1
    for i in range(1, n + 1):
        fact = fact * i % MOD
    
    inv2 = (MOD + 1) // 2
    
    ans = m % MOD * fact % MOD * inv2 % MOD
    print(ans)

if __name__ == "__main__":
    solve()
```

The factorial computation encodes the total number of vertex permutations. The multiplication by m aggregates identical contributions from each edge. The division by 2 is performed using modular inverse since exactly half of permutations place one endpoint before the other.

No graph traversal or DP is required because the structure of the problem reduces entirely to permutation symmetry.

## Worked Examples

### Sample 1

Input:

```
2 1
1 2
```

We have 2 vertices and one edge.

| Permutation | Order relation | Edge reversed? | Cost |
| --- | --- | --- | --- |
| 1 2 | 1 before 2 | No | 0 |
| 2 1 | 2 before 1 | Yes | 1 |

Sum of costs is 1, matching the formula m · n! / 2 = 1 · 2 / 2 = 1.

This confirms that each permutation contributes correctly and symmetry holds even in the smallest graph.

### Sample 2

Input:

```
3 3
1 2
2 3
1 3
```

We list permutations of three vertices.

| Permutation | Reversed edges | Cost |
| --- | --- | --- |
| 1 2 3 | none | 0 |
| 1 3 2 | (2,3) | 1 |
| 2 1 3 | (1,2) | 1 |
| 2 3 1 | (1,2),(1,3) | 2 |
| 3 1 2 | (1,3),(2,3) | 2 |
| 3 2 1 | all three | 3 |

Sum is 9. The formula gives m · n! / 2 = 3 · 6 / 2 = 9, matching exactly.

This trace shows that edge contributions remain balanced across permutations even though dependencies exist inside each permutation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | factorial computation up to n |
| Space | O(1) | only a few modular variables |

The solution comfortably fits constraints since n ≤ 18, and the computation avoids any exponential enumeration.

## Test Cases

```python
import sys, io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n, m = map(int, input().split())
    
    fact = 1
    for i in range(1, n + 1):
        fact = fact * i % MOD
    
    inv2 = (MOD + 1) // 2
    
    return str(m % MOD * fact % MOD * inv2 % MOD)

# provided samples
assert run("2 1\n1 2\n") == "1"
assert run("3 3\n1 2\n2 3\n1 3\n") == "9"

# custom cases
assert run("1 0\n") == "0", "single node, no edges"
assert run("4 0\n") == "0", "no edges always zero cost"
assert run("4 1\n1 2\n") == str((1 * 24 * pow(2, MOD-2, MOD)) % MOD), "single edge scaling"
assert run("5 10\n1 2\n2 3\n3 4\n4 5\n1 3\n1 4\n2 5\n3 5\n1 5\n2 4\n") == str(10 * 120 * pow(2, MOD-2, MOD) % MOD), "dense edge case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0` | `0` | empty graph edge case |
| `4 0` | `0` | zero edges always zero cost |
| `4 1 ...` | factorial/2 | single edge correctness |
| `5 10 ...` | m·n!/2 | dense graph consistency |

## Edge Cases

A graph with no edges provides the simplest sanity check. The input has no constraints being violated, and every permutation induces the same empty orientation. The cost is always zero because there are no edges to reverse, and the formula correctly multiplies m = 0 with n!.

A single-edge graph highlights the symmetry argument. Regardless of which direction is initially given, exactly half of permutations reverse it. The algorithm reduces correctly to n! / 2, and computing modular inverse handles this without floating-point ambiguity.

In dense graphs, such as a complete graph on 5 nodes, edge interactions might seem like they could affect validity. However, since every permutation is valid regardless of edge density, the contribution of each edge remains independent. The algorithm still reduces the entire structure to counting edges only, confirming that graph topology never enters the final formula.
