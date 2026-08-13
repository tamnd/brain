---
title: "CF 102341I - Infernape"
description: "For every query, we have several Infernape placed on vertices of one fixed tree. An Infernape at vertex (vi) with power (ri) heats exactly the vertices whose tree distance from (vi) is at most (ri). A vertex is considered good if at least (k-1) of the (k) Infernape heat it."
date: "2026-08-14T01:53:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102341
codeforces_index: "I"
codeforces_contest_name: "Radewoosh+mnbvmar Contest (supported by AIM Tech)"
rating: 0
weight: 102341
solve_time_s: 953
verified: true
draft: false
---

[CF 102341I - Infernape](https://codeforces.com/problemset/problem/102341/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 15m 53s  
**Verified:** yes  

## Solution
## Problem Understanding

For every query, we have several Infernape placed on vertices of one fixed tree. An Infernape at vertex (v_i) with power (r_i) heats exactly the vertices whose tree distance from (v_i) is at most (r_i).

A vertex is considered good if at least (k-1) of the (k) Infernape heat it. Equivalently, among the (k) balls defined by the Infernape, the vertex may lie outside at most one ball. The task is to count all good vertices independently for every query.

The tree itself has up to (10^5) vertices, while the total number of Infernape over all queries is at most (3\cdot10^5). The time limit is 7 seconds, so an algorithm that scans the whole tree for every Infernape is far too expensive. A bound such as (10^5\cdot3\cdot10^5=3\cdot10^{10}) operations rules out any (O(nk)) approach. We need roughly (O((n+\sum k)\log n)), or something close to it.

There are several boundary cases that a solution has to handle exactly. First, the desired set is not the intersection of all balls. For example, on the tree (1-2), take two Infernape at (1) and (2), both with power (0). The correct answer is (2), because each vertex is heated by one Infernape and (k-1=1). The intersection of the two balls is empty, so an implementation that only computes the common intersection would incorrectly return (0).

Second, the distance bound is inclusive. On the path (1-2-3), put one Infernape at (1) with power (1) and another at (3) with power (1). Every vertex is heated by at least one Infernape, so the answer is (3). Treating distance (r_i) as excluded would incorrectly leave only vertex (2).

Third, the intersection of several balls may have a center in the middle of an edge rather than at an original vertex. On the tree (1-2), put Infernape at both endpoints with power (1). Their common heated region contains both vertices and is naturally centered at the midpoint of the edge. Restricting every intermediate ball center to an original vertex makes the intersection operation awkward and can introduce off-by-one errors.

Finally, an intersection can become empty after adding another ball. Such an intersection must simply contribute zero. The algorithm represents this state explicitly instead of trying to assign it an artificial center.

## Approaches

The direct approach is to inspect every tree vertex for every Infernape in a query. We can compute its distance from the Infernape, count how many balls contain it, and increment the answer when that count reaches (k-1). This is correct because it follows the definition literally. Its cost is (O(nk)) for one query and (O(n\sum k)) for the whole input. At the maximum total (k), this is about (3\cdot10^{10}) vertex checks, which is nowhere near feasible.

The first useful observation is that the answer can be expressed using intersections instead of counting coverage directly. Let (S_i) be the set of vertices heated by every Infernape except number (i), and let (S) be the set heated by all (k) Infernape. A vertex heated by exactly (k-1) Infernape belongs to exactly one (S_i). A vertex heated by all (k) belongs to every (S_i), so it is counted (k) times in their sum. Subtracting (k-1) copies of (S) fixes exactly that overcount:

[
\text{answer}=\sum_{i=1}^{k}|S_i|-(k-1)|S|.
]

This reduces the problem to computing the size of (k+1) intersections of tree balls.

The second observation is the structure of ball intersections on a tree. The intersection of two connected balls in a tree is again either empty or a ball whose center lies on the path between the two original centers. Repeating the operation means that the intersection of any number of balls can still be represented by one pair

[
(c,R),
]

meaning all points at distance at most (R) from center (c).

The center can lie halfway along an edge, which is why the tree is subdivided. Every original edge (u-v) is replaced by (u-x-v), where (x) is a new auxiliary vertex. Every original tree distance is then doubled. We also double every Infernape radius. This makes the midpoint of an original edge an actual vertex, so every intersection can be represented by an integer center and an integer radius. Only original vertices are counted in the final answer.

For two balls (U(a,A)) and (U(b,B)), let (D=\operatorname{dist}(a,b)). If (A+B<D), their intersection is empty. If one radius reaches far enough to contain the other ball, we return the smaller ball unchanged. Otherwise the new radius is

[
R=\min(A,B)-\left\lfloor\frac{D-|A-B|}{2}\right\rfloor,
]

and the new center is the corresponding point on the path from (a) to (b). Binary lifting supplies both the distance and the point at a specified distance along the path. This is the geometric core of the solution. The same representation and intersection operation are used in the known solution for this problem.

We can construct all intersections in linear many intersection operations using prefix and suffix intersections. Let `pre[i]` be the intersection of the first (i) balls and `suf[i]` the intersection of the balls from (i) onward. Then the intersection excluding ball (i) is simply

[
\text{pre}[i-1]\cap\text{suf}[i+1].
]

Thus every query creates only (k+1) ball-counting requests.

The remaining problem is to count how many original tree vertices lie inside many arbitrary balls efficiently. Centroid decomposition solves this offline. For each centroid, we know the distance from every vertex in its current component to that centroid. A query centered at (u) with radius (R) can be tested through the centroid using

[
\operatorname{dist}(u,c)+\operatorname{dist}(c,x)\le R.
]

All vertices in the component satisfy the second part through their distance from the centroid. A prefix count by distance gives the number of possible (x). If (u) lies in one child component of the centroid, vertices from that same child may have a shorter path that does not pass through the centroid. We first count the entire component through the centroid, then subtract exactly the same-child vertices. Every vertex-query pair is assigned to the highest centroid where their path passes through that centroid, so it is counted exactly once.

The centroid decomposition is processed offline because all ball-counting requests are known before the decomposition starts. The resulting approach has (O((n+K)\log n)) time, where (K) is the total number of Infernape, and (O(n\log n+K)) memory.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nK)) | (O(n)) | Too slow |
| Optimal | (O((n+K)\log n)) | (O(n\log n+K)) | Accepted |

## Algorithm Walkthrough

1. Subdivide every original edge by inserting one auxiliary vertex. The resulting tree has (2n-1) vertices, and every original distance is exactly doubled. Store original vertices as the first (n) vertices, so the centroid counting phase can ignore auxiliary vertices.
2. Root the subdivided tree and build binary lifting tables. The tables support `lca(u,v)` and `jump(u,d)`, where `jump` moves (d) edges upward from (u). These operations are enough to find the distance between two centers and to locate a new center on their connecting path.
3. Represent a nonempty intersection by `(center, radius)` in the subdivided tree. An empty intersection is represented by an invalid center. Use a very large radius as the identity element, because intersecting an infinite ball with an ordinary ball should return the ordinary ball.
4. Implement the intersection of two represented balls. Let their centers be (a,b), radii (A,B), and let (D) be their distance. If (A+B<D), return empty. If (A\ge D+B), the second ball is contained in the first, so return the second. The symmetric case returns the first. Otherwise compute the new radius with
[
R=\min(A,B)-\left\lfloor\frac{D-|A-B|}{2}\right\rfloor.
]
The new center is the point on the path from (a) to (b) at distance (A-R) from (a), or equivalently (B-R) from (b). Binary lifting locates that point.
5. For every query, build prefix intersections `pre` and suffix intersections `suf`. The full intersection is `suf[0]`. For every possible omitted Infernape (i), the intersection of all other balls is `pre[i] ∩ suf[i+1]`. If this intersection is nonempty, create a ball-counting request with coefficient (+1). Create one additional request for the full intersection with coefficient (1-k).
6. Decompose the subdivided tree by centroids. Removing a centroid splits the current component into smaller components, each containing at most half as many vertices. The decomposition consequently has (O(\log n)) levels.
7. At one centroid (c), traverse the whole current component and build `cnt[d]`, the number of original vertices at distance exactly (d) from (c). Convert it into a prefix array, so `cnt[d]` becomes the number of original vertices at distance at most (d).
8. Traverse the component again and process every ball-counting request whose center is a vertex of this component. If its center (u) is at distance (du) from (c), a radius (R) can reach through (c) to every vertex (x) with
[
du+\operatorname{dist}(c,x)\le R.
]
The contribution is consequently `cnt[min(max_distance, R-du)]`.
9. For every child component of (c), repeat the counting traversal with only vertices from that child, but give their counts coefficient (-1). This removes same-child vertices from the contribution computed through (c). After that, recurse into the child component. The subtraction is necessary because the path through (c) is not the actual path for two vertices inside the same child.
10. After all centroid decomposition levels are processed, each ball request contains the size of its represented ball among original vertices. For query (q), its stored coefficients already compute
[
\sum_i |S_i|-(k-1)|S|,
]
which is exactly the required answer.

### Why it works

The correctness has two independent parts. First, the inclusion formula is exact because a vertex covered by exactly (k-1) balls belongs to one omitted-ball intersection, while a vertex covered by all (k) balls belongs to all (k) omitted-ball intersections and is subsequently subtracted (k-1) times.

Second, every intersection is represented exactly by one tree ball or by the empty state. On a tree, the boundary constraints of two intersecting balls meet along the unique path between their centers, so the intersection is centered on that path and has the radius given above. Subdivision makes every possible midpoint an actual vertex, while doubling distances preserves all statements about original vertices.

For a fixed centroid, the first traversal counts vertices according to their distance through the centroid. Such a path is correct for vertices outside the center's child component. For vertices in the same child, the through-centroid distance can be different from the real distance, so the second traversal subtracts precisely those same-child candidates. Thus this centroid level counts exactly the pairs whose path passes through the centroid. Every pair of vertices is separated by exactly one highest centroid in the decomposition, so no pair is missed or counted twice.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    N = 2 * n - 1

    g = [[] for _ in range(N)]

    for i in range(n - 1):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        x = n + i
        g[a].append(x)
        g[x].append(a)
        g[b].append(x)
        g[x].append(b)

    # Root the subdivided tree and build binary lifting.
    parent = [0] * N
    depth = [0] * N
    order = [0]

    for u in order:
        pu = parent[u]
        for v in g[u]:
            if v == pu:
                continue
            parent[v] = u
            depth[v] = depth[u] + 1
            order.append(v)

    LOG = N.bit_length()
    up = [parent]

    for _ in range(1, LOG):
        prev = up[-1]
        cur = [0] * N
        for i in range(N):
            cur[i] = prev[prev[i]]
        up.append(cur)

    def jump(u, d):
        bit = 0
        while d:
            if d & 1:
                u = up[bit][u]
            d >>= 1
            bit += 1
        return u

    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a

        diff = depth[a] - depth[b]
        bit = 0
        while diff:
            if diff & 1:
                a = up[bit][a]
            diff >>= 1
            bit += 1

        if a == b:
            return a

        for j in range(LOG - 1, -1, -1):
            if up[j][a] != up[j][b]:
                a = up[j][a]
                b = up[j][b]

        return up[0][a]

    def distance(a, b):
        p = lca(a, b)
        return depth[a] + depth[b] - 2 * depth[p]

    INF = 10**9

    # A ball is (center, radius). (-1, -1) is empty.
    def intersect(A, B):
        a, ra = A
        b, rb = B

        if a < 0 or b < 0:
            return (-1, -1)

        p = lca(a, b)
        D = depth[a] + depth[b] - 2 * depth[p]

        if ra + rb < D:
            return (-1, -1)

        if ra >= D + rb:
            return B

        if rb >= D + ra:
            return A

        R = min(ra, rb) - (D - abs(ra - rb)) // 2

        da = depth[a] - depth[p]
        move_a = ra - R

        if da >= move_a:
            c = jump(a, move_a)
        else:
            c = jump(b, rb - R)

        return (c, R)

    q = int(input())

    answers = [0] * q

    # Offline ball-counting requests.
    qhead = [-1] * N
    qradius = []
    qid = []
    qcoef = []
    qnext = []

    def add_request(center, radius, idx, coef):
        pos = len(qradius)
        qradius.append(radius)
        qid.append(idx)
        qcoef.append(coef)
        qnext.append(qhead[center])
        qhead[center] = pos

    for qi in range(q):
        k = int(input())

        balls = [None] * k
        for i in range(k):
            v, r = map(int, input().split())
            balls[i] = (v - 1, 2 * r)

        pre = [None] * (k + 1)
        pre[0] = (0, INF)

        for i in range(k):
            pre[i + 1] = intersect(pre[i], balls[i])

        suf = [None] * (k + 1)
        suf[k] = (0, INF)

        for i in range(k - 1, -1, -1):
            suf[i] = intersect(balls[i], suf[i + 1])

        # Full intersection has coefficient 1-k.
        all_ball = suf[0]
        if all_ball[0] >= 0:
            add_request(all_ball[0], all_ball[1], qi, 1 - k)

        # Intersection of every ball except i has coefficient +1.
        for i in range(k):
            cur = intersect(pre[i], suf[i + 1])
            if cur[0] >= 0:
                add_request(cur[0], cur[1], qi, 1)

    # Centroid decomposition.
    dead = bytearray(N)
    temp_parent = [-1] * N
    subsize = [0] * N

    def find_centroid(start):
        comp = [start]
        temp_parent[start] = -1

        for u in comp:
            pu = temp_parent[u]
            for v in g[u]:
                if dead[v] or v == pu:
                    continue
                temp_parent[v] = u
                comp.append(v)

        total = len(comp)

        for u in comp:
            subsize[u] = 1

        for u in reversed(comp):
            p = temp_parent[u]
            if p != -1:
                subsize[p] += subsize[u]

        centroid = start
        best = total + 1

        for u in comp:
            largest = total - subsize[u]

            for v in g[u]:
                if dead[v]:
                    continue
                if temp_parent[v] == u and subsize[v] > largest:
                    largest = subsize[v]

            if largest < best:
                best = largest
                centroid = u

        return centroid, total

    def collect(start, parent_node, start_dist, cnt, sign):
        stack = [(start, parent_node, start_dist)]
        max_dist = start_dist

        while stack:
            u, p, d = stack.pop()

            if u < n:
                cnt[d] += sign

            if d > max_dist:
                max_dist = d

            for v in g[u]:
                if dead[v] or v == p:
                    continue
                stack.append((v, u, d + 1))

        return max_dist

    def process_requests(start, parent_node, start_dist, cnt, deg):
        stack = [(start, parent_node, start_dist)]

        while stack:
            u, p, d = stack.pop()

            e = qhead[u]
            while e != -1:
                r = qradius[e]

                if r >= d:
                    limit = r - d
                    if limit > deg:
                        limit = deg
                    answers[qid[e]] += qcoef[e] * cnt[limit]

                e = qnext[e]

            for v in g[u]:
                if dead[v] or v == p:
                    continue
                stack.append((v, u, d + 1))

    tasks = [0]

    while tasks:
        start = tasks.pop()

        centroid, total = find_centroid(start)
        dead[centroid] = 1

        cnt = [0] * (total + 1)

        # First count all vertices through the centroid.
        deg = collect(centroid, -1, 0, cnt, 1)

        for d in range(1, deg + 1):
            cnt[d] += cnt[d - 1]

        process_requests(centroid, -1, 0, cnt, deg)

        # Then subtract vertices belonging to the same child component.
        for v in g[centroid]:
            if dead[v]:
                continue

            # Only the prefix that will be used by this child needs clearing.
            child_deg = 0
            stack = [(v, centroid, 1)]
            while stack:
                u, p, d = stack.pop()
                if d > child_deg:
                    child_deg = d
                for w in g[u]:
                    if dead[w] or w == p:
                        continue
                    stack.append((w, u, d + 1))

            for d in range(child_deg + 1):
                cnt[d] = 0

            child_deg = collect(v, centroid, 1, cnt, -1)

            for d in range(1, child_deg + 1):
                cnt[d] += cnt[d - 1]

            process_requests(v, centroid, 1, cnt, child_deg)

        # The remaining neighbors are roots of independent components.
        for v in g[centroid]:
            if not dead[v]:
                tasks.append(v)

    sys.stdout.write("\n".join(map(str, answers)))

if __name__ == "__main__":
    solve()
```

The first part constructs the subdivided tree and roots it once. The auxiliary vertices are deliberately placed after the original vertices, so the test `u < n` later identifies exactly the vertices that must be counted.

The binary lifting table is used twice. `lca` gives the distance between two ball centers, while `jump` locates the new center of an intersection. All radii are doubled when the query is read, matching the doubled edge lengths in the subdivided tree.

The prefix and suffix arrays are the reason each query needs only (O(k)) ball intersections. The identity ball `(0, INF)` allows the first prefix or suffix operation to be written exactly like every other intersection.

The request arrays form a linked list for every tree vertex. This avoids creating up to (2n-1) Python list objects containing request lists, and it also avoids storing a large number of four-element tuples. Each request stores its center, radius, original query index, coefficient, and the next request at the same center.

The centroid decomposition is written iteratively. A recursive DFS on a path with (10^5) vertices would exceed Python's recursion limit, while the centroid decomposition itself has logarithmic depth but its component traversals do not. The component finder explicitly constructs a traversal order and computes subtree sizes backwards.

The centroid counting phase first counts every original vertex through the centroid. For a request centered at distance (d) from the centroid, only a radius of `r - d` remains available for the second half of the path. The prefix array answers that count in (O(1)).

The second traversal for a child component has negative weights. It removes same-child vertices from the first count, leaving exactly the vertices whose path from the request center passes through the current centroid. After this centroid level is complete, the centroid is permanently removed and every remaining neighbor starts an independent subproblem.

All arithmetic is integer arithmetic. Python integers also remove any concern about the 64-bit overflow that would otherwise have to be considered for accumulated answers.

## Worked Examples

The official sample contains the following tree and two queries, with outputs (5) and (7).

### Sample 1

The first query has three Infernape:

```
(8, 1)
(3, 1)
(3, 2)
```

The relevant heated sets are

[
B_1={8,9,1,2,7},
]

[
B_2={3,1,4,10},
]

and

[
B_3={3,1,4,10,5,8}.
]

The intersection calculations can be summarized as follows.

| Operation | Resulting intersection | Size among original vertices | Coefficient |
| --- | --- | --- | --- |
| (B_2\cap B_3) | ({3,1,4,10}) | 4 | (+1) |
| (B_1\cap B_3) | ({1,8}) | 2 | (+1) |
| (B_1\cap B_2) | ({1}) | 1 | (+1) |
| (B_1\cap B_2\cap B_3) | ({1}) | 1 | (1-3=-2) |

The accumulated answer is

[
4+2+1-2\cdot1=5.
]

The vertex (1) is heated by all three Infernape, so it initially appears in all three omitted-ball intersections. The coefficient (-2) removes exactly two copies, leaving one occurrence as required.

### Sample 2

The second query has two Infernape:

```
(7, 3)
(6, 0)
```

The second ball contains only vertex (6). The first ball contains

[
{7,8,1,2,9,3}.
]

Since (k=2), a vertex needs to be heated by at least one Infernape, so the answer is simply the union of these two sets.

| Operation | Result | Size | Coefficient |
| --- | --- | --- | --- |
| First ball only | ({7,8,1,2,9,3}) | 6 | (+1) |
| Second ball only | ({6}) | 1 | (+1) |
| Both balls | empty | 0 | (-1) |

The result is

[
6+1-0=7.
]

This example also exercises the empty-intersection state. The algorithm does not create a centroid request for an empty intersection, so it contributes exactly zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O((n+K)\log n)) | Binary lifting handles each ball intersection in (O(\log n)), and centroid decomposition processes every tree vertex and every request at (O(\log n)) levels |
| Space | (O(n\log n+K)) | Binary lifting uses (O(n\log n)), while the offline requests and tree use (O(n+K)) |

Here (K) is the sum of all query sizes, with (K\le300000). The subdivided tree has fewer than (200000) vertices, so the logarithmic factors remain small. The offline centroid processing avoids the (O(nK)) bottleneck of the brute-force method and is designed around the given (10^5) and (3\cdot10^5) limits.

## Test Cases

The following harness assumes the submitted solution is saved as `solution.py`. The sample is the official sample, followed by four targeted cases. The last case constructs a path with the maximum allowed (n=100000).

```python
import sys
import io
import solution

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = solution.input

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solution.input = sys.stdin.readline

    try:
        solution.solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        solution.input = old_input

# Official sample
sample = """\
10
1 3
6 4
9 8
1 8
3 4
2 8
10 3
4 5
8 7
2
3
8 1
3 1
3 2
2
7 3
6 0
"""

assert run(sample) == "5\n7", "official sample"

# Minimum-size tree, zero-radius balls.
# Each vertex is heated by exactly one Infernape.
case_min = """\
2
1 2
1
2
1 0
2 0
"""

assert run(case_min) == "2", "minimum-size tree"

# Boundary distance is inclusive.
# On 1-2-3, each endpoint reaches vertex 2.
# The union contains all three vertices.
case_boundary = """\
3
1 2
2 3
1
2
1 1
3 1
"""

assert run(case_boundary) == "3", "inclusive radius boundary"

# Three identical zero-radius balls.
# Only vertex 2 is heated, and it is heated by all three.
case_equal = """\
3
1 2
2 3
1
3
2 0
2 0
2 0
"""

assert run(case_equal) == "1", "identical balls"

# Maximum-size path.
# Both radius-(n-1) balls cover the whole tree.
n = 100000
edges = "\n".join(f"{i} {i + 1}" for i in range(1, n))
case_max = (
    f"{n}\n"
    f"{edges}\n"
    "1\n"
    "2\n"
    f"1 {n - 1}\n"
    f"{n} {n - 1}\n"
)

assert run(case_max) == str(n), "maximum-size path"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Official 10-vertex sample | `5` and `7` | Full intersection formula and general centroid counting |
| Two vertices, both radius 0 | `2` | Minimum tree and the fact that (k-1=1) means union rather than intersection |
| Path (1-2-3), endpoint radius 1 | `3` | Inclusive distance boundary |
| Three identical radius-0 balls | `1` | Repeated centers, equal balls, and the coefficient (1-k) |
| Generated path with (100000) vertices | `100000` | Maximum (n), maximum radius, and large-tree decomposition |

## Edge Cases

For the minimum tree

```
2
1 2
1
2
1 0
2 0
```

the two balls are ({1}) and ({2}). Their full intersection is empty, while the two intersections obtained by omitting one ball have sizes (1) and (1). The formula gives (1+1-1\cdot0=2). The centroid phase never receives a request for the empty intersection, so it cannot accidentally count an invalid center.

For the inclusive-radius case

```
3
1 2
2 3
1
2
1 1
3 1
```

the doubled tree contains the path with edge lengths (1), and the two original balls have doubled radii (2). Their boundaries both reach vertex (2) exactly. The omitted-ball intersections are simply the two original balls, while their common intersection is vertex (2). The formula is (2+2-1=3), matching the union of the two balls.

For identical balls

```
3
1 2
2 3
1
3
2 0
2 0
2 0
```

every ball is the singleton ({2}). Each omitted-ball intersection has size (1), and the full intersection also has size (1). The accumulated value is

[
1+1+1-2\cdot1=1.
]

This demonstrates why simply summing the (k) omitted intersections is wrong when a vertex is covered by all (k) Infernape.

The midpoint case occurs on

```
2
1 2
1
2
1 1
2 1
```

After subdivision, the tree is (1-x-2), and both radii become (2). The intersection of the two balls has center (x), the inserted midpoint, and radius (1) in the subdivided metric. Both original vertices are at distance (1) from (x), so the counted size is (2). This is exactly why the edge subdivision is part of the representation rather than merely an implementation convenience.

Finally, the maximum-size path contains (100000) original vertices and (99999) edges. Two Infernape placed at the endpoints with radius (99999) each cover the entire path. The intersection is also the entire path, so the answer is (100000). The centroid decomposition repeatedly cuts the path roughly in half, keeping the number of levels logarithmic even though the original tree is highly unbalanced.
