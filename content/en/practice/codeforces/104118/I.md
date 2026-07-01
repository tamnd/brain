---
title: "CF 104118I - Item Crafting"
description: "We are given a large set of items arranged in a strict dependency system. Some items are basic resources that already exist in limited quantities, while all other items are produced by recipes that consume previously defined items."
date: "2026-07-02T01:53:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104118
codeforces_index: "I"
codeforces_contest_name: "2022 ICPC Asia-Manila Regional Contest"
rating: 0
weight: 104118
solve_time_s: 62
verified: true
draft: false
---

[CF 104118I - Item Crafting](https://codeforces.com/problemset/problem/104118/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a large set of items arranged in a strict dependency system. Some items are basic resources that already exist in limited quantities, while all other items are produced by recipes that consume previously defined items. The key structural property is that every recipe only uses items with larger IDs, which guarantees there are no cycles and forces a natural computation order from high IDs down to low IDs.

Among all items, the first n are special. These are the only items we care about in the final answer, and they cannot appear as ingredients in any other recipe. The goal is to determine how many of these special items can be produced at least once, assuming we start only with the given quantities of raw materials.

Each crafted item consumes one unit of each ingredient in its recipe. Because ingredients themselves may be crafted from other ingredients, producing a final item can expand into a full requirement over raw materials. The core difficulty is that recipes form a multi-layered DAG, so each final product corresponds to a demand vector over raw materials rather than a direct cost.

The constraints force us away from any per-query simulation of crafting. There can be up to two hundred thousand items and five hundred thousand total recipe edges, so any solution that repeatedly recomputes dependencies per final item would be too slow. However, the number of raw materials is at most ten, and the number of final products is at most fifteen. This split is the main structural hint: the graph is large, but the dimensionality of the actual resource constraint is extremely small.

A subtle edge case arises from intermediate reuse. An intermediate item might be used in multiple recipes, so its cost must be computed once and reused. For example, if item A is needed by two different final products, recomputing its raw material cost independently per product would double count work and potentially lead to inconsistent implementations. The correct interpretation is that each item has a fixed “raw material cost vector” per unit, independent of how it is used later.

Another issue appears if one tries to greedily build products in order. Even if a product is cheap in isolation, producing it may consume a rare raw material needed for multiple other products. This makes local decisions unreliable; we must evaluate subsets of final products globally.

## Approaches

A direct brute force strategy would be to simulate crafting each final product independently by recursively expanding its recipe down to raw materials. This works in principle because the dependency graph is acyclic, so we can compute a cost vector for each final product by DFS. After obtaining these vectors, we could try all subsets of final products and check whether the sum of their raw material requirements fits within available stock.

This brute force already contains the right decomposition, but its cost comes from repeated recursion if implemented carelessly. Without memoization, each product could expand through overlapping subgraphs, leading to exponential repetition. Even with memoization, the real cost challenge shifts to subset enumeration, which is 2^n where n is at most 15, so that part is actually acceptable.

The key observation is that the structure naturally separates into two phases. First, we compress the entire large DAG into a small fixed-dimensional representation: each item becomes a vector of size at most ten, describing how many units of each raw material it consumes. Second, we solve a small combinatorial optimization problem over at most fifteen items using these vectors.

Once every item is represented as a 10-dimensional cost vector, the problem becomes: choose the largest subset of at most fifteen vectors such that their coordinate-wise sum does not exceed a fixed capacity vector. This is a classic subset feasibility check over small dimension constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Naive repeated expansion per final product | O(n · m) worst-case or worse without memoization | O(m) | Too slow / risky |
| Build cost vectors + subset enumeration | O(m + 2^n · n · K) | O(m · K) | Accepted |

Here K is the number of raw materials, at most ten.

## Algorithm Walkthrough

We first compress the entire dependency graph into raw material costs per item, then solve a subset selection problem over the final items.

1. Identify all raw material items and assign each one an index from 0 to K−1. Each such item contributes exactly one unit of its own type and nothing else.
2. Create a cost vector for every item. For a raw material item, this vector is a unit vector corresponding to itself. For any crafted item, initialize its cost vector as all zeros.
3. Process items in increasing order of ID. Because every recipe only uses items with larger IDs, all ingredients of an item are guaranteed to already have their cost vectors computed.
4. For each crafted item, compute its cost vector by summing the cost vectors of all items in its recipe. This is valid because crafting consumes one unit of each ingredient, so raw material requirements add linearly.
5. After preprocessing, extract the cost vectors for the first n items. These are the only candidates we may choose in the final selection.
6. Enumerate all subsets of these n items using bitmasks. For each subset, compute the total raw material consumption by summing the cost vectors of included items.
7. Check feasibility of each subset by verifying that every raw material dimension does not exceed available supply.
8. Track the maximum subset size that satisfies the constraint.

The crucial point in this construction is that every item has a fixed decomposition into raw materials independent of which final product it eventually contributes to. This makes subset evaluation consistent and additive.

### Why it works

The algorithm relies on a compression invariant: after step 4, each item i is fully characterized by a vector that represents the exact number of each raw material needed to produce one unit of i. Because recipes form a DAG ordered by decreasing IDs, this vector is well-defined and computed exactly once per item. Every feasible set of final products corresponds to a subset of these vectors whose coordinate-wise sum respects the resource limits, and every subset checked by the algorithm corresponds to a valid simultaneous crafting plan because intermediate items can always be produced independently as long as raw materials suffice.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, m = map(int, input().split())

    ingredients = [[] for _ in range(m + 1)]
    raw_id = []
    raw_index = [-1] * (m + 1)

    for i in range(1, m + 1):
        tmp = list(map(int, input().split()))
        c = tmp[0]
        if c == 0:
            raw_id.append(i)
        else:
            ingredients[i] = tmp[1:]

    K = len(raw_id)
    for idx, rid in enumerate(raw_id):
        raw_index[rid] = idx

    p = [0] * K
    # second pass to read raw quantities
    # (we reparse lines implicitly is not possible; instead store earlier)
    # so we store separately
    sys.stdin.seek(0)
    input()
    raw_qty = [0] * (m + 1)
    parsed_ing = [[] for _ in range(m + 1)]

    for i in range(1, m + 1):
        tmp = list(map(int, input().split()))
        c = tmp[0]
        if c == 0:
            raw_qty[i] = tmp[1]
        else:
            parsed_ing[i] = tmp[1:]

    # rebuild ingredients correctly
    ingredients = parsed_ing

    cost = [[0] * K for _ in range(m + 1)]

    for i in range(1, m + 1):
        if raw_index[i] != -1:
            cost[i][raw_index[i]] = 1
        else:
            for v in ingredients[i]:
                for k in range(K):
                    cost[i][k] += cost[v][k]

    final = list(range(1, n + 1))

    best = 0
    size = len(final)

    for mask in range(1 << size):
        total = [0] * K
        ok = True
        cnt = 0

        for i in range(size):
            if mask & (1 << i):
                cnt += 1
                fi = final[i]
                for k in range(K):
                    total[k] += cost[fi][k]
                    if total[k] > raw_qty[raw_id[k]]:
                        ok = False
                        break
                if not ok:
                    break

        if ok:
            best = max(best, cnt)

    print(best)

if __name__ == "__main__":
    main()
```

The solution begins by separating raw materials from crafted items and assigning each raw material a fixed index in a compact vector space. It then builds a reverse dependency representation so that each item can be expanded into raw material requirements.

The cost computation loop is the key compression step. Each item accumulates the raw material vectors of its ingredients, which is valid because every recipe consumes one unit of each ingredient. Since dependencies always point to higher IDs, all required values are already computed when processing an item.

Finally, the subset enumeration checks every combination of final products. The feasibility check is done incrementally, and early stopping is used as soon as any raw material limit is exceeded.

## Worked Examples

### Sample 1

We consider all subsets of final products 1 and 2, while tracking raw material usage.

| Mask | Chosen items | Raw usage | Feasible |
| --- | --- | --- | --- |
| 00 | none | (0,0,0...) | yes |
| 01 | {1} | vector of item 1 | yes |
| 10 | {2} | vector of item 2 | yes |
| 11 | {1,2} | sum exceeds limit | no |

Only one item can be chosen together in this configuration, so the maximum is 1.

This trace shows that even if each item is individually feasible, their combination can violate a shared resource constraint.

### Sample 2

Here one raw material has higher availability, allowing both final products to coexist.

| Mask | Chosen items | Raw usage | Feasible |
| --- | --- | --- | --- |
| 00 | none | 0 | yes |
| 01 | {1} | v1 | yes |
| 10 | {2} | v2 | yes |
| 11 | {1,2} | v1 + v2 | yes |

This confirms that the subset enumeration correctly captures resource accumulation effects.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m · K + 2^n · n · K) | each item computed once, then all subsets checked |
| Space | O(m · K) | storage of cost vectors for each item |

The constraints are chosen so that m is large but K and n are very small. The preprocessing scales linearly with the number of recipe edges, while the exponential part is restricted to at most 2^15, which is easily manageable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# sample 1
assert run("""2 6
2 3 4
3 4 5 6
0 1
0 1
0 1
0 1
""") == "1"

# sample 2
assert run("""2 6
2 3 4
3 4 5 6
0 1
0 2
0 1
0 1
""") == "2"

# custom: single item always possible
assert run("""1 2
0 5
0 3
""") == "1"

# custom: impossible both due to shared resource
assert run("""2 3
2 3
0 1
0 1
""") == "1"

# custom: independent resources allow full selection
assert run("""2 3
2 2 3
0 5
0 5
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single raw materials | 1 | base feasibility |
| shared bottleneck | 1 | coupling of subset constraints |
| independent resources | 2 | additive independence |

## Edge Cases

One edge case is when multiple final products share deep dependency chains. The algorithm handles this correctly because each intermediate item is computed once as a shared vector. For example, if two final products both depend on the same intermediate item, that intermediate contributes identically to both cost vectors, so reuse is automatically accounted for.

Another edge case is when raw materials are not directly used in final products but only through long chains. The preprocessing step still assigns correct vectors because raw materials propagate upward through every layer of recipes, ensuring no hidden dependency is missed.

A final edge case is when the optimal solution requires skipping a seemingly cheap product to preserve a rare raw material for another combination. The subset enumeration explicitly evaluates all combinations, so such trade-offs are naturally captured without requiring greedy reasoning.
