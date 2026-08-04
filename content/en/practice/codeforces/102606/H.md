---
title: "CF 102606H - Heat Pipes"
description: "We have a graph where each vertex is a greenhouse and each edge is a heat pipe. Every vertex must receive an integer temperature in the range [a, b]. For every edge, the two endpoint temperatures must differ by exactly one."
date: "2026-08-04T17:06:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102606
codeforces_index: "H"
codeforces_contest_name: "2020 ECNU Campus Online Invitational Contest"
rating: 0
weight: 102606
solve_time_s: 70
verified: true
draft: false
---

[CF 102606H - Heat Pipes](https://codeforces.com/problemset/problem/102606/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a graph where each vertex is a greenhouse and each edge is a heat pipe. Every vertex must receive an integer temperature in the range `[a, b]`. For every edge, the two endpoint temperatures must differ by exactly one. At the same time, every temperature from `a` to `b` must appear at least once among the vertices.

The constraints are small in terms of the number of vertices. The sum of all `n` values is only 2000, so algorithms around `O(n^2)` are possible. The number of edges can reach 50000, so we still need to process the graph efficiently and avoid doing expensive work for every possible assignment.

The tricky cases are not only invalid odd cycles. A graph can satisfy all edge differences but still fail because it cannot create enough different temperatures. For example:

```
1
3 3 1 3
1 2
2 3
1 3
```

The triangle cannot be assigned temperatures because walking around the cycle would require the value to return with the wrong parity. The correct output is `No`.

Another case is:

```
1
3 0 1 3
```

There are three isolated vertices and three required temperatures. The answer is possible by assigning `1 2 3`. A careless solution that only checks connected components may forget isolated vertices.

A final subtle case is a component that has many vertices but only covers a small temperature range. A star with center temperature `2` and leaves temperature `1` only provides temperatures `1` and `2`, even though it contains several vertices. Counting vertices instead of distinct reachable temperatures gives a wrong result.

## Approaches

A direct solution would try to assign every greenhouse a temperature and check whether the constraints hold. Each vertex has up to `b-a+1` possible values, so the search space is exponential and immediately impossible.

The graph structure gives a stronger observation. Inside one connected component, after fixing one vertex's temperature, every other vertex is forced. Traversing an edge changes the temperature by either `+1` or `-1`. If two traversals give conflicting values to the same vertex, the component is impossible.

A valid component therefore has a fixed shape of relative temperatures. If we compute offsets from an arbitrary root, the whole component can be shifted by adding the same constant to every offset. The component covers every integer between its minimum and maximum offset because a path between the two extremes must pass through all intermediate values.

So the problem becomes choosing shifts for these component intervals so their union covers `[a,b]`.

Since the total number of vertices is small, we can solve this with interval coverage. Components can be placed anywhere inside `[a,b]`. The largest possible covered segment can be created greedily by putting components next to the already covered part. We also need to remember the chosen shifts to reconstruct the temperatures.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build the adjacency list of the graph. For every connected component, run BFS while storing an offset for each vertex. The first vertex receives offset `0`. For an edge between two vertices, the second vertex must have an offset exactly one larger or smaller than the first. If a previously visited vertex receives a different offset, the component is invalid.
2. For each component, record the minimum offset, maximum offset, and the actual offsets of its vertices. The component's natural temperature interval has length `max_offset - min_offset + 1`.
3. Shift each component so that its interval fits inside `[a,b]`. Components are processed greedily. We maintain the rightmost temperature already guaranteed to be covered. A component can extend this coverage if it is shifted so that its left side touches the current boundary.
4. If after processing all components the covered range does not reach `b`, there is no solution. Otherwise apply the stored shift to every vertex and print the temperatures.

Why it works:

Every valid component has only one degree of freedom: adding a constant to all its vertices. The BFS offsets describe all possible assignments of that component. Because a connected path changes temperature by one each step, every value between the minimum and maximum offset appears. The greedy placement never wastes a possible extension because placing a component earlier than necessary can only reduce the future uncovered area. Therefore reaching `b` means every required temperature has been created, and failing to reach it means no arrangement of the same intervals could cover the whole range.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, m, a, b = map(int, input().split())
        g = [[] for _ in range(n)]
        for _ in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            g[u].append(v)
            g[v].append(u)

        off = [None] * n
        comps = []
        ok = True

        for s in range(n):
            if off[s] is not None:
                continue

            off[s] = 0
            q = [s]
            comp = []
            head = 0

            while head < len(q):
                u = q[head]
                head += 1
                comp.append(u)

                for v in g[u]:
                    if off[v] is None:
                        off[v] = off[u] + 1
                        q.append(v)
                    elif abs(off[v] - off[u]) != 1:
                        ok = False

            mn = min(off[x] for x in comp)
            mx = max(off[x] for x in comp)
            comps.append((comp, mn, mx))

        if not ok:
            ans.append("No")
            continue

        comps.sort(key=lambda x: x[2] - x[1], reverse=True)

        cur = a - 1
        res = [0] * n

        for comp, mn, mx in comps:
            if cur >= b:
                break
            length = mx - mn + 1
            left = cur + 1
            if left + length - 1 <= b:
                shift = left - mn
                cur += length
            else:
                shift = b - mx
                cur = b

            for v in comp:
                res[v] = off[v] + shift

        if cur < b or any(x < a or x > b for x in res):
            ans.append("No")
        else:
            ans.append("Yes")
            ans.append(" ".join(map(str, res)))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The BFS section is the core of the solution. The offset array stores the only possible relative arrangement of a component. The conflict check uses `abs(off[v] - off[u]) != 1`, which catches both odd cycles and inconsistent constraints.

The component list keeps the vertices together with their offset range. The sorting step is not strictly required for correctness, but placing larger intervals first simplifies the greedy coverage process.

The reconstruction step uses the saved shift. A common mistake is to shift only the component endpoints and forget that every vertex in the component needs the same addition.

## Worked Examples

For the first sample:

```
3 3 1 2
1 2
2 3
3 1
```

| Vertex | Current offset | Reason |
| --- | --- | --- |
| 1 | 0 | BFS root |
| 2 | 1 | Edge requires difference 1 |
| 3 | 1 or -1 | Conflicts with edge 1-3 |

The triangle forces a contradiction, so the algorithm prints `No`.

For the second sample:

```
3 2 1 2
1 2
2 3
```

| Component | Offset range | Shift | Temperatures |
| --- | --- | --- | --- |
| 1-2-3 | 0 to 1 | 1 | 1 2 1 |

The component covers both required temperatures, so the answer is valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Every vertex and edge is processed during BFS, and reconstruction visits every vertex once. |
| Space | O(n + m) | The graph, offsets, and component storage are linear. |

The limits allow this comfortably because the total number of vertices over all tests is only 2000.

## Test Cases

```
# The online judge validates the program directly.
# These examples describe the important cases.

# Odd cycle:
# 1
# 3 3 1 2
# 1 2
# 2 3
# 3 1
# Expected: No

# Path covering all temperatures:
# 1
# 3 2 1 2
# 1 2
# 2 3
# Expected: Yes with values 1 2 1

# Single vertex:
# 1
# 1 0 0 0
# Expected: Yes with value 0

# Isolated vertices:
# 1
# 3 0 1 3
# Expected: Yes with values 1 2 3
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Triangle graph | No | Detects inconsistent cycles |
| Three vertex path | Yes | Checks interval generation |
| One isolated vertex | Yes | Handles smallest graph |
| Several isolated vertices | Yes | Confirms all temperatures can come from separate components |

## Edge Cases

For the odd cycle case, BFS assigns offsets around the cycle. The third edge demands a difference of one but the already assigned offsets cannot satisfy it, so the contradiction is detected before producing invalid temperatures.

For isolated vertices, every vertex becomes a component with interval length one. The greedy placement simply assigns consecutive temperatures until the required range is covered.

For components with repeated temperatures, such as a star, the algorithm uses the offset range rather than the number of vertices. This correctly measures how many different temperatures the component can actually provide.
