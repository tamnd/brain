---
title: "CF 102277G - World Cup Fever"
description: "The problem places two soccer teams in the Cartesian plane. Each team has (n) players, so there are (2n) distinct points in total. Player positions never change."
date: "2026-08-16T19:37:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102277
codeforces_index: "G"
codeforces_contest_name: "UCF Locals 2018"
rating: 0
weight: 102277
solve_time_s: 98
verified: true
draft: false
---

[CF 102277G - World Cup Fever](https://codeforces.com/problemset/problem/102277/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem places two soccer teams in the Cartesian plane. Each team has (n) players, so there are (2n) distinct points in total. Player positions never change.

A player can pass the ball directly to another player only when both players belong to the same team and no other player, from either team, lies strictly between them on the straight line segment connecting the two players. The pass distance does not matter.

The ball starts at Player 1 of Team 1, and the goal is to reach Player (n) of Team 1 using as few passes as possible. If there is no sequence of legal passes that reaches the target, the answer is (-1).

The original contest statement gives (2 \le n \le 11), while every coordinate is an integer from 1 through 999 and all (2n) player positions are distinct. The time limit is 1 second and the memory limit is 256 MB. Since there are at most 22 vertices, even an (O(n^3)) algorithm performs only a few thousand geometric checks. The real issue is not the size of the graph, but recognizing that the passing rules form a shortest-path problem rather than requiring geometric search.

There are several edge cases where a careless implementation can fail. First, an opponent exactly between two teammates blocks the pass. For example,

```
2
1 1 3 1
2 1 2 2
```

has Team 1 at ((1,1)) and ((3,1)), with an opponent at ((2,1)). The correct output is

```
-1
```

because the only possible Team 1 pass is blocked. A test that checks only whether the three points are collinear, without checking whether the third point lies between the endpoints, can incorrectly reject or accept the wrong segment depending on its implementation.

Second, a teammate between two players also blocks the direct pass, but that teammate can become an intermediate vertex. For example,

```
3
1 1 3 1 5 1
1 3 3 3 5 3
```

has Team 1 players at ((1,1),(3,1),(5,1)). Player 1 cannot pass directly to Player 3 because Player 2 is between them, but Player 1 can pass to Player 2 and then Player 2 can pass to Player 3. The correct output is

```
2
```

A careless solution that treats "there is a teammate between them" as meaning the target is unreachable would miss this path.

Third, collinearity alone is not enough. A player lying on the same infinite line but outside the segment does not block a pass. For example,

```
2
1 1 3 1
5 1 5 2
```

has no player between ((1,1)) and ((3,1)), so the correct output is

```
1
```

A solution that checks only the cross product and forgets the "between" condition would incorrectly declare this pass blocked.

## Approaches

The most direct brute-force idea is to enumerate every possible sequence of passes from Player 1 until Player (n) is reached. This is correct because every legal solution is exactly such a sequence of graph edges. Since repeating a vertex can never improve a shortest path, we can restrict attention to simple paths. With at most 22 players, there can be as many as

[
\sum_{k=0}^{20} P(20,k)
]

different simple paths from the start to the target, where (P(20,k)=20!/(20-k)!). This quantity is on the order of (20!), roughly (6.6\cdot10^{18}), so enumerating paths is completely impractical.

The brute-force works because it explores exactly the possible passing sequences, but fails because the number of sequences grows factorially. The key observation is that the geometric part of the problem is only needed to determine whether a direct pass exists. Once those legal passes are known, the problem becomes an ordinary unweighted shortest-path problem.

We can create one graph vertex for every player. Connect two vertices when the corresponding players are teammates and no player lies strictly between them. Every legal pass costs exactly one, so the minimum number of passes is precisely the shortest-path distance between Team 1 Player 1 and Team 1 Player (n).

Because there are at most 22 vertices, we can simply test every pair of players and scan every third player to decide whether the pair is connected. This takes (O(n^3)) time. After the graph is built, BFS finds the shortest path in (O(n^2)), which is negligible compared with the geometric preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(20!)) path exploration in the worst case | (O(n)) recursion depth | Too slow |
| Optimal | (O(n^3)) | (O(n^2)) | Accepted |

## Algorithm Walkthrough

1. Store all (2n) players in one array. The first (n) players belong to Team 1 and the remaining (n) players belong to Team 2. This lets every geometric check work with one common indexing scheme.
2. For every pair of distinct players (u,v), first check whether they belong to the same team. If they are on different teams, there can never be an edge between them because a pass is allowed only between teammates.
3. For a same-team pair, inspect every other player (w). Compute the cross product

[
(v-u)\times(w-u).
]

If it is nonzero, (w) is not on the line through (u) and (v), so it cannot block the pass.

1. When the cross product is zero, check whether (w) lies inside the segment from (u) to (v). With distinct points, checking that its coordinates lie within the coordinate ranges of the endpoints is sufficient after collinearity has already been established. If such a player exists, the direct pass is blocked.
2. If no player blocks the segment, add an undirected graph edge between (u) and (v). Passing works in either direction, so the graph is undirected.
3. Run BFS from vertex 0, representing Team 1 Player 1. Initialize its distance to zero and every other distance to (-1). When BFS first reaches a vertex, its distance is the minimum number of passes needed to reach it because every graph edge has the same cost.
4. Return the distance of vertex (n-1), representing Team 1 Player (n). If BFS never reaches it, the stored value remains (-1), which is exactly the required result.

Why it works: the graph contains an edge exactly when the corresponding pass is legal. Thus every sequence of legal passes corresponds to a graph path, and every graph path corresponds to a valid sequence of passes. Since each pass has cost one, minimizing the number of passes is identical to finding the shortest unweighted graph path. BFS returns that shortest distance, so the algorithm cannot produce a smaller or larger valid answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(n, team1, team2):
    points = team1 + team2
    total = 2 * n

    graph = [[] for _ in range(total)]

    def blocked(a, b):
        ax, ay = points[a]
        bx, by = points[b]

        dx = bx - ax
        dy = by - ay

        for c in range(total):
            if c == a or c == b:
                continue

            cx, cy = points[c]

            cross = dx * (cy - ay) - dy * (cx - ax)
            if cross != 0:
                continue

            if min(ax, bx) <= cx <= max(ax, bx) and \
               min(ay, by) <= cy <= max(ay, by):
                return True

        return False

    for i in range(total):
        for j in range(i + 1, total):
            same_team = (i < n) == (j < n)
            if not same_team:
                continue

            if not blocked(i, j):
                graph[i].append(j)
                graph[j].append(i)

    dist = [-1] * total
    dist[0] = 0
    queue = [0]
    head = 0

    while head < len(queue):
        u = queue[head]
        head += 1

        if u == n - 1:
            return dist[u]

        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)

    return -1

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    pos = 0

    n = data[pos]
    pos += 1

    team1 = []
    for _ in range(n):
        x = data[pos]
        y = data[pos + 1]
        pos += 2
        team1.append((x, y))

    team2 = []
    for _ in range(n):
        x = data[pos]
        y = data[pos + 1]
        pos += 2
        team2.append((x, y))

    print(solve_case(n, team1, team2))

if __name__ == "__main__":
    solve()
```

The implementation first combines both teams into `points`. Indexes `0` through `n - 1` are Team 1, while indexes `n` through `2 * n - 1` are Team 2. This makes the identity of a player's team a simple comparison with `n`.

The `blocked` function performs the geometric part of the algorithm. The cross product uses only integer arithmetic, so there is no floating-point precision problem. With coordinates bounded by 999, the intermediate values are tiny in Python and would also fit comfortably in standard 64-bit integers.

The range check comes only after `cross == 0`. This ordering matters because a coordinate-range test by itself does not establish that the point lies on the segment. Collinearity plus being inside both coordinate ranges gives exactly the required "strictly between" condition, since the endpoints themselves are skipped explicitly.

The graph construction checks each unordered pair once by using `j` from `i + 1` onward. Whenever the pass is legal, both directions are inserted because a pass between two teammates is reversible.

BFS uses a list plus an integer `head` instead of repeatedly removing the first element. Removing from the front of a Python list costs (O(n)), while advancing `head` keeps each queue operation constant time. The early return when the target is dequeued is valid because BFS processes vertices in nondecreasing distance order.

The input statement contains one test case rather than a test-case count, so the solution reads exactly one value of (n) and the two coordinate lists. The use of `sys.stdin.buffer.read()` is safe here and keeps parsing fast.

## Worked Examples

The original 2018 contest statement does not provide sample input/output pairs, so the following traces use constructed examples that exercise the graph construction and BFS.

### Example 1

```
3
1 1 3 1 5 1
1 3 3 3 5 3
```

Team 1 consists of three players on the horizontal line (y=1). The middle player blocks a direct pass from Player 1 to Player 3.

| Player processed | Legal new edge | Distance |
| --- | --- | --- |
| 1 | 1 -> 2 | 0 |
| 2 | 2 -> 3 | 1 |
| 3 | target reached | 2 |

The direct edge from Player 1 to Player 3 is absent because Player 2 lies strictly between them. BFS instead follows `1 -> 2 -> 3`, producing the minimum of two passes. The second team's players are on a parallel line, so they do not block any of these horizontal Team 1 segments.

### Example 2

```
2
1 1 3 1
2 1 2 2
```

The only two Team 1 players are ((1,1)) and ((3,1)). The Team 2 player at ((2,1)) lies directly between them.

| Player pair | Same team | Blocked | Edge |
| --- | --- | --- | --- |
| 1, 2 | Yes | Yes, opponent at (2,1) | No |

BFS starts at Player 1, finds no outgoing edge, and the target remains at distance (-1). This demonstrates that a player from the other team blocks a pass just as effectively as a teammate.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^3)) | There are (O(n^2)) player pairs, and each pair checks at most (2n) possible blockers. |
| Space | (O(n^2)) | The passing graph contains at most (O(n^2)) edges and the BFS arrays are linear. |

With (n \le 11), there are at most 22 players, so the geometric construction performs at most a few thousand blocker checks. The (O(n^3)) bound is easily within the 1 second time limit, and the (O(n^2)) graph uses only a tiny fraction of the 256 MB memory limit.

## Test Cases

```python
# helper: run the solution logic on an input string
import sys
import io

def solve_case(n, team1, team2):
    points = team1 + team2
    total = 2 * n

    graph = [[] for _ in range(total)]

    def blocked(a, b):
        ax, ay = points[a]
        bx, by = points[b]

        dx = bx - ax
        dy = by - ay

        for c in range(total):
            if c == a or c == b:
                continue

            cx, cy = points[c]
            cross = dx * (cy - ay) - dy * (cx - ax)

            if cross == 0 and \
               min(ax, bx) <= cx <= max(ax, bx) and \
               min(ay, by) <= cy <= max(ay, by):
                return True

        return False

    for i in range(total):
        for j in range(i + 1, total):
            if (i < n) != (j < n):
                continue

            if not blocked(i, j):
                graph[i].append(j)
                graph[j].append(i)

    dist = [-1] * total
    dist[0] = 0
    queue = [0]
    head = 0

    while head < len(queue):
        u = queue[head]
        head += 1

        if u == n - 1:
            return dist[u]

        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)

    return -1

def run(inp: str) -> str:
    data = list(map(int, inp.split()))
    pos = 0

    n = data[pos]
    pos += 1

    team1 = []
    for _ in range(n):
        team1.append((data[pos], data[pos + 1]))
        pos += 2

    team2 = []
    for _ in range(n):
        team2.append((data[pos], data[pos + 1]))
        pos += 2

    return str(solve_case(n, team1, team2))

# The original 2018 statement has no sample input/output pairs.

# Minimum-size input, direct pass.
assert run(
    """2
1 1 3 1
1 3 3 3
"""
) == "1", "minimum-size direct pass"

# Blocked direct pass, and no alternate teammate exists.
assert run(
    """2
1 1 3 1
2 1 2 2
"""
) == "-1", "opponent blocks the only pass"

# Teammate blocks the direct pass but provides an intermediate route.
assert run(
    """3
1 1 3 1 5 1
1 3 3 3 5 3
"""
) == "2", "intermediate teammate"

# Player on the same infinite line but outside the segment does not block.
assert run(
    """2
1 1 3 1
5 1 5 2
"""
) == "1", "collinear point outside segment"

# Maximum-size case: 22 players, Team 1 lies on y=1 and Team 2 on y=2.
# Adjacent Team 1 players can pass, so reaching Player 11 needs 10 passes.
team1 = " ".join(f"{x} 1" for x in range(1, 12))
team2 = " ".join(f"{x} 2" for x in range(1, 12))
assert run(f"11\n{team1}\n{team2}\n") == "10", "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=2`, four distinct players with no blocker | `1` | Minimum-size graph and direct edge |
| `n=2`, opponent exactly between the two teammates | `-1` | Blocking by the other team |
| `n=3`, teammate between source and target | `2` | Intermediate vertices and shortest path |
| `n=2`, collinear player outside the segment | `1` | Correct segment boundary handling |
| `n=11`, 22 players on two parallel lines | `10` | Maximum number of players and repeated BFS transitions |

## Edge Cases

For the minimum-size case

```
2
1 1 3 1
1 3 3 3
```

there are only four vertices. Team 1's two players have no player between them, so the graph contains the edge from vertex 0 to vertex 1. BFS initializes the source at distance zero, discovers the target at distance one, and returns `1`. There is no assumption in the implementation that an intermediate teammate must exist.

For the blocked-segment case

```
2
1 1 3 1
2 1 2 2
```

the pair of Team 1 players has direction vector ((2,0)). The opponent at ((2,1)) gives a cross product of zero and lies within both endpoint coordinate ranges, so `blocked` returns true. No graph edge is added. BFS therefore leaves the target at `-1`, giving the correct answer.

For the intermediate-player case

```
3
1 1 3 1 5 1
1 3 3 3 5 3
```

the pair ((1,1),(5,1)) is blocked by ((3,1)), so there is no direct edge between Players 1 and 3. The adjacent pairs ((1,1),(3,1)) and ((3,1),(5,1)) have no player strictly between their endpoints, so both edges are present. BFS reaches Player 2 at distance one and Player 3 at distance two.

For the collinear-outside-the-segment case

```
2
1 1 3 1
5 1 5 2
```

the point ((5,1)) is collinear with the Team 1 pair, but it lies outside the segment from ((1,1)) to ((3,1)). The range check rejects it as a blocker. The Team 1 edge remains in the graph, and BFS returns `1`.

For the maximum-size case, there are 22 players, which is the largest graph permitted by the statement:

```
11
1 1 2 1 3 1 4 1 5 1 6 1 7 1 8 1 9 1 10 1 11 1
1 2 2 2 3 2 4 2 5 2 6 2 7 2 8 2 9 2 10 2 11 2
```

Every adjacent Team 1 pair has a clear segment, while a non-adjacent pair is blocked by one of the Team 1 players between its endpoints. BFS consequently walks through all eleven Team 1 players in order, reaching Player 11 after 10 passes. The test also confirms that the implementation remains straightforward at the largest possible input size.
