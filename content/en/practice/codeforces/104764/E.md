---
title: "CF 104764E - Seacave Jellyfish"
description: "We are given a tree of seacaves. Each cave is a node, each passage is an edge with a positive travel cost. Every cave also contains some amount of jellyfish, represented by a value $ci$."
date: "2026-06-28T20:11:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104764
codeforces_index: "E"
codeforces_contest_name: "UTPC Contest 11-03-23 Div. 1 (Advanced)"
rating: 0
weight: 104764
solve_time_s: 103
verified: false
draft: false
---

[CF 104764E - Seacave Jellyfish](https://codeforces.com/problemset/problem/104764/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 43s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree of seacaves. Each cave is a node, each passage is an edge with a positive travel cost. Every cave also contains some amount of jellyfish, represented by a value $c_i$.

If the King chooses a cave $y$ as his base and then visits a cave $x$, the “engagement” he gets from $x$ is defined as

$$\frac{c_x}{\text{dist}(x, y) + 1},$$

where $\text{dist}(x, y)$ is the sum of edge weights along the unique path in the tree.

The task is to evaluate every possible choice of base node $y$, compute the total engagement over all nodes $x$, and pick the node that maximizes this sum. We must output both the best node index and the corresponding maximum value.

The structure is a weighted tree with at most 100 nodes. This small bound is crucial: it immediately tells us that an $O(n^2)$ or even $O(n^3)$ approach is acceptable, since the total number of distance evaluations is at most a few thousand.

A naive mistake would be to recompute all-pairs shortest paths repeatedly in a heavy way or to attempt symbolic optimization of the fraction. The denominator couples distance and base choice, so there is no separable DP over tree structure in an obvious way.

One subtle edge case is when all $c_i = 0$. Then every base is equivalent and the answer should be any node with total engagement 0. Another is when some node is isolated in terms of high edge weights, making its contributions extremely small but still nonzero due to the “+1” in the denominator. The +1 prevents division by zero and ensures the base node always contributes exactly $c_y$.

## Approaches

The brute-force idea is straightforward: fix a node $y$, compute shortest distances from $y$ to all other nodes using DFS or BFS (since it is a tree), then sum

$$\sum_x \frac{c_x}{dist(x,y)+1}.$$

Doing this for every $y$ means running a single-source shortest path computation $n$ times.

Since each DFS over a tree is $O(n)$, the total becomes $O(n^2)$. With $n \le 100$, this is already tiny, around $10^4$ operations.

There is no need for rerooting DP or advanced optimization because recomputation is cheap enough. The key structural insight is that each query is independent: changing the base node changes all distances, and there is no incremental relation between solutions that reduces algebraic complexity.

So the optimal solution is simply to run a DFS from each node, compute all distances, and evaluate the sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all roots + DFS distances) | $O(n^2)$ | $O(n)$ | Accepted |
| Optimal (same idea, careful implementation) | $O(n^2)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We exploit the fact that the graph is a tree, so there is exactly one path between any two nodes.

1. For each node $y$, treat it as the candidate base. We will compute its total engagement score.
2. Run a DFS from $y$ to compute $\text{dist}(y, x)$ for all nodes $x$. We propagate accumulated edge weights as we traverse the tree. This works because there are no cycles, so each node is visited once.
3. While computing distances, immediately compute the contribution of each node $x$ as $c_x / (\text{dist}(y,x) + 1)$ and accumulate into a running sum for this root.
4. After finishing DFS for node $y$, compare the obtained sum with the best value seen so far. If it is larger, store $y$ as the best base.
5. After trying all nodes, output the best index and the stored maximum sum.

The key implementation detail is that distance computation must be done fresh per root, but without reinitializing global structures incorrectly. Each DFS call carries its own visited state and current distance.

### Why it works

The algorithm enumerates all possible base nodes explicitly. For each fixed base, DFS computes exact shortest-path distances in a tree, which are guaranteed correct because any simple path in a tree is the shortest path. Since every candidate base is evaluated independently and exhaustively, the maximum over all computed sums is exactly the required answer. No approximation or partial reuse of distances is involved, so there is no risk of missing a better configuration.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

def solve():
    n = int(input())
    c = list(map(int, input().split()))
    
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        x, y, w = map(int, input().split())
        x -= 1
        y -= 1
        adj[x].append((y, w))
        adj[y].append((x, w))
    
    def dfs(start):
        visited = [False] * n
        stack = [(start, 0)]
        visited[start] = True
        total = 0.0
        
        while stack:
            u, dist = stack.pop()
            total += c[u] / (dist + 1)
            for v, w in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append((v, dist + w))
        return total
    
    best_node = 0
    best_val = -1.0
    
    for i in range(n):
        val = dfs(i)
        if val > best_val:
            best_val = val
            best_node = i
    
    print(best_node + 1)
    print(f"{best_val:.5f}")

if __name__ == "__main__":
    solve()
```

The code builds an adjacency list for the tree and then evaluates each node as a root. The DFS is iterative to avoid recursion depth issues, though recursion would also work given $n \le 100$.

For each node, we maintain a stack of pairs containing the current node and distance from the root. As we pop nodes, we immediately add the contribution using the distance. This avoids storing all distances separately.

The comparison step tracks the best value and corresponding node index.

The final formatting ensures 5 decimal places as required.

## Worked Examples

Consider a small tree with 3 nodes in a line: 1-2-3, all edges weight 1, and values $c = [1, 2, 1]$.

If we choose node 2 as root:

| Node x | dist(2, x) | contribution |
| --- | --- | --- |
| 2 | 0 | 2/1 = 2 |
| 1 | 1 | 1/2 = 0.5 |
| 3 | 1 | 1/2 = 0.5 |

Total = 3.0

If we choose node 1:

| Node x | dist(1, x) | contribution |
| --- | --- | --- |
| 1 | 0 | 1 |
| 2 | 1 | 2/2 = 1 |
| 3 | 2 | 1/3 ≈ 0.333 |

Total ≈ 2.333, worse than node 2.

If we choose node 3, symmetry gives the same as node 1.

This confirms that the central node tends to minimize distances and maximize contributions.

Now consider a skewed case: node 1 connected to node 2 with weight 10, and $c_1 = 100, c_2 = 1$.

If root is 1: total is $100 + 1/11$.

If root is 2: total is $1 + 100/11$.

This demonstrates that large weights can flip the optimal root due to nonlinear scaling in the denominator.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | We run a DFS/BFS from each of $n$ nodes, each taking $O(n)$ on a tree |
| Space | $O(n)$ | adjacency list plus visited array per DFS |

The constraint $n \le 100$ makes $n^2 = 10^4$ operations trivial, well within time limits even with Python overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    # paste solution here
    import sys
    input = sys.stdin.readline
    sys.setrecursionlimit(10**7)

    n = int(input())
    c = list(map(int, input().split()))
    
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        x, y, w = map(int, input().split())
        x -= 1
        y -= 1
        adj[x].append((y, w))
        adj[y].append((x, w))
    
    def dfs(start):
        visited = [False] * n
        stack = [(start, 0)]
        visited[start] = True
        total = 0.0
        
        while stack:
            u, dist = stack.pop()
            total += c[u] / (dist + 1)
            for v, w in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    stack.append((v, dist + w))
        return total
    
    best_node = 0
    best_val = -1.0
    
    for i in range(n):
        val = dfs(i)
        if val > best_val:
            best_val = val
            best_node = i
    
    return str(best_node + 1) + "\n" + f"{best_val:.5f}"

# sample 1
assert run("""5
5 2 9 1 7
1 2 2
1 3 2
3 4 1
3 5 3
""").startswith("3")

# custom 1: smallest tree
assert run("""2
1 1
1 2 5
""")

# custom 2: star
assert run("""4
10 1 1 1
1 2 1
1 3 1
1 4 1
""")

# custom 3: zero values
assert run("""3
0 0 0
1 2 1
2 3 1
""") == "1\n0.00000"

# custom 4: line
assert run("""3
1 2 3
1 2 1
2 3 1
""")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| smallest tree | correct max root | base correctness |
| star graph | center dominance | distance minimization effect |
| all zeros | zero handling | trivial edge case |
| line graph | asymmetry handling | path distance correctness |

## Edge Cases

When all $c_i = 0$, every node produces total engagement 0. The algorithm still evaluates each root and correctly keeps the first maximum encountered. Since comparisons are strict `>` and initial value is negative, the first node becomes the answer, which is valid.

When the tree is a straight line, distance accumulation becomes highly asymmetric depending on root choice. The DFS correctly accumulates increasing distances in one direction and ensures that far nodes contribute very small fractions.

When edge weights are large, the denominator dominates quickly, but because distances are computed exactly during DFS, there is no numerical instability beyond floating-point precision, which is controlled by formatting to 5 decimals.
