---
title: "CF 106367C - Shichieichou's Guidance"
description: "We are given a rooted tree whose root is node 1. Every leaf lies at the same depth, so the tree is perfectly balanced with respect to leaf depth, although the branching structure can be arbitrary. Each butterfly is attached to a node and disappears at a specified time."
date: "2026-06-19T15:04:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106367
codeforces_index: "C"
codeforces_contest_name: "Whalica Cup (Round 2)"
rating: 0
weight: 106367
solve_time_s: 145
verified: true
draft: false
---

[CF 106367C - Shichieichou's Guidance](https://codeforces.com/problemset/problem/106367/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rooted tree whose root is node 1. Every leaf lies at the same depth, so the tree is perfectly balanced with respect to leaf depth, although the branching structure can be arbitrary.

Each butterfly is attached to a node and disappears at a specified time. Ao starts from any leaf at time 0 and must eventually reach the root. Moving from a node at depth `d` to depth `d - 1` always costs one unit of time.

Normally, Ao can only move to the parent. Once during the journey, she may instead use a special power and move from her current node at depth `d` to any node at depth `d - 1`.

Whenever Ao visits a node at time `t`, every butterfly at that node whose disappearance time is at least `t` can be collected.

The task is to choose the starting leaf and the optional special move so that the number of collected butterflies is maximized.

The input size is large. Across all test cases, both the total number of nodes and the total number of butterflies are at most `2 · 10^5`. Any solution that examines every leaf together with every possible jump location would be far too slow. We need something close to linear time per test case.

A subtle observation is that the actual arrival time at a node depends only on its depth. Since all leaves are at depth `H`, a node at depth `d` is always visited at time `H - d`, regardless of the chosen route. This dramatically simplifies the problem.

Several edge cases are easy to mishandle.

Consider a butterfly that disappears exactly when Ao arrives.

```
3 1
1 2
1 3
1 1
```

The leaves are at depth 1, so the root is reached at time 1. A butterfly at the root with `t = 1` is still collectible because the condition is `current time ≤ ti`.

Another trap is that the special move does not save time. From depth `d` to depth `d - 1`, both a normal parent move and the special move cost exactly one unit. The special move changes only the location, not the arrival time.

For example:

```
    1
   / \
  2   3
 /     \
4       5
```

Jumping from node 4 to node 3 still reaches depth 1 at time 1. Any solution that treats the jump as a shortcut in time will produce incorrect eligibility checks.

A third pitfall is forgetting that the special move is optional. Sometimes the best route is simply a normal leaf-to-root path.

## Approaches

A brute-force approach would enumerate every starting leaf, every possible depth where the special move is used, and every destination node at the next higher level. For each candidate route we could simulate the journey and count collected butterflies.

This works conceptually because every valid journey can be described in exactly that way. Unfortunately, the number of leaves can be linear in `n`, and the number of possible jump choices can also be linear. The resulting complexity easily reaches `O(n^2)` or worse, which is impossible for `2 · 10^5` nodes.

The key observation is that arrival time depends only on depth.

Let `H` be the common leaf depth.

A butterfly at node `v` is collectible if

```
ti ≥ H - depth(v)
```

This condition depends only on the node and the butterfly. It does not depend on the chosen route.

We can therefore preprocess each node and compute:

```
value(v) = number of butterflies at v that are collectible whenever v is visited
```

The original problem becomes purely structural.

Suppose the special move is used while standing at node `a` of depth `d`.

Before the jump, Ao follows a path from some leaf upward to `a`.

After the jump, Ao lands on some node `b` at depth `d - 1` and then follows the ancestor chain from `b` to the root.

The collected nodes split into two independent pieces:

1. A downward chain from `a` to some leaf.
2. An upward chain from the root to `b`.

Since these two parts involve different depth ranges, their scores can be optimized independently.

This turns the problem into two tree dynamic programming computations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) or worse | O(n) | Too slow |
| Optimal | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Root the tree at node 1 and compute the depth of every node.
2. Find the common leaf depth `H`.
3. For every butterfly `(a, t)`, check whether

```
t ≥ H - depth(a)
```

If true, increase `value(a)` by one.

After this step, every node stores how many butterflies are guaranteed to be collectible whenever that node is visited.
4. Compute

```
prefix(v) = sum of value(x)
            along the root-to-v path
```

using a DFS or BFS traversal.
5. For every depth `d`, store

```
bestPrefix[d] =
    maximum prefix(v)
    among all nodes at depth d
```

If a jump lands on depth `d`, this is the best possible score obtainable from the root portion of the route.
6. Compute a bottom-up DP:

```
down(v) =
    maximum score of a path
    starting at v and ending at a leaf
```

For a leaf:

```
down(v) = value(v)
```

For an internal node:

```
down(v) = value(v) + max(down(child))
```
7. Consider journeys that do not use the special move.

Any such journey is exactly a leaf-to-root path.

Its score equals `prefix(leaf)`.

Initialize the answer with the maximum value among all leaves.
8. Consider journeys that use the special move.

Suppose the jump is performed from node `v` at depth `d ≥ 1`.

The best leaf-side contribution is `down(v)`.

The best root-side contribution is `bestPrefix[d - 1]`.

The total score is

```
down(v) + bestPrefix[d - 1]
```

Update the answer with the maximum over all non-root nodes.
9. Output the maximum score.

### Why it works

Every visited node at depth `d` is reached at time `H - d`, regardless of the route. Consequently, whether a butterfly can be collected depends only on its node and disappearance time. Replacing butterflies by node weights preserves the objective exactly.

If the special move is used from a node at depth `d`, the route decomposes into two disjoint depth intervals. The part below depth `d` contributes a leaf-to-node chain, whose optimum is `down(v)`. The part above depth `d` contributes a root-to-node chain ending at some depth `d - 1` node, whose optimum is `bestPrefix[d - 1]`.

Because the two intervals use different depths, they never overlap and can be optimized independently. Every valid route corresponds to exactly one such decomposition, and every decomposition corresponds to a valid route. Taking the maximum over all possible jump positions and also considering the no-jump case guarantees the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, m = map(int, input().split())

        g = [[] for _ in range(n + 1)]

        for _ in range(n - 1):
            u, v = map(int, input().split())
            g[u].append(v)
            g[v].append(u)

        parent = [0] * (n + 1)
        depth = [0] * (n + 1)

        order = [1]
        parent[1] = -1

        for v in order:
            for to in g[v]:
                if to == parent[v]:
                    continue
                parent[to] = v
                depth[to] = depth[v] + 1
                order.append(to)

        H = 0
        for v in range(2, n + 1):
            if len(g[v]) == 1:
                H = depth[v]
                break

        value = [0] * (n + 1)

        for _ in range(m):
            a, ti = map(int, input().split())
            if ti >= H - depth[a]:
                value[a] += 1

        prefix = [0] * (n + 1)
        best_prefix = [-10**18] * (H + 1)

        for v in order:
            if v == 1:
                prefix[v] = value[v]
            else:
                prefix[v] = prefix[parent[v]] + value[v]

            d = depth[v]
            if prefix[v] > best_prefix[d]:
                best_prefix[d] = prefix[v]

        down = value[:]

        for v in reversed(order):
            best_child = 0

            for to in g[v]:
                if to == parent[v]:
                    continue
                if down[to] > best_child:
                    best_child = down[to]

            down[v] = value[v] + best_child

        answer = 0

        for v in range(2, n + 1):
            if len(g[v]) == 1:
                answer = max(answer, prefix[v])

        for v in range(2, n + 1):
            d = depth[v]
            answer = max(answer, down[v] + best_prefix[d - 1])

        ans.append(str(answer))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The first traversal roots the tree and computes depths. Since all leaves share the same depth, finding any leaf immediately gives the common value `H`.

The butterfly processing stage converts the original time-dependent problem into node weights. After that point, the rest of the algorithm never needs to look at disappearance times again.

`prefix[v]` stores the score of the entire root-to-`v` chain. Recording the maximum value at every depth allows us to instantly answer the question: "If a jump lands on depth `d`, what is the best root-side score available?"

The bottom-up DP computes `down[v]`, the best score obtainable by choosing the most profitable leaf beneath `v`. The transition uses the maximum child value because any root-to-leaf path can continue through only one child.

A common mistake is double-counting the jump boundary. The formula

```
down(v) + bestPrefix[d - 1]
```

avoids that because the two pieces occupy different depths. The node at depth `d` belongs only to `down(v)`, while the destination node belongs only to the prefix part.

## Worked Examples

### Example 1

Input:

```
3 2
1 2
1 3
3 0
1 1
```

The common leaf depth is `H = 1`.

Node values:

| Node | Depth | Required time | Butterflies | value |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | (1,1) | 1 |
| 2 | 1 | 0 | none | 0 |
| 3 | 1 | 0 | (3,0) | 1 |

Prefix values:

| Node | prefix |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 2 |

Down values:

| Node | down |
| --- | --- |
| 2 | 0 |
| 3 | 1 |
| 1 | 2 |

The best no-jump path is leaf 3 to root, giving score 2.

The jump option cannot improve this.

Answer: `2`.

This example confirms that arrival exactly at the disappearance time still counts.

### Example 2

Input:

```
6 3
1 2
1 3
2 4
2 5
3 6
6 1
2 1
1 1
```

The common leaf depth is `H = 2`.

Node values:

| Node | Depth | value |
| --- | --- | --- |
| 1 | 0 | 0 |
| 2 | 1 | 1 |
| 6 | 2 | 1 |
| others | - | 0 |

Prefix values:

| Node | prefix |
| --- | --- |
| 1 | 0 |
| 2 | 1 |
| 3 | 0 |
| 4 | 1 |
| 5 | 1 |
| 6 | 1 |

Down values:

| Node | down |
| --- | --- |
| 6 | 1 |
| 3 | 1 |
| 2 | 1 |
| 1 | 2 |

Using the jump from node 6 to node 2 collects both profitable regions:

```
6 -> jump to 2 -> 1
```

Score = 2.

Answer: `2`.

This example demonstrates why the special move is valuable even though it does not save time.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Every node and butterfly is processed a constant number of times |
| Space | O(n) | Graph, depths, DP arrays, and traversal order |

The total sums of `n` and `m` over all test cases are at most `2 · 10^5`, so a linear solution easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = old_stdout
    return out.getvalue().strip()

# sample-style tests
assert run(
"""1
3 2
1 2
1 3
3 0
1 1
"""
) == "2"

assert run(
"""1
6 3
1 2
1 3
2 4
2 5
3 6
6 1
2 1
1 1
"""
) == "2"

# minimum tree
assert run(
"""1
2 1
1 2
2 0
"""
) == "1"

# no butterflies
assert run(
"""1
3 0
1 2
1 3
"""
) == "0"

# jump strictly improves answer
assert run(
"""1
6 2
1 2
1 3
2 4
2 5
3 6
4 0
3 1
"""
) == "2"

# boundary: disappearance exactly at arrival time
assert run(
"""1
2 1
1 2
1 1
"""
) == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum tree with one butterfly | 1 | Smallest valid instance |
| No butterflies anywhere | 0 | Empty contribution handling |
| Jump strictly improves score | 2 | Correct use of special move |
| Disappearance time equals arrival time | 1 | Inclusive comparison `≤` |
| Sample-style cases | 2, 2 | Core functionality |

## Edge Cases

Consider the equality boundary:

```
1
2 1
1 2
1 1
```

The leaf depth is `H = 1`. The root is visited at time `1`. The butterfly also disappears at time `1`, so it is collectible. The preprocessing check uses

```
ti >= H - depth(node)
```

which becomes

```
1 >= 1
```

and correctly counts the butterfly.

Now consider a case where the jump changes location but not time:

```
1
6 2
1 2
1 3
2 4
2 5
3 6
4 0
3 1
```

Node 4 contributes at depth 2 and node 3 contributes at depth 1. A mistaken solution that treats the jump as a time shortcut would compute incorrect arrival times. The algorithm never does this. Arrival time is determined solely from depth, so both butterflies are counted correctly, yielding answer `2`.

Finally, consider a situation where skipping the jump is optimal:

```
1
3 1
1 2
1 3
2 0
```

Starting at leaf 2 already collects the only butterfly. Any jump would visit a different branch and cannot improve the score. The algorithm explicitly evaluates all leaf-to-root paths through the `prefix(leaf)` values, so the no-jump optimum is never missed.
