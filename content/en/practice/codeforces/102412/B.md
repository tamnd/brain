---
title: "CF 102412B - Alexey the Sage of The Six Paths"
description: "Think of every party member as a vertex. There are (n) vertices on the left, numbered (1) through (n), and (n) vertices on the right, numbered (n+1) through (2n). Every problem creates one edge between one left vertex and one right vertex."
date: "2026-08-10T13:43:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102412
codeforces_index: "B"
codeforces_contest_name: "MEX Foundation Contest (supported by AIM Tech)"
rating: 0
weight: 102412
solve_time_s: 352
verified: true
draft: false
---

[CF 102412B - Alexey the Sage of The Six Paths](https://codeforces.com/problemset/problem/102412/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

Think of every party member as a vertex. There are (n) vertices on the left, numbered (1) through (n), and (n) vertices on the right, numbered (n+1) through (2n). Every problem creates one edge between one left vertex and one right vertex. Several problems may connect the same pair of members, so parallel edges are allowed.

After all assignments are made, each member chooses one of their assigned problems. A problem is solved exactly when its two endpoints both choose that problem. Since every member chooses at most one problem, the maximum possible number of solved problems is precisely the maximum matching size of this bipartite multigraph. The task is to choose exactly (m) edges so that the maximum matching has size between (l) and (r), while minimizing the sum of the salaries determined by every vertex's degree.

If vertex (i) receives degree (d_i), its contribution is (p_{i,d_i}). Thus the actual graph structure matters only through two things: the degree of every vertex determines the cost, while the way those degrees are connected determines the maximum matching.

The bounds (n,m\le30) are the main clue. An algorithm exponential in (m) or (n) is already too large, because (30) is large enough that even (2^{30}) is around one billion. On the other hand, a polynomial algorithm with a few dimensions bounded by (30) is realistic. The intended solution uses several counters ranging from (0) to (n) or (m), giving an (O(n^3m^3)) dynamic program. Accepted C++ implementations use exactly this asymptotic approach.

There is one slightly surprising input boundary. The examples contain (m=0), even though some copies of the statement describe (m) together with the positive lower bound. The implementation should naturally support (m=0). For example,

```
2 0 2 2
8
9
3
4
```

has no edges at all, so its maximum matching is (0), not (2). The correct output is

```
DEFEAT
```

A careless solution that assumes at least one problem and blindly tries to construct a matching can fail here.

Another edge case is (l=0). If the required interval contains zero, an edgeless graph is allowed whenever (m=0). For example,

```
1 0 0 0
7
9
```

has answer (16), because both members receive degree zero and the maximum matching is zero. A solution that always tries to create a positive-size matching would incorrectly report defeat.

The upper bound on the matching also matters. For example,

```
2 1 2 2
0 0
0 0
0 0
0 0
```

contains only one problem, hence only one edge, so a matching of size (2) is impossible. The correct output is `DEFEAT`. A naive check based only on the number of available members might incorrectly think that two members on each side are enough.

Finally, parallel edges must not be treated as separate matching opportunities. With

```
2 2 2 2
0 0 0
0 0 0
0 0 0
0 0 0
```

both problems could connect the same pair of members, but those two problems still produce only one solved problem, because the same two members cannot each choose two different problems. The graph has two parallel edges, but its maximum matching is (1). Any implementation that treats the (m) problems as independently matchable pairs would get this wrong.

## Approaches

The most direct approach is to decide the two endpoints of every problem. There are (n^2) possible pairs for one problem, so enumerating all assignments considers

[
(n^2)^m=n^{2m}
]

graphs. For the maximum values (n=m=30), this is (900^{30}), roughly (10^{88}) possibilities, before even computing the maximum matching of each graph. The approach is correct because every possible assignment is eventually considered, but it becomes useless almost immediately.

The useful observation is that the salary depends only on vertex degrees. We should avoid deciding the exact endpoints until the very end. Instead, we can describe a graph by a carefully chosen matching and vertex cover, because bipartite graphs have the property that the size of a maximum matching equals the size of a minimum vertex cover. This is Kőnig's theorem.

Suppose we want the final maximum matching to be exactly (k). We can explicitly choose (k) matching edges and a vertex cover containing exactly (k) vertices. Every matching edge must contain exactly one cover vertex. Every other edge must contain at least one cover vertex. Then the chosen cover has size (k), so no matching can have more than (k) edges, while the explicitly constructed matching has (k) edges. The maximum matching is consequently exactly (k).

This is the key reduction. Instead of reasoning about arbitrary graph connectivity, we only need to decide, for every member, its degree, whether it is an endpoint of one of the (k) matching edges, and whether it belongs to the cover.

For the left side, define (x_1) as the number of matching endpoints, (x_2) as the number of those matching endpoints that belong to the cover, (x_3) as the number of nonmatching edges incident to the left side, and (x_4) as the number of those nonmatching incidences whose left endpoint is in the cover. Define (y_1,y_2,y_3,y_4) analogously on the right.

At the end we need

[
x_1=y_1=k,
]

because the matching has (k) edges and every matching edge has one endpoint on each side. We also need

[
x_2+y_2=k,
]

because every matching edge must have exactly one endpoint in the cover. There are (m-k) nonmatching edges, so

[
x_3=y_3=m-k.
]

Finally, every nonmatching edge must touch the cover. The quantities (x_4) and (y_4) count cover incidences on those edges. An edge whose two endpoints are both in the cover contributes twice, so the necessary and sufficient condition is

[
x_4+y_4\ge m-k.
]

The DP independently finds the cheapest left-side and right-side assignments satisfying these counters. We then combine compatible states.

The original editorial describes the same four counters and the (O(n^3m^3)) DP, followed by a constructive procedure that realizes the selected degree information as actual edges.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^{2m}\cdot n^3)) | (O(n^2+m)) | Too slow |
| Optimal DP | (O(n^3m^3)) | (O(n^3m^2)) for the sparse Python representation | Accepted |

## Algorithm Walkthrough

1. Interpret the problems as edges of a bipartite multigraph. A member's degree is exactly the number of problems assigned to that member, so choosing degrees determines the salary contribution.
2. Fix a desired maximum matching size (k) with (l\le k\le r). We will explicitly build a matching of (k) edges and a vertex cover of (k) vertices. By Kőnig's theorem, making both structures have size (k) is enough to force the maximum matching to be exactly (k).
3. For each side, process its (n) vertices one by one with a dynamic program. The state is ((x_1,x_2,x_3,x_4)). Here (x_1) counts chosen matching endpoints, (x_2) counts matching endpoints that are cover vertices, (x_3) counts nonmatching edge incidences, and (x_4) counts those incidences whose endpoint is in the cover.
4. When processing a vertex, let (c) be the number of its nonmatching incident edges. There are three possible roles. The vertex can be outside the matching and outside the cover, giving degree (c). It can be a matching endpoint but not a cover vertex, giving degree (c+1). Or it can be both a matching endpoint and a cover vertex, again giving degree (c+1), while its (c) nonmatching edges also contribute to (x_4).
5. Add the corresponding salary (p_{i,d}) to the DP cost. Since the salary depends only on the resulting degree (d), the exact destinations of the edges do not matter during the DP.
6. After all vertices on one side are processed, combine the two sides. For a fixed (k), require both sides to have (k) matching endpoints and exactly (m-k) nonmatching incidences. Pair states whose cover counts on matching endpoints sum to (k), and whose cover incidences on nonmatching edges sum to at least (m-k).
7. Keep the minimum total salary among all compatible states. If no compatible pair exists for any (k\in[l,r]), print `DEFEAT`.
8. Recover the selected degree and role of every vertex from the DP parent pointers. The recovered information tells us which vertices are matching endpoints, which of those are cover vertices, and the final degree of every vertex.
9. Construct the (k) matching edges first. A left matching vertex outside the cover is paired with a right matching vertex inside the cover. A left matching vertex inside the cover is paired with a right matching vertex outside the cover. The two groups have exactly the required equal sizes because (x_2+y_2=k).
10. Some nonmatching edges need both endpoints in the cover. The number of such edges is determined by the remaining degrees of cover vertices after the matching edges have been placed. Connect cover vertices on the two sides until this required number of double-covered edges has been created.
11. All remaining degrees can now be satisfied using edges between a cover vertex on one side and a non-cover matching vertex on the other side. Every remaining edge has exactly one cover endpoint, so every edge is covered.
12. Output the resulting (m) pairs. Parallel edges are allowed, so the construction does not need to avoid using the same pair more than once.

The invariant behind the DP is that every stored state describes a realizable partial assignment of the first processed vertices with exactly the recorded matching and cover incidences and with the minimum possible salary for those counters. When the two final states satisfy the four compatibility equations, the construction creates a matching of size (k) and a cover of size (k). The matching proves that the graph has matching number at least (k), while the cover proves that it has matching number at most (k). Hence its maximum matching is exactly (k), and because (k\in[l,r]), the graph is valid. Since the DP minimizes the salary for every state and the final enumeration considers every compatible pair of states, the selected graph has globally minimum cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**30

def dp_side(cost, n, m, r):
    """
    DP over one side.

    State:
        (x1, x2, x3, x4)

    x1 = number of matching endpoints
    x2 = number of matching endpoints in the cover
    x3 = number of nonmatching edge incidences
    x4 = number of those incidences whose endpoint is in the cover

    Returns:
        dp      : final-state -> minimum cost
        parents : parent information for reconstruction
    """

    dp = {(0, 0, 0, 0): 0}
    parents = [None] * (n + 1)
    parents[0] = {}

    for i in range(1, n + 1):
        ndp = {}
        par = {}

        for state, old_cost in dp.items():
            x1, x2, x3, x4 = state

            remaining = m - x1 - x3

            for c in range(remaining + 1):
                nx3 = x3 + c

                # Vertex is neither a matching endpoint nor a cover vertex.
                ns = (x1, x2, nx3, x4)
                value = old_cost + cost[i - 1][c]

                if value < ndp.get(ns, INF):
                    ndp[ns] = value
                    par[ns] = (state, 1, c)

                # The vertex is a matching endpoint, but not in the cover.
                if x1 < r and remaining - c > 0:
                    ns = (x1 + 1, x2, nx3, x4)
                    value = old_cost + cost[i - 1][c + 1]

                    if value < ndp.get(ns, INF):
                        ndp[ns] = value
                        par[ns] = (state, 2, c + 1)

                    # The vertex is both a matching endpoint and a cover vertex.
                    ns = (x1 + 1, x2 + 1, nx3, x4 + c)
                    value = old_cost + cost[i - 1][c + 1]

                    if value < ndp.get(ns, INF):
                        ndp[ns] = value
                        par[ns] = (state, 3, c + 1)

        dp = ndp
        parents[i] = par

    return dp, parents

def reconstruct(parents, final_state, n):
    degree = [0] * n
    matched = [False] * n
    cover = [False] * n

    state = final_state

    for i in range(n, 0, -1):
        prev, kind, d = parents[i][state]

        degree[i - 1] = d

        if kind == 2:
            matched[i - 1] = True
        elif kind == 3:
            matched[i - 1] = True
            cover[i - 1] = True

        state = prev

    return degree, matched, cover

def solve_case(n, m, l, r, costs):
    left = costs[:n]
    right = costs[n:]

    left_dp, left_parents = dp_side(left, n, m, r)
    right_dp, right_parents = dp_side(right, n, m, r)

    best = INF
    best_states = None

    max_k = min(r, n, m)

    for k in range(l, max_k + 1):
        nonmatching = m - k

        for x2 in range(k + 1):
            y2 = k - x2

            for x4 in range(nonmatching + 1):
                min_y4 = nonmatching - x4

                for y4 in range(min_y4, nonmatching + 1):
                    ls = (k, x2, nonmatching, x4)
                    rs = (k, y2, nonmatching, y4)

                    lc = left_dp.get(ls)
                    rc = right_dp.get(rs)

                    if lc is None or rc is None:
                        continue

                    value = lc + rc

                    if value < best:
                        best = value
                        best_states = (ls, rs)

    if best_states is None:
        return None

    left_state, right_state = best_states

    left_degree, left_matched, left_cover = reconstruct(
        left_parents, left_state, n
    )
    right_degree, right_matched, right_cover = reconstruct(
        right_parents, right_state, n
    )

    # Vectors are indexed by cover status and matching status.
    groups = [[[], []], [[], []]]

    for i in range(n):
        if left_matched[i]:
            groups[0][1 if left_cover[i] else 0].append(i)
        if right_matched[i]:
            groups[1][1 if right_cover[i] else 0].append(i)

    edges = []

    def add_edge(u, v):
        edges.append((u + 1, v + n + 1))
        left_degree[u] -= 1
        right_degree[v] -= 1

    # Construct the k matching edges.
    #
    # Left non-cover matching vertices pair with right cover
    # matching vertices, and vice versa.
    if len(groups[0][0]) != len(groups[1][1]):
        raise AssertionError("invalid matching partition")
    if len(groups[0][1]) != len(groups[1][0]):
        raise AssertionError("invalid matching partition")

    for u, v in zip(groups[0][0], groups[1][1]):
        add_edge(u, v)

    for u, v in zip(groups[0][1], groups[1][0]):
        add_edge(u, v)

    # Rebuild groups using remaining degrees.
    rem_groups = [[[], []], [[], []]]

    for side in range(2):
        for i in range(n):
            if side == 0:
                d = left_degree[i]
                is_cover = left_cover[i]
            else:
                d = right_degree[i]
                is_cover = right_cover[i]

            if d > 0:
                rem_groups[side][1 if is_cover else 0].append(i)

    # First create edges covered at both endpoints.
    #
    # The amount is exactly the excess cover incidence after all
    # edges with one cover endpoint are accounted for.
    left_cover_degree = sum(
        left_degree[i] for i in range(n) if left_cover[i]
    )
    right_noncover_degree = sum(
        right_degree[i] for i in range(n) if not right_cover[i]
    )

    double_edges = left_cover_degree - right_noncover_degree

    p = rem_groups[0][1]
    q = rem_groups[1][1]

    while double_edges > 0:
        if not p or not q:
            raise AssertionError("failed to construct double-covered edges")

        u = p[-1]
        v = q[-1]
        add_edge(u, v)
        double_edges -= 1

        if left_degree[u] == 0:
            p.pop()
        if right_degree[v] == 0:
            q.pop()

    # Finish all remaining edges. Every such edge has exactly one
    # cover endpoint.
    for side in range(2):
        p = rem_groups[side][0]
        q = rem_groups[1 - side][1]

        while p:
            if not q:
                raise AssertionError("failed to construct remaining edges")

            if side == 0:
                u = p[-1]
                v = q[-1]
                add_edge(u, v)
            else:
                u = q[-1]
                v = p[-1]
                add_edge(u, v)

            if left_degree[u] == 0:
                p.pop()
            if right_degree[v] == 0:
                q.pop()

    if len(edges) != m:
        raise AssertionError("wrong number of edges")

    if any(left_degree) or any(right_degree):
        raise AssertionError("degrees were not fully constructed")

    return best, edges

def solve():
    n, m, l, r = map(int, input().split())

    costs = []
    for _ in range(2 * n):
        costs.append(list(map(int, input().split())))

    result = solve_case(n, m, l, r, costs)

    if result is None:
        print("DEFEAT")
        return

    answer, edges = result

    out = [str(answer)]
    out.extend(f"{u} {v}" for u, v in edges)
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first part of the implementation, `dp_side`, handles one group independently. The four counters are stored as a tuple, and a dictionary keeps only states that are actually reachable. This is especially useful in Python because a full six-dimensional array would require a large amount of object overhead.

For a vertex with (c) nonmatching edges, the first transition assigns it degree (c). The other two transitions assign degree (c+1), because the vertex additionally receives one matching edge. The third transition also increases the cover-incidence counter by (c), since all of those nonmatching edges have a cover endpoint at this vertex.

The condition `remaining - c > 0` before the matching transitions prevents the DP from creating a matching edge after all (m) edge slots have already been consumed. This is the boundary condition that is easiest to get wrong. A matching endpoint always needs one additional edge beyond its (c) nonmatching edges.

The reconstruction walks backward through the stored parent dictionaries. For each processed member it recovers its degree, whether it is a matching endpoint, and whether it is a cover vertex.

The final state enumeration uses

[
(k,x_2,m-k,x_4)
]

on the left and

[
(k,k-x_2,m-k,y_4)
]

on the right. The lower bound

[
y_4\ge m-k-x_4
]

is exactly the requirement that the (m-k) nonmatching edges have at least one cover endpoint each.

The construction deliberately creates the matching first. After those (k) edges are removed from the remaining degree requirements, the residual degree sums on both sides are equal. Some residual edges must be covered twice, and these are placed between cover vertices. Once those are removed, every remaining edge can be placed between a cover vertex and a non-cover vertex. Parallel edges are perfectly legal, so no additional restriction is needed.

Python integers have arbitrary precision, so the salary values as large as (10^9), and their sums over at most (2n) members, do not require any special overflow handling.

## Worked Examples

### Sample 1

The first sample is

```
2 0 2 2
8
9
3
4
```

There are no problems, so every vertex has degree zero. The only possible graph has maximum matching (0).

The relevant final DP state is the zero state on both sides.

| Quantity | Left | Right |
| --- | --- | --- |
| Matching endpoints | 0 | 0 |
| Cover matching endpoints | 0 | 0 |
| Nonmatching incidences | 0 | 0 |
| Cover nonmatching incidences | 0 | 0 |
| Cost | 17 | 7 |

The desired matching size must be between (2) and (2), but the only possible value is (0). No compatible final state exists, so the algorithm prints `DEFEAT`.

This example confirms that the DP does not invent edges when (m=0), and that the requested lower bound is checked against the actual matching size.

### Sample 2

The second sample has (n=2), (m=8), and (l=r=2). One optimal degree pattern is

[
d_L=(4,4),\qquad d_R=(5,3),
]

whose cost is

[
p_{1,4}+p_{2,4}+p_{3,5}+p_{4,3}
=-10+0-9-2=-21.
]

The corresponding final state can be described as follows.

| Quantity | Left | Right |
| --- | --- | --- |
| (k) | 2 | 2 |
| Matching endpoints (x_1,y_1) | 2 | 2 |
| Matching endpoints in cover (x_2,y_2) | 2 | 0 |
| Nonmatching incidences (x_3,y_3) | 6 | 6 |
| Covered nonmatching incidences (x_4,y_4) | 6 | 0 |
| Cost | -10 | -11 |

The matching size is (k=2). Both left matching vertices are in the cover, so every nonmatching edge can also be covered from the left. Since there are (m-k=6) nonmatching edges and the left side supplies six cover incidences, all six are covered.

The sample output uses four copies of the edge ((1,3)), three edges involving vertex (2) and vertex (4), and one edge ((2,3)). Its degree sequence is exactly the one above, and the two left vertices are the only nonzero left vertices, so the maximum matching is exactly (2). The official sample gives total cost (-21).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^3m^3)) | There are (O(n^2m^2)) DP states across the four counters and up to (O(m)) degree choices per transition, for each of (n) vertices and two sides |
| Space | (O(n^3m^2)) | The Python implementation stores reachable states and reconstruction information for all (n) layers |

The intended bounds are only (n,m\le30), which makes the six-counter formulation practical in a low-level implementation. The official time limit is 2 seconds and the memory limit is 1024 MiB.

The original accepted implementations use the same (O(n^3m^3)) DP and store the full DP structure in arrays. The Python version uses sparse dictionaries to avoid allocating a huge multidimensional object array, trading some constant-factor speed for substantially simpler memory management.

## Test Cases

The test harness below assumes the submitted code is saved as `solution.py`. It checks the exact answer value, while allowing any valid construction because the problem explicitly permits arbitrary optimal solutions.

```python
# helper: run solution on input string, return output string
import subprocess
import sys

def run(inp: str) -> str:
    result = subprocess.run(
        [sys.executable, "solution.py"],
        input=inp.encode(),
        stdout=subprocess.PIPE,
        check=True,
    )
    return result.stdout.decode().strip()

sample1 = """\
2 0 2 2
8
9
3
4
"""

assert run(sample1) == "DEFEAT", "sample 1"

sample2 = """\
2 8 2 2
2 5 5 10 -10 -1 3 5 9
8 -10 9 9 0 1 -3 1 -1
0 5 -1 5 3 -9 1 10 6
5 -4 8 -2 2 -8 6 3 -3
"""

out = run(sample2).splitlines()
assert int(out[0]) == -21, "sample 2"

sample3 = """\
3 5 2 3
100 75 125 150 175 200
125 100 75 100 125 150
225 200 175 200 225 250
225 200 175 200 225 250
125 100 75 100 125 150
100 75 125 150 175 200
"""

out = run(sample3).splitlines()
assert int(out[0]) == 650, "sample 3"

# Minimum-size case: no problems, matching number must be zero.
case_min = """\
1 0 0 0
7
9
"""

assert run(case_min) == "16", "minimum-size case"

# Boundary case: one edge cannot create a matching of size two.
case_boundary = """\
2 1 2 2
0 0
0 0
0 0
0 0
"""

assert run(case_boundary) == "DEFEAT", "matching upper-bound case"

# All costs are equal, so every feasible construction has the same cost.
case_equal = """\
2 2 1 1
5 5 5
5 5 5
5 5 5
5 5 5
"""

out = run(case_equal).splitlines()
assert int(out[0]) == 20, "all-equal costs"

# Maximum-size instance. With 30 problems and a required matching
# of 30, every one of the 60 vertices must have degree exactly one.
rows = ["0 1" for _ in range(60)]
case_max = "30 30 30 30\n" + "\n".join(rows) + "\n"

out = run(case_max).splitlines()
assert int(out[0]) == 60, "maximum-size case"
assert len(out) == 31, "maximum-size edge count"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | `DEFEAT` | Zero problems and impossible lower matching bound |
| Sample 2 | `-21` | Optimal cost and nontrivial parallel-edge construction |
| Sample 3 | `650` | Second official feasible construction |
| (n=1,m=0,l=r=0) | `16` | Minimum-size and zero-matching case |
| (n=2,m=1,l=r=2) | `DEFEAT` | Matching upper bound and off-by-one handling |
| (n=2,m=2,l=r=1), all costs (5) | `20` | All-equal costs and deliberately non-perfect matching |
| (n=m=30,l=r=30) | `60` | Maximum-size boundary and perfect matching |

## Edge Cases

For the zero-problem case,

```
1 0 0 0
7
9
```

the DP starts and finishes at ((0,0,0,0)). There are no transition choices because there are no edges to distribute. The left cost is (7), the right cost is (9), and the matching size is (0), which belongs to the requested interval. The answer is (16).

For an impossible lower bound,

```
2 1 2 2
0 0
0 0
0 0
0 0
```

the DP cannot produce a final state with (k=2), because a matching endpoint consumes one complete edge and there is only one edge available. The final enumeration has no candidate state, so `DEFEAT` is produced.

For repeated edges, consider

```
2 2 1 1
5 5 5
5 5 5
5 5 5
5 5 5
```

Both problems can be assigned to the same pair. Both left and right degrees then contain one vertex of degree two and one vertex of degree zero. The graph has two parallel edges but only one possible matched pair, so its maximum matching is (1). The DP permits this because it records degrees rather than forbidding repeated pairs. The total cost is (20).

For the maximum matching boundary,

```
30 30 30 30
```

with every salary row equal to `0 1`, a matching of size (30) is required. Since there are only (30) problems, every problem must belong to the matching, so every one of the (60) vertices has degree exactly one. The total salary is consequently (60). The DP reaches (k=30) and (m-k=0), so the nonmatching counters are both zero. This exercises the exact boundary where no residual edge may be created.

For negative salaries, the DP must never assume that a larger degree is more expensive. In the second official sample, some entries are negative, and the optimum deliberately assigns degree four to the first two left vertices and degree five to one right vertex. A greedy strategy based on choosing the cheapest degree independently for each member would fail because the degrees must sum to (m) on each side and must simultaneously support the required matching and cover structure. The DP considers all compatible degree choices and minimizes their total cost. The official answer for this sample is (-21).

The main conceptual edge case is a graph whose maximum matching is smaller than the number of nonzero-degree vertices on either side. Merely counting active vertices is not enough to determine the matching number. The cover part of the DP handles exactly this situation: several active vertices can be forced into a structure covered by only (k) vertices, which limits the maximum matching to (k). This is why tracking only degrees or only the number of nonzero vertices would lose essential information.

The final construction also handles edges covered at both endpoints. Such an edge contributes two cover incidences, so (x_4+y_4) may be strictly larger than (m-k). The construction first creates exactly the required number of these double-covered edges, then distributes all remaining degree using edges with one cover endpoint. This is what makes the final degree sequence simultaneously satisfy the salary DP and the vertex-cover condition.

The core idea to carry to similar problems is to stop thinking about the exact graph first. The salaries care about degrees, while the matching constraint can be certified by pairing a matching with a vertex cover. Once those two structures are encoded by small counters, the graph itself can be reconstructed afterward.
