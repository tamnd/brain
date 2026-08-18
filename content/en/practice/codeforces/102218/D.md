---
title: "CF 102218D - Dynamic Network"
description: "The network is a tree that grows one computer at a time. Computer 1 exists initially. Every new computer receives the next unused id, so when there are currently curr computers, the new computer gets id curr + 1. It is attached by one edge to an already existing computer."
date: "2026-08-18T22:46:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102218
codeforces_index: "D"
codeforces_contest_name: "2019, XI Annual Programming Contest by ESCOM-IPN"
rating: 0
weight: 102218
solve_time_s: 870
verified: false
draft: false
---

[CF 102218D - Dynamic Network](https://codeforces.com/problemset/problem/102218/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 14m 30s  
**Verified:** no  

## Solution
## Problem Understanding

The network is a tree that grows one computer at a time. Computer 1 exists initially. Every new computer receives the next unused id, so when there are currently `curr` computers, the new computer gets id `curr + 1`. It is attached by one edge to an already existing computer.

A query of type 1 specifies the parent of the new computer indirectly. A query of type 2 asks for the shortest path between two existing computers. The answer counts computers rather than edges, so a path containing `k` edges has answer `k + 1`.

The input is deliberately encoded using the previous answer. If `last` is the most recent answer and there are `curr` existing computers, a type 1 value `p'` represents parent

[
p=(p'+last)\bmod curr+1.
]

For type 2, the two endpoints are decoded in exactly the same way. This means the queries must be processed strictly online. We cannot decode all queries first and then preprocess the final tree, because the value needed to decode the next query is produced by the current query.

There can be up to (2\cdot10^5) operations, so the final tree also has at most (2\cdot10^5+1) computers. A solution that walks through a whole root-to-node path for every query can take (O(Q^2)) time. With (Q=2\cdot10^5), that can reach roughly (4\cdot10^{10}) parent traversals, far beyond what a two-second limit permits. We need logarithmic work per operation.

The tree structure gives us a particularly useful property: every newly created vertex is a leaf, and its parent already exists. Consequently, all information about the new vertex can be computed immediately from its parent. We never have to rebuild or traverse the existing tree after an insertion.

There are several edge cases that can silently break an implementation. The first is querying the same computer twice. For example,

```
1
2 0 0
```

There is only computer 1, so both decoded endpoints are 1 and the correct output is `1`. The distance in edges is zero, but the problem asks for the number of computers, so the answer is one. An implementation that forgets the final `+1` would print zero.

The second edge case is a newly added computer whose parent is the largest currently valid id. Consider

```
4
1 0
1 1
2 0 0
2 0 1
```

The first insertion creates computer 2 under computer 1 and outputs `2`. The second insertion has `last=2`, so its parent is `(1+2)%2+1=2`, creating computer 3 under computer 2 and outputting `3`. The third query decodes to `(1,1)` and outputs `1`. The final query decodes to `(2,3)`, whose path is `2-3`, so the output is `2`. The correct output is

```
2
3
1
2
```

A common off-by-one error is to use the value of `curr` after incrementing it when decoding the parent. The parent must be decoded using the number of computers before the new vertex is inserted.

The third edge case is that `last` changes after every query, including type 2 queries. For example,

```
3
1 0
2 0 0
2 0 0
```

After the insertion, `last=2`. The next query decodes both endpoints as 1 and outputs `1`, so `last` becomes 1. The final query therefore still has both endpoints equal to 2 only if the current number of computers and encoded values produce that result. Reusing an older `last` value would decode subsequent queries incorrectly. The encoding is part of the state of the algorithm, not merely input preprocessing.

## Approaches

The direct solution is to store the parent of every computer and, for a query between `u` and `v`, walk upward from both vertices until their paths meet. This is correct because the network is always a tree, so there is exactly one path between two computers. If we can find their lowest common ancestor, the number of edges on the path is

[
depth[u]+depth[v]-2\cdot depth[lca].
]

Adding one gives the required number of computers.

The problem is the running time. Consider a tree that is just one long chain. A query involving the deepest computer can require (O(n)) parent steps. If the tree has (2\cdot10^5) vertices and we make (2\cdot10^5) such queries, the total can be about (4\cdot10^{10}) operations. The brute-force method is correct, but it is fundamentally too slow.

The observation that changes the problem is that insertions only add leaves. When a new computer `x` is attached to an existing parent `p`, its entire ancestor chain can be summarized immediately. Store `up[k][x]`, the ancestor of `x` obtained by moving upward (2^k) edges. Since `p` is already known, the recurrence is

[
up[0][x]=p
]

and

[
up[k][x]=up[k-1][up[k-1][x]].
]

No existing vertex changes when `x` is inserted, so all previously computed binary-lifting information remains valid forever.

This is exactly the setting where binary lifting works well. It lets us find an LCA in (O(\log n)) time by first moving the deeper vertex upward until both vertices have equal depth, then lifting both vertices together from large jumps to small jumps. The insertion itself also takes (O(\log n)), because we compute the new vertex's ancestors for all powers of two.

The encoded input does not change the data structure. It only requires that we decode a query before processing it, calculate its answer, and immediately store that answer in `last` for the next query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(Q^2)) worst case | (O(Q)) | Too slow |
| Optimal | (O(Q\log Q)) | (O(Q\log Q)) | Accepted |

## Algorithm Walkthrough

1. Initialize computer 1 as the root. Set its depth to zero and initialize every binary-lifting ancestor to zero. The root has no real parent, so zero is a convenient sentinel.
2. Keep `curr` equal to the number of computers currently present and `last` equal to the previous answer. Initially both have the required values, `curr=1` and `last=0`.
3. For a type 1 query, decode the parent using `(p_prime + last) % curr + 1` before changing `curr`. The new computer has id `curr + 1`, because ids are assigned consecutively.
4. Set the new computer's depth to `depth[parent] + 1` and its immediate parent to `parent`. Then compute every higher ancestor with `up[k][new] = up[k-1][up[k-1][new]]`. This works because every vertex referenced on the right side already existed before the insertion.
5. The new computer's path to computer 1 contains `depth[new] + 1` computers. Set this value as `last` and output it. Since the root has depth zero, a vertex at depth `d` has exactly `d+1` vertices on its path to the root.
6. For a type 2 query, decode both endpoints using the current `last` and `curr`. Both endpoints are guaranteed to refer to existing computers because the modulo is taken by the current number of vertices.
7. Find the LCA of the decoded endpoints. First lift the deeper endpoint until the depths match. Then inspect binary-lifting levels from largest to smallest and lift both endpoints whenever their corresponding ancestors differ. After this process, their immediate parent is the LCA.
8. Compute the number of edges between the endpoints as `depth[u] + depth[v] - 2 * depth[lca]`. Add one because both endpoints are counted, store the result in `last`, and output it.

### Why it works

The key invariant is that for every existing computer `v`, `depth[v]` is its exact distance in edges from computer 1, and `up[k][v]` is its exact (2^k)-th ancestor. When a new leaf is inserted, its parent is already valid, so the recurrence computes all of the new ancestor values correctly without modifying any old values. Binary lifting then finds the true LCA because equalizing depths puts both vertices at the same level, and the subsequent largest-to-smallest jumps move them upward without crossing their LCA. The standard tree distance formula consequently gives the exact number of edges, and adding one gives exactly the number of computers on the path.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAX_Q = 200000
MAX_N = MAX_Q + 1
LOG = MAX_N.bit_length()

def solve():
    q = int(input())

    depth = [0] * (MAX_N + 1)
    up = [[0] * (MAX_N + 1) for _ in range(LOG)]

    curr = 1
    last = 0

    out = []

    for _ in range(q):
        parts = input().split()
        t = int(parts[0])

        if t == 1:
            p_prime = int(parts[1])

            # Decode using the number of computers before insertion.
            parent = (p_prime + last) % curr + 1

            new_node = curr + 1
            depth[new_node] = depth[parent] + 1
            up[0][new_node] = parent

            for k in range(1, LOG):
                mid = up[k - 1][new_node]
                up[k][new_node] = up[k - 1][mid]

            curr += 1

            last = depth[new_node] + 1
            out.append(str(last))

        else:
            u_prime = int(parts[1])
            v_prime = int(parts[2])

            u = (u_prime + last) % curr + 1
            v = (v_prime + last) % curr + 1

            if depth[u] < depth[v]:
                u, v = v, u

            # Bring u to the same depth as v.
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

The `depth` array uses zero-based tree depth, so computer 1 has depth zero. This makes the standard distance formula particularly clean. The requested answer is then the edge distance plus one.

`up[0][v]` stores the direct parent, while `up[k][v]` stores the ancestor (2^k) edges above `v`. The number of levels is `MAX_N.bit_length()`. With at most `200001` computers, this gives enough levels to represent every possible depth difference and every possible LCA jump.

For an insertion, `curr` still represents the old number of computers while the parent is decoded. Only after all information for the new computer has been computed do we increment `curr`. This ordering is required by the encoding formula.

For a type 2 query, the endpoints are decoded before any LCA work. The deeper endpoint is then lifted according to the set bits of the depth difference. If the vertices become equal, that vertex is already the LCA. Otherwise, the loop considers jumps from largest to smallest. When `up[k][u]` and `up[k][v]` differ, both vertices can safely move upward by (2^k), because their LCA is still above those two distinct ancestors. Eventually they become children of the LCA.

Python integers do not overflow for the values used here. The largest intermediate value in the decoding formula is only a few hundred thousand, and the distance is at most the number of computers.

## Worked Examples

### Sample 1

The first four operations create the tree described by the decoded operations. The table tracks the number of computers before each operation, the previous answer, the decoded parent or endpoints, and the resulting answer.

| Step | Type | `curr` before | `last` before | Decoded operation | New `curr` | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | new 2 under 1 | 2 | 2 |
| 2 | 1 | 2 | 2 | new 3 under 1 | 3 | 2 |
| 3 | 1 | 3 | 2 | new 4 under 2 | 4 | 3 |
| 4 | 1 | 4 | 3 | new 5 under 2 | 5 | 3 |
| 5 | 2 | 5 | 3 | query 4, 3 | 5 | 4 |
| 6 | 2 | 5 | 4 | query 1, 2 | 5 | 2 |
| 7 | 2 | 5 | 2 | query 5, 4 | 5 | 3 |

After the first insertion, computer 2 is one edge from the root, so its root path contains two computers. The second insertion also attaches to computer 1. The third and fourth insertions attach to computer 2, producing depths 2 for computers 4 and 5.

For the first distance query, the path is `4 -> 2 -> 1 -> 3`, containing four computers. The LCA is computer 1. The final query asks for computers 5 and 4, which share computer 2 as their parent, so the path contains `5 -> 2 -> 4`, giving three computers.

### Sample 2

Here the encoded values depend on answers from both insertion and distance queries, so it is useful to explicitly track `last`.

| Step | Type | `curr` before | `last` before | Decoded operation | New `curr` | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | new 2 under 1 | 2 | 2 |
| 2 | 2 | 2 | 2 | query 1, 2 | 2 | 2 |
| 3 | 1 | 2 | 2 | new 3 under 1 | 3 | 2 |
| 4 | 1 | 3 | 2 | new 4 under 1 | 4 | 2 |
| 5 | 2 | 4 | 2 | query 3, 4 | 4 | 3 |
| 6 | 2 | 4 | 3 | query 2, 2 | 4 | 1 |

The second operation decodes to endpoints 1 and 2. Its answer is two, which becomes the `last` value used by the third operation. The fifth operation has endpoints 3 and 4, both children of computer 1, so their path contains three computers. The final query decodes both endpoints to computer 2, demonstrating the zero-distance case and producing one as required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(Q\log Q)) | Every insertion computes (O(\log Q)) ancestors, and every distance query performs (O(\log Q)) LCA work. |
| Space | (O(Q\log Q)) | The binary-lifting table stores (O(\log Q)) ancestors for each of at most (Q+1) computers. |

With (Q\le2\cdot10^5), the logarithmic factor is below twenty. The algorithm performs only a small constant amount of work at each binary-lifting level, so the total is suitable for the two-second limit. The table also fits comfortably within 256 MB in the Python implementation.

## Test Cases

```python
# This test block is intended to be placed after the solution code.
# It reuses solve() and captures its output.

import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run("""7
1 0
1 2
1 2
1 2
2 0 4
2 1 2
2 2 1
""") == """2
2
3
3
4
2
3""", "sample 1"

# Provided sample 2
assert run("""6
1 1
2 1 2
1 0
1 1
2 0 3
2 2 2
""") == """2
2
2
2
3
1""", "sample 2"

# Minimum-size input, querying the only existing computer.
assert run("""1
2 0 0
""") == """1""", "single vertex"

# Repeated identical queries. They all decode to the same vertex.
assert run("""4
2 0 0
2 0 0
2 0 0
2 0 0
""") == """1
1
1
1""", "all equal endpoints"

# Exercises parent == curr and then a query involving the deepest vertices.
assert run("""4
1 0
1 1
2 0 0
2 0 1
""") == """2
3
1
2""", "boundary parent and self query"

# Maximum number of operations. There is only one computer, so every query
# must decode to (1, 1) and answer 1.
max_q = 200000
max_input = str(max_q) + "\n" + "2 0 0\n" * max_q
max_expected = "1\n" * max_q
assert run(max_input) == max_expected, "maximum query count"

# Large encoded values with curr = 1. Modulo must reduce them correctly.
assert run("""3
1 200000
2 200000 200000
2 0 0
""") == """2
1
1""", "maximum encoded values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 2 0 0` | `1` | Minimum tree size and the `+1` converting edges to computers |
| Four `2 0 0` queries | `1 1 1 1` | Repeated decoding and the case `u = v` |
| Two insertions followed by two queries | `2 3 1 2` | Parent equal to the largest valid id, depth handling, and endpoint decoding |
| `200000` identical type 2 queries | `1` repeated 200000 times | Maximum operation count and online processing |
| Insert and queries using `200000` | `2 1 1` | Boundary values in encoded input and modulo behavior |

## Edge Cases

The single-computer case is handled because the root has depth zero and every query on it has distance zero edges. The implementation adds one when converting the distance into a number of computers. For

```
1
2 0 0
```

both endpoints decode to 1, `lca=1`, and the answer is `0+0-2*0+1=1`.

The self-query case does not require a special data structure operation. When `u == v`, the depth equalization makes them equal immediately, so the LCA is that same vertex. The distance formula becomes `depth[u] + depth[u] - 2*depth[u] + 1`, which is one. Thus

```
4
2 0 0
2 0 0
2 0 0
2 0 0
```

produces four lines containing `1`, even though `last` changes after each query.

The parent boundary case is controlled by the modulo formula. In

```
4
1 0
1 1
2 0 0
2 0 1
```

the first insertion uses parent 1. Its answer is 2, so the second insertion decodes its parent as `(1+2)%2+1=2`. The new computer therefore has depth 2 and answer 3. After the next query, `last` becomes 1, and the final encoded endpoints become 2 and 3. Their path contains exactly two computers. The algorithm obtains these results without ever walking the complete path.

The ordering of `curr` is another subtle boundary condition. Suppose there are two computers before an insertion. The parent must be decoded with modulo 2, because only ids 1 and 2 currently exist. Incrementing `curr` first would incorrectly allow the formula to select the not-yet-created computer 3. The implementation computes `parent` first, constructs `new_node`, and only then increments `curr`.

Finally, the encoded input must be processed online. A query can change `last`, and that value changes the meaning of every subsequent encoded number. For example, in Sample 1 the first insertion produces `last=2`; the second insertion's raw parent value is `2`, but its actual parent is `(2+2)%2+1=1`. Any implementation that decodes all operations with `last=0`, or with the final answer instead of the previous answer, constructs a different tree and consequently gives different results.
