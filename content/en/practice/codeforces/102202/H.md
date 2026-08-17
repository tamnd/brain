---
title: "CF 102202H - Jealous Teachers"
description: "Think of the input as a bipartite graph. The left side contains the (N-1) students who are still at school, and the right side contains the (N) teachers. An edge ((s,t)) means student (s) is allowed to give flowers to teacher (t)."
date: "2026-08-18T01:19:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102202
codeforces_index: "H"
codeforces_contest_name: "2019 KAIST RUN Spring Contest"
rating: 0
weight: 102202
solve_time_s: 390
verified: true
draft: false
---

[CF 102202H - Jealous Teachers](https://codeforces.com/problemset/problem/102202/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

Think of the input as a bipartite graph. The left side contains the (N-1) students who are still at school, and the right side contains the (N) teachers. An edge ((s,t)) means student (s) is allowed to give flowers to teacher (t). Each student has exactly (N) flowers, while every teacher must receive exactly (N-1) flowers.

For every given edge, we have to output a nonnegative integer representing how many flowers travel through that edge. The sum of the values on edges incident to every student must be (N), and the sum on edges incident to every teacher must be (N-1). Edges that exist in the graph but receive zero flowers are completely valid.

The total supply is ((N-1)N), and the total demand is (N(N-1)), so the global totals agree automatically. The difficulty is entirely caused by the missing edges. This is a transportation problem on a sparse bipartite graph.

The constraints are large enough to rule out generic maximum flow. There can be (10^5) students and (2\cdot10^5) allowed pairs, so an (O(NM)) or worse algorithm is already too large. The intended solution reduces the expensive part to bipartite matching, which can be done in (O(M\sqrt N)), followed by only linear graph processing. The original contest solution also uses this matching-based construction rather than a general flow algorithm.

There are several edge cases where a seemingly reasonable construction fails. An isolated teacher immediately makes the answer impossible. For example,

```
2 1
1 1
```

has teacher 2 with no possible incoming edge, so the correct output is `-1`. A careless implementation that only checks whether every student has an available teacher could miss this.

An isolated student is equally fatal. For example,

```
3 1
1 1
```

leaves student 2 with nowhere to send his three flowers, so the correct output is `-1`.

A matching is necessary but not sufficient. For example, the second sample has a matching of size five, but the graph splits into a component containing student 5 and teachers 5 and 6, while the other students cannot interact with those teachers. The correct output is `-1`. A solution that stops immediately after finding a matching of size (N-1) silently accepts an invalid instance.

Finally, zero-flow edges must be allowed. In the first sample, many input pairs receive zero flowers in a valid solution. Treating every input edge as if it had to carry positive flow changes the problem and can incorrectly reject valid graphs.

## Approaches

The most direct approach is to model the problem as maximum flow. Add a source connected to every student with capacity (N), connect every allowed student-teacher pair with infinite capacity, and connect every teacher to the sink with capacity (N-1). A flow of (N(N-1)) is exactly the desired assignment.

This model is correct, but a deliberately naive Ford-Fulkerson implementation that augments one flower at a time can perform (N(N-1)) augmentations. Each augmentation may inspect (O(M+N)) graph edges, giving roughly

[
N(N-1)(M+2N)
]

edge inspections. At the maximum bounds this is on the order of (4\cdot10^{15}), far beyond the time limit. The official solution describes this maximum-flow formulation for the small subtask and gives (O(N^4)) there.

The useful observation comes from looking at a cut containing some subset (S) of students. Those students collectively own (N|S|) flowers. Only their neighboring teachers can receive them, and each such teacher can receive at most (N-1) flowers. Thus every nonempty student subset must have at least

[
N|S|\le (N-1)|N(S)|
]

neighboring teachers. Since (1\le |S|\le N-1), this inequality is equivalent to

[
|N(S)|\ge |S|+1.
]

That extra one teacher is the key structure of the problem. It is stronger than ordinary Hall's condition.

First find a matching that covers all (N-1) students. Exactly one teacher remains unmatched. Call that teacher the root. Now orient the bipartite graph in a special way. Every matching edge is directed from student to teacher, while every nonmatching edge is directed from teacher to student.

Starting from the unmatched teacher, perform a search using these directed edges. If every student is reached, the search edges form a tree connecting all (N) teachers. If some student cannot be reached, the required stronger Hall condition fails, so no flower assignment exists.

The remaining construction is surprisingly simple. In this tree, every student has exactly one child teacher, because its matching edge is directed from the student to that teacher. Every teacher except the root has exactly one parent student. Once we know the number of students in every subtree, the flower count on every tree edge follows directly from conservation.

The brute-force flow model works because it expresses exactly the required supply and demand. It fails because the total flow is quadratic in (N). The observation that the capacities differ by exactly one converts the feasibility question into a matching plus an alternating-tree problem, after which the actual flow values can be obtained from subtree sizes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N(N-1)(M+N))) for unit augmentations | (O(M+N)) | Too slow |
| Optimal | (O(M\sqrt N)) | (O(M+N)) | Accepted |

## Algorithm Walkthrough

1. Build the bipartite graph with students on the left and teachers on the right. Store the original input edge index together with every adjacency entry, because the final answer has to be printed in exactly the input order.
2. Find a maximum bipartite matching. We need all (N-1) students to be matched. If the matching contains fewer than (N-1) edges, immediately print `-1`.

The matching is necessary because any valid flower assignment satisfies the stronger Hall condition, and that condition in particular implies the ordinary Hall condition.

1. Find the unique unmatched teacher and use it as the root of the alternating search.
2. Direct every matching edge from its student to its matched teacher. Direct every nonmatching edge from its teacher to its student.

Starting from the unmatched teacher, follow these directions. Whenever a teacher reaches a previously unseen student, add that student to the tree. Immediately follow the student's matching edge to its matched teacher and add that teacher as well.

1. If the search reaches fewer than (N-1) students, print `-1`.

Suppose the search reaches a set of (k) students. It also reaches exactly (k+1) teachers, because the root teacher is initially present and every newly reached student introduces its unique matched teacher. If the graph has a valid assignment, the stronger Hall condition guarantees that every student can be reached from the unmatched teacher in this alternating graph. One way to see this is to compare the current matching with a matching that avoids the current student's matched teacher. Their symmetric difference contains an alternating path from the unmatched root to that student.

1. Treat the search edges as an ordinary rooted tree. Give every student node an initial subtree weight of (1), and every teacher node an initial subtree weight of (0). Process the tree in reverse order so that every node receives the total number of students in its subtree.
2. For a tree edge whose child is a student (s), assign

[
f = \operatorname{size}(s).
]

The edge connects that student to its parent teacher, so (f) is exactly the number of flowers that the whole student subtree must send upward.

1. For a tree edge whose child is a teacher (t), assign

[
f = N-1-\operatorname{size}(t).
]

Equivalently, if its parent student is (s),

[
f=N-\operatorname{size}(s).
]

All input edges that are not tree edges receive zero flowers.

1. Output the flow assigned to each original edge in input order.

### Why it works

The key invariant is that every student subtree contains equally many students and teachers, while every non-root teacher subtree contains exactly one more teacher than student. Consider a student (s). Its parent edge carries (\operatorname{size}(s)) flowers, and its child teacher edge carries (N-\operatorname{size}(s)) flowers. Their sum is exactly (N), so every student sends all of their flowers.

Now consider a non-root teacher (t). Let its subtree contain (k) students. Its parent student sends (N-1-k) flowers into (t), while the child student subtrees collectively send (k) flowers. The total is (N-1). The root has no parent edge, and its child student subtrees contain all (N-1) students, so it also receives exactly (N-1) flowers.

Every assigned value is nonnegative because a student subtree contains at most (N-1) students. All non-tree edges carry zero, so every original graph restriction is respected.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def hopcroft_karp(adj, n_left, n_right):
    pair_u = [-1] * n_left
    pair_v = [-1] * n_right
    dist = [-1] * n_left

    def bfs():
        q = deque()

        for u in range(n_left):
            if pair_u[u] == -1:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = -1

        found = False

        while q:
            u = q.popleft()

            for v in adj[u]:
                w = pair_v[v]

                if w == -1:
                    found = True
                elif dist[w] == -1:
                    dist[w] = dist[u] + 1
                    q.append(w)

        return found

    def dfs(start):
        stack = [start]
        chosen = []
        it = {}

        while stack:
            u = stack[-1]

            if u not in it:
                it[u] = 0

            i = it[u]

            while i < len(adj[u]):
                v = adj[u][i]
                i += 1
                it[u] = i

                w = pair_v[v]

                if w == -1:
                    pair_u[u] = v
                    pair_v[v] = u

                    for j in range(len(chosen) - 1, -1, -1):
                        left = stack[j]
                        right = chosen[j]
                        pair_u[left] = right
                        pair_v[right] = left

                    return True

                if dist[w] == dist[u] + 1:
                    stack.append(w)
                    chosen.append(v)
                    break
            else:
                dist[u] = -1
                stack.pop()
                if chosen:
                    chosen.pop()

        return False

    matching = 0

    while bfs():
        for u in range(n_left):
            if pair_u[u] == -1 and dfs(u):
                matching += 1

    return matching, pair_u, pair_v

def solve():
    n, m = map(int, input().split())
    left = n - 1

    adj = [[] for _ in range(left)]
    edges = []

    for idx in range(m):
        s, t = map(int, input().split())
        s -= 1
        t -= 1
        adj[s].append((t, idx))
        edges.append((s, t))

    # The matching algorithm only needs the teacher number.
    match_adj = [[t for t, _ in adj[s]] for s in range(left)]

    matching, pair_u, pair_v = hopcroft_karp(
        match_adj, left, n
    )

    if matching != left:
        print(-1)
        return

    # Find the original edge corresponding to every matching pair.
    match_edge = [-1] * left
    for s in range(left):
        mt = pair_u[s]
        for t, idx in adj[s]:
            if t == mt:
                match_edge[s] = idx
                break

    root = -1
    for t in range(n):
        if pair_v[t] == -1:
            root = t
            break

    # Nodes 0..n-1 are teachers.
    # Nodes n..n+left-1 are students.
    total_nodes = n + left
    parent = [-1] * total_nodes
    parent_edge = [-1] * total_nodes

    root_node = root
    parent[root_node] = root_node

    visited_students = [False] * left
    teacher_stack = [root_node]
    order = [root_node]

    while teacher_stack:
        tnode = teacher_stack.pop()
        t = tnode

        for s, idx in []:
            pass

        # Every adjacency entry is stored as (teacher, edge_index),
        # so scan all students that are adjacent to this teacher.
        # The graph is stored from students to teachers, therefore
        # build this reverse adjacency lazily once below.
        # This branch is intentionally replaced after reverse_adj exists.
        break

    # Reverse adjacency: teacher -> (student, original edge).
    reverse_adj = [[] for _ in range(n)]
    for s in range(left):
        for t, idx in adj[s]:
            reverse_adj[t].append((s, idx))

    # Restart the alternating-tree search.
    parent = [-1] * total_nodes
    parent_edge = [-1] * total_nodes
    parent[root_node] = root_node

    visited_students = [False] * left
    teacher_stack = [root_node]
    order = [root_node]

    while teacher_stack:
        t = teacher_stack.pop()

        for s, idx in reverse_adj[t]:
            # Matching edges point student -> teacher, so they cannot
            # be followed from a teacher.
            if pair_u[s] == t:
                continue

            if visited_students[s]:
                continue

            visited_students[s] = True

            snode = n + s
            parent[snode] = t
            parent_edge[snode] = idx
            order.append(snode)

            mt = pair_u[s]
            tchild = mt

            # A newly reached student's matched teacher is new as well.
            if parent[tchild] == -1:
                parent[tchild] = snode
                parent_edge[tchild] = match_edge[s]
                order.append(tchild)
                teacher_stack.append(tchild)

    if sum(visited_students) != left:
        print(-1)
        return

    # Count students in every subtree.
    size = [0] * total_nodes

    for node in range(n, total_nodes):
        size[node] = 1

    for node in reversed(order[1:]):
        size[parent[node]] += size[node]

    answer = [0] * m

    # Assign the flow on every tree edge.
    for node in order[1:]:
        idx = parent_edge[node]

        if node >= n:
            # Child is a student.
            answer[idx] = size[node]
        else:
            # Child is a teacher.
            answer[idx] = n - 1 - size[node]

    sys.stdout.write("\n".join(map(str, answer)))

if __name__ == "__main__":
    solve()
```

The input is stored twice conceptually. `adj` keeps the original student-to-teacher adjacency together with edge indices, while `reverse_adj` is created after matching so the alternating search can efficiently move from a teacher to its neighboring students.

The matching is computed only from teacher numbers. After the matching is known, each student's matching edge is recovered by scanning that student's adjacency list once. Since the total number of input pairs is (M), this recovery costs (O(M)).

The alternating tree uses `parent` to mark visited nodes. Teacher nodes occupy indices `0` through `N-1`, while student node (s) occupies `N+s`. This avoids allocating separate graph objects for the tree and makes the subtree computation straightforward.

The first exploratory loop before `reverse_adj` is unnecessary and should not be present in a polished implementation. The following cleaned-up version is the version to submit:

```python
import sys
from collections import deque

input = sys.stdin.readline

def hopcroft_karp(adj, n_left, n_right):
    pair_u = [-1] * n_left
    pair_v = [-1] * n_right
    dist = [-1] * n_left

    def bfs():
        q = deque()

        for u in range(n_left):
            if pair_u[u] == -1:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = -1

        found = False

        while q:
            u = q.popleft()

            for v in adj[u]:
                w = pair_v[v]
                if w == -1:
                    found = True
                elif dist[w] == -1:
                    dist[w] = dist[u] + 1
                    q.append(w)

        return found

    def dfs(start):
        stack = [start]
        chosen = []
        it = [0] * n_left

        while stack:
            u = stack[-1]

            while it[u] < len(adj[u]):
                v = adj[u][it[u]]
                it[u] += 1

                w = pair_v[v]

                if w == -1:
                    pair_u[u] = v
                    pair_v[v] = u

                    for j in range(len(chosen) - 1, -1, -1):
                        left = stack[j]
                        right = chosen[j]
                        pair_u[left] = right
                        pair_v[right] = left

                    return True

                if dist[w] == dist[u] + 1:
                    stack.append(w)
                    chosen.append(v)
                    break
            else:
                dist[u] = -1
                stack.pop()
                if chosen:
                    chosen.pop()

        return False

    matching = 0

    while bfs():
        for u in range(n_left):
            if pair_u[u] == -1 and dfs(u):
                matching += 1

    return matching, pair_u, pair_v

def solve():
    n, m = map(int, input().split())
    left = n - 1

    adj = [[] for _ in range(left)]
    reverse_adj = [[] for _ in range(n)]
    edges = [None] * m

    for idx in range(m):
        s, t = map(int, input().split())
        s -= 1
        t -= 1

        adj[s].append((t, idx))
        reverse_adj[t].append((s, idx))
        edges[idx] = (s, t)

    match_adj = [[t for t, _ in adj[s]] for s in range(left)]

    matching, pair_u, pair_v = hopcroft_karp(
        match_adj, left, n
    )

    if matching != left:
        print(-1)
        return

    match_edge = [-1] * left
    for s in range(left):
        mt = pair_u[s]
        for t, idx in adj[s]:
            if t == mt:
                match_edge[s] = idx
                break

    root = -1
    for t in range(n):
        if pair_v[t] == -1:
            root = t
            break

    total_nodes = n + left
    parent = [-1] * total_nodes
    parent_edge = [-1] * total_nodes

    parent[root] = root
    visited_student = [False] * left

    stack = [root]
    order = [root]

    while stack:
        t = stack.pop()

        for s, idx in reverse_adj[t]:
            if pair_u[s] == t:
                continue

            if visited_student[s]:
                continue

            visited_student[s] = True

            snode = n + s
            parent[snode] = t
            parent_edge[snode] = idx
            order.append(snode)

            mt = pair_u[s]
            parent[mt] = snode
            parent_edge[mt] = match_edge[s]
            order.append(mt)
            stack.append(mt)

    if not all(visited_student):
        print(-1)
        return

    size = [0] * total_nodes

    for s in range(left):
        size[n + s] = 1

    for node in reversed(order[1:]):
        size[parent[node]] += size[node]

    answer = [0] * m

    for node in order[1:]:
        idx = parent_edge[node]

        if node >= n:
            answer[idx] = size[node]
        else:
            answer[idx] = n - 1 - size[node]

    sys.stdout.write("\n".join(map(str, answer)))

if __name__ == "__main__":
    solve()
```

The second version removes the redundant initialization and is the actual submission version. The iterative DFS inside Hopcroft-Karp avoids Python recursion depth problems, which matter because the graph can contain (10^5) vertices on one side.

There is no integer overflow issue in Python. The largest flow value is (N-1), while subtree counts are at most (N-1). The only delicate boundary is the teacher-child formula, which is `n - 1 - size[node]`, not `n - size[node]`. A teacher subtree containing (k) students needs (N-1-k) flowers from its parent student.

## Worked Examples

### Sample 1

Use the following valid matching as a trace:

[
s_1\to t_5,\quad
s_2\to t_2,\quad
s_3\to t_3,\quad
s_4\to t_1,\quad
s_5\to t_6.
]

Teacher (t_4) is unmatched, so it becomes the root. The directed alternating tree is

[
t_4
\to s_1\to t_5,
\quad
t_4\to s_4\to t_1\to s_3\to t_3,
\quad
t_4\to s_5\to t_6,
\quad
t_4\to s_2\to t_2.
]

| Step | Current teacher | Newly reached student | Matched teacher | Student subtree size |
| --- | --- | --- | --- | --- |
| 1 | (t_4) | (s_1) | (t_5) | (1) |
| 2 | (t_4) | (s_4) | (t_1) | (2) |
| 3 | (t_4) | (s_5) | (t_6) | (1) |
| 4 | (t_4) | (s_2) | (t_2) | (1) |
| 5 | (t_1) | (s_3) | (t_3) | (1) |

The final subtree sizes are (1,2,1,1,1) for (s_1,s_4,s_5,s_2,s_3), respectively. The resulting nonzero tree flows are

| Edge | Child subtree size | Flowers |
| --- | --- | --- |
| (s_1,t_4) | (1) | (1) |
| (s_1,t_5) | (0) teacher subtree | (5) |
| (s_4,t_4) | (2) | (2) |
| (s_4,t_1) | (1) teacher subtree | (4) |
| (s_3,t_1) | (1) | (1) |
| (s_3,t_3) | (0) teacher subtree | (5) |
| (s_5,t_4) | (1) | (1) |
| (s_5,t_6) | (0) teacher subtree | (5) |
| (s_2,t_4) | (1) | (1) |
| (s_2,t_2) | (0) teacher subtree | (5) |

Every student gets total (6), and every teacher gets total (5). This demonstrates the subtree invariant directly.

### Sample 2

Choose a matching such as

[
s_1\to t_2,\quad
s_2\to t_4,\quad
s_3\to t_3,\quad
s_4\to t_1,\quad
s_5\to t_6.
]

Teacher (t_5) is unmatched and becomes the root.

| Step | Current teacher | Newly reached student | Matched teacher | Result |
| --- | --- | --- | --- | --- |
| 1 | (t_5) | (s_5) | (t_6) | (s_5) reached |
| 2 | (t_6) | none | none | search stops |
| 3 | unreachable teachers | (s_1,s_2,s_3,s_4) | various | never reached |

Only one student is reached, while four students remain outside the alternating tree. The construction consequently prints `-1`.

The reason is structural rather than an accident of the chosen matching. Students (s_1,s_2,s_3,s_4) and their teachers form a separate part of the graph, while (s_5) is confined to teachers (5) and (6). The extra teacher required by the strengthened Hall condition is missing for the larger student set.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(M\sqrt N)) | Hopcroft-Karp finds the matching; the remaining graph searches and subtree computation are linear |
| Space | (O(M+N)) | Adjacency lists, matching arrays, tree arrays, and the answer all have linear size |

With (N\le10^5) and (M\le2\cdot10^5), the linear part is easily small enough. The matching is the only non-linear component, and (O(M\sqrt N)) is the intended bound for this problem. The original contest discussion explicitly identifies (O(E\sqrt V)) bipartite matching as the intended approach.

## Test Cases

The output is not unique, so the test harness should validate an output rather than compare it against one particular assignment. The validator below checks that every printed value belongs to an input edge, every value is nonnegative, every student sends exactly (N) flowers, and every teacher receives exactly (N-1).

```python
# Run this block after defining solve() from the solution above.

import sys
import io
from contextlib import redirect_stdout

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    out = io.StringIO()
    with redirect_stdout(out):
        solve()

    sys.stdin = old_stdin
    return out.getvalue().strip()

def check_feasible(inp: str, out: str):
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    m = next(it)

    edges = []
    for _ in range(m):
        s = next(it) - 1
        t = next(it) - 1
        edges.append((s, t))

    assert out != "-1", "expected a feasible assignment"

    values = list(map(int, out.split()))
    assert len(values) == m

    student_sum = [0] * (n - 1)
    teacher_sum = [0] * n

    for value, (s, t) in zip(values, edges):
        assert value >= 0
        student_sum[s] += value
        teacher_sum[t] += value

    assert student_sum == [n] * (n - 1)
    assert teacher_sum == [n - 1] * n

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

check_feasible(sample1, run(sample1))
assert run(sample2) == "-1", "sample 2"

# Custom 1: minimum-size feasible instance.
case1 = """\
2 2
1 1
1 2
"""
check_feasible(case1, run(case1))

# Custom 2: minimum-size impossible instance because one teacher is isolated.
case2 = """\
2 1
1 1
"""
assert run(case2) == "-1", "isolated teacher"

# Custom 3: a chain-like instance that exercises nested subtree sizes.
case3 = """\
3 4
1 1
1 2
2 2
2 3
"""
check_feasible(case3, run(case3))

# Custom 4: maximum-size boundary test.
# N = 100000, M = 199998. Student i can use teachers i and i+1.
n = 100000
lines = [f"{n} {2 * (n - 1)}"]
for s in range(1, n):
    lines.append(f"{s} {s}")
    lines.append(f"{s} {s + 1}")
case4 = "\n".join(lines)

check_feasible(case4, run(case4))

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | Any valid assignment with 12 values | Normal feasible construction and subtree flows |
| Sample 2 | `-1` | A graph with a matching but no valid flower assignment |
| `2 2 / 1 1 / 1 2` | One flower on each edge | Minimum feasible (N=2) case |
| `2 1 / 1 1` | `-1` | Isolated teacher and boundary handling |
| `3 4 / 1 1 / 1 2 / 2 2 / 2 3` | Any valid assignment | Nested alternating tree and off-by-one in teacher flow |
| Generated (N=100000) chain | Any valid assignment with 199998 values | Maximum (N), maximum sparse scale, and performance |

## Edge Cases

An isolated teacher is handled during the alternating search because that teacher can only be the root if it is the unique unmatched teacher. If another teacher is isolated, no matching can cover all students while the alternating tree reaches every teacher. For

```
2 1
1 1
```

the matching covers student 1 with teacher 1, leaving teacher 2 as root. The root has no outgoing nonmatching edge, so student 1 is never reached. The algorithm prints `-1`.

An isolated student is rejected even earlier. With

```
3 1
1 1
```

the matching size is only one, while there are two students. Since the matching does not cover all students, the algorithm prints `-1` before constructing the alternating tree.

A matching that covers every student can still be insufficient. In Sample 2, the matching has size five, but choosing the unmatched teacher as the root only reaches the component containing student 5. The search reaches one student instead of all five, so the algorithm rejects the graph. This is exactly the additional condition beyond ordinary Hall matching.

The minimum feasible case

```
2 2
1 1
1 2
```

has one student with two available teachers. The only possible assignment is one flower to each teacher. The matching leaves one teacher unmatched, the root reaches the student through the nonmatching edge, and the two tree edges both receive one flower. The formula uses `N - 1 - size[teacher_subtree] = 1`.

The chain case

```
3 4
1 1
1 2
2 2
2 3
```

is useful because the tree is nested rather than a star. The root teacher reaches student 2, whose matched teacher reaches student 1, whose matched teacher is a leaf. The student subtree sizes become (2) for student 2 and (1) for student 1. Consequently the root-to-student edge gets (2) flowers, student 2 sends (1) flower to its matched teacher, and student 1 sends (2) flowers to its matched teacher. Each student sends exactly (3), while each teacher receives exactly (2).

Zero-flow edges need no special treatment. Once the alternating tree is selected, every input edge outside that tree simply remains zero. The construction never tries to force positive flow through an edge merely because it exists.

The maximum-size case stresses the matching implementation and the linear construction simultaneously. With (N=100000) and (M=199998), the graph

```
s -> t_s
s -> t_{s+1}
```

for (1\le s<N) forms a long chain. The iterative matching and tree traversals avoid recursion depth failures, and the subtree computation remains linear in the number of vertices and edges.
