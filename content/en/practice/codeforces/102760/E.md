---
title: "CF 102760E - Min-hashing"
description: "We have an undirected graph. Every vertex starts with a unique label, and the label values are a permutation of the numbers from 1 to n. In each round of the process, every vertex looks at its neighbors and keeps the smallest value currently present among them."
date: "2026-07-28T23:50:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102760
codeforces_index: "E"
codeforces_contest_name: "2020 KAIST 10th ICPC Mock Contest (XXI Open Cup. Grand Prix of Korea. Division 2)"
rating: 0
weight: 102760
solve_time_s: 65
verified: true
draft: false
---

[CF 102760E - Min-hashing](https://codeforces.com/problemset/problem/102760/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an undirected graph. Every vertex starts with a unique label, and the label values are a permutation of the numbers from `1` to `n`. In each round of the process, every vertex looks at its neighbors and keeps the smallest value currently present among them. The first round uses the original labels, and every later round uses the values produced by the previous round.

After round `k`, we count how many pairs of different vertices have exactly the same value. The task is to find the maximum possible value of this count over all positive rounds.

The constraints are large: there can be up to `100000` vertices and `250000` edges. A simulation that repeatedly updates every vertex would require understanding how many rounds are needed, and even one round already costs `O(n + m)`. Since the graph can be large and the answer depends on the behavior after many rounds, we need a structural observation rather than direct simulation.

The labels are unique, which is a useful property. When two vertices have the same value after some number of rounds, they are both choosing the same minimum-labeled vertex from some set of reachable vertices. The repeated minimum operation is not creating new values, it is only selecting existing labels.

A few cases are easy to mishandle. Consider a graph with a single edge.

```
2 1
1 2
1 2
```

After the first round, both vertices receive the other vertex's label, so the values are `[2, 1]` and the answer is `0`. A solution that incorrectly includes the original labels as a possible round would count the pair, which is not allowed because `k` starts from `1`.

Another tricky case is a star.

```
4 3
1 2 3 4
1 2
1 3
1 4
```

After one round, the leaves all receive label `1`, giving `C(3, 2) = 3` equal pairs. The center receives the smallest leaf label. The important detail is that the center and leaves do not become one group forever, because the graph is bipartite and parity of walks matters.

A final case is an odd cycle.

```
3 3
1 2 3
1 2
2 3
3 1
```

After enough rounds every vertex can reach every other vertex with a walk of the required length. Eventually all vertices receive label `1`, producing `C(3, 2) = 3`. Treating every component like a bipartite graph would miss this because odd cycles remove the parity restriction.

## Approaches

The direct approach is to simulate the process. For every round, we scan every edge and compute the minimum neighbor value for both endpoints. After obtaining the new labels, we count equal values using a frequency table. This is correct because it follows the definition exactly.

The problem is deciding how long we need to simulate. A graph can contain long paths, and there is no useful small bound on the number of rounds from the statement. Repeating `O(n + m)` work for many rounds is too expensive. In the worst case, attempting to simulate until nothing changes can take far beyond what is possible for `n = 100000`.

The key observation is to stop looking at values and instead look at which original vertices can influence a vertex after `k` rounds. After one round, a vertex stores the minimum label among vertices at distance one. After two rounds, it stores the minimum label among vertices reachable by a walk of length two. In general, `h^(k)` is the minimum label among all vertices reachable by a walk of exactly length `k`.

For a connected non-bipartite component, after enough steps every vertex can reach every vertex using walks of the required length. The smallest label in the component will spread everywhere, so the entire component becomes one group.

For a connected bipartite component, every walk alternates sides. After enough steps, a vertex can reach every vertex on the side determined by the parity of the walk length. The smallest label on each side spreads to the opposite side or the same side depending on the round parity. The actual labels do not affect the number of equal pairs, only the sizes of the two color classes matter.

The maximum is therefore obtained from the stable state of every component. The component contributions can be added independently because vertices from different connected components can never influence each other.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Too dependent on number of rounds, each round is `O(n + m)` | `O(n)` | Too slow |
| Optimal | `O(n + m)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Traverse every connected component with DFS or BFS while coloring the graph with two colors. The coloring tells us whether the component is bipartite and also gives the size of each side. The side information is exactly what controls reachability after many rounds.
2. While traversing a component, store whether a conflict appears, meaning an edge connects two vertices with the same color. Such a conflict proves that the component is not bipartite. For a non-bipartite component, all vertices eventually receive the component's minimum label.
3. For a non-bipartite component of size `s`, add `s * (s - 1) / 2` to the answer. Every pair inside this component eventually has equal values.
4. For a bipartite component with color class sizes `a` and `b`, add `a * (a - 1) / 2 + b * (b - 1) / 2`. After enough rounds, the two color classes become two independent groups with equal values inside each group.
5. Print the sum of all component contributions. The process of finding components already covers the whole graph, so no simulation of the hashing rounds is needed.

Why it works:

The value of a vertex after `k` rounds is determined by the minimum original label among vertices reachable by a walk of length `k`. In a connected non-bipartite graph, sufficiently long walks can connect any two vertices, so the minimum label of the whole component reaches every vertex. In a connected bipartite graph, walks preserve the side parity, so only vertices from the same color class can share the same eventual reachable set. Since the label chosen inside each reachable set is unique but identical for all vertices with the same reachable set, the final groups are exactly the color classes of bipartite components and the whole component for non-bipartite components. No earlier round can create larger groups because every round is only a restriction of the possible reachable vertices before the stable reachable sets are reached.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    labels = list(map(int, input().split()))

    graph = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    color = [-1] * n
    ans = 0

    for start in range(n):
        if color[start] != -1:
            continue

        stack = [start]
        color[start] = 0
        cnt = [1, 0]
        bipartite = True

        while stack:
            v = stack.pop()
            for u in graph[v]:
                if color[u] == -1:
                    color[u] = color[v] ^ 1
                    cnt[color[u]] += 1
                    stack.append(u)
                elif color[u] == color[v]:
                    bipartite = False

        if bipartite:
            ans += cnt[0] * (cnt[0] - 1) // 2
            ans += cnt[1] * (cnt[1] - 1) // 2
        else:
            s = cnt[0] + cnt[1]
            ans += s * (s - 1) // 2

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation only needs graph traversal. The labels are read because they belong to the original definition, but the final number of equal pairs depends only on the component structure, not on the actual values of the labels.

The `color` array performs the bipartite check. A new component starts with color `0`, and every edge requires the other endpoint to have the opposite color. If we ever find an edge between equal colors, the component contains an odd cycle.

The counts `cnt[0]` and `cnt[1]` are the sizes of the two sides of a bipartite component. The number of equal pairs inside a group of size `x` is `x * (x - 1) // 2`, which is why the formula is used directly instead of constructing the final hash values.

Python integers do not overflow, but the answer can be as large as `C(100000, 2)`, so a language with fixed-width integers would need a 64-bit type.

## Worked Examples

### Sample 1

Input:

```
5 5
1 2 3 4 5
1 2
2 3
3 4
4 5
5 1
```

The graph is a cycle of length five, so it is not bipartite.

| Step | Component size | Bipartite | Color sizes | Added pairs |
| --- | --- | --- | --- | --- |
| DFS finishes | 5 | No | N/A | `5 * 4 / 2 = 10` |

The odd cycle means every vertex can eventually reach every vertex with a suitable walk length. The minimum label spreads to all five vertices, creating ten equal pairs.

### Sample 2

Input:

```
4 3
1 2 3 4
1 2
2 3
3 4
```

The graph is a path with two vertices on each side.

| Step | Component size | Bipartite | Color sizes | Added pairs |
| --- | --- | --- | --- | --- |
| DFS finishes | 4 | Yes | 2, 2 | `1 + 1 = 2` |

After many rounds, one side of the path receives one minimum label and the other side receives the other minimum label. Each side contributes one equal pair.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n + m)` | Every vertex and edge is visited once during the graph traversal. |
| Space | `O(n + m)` | The adjacency list stores the graph and the arrays store traversal state. |

The limits allow linear graph processing. A traversal over `100000` vertices and `250000` edges fits comfortably, while repeated simulation of the hashing process would not.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.getvalue()

# Sample 1
assert run("""5 5
1 2 3 4 5
1 2
2 3
3 4
4 5
5 1
""") == "10\n"

# Sample 2
assert run("""4 3
1 2 3 4
1 2
2 3
3 4
""") == "2\n"

# Minimum graph
assert run("""2 1
1 2
1 2
""") == "0\n"

# Star graph
assert run("""5 4
1 2 3 4 5
1 2
1 3
1 4
1 5
""") == "6\n"

# Complete triangle
assert run("""3 3
1 2 3
1 2
2 3
3 1
""") == "3\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two vertices with one edge | `0` | The first valid round is `k = 1`, not the initial labels. |
| Star graph | `6` | A large bipartite side creates many equal pairs. |
| Triangle | `3` | Odd cycles must be treated as non-bipartite. |
| Path sample | `2` | Bipartite components use color class sizes. |

## Edge Cases

For the single-edge graph:

```
2 1
1 2
1 2
```

DFS finds one bipartite component with color sizes `1` and `1`. The contribution is `0 + 0 = 0`. This matches the process because each vertex always receives the other vertex's label, so no two vertices ever share a value.

For the star graph:

```
4 3
1 2 3 4
1 2
1 3
1 4
```

The colors have sizes `1` and `3`. The algorithm adds `C(1,2) + C(3,2) = 3`. The three leaves have the same eventual reachable side, while the center remains in the other group.

For the odd cycle:

```
3 3
1 2 3
1 2
2 3
3 1
```

The DFS detects that the graph cannot be colored with two colors because adjacent vertices would need the same color somewhere. The whole component has size three, so it contributes `C(3,2) = 3`.

For disconnected graphs, each component is handled separately. A vertex in one component can never see a label from another component, so adding the independent component contributions gives the correct global maximum.
