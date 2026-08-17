---
title: "CF 102218D - Dynamic Network"
description: "The computers form a rooted tree. Computer 1 exists initially and acts as the root. Every time a computer is added, it receives the next unused ID, so if there are currently curr computers, the new computer gets ID curr + 1."
date: "2026-08-17T23:15:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102218
codeforces_index: "D"
codeforces_contest_name: "2019, XI Annual Programming Contest by ESCOM-IPN"
rating: 0
weight: 102218
solve_time_s: 391
verified: false
draft: false
---

[CF 102218D - Dynamic Network](https://codeforces.com/problemset/problem/102218/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 31s  
**Verified:** no  

## Solution
## Problem Understanding

The computers form a rooted tree. Computer `1` exists initially and acts as the root. Every time a computer is added, it receives the next unused ID, so if there are currently `curr` computers, the new computer gets ID `curr + 1`. Its only new edge connects it to some already existing computer `p`.

Because every new vertex has exactly one edge to an older vertex, the network always remains a tree. The answer for a pair of computers is the number of vertices on their unique tree path, including both endpoints. For a newly inserted computer, the required answer is its path length in vertices from that computer to root `1`.

The input is deliberately encoded using the previous answer. Before decoding a query, `last` contains the answer to the preceding query, or zero initially. For an insertion, the actual parent is `(p' + last) % curr + 1`, where `curr` is the number of computers before insertion. For a path query, both endpoints are decoded with the current value of `curr`. This means the program cannot preprocess the queries independently, because the answer to one query changes the meaning of all subsequent encoded values.

There are at most `2 * 10^5` queries, so there are also at most `2 * 10^5` computers. A solution that spends linear time in the number of computers on every query could perform around `4 * 10^10` tree operations in the worst case, far beyond what a 2 second limit permits. We need roughly logarithmic time per operation. Since the tree only grows and a newly added vertex always attaches to an existing vertex, we can maintain ancestor information incrementally.

Several edge cases can silently break an implementation. If the queried endpoints are equal, the path contains exactly one computer. For example,

```
1
2 0 0
```

has only computer `1`, so the decoded query is `(1, 1)` and the answer is `1`. A distance formula that forgets to count endpoints can incorrectly return zero.

A second edge case is a new computer attached directly to the root. For example,

```
1
1 0
```

decodes the parent as `1`, creates computer `2`, and the answer is `2`, because the path is `2 -> 1`. An implementation that reports the number of edges instead of the number of computers would return `1`.

The encoding state is another source of errors. Consider

```
3
1 0
2 0 0
2 0 0
```

After the insertion, `last = 2`, so the first type 2 query decodes to `(1, 1)` and produces `1`. The next query must then use `last = 1`, so it also decodes differently from what it would have decoded with `last = 0`. Reading all queries first and decoding them without processing previous answers would produce the wrong tree or wrong endpoints.

Finally, the modulo base differs between insertion and later queries. For an insertion, `curr` is the number of existing computers, so the parent must be decoded before increasing `curr`. For a type 2 query, `curr` already includes every inserted computer. Mixing up this order causes an off-by-one error exactly when a new computer has just been added.

## Approaches

The direct approach is to store `parent[v]` and `depth[v]` for every computer. To answer a query, repeatedly move the deeper endpoint upward until both endpoints have the same depth, then move both upward until they meet. The meeting vertex is their lowest common ancestor. If its depth is `d`, the number of computers on the path is

`depth[u] + depth[v] - 2 * d + 1`.

This method is correct because every move follows an actual tree edge, and the first common ancestor reached after equalizing the depths is exactly the lowest common ancestor. The problem is the running time. A single query can require Θ(n) parent moves on a chain. With `2 * 10^5` computers and `2 * 10^5` queries, that can reach roughly `4 * 10^10` parent operations.

The key observation is that the tree is not arbitrary and static. Every new vertex is attached to an already existing vertex, so when vertex `v` is created, every ancestor of `v` can be derived from the already known ancestors of its parent. This lets us store not only the direct parent, but the `2^k`-th ancestor of every vertex.

For each vertex `v`, let `up[k][v]` denote its ancestor after `2^k` upward edges. When `v` is inserted with parent `p`, we know

`up[0][v] = p`

and for every larger `k`,

`up[k][v] = up[k-1][up[k-1][v]]`.

Thus all binary lifting information for a new computer can be computed immediately. A lowest common ancestor can then be found in O(log n), and every insertion also takes O(log n). The encoded nature of the input causes no additional algorithmic difficulty, because we process queries in order and update `last` immediately after every answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(QN) worst case | O(N) | Too slow |
| Optimal | O(Q log N) | O(N log N) | Accepted |

## Algorithm Walkthrough

1. Initialize the tree with computer `1`. Its depth is zero, and every ancestor entry can point to `1`, which acts as the root's own ancestor.
2. Process the queries in their given order while maintaining `curr`, the number of existing computers, and `last`, the previous answer. The queries must be processed online because `last` participates in decoding the next query.
3. For a type 1 query, decode the parent using `(p' + last) % curr + 1`. The modulo uses the old value of `curr`, because the new computer does not exist yet.
4. Assign the new computer ID `curr + 1`, set its depth to `depth[parent] + 1`, and set its direct parent to the decoded parent.
5. Build the new computer's binary lifting table. Its `2^k`-th ancestor is obtained by taking the `2^(k-1)`-th ancestor twice. This is possible in O(log N) because every referenced ancestor was created earlier.
6. The path from the new computer to root `1` contains `depth[new] + 1` computers. Print this value and set `last` to it.
7. For a type 2 query, decode both endpoints using the current `curr`, since both computers already belong to the network.
8. Find their lowest common ancestor with binary lifting. First equalize their depths by lifting the deeper vertex by the appropriate powers of two. If the vertices are then equal, that vertex itself is their lowest common ancestor.
9. Otherwise, inspect the lifting levels from largest to smallest. Whenever the `2^k`-th ancestors of the two vertices differ, move both vertices to those ancestors. After all levels have been processed, the two vertices are distinct children of their lowest common ancestor, so their direct parent is the LCA.
10. Convert the LCA into the requested number of computers with `depth[u] + depth[v] - 2 * depth[lca] + 1`. Print the result and store it in `last`.

### Why it works

The invariant is that for every existing computer `v` and every lifting level `k`, `up[k][v]` is exactly the ancestor reached after `2^k` parent edges. This holds for the root initially and remains true for every new vertex because its level `k` ancestor is constructed by applying two correct level `k-1` jumps.

Binary lifting first moves the deeper query vertex to the same depth as the other vertex, so afterwards both vertices are equally far from the root. If they are equal, that vertex is their LCA. Otherwise, processing powers of two from largest to smallest moves both vertices upward without crossing their LCA, while making their ancestors as high as possible while still remaining different. The vertices finally reached are the two children immediately below the LCA, so their common parent is the correct LCA.

For any two vertices, the number of edges on their path is `depth[u] + depth[v] - 2 * depth[lca]`. The problem asks for computers rather than edges, so exactly one must be added. The same formula specialized to the root gives `depth[v] + 1`, which is why insertion queries can be answered directly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())

    LOG = 19
    max_nodes = q + 1

    up = [[1] * max_nodes for _ in range(LOG)]
    depth = [0] * max_nodes

    curr = 1
    last = 0
    out = []

    for _ in range(q):
        data = list(map(int, input().split()))
        t = data[0]

        if t == 1:
            p_encoded = data[1]

            parent = (p_encoded + last) % curr + 1
            v = curr + 1

            depth[v] = depth[parent] + 1
            up[0][v] = parent

            for k in range(1, LOG):
                up[k][v] = up[k - 1][up[k - 1][v]]

            curr += 1

            last = depth[v] + 1
            out.append(str(last))

        else:
            u_encoded = data[1]
            v_encoded = data[2]

            u = (u_encoded + last) % curr + 1
            v = (v_encoded + last) % curr + 1

            if depth[u] < depth[v]:
                u, v = v, u

            diff = depth[u] - depth[v]

            bit = 0
            while diff:
                if diff & 1:
                    u = up[bit][u]
                diff >>= 1
                bit += 1

            if u == v:
                lca = u
            else:
                for k in range(LOG - 1, -1, -1):
                    if up[k][u] != up[k][v]:
                        u = up[k][u]
                        v = up[k][v]

                lca = up[0][u]

            last = depth[u] + depth[v] - 2 * depth[lca] + 1
            out.append(str(last))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `up` array has one row for every power of two. With at most `2 * 10^5` queries, there are at most `200001` computers, and `2^18 = 262144`, so 19 levels are enough to represent every possible depth.

When a new vertex is inserted, `up[0][v]` is its decoded parent. Every higher entry is filled from already computed entries, so no information about future vertices is required.

The insertion answer is computed after `curr` is increased, but the parent is decoded before that increment. This ordering is essential. The new ID is `old_curr + 1`, while the valid parent IDs are exactly `1` through `old_curr`.

For a type 2 query, the endpoints are decoded before any LCA work. The current value of `curr` is already the number of computers in the network, so both modulo operations use that value.

The code equalizes depths using the binary representation of their difference. Once the depths match, it either handles the equal-vertex case immediately or lifts both vertices from the largest power of two downward. Python integers do not overflow, so no special integer-width handling is necessary.

The variable names `u` and `v` are temporarily changed while finding the LCA. After they are equalized, they may no longer represent the original endpoints. This does not cause a problem because their original depths are still needed only through the depth values before the LCA search. In this implementation, after equalization the deeper endpoint may have moved, so the final distance formula uses the depths of the current vertices. That is not sufficient for arbitrary queries, because the current vertices can have smaller depths than the originals.

To avoid that issue, the implementation above must preserve the original endpoint depths before modifying the vertices. The corrected implementation is below.

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())

    LOG = 19
    max_nodes = q + 2

    up = [[1] * max_nodes for _ in range(LOG)]
    depth = [0] * max_nodes

    curr = 1
    last = 0
    out = []

    for _ in range(q):
        data = list(map(int, input().split()))
        t = data[0]

        if t == 1:
            p_encoded = data[1]

            parent = (p_encoded + last) % curr + 1
            v = curr + 1

            depth[v] = depth[parent] + 1
            up[0][v] = parent

            for k in range(1, LOG):
                up[k][v] = up[k - 1][up[k - 1][v]]

            curr += 1

            last = depth[v] + 1
            out.append(str(last))

        else:
            u = (data[1] + last) % curr + 1
            v = (data[2] + last) % curr + 1

            original_u = u
            original_v = v

            if depth[u] < depth[v]:
                u, v = v, u

            diff = depth[u] - depth[v]
            bit = 0

            while diff:
                if diff & 1:
                    u = up[bit][u]
                diff >>= 1
                bit += 1

            if u == v:
                lca = u
            else:
                for k in range(LOG - 1, -1, -1):
                    if up[k][u] != up[k][v]:
                        u = up[k][u]
                        v = up[k][v]

                lca = up[0][u]

            last = (
                depth[original_u]
                + depth[original_v]
                - 2 * depth[lca]
                + 1
            )
            out.append(str(last))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The second version is the one to submit. Preserving `original_u` and `original_v` is a subtle but necessary implementation detail. The vertices used during LCA lifting are working variables, and their depths after lifting are not necessarily the original endpoint depths.

## Worked Examples

### Sample 1

The four insertion queries construct the tree `1` as the root, with computers `2` and `3` attached to `1`, followed by computers `4` and `5` attached to `2`.

| Query | Type | Decoded parent / endpoints | `curr` after query | `last` |
| --- | --- | --- | --- | --- |
| `1 0` | 1 | parent `1`, new `2` | 2 | 2 |
| `1 2` | 1 | parent `1`, new `3` | 3 | 2 |
| `1 2` | 1 | parent `2`, new `4` | 4 | 3 |
| `1 2` | 1 | parent `2`, new `5` | 5 | 3 |
| `2 0 4` | 2 | `(4, 3)` | 5 | 4 |
| `2 1 2` | 2 | `(1, 2)` | 5 | 2 |
| `2 2 1` | 2 | `(5, 4)` | 5 | 3 |

For the first four queries, the insertion answers are the depths plus one, giving `2, 2, 3, 3`. The query from `4` to `3` has LCA `1`, so its path is `4 -> 2 -> 1 -> 3`, containing four computers. The last two paths contain two and three computers respectively.

### Sample 2

The first insertion is encoded with `last = 0`, so `p = (1 + 0) % 1 + 1 = 1`, creating computer `2` under the root. Its answer is `2`, and that answer changes how the next query is decoded.

| Query | Type | Decoded parent / endpoints | `curr` after query | `last` |
| --- | --- | --- | --- | --- |
| `1 1` | 1 | parent `1`, new `2` | 2 | 2 |
| `2 1 2` | 2 | `(2, 1)` | 2 | 2 |
| `1 0` | 1 | parent `1`, new `3` | 3 | 2 |
| `1 1` | 1 | parent `1`, new `4` | 4 | 2 |
| `2 0 3` | 2 | `(3, 2)` | 4 | 3 |
| `2 2 2` | 2 | `(2, 2)` | 4 | 1 |

The second query is decoded using `last = 2`, and the final query demonstrates the equal-endpoint case. Since both endpoints are computer `2`, the unique path contains exactly one computer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(Q log Q) | Every insertion fills `O(log Q)` ancestors, and every LCA query uses `O(log Q)` lifting operations. |
| Space | O(Q log Q) | The binary lifting table stores `O(log Q)` ancestors for each of at most `Q + 1` computers. |

With `Q <= 2 * 10^5`, the lifting table has only about `200001 * 19` integer entries. Every query performs at most a few dozen ancestor operations, which is appropriate for the 2 second limit, while the brute-force approach can require tens of billions of parent traversals.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    q = int(input())

    LOG = 19
    max_nodes = q + 2

    up = [[1] * max_nodes for _ in range(LOG)]
    depth = [0] * max_nodes

    curr = 1
    last = 0
    out = []

    for _ in range(q):
        data = list(map(int, input().split()))
        t = data[0]

        if t == 1:
            parent = (data[1] + last) % curr + 1
            v = curr + 1

            depth[v] = depth[parent] + 1
            up[0][v] = parent

            for k in range(1, LOG):
                up[k][v] = up[k - 1][up[k - 1][v]]

            curr += 1
            last = depth[v] + 1
            out.append(str(last))

        else:
            u = (data[1] + last) % curr + 1
            v = (data[2] + last) % curr + 1

            original_u = u
            original_v = v

            if depth[u] < depth[v]:
                u, v = v, u

            diff = depth[u] - depth[v]
            bit = 0

            while diff:
                if diff & 1:
                    u = up[bit][u]
                diff >>= 1
                bit += 1

            if u == v:
                lca = u
            else:
                for k in range(LOG - 1, -1, -1):
                    if up[k][u] != up[k][v]:
                        u = up[k][u]
                        v = up[k][v]
                lca = up[0][u]

            last = (
                depth[original_u]
                + depth[original_v]
                - 2 * depth[lca]
                + 1
            )
            out.append(str(last))

    return "\n".join(out)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

sample1 = """7
1 0
1 2
1 2
1 2
2 0 4
2 1 2
2 2 1
"""

sample2 = """6
1 1
2 1 2
1 0
1 1
2 0 3
2 2 2
"""

assert run(sample1) == "2\n2\n3\n3\n4\n2\n3", "sample 1"
assert run(sample2) == "2\n2\n2\n2\n3\n1", "sample 2"

minimum_case = """1
2 0 0
"""
assert run(minimum_case) == "1", "single root, equal endpoints"

root_children = """4
1 0
1 0
2 0 0
2 1 0
"""
assert run(root_children) == "2\n2\n1\n2", "root children and equal endpoints"

chain_case = """6
1 0
1 0
1 0
2 0 0
2 0 1
2 1 2
"""
assert run(chain_case) == "2\n3\n4\n1\n4\n2", "deep chain"

maximum_case = "200000\n" + "\n".join(["1 0"] * 199999)
expected = "\n".join(str(i) for i in range(2, 200001))
assert run(maximum_case) == expected, "maximum-size chain"

all_equal_case = """8
1 0
2 0 0
2 1 1
1 0
2 0 0
2 1 1
1 0
2 0 0
"""
assert run(all_equal_case) == "2\n1\n1\n2\n1\n1\n2\n1", "repeated equal endpoints"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 2 0 0` | `1` | Minimum network and equal endpoints |
| `1 0 / 1 0 / 2 0 0 / 2 1 0` | `2, 2, 1, 2` | Multiple root children and endpoint decoding |
| Three consecutive `1 0` insertions followed by path queries | `2, 3, 4, 1, 4, 2` | Deep chain and long LCA paths |
| `199999` consecutive `1 0` insertions | Depth sequence from `2` through `200000` | Maximum input size and logarithmic preprocessing |
| Repeated insertions and equal-endpoint queries | `2, 1, 1, 2, 1, 1, 2, 1` | Repeated `last` values and the `u = v` boundary case |

## Edge Cases

The single-root case is handled before any insertion. For

```
1
2 0 0
```

`curr = 1` and `last = 0`, so both encoded endpoints become `1`. The LCA is `1`, and the answer is `0 + 0 - 2 * 0 + 1 = 1`.

A direct child of the root has depth one. For

```
1
1 0
```

the parent is `(0 + 0) % 1 + 1 = 1`, and the new vertex has depth `1`. The required number of computers is `1 + 1 = 2`. The parent is decoded before `curr` becomes `2`, which prevents the modulo base from being accidentally changed.

A long chain tests whether the implementation really performs logarithmic LCA queries rather than walking parents one by one. For example,

```
3
1 0
1 0
1 0
```

creates `1 -> 2 -> 3 -> 4`, and the three insertion answers are `2`, `3`, and `4`. A later query between `4` and `1` has LCA `1`, so its answer is `4`.

Equal endpoints exercise a different branch of the LCA algorithm. If both decoded endpoints are `v`, their lowest common ancestor is immediately `v`. The distance has zero edges, but the requested answer is one computer, so the final `+1` is necessary.

The encoded input can also make two identical encoded values represent different actual vertices at different times because `last` changes. For example,

```
3
1 0
2 0 0
2 0 0
```

starts with computer `1`, inserts computer `2`, and obtains `last = 2`. The first type 2 query decodes both endpoints as `1`, producing answer `1`. Now `last = 1`, so the next identical encoded query uses `(0 + 1) % 2 + 1 = 2` for both endpoints and produces another answer of `1`. Processing and updating `last` immediately is what makes these two identical-looking queries behave correctly.
