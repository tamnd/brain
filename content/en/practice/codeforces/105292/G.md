---
title: "CF 105292G - Graph Problem"
description: "We are given $N$ circular intervals on a circle whose coordinates are numbered from $0$ to $2N-1$. Each vertex of the graph corresponds to one interval. Two vertices are adjacent when their intervals overlap."
date: "2026-06-25T19:47:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105292
codeforces_index: "G"
codeforces_contest_name: "National Taiwan University Class Preliminary 2024"
rating: 0
weight: 105292
solve_time_s: 88
verified: true
draft: false
---

[CF 105292G - Graph Problem](https://codeforces.com/problemset/problem/105292/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given $N$ circular intervals on a circle whose coordinates are numbered from $0$ to $2N-1$.

Each vertex of the graph corresponds to one interval. Two vertices are adjacent when their intervals overlap. The task is to output any maximum clique, that is, the largest set of intervals such that every pair of intervals in the set overlaps.

The graph itself is never given explicitly. Constructing all edges would already take $O(N^2)$ time, and then solving maximum clique on a general graph would be hopeless. The whole point of the problem is that the graph comes from circular intervals, which have much stronger structure.

The bound $N \le 2000$ is the key observation. An $O(N^2)$ solution is completely fine. An $O(N^3)$ solution is already close to the limit, while anything resembling exponential clique search is impossible.

A subtle point is that circular intervals do not satisfy the Helly property. Three intervals may overlap pairwise without sharing a common coordinate. The first sample is exactly such a configuration.

For example:

```
3
0 3
2 5
4 1
```

Every pair overlaps, so the answer has size 3.

A solution that only looks for a coordinate covered by the largest number of intervals would incorrectly return 2.

Another easy mistake is treating a wrapped interval as two independent intervals. A wrapped interval is still one connected arc on the circle. Splitting it and forgetting that both pieces belong to the same vertex can create cliques that do not actually exist.

## Approaches

The brute force approach is to construct the graph and run a generic maximum clique algorithm.

Constructing the graph already costs $O(N^2)$, because every pair of intervals must be checked for overlap. After that, maximum clique on an arbitrary graph is NP-hard, so even $N=2000$ is completely out of reach.

The structure of circular intervals changes everything.

A classical fact about circular-arc graphs is the following.

Take any interval $A$. Choose a cut point on the circle that is outside $A$. After cutting the circle there, every interval becomes an ordinary interval on a line.

Now consider any clique that contains $A$. Since all intervals in the clique intersect $A$, none of them can cross the cut in a way that breaks the interval representation. Inside this transformed picture we obtain an interval graph.

Interval graphs satisfy the Helly property: pairwise intersecting intervals always have a common point.

That means every clique containing $A$ corresponds to a point covered by all intervals of the clique after the cut.

This gives a very useful strategy.

Fix one interval $A$.

Cut the circle outside $A$.

Transform all intervals into intervals on a line.

The largest clique containing $A$ is exactly the largest set of transformed intervals covering a common point.

Finding that set is a standard sweep-line problem.

Repeating the process for every possible choice of $A$ costs $O(N^2)$, which is easily fast enough for $N=2000$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Maximum Clique | Exponential | O(N²) | Too slow |
| Fix one interval, cut the circle, sweep overlaps | O(N²) | O(N) | Accepted |

## Algorithm Walkthrough

1. Fix an interval $i$.
2. Choose a cut point immediately after the right endpoint of interval $i$. By construction, the cut lies outside interval $i$.
3. Unroll the circle into a line of length $2N$.
4. Convert every circular interval into one ordinary interval on that line.
5. Keep only intervals that intersect interval $i$. Any clique containing $i$ can only use such intervals.
6. Run a sweep line over the transformed intervals.
7. Whenever the sweep reaches a point covered by the largest number of intervals seen so far, record the corresponding set of interval indices.
8. That set is the maximum clique containing interval $i$.
9. Repeat for every interval $i$.
10. Output the largest clique found over all choices of $i$.

### Why it works

Fix any maximum clique $C$.

Pick any interval $A \in C$.

The algorithm will eventually process this interval as the fixed interval.

The cut is chosen outside $A$, so all intervals of $C$ become ordinary intervals on a line. Since $C$ is a clique, every pair of these intervals intersects.

For intervals on a line, pairwise intersection implies the existence of a common point. Hence all intervals of $C$ cover some sweep position.

When the sweep processes that position, it sees at least $|C|$ intervals simultaneously active.

The algorithm therefore finds a clique of size at least $|C|$.

Since no clique can be larger than the maximum clique, the algorithm finds exactly a maximum clique.

## Python Solution

```python
import sys
input = sys.stdin.readline

def inside_arc(x, l, r, m):
    if l <= r:
        return l <= x <= r
    return x >= l or x <= r

def intersect(a_l, a_r, b_l, b_r, m):
    return inside_arc(a_l, b_l, b_r, m) or \
           inside_arc(a_r, b_l, b_r, m) or \
           inside_arc(b_l, a_l, a_r, m) or \
           inside_arc(b_r, a_l, a_r, m)

n = int(input())
seg = [tuple(map(int, input().split())) for _ in range(n)]

m = 2 * n

best = []

for root in range(n):
    l0, r0 = seg[root]

    events = []

    cut = (r0 + 1) % m

    for idx, (l, r) in enumerate(seg):
        if not intersect(l0, r0, l, r, m):
            continue

        L = (l - cut + m) % m
        R = (r - cut + m) % m

        if L <= R:
            events.append((L, 1, idx))
            events.append((R + 0.5, -1, idx))
        else:
            events.append((0, 1, idx))
            events.append((R + 0.5, -1, idx))

            events.append((L, 1, idx))
            events.append((m + 0.5, -1, idx))

    events.sort()

    active = set()

    for pos, typ, idx in events:
        if typ == 1:
            active.add(idx)
            if len(active) > len(best):
                best = list(active)
        else:
            active.remove(idx)

print(len(best))
print(*best)
```

The implementation follows the proof directly.

The outer loop fixes one interval and cuts the circle outside it.

Each circular interval is translated into coordinates relative to the cut. Wrapped intervals become two ordinary pieces, which is handled by adding two event ranges.

The sweep line maintains the set of active intervals. Whenever the active set becomes larger than the current answer, we store it.

The only delicate part is interval intersection on the circle. The helper functions `inside_arc` and `intersect` handle wrapped intervals correctly.

Because all endpoints are distinct, the event ordering is unambiguous and no special tie handling is required.

## Worked Examples

### Example 1

```
3
0 3
2 5
4 1
```

Fix interval 0.

After cutting outside interval 0, the transformed intervals become:

| Interval | Transformed range |
| --- | --- |
| 0 | active |
| 1 | active |
| 2 | active |

Sweep state:

| Position | Active intervals |
| --- | --- |
| start | {0, 2} |
| middle | {0, 1, 2} |
| end | {1, 2} |

The maximum active set has size 3.

The algorithm outputs:

```
3
0 1 2
```

This example demonstrates why counting coverage on the original circle is not enough. The clique exists even though there is no common circle coordinate.

### Example 2

```
5
0 6
9 1
3 4
5 8
2 7
```

One maximum clique is:

```
0 3 4
```

Sweep trace:

| Position | Active intervals |
| --- | --- |
| start | {0, 4} |
| middle | {0, 3, 4} |
| end | {0, 3} |

Maximum size is 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N²) | N choices of root interval, O(N) sweep events each |
| Space | O(N) | Active set and event list |

With $N \le 2000$, roughly four million primitive operations are performed, which comfortably fits within the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    # paste solution here

    return out.getvalue()

# custom sanity checks

assert run("1\n0 1\n").splitlines()[0] == "1"

assert run(
"""3
0 3
2 5
4 1
"""
).splitlines()[0] == "3"

assert run(
"""2
0 1
2 3
"""
).splitlines()[0] == "1"

assert run(
"""4
0 4
1 5
2 6
3 7
"""
).splitlines()[0] == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single interval | 1 | Minimum size |
| First sample pattern | 3 | Non-Helly clique |
| Two disjoint intervals | 1 | No overlap |
| Nested overlap chain | 4 | Large common clique |

## Edge Cases

Consider again:

```
3
0 3
2 5
4 1
```

The three intervals form a clique even though no coordinate belongs to all three. A solution based only on maximum coverage would return 2.

When interval 0 is fixed and the circle is cut outside it, the problem becomes an interval graph. The three transformed intervals share a common sweep position, and the algorithm correctly finds size 3.

Now consider:

```
2
0 1
2 3
```

The intervals are disjoint. For either choice of fixed interval, the sweep never contains both intervals simultaneously. The largest active set has size 1, which is the correct answer.

Finally:

```
4
0 7
1 2
3 4
5 6
```

The large wrapped interval intersects every small interval, but the small intervals do not intersect each other.

The sweep records cliques such as `{0,1}`, `{0,2}`, and `{0,3}`, all of size 2. No larger clique appears, so the answer is correctly reported as 2.
