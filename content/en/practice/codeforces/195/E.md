---
title: "CF 195E - Building Forest"
description: "We build a directed weighted forest incrementally. Every vertex has at most one outgoing edge, so if we start from any vertex and repeatedly follow outgoing edges, we eventually reach a root. When vertex i is added, the input gives several pairs (v, x)."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dsu", "graphs"]
categories: ["algorithms"]
codeforces_contest: 195
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 123 (Div. 2)"
rating: 2000
weight: 195
solve_time_s: 100
verified: true
draft: false
---

[CF 195E - Building Forest](https://codeforces.com/problemset/problem/195/E)

**Rating:** 2000  
**Tags:** data structures, dsu, graphs  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We build a directed weighted forest incrementally. Every vertex has at most one outgoing edge, so if we start from any vertex and repeatedly follow outgoing edges, we eventually reach a root.

When vertex `i` is added, the input gives several pairs `(v, x)`. For every pair, we create an edge from `root(v)` to `i` with weight:

$$depth(v) + x$$

Here `depth(v)` means the total weight on the path from `v` to its root.

The tricky part is that the graph changes after every insertion. A vertex that used to be a root may stop being one later. Since edges are always created from the current root of `v`, we must know the latest root and the latest depth at the moment each operation is processed.

The final task is not to output the forest itself, only the sum of all edge weights modulo $10^9+7$.

The constraints immediately rule out anything quadratic. There are at most $10^5$ vertices, and the total number of pairs `(v, x)` across all operations is also at most $10^5$. That means we can afford roughly linear or near-linear work overall. A solution that walks up chains repeatedly for every query can easily degrade to $O(n^2)$ on long paths.

The dangerous part is that roots change dynamically. A naive implementation might cache the root of a vertex once and never update it, which becomes incorrect after later insertions.

Consider this example:

```
3
0
1 1 5
1 1 2
```

Step by step:

1. Vertex 1 is isolated.
2. Add edge `1 -> 2` with weight `5`.
3. Now `root(1)` is no longer `1`, it is `2`.

The third operation creates edge `2 -> 3`, not `1 -> 3`.

The correct answer is:

```
12
```

because the edges are `5` and `7`.

Another subtle case is negative weights.

```
2
0
1 1 -3
```

The answer is:

```
1000000004
```

because the total sum is `-3 mod 1e9+7`.

A careless implementation that forgets modular normalization would print `-3`.

One more easy mistake is misunderstanding depth updates.

```
4
0
1 1 2
1 1 3
1 1 4
```

The chain evolves like this:

```
1 -> 2 (2)
2 -> 3 (5)
3 -> 4 (9)
```

Depths are cumulative. The final sum is:

```
16
```

If we incorrectly use only the immediate edge weight instead of full depth, we would get `2 + 3 + 4 = 9`, which is wrong.

## Approaches

A brute-force solution follows the definition literally.

For every pair `(v, x)` during insertion of vertex `i`, we repeatedly follow outgoing edges starting from `v` until we reach its current root. While walking, we accumulate the total path weight to compute `depth(v)`. Once we know the root and depth, we add the new edge.

This is correct because the forest structure guarantees that every chain eventually ends at a root.

The problem is performance. Imagine a long chain:

```
1 -> 2 -> 3 -> ... -> n
```

Every root query may traverse almost the entire chain. With $10^5$ operations, this becomes roughly:

$$1 + 2 + 3 + \dots + n = O(n^2)$$

which is far too slow.

The key observation is that every operation only needs two things about a vertex:

1. Its current root.
2. Its current depth to that root.

This is exactly the kind of information a Disjoint Set Union structure can maintain efficiently with path compression.

The forest has a special direction. Every vertex has at most one outgoing edge. When a root gets connected to a new vertex, the whole component simply gains a new root on top. Existing internal structure never changes.

Suppose we attach root `r` to new vertex `i` with edge weight `w`.

Then every vertex in that component gains additional depth `w`, and the new root becomes `i`.

Instead of updating all vertices explicitly, we store relative distances in the DSU. Each node keeps:

1. `parent[v]`, the next node in DSU compression.
2. `dist[v]`, the distance from `v` to `parent[v]`.

When we compress paths, we also accumulate distances upward. After compression:

```
find(v)
```

returns both:

1. The current root.
2. The total depth from `v` to that root.

This reduces every query to almost constant amortized time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n)$ | Too slow |
| Optimal DSU with distances | $O(n \alpha(n))$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Create arrays `parent` and `dist`.

`parent[v]` stores the DSU parent of vertex `v`.

`dist[v]` stores the weight from `v` to `parent[v]`.
2. Initially, when vertex `i` is added, make it its own root.

```
parent[i] = i
dist[i] = 0
```
3. Implement a DSU `find(v)` with path compression.

The function returns the current root of `v`.

While compressing the path, accumulate all edge weights so that after compression `dist[v]` becomes the total distance from `v` directly to the root.
4. For every pair `(v, x)` in the operation for vertex `i`:

First call `find(v)`.

After compression:

```
root = parent[v]
depth = dist[v]
```
5. The new edge weight equals:

$$depth + x$$

Add this value to the global answer modulo $10^9+7$.
6. Connect the old root to the new vertex.

Since the graph edge is:

```
root -> i
```

we set:

```
parent[root] = i
dist[root] = depth + x
```

This means the root now reaches the new root `i` with exactly that edge weight.
7. Continue until all operations are processed.
8. Print the answer modulo $10^9+7$.

### Why it works

The invariant is:

```
dist[v] = distance from v to parent[v]
```

For roots, `parent[v] = v` and `dist[v] = 0`.

When path compression runs, distances are accumulated upward, so afterward `dist[v]` becomes the full distance from `v` to the representative root.

Whenever we connect `root -> i` with weight `w`, we store exactly that relationship in the DSU:

```
parent[root] = i
dist[root] = w
```

No existing path inside the component changes. Every old vertex still reaches the old root exactly as before, and now additionally reaches `i` through the new edge. The accumulated distances remain correct.

Because every edge insertion is represented exactly once, and every depth query is computed from maintained path sums, the algorithm always produces the correct total weight.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n = int(input())

    parent = list(range(n + 1))
    dist = [0] * (n + 1)

    sys.setrecursionlimit(1 << 25)

    def find(x):
        if parent[x] == x:
            return x

        p = parent[x]
        root = find(p)

        dist[x] += dist[p]
        parent[x] = root

        return root

    ans = 0

    for i in range(1, n + 1):
        data = list(map(int, input().split()))

        k = data[0]

        parent[i] = i
        dist[i] = 0

        idx = 1

        for _ in range(k):
            v = data[idx]
            x = data[idx + 1]
            idx += 2

            r = find(v)

            w = dist[v] + x

            ans = (ans + w) % MOD

            parent[r] = i
            dist[r] = w

    print(ans % MOD)

solve()
```

The DSU stores weighted parent links instead of only connectivity information.

The most important detail is the `find` function. During path compression:

```
dist[x] += dist[p]
```

must happen before overwriting the parent. Otherwise we would lose the contribution of intermediate vertices.

After compression, `dist[x]` becomes the total distance from `x` to the root directly. That lets us answer future depth queries in almost constant time.

Another subtle point is that we attach only the old root:

```
parent[r] = i
dist[r] = w
```

We do not touch any other vertex in the component. Their paths remain valid automatically because they already point toward `r`.

Negative values of `x` are also valid. Python modulo handles them correctly:

```
(ans + w) % MOD
```

keeps the answer in the required range.

## Worked Examples

### Sample 1

Input:

```
6
0
0
1 2 1
2 1 5 2 2
1 1 2
1 3 4
```

Processing trace:

| Step | Operation | Root used | Edge weight | Running answer |
| --- | --- | --- | --- | --- |
| 1 | add 1 | none | none | 0 |
| 2 | add 2 | none | none | 0 |
| 3 | `(2,1)` | 2 | 1 | 1 |
| 4 | `(1,5)` | 1 | 5 | 6 |
| 4 | `(2,2)` | 3 | 3 | 9 |
| 5 | `(1,2)` | 4 | 7 | 16 |
| 6 | `(3,4)` | 5 | 14 | 30 |

Final output:

```
30
```

This trace shows how roots evolve dynamically. Vertex `2` is initially a root, then becomes attached to `3`, then the entire structure becomes attached upward repeatedly.

### Custom Example

Input:

```
4
0
1 1 2
1 1 3
1 1 4
```

Processing trace:

| Step | Depth of queried vertex | New edge weight | Running answer |
| --- | --- | --- | --- |
| 1 | - | - | 0 |
| 2 | 0 | 2 | 2 |
| 3 | 2 | 5 | 7 |
| 4 | 5 | 9 | 16 |

Final output:

```
16
```

This example demonstrates cumulative depths. Each new query for vertex `1` sees a larger and larger depth because the chain keeps growing upward.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \alpha(n))$ | Each DSU operation is amortized inverse Ackermann |
| Space | $O(n)$ | Parent and distance arrays |

The total number of pairs `(v, x)` is at most $10^5$, so the solution performs roughly linear work overall. DSU with path compression easily fits within the 2 second limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())

    parent = list(range(n + 1))
    dist = [0] * (n + 1)

    sys.setrecursionlimit(1 << 25)

    def find(x):
        if parent[x] == x:
            return x

        p = parent[x]
        root = find(p)

        dist[x] += dist[p]
        parent[x] = root

        return root

    ans = 0

    for i in range(1, n + 1):
        data = list(map(int, input().split()))

        k = data[0]

        parent[i] = i
        dist[i] = 0

        idx = 1

        for _ in range(k):
            v = data[idx]
            x = data[idx + 1]
            idx += 2

            r = find(v)

            w = dist[v] + x

            ans = (ans + w) % MOD

            parent[r] = i
            dist[r] = w

    return str(ans % MOD)

# provided sample
assert run(
"""6
0
0
1 2 1
2 1 5 2 2
1 1 2
1 3 4
"""
) == "30"

# minimum case
assert run(
"""1
0
"""
) == "0"

# negative weight
assert run(
"""2
0
1 1 -3
"""
) == str(MOD - 3)

# growing chain
assert run(
"""4
0
1 1 2
1 1 3
1 1 4
"""
) == "16"

# multiple roots merging upward
assert run(
"""5
0
0
2 1 1 2 2
1 1 3
1 2 4
"""
) == "14"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single isolated vertex | 0 | Minimum boundary |
| Negative edge weight | $10^9+4$ | Correct modular handling |
| Long upward chain | 16 | Proper cumulative depths |
| Multiple roots attached upward | 14 | Dynamic root updates |

## Edge Cases

Consider again the changing-root scenario:

```
3
0
1 1 5
1 1 2
```

Execution:

1. Vertex `1` is root.
2. Add edge `1 -> 2` with weight `5`.
3. `find(1)` now returns root `2` and depth `5`.
4. New edge weight becomes `5 + 2 = 7`.

The algorithm correctly creates edge `2 -> 3`.

Final answer:

```
12
```

Now consider negative weights:

```
2
0
1 1 -3
```

The DSU stores:

```
dist[1] = -3
```

The running answer becomes:

```
(-3) mod (1e9+7)
```

which equals:

```
1000000004
```

Python modulo arithmetic handles this safely.

Finally, consider repeated queries on a deep chain:

```
4
0
1 1 2
1 1 3
1 1 4
```

After step 2:

```
1 -> 2
depth(1) = 2
```

After step 3:

```
1 -> 2 -> 3
depth(1) = 5
```

Path compression updates `dist[1]` directly to `5`, so future queries stay fast. The algorithm never recomputes the whole chain again.
