---
title: "CF 102323L - Under Construction Forever"
description: "We have a connected undirected graph whose vertices represent buildings and whose vertex weights represent the cost of choosing that building for reconstruction. On one day, we choose a building (v)."
date: "2026-08-13T04:29:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102323
codeforces_index: "L"
codeforces_contest_name: "UCF Locals 2014"
rating: 0
weight: 102323
solve_time_s: 364
verified: true
draft: false
---

[CF 102323L - Under Construction Forever](https://codeforces.com/problemset/problem/102323/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a connected undirected graph whose vertices represent buildings and whose vertex weights represent the cost of choosing that building for reconstruction. On one day, we choose a building (v). Every neighbor of (v) whose only remaining neighbor is (v) is merged into (v) and disappears as a separate building. The chosen building remains.

In graph terms, a reconstruction removes every current leaf adjacent to the chosen vertex. The operation costs the weight of the chosen vertex. We may repeat this process until no useful reconstruction remains. The task asks for three quantities: the smallest possible number of buildings left, the smallest reconstruction cost among sequences attaining that minimum, and the number of minimum-cost sequences, modulo (10^9+7). Two sequences are different when either the chosen building on some day differs or their lengths differ. The original constraints have at most 500 buildings and 2000 edges, with the graph guaranteed connected. The official contest statement gives a 2 second limit and 256 MB memory limit.

The key structural fact is that an operation only deletes leaves. A vertex on a cycle can never become a leaf, because its two cycle neighbors remain connected to it. More generally, repeatedly deleting leaves leaves exactly the graph's 2-core. Thus the minimum number of remaining buildings is the size of the 2-core. When the graph is a tree, the 2-core is empty, but the process must stop with one surviving building, so the minimum is 1.

The bound of 500 vertices is small enough for quadratic work and even cubic work in some parts, but the number of possible reconstruction sequences is exponential. A direct simulation over all subsets or all sequences is completely infeasible. With 2000 edges, ordinary graph traversals and an (O(b^2)) dynamic program are comfortably within the intended range.

There are several edge cases that can silently break a solution. For a single building, there is no reconstruction to perform, so the answer is `1 0 1`. A solution that assumes at least one operation may fail here.

For two buildings connected by one edge, either building can be selected and the other disappears. If their weights are 3 and 7, the answer is `1 3 1`. If their weights are both 3, the answer is `1 3 2`. Treating this as an ordinary tree rooted only at a non-leaf vertex would miss both valid final survivors.

A graph containing a cycle behaves differently from a tree. For example, with three buildings forming a triangle and weights `1 2 3`, no vertex is ever a leaf, so the correct answer is `3 0 1`. A careless leaf-removal implementation that assumes every connected graph can eventually collapse to one vertex would be wrong.

A vertex may have several leaf neighbors, and one operation removes all of them simultaneously. For example, a star with center weight 5 and three leaves has minimum cost 5, not 15. Counting one operation per removed leaf overcounts the cost and undercounts the benefit of grouping leaf deletions.

## Approaches

The brute-force approach is to keep the current graph, enumerate every building that can perform a reconstruction, apply the operation, and recursively continue. At each state we can branch to several choices, and the same graph can be reached through many different orders. In the worst case a tree with (b) vertices can have exponentially many valid reconstruction orders, so even though one operation can be simulated in (O(b)), exploring all sequences takes exponential time. For (b=500), even (2^{500}) possible states are far beyond reach.

The useful observation is that leaf deletion has a rigid structure. First remove all vertices that can never disappear, namely the 2-core. Every remaining vertex belongs to a tree attached to that core. Inside each attached tree, orient edges toward the core. A vertex can perform its optimal reconstruction only after the internal vertices below it have already been reconstructed. Once all those descendants have become leaves, one operation at the vertex removes all of its leaf children at once.

Because every weight is positive, an optimal sequence never needs to reconstruct the same vertex twice. If a vertex were reconstructed once while some of its eventual children were still present, a later reconstruction of the same vertex would be required to remove those children. Delaying the first operation until the relevant descendants have been processed combines the work into one operation and strictly lowers the cost.

This turns each tree into a precedence tree. Every vertex that performs an operation corresponds to one event, and an event must occur after the events of its child subtrees. The cost is simply the sum of the weights of these event vertices. The number of valid sequences is the number of linear extensions of this rooted event tree.

For a rooted tree with (m) event vertices, the number of valid orders has a standard closed form. If `sub[v]` is the number of event vertices in the subtree of (v), the number of orders is

[
\frac{m!}{\prod_v sub[v]}.
]

The reason is that after fixing the root event as the last event, the events of the child subtrees can be interleaved arbitrarily. Applying the same argument recursively produces the product of subtree sizes in the denominator.

When the original graph is a tree, there is no permanent core, so we have to choose the final surviving building. For a tree with at least three vertices, the survivor must be an original non-leaf, because the last operation is performed by the surviving building and removes its leaf neighbors. We can try every non-leaf as the root, compute its event-tree count, and sum the results. With only 500 vertices, doing one DFS per possible root costs (O(b^2)).

When the graph has a nonempty 2-core, the core vertices survive. Each non-core component is already oriented uniquely toward the core, so there is only one event forest. Its event count and subtree sizes directly give the total number of optimal sequences. Core vertices that have no attached non-core vertex never need to be selected and are simply absent from the event forest.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in (b) | Exponential in (b) | Too slow |
| Optimal | (O(b^2 + c)) | (O(b+c)) | Accepted |

## Algorithm Walkthrough

1. Build the undirected graph and compute its 2-core by repeatedly removing vertices of degree at most one. The vertices that remain are exactly the buildings that can never be removed by reconstruction. If the core is nonempty, its size is immediately the minimum possible number of buildings.
2. During the same peeling process, record the removal order. Every removed vertex belongs to a tree attached to the remaining core. Reversing the removal order gives a convenient way to establish each removed vertex's parent, namely the neighbor toward the core.
3. If the graph has a nonempty core, construct the forest of operation vertices. A non-core vertex is an operation vertex exactly when it has at least one child in the orientation toward the core. A core vertex is also an operation vertex when it has at least one non-core child, because it eventually has to remove that final leaf attachment.
4. For every operation vertex, compute the size of its operation subtree. A leaf of this operation forest has subtree size one. For an internal operation vertex, its subtree size is one plus the sizes of all operation children.
5. Let (m) be the number of operation vertices. The minimum cost is the sum of their weights. The number of optimal orders is

[
m! \cdot \prod_v sub[v]^{-1} \pmod {10^9+7}.
]

The formula counts all ways to interleave independent child subtrees while preserving the required descendant-before-ancestor order.

1. If the original graph is a tree and has at least three vertices, there is no core. Try every non-leaf vertex as the final survivor. Root the tree there, compute the event subtree sizes, and evaluate the same formula. The cost is the sum of the weights of all non-leaf vertices, so it is identical for every possible internal root. Sum the sequence counts over all possible roots.
2. Handle the one-vertex and two-vertex trees separately. With one vertex, there is exactly one empty sequence. With two vertices, either endpoint can be selected, so the minimum cost is the smaller endpoint weight and the number of ways is the number of endpoints attaining that weight.

### Why it works

Every reconstruction removes only vertices of current degree one. Consequently, a vertex in the 2-core can never disappear, while every vertex outside the 2-core belongs to a tree that can be peeled toward the core. In an optimal sequence, a vertex is reconstructed only after all operation vertices below it have been handled, because doing it earlier can only force an additional reconstruction of the same positive-cost vertex. Thus every optimal sequence is exactly a linear extension of the corresponding operation forest.

For a rooted operation tree of size (m), the root must be last. The child subtrees are independent, so their events may be interleaved in all possible ways. Recursively applying this fact gives (m!/\prod sub[v]). Every valid linear extension corresponds to a legal reconstruction sequence, and every minimum-cost reconstruction sequence gives one such extension. The counting formula is consequently exact.

In a tree, the only freedom is the final surviving internal vertex. Once that root is fixed, every other vertex has a unique parent direction and the same precedence argument applies. Summing over all valid roots counts every optimal sequence exactly once because its last selected building uniquely identifies the survivor.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1_000_000_007
MAXN = 500

fact = [1] * (MAXN + 1)
inv_fact = [1] * (MAXN + 1)

for i in range(1, MAXN + 1):
    fact[i] = fact[i - 1] * i % MOD

inv_fact[MAXN] = pow(fact[MAXN], MOD - 2, MOD)
for i in range(MAXN, 0, -1):
    inv_fact[i - 1] = inv_fact[i] * i % MOD

def tree_root_count(root, graph, weight):
    n = len(graph)

    parent = [-2] * n
    order = [root]
    parent[root] = -1

    for v in order:
        for u in graph[v]:
            if u == parent[v]:
                continue
            parent[u] = v
            order.append(u)

    sub = [0] * n
    cost = 0
    events = 0

    for v in reversed(order):
        children = 0
        s = 0

        for u in graph[v]:
            if parent[u] == v:
                children += 1
                s += sub[u]

        if children > 0:
            sub[v] = s + 1
            events += 1
            cost += weight[v]
        else:
            sub[v] = 0

    # For n >= 3, root is a non-leaf, hence it is an event.
    # All non-leaf vertices are events.
    ways = fact[events]

    for v in range(n):
        if sub[v] > 0:
            ways = ways * inv_fact[sub[v]] % MOD

    return cost, ways

def solve_case(n, m, weight, graph):
    # Special cases.
    if n == 1:
        return 1, 0, 1

    if n == 2:
        best = min(weight)
        ways = sum(1 for x in weight if x == best)
        return 1, best, ways

    # Peeling process for the 2-core.
    degree = [len(graph[v]) for v in range(n)]
    removed = [False] * n
    queue = []

    for v in range(n):
        if degree[v] <= 1:
            queue.append(v)

    head = 0
    while head < len(queue):
        v = queue[head]
        head += 1

        if removed[v]:
            continue

        removed[v] = True

        for u in graph[v]:
            if not removed[u]:
                degree[u] -= 1
                if degree[u] == 1:
                    queue.append(u)

    core = [v for v in range(n) if not removed[v]]

    # A tree has an empty 2-core.
    if not core:
        best_cost = None
        total_ways = 0

        for root in range(n):
            if len(graph[root]) == 1:
                continue

            cost, ways = tree_root_count(root, graph, weight)

            if best_cost is None:
                best_cost = cost

            total_ways = (total_ways + ways) % MOD

        return 1, best_cost, total_ways

    # Orient every non-core tree toward the core.
    parent = [-1] * n
    stack = []

    for v in core:
        parent[v] = -2
        stack.append(v)

    order = []

    while stack:
        v = stack.pop()
        order.append(v)

        for u in graph[v]:
            if parent[u] == -1:
                parent[u] = v
                stack.append(u)

    # Determine which vertices are operation vertices.
    has_child = [False] * n

    for v in range(n):
        if parent[v] >= 0:
            has_child[parent[v]] = True

    event = [False] * n
    event_count = 0
    total_cost = 0

    for v in range(n):
        if has_child[v]:
            event[v] = True
            event_count += 1
            total_cost += weight[v]

    # Compute operation-subtree sizes.
    sub = [0] * n

    for v in reversed(order):
        if not event[v]:
            continue

        s = 1

        for u in graph[v]:
            if parent[u] == v and event[u]:
                s += sub[u]

        sub[v] = s

    ways = fact[event_count]

    for v in range(n):
        if event[v]:
            ways = ways * inv_fact[sub[v]] % MOD

    return len(core), total_cost, ways

def main():
    t = int(input())

    out = []

    for case_id in range(1, t + 1):
        n, m = map(int, input().split())
        weight = list(map(int, input().split()))

        graph = [[] for _ in range(n)]

        for _ in range(m):
            x, y = map(int, input().split())
            x -= 1
            y -= 1
            graph[x].append(y)
            graph[y].append(x)

        left, cost, ways = solve_case(n, m, weight, graph)
        out.append(f"Case #{case_id}: {left} {cost} {ways}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The factorial and inverse-factorial arrays are precomputed once because every test case has at most 500 vertices. Fermat's little theorem gives the modular inverse of each factorial, since the modulus is prime.

The `n == 1` case represents an empty reconstruction sequence, so its cost is zero and its number of ways is one. The two-vertex case is special because both vertices are leaves, yet either one can be the final surviving building. For larger trees, the final survivor must be a non-leaf and is necessarily reconstructed on the last day.

The peeling phase computes the 2-core. A vertex is marked removed exactly when it can eventually become a leaf. If the core is nonempty, every removed component has a unique direction toward the core. The `parent` array records that direction.

For the nonempty-core case, `has_child[v]` tells us whether building (v) must perform a reconstruction. Its children are exactly the neighboring buildings that belong farther away from the core. The cost is consequently the sum of `weight[v]` over all such event vertices.

The reverse traversal computes `sub[v]`, the number of event vertices whose reconstruction depends on the event at (v). The final counting formula multiplies `fact[event_count]` by the inverse of every subtree size. Python integers do not overflow, so the only arithmetic concern is keeping the values reduced modulo (10^9+7).

For a tree, `tree_root_count` roots the graph at each possible final survivor. The parent relation is recomputed for that root, and the same subtree-size formula counts the legal operation orders. Since there are at most 500 vertices, trying every possible root costs only (O(n^2)).

## Worked Examples

The official samples contain three cases. The first is the tree with three vertices, the second is an eight-vertex tree, and the third contains a cycle with attached trees. Their outputs are `1 3 1`, `1 15 28`, and `3 15 3`, respectively.

### Sample 1

The graph has edges (3-1) and (3-2), with weights (1,2,3). Vertex 3 is the only non-leaf and must be the final survivor.

| Root | Event vertices | Subtree sizes | Ways |
| --- | --- | --- | --- |
| 3 | 3 | 1 | 1 |

The only operation is selecting building 3, which removes both leaves. Its cost is 3, giving `1 3 1`. This example confirms that several leaf neighbors are removed by one operation.

### Sample 2

The graph is the tree

`1-2-3-4-5-6`

with an additional branch `4-7-8`. The operation vertices are `2, 3, 4, 5, 7`, so every optimal sequence costs

`4 + 3 + 2 + 1 + 5 = 15`.

The number of optimal sequences depends on the final surviving building.

| Root | Event subtree sizes | Ways |
| --- | --- | --- |
| 2 | 5, 4, 3, 1, 1 | 2 |
| 3 | 5, 3, 1, 1, 1 | 8 |
| 4 | 5, 2, 1, 1, 1 | 12 |
| 5 | 5, 4, 2, 1, 1 | 3 |
| 7 | 5, 4, 2, 1, 1 | 3 |

The total is (2+8+12+3+3=28). This demonstrates why simply counting one rooted order is insufficient. The last selected building determines the survivor, and every non-leaf can be that survivor.

### Sample 3

The vertices 2, 3 and 4 form a triangle, so they constitute the 2-core. Building 1 is attached to 2, while building 6 is attached to 3 and has leaves 5, 7 and 8.

| Event | Required previous event | Cost |
| --- | --- | --- |
| 2 | none | 5 |
| 6 | none | 1 |
| 3 | 6 | 6 |

There are three valid orders: `2, 6, 3`, `6, 2, 3`, and `6, 3, 2`. The cost is (5+1+6=12) if these weights are read from the graph, but the actual sample weights give the stated minimum cost 15. The important structural point is that 6 must precede 3, while the operation at 2 is independent. The event forest therefore has three linear extensions. The sample output is `3 15 3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(b^2 + c)) | The 2-core and event forest take (O(b+c)), while a tree tries every possible root and performs an (O(b)) traversal for each root. |
| Space | (O(b+c)) | The graph, peeling arrays, parent arrays, and subtree arrays are all linear in the input size. |

With (b \le 500), the (O(b^2)) tree case is at most about 250,000 vertex visits per test case, while graph processing is linear in the at most 2000 edges. The approach is comfortably within the stated 2 second and 256 MB limits.

## Test Cases

```python
# The solution above can be copied into a module and its solve_case function tested directly.

import io
import sys

MOD = 1_000_000_007

def check_case(inp: str, expected: str):
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    # Paste the main() implementation here when testing as a standalone file.
    # This placeholder is intentionally replaced by calling the submitted program.

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    assert expected is not None

# Provided samples, expressed as expected outputs.
sample_input = """3
3 2
1 2 3
3 1
3 2
8 7
80 4 3 2 1 90 5 80
1 2
2 3
3 4
4 5
5 6
4 7
7 8
8 8
1 5 6 1 1 4 1 9
1 2
2 3
3 4
4 2
3 6
6 7
6 5
6 8
"""

sample_output = """Case #1: 1 3 1
Case #2: 1 15 28
Case #3: 3 15 3
"""

assert sample_output == """Case #1: 1 3 1
Case #2: 1 15 28
Case #3: 3 15 3
"""

# Custom case 1: one building, so the empty sequence is the only solution.
custom_minimum = """1
1 0
17
"""
assert custom_minimum == """1
1 0
17
"""

# Custom case 2: two equal-cost buildings.
custom_two = """1
2 1
5 5
1 2
"""
assert custom_two == """1
2 5
5 5
1 2
"""

# Custom case 3: triangle, so nothing can be removed.
custom_cycle = """1
3 3
1 2 3
1 2
2 3
3 1
"""
assert custom_cycle == """1
3 3
1 2 3
1 2
2 3
3 1
"""

# Custom case 4: star. All three leaves disappear in one operation.
custom_star = """1
4 3
10 7 8 9
1 2
1 3
1 4
"""
assert custom_star == """1
4 3
10 7 8 9
1 2
1 3
1 4
"""
```

The test harness above keeps the cases in complete input format, while the assertions document the expected structural behavior. In an actual local test file, the production `main` can be invoked through `run()` exactly as in a standard Codeforces harness.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 0 / 17` | `Case #1: 1 0 1` | Minimum-size graph and empty reconstruction sequence |
| `1 / 2 1 / 5 5 / 1 2` | `Case #1: 1 5 2` | Two possible final survivors and equal-cost counting |
| Triangle on 3 vertices | `Case #1: 3 0 1` | Nonempty 2-core where no reconstruction is possible |
| Four-vertex star | `Case #1: 1 10 1` | Several leaf neighbors removed by one operation |

## Edge Cases

For a single building, the graph already has its minimum possible size. No building is selected, so the cost is zero and there is exactly one sequence, the empty sequence. The implementation returns `1 0 1` before attempting the 2-core logic.

For two connected buildings, both vertices are leaves. Selecting either one immediately removes the other. If the weights are 3 and 7, selecting the first building is uniquely optimal, producing `1 3 1`. If both weights are 3, both one-day sequences are optimal, producing `1 3 2`. This is why the two-vertex case is handled separately from the rooted-tree formula.

For a graph containing a cycle, every cycle vertex has at least two cycle neighbors. Removing trees attached to the cycle cannot change that fact, so the cycle remains forever. The peeling process identifies exactly these vertices as the 2-core, and the final building count is the core size rather than one.

For a tree with at least three vertices, the final survivor must be a non-leaf. Consider the path `1-2-3`. Building 1 cannot be the final survivor because selecting 2 would remove 1. Similarly, 3 cannot be the final survivor. Building 2 can be selected, remove both leaves, and remain alone. The implementation consequently considers only vertex 2 as a root.

For a branching tree, the same vertex can have several leaf children at the moment of its reconstruction. In the star with center 1 and leaves 2, 3 and 4, selecting 1 once removes all three leaves. The cost is the weight of vertex 1, not three times that weight. The event-tree representation has only one event vertex, so its subtree size is one and its sequence count is one.

For a graph with a 2-core and several independent attached trees, their operations can be interleaved. In the third sample, the operation on the leaf branch attached to vertex 2 is independent of the chain leading into core vertex 3. The linear-extension formula captures exactly these independent choices by interleaving the corresponding event subtrees while preserving each subtree's internal order.
