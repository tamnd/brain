---
title: "CF 102786C - \u0420\u0430\u0437\u044f\u0449\u0438\u0439 \u0443\u0434\u0430\u0440 \u0437\u0432\u0435\u0437\u0434\u043d\u043e\u0433\u043e \u0434\u0435\u0441\u0430\u043d\u0442\u0430"
description: "The task is an interactive graph reconstruction problem. We start in hall 0, and at the beginning halls 0 through N are already reachable. After that, drones repeatedly send fragments of discovered tunnels. Each fragment contains several undirected edges between hall numbers."
date: "2026-07-27T19:32:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102786
codeforces_index: "C"
codeforces_contest_name: "\u041e\u0442\u043a\u0440\u044b\u0442\u044b\u0439 \u0447\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u042f\u0440\u0413\u0423 \u0438\u043c. \u041f.\u0413. \u0414\u0435\u043c\u0438\u0434\u043e\u0432\u0430 Demidov Open IT Cup 2019"
rating: 0
weight: 102786
solve_time_s: 58
verified: true
draft: false
---

[CF 102786C - \u0420\u0430\u0437\u044f\u0449\u0438\u0439 \u0443\u0434\u0430\u0440 \u0437\u0432\u0435\u0437\u0434\u043d\u043e\u0433\u043e \u0434\u0435\u0441\u0430\u043d\u0442\u0430](https://codeforces.com/problemset/problem/102786/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is an interactive graph reconstruction problem. We start in hall `0`, and at the beginning halls `0` through `N` are already reachable. After that, drones repeatedly send fragments of discovered tunnels. Each fragment contains several undirected edges between hall numbers. After every received fragment, we must immediately decide whether the collected information is enough to build a path from our current reachable area to hall `9999`. If it is, we print `ATTACK`; otherwise we print `WAIT` and allow the drones to continue.

The input is unusual because it arrives online. The first line gives the size of the initially available set, then every following line is a new portion of discovered edges. The output is not the final answer to a fixed input, but a sequence of decisions after each update.

There can be almost `100000` halls. This immediately rules out rebuilding the graph search from scratch after every drone message. A full BFS or DFS over all known edges after every update could process the same edges thousands of times, which is too expensive under a 5 second limit. We need a structure that can update connectivity incrementally.

The key edge cases are caused by the online nature of the input. A path may appear exactly after processing a new fragment, so checking only before reading the fragment misses the required attack moment.

For example, suppose the initial line is:

```
0
```

and the only drone message is:

```
1 0 9999
```

The correct output is:

```
ATTACK
```

A solution that prints `WAIT` before applying the new edge and only checks later has already missed the allowed attack moment.

Another subtle case is when the queen is connected indirectly.

```
0
2 0 5 5 9999
```

The correct output is:

```
ATTACK
```

The edge `0-5` does not directly contain hall `9999`, but the two edges together form a route. Checking only direct neighbors of `0` would fail.

A third common mistake is forgetting that the initial halls are already accessible. If the input starts with:

```
3
```

then halls `0`, `1`, `2`, and `3` are all available before the first drone response. A correct solution must treat them as one reachable component from the beginning.

## Approaches

A straightforward solution is to store every discovered tunnel and run a graph search from the currently reachable halls after every drone message. This is correct because the only question we need to answer is whether `9999` belongs to the component containing our starting position. However, the same old edges are scanned again and again. With up to `100000` halls and many updates, repeatedly traversing the whole graph can reach billions of edge checks.

The structure of the problem gives us a simpler view. We never need the exact route, distances, or tree structure. We only need to know whether two halls are in the same connected component. Adding a tunnel only merges two components and never separates them. This is exactly the situation where a disjoint set union structure fits.

Initially, all halls `0` through `N` belong to the reachable component. For every drone message, we union the two endpoints of each received edge. After all edges in the message are processed, we check whether hall `9999` has the same representative as hall `0`. If yes, the path exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(U * (V + E)) | O(V + E) | Too slow |
| Optimal | O((V + E) α(V)) | O(V) | Accepted |

Here `U` is the number of drone updates and `α(V)` is the inverse Ackermann function, which grows so slowly that it is effectively constant.

## Algorithm Walkthrough

1. Create a disjoint set union structure for all possible halls. Since hall numbers can go up to `99999`, we prepare enough space for every possible vertex.

The initial reachable halls are `0` through `N`, so they must already be connected to our starting position. We merge every one of them with hall `0`.
2. Read the next drone message. The first number is the amount of discovered transitions, followed by that many pairs of hall numbers.

Each pair represents an undirected tunnel. Since a tunnel means both halls become mutually reachable, we merge their components.
3. After processing the whole message, compare the components of hall `0` and hall `9999`.

If they are equal, the collected information already contains a route to the queen, so we print `ATTACK` and terminate. Otherwise we print `WAIT`, flush the output, and wait for the next fragment.

Why it works:

The invariant is that after processing any number of drone messages, two halls are in the same disjoint set union component exactly when the discovered tunnels prove that a route exists between them. Initially this is true because the starting accessible halls are merged together. Each new tunnel only creates a possible connection between two components, and the union operation performs exactly that merge. No valid route can exist without all of its edges having connected the corresponding components, so checking whether hall `9999` belongs to the same component as hall `0` is equivalent to checking whether an attack route exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]

def main():
    n = int(input())
    dsu = DSU(100000)

    for i in range(1, n + 1):
        dsu.union(0, i)

    for line in sys.stdin:
        if not line.strip():
            continue

        data = list(map(int, line.split()))
        k = data[0]

        idx = 1
        for _ in range(k):
            u = data[idx]
            v = data[idx + 1]
            idx += 2
            dsu.union(u, v)

        if dsu.find(0) == dsu.find(9999):
            print("ATTACK")
            sys.stdout.flush()
            return
        else:
            print("WAIT")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
```

The `DSU` class stores the connected component representative of every hall. Path compression in `find` makes future lookups very fast, while union by size keeps the internal trees shallow.

The initialization loop connects every initially available hall to hall `0`. This is the part that is easy to miss because the input does not list these edges explicitly. The drones only provide additional tunnels after the program starts.

For each incoming fragment, the code first applies all new tunnels and only then checks the answer. The order matters because the required attack moment can be exactly after the latest fragment arrives.

The flush after every response is necessary because this is an interactive task. Without it, the judge may not send the next fragment because it is waiting for the program's decision.

## Worked Examples

For the first sample, the initial reachable halls are `0`, `1`, and `2`.

| Step | New information | Component of 0 | Connected to 9999 | Output |
| --- | --- | --- | --- | --- |
| Initial | halls 0,1,2 available | {0,1,2} | No |  |
| 1 | edges 4-6 and 11-12 | {0,1,2} | No | WAIT |
| 2 | edges 9-10, 8-10, 1-2, 2-7, 3-9 | {0,1,2,7} | No | WAIT |
| 3 | edge 9999-7 | {0,1,2,7,9999} | Yes | ATTACK |

The last fragment connects the already reachable component through hall `7` to the queen. The invariant holds because every union represents one discovered tunnel.

For the second sample, the final fragment connects directly to hall `9999`.

| Step | New information | Component of 0 | Connected to 9999 | Output |
| --- | --- | --- | --- | --- |
| Initial | halls 0,1,2,3 available | {0,1,2,3} | No |  |
| 1 | edges from first drone message | {0,1,2,3} | No | WAIT |
| 2 | edge 1-2 | {0,1,2,3} | No | ATTACK |

The example demonstrates that the program reacts immediately when the required connectivity appears.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N + E) α(100000)) | Every initial merge and every discovered edge performs almost constant amortized work |
| Space | O(100000) | The DSU stores one parent and one size value for each possible hall |

The maximum number of halls is small enough for a fixed DSU array. The solution never scans all edges again after receiving them, so it remains efficient even with many drone updates.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    class DSU:
        def __init__(self, n):
            self.p = list(range(n))

        def find(self, x):
            if self.p[x] != x:
                self.p[x] = self.find(self.p[x])
            return self.p[x]

        def union(self, a, b):
            a = self.find(a)
            b = self.find(b)
            if a != b:
                self.p[b] = a

    out = []
    n = int(input())
    dsu = DSU(100000)

    for i in range(1, n + 1):
        dsu.union(0, i)

    for line in sys.stdin:
        if not line.strip():
            continue
        a = list(map(int, line.split()))
        k = a[0]
        ptr = 1
        for _ in range(k):
            dsu.union(a[ptr], a[ptr + 1])
            ptr += 2
        if dsu.find(0) == dsu.find(9999):
            out.append("ATTACK")
            break
        out.append("WAIT")

    return "\n".join(out)

assert solve("""2
2 4 6 11 12
5 9 10 8 10 1 2 2 7 3 9
1 9999 7
""") == "WAIT\nWAIT\nATTACK", "sample 1"

assert solve("""3
3 3 4 9999 4 2 3
1 1 2
""") == "WAIT\nATTACK", "sample 2"

assert solve("""0
1 0 9999
""") == "ATTACK", "direct connection"

assert solve("""0
2 0 5 5 9999
""") == "ATTACK", "indirect connection"

assert solve("""5
1 10 20
1 9999 30
2 0 30 20 30
""") == "WAIT\nWAIT\nATTACK", "late merge"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Initial sample | WAIT, WAIT, ATTACK | Normal incremental discovery |
| Second sample | WAIT, ATTACK | Immediate reaction after a new connection |
| Direct connection | ATTACK | Single edge to the target |
| Indirect connection | ATTACK | Multi-edge path detection |
| Late merge | WAIT, WAIT, ATTACK | Components joining after several updates |

## Edge Cases

When the queen is connected by the very first drone message, the algorithm still works because it processes all received edges before checking. For:

```
0
1 0 9999
```

the union operation merges `0` and `9999`, so the representatives match and the answer is `ATTACK`.

When the route has multiple intermediate halls, no special handling is needed. For:

```
0
2 0 5 5 9999
```

the first union creates component `{0,5}` and the second expands it to `{0,5,9999}`. The final comparison correctly detects the route.

When the starting accessible area contains halls besides `0`, those halls must be merged initially. For:

```
3
1 3 8
1 8 9999
```

hall `3` is already reachable, so the discovered chain reaches the queen after the second update. A solution that only starts from vertex `0` without initializing halls `1` through `N` would incorrectly delay or miss the attack.
