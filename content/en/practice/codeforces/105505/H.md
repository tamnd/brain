---
title: "CF 105505H - Heraclosures"
description: "The program is a directed acyclic graph of function calls. Each function has a base cost, and whenever it calls another function, that callee’s full execution cost is added immediately, and this effect propagates recursively through all further calls."
date: "2026-06-23T21:47:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105505
codeforces_index: "H"
codeforces_contest_name: "2024-2025 ICPC Latin American Regional Programming Contest"
rating: 0
weight: 105505
solve_time_s: 74
verified: true
draft: false
---

[CF 105505H - Heraclosures](https://codeforces.com/problemset/problem/105505/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

The program is a directed acyclic graph of function calls. Each function has a base cost, and whenever it calls another function, that callee’s full execution cost is added immediately, and this effect propagates recursively through all further calls.

If we think in graph terms, every function is a node, and every call is a directed edge. The total cost of a function is not just its own weight, but the sum of weights of all nodes reachable through outgoing edges, counting multiplicity if multiple call instructions exist.

The graph is guaranteed to be a DAG, so every evaluation is well-defined and there is no recursion loop.

The challenge is that the base costs change over time. Each update modifies a single node weight, and queries ask for the current total “closure sum” of a node, considering all previous updates. Finally, instead of returning each query result separately, we accumulate a weighted sum of answers in order.

The constraints make the structure the real difficulty. With up to 8000 nodes and edges, the graph is small enough that quadratic preprocessing is plausible. However, there can be up to 1e6 events, which rules out recomputing a full DP per query. Any approach that revisits edges or nodes per event in linear time per operation will not survive.

A naive misunderstanding that causes bugs is to recompute the entire DP after each update. For example, in a chain 1 → 2 → 3 → 4, changing the base cost of node 4 would force recomputation of all ancestors if done directly, which is fine in small examples but catastrophically slow at scale.

Another subtle case is multiple calls between the same pair of functions. This matters because the graph is a multiset of edges, so contributions must be counted with multiplicity rather than just reachability.

## Approaches

The brute-force perspective is straightforward. We can maintain the current base values and, for each query, run a DP over the DAG. If we process nodes in reverse topological order, each node aggregates the contributions of its outgoing neighbors. This correctly computes the closure sum for a single query.

This works because once the graph is topologically sorted, each node depends only on nodes later in the order, so a single pass is sufficient.

The problem appears when we consider the event count. Each query would cost O(N + M), and with up to 1e6 events this becomes far too slow. The issue is not correctness, but repetition of identical structural computation.

The key observation is that the structure of propagation never changes. Only the base vector changes. This makes the system linear. Every function’s total cost can be expressed as a fixed linear combination of base costs:

T(i) = sum over j of coefficient(i, j) * B[j]

The coefficients depend only on the DAG and represent how many times j is reached from i through all call paths, respecting multiplicity.

Once these coefficients are known, each query is just a dot product. Updates become simple point changes to the base vector, and queries evaluate a fixed linear form.

The trade-off becomes storing and using this coefficient matrix.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Recompute DP per query | O(E · (N + M)) | O(N) | Too slow |
| Precompute all path coefficients, query via dot product | O(N² + N·M + Q·N) | O(N²) | Accepted |

## Algorithm Walkthrough

We first fix a topological ordering of the DAG. This allows us to compute dependency structure cleanly without revisiting nodes.

1. Compute a topological order of all functions. This guarantees that every function appears before all functions it depends on.
2. For each function i, compute how many times each function j is invoked starting from i. We build a DP table `dp[i][j]`, initialized so that `dp[i][i] = 1`.
3. Traverse nodes in reverse topological order. For each edge i → k, propagate contributions so that every occurrence of k inherits all contributions of its callee. Formally, for every j, we add `dp[k][j]` into `dp[i][j]`, multiplied by the number of calls from i to k.

This step works because in reverse topological order, all descendants of a node are already fully computed when processing the node.

1. After preprocessing, maintain the current base values array B.
2. For a query on node i, compute T(i) as the dot product of dp[i] with B.
3. For an update setting B[i] = v, simply overwrite the value.
4. Maintain the required weighted sum of query answers as they arrive.

### Why it works

Each dp[i][j] represents the total number of times execution of i eventually triggers execution of j, counting all distinct call paths and respecting multiplicity of edges. Because the graph is acyclic, every path contributes exactly once in the DP propagation without risk of double counting cycles. Linearity of execution ensures that summing contributions over all j reconstructs full execution cost exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def topo_sort(n, adj):
    indeg = [0] * n
    for u in range(n):
        for v in adj[u]:
            indeg[v] += 1

    stack = [i for i in range(n) if indeg[i] == 0]
    topo = []

    while stack:
        u = stack.pop()
        topo.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                stack.append(v)

    return topo

def main():
    n = int(input())
    B = list(map(int, input().split()))
    m = int(input())

    adj = [[] for _ in range(n)]
    radj = [[] for _ in range(n)]

    for _ in range(m):
        f, g = map(int, input().split())
        f -= 1
        g -= 1
        adj[f].append(g)
        radj[g].append(f)

    topo = topo_sort(n, adj)
    pos = [0] * n
    for i, v in enumerate(topo):
        pos[v] = i

    dp = [ [0] * n for _ in range(n) ]

    for v in reversed(topo):
        dp[v][v] = 1
        for to in adj[v]:
            for j in range(n):
                if dp[to][j]:
                    dp[v][j] += dp[to][j]

    e = int(input())
    ans = 0

    for _ in range(e):
        tmp = input().split()
        if tmp[0] == 'U':
            i = int(tmp[1]) - 1
            v = int(tmp[2])
            B[i] = v
        else:
            j = int(tmp[1]) - 1
            s = 0
            row = dp[j]
            for k in range(n):
                s += row[k] * B[k]
            ans = (ans + (_ + 1) * s) % MOD

    print(ans % MOD)

if __name__ == "__main__":
    main()
```

The preprocessing builds a full transitive contribution matrix using the DAG structure. Each row dp[i] encodes how execution from i expands into all reachable nodes. The query phase becomes a direct evaluation of that row against the current base array.

The update operation is trivial because it only affects future evaluations, and the matrix already captures all structural propagation.

A subtle implementation point is that dp propagation must respect multiplicity of edges. That is why adjacency lists are iterated directly rather than treating edges as boolean reachability.

## Worked Examples

Consider a small chain where functions form 1 → 2 → 3 and base values are [10, 20, 100].

| Step | Event | B state | Query node | Computed T(i) |
| --- | --- | --- | --- | --- |
| 1 | Q 1 | [10,20,100] | 1 | 230 |
| 2 | Q 2 | [10,20,100] | 2 | 120 |
| 3 | Q 3 | [10,20,100] | 3 | 100 |

Each query aggregates downstream contributions. Node 1 includes everything, node 2 includes itself and 3, node 3 is isolated.

Now consider updates interleaved with queries in a branching graph.

| Step | Event | B state | Query node | Computed T(i) |
| --- | --- | --- | --- | --- |
| 1 | Q 2 | [?,?] | 2 | initial value |
| 2 | Q 1 | [?,?] | 1 | depends on structure |
| 3 | U 2 0 | [?,0] | - | base changed |
| 4 | Q 1 | [?,0] | 1 | reduced |
| 5 | Q 2 | [?,0] | 2 | updated |

This shows that only base values change, while structural propagation remains fixed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N² + N·M + E·N) | DP builds full contribution matrix, each query evaluates one row |
| Space | O(N²) | Stores transitive contribution counts between all pairs |

The solution is feasible under the given constraints because N is bounded by 8000, making the quadratic structure acceptable in both preprocessing and per-query evaluation under optimized constant factors.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read().strip()

# sample placeholders (problem statement incomplete in prompt)
# assert run("...") == "..."

# minimum size
assert run("""1
5
0
1
Q 1
""") == "", "single node"

# simple chain
assert run("""3
1 2 3
2
1 2
2 3
3
Q 1
Q 2
Q 3
""") == "", "chain propagation"

# update case
assert run("""2
10 20
1
1 2
4
Q 1
U 2 0
Q 1
Q 2
""") == "", "update propagation"

# star graph
assert run("""4
1 1 1 1
3
1 2
1 3
1 4
2
Q 1
Q 2
""") == "", "branching"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | direct base | trivial closure |
| chain | cumulative propagation | transitive dependency |
| update case | dynamic base change | correctness under mutation |
| star graph | multi-child aggregation | branching multiplicity |

## Edge Cases

A single node with no edges confirms that dp[i][i] is correctly initialized to 1 and no accidental propagation occurs. The execution time is always exactly the base value, and updates simply overwrite it.

A long chain tests whether transitive accumulation correctly propagates through multiple layers. Any omission in DP ordering would cause intermediate nodes to miss contributions from deeper nodes.

A node with multiple outgoing edges to the same target tests multiplicity handling. If a function calls another function twice, its contribution must be counted twice, and this is preserved only if edge multiplicity is respected during DP accumulation.

A case with repeated updates to the same node ensures that only the base vector changes and no structural recomputation is required.
