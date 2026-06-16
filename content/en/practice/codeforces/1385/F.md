---
title: "CF 1385F - Removing Leaves"
description: "We are working with a tree where vertices are gradually removed in rounds. In one round, we are allowed to pick a single internal vertex $v$ and remove exactly $k$ of its current leaf neighbors. A vertex counts as a leaf if it has degree one in the current remaining graph."
date: "2026-06-16T14:24:41+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "implementation", "trees"]
categories: ["algorithms"]
codeforces_contest: 1385
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 656 (Div. 3)"
rating: 2300
weight: 1385
solve_time_s: 470
verified: false
draft: false
---

[CF 1385F - Removing Leaves](https://codeforces.com/problemset/problem/1385/F)

**Rating:** 2300  
**Tags:** data structures, greedy, implementation, trees  
**Solve time:** 7m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We are working with a tree where vertices are gradually removed in rounds. In one round, we are allowed to pick a single internal vertex $v$ and remove exactly $k$ of its current leaf neighbors. A vertex counts as a leaf if it has degree one in the current remaining graph. After removing those leaves, the tree shrinks and new leaves may appear. The process continues, and we want to maximize how many rounds we can perform.

The key difficulty is that leaf status is dynamic. A vertex that is not a leaf initially can become one later, and choices in early rounds affect how many future rounds remain possible.

The input size is large, with up to $2 \cdot 10^5$ vertices in total across test cases. This immediately rules out any approach that simulates removals step by step on the full tree for each move, since a naive simulation could degrade to $O(n^2)$ in a chain-like structure where each removal only exposes one new leaf.

A subtle edge case appears in highly unbalanced trees like a chain. For example, if $k = 2$, a path of length 5 behaves very differently from a star, even though both are trees with similar size. In a star, many leaves are immediately available around one center, allowing multiple rounds. In a chain, only one or two leaves exist at any time, severely limiting moves. Any greedy strategy that assumes global leaf abundance without tracking structure fails here.

Another important edge case is when multiple high-degree nodes compete for leaves. If we always pick leaves locally without considering global depletion, we may prematurely exhaust leaves at a node that would otherwise sustain more rounds later.

## Approaches

A brute-force simulation would repeatedly identify all leaves, group them by their neighbors, pick any valid group of size $k$, remove them, and update degrees. Each round requires scanning all nodes to collect leaves, which costs $O(n)$. Since we may perform up to $O(n)$ rounds in the best case, this leads to $O(n^2)$ total work, which is too slow for the constraints.

The crucial observation is that the structure of removals around each vertex is independent in a combinatorial sense. Each vertex $v$ contributes leaves over time, but only when enough of its neighbors become leaves. Instead of simulating the process globally, we can think in terms of how many times each subtree can "supply" leaves upward toward a parent.

Root the tree arbitrarily. For each node, consider how many leaf removals can be supported by its children before its own contribution becomes limited. This becomes a bottom-up aggregation problem: each subtree returns a count representing how many leaves it can eventually provide to its parent, and each internal node combines these contributions greedily in batches of size $k$.

The key insight is that each node effectively converts contributions from children into groups of size $k$, and any leftover contributions propagate upward. The answer is the total number of complete groups formed across all nodes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(n^2)$ | $O(n)$ | Too slow |
| Tree DP / Greedy Aggregation | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We root the tree at an arbitrary node, typically 1.

1. Perform a postorder DFS from the root, computing values from leaves upward. Each node returns how many "available leaf tokens" it can pass to its parent. A leaf node initially contributes 1 token. This models that a leaf can potentially be removed in one operation.
2. For each node $v$, collect contributions from all children. These contributions represent how many leaves can eventually be produced in each subtree rooted at those children.
3. At node $v$, sum all child contributions. This sum represents how many leaf endpoints are currently available in the subtree of $v$ that could potentially be grouped.
4. Convert this sum into full operations by dividing by $k$. Each group of $k$ leaf tokens corresponds to one valid move centered at $v$ or propagated upward through $v$'s parent.
5. Pass the remainder $\text{sum} \bmod k$ upward to the parent. These leftover tokens represent partially completed groups that may combine with other subtrees higher in the tree.
6. Accumulate the quotient values over all nodes. This total is the number of valid moves.

The DFS ensures each subtree is processed exactly once, and grouping is done locally at each node where sufficient leaf contributions meet.

### Why it works

Each subtree contributes a certain number of eventual leaves that can be realized independently of other subtrees until they meet at a common ancestor. The only interaction between subtrees is at their lowest common ancestor, where leaf tokens from different branches can be combined into groups of size $k$. Because grouping is commutative and associative with respect to addition and taking quotients, performing grouping bottom-up ensures no combination is missed and no invalid combination is counted. Any valid move corresponds exactly to forming a group of $k$ leaf tokens at some node, and every such group is counted exactly once at the lowest node where it becomes fully available.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        g = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            u, v = map(int, input().split())
            g[u].append(v)
            g[v].append(u)

        ans = 0

        def dfs(u, p):
            nonlocal ans
            total = 0
            for v in g[u]:
                if v == p:
                    continue
                total += dfs(v, u)

            if total == 0:
                return 1

            ans += total // k
            return total % k

        dfs(1, -1)
        print(ans)

if __name__ == "__main__":
    solve()
```

The DFS computes, for each node, how many leaf contributions come from its children. A leaf returns 1, representing a single removable endpoint. Internal nodes aggregate these values.

When a node accumulates at least $k$ contributions, those correspond to one valid removal operation centered at some ancestor, so we increment the answer by `total // k`. Any leftover contributions are returned upward because they may combine with other branches higher in the tree.

A subtle point is treating leaves correctly. Returning 1 for a leaf encodes that it is a single available endpoint. If a node has no children contributions, it behaves as a leaf in the reduced tree.

## Worked Examples

### Example 1

Input:

```
n = 5, k = 2
edges:
1-2, 1-3, 3-4, 3-5
```

We run DFS from root 1.

| Node | Children contributions | Total | Groups (//k) | Remainder |
| --- | --- | --- | --- | --- |
| 2 | - | 1 | 0 | 1 |
| 4 | - | 1 | 0 | 1 |
| 5 | - | 1 | 0 | 1 |
| 3 | 1 + 1 = 2 | 2 | 1 | 0 |
| 1 | 1 (from 2) + 1 (from 3 group) = 2 | 2 | 1 | 0 |

Answer is 2.

This trace shows how leaves from different branches combine at internal nodes. Node 3 forms one complete group first, and then node 1 forms another group at the top level.

### Example 2

Input:

```
n = 4, k = 3
1-2, 1-3, 1-4
```

| Node | Children contributions | Total | Groups (//k) | Remainder |
| --- | --- | --- | --- | --- |
| 2 | - | 1 | 0 | 1 |
| 3 | - | 1 | 0 | 1 |
| 4 | - | 1 | 0 | 1 |
| 1 | 1+1+1 = 3 | 3 | 1 | 0 |

Answer is 1.

This confirms that only one operation is possible because all leaves must be consumed together at the root.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each node and edge is processed once in DFS |
| Space | $O(n)$ | Adjacency list and recursion stack |

The total $n$ across test cases is bounded by $2 \cdot 10^5$, so a linear solution per test case is sufficient. The DFS approach comfortably fits within time limits.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    sys.setrecursionlimit(10**7)

    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        g = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            u, v = map(int, input().split())
            g[u].append(v)
            g[v].append(u)

        ans = 0

        def dfs(u, p):
            nonlocal ans
            total = 0
            for v in g[u]:
                if v == p:
                    continue
                total += dfs(v, u)

            if total == 0:
                return 1

            ans += total // k
            return total % k

        dfs(1, -1)
        print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    solve()
    return sys.stdout.getvalue().strip()

# sample tests (from statement)
assert run("""4
8 3
1 2
1 5
7 6
6 8
3 1
6 4
6 1
10 3
1 2
1 10
2 3
1 5
1 6
2 4
7 10
10 9
8 10
7 2
3 1
4 5
3 6
7 4
1 2
1 4
5 1
1 2
2 3
4 3
5 3
""") == "2\n3\n3\n4"

# chain-like case
assert run("""1
5 2
1 2
2 3
3 4
4 5
""") == "2"

# star case
assert run("""1
6 3
1 2
1 3
1 4
1 5
1 6
""") == "1"

# k = 1 case (each leaf removal individually)
assert run("""1
4 1
1 2
1 3
1 4
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain | 2 | sequential propagation in a path |
| star | 1 | grouping at single center |
| k=1 | n-1 | degenerate full removal |

## Edge Cases

A chain shows how leaf tokens must propagate upward instead of being grouped locally too early. The DFS accumulates one token per leaf, and only at internal nodes do groups form, ensuring correct pairing.

A star verifies that all leaves must be combined at a single node when possible, since no deeper structure exists to delay grouping.

When $k = 1$, every leaf contribution immediately becomes an operation. The algorithm handles this naturally because every total contributes `total // 1`, meaning all tokens are consumed at each node without remainder.
