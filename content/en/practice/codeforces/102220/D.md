---
title: "CF 102220D - Master of Data Structure"
description: "We have a tree whose vertices start with value zero. Each event either changes the values on every vertex of one simple path or asks for an aggregate over such a path."
date: "2026-08-17T22:32:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102220
codeforces_index: "D"
codeforces_contest_name: "The 13th Chinese Northeast Collegiate Programming Contest"
rating: 0
weight: 102220
solve_time_s: 360
verified: true
draft: false
---

[CF 102220D - Master of Data Structure](https://codeforces.com/problemset/problem/102220/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m  
**Verified:** yes  

## Solution
## Problem Understanding

We have a tree whose vertices start with value zero. Each event either changes the values on every vertex of one simple path or asks for an aggregate over such a path. The updates are deliberately mixed: addition is ordinary arithmetic, XOR is bitwise, and subtraction is conditional because a value smaller than the subtraction amount must remain unchanged. The queries ask for the path sum, path XOR, the difference between the maximum and minimum values, or the closest value on the path to a given integer.

The input contains up to five test cases. A tree may contain 500,000 vertices, while there are only 2,000 events. That asymmetry is the key constraint. The tree is too large to scan for every event. A direct implementation can touch 500,000 vertices per event, giving about 1,000,000,000 vertex operations in the worst case. Even though 2,000 is small, it is not small enough to compensate for a factor of 500,000. On the other hand, 2,000 events are small enough that a structure containing only a few thousand carefully selected tree vertices can be processed almost directly.

There are several easy-to-miss boundary cases. The first is a subtraction that should do nothing. For example,

```
1
1 2
1 1 1 5
3 1 1 7
4 1 1
```

The value becomes 5 after the first operation, and the subtraction by 7 is ignored because 5 is smaller than 7. The correct output is `5`. A careless implementation using `max(0, w-k)` would accidentally produce zero, which is not the specified operation.

The second case is XOR over an even number of equal values. Consider a two-vertex tree:

```
1
2 2
1 2
1 1 2 5
5 1 2
```

Both vertices become 5, but `5 XOR 5 = 0`, so the correct output is `0`. When a compressed tree edge represents several original vertices, the XOR contribution depends only on whether that multiplicity is odd or even.

The third case concerns compressed edges themselves. On a chain with five vertices,

```
1
5 2
1 2
2 3
3 4
4 5
1 1 5 3
4 1 5
```

all five vertices receive 3, so the answer is `15`. A virtual tree containing only vertices 1 and 5 would have one edge, but that edge represents the three internal vertices as well. Ignoring those omitted vertices would incorrectly return 6 instead of 15.

## Approaches

The straightforward solution stores the current value of every tree vertex. For an update, find the path between its two endpoints and visit every vertex on that path. For a query, visit the same path and calculate the requested aggregate. This is correct because every event is defined directly in terms of the vertices on one simple path.

The problem is the worst case. A path can contain all 500,000 vertices, and there can be 2,000 events. A brute-force implementation can consequently perform about

[
500000 \times 2000 = 10^9
]

vertex visits. The large value of `n` rules this out.

The useful observation is that the set of endpoints is tiny. Across all events there are only `2m` endpoint vertices, at most 4,000 when `m = 2000`. We can build a virtual tree containing every endpoint and every LCA needed to connect them. A virtual tree has at most about `4m` vertices, so at most 8,000 here. The same compression strategy is the central idea of the published solution for this problem.

There is one subtlety. We cannot simply discard the original vertices between two virtual-tree vertices. Suppose the virtual tree contains an edge from `a` to `b`, but the original tree path from `a` to `b` has ten internal vertices. Every relevant path either uses that whole chain or does not use it at all, because no endpoint or required LCA lies strictly inside the chain. All of those internal vertices therefore always have the same value. We can store one value for the entire compressed chain together with its number of vertices.

A virtual-tree vertex stores the value of that original vertex. A virtual-tree edge stores the value shared by all omitted internal vertices on the corresponding original-tree chain. The path between two endpoints can then be processed by climbing virtual-tree parents toward their LCA. Each virtual edge is visited once, rather than once for every original vertex it represents.

The two approaches can be summarized as follows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Virtual Tree | O(n log n + m²) | O(n log n) | Accepted |

## Algorithm Walkthrough

1. Root the original tree at vertex 1 and compute `parent`, `depth`, DFS order, and subtree sizes. The DFS order together with subtree size lets us test whether one vertex is an ancestor of another, which is needed while constructing the virtual tree.
2. Build a binary-lifting table for ancestors. This gives `LCA(u, v)` in O(log n), which is needed both while creating the virtual tree and while processing individual events.
3. Read all events before executing any of them. Collect both endpoints of every event. There are at most `2m` such vertices, so the complete relevant part of the tree is small even when the original tree has 500,000 vertices.
4. Sort the distinct endpoints by DFS order. For every two consecutive endpoints in that order, compute their LCA and add it to the relevant vertex set. Also add the root. After sorting and removing duplicates again, these vertices form exactly the critical vertices needed by the virtual tree.
5. Construct the virtual tree with a stack. Process the critical vertices in DFS order. The stack represents the current chain of virtual ancestors. For every new vertex, pop vertices until the stack top is an ancestor of the new vertex, then make that top the virtual parent.
6. For every virtual-tree edge from a child `x` to its virtual parent `p`, store two pieces of information. The child vertex `x` has its own value, while the edge stores the value of the original vertices strictly between `p` and `x`. Their count is

[
depth[x]-depth[p]-1.
]

The count can be zero, in which case the edge has no omitted vertices.

1. Process an update by finding the LCA of its endpoints. Climb from each endpoint toward the LCA through virtual parents. Every visited virtual vertex receives the update, and every corresponding compressed edge also receives the update. Finally, apply the update to the LCA itself.
2. For a query, perform the same two climbs. For every virtual vertex encountered, include one copy of its value. For every compressed edge, include its stored value with multiplicity `depth[x] - depth[parent[x]] - 1`. The sum is multiplied by that multiplicity, the XOR is included only when the multiplicity is odd, and the minimum, maximum, and distance-to-`k` calculations use the stored value once because every represented vertex has that same value.
3. For query type 4 return the accumulated sum. For type 5 return the accumulated XOR. For type 6 return `maximum - minimum`. For type 7 return the smallest absolute difference from `k`.

**Why it works.** Consider any compressed virtual-tree edge from `p` to `x`. By construction, no endpoint or required LCA lies strictly inside the original path from `p` to `x`. Every event path whose endpoints come from the collected endpoint set must either contain the entire internal chain or contain none of it. Consequently all internal vertices on that chain always undergo exactly the same sequence of updates, so they always have one common value. The virtual vertex values represent every critical original vertex individually, while every compressed edge represents all of its omitted internal vertices with their exact multiplicity. Every path operation is thus applied to exactly the same original vertices as in the uncompressed tree, and every query aggregates exactly those same vertices.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    t = int(input())
    output = []

    for _ in range(t):
        n, m = map(int, input().split())

        head = array('i', [-1]) * (n + 1)
        to = array('i', [0]) * (2 * (n - 1))
        nxt = array('i', [0]) * (2 * (n - 1))
        edge_count = 0

        for _ in range(n - 1):
            u, v = map(int, input().split())

            to[edge_count] = v
            nxt[edge_count] = head[u]
            head[u] = edge_count
            edge_count += 1

            to[edge_count] = u
            nxt[edge_count] = head[v]
            head[v] = edge_count
            edge_count += 1

        parent = array('i', [0]) * (n + 1)
        depth = array('i', [0]) * (n + 1)
        tin = array('i', [0]) * (n + 1)
        order = array('i')

        stack = [1]
        timer = 0

        while stack:
            x = stack.pop()
            timer += 1
            tin[x] = timer
            order.append(x)

            e = head[x]
            while e != -1:
                y = to[e]
                if y != parent[x]:
                    parent[y] = x
                    depth[y] = depth[x] + 1
                    stack.append(y)
                e = nxt[e]

        size = array('i', [1]) * (n + 1)
        for x in reversed(order):
            p = parent[x]
            if p:
                size[p] += size[x]

        log = n.bit_length()
        up = [parent]

        for _ in range(1, log):
            prev = up[-1]
            cur = array('i', [0]) * (n + 1)
            for i in range(1, n + 1):
                cur[i] = prev[prev[i]]
            up.append(cur)

        def lca(a, b):
            if depth[a] < depth[b]:
                a, b = b, a

            diff = depth[a] - depth[b]
            bit = 0
            while diff:
                if diff & 1:
                    a = up[bit][a]
                diff >>= 1
                bit += 1

            if a == b:
                return a

            for j in range(log - 1, -1, -1):
                ua = up[j][a]
                ub = up[j][b]
                if ua != ub:
                    a = ua
                    b = ub

            return parent[a]

        operations = []
        endpoints = []

        for _ in range(m):
            parts = list(map(int, input().split()))
            typ, u, v = parts[0], parts[1], parts[2]
            k = parts[3] if len(parts) == 4 else 0

            operations.append((typ, u, v, k))
            endpoints.append(u)
            endpoints.append(v)

        critical = sorted(set(endpoints), key=tin.__getitem__)

        extra = []
        for i in range(1, len(critical)):
            extra.append(lca(critical[i - 1], critical[i]))

        virtual_nodes = sorted(
            set(critical + extra + [1]),
            key=tin.__getitem__
        )

        def is_ancestor(a, b):
            return tin[a] <= tin[b] < tin[a] + size[a]

        vparent = [0] * (n + 1)
        edge_id = [0] * (n + 1)

        edge_value = [0]
        vstack = []

        for x in virtual_nodes:
            if not vstack:
                vstack.append(x)
                continue

            while not is_ancestor(vstack[-1], x):
                vstack.pop()

            p = vstack[-1]
            vparent[x] = p
            edge_id[x] = len(edge_value)
            edge_value.append(0)

            vstack.append(x)

        value = [0] * (n + 1)

        def change(x, k, typ):
            if typ == 1:
                return x + k
            if typ == 2:
                return x ^ k
            if x >= k:
                return x - k
            return x

        for typ, u, v, k in operations:
            if typ <= 3:
                a = lca(u, v)

                x = u
                while x != a:
                    value[x] = change(value[x], k, typ)
                    e = edge_id[x]
                    edge_value[e] = change(edge_value[e], k, typ)
                    x = vparent[x]

                x = v
                while x != a:
                    value[x] = change(value[x], k, typ)
                    e = edge_id[x]
                    edge_value[e] = change(edge_value[e], k, typ)
                    x = vparent[x]

                value[a] = change(value[a], k, typ)
                continue

            a = lca(u, v)

            total_sum = 0
            total_xor = 0
            maximum = -1
            minimum = 10**30
            closest = 10**30

            x = u
            while x != a:
                cur = value[x]

                total_sum += cur
                total_xor ^= cur
                if cur > maximum:
                    maximum = cur
                if cur < minimum:
                    minimum = cur
                d = abs(cur - k)
                if d < closest:
                    closest = d

                p = vparent[x]
                cnt = depth[x] - depth[p] - 1

                if cnt:
                    cur = edge_value[edge_id[x]]
                    total_sum += cnt * cur

                    if cnt & 1:
                        total_xor ^= cur

                    if cur > maximum:
                        maximum = cur
                    if cur < minimum:
                        minimum = cur

                    d = abs(cur - k)
                    if d < closest:
                        closest = d

                x = p

            x = v
            while x != a:
                cur = value[x]

                total_sum += cur
                total_xor ^= cur
                if cur > maximum:
                    maximum = cur
                if cur < minimum:
                    minimum = cur
                d = abs(cur - k)
                if d < closest:
                    closest = d

                p = vparent[x]
                cnt = depth[x] - depth[p] - 1

                if cnt:
                    cur = edge_value[edge_id[x]]
                    total_sum += cnt * cur

                    if cnt & 1:
                        total_xor ^= cur

                    if cur > maximum:
                        maximum = cur
                    if cur < minimum:
                        minimum = cur

                    d = abs(cur - k)
                    if d < closest:
                        closest = d

                x = p

            cur = value[a]
            total_sum += cur
            total_xor ^= cur

            if cur > maximum:
                maximum = cur
            if cur < minimum:
                minimum = cur

            d = abs(cur - k)
            if d < closest:
                closest = d

            if typ == 4:
                output.append(str(total_sum))
            elif typ == 5:
                output.append(str(total_xor))
            elif typ == 6:
                output.append(str(maximum - minimum))
            else:
                output.append(str(closest))

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    solve()
```

The adjacency structure uses three compact integer arrays instead of a Python list of lists. This matters because the original tree can contain 500,000 vertices and almost one million directed adjacency entries. The arrays keep the memory footprint substantially smaller.

The initial DFS is iterative rather than recursive. A tree can be a single chain of length 500,000, which would exceed Python's normal recursion limit and would also make recursive Python calls unnecessarily expensive.

The `parent`, `depth`, `tin`, and `size` arrays are enough to determine ancestry. For vertices `a` and `b`, `a` is an ancestor of `b` exactly when `tin[a] <= tin[b] < tin[a] + size[a]`. The subtree occupies one contiguous interval of DFS order.

Binary lifting is stored in `array('i')` objects because 500,000 vertices times roughly 19 levels is around ten million ancestor entries. A normal Python integer matrix would consume far more memory.

The virtual tree is built only once because every event is known before execution. This is a major advantage of the small value of `m`. The `vparent` array points from every virtual vertex toward its virtual parent, while `edge_id[x]` identifies the compressed edge immediately above `x`.

The value array is indexed by original vertex number, but only virtual vertices ever receive a nonzero value. The compressed edge values are stored separately because an edge may represent many original vertices, and those vertices must not be confused with the endpoint represented by the child virtual vertex.

For subtraction, the comparison is `x >= k`, not `x > k`. When `x == k`, the resulting value is zero. When `x < k`, the value remains unchanged.

For XOR queries, a compressed edge containing `cnt` equal values contributes that value when `cnt` is odd and contributes zero when `cnt` is even. This is exactly the parity property of repeated XOR.

Python integers have arbitrary precision, so the potentially large path sums do not require explicit 64-bit handling. The C++ implementation would need a 64-bit integer type, but Python's integer representation already handles the required range.

## Worked Examples

For the provided sample, the input shown in the statement represents one test case. With the test-case count included, it is:

```
1
5 8
5 2
5 1
2 4
2 3
1 4 4 5
3 4 4 1
2 3 1 4
6 3 5
4 2 5
5 1 3
6 5 4
7 1 4 2
```

The tree is a chain-like structure with vertex 2 connected to 3 and 4, and vertex 5 connected to 2 and 1.

| Event | Path | Values after event | Answer |
| --- | --- | --- | --- |
| `1 4 4 5` | `{4}` | `w4 = 5` |  |
| `3 4 4 1` | `{4}` | `w4 = 4` |  |
| `2 3 1 4` | `{3,2,5,1}` | `w1=w2=w3=w4=w5=4` |  |
| `6 3 5` | `{3,2,5}` | all three values are 4 | `0` |
| `4 2 5` | `{2,5}` | both values are 4 | `8` |
| `5 1 3` | `{1,5,2,3}` | four values are 4 | `0` |
| `6 5 4` | `{5,2,4}` | all three values are 4 | `0` |
| `7 1 4 2` | `{1,5,2,4}` | all four values are 4 | `2` |

The output is consequently `0`, `8`, `0`, `0`, and `2`. The trace demonstrates that XOR updates can completely erase the distinctions created by earlier arithmetic updates, so the data structure must store the actual current value rather than trying to summarize the history of operations.

For a second example, consider:

```
1
3 6
1 2
2 3
1 1 3 5
2 2 3 3
3 1 2 6
4 1 3
5 1 3
7 1 3 4
```

The state evolves as follows.

| Event | Path | Values after event | Answer |
| --- | --- | --- | --- |
| `1 1 3 5` | `{1,2,3}` | `(5,5,5)` |  |
| `2 2 3 3` | `{2,3}` | `(5,6,6)` |  |
| `3 1 2 6` | `{1,2}` | `(5,0,6)` |  |
| `4 1 3` | `{1,2,3}` | `(5,0,6)` | `11` |
| `5 1 3` | `{1,2,3}` | `(5,0,6)` | `3` |
| `7 1 3 4` | `{1,2,3}` | `(5,0,6)` | `1` |

The third event exercises conditional subtraction. Vertex 1 has value 5, which is smaller than 6, so it remains 5, while vertex 2 becomes zero. The final query asks for the closest value to 4, and 5 is at distance 1, so the answer is 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m²) | Binary lifting takes O(n log n), while at most O(m) virtual vertices are traversed by each of O(m) events |
| Space | O(n log n) | The binary-lifting table dominates the compact tree arrays |

There are at most `2m` original endpoints and at most one LCA for each consecutive pair after sorting, so the virtual tree contains at most about `4m + 1` vertices. With `m <= 2000`, that is at most roughly 8,000 virtual vertices. Processing all events therefore requires on the order of 16 million virtual-tree visits in the worst case, instead of one billion original-tree vertex visits. The large `n` is handled once during preprocessing, while the small `m` controls the expensive dynamic part.

## Test Cases

The following test harness assumes the submitted solution is saved as `solution.py`. The maximum-size case is generated rather than written out explicitly, so it still represents the full constraint.

```python
import io
import subprocess
import sys

def run(inp: str) -> str:
    result = subprocess.run(
        [sys.executable, "solution.py"],
        input=inp,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()

sample1 = """\
1
5 8
5 2
5 1
2 4
2 3
1 4 4 5
3 4 4 1
2 3 1 4
6 3 5
4 2 5
5 1 3
6 5 4
7 1 4 2
"""

assert run(sample1) == "0\n8\n0\n0\n2", "sample 1"

sample2 = """\
1
3 6
1 2
2 3
1 1 3 5
2 2 3 3
3 1 2 6
4 1 3
5 1 3
7 1 3 4
"""

assert run(sample2) == "11\n3\n1", "sample 2"

minimum_case = """\
1
1 5
1 1 1 5
3 1 1 7
4 1 1
2 1 1 3
5 1 1
"""

assert run(minimum_case) == "5\n6", "minimum-size and ignored subtraction"

equal_case = """\
1
4 6
1 2
2 3
3 4
1 1 4 7
4 1 4
5 1 4
6 1 4
7 1 4 5
3 1 4 7
"""

assert run(equal_case) == "28\n0\n0\n2", "all-equal values"

compressed_edge_case = """\
1
5 5
1 2
2 3
3 4
4 5
1 1 5 3
4 1 5
3 2 4 2
4 1 5
7 1 5 2
"""

assert run(compressed_edge_case) == "15\n9\n1", "compressed edge multiplicity"

n = 500000
edges = "\n".join(f"{i} {i + 1}" for i in range(1, n))
maximum_case = (
    f"1\n{n} 2\n"
    + edges
    + f"\n1 1 {n} 1\n4 1 {n}\n"
)

assert run(maximum_case) == str(n), "maximum-size chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Provided sample 1 | `0 8 0 0 2` | Combined arithmetic, XOR, range, sum, and nearest-value queries |
| Sample 2 | `11 3 1` | Conditional subtraction and mixed query types |
| Minimum-size case | `5 6` | A single vertex and subtraction when `w < k` |
| All-equal case | `28 0 0 2` | XOR parity, zero range, and nearest-value calculation |
| Compressed-edge case | `15 9 1` | Correct multiplicity of omitted virtual-tree vertices |
| Maximum-size chain | `500000` | Large `n` with a path containing the entire tree |

## Edge Cases

The conditional subtraction case is handled directly in `change`. For

```
1
1 2
1 1 1 5
3 1 1 7
4 1 1
```

the only vertex has value 5 after the first event. Since `5 < 7`, the second event returns the value unchanged, and the query outputs `5`. The implementation never replaces the value by zero unless the subtraction amount is exactly equal to the value.

The XOR multiplicity case is handled when a compressed edge is queried. Suppose an edge represents four original vertices, all with value 5. The code adds `5` to the XOR accumulator only when `cnt & 1` is true. Since four is even, the contribution is zero, matching `5 XOR 5 XOR 5 XOR 5 = 0`. This avoids expanding the compressed edge back into its original vertices.

The compressed-edge boundary case is handled by separating each virtual vertex from the internal vertices immediately below it. On

```
1
5 2
1 2
2 3
3 4
4 5
1 1 5 3
4 1 5
```

the virtual tree can consist essentially of vertices 1 and 5. Vertex 1 stores 3, vertex 5 stores 3, and the virtual edge stores 3 with multiplicity `5 - 1 - 1 = 3`. The query computes `3 + 3 * 3 + 3 = 15`, exactly matching all five original vertices.

The case `u = v` also requires care because the path contains exactly one vertex. The update loops from `u` toward the LCA, but when the endpoints are identical, `u == lca(u, v)` and both climbing loops execute zero times. The LCA itself is then updated exactly once. The same reasoning makes every query on a single vertex return that vertex's current value.

The root can be absent from every event endpoint. The construction explicitly inserts vertex 1 into the virtual tree so that every virtual vertex has a well-defined ancestor chain. This does not change any event path, because the root is only a structural vertex unless an actual path passes through it.

Finally, a compressed edge can have zero internal vertices. When two virtual vertices are adjacent in the original tree, `depth[x] - depth[parent[x]] - 1` equals zero. The code still assigns an edge value for uniformity, but query and update logic skips it whenever its multiplicity is zero. This prevents an artificial extra vertex from entering any answer.
