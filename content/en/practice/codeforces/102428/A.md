---
title: "CF 102428A - Algorithm Teaching"
description: "Each teacher knows a small set of algorithms. A student trained by that teacher can learn any non-empty subset of those algorithms. Two students can coexist in the final team exactly when neither student's learned set contains the other's learned set."
date: "2026-08-14T15:30:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102428
codeforces_index: "A"
codeforces_contest_name: "2019-2020 ACM-ICPC Latin American Regional Programming Contest"
rating: 0
weight: 102428
solve_time_s: 156
verified: true
draft: false
---

[CF 102428A - Algorithm Teaching](https://codeforces.com/problemset/problem/102428/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

Each teacher knows a small set of algorithms. A student trained by that teacher can learn any non-empty subset of those algorithms. Two students can coexist in the final team exactly when neither student's learned set contains the other's learned set. In other words, the learned sets must form an antichain under set inclusion.

The same learned set may be available through several teachers, but that does not create several useful students. Two students with exactly the same learned set are comparable because the sets are equal, so they cannot both belong to the team. We only care about the distinct feasible subsets.

The crucial structural observation is that every feasible set brings all of its subsets with it. If a teacher knows `{A, B, C}`, then `{A}`, `{B}`, `{A,B}`, and every other subset is feasible. Thus the feasible sets form a downward-closed family inside the Boolean lattice of all subsets.

The constraints are small in the dimension that matters. There are at most 100 teachers, and each teacher knows at most 10 algorithms. A single teacher consequently contributes at most (2^{10}-1=1023) different non-empty training sets. Across all teachers there can be at most about 102,300 distinct feasible sets. This is far too many for exponential search over all algorithms globally, since the teachers may collectively mention up to 1000 different algorithm names. Enumerating every subset of those 1000 algorithms would already require (2^{1000}-1) candidates.

The maximum answer itself is also comfortably within ordinary integer ranges. At most about 102,300 distinct students can be represented by distinct training sets, so Python integers have no special arithmetic difficulty here.

Several edge cases matter because they expose common incorrect simplifications. With one teacher knowing one algorithm, the only feasible training set is that singleton, so the answer is 1.

```
1
1 HAVEFUN
```

The output is `1`. A solution that accidentally allows the empty subset would count an extra possibility.

A second edge case is two teachers with disjoint algorithms.

```
2
1 A
1 B
```

The answer is `2`, because `{A}` and `{B}` are incomparable. A solution that only considers students trained by the same teacher would incorrectly return 1.

Duplicate teacher knowledge must also be handled without multiplying identical training sets.

```
2
2 A B
2 A B
```

The answer is `2`, not `4`. The feasible sets are `{A}`, `{B}`, and `{A,B}`, and the largest antichain consists of `{A}` and `{B}`.

Finally, the best team does not necessarily consist of sets of the same size. Consider the second sample. The first teacher contributes six distinct pairs, while the second teacher contributes two singleton sets on completely different algorithms. Those six pairs together with the two singletons form an antichain of size 8. Looking only for the largest single level would find 7 and would be wrong.

## Approaches

The direct brute-force approach would construct every subset of every algorithm appearing anywhere in the input and then search for the largest collection of pairwise incomparable subsets. The search space is determined by the total number of distinct algorithm names, not by the number of algorithms known by one teacher. In the worst case there can be 1000 distinct names, so merely enumerating all possible non-empty subsets takes (2^{1000}-1) operations. Checking all combinations of those subsets would be even worse. The brute force is correct because it explicitly considers every possible student, but the global algorithm universe makes it unusable.

The useful observation is that we do not need the global Boolean lattice. A student can only be trained on a subset of one teacher's at most 10 algorithms. We can enumerate those local subsets directly. Their union gives the complete set of feasible students, with at most (100\cdot(2^{10}-1)) candidates before removing duplicates.

Now regard every feasible training set as a vertex of a directed acyclic graph. Put an order relation from set (X) to set (Y) whenever (X\subset Y). A chain in this graph is a collection of students whose training sets are mutually comparable, so an antichain is exactly a team satisfying the cooperation condition.

Dilworth's theorem gives the key reduction: in any finite partially ordered set, the size of a maximum antichain equals the minimum number of chains needed to cover all vertices. A minimum chain cover can be obtained from a maximum matching in a bipartite graph. We make two copies of every feasible set, put the left copy in the first side and the right copy in the second side, and connect left (X) to right (Y) whenever (X) is a proper subset of (Y). If the maximum matching has size (M) and there are (V) feasible sets, the minimum chain cover has (V-M) chains, which is the desired answer.

There is one implementation refinement specific to this problem. It is enough to use only inclusion edges that differ by exactly one algorithm. Suppose (X\subset Y) and both sets are feasible. Since the feasible family is downward closed, every set obtained while adding the elements of (Y\setminus X) one at a time is also feasible. The subset relation can thus be represented by paths through these one-element extensions. For this family, a minimum chain decomposition can be saturated in this way, so the matching graph only needs cover edges.

For a teacher with (k) algorithms, there are (2^k) subsets including the empty set. Every subset has at most (k) one-element extensions, so the number of generated directed edges is at most (k2^{k-1}). With (k\le10) and (N\le100), this is at most 512,000 generated edges before duplicate edges are removed.

The maximum matching is computed with Hopcroft-Karp. Its layered BFS phase finds the shortest augmenting paths, while DFS then augments along all possible paths in that layer graph. This is much more suitable than trying to compare every pair of feasible subsets.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^K)) just to enumerate candidates, (K\le1000) | (O(2^K)) | Too slow |
| Optimal | (O(NK2^K + E\sqrt V)), with (K\le10), (V\le N2^K), (E\le NK2^{K-1}) | (O(V+E)) | Accepted |

Here (K) in the complexity expression for the local enumeration means the maximum number of algorithms known by one teacher, so (K\le10), not the potentially 1000 globally distinct algorithm names.

## Algorithm Walkthrough

1. Assign every algorithm name a unique global bit position. A teacher's knowledge can then be represented by a bitmask. This gives every training set a compact, hashable representation even when different teachers share algorithm names.
2. For every teacher, enumerate all non-empty submasks of that teacher's mask. Insert each resulting global mask into a dictionary that maps the training set to a unique vertex ID. Duplicate subsets from different teachers receive the same ID because they represent the same possible student.
3. Create an adjacency list for the bipartite matching graph. For every teacher and every non-empty subset (S) of that teacher's algorithms, try adding each algorithm that is not already in (S). The resulting set (T) differs from (S) by exactly one algorithm, so add an edge from (S) to (T).
4. Remove duplicate neighbors from each adjacency list. The same inclusion edge can be generated by several teachers when they share the relevant algorithms, but it only represents one relation in the poset.
5. Run Hopcroft-Karp on the bipartite graph. The left and right sides both contain all feasible training sets. An edge means that one feasible set can immediately precede another in a saturated inclusion chain.
6. Let (V) be the number of distinct feasible sets and (M) the maximum matching size. By the chain-cover form of Dilworth's theorem, the minimum number of chains is (V-M). Since a team is precisely an antichain, print (V-M).

### Why it works

The vertex set is exactly the set of possible non-empty student training sets, so no valid student is omitted and no impossible student is introduced. Inclusion defines the required partial order because two students fail to cooperate exactly when their training sets are comparable.

Every inclusion relation can be expanded into one-element additions because the feasible family is downward closed. If (X\subset Y) is feasible, every intermediate subset between them is also contained in (Y), hence is feasible. Consequently the same chain order can be represented using only edges that add one algorithm at a time. A chain in the constructed graph is therefore exactly a valid comparable sequence of training sets.

Dilworth's theorem says that the largest possible antichain has the same size as the smallest chain cover. The standard bipartite reduction says that, for a poset represented by its inclusion relations, the minimum chain cover size is (V-M), where (M) is the maximum matching between the two copies of the poset. Hopcroft-Karp finds that maximum matching, so the value printed by the algorithm is exactly the largest possible team.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1_000_000)

def solve():
    n = int(input())

    name_id = {}
    teachers = []

    for _ in range(n):
        parts = input().split()
        k = int(parts[0])

        mask = 0
        for name in parts[1:]:
            if name not in name_id:
                name_id[name] = len(name_id)
            mask |= 1 << name_id[name]

        teachers.append(mask)

    # Assign one vertex id to every distinct non-empty feasible subset.
    vertex_id = {}
    masks_by_teacher = []

    for teacher_mask in teachers:
        bits = []
        x = teacher_mask
        while x:
            b = x & -x
            bits.append(b)
            x -= b

        k = len(bits)
        local_masks = [0] * (1 << k)

        for lm in range(1, 1 << k):
            lb = lm & -lm
            j = lb.bit_length() - 1
            local_masks[lm] = local_masks[lm ^ lb] | bits[j]

        masks_by_teacher.append((bits, local_masks))

        for lm in range(1, 1 << k):
            mask = local_masks[lm]
            if mask not in vertex_id:
                vertex_id[mask] = len(vertex_id)

    v = len(vertex_id)

    # Build cover edges: S -> S union {x}.
    adj = [[] for _ in range(v)]

    for bits, local_masks in masks_by_teacher:
        k = len(bits)

        for lm in range(1, 1 << k):
            u_mask = local_masks[lm]
            u = vertex_id[u_mask]

            missing = ((1 << k) - 1) ^ lm
            while missing:
                lb = missing & -missing
                missing -= lb

                j = lb.bit_length() - 1
                v_mask = u_mask | bits[j]
                w = vertex_id[v_mask]
                adj[u].append(w)

    # The same edge may have been generated by several teachers.
    for u in range(v):
        if len(adj[u]) > 1:
            adj[u] = list(set(adj[u]))

    # Hopcroft-Karp maximum matching.
    pair_u = [-1] * v
    pair_v = [-1] * v
    dist = [-1] * v

    from collections import deque

    def bfs():
        q = deque()

        for u in range(v):
            if pair_u[u] == -1:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = -1

        found = False

        while q:
            u = q.popleft()

            for w in adj[u]:
                pu = pair_v[w]

                if pu == -1:
                    found = True
                elif dist[pu] == -1:
                    dist[pu] = dist[u] + 1
                    q.append(pu)

        return found

    def dfs(u):
        for w in adj[u]:
            pu = pair_v[w]

            if pu == -1 or (
                dist[pu] == dist[u] + 1 and dfs(pu)
            ):
                pair_u[u] = w
                pair_v[w] = u
                return True

        dist[u] = -1
        return False

    matching = 0

    while bfs():
        for u in range(v):
            if pair_u[u] == -1 and dfs(u):
                matching += 1

    print(v - matching)

if __name__ == "__main__":
    solve()
```

The first input loop converts every algorithm name into a bit position. A teacher is then stored as one integer whose set bits identify exactly the algorithms that teacher knows.

The `local_masks` array is useful because the global bit positions can be far apart. For a teacher with (k) algorithms, its local masks range from `0` to `(1 << k) - 1`, and each local bit corresponds to one global algorithm bit. This lets us enumerate all (2^k-1) non-empty subsets without ever iterating over the potentially 1000 global algorithm positions.

The `vertex_id` dictionary is the deduplication mechanism. If two teachers can train a student on exactly the same algorithm subset, both occurrences map to the same vertex. This is necessary because two identical training sets cannot cooperate.

The adjacency construction only adds one-element extensions. The `missing` mask contains the teacher's algorithms that are absent from the current subset. Taking its lowest set bit repeatedly enumerates every possible next algorithm.

The matching arrays have one entry per feasible set. `pair_u[u]` stores the right-side vertex matched to left vertex `u`, while `pair_v[v]` stores the corresponding left vertex. The BFS constructs the layered graph used by Hopcroft-Karp, and DFS searches only along edges that respect those layers.

There is no integer-overflow issue in Python. The recursion depth of the DFS is also small in this problem because every matching edge increases the subset size by one along an inclusion path, but the recursion limit is raised anyway to make the implementation robust.

The final subtraction is the key Dilworth step. Every matching edge allows two vertices that would otherwise require separate chains to be joined into one chain. Starting from (V) singleton chains, a matching of size (M) reduces the required number of chains to (V-M), which equals the maximum antichain size.

## Worked Examples

### Sample 1

The input contains one teacher who knows three algorithms. There are seven non-empty feasible subsets.

| Step | Subset size | New feasible sets | Total vertices |
| --- | --- | --- | --- |
| Enumerate singletons | 1 | 3 | 3 |
| Enumerate pairs | 2 | 3 | 6 |
| Enumerate triple | 3 | 1 | 7 |
| Build cover edges |  | 12 | 7 |
| Maximum matching |  | 4 matched vertices | 7 |
| Final answer |  | (7-4) | 3 |

The three pair sets form an antichain of size 3. The matching has size 4, so Dilworth gives a minimum chain cover of four chains and consequently a maximum antichain of three sets.

### Sample 2

The first teacher knows four algorithms, so it contributes all 15 non-empty subsets of those four algorithms. The second teacher knows two completely different algorithms, contributing three more subsets. Since the algorithm sets are disjoint, there are 18 distinct vertices.

| Step | Source | New vertices | Total vertices |
| --- | --- | --- | --- |
| Enumerate subsets | Teacher 1 | 15 | 15 |
| Enumerate subsets | Teacher 2 | 3 | 18 |
| Build cover edges | Teacher 1 | 32 | 32 |
| Build cover edges | Teacher 2 | 2 | 34 |
| Maximum matching | Both | 10 | 18 |
| Final answer |  | (18-10) | 8 |

The interesting part is the structure of the optimal team. From the first teacher, take all six two-algorithm subsets. From the second teacher, take its two singleton subsets. The two groups use disjoint algorithms, so no selected set contains another. This gives 8 students.

This example is exactly why simply counting the largest level is insufficient. The largest level of the whole family contains 7 sets, but a mixed-rank antichain reaches 8.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(NK2^K + E\sqrt V)) | Each teacher generates (O(K2^K)) cover edges, followed by Hopcroft-Karp |
| Space | (O(V+E)) | Store distinct feasible sets, adjacency lists, and matching arrays |

Here (K\le10), (V\le N(2^K-1)), and the number of generated cover edges is at most (NK2^{K-1}). With (N=100) and (K=10), that means at most about 102,300 vertices and 512,000 generated edges before duplicate removal. These bounds are deliberately based on the small per-teacher algorithm count, rather than the potentially much larger number of globally distinct algorithm names.

## Test Cases

```python
# Save the competitive-programming solution as solution.py first.

import io
import sys

from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("""1
3 DFS BFS DIJKSTRA
""") == "3", "sample 1"

assert run("""2
4 BFS DFS LCA RMQ
2 PRIM KRUSKAL
""") == "8", "sample 2"

assert run("""4
3 BFS DFS DIJKSTRA
4 BFS DFS LCA RMQ
3 DIJKSTRA BFS DFS
3 FLOYD DFS BFS
""") == "10", "sample 3"

assert run("""1
1 HAVEFUN
""") == "1", "sample 4"

assert run("""3
4 FFEK DANTZIG DEMOUCRON FFT
4 PRIM KRUSKAL LCA FLOYD
4 DFS BFS DIJKSTRA RMQ
""") == "18", "sample 5"

# Minimum-size input.
assert run("""1
1 A
""") == "1", "single possible student"

# Two disjoint singleton teachers.
assert run("""2
1 A
1 B
""") == "2", "disjoint singleton sets"

# All teachers have exactly the same knowledge.
same_teachers = "100\n" + "2 A B\n" * 100
assert run(same_teachers) == "2", "duplicate teachers"

# One teacher with 10 algorithms.
# Its Boolean lattice has maximum antichain size C(10, 5) = 252.
names = " ".join(f"A{i}" for i in range(10))
assert run(f"""1
10 {names}
""") == "252", "maximum local subset size"

# Mixed ranks are required for the optimum.
assert run("""2
4 A B C D
2 E F
""") == "8", "mixed-rank antichain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 A` | 1 | Minimum-size input and non-empty subset requirement |
| `2 / 1 A / 1 B` | 2 | Students trained by different teachers can coexist |
| 100 identical `2 A B` teachers | 2 | Duplicate teachers must not duplicate vertices |
| One teacher with 10 algorithms | 252 | Maximum local subset size and central Boolean-lattice antichain |
| `4 A B C D` and `2 E F` | 8 | Maximum antichain may mix different subset sizes |

## Edge Cases

The single-algorithm case is handled because the subset enumeration starts at local mask 1, so the empty training set is never inserted. For

```
1
1 HAVEFUN
```

the only vertex is `{HAVEFUN}`, there are no edges, the matching size is 0, and the answer is (1-0=1).

Disjoint teachers are handled naturally because their subsets become different global masks. For

```
2
1 A
1 B
```

the vertices are `{A}` and `{B}`. There is no inclusion edge between them, so the maximum matching is 0 and the answer is 2. This captures the fact that cooperation only compares the algorithms learned by the two students, not which teachers trained them.

Duplicate teachers are collapsed by `vertex_id`. For

```
2
2 A B
2 A B
```

both teachers generate exactly the same three vertices. The cover edges are `{A}->{A,B}` and `{B}->{A,B}`. The maximum matching has size 1, so the answer is (3-1=2). Without deduplication, a program could incorrectly treat the same training set as several different students.

The ten-algorithm boundary is handled without any special case. A teacher with ten algorithms produces exactly 1023 non-empty subsets and 512 one-element-extension edges. For one such teacher, the Boolean lattice has a central antichain of size (\binom{10}{5}=252), which the matching formulation obtains as (1023-771=252).

The mixed-rank case is the most instructive. For

```
2
4 A B C D
2 E F
```

the first teacher supplies six two-element subsets, while the second supplies `{E}` and `{F}`. None of the latter contains or is contained in any of the six pairs, so all eight sets can be selected simultaneously. The algorithm does not assume that an optimal antichain lies in one level. Dilworth's theorem finds the mixed-rank optimum automatically and returns 8.
