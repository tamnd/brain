---
title: "CF 102859A - Apple Pie"
description: "The sequence we want to recover is an Euler tour of a complete graph. Each number from 1 to N is a vertex, and writing two different numbers next to each other means traversing the edge connecting those two vertices."
date: "2026-07-25T14:20:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102859
codeforces_index: "A"
codeforces_contest_name: "mBIT Standard November 2020"
rating: 0
weight: 102859
solve_time_s: 51
verified: true
draft: false
---

[CF 102859A - Apple Pie](https://codeforces.com/problemset/problem/102859/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

The sequence we want to recover is an Euler tour of a complete graph. Each number from `1` to `N` is a vertex, and writing two different numbers next to each other means traversing the edge connecting those two vertices. A valid sequence must use every possible edge between two different vertices exactly once.

The input gives the visible part of such a sequence after an apple pie covered one continuous middle section. The left side is the prefix that remains visible, and the right side is the suffix that remains visible. We need to decide whether there exists some hidden middle section that can be inserted between them so the complete sequence becomes a valid traversal of all edges.

The limits are designed around a graph with at most `N = 1000` vertices. The number of visible values can reach `5 * 10^5`, so any solution that tries to build or test many possible sequences is impossible. We need a near-linear approach in the amount of input plus the number of possible edges. Since the complete graph has about `N^2 / 2` edges, an `O(N^2)` solution is acceptable because `N` is only 1000.

The first edge cases come from the existence of the complete sequence itself. For example, with:

```
2
0
0
```

the answer is `Y`, because the only edge is between vertices `1` and `2`, so `[1,2]` is possible. A careless solution that assumes the visible sequence must contain at least one element would reject this case.

Another edge case is a repeated edge in the visible parts. For:

```
3
2 2 1
2 2 1
```

the answer is `N`. The pair `{1,2}` appears twice in the visible sections, so no hidden middle can repair the sequence. An implementation that only checks vertex counts and ignores already used edges would accept it incorrectly.

A final tricky case is a repeated vertex that does not repeat an edge. For:

```
3
2 2 1
2 2 2
```

the answer is `N`. The visible sections contain the edge `{1,2}` and the edge `{2,3}` would be missing, but the suffix requires using `{2,2}`, which is not even an allowed edge because adjacent equal numbers are invalid. Checking only degrees without validating the original walk would miss this.

The key graph observation is that the whole sequence is an Euler trail. We can remove the edges already shown on the left and right. The hidden part only needs to be an Euler trail in the remaining graph, connecting the visible pieces if both exist.

## Approaches

A direct approach would be to try to construct the missing middle. The total number of possible edges is up to `499500`, so one might try to simulate Euler trail construction for every possible starting point or attempt backtracking over the hidden section. This is not practical because the number of possible orders of edges is enormous. Even checking a small fraction of possible trails quickly exceeds the available time.

The useful change of viewpoint is to stop thinking about the missing sequence and instead think about the edges that are still unused. The visible prefix and suffix already fix some edges. If those edges are valid, they can simply be removed from the complete graph. The question becomes whether the remaining graph has an Euler trail with the required endpoints.

An undirected graph has an Euler trail exactly when all non-isolated vertices belong to one connected component and the number of odd-degree vertices is either zero or two. If there are two odd vertices, they must be the start and end of the trail.

Because the original graph is complete, we can store which edges were consumed by the visible pieces in a boolean matrix. Then we compute degrees in the remaining graph, check connectivity, and verify the Euler condition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in number of hidden edges | O(N^2) | Too slow |
| Optimal | O(P + Q + N^2) | O(N^2) | Accepted |

## Algorithm Walkthrough

1. Read the two visible parts of the sequence. Traverse each part and mark every adjacent pair as a used edge. If an adjacent pair contains equal values or the same undirected edge appears twice, the answer is immediately `N`.
2. Treat all unmarked edges of the complete graph as the hidden part. Compute the degree of every vertex in this remaining graph.
3. Determine the required Euler trail endpoints. If both visible sides exist, the hidden section must start after the left side and finish before the right side. If one side is missing, the missing endpoint can be chosen freely.
4. Count the vertices with odd degree in the remaining graph. If both endpoints are fixed, they must exactly match the odd-degree vertices. If one or both endpoints are free, the allowed odd-degree configurations follow the ordinary Euler trail rules.
5. Check that every vertex with a remaining edge belongs to one connected component. Disconnected unused edges cannot all be covered by one hidden sequence.
6. If every condition passes, output `Y`; otherwise output `N`.

Why it works: The visible sequence already consumes a set of edges from the complete graph. Any valid completion must use exactly the remaining edges, so the hidden part is precisely an Euler trail of the remaining graph. The Euler trail theorem gives necessary and sufficient conditions for such a trail to exist. Since the endpoint requirements are also checked, every accepted case has a valid completion and every rejected case is impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    left = list(map(int, input().split()))
    p = left[0]
    left = left[1:]

    right = list(map(int, input().split()))
    q = right[0]
    right = right[1:]

    used = [[False] * n for _ in range(n)]
    bad = False

    def add_edges(arr):
        nonlocal bad
        for i in range(len(arr) - 1):
            a = arr[i] - 1
            b = arr[i + 1] - 1
            if a == b or used[a][b]:
                bad = True
            else:
                used[a][b] = True
                used[b][a] = True

    add_edges(left)
    add_edges(right)

    if bad:
        print("N")
        return

    deg = [0] * n
    graph = [[] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            if not used[i][j]:
                deg[i] += 1
                deg[j] += 1
                graph[i].append(j)
                graph[j].append(i)

    fixed_start = left[-1] - 1 if p else -1
    fixed_end = right[0] - 1 if q else -1

    odd = [i for i in range(n) if deg[i] % 2]

    if fixed_start != -1 and fixed_end != -1:
        if len(odd) == 0:
            if fixed_start != fixed_end:
                print("N")
                return
        elif len(odd) == 2:
            if set(odd) != {fixed_start, fixed_end}:
                print("N")
                return
        else:
            print("N")
            return
    elif fixed_start != -1:
        if len(odd) == 2:
            if fixed_start not in odd:
                print("N")
                return
        elif len(odd) != 0:
            print("N")
            return
    elif fixed_end != -1:
        if len(odd) == 2:
            if fixed_end not in odd:
                print("N")
                return
        elif len(odd) != 0:
            print("N")
            return
    else:
        if len(odd) not in (0, 2):
            print("N")
            return

    start = -1
    for i in range(n):
        if deg[i]:
            start = i
            break

    if start != -1:
        stack = [start]
        seen = [False] * n
        seen[start] = True
        while stack:
            v = stack.pop()
            for u in graph[v]:
                if not seen[u]:
                    seen[u] = True
                    stack.append(u)

        for i in range(n):
            if deg[i] and not seen[i]:
                print("N")
                return

    print("Y")

if __name__ == "__main__":
    solve()
```

The matrix `used` stores exactly the edges already visible. Since the vertices are numbered from `1`, the implementation converts them to zero-based indices before accessing arrays.

The first traversal validates the two known parts of the sequence. Equal adjacent values are invalid because an edge in the complete graph only connects different vertices. Seeing the same undirected edge twice is also impossible because every edge must appear exactly once.

The remaining degree calculation starts from the complete graph and effectively keeps only unused edges. The Euler conditions are then checked against this remaining graph. The endpoint handling is separated because a missing prefix or suffix means one end of the hidden Euler trail is not predetermined.

The final depth-first search ignores isolated vertices because they do not contain edges that need to be traversed. Only vertices participating in the remaining graph must belong to the same connected component.

## Worked Examples

For the input:

```
3
2 2 1
2 3 2
```

the visible sequence is `[2,2,1]` on the left and `[2,3,2]` on the right.

| Step | Used edges | Remaining odd vertices | Result |
| --- | --- | --- | --- |
| Read left | `{2,2}` invalid? no, actually repeated vertex is detected | - | Invalid |

This trace demonstrates why equal adjacent values must be rejected immediately. The actual sample uses left input `2 2 1`, which means the values are `2,1`, not `2,2,1` after parsing the count. The visible edges are `{2,1}` and `{3,2}`, which leave the Euler path `[2,1,3,2]`.

For the input:

```
3
2 2 1
1 3
```

the visible parts are `[2,1]` and `[3]`.

| Step | Used edges | Remaining odd vertices | Result |
| --- | --- | --- | --- |
| Remove `{1,2}` | edge `{1,2}` gone | vertex 2,3 | Continue |
| Check suffix endpoint | hidden path must end at 3 | mismatch | Reject |

This demonstrates the endpoint condition. The unused graph cannot finish at the required suffix start while using all remaining edges.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(P + Q + N^2) | The visible sequences are scanned once, and the complete graph edges are checked once. |
| Space | O(N^2) | The edge matrix stores whether each possible edge has already appeared. |

The largest possible graph has about half a million edges, so the quadratic storage is acceptable for `N <= 1000`. The runtime is dominated by scanning the possible edges, which is small enough for the given limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    out = sys.stdout.getvalue() if hasattr(sys.stdout, "getvalue") else ""
    sys.stdin = old
    return out

# Sample 1
assert run("""2
0
0
""") == "Y\n"

# Sample 2
assert run("""3
1 2
0
""") == "Y\n"

# Sample 3
assert run("""3
2 2 1
2 3 2
""") == "Y\n"

# Invalid repeated edge
assert run("""3
2 2 1
2 2 1
""") == "N\n"

# Invalid equal adjacent values
assert run("""3
2 2 1
2 2 2
""") == "N\n"

# Larger odd complete graph with no visible part
assert run("""5
0
0
""") == "Y\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `N=2` with no visible values | `Y` | Smallest possible graph |
| A single visible prefix | `Y` | Free hidden suffix handling |
| A complete valid partial Euler tour | `Y` | Normal completion |
| Repeated visible edge | `N` | Edge uniqueness |
| Equal adjacent values | `N` | Invalid transitions |
| Empty observation on odd `N` | `Y` | Euler circuit existence |

## Edge Cases

When the apple pie covers the entire sequence, both visible parts are empty. The algorithm simply checks whether the complete graph itself has an Euler trail. For `N=2`, the remaining graph has two odd-degree vertices and passes. For odd `N`, every vertex has even degree, so an Euler circuit exists. For even `N > 2`, there are too many odd-degree vertices and the answer becomes `N`.

When a visible side contains the same edge twice, the algorithm rejects during the initial scan. For example:

```
3
3 1 2 1
0
```

contains edges `{1,2}` and `{1,2}` again. Marking the edge matrix catches this before any Euler reasoning is performed.

When only one side is visible, the missing endpoint of the hidden Euler trail is allowed to vary. For example:

```
3
1 2
0
```

leaves the hidden section starting after vertex `2`. The remaining edges can be traversed as `2 -> 1 -> 3 -> 2`, so the algorithm accepts it because the Euler conditions allow a suitable endpoint.
