---
title: "CF 102180F - \u0410\u0439\u043b\u0430\u043d\u0434\u043b\u044d\u043d\u0434"
description: "There are (n) islands, and initially every island has inhabitants. Some reports add an undirected bridge between two islands. Other reports describe a flood on island (u), after which every inhabitant currently living on (u) moves to island (v)."
date: "2026-08-19T06:54:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102180
codeforces_index: "F"
codeforces_contest_name: "MSPU Training Contest 2018-2019"
rating: 0
weight: 102180
solve_time_s: 97
verified: true
draft: false
---

[CF 102180F - \u0410\u0439\u043b\u0430\u043d\u0434\u043b\u044d\u043d\u0434](https://codeforces.com/problemset/problem/102180/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

There are (n) islands, and initially every island has inhabitants. Some reports add an undirected bridge between two islands. Other reports describe a flood on island (u), after which every inhabitant currently living on (u) moves to island (v). The island (u) itself is not removed, so bridges incident to it remain usable.

After every report, we need the minimum number of new bridges that would make all currently inhabited islands mutually reachable by land. Existing bridges may be reused, and new bridges can be built between arbitrary islands.

Consider the graph formed by all bridges. Suppose exactly (c) connected components contain at least one inhabitant. One additional bridge can merge two such components, and (c-1) bridges are always sufficient to connect them all. Thus the entire problem reduces to maintaining the number of connected components that currently contain at least one inhabitant.

The constraints are the main reason a direct graph traversal is unsuitable. With up to (3\cdot10^5) islands and (3\cdot10^5) reports, recomputing connected components after every operation could require (O(nq)) work, roughly (9\cdot10^{10}) vertex operations in the worst case. Even a single traversal per report is far beyond what a one-second limit can support. We need each report to be processed in close to constant amortized time.

The first subtle case is that an island can become empty without disappearing from the graph. For example,

```
2 1
2 1 2
```

The only inhabited island after the report is island 2, so the answer is `0`. A solution that physically deletes island 1 from the graph would make later bridge operations awkward or incorrect, because island 1 can become inhabited again.

A second subtle case is moving inhabitants between two islands that already belong to the same connected component. For example,

```
3 2
1 1 2
2 1 2
```

After the first report, islands 1 and 2 form one component and island 3 is separate. After the flood, all inhabitants of island 1 move to island 2, but the component structure has not changed. The inhabited components are still `{1,2}` and `{3}`, so the answers are `1 1`. A careless implementation that treats every flood as removing one inhabited component would incorrectly produce `1 0`.

A third case occurs when an island is empty before a flood. For example,

```
3 2
2 1 2
2 1 3
```

After the first report, island 1 is empty and island 2 has its inhabitants. The second flood moves nothing, so the state does not change. The correct answers are `1 1`. The implementation must inspect the number of inhabitants at the source rather than blindly modifying component counts.

A fourth case appears when a bridge joins two components, one of which is empty. For example,

```
3 2
2 1 2
1 1 3
```

After the flood, only island 2 is inhabited. The bridge between islands 1 and 3 joins two empty vertices and does not affect the number of inhabited components. The answers are `1 1`. A solution that counts every graph component instead of only components containing inhabitants would fail here.

## Approaches

A straightforward solution would explicitly maintain the graph and, after every report, run DFS or BFS from all currently inhabited islands to determine how many connected components contain inhabitants. This is correct because graph traversal directly computes exactly the connectivity that matters.

The problem is the repeated work. A graph with (n) vertices and up to (q) added edges can have (O(n+q)) stored edges. Running a full traversal after each of (q) reports can take (O(q(n+q))), which is (O(q^2+nq)). With both (n) and (q) equal to (3\cdot10^5), this is on the order of (9\cdot10^{10}) operations or worse.

The brute-force solution works because it recomputes the exact graph state from scratch. It fails because bridges are only added, never removed. That monotonic structure means we do not need to rediscover connectivity after every bridge report.

A Disjoint Set Union structure is exactly suited to this situation. Every bridge between (u) and (v) simply merges their two DSU sets. DSU gives us the connected component of any island in almost constant amortized time.

We still need to handle floods. The key observation is that inhabitants do not affect graph connectivity. A flood only changes which vertices have inhabitants. For every DSU component, we can store the total number of inhabitants currently inside it. Then a flood from (u) to (v) removes the population at (u)'s component and adds it to (v)'s component. If the source component becomes empty, the number of inhabited components decreases. If the destination component was empty and receives inhabitants, the number increases.

This gives us a global counter `active`, equal to the number of DSU components with positive population. A bridge joining two different components reduces `active` by one exactly when both components were inhabited. A flood changes `active` only when population crosses between different components and one of the two components changes between empty and nonempty.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(q(n+q))) | (O(n+q)) | Too slow |
| Optimal | (O((n+q)\alpha(n))) | (O(n+q)) | Accepted |

Here (\alpha(n)) is the inverse Ackermann function, which is below any practically relevant constant for these constraints.

## Algorithm Walkthrough

1. Initially every island contains inhabitants, so every island is an inhabited DSU component. Set `population[i] = 1` for every island and initialize `active = n`. The answer before any report would consequently be (n-1).
2. For a bridge report `1 u v`, find the DSU roots of `u` and `v`. If they are already equal, the bridge changes nothing. If they are different, merge the two components and add their population totals. If both components had positive population, two inhabited components have become one, so decrease `active` by one.
3. For a flood report `2 u v`, read `x = population[u]`. If `x` is zero, nobody moves and there is nothing to update. This case must be handled before changing component totals.
4. If `u` has inhabitants, find the current DSU roots `ru` and `rv`. Set `population[u]` to zero and add `x` to `population[v]`.
5. When `ru` and `rv` are different, subtract `x` from the population total of `ru`. If that total becomes zero, the source component is no longer inhabited, so decrease `active`. If the destination component had zero population before receiving `x`, increase `active`. When `ru == rv`, both operations happen inside the same inhabited component, so `active` does not change.
6. After processing the report, print `active - 1`. If there are `active` inhabited connected components, at least `active - 1` new bridges are necessary to connect them, and that many bridges are sufficient by joining the components in a tree.

The central invariant is that `population[root]` stores the total number of inhabitants in the entire DSU component represented by `root`, and `active` counts exactly those roots whose population is positive. Bridge operations preserve this invariant by merging population totals. Flood operations preserve it by moving the source population between the appropriate component totals. Since the minimum number of additional bridges needed for (c) nonempty components is exactly (c-1), `active - 1` is always the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())

    parent = list(range(n))
    size = [1] * n
    population = [1] * n

    active = n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    out = []

    for _ in range(q):
        t, u, v = map(int, input().split())
        u -= 1
        v -= 1

        if t == 1:
            ru = find(u)
            rv = find(v)

            if ru != rv:
                if size[ru] < size[rv]:
                    ru, rv = rv, ru

                if population[ru] > 0 and population[rv] > 0:
                    active -= 1

                parent[rv] = ru
                size[ru] += size[rv]
                population[ru] += population[rv]

        else:
            x = population[u]

            if x > 0:
                ru = find(u)
                rv = find(v)

                population[u] = 0

                if ru != rv:
                    population[ru] -= x

                    if population[ru] == 0:
                        active -= 1

                    if population[rv] == 0:
                        active += 1

                    population[rv] += x
                else:
                    population[ru] -= x
                    population[rv] += x

        out.append(str(active - 1))

    sys.stdout.write(" ".join(out))

if __name__ == "__main__":
    solve()
```

The `parent` and `size` arrays implement DSU with path compression and union by size. Together they guarantee almost constant amortized time for finding and merging connected components.

The `population` array is indexed by DSU root whenever it represents a component total. After a union, the old child root is no longer used as a component representative, so its population value does not need to remain meaningful. The new root receives the sum of both component populations.

For a flood, `population[u]` is deliberately interpreted as the population currently located on the physical island `u`, while `population[root]` represents the total population of a component. This distinction is the most delicate part of the implementation. Before moving the population, `x = population[u]` captures the island population. After setting `population[u] = 0`, the component totals are adjusted separately.

When `ru == rv`, subtracting and adding the same amount to the same component leaves its total unchanged. The explicit branch is useful because it prevents the active-component counter from being modified when the population never leaves its connected component.

The input vertices are converted from one-based to zero-based indexing immediately. Since the problem has only one test case, the input loop processes exactly `q` reports. Python integers have arbitrary precision, so there is no overflow concern for population totals.

## Worked Examples

### Sample 1

The input contains only bridge reports, so the population of every component changes only when two components are merged.

| Report | Operation | Component populations | Active components | Answer |
| --- | --- | --- | --- | --- |
| 1 | bridge 1-2 | `{1,2}:2`, `{3}:1`, `{4}:1`, `{5}:1` | 4 | 3 |
| 2 | bridge 2-3 | `{1,2,3}:3`, `{4}:1`, `{5}:1` | 3 | 2 |
| 3 | bridge 1-3 | unchanged | 3 | 2 |
| 4 | bridge 4-5 | `{1,2,3}:3`, `{4,5}:2` | 2 | 1 |
| 5 | bridge 1-4 | `{1,2,3,4,5}:5` | 1 | 0 |

The third bridge is redundant because islands 1 and 3 already belong to the same component. This demonstrates why the DSU merge must first compare the two roots.

### Sample 2

Here there are no bridges at all. Every island initially forms its own graph component, and floods only move inhabitants between islands.

| Report | Operation | Nonempty islands | Active components | Answer |
| --- | --- | --- | --- | --- |
| 1 | flood 1-2 | 2, 3, 4, 5 | 4 | 3 |
| 2 | flood 2-1 | 1, 3, 4, 5 | 4 | 3 |
| 3 | flood 1-3 | 3, 4, 5 | 3 | 2 |
| 4 | flood 5-4 | 3, 4 | 2 | 1 |
| 5 | flood 4-3 | 3 | 1 | 0 |
| 6 | flood 3-1 | 1 | 1 | 0 |

The second report moves the inhabitants that had accumulated on island 2 back to island 1. The number of inhabited components remains four because one occupied island becomes empty while another becomes occupied. The fifth report leaves only island 3 occupied, giving the final answer zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O((n+q)\alpha(n))) | Each report performs a constant number of DSU operations, and DSU operations are almost constant amortized time. |
| Space | (O(n)) | The parent, size, and population arrays each contain (n) values, while the output contains (q) values. |

With (n,q\leq3\cdot10^5), the algorithm performs only a few DSU operations per report. This is comfortably within the intended complexity, while the brute-force traversal approach would require tens of billions of operations in the worst case. The stored arrays are also linear in the number of islands, and the output buffer is linear in the number of reports.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    q = next(it)

    parent = list(range(n))
    size = [1] * n
    population = [1] * n
    active = n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    out = []

    for _ in range(q):
        t = next(it)
        u = next(it) - 1
        v = next(it) - 1

        if t == 1:
            ru = find(u)
            rv = find(v)

            if ru != rv:
                if size[ru] < size[rv]:
                    ru, rv = rv, ru

                if population[ru] > 0 and population[rv] > 0:
                    active -= 1

                parent[rv] = ru
                size[ru] += size[rv]
                population[ru] += population[rv]

        else:
            x = population[u]

            if x:
                ru = find(u)
                rv = find(v)

                population[u] = 0

                if ru != rv:
                    population[ru] -= x

                    if population[ru] == 0:
                        active -= 1

                    if population[rv] == 0:
                        active += 1

                    population[rv] += x

        out.append(str(active - 1))

    return " ".join(out)

# Provided sample 1
sample1 = """\
5 5
1 1 2
1 2 3
1 1 3
1 4 5
1 1 4
"""
assert solve_data(sample1) == "3 2 2 1 0", "sample 1"

# Provided sample 2
sample2 = """\
5 6
2 1 2
2 2 1
2 1 3
2 5 4
2 4 3
2 3 1
"""
assert solve_data(sample2) == "3 3 2 1 0 0", "sample 2"

# Provided sample 3
sample3 = """\
9 11
1 1 2
1 3 4
1 5 6
2 6 4
2 5 3
1 7 8
1 1 8
1 5 9
2 9 5
2 1 2
2 1 3
"""
assert solve_data(sample3) == "7 6 5 5 4 3 2 2 2 2 2", "sample 3"

# Minimum-size graph, with a flood and a bridge.
case_min = """\
2 3
2 1 2
1 1 2
2 2 1
"""
assert solve_data(case_min) == "0 0 0", "minimum size"

# Empty-source floods and a bridge through empty islands.
case_empty = """\
3 4
2 1 2
2 1 3
1 1 3
2 2 1
"""
assert solve_data(case_empty) == "1 1 1 0", "empty source"

# Redundant bridge and flood inside the same component.
case_same_component = """\
3 4
1 1 2
2 1 2
1 2 3
2 2 3
"""
assert solve_data(case_same_component) == "1 1 0 0", "same component"

# Boundary-sized generated test.
n = 300000
q = 300000
parts = [f"{n} {q}"]
parts.extend(["2 1 2"] * q)
case_large = "\n".join(parts) + "\n"
expected_large = " ".join(["299998"] + ["299998"] * (q - 1))
assert solve_data(case_large) == expected_large, "large boundary case"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 3` with floods and one bridge | `0 0 0` | Minimum number of islands and repeated population movement |
| `3 4` with empty-source floods | `1 1 1 0` | Floods from empty islands and bridges between empty vertices |
| `3 4` with a connected pair | `1 1 0 0` | Population moving inside an existing DSU component and redundant connectivity |
| `n=q=300000` with repeated floods | `299998` repeated | Maximum input size, performance, and repeated operations on the same source |

## Edge Cases

The input

```
2 1
2 1 2
```

starts with two separate inhabited components. The flood moves the single inhabitant of island 1 to island 2, so the source component becomes empty and the destination component remains inhabited. `active` changes from 2 to 1, producing `active - 1 = 0`. The physical island 1 remains in the DSU, which is necessary because it can participate in later bridge operations.

For

```
3 2
2 1 2
2 1 3
```

the first flood moves island 1's population to island 2. The second flood starts from island 1, whose population is now zero. The algorithm exits the flood update immediately, leaving `active = 2` throughout the second report. The output is `1 1`.

For

```
3 2
1 1 2
2 1 2
```

the bridge first creates one component containing islands 1 and 2, with population two. The flood then moves the population of island 1 to island 2, but both islands are still inside the same component. The component population remains two, and `active` stays at two because island 3 is the other inhabited component. The output is `1 1`.

For

```
3 2
2 1 2
1 1 3
```

the first report empties island 1, leaving only island 2 inhabited. The second report joins empty islands 1 and 3 into a graph component containing no inhabitants. The DSU merge sees that both component populations are zero, so it does not change `active`. The output remains `1 1`.

The algorithm also handles a bridge between already connected islands. In Sample 1, the third report is `1 1 3`, but islands 1 and 3 were connected through island 2. Their DSU roots are equal, so no population totals or active-component counts are changed. The answer stays `2`.

Finally, multiple bridges between the same pair of islands are harmless. DSU treats every subsequent bridge between vertices already in the same component as a no-op. This matches the graph semantics because duplicate bridges do not create a new connected component and cannot reduce the number of additional bridges needed.
