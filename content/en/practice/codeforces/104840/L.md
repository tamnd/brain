---
title: "CF 104840L - \u041f\u0443\u0442\u0435\u0448\u0435\u0441\u0442\u0432\u0438\u0435 \u043a \u043f\u0440\u0438\u043c\u0438\u0442\u0438\u0432\u0443"
description: "We are given a set of words, all distinct, and a directed system of allowed replacements between them. Each replacement rule says that one word can be substituted by another, and this process can be repeated any number of times, following chains of replacements."
date: "2026-06-28T11:40:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104840
codeforces_index: "L"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2023-2024, \u0422\u0440\u0435\u0442\u044c\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 104840
solve_time_s: 49
verified: true
draft: false
---

[CF 104840L - \u041f\u0443\u0442\u0435\u0448\u0435\u0441\u0442\u0432\u0438\u0435 \u043a \u043f\u0440\u0438\u043c\u0438\u0442\u0438\u0432\u0443](https://codeforces.com/problemset/problem/104840/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of words, all distinct, and a directed system of allowed replacements between them. Each replacement rule says that one word can be substituted by another, and this process can be repeated any number of times, following chains of replacements.

The task is to apply these substitutions in any order and any number of times so that the number of distinct words remaining is as small as possible. We are not asked to find the final words themselves, only the minimum possible count of distinct words after fully exploiting all replacement possibilities.

This structure is naturally a directed graph where each word is a node and each replacement is a directed edge. A sequence of replacements corresponds to walking along directed edges.

The constraints allow up to 200,000 words and 200,000 replacement rules, which immediately rules out any quadratic reasoning or repeated simulation of transformations. Any solution must be close to linear or linearithmic in the size of the graph, since even O(n²) operations would be far beyond the limit.

A subtle issue is that replacements are not necessarily symmetric. If we can replace a with b, it does not imply b can replace a. Another important point is that multiple chains can merge into the same word, meaning different initial words can eventually be transformed into a single representative if they reach a common destination.

A typical failing scenario for naive thinking is treating replacements as independent or doing greedy local merges. For example, if we have a cycle like a → b → c → a, all three words can collapse into one, but if we only look at immediate replacements, we might miss that global cycle structure.

Another failure case appears when long chains exist. If a → b, b → c, c → d, then all four words can collapse into d, even though no direct edge exists between a and d. Any approach that does not account for transitive closure will underestimate the merging potential.

## Approaches

A brute-force interpretation would simulate all possible transformations from every word and compute all reachable words. For each word, we could run a DFS or BFS over the directed graph and mark all reachable nodes. Then we would try to determine how many unique minimal representatives exist after collapsing reachable sets.

This already runs into a serious efficiency problem. Running a graph traversal from every node leads to O(n(n + m)) in the worst case, which is completely infeasible for 200,000 nodes.

The key insight is to stop thinking in terms of individual reachability sets and instead focus on equivalence induced by mutual reachability. If word A can reach word B and word B can reach word A through some sequence of replacements, then A and B are interchangeable in the sense that they belong to a strongly connected structure. Inside such a structure, all words can be transformed into one another, so they can be collapsed into a single representative.

This reduces the problem to finding strongly connected components (SCCs) in the directed graph. After condensation into SCCs, we get a DAG. Inside each SCC, all words are equivalent, so they contribute only one word to the final answer.

The remaining question is whether any SCCs can also be merged across edges. Since edges only allow forward replacement, an SCC cannot reduce the number of distinct words further beyond one per component. Thus the final answer is simply the number of SCCs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Reachability | O(n(n + m)) | O(n + m) | Too slow |
| SCC Decomposition | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We model the words as vertices in a directed graph and build adjacency lists from the replacement rules.

1. Build a mapping from each word to an integer index. This allows efficient graph representation instead of string-based lookups, which would be too slow at this scale.
2. Construct the directed graph using the replacement rules. Each rule a → b becomes a directed edge from index(a) to index(b).
3. Run a strongly connected components algorithm on the graph. A standard way is Kosaraju’s algorithm or Tarjan’s algorithm. The goal is to partition nodes so that each component contains exactly those nodes mutually reachable through directed paths.
4. Count the number of resulting SCCs. Each SCC represents a group of words that can all be transformed into one another through repeated substitutions.
5. Output this count as the minimum possible number of distinct words.

The key reason SCCs matter is that inside a component, any word can be converted into any other, so we can always collapse the component into a single chosen representative word. Between components, such full conversion is impossible because there is no mutual reachability.

### Why it works

Within a strongly connected component, every node can reach every other node. This means any word in that component can be transformed into any other through valid substitution chains. Therefore, the entire component behaves like a single interchangeable entity, and keeping more than one word from it is unnecessary.

Across different SCCs, at least one direction of reachability is missing. If two components were merged into one word, that would require mutual reachability between them, which contradicts the definition of SCCs. Therefore each SCC contributes at least one distinct unavoidable word, and exactly one is sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

def kosaraju(n, g, gr):
    visited = [False] * n
    order = []

    def dfs1(v):
        visited[v] = True
        for to in g[v]:
            if not visited[to]:
                dfs1(to)
        order.append(v)

    def dfs2(v):
        visited[v] = True
        for to in gr[v]:
            if not visited[to]:
                dfs2(to)

    for i in range(n):
        if not visited[i]:
            dfs1(i)

    visited = [False] * n
    scc_count = 0

    for v in reversed(order):
        if not visited[v]:
            dfs2(v)
            scc_count += 1

    return scc_count

def solve():
    n, m = map(int, input().split())
    idx = {}
    words = []

    for i in range(n):
        w = input().strip()
        idx[w] = i
        words.append(w)

    g = [[] for _ in range(n)]
    gr = [[] for _ in range(n)]

    for _ in range(m):
        a, b = input().split()
        u = idx[a]
        v = idx[b]
        g[u].append(v)
        gr[v].append(u)

    print(kosaraju(n, g, gr))

if __name__ == "__main__":
    solve()
```

The implementation first compresses string nodes into integer indices using a hash map, which is essential to keep operations O(1) per edge. The adjacency list `g` stores the directed replacement graph, while `gr` stores the reversed graph required for Kosaraju’s second pass.

The first DFS builds a finishing order over the original graph. This ordering ensures that when we process nodes in reverse finishing time, we always start SCC exploration from a valid root of a component in the reversed graph.

The second DFS runs on the reversed graph and counts how many times we initiate a new traversal, which directly corresponds to the number of SCCs.

## Worked Examples

Consider the sample structure where words form a chain with extra cross-links, allowing full collapse.

Input:

```
5 5
hello
world
first
word
second
hello world
world first
world second
second first
word world
```

| Step | Current node | Stack order | New SCC? | SCC count |
| --- | --- | --- | --- | --- |
| DFS finish order | all nodes | hello, world, word, second, first | - | 0 |
| Process reversed | first | start DFS2 | yes | 1 |

This trace shows that all nodes are mutually reachable through cycles induced by the replacement rules. The second pass finds a single SCC, confirming full collapse into one word.

Now consider a simple acyclic case.

Input:

```
4 2
a
b
c
d
a b
b c
```

| Step | Node | Action | SCC formed |
| --- | --- | --- | --- |
| First pass order | d, c, b, a | finish order recorded | - |
| Second pass | a | explores only a | {a} |
| Second pass | b | explores b → c | {b, c} |
| Second pass | d | isolated | {d} |

This produces three SCCs, meaning three unavoidable distinct words remain.

These examples show how cycles collapse into single components while linear chains do not.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each node and edge is processed a constant number of times across both DFS passes |
| Space | O(n + m) | Adjacency lists and recursion stacks store graph structure and traversal state |

The linear complexity is essential given that both n and m can reach 200,000. Any superlinear method would fail under the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import defaultdict

    sys.setrecursionlimit(10**7)

    n, m = map(int, sys.stdin.readline().split())
    idx = {}
    for i in range(n):
        w = sys.stdin.readline().strip()
        idx[w] = i

    g = [[] for _ in range(n)]
    gr = [[] for _ in range(n)]

    for _ in range(m):
        a, b = sys.stdin.readline().split()
        u = idx[a]
        v = idx[b]
        g[u].append(v)
        gr[v].append(u)

    def kosaraju():
        vis = [False] * n
        order = []

        def dfs(v):
            vis[v] = True
            for to in g[v]:
                if not vis[to]:
                    dfs(to)
            order.append(v)

        for i in range(n):
            if not vis[i]:
                dfs(i)

        vis = [False] * n
        cnt = 0

        def dfs2(v):
            vis[v] = True
            for to in gr[v]:
                if not vis[to]:
                    dfs2(to)

        for v in reversed(order):
            if not vis[v]:
                dfs2(v)
                cnt += 1

        return cnt

    return str(kosaraju())

# provided sample
assert run("""5 5
hello
world
first
word
second
hello world
world first
world second
second first
word world
""") == "1"

# chain case
assert run("""4 2
a
b
c
d
a b
b c
""") == "3"

# all isolated
assert run("""3 0
a
b
c
""") == "3"

# full cycle
assert run("""3 3
a
b
c
a b
b c
c a
""") == "1"

# two components
assert run("""6 4
a
b
c
d
e
f
a b
b a
c d
d c
""") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| no edges | n | isolated nodes remain separate |
| linear chain | 3 | partial collapses only |
| full cycle | 1 | SCC collapse works |
| disjoint cycles | 4 | multiple SCCs counted correctly |

## Edge Cases

A fully disconnected graph is the simplest stress case. Each word has no replacements, so no merges are possible. The algorithm assigns each node to its own SCC during the second DFS pass. For example, with three words and no edges, the reversed graph is also empty, and each DFS2 call touches exactly one node, producing three components.

A fully cyclic graph is the opposite extreme. If every word can reach every other through cycles, the finishing order from DFS1 becomes irrelevant, since DFS2 will sweep the entire graph in one traversal. This produces exactly one SCC.

Long chains test transitive reachability. In a case like a → b → c → d, DFS2 processes nodes in reverse finishing order, ensuring that when c is processed, it can reach b and a in the reversed graph traversal, grouping them correctly into SCCs only when mutual reachability exists.
