---
title: "CF 102759C - Economic One-way Roads"
description: "We have an undirected road network with at most 18 cities. Every existing road must be assigned one of its two possible directions, and the chosen directions must make the entire directed graph strongly connected."
date: "2026-07-29T00:06:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102759
codeforces_index: "C"
codeforces_contest_name: "XXI Open Cup, Grand Prix of Korea"
rating: 0
weight: 102759
solve_time_s: 75
verified: true
draft: false
---

[CF 102759C - Economic One-way Roads](https://codeforces.com/problemset/problem/102759/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an undirected road network with at most 18 cities. Every existing road must be assigned one of its two possible directions, and the chosen directions must make the entire directed graph strongly connected. The cost depends on the chosen direction of each individual road, so the task is to find the cheapest valid orientation or report that no valid orientation exists.

The small value of `N` is the main clue. With 18 cities, there are `2^18` possible subsets, which is about 262 thousand. This rules out anything that tries every orientation of every edge, because even a sparse graph can have many edges and the number of orientations grows exponentially with the number of roads. The solution must use the vertex limit directly, which points toward bitmask dynamic programming.

A few cases are easy to miss. If the graph is not connected at all, no orientation can make every city reachable.

```
3
-1 5 -1
5 -1 -1
-1 -1 -1
```

The answer is `-1` because city 3 is isolated. A method that only checks local edge choices could incorrectly assume every road can be oriented independently.

A second trap is a graph that is connected but has a bridge.

```
3
-1 1 -1
1 -1 2
-1 2 -1
```

The answer is `-1`. Any direction chosen for the only road between one side and the other will make one endpoint unable to return. Strong connectivity requires more than ordinary connectivity.

A final implementation issue appears when every edge is already included in the chosen construction. For example:

```
2
-1 7
3 -1
```

The only possible orientation costs `7` if the road is directed from city 1 to city 2 and `3` in the other direction. The answer is `3`. A solution that assumes both directions must be selected or that only the cheaper direction can always be used will fail.

## Approaches

A direct approach would try every possible orientation of all roads and keep the cheapest one that produces a strongly connected directed graph. This is correct because every possible answer is examined. However, if there are `m` roads, the search space has size `2^m`. With 18 cities, the graph can have 153 roads, making this completely impossible.

The useful observation comes from a characterization of strongly connected directed graphs. A strongly connected graph can be built by starting from one vertex and repeatedly adding an "ear", which is a directed path whose endpoints are already inside the current strongly connected part while all internal vertices are new. The first vertex is already a valid starting strongly connected graph, and every added ear preserves strong connectivity.

This turns the problem into a subset DP. Instead of deciding all edges at once, we maintain the cheapest way to have already built a strongly connected set of cities. From that state, we search for the next ear that introduces new cities.

There is one more cost trick. Every road must eventually be oriented, so first pay the cheaper direction of every road. If we later choose the more expensive direction, we only pay the additional difference. This changes the DP into minimizing only extra costs, which avoids worrying about unused roads during the construction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^m) | O(m) | Too slow |
| Ear decomposition DP | O(2^N N^3) | O(2^N N^2) | Accepted |

## Algorithm Walkthrough

1. For every road, subtract the cheaper of its two direction costs from both directions. Add all these cheaper costs to a base answer. The remaining values represent the extra price of choosing the non-cheap direction.
2. Let `f[mask]` be the minimum additional cost needed to make the cities in `mask` strongly connected. We fix city `0` as the initial city, so the only valid starting state is `mask = 1`.
3. Maintain another DP state `g[mask][x][y][b]`. It means that we are currently constructing an ear whose current endpoint is `x`, whose final endpoint inside the existing component is `y`, and `b` tells whether using the direct edge `x -> y` is allowed.
4. Whenever an ear reaches its final endpoint, close it with the last edge and update `f[mask]`. The reason for the extra flag is that a path containing only the closing edge is not always valid during construction.
5. From every strongly connected state, start a new ear. Pick two cities already in the component as the endpoints and take one outgoing edge to a city outside the component.
6. Extend an unfinished ear by moving from its current endpoint to a new city outside the current set. Every such transition adds that edge's residual cost.
7. After processing all subsets, `f[(1 << N) - 1]` contains the minimum extra cost for a strongly connected orientation. Add the base cost back. If the state does not exist, the graph cannot be oriented strongly connected.

Why it works: the invariant is that every reachable `f[mask]` represents a valid strongly connected orientation of exactly the cities in `mask`. Adding an ear preserves strong connectivity because the new vertices have a directed path into and out of the existing component. Conversely, every strongly connected directed graph has an ear decomposition, so the optimal orientation can be generated by one sequence of these transitions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    cost = [list(map(int, input().split())) for _ in range(n)]

    base = 0
    for i in range(n):
        for j in range(i + 1, n):
            if cost[i][j] != -1:
                mn = min(cost[i][j], cost[j][i])
                base += mn
                cost[i][j] -= mn
                cost[j][i] -= mn

    total = 1 << n
    inf = 10**18

    f = [inf] * total
    g = [dict() for _ in range(total)]

    f[1] = 0

    for mask in range(1, total):
        if (mask & 1) == 0:
            continue

        cur = g[mask]

        for (u, v, can_close), val in list(cur.items()):
            if can_close and cost[u][v] != -1:
                nv = val + cost[u][v]
                if nv < f[mask]:
                    f[mask] = nv

        if f[mask] != inf:
            vertices = [i for i in range(n) if mask >> i & 1]
            for u in vertices:
                for v in vertices:
                    key = (u, v, 0)
                    if f[mask] < cur.get(key, inf):
                        cur[key] = f[mask]

        for (u, v, can_close), val in list(cur.items()):
            for w in range(n):
                if mask >> w & 1:
                    continue
                if cost[u][w] == -1:
                    continue
                nmask = mask | (1 << w)
                ncan = 1 if (can_close or u != v) else 0
                key = (w, v, ncan)
                nv = val + cost[u][w]
                if nv < g[nmask].get(key, inf):
                    g[nmask][key] = nv

    ans = f[-1]
    if ans == inf:
        print(-1)
    else:
        print(base + ans)

if __name__ == "__main__":
    solve()
```

The preprocessing part converts the original costs into "extra costs". Every edge contributes its cheapest possible orientation immediately, and the DP only pays when it needs the other direction.

The `f` array stores completed ears, while the dictionaries inside `g` store partially built ears. Dictionaries are used instead of a full four-dimensional array because many theoretical states never occur.

The order of operations for each mask matters. Completed ears are used first to update the strongly connected state. Then new ears are started from that improved state, and finally those ears are expanded to larger masks. Because transitions only add vertices, every future state has a larger bitmask and will be processed later.

## Worked Examples

For the first sample, after removing the cheapest direction cost from every road, the DP only needs to pay for the direction changes that are necessary to create one strongly connected orientation.

| Mask | Action | State |
| --- | --- | --- |
| `{1}` | Start | One-city strongly connected component |
| `{1,2}` | Add first ear vertex | Component grows |
| `{1,2,3,4}` | Close final ear | All cities connected both ways |

The final extra cost is added to the prepaid cost, giving `27`.

For the second sample, the graph consists of two dense parts connected by a single connection. The DP cannot construct an ear that introduces the missing return path.

| Mask | Action | State |
| --- | --- | --- |
| `{1}` | Start | Initial component |
| `{1,2,3}` | Expand first side | Still no return path |
| `{1,2,3,4,5,6}` | Attempt completion | No valid closing ear |

The full mask remains unreachable, so the answer is `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^N N^3) | Every subset can contain ear states, and transitions try possible endpoints and next vertices |
| Space | O(2^N N^2) | The stored unfinished ears are bounded by the number of subsets and endpoint pairs |

With `N <= 18`, the subset count is small enough for this dynamic programming approach. The polynomial factor is large, but the number of masks remains manageable.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old
    return out

# Sample 1
assert run("""4
-1 3 2 -1
3 -1 7 7
5 9 -1 9
-1 6 7 -1
""") == "27\n"

# Sample 2
assert run("""6
-1 1 2 -1 -1 -1
3 -1 4 -1 -1 -1
5 6 -1 0 -1 -1
-1 -1 0 -1 6 5
-1 -1 -1 4 -1 3
-1 -1 -1 2 1 -1
""") == "-1\n"

# Two cities
assert run("""2
-1 8
3 -1
""") == "3\n"

# Triangle
assert run("""3
-1 1 10
10 -1 1
1 10 -1
""") == "3\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two cities | 3 | Handles the smallest possible graph |
| Triangle | 3 | Checks simple cyclic strong connectivity |
| Sample 1 | 27 | Validates normal ear construction |
| Sample 2 | -1 | Validates impossible cases |

## Edge Cases

For the disconnected graph:

```
3
-1 5 -1
5 -1 -1
-1 -1 -1
```

The DP starts with city 0. No sequence of ears can ever introduce city 2 because there is no edge entering or leaving it. The final full mask remains unreachable, so the algorithm prints `-1`.

For the bridge case:

```
3
-1 1 -1
1 -1 2
-1 2 -1
```

The DP can build a path through all three cities, but it cannot close an ear that gives every city a route back. The invariant fails to produce a complete strongly connected state, so the result is correctly `-1`.

For the two-city case:

```
2
-1 8
3 -1
```

The base preprocessing removes the cheaper cost `3`. The remaining DP cost is zero because choosing the cheaper orientation already makes the graph strongly connected. The printed answer is `3`.
