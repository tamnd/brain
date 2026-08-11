---
title: "CF 102411E - Equidistant"
description: "The railroad network is a tree. Each city is a vertex, each railroad is an edge, and traveling across one edge takes one hour. A subset of the vertices contains the cities where the teams are located."
date: "2026-08-12T00:12:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102411
codeforces_index: "E"
codeforces_contest_name: "ICPC 2019-2020 North-Western Russia Regional Contest"
rating: 0
weight: 102411
solve_time_s: 167
verified: true
draft: false
---

[CF 102411E - Equidistant](https://codeforces.com/problemset/problem/102411/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

The railroad network is a tree. Each city is a vertex, each railroad is an edge, and traveling across one edge takes one hour. A subset of the vertices contains the cities where the teams are located. We need to find a city whose tree distance to every team city is exactly the same. If such a city exists, any one valid city may be printed.

The fact that the graph is a tree is the key structural property. Between every two cities there is exactly one path, so there is no ambiguity about distance or about where two paths meet. The number of cities can reach (2 \cdot 10^5), and the number of teams can also reach (2 \cdot 10^5). With a 2 second limit, an (O(n^2)) or (O(nm)) algorithm would require around (4 \cdot 10^{10}) operations in the worst case, which is far beyond what is practical. We need an algorithm close to linear in the size of the tree.

There are several edge cases that can make a seemingly reasonable solution fail. If there is only one team, every city is equally distant from that single city only in the trivial sense that there is just one distance to compare, so any city is valid. For example,

```
1 1
1
```

has answer `YES` with city `1`. A solution that blindly takes two team cities would access a nonexistent second element.

With two teams, their path must have even length. For example,

```
2 2
1 2
1 2
```

has only one edge between the teams, so no vertex is exactly halfway between them. The correct answer is `NO`. A careless solution might use integer division on the distance and choose one endpoint, but that endpoint is distance zero from one team and one from the other.

There is also a second failure mode when there are at least three teams. Checking only the first two teams is not enough. Consider

```
5 3
1 2
2 3
3 4
4 5
1 5 2
```

The first two teams are at cities 1 and 5, so their midpoint is city 3. Its distances to cities 1 and 5 are both 2, but its distance to the third team at city 2 is only 1. The correct answer is `NO`. The final verification against every team is essential.

## Approaches

A direct brute-force solution can try every city as the final location. For each candidate city, it can traverse the tree once to compute distances and then check whether all marked cities have the same distance. A single traversal costs (O(n)), and there can be (n) candidate cities, giving (O(n^2)) time. With (n=2\cdot10^5), this is about (4\cdot10^{10}) vertex visits in the worst case. The brute force is correct because it explicitly checks every possible answer, but it is far too slow.

The useful observation comes from considering just two team cities. Suppose a valid final city (x) exists and two teams are at (a) and (b). Since (d(x,a)=d(x,b)), the unique path from (a) to (b) must pass through (x), and the two portions of that path must have the same length. Thus (x) is exactly the midpoint of the path from (a) to (b).

This completely determines the candidate. If the distance between (a) and (b) is odd, there is no vertex at the midpoint, so the answer is immediately impossible. If the distance is even, there is exactly one midpoint vertex. We can find it with one tree traversal and then check that every team has the same distance to that vertex.

The brute-force solution works because it tests all possible centers, but fails because there are too many centers. The observation that any valid center must be the midpoint of the path between any two teams lets us reduce the search from all (n) cities to one candidate, followed by one verification traversal.

For one team, no pair is available, so we handle that case separately and simply return the team city itself.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(n)) | Too slow |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read the tree and the list of team cities. If there is only one team, output that city immediately. No comparison with another team is necessary because there is only one distance.
2. Choose the first two team cities, call them (a) and (b). Root the tree at (a), and run an iterative DFS to compute `parent[v]` and `dist[v]` for every city. The parent array records the unique path from every city back toward (a), while `dist[b]` gives the length of the path from (a) to (b).
3. Let (D=dist[b]). If (D) is odd, output `NO`. A path of odd length has an edge in its middle rather than a vertex, so no city can be equally far from both endpoints.
4. If (D) is even, find the midpoint by starting at (b) and moving upward through `parent` exactly (D/2) times. Call the resulting city (x). Its distance from both (a) and (b) is exactly (D/2).
5. Run another traversal starting from (x), computing the distance from (x) to every city. Let `target` be the distance from (x) to the first team city.
6. Check every team city. If its distance from (x) differs from `target`, output `NO`. Otherwise, output `YES` and (x).
7. The candidate cannot be wrong after this verification. Any valid answer must be the midpoint of the first two team cities, and we have explicitly checked that this midpoint has the same distance to every remaining team.

Why it works: assume a valid city (y) exists. For the first two team cities (a) and (b), the equality (d(y,a)=d(y,b)) forces (y) to lie on their unique path and be its midpoint. Consequently, if that path has odd length, no valid city exists, while if it has even length, the only possible answer is the midpoint (x) constructed by the algorithm. The final traversal checks exactly the original condition for every team, so the algorithm accepts precisely when that unique candidate is valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    graph = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    teams = list(map(int, input().split()))

    if m == 1:
        print("YES")
        print(teams[0])
        return

    a = teams[0]
    b = teams[1]

    parent = [0] * (n + 1)
    dist = [-1] * (n + 1)

    dist[a] = 0
    stack = [a]

    while stack:
        v = stack.pop()
        for u in graph[v]:
            if u == parent[v]:
                continue
            parent[u] = v
            dist[u] = dist[v] + 1
            stack.append(u)

    d = dist[b]

    if d % 2 == 1:
        print("NO")
        return

    center = b
    for _ in range(d // 2):
        center = parent[center]

    center_dist = [-1] * (n + 1)
    center_dist[center] = 0
    stack = [center]

    while stack:
        v = stack.pop()
        for u in graph[v]:
            if u == parent[v]:
                continue
            if center_dist[u] != -1:
                continue
            center_dist[u] = center_dist[v] + 1
            stack.append(u)

    target = center_dist[a]

    for city in teams:
        if center_dist[city] != target:
            print("NO")
            return

    print("YES")
    print(center)

if __name__ == "__main__":
    solve()
```

The first traversal is rooted at the first team city. `dist[b]` gives the exact distance between the first two teams, while `parent` lets us walk backward along their unique path. We do not need a separate lowest common ancestor structure because one endpoint is the root, so the entire path to the other endpoint is already stored in the parent chain.

The midpoint calculation uses `d // 2` parent moves from `b`. If the path has length (d=2k), city `b` is (2k) edges from `a`, and moving upward (k) edges leaves exactly (k) edges to either endpoint. The odd-distance check must happen before this calculation, because an odd-length path has no vertex midpoint.

The second traversal starts from the proposed center. Its purpose is not to search for another candidate, but only to verify the original condition. The reference distance can be taken from `a`, and every team must have exactly that distance.

The traversals are implemented with an explicit stack rather than recursive DFS. A tree can be a chain of (2\cdot10^5) vertices, which would exceed Python's normal recursion depth if recursive DFS were used. The explicit stack avoids that problem.

The `center_dist[u] != -1` check in the second traversal prevents revisiting the parent. In the first traversal, checking `u == parent[v]` is sufficient because every newly reached vertex has only one parent in the rooted tree.

All distances are at most (n-1), so Python integers easily handle them. There are no indexing conversions needed for the cities because the input uses one-based vertex numbers and the arrays are allocated with `n + 1` positions.

## Worked Examples

For Sample 1, the tree is

```
1 - 2 - 3 - 4 - 5
            |
            6
```

and the teams are at cities 1, 5, and 6.

| Step | `a` | `b` | `dist[b]` | `center` | `target` | Result |
| --- | --- | --- | --- | --- | --- | --- |
| Read teams | 1 | 5 | 4 | not set | not set | Continue |
| Find midpoint | 1 | 5 | 4 | 3 | not set | Even distance |
| Verify teams | 1 | 5 | 4 | 3 | 2 | Check all |
| Team 1 | 1 | 5 | 4 | 3 | 2 | Distance 2 |
| Team 2 | 1 | 5 | 4 | 3 | 2 | Distance 2 |
| Team 3 | 1 | 5 | 4 | 3 | 2 | Distance 2 |
| Output | 1 | 5 | 4 | 3 | 2 | `YES 3` |

The path from city 1 to city 5 has length 4, so city 3 is its midpoint. City 6 is also two edges from city 3, so all three teams are exactly two hours away. The invariant from the algorithm is visible here: after constructing the midpoint, the only remaining question is whether every marked city has the same distance to it.

For Sample 2, the tree contains only the edge (1-2), and both cities contain teams.

| Step | `a` | `b` | `dist[b]` | `dist[b] % 2` | Result |
| --- | --- | --- | --- | --- | --- |
| Read teams | 1 | 2 | not set | not set | Continue |
| Find distance | 1 | 2 | 1 | 1 | Odd |
| Check parity | 1 | 2 | 1 | 1 | `NO` |

The only path has one edge. There is no city half an edge away from both endpoints, so the algorithm correctly stops before attempting to construct a midpoint.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Two traversals inspect every vertex and every tree edge a constant number of times. |
| Space | (O(n)) | The adjacency list, parent array, distance arrays, and traversal stack all use linear space. |

The tree contains only (n-1) edges, so the two traversals together perform (O(n)) work. For (n=2\cdot10^5), this is comfortably within the intended scale for a 2 second limit, while the linear memory usage also fits easily inside 512 MB.

## Test Cases

The test harness below keeps the same `solve()` implementation and temporarily replaces standard input and output. The maximum-size test constructs a star with 200,000 cities and 199,999 teams. Every team is one edge from city 1, so city 1 is the required center.

```python
import sys
import io

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    graph = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    teams = list(map(int, input().split()))

    if m == 1:
        print("YES")
        print(teams[0])
        return

    a = teams[0]
    b = teams[1]

    parent = [0] * (n + 1)
    dist = [-1] * (n + 1)

    dist[a] = 0
    stack = [a]

    while stack:
        v = stack.pop()
        for u in graph[v]:
            if u == parent[v]:
                continue
            parent[u] = v
            dist[u] = dist[v] + 1
            stack.append(u)

    d = dist[b]

    if d % 2 == 1:
        print("NO")
        return

    center = b
    for _ in range(d // 2):
        center = parent[center]

    center_dist = [-1] * (n + 1)
    center_dist[center] = 0
    stack = [center]

    while stack:
        v = stack.pop()
        for u in graph[v]:
            if u == parent[v]:
                continue
            if center_dist[u] != -1:
                continue
            center_dist[u] = center_dist[v] + 1
            stack.append(u)

    target = center_dist[a]

    for city in teams:
        if center_dist[city] != target:
            print("NO")
            return

    print("YES")
    print(center)

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run(
    """6 3
1 2
2 3
3 4
4 5
4 6
1 5 6
"""
) == "YES\n3", "sample 1"

# Provided sample 2
assert run(
    """2 2
1 2
1 2
"""
) == "NO", "sample 2"

# Minimum-size input
assert run(
    """1 1

1
"""
) == "YES\n1", "single city and single team"

# Even path, midpoint is an internal vertex
assert run(
    """5 2
1 2
2 3
3 4
4 5
1 5
"""
) == "YES\n3", "even path midpoint"

# First two teams have a midpoint, but the third team breaks equality
assert run(
    """5 3
1 2
2 3
3 4
4 5
1 5 2
"""
) == "NO", "must verify every team"

# Maximum-size input with all team distances equal to the center
n = 200000
edges = "\n".join(f"1 {v}" for v in range(2, n + 1))
teams = " ".join(str(v) for v in range(2, n + 1))
maximum_case = f"{n} {n - 1}\n{edges}\n{teams}\n"

assert run(maximum_case) == "YES\n1", "maximum-size star"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1`, with the single city as the team city | `YES`, city `1` | Minimum size and the single-team special case |
| Five-city path with teams at 1 and 5 | `YES`, city `3` | Exact midpoint calculation and boundary distances |
| Five-city path with teams at 1, 5, and 2 | `NO` | Final verification of every team |
| 200,000-city star with all 199,999 leaves as teams | `YES`, city `1` | Maximum input size, equal distances, and linear performance |

## Edge Cases

The single-team case is handled before any pair-based reasoning. For

```
1 1
1
```

the algorithm sees `m == 1` and immediately prints `YES` and `1`. There is no need to define a midpoint because there is no second team. A solution that always reads `teams[1]` would fail here.

The odd-distance case is rejected before midpoint construction. For

```
2 2
1 2
1 2
```

the first traversal gives `dist[2] = 1`. Since `1 % 2 == 1`, the algorithm prints `NO`. There is no integer-valued city halfway between the two team cities.

The case where the first pair looks valid but another team is not centered is handled by the second traversal. For

```
5 3
1 2
2 3
3 4
4 5
1 5 2
```

the distance from 1 to 5 is 4, so the algorithm chooses city 3. The distance array from city 3 gives `d(3,1)=2`, `d(3,5)=2`, and `d(3,2)=1`. Since the third value differs from the reference distance 2, the algorithm prints `NO`. This prevents the common mistake of checking only the pair used to construct the candidate.

A maximum-depth tree is another practical edge case for Python. A path with 200,000 vertices can make recursive DFS exceed Python's recursion limit. The solution uses explicit stacks for both traversals, so a tree such as

```
1 - 2 - 3 - ... - 200000
```

is processed without recursion. The stack contains vertices waiting to be processed, while the parent and distance arrays retain the tree information needed for the midpoint and verification phases.

Finally, a large collection of teams can all be equally distant from one city. In the maximum-size star, city 1 is connected directly to every other city, and every city from 2 through 200,000 contains a team. The first two teams are at distance 2 from each other through city 1, so the midpoint is city 1. The second traversal finds distance 1 to every team, and all comparisons succeed. The algorithm prints `YES` and `1`, demonstrating that the number of teams does not change the linear complexity.
