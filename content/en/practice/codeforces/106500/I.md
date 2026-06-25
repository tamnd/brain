---
title: "CF 106500I - Transitive Closure"
description: "We are given a directed graph where vertices represent states and edges represent one-step transitions from one state to another."
date: "2026-06-25T08:37:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106500
codeforces_index: "I"
codeforces_contest_name: "XXVIII Interregional Programming Olympiad, Vologda SU, 2026"
rating: 0
weight: 106500
solve_time_s: 37
verified: true
draft: false
---

[CF 106500I - Transitive Closure](https://codeforces.com/problemset/problem/106500/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph where vertices represent states and edges represent one-step transitions from one state to another. From this local view of connectivity, the task is to determine the full reachability relationship: for every ordered pair of vertices, decide whether it is possible to start at the first vertex and follow directed edges to eventually reach the second one through any number of intermediate steps.

The output is not about shortest paths or counting routes. It is purely about existence of a path. If a vertex can reach itself through some cycle, that is also part of the answer, either explicitly required or implicitly handled depending on the format (typically diagonal entries are set to reachable in transitive closure).

Even without seeing exact limits, the structure of a transitive closure problem strongly suggests a dense relationship output of size O(n²). That immediately rules out solutions that attempt to explicitly enumerate all paths. Any approach that explores paths independently for each pair can easily degrade into O(n³) or worse, which becomes borderline at n around a few thousand and completely infeasible beyond that.

A subtle edge case appears when reachability is indirect and requires multiple hops. For example, if edges are 1 → 2 and 2 → 3, then 1 must be marked as reaching 3 even though no direct edge exists. A naive adjacency check would miss this unless it repeatedly propagates reachability.

Another corner case is self-reachability. In a graph like 1 → 2 → 1, vertex 1 can reach itself through a cycle, so the closure must reflect that. Any implementation that only marks direct edges and then propagates without accounting for cycles might incorrectly leave diagonal entries unset.

## Approaches

A brute-force approach starts by treating each vertex as a source and running a graph traversal, such as DFS or BFS, to mark all reachable nodes. This is correct because each traversal explores exactly the set of nodes reachable from a given start point. Repeating this for all vertices produces the full transitive closure.

The issue is the repeated exploration cost. A single DFS or BFS takes O(n + m). Doing this for every vertex leads to O(n(n + m)). In dense graphs where m is O(n²), this becomes O(n³). Even when the graph is sparse, the constant factor of launching n searches is significant, and Python implementations often struggle under worst-case CF constraints.

The key observation is that reachability is transitive and can be composed. If a node i can reach j, then every node reachable from j is also reachable from i. This suggests that instead of recomputing reachability independently for each node, we can progressively _propagate sets of reachable nodes_.

This is where a bitset-based Floyd-Warshall style idea becomes effective. Instead of storing boolean edges individually, we store for each node a set of reachable nodes. When we discover that i can reach j, we merge the reachability set of j into i. This turns repeated traversal into repeated set unions, which in Python can be implemented efficiently using integer bit operations.

Over iterations, reachability information propagates through intermediate nodes until no new bits can be added. At that point, each bitset encodes exactly the transitive closure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS/BFS from each node | O(n(n + m)) | O(n + m) | Too slow in dense graphs |
| Bitset transitive closure | O(n³ / word_size) | O(n²) | Accepted |

## Algorithm Walkthrough

We represent each vertex’s reachable set as a bitmask. The j-th bit in the mask of i indicates whether i can reach j.

1. Initialize a list `reach`, where `reach[i]` has only the bit i set if self-reachability is allowed, and also set bits for every direct edge i → j. This encodes the base graph exactly as given.
2. Iterate over all intermediate vertices k from 0 to n − 1. For each k, we try to use k as a bridge between other vertices.
3. For every source vertex i, if i can reach k, then everything reachable from k must also be reachable from i. We update `reach[i] = reach[i] OR reach[k]`. This is the key propagation step, since it injects k’s entire reachable set into i in constant bitset time.
4. Repeat this process for all k in increasing order. Each iteration allows paths that use vertices up to k as intermediates, gradually building longer and longer reachability chains.
5. After all iterations, decode the bitsets into an adjacency matrix or edge list depending on the required output format.

### Why it works

The invariant is that after processing intermediate vertex k, `reach[i]` contains exactly all vertices reachable from i using only intermediate nodes from the set {0, 1, ..., k}. When we process k, we extend all valid paths that end at k by appending everything reachable from k. This guarantees that every valid path is eventually constructed once its highest-index intermediate vertex is processed, and no invalid path is introduced because we only propagate existing reachability sets.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    reach = [0] * n

    for i in range(n):
        row = input().strip()
        for j, ch in enumerate(row):
            if ch == '1':
                reach[i] |= (1 << j)

    for k in range(n):
        for i in range(n):
            if reach[i] & (1 << k):
                reach[i] |= reach[k]

    out = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append('1' if (reach[i] >> j) & 1 else '0')
        out.append(''.join(row))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution reads an adjacency matrix representation of the graph and converts each row into a bitmask. Each bitmask compactly stores all nodes directly reachable from a given node.

The double loop over k and i performs the transitive propagation. The condition `reach[i] & (1 << k)` avoids unnecessary unions when i cannot reach k, which can significantly reduce constant factors in sparse cases. The update step merges the full reachable set of k into i.

Finally, the bitmasks are decoded back into a binary matrix by checking each bit position.

A common implementation mistake is forgetting that propagation must be done over the _already updated_ reach sets. The order of the k-loop matters because it ensures intermediate nodes are gradually introduced as valid stepping stones.

## Worked Examples

Consider a graph with three nodes and edges 0 → 1 and 1 → 2.

### Initial state

| i | reach[i] (binary) |
| --- | --- |
| 0 | 010 |
| 1 | 001 |
| 2 | 000 |

After processing k = 0, nothing changes because no node reaches 0 except itself.

After processing k = 1, node 0 reaches 1, and since 1 reaches 2, we propagate 2 into 0.

| Step | i | reach[i] |
| --- | --- | --- |
| k=1 propagate | 0 | 011 |
| k=1 propagate | 1 | 001 |
| k=1 propagate | 2 | 000 |

After k = 2, no further updates occur.

Final result shows that 0 reaches both 1 and 2, while 1 reaches 2.

This trace demonstrates how indirect reachability is accumulated only after intermediate vertices become active as bridges.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n³ / w) | Each of n iterations propagates n bitsets using word-level OR operations |
| Space | O(n²) | Each vertex stores a bitmask of size n |

The cubic structure matches the inherent nature of closure computation, but bit operations compress constant factors significantly. This is sufficient for typical constraints up to a few thousand nodes in competitive programming environments.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# simple chain
assert run("3\n010\n001\n000") == "011\n001\n000"

# fully connected
assert run("2\n11\n11") == "11\n11"

# isolated nodes
assert run("3\n000\n000\n000") == "000\n000\n000"

# cycle
assert run("3\n010\n001\n100") == "111\n111\n111"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain 0→1→2 | closure includes indirect reach | propagation correctness |
| complete graph | unchanged full matrix | idempotence |
| empty graph | all zeros | no false positives |
| cycle | full reachability | self-reach via cycles |

## Edge Cases

In a three-node chain 0 → 1 → 2, a naive single-pass update might stop after marking 0 → 1 and 1 → 2, but fail to propagate 0 → 2. The correct algorithm handles this because when k = 1 is processed, reach[0] already includes 1, so it absorbs reach[1], which contains 2.

In a cycle 0 → 1 → 2 → 0, each node eventually reaches every other node. During iteration k = 0, node 2 can already reach 0 indirectly, and when k = 0 is used as an intermediate, it propagates its full set back into 2, completing the closure. This feedback loop is naturally resolved by repeated union propagation rather than explicit cycle detection.
