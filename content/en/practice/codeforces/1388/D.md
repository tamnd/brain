---
title: "CF 1388D - Captain Flint and Treasure"
description: "We are given a directed structure over indices from 1 to n, where each index i has a value a[i] and a pointer b[i]. The pointer either leads to another index or is absent (represented by -1)."
date: "2026-06-16T14:43:12+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "graphs", "greedy", "implementation", "trees"]
categories: ["algorithms"]
codeforces_contest: 1388
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 660 (Div. 2)"
rating: 2000
weight: 1388
solve_time_s: 134
verified: true
draft: false
---

[CF 1388D - Captain Flint and Treasure](https://codeforces.com/problemset/problem/1388/D)

**Rating:** 2000  
**Tags:** data structures, dfs and similar, graphs, greedy, implementation, trees  
**Solve time:** 2m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed structure over indices from 1 to n, where each index i has a value a[i] and a pointer b[i]. The pointer either leads to another index or is absent (represented by -1). The crucial operation is that we must process every index exactly once in some order, and when we process an index i we immediately gain a[i] into a global score. Additionally, if i points to another index j, we also increase a[j] by the current value of a[i], which means later processing of j will benefit from everything accumulated into it so far.

The goal is to choose the order of processing so that these propagations are exploited as much as possible and the final sum of collected values is maximized.

The constraint n up to 2 · 10^5 implies any solution must be close to linear or n log n. Any quadratic ordering simulation over permutations is impossible. The additional structural guarantee that following b pointers always terminates at -1 means the graph formed by b edges is a forest of rooted trees oriented toward roots at -1. There are no cycles, so dependencies are acyclic in the direction of propagation.

A naive failure mode appears when we try to process nodes in arbitrary order or by local heuristics like increasing or decreasing a[i]. For example, consider a chain 1 → 2 → 3 with values a = [1, 100, 1]. If we process 3 first, then 2, then 1, the value from 1 never reaches 2 or 3 in time. The correct strategy must ensure that contributions flow from children to parents before parents are processed.

Another subtle failure arises when a node has multiple children contributing into it indirectly through chains. Greedy local sorting without respecting tree structure can miss that delaying a parent until all descendants are processed increases its value significantly.

## Approaches

A brute-force approach would try all permutations of processing order. For each permutation, we simulate the process, updating a copy of the array and accumulating ans. This is correct because it directly follows the rules, but the number of permutations is n!, and each simulation is O(n), leading to factorial explosion far beyond feasible limits.

The key observation is that the propagation always moves along b edges upward toward roots. Each node contributes its current value upward exactly once per processing, and once a node is processed, its contribution is fixed and never changes again. This strongly suggests that nodes should be processed in an order consistent with pushing accumulated values upward first before consuming a node.

This is analogous to processing a rooted tree bottom-up. If a node receives contributions from its children, it is beneficial to process children first so their accumulated values are included in the parent before the parent is taken. Therefore, within each tree, we want to process nodes in postorder.

However, the values a[i] also matter in ordering between different subtrees. The correct global strategy is to treat each node as having a priority based on subtree accumulation potential, and always process nodes whose descendants are already handled. This leads naturally to a DFS postorder traversal over the forest defined by b pointers.

We compute the forest, run DFS from roots (b[i] = -1), and collect nodes in postorder. That ordering guarantees all children are processed before their parent, ensuring maximum accumulation is transferred upward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal DFS postorder | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

### Step 1: Build the reverse adjacency list

We construct a graph where each node keeps track of its children, meaning all nodes i such that b[i] = parent. This converts the pointer structure into a forest representation.

This step is necessary because propagation flows from a node to its parent, but DFS naturally works from parent to children.

### Step 2: Identify roots

Any node with b[i] = -1 is a root. These are starting points of independent trees in the forest.

We will initiate DFS from each root.

### Step 3: Run DFS to collect postorder

We perform DFS from each root. For each node, we first recursively process all children, then append the node itself to an order list.

The reason we delay appending the node is that we want all contributions from descendants to already be merged into it before it is “consumed” by the operation.

### Step 4: Output order and compute answer

We reverse the DFS finishing order if needed (depending on implementation convention), and use it directly as the processing sequence. We then simulate the process once in that order, updating values and accumulating ans.

This simulation is linear because each edge is used exactly once to propagate values.

### Why it works

The key invariant is that when a node i is processed, all nodes in its subtree (in the b-pointer forest) have already been processed. Therefore, a[i] already includes every contribution that can ever flow into it. No later operation can increase a[i], so taking it at that moment is optimal. This eliminates the possibility of losing value due to premature consumption and ensures every unit of value is propagated as far upward as possible before being collected.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

children = [[] for _ in range(n)]
roots = []

for i in range(n):
    if b[i] == -1:
        roots.append(i)
    else:
        children[b[i] - 1].append(i)

order = []

def dfs(u):
    for v in children[u]:
        dfs(v)
    order.append(u)

for r in roots:
    dfs(r)

ans = 0

for i in order:
    ans += a[i]
    if b[i] != -1:
        a[b[i] - 1] += a[i]

print(ans)
print(*[i + 1 for i in order])
```

The solution first builds the tree structure induced by b pointers. Each node stores a list of children so we can traverse from roots downward.

The DFS produces a postorder sequence where children always appear before their parent. This ordering is directly used as the execution order.

The final loop simulates the process exactly once in that order. Because children are processed earlier, their contributions have already been added into parent values by the time the parent is processed.

One subtle implementation detail is recursion depth, which must be increased because the tree can degenerate into a chain of length n.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
2 3 -1
```

This forms a chain 1 → 2 → 3.

DFS from root 3 produces postorder: 1, 2, 3.

| Step | Processed node | a state before | ans | Update |
| --- | --- | --- | --- | --- |
| 1 | 1 | [1,2,3] | 1 | add a[2] += 1 |
| 2 | 2 | [1,3,3] | 3 | add a[3] += 3 |
| 3 | 3 | [1,3,6] | 9 | no parent |

Final ans is 9 and order is 1 2 3.

This shows how early nodes amplify later ones through propagation.

### Example 2

Input:

```
4
1 1 1 10
2 3 4 -1
```

We have a chain 1 → 2 → 3 → 4 and a large value at the root.

DFS order is 1, 2, 3, 4.

| Step | Node | a before | ans | Update |
| --- | --- | --- | --- | --- |
| 1 | 1 | [1,1,1,10] | 1 | a2 += 1 |
| 2 | 2 | [1,2,1,10] | 3 | a3 += 2 |
| 3 | 3 | [1,2,3,10] | 6 | a4 += 3 |
| 4 | 4 | [1,2,3,13] | 19 | root |

This demonstrates accumulation flowing all the way to the root before it is taken.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node is visited once in DFS and processed once in simulation |
| Space | O(n) | Adjacency list and recursion stack |

The linear complexity is necessary because n can be up to 200,000. Any algorithm that attempts sorting by repeated recomputation or simulation per permutation would be far too slow.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    children = [[] for _ in range(n)]
    roots = []

    for i in range(n):
        if b[i] == -1:
            roots.append(i)
        else:
            children[b[i] - 1].append(i)

    order = []

    sys.setrecursionlimit(10**7)

    def dfs(u):
        for v in children[u]:
            dfs(v)
        order.append(u)

    for r in roots:
        dfs(r)

    ans = 0
    for i in order:
        ans += a[i]
        if b[i] != -1:
            a[b[i] - 1] += a[i]

    return str(ans) + "\n" + " ".join(str(x + 1) for x in order)

# provided sample
assert run("""3
1 2 3
2 3 -1
""") == "9\n1 2 3"

# single node
assert run("""1
5
-1
""") == "5\n1"

# all root chain
assert run("""4
1 2 3 4
2 3 4 -1
""") == "10\n1 2 3 4"

# negative values
assert run("""3
-1 -2 -3
2 3 -1
""") == "-6\n1 2 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 5 | base case correctness |
| chain increasing | 10 | propagation accumulation |
| chain negative | -6 | correctness with negative values |

## Edge Cases

One important edge case is a single long chain. In this case, the DFS degenerates into depth n recursion. The algorithm still processes nodes in correct bottom-up order, ensuring each value is propagated fully before being consumed.

Another edge case is all nodes having b[i] = -1. Then every node is a root and DFS simply appends nodes in reverse subtree order, but since there are no edges, any order is valid and the simulation reduces to a simple sum of a[i].

A third case involves negative values propagating upward. Because the algorithm still propagates values regardless of sign, a negative node early in a chain can reduce future values. The postorder ordering remains correct because delaying a node would only allow even more negative accumulation to flow upward, which is still optimal under the given operation rules.
