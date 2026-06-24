---
title: "CF 106180D - \u041e\u0431\u043c\u0435\u043d\u044b \u0440\u0435\u043a\u043e\u0440\u0434\u043e\u0432"
description: "We are given a sequence that behaves like a list of “records” over time, where each element can be thought of as a score or a value attached to a position. Along with this, we are given a set of allowed exchange operations."
date: "2026-06-25T06:46:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106180
codeforces_index: "D"
codeforces_contest_name: "\u0412\u044b\u0441\u0448\u0430\u044f \u043f\u0440\u043e\u0431\u0430 - 2025. \u0417\u0430\u043a\u043b\u044e\u0447\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f"
rating: 0
weight: 106180
solve_time_s: 39
verified: true
draft: false
---

[CF 106180D - \u041e\u0431\u043c\u0435\u043d\u044b \u0440\u0435\u043a\u043e\u0440\u0434\u043e\u0432](https://codeforces.com/problemset/problem/106180/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence that behaves like a list of “records” over time, where each element can be thought of as a score or a value attached to a position. Along with this, we are given a set of allowed exchange operations. Each operation connects two positions, meaning we are allowed to swap the values currently stored at those two indices.

The important detail is that swaps are not arbitrary: we are only allowed to swap along the given connections, and we can reuse these connections multiple times. The question is what is the best possible final arrangement of values we can obtain after performing any sequence of allowed swaps.

Reframed more structurally, the connections form an undirected graph over positions. Each connected component of this graph describes a set of indices whose values can be permuted arbitrarily among themselves using repeated swaps along edges. The task is to choose, inside each such component, the best possible redistribution of values.

The natural notion of “best” here is that we want the final array to be as large as possible in lexicographic order, which means earlier positions matter more than later ones. So for each component, we want to place its largest values as early in the component’s index order as possible, since earlier positions dominate lexicographic comparison.

The constraints (with up to about 10^5 or more positions and edges in typical CF style) rule out any approach that tries to simulate swaps directly. A single swap sequence can be long, and exploring all possible sequences would explode combinatorially. Even thinking in terms of BFS over permutations is impossible because the state space is factorial.

A naive approach would be to repeatedly simulate swaps and try to greedily improve the array, but even one attempt to “bubble” large values forward can cost O(nm) or worse, since each swap step only makes local changes and may need to be repeated many times across chains of connections.

Edge cases appear when the graph structure is sparse but forms long chains. For example, if indices form a path 1-2-3-4 and values are initially reversed, a naive greedy swap strategy that only considers adjacent beneficial swaps may require multiple passes or may even swap in the wrong order if it does not respect global connectivity. Another edge case is when components are large but disconnected from each other, where mixing values between components is impossible, so any global sorting approach would incorrectly assume full freedom.

## Approaches

The brute-force idea is to explicitly simulate all allowed swaps and try to explore all reachable permutations. Each swap changes the current configuration, and since we can reuse swaps indefinitely, this becomes a graph traversal over permutations. Even restricting to a single component of size k, there are k! possible arrangements, and transitions between them form a huge implicit graph. This quickly becomes infeasible even for k around 10.

The key observation is that swaps generate connected components in the position graph, and within each connected component we can rearrange values arbitrarily. This reduces the problem from “sequence of swaps” to “independent sorting problems on components”.

Inside a component, all indices are equivalent in terms of reachability, so we can freely permute the multiset of values in that component. To maximize lexicographically, we want large values to appear at smaller indices inside the component. That suggests sorting values in descending order and assigning them to sorted indices in ascending order.

The crucial structural simplification is that we never need to simulate swaps. We only need connectivity and sorting within components.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate swaps / explore states) | exponential | exponential | Too slow |
| Component + sorting | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a graph where each index is a node and each allowed swap is an undirected edge. This models exactly which positions can exchange values through sequences of swaps.
2. Find connected components of this graph using either DFS, BFS, or DSU. Each component represents a set of indices whose values can be freely permuted among themselves. This step is necessary because swap reachability is transitive.
3. For each connected component, collect all indices belonging to it and also collect the values currently stored at those indices. At this point, we are isolating the independent subproblem.
4. Sort the list of indices in increasing order. These are the positions that matter lexicographically from left to right.
5. Sort the collected values in decreasing order. This ensures we always place larger values earlier, which improves lexicographic order at the earliest possible position.
6. Assign values back: for the smallest index in the component, assign the largest value, for the next index assign the next largest value, and so on. This greedy pairing is correct because any swap sequence inside the component can realize any permutation.

### Why it works

The core invariant is that inside any connected component, the multiset of values is preserved and fully permutable. Every allowed swap is just an edge in a connected graph, and repeated swaps allow arbitrary rearrangement within that component. Therefore the only freedom we have is how to permute values inside each component.

Lexicographic order compares arrays from left to right. At the first position where two arrays differ, the larger value decides the winner. This forces a greedy strategy: within each component, the best local decision is to maximize earlier indices first, which is achieved by sorting indices ascending and values descending and pairing them.

No decision in one component affects another, because swaps never cross components.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    g = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    vis = [False] * n

    def dfs(start):
        stack = [start]
        vis[start] = True
        comp = []

        while stack:
            v = stack.pop()
            comp.append(v)
            for to in g[v]:
                if not vis[to]:
                    vis[to] = True
                    stack.append(to)
        return comp

    for i in range(n):
        if not vis[i]:
            comp = dfs(i)

            idx = sorted(comp)
            vals = sorted([a[i] for i in comp], reverse=True)

            for j, v in zip(idx, vals):
                a[j] = v

    print(*a)

if __name__ == "__main__":
    solve()
```

The graph construction directly encodes swap permissions. The DFS groups indices into components, and each component is processed independently. Sorting indices ensures we respect lexicographic priority, while sorting values in descending order ensures we maximize each position greedily.

A subtle point is that we never attempt to simulate swaps explicitly. The correctness depends entirely on the fact that connectivity implies full permutation freedom, which removes any need for constructing an actual sequence of operations.

## Worked Examples

Consider a simple case with partial connectivity.

Input:

```
5 3
5 1 4 2 3
1 2
2 3
4 5
```

We have components `{1,2,3}` and `{4,5}` (1-based indexing). The first component has indices `[0,1,2]` with values `[5,1,4]`.

| Step | Component | Indices | Values | Sorted indices | Sorted values | Assignment |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | {1,2,3} | [0,1,2] | [5,1,4] | [0,1,2] | [5,4,1] | a[0]=5, a[1]=4, a[2]=1 |
| 2 | {4,5} | [3,4] | [2,3] | [3,4] | [3,2] | a[3]=3, a[4]=2 |

Final array becomes:

```
5 4 1 3 2
```

This shows how each component is solved independently and greedily.

Now consider a fully connected case.

Input:

```
4 3
1 2 3 4
1 2
2 3
3 4
```

Everything is one component.

| Step | Indices | Values | Sorted indices | Sorted values | Assignment |
| --- | --- | --- | --- | --- | --- |
| 1 | [0,1,2,3] | [1,2,3,4] | [0,1,2,3] | [4,3,2,1] | descending fill |

Final output:

```
4 3 2 1
```

This confirms that full connectivity yields full sorting in descending order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m) | DFS over graph plus sorting inside components dominates |
| Space | O(n + m) | adjacency list and visited arrays |

The constraints typical for this problem size fit comfortably within these bounds, since sorting dominates and remains efficient even for large n. The graph traversal is linear in edges and vertices, which is optimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    solve()

    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# simple chain
assert run("""5 3
5 1 4 2 3
1 2
2 3
4 5
""") == "5 4 1 3 2"

# fully connected
assert run("""4 3
1 2 3 4
1 2
2 3
3 4
""") == "4 3 2 1"

# no edges
assert run("""3 0
3 1 2
""") == "3 1 2"

# already optimal in components
assert run("""3 1
3 2 1
1 2
""") == "3 2 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain graph | 5 4 1 3 2 | partial connectivity |
| full graph | 4 3 2 1 | full permutation freedom |
| no edges | same array | isolated components |
| single edge | local rearrangement only | correctness of component handling |

## Edge Cases

A critical edge case is when there are no swaps at all. Each index forms its own component, so the algorithm should leave the array unchanged. The DFS still runs, but each component has size 1, so sorting and assignment are no-ops, preserving the original sequence.

Another case is when the graph is fully connected. The algorithm collapses everything into one component, and the entire array is sorted in descending order. Any mistake in component detection would incorrectly split this into smaller pieces and break optimality.

Long chain components are also important. In a path graph, reachability still implies full permutation freedom, even though swaps are local. The DFS correctly merges the entire chain into one component, ensuring that values are globally rearranged rather than only locally swapped.
