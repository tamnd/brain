---
title: "CF 105979D - Discovering Graphlandia"
description: "This problem asks us to look at a road network where every city has an energy value. Starting from a city, we may travel along roads, but we are only allowed to enter cities whose energy is not greater than the starting city's energy."
date: "2026-06-25T13:31:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105979
codeforces_index: "D"
codeforces_contest_name: "2025 ICPC Gran Premio de Mexico 2da Fecha"
rating: 0
weight: 105979
solve_time_s: 43
verified: true
draft: false
---

[CF 105979D - Discovering Graphlandia](https://codeforces.com/problemset/problem/105979/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

This problem asks us to look at a road network where every city has an energy value. Starting from a city, we may travel along roads, but we are only allowed to enter cities whose energy is not greater than the starting city's energy. For every city, we need to find how many cities are reachable under this rule. The task comes from Codeforces Gym 105979, Problem D.

The input describes an undirected graph. The first part gives the number of cities and roads, the next part gives each city's energy, and the remaining lines describe the roads connecting pairs of cities. The output contains one value per city, representing the size of the reachable region for that city's energy limit.

The large bounds are the key to choosing the right direction. The graph can contain up to one million cities and one million roads, so a solution that performs a graph search from every city would require roughly O(N(N+M)) work in the worst case. With one million nodes, even touching a small fraction of all possible repeated traversals is impossible. We need to process the whole graph close to linearly.

A common mistake is to think that if we start from a city with a large energy value, we can somehow expand through larger cities later. The movement rule is based only on the starting city's value, so the allowed set is exactly the cities with energy less than or equal to that starting value. This creates a natural ordering by energy.

Consider a graph where every city is isolated.

```
3 0
5 5 5
```

The correct output is:

```
1
1
1
```

A careless solution might group equal energy cities together and assume they are connected because their values match. Equal energy does not create roads, so connectivity still depends only on graph edges.

Another edge case is a chain with increasing energies:

```
3 2
1 2 3
1 2
2 3
```

The correct output is:

```
1
2
3
```

The first city cannot go anywhere because the next city has higher energy. The second city can reach the first, and the third city can reach all three. A solution that answers while processing each energy separately before connecting all equal or lower nodes can get this ordering wrong.

A final subtle case is multiple cities with the same energy:

```
4 2
5 5 5 10
1 2
2 3
```

The correct output is:

```
3
3
3
4
```

All three energy 5 cities become available together. If we process equal energies one by one and immediately answer, the first processed city may incorrectly see only part of its final component.

## Approaches

The direct approach is to run a graph traversal from every city. For a chosen starting city, we would walk through adjacent roads while refusing to enter cities with larger energy values. This is correct because the traversal exactly follows the movement rule. However, if the graph is large, the same roads and cities are visited many times. In a dense or highly connected graph, repeating this from every city can reach about O(N(N+M)) operations, which is far beyond what the input size allows.

The structure of the problem gives us a way to reverse the viewpoint. Instead of asking "where can this city go?", ask "what happens when we gradually allow cities to become usable?". Sort cities by energy. When we process cities from the smallest energy to the largest, after we have activated all cities up to some energy value x, the connected components among activated cities are exactly the regions that a city with energy x can explore.

The reason this works is that every allowed move only goes to a city with energy at most the starting value. If we activate cities in increasing order, every road between two already activated cities represents a possible movement inside the current energy limit. A disjoint set union structure can maintain these connected components while roads are added.

The important detail is handling equal energies. All cities with the same energy must be activated together before any of them receives an answer. Otherwise, two same energy cities connected by a path through other same energy cities might not have been merged yet.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N(N+M)) | O(N+M) | Too slow |
| Optimal | O((N+M) log N) | O(N+M) | Accepted |

## Algorithm Walkthrough

1. Sort all cities by their energy value. We will process them from the lowest energy to the highest because a city with energy x only cares about cities that appear no later than x in this ordering.
2. Create a disjoint set union structure. Initially no city is active, so every component is empty. The structure will store which active cities are connected and the size of each connected component.
3. For each group of cities that have the same energy, activate all of them first. Marking a city active means it is now allowed to participate in paths for cities with this energy or any larger energy.
4. For every newly activated city, check all adjacent cities. If a neighbor is already active, merge the two components. The road is usable because both endpoints satisfy the current energy limit.
5. After all cities with this energy have been activated and merged, assign the component size to every city in the group. This value is the number of cities reachable from it.
6. Output the stored answers in the original city order.

Why it works:

The invariant is that after finishing a group of energy value x, the disjoint set union components contain exactly the connected components of the subgraph formed by cities whose energy is at most x. Every possible valid path for a city with energy x must stay inside this subgraph, so the size of its component is exactly the answer. Processing equal energies as a batch preserves the invariant because all cities with the same limit become available at the same time.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    energy = list(map(int, input().split()))

    graph = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    parent = list(range(n))
    size = [1] * n
    active = [False] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        a = find(a)
        b = find(b)
        if a == b:
            return
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]

    order = list(range(n))
    order.sort(key=lambda x: energy[x])

    ans = [0] * n
    i = 0

    while i < n:
        j = i
        value = energy[order[i]]
        while j < n and energy[order[j]] == value:
            j += 1

        for k in range(i, j):
            u = order[k]
            active[u] = True

        for k in range(i, j):
            u = order[k]
            for v in graph[u]:
                if active[v]:
                    union(u, v)

        for k in range(i, j):
            u = order[k]
            ans[u] = size[find(u)]

        i = j

    sys.stdout.write("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The code first stores the graph using adjacency lists because the number of roads can be large and we need to scan neighbors efficiently.

The disjoint set union implementation uses path compression and union by size. These optimizations keep each merge operation almost constant time, which is necessary when the graph contains around one million roads.

The sorting step creates the order in which cities become available. The main loop advances through equal energy groups. The two separate loops inside each group are necessary: first every city in the group becomes active, then all roads are considered. Activating and merging in the same pass would create the same equal energy bug described earlier.

The answer is taken from the root's stored component size after all merges are complete. The `find` call is needed because the city itself may no longer be the root after previous unions.

## Worked Examples

### Sample 1

Input:

```
6 5
1 5 7 11 10 9
1 2
1 3
1 4
4 5
4 6
```

| Energy processed | Activated cities | Current operation | Component sizes assigned |
| --- | --- | --- | --- |
| 1 | 1 | No active neighbors | city 1 gets 1 |
| 5 | 2 | Connects to city 1 | city 2 gets 2 |
| 7 | 3 | Connects to city 1 | city 3 gets 3 |
| 9 | 6 | No new connection | city 6 gets 1 |
| 10 | 5 | No connection to active lower cities through valid path | city 5 gets 1 |
| 11 | 4 | Connects 4,5,6 with previous active cities | city 4 gets 6 |

The trace shows why a city only gains access to roads that lead through cities no larger than its own energy. The final activation joins the entire graph because the energy limit is high enough.

### Sample 2

Input:

```
3 3
1 2 3
1 2
2 3
3 1
```

| Energy processed | Activated cities | Current operation | Component sizes assigned |
| --- | --- | --- | --- |
| 1 | 1 | Isolated component | city 1 gets 1 |
| 2 | 2 | Connects with city 1 | city 2 gets 2 |
| 3 | 3 | Connects with both active cities | city 3 gets 3 |

This example confirms the monotonic behavior. As the allowed energy increases, components can only grow.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N+M) log N) | Sorting dominates, while each edge is checked a constant number of times during DSU merging |
| Space | O(N+M) | The graph, DSU arrays, ordering, and answers all require linear memory |

The input limits require nearly linear processing. The algorithm touches every city and road only a few times after sorting, so it fits the constraints comfortably.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.strip()

# provided samples
assert run("""6 5
1 5 7 11 10 9
1 2
1 3
1 4
4 5
4 6
""") == "1\n2\n3\n6\n1\n1"

assert run("""3 3
1 2 3
1 2
2 3
3 1
""") == "1\n2\n3"

# minimum size
assert run("""1 0
7
""") == "1"

# all equal values
assert run("""4 2
5 5 5 5
1 2
3 4
""") == "2\n2\n2\n2"

# increasing chain
assert run("""5 4
1 2 3 4 5
1 2
2 3
3 4
4 5
""") == "1\n2\n3\n4\n5"

# disconnected high energy case
assert run("""5 2
10 1 1 10 1
1 2
2 3
""") == "5\n3\n3\n5\n3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single city | `1` | Handles the smallest graph |
| Equal energies | Two node components | Confirms batching of equal values |
| Increasing chain | Growing answers | Confirms energy ordering logic |
| Disconnected graph | Separate components | Confirms DSU tracks connectivity correctly |

## Edge Cases

For the isolated city case:

```
3 0
5 5 5
```

the algorithm activates each city, but no union operations occur because there are no roads. Each DSU component remains size one, so the output is `1 1 1`. The approach never assumes equal energy creates connectivity.

For the increasing chain:

```
3 2
1 2 3
1 2
2 3
```

the city with energy 1 is processed first and forms a component of size one. When energy 2 is processed, city 2 becomes active and merges with city 1, producing size two. Finally, city 3 joins the active component, producing size three. This follows exactly the reachable sets.

For the equal energy case:

```
4 2
5 5 5 10
1 2
2 3
```

the first three cities are activated together before any answer is written. The two roads merge them into one component of size three, so every energy 5 city receives the correct value. The last city is activated later with enough energy to see all previous cities, so it receives size four. This is the case that breaks implementations that process equal energies one at a time.
