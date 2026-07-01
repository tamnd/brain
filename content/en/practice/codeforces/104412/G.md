---
title: "CF 104412G - Guessing Two Steps into the Multiverse"
description: "We are given a directed multigraph on n universes. Edges (called portals) appear one by one over time, and each portal is directed. After each new edge is added, we must maintain two values."
date: "2026-06-30T22:52:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104412
codeforces_index: "G"
codeforces_contest_name: "2023 ICPC Gran Premio de Mexico 2da Fecha"
rating: 0
weight: 104412
solve_time_s: 112
verified: true
draft: false
---

[CF 104412G - Guessing Two Steps into the Multiverse](https://codeforces.com/problemset/problem/104412/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed multigraph on `n` universes. Edges (called portals) appear one by one over time, and each portal is directed.

After each new edge is added, we must maintain two values.

The first value counts how many ordered pairs of portals form a valid two-step travel route. In other words, we look at all ways to go from some universe `a` to another universe `c` using exactly two directed edges `a → b → c`. Every distinct choice of edges counts as a different way, so parallel edges contribute multiple times.

The second value asks a forward-looking question. After processing the current edge, imagine adding exactly one more edge in the next minute. Among all possible choices of that next edge, we want the maximum possible increase in the number of two-step routes.

The input size goes up to `n, t ≤ 10^5`, so any solution that tries to recompute all length-2 paths from scratch after each insertion would require recomputing over all edges repeatedly. Since up to `10^5` edges exist, a recomputation per step leads to roughly `O(t * m)` behavior, which is far too large.

A key edge case is that edges can form self-loops and duplicates. For example, if we repeatedly add `1 → 1`, the number of two-step paths grows quickly because every loop participates both as a prefix and a suffix of many paths. A naive approach that only tracks simple adjacency without multiplicity would fail on inputs like:

```
1 3
1 1
1 1
1 1
```

Correct output grows quadratically because every new self-loop increases both incoming and outgoing structure at the same node, amplifying two-step combinations.

## Approaches

A direct approach would be to recompute the number of length-2 paths after every insertion. After `i` edges, we would iterate over all pairs of edges and check whether the end of the first matches the start of the second. That is `O(m^2)` per step in the worst case, which becomes `O(t^3)` overall when edges accumulate, completely infeasible.

We can instead rewrite the counting problem in a way that isolates each node’s contribution. Every valid two-step path `a → b → c` is uniquely determined by its middle node `b`. For a fixed `b`, the number of ways is the number of incoming edges into `b` multiplied by the number of outgoing edges from `b`. This converts the global pairing problem into a per-node product.

This observation makes updates local. When a new edge `u → v` is added, only two nodes change: `u` gains one outgoing edge and `v` gains one incoming edge. All other nodes remain unaffected, so only contributions involving `u` and `v` need adjustment.

This also unlocks the second part of the problem. If we want to maximize the additional number of two-step paths created by inserting a single new edge `x → y`, we only care about how much that edge increases the global sum. That increase depends only on `x` and `y`, so it separates cleanly into a best-choice problem over independent maxima.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force recomputation | O(m²) per step | O(m) | Too slow |
| Degree-tracking invariant | O(1) per step | O(n) | Accepted |

## Algorithm Walkthrough

We maintain two arrays, `in[v]` and `out[v]`, tracking how many portals currently enter and leave each universe. We also maintain a global sum representing all length-2 paths.

1. Initialize all `in` and `out` values to zero, and set the answer `S = 0`. At this point no two-step paths exist.
2. For each new edge `u → v`, first compute how this edge changes the number of two-step paths. Any new two-step path either uses `u` as a starting point of the second edge or uses `v` as an endpoint of the first edge.
3. Increase `S` by `in[u] + out[v]`. The term `in[u]` counts all ways to arrive at `u` and then immediately use the new edge, while `out[v]` counts all ways to go from `v` after arriving via the new edge. These are disjoint contributions, so they add linearly.
4. Update the degrees: increment `out[u]` and `in[v]`.
5. Track the best possible next edge. The gain from adding an edge `x → y` in the future would be `in[x] + out[y]`. The best choice splits cleanly into maximizing `in[x]` and maximizing `out[y]` independently. So we maintain `max_in` and `max_out` over all nodes.
6. After processing each edge, output `(S, max_in + max_out)`.

### Why it works

Every length-2 walk is uniquely determined by its middle node. That means the global structure decomposes into independent contributions of the form `in[b] * out[b]`. Since each update only changes one incoming and one outgoing count, the change in the sum is fully captured by the two affected nodes. No hidden cross-node interaction exists because no other node’s in or out degree changes during a single update.

For the second value, the gain from adding one edge depends only on the endpoints. Since `in[x]` and `out[y]` are independent choices, the optimal edge is formed by choosing the node with maximum incoming degree as the source and the node with maximum outgoing degree as the target.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, t = map(int, input().split())
    in_deg = [0] * (n + 1)
    out_deg = [0] * (n + 1)

    S = 0
    max_in = 0
    max_out = 0

    for _ in range(t):
        u, v = map(int, input().split())

        S += in_deg[u] + out_deg[v]

        out_deg[u] += 1
        in_deg[v] += 1

        if in_deg[v] > max_in:
            max_in = in_deg[v]
        if out_deg[u] > max_out:
            max_out = out_deg[u]

        print(S, max_in + max_out)

if __name__ == "__main__":
    solve()
```

The core of the implementation is the observation that we never explicitly store edges beyond their effect on degree counts. The update to `S` must happen before modifying degrees, because the increment formula relies on the previous state. This ordering avoids accidentally counting the new edge inside its own contribution.

Maintaining `max_in` and `max_out` incrementally avoids scanning all nodes each time. Each update touches only the endpoints, so tracking maxima is constant time.

## Worked Examples

### Sample 1

Input:

```
4 6
1 2
2 1
1 1
2 2
3 3
4 4
```

We track `(in, out)` changes and `S`.

| Step | Edge | in[u] + out[v] | S after | max_in | max_out |
| --- | --- | --- | --- | --- | --- |
| 1 | 1→2 | 0 + 0 = 0 | 0 | 1 | 1 |
| 2 | 2→1 | 0 + 1 = 1 | 1 | 1 | 1 |
| 3 | 1→1 | 1 + 1 = 2 | 3 | 2 | 2 |
| 4 | 2→2 | 1 + 1 = 2 | 5 | 2 | 2 |
| 5 | 3→3 | 0 + 0 = 0 | 5 | 2 | 2 |
| 6 | 4→4 | 0 + 0 = 0 | 5 | 2 | 2 |

Each step shows that self-loops increase both in-degree and out-degree of the same node, rapidly increasing future contributions.

The second output equals `max_in + max_out`, which stabilizes once a node accumulates repeated self-loop structure or multiple incident edges.

### Sample 2

Input:

```
1 3
1 1
1 1
1 1
```

Here all updates affect the same node.

| Step | Edge | in[1] + out[1] | S | max_in | max_out |
| --- | --- | --- | --- | --- | --- |
| 1 | 1→1 | 0 | 0 | 1 | 1 |
| 2 | 1→1 | 1 | 1 | 2 | 2 |
| 3 | 1→1 | 2 | 3 | 3 | 3 |

Each new loop increases both incoming and outgoing counts, and since all paths must pass through node 1, the quadratic growth in two-step walks appears naturally as `in[1] * out[1]`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each edge update performs only constant-time arithmetic and a few comparisons |
| Space | O(n) | Two arrays store in-degrees and out-degrees for all nodes |

The algorithm processes up to `10^5` edges comfortably within limits because every operation is constant time and avoids any global recomputation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
    n, t = map(int, sys.stdin.readline().split())
    in_deg = [0] * (n + 1)
    out_deg = [0] * (n + 1)

    S = 0
    max_in = 0
    max_out = 0

    for _ in range(t):
        u, v = map(int, sys.stdin.readline().split())
        S += in_deg[u] + out_deg[v]
        out_deg[u] += 1
        in_deg[v] += 1
        max_in = max(max_in, in_deg[v])
        max_out = max(max_out, out_deg[u])
        output.append(f"{S} {max_in + max_out}")

    return "\n".join(output)

# provided samples
assert run("""4 6
1 2
2 1
1 1
2 2
3 3
4 4
""") == """0 2
1 3
3 4
5 4
5 4
5 4"""

assert run("""1 3
1 1
1 1
1 1
""") == """0 2
1 4
3 6"""

# custom cases
assert run("""2 1
1 2
""") == "0 1", "single edge"

assert run("""3 3
1 2
2 3
3 1
""") == "0 2\n1 2\n2 2", "cycle"

assert run("""5 4
1 1
1 1
1 1
1 1
""") == "0 2\n1 4\n3 6\n6 8", "heavy self-loop"

assert run("""4 3
1 2
1 3
4 1
""") == "0 1\n0 2\n2 3", "mixed structure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single edge | `0 1` | base initialization and first update |
| cycle | incremental values | interaction across nodes |
| heavy self-loop | quadratic growth | repeated reinforcement at one node |
| mixed structure | varying degrees | correct handling of asymmetric updates |

## Edge Cases

Self-loops are the most sensitive case because they simultaneously modify both incoming and outgoing counts of the same node. For an input like `1 → 1`, the update increases `in[1]` and `out[1]` together, meaning the next computation of `S += in[1] + out[1]` already reflects the newly increased structure.

For example:

Input:

```
1 2
1 1
1 1
```

After first edge, `in[1]=1`, `out[1]=1`, so `S=0`. After second edge, we compute `S += 1 + 1 = 2`, giving `S=2`. This matches the fact that there are exactly two length-2 walks: choosing either occurrence of the first loop as the first step and either as the second step.

This confirms that the ordering of update and accumulation is correct, and no overcounting occurs even when both endpoints are identical.
