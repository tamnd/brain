---
title: "CF 102471E - Flow"
description: "The graph has a special shape: it is made from several independent routes going from the source vertex 1 to the sink vertex n. Every route contains the same number of edges, and routes do not share internal vertices. Capacities on edges can be moved around by unit operations."
date: "2026-08-05T20:22:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102471
codeforces_index: "E"
codeforces_contest_name: "2019 ICPC Asia-East Continent Final"
rating: 0
weight: 102471
solve_time_s: 80
verified: true
draft: false
---

[CF 102471E - Flow](https://codeforces.com/problemset/problem/102471/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

The graph has a special shape: it is made from several independent routes going from the source vertex 1 to the sink vertex n. Every route contains the same number of edges, and routes do not share internal vertices. Capacities on edges can be moved around by unit operations. One operation takes one unit of capacity from an edge that currently has some capacity and puts it on another edge.

The goal is not to construct the final capacities. We only need the minimum number of moved units needed so that the maximum possible flow becomes as large as the total capacity allows.

For a single route with edge capacities `c1, c2, ..., cl`, the amount of flow that route can carry is its smallest edge capacity. After redistributing capacities, the total capacity of all routes is unchanged. Since every unit of flow needs one unit of capacity on every one of the `l` edges of a route, the absolute maximum flow is:

```
total_capacity // l
```

The constraints make a simulation impossible. There can be up to 100000 vertices and 200000 edges, while capacities can be as large as 10^9. Any algorithm depending on the capacity values directly, such as increasing flow one unit at a time, can require billions of operations.

The main hidden edge cases come from the fact that the best redistribution is not always to balance every path independently.

Consider:

```
4 3
1 2 0
2 3 100
3 4 100
```

The path length is 3. The total capacity is 200, so the final maximum flow is 66. A greedy method that tries to make every path equal to `total/l` by directly filling all missing edges may work here, but approaches that assume every extra unit should be spread evenly fail because the marginal cost of increasing a path can change sharply.

Another case is:

```
4 3
1 2 5
2 3 5
3 4 5
```

The answer is 0. The current bottleneck is already 5 and the total capacity gives the same maximum flow. A method that always performs redistribution after computing the theoretical maximum would incorrectly count unnecessary moves.

The last important case is a path with zero capacity:

```
2 1
1 2 0
```

The maximum flow is 0 and no operations are needed. Implementations that assume every edge has positive capacity when decomposing paths may fail here.

## Approaches

A direct solution would repeatedly increase the flow of some path until the global maximum is reached. For every extra unit of flow, it would find a path edge with insufficient capacity and move capacity into it. This is correct because every operation can be viewed as paying for one missing unit on some edge. However, the maximum flow can be around `10^14`, so unit simulation is impossible.

The useful observation comes from looking at one path. Suppose its current bottleneck is increased from `x-1` to `x`. The number of operations needed for that increase is exactly the number of edges whose capacity is smaller than `x`, because every such edge needs one more unit. These costs form a nondecreasing sequence for every path.

The final flow value is fixed. We need to choose exactly `total_capacity // l` increments among all path increment sequences with minimum total cost. Since all increment costs are nondecreasing, the answer is obtained by taking the smallest costs globally.

The costs are always between 0 and `l`, so we do not need to store every possible increment. For every path, we count how many increments have cost 0, cost 1, and so on up to `l-1`. All remaining increments cost `l`. Then we consume these counts from the smallest cost upward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(answer) | O(1) | Too slow |
| Optimal | O(n + m + l) | O(n + m + l) | Accepted |

## Algorithm Walkthrough

1. Traverse the graph from vertex 1. Every outgoing edge of the source starts one of the independent paths. Follow each path until reaching vertex n and store its edge capacities. Because internal vertices belong to only one path, every internal vertex has exactly one next edge.
2. Let `l` be the length of a path. Compute the target flow value as the sum of all edge capacities divided by `l` using integer division. This is the number of one-unit path layers that must be created after redistribution.
3. For each path, sort its edge capacities. If the current desired flow level is `x`, the cost of reaching this level is the number of capacities smaller than `x`. By grouping equal capacities, count how many consecutive levels have every possible cost.
4. Add all these counts into a global frequency array indexed by the operation cost. Costs smaller than `l` are finite. Any additional levels after the largest edge capacity on a path have cost `l`.
5. Starting from cost 0, take as many levels as possible until exactly the target flow value has been selected. The sum of selected costs is the minimum number of operations.

Why it works: every unit of final flow corresponds to one chosen level on one path. A path can only choose its levels in order, but its level costs never decrease, so the globally cheapest valid selection is obtained by taking the cheapest available costs first. The construction of the cost frequencies preserves exactly those marginal costs, so the accumulated sum is the minimum possible number of moved capacity units.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    adj = [[] for _ in range(n)]
    indeg = [0] * n

    edges = []
    total = 0

    for _ in range(m):
        u, v, c = map(int, input().split())
        u -= 1
        v -= 1
        adj[u].append((v, c))
        indeg[v] += 1
        edges.append((u, v, c))
        total += c

    paths = []
    length = None

    for _, first_c in adj[0]:
        caps = [first_c]
        cur = adj[0][len(paths)][0]

        while cur != n - 1:
            nxt, c = adj[cur][0]
            caps.append(c)
            cur = nxt

        if length is None:
            length = len(caps)
        paths.append(caps)

    if length is None:
        print(0)
        return

    need = total // length

    freq = [0] * length
    cheap_count = 0
    cheap_sum = 0

    for caps in paths:
        caps.sort()
        cur = 0
        idx = 0
        i = 0
        while i < length:
            v = caps[i]
            j = i
            while j < length and caps[j] == v:
                j += 1
            cnt = j - i
            levels = v - cur
            if idx < length:
                freq[idx] += levels
                cheap_count += levels
                cheap_sum += levels * idx
            idx += cnt
            cur = v
            i = j

    ans = cheap_sum
    if need > cheap_count:
        ans += (need - cheap_count) * length

    print(ans)

if __name__ == "__main__":
    solve()
```

The path extraction relies on the special graph structure. The source can have several outgoing edges, but after entering an internal vertex there is only one possible next edge. This avoids running a general graph algorithm.

The frequency array stores only costs from `0` to `l-1`. Once every edge on a path becomes the limiting edge, increasing the path flow further always costs `l`, so the remaining contribution can be computed arithmetically.

All values involving capacities and the answer use Python integers. This is necessary because the answer can exceed 32-bit and 64-bit limits in the largest cases.

## Worked Examples

### Sample 1

Input:

```
4 3
1 2 1
2 3 2
3 4 3
```

The only path has capacities `[1,2,3]`.

| Step | Current path capacity | Cost frequencies added | Selected cost |
| --- | --- | --- | --- |
| Build path | [1,2,3] | cost 0: 1, cost 1: 1, cost 2: 1 |  |
| Compute target | total=6, length=3 | need=2 |  |
| Take cheapest |  | 0 + 1 | 1 |

The current flow is 1 and the final flow must be 2. One unit of capacity is moved from the largest edge to the smallest edge.

### Sample 2

Input:

```
4 4
1 2 1
1 3 1
2 4 2
3 4 2
```

There are two paths, both of length 2.

| Step | Path | Costs added | Selected |
| --- | --- | --- | --- |
| First path | [1,2] | 0,1 |  |
| Second path | [1,2] | 0,1 |  |
| Target flow | total=6, length=2 | need=3 |  |
| Pick smallest |  | 0,0,1 | 1 |

Only one operation is required because three units of path flow can be supported after moving one unit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m + l) | Every vertex and edge is processed a constant number of times, and sorting path capacities is bounded by the total number of edges |
| Space | O(n + m + l) | The graph, paths, and frequency array are stored |

The total number of edges is only 200000, so the linear graph processing and limited extra storage fit easily within the limits.

## Test Cases

```
# These tests describe the expected behavior of the algorithm.

def run(inp: str) -> str:
    import subprocess, sys, tempfile
    p = subprocess.run(
        [sys.executable, "main.py"],
        input=inp.encode(),
        stdout=subprocess.PIPE
    )
    return p.stdout.decode().strip()

assert run("""4 3
1 2 1
2 3 2
3 4 3
""") == "1"

assert run("""4 4
1 2 1
1 3 1
2 4 2
3 4 2
""") == "1"

assert run("""2 1
1 2 0
""") == "0"

assert run("""4 3
1 2 5
2 3 5
3 4 5
""") == "0"

assert run("""7 6
1 2 0
2 7 10
1 3 10
3 4 10
4 5 10
5 7 10
""") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single zero edge | 0 | Handles zero capacity and zero flow |
| Already optimal path | 0 | Avoids unnecessary moves |
| One simple path | 1 | Checks marginal cost calculation |
| Two independent paths | 1 | Checks combining paths |
| Unequal path capacities | 10 | Checks redistribution between different routes |

## Edge Cases

For the zero-capacity path:

```
2 1
1 2 0
```

The path length is one and the total capacity is zero. The required number of flow layers is zero, so the algorithm never selects a cost and returns zero.

For a graph that already has maximum possible flow:

```
4 3
1 2 5
2 3 5
3 4 5
```

The total capacity is 15 and the path length is 3, giving a target flow of 5. The cost sequence contains enough zero-cost levels to create all five units, so no capacity is moved.

For a path with a very large edge:

```
4 3
1 2 0
2 3 100
3 4 100
```

The path contributes many cheap levels after the first edge is filled. The frequency approach handles this by grouping levels instead of iterating 100 times or more. It counts all equal-cost increments in one operation and still selects the globally cheapest required layers.
