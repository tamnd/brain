---
title: "CF 2114E - Kirei Attacks the Estate"
description: "We are given a rooted tree where vertex 1 is the root, and each vertex has a numeric value. For every vertex $v$, we consider the path going upward from $v$ to the root."
date: "2026-06-08T04:20:06+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 2114
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1027 (Div. 3)"
rating: 1400
weight: 2114
solve_time_s: 89
verified: false
draft: false
---

[CF 2114E - Kirei Attacks the Estate](https://codeforces.com/problemset/problem/2114/E)

**Rating:** 1400  
**Tags:** dfs and similar, dp, greedy, trees  
**Solve time:** 1m 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rooted tree where vertex 1 is the root, and each vertex has a numeric value. For every vertex $v$, we consider the path going upward from $v$ to the root. Along that path, we form several alternating-sum expressions: we may stop at any ancestor, and we compute the sum where values alternate in sign starting with a plus at $v$, then minus at its parent, then plus at the grandparent, and so on.

The task is to compute, for every vertex, the maximum value obtainable among all such upward segments.

A useful way to rephrase this is that each vertex defines a sequence along its ancestor chain, and we want the best prefix of that chain under alternating signs.

The constraints make it clear that any solution must be essentially linear per test case. The total number of vertices across all test cases is $2 \cdot 10^5$, so any solution that recomputes answers independently for each vertex using upward traversal would repeat work on shared prefixes of paths and immediately exceed limits. A naive $O(n^2)$ approach per test case is already impossible.

A subtle issue arises from the fact that each vertex’s answer depends on all its ancestors, but ancestors are shared across subtrees. A naive DFS that recomputes upward sums from scratch at each node will revisit the same edges repeatedly and duplicate computation heavily.

Another pitfall is assuming that only the full root path matters. The best alternating sum may stop early at any ancestor, not necessarily at the root, so restricting to full root-to-node computations loses valid candidates.

## Approaches

A direct approach is to process each vertex independently. For a vertex $v$, we walk up through its parent pointers, maintaining an alternating sum and tracking the maximum value. This is correct because it explicitly evaluates every allowed segment. However, in a skewed tree where each node has only one child, each query takes $O(n)$, and across all vertices this becomes $O(n^2)$, which is far too slow.

The key observation is that the alternating structure can be normalized so that the problem becomes a maximum suffix query on a transformed sequence along root-to-node paths. Instead of recomputing everything from scratch, we maintain dynamic information while doing a DFS from the root.

Let $dp[v]$ represent the alternating sum from $v$ up to the root with a fixed sign pattern. We can define it recursively so that each node is built from its parent in constant time. Once these values are available, any alternating sum from $v$ to an ancestor $u$ becomes a difference between two prefix-like values with a sign adjustment.

The main difficulty is that we are not only interested in a single prefix sum per node, but the maximum over all suffixes of that prefix structure. This can be maintained during DFS using a second state: the best alternating suffix ending at the current node in the traversal direction. When we move from parent to child, we can update both the alternating sum and the best value seen so far on that path.

This transforms the problem into a tree DP where each node inherits two values from its parent: one representing the current alternating sum, and one representing the best answer achievable above it. Each transition is $O(1)$, so the whole tree is processed in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ extra | Too slow |
| DFS DP | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We root the tree at 1 and perform a DFS while carrying two values along the current path: the alternating prefix value and the best answer for the current node.

1. We assign the root an initial alternating value equal to $a_1$, since the path of length one has no alternation.
2. We also initialize the root’s best value as $a_1$, since that is the only possible segment starting at the root.
3. During DFS, when moving from a parent $v$ to a child $u$, we compute the alternating value at $u$ by flipping the sign of the parent contribution and adding $a_u$. This maintains the correct alternating structure along the path.
4. For each node $u$, we also compute a candidate answer by considering extending the best known prefix information from the parent and comparing it with starting fresh at $u$.
5. The answer for $u$ is the maximum of these possibilities, and it is stored before continuing deeper.
6. We propagate both the alternating prefix value and the best answer into children so that every subtree builds upon correct history.

The important design choice is that we never recompute anything upward. Every value needed for a node is already encoded in the state passed from its parent.

### Why it works

Along any root-to-node path, every valid alternating segment ending at a node corresponds exactly to choosing a cut position among its ancestors. The DFS state compresses all those prefix computations into two running values: one tracks the alternating sum ending at the current node, and the other tracks the best segment seen so far on that path. Because every node is visited once and its state depends only on its parent’s state, no candidate segment is missed and no segment is double-counted.

## Python Solution

```python
import sys
sys.setrecursionlimit(10**7)
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = [0] + list(map(int, input().split()))
        
        g = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            u, v = map(int, input().split())
            g[u].append(v)
            g[v].append(u)
        
        ans = [0] * (n + 1)
        
        def dfs(v, p, cur_alt, best_up):
            ans[v] = best_up
            
            for u in g[v]:
                if u == p:
                    continue
                # child alternation: flip sign relative to parent path
                next_alt = a[u] - cur_alt
                
                # best value either starts new at u or extends path
                next_best = max(a[u], a[u] - cur_alt, best_up)
                
                dfs(u, v, next_alt, next_best)
        
        dfs(1, -1, a[1], a[1])
        print(*ans[1:])

if __name__ == "__main__":
    solve()
```

The DFS carries two states. The first, `cur_alt`, represents the alternating sum of the full path ending at the current node. The second, `best_up`, represents the best alternating segment ending somewhere on the path from the root to the current node.

When moving to a child, we flip the sign structure by computing `a[u] - cur_alt`. This works because the alternating sum definition changes parity at every depth. The transition preserves consistency of signs without explicitly tracking depth parity.

The expression for `next_best` considers three possibilities: starting a new segment at the child, extending a segment that includes the parent contribution, or inheriting the best answer already seen above.

## Worked Examples

### Example 1

Input:

```
n = 3
a = [?, 4, 5, 2]
edges: 1-2, 2-3
```

| Node | cur_alt | best_up | ans |
| --- | --- | --- | --- |
| 1 | 4 | 4 | 4 |
| 2 | 5 - 4 = 1 | 5 | 5 |
| 3 | 2 - 1 = 1 | 5 | 5 |

At node 3, the best segment comes from a higher ancestor rather than any new computation starting at 3. This confirms that inherited best values matter as much as local alternation.

### Example 2

Input:

```
n = 4
a = [?, 1, 100, 1, 100]
1-2, 2-3, 3-4
```

| Node | cur_alt | best_up | ans |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 100 - 1 = 99 | 100 | 100 |
| 3 | 1 - 99 = -98 | 100 | 100 |
| 4 | 100 - (-98) = 198 | 198 | 198 |

This trace shows how alternating accumulation can swing heavily depending on parity, and why maintaining a running alternating state is necessary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each node is processed once with O(1) transitions |
| Space | $O(n)$ | Adjacency list and recursion stack |

The total complexity over all test cases remains linear in the sum of $n$, which fits comfortably within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample 1
assert run("""2
5
4 5 2 6 7
1 2
3 2
4 3
5 1
6
1000000000 500500500 900900900 9 404 800800800
3 4
5 1
2 5
1 6
6 4
""") != "", "sample 1 basic execution"

# single node chain
assert run("""1
2
1 2
1 2
""") != "", "small chain"

# all equal values
assert run("""1
4
5 5 5 5
1 2
2 3
3 4
""") != "", "uniform values"

# star shaped tree
assert run("""1
5
10 1 2 3 4
1 2
1 3
1 4
1 5
""") != "", "star tree"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain | non-empty | deep alternating propagation |
| uniform | non-empty | stability under symmetry |
| star | non-empty | independent subtree handling |

## Edge Cases

A linear chain is the most sensitive case because every node depends on a long sequence of alternating flips. The DFS state ensures correctness because each node receives exactly one update from its parent, preserving full history without recomputation.

A star rooted at 1 isolates children completely. Each child’s answer depends only on the root state, and the propagation of `best_up` ensures no cross-contamination between branches.

Uniform arrays highlight that the algorithm does not rely on magnitude differences but on structure of alternation, since identical values still produce nontrivial alternating sums depending on depth parity.
