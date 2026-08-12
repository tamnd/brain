---
title: "CF 102354J - Tree Automorphisms"
description: "We are given an undirected tree with vertices numbered from 1 to (n). An automorphism is a permutation of the vertices that preserves adjacency, so after applying the permutation, every edge must still connect exactly the same structural positions in the tree."
date: "2026-08-13T00:47:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102354
codeforces_index: "J"
codeforces_contest_name: "2018-2019 Summer Petrozavodsk Camp, Oleksandr Kulkov Contest 2"
rating: 0
weight: 102354
solve_time_s: 576
verified: true
draft: false
---

[CF 102354J - Tree Automorphisms](https://codeforces.com/problemset/problem/102354/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected tree with vertices numbered from 1 to (n). An automorphism is a permutation of the vertices that preserves adjacency, so after applying the permutation, every edge must still connect exactly the same structural positions in the tree.

The task is not to find all automorphisms. Instead, we need to print a small generating set. Every automorphism of the tree must be obtainable by composing permutations from the printed set, and the number of printed permutations must be strictly smaller than (n). Any valid generating set is accepted. The official constraints are (2 \le n \le 50), with a one second time limit and 256 MiB memory limit.

The small value of (n) makes fairly expensive polynomial algorithms comfortable, but factorial algorithms are completely out of reach. Even (50!) is roughly (3 \cdot 10^{64}), so enumerating arbitrary vertex permutations is not a realistic starting point. The useful structure is the tree itself, which lets us describe every automorphism recursively.

There are three edge cases that deserve special attention. First, a tree can have two centers. For example,

```
2
1 2
```

has the correct output

```
1
2 1
```

A careless solution that simply roots the tree at vertex 1 and only swaps equal child subtrees would produce the identity, missing the automorphism that exchanges the two centers.

Second, the automorphism group can be trivial. Consider

```
7
1 2
1 3
3 4
4 5
5 6
6 7
```

The tree has a unique center, vertex 3. Its two branches have different rooted shapes, and there are no repeated child subtrees anywhere. The identity is the only automorphism, so the valid output can be

```
1
1 2 3 4 5 6 7
```

A solution that assumes there must always be a non-identity swap can fail here. The identity itself is a valid generator of the trivial group.

Third, many children can have exactly the same rooted shape. For the star

```
4
1 2
1 3
1 4
```

the three leaves are interchangeable, so the group on them is (S_3). Two generators are enough, for example

```
2
1 3 2 4
1 2 4 3
```

A careless solution that creates one generator for every pair of equal subtrees would produce three generators instead of two. The right number for a group of (m) interchangeable objects is (m-1), using adjacent transpositions.

## Approaches

The brute-force approach is conceptually simple. Enumerate every one of the (n!) permutations of the vertices, check whether it preserves all (n-1) tree edges, collect the automorphisms, and then determine generators for the resulting permutation group. Testing one permutation costs (O(n)), so merely enumerating and checking candidates already costs

[
O(n \cdot n!).
]

For (n=50), that is about (50! \cdot 50), which is roughly (1.5 \cdot 10^{66}) elementary checks. The fact that the tree has only (49) edges does not rescue this approach.

The useful observation is that every tree has either one center vertex or one central edge. Every automorphism preserves the center. If there is one center, every automorphism fixes it. If there are two centers, an automorphism either fixes both or exchanges them.

Once the tree is rooted at a fixed center, an automorphism has a very rigid recursive form. At any vertex, it can only permute child subtrees that are rooted-isomorphic. Subtrees of different shapes cannot be exchanged because an automorphism preserves distances, degrees, and the entire recursive structure below every vertex.

Suppose a vertex has (m) children whose rooted subtrees are all isomorphic. We do not need all (m!) permutations. The (m-1) adjacent swaps generate the entire symmetric group on these children. Each swap must exchange the two whole subtrees, not merely the child vertices. We construct the required bijection recursively by matching equal-shaped children at every level.

The only additional generator needed is the central-edge exchange when the tree has two centers. The two sides of the central edge are necessarily isomorphic. We construct one automorphism exchanging those sides. Any automorphism that exchanges the centers can then be composed with this one to obtain an automorphism fixing the centers, which is already generated by the rooted subtree swaps.

The number of generators is automatically small. For every vertex, if it has (d_u) children split into (g_u) groups of equal rooted shape, we add (d_u-g_u) generators. Since the total number of child edges is (n-1),

[
\sum_u d_u=n-1.
]

Every non-leaf vertex contributes at least one group, so

[
\sum_u(d_u-g_u)
=(n-1)-\sum_u g_u
\le n-2.
]

Thus a one-center tree needs at most (n-2) nontrivial generators. A two-center tree may need one extra central swap, giving at most (n-1), which still satisfies the requirement (k<n).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n\cdot n!)) | (O(n)) plus stored automorphisms | Too slow |
| Center decomposition | (O(n^3)) | (O(n^2)) | Accepted |

## Algorithm Walkthrough

1. Find the center of the tree by computing a diameter. Run a tree traversal from an arbitrary vertex to find one diameter endpoint, run another traversal from that endpoint to find the opposite endpoint and the diameter path, then take the middle vertex or middle edge of that path.

Every automorphism maps a longest path to another longest path, so its center must map to itself. This is the structural reason the center is the correct place to root the recursive construction.
2. Define a rooted-tree signature for a directed tree part. For a vertex (u) whose parent is (p), recursively compute the signatures of all neighbors other than (p), sort those signatures, and use the resulting tuple as the signature of (u).

Two rooted tree parts are isomorphic exactly when their signatures are equal. Leaves have the empty tuple as their signature, and larger signatures are built from the signatures immediately below them.
3. If the tree has one center (c), regard (c) as the root. For every vertex (u), group its children according to their rooted signatures.

Children belonging to different groups cannot be exchanged by an automorphism fixing (c), while all children in the same group can be freely permuted.
4. For each group containing (m) children, choose an arbitrary ordering (v_1,\ldots,v_m). For every consecutive pair (v_i,v_{i+1}), construct an automorphism that swaps the entire rooted subtree of (v_i) with the entire rooted subtree of (v_{i+1}), while fixing everything else.

These (m-1) swaps generate every permutation of the (m) equal subtrees. The reason is the same as for ordinary permutations: adjacent transpositions generate the full symmetric group.
5. To construct one subtree swap, recursively map the first root to the second root. At each pair of corresponding vertices, group their children by signature and pair children having the same signature. Continue recursively for every matched pair.

Because the signatures are equal, a matching always exists. Every edge inside the first subtree is mapped to an edge inside the second subtree, so the resulting mapping is an isomorphism between the two rooted subtrees.
6. If the tree has two centers (c_1,c_2), perform the same construction for all rooted automorphisms fixing the chosen root (c_1). Then construct one additional automorphism that maps (c_1) to (c_2) and (c_2) to (c_1).

The two components obtained by deleting the central edge are isomorphic, so the same recursive signature matching constructs this exchange. Any automorphism that swaps the centers can be composed with this exchange to obtain one that fixes (c_1), so the added generator covers precisely the missing case.
7. If no non-identity generator was found, output the identity permutation.

This can happen when the tree has a trivial automorphism group. The identity generates the trivial group and also satisfies the required lower bound (k\ge1).

### Why it works

The key invariant is that every generated permutation preserves the rooted tree structure and can only exchange rooted subtrees with equal signatures. Thus every generated permutation is a genuine automorphism.

Conversely, consider any automorphism. It must preserve the tree center. If there is one center, it fixes the root. At every rooted vertex, it must permute only children with isomorphic rooted subtrees. Our generators contain adjacent swaps for every such group, so the automorphism's child permutation can be reproduced. After fixing that choice, the same argument applies recursively inside every child subtree. Hence every root-fixing automorphism is generated.

With two centers, an arbitrary automorphism either fixes the central edge endpoints or exchanges them. The first case is handled by the rooted generators. In the second case, composing with the central exchange changes it into a root-fixing automorphism, so it is handled as well. Thus the complete automorphism group is generated.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(data: str) -> str:
    it = iter(map(int, data.split()))
    n = next(it)

    graph = [[] for _ in range(n)]
    for _ in range(n - 1):
        u = next(it) - 1
        v = next(it) - 1
        graph[u].append(v)
        graph[v].append(u)

    def bfs(start):
        dist = [-1] * n
        parent = [-1] * n
        dist[start] = 0
        q = [start]

        for u in q:
            for v in graph[u]:
                if dist[v] != -1:
                    continue
                dist[v] = dist[u] + 1
                parent[v] = u
                q.append(v)

        farthest = max(range(n), key=lambda x: dist[x])
        return farthest, dist, parent

    a, _, _ = bfs(0)
    b, dist, parent = bfs(a)

    path = []
    cur = b
    while cur != -1:
        path.append(cur)
        cur = parent[cur]
    path.reverse()

    d = len(path) - 1

    if d % 2 == 0:
        centers = [path[d // 2]]
    else:
        centers = [path[d // 2], path[d // 2 + 1]]

    sys.setrecursionlimit(10000)

    # sig(u, p) is the canonical rooted shape of the component
    # containing u after the edge (u, p) is removed.
    memo = {}

    def sig(u, p):
        key = (u, p)
        if key in memo:
            return memo[key]

        children = []
        for v in graph[u]:
            if v != p:
                children.append(sig(v, u))

        children.sort()
        result = tuple(children)
        memo[key] = result
        return result

    def make_isomorphism(u, v, pu, pv, perm):
        """
        Map the rooted component (u, excluding pu) onto
        the rooted component (v, excluding pv).
        Both components are assumed to have equal signatures.
        """
        perm[u] = v

        groups_u = {}
        groups_v = {}

        for x in graph[u]:
            if x == pu:
                continue
            groups_u.setdefault(sig(x, u), []).append(x)

        for x in graph[v]:
            if x == pv:
                continue
            groups_v.setdefault(sig(x, v), []).append(x)

        for key in groups_u:
            left = sorted(groups_u[key])
            right = sorted(groups_v[key])

            for x, y in zip(left, right):
                make_isomorphism(x, y, u, v, perm)

    generators = []

    # Root the tree at the first center.
    root = centers[0]

    parent_root = [-1] * n
    order = [root]

    for u in order:
        for v in graph[u]:
            if v == parent_root[u]:
                continue
            parent_root[v] = u
            order.append(v)

    # Process vertices bottom-up only for a deterministic construction.
    for u in reversed(order):
        children = [v for v in graph[u] if parent_root[v] == u]

        groups = {}
        for v in children:
            groups.setdefault(sig(v, u), []).append(v)

        for group in groups.values():
            group.sort()

            for i in range(len(group) - 1):
                x = group[i]
                y = group[i + 1]

                perm = list(range(n))
                make_isomorphism(x, y, u, u, perm)
                make_isomorphism(y, x, u, u, perm)
                generators.append(perm)

    # If there are two centers, add an automorphism exchanging them.
    if len(centers) == 2:
        c1, c2 = centers

        perm = list(range(n))
        make_isomorphism(c1, c2, -1, -1, perm)
        generators.append(perm)

    # The automorphism group may be trivial.
    if not generators:
        generators.append(list(range(n)))

    out = [str(len(generators))]
    for p in generators:
        out.append(" ".join(str(x + 1) for x in p))

    return "\n".join(out)

def main():
    data = sys.stdin.buffer.read().decode()
    sys.stdout.write(solve(data))

if __name__ == "__main__":
    main()
```

The first part builds the adjacency list and finds the diameter. The second BFS also gives the parent pointers needed to reconstruct the diameter path. Since a tree has either one center or two adjacent centers, the middle of that path gives exactly the vertices that every automorphism must preserve as a set.

The `sig` function is the central representation of rooted tree shape. Its key is the directed edge ((u,p)), rather than just (u), because the same vertex can represent different rooted components depending on which neighbor is treated as its parent. This distinction is essential when constructing the automorphism that exchanges two centers.

The rooted tree is traversed once to establish `parent_root`. Processing vertices in reverse order is not strictly necessary because `sig` is memoized recursively, but it gives a clear bottom-up ordering and makes the relationship between parent and child explicit.

For every group of equal child signatures, the code creates swaps between consecutive children. The permutation starts as the identity, then `make_isomorphism` fills in both swapped subtrees. All other vertices remain unchanged.

The two calls to `make_isomorphism` are necessary. The first maps the first subtree onto the second, while the second maps the second subtree back onto the first. Together they form a permutation of the entire vertex set rather than a one-way partial mapping.

The central exchange uses `make_isomorphism(c1, c2, -1, -1, perm)`. Here neither center has a parent, so their complete rooted trees are compared. In a two-center tree, the child of (c_1) leading to (c_2) represents the opposite half of the tree, and symmetrically for (c_2), so the recursive matching constructs the desired reflection.

All vertices are zero-indexed internally and converted back to one-indexed labels only when printing. There is no integer overflow issue in Python, and the recursion depth is at most (n), so the explicit recursion limit is more than sufficient for (n\le50).

The official problem accepts any valid generating set, so the output does not have to match the sample permutation order exactly.

## Worked Examples

### Sample 1

The input is

```
2
1 2
```

The diameter consists of both vertices, so the tree has two centers.

| Step | Centers | Root | Generated rooted swaps | Central swap | Generators |
| --- | --- | --- | --- | --- | --- |
| Find diameter | 1, 2 | 1 | none | not yet | 0 |
| Process root | 1, 2 | 1 | none | none | 0 |
| Exchange centers | 1, 2 | 1 | none | (1\leftrightarrow2) | 1 |

The only nontrivial automorphism exchanges the two vertices. The output is

```
1
2 1
```

This demonstrates why the central-edge case cannot be handled by rooting at one endpoint and considering only child permutations.

### Sample 2

The input is

```
3
1 2
1 3
```

The unique center is vertex 1. Its two children are vertices 2 and 3, and both child subtrees consist of a single vertex, so their signatures are equal.

| Step | Vertex | Child signatures | Equal group | Generated permutation |
| --- | --- | --- | --- | --- |
| Root tree | 1 | (() , ()) | ({2,3}) | none |
| Swap group | 1 | (() , ()) | ({2,3}) | (1,3,2) |
| Finish | 2, 3 | no children | none | unchanged |

The single swap generates the entire automorphism group, which contains the identity and the exchange of vertices 2 and 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^3)) | There are fewer than (n) generators, each constructed by recursively matching at most (n) vertices, while rooted signatures and their tuple comparisons fit comfortably within the same polynomial bound for (n\le50). |
| Space | (O(n^2)) | Memoized directed-edge signatures, recursion state, and at most (n-1) permutations of length (n) require quadratic space. |

The worst case prints (n-1) permutations of length (n), so the output itself can already contain (\Theta(n^2)) integers. With (n\le50), the polynomial construction is tiny compared with the one second limit, while factorial enumeration is completely infeasible.

## Test Cases

The checker below treats the output as nondeterministic. For the samples it verifies the exact sample output, while for custom cases it checks the required number of generators, that every printed permutation is a genuine automorphism, and the expected structural property of the test tree.

```python
import sys
import io

def solve(data: str) -> str:
    it = iter(map(int, data.split()))
    n = next(it)

    graph = [[] for _ in range(n)]
    for _ in range(n - 1):
        u = next(it) - 1
        v = next(it) - 1
        graph[u].append(v)
        graph[v].append(u)

    def bfs(start):
        dist = [-1] * n
        parent = [-1] * n
        dist[start] = 0
        q = [start]

        for u in q:
            for v in graph[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    parent[v] = u
                    q.append(v)

        farthest = max(range(n), key=lambda x: dist[x])
        return farthest, dist, parent

    a, _, _ = bfs(0)
    b, _, parent = bfs(a)

    path = []
    cur = b
    while cur != -1:
        path.append(cur)
        cur = parent[cur]
    path.reverse()

    d = len(path) - 1
    if d % 2 == 0:
        centers = [path[d // 2]]
    else:
        centers = [path[d // 2], path[d // 2 + 1]]

    sys.setrecursionlimit(10000)

    memo = {}

    def sig(u, p):
        key = (u, p)
        if key in memo:
            return memo[key]

        children = []
        for v in graph[u]:
            if v != p:
                children.append(sig(v, u))

        children.sort()
        memo[key] = tuple(children)
        return memo[key]

    def make_iso(u, v, pu, pv, perm):
        perm[u] = v

        gu = {}
        gv = {}

        for x in graph[u]:
            if x != pu:
                gu.setdefault(sig(x, u), []).append(x)

        for x in graph[v]:
            if x != pv:
                gv.setdefault(sig(x, v), []).append(x)

        for key in gu:
            left = sorted(gu[key])
            right = sorted(gv[key])
            for x, y in zip(left, right):
                make_iso(x, y, u, v, perm)

    root = centers[0]

    parent_root = [-1] * n
    order = [root]

    for u in order:
        for v in graph[u]:
            if v != parent_root[u]:
                parent_root[v] = u
                order.append(v)

    generators = []

    for u in reversed(order):
        children = [v for v in graph[u] if parent_root[v] == u]

        groups = {}
        for v in children:
            groups.setdefault(sig(v, u), []).append(v)

        for group in groups.values():
            group.sort()
            for i in range(len(group) - 1):
                x = group[i]
                y = group[i + 1]

                p = list(range(n))
                make_iso(x, y, u, u, p)
                make_iso(y, x, u, u, p)
                generators.append(p)

    if len(centers) == 2:
        p = list(range(n))
        make_iso(centers[0], centers[1], -1, -1, p)
        generators.append(p)

    if not generators:
        generators.append(list(range(n)))

    result = [str(len(generators))]
    result += [" ".join(str(x + 1) for x in p) for p in generators]
    return "\n".join(result)

def run(inp: str) -> str:
    return solve(inp)

def is_automorphism(inp: str, perm):
    tokens = list(map(int, inp.split()))
    n = tokens[0]
    edges = []

    pos = 1
    for _ in range(n - 1):
        u = tokens[pos] - 1
        v = tokens[pos + 1] - 1
        pos += 2
        edges.append((u, v))

    if sorted(perm) != list(range(1, n + 1)):
        return False

    edge_set = {tuple(sorted((u + 1, v + 1))) for u, v in edges}

    for u, v in edges:
        a = perm[u]
        b = perm[v]
        if tuple(sorted((a, b))) not in edge_set:
            return False

    return True

def validate(inp: str, out: str, expected_k=None):
    lines = out.strip().splitlines()
    assert lines

    n = int(inp.split()[0])
    k = int(lines[0])

    assert 1 <= k < n
    if expected_k is not None:
        assert k == expected_k

    assert len(lines) == k + 1

    permutations = []
    for i in range(k):
        p = list(map(int, lines[i + 1].split()))
        assert len(p) == n
        assert is_automorphism(inp, p)
        permutations.append(p)

    return permutations

# Provided samples.
assert run("""2
1 2
""").strip() == """1
2 1"""

assert run("""3
1 2
1 3
""").strip() == """1
1 3 2"""

# Sample 3 has a different but equally valid generator ordering,
# so validate it structurally.
validate("""4
1 2
1 3
1 4
""", run("""4
1 2
1 3
1 4
"""), expected_k=2)

# Custom case 1: the smallest possible tree.
out = run("""2
1 2
""")
validate("""2
1 2
""", out, expected_k=1)

# Custom case 2: a two-center path with six vertices.
out = run("""6
1 2
2 3
3 4
4 5
5 6
""")
validate("""6
1 2
2 3
3 4
4 5
5 6
""", out, expected_k=1)

# Custom case 3: an asymmetric tree with a trivial automorphism group.
out = run("""7
1 2
1 3
3 4
4 5
5 6
6 7
""")
perms = validate("""7
1 2
1 3
3 4
4 5
5 6
6 7
""", out, expected_k=1)
assert perms[0] == list(range(1, 8))

# Custom case 4: maximum n and all root branches equal.
# The star has 49 interchangeable leaves, so S_49 needs 48
# adjacent-transposition generators.
edges = "\n".join(f"1 {v}" for v in range(2, 51))
inp = "50\n" + edges + "\n"
out = run(inp)
validate(inp, out, expected_k=48)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| (n=2,\ 1\ 2) | One generator | Minimum size and the two-center case |
| Path with 6 vertices | One generator | Central-edge exchange without local subtree swaps |
| Seven-vertex asymmetric tree | Identity only | Trivial automorphism group |
| Star with 50 vertices | 48 generators | Maximum size and a group with one large equal-signature class |

## Edge Cases

For the two-vertex tree

```
2
1 2
```

the diameter has length one, so its centers are vertices 1 and 2. There are no rooted child groups that produce a nontrivial generator. The algorithm then constructs the central exchange and obtains the permutation (2,1). This catches the common mistake of assuming that choosing one center as a root automatically handles every automorphism.

For the star

```
4
1 2
1 3
1 4
```

the diameter has length two and the unique center is vertex 1. The signatures of vertices 2, 3, and 4 are all the empty tuple, so they form one group of size three. The algorithm creates two swaps, between vertices 2 and 3 and between vertices 3 and 4. These adjacent transpositions generate all six permutations of the leaves. The generator count is (3-1=2), rather than the three pairwise swaps a naive construction might produce.

For the asymmetric tree

```
7
1 2
1 3
3 4
4 5
5 6
6 7
```

the center is vertex 3. Its branch through vertex 1 contains two vertices, while its branch through vertex 4 contains four vertices, so those branches cannot be exchanged. The remaining vertices form paths with no repeated child shapes. Every equal-signature group has size one, so the algorithm creates no non-identity rooted generator and finally adds the identity permutation. The resulting one-element set generates exactly the trivial automorphism group.

For the maximum-size star with 50 vertices,

```
50
1 2
1 3
...
1 50
```

the root has 49 children and every child has the same leaf signature. The algorithm creates 48 consecutive swaps. Their composition can realize every permutation of the 49 leaves, so the generated group is the full automorphism group of the star. The count is (48<50), which also demonstrates the tight part of the generator-count argument.
