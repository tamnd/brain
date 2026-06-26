---
title: "CF 105622B - Tree Game"
description: "The game is played on a tree. Spyrosaliv starts on node s and wants to reach node d. On every turn he must move across an edge that is currently not blocked. Reaching d immediately wins. If he has no legal move, he loses."
date: "2026-06-26T18:16:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105622
codeforces_index: "B"
codeforces_contest_name: "TheForces Round #38 (Tree-Forces)"
rating: 0
weight: 105622
solve_time_s: 56
verified: true
draft: false
---

[CF 105622B - Tree Game](https://codeforces.com/problemset/problem/105622/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

The game is played on a tree. Spyrosaliv starts on node `s` and wants to reach node `d`. On every turn he must move across an edge that is currently not blocked. Reaching `d` immediately wins. If he has no legal move, he loses.

After every move made by Spyrosaliv, Cow the Cow gets a turn. The cow controls one blocked edge. It can remove the previous block and place a new block on a different edge. The cow is trying to prevent Spyrosaliv from ever reaching `d`.

The key question is whether the starting position has any chance against an opponent who can always react after seeing the previous move.

The number of nodes can be as large as `200000`, so any solution that explores many possible game states is impossible. A tree of this size only allows algorithms close to linear time. We need to find a structural property of the tree instead of simulating moves.

The non-obvious edge cases are caused by the fact that Spyrosaliv moves first. If the destination is directly adjacent, the cow never gets a chance to interfere.

For example:

```
2 1 2
1 2
```

The correct output is:

```
YES
```

Spyrosaliv immediately moves from node `1` to node `2`.

A careless approach that only considers whether the cow can block the route would incorrectly say that the cow always wins, because it ignores the first move advantage.

Another important case is a longer path:

```
3 1 3
1 2
2 3
```

The correct output is:

```
NO
```

Spyrosaliv moves to node `2`. The cow blocks the only edge leading to node `3`, so Spyrosaliv cannot continue toward the target. Moving back only gives the cow another opportunity to block the edge behind him.

The same problem appears in larger trees. Extra branches do not create a winning strategy because the cow can always block the edge that goes toward the destination after Spyrosaliv leaves his current node.

## Approaches

A natural brute-force approach is to treat the game as a graph search. A state would contain Spyrosaliv's current node and the currently blocked edge. From every state we could try every legal move, then simulate every possible response from the cow. This is correct because it exactly models optimal play, but the number of states is far too large.

There are up to `n` possible positions and `n - 1` possible blocked edges, giving roughly `O(n^2)` states. For `n = 200000`, this is far beyond what can fit in time or memory.

The important observation comes from rooting the tree at the destination node `d`. Every node except `d` has exactly one parent edge that moves closer to the destination. If Spyrosaliv is not adjacent to `d`, his first move can be considered as moving to some child of `d`'s rooted tree or moving upward toward `d`. After every successful move toward `d`, the cow can block the exact edge Spyrosaliv would need next.

Suppose Spyrosaliv is currently at node `u`, and the edge from `u` to its parent is the only useful direction. After Spyrosaliv moves somewhere, the cow can block the parent edge of the new node. Spyrosaliv is then forced away from the destination. Repeating this strategy pushes Spyrosaliv farther from `d` until he reaches a dead end.

The only time the cow does not get this opportunity is the very first move. If `s` is adjacent to `d`, Spyrosaliv reaches the destination immediately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) states | O(n²) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the tree and store the neighbors of every node. The only information needed is whether `d` is directly connected to `s`, so a full traversal is unnecessary.
2. Check every neighbor of `s`. If one of them is `d`, Spyrosaliv can move there on the first turn and wins before the cow acts.
3. If `d` is not adjacent to `s`, output `NO`. The cow can always block Spyrosaliv's progress after the first move by blocking the edge leading toward the destination.

Why it works:

Root the tree at `d`. Every node has exactly one edge that decreases its distance to `d`. Spyrosaliv needs to repeatedly use such edges to approach the target. After every move, the cow knows Spyrosaliv's new location and can block that next decreasing edge. Since the cow acts after Spyrosaliv, the only possible escape from this strategy is reaching `d` on the first move. That happens exactly when `s` and `d` are adjacent.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, s, d = map(int, input().split())
    adj = [[] for _ in range(n + 1)]

    for _ in range(n - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)

    for v in adj[s]:
        if v == d:
            print("YES")
            return

    print("NO")

if __name__ == "__main__":
    solve()
```

The implementation only needs the adjacency list because the answer depends on the first move. We do not need to store parent relationships or simulate the game.

The loop over `adj[s]` checks every possible first move. If the destination appears there, the game ends immediately in Spyrosaliv's favor. Otherwise, the cow's blocking strategy works regardless of the rest of the tree.

There are no indexing tricks involved because the nodes are numbered from `1` and the adjacency list is created with size `n + 1`.

## Worked Examples

### Sample 1

Input:

```
5 2 4
1 4
2 5
4 3
3 5
```

The relevant starting node information is:

| Current node | Neighbor checked | Is destination? |
| --- | --- | --- |
| 2 | 5 | No |

The algorithm never finds node `4` as a neighbor of node `2`, so the answer is `NO`.

This example shows that having a path to the destination is not enough. The cow can interfere after the first move.

### Sample 2

Input:

```
2 1 2
1 2
```

The trace is:

| Current node | Neighbor checked | Is destination? |
| --- | --- | --- |
| 1 | 2 | Yes |

The destination is reached on the first move, before the cow can block anything.

This confirms the first-move exception that defines the entire solution.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Building the adjacency list touches every edge once, then checking the neighbors of `s` is linear in the degree of `s`. |
| Space | O(n) | The adjacency list stores the tree edges. |

The solution fits the `200000` node limit because it performs only a linear amount of work and stores the tree once.

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

# provided samples
assert run("""5 2 4
1 4
2 5
4 3
3 5
""") == "NO\n", "sample 1"

assert run("""2 1 2
1 2
""") == "YES\n", "sample 2"

# minimum size
assert run("""2 2 1
1 2
""") == "YES\n", "two nodes"

# longer chain
assert run("""4 1 4
1 2
2 3
3 4
""") == "NO\n", "chain longer than one edge"

# star with unrelated branches
assert run("""5 1 5
1 2
1 3
1 4
1 5
""") == "YES\n", "destination is immediate neighbor"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two-node tree | YES | The first move wins immediately. |
| Four-node chain | NO | A longer path can always be blocked. |
| Star tree | YES | Branching does not matter when the target is adjacent. |

## Edge Cases

For a direct connection between start and destination:

```
2 1 2
1 2
```

The adjacency list of node `1` contains node `2`. The algorithm prints `YES` because Spyrosaliv reaches the target before the cow gets a turn.

For a destination that requires multiple moves:

```
3 1 3
1 2
2 3
```

Node `1` only checks neighbor `2`. Since `2` is not the destination, the algorithm prints `NO`. The cow can block the edge from node `2` to node `3` immediately after the first move.

For a tree with many branches:

```
5 1 5
1 2
1 3
1 4
1 5
```

The starting node has several possible moves, but one of them reaches the destination immediately. The algorithm detects node `5` among the neighbors and prints `YES`.

For a tree where the start node has no direct connection to the target, the number of alternative routes does not matter. Every route in a tree eventually has to use the unique edge that approaches `d`, and the cow can always block that edge after the previous move.
