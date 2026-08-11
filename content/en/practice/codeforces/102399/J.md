---
title: "CF 102399J - \u041a\u043e\u043d\u043a\u0443\u0440\u0441 \u043a\u043e\u0442\u0438\u043a\u043e\u0432"
description: "There are (n) residents and (n) cats. Resident (i) owns cat (i). Each acquaintance relation is represented by a directed edge from resident (a) to cat (b), meaning that resident (a) knows cat (b). Every resident knows their own cat, so every vertex has a self-loop."
date: "2026-08-11T16:00:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102399
codeforces_index: "J"
codeforces_contest_name: "2019 \u041c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432, \u043b\u0438\u0433\u0430 A"
rating: 0
weight: 102399
solve_time_s: 227
verified: false
draft: false
---

[CF 102399J - \u041a\u043e\u043d\u043a\u0443\u0440\u0441 \u043a\u043e\u0442\u0438\u043a\u043e\u0432](https://codeforces.com/problemset/problem/102399/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 47s  
**Verified:** no  

## Solution
## Problem Understanding

There are (n) residents and (n) cats. Resident (i) owns cat (i). Each acquaintance relation is represented by a directed edge from resident (a) to cat (b), meaning that resident (a) knows cat (b). Every resident knows their own cat, so every vertex has a self-loop.

We need to split the (n) indices into two nonempty sets. The first set becomes the jury, meaning those indices are taken as residents. The second set becomes the participants, meaning those indices are taken as cats. The sizes must add up to (n), so every index must belong to exactly one of the two sets. A jury resident must not know any participating cat.

The last condition has a useful graph interpretation. Suppose index (a) is assigned to the jury and there is an edge (a \to b). Then cat (b) cannot be a participant, so (b) must also belong to the jury. Thus, whenever a vertex is put into the jury, every vertex reachable by one outgoing edge must be put there too. The jury is a nonempty proper subset closed under outgoing edges.

The constraints strongly suggest a linear graph algorithm. There can be up to (10^6) vertices and (10^6) acquaintance edges over all tests. Even (O(n^2)) is far too large, while (O(n+m)) is appropriate. The large number of test cases also means the implementation should process each edge only a constant number of times and use iterative graph traversal rather than recursive DFS, because a graph with (10^6) vertices can easily exceed Python's recursion limit and create excessive call-stack overhead.

There are several edge cases that can fool a careless construction.

For (n=1), the only possible partition would have either no jury member or no participant. The required output is `No`.

```
1
1 1
1 1
```

A construction that blindly chooses a reachable or unreachable set can accidentally produce an empty side.

For a graph that is not strongly connected, the answer does exist even if there are many edges. For example,

```
2
2 3
1 1
2 2
1 2
```

The answer can be jury ({2}) and participant cat ({1}). Resident 2 knows only cat 2, so the cross-condition is satisfied. A careless approach that insists on finding vertices with zero degree would miss this, because both vertices have outgoing edges.

The direction of the graph also matters. Consider

```
3
3 4
1 1
2 2
3 3
2 1
```

Here jury ({1}) works, because resident 1 knows only cat 1. The set of vertices that cannot reach vertex 1 is ({2,3}), which also forms a valid jury. An implementation that treats acquaintance as an undirected relation would incorrectly conclude that vertices 1 and 2 must be on the same side, even though the condition only forbids an edge from a jury resident to a participant cat.

Finally, if every vertex can reach every other vertex, no solution exists. For example,

```
2
2 4
1 1
1 2
2 1
2 2
```

Putting either vertex into the jury forces the other vertex into the jury through reachability. Hence every nonempty closed set is the whole graph, leaving no participant.

## Approaches

A direct brute-force approach would enumerate every possible jury subset. There are (2^n) subsets, and the empty set and the full set are invalid, leaving (2^n-2) candidates. For every candidate we could scan all (m) acquaintance edges and reject it if some edge starts in the jury and ends outside it. This is correct because every possible partition is examined, but its worst-case work is ((2^n-2)m), which is already enormous for (n=30), let alone (n=10^6).

The brute-force works because the only real choice is which indices belong to the jury. The key is to understand what makes a chosen subset valid. If (a) is in the jury and there is an edge (a\to b), then (b) must also be in the jury. Repeating this argument shows that the jury must contain every vertex reachable from any jury vertex. In graph terminology, we need a nonempty proper set closed under outgoing edges.

This immediately connects the problem to reachability. Start from vertex 1. If some vertices cannot be reached from 1, take all such unreachable vertices as the jury. This set is closed under outgoing edges: if an unreachable vertex had an edge to a reachable vertex, then it would itself be reachable.

What if every vertex is reachable from 1? We then perform the same idea in the reversed graph. If some vertex cannot be reached from 1 in the reversed graph, that means the corresponding vertex cannot reach 1 in the original graph. Take all such vertices as the jury. This set is again closed under outgoing edges. If every vertex is also reachable from 1 in the reversed graph, then every vertex can reach 1 and 1 can reach every vertex, so the graph is strongly connected. In a strongly connected graph, every nonempty outgoing-closed set must contain all vertices, making a valid partition impossible.

The two traversals therefore distinguish exactly the two cases we need.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^n m)) | (O(n+m)) | Too slow |
| Optimal | (O(n+m)) | (O(n+m)) | Accepted |

## Algorithm Walkthrough

1. Treat every index (1,\ldots,n) as a graph vertex. For every acquaintance pair ((a,b)), add a directed edge (a\to b). The direction represents exactly the forbidden situation: a jury vertex (a) cannot have an outgoing edge to a participant vertex (b).
2. Run a DFS or BFS from vertex (1) in the original graph and mark every reachable vertex. If some vertices remain unvisited, put exactly those vertices into the jury and put every other vertex into the participant set. This is the first useful case because an edge cannot leave the unreachable set and enter the reachable set.
3. If every vertex was reached, construct the reversed graph and run a traversal from vertex (1) there. Reaching (v) in the reversed graph is equivalent to saying that (v) can reach (1) in the original graph.
4. If some vertices remain unreachable in the reversed graph, put those vertices into the jury and all other vertices into the participant set. This set is closed under original outgoing edges. Suppose (v) is in it and (v\to u). If (u) could reach (1), then (v) could reach (u) and then (1), contradicting that (v) was unreachable from (1) in the reversed graph.
5. If the second traversal also reaches every vertex, output `No`. At this point vertex 1 can reach every vertex, and every vertex can reach vertex 1. Consequently, every pair of vertices can reach each other, so the graph is strongly connected.
6. For a successful case, output the vertices in the chosen closed set as jury residents and its complement as participant cats. The two sets partition all (n) indices, so their sizes automatically sum to (n). Since a successful traversal left at least one vertex outside the chosen set, both sides are nonempty.

### Why it works

The central invariant is that the jury must be closed under outgoing edges. The first traversal constructs such a set from vertices that cannot be reached from 1. The second traversal constructs such a set from vertices that cannot reach 1. In either case, an outgoing edge from the chosen set cannot enter its complement, so no jury resident knows a participating cat.

If both traversals reach every vertex, the graph is strongly connected. Take any nonempty jury set and choose one vertex (v) in it. Since the graph is strongly connected, every vertex is reachable from (v). Closure under outgoing edges consequently forces every vertex into the jury. The jury would then contain all (n) vertices and there would be no participant, which is forbidden. Thus `No` is correct exactly in the strongly connected case.

## Python Solution

```python
import sys
input = sys.stdin.readline

def traverse(graph, start):
    n = len(graph)
    seen = bytearray(n)
    seen[start] = 1
    stack = [start]

    while stack:
        v = stack.pop()
        for u in graph[v]:
            if not seen[u]:
                seen[u] = 1
                stack.append(u)

    return seen

def solve():
    t = int(input())
    answer = []

    for _ in range(t):
        line = input()
        while not line.strip():
            line = input()

        n, m = map(int, line.split())

        graph = [[] for _ in range(n)]
        rev = [[] for _ in range(n)]

        for _ in range(m):
            a, b = map(int, input().split())
            a -= 1
            b -= 1
            graph[a].append(b)
            rev[b].append(a)

        reachable = traverse(graph, 0)

        if not all(reachable):
            jury = [i + 1 for i in range(n) if not reachable[i]]
            participants = [i + 1 for i in range(n) if reachable[i]]

            answer.append("Yes")
            answer.append(f"{len(jury)} {len(participants)}")
            answer.append(" ".join(map(str, jury)))
            answer.append(" ".join(map(str, participants)))
            continue

        can_reach_one = traverse(rev, 0)

        if not all(can_reach_one):
            jury = [i + 1 for i in range(n) if not can_reach_one[i]]
            participants = [i + 1 for i in range(n) if can_reach_one[i]]

            answer.append("Yes")
            answer.append(f"{len(jury)} {len(participants)}")
            answer.append(" ".join(map(str, jury)))
            answer.append(" ".join(map(str, participants)))
        else:
            answer.append("No")

    sys.stdout.write("\n".join(answer))

if __name__ == "__main__":
    solve()
```

The adjacency list `graph` represents resident-to-cat acquaintance edges. The reverse list `rev` contains exactly the opposite edges, which lets the second traversal answer the question "which vertices can reach vertex 1?" without running a separate search from every vertex.

The traversal uses a `bytearray` instead of a Python list of booleans. With up to (10^6) vertices, this substantially reduces memory consumption. The stack is also iterative, avoiding recursion depth problems on long chains.

The first search checks whether every vertex is reachable from vertex 1. When some vertex is unreachable, the code selects precisely the unreachable vertices as the jury. The condition `if not reachable[i]` is the important boundary choice: vertex 1 itself belongs to the complement in this case, while every unreachable vertex belongs to the jury.

The second search uses `rev`. A vertex is marked there exactly when it can reach vertex 1 in the original graph. Consequently, selecting `not can_reach_one[i]` gives the second possible closed set.

No integer can overflow because Python integers are arbitrary precision, and all indices are converted to zero-based form only inside the implementation. The input guarantees that acquaintance pairs are unique, so there is no need to remove duplicate edges.

The blank line separating test cases is handled by skipping empty lines before reading (n) and (m). Output is accumulated and written once, which is considerably faster than repeatedly calling `print` for potentially millions of indices.

## Worked Examples

Consider the first test case from the sample.

```
3 4
1 1
2 2
3 3
1 3
```

The directed edges are (1\to1), (2\to2), (3\to3), and (1\to3).

| Step | Start vertex | Reachable vertices | Unreachable vertices | Action |
| --- | --- | --- | --- | --- |
| Original DFS | 1 | ({1,3}) | ({2}) | Jury = ({2}) |
| Output |  | Jury ({2}) | Participants ({1,3}) | `Yes` |

The set ({2}) is closed because its only outgoing edge is (2\to2). The participant cats are 1 and 3, and resident 2 knows neither of them. This gives a valid partition with sizes (1+2=3).

Now consider the second sample test.

```
3 7
1 1
1 2
1 3
2 2
3 1
3 2
3 3
```

The graph has edges from 1 to every vertex, from 3 to every vertex except 3 itself is also present, and vertex 2 has only its self-loop.

| Step | Start vertex | Reachable vertices | Unreachable vertices | Action |
| --- | --- | --- | --- | --- |
| Original DFS | 1 | ({1,2,3}) | (\varnothing) | Continue |
| Reverse DFS | 1 | ({1,3}) | ({2}) | Jury = ({2}) |
| Output |  | Jury ({2}) | Participants ({1,3}) | `Yes` |

In the original graph, every vertex is reachable from 1, so the first construction cannot give a nonempty jury. In the reversed graph, vertex 2 cannot be reached from 1, which means vertex 2 cannot reach 1 in the original graph. Selecting vertex 2 as the jury works because its only outgoing edge is the self-loop (2\to2).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+m)) | Each graph edge is examined at most once in each of the two traversals. |
| Space | (O(n+m)) | The original and reversed adjacency lists store (2m) directed entries, plus traversal state. |

Across all test cases, the sums of (n) and (m) are at most (10^6). Thus the total number of graph operations is linear in roughly (2\cdot10^6) vertices and (2\cdot10^6) edge entries, which is appropriate for the given limits. The iterative traversal also avoids Python recursion overhead and recursion-depth failures.

## Test Cases

Because the problem accepts any valid partition, an exact output string is not a suitable assertion. The test harness below instead validates the actual output: it checks the sizes, verifies that both sets form a partition, and checks every acquaintance edge against the jury and participant sets.

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    try:
        t = int(sys.stdin.readline())
        answer = []

        def traverse(graph, start):
            n = len(graph)
            seen = bytearray(n)
            seen[start] = 1
            stack = [start]

            while stack:
                v = stack.pop()
                for u in graph[v]:
                    if not seen[u]:
                        seen[u] = 1
                        stack.append(u)

            return seen

        for _ in range(t):
            line = sys.stdin.readline()
            while not line.strip():
                line = sys.stdin.readline()

            n, m = map(int, line.split())
            graph = [[] for _ in range(n)]
            rev = [[] for _ in range(n)]

            edges = []

            for _ in range(m):
                a, b = map(int, sys.stdin.readline().split())
                a -= 1
                b -= 1
                graph[a].append(b)
                rev[b].append(a)
                edges.append((a, b))

            first = traverse(graph, 0)

            if not all(first):
                jury = [i + 1 for i in range(n) if not first[i]]
                participants = [i + 1 for i in range(n) if first[i]]

                answer.append("Yes")
                answer.append(f"{len(jury)} {len(participants)}")
                answer.append(" ".join(map(str, jury)))
                answer.append(" ".join(map(str, participants)))
            else:
                second = traverse(rev, 0)

                if not all(second):
                    jury = [i + 1 for i in range(n) if not second[i]]
                    participants = [i + 1 for i in range(n) if second[i]]

                    answer.append("Yes")
                    answer.append(f"{len(jury)} {len(participants)}")
                    answer.append(" ".join(map(str, jury)))
                    answer.append(" ".join(map(str, participants)))
                else:
                    answer.append("No")

        return out.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def validate(inp: str, out: str) -> bool:
    data = inp.split()
    pos = 0
    t = int(data[pos])
    pos += 1

    cases = []

    for _ in range(t):
        n = int(data[pos])
        m = int(data[pos + 1])
        pos += 2

        edges = []
        for _ in range(m):
            a = int(data[pos])
            b = int(data[pos + 1])
            pos += 2
            edges.append((a, b))

        cases.append((n, edges))

    tokens = out.split()
    pos = 0

    for n, edges in cases:
        if pos >= len(tokens):
            return False

        verdict = tokens[pos]
        pos += 1

        if verdict == "No":
            continue

        if verdict != "Yes" or pos + 2 > len(tokens):
            return False

        j = int(tokens[pos])
        p = int(tokens[pos + 1])
        pos += 2

        if j <= 0 or p <= 0 or j + p != n:
            return False

        if pos + j + p > len(tokens):
            return False

        jury = list(map(int, tokens[pos:pos + j]))
        pos += j

        participants = list(map(int, tokens[pos:pos + p]))
        pos += p

        if len(set(jury)) != j or len(set(participants)) != p:
            return False

        if any(x < 1 or x > n for x in jury + participants):
            return False

        jury_set = set(jury)
        participant_set = set(participants)

        if jury_set & participant_set:
            return False

        if len(jury_set | participant_set) != n:
            return False

        for a, b in edges:
            if a in jury_set and b in participant_set:
                return False

    return pos == len(tokens)

sample = """\
4
3 4
1 1
2 2
3 3
1 3

3 7
1 1
1 2
1 3
2 2
3 1
3 2
3 3

1 1
1 1

2 4
1 1
1 2
2 1
2 2
"""

assert validate(sample, solve_data(sample)), "provided sample"

minimum = """\
1
1 1
1 1
"""

assert solve_data(minimum).strip() == "No", "minimum-size case"

all_self = """\
1
4 4
1 1
2 2
3 3
4 4
"""

assert validate(all_self, solve_data(all_self)), "all-self edges"

chain = """\
1
4 7
1 1
2 2
3 3
4 4
1 2
2 3
3 4
"""

assert validate(chain, solve_data(chain)), "directed chain"

strongly_connected = """\
1
3 6
1 1
2 2
3 3
1 2
2 3
3 1
"""

assert solve_data(strongly_connected).strip() == "No", "strongly connected graph"

boundary = """\
1
2 3
1 1
2 2
1 2
"""

assert validate(boundary, solve_data(boundary)), "two-vertex boundary case"

large_self_loop_case = "1\n100000 100000\n" + "".join(
    f"{i} {i}\n" for i in range(1, 100001)
)

assert validate(
    large_self_loop_case,
    solve_data(large_self_loop_case)
), "large linear-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1 / 1 1` | `No` | The smallest possible graph cannot split into two nonempty sides. |
| Four self-loops | `Yes` | Vertices with only self-edges can be divided arbitrarily into two nonempty groups. |
| Directed chain | `Yes` | Checks that the selected set must be closed under outgoing edges. |
| Three-cycle with self-loops | `No` | Detects a strongly connected graph correctly. |
| Two vertices with (1\to2) | `Yes` | Checks the smallest nontrivial directed implication and boundary indexing. |
| (100000) self-loops | `Yes` | Exercises linear memory and time behavior on a large input. |

## Edge Cases

For the minimum case,

```
1
1 1
1 1
```

the first traversal reaches vertex 1, so there is no unreachable vertex. The reversed traversal also reaches vertex 1. The graph is strongly connected, which means the algorithm prints `No`. This avoids the common mistake of printing a one-element jury or participant set while leaving the other side empty.

For a graph consisting only of self-loops,

```
1
4 4
1 1
2 2
3 3
4 4
```

the first traversal from vertex 1 reaches only vertex 1. Vertices 2, 3, and 4 are unreachable, so the algorithm chooses ({2,3,4}) as the jury and ({1}) as the participant set. Every jury vertex knows only its own cat, which is also a jury index, so there is no forbidden jury-to-participant edge.

For a directed chain,

```
1
4 7
1 1
2 2
3 3
4 4
1 2
2 3
3 4
```

the first traversal from 1 reaches all four vertices, so it cannot directly provide a closed unreachable set. In the reversed graph, vertex 1 is reachable from every vertex because the original chain leads toward 4 rather than toward 1. Thus the reverse traversal reaches only vertex 1, leaving ({2,3,4}) as the jury. This set is closed under the original edges because (2\to3) and (3\to4) stay inside it.

For the strongly connected case,

```
1
3 6
1 1
2 2
3 3
1 2
2 3
3 1
```

the original traversal from 1 reaches all vertices. The reversed graph also lets 1 reach all vertices, because the original cycle allows every vertex to reach 1. The algorithm prints `No`. Any nonempty jury would force the entire cycle into the jury, leaving no participant cat.

For the two-vertex boundary case,

```
1
2 3
1 1
2 2
1 2
```

the first traversal reaches both vertices. In the reversed graph, vertex 1 reaches only itself, because the original edge (1\to2) becomes (2\to1). The algorithm therefore chooses vertex 2 as the jury and vertex 1 as the participant. Resident 2 knows only cat 2, so the construction is valid. This case is especially useful for catching an off-by-one error in the conversion between one-based input labels and zero-based Python arrays.
