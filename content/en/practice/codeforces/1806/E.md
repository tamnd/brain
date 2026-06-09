---
title: "CF 1806E - Tree Master"
description: "The tree is rooted at vertex 1. Every vertex has a value a[v], and every vertex except the root has a parent. For a query (x, y), both vertices are guaranteed to lie at the same depth. Starting from these two vertices, we repeatedly move both upward one edge at a time."
date: "2026-06-09T09:10:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dfs-and-similar", "trees"]
categories: ["algorithms"]
codeforces_contest: 1806
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 858 (Div. 2)"
rating: 2200
weight: 1806
solve_time_s: 92
verified: true
draft: false
---

[CF 1806E - Tree Master](https://codeforces.com/problemset/problem/1806/E)

**Rating:** 2200  
**Tags:** brute force, data structures, dfs and similar, trees  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

The tree is rooted at vertex 1. Every vertex has a value `a[v]`, and every vertex except the root has a parent.

For a query `(x, y)`, both vertices are guaranteed to lie at the same depth. Starting from these two vertices, we repeatedly move both upward one edge at a time. At every step we multiply the values on the current pair of vertices and add that product to the answer.

If we write the ancestor chains as

`x = x0, x1 = parent(x0), x2 = parent(x1), ...`

and

`y = y0, y1 = parent(y0), y2 = parent(y1), ...`

then the answer is

`a[x0]a[y0] + a[x1]a[y1] + a[x2]a[y2] + ...`

until both chains reach the root.

The recurrence hidden inside the definition is

$$f(x,y)=a_xa_y+f(p_x,p_y)$$

with

$$f(0,0)=0.$$

The constraints are the real challenge. Both `n` and `q` can reach `10^5`. A single query may involve a path of length `10^5`, so directly walking to the root for every query could require around `10^10` operations in the worst case. Any solution that processes an entire ancestor chain per query is immediately ruled out.

The memory limit is very generous, 1024 MB. This is a strong hint that we are allowed to cache a large amount of information, but not all `n²` possible vertex pairs.

A subtle edge case appears when both queried vertices are the same.

Example:

```
3 1
2 3 5
1 2
3 3
```

The correct answer is

$$5^2+3^2+2^2=38.$$

A careless implementation that tries to exploit symmetry without handling identical vertices correctly can accidentally double count or skip terms.

Another easy mistake is assuming that memoization over all pairs is feasible.

Consider a star:

```
1
├── 2
├── 3
├── ...
└── 100000
```

All leaves have the same depth. There are almost `10^10` possible leaf pairs. Storing every pair value is impossible.

A third pitfall comes from recursion depth. The recurrence naturally suggests a recursive implementation, but a chain of length `10^5` exceeds Python's recursion limit. An accepted Python solution must either increase the limit carefully or use an iterative formulation.

## Approaches

The brute-force solution follows the definition directly. For each query, repeatedly add `a[x] * a[y]`, then replace both vertices by their parents.

The recurrence

$$f(x,y)=a_xa_y+f(p_x,p_y)$$

shows that this is correct. Unfortunately, if the tree is a long chain, a single query costs `O(n)`, and `10^5` queries become `O(nq)=10^{10}` operations.

The recurrence also reveals something useful. Many queries eventually reach the same pair `(u,v)`. Once we know `f(u,v)`, every future computation that reaches that state can stop immediately.

The problem is that there are too many possible pairs. We cannot memoize all of them.

The key observation is about depths.

Let `cnt[d]` be the number of vertices at depth `d`.

Choose a threshold

$$B \approx \sqrt n.$$

Depths with at most `B` vertices are called small depths.

For every small depth, there are at most `B` possible vertices on that depth. Storing answers involving those vertices becomes affordable.

Suppose we assign each vertex a position inside its depth level. For a vertex `y` on a small depth, we may store `f(x,y)` for every vertex `x`.

The number of stored states is

$$\sum_{\text{small depths}} n \cdot cnt[d].$$

Since every small depth contains at most `B` vertices, the total is at most `nB`.

Now consider a query. While climbing upward, if the current depth is large, that depth contains more than `B` vertices. Since the total number of vertices is `n`, there can be at most `n/B` such large depths on any root path.

After at most `n/B` upward moves, we reach a small depth. At that moment we can immediately retrieve the precomputed value.

This gives

$$O\!\left(\frac{n}{B}\right)$$

work per query and

$$O(nB)$$

total stored states.

Choosing

$$B \approx \sqrt n$$

balances both terms and yields

$$O(n\sqrt n)$$

overall complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Optimal | O(n√n + q√n) | O(n√n) | Accepted |

## Algorithm Walkthrough

1. Build the rooted tree and compute the depth of every vertex.
2. For every depth `d`, count how many vertices belong to that depth.
3. Inside each depth, assign a local index `h[v]` to every vertex. This index is used to address memoized states.
4. Let `B = 320` (approximately `√100000`).
5. Define a memoized function:

$$f(x,y)=a_xa_y+f(p_x,p_y).$$

The base case is `f(0,0)=0`.

1. Whenever the current depth of `y` is small, meaning `cnt[depth[y]] <= B`, store the answer in a table `dp[x][h[y]]`.

The local index is enough because all vertices at the same depth have distinct positions.

1. To answer a query `(x,y)`, evaluate the recurrence. If a memoized value already exists, return it immediately.
2. Otherwise compute

$$f(x,y)=a_xa_y+f(p_x,p_y),$$

store it if the depth is small, and return it.

### Why it works

The recurrence exactly matches the definition of the query. Every recursive step removes one pair of vertices from the sum and delegates the remaining suffix to the parent pair.

Memoization never changes the value being returned. It only avoids recomputing a state that was already solved earlier.

For depths containing at most `B` vertices, every state `(x,y)` is stored after its first computation. For depths larger than `B`, there are few such levels on any root path, because each large level contains more than `B` vertices and the tree has only `n` vertices in total.

Thus every query performs only a bounded number of uncached transitions before reaching a cached state, and every returned value is exactly the recurrence value defined by the problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    a = [0] + list(map(int, input().split()))

    parent = [0] * (n + 1)
    children = [[] for _ in range(n + 1)

]
    p = list(map(int, input().split()))

    for i in range(2, n + 1):
        parent[i] = p[i - 2]
        children[parent[i]].append(i)

    depth = [0] * (n + 1)

    cnt = [0] * (n + 1)
    pos = [0] * (n + 1)

    stack = [(1, 0)]
    while stack:
        v, d = stack.pop()
        depth[v] = d
        cnt[d] += 1
        pos[v] = cnt[d]

        for to in children[v]:
            stack.append((to, d + 1))

    B = 320

    dp = [[0] * (B + 2) for _ in range(n + 1)]

    sys.setrecursionlimit(300000)

    def ask(x, y):
        if x == 0:
            return 0

        if cnt[depth[y]] <= B:
            cached = dp[x][pos[y]]
            if cached:
                return cached

        ans = ask(parent[x], parent[y]) + a[x] * a[y]

        if cnt[depth[y]] <= B:
            dp[x][pos[y]] = ans

        return ans

    out = []
    for _ in range(q):
        x, y = map(int, input().split())
        out.append(str(ask(x, y)))

    sys.stdout.write("\n".join(out))

solve()
```

The first part constructs the rooted tree and computes depths. While traversing the tree, every vertex receives a position inside its own depth level. If a depth contains vertices `{v1, v2, ..., vk}`, their positions are `1..k`.

The table `dp[x][pos[y]]` is only used when the depth of `y` is small. Because small depths contain at most `B` vertices, `pos[y]` never exceeds the table width.

The recurrence `ask(parent[x], parent[y]) + a[x] * a[y]` directly mirrors the mathematical definition of the answer.

The cache lookup happens before the recursive call. Once a state from a small depth has been computed, every future query reaching that state stops immediately.

One implementation detail is important. The cache uses `0` as the "not computed" marker. This is safe because every vertex value is positive, so every valid answer is strictly positive.

Another detail is the recursion limit. A chain-shaped tree can have depth `100000`, so the default Python recursion limit is insufficient.

## Worked Examples

### Sample 1

Input:

```
6 2
1 5 2 3 1 1
1 2 3 3 2
4 5
6 6
```

For query `(4,5)`:

| x | y | Added value | Running sum |
| --- | --- | --- | --- |
| 4 | 5 | 3×1=3 | 3 |
| 3 | 3 | 2×2=4 | 7 |
| 2 | 2 | 5×5=25 | 32 |
| 1 | 1 | 1×1=1 | 33 |

Answer = 33.

For query `(6,6)`:

| x | y | Added value | Running sum |
| --- | --- | --- | --- |
| 6 | 6 | 1×1=1 | 1 |
| 2 | 2 | 5×5=25 | 26 |
| 1 | 1 | 1×1=1 | 27 |

Answer = 27.

This example shows the recurrence directly. Each row corresponds to one recursive transition.

### Custom Example

```
4 1
1 2 3 4
1 2 3
4 4
```

The tree is a chain.

| x | y | Added value | Running sum |
| --- | --- | --- | --- |
| 4 | 4 | 16 | 16 |
| 3 | 3 | 9 | 25 |
| 2 | 2 | 4 | 29 |
| 1 | 1 | 1 | 30 |

Answer = 30.

This example exercises the maximum-depth behavior. The algorithm repeatedly applies the same recurrence until reaching `(0,0)`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n√n + q√n) | Each query climbs through at most O(√n) uncached levels |
| Space | O(n√n) | Memoized states for all small depths |

With `n = 10^5`, `√n` is roughly `316`. The resulting number of operations is comfortably inside the limit, and the memory usage fits inside the available 1024 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    input_data = io.StringIO(inp)

    n, q = map(int, input_data.readline().split())
    a = [0] + list(map(int, input_data.readline().split()))

    parent = [0] * (n + 1)
    children = [[] for _ in range(n + 1)]

    p = list(map(int, input_data.readline().split()))
    for i in range(2, n + 1):
        parent[i] = p[i - 2]
        children[parent[i]].append(i)

    depth = [0] * (n + 1)
    cnt = [0] * (n + 1)
    pos = [0] * (n + 1)

    stack = [(1, 0)]
    while stack:
        v, d = stack.pop()
        depth[v] = d
        cnt[d] += 1
        pos[v] = cnt[d]
        for to in children[v]:
            stack.append((to, d + 1))

    B = 320
    dp = [[0] * (B + 2) for _ in range(n + 1)]

    sys.setrecursionlimit(300000)

    def ask(x, y):
        if x == 0:
            return 0
        if cnt[depth[y]] <= B and dp[x][pos[y]]:
            return dp[x][pos[y]]
        ans = ask(parent[x], parent[y]) + a[x] * a[y]
        if cnt[depth[y]] <= B:
            dp[x][pos[y]] = ans
        return ans

    out = []
    for _ in range(q):
        x, y = map(int, input_data.readline().split())
        out.append(str(ask(x, y)))

    return "\n".join(out)

# sample 1
assert run(
"""6 2
1 5 2 3 1 1
1 2 3 3 2
4 5
6 6
"""
) == "33\n27"

# minimum tree
assert run(
"""2 1
1 2
1
1 1
"""
) == "1"

# chain, same vertex
assert run(
"""4 1
1 2 3 4
1 2 3
4 4
"""
) == "30"

# star tree
assert run(
"""5 1
1 2 3 4 5
1 1 1 1
2 3
"""
) == "7"

# repeated query checks memoization path
assert run(
"""3 3
1 2 3
1 2
3 3
3 3
3 3
"""
) == "14\n14\n14"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum tree | 1 | Root handling and base case |
| Chain, same vertex | 30 | Deep recursion path |
| Star tree | 7 | Same-depth leaves with common root |
| Repeated identical queries | 14 each time | Memoized states reused correctly |

## Edge Cases

Consider the identical-vertex case:

```
4 1
1 2 3 4
1 2 3
4 4
```

The algorithm computes

`f(4,4) = 16 + f(3,3)`

`f(3,3) = 9 + f(2,2)`

`f(2,2) = 4 + f(1,1)`

`f(1,1) = 1 + f(0,0)`

which produces `30`. Nothing special is required because the recurrence naturally handles equal vertices.

Now consider a star:

```
5 1
1 2 3 4 5
1 1 1 1
2 3
```

The execution is

`f(2,3) = 2*3 + f(1,1)`

`f(1,1) = 1`

giving `7`.

This confirms that the algorithm correctly continues all the way to the root even when the queried vertices diverge immediately.

Finally, consider many vertices on the same depth. A star with `99999` leaves creates an enormous number of potential pairs. The algorithm never stores all pair values. It only caches states involving depths whose size is at most `B`, keeping memory at `O(n√n)` rather than `O(n²)`. This is exactly the situation the square root decomposition argument was designed to handle.
