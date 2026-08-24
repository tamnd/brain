---
title: "CF 102191I - Project Presentation"
description: "The company hierarchy is a rooted tree. Employee u reports directly to p[u], and repeatedly following parent pointers eventually reaches the CEO. Every employee belongs to exactly one project."
date: "2026-08-24T10:57:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102191
codeforces_index: "I"
codeforces_contest_name: "PSUT Coding Marathon 2019"
rating: 0
weight: 102191
solve_time_s: 2145
verified: true
draft: false
---

[CF 102191I - Project Presentation](https://codeforces.com/problemset/problem/102191/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 35m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

The company hierarchy is a rooted tree. Employee `u` reports directly to `p[u]`, and repeatedly following parent pointers eventually reaches the CEO. Every employee belongs to exactly one project.

For a particular project, its presentation is attended by every employee assigned to that project, together with every manager on the path from each such employee to the CEO. If two project members have a common manager, that manager must be counted only once. The required answer for a project is thus the number of distinct vertices contained in the union of all root-to-project-member paths.

The input contains up to (10^6) employees, so an algorithm that walks to the CEO separately for every project member can perform (O(n^2)) work. With one million vertices, even a linear pass is already substantial in a three-second limit, so the target must be close to linear. Storing an (O(\log n)) ancestor table for every vertex is also undesirable in Python because (10^6 \log n) integers exceed the memory budget. The solution should use linear-sized arrays and avoid recursive DFS.

Several cases are easy to mishandle. If two employees from the same project lie on the same root path, their common ancestors must not be counted twice. For example,

```
3 1
1 1 1
0 1 2
```

All three employees belong to project 1, and the answer is `3`. A solution that adds the three root-path lengths independently would count employees 1 and 2 multiple times.

An employee can itself be an ancestor of another employee with the same project. For example,

```
4 2
1 2 1 2
0 1 2 3
```

Project 1 contains employees 1 and 3. Their paths are `1` and `1 -> 2 -> 3`, so the answer for project 1 is `3`, not `4`. The output is `3 4`.

The CEO can also be the only member of a project. For

```
1 1
1
0
```

the answer is `1`. Any formula that starts with an edge count and forgets the root itself will produce zero.

Finally, a project can have members in completely different branches. In

```
5 2
1 1 2 1 2
0 1 1 2 2
```

project 1 contains employees 1, 2, and 4. Its attendees are `{1, 2, 4}`, so the answer is `3`. Project 2 contains employees 3 and 5, whose paths give `{1, 2, 3, 5}`, so its answer is `4`. The correct output is `3 4`.

## Approaches

The direct solution follows every project member from that employee up through all of its managers and inserts each visited employee into a set for the project. This is correct because exactly those ancestors are supposed to attend. The problem is the amount of repeated walking. Consider a chain of (n) employees where every employee belongs to the same project. The first employee may require one parent step, the next two steps, and so on, giving

[
1 + 2 + \cdots + (n-1) = \frac{n(n-1)}2 = O(n^2)
]

parent traversals. For (n=10^6), this is about (5\cdot10^{11}) operations, far beyond the limit.

The useful observation is that for one project we do not need to explicitly build the whole union of paths. Sort the project's employees in DFS preorder. Suppose their order is (v_1,v_2,\ldots,v_k). The first employee contributes its entire path from the root, which contains `depth[v1] + 1` vertices. After that, when adding (v_i), the part of its root path that was already covered by the previous project member ends at

[
LCA(v_{i-1},v_i).
]

Consequently, the number of new vertices contributed by (v_i) is

[
depth[v_i]-depth[LCA(v_{i-1},v_i)].
]

Thus the answer is

[
1+depth[v_1]
+\sum_{i=2}^{k}
\left(depth[v_i]-depth[LCA(v_{i-1},v_i)]\right).
]

The reason consecutive preorder occurrences are enough is that subtrees form contiguous intervals in preorder. When two marked nodes are separated in preorder, every branch between them is represented by one of the consecutive transitions. Their LCAs account exactly for the portions of root paths that overlap.

We therefore only need one LCA query between consecutive occurrences of each project. There are at most (n-1) such queries in total.

A conventional binary-lifting LCA would answer these queries in (O(\log n)) each and require (O(n\log n)) memory. With (10^6) vertices, that memory usage is particularly unattractive in Python. Since all our LCA queries are known after the preorder traversal, we can instead use Tarjan's offline LCA algorithm. It answers all these queries together using a disjoint-set structure in almost linear time and linear memory.

The complete strategy is therefore to traverse the hierarchy once in preorder, generate one LCA query between every pair of consecutive employees having the same project, and then process all queries with an iterative version of Tarjan's offline LCA algorithm.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(n)) | Too slow |
| Optimal | (O(n\alpha(n))) | (O(n)) | Accepted |

Here (\alpha(n)) is the inverse Ackermann function, which grows so slowly that it is effectively constant for this constraint range.

## Algorithm Walkthrough

1. Convert the parent array into a rooted child representation. Since every employee has exactly one manager except the CEO, each non-root employee can be inserted into its manager's linked list of children. We use arrays rather than Python lists of lists because one million nested Python objects would consume far too much memory.
2. Perform an iterative DFS from the CEO. When an employee is first entered, record its depth and inspect its project. For each project, keep `prev[project]`, the most recently encountered employee of that project in preorder.
3. If the current employee is the first occurrence of its project, initialize that project's answer with `depth[current] + 1`. This counts the complete path from the CEO to the first project member.
4. If the project has appeared before, create an LCA query between `prev[project]` and the current employee. The current employee is the later endpoint in preorder. Store the query at both endpoints so Tarjan's algorithm can process it when either endpoint becomes finished. Then replace `prev[project]` with the current employee.
5. The DFS also records a postorder sequence. We need this second ordering because Tarjan's offline LCA algorithm processes a vertex only after all of its descendants have been processed.
6. Initialize a disjoint-set structure with one set per employee. For every set, also maintain its current tree ancestor. The union operations are performed after a child is finished, exactly as in Tarjan's algorithm. Union by rank keeps the DSU shallow, while path compression makes repeated `find` operations almost constant amortized time.
7. Process employees in postorder. Mark the current employee as processed. For each LCA query attached to it, if the other endpoint is already processed, the LCA is `ancestor[find(other)]`. At this moment the DSU component containing the other endpoint represents exactly the already completed part of the tree up to the LCA.
8. For a query whose later preorder endpoint is `v`, add

[
depth[v]-depth[LCA]
]

to that project's answer. This is precisely the portion of the path to `v` that was not already included by the previous occurrence of the project.

1. After processing the queries of employee `u`, merge its DSU component with its parent. If `u` is the CEO, there is no parent and the processing ends. Otherwise, after the merge, set the ancestor of the new DSU representative to `parent[u]`.

### Why it works

For a fixed project, let its employees in preorder be (v_1,\ldots,v_k). The root path to (v_1) contributes exactly `depth[v1] + 1` vertices. Consider any later (v_i). Because (v_{i-1}) is the immediately preceding project member in preorder, the already covered part of the root path to (v_i) ends at (LCA(v_{i-1},v_i)). Everything below that LCA on the path to (v_i) is new, contributing exactly `depth[v_i] - depth[LCA]`. Summing these disjoint new portions counts every attending employee exactly once.

Tarjan's offline LCA invariant supplies the required LCA values. When a vertex becomes processed, every completed child subtree has already been merged into its DSU component, but the component has not yet been merged through this vertex into its parent. Hence, for a query whose other endpoint is already processed, the ancestor stored at that endpoint's DSU representative is exactly the lowest common ancestor of the two query endpoints.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    color = array('i', map(int, input().split()))

    # parent[v] is zero-based, -1 for the CEO.
    parent = array('i', (x - 1 for x in map(int, input().split())))

    # First-child linked lists.
    head = array('i', [-1]) * n
    nxt = array('i', [-1]) * n

    root = 0
    for v in range(n):
        p = parent[v]
        if p == -1:
            root = v
        else:
            nxt[v] = head[p]
            head[p] = v

    depth = array('i', [0]) * n

    # Last occurrence of every project in preorder.
    prev = array('i', [-1]) * (m + 1)

    # At most n-1 consecutive-occurrence queries exist.
    q_u = array('i', [0]) * n
    q_v = array('i', [0]) * n
    q1 = array('i', [-1]) * n
    q2 = array('i', [-1]) * n
    q_count = 0

    answer = array('i', [0]) * (m + 1)

    # Iterative DFS. head[u] is consumed as the current child iterator.
    stack = array('i', [root])
    postorder = array('i')

    # Enter the root.
    c = color[root]
    prev[c] = root
    answer[c] = 1

    while stack:
        u = stack[-1]
        e = head[u]

        if e == -1:
            stack.pop()
            postorder.append(u)
            continue

        # Consume this child edge.
        head[u] = nxt[e]
        v = e
        depth[v] = depth[u] + 1

        c = color[v]
        old = prev[c]

        if old == -1:
            answer[c] = depth[v] + 1
        else:
            qid = q_count
            q_count += 1

            q_u[qid] = old
            q_v[qid] = v

            if q1[old] == -1:
                q1[old] = qid
            else:
                q2[old] = qid

            if q1[v] == -1:
                q1[v] = qid
            else:
                q2[v] = qid

        prev[c] = v
        stack.append(v)

    # Tarjan offline LCA.
    dsu = array('i', range(n))
    ancestor = array('i', range(n))
    rank = bytearray(n)
    processed = bytearray(n)

    def find(x):
        r = x
        while dsu[r] != r:
            r = dsu[r]

        while dsu[x] != x:
            y = dsu[x]
            dsu[x] = r
            x = y

        return r

    for u in postorder:
        processed[u] = 1

        qid = q1[u]
        if qid != -1:
            v = q_v[qid] if q_u[qid] == u else q_u[qid]
            if processed[v]:
                r = find(v)
                lca = ancestor[r]
                cur = q_v[qid]
                answer[color[cur]] += depth[cur] - depth[lca]

        qid = q2[u]
        if qid != -1:
            v = q_v[qid] if q_u[qid] == u else q_u[qid]
            if processed[v]:
                r = find(v)
                lca = ancestor[r]
                cur = q_v[qid]
                answer[color[cur]] += depth[cur] - depth[lca]

        p = parent[u]
        if p != -1:
            ru = find(u)
            rp = find(p)

            if ru != rp:
                if rank[ru] < rank[rp]:
                    dsu[ru] = rp
                    new_root = rp
                elif rank[ru] > rank[rp]:
                    dsu[rp] = ru
                    new_root = ru
                else:
                    dsu[rp] = ru
                    rank[ru] += 1
                    new_root = ru

                ancestor[new_root] = p

    sys.stdout.write(' '.join(map(str, answer[1:])))

if __name__ == "__main__":
    solve()
```

The first input line is read normally, while the two large arrays are constructed directly from iterators. Using `array('i')` keeps each integer at four bytes instead of the much larger Python integer representation. This difference matters when several arrays each contain one million elements.

The parent array is converted to zero-based indices immediately. The CEO becomes `-1`, which gives a convenient sentinel for the only vertex that should not be merged into another DSU component.

The child tree is represented using `head` and `nxt`. For every employee `v`, `nxt[v]` points to another child of `parent[v]`. The DFS consumes `head[u]` as its current child pointer, so a separate iterator array is unnecessary.

The preorder DFS performs two jobs at once. It computes depths and discovers consecutive project occurrences, while the same iterative traversal records the postorder needed later. The stack contains only vertex indices, avoiding Python recursion and its failure on a chain of one million employees.

There can be at most (n-1) LCA queries because the first occurrence of each project creates no query. Each vertex can be an endpoint of at most two such queries, one connecting it to the previous occurrence and one connecting it to the next occurrence. This allows `q1` and `q2` to store the query IDs without building a large list of Python objects for every vertex.

The answer is initialized with `depth[v] + 1` for the first occurrence of each project. The `+1` accounts for the employee itself when depth is measured with the CEO at depth zero.

The second phase implements Tarjan's offline LCA algorithm iteratively. `processed[v]` plays the role of Tarjan's black color. A query is answered only when its other endpoint has already been processed. At that moment, its DSU component represents the completed branch containing that endpoint, and `ancestor[find(v)]` gives the correct LCA.

Union by rank is used even though the DSU represents a tree traversal. The representative of a set does not have to be the actual tree ancestor, because `ancestor` separately records which tree vertex represents the highest relevant ancestor of that component. This distinction is what allows the standard nearly constant-time DSU guarantees.

All arithmetic fits comfortably in a signed 32-bit integer because every project answer is at most (n\le10^6). Python integers would also handle the values safely, but the compact integer arrays are useful for memory usage.

## Worked Examples

### Sample 1

The hierarchy is

```
1
├── 3
│   ├── 4
│   └── 5
└── 2
    └── 6
```

The child insertion order makes the actual DFS preorder `1, 3, 5, 4, 2, 6`. The project occurrences and the resulting LCA queries are shown below.

| Preorder position | Employee | Project | Previous same project | New initial contribution |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | none | 1 |
| 2 | 3 | 4 | none | 2 |
| 3 | 5 | 2 | none | 3 |
| 4 | 4 | 3 | none | 3 |
| 5 | 2 | 2 | 5 | 0 |
| 6 | 6 | 4 | 3 | 0 |

For project 2, the query is `(5, 2)`. Their LCA is employee 1. Employee 5 initially contributed three vertices, namely `{1,3,5}`. Adding employee 2 contributes `depth[2] - depth[1] = 1`, giving four attendees.

For project 4, the query is `(3, 6)`. Their LCA is employee 1. The first occurrence contributes two vertices `{1,3}`, and employee 6 contributes two additional levels from employee 1, producing four attendees.

The final answers are `1 4 3 4`.

### Custom Example

Consider

```
5 2
1 1 2 1 2
0 1 1 2 2
```

The tree is

```
1
├── 2
│   ├── 4
│   └── 5
└── 3
```

A possible DFS preorder is `1, 3, 2, 5, 4`. The relevant state is:

| Employee | Project | Previous same project | LCA query | Contribution |
| --- | --- | --- | --- | --- |
| 1 | 1 | none | none | 1 |
| 3 | 2 | none | none | 2 |
| 2 | 1 | 1 | `(1,2)` | 1 |
| 5 | 2 | 3 | `(3,5)` | 2 |
| 4 | 1 | 2 | `(2,4)` | 1 |

For project 1, the first employee is the CEO, so the initial contribution is one. The query `(1,2)` has LCA 1 and contributes one more vertex. The query `(2,4)` has LCA 2 and contributes one more vertex. The result is `3`.

For project 2, employee 3 contributes `{1,3}`, and employee 5 contributes the path below the LCA 1, namely `{2,5}`. The result is `4`.

The output is `3 4`. This example demonstrates why ancestor-descendant pairs must not cause an entire path to be counted again.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\alpha(n))) | The DFS, query construction, and postorder traversal are linear, while Tarjan's DSU operations are amortized (O(\alpha(n))). |
| Space | (O(n)) | Every tree, query, traversal, and DSU structure uses a linear-sized compact array. |

The constraint (n\le10^6) makes the linear memory design particularly relevant. The implementation stores integer data in compact `array` objects and uses an iterative traversal, so it avoids both Python's recursive call stack and the large object overhead of nested lists. The algorithm performs only a constant number of passes over the tree plus nearly constant-amortized DSU operations.

## Test Cases

```python
import sys
import io
from array import array

def solve():
    n, m = map(int, input().split())
    color = array('i', map(int, input().split()))
    parent = array('i', (x - 1 for x in map(int, input().split())))

    head = array('i', [-1]) * n
    nxt = array('i', [-1]) * n

    root = 0
    for v in range(n):
        p = parent[v]
        if p == -1:
            root = v
        else:
            nxt[v] = head[p]
            head[p] = v

    depth = array('i', [0]) * n
    prev = array('i', [-1]) * (m + 1)
    answer = array('i', [0]) * (m + 1)

    q_u = array('i', [0]) * n
    q_v = array('i', [0]) * n
    q1 = array('i', [-1]) * n
    q2 = array('i', [-1]) * n
    q_count = 0

    stack = array('i', [root])
    postorder = array('i')

    c = color[root]
    prev[c] = root
    answer[c] = 1

    while stack:
        u = stack[-1]
        e = head[u]

        if e == -1:
            stack.pop()
            postorder.append(u)
            continue

        head[u] = nxt[e]
        v = e
        depth[v] = depth[u] + 1

        c = color[v]
        old = prev[c]

        if old == -1:
            answer[c] = depth[v] + 1
        else:
            qid = q_count
            q_count += 1

            q_u[qid] = old
            q_v[qid] = v

            if q1[old] == -1:
                q1[old] = qid
            else:
                q2[old] = qid

            if q1[v] == -1:
                q1[v] = qid
            else:
                q2[v] = qid

        prev[c] = v
        stack.append(v)

    dsu = array('i', range(n))
    ancestor = array('i', range(n))
    rank = bytearray(n)
    processed = bytearray(n)

    def find(x):
        r = x
        while dsu[r] != r:
            r = dsu[r]

        while dsu[x] != x:
            y = dsu[x]
            dsu[x] = r
            x = y

        return r

    for u in postorder:
        processed[u] = 1

        for qid in (q1[u], q2[u]):
            if qid == -1:
                continue

            v = q_v[qid] if q_u[qid] == u else q_u[qid]

            if processed[v]:
                lca = ancestor[find(v)]
                cur = q_v[qid]
                answer[color[cur]] += depth[cur] - depth[lca]

        p = parent[u]
        if p != -1:
            ru = find(u)
            rp = find(p)

            if ru != rp:
                if rank[ru] < rank[rp]:
                    dsu[ru] = rp
                    new_root = rp
                elif rank[ru] > rank[rp]:
                    dsu[rp] = ru
                    new_root = ru
                else:
                    dsu[rp] = ru
                    rank[ru] += 1
                    new_root = ru

                ancestor[new_root] = p

    sys.stdout.write(' '.join(map(str, answer[1:])))

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    try:
        solve()
        return ""
    finally:
        sys.stdin = old_stdin
        input = old_input

# Provided sample.
sample1 = """\
6 4
1 2 4 3 2 4
0 1 1 3 3 2
"""

# The helper above writes directly to stdout in solve(), so capture it.
def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_input = input
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = old_input

assert run(sample1) == "1 4 3 4", "sample 1"

assert run("""\
1 1
1
0
""") == "1", "single employee"

assert run("""\
4 1
1 1 1 1
0 1 2 3
""") == "4", "all employees same project"

assert run("""\
4 2
1 2 1 2
0 1 2 3
""") == "3 4", "ancestor-descendant overlap"

assert run("""\
5 2
1 1 2 1 2
0 1 1 2 2
""") == "3 4", "different branches"

# Maximum-size shape, one project, one million employees in a chain.
n = 1_000_000
colors = "1 " * (n - 1) + "1"
parents = "0 " + " ".join(map(str, range(1, n)))
max_case = f"{n} 1\n{colors}\n{parents}\n"

assert run(max_case) == "1000000", "maximum-size chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1 / 0` | `1` | Minimum-size tree and CEO-only project |
| `4 1 / 1 1 1 1 / 0 1 2 3` | `4` | All employees share one project and every path overlaps |
| `4 2 / 1 2 1 2 / 0 1 2 3` | `3 4` | Ancestor-descendant overlap and boundary depths |
| `5 2 / 1 1 2 1 2 / 0 1 1 2 2` | `3 4` | Project members in different branches |
| One million employees in one project forming a chain | `1000000` | Maximum `n`, long depth, iterative DFS, and linear memory |

## Edge Cases

For the single-employee case

```
1 1
1
0
```

the CEO is also the only project member. During preorder traversal, project 1 has no previous occurrence, so its answer is initialized to `depth[1] + 1 = 1`. There are no LCA queries, and the CEO has no parent to merge into. The result is `1`.

For the all-equal chain

```
4 1
1 1 1 1
0 1 2 3
```

the preorder is `1,2,3,4`. The first occurrence contributes one vertex. The consecutive queries are `(1,2)`, `(2,3)`, and `(3,4)`. Their LCAs are respectively `1`, `2`, and `3`, so every query contributes exactly one new vertex. The answer becomes `1+1+1+1=4`. No employee is counted twice even though every project member lies on the same root path.

For ancestor-descendant overlap,

```
4 2
1 2 1 2
0 1 2 3
```

project 1 occurs at employees 1 and 3. The first occurrence contributes employee 1. The LCA of employees 1 and 3 is employee 1, so the second occurrence contributes `depth[3] - depth[1] = 2`. The answer is `3`, corresponding to employees `{1,2,3}`. Project 2 similarly covers all four employees, giving `4`.

For members in different branches,

```
5 2
1 1 2 1 2
0 1 1 2 2
```

project 2 has employees 3 and 5. Their LCA is employee 1. The first member contributes two vertices, `{1,3}`, and the second contributes `depth[5] - depth[1] = 2`, adding `{2,5}`. The result is `4`. The shared CEO is counted once even though both project members require that CEO.

For the maximum-depth case, a chain of one million employees stresses both traversal depth and memory. The implementation never calls DFS recursively, so the Python recursion limit is irrelevant. Each employee contributes only to a constant number of compact arrays, and Tarjan's DSU processes the consecutive project queries without constructing an (O(n\log n)) ancestor table. For a single project containing every employee, the union of the root paths is the whole chain, so the answer is exactly `1000000`.
