---
title: "CF 104786B - John and tree game"
description: "We are given a tree with (N) nodes. John wants to select disjoint pairs of nodes, with the restriction that a pair is valid only if the distance between the two nodes along the tree is even."
date: "2026-06-28T14:36:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104786
codeforces_index: "B"
codeforces_contest_name: "FIICode2023Round1"
rating: 0
weight: 104786
solve_time_s: 81
verified: true
draft: false
---

[CF 104786B - John and tree game](https://codeforces.com/problemset/problem/104786/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree with \(N\) nodes. John wants to select disjoint pairs of nodes, with the restriction that a pair is valid only if the distance between the two nodes along the tree is even. Every node can appear in at most one chosen pair, and the goal is to use every node exactly once in some pair.

The question is simply whether a perfect pairing exists under this rule.

The constraint \(N \le 5 \cdot 10^5\) rules out anything that tries to test pairs explicitly or searches over matchings. A quadratic check over all node pairs would already require about \(10^{11}\) operations in the worst case, which is far beyond the time limit. Even cubic or flow-based approaches are unnecessary and would be too slow or overkill for what turns out to be a structural observation about trees.

A subtle issue appears if one tries to reason locally. For example, it is tempting to think that since we can pair nodes at even distance, we might need to carefully construct paths or match nodes greedily by distance. That fails because distance is not independent per pair; pairing one node changes availability of others.

Consider a simple path of three nodes:
```
1 - 2 - 3
```
Valid even-distance pairs are (1,3). Node 2 cannot be paired with either endpoint, so the correct answer is NO. A naive greedy attempt might pair (1,2) or (2,3), but those pairs are invalid because their distances are 1.

Another example:
```
1 - 2 - 3 - 4
```
Here (1,3) and (2,4) are valid, so a full pairing exists. Any method that does not recognize the global structure of parity will struggle to consistently distinguish these cases.

## Approaches

The key observation is that in a tree, parity of distance is completely determined by bipartite coloring. If we root the tree anywhere, every node gets a depth, and the parity of the distance between two nodes equals the XOR of their depth parities. This means two nodes have even distance if and only if they lie on the same side of the bipartition.

So the problem stops being about geometry of paths and becomes about grouping nodes by parity of depth. Every valid pair must be formed inside one of these two groups.

A brute-force approach would compute all-pairs shortest paths or check every possible pairing of nodes, verifying constraints and trying to build a perfect matching. Even if we assume a clever matching routine, the structure is still overkill since the only constraint is “same parity group”. The bottleneck is not correctness but combinatorial explosion: pairing decisions grow factorially.

Once we reduce the problem to bipartite coloring, the remaining question is whether each color class can be fully partitioned into pairs. A set can be partitioned into disjoint pairs if and only if its size is even. Since pairs never cross between color classes, each side must independently have even cardinality.

This reduces the entire tree problem to a single DFS coloring and two parity checks.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute force pairing search | exponential | O(N) | Too slow |
| BFS/DFS bipartite coloring + parity check | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Root the tree at any node, for convenience node 1. Run a DFS or BFS to compute the parity of depth for every node. This assigns each node to one of two groups, depending on whether its distance from the root is even or odd.

2. Maintain two counters, one for each parity group.

3. While traversing the tree, increment the counter corresponding to each node’s parity.

4. After traversal finishes, check whether both counters are even. If either counter is odd, return NO immediately because that group cannot be fully split into pairs.

5. If both counters are even, return YES since we can pair nodes arbitrarily within each group.

The important hidden step is recognizing that once nodes are partitioned by parity, there are no further structural constraints. Any two nodes in the same parity class have an even distance in a tree, so every pairing inside a class is valid.

### Why it works

A tree is bipartite, so every edge connects opposite parity nodes in a rooted traversal. This implies that the parity of the path length between two nodes depends only on whether their depths share the same parity. Thus, the allowed pairing relation becomes exactly “same color in bipartite coloring”.

Inside each color class, the induced restriction graph is complete: every pair is valid. Therefore the only condition for a perfect pairing is that each class has an even number of nodes, since pairing reduces the count by two each time and no cross-class pairing is allowed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    g = [[] for _ in range(n + 1)]
    
    for _ in range(n - 1):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)
    
    color = [-1] * (n + 1)
    stack = [(1, 0)]
    color[1] = 0
    
    cnt = [0, 0]
    
    while stack:
        u, c = stack.pop()
        color[u] = c
        cnt[c] += 1
        
        for v in g[u]:
            if color[v] == -1:
                stack.append((v, c ^ 1))
    
    if cnt[0] % 2 == 0 and cnt[1] % 2 == 0:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()
```

The solution builds the tree adjacency list and performs an iterative DFS to avoid recursion depth issues given \(N\) up to \(5 \cdot 10^5\). The coloring uses a simple XOR flip to alternate parity between parent and child.

The counters `cnt[0]` and `cnt[1]` accumulate the size of each bipartite side. The final condition directly implements the requirement that each side must be perfectly pairable internally.

## Worked Examples

### Example 1
Input:
```
3
2 1
3 2
```

We root at 1.

| Node | Parent | Parity (color) | cnt[0] | cnt[1] |
|------|--------|----------------|--------|--------|
| 1 | - | 0 | 1 | 0 |
| 2 | 1 | 1 | 1 | 1 |
| 3 | 2 | 0 | 2 | 1 |

Final counts are \(cnt[0]=2\), \(cnt[1]=1\). One group has odd size, so pairing is impossible.

This matches the fact that node 2 becomes stranded because it lies in a singleton parity class.

Output:
```
NO
```

### Example 2
Input:
```
6
4 2
6 5
3 5
5 1
4 5
```

Root at 1.

| Node | Parity | cnt[0] | cnt[1] |
|------|--------|--------|--------|
| 1 | 0 | 1 | 0 |
| 5 | 1 | 1 | 1 |
| 6 | 0 | 2 | 1 |
| 3 | 0 | 3 | 1 |
| 4 | 0 | 4 | 1 |
| 2 | 1 | 4 | 2 |

Final counts: \(cnt[0]=4\), \(cnt[1]=2\), both even.

We can pair within each group, and since every same-parity pair has even distance, a full pairing exists.

Output:
```
YES
```

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(N) | Each node and edge is processed once during DFS traversal |
| Space | O(N) | Adjacency list and color array store linear information |

The linear complexity is sufficient for \(N \le 5 \cdot 10^5\), and memory usage fits easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    def solve():
        n = int(input())
        g = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            u, v = map(int, input().split())
            g[u].append(v)
            g[v].append(u)

        color = [-1] * (n + 1)
        stack = [(1, 0)]
        color[1] = 0
        cnt = [0, 0]

        while stack:
            u, c = stack.pop()
            color[u] = c
            cnt[c] += 1
            for v in g[u]:
                if color[v] == -1:
                    stack.append((v, c ^ 1))

        return "YES" if cnt[0] % 2 == 0 and cnt[1] % 2 == 0 else "NO"

    return solve()

# provided samples
assert run("3\n2 1\n3 2\n") == "NO"
assert run("6\n4 2\n6 5\n3 5\n5 1\n4 5\n") == "YES"

# single node
assert run("1\n") == "NO"

# simple even path
assert run("4\n1 2\n2 3\n3 4\n") == "YES"

# star tree (impossible)
assert run("5\n1 2\n1 3\n1 4\n1 5\n") == "NO"

# balanced binary-like
assert run("7\n1 2\n1 3\n2 4\n2 5\n3 6\n3 7\n") == "NO"
```

| Test input | Expected output | What it validates |
|---|---|---|
| 1 node | NO | minimal edge case |
| 4-line path | YES | even chain pairing |
| star tree | NO | skewed parity imbalance |
| full binary tree | NO | non-trivial parity mismatch |

## Edge Cases

For \(N=1\), the DFS assigns a single node to one parity class of size 1. Since pairing requires groups of even size, the algorithm returns NO immediately.

For a path of four nodes \(1-2-3-4\), the coloring produces two nodes in each parity class. Both counts are even, and the algorithm outputs YES. This matches the valid pairing (1,3) and (2,4), confirming that no structural constraints beyond parity exist.

For a star-shaped tree, the center has one parity and all leaves share the opposite parity. If the number of leaves is odd, one class becomes odd-sized and the algorithm correctly rejects the case, since one leaf would remain unmatched regardless of pairing strategy.
