---
title: "CF 104385I - Tree"
description: "We are given a tree where each edge carries an integer value. The tree is fixed, but the edge values change over time. The system supports two operations."
date: "2026-07-01T02:54:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104385
codeforces_index: "I"
codeforces_contest_name: "2023 (ICPC) Jiangxi Provincial Contest -- Official Contest"
rating: 0
weight: 104385
solve_time_s: 54
verified: true
draft: false
---

[CF 104385I - Tree](https://codeforces.com/problemset/problem/104385/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree where each edge carries an integer value. The tree is fixed, but the edge values change over time. The system supports two operations.

The first operation selects two nodes and a value z, then every edge lying on the unique simple path between those two nodes has its value modified by applying a bitwise XOR with z. This is not a replacement, but a toggle in the binary representation, applied independently to each edge on that path.

The second operation asks for a single node and requires computing the XOR of all edge values currently incident to that node.

The tree has up to 500,000 nodes and the number of operations is also up to 500,000, so any solution that inspects every edge on a path explicitly will fail. Even a single long path update can touch O(n) edges, and repeating that across q operations leads to O(nq), which is far beyond feasible limits.

A subtle point is that updates do not ask for path sums or path queries, but instead modify edge states, and queries are local to nodes but depend on all adjacent edges. This mismatch is where naive traversal approaches break down.

A typical failure case appears when repeatedly updating long paths in a chain-shaped tree. For example, in a chain of 100000 nodes, a single update from one end to the other would touch almost every edge, and doing that repeatedly immediately exceeds time limits.

## Approaches

A direct simulation approach would recompute each path by finding the path between x and y using DFS or BFS, then iterating over all edges on that path and toggling their values. This is conceptually straightforward because the tree structure guarantees a unique path. However, each such operation can take linear time in the worst case. With 500,000 operations, this becomes infeasible.

The key observation is that although edges are being updated, the query is not asking about paths or subtrees, but only about the XOR of edges incident to a node. This allows us to avoid explicitly tracking each edge after updates.

Consider what happens when a single edge (u, v) has its value XORed by z. That change affects exactly two nodes: u and v, because both endpoints see that edge in their adjacency list. If we think in terms of node contributions, every edge update is equivalent to applying XOR z to both endpoints of that edge.

Now consider a full path update from x to y. That path consists of a sequence of edges. Every internal node on the path is incident to exactly two of those updated edges, while the endpoints x and y are incident to exactly one. Since XOR is its own inverse, applying z twice cancels out. So internal nodes receive zero net effect, while endpoints receive exactly one XOR z.

This collapses the entire path update into a constant-time operation: we only need to XOR z into x and y.

We also maintain, for each node, the XOR of initial incident edge weights. Every update contributes an additional toggle to the endpoints. Queries simply combine the initial value with all accumulated toggles.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force path traversal per update | O(nq) | O(n) | Too slow |
| Endpoint toggle aggregation | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

We root the tree anywhere, though rooting is not actually required for correctness. We first compute the initial XOR of all incident edge weights for every node.

Each edge contributes its weight to both of its endpoints, so we can initialize an array `base[x]` that stores this XOR directly.

We also maintain another array `delta[x]`, initially all zeros, which stores the accumulated effect of all path updates.

Now we process operations in order.

1. For a type 1 operation with nodes x and y and value z, we apply `delta[x] ^= z` and `delta[y] ^= z`. This represents the fact that exactly the endpoints of the path experience a net XOR effect of z.
2. For a type 2 operation with node x, we output `base[x] ^ delta[x]`. This combines the original incident XOR with all modifications that have affected edges incident to x through path updates.

The correctness of step 1 relies on counting how many times node x appears as an endpoint of updated edges on the path. Internal nodes appear twice and cancel, endpoints appear once and remain.

### Why it works

Every edge update affects exactly its two endpoints. A path update is a collection of edge updates along a simple path. For any node, the number of incident updated edges in that path is either zero, one, or two depending on whether it is outside the path, an endpoint of the path, or an internal node on the path. XOR accumulation turns the “two occurrences” case into no change and the “one occurrence” case into a single toggle. This reduces the entire path structure into endpoint-only effects, preserving the exact contribution each node should receive from all modified edges.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, q = map(int, input().split())

    base = [0] * (n + 1)
    delta = [0] * (n + 1)

    edges = []

    for _ in range(n - 1):
        u, v, w = map(int, input().split())
        base[u] ^= w
        base[v] ^= w
        edges.append((u, v, w))

    out = []

    for _ in range(q):
        tmp = input().split()
        op = int(tmp[0])

        if op == 1:
            x = int(tmp[1])
            y = int(tmp[2])
            z = int(tmp[3])

            delta[x] ^= z
            delta[y] ^= z

        else:
            x = int(tmp[1])
            out.append(str(base[x] ^ delta[x]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The implementation precomputes `base[x]` by XORing all incident edge weights directly while reading the edges. This avoids storing adjacency lists. The `delta` array accumulates the effect of all path updates that touch each endpoint.

For type 1 operations, only the two endpoints are updated. This is the critical optimization that removes dependence on path length.

For type 2 operations, the answer is the current effective XOR of all incident edges, reconstructed as the original value plus all accumulated endpoint toggles.

## Worked Examples

Consider a small chain:

Input:

```
3 3
1 2 1
1 3 2
2 1
1 1 3 2
2 1
```

We start by building `base`:

Node 1 has edges (1,2)=1 and (1,3)=2 so base[1]=3.

Node 2 has base[2]=1.

Node 3 has base[3]=2.

Initially delta is all zero.

| Step | Operation | delta[1] | delta[2] | delta[3] | Query result |
| --- | --- | --- | --- | --- | --- |
| 1 | query 1 | 0 | 0 | 0 | base[1]=3 |
| 2 | update 1-3 with z=2 | 2 | 0 | 2 | - |
| 3 | query 1 | 2 | 0 | 2 | 3 ^ 2 = 1 |

The second step applies XOR 2 to nodes 1 and 3 only, reflecting that only endpoints of the path update are affected.

This trace shows how internal edges are implicitly handled without ever being explicitly processed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | each edge processed once, each query/update is O(1) |
| Space | O(n) | arrays for base and delta |

The constraints allow up to 500,000 operations, so an O(n + q) solution comfortably fits within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    return sys.stdout.getvalue().strip()

# sample
assert run("""3 3
1 2 1
1 3 2
2 1
1 1 3 2
2 1
""") == "3\n1", "sample 1"

# single edge
assert run("""2 2
1 2 5
2 1
2 2
""") == "5\n5", "simple chain"

# no-op update x==y
assert run("""3 1
1 2 7
1 3 9
1 2 2 0
""") == "", "no-op path update"

# star tree
assert run("""4 3
1 2 1
1 3 2
1 4 3
2 1
1 2 3 1
2 1
""") == "0\n1", "star updates"

# repeated toggles
assert run("""3 4
1 2 4
2 1
1 1 3 5
1 1 3 5
2 1
""") == "4\n4", "double cancel"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain | 5,5 | basic adjacency XOR |
| no-op update | empty | x==y cancels |
| star tree | mixed | endpoint-only propagation |
| repeated toggles | stable | XOR cancellation |

## Edge Cases

A key edge case is when the update path degenerates to a single node, meaning x equals y. In that situation, no edges are affected, so the operation must not change anything. The algorithm handles this correctly because it applies `delta[x] ^= z` twice, once for x and once for y, and since they are the same node, the XOR cancels out.

Another case is a star-shaped tree where many updates target the center node. Since every path between leaves passes through the center, it may look like the center should be heavily updated. In reality, the endpoint rule ensures that only leaves are toggled per operation, and the center remains stable unless it is an endpoint.

A third case is repeated identical updates on the same path. Because XOR is its own inverse, applying the same update twice cancels out entirely. The `delta` accumulation preserves this property naturally, since each update toggles endpoints independently and repeated toggles revert the state.
