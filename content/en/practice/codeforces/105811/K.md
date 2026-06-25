---
title: "CF 105811K - Philadelphia Museum of Art"
description: "We are given a tree of museum rooms rooted at room 1, where room 1 is the entrance. Two people, Kuroni and Tfg, start at the entrance and always move together along a single path. At any non-leaf room, exactly one child room must be chosen as the next destination."
date: "2026-06-25T15:21:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105811
codeforces_index: "K"
codeforces_contest_name: "UT Open 2025"
rating: 0
weight: 105811
solve_time_s: 48
verified: true
draft: false
---

[CF 105811K - Philadelphia Museum of Art](https://codeforces.com/problemset/problem/105811/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree of museum rooms rooted at room 1, where room 1 is the entrance. Two people, Kuroni and Tfg, start at the entrance and always move together along a single path.

At any non-leaf room, exactly one child room must be chosen as the next destination. Kuroni chooses the first move, then Tfg chooses the next move, then Kuroni again, and so on. Since the graph is a tree and revisiting rooms is forbidden, their journey is simply a root-to-leaf path.

Each room may be liked by Kuroni, by Tfg, by both, or by neither. A player's score is the number of liked rooms that appear on the final path.

When a player is making a decision, they act optimally. They first maximize their own final score. If several choices give the same score for themselves, they choose the one that gives the largest score to the other player.

The task is to determine the final scores of both players.

The tree contains up to $10^5$ nodes. Any solution that explores every possible root-to-leaf path independently is immediately ruled out, because a tree of this size can contain a linear number of leaves and exponentially many decision sequences in terms of depth. We need a linear or near-linear solution.

A subtle point is that the players are not trying to minimize the other player's score. Their tie-breaking rule is actually cooperative after their own score is fixed.

Consider this small example:

```
1
|
2
```

If both players like room 1 and room 2, the answer is simply `(2, 2)`. There are no choices at all, so game-theoretic reasoning must still correctly include every visited room.

Another easy mistake is forgetting the tie-break rule.

```
    1
   / \
  2   3
```

Suppose Kuroni's final score is the same regardless of whether she chooses room 2 or room 3. Then she must pick the child that gives Tfg the larger final score. A solution that only maximizes the current player's score and ignores ties can produce the wrong path.

A third pitfall is forgetting that scores come from all rooms on the chosen path, not just the room selected on the current move. A locally attractive child may lead to a worse subtree later.

## Approaches

A brute-force solution would treat the problem as a complete game tree. From each room we try every child, recursively evaluate the resulting game state, and choose according to the player's preference order. This is correct because it exactly follows the rules of optimal play.

The problem is that many subgames repeat. Suppose we arrive at some room $u$ and it is Kuroni's turn. The outcome from that point onward depends only on the subtree rooted at $u$ and whose turn it is. It does not depend on the path used to reach $u$.

That observation turns the game into a tree dynamic programming problem.

Define a state by two pieces of information:

```
(current node, whose turn chooses next)
```

For every node we compute two answers.

`dp0[u]` is the pair of final scores obtainable from the subtree rooted at `u` when it is Kuroni's turn to choose the next room.

`dp1[u]` is the analogous pair when it is Tfg's turn.

If `u` is a leaf, there is no decision left. The path ends immediately, so the result is simply the contribution of room `u`.

For an internal node, the current player selects one child. The rest of the game is exactly the corresponding DP state in that child with the turn switched.

The only remaining detail is the comparison rule.

When Kuroni chooses, she prefers larger Kuroni score first, then larger Tfg score.

When Tfg chooses, she prefers larger Tfg score first, then larger Kuroni score.

After selecting the best child, we add the contribution of the current room.

Each node is processed once, and every edge is examined once, giving a linear-time solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in tree depth | O(depth) | Too slow |
| Optimal DP on Tree | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Root the tree at node 1.
2. Perform a DFS traversal and obtain a postorder so that every child is processed before its parent.
3. For a leaf node `u`, set:

```
dp0[u] = dp1[u] = (a[u], b[u])
```

Since no move remains, the path consists only of `u`.
4. Compute `dp0[u]`.

Examine every child `v`.

The game continues from `v` with Tfg's turn, so the candidate outcome is `dp1[v]`.

Choose the child whose outcome is lexicographically largest under:

```
(Kuroni score, Tfg score)
```

After choosing the best child, add the contribution of node `u`.
5. Compute `dp1[u]`.

Examine every child `v`.

The game continues from `v` with Kuroni's turn, so the candidate outcome is `dp0[v]`.

Choose the child whose outcome is lexicographically largest under:

```
(Tfg score, Kuroni score)
```

After choosing the best child, add the contribution of node `u`.
6. The answer is `dp0[1]`, because the game starts at room 1 and Kuroni makes the first decision.

### Why it works

For any node, once we know whose turn it is, the future game depends only on that subtree. This gives optimal substructure.

Assume all children already contain correct DP values.

If it is Kuroni's turn, every legal move corresponds to selecting one child. The resulting scores are exactly the scores stored in that child's state. Kuroni's rules say she chooses the outcome maximizing her own score, with Tfg's score used only as a tie-breaker. Selecting the best child under that ordering exactly matches the game's definition.

The same argument applies to Tfg's turn.

Since leaves are correct and every parent is computed from already-correct children, induction on subtree size proves that every DP state is correct. The value at the root is the game's final outcome.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

a = list(map(int, input().split()))
b = list(map(int, input().split()))

g = [[] for _ in range(n)]

for _ in range(n - 1):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    g[u].append(v)
    g[v].append(u)

parent = [-1] * n
order = [0]
parent[0] = 0

for u in order:
    for v in g[u]:
        if parent[v] == -1:
            parent[v] = u
            order.append(v)

dp0 = [(0, 0)] * n
dp1 = [(0, 0)] * n

for u in reversed(order):
    children = [v for v in g[u] if v != parent[u]]

    if not children:
        dp0[u] = (a[u], b[u])
        dp1[u] = (a[u], b[u])
        continue

    best_k = None
    for v in children:
        cand = dp1[v]
        if best_k is None or (cand[0], cand[1]) > (best_k[0], best_k[1]):
            best_k = cand

    dp0[u] = (best_k[0] + a[u], best_k[1] + b[u])

    best_t = None
    for v in children:
        cand = dp0[v]
        if best_t is None or (cand[1], cand[0]) > (best_t[1], best_t[0]):
            best_t = cand

    dp1[u] = (best_t[0] + a[u], best_t[1] + b[u])

ans = dp0[0]
print(ans[0], ans[1])
```

The first DFS constructs parent relationships and a traversal order. Reversing that order gives a postorder-like processing sequence where every child is handled before its parent.

The two DP arrays store pairs `(kuroni_score, tfg_score)`.

For `dp0`, we compare child outcomes directly as `(kuroni, tfg)` because Kuroni's preference order follows exactly that lexicographic ordering.

For `dp1`, we compare as `(tfg, kuroni)` because Tfg's score is the primary objective.

The implementation uses iterative traversal rather than recursive DFS. With $10^5$ nodes, recursion depth can exceed Python's default recursion limit.

## Worked Examples

### Example 1

Input:

```
5
0 1 1 0 1
0 0 1 1 1
1 2
1 3
2 4
2 5
```

Processing from leaves upward:

| Node | dp0 | dp1 |
| --- | --- | --- |
| 3 | (1,1) | (1,1) |
| 4 | (0,1) | (0,1) |
| 5 | (1,1) | (1,1) |
| 2 | (2,1) | (2,1) |
| 1 | (2,1) | (2,2) |

At node 2, both turns choose room 5 because `(1,1)` dominates `(0,1)`.

At node 1, Kuroni compares child outcomes `(2,1)` and `(1,1)`, choosing the first. The final answer is:

```
2 1
```

This demonstrates that decisions are based on complete future outcomes, not immediate room values.

### Example 2

Input:

```
3
0 1 1
0 0 1
1 2
1 3
```

DP values:

| Node | dp0 | dp1 |
| --- | --- | --- |
| 2 | (1,0) | (1,0) |
| 3 | (1,1) | (1,1) |
| 1 | (1,1) | (1,1) |

Kuroni compares `(1,0)` and `(1,1)`.

Her own score is tied, so the tie-break chooses `(1,1)`.

Final answer:

```
1 1
```

This example isolates the secondary comparison rule.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node and edge is processed a constant number of times |
| Space | O(n) | Adjacency list, parent array, traversal order, and DP arrays |

With $n \le 10^5$, linear time is easily fast enough. Memory usage is also linear and comfortably fits within typical contest limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    g = [[] for _ in range(n)]

    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    parent = [-1] * n
    order = [0]
    parent[0] = 0

    for u in order:
        for v in g[u]:
            if parent[v] == -1:
                parent[v] = u
                order.append(v)

    dp0 = [(0, 0)] * n
    dp1 = [(0, 0)] * n

    for u in reversed(order):
        children = [v for v in g[u] if v != parent[u]]

        if not children:
            dp0[u] = (a[u], b[u])
            dp1[u] = (a[u], b[u])
            continue

        best_k = None
        for v in children:
            cand = dp1[v]
            if best_k is None or (cand[0], cand[1]) > (best_k[0], best_k[1]):
                best_k = cand

        dp0[u] = (best_k[0] + a[u], best_k[1] + b[u])

        best_t = None
        for v in children:
            cand = dp0[v]
            if best_t is None or (cand[1], cand[0]) > (best_t[1], best_t[0]):
                best_t = cand

        dp1[u] = (best_t[0] + a[u], best_t[1] + b[u])

    return f"{dp0[0][0]} {dp0[0][1]}\n"

# sample
assert run(
"""5
0 1 1 0 1
0 0 1 1 1
1 2
1 3
2 4
2 5
"""
) == "2 1\n"

# minimum size
assert run(
"""1
1
0
"""
) == "1 0\n"

# tie-break by other player's score
assert run(
"""3
0 1 1
0 0 1
1 2
1 3
"""
) == "1 1\n"

# chain
assert run(
"""4
1 0 1 0
0 1 0 1
1 2
2 3
3 4
"""
) == "2 2\n"

# all zero preferences
assert run(
"""3
0 0 0
0 0 0
1 2
1 3
"""
) == "0 0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single node tree | `1 0` | Base case with no moves |
| Tie-break example | `1 1` | Secondary comparison rule |
| Chain tree | `2 2` | No branching, forced path |
| All zeros | `0 0` | Scores accumulate correctly even when empty |
| Sample case | `2 1` | General correctness |

## Edge Cases

Consider a tree consisting of only the root:

```
1
1
0
```

The root is also a leaf. The algorithm immediately assigns:

```
dp0[1] = dp1[1] = (1, 0)
```

No decisions are made, and the answer is `(1, 0)`.

Now consider a pure tie:

```
3
0 1 1
0 0 1
1 2
1 3
```

The child outcomes are `(1,0)` and `(1,1)`.

Kuroni's primary score is 1 in both cases. The algorithm compares lexicographically as `(Kuroni, Tfg)` and selects `(1,1)`. This exactly matches the problem's tie-break rule.

Finally, consider a path-shaped tree:

```
4
1 0 1 0
0 1 0 1
1 2
2 3
3 4
```

Every node has at most one child. No choices exist anywhere. The DP simply accumulates room contributions from the leaf upward, producing `(2,2)`. This confirms that the algorithm behaves correctly even when the game aspect disappears and the path is forced.
