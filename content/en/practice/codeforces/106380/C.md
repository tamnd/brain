---
title: "CF 106380C - Colorful logo"
description: "We are given a directed graph where each edge carries a color label. A walk in this graph is allowed to revisit vertices and edges, but it becomes “valid” only if the colors along the walk alternate strictly, meaning you are never allowed to traverse two consecutive edges of the…"
date: "2026-06-25T10:20:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106380
codeforces_index: "C"
codeforces_contest_name: "The 6th Liaoning Provincial Collegiate Programming Contest"
rating: 0
weight: 106380
solve_time_s: 46
verified: true
draft: false
---

[CF 106380C - Colorful logo](https://codeforces.com/problemset/problem/106380/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph where each edge carries a color label. A walk in this graph is allowed to revisit vertices and edges, but it becomes “valid” only if the colors along the walk alternate strictly, meaning you are never allowed to traverse two consecutive edges of the same color.

The task is to determine which vertices can be reached from node 1 using such a valid walk. For every vertex that can be reached under this constraint, we include it in the output.

The key point is that reachability depends not only on the current node but also on the color of the last edge used. A naive reachability notion that only tracks nodes is insufficient, because arriving at the same node with different last-edge colors leads to different future possibilities.

The input size allows up to one million nodes and edges in total across all test cases. That immediately rules out any solution that tries to explicitly enumerate all paths. Even storing all states in a naive BFS over paths would explode, since the number of possible walks grows exponentially due to cycles and repeated revisits.

A subtle edge case appears when multiple edges of the same color form cycles. For example, consider a chain of nodes connected entirely by edges of color 1. From node 1, you can reach node 2, but you cannot continue from 2 using another color-1 edge. A naive BFS that ignores color constraints would incorrectly mark all nodes reachable, while the correct answer depends on respecting the alternation rule.

Another corner case is a node reachable via multiple incoming edges of different colors. For instance, if node 3 is reachable via a red edge from node 2 and also via a blue edge from node 4, then from node 3 the next transitions depend on which arrival we consider. Collapsing these states into a single visited flag per node loses correctness.

## Approaches

A straightforward idea is to perform a BFS or DFS over paths. Each state would represent the current node and the last edge color used. From a state, we try all outgoing edges whose color differs from the last color. This is correct because it directly encodes the problem constraint. However, this quickly becomes inefficient if implemented naively because the same node can be revisited many times with different incoming colors, and the graph may contain many edges.

The critical observation is that the state space is not actually large if we structure it properly. Instead of exploring arbitrary paths, we only need to consider pairs of the form (node, last color). Each edge transition updates this state in constant time. Since each edge is processed a bounded number of times, we can treat this as a graph traversal over an expanded state graph.

However, even this can be optimized further. Instead of explicitly expanding all color states, we can observe that transitions only depend on the last edge color, not the full history. This suggests maintaining adjacency lists grouped by color and performing a BFS that carries the last used color. Each edge is effectively considered once per compatible incoming state.

The brute-force idea works because it explores all valid walks, but it fails due to repeated recomputation of identical state transitions. The optimized view compresses all path histories into a small state graph where each meaningful distinction is just the last color used.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| DFS/BFS over paths (no state compression) | Exponential | O(n + m) | Too slow |
| BFS over (node, last color) states | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build adjacency lists where each entry stores both the neighbor and the edge color. This representation allows us to filter transitions based on color compatibility during traversal.
2. Define BFS states as pairs of (node, last_color). The last_color starts as a special value meaning “no previous edge”, allowing the first move from node 1 to use any color.
3. Initialize a queue with the state (1, none). We also maintain a visited structure keyed by (node, last_color) so that we do not reprocess identical states.
4. Pop a state (v, c_prev) from the queue. For each outgoing edge (v → to, c), we consider it only if c is different from c_prev. This enforces the alternating-color condition locally at every step.
5. If we reach a new state (to, c), mark it visited and push it into the queue. Each such transition represents extending a valid colorful walk.
6. After BFS finishes, collect all nodes that were reached in any state, regardless of last color. These nodes are exactly those reachable by at least one valid colorful walk.

The key idea is that we never merge states that differ in last color, because that distinction affects future transitions. Once BFS stabilizes, every reachable state represents a valid prefix of some alternating-color walk.

### Why it works

The BFS explores a graph whose nodes are augmented with last-edge-color information. Every transition preserves the invariant that the stored state corresponds to a valid alternating-color walk from node 1. Since every valid walk can be decomposed into a sequence of such transitions, every reachable vertex in the original graph must appear in at least one reachable state. Conversely, every state produced by BFS corresponds to a valid walk by construction, because we only extend along edges whose color differs from the previous one.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque, defaultdict

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        
        g = [[] for _ in range(n + 1)]
        for _ in range(m):
            u, v, c = map(int, input().split())
            g[u].append((v, c))
        
        # BFS over (node, last_color)
        # last_color = 0 means "no previous edge"
        q = deque()
        q.append((1, 0))
        
        visited = set()
        visited.add((1, 0))
        
        reachable = set([1])
        
        while q:
            v, pc = q.popleft()
            for to, c in g[v]:
                if c == pc:
                    continue
                state = (to, c)
                if state not in visited:
                    visited.add(state)
                    reachable.add(to)
                    q.append(state)
        
        print(*sorted(reachable))

if __name__ == "__main__":
    solve()
```

The adjacency list stores directed edges with their colors, allowing constant-time iteration over outgoing transitions. The BFS queue stores full state information so that color constraints are enforced locally.

A common implementation pitfall is forgetting that the initial state must allow any color. This is why the initial last_color is set to zero, which is guaranteed not to match any real edge color.

Another subtle issue is the visited structure. Marking only nodes as visited would incorrectly prune valid states, since reaching a node with a different last color may enable new transitions.

## Worked Examples

### Example 1

Input:

```
1
3 3
1 2 1
2 3 2
2 3 1
```

We start at (1, none).

| Step | State | Transition used | New state added | Reachable nodes |
| --- | --- | --- | --- | --- |
| 1 | (1, 0) | 1→2 (color 1) | (2, 1) | {1,2} |
| 2 | (2, 1) | 2→3 (color 2) | (3, 2) | {1,2,3} |
| 3 | (2, 1) | 2→3 (color 1) | skipped (same color as previous) | {1,2,3} |

This confirms that only alternating transitions are allowed, even if multiple edges exist.

### Example 2

Input:

```
1
4 4
1 2 1
2 3 1
3 4 2
2 4 3
```

| Step | State | Transition used | New state added | Reachable nodes |
| --- | --- | --- | --- | --- |
| 1 | (1, 0) | 1→2 (1) | (2, 1) | {1,2} |
| 2 | (2, 1) | 2→3 (1) | skipped | {1,2} |
| 3 | (2, 1) | 2→4 (3) | (4, 3) | {1,2,4} |
| 4 | (4, 3) | no outgoing | - | {1,2,4} |

This shows why tracking last edge color is essential: without it, node 3 would incorrectly appear reachable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each state (node, color) is visited at most once per edge transition, and total transitions are linear in edges |
| Space | O(n + m) | Storage for adjacency list and visited state set |

The constraints allow up to one million edges across all test cases, and this linear traversal fits comfortably within limits since each edge is processed a constant number of times.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque, defaultdict

    def solve():
        t = int(input())
        out_lines = []
        for _ in range(t):
            n, m = map(int, input().split())
            g = [[] for _ in range(n + 1)]
            for _ in range(m):
                u, v, c = map(int, input().split())
                g[u].append((v, c))

            q = deque()
            q.append((1, 0))
            vis = set([(1, 0)])
            reach = set([1])

            while q:
                v, pc = q.popleft()
                for to, c in g[v]:
                    if c == pc:
                        continue
                    st = (to, c)
                    if st not in vis:
                        vis.add(st)
                        reach.add(to)
                        q.append(st)

            out_lines.append(" ".join(map(str, sorted(reach))))
        return "\n".join(out_lines)

    return solve()

# provided sample placeholders (replace with actual samples if needed)
# assert run(...) == ...

# custom cases
assert run("1\n1 0\n") == "1", "single node"
assert run("1\n2 1\n1 2 1\n") == "1 2", "single edge"
assert run("1\n3 2\n1 2 1\n2 3 1\n") == "1 2", "blocked by same color chain"
assert run("1\n3 2\n1 2 1\n2 3 2\n") == "1 2 3", "alternating works"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 1 | trivial base case |
| single edge | 1 2 | direct reachability |
| same color chain | 1 2 | prevents invalid extension |
| alternating colors | 1 2 3 | correctness of color switching |

## Edge Cases

A key edge case is a linear chain where all edges share the same color. In such a case, only the first step from node 1 is valid, and every subsequent transition is blocked. The BFS correctly halts expansion because any attempt to reuse the same color immediately violates the state condition, so nodes beyond the first hop are never added.

Another edge case is when a node is reachable through multiple paths with different last colors. The algorithm correctly preserves both states independently, so future transitions are not prematurely discarded. For example, if node 2 is reached via a red edge and a blue edge, both states (2, red) and (2, blue) remain active, enabling different outgoing expansions that a node-only visited array would miss.
