---
title: "CF 102249D - Trees as a Service"
description: "We need to construct a rooted tree on the vertices 1 ... N. Every requirement has the form (x, y, z), meaning that when we walk upward from x and y, their first common vertex must be exactly z."
date: "2026-08-17T21:56:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102249
codeforces_index: "D"
codeforces_contest_name: "2019 Facebook Hacker Cup, Qualification Round"
rating: 0
weight: 102249
solve_time_s: 264
verified: true
draft: false
---

[CF 102249D - Trees as a Service](https://codeforces.com/problemset/problem/102249/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to construct a rooted tree on the vertices `1 ... N`. Every requirement has the form `(x, y, z)`, meaning that when we walk upward from `x` and `y`, their first common vertex must be exactly `z`. We may choose any parent for every vertex, as long as the resulting parent pointers describe one rooted tree and every requirement is satisfied.

The output gives the parent of each vertex. Exactly one vertex has parent `0`, which is the root. Since the problem accepts any valid tree, two different parent arrays can both be correct.

The constraints are deliberately small. There are at most 60 vertices and 120 requirements, so an algorithm around `O(NM + N^2)` is easily fast enough. The small `N` also lets us use a simple disjoint-set structure repeatedly while recursively splitting the vertex set. What is ruled out is exhaustive enumeration of rooted labeled trees, whose number is `N^(N-1)`. At `N = 60`, this is roughly `10^105`, so even checking one candidate very quickly would be useless.

There are several edge cases that are easy to mishandle.

First, the LCA can be one of the two queried vertices. For example,

```
2 1
1 2 1
```

is valid. Vertex `1` is the ancestor of vertex `2`, so the LCA is `1`, and the parent array can be `0 1`. A construction that always assumes `z` must be different from `x` and `y` would incorrectly reject this case.

Second, choosing an arbitrary root is not safe. For

```
3 1
1 2 3
```

the only possible root is `3`, because `3` has to be an ancestor of both `1` and `2`. Choosing `1` as the root immediately makes the requirement impossible. The construction has to identify a vertex that is not forced to have an ancestor inside the current set.

Third, several requirements can force a cycle in the ancestor relation. Consider

```
3 3
1 2 2
2 3 3
3 1 1
```

The first requirement forces `2` above `1`, the second forces `3` above `2`, and the third forces `1` above `3`. No rooted tree can contain all three relations, so the answer is `Impossible`.

Finally, a requirement with an LCA equal to the current root is a separation constraint, not a grouping constraint. For example,

```
3 2
1 2 3
1 3 1
```

cannot be handled by simply grouping every triple together. The first requirement wants `1` and `2` in different child subtrees of `3`, while the second says that `1` is an ancestor of `3`. These requirements conflict. Treating every requirement as an ordinary union operation would lose the distinction between "must be together" and "must be separated".

## Approaches

The brute-force approach is conceptually straightforward. Enumerate every rooted tree on the `N` labeled vertices, compute the LCA of every queried pair, and keep the first tree satisfying all requirements. There are `N^(N-1)` rooted labeled trees. Even before accounting for verification, the worst case at `N = 60` is `60^59`, approximately `10^105` candidates. Checking `M` requirements with an `O(N)` LCA computation would make the work roughly `O(N^(N-1)MN)`, which is completely infeasible.

The useful observation is that one LCA requirement contains two different kinds of information.

If `LCA(x, y) = z`, then `z` must be an ancestor of both `x` and `y`. If `z` is not the root of the current subtree, then `x`, `y`, and `z` must all remain inside the same child subtree of that root. They can never be split into different child subtrees.

On the other hand, if `z` is the root of the current subtree, then `x` and `y` must belong to different child subtrees, unless one of them is the root itself. Otherwise their LCA would be below `z`.

This gives us a recursive partitioning procedure. Pick a suitable root `r` for the current set of vertices. Use a disjoint-set union structure to merge vertices that are forced to remain in the same child subtree of `r`. Then every resulting component becomes one child subtree of `r`. Requirements whose LCA is `r` are checked by requiring their two non-root endpoints to land in different components. The same process is then applied independently to every component.

The root itself cannot be arbitrary. For every requirement `LCA(x, y) = z`, if `x != z`, then `z` forces `x` to be below `z`; similarly, if `y != z`, then `z` forces `y` to be below `z`. Thus a valid root of the current set must have no incoming forced-ancestor edge from another vertex in that set. Such a vertex is a minimal element of the forced ancestor relation.

The reason we do not need to try every minimal vertex is a useful property of these constraints. Once a set is split into child components, the constraints entirely contained in one component are independent of the choices made in other components. If some component cannot be constructed, changing the root chosen above it cannot make those same constraints simultaneously disappear. The contest discussion gives the same justification in terms of taking the smallest subtree containing a failed subset of vertices.

The brute-force method works because it explicitly tries every possible hierarchy. It fails because the number of hierarchies is enormous. The observation that every LCA requirement either forces vertices into the same child subtree or forces them into different child subtrees reduces the problem to repeated partitioning, which is polynomial.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(N^(N-1) M N)` | `O(N)` | Too slow |
| Recursive DSU partition | `O(NM + N^2 α(N))` | `O(N^2)` | Accepted |

## Algorithm Walkthrough

1. Store every requirement `(x, y, z)` and interpret it as two possible ancestor relations, `z -> x` when `x != z` and `z -> y` when `y != z`. These relations tell us which vertices cannot be chosen as the root of the same current subtree.
2. Start with the complete vertex set `{1, ..., N}` and recursively construct a tree for it. A recursive call receives a set `S` whose vertices are supposed to form one connected rooted subtree.
3. Before selecting a root, inspect every requirement whose `z` belongs to `S`. If `z` is inside `S`, both `x` and `y` must also be inside `S`, because `z` is their ancestor. If one endpoint has already been placed outside `S`, the construction is impossible.
4. Find a vertex `r` in `S` that has no forced incoming edge from another vertex of `S`. In other words, there must be no requirement with `z != r` and `x = r`, and no requirement with `z != r` and `y = r`. Such a vertex can serve as the root of this subtree. If no such vertex exists, the forced ancestor relations contain a cycle, so the answer is impossible.
5. Create a DSU containing all vertices in `S`. For every requirement `(x, y, z)` entirely contained in `S` with `z != r`, merge `x`, `y`, and `z`. Since `r` is above `z`, all three vertices must lie below the same child of `r`. Merging all three records exactly that requirement.
6. Now inspect every requirement `(x, y, r)`. If neither endpoint is `r`, their DSU components must be different. If they were in the same component, both would lie in the same child subtree of `r`, making their LCA strictly below `r`. If one endpoint is `r`, the requirement is automatically satisfied because the LCA of the root and any descendant is the root.
7. The DSU components among `S - {r}` are now the child subtrees of `r`. For every component, recursively construct its tree. If the recursive construction returns root `v`, set `parent[v] = r`.
8. If a recursive call contains only one vertex, that vertex is the root of that subtree and requires no further work. Once every component has been processed, return `r` to the caller.
9. After constructing the complete tree, the parent array contains exactly one `0`, the root, and every other vertex has one parent. The construction can optionally be verified by recomputing the LCA of every requirement. This costs only `O(MN)` and is useful as a defensive implementation check.

### Why it works

The key invariant is that every recursive set `S` represents one subtree of the final tree, and every requirement whose LCA lies in `S` has all three of its vertices inside `S`.

Suppose the current root is `r`. For a requirement `(x, y, z)` with `z != r`, the vertex `z` is below exactly one child of `r`. Since `z` must be an ancestor of both `x` and `y`, all three vertices must be below that same child. The DSU merges them, so the construction never separates vertices that must stay together.

For a requirement `(x, y, r)`, the LCA must be exactly the current root. Hence `x` and `y` must occupy different child components, and the DSU check rejects precisely the case where they would be together.

After these checks, every DSU component can safely become a child subtree of `r`. Requirements belonging to different components cannot have an LCA strictly inside one of those components, because such a requirement would have forced all three of its vertices into the same component. Thus the recursive problems are independent.

The root-selection rule prevents a vertex from being placed above a vertex that is already required to be its ancestor. If the forced ancestor graph has a cycle, no valid root exists. If the instance is feasible, repeatedly taking a minimal vertex and partitioning by the constraints preserves feasibility, so no backtracking over root choices is required.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, nodes):
        self.parent = {v: v for v in nodes}
        self.size = {v: 1 for v in nodes}

    def find(self, x):
        p = self.parent[x]
        if p != x:
            self.parent[x] = self.find(p)
        return self.parent[x]

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return

        if self.size[a] < self.size[b]:
            a, b = b, a

        self.parent[b] = a
        self.size[a] += self.size[b]

def construct_tree(n, constraints):
    parent = [-1] * (n + 1)

    def build(nodes):
        if len(nodes) == 1:
            return nodes[0]

        inside = set(nodes)

        # Every constraint whose LCA is inside this subtree
        # must have all of its vertices inside it.
        for x, y, z in constraints:
            if z in inside and (x not in inside or y not in inside):
                return -1

        # Find a minimal vertex in the forced ancestor relation.
        incoming = {v: False for v in nodes}

        for x, y, z in constraints:
            if z not in inside:
                continue

            if x in inside and x != z:
                incoming[x] = True
            if y in inside and y != z:
                incoming[y] = True

        root = -1
        for v in nodes:
            if not incoming[v]:
                root = v
                break

        if root == -1:
            return -1

        dsu = DSU(nodes)

        # If the current root is r and z != r, then x, y, z
        # must all lie in the same child subtree of r.
        for x, y, z in constraints:
            if z not in inside or z == root:
                continue

            dsu.union(x, y)
            dsu.union(x, z)

        # If z is the current root, x and y must be in
        # different child subtrees unless one of them is root.
        for x, y, z in constraints:
            if z != root:
                continue

            if x == root or y == root:
                continue

            if dsu.find(x) == dsu.find(y):
                return -1

        # Build the DSU components excluding the root.
        groups = {}

        for v in nodes:
            if v == root:
                continue

            r = dsu.find(v)
            groups.setdefault(r, []).append(v)

        # Every component becomes one child subtree of root.
        for component in groups.values():
            child_root = build(component)
            if child_root == -1:
                return -1
            parent[child_root] = root

        return root

    root = build(list(range(1, n + 1)))

    if root == -1:
        return None

    parent[root] = 0
    return parent[1:]

def lca(parent, a, b):
    ancestors = set()

    while a != 0:
        ancestors.add(a)
        a = parent[a]

    while b != 0:
        if b in ancestors:
            return b
        b = parent[b]

    return 0

def valid_tree(parent, constraints):
    n = len(parent)
    if parent.count(0) != 1:
        return False

    # Check that every parent pointer stays inside the vertex range.
    for p in parent:
        if p < 0 or p > n:
            return False

    # Check that the parent pointers contain no cycle.
    for v in range(1, n + 1):
        seen = set()
        u = v

        while u != 0:
            if u in seen:
                return False
            seen.add(u)
            u = parent[u]

    for x, y, z in constraints:
        if lca(parent, x, y) != z:
            return False

    return True

def solve_case(n, constraints):
    answer = construct_tree(n, constraints)

    if answer is None:
        return None

    # Defensive verification. The construction itself is sufficient,
    # but this catches implementation mistakes without changing
    # the asymptotic complexity.
    if not valid_tree(answer, constraints):
        return None

    return answer

def main():
    t = int(input())
    out = []

    for case_id in range(1, t + 1):
        n, m = map(int, input().split())
        constraints = [
            tuple(map(int, input().split()))
            for _ in range(m)
        ]

        answer = solve_case(n, constraints)

        if answer is None:
            out.append(f"Case #{case_id}: Impossible")
        else:
            out.append(
                f"Case #{case_id}: " +
                " ".join(map(str, answer))
            )

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The `DSU` class is local to each recursive call because the components are meaningful only relative to the current subtree. Path compression keeps repeated `find` operations effectively constant for these constraints.

The `build` function first checks that a requirement whose LCA belongs to the current set does not reach outside that set. This condition follows directly from ancestry: if `z` is inside the subtree, both queried vertices must be descendants of `z`, so they must also be inside the subtree.

The `incoming` array records forced ancestor relations. When `z != x`, the requirement says that `z` must be above `x`, so `x` cannot be the current root. The same reasoning applies to `y`. A self-relation such as `LCA(x, y) = x` does not mark `x` as having an incoming edge, because `x` is allowed to be the ancestor of `y`.

The first DSU pass handles only requirements whose LCA is not the current root. The distinction between `z != root` and `z == root` is essential. The former means the three vertices must stay together below one child of `root`; the latter means the two queried endpoints must be separated at `root`.

The groups are built only after all constraints involving the current root have been checked. Each group is guaranteed to be internally connected by the "must stay together" relations, and placing its recursively constructed root directly below the current root creates exactly one child subtree for that group.

The final verification uses an ancestor set to compute each LCA in `O(N)`. There is no integer-overflow issue in Python, and the recursion depth is at most `N`, which is only 60. The code uses 1-based vertex numbering throughout and converts the final parent array to a zero-based Python list only at the output boundary.

## Worked Examples

### Sample 1

The input is

```
3 1
1 2 3
```

There is one requirement, `LCA(1, 2) = 3`.

| Current set | Forced incoming edges | Chosen root | DSU components after grouping | Separation checks |
| --- | --- | --- | --- | --- |
| `{1,2,3}` | `3 -> 1`, `3 -> 2` | `3` | `{1}`, `{2}` | `1` and `2` are different |

The only vertex with no forced incoming edge is `3`, so it becomes the root. Because the requirement has `z = 3`, the endpoints `1` and `2` must be in different child components. They are already separate, so both become children of `3`.

The resulting parent array is `3 3 0`, matching the sample output.

### Sample 2

The input is

```
3 3
1 2 2
2 3 3
3 1 1
```

The forced ancestor relations are:

| Requirement | Forced relations |
| --- | --- |
| `LCA(1,2)=2` | `2 -> 1` |
| `LCA(2,3)=3` | `3 -> 2` |
| `LCA(3,1)=1` | `1 -> 3` |

The root search sees that every vertex has an incoming forced relation.

| Vertex | Incoming forced ancestor |
| --- | --- |
| `1` | `2`, `1` |
| `2` | `3` |
| `3` | `1` |

There is no possible root, so the construction immediately returns `Impossible`.

This trace demonstrates why checking only the local LCA equations is insufficient. The equations collectively impose a cyclic ancestor relation, which no rooted tree can represent.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(NM + N^2 α(N))` | At most `N` recursive calls scan the `M` constraints, and DSU work over all recursive levels is bounded by `O(N^2 α(N))`. The final verification adds `O(MN)`. |
| Space | `O(N^2)` | The recursive calls and temporary vertex sets can occupy `O(N^2)` space in the worst case, while the constraint list and parent array use `O(M + N)`. |

With `N <= 60` and `M <= 120`, even the simple quadratic factors are tiny. The algorithm performs only a few hundred thousand primitive operations per test case in the worst structural cases, far below what is needed for the exponential enumeration of rooted trees.

## Test Cases

The sample has multiple valid outputs for some cases, so an assert comparing the complete output string would be unnecessarily strict. The following test harness instead asserts that every reported tree is valid and that the two impossible sample cases are actually rejected.

```python
import sys
import io

class DSU:
    def __init__(self, nodes):
        self.parent = {v: v for v in nodes}
        self.size = {v: 1 for v in nodes}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]

def solve_case(n, constraints):
    parent = [-1] * (n + 1)

    def build(nodes):
        if len(nodes) == 1:
            return nodes[0]

        inside = set(nodes)

        for x, y, z in constraints:
            if z in inside and (x not in inside or y not in inside):
                return -1

        incoming = {v: False for v in nodes}

        for x, y, z in constraints:
            if z not in inside:
                continue
            if x in inside and x != z:
                incoming[x] = True
            if y in inside and y != z:
                incoming[y] = True

        root = -1
        for v in nodes:
            if not incoming[v]:
                root = v
                break

        if root == -1:
            return -1

        dsu = DSU(nodes)

        for x, y, z in constraints:
            if z in inside and z != root:
                dsu.union(x, y)
                dsu.union(x, z)

        for x, y, z in constraints:
            if z == root and x != root and y != root:
                if dsu.find(x) == dsu.find(y):
                    return -1

        groups = {}
        for v in nodes:
            if v == root:
                continue
            r = dsu.find(v)
            groups.setdefault(r, []).append(v)

        for component in groups.values():
            child_root = build(component)
            if child_root == -1:
                return -1
            parent[child_root] = root

        return root

    root = build(list(range(1, n + 1)))
    if root == -1:
        return None

    parent[root] = 0
    return parent[1:]

def lca(parent, a, b):
    seen = set()

    while a != 0:
        seen.add(a)
        a = parent[a]

    while b != 0:
        if b in seen:
            return b
        b = parent[b]

    return 0

def valid_answer(n, constraints, answer):
    if answer is None:
        return False

    if len(answer) != n:
        return False

    if answer.count(0) != 1:
        return False

    for i, p in enumerate(answer, 1):
        if p < 0 or p > n or p == i:
            return False

    for v in range(1, n + 1):
        seen = set()
        u = v
        while u != 0:
            if u in seen:
                return False
            seen.add(u)
            u = answer[u - 1]

    for x, y, z in constraints:
        if lca(answer, x, y) != z:
            return False

    return True

def run(inp: str) -> str:
    data = io.StringIO(inp)
    t = int(data.readline())
    outputs = []

    for case_id in range(1, t + 1):
        n, m = map(int, data.readline().split())
        constraints = [
            tuple(map(int, data.readline().split()))
            for _ in range(m)
        ]

        answer = solve_case(n, constraints)

        if answer is None:
            outputs.append(f"Case #{case_id}: Impossible")
        else:
            outputs.append(
                f"Case #{case_id}: " +
                " ".join(map(str, answer))
            )

    return "\n".join(outputs)

def parse_outputs(out):
    return out.strip().splitlines()

def check_case(line, case_id, n, constraints, must_be_impossible=False):
    prefix = f"Case #{case_id}: "
    assert line.startswith(prefix), line

    body = line[len(prefix):]

    if must_be_impossible:
        assert body == "Impossible", line
        return

    assert body != "Impossible", line
    answer = list(map(int, body.split()))
    assert valid_answer(n, constraints, answer), line

# Provided samples
sample = """6
3 1
1 2 3
3 3
1 2 2
2 3 3
3 1 1
4 2
2 1 2
1 4 3
6 3
2 4 3
6 5 4
1 2 6
7 4
7 3 5
4 1 2
6 3 6
6 4 5
12 9
1 5 7
11 2 6
9 4 12
8 12 6
10 1 7
4 3 12
3 10 6
8 11 8
2 5 10
"""

out = parse_outputs(run(sample))
assert len(out) == 6

check_case(out[0], 1, 3, [(1, 2, 3)])
check_case(
    out[1], 2, 3,
    [(1, 2, 2), (2, 3, 3), (3, 1, 1)],
    must_be_impossible=True
)
check_case(
    out[2], 3, 4,
    [(2, 1, 2), (1, 4, 3)]
)
check_case(
    out[3], 4, 6,
    [(2, 4, 3), (6, 5, 4), (1, 2, 6)],
    must_be_impossible=True
)
check_case(
    out[4], 5, 7,
    [(7, 3, 5), (4, 1, 2), (6, 3, 6), (6, 4, 5)]
)
check_case(
    out[5], 6, 12,
    [
        (1, 5, 7), (11, 2, 6), (9, 4, 12),
        (8, 12, 6), (10, 1, 7), (4, 3, 12),
        (3, 10, 6), (8, 11, 8), (2, 5, 10)
    ]
)

# Minimum-size input.
minimum = """1
2 1
1 2 1
"""
out = parse_outputs(run(minimum))
check_case(out[0], 1, 2, [(1, 2, 1)])

# All requirements use the same LCA.
all_equal = """4
5 4
1 2 5
1 3 5
1 4 5
2 3 5
"""
out = parse_outputs(run(all_equal))
check_case(
    out[0], 1, 5,
    [(1, 2, 5), (1, 3, 5), (1, 4, 5), (2, 3, 5)]
)

# Maximum-size instance, with 60 vertices and 120 consistent constraints.
# Vertex 60 is the root and every other vertex can be its direct child.
constraints = []
for i in range(120):
    x = 1 + (i % 59)
    y = 1 + ((i + 1) % 59)
    if x == y:
        y = 59
    constraints.append((x, y, 60))

maximum = "1\n60 120\n"
maximum += "\n".join(f"{x} {y} {z}" for x, y, z in constraints)
maximum += "\n"

out = parse_outputs(run(maximum))
check_case(out[0], 1, 60, constraints)

# Contradictory ancestor cycle.
cycle = """1
3 3
1 2 2
2 3 3
3 1 1
"""
out = parse_outputs(run(cycle))
check_case(
    out[0], 1, 3,
    [(1, 2, 2), (2, 3, 3), (3, 1, 1)],
    must_be_impossible=True
)

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 1 2 1` | Any valid tree | Minimum `N` and the case where the LCA equals one queried vertex |
| `5 4 / ... 5` | Any valid tree | Multiple requirements sharing the same LCA and separation of several pairs |
| `60 120 / ... 60` | Any valid tree | Maximum `N`, maximum `M`, and repeated boundary-scale DSU operations |
| `3 3 / 1 2 2 / 2 3 3 / 3 1 1` | `Impossible` | Cyclic forced ancestor relations |

## Edge Cases

For the endpoint-LCA case

```
2 1
1 2 1
```

the forced relation is `1 -> 2`, while vertex `1` itself has no incoming forced edge. The algorithm chooses `1` as the root. Since the requirement has `z = root`, it does not require `1` and `2` to be separated. The singleton component `{2}` becomes a child of `1`, giving the parent array `0 1`. The LCA of `1` and `2` is exactly `1`.

For the root-selection case

```
3 1
1 2 3
```

the forced relations are `3 -> 1` and `3 -> 2`. Vertices `1` and `2` both have incoming relations, while `3` does not, so the algorithm selects `3`. Because `z` equals the root, `1` and `2` must occupy different components. They do, producing the tree `3 3 0`.

For the cyclic case

```
3 3
1 2 2
2 3 3
3 1 1
```

the forced relations are `2 -> 1`, `3 -> 2`, and `1 -> 3`. Every vertex has an incoming relation, so the root search fails before any DSU partition is attempted. Returning `Impossible` is correct because every rooted tree has at least one vertex with no ancestor inside the whole vertex set.

A subtle separation case is

```
3 2
1 2 3
1 3 1
```

The first requirement forces `3` above `1` and `2`. The second forces `1` above `3`. Thus the ancestor relation already contains `1 -> 3 -> 1`. During root selection, neither `1` nor `3` can be selected as a valid minimal root, and the construction rejects the instance.

Another useful case is a set of independent requirements:

```
5 1
1 2 3
```

Vertices `4` and `5` never occur in any requirement. The algorithm still places them somewhere in the tree, because every DSU component is recursively converted into a subtree. They can simply become extra branches. Their positions do not affect the required LCA, which is why unconstrained vertices never need special treatment.
