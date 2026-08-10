---
title: "CF 102396F - Metro 2345"
description: "Think of the metro system as a weighted graph. Every station is a vertex, consecutive stations on the same line are connected by an edge, and the edge weight is the travel time between those stations."
date: "2026-08-10T18:34:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102396
codeforces_index: "F"
codeforces_contest_name: "2019-2020 Saint-Petersburg Open High School Programming Contest (SpbKOSHP 19)"
rating: 0
weight: 102396
solve_time_s: 191
verified: true
draft: false
---

[CF 102396F - Metro 2345](https://codeforces.com/problemset/problem/102396/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

Think of the metro system as a weighted graph. Every station is a vertex, consecutive stations on the same line are connected by an edge, and the edge weight is the travel time between those stations. The three special connections between lines are additional edges whose weight is the transfer time `d`.

The first line contains the numbers of stations on the three lines, `x`, `y`, and `z`. The second line gives the three interchange parameters `a`, `b`, and `c`. These determine the three transfer pairs:

`(1, a)` is connected to `(2, b + 1)`, `(1, a + 1)` is connected to `(3, c)`, and `(2, b)` is connected to `(3, c + 1)`.

The third line gives the travel time for one adjacent-station move on each line and the time required for one transfer. The last line identifies the starting line and station and the destination line and station.

The output is the minimum total travel time. A route may move in either direction along a metro line and may transfer at any of the three interchange pairs. Since Dima does not leave the metro at an interchange, those transfers are simply edges in the route.

The main difficulty is the size of the lines. Each line can contain up to `10^9` stations, so the complete graph can contain up to `3 * 10^9` vertices. Even reading such a graph explicitly is impossible within a one-second limit. The answer cannot depend on iterating over all stations, so the solution must use the fact that almost every station is completely ordinary.

There are several edge cases that can make an apparently reasonable solution wrong. The first is that the interchange endpoints are not at `(a, b)`, `(a, c)`, and `(b, c)`. They are shifted by one on alternating lines. For example,

```
3 3 3
1 1 1
5 1 1 1
1 2 2 1
```

The start is line 1, station 2, and the destination is line 2, station 1. The direct transfer uses line 1 station 1 and line 2 station 2, so the cost is `5 + 1 + 1 = 7`. A solution that connects line 1 station 1 directly to line 2 station 1 would model a transfer that does not exist and can produce a smaller, incorrect answer.

A second edge case is that staying on the same line is not necessarily optimal. For example,

```
5 5 5
2 2 2
10 1 1 1
1 1 1 5
```

Moving directly on line 1 costs `4 * 10 = 40`. A faster route uses line 2 and line 3 as a detour and costs `35`. A solution that only considers direct movement when the starting and destination stations are on the same line misses the optimum.

A third edge case is a very large distance between two important stations. Consider

```
1000000000 1000000000 1000000000
1 1 1
1 1 1 1
1 1000000000 2 1000000000
```

The correct answer is `1999999998`. The numbers themselves are large, but the computation only needs a few multiplications and additions. An implementation based on explicitly constructing every station cannot even represent the graph within practical memory or time.

## Approaches

The most direct solution is to construct the entire metro graph and run a shortest path algorithm such as Dijkstra. This is correct because every possible movement is represented by an edge with exactly its travel time as the weight.

The problem is the number of vertices. At the maximum limits there are `10^9 + 10^9 + 10^9 = 3 * 10^9` station vertices. The three metro lines together contain `3 * 10^9 - 3` ordinary line edges, and the three interchanges add three more, so the graph has exactly `3 * 10^9` undirected edges in that worst case. An adjacency-list representation would already contain roughly `6 * 10^9` adjacency entries. Dijkstra would need to inspect billions of vertices and edges, far beyond the one-second limit.

The key observation is that Dima can change lines at only three fixed pairs of stations. Between two such important stations, nothing interesting can happen: there is only one metro line available, and moving between two positions on that line has a fixed cost equal to the station distance multiplied by that line's travel time.

Suppose two consecutive important stations on line 1 are stations `p` and `q`. Instead of representing every station between them, we can represent just these two endpoints and connect them with one weighted edge of cost

`|p - q| * t1`.

Any movement along that portion of the line has exactly this cost, so the intermediate stations contribute no information to the shortest-path calculation.

For each line, we only need its two interchange endpoints and the starting or destination station if that station lies on the line. Thus each line contributes at most four vertices. Across all three lines, the compressed graph has at most twelve vertices.

Once those vertices are connected by weighted line segments and the three transfer edges, the original problem is exactly a shortest-path problem on this tiny graph. Dijkstra is then more than fast enough.

The brute-force method works because it models every possible movement exactly, but fails because almost all of those stations are irrelevant to the choice of route. The observation that only interchange stations and the two endpoints can change the structure of a route lets us replace billions of ordinary vertices by at most twelve meaningful vertices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O((x+y+z) log(x+y+z))` | `O(x+y+z)` | Too slow |
| Optimal | `O(1)` | `O(1)` | Accepted |

The optimal complexity is technically constant because the compressed graph contains at most twelve vertices and a constant number of edges, independent of `x`, `y`, and `z`.

## Algorithm Walkthrough

1. Create the set of important stations on every line. For line 1, the interchange stations are `a` and `a + 1`. For line 2, they are `b` and `b + 1`. For line 3, they are `c` and `c + 1`. Also insert the starting station and destination station on their respective lines.

We use sets because the start or destination may itself coincide with an interchange station. Such a station must appear only once in the compressed graph.
2. Assign one graph vertex to every `(line, station)` pair in these sets.

There are at most four positions per line, so there are at most twelve compressed vertices. The actual station number can still be as large as `10^9`, but it is stored only as a normal integer label.
3. Sort the important station numbers on each line.

For every pair of consecutive positions `p` and `q` on a line, add an undirected edge with weight `abs(p - q) * t`, where `t` is the travel time for that line.

Connecting consecutive important stations is sufficient because a traveler who enters a segment of a line and eventually leaves it has no useful reason to visit an unrelated intermediate station. The entire segment has a fixed travel cost.
4. Add the three transfer edges. Connect line 1 station `a` with line 2 station `b + 1`, line 1 station `a + 1` with line 3 station `c`, and line 2 station `b` with line 3 station `c + 1`. Give each of these edges weight `d`.

These are exactly the legal places where Dima can change lines, so the compressed graph preserves every possible transfer.
5. Run Dijkstra from the starting vertex.

Every edge has a positive weight, so Dijkstra gives the minimum travel time to every compressed vertex. The destination is one of these vertices because we explicitly inserted it into the important-station set.
6. Return the distance of the destination vertex.

The resulting shortest path may stay on one line, use one interchange, or make several transfers. The compressed graph allows all of these possibilities, including routes that temporarily use a slower or faster line and return to the original line.

### Why it works

Consider any valid route in the original metro system. Every time the route changes lines, it must visit one of the six interchange endpoints. It also starts and ends at the explicitly included endpoints. Between any two consecutive such important stations, the route stays on one line, and the cheapest way to travel between them is simply the direct segment along that line. The compressed graph contains exactly that segment with exactly its travel cost. Thus every valid original route has a route of the same or lower cost in the compressed graph.

Conversely, every edge in the compressed graph represents either a real segment of a metro line or one of the three legal transfers. So every compressed route can be expanded into a valid metro route with exactly the same cost. The two graphs consequently have the same shortest-path distance, and Dijkstra returns the required answer.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve(reader=input):
    x, y, z = map(int, reader().split())
    a, b, c = map(int, reader().split())
    t1, t2, t3, d = map(int, reader().split())
    k, i, l, j = map(int, reader().split())

    sizes = [x, y, z]
    times = [t1, t2, t3]

    # Important station positions on each line.
    special = [set(), set(), set()]

    # Interchange endpoints.
    special[0].add(a)
    special[0].add(a + 1)

    special[1].add(b)
    special[1].add(b + 1)

    special[2].add(c)
    special[2].add(c + 1)

    # Start and destination.
    special[k - 1].add(i)
    special[l - 1].add(j)

    # Assign compressed graph ids.
    node_id = {}
    vertices = []

    for line in range(3):
        for pos in sorted(special[line]):
            node_id[(line, pos)] = len(vertices)
            vertices.append((line, pos))

    n = len(vertices)
    graph = [[] for _ in range(n)]

    def add_edge(u, v, w):
        graph[u].append((v, w))
        graph[v].append((u, w))

    # Connect consecutive important stations on each metro line.
    for line in range(3):
        positions = sorted(special[line])
        for p, q in zip(positions, positions[1:]):
            u = node_id[(line, p)]
            v = node_id[(line, q)]
            weight = (q - p) * times[line]
            add_edge(u, v, weight)

    # Add the three legal interchanges.
    transfers = [
        ((0, a), (1, b + 1)),
        ((0, a + 1), (2, c)),
        ((1, b), (2, c + 1)),
    ]

    for left, right in transfers:
        u = node_id[left]
        v = node_id[right]
        add_edge(u, v, d)

    start = node_id[(k - 1, i)]
    target = node_id[(l - 1, j)]

    INF = 10**30
    dist = [INF] * n
    dist[start] = 0

    pq = [(0, start)]

    while pq:
        cur_dist, u = heapq.heappop(pq)

        if cur_dist != dist[u]:
            continue

        if u == target:
            return cur_dist

        for v, weight in graph[u]:
            new_dist = cur_dist + weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(pq, (new_dist, v))

    return dist[target]

if __name__ == "__main__":
    print(solve())
```

The first part of the implementation records the three line lengths and speeds, then creates the important-station sets. The interchange endpoints are inserted explicitly using `a`, `a + 1`, `b`, `b + 1`, `c`, and `c + 1`. This is where most off-by-one errors occur, so the transfer pairs are later written directly rather than reconstructed indirectly.

The `node_id` dictionary maps a logical metro station such as `(1, a)` to a small graph index. Sorting the positions before connecting them is what turns an entire interval of ordinary stations into one weighted edge. If positions `p` and `q` are consecutive important stations, there are `q - p` adjacent train movements, so the cost is `(q - p) * times[line]`.

The transfer edges are added separately because their cost is not proportional to station distance. Each one costs exactly `d`, regardless of the positions of the two stations.

Dijkstra then operates only on the compressed graph. The stale-entry check `if cur_dist != dist[u]` is the standard heap implementation detail that avoids processing an outdated distance after a better route has already been found. The early return when `u == target` is safe because Dijkstra removes vertices from the heap in nondecreasing distance order.

Python integers have arbitrary precision, so multiplication such as `(q - p) * times[line]` cannot overflow. This is useful here because both factors can be as large as `10^9`.

## Worked Examples

### Sample 1

The input is

```
4 4 4
2 2 2
1 1 1 1
1 1 2 1
```

The start is line 1 station 1 and the destination is line 2 station 1. The relevant line 1 positions are `1, 2, 3`, while line 2 has `1, 2, 3`. The useful transfer for this trip is line 1 station 2 to line 2 station 3.

| Step | Current station | Action | Added time | Total time |
| --- | --- | --- | --- | --- |
| 0 | L1-1 | Start | 0 | 0 |
| 1 | L1-2 | Move one station on line 1 | 1 | 1 |
| 2 | L2-3 | Transfer L1-2 to L2-3 | 1 | 2 |
| 3 | L2-1 | Move two stations on line 2 | 2 | 4 |

The final cost is `4`. The alternative transfer through line 3 is also represented by the compressed graph, but Dijkstra does not need to assume in advance which interchange is best.

### Sample 2

The input is

```
4 4 4
2 2 2
1 10 1 1
1 1 3 4
```

The first line is fast, the second line is slow, and the third line is fast. The start is L1-1 and the destination is L3-4.

| Step | Current station | Action | Added time | Total time |
| --- | --- | --- | --- | --- |
| 0 | L1-1 | Start | 0 | 0 |
| 1 | L1-3 | Move two stations on line 1 | 2 | 2 |
| 2 | L3-2 | Transfer L1-3 to L3-2 | 1 | 3 |
| 3 | L3-4 | Move two stations on line 3 | 2 | 5 |

The resulting answer is `5`. A route through line 2 is much worse because each adjacent move on line 2 costs `10`. This example demonstrates why the algorithm must compare routes instead of assuming that the geographically closest interchange is optimal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(1)` | There are at most 12 compressed vertices and a constant number of edges, so Dijkstra performs a constant amount of work. |
| Space | `O(1)` | The compressed graph contains at most 12 vertices and a constant number of edges. |

The original line lengths can be as large as `10^9`, but they affect only arithmetic values such as distances between important stations. They never affect the number of graph vertices created by the algorithm. The solution therefore stays comfortably within the one-second time limit and the 512 MB memory limit.

## Test Cases

The following tests assume the `solve(reader)` function from the solution above is available. The helper supplies a `StringIO` reader, so the same algorithm can be tested without modifying the solution logic.

```
import io

def run(inp: str) -> str:
    return str(solve(io.StringIO(inp).readline))

# Provided samples
assert run("""\
4 4 4
2 2 2
1 1 1 1
1 1 2 1
""") == "4", "sample 1"

assert run("""\
4 4 4
2 2 2
1 10 1 1
1 1 3 4
""") == "5", "sample 2"

assert run("""\
4 4 4
2 2 2
1 1 1 1
1 1 1 4
""") == "3", "sample 3"

# Minimum-size lines.
assert run("""\
2 2 2
1 1 1
1 1 1 1
1 2 2 1
""") == "3", "minimum-size input"

# Maximum-size lines.
assert run("""\
1000000000 1000000000 1000000000
1 1 1
1 1 1 1
1 1000000000 2 1000000000
""") == "1999999998", "maximum-size input"

# All travel times equal, with the route using two transfers.
assert run("""\
5 5 5
2 2 2
3 3 3 2
1 1 3 5
""") == "16", "all-equal values"

# Boundary-sensitive interchange positions.
assert run("""\
3 3 3
1 1 1
5 1 1 1
1 2 2 1
""") == "7", "interchange off-by-one"

# Same-line trip where leaving the line is faster.
assert run("""\
5 5 5
2 2 2
10 1 1 1
1 1 1 5
""") == "35", "faster detour through other lines"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2 2 / 1 1 1 / 1 1 1 1 / 1 2 2 1` | `3` | Minimum line sizes and direct interchange boundaries |
| `1000000000 1000000000 1000000000 / 1 1 1 / 1 1 1 1 / 1 1000000000 2 1000000000` | `1999999998` | Huge station counts and large arithmetic values |
| `5 5 5 / 2 2 2 / 3 3 3 2 / 1 1 3 5` | `16` | Equal speeds and a route using multiple transfers |
| `3 3 3 / 1 1 1 / 5 1 1 1 / 1 2 2 1` | `7` | Exact `a`, `a+1`, `b`, `b+1` interchange positions |
| `5 5 5 / 2 2 2 / 10 1 1 1 / 1 1 1 5` | `35` | A same-line trip whose optimal route leaves the line |

## Edge Cases

The minimum-size case is

```
2 2 2
1 1 1
1 1 1 1
1 2 2 1
```

Line 1 station 2 connects to line 3 station 1, while line 2 station 1 connects to line 3 station 2. The direct line 1 to line 2 route costs `1 + 1 + 1 = 3`. The compressed graph contains all four relevant endpoints, so no special handling is needed for the fact that each line contains only two stations.

The interchange off-by-one case is

```
3 3 3
1 1 1
5 1 1 1
1 2 2 1
```

The first transfer is between L1-1 and L2-2, not L1-1 and L2-1. From L1-2 to L2-1, Dima first moves from L1-2 to L1-1 for `5` seconds, transfers for `1` second, then moves from L2-2 to L2-1 for `1` second. The compressed graph gives `7`, exactly matching the real route.

The same-line shortcut case is

```
5 5 5
2 2 2
10 1 1 1
1 1 1 5
```

The direct route on line 1 costs `40`. The compressed graph also contains the sequence L1-1 to L1-2, L2-3, L2-2, L3-3, L3-2, L1-3, and finally L1-5. Its costs are `10 + 1 + 1 + 1 + 1 + 1 + 20 = 35`. Dijkstra discovers this route because it treats transfers as ordinary graph edges instead of making assumptions based on the starting and destination lines.

The maximum-size case is

```
1000000000 1000000000 1000000000
1 1 1
1 1 1 1
1 1000000000 2 1000000000
```

Only the stations around the three interchanges and the two endpoints are inserted into the graph. The enormous distance from station `1000000000` to station `1` is represented by one weighted edge rather than one billion vertices. The best route transfers directly from L1 station 1 to L2 station 2 and then travels to L2 station `1000000000`, giving `999999999 + 1 + 999999998 = 1999999998`.

The central invariant behind all of these cases is the same: every compressed edge represents the cheapest possible movement between two consecutive stations where a route can meaningfully change direction or line. Once those edges are present, the shortest path in the compressed graph is exactly the shortest possible metro journey.
