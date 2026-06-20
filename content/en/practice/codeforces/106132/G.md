---
title: "CF 106132G - Torque Transmission"
description: "We are given a directed network of gears connected by shafts. Each shaft transfers torque from one gear to another, but only a fraction of the incoming torque survives, determined by an efficiency percentage on that shaft."
date: "2026-06-20T07:57:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106132
codeforces_index: "G"
codeforces_contest_name: "National Yang Ming Chiao Tung University 2025 Individual Programming Contest"
rating: 0
weight: 106132
solve_time_s: 47
verified: true
draft: false
---

[CF 106132G - Torque Transmission](https://codeforces.com/problemset/problem/106132/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed network of gears connected by shafts. Each shaft transfers torque from one gear to another, but only a fraction of the incoming torque survives, determined by an efficiency percentage on that shaft. If a shaft from gear `u` to gear `v` has efficiency `e`, then any torque `x` arriving at `u` contributes `x * (e / 100)` at `v`.

For each query, we start by applying a fixed torque at a source gear `s`. That torque then propagates along directed edges, being multiplied by efficiencies along the way. If there are multiple possible paths to a target gear `t`, the torque contributions do not add across different paths in a linear way unless we are considering the maximum possible delivered torque. Since we want the best achievable outcome, we are effectively looking for the path from `s` to `t` that maximizes the product of edge efficiencies, and then multiplying the initial torque by that maximum product.

So each query reduces to finding a maximum multiplicative path value in a directed weighted graph, where edge weights are probabilities in `[0, 1]`.

The constraints are small enough that we can afford a shortest-path style computation per query. With `n ≤ 1000` and `m ≤ 5000`, running a Dijkstra-like algorithm per query is feasible because `q ≤ 100`. A naive all-pairs preprocessing approach like Floyd-Warshall would involve about `n^3 ≈ 10^9` operations, which is borderline but too slow in Python. Re-running a heap-based best-path search per query is comfortably within limits.

A subtle issue appears when thinking about multiple paths. A greedy relaxation must ensure we always propagate the best known product, because a suboptimal intermediate value can later become optimal if extended through a high-efficiency edge. This rules out any BFS-style “first arrival wins” approach.

Edge cases that matter:

First, unreachable targets. If there is no path from `s` to `t`, the answer must be `0`, not a tiny floating-point value. For example, if `s = 1`, `t = 2`, and no path exists, the correct output is `0`, even though internal distances might remain at `0` or `-inf` depending on representation.

Second, cycles with efficiency greater than 100% are impossible since `e ≤ 100`, so no amplification exists. This guarantees that path products never increase by looping, so Dijkstra-style monotonicity holds.

Third, floating-point precision matters because we multiply many percentages. Using double precision is sufficient since the required error tolerance is `1e-6`.

## Approaches

The brute-force idea is to enumerate all possible paths from `s` to `t`, compute the product of efficiencies along each path, and take the maximum. This is correct because it directly matches the definition of the problem. However, the number of paths in a graph with cycles can grow exponentially. Even in a moderately connected graph, the number of distinct simple paths can explode beyond any feasible bound, making this approach unusable beyond tiny instances.

A more structured view is to notice that each path contributes a multiplicative score. If we transform edge weights by taking logarithms, maximizing a product becomes equivalent to maximizing a sum of log values. That converts the problem into a longest path problem in a graph with positive edge weights in log space. However, because logs of values in `(0,1]` are non-positive, we are actually maximizing a sum of negative weights, which is equivalent to finding a shortest path in a graph with non-negative edge costs after negation. Instead of explicitly transforming signs, it is simpler to directly run a Dijkstra-style algorithm on multiplicative weights, treating relaxation as maximization.

The key observation is that the best value to a node is monotonic under relaxation: once we have a larger product for a node, extending it can only produce better or equal candidates for neighbors. This allows a priority queue approach where we always expand the currently best-known state.

Since we have up to 100 queries, running this single-source maximum-product search per query is efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all paths) | Exponential | O(n) recursion stack | Too slow |
| Optimal (Dijkstra per query) | O(q · m log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

We treat each query independently.

### 1. Convert efficiencies into multiplicative weights

Each edge `u → v` with efficiency `e` is treated as a factor `e / 100`. This is the value we multiply along a path.

### 2. Initialize best-torque array

We maintain an array `dist[]` where `dist[i]` stores the maximum fraction of initial torque that can reach node `i`. We set all values to `0`, except `dist[s] = 1`.

This represents that at the source we retain full torque before any transmission losses.

### 3. Use a max-priority queue

We store states `(current_best_factor, node)` in a priority queue ordered by highest factor first. We begin with `(1, s)`.

We use a max-heap behavior (implemented via negative values or reversed comparison) so that we always expand the most promising partial path first.

### 4. Relax outgoing edges

When processing node `u` with current factor `f`, we attempt to improve all neighbors `v` via `f * (e / 100)`. If this value is greater than `dist[v]`, we update `dist[v]` and push it into the heap.

This step ensures that any improvement to a node immediately propagates forward, similar to Dijkstra’s relaxation.

### 5. Early stopping is optional

We can stop once we pop the target node `t` from the priority queue, since at that moment we have found its optimal value.

### 6. Output result

If `dist[t]` remains `0`, the node is unreachable and we output `0`. Otherwise we multiply `dist[t]` by the initial torque `T`.

### Why it works

The core invariant is that whenever a node is popped from the priority queue, the associated value is the maximum achievable multiplicative factor for that node. This holds because all edge weights are in `[0, 1]`, so extending a path can never increase its value. Therefore, any later discovered path to a node already processed cannot exceed the best value already finalized. This makes the process identical in correctness to Dijkstra’s algorithm, except we maximize instead of minimize.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, m, q = map(int, input().split())
    g = [[] for _ in range(n + 1)]

    for _ in range(m):
        u, v, e = map(int, input().split())
        w = e / 100.0
        g[u].append((v, w))

    for _ in range(q):
        s, t, T = map(int, input().split())

        dist = [0.0] * (n + 1)
        dist[s] = 1.0

        pq = [(-1.0, s)]

        while pq:
            neg_f, u = heapq.heappop(pq)
            f = -neg_f

            if f < dist[u]:
                continue

            if u == t:
                break

            for v, w in g[u]:
                nf = f * w
                if nf > dist[v]:
                    dist[v] = nf
                    heapq.heappush(pq, (-nf, v))

        print(dist[t] * T if dist[t] > 0 else 0.0)

if __name__ == "__main__":
    solve()
```

The graph is stored as adjacency lists with precomputed probabilities. For each query, we reset the `dist` array because each query has an independent source.

The priority queue uses negative values to simulate a max-heap since Python’s `heapq` is a min-heap. We also include a stale-state check `if f < dist[u]` to skip outdated entries.

The early exit when reaching `t` reduces runtime in practice but is not required for correctness.

## Worked Examples

### Example 1

Input:

```
5 6 1
1 2 90
2 3 80
1 4 50
4 5 70
2 5 60
3 5 85
1 5 1000
```

We track best multiplicative factors:

| Step | Node | Factor | dist updates |
| --- | --- | --- | --- |
| init | 1 | 1.0 | dist[1]=1.0 |
| relax | 2 | 0.9 | dist[2]=0.9 |
| relax | 4 | 0.5 | dist[4]=0.5 |
| process 2 | 3 | 0.72 | dist[3]=0.72 |
| process 2 | 5 | 0.54 | dist[5]=0.54 |
| process 3 | 5 | 0.612 | dist[5]=0.612 |

Final best factor to node 5 is `0.612`, so output is `612.0`.

This shows that a later path via node `3` improves over the direct `2 → 5` route.

### Example 2

Input:

```
3 2 1
1 2 50
2 3 50
1 3 100
1 3 100
```

| Step | Node | Factor | dist updates |
| --- | --- | --- | --- |
| init | 1 | 1.0 | dist[1]=1.0 |
| relax | 2 | 0.5 | dist[2]=0.5 |
| relax | 3 | 0.25 | dist[3]=0.25 |

Node 3 is unreachable from a direct edge, so best is `0.25`. Multiplying by `100` gives `25.0`.

This demonstrates that even if a direct edge exists in some variants, the algorithm correctly compares all competing paths.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q · m log n) | Each query runs a Dijkstra-style search over at most m edges, each heap operation costs log n |
| Space | O(n + m) | adjacency list plus distance array and priority queue |

With `q ≤ 100`, `m ≤ 5000`, and `n ≤ 1000`, this runs comfortably within limits in Python, since the total heap operations remain on the order of a few million.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from solution import solve
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample-like case
assert abs(float(run("""5 6 1
1 2 90
2 3 80
1 4 50
4 5 70
2 5 60
3 5 85
1 5 1000
""")) - 612.0) < 1e-6

# unreachable case
assert run("""3 1 1
1 2 50
3 3 10
""") == "0.0"

# direct best path dominates long path
assert abs(float(run("""3 3 1
1 2 90
2 3 90
1 3 50
1 3 100
""")) - 100 * 0.81) < 1e-6

# single node style
assert abs(float(run("""1 0 1
1 1 100
""")) - 100.0) < 1e-6

# cycle harmless
assert abs(float(run("""3 3 1
1 2 90
2 3 90
3 1 90
1 3 100
""")) - 81.0 * 100) < 1e-6
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| small multi-path | 612.0 | competing paths correctness |
| unreachable | 0.0 | no path handling |
| direct vs indirect | 81.0 | path comparison |
| single node | 100.0 | base case |
| cycle | 81.0 | cycle safety |

## Edge Cases

One important edge case is when the target is unreachable. Suppose we have:

```
3 1 1
1 2 50
1 3 100
```

There is no path from `3` to `1`, so the algorithm initializes `dist[3]=1` but never reaches `1`. The priority queue empties without visiting the target, leaving `dist[1]=0`. The output correctly becomes `0`.

Another case is when multiple paths exist with different lengths and efficiencies:

```
1 → 2 → 3 (0.5 * 0.5 = 0.25)
1 → 3 (0.2)
```

The algorithm first discovers `3` with `0.2`, then later improves it to `0.25`. The relaxation step ensures the improvement is not ignored, since we only finalize a node when its best value is extracted from the heap.

A third case is self-contained cycles. Because all weights are at most `1`, repeatedly traversing a cycle can never increase the product. Even if a cycle exists, it cannot create infinite improvement loops. The priority queue will naturally ignore revisiting nodes with worse values, preventing infinite processing.
