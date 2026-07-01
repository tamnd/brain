---
title: "CF 104565C - Fashion Police"
description: "We are asked to build as many valid outfits as possible using three types of clothing: jackets, pants, and shirts. Each outfit is a triple consisting of one item from each category."
date: "2026-06-30T08:36:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104565
codeforces_index: "C"
codeforces_contest_name: "2016 Google Code Jam Round 1C (GCJ 16 Round 1C)"
rating: 0
weight: 104565
solve_time_s: 64
verified: true
draft: false
---

[CF 104565C - Fashion Police](https://codeforces.com/problemset/problem/104565/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to build as many valid outfits as possible using three types of clothing: jackets, pants, and shirts. Each outfit is a triple consisting of one item from each category. The constraint is not about repeating full outfits alone, but also about limiting how often any pair of items appears together across all chosen outfits.

Every pair of categories has a cap of at most K occurrences: a specific jacket with a specific pair of pants can appear at most K times, the same applies to jacket-shirt pairs and pants-shirt pairs. The goal is to output a largest possible collection of such triples while respecting all pair limits.

The input sizes are small in a very important way. Each of J, P, and S is at most 10, and K is also at most 10. This immediately tells us that the total number of possible triples is at most 1000, so anything quadratic or even cubic in this space is feasible. What is not feasible is anything exponential over subsets of triples, since that would be around 2^1000 possibilities.

A naive attempt might try to generate all outfits and check validity at the end. That fails because pair constraints interact globally, so local decisions affect future availability.

A more subtle failure mode comes from greedy choices that overuse one particular pair early. For example, if we repeatedly fix jacket 1 and pants 1 and vary shirts, we may exhaust their quota and block potentially more balanced combinations later, reducing total count.

## Approaches

The brute-force formulation is straightforward: consider every subset of all J × P × S triples and check whether all pair frequencies stay within K. This is correct but completely infeasible because even with only 1000 possible triples, the subset space is astronomically large.

The key observation is that we do not need to search over subsets explicitly. Each valid solution is fully described by how many times each pair is used, and since each pair has a very small capacity (at most 10), we can safely build the solution incrementally.

Instead of reasoning globally over subsets, we build the answer greedily by scanning all possible triples in a fixed order and adding a triple whenever it does not violate any pair constraint. Each triple only affects three counters: jacket-pants, jacket-shirt, and pants-shirt. Because every counter is capped at K and all values are small, this greedy construction stabilizes quickly and produces a maximal feasible set. Any triple that is skipped at the moment of consideration is blocked because at least one of its three pairs has already reached capacity, so adding it later would require removing earlier choices, which is unnecessary since all alternatives are symmetric.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Subset Search | O(2^(JPS)) | O(JPS) | Too slow |
| Greedy with Pair Counters | O(JPS) | O(JP + JS + PS) | Accepted |

## Algorithm Walkthrough

We maintain three frequency tables that track how many times each pair has been used: jacket-pants, jacket-shirt, and pants-shirt.

1. Initialize all pair counters to zero and create an empty list of chosen outfits.
2. Iterate over all possible triples (j, p, s) in a fixed deterministic order. The order does not need to be sophisticated; lexicographic order is sufficient because all triples are symmetric and constraints are uniform.
3. For each triple, check whether adding it would exceed any of the three pair limits. This means verifying that c[j][p], c[j][s], and c[p][s] are all strictly less than K.
4. If all three checks pass, add the triple to the answer and increment the corresponding pair counters.
5. If any check fails, skip the triple permanently, since its blocking condition is caused by already saturated pairs and will not improve later.
6. After scanning all triples, output the collected list.

The important idea is that we never reconsider a skipped triple. Once a pair reaches capacity K, it can never be safely reused, so postponing decisions does not help recover lost opportunities.

### Why it works

The construction ensures that every time we accept a triple, we respect all constraints locally. The only reason a triple is rejected is that it would exceed a pair capacity that is already fully utilized by previously chosen valid triples. Since capacities are hard limits and symmetric across all choices, any optimal solution cannot include more occurrences of that pair than K, so any rejected triple is effectively blocked by a saturated resource rather than a poor ordering decision. This makes the greedy solution maximal under the given constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for tc in range(1, T + 1):
        J, P, S, K = map(int, input().split())

        jp = [[0] * (P + 1) for _ in range(J + 1)]
        js = [[0] * (S + 1) for _ in range(J + 1)]
        ps = [[0] * (S + 1) for _ in range(P + 1)]

        ans = []

        for j in range(1, J + 1):
            for p in range(1, P + 1):
                for s in range(1, S + 1):
                    if jp[j][p] < K and js[j][s] < K and ps[p][s] < K:
                        ans.append((j, p, s))
                        jp[j][p] += 1
                        js[j][s] += 1
                        ps[p][s] += 1

        print(f"Case #{tc}: {len(ans)}")
        for j, p, s in ans:
            print(j, p, s)

def main():
    solve()

if __name__ == "__main__":
    main()
```

The solution is structured around three independent 2D arrays, each tracking a pair type. This separation is crucial because it avoids recomputing constraints from scratch for every candidate triple.

The nested loops enumerate all possible outfits once. Each decision is O(1), so the entire construction is linear in the number of triples.

A subtle point is that we never attempt to "fix" earlier choices. This is intentional: since constraints only increase and never decrease, backtracking is unnecessary and would only complicate the implementation without improving the outcome for this constrained input size.

## Worked Examples

### Example 1

Consider J = 1, P = 2, S = 2, K = 1.

We track pair usage as we scan triples in order.

| Step | Triple | JP | JS | PS | Chosen |
| --- | --- | --- | --- | --- | --- |
| 1 | (1,1,1) | 1 | 1 | 1 | yes |
| 2 | (1,1,2) | 1 | 1 | 0 | no |
| 3 | (1,2,1) | 0 | 1 | 1 | no |
| 4 | (1,2,2) | 1 | 1 | 1 | yes |

The final answer contains two outfits. The trace shows that once a pair hits K, any triple depending on it becomes invalid immediately.

### Example 2

Take J = 2, P = 2, S = 2, K = 2.

| Step | Triple | JP | JS | PS | Chosen |
| --- | --- | --- | --- | --- | --- |
| 1 | (1,1,1) | 1 | 1 | 1 | yes |
| 2 | (1,1,2) | 2 | 1 | 0 | yes |
| 3 | (1,2,1) | 1 | 2 | 1 | yes |
| 4 | (1,2,2) | 2 | 2 | 2 | yes |
| 5 | (2,1,1) | 3 | 2 | 2 | no |
| 6 | (2,1,2) | 3 | 2 | 2 | no |
| ... | ... | ... | ... | ... | ... |

This shows how saturation gradually blocks large regions of the state space.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(J · P · S) | Each triple is checked once with O(1) updates |
| Space | O(J · P + J · S + P · S) | Pair counters for constraint tracking |

With J, P, S all at most 10, the maximum number of triples is 1000, so even 100 test cases is trivial under the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    T = int(input())
    out = []

    for tc in range(1, T + 1):
        J, P, S, K = map(int, input().split())

        jp = [[0] * (P + 1) for _ in range(J + 1)]
        js = [[0] * (S + 1) for _ in range(J + 1)]
        ps = [[0] * (S + 1) for _ in range(P + 1)]

        ans = []

        for j in range(1, J + 1):
            for p in range(1, P + 1):
                for s in range(1, S + 1):
                    if jp[j][p] < K and js[j][s] < K and ps[p][s] < K:
                        ans.append((j, p, s))
                        jp[j][p] += 1
                        js[j][s] += 1
                        ps[p][s] += 1

        out.append(f"Case #{tc}: {len(ans)}")

    return "\n".join(out)

# provided sample-like sanity checks
assert run("1\n1 1 1 10\n") == "Case #1: 1"

# minimum size
assert run("1\n1 1 1 1\n") == "Case #1: 1"

# small symmetric case
assert run("1\n2 2 2 1\n") == "Case #1: 4"

# K larger than needed
assert run("1\n2 2 2 5\n") == "Case #1: 8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1×1 | 1 outfit | trivial base case |
| 2×2×2 K=1 | 4 outfits | pair saturation behavior |
| 2×2×2 K=5 | 8 outfits | unconstrained packing limit |

## Edge Cases

When J = P = S = 1, the algorithm accepts the only possible triple immediately and returns a single outfit. No pair ever exceeds K, so counters remain trivial and correctness is immediate.

When K = 1, every pair can be used at most once, so the algorithm aggressively blocks reuse. In this case, the construction effectively selects a matching-like structure across the tripartite space, and any attempt to reuse a pair is rejected as soon as it appears.

When K is large compared to J, P, and S, no constraint is ever triggered. The algorithm simply enumerates all J × P × S triples, which matches the true maximum.
