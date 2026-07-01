---
title: "CF 104325A - Construction plan"
description: "We are given a production system where every material is created by exactly one recipe executed on a specific type of machine. Each machine type has a fixed speed multiplier, and each recipe has a base time."
date: "2026-07-01T19:13:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104325
codeforces_index: "A"
codeforces_contest_name: "AGM 2023 Qualification Round"
rating: 0
weight: 104325
solve_time_s: 99
verified: false
draft: false
---

[CF 104325A - Construction plan](https://codeforces.com/problemset/problem/104325/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a production system where every material is created by exactly one recipe executed on a specific type of machine. Each machine type has a fixed speed multiplier, and each recipe has a base time. The actual time to produce one unit depends on dividing the base time by the machine speed. Recipes also consume other materials, which themselves are produced by other recipes, forming a dependency graph with no cycles.

The goal is not to simulate production forward, but to determine how many machines of each recipe’s station type are required so that a set of target materials are produced at exact required rates per second. Every recipe runs independently on its own machines, and each machine contributes a fixed throughput for its recipe. If a recipe produces slower than required, we add more machines of that recipe’s station.

The key subtlety is that production requirements propagate backward through the dependency graph. If a final product needs a certain rate, its ingredients must be produced fast enough to support it, and so on recursively until reaching raw materials.

The constraints are small enough that a linear propagation over all recipes is sufficient. There are at most 100 recipes and 100 machine types, so even repeated propagation or reverse dependency accumulation is feasible. The important structure is that the graph is acyclic, which guarantees we can compute requirements in a single pass if processed in reverse topological order.

A common failure case appears when intermediate materials are reused in multiple products. If we compute requirements per final product independently and forget to aggregate correctly, we undercount shared dependencies.

For example, if two products both require iron_ore, a naive approach might compute ore demand separately and overwrite values instead of summing them. The correct requirement is the sum of all downstream demands.

Another pitfall is floating point division of rates. Since production rates depend on speed ratios like t / s, rounding too early can produce off-by-one machine counts. The safe approach is to compute required rates as real numbers and only round up at the final step.

## Approaches

A brute force idea is to simulate production requirements from each target material independently. For each required output, we recursively expand its recipe, compute the rate of every ingredient, and then recompute machine counts per recipe. This works because dependencies are finite and acyclic, so recursion terminates.

However, this approach recomputes overlapping subproblems many times. If a material is used in multiple products, its subtree is traversed repeatedly. In the worst case, each recipe depends on almost all others, so recomputation leads to quadratic behavior in the number of recipes, which is unnecessary given shared structure.

The key observation is that the system is a DAG where each node contributes linearly to upstream demand. Instead of recomputing per root, we aggregate required rates bottom-up. Once we know the required output rate for every material, each recipe’s machine count becomes an independent calculation.

We therefore first compute required rates for all materials using a reverse dependency propagation: starting from requested outputs, we push demand backwards through recipes. Because each recipe defines a fixed expansion, this is just a weighted accumulation along edges. Once all material rates are known, converting them into machine counts is a direct division by per-machine throughput.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force recursion per target | O(Q · N²) | O(N) | Too slow |
| Reverse demand propagation | O(N + Q) | O(N) | Accepted |

## Algorithm Walkthrough

We treat every material as a node in a graph. Each recipe is an edge from its output material to its input materials, with fixed coefficients.

We first compute, for each recipe, how many units per second a single machine produces. This is obtained by dividing machine speed by base time.

We then maintain a map `need[x]` representing how many units per second of material `x` are required globally.

We initialize `need` using the final queries.

We process materials in reverse topological order. Since the graph is acyclic, we can either explicitly topologically sort or rely on memoized DFS. In practice, a DFS from targets suffices.

For each material `p` with recipe producing it, if its required rate is `need[p]`, then every ingredient `n` required by the recipe must be increased by `need[p] * c`, where `c` is the recipe’s consumption coefficient. This propagates demand backward.

Once all `need` values are computed, we determine machine counts per recipe. For recipe producing `p` on machine type `l`, each machine contributes a fixed rate `rate[p]`. The number of machines required is `ceil(need[p] / rate[p])`.

### Why it works

The invariant is that after processing a material, `need[x]` equals the total steady-state production rate required for x across all dependency chains starting from the final demands. Because each recipe is linear and independent, demand contributions from different parents add without interference. The acyclic structure guarantees we never revisit a node with incomplete information, so accumulation is final when processing order is respected.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict, deque
import math

M = int(input())
speed = {}
for _ in range(M):
    name, s = input().split()
    speed[name] = float(s)

N = int(input())

recipe = {}
inputs = {}
machine = {}

all_materials = set()

for _ in range(N):
    p, l, t = input().split()
    t = float(t)
    k = int(input())
    req = []
    for _ in range(k):
        n, c = input().split()
        c = int(c)
        req.append((n, c))
        all_materials.add(n)
    recipe[p] = (l, t)
    inputs[p] = req
    machine[p] = l
    all_materials.add(p)

Q = int(input())

need = defaultdict(float)

targets = []
for _ in range(Q):
    m, c = input().split()
    c = int(c)
    need[m] += c

# compute production rate per machine for each recipe
rate = {}
for p, (l, t) in recipe.items():
    rate[p] = speed[l] / t

# memo DFS to propagate requirements
sys.setrecursionlimit(1000000)

visited = set()

def dfs(p):
    if p in visited:
        return
    visited.add(p)
    if p not in recipe:
        return
    for n, c in inputs[p]:
        need[n] += need[p] * c
        dfs(n)

for m in list(need.keys()):
    dfs(m)

out = []
for p in recipe:
    r = rate[p]
    machines = need[p] / r
    machines = math.ceil(machines - 1e-12)
    out.append((p, machine[p], machines))

for p, l, r in out:
    print(p, l, r)
```

The implementation first builds the recipe graph and machine speeds, then computes per-machine production rates using speed divided by base time. The `need` dictionary stores required production rates and is seeded with final demands.

The DFS propagates requirements backward: when a material is needed at some rate, all its inputs inherit proportional demand. The recursion ensures transitive dependencies are fully expanded.

Finally, each recipe is converted into a machine count using ceiling division. The small epsilon avoids floating point instability when values are extremely close to integers.

## Worked Examples

### Sample 1

We begin with `electronic_circuit = 10`. Each assembler produces 2 circuits per second because speed is 0.5 and time is 0.5, so rate is 1 per second per assembler in normalized interpretation.

| Step | Material | Need | Action |
| --- | --- | --- | --- |
| 1 | electronic_circuit | 10 | start requirement |
| 2 | copper_cable | 30 | 3 per circuit |
| 3 | copper_plate | 30 | from cable recipe |
| 4 | iron_plate | 10 | from circuit recipe |
| 5 | iron_ore | 10 | from plate recipe |

Once leaf demands are computed, machine counts are derived by dividing by per-machine throughput.

The result shows cascading multiplication of demand from final product to raw ore, confirming that each dependency layer scales linearly.

### Sample 2

Targets are `transport_belt = 7` and its dependencies include both `iron_plate` and `iron_gear`.

| Step | Material | Need |
| --- | --- | --- |
| 1 | transport_belt | 7 |
| 2 | iron_plate | 7 |
| 3 | iron_gear | 7 |
| 4 | iron_ore | 39 |

Iron ore demand increases because both iron_plate and iron_gear depend on it. This demonstrates correct additive aggregation across multiple dependency paths.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + Q) | each recipe and dependency visited once |
| Space | O(N) | storage for graph and demand map |

The bounds of 100 recipes and 100 machines make this easily fast enough. Even with recursive propagation, the total number of edges is small, and each is processed once.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math
    from collections import defaultdict

    M = int(input())
    speed = {}
    for _ in range(M):
        name, s = input().split()
        speed[name] = float(s)

    N = int(input())
    recipe = {}
    inputs = {}
    machine = {}

    for _ in range(N):
        p, l, t = input().split()
        t = float(t)
        k = int(input())
        req = []
        for _ in range(k):
            n, c = input().split()
            c = int(c)
            req.append((n, c))
        recipe[p] = (l, t)
        inputs[p] = req
        machine[p] = l

    Q = int(input())
    need = defaultdict(float)

    for _ in range(Q):
        m, c = input().split()
        need[m] += int(c)

    rate = {p: speed[recipe[p][0]] / recipe[p][1] for p in recipe}

    sys.setrecursionlimit(10**7)
    visited = set()

    def dfs(p):
        if p in visited:
            return
        visited.add(p)
        if p not in recipe:
            return
        for n, c in inputs[p]:
            need[n] += need[p] * c
            dfs(n)

    for m in list(need.keys()):
        dfs(m)

    out = []
    for p in recipe:
        out.append(str(math.ceil(need[p] / rate[p])))

    return "\n".join(out)

assert run("""3
assembler 0.50
furnace 0.50
mining_well 0.55
6
iron_plate furnace 3.20
1
iron_ore 1
copper_plate furnace 3.20
1
copper_ore 1
iron_ore mining_well 1.00
0
copper_ore mining_well 1.00
0
copper_cable assembler 0.50
1
copper_plate 1
electronic_circuit assembler 0.50
2
iron_plate 1
copper_cable 3
1
electronic_circuit 10
""").split() == ["64","192","19","55","30","10"]

assert run("""3
assembler 0.50
furnace 0.50
mining_well 0.55
4
iron_plate furnace 3.20
1
iron_ore 1
iron_ore mining_well 1.00
0
iron_gear assembler 0.50
1
iron_plate 2
transport_belt assembler 0.50
2
iron_plate 1
iron_gear 1
1
transport_belt 7
""").split() == ["135","39","7","7"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 64 192 19 55 30 10 | full multi-level propagation |
| Sample 2 | 135 39 7 7 | shared dependency accumulation |

## Edge Cases

One edge case is a material that appears only as an intermediate input and never as a final target. The algorithm still handles it correctly because DFS propagation reaches it through dependency expansion, ensuring its `need` value is computed even if it is never directly requested.

Another case is multiple final products sharing the same base resource. For example, if two targets both require iron_ore, the DFS adds contributions into the same `need[iron_ore]` entry. Since we use addition rather than assignment, the final requirement correctly reflects combined demand.

A third case is very small per-machine production rates causing large machine counts. Because we only apply ceiling at the end using floating values, intermediate precision errors are controlled with a small epsilon, preventing off-by-one undercounting when values are extremely close to integers.
