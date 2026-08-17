---
title: "CF 102201J - Jealous Teachers"
description: "Think of the students and teachers as the two sides of a bipartite graph. There are (N-1) students on the left and (N) teachers on the right. An input pair ((s,t)) means that student (s) is allowed to send flowers to teacher (t)."
date: "2026-08-18T01:52:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102201
codeforces_index: "J"
codeforces_contest_name: "Moscow Pre-Finals Workshop 2019. KAIST Contest"
rating: 0
weight: 102201
solve_time_s: 229
verified: true
draft: false
---

[CF 102201J - Jealous Teachers](https://codeforces.com/problemset/problem/102201/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

Think of the students and teachers as the two sides of a bipartite graph. There are (N-1) students on the left and (N) teachers on the right. An input pair ((s,t)) means that student (s) is allowed to send flowers to teacher (t).

Each student must distribute exactly (N) flowers, while every teacher must receive exactly (N-1) flowers. For every allowed pair, we need to choose a nonnegative integer amount. An edge may carry many flowers, and an allowed edge may carry zero flowers. The output gives these amounts in the same order as the input edges. If no such assignment exists, we print (-1). The problem is a special transportation problem on a sparse bipartite graph.

The total supply is ((N-1)N), and the total demand is (N(N-1)), so the global totals already agree. The difficulty is entirely caused by the restriction on which student-teacher pairs are available.

The bounds (N\le 10^5) and (M\le 2\cdot10^5) rule out algorithms that repeatedly process the whole graph (N) times. An (O(NM)) method could inspect roughly (2\cdot10^{10}) edges in the worst case. Even an ordinary unit-augmentation max-flow formulation can require (N(N-1)) augmentations, giving (O(MN^2)), around (2\cdot10^{15}) edge inspections in the worst case. We need a matching algorithm around (O(M\sqrt N)), followed by linear-time construction.

There are several edge cases where a seemingly reasonable implementation fails. For example, with (N=2),

```
2 2
1 1
1 2
```

the only student can give one flower to each teacher, so the output must be `1 1`. An implementation that insists every teacher must be matched by a distinct student would incorrectly reject this, because the final flower amounts are not a matching.

A more subtle case is

```
3 2
1 1
2 2
```

There is a matching containing both students, but teacher 3 has no incident edge. The correct output is `-1`. Thus finding a matching that covers every student is necessary but not sufficient.

Another subtle case occurs when a teacher is unmatched by the initial matching. That teacher is not a mistake in the matching. It is exactly the root from which we build the alternating structure used to construct all required flower distributions.

Finally, output values may legitimately be zero. For example, an allowed edge can receive no flowers because other allowed edges of the same student can carry the entire amount. Treating every input edge as requiring a positive value would reject valid solutions.

## Approaches

A direct approach is to build a flow network. Add a source connected to every student with capacity (N), connect every allowed student-teacher pair with effectively unlimited capacity, and connect every teacher to the sink with capacity (N-1). A flow of (N(N-1)) would be exactly the required answer.

This model is correct, but using a generic augmenting-path algorithm is far too slow. If we augment one flower at a time, there can be (N(N-1)) augmentations. Each search can inspect (O(M+N)) edges, giving (O(MN^2)) work, which is about (2\cdot10^{15}) edge inspections at the maximum constraints.

The useful observation is that the capacities have a very special relationship. Each student needs (N), while each teacher needs (N-1), and there is exactly one more teacher than student.

Suppose we temporarily restrict every allowed edge to carry at most one flower. A matching covering all (N-1) students gives every student one flower and gives (N-1) teachers one flower. Exactly one teacher remains unmatched.

Now imagine constructing one matching for every possible omitted teacher. If teacher (t) is omitted, we want a matching between all (N-1) students and the other (N-1) teachers. For every omitted teacher (t), give one flower along every edge of that matching.

There are (N) such matchings. Every student belongs to every matching, so each student receives exactly (N) flowers in total. A fixed teacher (t) belongs to all matchings except the one in which (t) was omitted, so that teacher receives exactly (N-1) flowers.

The remaining problem is to construct all these matchings without running a matching algorithm (N) times. Start with one matching that covers all students, leaving teacher (r) unmatched. Direct every unmatched edge from teacher to student and every matched edge from student to teacher. Starting at (r), follow this directed alternating graph.

Whenever we move

[
\text{teacher } a \rightarrow \text{student } s \rightarrow \text{teacher } b,
]

the first edge is not in the matching and the second edge is in the matching. Flipping those two edges changes which teacher is unmatched, moving the unmatched teacher from (a) to (b).

If every teacher is reachable from (r), a spanning tree of these alternating transitions gives a path from (r) to every teacher. Flipping the edges along that path produces the matching in which that destination teacher is unmatched. Thus all (N) matchings can be represented by one tree instead of being stored explicitly.

The reachability condition is also exactly what separates feasible and infeasible instances. The Hall condition for the original flower assignment reduces to the stronger requirement that after deleting any one teacher, the remaining graph still has a matching covering every student. This is precisely what the alternating reachability test checks. The intended solution uses maximum bipartite matching followed by this alternating construction, with (O(M\sqrt N)) matching time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force / unit-augmentation flow | (O(MN^2)) worst case | (O(N+M)) | Too slow |
| Optimal | (O(M\sqrt N)) | (O(N+M)) | Accepted |

## Algorithm Walkthrough

1. Build the bipartite graph using students on one side and teachers on the other. Keep the original edge index because the final answer has to be printed in input order.
2. Find a maximum bipartite matching using Hopcroft-Karp. We only need a matching of size (N-1), which means every student is matched. If the maximum matching has smaller size, no flower assignment can exist.
3. Let (r) be the unique teacher that is unmatched by this matching. Regard every nonmatching edge as directed from teacher to student, and every matching edge as directed from student to teacher.
4. Start a traversal at (r). When the traversal is at teacher (t), inspect every nonmatching edge (t-s). Student (s) has exactly one matching edge, say (s-u), so the alternating transition is (t\rightarrow s\rightarrow u). If (u) has not been reached yet, make it a child of (t) in the teacher tree.
5. If some teacher is never reached, print (-1). The unreachable part gives a Hall obstruction, so no valid flower assignment exists.
6. The traversal gives a tree whose vertices are the (N) teachers. Every non-root teacher (u) has a parent teacher (p), a nonmatching edge (p-s), and a matching edge (s-u). These two original edges form one alternating step in the tree.
7. Root the teacher tree at (r) and compute every subtree size. Let the subtree size of a non-root teacher (u) be (k). Exactly (k) of the (N) root-to-teacher paths contain the tree edge from (p) to (u).
8. Initially give every original matching edge (N) flowers and every other edge zero flowers. For the tree edge (p-s-u), change the amount on the nonmatching edge (p-s) to (k), and change the amount on the matching edge (s-u) to (N-k).

The reason for these two values is simple. For each target teacher in the subtree of (u), the path from (r) to that target flips this alternating pair. Thus the nonmatching edge is selected in exactly (k) of the (N) matchings, while the original matching edge is selected in the other (N-k) matchings.

### Why it works

The key invariant is that for every teacher (t), the unique path from the root (r) to (t) is an alternating path whose edges alternate between nonmatching and matching edges. Flipping that path preserves the matching property and changes the unmatched teacher from (r) to (t). Consequently, for every teacher (t), we obtain a matching containing every student and every teacher except (t).

Now sum the indicator of every edge over all (N) such matchings. Every student is matched once in every matching, giving it (N) flowers. Teacher (t) is absent from exactly one matching, giving it (N-1) flowers. Every used edge belongs to the original graph, and all amounts are nonnegative because a subtree size is between (1) and (N-1).

If the alternating traversal cannot reach some teacher, then the graph does not have the required matching after deleting that teacher. Hence the flower assignment is impossible. This establishes both directions of the construction.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

sys.setrecursionlimit(300000)

def solve(stream=None):
    if stream is None:
        stream = sys.stdin
    input = stream.readline

    N, M = map(int, input().split())

    # Edge i joins student S[i] with teacher T[i].
    S = [0] * M
    T = [0] * M

    # Adjacency by student, storing edge indices.
    adj = [[] for _ in range(N - 1)]

    for i in range(M):
        s, t = map(int, input().split())
        s -= 1
        t -= 1
        S[i] = s
        T[i] = t
        adj[s].append(i)

    left_n = N - 1
    right_n = N

    # pair_s[s] = teacher matched to student s, or -1.
    # pair_t[t] = student matched to teacher t, or -1.
    pair_s = [-1] * left_n
    pair_t = [-1] * right_n
    dist = [0] * left_n
    ptr = [0] * left_n

    # A greedy initial matching greatly reduces the number of
    # Hopcroft-Karp phases in practice.
    matching = 0
    for s in range(left_n):
        for eid in adj[s]:
            t = T[eid]
            if pair_t[t] == -1:
                pair_s[s] = t
                pair_t[t] = s
                matching += 1
                break

    def bfs():
        q = deque()
        for s in range(left_n):
            if pair_s[s] == -1:
                dist[s] = 0
                q.append(s)
            else:
                dist[s] = -1

        found = False

        while q:
            s = q.popleft()
            d = dist[s]

            for eid in adj[s]:
                t = T[eid]
                ns = pair_t[t]

                if ns == -1:
                    found = True
                elif dist[ns] == -1:
                    dist[ns] = d + 1
                    q.append(ns)

        return found

    def dfs(s):
        while ptr[s] < len(adj[s]):
            eid = adj[s][ptr[s]]
            ptr[s] += 1

            t = T[eid]
            ns = pair_t[t]

            if ns == -1 or (
                dist[ns] == dist[s] + 1 and dfs(ns)
            ):
                pair_s[s] = t
                pair_t[t] = s
                return True

        dist[s] = -1
        return False

    while bfs():
        for s in range(left_n):
            ptr[s] = 0

        for s in range(left_n):
            if pair_s[s] == -1 and dfs(s):
                matching += 1

    if matching != left_n:
        return "-1\n"

    # For every student, remember the edge used by the matching.
    match_edge = [-1] * left_n
    for s in range(left_n):
        t = pair_s[s]
        for eid in adj[s]:
            if T[eid] == t:
                match_edge[s] = eid
                break

    # Root is the unique unmatched teacher.
    root = -1
    for t in range(right_n):
        if pair_t[t] == -1:
            root = t
            break

    # Teacher-tree construction.
    #
    # parent[t] = parent teacher of t.
    # parent_student[t] is the student used in the alternating step.
    # parent_edge[t] is the nonmatching edge parent[t] -> parent_student[t].
    parent = [-1] * right_n
    parent_student = [-1] * right_n
    parent_edge = [-1] * right_n

    visited_teacher = [False] * right_n
    visited_student = [False] * left_n

    visited_teacher[root] = True
    stack = [root]

    while stack:
        t = stack.pop()

        # Inspect nonmatching edges from teacher t to students.
        for s in range(left_n):
            # This scan would be too slow, so this branch is replaced below.
            pass
        # The actual traversal is performed using a reverse adjacency list.
        break

    # Reverse adjacency by teacher, storing edge indices.
    by_teacher = [[] for _ in range(right_n)]
    for eid in range(M):
        by_teacher[T[eid]].append(eid)

    stack = [root]
    while stack:
        t = stack.pop()

        for eid in by_teacher[t]:
            s = S[eid]

            # Matching edges are directed student -> teacher,
            # so from a teacher we may only use nonmatching edges.
            if pair_s[s] == t:
                continue

            if visited_student[s]:
                continue

            visited_student[s] = True
            nt = pair_s[s]

            if nt == -1 or visited_teacher[nt]:
                continue

            visited_teacher[nt] = True
            parent[nt] = t
            parent_student[nt] = s
            parent_edge[nt] = eid
            stack.append(nt)

    if not all(visited_teacher):
        return "-1\n"

    # Build the teacher tree as an ordinary adjacency list.
    tree = [[] for _ in range(right_n)]
    for t in range(right_n):
        if t == root:
            continue
        p = parent[t]
        tree[p].append(t)

    # Compute subtree sizes iteratively.
    order = [root]
    for t in order:
        for child in tree[t]:
            order.append(child)

    subtree = [1] * right_n
    for t in reversed(order):
        if t != root:
            subtree[parent[t]] += subtree[t]

    # Start from the interpretation of the original matching:
    # every matching edge occurs in all N matchings.
    ans = [0] * M
    for s in range(left_n):
        ans[match_edge[s]] = N

    # Each teacher-tree edge represents an alternating pair:
    # nonmatching edge gets subtree size,
    # matching edge gets N - subtree size.
    for t in range(right_n):
        if t == root:
            continue

        k = subtree[t]
        s = parent_student[t]

        ans[parent_edge[t]] = k
        ans[match_edge[s]] = N - k

    return "".join(f"{x}\n" for x in ans)

if __name__ == "__main__":
    sys.stdout.write(solve())
```

The code first stores every input relation by student, which is the natural representation for Hopcroft-Karp. The edge index is kept separately so that the final amount can be written in exactly the input order.

The initial greedy matching is only an optimization. Hopcroft-Karp remains responsible for obtaining a maximum matching, so the greedy choice cannot affect correctness.

The matching arrays use `-1` as the unmatched value. After matching, every student has exactly one matched teacher, and exactly one teacher has no matched student because there are (N-1) students and (N) teachers.

The alternating traversal needs adjacency in the opposite direction, from teachers to edge indices, so `by_teacher` is built once in (O(M)). From a teacher we deliberately ignore its matching edge. A nonmatching edge leads to a student, and that student has exactly one matching edge leading to the next teacher in the tree.

The subtree sizes are computed without recursive tree DFS. This avoids Python recursion depth problems on a path containing (10^5) teachers.

The final formula uses `N - k`, not `N - 1 - k`. The original matching edge appears in every one of the (N) matchings before we flip paths. Exactly (k) of those paths contain this tree edge and remove that matching edge, leaving (N-k) occurrences.

The amount is always an integer between zero and (N), so Python's arbitrary-precision integers are more than sufficient.

One small implementation detail can be simplified further in a production submission: the first `while stack` loop in the code is intentionally harmless but unnecessary. The actual teacher traversal immediately follows after `by_teacher` is built. Removing that preliminary loop makes the submitted version cleaner.

Here is the cleaned version of the same solution.

```python
import sys
input = sys.stdin.readline
from collections import deque

sys.setrecursionlimit(300000)

def solve(stream=None):
    if stream is None:
        stream = sys.stdin
    input = stream.readline

    N, M = map(int, input().split())

    S = [0] * M
    T = [0] * M
    adj = [[] for _ in range(N - 1)]
    by_teacher = [[] for _ in range(N)]

    for i in range(M):
        s, t = map(int, input().split())
        s -= 1
        t -= 1
        S[i] = s
        T[i] = t
        adj[s].append(i)
        by_teacher[t].append(i)

    L = N - 1
    pair_s = [-1] * L
    pair_t = [-1] * N
    dist = [0] * L
    ptr = [0] * L

    matching = 0

    for s in range(L):
        for eid in adj[s]:
            t = T[eid]
            if pair_t[t] == -1:
                pair_s[s] = t
                pair_t[t] = s
                matching += 1
                break

    def bfs():
        q = deque()

        for s in range(L):
            if pair_s[s] == -1:
                dist[s] = 0
                q.append(s)
            else:
                dist[s] = -1

        found = False

        while q:
            s = q.popleft()
            d = dist[s]

            for eid in adj[s]:
                t = T[eid]
                ns = pair_t[t]

                if ns == -1:
                    found = True
                elif dist[ns] == -1:
                    dist[ns] = d + 1
                    q.append(ns)

        return found

    def dfs(s):
        while ptr[s] < len(adj[s]):
            eid = adj[s][ptr[s]]
            ptr[s] += 1

            t = T[eid]
            ns = pair_t[t]

            if ns == -1 or (
                dist[ns] == dist[s] + 1 and dfs(ns)
            ):
                pair_s[s] = t
                pair_t[t] = s
                return True

        dist[s] = -1
        return False

    while bfs():
        for s in range(L):
            ptr[s] = 0

        for s in range(L):
            if pair_s[s] == -1 and dfs(s):
                matching += 1

    if matching != L:
        return "-1\n"

    match_edge = [-1] * L
    for s in range(L):
        target = pair_s[s]
        for eid in adj[s]:
            if T[eid] == target:
                match_edge[s] = eid
                break

    root = pair_t.index(-1)

    parent = [-1] * N
    parent_student = [-1] * N
    parent_edge = [-1] * N
    visited = [False] * N

    visited[root] = True
    stack = [root]

    while stack:
        t = stack.pop()

        for eid in by_teacher[t]:
            s = S[eid]

            if pair_s[s] == t:
                continue

            nt = pair_s[s]

            if visited[nt]:
                continue

            visited[nt] = True
            parent[nt] = t
            parent_student[nt] = s
            parent_edge[nt] = eid
            stack.append(nt)

    if not all(visited):
        return "-1\n"

    tree = [[] for _ in range(N)]
    for t in range(N):
        if t != root:
            tree[parent[t]].append(t)

    order = [root]
    for t in order:
        order.extend(tree[t])

    subtree = [1] * N
    for t in reversed(order):
        if t != root:
            subtree[parent[t]] += subtree[t]

    ans = [0] * M

    for s in range(L):
        ans[match_edge[s]] = N

    for t in range(N):
        if t == root:
            continue

        k = subtree[t]
        s = parent_student[t]

        ans[parent_edge[t]] = k
        ans[match_edge[s]] = N - k

    return "".join(f"{x}\n" for x in ans)

if __name__ == "__main__":
    sys.stdout.write(solve())
```

## Worked Examples

### Sample 1

The sample has (N=6), so there are five students and six teachers. With the input order, a greedy matching can choose

[
1\rightarrow3,\quad
2\rightarrow2,\quad
3\rightarrow1,\quad
4\rightarrow4,\quad
5\rightarrow6.
]

Teacher 5 is unmatched, so it becomes the root.

The alternating traversal creates the teacher tree

[
5\rightarrow3\rightarrow1\rightarrow4,
]

with teacher 4 also having children 2 and 6. The resulting subtree sizes are shown below.

| Teacher | Parent | Student on transition | Subtree size |
| --- | --- | --- | --- |
| 5 | none | none | 6 |
| 3 | 5 | 1 | 5 |
| 1 | 3 | 3 | 4 |
| 4 | 1 | 4 | 3 |
| 2 | 4 | 2 | 1 |
| 6 | 4 | 5 | 1 |

For example, the tree transition (5\rightarrow1\rightarrow3) uses the nonmatching edge ((1,5)) and the matching edge ((1,3)). Since teacher 3 has subtree size 5, edge ((1,5)) receives 5 flowers and edge ((1,3)) receives (6-5=1).

The complete trace of the resulting edge values is:

| Input edge | Matching status | Tree subtree | Flowers |
| --- | --- | --- | --- |
| (1,3) | matching | 5 | 1 |
| (1,4) | non-tree | 0 | 0 |
| (1,5) | tree nonmatching | 5 | 5 |
| (2,2) | matching | 1 | 5 |
| (2,4) | tree nonmatching | 1 | 1 |
| (3,1) | matching | 4 | 2 |
| (3,3) | tree nonmatching | 4 | 4 |
| (4,1) | tree nonmatching | 3 | 3 |
| (4,2) | non-tree | 0 | 0 |
| (4,4) | matching | 3 | 3 |
| (5,4) | tree nonmatching | 1 | 1 |
| (5,6) | matching | 1 | 5 |

Every student receives (6) flowers. Every teacher receives (5). The values differ from the sample output, which is expected because the problem allows any valid construction.

### Sample 2

The second sample has the same (N=6), but student 5 can only reach teachers 5 and 6. A greedy matching can cover students 1, 2, 3 and 5, while student 4 cannot be matched.

| Student | Available teachers | Matching state |
| --- | --- | --- |
| 1 | 2, 3, 4 | matched |
| 2 | 2, 4 | matched |
| 3 | 1, 3 | matched |
| 4 | 1, 2, 4 | unmatched |
| 5 | 5, 6 | matched |

The maximum matching has size 4 instead of the required 5. Hopcroft-Karp consequently finishes without matching student 4, and the algorithm immediately prints (-1).

This demonstrates the first feasibility test. There is no reason to build the alternating tree when the graph cannot even provide one distinct teacher for every student.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(M\sqrt N)) | Hopcroft-Karp dominates; the alternating traversal, tree construction and subtree computation are all (O(N+M)) |
| Space | (O(N+M)) | Adjacency lists, matching arrays, tree arrays and answer storage |

The maximum matching is the only non-linear part. With (M\le2\cdot10^5) and (N\le10^5), the intended (O(M\sqrt N)) bound is roughly (6.3\cdot10^7) elementary edge-layer operations in the worst asymptotic estimate, while all construction work is linear. The memory usage is comfortably within the 1024 MB limit. The original contest discussion also identifies (O(E\sqrt V)) bipartite matching as the intended complexity.

## Test Cases

Because this is a special-judge problem, the exact valid output is not unique. The tests below validate the structural conditions instead of comparing against one particular output.

```python
# This test file assumes the solution above is available as:
# from solution import solve

import io
from solution import solve

def run(inp: str) -> str:
    return solve(io.StringIO(inp))

def validate(inp: str, out: str):
    data = list(map(int, inp.split()))
    n, m = data[0], data[1]

    edges = []
    pos = 2
    allowed = set()

    for _ in range(m):
        s = data[pos] - 1
        t = data[pos + 1] - 1
        pos += 2
        edges.append((s, t))
        allowed.add((s, t))

    out = out.strip()

    if out == "-1":
        return False

    values = list(map(int, out.split()))
    assert len(values) == m

    row = [0] * (n - 1)
    col = [0] * n

    for value, (s, t) in zip(values, edges):
        assert value >= 0
        row[s] += value
        col[t] += value

    assert row == [n] * (n - 1)
    assert col == [n - 1] * n

    return True

sample1 = """\
6 12
1 3
1 4
1 5
2 2
2 4
3 1
3 3
4 1
4 2
4 4
5 4
5 6
"""

sample2 = """\
6 12
1 2
1 3
1 4
2 2
2 4
3 1
3 3
4 1
4 2
4 4
5 5
5 6
"""

assert validate(sample1, run(sample1)), "sample 1"

assert run(sample2).strip() == "-1", "sample 2"

minimum = """\
2 2
1 1
1 2
"""
assert validate(minimum, run(minimum)), "minimum valid case"

disconnected = """\
3 2
1 1
2 2
"""
assert run(disconnected).strip() == "-1", "isolated teacher"

complete = """\
4 12
1 1
1 2
1 3
1 4
2 1
2 2
2 3
2 4
3 1
3 2
3 3
3 4
"""
assert validate(complete, run(complete)), "complete bipartite graph"

# Maximum-size edge count: N = 100000, M = 200000.
# Each student i connects to teachers i and i+1, then two
# additional legal edges make M exactly 200000.
n = 100000
lines = [f"{n} 200000"]

for i in range(1, n):
    lines.append(f"{i} {i}")
    lines.append(f"{i} {i + 1}")

lines.append("1 3")
lines.append("1 4")

maximum = "\n".join(lines) + "\n"
assert validate(maximum, run(maximum)), "maximum-size valid case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | Any valid (M)-line assignment | Full construction on a cyclic-looking graph |
| Sample 2 | `-1` | Failure to obtain a matching covering every student |
| (N=2), two edges | Any valid assignment | Minimum boundary case |
| (N=3), two disconnected edges | `-1` | A full student matching is not sufficient |
| Complete (K_{3,4}) | Any valid assignment | Dense graph and many possible solutions |
| (N=100000,\ M=200000) | Any valid assignment | Maximum-size input and long alternating tree |

## Edge Cases

The minimum case

```
2 2
1 1
1 2
```

has one student and two teachers. Hopcroft-Karp finds the matching student 1 to teacher 1, leaving teacher 2 as the root. The alternating traversal uses the edge to teacher 2 and the matching edge to teacher 1, creating a two-vertex teacher tree. The subtree size of teacher 1 is 1, so the matching edge gets (2-1=1) flower and the other edge gets 1 flower. Both teachers receive (N-1=1), and the student receives (N=2).

The isolated-teacher case

```
3 2
1 1
2 2
```

is more subtle. A maximum matching covers both students, but teacher 3 is unmatched and has no edge leading into the alternating traversal. The traversal reaches only teacher 3 itself, so not all teachers are visited. The algorithm prints (-1). This catches the common mistake of checking only whether all students can be matched.

An allowed edge receiving zero flowers is handled naturally. In Sample 1, the edge ((1,4)) can receive zero because student 1 already sends all six flowers through ((1,3)) and ((1,5)). The algorithm never assumes that an input edge must carry positive flow.

The case where many edges form cycles is also safe. The alternating traversal deliberately keeps only the first transition that reaches each teacher, producing a tree. Extra edges are left at zero unless they belong to the original matching. They are unnecessary because the tree already represents all (N) required matchings.

The maximum-size case has (N=100000) and (M=200000). A long chain of alternating transitions can contain almost all teachers, so recursive tree traversal would risk exceeding Python's recursion depth. The implementation computes the traversal order and subtree sizes iteratively, keeping the construction phase linear and safe for the boundary case.
