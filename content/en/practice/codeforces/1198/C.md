---
title: "CF 1198C - Matching vs  Independent Set"
description: "Each test case describes an undirected graph with exactly $3n$ vertices. We must output one of two structures: 1. A matching containing exactly $n$ edges, where no two chosen edges share a vertex. 2."
date: "2026-06-12T00:03:30+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "graphs", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1198
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 576 (Div. 1)"
rating: 2000
weight: 1198
solve_time_s: 445
verified: false
draft: false
---

[CF 1198C - Matching vs  Independent Set](https://codeforces.com/problemset/problem/1198/C)

**Rating:** 2000  
**Tags:** constructive algorithms, graphs, greedy, sortings  
**Solve time:** 7m 25s  
**Verified:** no  

## Solution
## Problem Understanding

Each test case describes an undirected graph with exactly $3n$ vertices. We must output one of two structures:

1. A matching containing exactly $n$ edges, where no two chosen edges share a vertex.
2. An independent set containing exactly $n$ vertices, where no edge exists between any pair of chosen vertices.

The graph may contain up to $5 \cdot 10^5$ edges across all test cases, while the sum of all $n$ values is at most $10^5$. These limits immediately rule out anything that tries to examine large subsets of vertices or edges. Even an $O(V^2)$ algorithm would be far too slow when $V = 3n$ reaches $3 \cdot 10^5$ over all tests. We need something close to linear in the graph size.

The most interesting part of the problem is that we are guaranteed nothing about the graph structure. We are not asked to maximize a matching or maximize an independent set. We only need one of them of size exactly $n$. The existence of at least one valid answer is the key observation behind the solution.

A common mistake is to think that a maximum matching must be computed. Consider:

```
n = 2
Vertices: 1..6
Edges:
1-2
3-4
```

The matching $\{(1,2),(3,4)\}$ already has size $2$, so we can stop immediately. Running a full maximum matching algorithm would be unnecessary.

Another easy mistake is to construct an independent set from arbitrary unused vertices. Suppose:

```
n = 2
Vertices: 1..6
Edges:
1-2
3-4
2-3
```

If we greedily choose vertices without understanding why they are unused, we could accidentally select both 2 and 3, which are adjacent. The solution relies on a stronger property that guarantees the selected vertices are pairwise non-adjacent.

A third subtle case occurs when the matching found greedily is smaller than $n$:

```
n = 2
Vertices: 1..6
Edges:
1-2
2-3
```

The greedy matching contains only one edge. A careless implementation might conclude that no solution exists. In reality, vertices 4, 5, 6 together with either 1 or 3 form a large independent set, and the problem guarantees that one of the two structures can always be produced.

## Approaches

The brute-force viewpoint is straightforward. We could search for a matching of size $n$, and if that fails, search for an independent set of size $n$. Unfortunately, both tasks are difficult in general graphs.

A brute-force matching search would examine subsets of edges. With up to $5 \cdot 10^5$ edges, even checking all subsets of size $n$ is completely infeasible. The number of possibilities is astronomical.

Similarly, checking all vertex subsets of size $n$ to find an independent set would require

$$\binom{3n}{n}$$

possibilities, which is even worse.

The crucial observation is that the problem does not ask for an optimal matching. Any matching of size $n$ is acceptable.

Suppose we process edges one by one. Whenever an edge connects two currently unused vertices, we take it into our matching and mark both endpoints as used. This is the standard greedy construction of a maximal matching.

Why is a maximal matching useful? Because once the process ends, every remaining unused vertex has a very strong property. If two unused vertices were connected by an edge, that edge would have been available when processed, since neither endpoint would have been used. The greedy algorithm would then have selected it. Since that never happened, no edge can exist between two unused vertices.

That means all unused vertices automatically form an independent set.

Now count vertices. Let the greedy matching contain $k$ edges. It uses $2k$ vertices, leaving

$$3n - 2k$$

unused vertices.

If $k \ge n$, the first $n$ matching edges solve the problem.

Otherwise $k < n$. Then

$$3n - 2k > 3n - 2(n-1) = n+2.$$

So there are more than $n$ unused vertices. Since all unused vertices form an independent set, we can simply take any $n$ of them.

This transforms the problem from a difficult graph optimization problem into a single greedy pass through the edges.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal Greedy Maximal Matching | $O(m+n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Create a boolean array `used` for all $3n$ vertices.
2. Process the edges in input order.
3. For edge $i = (u,v)$, check whether both endpoints are currently unused.
4. If both endpoints are unused, add edge index $i$ to the matching and mark both vertices as used.

This keeps the chosen edges pairwise disjoint, so they always form a valid matching.
5. After all edges are processed, examine the size of the matching.
6. If the matching contains at least $n$ edges, output `"Matching"` and print any $n$ edge indices from it.
7. Otherwise collect all vertices whose `used` value is false.
8. Output `"IndSet"` and print any $n$ unused vertices.

The unused vertices form an independent set because every edge between two unused vertices would have been selected during the greedy process.

### Why it works

The greedy procedure constructs a maximal matching. Every chosen edge has two previously unused endpoints, so no two chosen edges share a vertex.

Consider any two vertices that remain unused after processing all edges. If an edge existed between them, then when that edge was examined neither endpoint would have been marked used. The greedy rule would have selected that edge, contradicting the fact that both vertices remained unused. Hence the set of unused vertices is independent.

Let the matching size be $k$.

If $k \ge n$, selecting any $n$ matching edges gives a valid answer.

If $k < n$, the number of unused vertices is

$$3n - 2k > n.$$

Since all unused vertices form an independent set, at least $n$ of them can be chosen.

One of the two cases must occur, so the algorithm always produces a valid output.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, m = map(int, input().split())

        used = [False] * (3 * n + 1)
        matching = []

        for idx in range(1, m + 1):
            u, v = map(int, input().split())

            if not used[u] and not used[v]:
                used[u] = True
                used[v] = True
                matching.append(idx)

        if len(matching) >= n:
            ans.append("Matching")
            ans.append(" ".join(map(str, matching[:n])))
        else:
            independent = []

            for v in range(1, 3 * n + 1):
                if not used[v]:
                    independent.append(v)

            ans.append("IndSet")
            ans.append(" ".join(map(str, independent[:n])))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The `used` array records whether a vertex has already been consumed by a selected matching edge.

Whenever an edge has two unused endpoints, we immediately take it. This greedily grows a maximal matching. No later decision can invalidate an earlier one because marked vertices are never reused.

After processing all edges, the matching either already has size at least `n`, or it does not. In the first case we only need the first `n` edge indices. The problem does not require a maximum matching.

In the second case we scan all vertices and collect those that were never matched. These vertices are exactly the unused vertices from the correctness proof. Taking the first `n` of them is safe because the proof guarantees that the entire set is independent.

A common implementation mistake is storing matching edges themselves rather than their input indices. The output requires edge indices, so the code saves `idx`.

Another easy error is forgetting that vertices are numbered from `1` to `3n`. The array size must be `3*n + 1` to support 1-based indexing.

## Worked Examples

### Example 1

Input:

```
n = 2
Edges:
1: 1-2
2: 2-3
3: 4-5
```

Processing:

| Edge Index | Edge | Both Unused? | Matching | Used Vertices |
| --- | --- | --- | --- | --- |
| 1 | (1,2) | Yes | [1] | {1,2} |
| 2 | (2,3) | No | [1] | {1,2} |
| 3 | (4,5) | Yes | [1,3] | {1,2,4,5} |

The matching size is 2, which equals $n$.

Output:

```
Matching
1 3
```

This example shows how the greedy procedure directly produces a sufficient matching.

### Example 2

Input:

```
n = 2
Edges:
1: 1-2
2: 2-3
```

Processing:

| Edge Index | Edge | Both Unused? | Matching | Used Vertices |
| --- | --- | --- | --- | --- |
| 1 | (1,2) | Yes | [1] | {1,2} |
| 2 | (2,3) | No | [1] | {1,2} |

After processing all edges:

| Vertex | Used? |
| --- | --- |
| 1 | Yes |
| 2 | Yes |
| 3 | No |
| 4 | No |
| 5 | No |
| 6 | No |

Unused vertices are `[3, 4, 5, 6]`.

Taking the first two gives:

```
IndSet
3 4
```

The trace demonstrates the key property of maximal matchings. Even though the matching is too small, the remaining vertices automatically form a large independent set.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m+n)$ | One pass through all edges and one pass through all $3n$ vertices |
| Space | $O(n)$ | The `used` array and stored answer indices |

The total input size over all test cases is bounded by $10^5$ vertices and $5 \cdot 10^5$ edges. A linear scan of these structures easily fits within the 1 second limit in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    input_data = io.StringIO(inp)
    output_data = io.StringIO()

    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = input_data
    sys.stdout = output_data

    try:
        def solve():
            import sys
            input = sys.stdin.readline

            t = int(input())

            for _ in range(t):
                n, m = map(int, input().split())

                used = [False] * (3 * n + 1)
                matching = []

                for idx in range(1, m + 1):
                    u, v = map(int, input().split())

                    if not used[u] and not used[v]:
                        used[u] = used[v] = True
                        matching.append(idx)

                if len(matching) >= n:
                    print("Matching")
                    print(*matching[:n])
                else:
                    indep = [v for v in range(1, 3 * n + 1) if not used[v]]
                    print("IndSet")
                    print(*indep[:n])

        solve()
        return output_data.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# minimum size
assert run(
"""1
1 0
"""
) == """IndSet
1"""

# single edge gives matching
assert run(
"""1
1 1
1 2
"""
) == """Matching
1"""

# independent-set case
assert run(
"""1
2 2
1 2
2 3
"""
) == """IndSet
3 4"""

# matching case
assert run(
"""1
2 2
1 2
3 4
"""
) == """Matching
1 2"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| $n=1,m=0$ | Independent set | Empty graph handling |
| One edge on three vertices | Matching | Smallest non-trivial matching |
| Path 1-2-3 with $n=2$ | Independent set | Matching too small |
| Two disjoint edges | Matching | Exact matching size reached |

## Edge Cases

Consider the graph

```
1
1 0
```

There are three vertices and no edges. The greedy matching remains empty. All vertices are unused, so the independent set candidates are `{1,2,3}`. The algorithm outputs any one of them. This verifies that isolated vertices are handled correctly.

Consider

```
1
2 2
1 2
2 3
```

The first edge is selected. The second cannot be selected because vertex 2 is already used. The matching size is only 1. The unused vertices are `{3,4,5,6}`. Since no edge connects any pair of unused vertices, choosing any two of them yields a valid independent set.

Consider

```
1
2 3
1 2
3 4
5 6
```

All three edges are disjoint. The greedy procedure selects all of them. Since the matching size is already greater than $n$, the algorithm simply outputs the first two edge indices. No maximum matching computation is needed.

Consider

```
1
2 5
1 2
1 3
1 4
1 5
1 6
```

Only the first edge can be chosen. Every other edge touches vertex 1, which is already used. The matching size is 1. The unused vertices are `{3,4,5,6}` and they form an independent set because every graph edge is incident to vertex 1. The algorithm correctly switches to the independent-set output mode.
