---
title: "CF 102458B - Daniel and gameshow"
description: "The graph is a tree because it has (n) vertices and exactly (n-1) edges while being connected. Every edge has a toughness (a), meaning Daniel may cross that edge at most (a) times during his turn. He chooses a starting vertex (R), or, when (R=0), he may choose any vertex."
date: "2026-08-08T10:29:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102458
codeforces_index: "B"
codeforces_contest_name: "Hanoi final contest"
rating: 0
weight: 102458
solve_time_s: 138
verified: true
draft: false
---

[CF 102458B - Daniel and gameshow](https://codeforces.com/problemset/problem/102458/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

The graph is a tree because it has (n) vertices and exactly (n-1) edges while being connected. Every edge has a toughness (a), meaning Daniel may cross that edge at most (a) times during his turn. He chooses a starting vertex (R), or, when (R=0), he may choose any vertex. He can stop at any time, and his score is simply the number of edge crossings he has made.

The key difficulty is that an edge in a tree has only one way to enter its far side and only one way to come back. If Daniel finishes on the same side from which he entered, that edge must be crossed an even number of times. If Daniel finishes on the other side, it must be crossed an odd number of times. The problem is consequently about choosing where the walk ends, while maximizing the usable number of crossings in every explored subtree.

The official constraints allow (n) up to (10^5), with edge toughness as large as (10^9), and the time limit is 2 seconds. This rules out anything quadratic in (n). A solution that spends (O(n)) work for every possible starting vertex would perform about (10^{10}) operations in the worst case. The intended solution has to process the tree only a constant number of times.

There are several edge cases where a simple sum of edge capacities gives the wrong answer. With one vertex there are no edges at all:

```
1
1
```

The answer is `0`. A formula that assumes every edge contributes something without handling the empty tree would fail immediately.

A single edge with toughness one can be used once if Daniel stops on the other endpoint:

```
2
1 2 1
1
```

The answer is `1`. A careless solution that assumes every traversed edge has to be used twice would return zero.

A toughness-one edge can also act as a one-way gateway into a large subtree. Consider:

```
3
1 2 1
2 3 9
1
```

Daniel can cross (1)-(2) once, then cross (2)-(3) nine times and finish at vertex 3, for a score of `10`. A solution that only counts subtrees which can be entered and completely returned from would miss the entire second edge.

The value (R=0) introduces another subtlety because the best starting vertex need not be the arbitrary root used by the implementation. For example:

```
3
1 2 3
1 3 3
0
```

Starting at vertex 2, Daniel can use both edges three times, ending at vertex 3, for a score of `6`. Starting at the center gives only `5`, so simply rooting the tree at vertex 1 and taking the answer there is not enough.

## Approaches

A direct approach is to fix a starting vertex and run a tree DP that decides whether each child subtree is visited and returned from, or whether the final walk goes into that child. This DP is correct because every walk on a tree has a unique final direction from the starting point, and every other explored branch has to be entered and left equally many times. If we repeated this computation independently for every possible starting vertex, each run would take (O(n)), producing (O(n^2)) work. At (n=10^5), that is roughly (10^{10}) operations, far beyond the time limit.

The useful observation is that the same DP can be expressed as a message between two adjacent vertices. Remove an edge (uv). The tree splits into two independent components. From the (u) side, we only need two pieces of information: the best score of a walk that starts and finishes at (u), and the best score of a walk that starts at (u) and finishes anywhere in that component.

Call these values (F(u\to v)) and (G(u\to v)). Once all messages coming into a vertex are known, the message sent toward any one neighbor is obtained by excluding that neighbor's contribution. This is exactly the structure that rerooting DP is designed for.

For an edge of toughness (a), define its best even usage and best odd usage. The best even usage is (a) when (a) is even and (a-1) when (a) is odd. If (a=1), this value is zero, and the edge cannot be used in a closed excursion at all. The best odd usage is (a) when (a) is odd and (a-1) when (a) is even.

Suppose a neighboring component provides a closed value (F). If the edge is used as a round trip, its contribution is its best even usage plus (F), except when the best even usage is zero, in which case the component cannot be entered and returned from. If the edge is used as the final path toward the endpoint, its contribution is its best odd usage plus the neighboring (G) value.

This gives both messages in linear time after rerooting. The first tree traversal computes child-to-parent messages. The second traversal supplies parent-to-child messages and, at every vertex, evaluates the best walk starting there. If (R) is fixed, we take the value for that vertex. If (R=0), we take the maximum over all vertices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(n)) | Too slow |
| Optimal rerooting DP | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Root the tree temporarily at vertex 1. This root is only an implementation device. It has nothing to do with Daniel's required starting vertex.
2. For every directed tree edge (u\to v), define (F(u\to v)) as the maximum score of a closed walk that starts and finishes at (u), using only the component containing (u) after removing (uv). Define (G(u\to v)) as the maximum score of a walk that starts at (u) and finishes anywhere in that same component.

These two values are enough because a closed child excursion can be attached to a walk at the current vertex, while at most one child can contain the final endpoint of an open walk.
3. For a neighbor (w) connected by an edge of toughness (a), compute its closed contribution

[
C =
\begin{cases}
a + F(w\to u), & a\text{ even},\
a-1 + F(w\to u), & a\text{ odd and }a>1,\
0, & a=1.
\end{cases}
]

The reason for the special case (a=1) is that entering the component would require one crossing, but returning would require a second crossing that does not exist.
4. Compute the corresponding open contribution

[
O = \operatorname{odd}(a) + G(w\to u),
]

where (\operatorname{odd}(a)) is the largest odd number not exceeding (a).

Choosing this contribution means the walk eventually ends inside the neighbor's component, so the connecting edge must be crossed an odd number of times.
5. Process the rooted tree bottom-up. For every vertex (u), sum the closed contributions of all children. This gives (F(u\to parent[u])). Among the children, find the largest value of (O-C). Replacing one closed child excursion by an open excursion gives

F(u\to parent[u])+\max(0,\max(O-C)).
]

Only one child can contain the final endpoint, so only one closed contribution may be replaced.
6. Process the tree top-down. At a vertex (u), all incoming messages from its parent and children are now available. Sum their closed contributions to obtain the best closed walk starting and finishing at (u).
7. For every incident edge, calculate (O-C). The best walk starting at (u) either remains closed or chooses exactly one incident edge through which its final endpoint is reached. Hence

closed[u]+\max(0,\max(O-C)).
]
8. When producing the message (u\to child), exclude that child's contribution from the total. We need the best (O-C) among all other neighbors, so the implementation keeps the two largest values. If the best value came from the child being excluded, the second-best value is used.
9. If (R\neq0), output `answer[R]`. If (R=0), output the maximum `answer[u]` over every vertex, because Daniel is free to choose his starting point.

### Why it works

Consider any valid walk starting at a fixed vertex. Because the graph is a tree, every edge that is not on the path from the starting vertex to the final vertex must be crossed an even number of times. Every edge on that path must be crossed an odd number of times. For an off-path edge, the best possible choice is exactly the closed contribution (C). For a path edge, the best possible choice is exactly the open contribution (O). At every vertex, only one incident direction can contain the final endpoint, so the DP needs to replace at most one closed contribution by an open contribution. The values (F) and (G) capture precisely these two possibilities inside every directed component. Rerooting makes the same statement available from every possible starting vertex, so `answer[u]` is optimal for that start, and taking the maximum is correct when (R=0).

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    graph = [[] for _ in range(n)]

    for _ in range(n - 1):
        u, v, a = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append((v, a))
        graph[v].append((u, a))

    R = int(input()) - 1

    # Root the tree at vertex 0.
    parent = [-1] * n
    parent_w = [0] * n
    order = [0]
    parent[0] = -2

    for v in order:
        for to, w in graph[v]:
            if to == parent[v]:
                continue
            parent[to] = v
            parent_w[to] = w
            order.append(to)

    # down_f[v] = F(v -> parent[v])
    # down_g[v] = G(v -> parent[v])
    down_f = [0] * n
    down_g = [0] * n

    for v in reversed(order):
        total = 0
        best_delta = 0

        for to, w in graph[v]:
            if parent[to] != v:
                continue

            even = w - (w & 1)

            if even == 0:
                closed = 0
            else:
                closed = even + down_f[to]

            odd = w if (w & 1) else w - 1
            opened = odd + down_g[to]

            total += closed
            delta = opened - closed
            if delta > best_delta:
                best_delta = delta

        down_f[v] = total
        down_g[v] = total + best_delta

    # up_f[v] = F(parent[v] -> v)
    # up_g[v] = G(parent[v] -> v)
    up_f = [0] * n
    up_g = [0] * n

    answer = [0] * n

    for v in order:
        total = 0

        # Store the two largest O - C values.
        best1 = 0
        best2 = 0
        best_source = -1

        for to, w in graph[v]:
            if to == parent[v]:
                even = w - (w & 1)

                if even == 0:
                    closed = 0
                else:
                    closed = even + up_f[v]

                odd = w if (w & 1) else w - 1
                opened = odd + up_g[v]
            else:
                even = w - (w & 1)

                if even == 0:
                    closed = 0
                else:
                    closed = even + down_f[to]

                odd = w if (w & 1) else w - 1
                opened = odd + down_g[to]

            total += closed
            delta = opened - closed

            if delta > best1:
                best2 = best1
                best1 = delta
                best_source = to
            elif delta > best2:
                best2 = delta

        answer[v] = total + best1

        # Build messages from v to each child.
        for to, w in graph[v]:
            if parent[to] != v:
                continue

            even = w - (w & 1)

            if even == 0:
                child_closed = 0
            else:
                child_closed = even + down_f[to]

            out_f = total - child_closed

            if best_source == to:
                best_delta = best2
            else:
                best_delta = best1

            out_g = out_f + best_delta

            up_f[to] = out_f
            up_g[to] = out_g

    if R == -1:
        print(max(answer))
    else:
        print(answer[R])

if __name__ == "__main__":
    solve()
```

The adjacency list stores each tree edge in both directions. The temporary root is vertex 1, and `parent` together with `order` gives an iterative DFS order. Iteration rather than recursive DFS avoids Python recursion-depth problems on a path containing (10^5) vertices.

The first reverse traversal computes `down_f` and `down_g`. For a child edge, `closed` represents taking the child subtree as a round trip, while `opened` represents making the final endpoint lie inside that subtree. Their difference tells us exactly how much is gained by choosing that child as the final direction.

The second traversal computes the opposite directed messages. At each vertex, `total` contains all closed excursions from every incident direction. The two largest `delta = opened - closed` values are retained because when constructing the message toward one child, that child must be excluded. Keeping two maxima avoids scanning all other neighbors separately, preserving linear complexity.

All scores can exceed 32-bit integer range. In fact, there can be (10^5-1) edges and each toughness can be close to (10^9), so Python's arbitrary-precision integers are convenient here. The parity calculations use `w & 1`, and `w - (w & 1)` gives the largest even value not exceeding `w`.

The expression `answer[v] = total + best1` is also safe when `best1` is zero. That corresponds to ending at the current vertex instead of entering another component. This handles leaves and cases where every possible open direction would make the score worse.

## Worked Examples

### Sample 1

The tree is a star centered at vertex 1, with edge toughnesses (3,4,3,4). Daniel may choose his starting vertex because (R=0).

For the center, every branch can be used as a closed excursion. A toughness-3 edge contributes 2 when Daniel returns, while a toughness-4 edge contributes 4. Thus the closed value at the center is (2+4+2+4=12). Choosing a toughness-3 branch as the final direction changes its contribution from 2 to 3, increasing the score by 1.

| Vertex | Closed value | Best (O-C) | Best start score |
| --- | --- | --- | --- |
| 1 | 12 | 1 | 13 |
| 2 | 12 | 2 | 14 |
| 3 | 12 | 0 | 12 |
| 4 | 12 | 2 | 14 |
| 5 | 12 | 0 | 12 |

The maximum is 14. One optimal walk starts at vertex 2, crosses the edge (2-1) three times, and uses the remaining branches as closed excursions. The rerooting calculation finds this possibility even though the implementation initially rooted the tree at vertex 1. The official sample gives output `14`.

### Sample 2

Here the tree is a path with toughnesses (2,1,2,1), and Daniel must start at vertex 1.

The closed contribution of a toughness-2 edge is 2. A toughness-1 edge contributes zero to a closed excursion because it cannot be crossed twice. Starting at vertex 1, the first edge can be crossed twice, giving two points. Daniel can then cross the toughness-1 edge once and stop, adding one point. Alternatively, after reaching vertex 3, he can use the toughness-2 edge in the appropriate direction, reaching the same optimum of 4.

| Edge | Toughness | Best even usage | Best odd usage |
| --- | --- | --- | --- |
| 1-2 | 2 | 2 | 1 |
| 2-3 | 1 | 0 | 1 |
| 3-4 | 2 | 2 | 1 |
| 4-5 | 1 | 0 | 1 |

For the fixed start at vertex 1, the DP obtains `answer[1] = 4`. The official sample output is `4`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | The tree is traversed a constant number of times, and every adjacency entry is processed a constant number of times. |
| Space | (O(n)) | The adjacency list and the parent, DP, message, and answer arrays all require linear space. |

With (n\le10^5), linear processing means only a few million adjacency operations, which is appropriate for the 2-second limit. The memory usage is also linear and comfortably below the 512 MB limit specified by the problem.

## Test Cases

The following test harness uses the same rerooting implementation as the submitted solution and checks the official samples together with cases targeting parity, toughness one, free starting position, and the maximum allowed tree size.

```python
import sys
import io

def solve_data(data: str) -> str:
    it = iter(data.split())
    n = int(next(it))

    graph = [[] for _ in range(n)]

    for _ in range(n - 1):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        w = int(next(it))
        graph[u].append((v, w))
        graph[v].append((u, w))

    R = int(next(it)) - 1

    parent = [-1] * n
    parent_w = [0] * n
    order = [0]
    parent[0] = -2

    for v in order:
        for to, w in graph[v]:
            if to == parent[v]:
                continue
            parent[to] = v
            parent_w[to] = w
            order.append(to)

    down_f = [0] * n
    down_g = [0] * n

    for v in reversed(order):
        total = 0
        best = 0

        for to, w in graph[v]:
            if parent[to] != v:
                continue

            even = w - (w & 1)
            closed = 0 if even == 0 else even + down_f[to]

            odd = w if (w & 1) else w - 1
            opened = odd + down_g[to]

            total += closed
            best = max(best, opened - closed)

        down_f[v] = total
        down_g[v] = total + best

    up_f = [0] * n
    up_g = [0] * n
    ans = [0] * n

    for v in order:
        total = 0
        best1 = 0
        best2 = 0
        source = -1

        for to, w in graph[v]:
            if to == parent[v]:
                even = w - (w & 1)
                closed = 0 if even == 0 else even + up_f[v]

                odd = w if (w & 1) else w - 1
                opened = odd + up_g[v]
            else:
                even = w - (w & 1)
                closed = 0 if even == 0 else even + down_f[to]

                odd = w if (w & 1) else w - 1
                opened = odd + down_g[to]

            total += closed
            delta = opened - closed

            if delta > best1:
                best2 = best1
                best1 = delta
                source = to
            elif delta > best2:
                best2 = delta

        ans[v] = total + best1

        for to, w in graph[v]:
            if parent[to] != v:
                continue

            even = w - (w & 1)
            child_closed = 0 if even == 0 else even + down_f[to]

            out_f = total - child_closed
            best_delta = best2 if source == to else best1
            out_g = out_f + best_delta

            up_f[to] = out_f
            up_g[to] = out_g

    if R == -1:
        return str(max(ans))
    return str(ans[R])

def run(inp: str) -> str:
    return solve_data(inp).strip()

# Official samples
assert run("""5
1 2 3
1 3 4
1 4 3
1 5 4
0
""") == "14", "sample 1"

assert run("""5
1 2 2
2 3 1
3 4 2
4 5 1
1
""") == "4", "sample 2"

assert run("""7
1 2 1
1 3 1
2 4 9
2 5 9
3 6 9
3 7 9
1
""") == "18", "sample 3"

assert run("""1
1
""") == "0", "sample 4"

# Custom: a single toughness-one edge can be crossed once.
assert run("""2
1 2 1
1
""") == "1", "toughness one"

# Custom: a toughness-one gateway can lead to a large final path.
assert run("""3
1 2 1
2 3 9
1
""") == "10", "one-way gateway"

# Custom: all equal even capacities, with free choice of start.
assert run("""5
1 2 2
1 3 2
1 4 2
1 5 2
0
""") == "8", "all equal capacities"

# Maximum-size test: 100000 vertices, every edge has toughness one.
# Starting at one leaf, Daniel can go through the center to another leaf.
n = 100000
parts = [str(n)]
for v in range(2, n + 1):
    parts.append(f"1 {v} 1")
parts.append("0")
large_input = "\n".join(parts) + "\n"

assert run(large_input) == "2", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `0` | Minimum-size tree with no edges |
| `2 / 1 2 1 / R=1` | `1` | Boundary case where an edge can only be used once |
| `3 / 1-2:1, 2-3:9 / R=1` | `10` | A toughness-one edge leading into a useful subtree |
| Four-edge star, all toughness `2`, `R=0` | `8` | Equal capacities and choosing the best starting vertex |
| 100000-vertex star, all toughness `1`, `R=0` | `2` | Maximum (n), large input, and rerooting over many neighbors |

## Edge Cases

For the one-vertex tree

```
1
1
```

the adjacency list is empty. Both the closed and open DP values are zero, so `answer[0]` is zero. Since (R=1), the program prints `0`. No special-case branch is needed beyond the normal DP.

For

```
2
1 2 1
1
```

the only edge has best even usage zero and best odd usage one. Starting at vertex 1, the closed value is zero, while the open value through the edge is one. The DP chooses the open direction, producing `1`. This is exactly why toughness-one edges must not simply be discarded.

For

```
3
1 2 1
2 3 9
1
```

the edge (1-2) cannot be used as a closed excursion, so its closed contribution is zero. Its open contribution is (1+G(2\to1)). Inside the component rooted at vertex 2, the toughness-nine edge can be used nine times as the final edge, giving (G(2\to1)=9). The resulting value at vertex 1 is (1+9=10). The DP captures the fact that an edge that is useless for a round trip can still be extremely valuable as part of the final path.

For

```
3
1 2 3
1 3 3
0
```

the center has two toughness-three edges. If the walk starts at the center and ends at a leaf, one edge can be used three times while the other can only be used twice, giving five. If the walk starts at one leaf and ends at the other, both edges are on the endpoint path and each can be used three times, giving six. The first bottom-up pass alone cannot discover this because it is rooted at vertex 1, but the top-down rerooting pass computes the message from the center toward each leaf. The resulting `answer` for the leaf is six, and (R=0) selects that maximum.

The provided third sample contains two toughness-one edges immediately below the starting vertex and four toughness-nine edges below them. A toughness-one edge cannot support a return trip, but it can be the first edge of the final path. Once Daniel crosses it, he can use a toughness-nine edge nine times and finish there. The rerooting DP gives the required score of `18`, matching the official sample.
