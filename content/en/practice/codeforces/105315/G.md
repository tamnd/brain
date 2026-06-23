---
title: "CF 105315G - Nagham's Birthday"
description: "We are given a directed or undirected weighted graph for each test case, together with a designated start node and a target node."
date: "2026-06-23T15:06:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105315
codeforces_index: "G"
codeforces_contest_name: "JPC 4.0"
rating: 0
weight: 105315
solve_time_s: 55
verified: true
draft: false
---

[CF 105315G - Nagham's Birthday](https://codeforces.com/problemset/problem/105315/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed or undirected weighted graph for each test case, together with a designated start node and a target node. A route is any sequence of edges that connects the start to the target, and vertices and edges may repeat as long as they form a valid walk in the graph. The value of such a route is defined as the bitwise AND of all edge weights along that route. The task is to maximize this value among all possible valid routes from the start to the target.

The important structural detail is how bitwise AND behaves over paths. Once a bit becomes zero in any edge weight used along the route, that bit is permanently lost for the entire route value. So longer routes only restrict the final value, but they may still be useful because they allow us to reach edges that preserve more high bits.

The constraints imply we cannot enumerate paths. With up to 10^5 nodes and 3×10^5 edges per test case, any solution that depends on exploring all walks or even all simple paths is impossible. Even shortest-path style dynamic programming over subsets is out of reach. The only viable direction is to treat bits independently and reduce the problem to repeated reachability checks under edge filtering.

A subtle failure case appears if we assume the answer is simply the minimum edge weight along some shortest path or any shortest path. For example, consider a graph where a direct path from s to e exists with a low-weight edge, but a longer cycle allows a different path using only high-weight edges. A greedy shortest path approach would incorrectly pick the direct edge and produce a smaller AND value, even though a better AND-preserving route exists.

Another pitfall is assuming monotonicity in path length or edge weights. Adding edges does not necessarily decrease the AND in a predictable way unless we enforce a constraint on which bits are allowed. This is why the problem naturally turns into a bit filtering and connectivity problem rather than a classic shortest path.

## Approaches

The brute-force idea is to consider all possible walks from s to e and compute the bitwise AND of weights along each. This is correct because it explicitly evaluates every valid route. However, the number of walks grows exponentially because cycles can be traversed arbitrarily many times. Even restricting to simple paths does not help, since enumerating them in a dense graph is still exponential in the worst case.

The key observation is to flip the perspective. Instead of constructing paths, we decide which bits we want to keep in the final answer. Suppose we guess that a certain bit mask X is achievable. That means there exists a path from s to e such that every edge on that path has all bits of X set. In other words, all edges on the path belong to the subgraph formed by filtering edges whose weights contain X as a subset of bits. So feasibility reduces to a connectivity check in a filtered graph.

This leads to a greedy bit construction from the highest bit downward. We start with answer = 0. For each bit from most significant to least significant, we try to set it and test whether s and e are still connected using only edges whose weights contain all currently required bits. If connectivity holds, we keep the bit; otherwise we discard it.

The connectivity test can be done with DFS, BFS, or DSU over the filtered edges. Since we repeat this check for up to 60 bits, total complexity remains manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all walks) | Exponential | O(n + m) | Too slow |
| Bitwise greedy + connectivity checks | O(60 × (n + m)) | O(n + m) | Accepted |

## Algorithm Walkthrough

We maintain a candidate answer mask that we build bit by bit from high to low.

1. Initialize the answer mask to 0. This represents that we are initially allowing all paths, since no bit constraints are enforced yet.
2. Iterate over bits from 59 down to 0. We consider whether each bit can be included in the final answer.
3. For a given bit b, temporarily construct a test mask equal to current answer plus this bit.
4. Build or traverse a subgraph consisting only of edges whose weight contains all bits in the test mask. This filtering ensures that any path found in this graph will preserve all bits in the mask under bitwise AND.
5. Run a connectivity search (typically BFS or DFS) from s. If we can reach e, then there exists a valid route that preserves all bits in the test mask, so we permanently set this bit in the answer.
6. If e is not reachable, discard this bit and keep the previous answer unchanged.

The reason this greedy choice is valid is that higher bits dominate lower ones in binary representation. Once a higher bit is found infeasible, no later operation can restore it, so we safely discard it. Conversely, if a bit is feasible, keeping it never prevents us from potentially adding lower bits later, since lower bits only tighten the constraint further.

### Why it works

At any step, the current mask represents a set of edges that are all compatible with every bit already chosen. The connectivity check ensures that there exists at least one path fully contained in this constrained subgraph. Thus the invariant is that after processing bit b, there exists a path from s to e using only edges whose weights contain all selected bits. Since bit decisions only restrict the graph, once feasibility is confirmed, it remains consistent with all previously accepted bits.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m, s, e = map(int, input().split())
        
        edges = []
        adj_all = [[] for _ in range(n + 1)]
        
        for _ in range(m):
            a, b, w = map(int, input().split())
            edges.append((a, b, w))
            adj_all[a].append((b, w))
            adj_all[b].append((a, w))
        
        def can(mask):
            from collections import deque
            vis = [False] * (n + 1)
            dq = deque([s])
            vis[s] = True
            
            while dq:
                u = dq.popleft()
                if u == e:
                    return True
                for v, w in adj_all[u]:
                    if not vis[v] and (w & mask) == mask:
                        vis[v] = True
                        dq.append(v)
            return False
        
        ans = 0
        for bit in range(59, -1, -1):
            if can(ans | (1 << bit)):
                ans |= (1 << bit)
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation keeps a full adjacency list and performs a BFS for each bit trial. The key check `(w & mask) == mask` enforces that every edge used preserves all bits currently required in the answer.

The BFS is restarted for each bit, which is acceptable because the constraint on bits is small and the graph size is moderate. The correctness depends on not reusing visited state between different masks, since reachability changes with each added constraint.

## Worked Examples

Consider a small graph where multiple paths compete in preserving bits.

Input:

```
1
4 4 1 4
1 2 8
2 4 12
1 3 12
3 4 8
```

We evaluate bits from high to low.

| Bit | Trial mask | Reachable s→e | Decision | Current answer |
| --- | --- | --- | --- | --- |
| 3 (8) | 8 | yes via 1-2-4 | keep | 8 |
| 2 (4) | 12 | no | discard | 8 |
| 1 (2) | 10 | no | discard | 8 |
| 0 (1) | 9 | no | discard | 8 |

This demonstrates how the algorithm locks in the highest feasible bit first and avoids lower bits that would break connectivity.

A second example:

Input:

```
1
3 3 1 3
1 2 7
2 3 3
1 3 2
```

| Bit | Trial mask | Reachable s→e | Decision | Current answer |
| --- | --- | --- | --- | --- |
| 2 (4) | 4 | no | discard | 0 |
| 1 (2) | 2 | yes via 1-3 | keep | 2 |
| 0 (1) | 3 | no (edge 2-3 fails constraint) | discard | 2 |

The result shows that indirect paths can dominate direct edges when preserving higher bits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(60 × (n + m)) | Each bit triggers one BFS over the graph, scanning all edges once |
| Space | O(n + m) | Adjacency list plus BFS visited array |

The bounds of up to 3×10^5 edges and 60 bit checks yield around 1.8×10^7 edge relaxations per test case worst-case, which fits comfortably within typical limits in Python if implemented with adjacency lists and simple integer operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    def solve():
        input = sys.stdin.readline
        t = int(input())
        out = []
        for _ in range(t):
            n, m, s, e = map(int, input().split())
            adj = [[] for _ in range(n + 1)]
            for _ in range(m):
                a, b, w = map(int, input().split())
                adj[a].append((b, w))
                adj[b].append((a, w))
            
            from collections import deque
            
            def can(mask):
                vis = [False] * (n + 1)
                dq = deque([s])
                vis[s] = True
                while dq:
                    u = dq.popleft()
                    if u == e:
                        return True
                    for v, w in adj[u]:
                        if not vis[v] and (w & mask) == mask:
                            vis[v] = True
                            dq.append(v)
                return False
            
            ans = 0
            for bit in range(59, -1, -1):
                if can(ans | (1 << bit)):
                    ans |= (1 << bit)
            out.append(str(ans))
        return "\n".join(out)
    
    return solve()

# simple cases
assert run("1\n2 1 1 2\n1 2 7\n") == "7"
assert run("1\n2 1 1 2\n1 2 1\n") == "1"
assert run("1\n3 2 1 3\n1 2 6\n2 3 1\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single edge path | full edge weight | direct feasibility |
| Minimal bit case | 1 | single-bit correctness |
| Disconnected after filtering | 0 | unreachable under constraints |

## Edge Cases

One edge case occurs when the only available path requires relaxing high bits to maintain connectivity. Suppose a graph where s connects to e through a low-weight bridge, but high-weight edges form a cycle disconnected from e. The algorithm will correctly reject high bits because BFS under the constrained mask fails to reach the target, even though a visually longer path exists in the full graph.

Another case is when multiple components exist and connectivity depends on the exact mask. For example, edges might connect s to a mid component under mask X, but e only under a different subset of edges. The BFS recomputes reachability fresh for each mask, ensuring that stale reachability assumptions do not leak between bit trials.
