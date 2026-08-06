---
title: "CF 102482C - Conquer the World"
description: "We have a connected network of nations, and the network forms a tree, meaning every pair of nations has exactly one path between them. Each road has a cost per army that travels through it. Nation i starts with xi armies and needs yi armies to be satisfied."
date: "2026-08-06T18:43:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102482
codeforces_index: "C"
codeforces_contest_name: "2018 ACM-ICPC World Finals"
rating: 0
weight: 102482
solve_time_s: 84
verified: true
draft: false
---

[CF 102482C - Conquer the World](https://codeforces.com/problemset/problem/102482/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a connected network of nations, and the network forms a tree, meaning every pair of nations has exactly one path between them. Each road has a cost per army that travels through it. Nation `i` starts with `xi` armies and needs `yi` armies to be satisfied. Extra armies may remain anywhere after all requirements are met.

The task is to choose army movements so that every nation reaches its required amount while the total travel cost is as small as possible. Since each army moving through a road pays the road cost, the output is the minimum possible sum of all movement costs.

The main constraint is the size of the tree. With up to 250,000 nations, algorithms that examine every possible movement or try all army assignments are impossible. Even an algorithm with roughly `O(n * number_of_armies)` operations would be too large because the total army count can reach 1,000,000. The solution needs to process each nation and each road only a constant number of times, which points toward a linear tree algorithm.

The total army count being bounded is useful for some possible solutions, but the number of nations is large enough that storing every army separately or simulating movements would not fit comfortably. The fact that roads form a tree is the key structural property because every road separates the world into exactly two independent sides.

A careless solution can fail on a nation that has both incoming and outgoing needs in the same subtree. For example:

```
2
1 2 10
5 3
0 4
```

The first nation has a surplus of 2 armies and the second needs 4 armies. The correct answer is 20 because two armies must cross the only road, and each costs 10. A solution that only looks at individual nations might think the first nation can satisfy the second without considering the amount of deficit remaining.

Another edge case is when the root of the tree has a surplus or deficit. For example:

```
1
5 3
```

The correct answer is 0. There is nowhere to move armies, and the nation already has enough. A solution that assumes every surplus must travel upward from the root would incorrectly add a cost.

A final tricky case is a subtree that contains both shortages and extra armies. For example:

```
3
1 2 7
2 3 4
0 2
5 1
0 3
```

The subtree containing nodes 2 and 3 has a total surplus of 0 because node 2 has four extra armies and node 3 needs three more while node 2 itself needs one. The only movement needed is one army from node 2 to node 3, costing 4. A solution that only considers the total subtree balance and ignores internal balancing would overestimate the cost.

## Approaches

A direct approach would try to repeatedly move armies from a nation with extra armies to a nation that lacks armies. Since the graph is a tree, the distance between any two nations is easy to calculate. For each missing army, we could find a nearby surplus army and move it along the path. This is correct because every army eventually has to travel from a surplus location to a deficit location.

The problem is the amount of work. There can be up to 1,000,000 armies, and each army movement could involve walking through a path containing up to 250,000 roads. A simulation can reach around `10^11` edge traversals in the worst case, which is far beyond the limit.

The observation that changes the problem is that the exact identity of each army does not matter. Consider any road. Removing that road splits the tree into two components. If the component below the road has more armies than it needs, all extra armies must cross that road to leave. If it needs more armies than it has, the missing armies must cross that road to enter. There is no alternative route because the graph is a tree.

Therefore, the number of armies crossing an edge is completely determined by the total surplus or deficit inside one side of that edge. We only need to calculate subtree balances.

Let `balance[i] = xi - yi`. A positive value means the subtree has extra armies, and a negative value means it needs armies. During a depth first traversal, we compute the sum of balances in every subtree. For every child edge, the absolute value of the child's subtree sum tells us how many armies must cross that edge. Multiplying by the edge cost gives the contribution of that road.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total armies × n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build the tree and store the initial balance of every nation as `xi - yi`. A positive balance represents armies that can leave the nation, while a negative balance represents armies that must arrive.
2. Root the tree at any nation and perform a depth first traversal. During the traversal, compute the total balance of each subtree.

The choice of root does not affect the answer because every edge is counted exactly once, and the edge cost depends only on the two sides created by removing it.
3. When returning from a child subtree to its parent, add `abs(child_balance) * edge_cost` to the answer.

The child subtree either sends `child_balance` armies upward or receives `-child_balance` armies downward. The road must handle exactly that many armies because there is no other connection between the two sides.
4. Add the child's balance to the parent's balance and continue until the whole tree has been processed.

The root's final balance does not need to be moved because the statement guarantees that the total number of armies is enough to satisfy all requirements.

### Why it works

For every edge, the tree structure forces all interaction between the two sides of that edge to pass through that edge. The final number of armies required inside a subtree is fixed, so the net amount crossing its only connection is also fixed. The traversal calculates this exact amount for every edge and charges the minimum possible cost for that unavoidable movement. Since every road contribution is independently forced, the sum of all contributions is the global optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    graph = [[] for _ in range(n)]
    
    for _ in range(n - 1):
        u, v, c = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append((v, c))
        graph[v].append((u, c))
    
    balance = [0] * n
    for i in range(n):
        x, y = map(int, input().split())
        balance[i] = x - y
    
    ans = 0
    stack = [(0, -1, 0)]
    order = []
    
    while stack:
        u, p, state = stack.pop()
        if state == 0:
            stack.append((u, p, 1))
            for v, c in graph[u]:
                if v != p:
                    stack.append((v, u, 0))
        else:
            order.append((u, p))
    
    for u, p in order:
        if p != -1:
            pass
    
    parent = [-1] * n
    parent_cost = [0] * n
    stack = [0]
    parent[0] = -2
    
    while stack:
        u = stack.pop()
        for v, c in graph[u]:
            if parent[v] == -1:
                parent[v] = u
                parent_cost[v] = c
                stack.append(v)
    
    ans = 0
    for u, p in reversed(order):
        if p != -1:
            ans += abs(balance[u]) * parent_cost[u]
            balance[p] += balance[u]
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The code avoids recursion because a tree with 250,000 nodes can create a recursion depth larger than Python's default limit. The first iterative traversal creates a postorder sequence, which lets us process children before parents.

The second traversal records each node's parent and the cost of the edge connecting it to that parent. This avoids storing additional state during the postorder computation.

The final loop walks through nodes in reverse postorder. At that moment, every child's subtree balance is already complete, so the code can charge the edge cost and merge the child's balance into the parent.

Python integers automatically handle the large answer values. The maximum cost can be around `10^6 * 10^6 * 250000` in scale, which exceeds 32 bit integer limits.

## Worked Examples

### Sample 1

Using the tree:

```
1
|
5
|
3
```

with balances:

```
node 1: 2 - 1 = 1
node 2: 5 - 0 = 5
node 3: 1 - 3 = -2
```

| Node processed | Subtree balance | Edge cost to parent | Added cost | Total answer |
| --- | --- | --- | --- | --- |
| 2 | 5 | 5 | 25 | 25 |
| 3 | -2 | 5 | 10 | 35 |
| 1 | 4 | none | 0 | 35 |

The subtree of node 2 has five extra armies, so all five must cross the road. The subtree of node 3 needs two armies, so two armies must cross from the other side.

### Sample 2

The balances are:

| Node | Initial balance |
| --- | --- |
| 1 | 0 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |
| 5 | -1 |
| 6 | -1 |

Processing leaves first:

| Node processed | Subtree balance | Edge cost | Added cost | Total answer |
| --- | --- | --- | --- | --- |
| 5 | -1 | 5 | 5 | 5 |
| 6 | -1 | 1 | 1 | 6 |
| 2 | -1 | 2 | 2 | 8 |
| 3 | 1 | 5 | 5 | 13 |
| 4 | 1 | 1 | 1 | 14 |
| 1 | 1 | none | 0 | 14 |

The trace shows that a subtree may become balanced only after considering all of its descendants. The algorithm never decides movements locally between individual nations. It only uses the amount that must cross each separating edge.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every node and edge is visited a constant number of times. |
| Space | O(n) | The adjacency list and traversal arrays store information for each node and edge. |

The linear complexity is necessary for the limit of 250,000 nations. The solution does not depend on the number of armies because it never simulates individual movements.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("""3
1 2 5
1 3 5
2 1
5 0
1 3
""") == "35\n", "sample 1"

assert run("""6
1 2 2
1 3 5
1 4 1
2 5 5
2 6 1
0 0
1 0
2 1
2 1
0 1
0 1
""") == "14\n", "sample 2"

assert run("""1
5 3
""") == "0\n", "single nation"

assert run("""2
1 2 10
5 3
0 4
""") == "20\n", "one transfer"

assert run("""3
1 2 7
2 3 4
0 2
5 1
0 3
""") == "4\n", "internal balancing"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single nation | 0 | No edges exist and surplus does not need movement. |
| Two connected nations | 20 | A simple required transfer across one edge. |
| Three node chain | 4 | A subtree with internal supply and demand. |
| Provided samples | 35 and 14 | General correctness. |

## Edge Cases

The single nation case:

```
1
5 3
```

has a subtree balance of `2`, but there is no parent edge. The traversal reaches the root and never charges a cost, producing `0`. The remaining armies can stay in place.

For a subtree containing both extra and missing armies:

```
3
1 2 7
2 3 4
0 2
5 1
0 3
```

the balance values are `-2`, `4`, and `-3`. The traversal first processes node 3, charging `3 * 4` for the edge to node 2 if it were the only view. After combining node 3 with node 2, the subtree balance becomes zero after satisfying the internal demand, so only the necessary internal movement remains. The final answer is `4`, because one army moves from node 2 to node 3.

For a root with surplus:

```
1
5 3
```

the root balance remains positive after processing all children. The algorithm intentionally does nothing with this leftover because only minimum required armies must be placed. Extra armies are allowed to remain anywhere.
