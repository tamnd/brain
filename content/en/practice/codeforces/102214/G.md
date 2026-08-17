---
title: "CF 102214G - Words"
description: "The game can be modeled as a directed graph. Each letter is a vertex, and every word is a directed edge from its first letter to its last letter."
date: "2026-08-18T00:14:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102214
codeforces_index: "G"
codeforces_contest_name: "\u041e\u0442\u043a\u0440\u044b\u0442\u043e\u0435 \u043b\u0438\u0447\u043d\u043e\u0435 \u043f\u0435\u0440\u0432\u0435\u043d\u0441\u0442\u0432\u043e \u0418\u041a\u0418\u0422 \u0421\u0424\u0423 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2015"
rating: 0
weight: 102214
solve_time_s: 97
verified: true
draft: false
---

[CF 102214G - Words](https://codeforces.com/problemset/problem/102214/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

The game can be modeled as a directed graph. Each letter is a vertex, and every word is a directed edge from its first letter to its last letter. If a player has just said a word represented by the edge (u \to v), the next word must start at (v), so the next edge must leave vertex (v).

The task is to add as few new words, hence as few directed edges, as possible so that from every existing word we can eventually reach every other word through valid game moves. The input contains up to (N,M\le 100000), where (N) is the alphabet size and (M) is the number of existing words. The official limits are 2 seconds and 256 MB. A quadratic algorithm would already require around (10^{10}) operations at the upper bound, so the solution must be essentially linear or (O((N+M)\log N)).

There is one subtle modeling issue: letters that occur in no word should not participate in the answer. For example,

```
5 1
1 2
```

has answer `1`. We only need to add `2 -> 1`. A careless implementation that creates SCCs for all five letters and counts the three isolated letters as components needing connections would produce a larger answer.

Another edge case is a graph that is already strongly connected. For example,

```
3 3
1 2
2 3
3 1
```

has answer `0`. There is already a valid route from every word to every other word. An implementation that blindly applies the usual source/sink formula without checking whether there is only one SCC would incorrectly return `1`.

A self-loop also deserves attention. For

```
1 1
1 1
```

the answer is `0`. The single word can only be followed by another word beginning with letter 1, and the same letter is both its beginning and end. Since there is only one active SCC, no new word is required.

Finally, several words can have the same pair of endpoint letters. They are different words in the game, but for reachability they behave identically as graph edges. The SCC computation only needs the existence of an edge between two letters, so duplicate edges do not change the component structure.

## Approaches

A direct approach would try adding possible words until the resulting graph becomes strongly connected. There are (N^2) possible ordered pairs of letters, so there are already (2^{N^2}) possible subsets of candidate words. For every candidate subset we would have to build the resulting graph and check reachability, requiring (O(N+M+N^2)) work in the worst case. The resulting worst-case operation count is (O(2^{N^2}(N+M+N^2))), which is completely infeasible even for very small alphabets. The brute force is conceptually correct because it tests exactly the property required by the game, but it ignores the structure of directed graphs.

The key observation is that the game condition is equivalent to strong connectivity of the graph formed by the letters that actually occur in words. Suppose there is a path from the last letter of word (A) to the first letter of word (B). We can play (A), follow that path using intermediate words, and eventually play (B). Thus every word can reach every other word exactly when every active letter can reach every other active letter.

Once the problem is phrased this way, strongly connected components give the whole structure. Inside one SCC, every vertex can reach every other vertex. After contracting every SCC into one vertex, the resulting condensation graph is a DAG. If it has more than one component, every source component needs an incoming edge, and every sink component needs an outgoing edge. Adding directed edges between components can repair both requirements.

Let (S) be the number of source SCCs and (T) the number of sink SCCs. At least (S) new words are necessary because one added word has only one starting point and therefore can provide an incoming edge to at most one source SCC. Similarly, at least (T) new words are necessary because one added word can leave at most one sink SCC. Hence at least (\max(S,T)) words are necessary.

That lower bound is also achievable. We can connect sink components to source components cyclically, reusing a source or sink when their counts differ. With (K=\max(S,T)) added edges, every source receives an incoming edge and every sink receives an outgoing edge, and the resulting condensation graph becomes strongly connected. So the answer is exactly (\max(S,T)), except that a graph with only one active SCC already needs zero added words.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^{N^2}(N+M+N^2))) | (O(N^2+N+M)) | Too slow |
| SCC condensation | (O(N+M)) | (O(N+M)) | Accepted |

## Algorithm Walkthrough

1. Build a directed graph using the letters as vertices and the words as edges. Also build the reversed graph. We only need vertices that occur as the first or last letter of some word, because isolated letters cannot affect transitions between words.
2. Find all strongly connected components with Kosaraju's algorithm. The first DFS records vertices in finishing order, and the second DFS on the reversed graph assigns component identifiers in reverse finishing order.
3. If all active vertices belong to one SCC, output `0`. Every word can already reach every other word.
4. For every original edge (u\to v), compare the SCC identifiers of (u) and (v). If they differ, this is an edge between two vertices of the condensation DAG. Increase the indegree of the destination SCC and the outdegree of the source SCC.
5. Count the SCCs with zero indegree and the SCCs with zero outdegree. These are the source and sink components of the condensation graph.
6. Output the larger of those two counts. This is the minimum number of new words required because every source needs an incoming connection and every sink needs an outgoing connection, while the cyclic construction described above achieves both requirements with exactly that many edges.

### Why it works

After contracting SCCs, every remaining edge goes between different components and the resulting graph is a DAG. A source component has no incoming path from another component, so at least one newly added word must enter it. Likewise, a sink component cannot reach another component, so at least one newly added word must leave it. Thus any valid solution needs at least (\max(S,T)) new words.

Conversely, take the sink SCCs and source SCCs and connect them cyclically. If one side has fewer components, reuse components from that side when necessary. Every source then receives an incoming edge, every sink receives an outgoing edge, and following the cyclic connections lets us move from every SCC to every other SCC. Since each SCC was already internally strongly connected, the entire graph becomes strongly connected. The lower bound is achievable, so (\max(S,T)) is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    graph = [[] for _ in range(n)]
    rev = [[] for _ in range(n)]
    edges = []
    active = [False] * n

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1

        graph[u].append(v)
        rev[v].append(u)
        edges.append((u, v))

        active[u] = True
        active[v] = True

    # First pass of Kosaraju: finishing order.
    visited = [False] * n
    order = []

    for start in range(n):
        if not active[start] or visited[start]:
            continue

        visited[start] = True
        stack = [(start, 0)]

        while stack:
            u, idx = stack[-1]

            if idx < len(graph[u]):
                v = graph[u][idx]
                stack[-1] = (u, idx + 1)

                if not visited[v]:
                    visited[v] = True
                    stack.append((v, 0))
            else:
                order.append(u)
                stack.pop()

    # Second pass on the reversed graph: assign SCCs.
    comp = [-1] * n
    comp_count = 0

    for start in reversed(order):
        if comp[start] != -1:
            continue

        comp[start] = comp_count
        stack = [start]

        while stack:
            u = stack.pop()

            for v in rev[u]:
                if comp[v] == -1:
                    comp[v] = comp_count
                    stack.append(v)

        comp_count += 1

    if comp_count == 1:
        print(0)
        return

    indeg = [0] * comp_count
    outdeg = [0] * comp_count

    for u, v in edges:
        cu = comp[u]
        cv = comp[v]

        if cu != cv:
            outdeg[cu] = 1
            indeg[cv] = 1

    sources = 0
    sinks = 0

    for c in range(comp_count):
        if indeg[c] == 0:
            sources += 1
        if outdeg[c] == 0:
            sinks += 1

    print(max(sources, sinks))

if __name__ == "__main__":
    solve()
```

The input loop constructs both the original and reversed graphs because Kosaraju needs the two orientations. The `active` array prevents isolated alphabet letters from being treated as meaningful components.

The first DFS is iterative rather than recursive. With (N=100000), a recursive DFS can exceed Python's recursion limit and can also incur unnecessary interpreter overhead. The stack stores both the current vertex and the index of the next outgoing edge, which lets us reproduce recursive DFS finishing order without recursion.

The second DFS walks through the reversed graph and assigns one component identifier to every reachable vertex. Because vertices are processed in decreasing finishing order from the first pass, each traversal stays inside exactly one SCC.

After the SCCs are known, only edges crossing between different components matter. We do not need the exact number of such edges, only whether each component has at least one incoming or outgoing edge, so `indeg` and `outdeg` are stored as boolean-like integers. An edge inside one SCC is ignored because it cannot affect the condensation DAG.

The special case `comp_count == 1` must be handled before counting sources and sinks. For a single component, it would have both zero indegree and zero outdegree in the condensation representation, but the correct answer is `0`, not `1`.

Python integers have arbitrary precision, so there is no integer overflow concern. The total amount of graph storage is linear in the number of vertices and edges.

## Worked Examples

### Sample 1

The official sample contains three directed cycles, with extra edges from the first cycle to the other two. Its answer is `2`.

```
9 11
1 2
2 3
3 1
4 5
5 6
6 4
7 8
8 9
9 7
1 4
1 7
```

The SCC decomposition and condensation information are:

| SCC | Vertices | Indegree | Outdegree | Role |
| --- | --- | --- | --- | --- |
| 0 | 1, 2, 3 | 0 | 1 | Source |
| 1 | 4, 5, 6 | 1 | 0 | Sink |
| 2 | 7, 8, 9 | 1 | 0 | Sink |

There is one source SCC and two sink SCCs, so the algorithm computes `max(1, 2) = 2`.

The two additional words can conceptually connect the two sink components back into the source component. Once those connections exist, all three SCCs lie in one strongly connected structure. The example demonstrates why counting only source components is insufficient: both directions of reachability have to be repaired.

### Constructed Example 2

Consider:

```
4 3
1 2
2 3
3 4
```

The SCCs are all single vertices. The condensation graph is simply a chain.

| SCC | Vertex | Indegree | Outdegree | Role |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | Source |
| 1 | 2 | 1 | 1 | Internal |
| 2 | 3 | 1 | 1 | Internal |
| 3 | 4 | 1 | 0 | Sink |

There is one source and one sink, so the answer is `1`. Adding the word `4 -> 1` closes the chain into a cycle.

This trace shows the simplest case where the source and sink counts are equal. It also illustrates why the answer is not the number of SCCs minus one. A single added edge can connect the final sink back to the initial source and repair the whole chain.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N+M)) | Each graph and reversed-graph edge is traversed a constant number of times. |
| Space | (O(N+M)) | The two adjacency lists, edge list, component arrays, and DFS stacks are all linear. |

The upper bound of (100000) letters and (100000) words makes linear complexity appropriate. The algorithm performs a few graph traversals and a scan over the original edges, so it remains within the intended 2-second and 256 MB limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    try:
        n, m = map(int, input().split())

        graph = [[] for _ in range(n)]
        rev = [[] for _ in range(n)]
        edges = []
        active = [False] * n

        for _ in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            graph[u].append(v)
            rev[v].append(u)
            edges.append((u, v))
            active[u] = True
            active[v] = True

        visited = [False] * n
        order = []

        for start in range(n):
            if not active[start] or visited[start]:
                continue

            visited[start] = True
            stack = [(start, 0)]

            while stack:
                u, idx = stack[-1]

                if idx < len(graph[u]):
                    v = graph[u][idx]
                    stack[-1] = (u, idx + 1)

                    if not visited[v]:
                        visited[v] = True
                        stack.append((v, 0))
                else:
                    order.append(u)
                    stack.pop()

        comp = [-1] * n
        comp_count = 0

        for start in reversed(order):
            if comp[start] != -1:
                continue

            comp[start] = comp_count
            stack = [start]

            while stack:
                u = stack.pop()

                for v in rev[u]:
                    if comp[v] == -1:
                        comp[v] = comp_count
                        stack.append(v)

            comp_count += 1

        if comp_count == 1:
            return "0\n"

        indeg = [0] * comp_count
        outdeg = [0] * comp_count

        for u, v in edges:
            cu = comp[u]
            cv = comp[v]

            if cu != cv:
                outdeg[cu] = 1
                indeg[cv] = 1

        sources = sum(x == 0 for x in indeg)
        sinks = sum(x == 0 for x in outdeg)

        return f"{max(sources, sinks)}\n"

    finally:
        sys.stdin = old_stdin
        input = old_input

# Provided sample
assert run("""\
9 11
1 2
2 3
3 1
4 5
5 6
6 4
7 8
8 9
9 7
1 4
1 7
""") == "2\n", "provided sample"

# Minimum size, one self-loop
assert run("""\
1 1
1 1
""") == "0\n", "single self-loop"

# One non-trivial word
assert run("""\
2 1
1 2
""") == "1\n", "single directed edge"

# Isolated letters must not count
assert run("""\
5 1
1 2
""") == "1\n", "isolated letters"

# All active vertices already strongly connected
assert run("""\
4 5
1 2
2 3
3 4
4 1
2 4
""") == "0\n", "already strongly connected"

# Maximum-size style case: a chain of 100000 vertices
n = 100000
chain = [f"{i} {i + 1}" for i in range(1, n)]
chain_input = f"{n} {n - 1}\n" + "\n".join(chain) + "\n"
assert run(chain_input) == "1\n", "maximum-size chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1 1` | `0` | Minimum-size graph and self-loop handling |
| `2 1 / 1 2` | `1` | Single source and single sink |
| `5 1 / 1 2` | `1` | Isolated letters must be ignored |
| `4 5 / 1 2 / 2 3 / 3 4 / 4 1 / 2 4` | `0` | Already strongly connected graph |
| 100000-vertex directed chain | `1` | Maximum-size input and linear performance |

## Edge Cases

For isolated letters, consider the exact input

```
5 1
1 2
```

Only letters 1 and 2 are active. Kosaraju creates two SCCs, one containing each active letter. The first has zero indegree and the second has zero outdegree, so the source count and sink count are both one. The algorithm returns `1`, correctly ignoring letters 3, 4, and 5.

For an already strongly connected graph,

```
3 3
1 2
2 3
3 1
```

all three vertices receive the same component identifier. The algorithm stops immediately at the `comp_count == 1` check and prints `0`. No source or sink counting is needed because the original graph already permits movement between every pair of words.

For a single non-loop word,

```
2 1
1 2
```

there are two SCCs. Vertex 1 is a source and vertex 2 is a sink. One new word, `2 -> 1`, closes the cycle, so the answer is `1`. This catches implementations that accidentally return zero when there is only one original edge.

For a long one-way chain,

```
4 3
1 2
2 3
3 4
```

every vertex is its own SCC, but only vertex 1 is a source and only vertex 4 is a sink. The answer is still `1`, because adding `4 -> 1` makes the entire graph strongly connected. Counting SCCs themselves instead of source and sink SCCs would greatly overestimate the answer.

For the official sample, the three cycles form three SCCs. The first SCC is a source, while the second and third are sinks. The answer is `2`, matching the sample output. The example demonstrates the asymmetric case where the number of sink components is larger than the number of source components, which is exactly why the formula uses `max(sources, sinks)`.
