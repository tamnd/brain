---
title: "CF 1404B - Tree Tag"
description: "We are given a tree where two players start on different vertices. Alice moves first. On each turn, Alice can jump to any vertex within distance da, and Bob can jump to any vertex within distance db. Distance is standard shortest path length in the tree."
date: "2026-06-14T17:13:28+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "games", "trees"]
categories: ["algorithms"]
codeforces_contest: 1404
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 668 (Div. 1)"
rating: 1900
weight: 1404
solve_time_s: 217
verified: true
draft: false
---

[CF 1404B - Tree Tag](https://codeforces.com/problemset/problem/1404/B)

**Rating:** 1900  
**Tags:** dfs and similar, dp, games, trees  
**Solve time:** 3m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree where two players start on different vertices. Alice moves first. On each turn, Alice can jump to any vertex within distance `da`, and Bob can jump to any vertex within distance `db`. Distance is standard shortest path length in the tree.

Alice’s goal is to eventually land on the same vertex as Bob at the end of some move sequence. If that never happens, Bob is considered to have escaped forever.

The key aspect is that movement is not local step-by-step. Each move allows a jump anywhere within a radius in the tree metric, which makes the game about reachability over large neighborhoods rather than adjacency.

The constraints suggest a solution close to linear per test case, since the total number of vertices over all tests is at most 100000. Any solution that repeatedly explores the tree per move or simulates the game is immediately too slow.

A naive interpretation would simulate all possible positions after each move. That fails because each move expands to a large ball in the tree, and the branching factor becomes the whole tree in the worst case. Even representing reachable sets explicitly becomes quadratic.

A subtler failure mode appears if we only compare initial distance. For example, if Alice is slightly far from Bob initially but has much larger mobility, she may still catch him later due to structure of the tree. Conversely, Bob may escape even when initially close if his movement radius is much larger.

The critical missing ingredient in naive reasoning is that the tree structure limits how quickly distance can shrink or grow, and global structure, especially the diameter, constrains escape routes.

## Approaches

A brute-force simulation would track all vertices each player can reach after every turn. From each current position, we would expand to all nodes within `da` or `db` using BFS. Repeating this over turns leads to exploring large overlapping subtrees repeatedly. In the worst case, each move costs `O(n)`, and since the game may last many moves, this becomes unbounded under the problem’s time limit.

The key insight is that we do not need to simulate the game over time. The outcome depends only on a small set of structural quantities: the initial distance between players and the overall “width” of the tree, captured by its diameter.

The reasoning splits into three regimes.

If Alice can already reach Bob in one move, she wins immediately.

If Bob is relatively slow compared to Alice, meaning his maximum jump is not more than twice Alice’s, then Alice can always eventually close the gap regardless of structure. Intuitively, Alice reduces distance every second move at a rate that Bob cannot compensate for.

If Bob is significantly faster, he can try to run toward the farthest part of the tree. In that case, the only way Alice still wins is if the tree is too “small” for Bob to maintain separation, meaning the diameter is not large enough to support an escape corridor.

This reduces the problem to computing a single shortest path distance and the tree diameter.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) worst-case | O(n) | Too slow |
| Diameter + Distance Logic | O(n) per test | O(n) | Accepted |

## Algorithm Walkthrough

### 1. Compute the distance between Alice and Bob

We run a BFS or DFS to compute the shortest path distance `d(a, b)` in the tree. This directly determines whether Alice can capture Bob in one move.

If this distance is at most `da`, Alice immediately wins because she can jump directly onto Bob’s position.

### 2. Compute the diameter of the tree

We find the tree diameter using two BFS passes. First BFS from any node finds the farthest node `x`, then a second BFS from `x` finds the farthest distance `D`.

This diameter represents the maximum possible separation between any two nodes in the tree and serves as a bound on how far Bob can continuously retreat.

### 3. Check whether Bob is too fast relative to Alice

If `db <= 2 * da`, Alice always wins.

The intuition is that even if Bob moves optimally away, Alice can still reduce the effective distance over alternating turns. Bob cannot increase separation faster than Alice can neutralize it.

### 4. Handle the fast-Bob regime

If `db > 2 * da`, Bob can potentially maintain distance by always moving toward the most distant part of the tree.

In this case, Alice wins only if the tree is too small to allow sustained escape, i.e. the diameter satisfies `D <= 2 * da`.

If the diameter is larger than this, Bob can keep repositioning toward a far endpoint and prevent capture.

### 5. Combine conditions

Alice wins if any of the following holds:

- `d(a, b) <= da`
- `db <= 2 * da`
- `D <= 2 * da`

Otherwise Bob wins.

### Why it works

The core invariant is that Bob’s ability to avoid capture depends on maintaining a non-decreasing separation along a longest path in the tree. If the tree is “wide” enough (large diameter) and Bob is sufficiently faster than Alice, he can always reposition to preserve distance greater than Alice’s capture radius.

If Bob is not sufficiently faster, Alice’s alternating advantage ensures that any separation eventually collapses. The diameter condition becomes irrelevant in that regime because Bob cannot exploit global structure fast enough.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def bfs(start, g):
    n = len(g) - 1
    dist = [-1] * (n + 1)
    q = deque([start])
    dist[start] = 0
    far = start
    while q:
        v = q.popleft()
        for to in g[v]:
            if dist[to] == -1:
                dist[to] = dist[v] + 1
                q.append(to)
                if dist[to] > dist[far]:
                    far = to
    return far, dist

def distance(a, b, g):
    _, dist = bfs(a, g)
    return dist[b]

def diameter(g):
    x, _ = bfs(1, g)
    y, dist = bfs(x, g)
    return dist[y]

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n, a, b, da, db = map(int, input().split())
        g = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            u, v = map(int, input().split())
            g[u].append(v)
            g[v].append(u)

        d = distance(a, b, g)
        D = diameter(g)

        if d <= da:
            out.append("Alice")
        elif db <= 2 * da:
            out.append("Alice")
        elif D <= 2 * da:
            out.append("Alice")
        else:
            out.append("Bob")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation separates the logic into three independent measurements: Alice-Bob distance, tree diameter, and speed comparison. The BFS routine is reused both for distance queries and diameter computation to avoid duplicated traversal logic.

A common pitfall is recomputing distances repeatedly per test case. Here everything is computed in linear time per tree, ensuring the total complexity stays within limits.

## Worked Examples

### Example 1

Input:

```
4 3 2 1 2
1 2
1 3
1 4
```

We compute distance `d(3,2)=2`. Alice’s jump is `da=1`, so she cannot reach Bob immediately.

The diameter of this star-shaped tree is 2.

We check conditions:

| Quantity | Value |
| --- | --- |
| d(a,b) | 2 |
| da | 1 |
| db | 2 |
| D | 2 |

Since `db <= 2 * da` is `2 <= 2`, Alice wins immediately.

This demonstrates the regime where Bob is not fast enough to maintain separation even in a branching tree.

### Example 2

Input:

```
6 6 1 2 5
1 2
2 3
3 4
4 5
5 6
```

This is a path graph. The distance between endpoints is 5.

| Quantity | Value |
| --- | --- |
| d(a,b) | 5 |
| da | 2 |
| db | 5 |
| D | 5 |

Here `db > 2 * da` (5 > 4), and both the initial distance and diameter exceed Alice’s reach threshold.

Bob can always retreat toward the far endpoint, maintaining separation. This confirms Bob wins.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | Each BFS is linear in nodes and we run a constant number per test |
| Space | O(n) | adjacency list plus distance arrays |

The total sum of `n` over all tests is bounded by 100000, so the solution runs comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    from collections import deque

    def bfs(start, g):
        n = len(g) - 1
        dist = [-1] * (n + 1)
        q = deque([start])
        dist[start] = 0
        far = start
        while q:
            v = q.popleft()
            for to in g[v]:
                if dist[to] == -1:
                    dist[to] = dist[v] + 1
                    q.append(to)
                    if dist[to] > dist[far]:
                        far = to
        return far, dist

    def distance(a, b, g):
        _, dist = bfs(a, g)
        return dist[b]

    def diameter(g):
        x, _ = bfs(1, g)
        y, dist = bfs(x, g)
        return dist[y]

    t = int(input())
    out = []
    for _ in range(t):
        n, a, b, da, db = map(int, input().split())
        g = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            u, v = map(int, input().split())
            g[u].append(v)
            g[v].append(u)

        d = distance(a, b, g)
        D = diameter(g)

        if d <= da or db <= 2 * da or D <= 2 * da:
            out.append("Alice")
        else:
            out.append("Bob")

    return "\n".join(out) + "\n"

# provided samples
assert run("""4
4 3 2 1 2
1 2
1 3
1 4
6 6 1 2 5
1 2
6 5
2 3
3 4
4 5
9 3 9 2 5
1 2
1 6
1 9
1 3
9 5
7 9
4 8
4 3
11 8 11 3 3
1 2
11 9
4 9
6 5
2 10
3 2
5 9
8 3
7 4
7 10
""") == """Alice
Bob
Alice
Alice
"""

# minimum case
assert run("""1
2 1 2 1 1
1 2
""") == "Alice\n"

# line case
assert run("""1
5 1 5 1 1
1 2
2 3
3 4
4 5
""") == "Alice\n"

# fast Bob
assert run("""1
5 1 5 1 10
1 2
2 3
3 4
4 5
""") == "Bob\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimum tree | Alice | base adjacency capture |
| line graph | Alice | diameter edge behavior |
| fast Bob | Bob | high-speed escape regime |

## Edge Cases

A critical edge case occurs when Alice and Bob are already close but Bob has a large movement range. Even if Bob can move far, Alice may still win if the diameter is small enough to prevent sustained evasion. The condition `D <= 2 * da` captures this by limiting Bob’s ability to exploit long escape paths.

Another subtle case is when Bob is faster but the tree is highly unbalanced. Even then, if the diameter is small, Bob cannot repeatedly reset distance. The algorithm correctly classifies such cases as Alice wins.

Finally, in very small trees like a single edge, direct distance comparison dominates. The BFS distance check ensures correctness without relying on diameter reasoning.
