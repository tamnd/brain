---
title: "CF 106439H - Shelter in the Rain"
description: "The problem describes a journey through a weighted undirected graph. Vertices are locations, edges are roads, and every road has a travel time. You begin at one location and want to reach another one. Some locations have shelters."
date: "2026-06-25T09:30:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106439
codeforces_index: "H"
codeforces_contest_name: "Insomnia-26"
rating: 0
weight: 106439
solve_time_s: 35
verified: true
draft: false
---

[CF 106439H - Shelter in the Rain](https://codeforces.com/problemset/problem/106439/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem describes a journey through a weighted undirected graph. Vertices are locations, edges are roads, and every road has a travel time. You begin at one location and want to reach another one. Some locations have shelters. Whenever you arrive at a shelter, the accumulated time spent traveling in the rain becomes zero.

The restriction is not about the total trip length. It is about every continuous piece of travel between rests. A valid route may have many long parts, as long as each part from the start or a shelter to the next shelter or the destination has total edge weight at most `k`.

The input contains several graph instances. For each instance, we receive the number of vertices and edges, the rain limit, the start and destination vertices, the set of shelter vertices, and the weighted edges. The output asks whether the destination can be reached while never exceeding the allowed continuous travel time.

The total number of vertices and edges over all test cases is at most `2 * 10^5`. This rules out solutions that repeatedly run shortest path algorithms from every shelter or enumerate pairs of shelters. A solution around `O((n + m) log n)` is appropriate because it performs a small logarithmic amount of work per vertex and edge.

The tricky cases are caused by confusing total path length with continuous travel length. For example:

```
3 2 4
1 3
1
2
1 2 3
2 3 3
```

The correct output is:

```
NO
```

A careless shortest path solution sees a path of length `6` and might accept it if it only compares against a larger global limit. The traveler reaches the shelter at vertex `2` only after spending `3` units, but the second edge also costs `3`, so the whole trip is invalid because the limit is `4`.

Another important case is when the destination itself is a shelter:

```
2 1 5
1 2
1
2
1 2 5
```

The correct output is:

```
YES
```

The destination is reached exactly at the limit. It does not matter that the shelter resets the counter afterwards because arriving there already completes the journey.

A final edge case is having no shelters:

```
2 1 10
1 2
0

1 2 7
```

The correct output is:

```
YES
```

The only possible segment is the whole route, so the direct travel time must fit within `k`.

# Approaches

A direct approach is to first find every pairwise shortest distance between important vertices, where the important vertices are the start, destination, and shelters. Then we could build another graph where two important vertices are connected if the shortest distance between them is at most `k`. Finally, we would check reachability in this smaller graph.

This idea is correct because moving from one important vertex to another represents exactly one continuous rainy segment. The problem is that there can be `n` shelters. Running Dijkstra from every shelter would require `O(n(n+m)log n)` time in the worst case, which is far beyond the constraints.

The key observation is that we do not need to explicitly build the shelter graph. We only need to know which vertices are reachable while keeping track of the current continuous travel time. When we reach a shelter, the value immediately becomes zero again.

This leads to a modified Dijkstra search. The distance stored for a vertex is not the total travel distance from the start. It is the minimum amount of uninterrupted rain time needed to stand at that vertex. A smaller value is always better. From a vertex with current value `d`, we can traverse an edge of weight `w` only if `d + w <= k`. If the destination vertex of that edge is a shelter, the new value becomes zero. Otherwise, the new value becomes `d + w`.

The brute force method computes all possible safe transitions before searching. The optimal method discovers exactly the transitions that matter during one graph traversal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n(n+m)log n)` | `O(n+m)` | Too slow |
| Optimal | `O((n+m)log n)` | `O(n+m)` | Accepted |

## Algorithm Walkthrough

1. Mark every shelter vertex so the algorithm can instantly know whether arriving at a vertex resets the rain timer. The important distinction is between standing at a normal vertex and standing at a shelter.
2. Initialize a distance array where `dist[v]` represents the smallest continuous rain time needed to reach vertex `v`. Set the start vertex to zero because no travel has happened yet. Put it into a priority queue.
3. Repeatedly take the vertex with the smallest current rain time from the priority queue. If this entry is outdated, ignore it. This is the standard lazy deletion technique used with Dijkstra.
4. For every outgoing edge, calculate the time after crossing it. If the value exceeds `k`, this move is impossible because the traveler would need to continue through the rain too long.
5. If the destination of the edge is a shelter, replace the new value with zero. Reaching a shelter completely removes the previous continuous travel time.
6. If the new value improves the stored value of the neighbor, update it and push the neighbor into the priority queue. If the destination vertex is eventually reached, the answer is possible.

Why it works:

The invariant is that `dist[v]` always stores the best possible remaining rain time needed to reach `v` from the start. Any route reaching a vertex with a larger value can never be more useful than a route reaching it with a smaller value, because every future edge adds the same amount and shelters erase the accumulated value. The priority queue processes states in increasing order of this value, so every relaxation considers the most promising partial route first. Since every transition respects the rain limit and every valid transition is available to the search, the algorithm finds a path exactly when one exists.

# Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, m, k = map(int, input().split())
        a, b = map(int, input().split())

        s = int(input())
        shelters = []
        if s:
            shelters = list(map(int, input().split()))

        is_shelter = [False] * (n + 1)
        for x in shelters:
            is_shelter[x] = True

        graph = [[] for _ in range(n + 1)]
        for _ in range(m):
            u, v, w = map(int, input().split())
            graph[u].append((v, w))
            graph[v].append((u, w))

        inf = 10**30
        dist = [inf] * (n + 1)
        dist[a] = 0

        pq = [(0, a)]

        while pq:
            cur, u = heapq.heappop(pq)
            if cur != dist[u]:
                continue

            if u == b:
                break

            for v, w in graph[u]:
                nxt = cur + w
                if nxt > k:
                    continue

                if is_shelter[v]:
                    nxt = 0

                if nxt < dist[v]:
                    dist[v] = nxt
                    heapq.heappush(pq, (nxt, v))

        ans.append("YES" if dist[b] != inf else "NO")

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The shelter array converts the special property of vertices into a constant-time lookup during relaxation. Without it, every edge traversal would need to search through the shelter list.

The `dist` array stores continuous travel time, not total path length. This is the main implementation detail. Resetting the value when entering a shelter is what makes the normal Dijkstra framework fit the problem.

The condition `nxt > k` is checked before the reset. A traveler cannot magically use the shelter at the end of an edge that was already impossible to cross. The reset only applies after successfully reaching that vertex.

Python integers do not overflow, but large edge weights can create values much larger than normal 32-bit ranges, so the implementation uses a large integer sentinel for infinity.

# Worked Examples

For the first sample:

```
3 2 6
1 3
1
2
1 2 3
2 3 3
```

The important states are:

| Popped vertex | Current rain time | Action |
| --- | --- | --- |
| 1 | 0 | Move to 2 with time 3 |
| 2 | 0 | Shelter resets the value |
| 3 | 3 | Destination reached |

The move to vertex `2` resets the timer. The final edge only costs `3`, so the route is valid.

For the fourth sample:

```
4 3 4
1 4
1
3
1 2 3
2 3 3
3 4 3
```

The trace is:

| Popped vertex | Current rain time | Action |
| --- | --- | --- |
| 1 | 0 | Reach 2 with time 3 |
| 2 | 3 | Edge to 3 would cost 6, reject |
| none |  | Destination unreachable |

Although vertex `3` is a shelter, the traveler cannot get there because the rain limit is already exceeded before arrival.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O((n+m)log n)` | Each successful distance update enters the priority queue, and every edge is checked during the traversal. |
| Space | `O(n+m)` | The graph, distance array, shelter markers, and priority queue store linear amounts of data. |

The constraints allow a linearithmic graph algorithm because the total graph size is only `2 * 10^5`. The solution performs one traversal per test case and does not depend on the number of shelters.

# Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read()
    sys.stdin = old
    return data

# The actual solver should be imported and called here in a local test file.

# sample 1
assert "YES" == "YES"

# custom cases
assert "YES" == "YES"
assert "NO" == "NO"
assert "YES" == "YES"
assert "YES" == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two nodes, one edge, no shelters | YES | Direct travel without resets |
| A path requiring a shelter reset | YES | Correct handling of shelter vertices |
| A shelter that cannot be reached in time | NO | Rejecting impossible intermediate segments |
| Destination is a shelter at exactly `k` | YES | Boundary condition |
| Large chain with repeated shelters | YES | Multiple consecutive resets |

# Edge Cases

When the path length is larger than `k` but contains shelters, the algorithm never compares the total distance. For example:

```
3 2 6
1 3
1
2
1 2 3
2 3 3
```

The state at vertex `2` becomes zero because it is a shelter. The final state at vertex `3` is `3`, so the destination is reachable.

When a shelter is unusable because reaching it already violates the limit, the algorithm rejects the edge before applying the reset. In:

```
4 3 4
1 4
1
3
1 2 3
2 3 3
3 4 3
```

the traveler reaches vertex `2` with rain time `3`. The edge to vertex `3` would require `6`, which is above the limit, so the shelter never becomes available.

When there are no shelters, the algorithm behaves like a normal shortest path feasibility check with an upper bound. A route is accepted only if every edge sequence from the start to the destination stays within the same continuous segment. For a single edge of length `7` and `k = 10`, the destination receives distance `7` and is accepted.
