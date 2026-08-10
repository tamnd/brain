---
title: "CF 102409C - Xor in Tree"
description: "We have a weighted tree with (N) vertices. Each edge stores an integer, and for any two vertices we define their path value as the XOR of all edge weights on the unique path connecting them. The task is to add these path values over every unordered pair of distinct vertices."
date: "2026-08-10T15:15:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102409
codeforces_index: "C"
codeforces_contest_name: "Semana i 2019"
rating: 0
weight: 102409
solve_time_s: 417
verified: true
draft: false
---

[CF 102409C - Xor in Tree](https://codeforces.com/problemset/problem/102409/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a weighted tree with (N) vertices. Each edge stores an integer, and for any two vertices we define their path value as the XOR of all edge weights on the unique path connecting them. The task is to add these path values over every unordered pair of distinct vertices.

The tree structure gives us a crucial property: between any two vertices there is exactly one path. The challenge is not finding an individual path, but avoiding the enormous number of paths when (N) reaches (10^5).

With (10^5) vertices, there are almost (5\times10^9) unordered pairs. Even an (O(N^2)) algorithm is already too slow, before considering any work required to process each path. A solution close to linear time is needed. The edge weights are at most (10^9), so every relevant XOR fits within 30 bits, since (10^9 < 2^{30}). This makes a per-bit counting strategy practical.

There are several small cases where an implementation can silently go wrong. The first is a tree containing a single vertex:

```
1
```

There are no pairs of distinct vertices, so the answer is (0). Code that assumes at least one edge can fail on this case.

Another useful case is a tree with two vertices:

```
2
1 2 1000000000
```

The only pair has path XOR (1000000000), so the answer is (1000000000). This checks both the pair counting and the upper boundary of the edge weight.

A third case is:

```
3
1 2 1
2 3 2
```

The three pair values are (1), (2), and (1\oplus2=3), giving an answer of (6). A careless implementation that treats path XOR like an ordinary sum would produce (1+2+(1+2)=6) here by coincidence, so a less symmetric example is useful for testing the actual XOR operation.

Finally, consider equal edge weights:

```
4
1 2 7
1 3 7
1 4 7
```

Each leaf has root-XOR value (7), while the root has value (0). The three root-to-leaf pairs contribute (7) each, while every leaf-to-leaf path has XOR (7\oplus7=0). The correct answer is (21). Counting edges instead of XOR values would incorrectly assign (14) to a leaf-to-leaf path.

## Approaches

A direct solution can start from every pair of vertices, find its unique path, XOR the edge weights along that path, and add the result to the answer. This is correct because it evaluates exactly the quantity requested for every pair.

The problem is the amount of repeated work. In a path-shaped tree, two vertices near opposite ends can have a path containing almost (N) edges. There are (N(N-1)/2) pairs, so processing each path independently can require on the order of

[
\frac{N(N-1)}{2}(N-1)=O(N^3)
]

edge visits. For (N=10^5), this is roughly (5\times10^{14}) edge operations in the worst case, far beyond what the time limit permits. Even a more efficient implementation that finds every pair using precomputed tree information would still have (O(N^2)) pairs, which is too many.

The key observation is that XOR paths can be represented using a value attached to each vertex. Choose vertex (1) as an arbitrary root and define

[
A[v]=\text{XOR of all edge weights on the path from }1\text{ to }v.
]

Suppose the paths from the root to (u) and (v) meet at their lowest common ancestor. The common prefix occurs in both root paths, so its XOR appears twice and cancels because

[
x\oplus x=0.
]

What remains is exactly the XOR of the path from (u) to (v). Consequently,

[
P(u,v)=A[u]\oplus A[v].
]

This completely removes the need to find paths between pairs.

Now the problem becomes: given (N) numbers (A[1],A[2],\ldots,A[N]), find the sum of (A[u]\oplus A[v]) over every unordered pair.

XOR can be handled independently one bit at a time. For a particular bit, a pair contributes (1) at that bit exactly when one endpoint has that bit equal to (0) and the other has it equal to (1). If (c_1) values contain the bit and (c_0=N-c_1) do not, exactly

[
c_0c_1
]

pairs contribute that bit. Its contribution to the final answer is therefore

[
c_0c_1\cdot 2^b.
]

We can compute all root-XOR values with one tree traversal, count set bits across those values, and combine the counts. The brute-force works because every pair can be evaluated independently, but fails because there are too many pairs. The observation that every path XOR is simply the XOR of two root-prefix XORs reduces the graph problem to a linear number of vertex values followed by 30 bit counts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^3)) worst case | (O(N)) | Too slow |
| Optimal | (O(30N)) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list for the tree. Each adjacency entry stores the neighboring vertex and the weight of the connecting edge.
2. Root the tree at vertex (1), and traverse it iteratively with a stack. Store `xor_value[v]`, the XOR of all edge weights from vertex (1) to (v). Initially, `xor_value[1] = 0`.
3. When traversing an edge from an already visited vertex (u) to an unvisited vertex (v) with weight (w), assign

[
xor_value[v]=xor_value[u]\oplus w.
]

Because the graph is a tree, there is exactly one path from the root to every vertex, so the first time we reach (v), this value is its correct root-path XOR.
4. After the traversal, consider every bit from (0) through (29). Count how many root-XOR values have that bit set. Call this count (c_1), and let (c_0=N-c_1).
5. For this bit, every pair with one value containing the bit and one value not containing it contributes (1) to the XOR. There are exactly (c_1c_0) such unordered pairs. Add

[
c_1c_0(1\ll b)
]

to the answer.
6. After processing all 30 bits, print the accumulated answer. Each bit was counted independently, so their weighted contributions exactly reconstruct the sum of all pairwise XORs.

### Why it works

The central invariant is that for every vertex (v), `xor_value[v]` equals the XOR of the edges on the unique path from the root to (v). For any two vertices (u) and (v), the common part of their root paths is traversed twice when computing `xor_value[u] XOR xor_value[v]`, so it cancels. The remaining edges are exactly those on the unique path between (u) and (v), giving

[
P(u,v)=xor_value[u]\oplus xor_value[v].
]

For each bit, an XOR has that bit set precisely when its two operands differ at that position. If (c_1) vertices have the bit and (c_0) do not, there are exactly (c_1c_0) pairs with different values at that bit. Thus the algorithm counts the contribution of every bit for every unordered pair exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    graph = [[] for _ in range(n)]

    for _ in range(n - 1):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append((v, w))
        graph[v].append((u, w))

    xor_value = [0] * n
    parent = [-1] * n
    parent[0] = 0

    stack = [0]

    while stack:
        u = stack.pop()

        for v, w in graph[u]:
            if v == parent[u]:
                continue

            parent[v] = u
            xor_value[v] = xor_value[u] ^ w
            stack.append(v)

    answer = 0

    for bit in range(30):
        mask = 1 << bit
        ones = 0

        for value in xor_value:
            if value & mask:
                ones += 1

        zeros = n - ones
        answer += ones * zeros * mask

    print(answer)

if __name__ == "__main__":
    solve()
```

The adjacency list represents the tree and stores each edge in both directions because the original tree is undirected. There are (2(N-1)) adjacency entries, so the representation remains linear in size.

The iterative traversal replaces a recursive DFS. A chain with (10^5) vertices can have recursion depth (10^5), which is unsafe for ordinary Python recursion. The explicit stack avoids that problem.

`xor_value[0]` is initialized to zero because the path from the root to itself contains no edges. Whenever an unvisited child is reached, its value is the parent's value XORed with the connecting edge weight.

The `parent` array is sufficient to prevent immediately walking back across the edge just used. Since the input is guaranteed to be a tree, there are no other previously visited vertices that could cause a cycle. The root's parent is set to itself so that the traversal has a defined parent value from the beginning.

The final loop checks exactly 30 bits. Every edge weight is at most (10^9), so every XOR of edge weights is below (2^{30}). Python integers do not overflow anyway, but restricting the loop to these 30 relevant bits keeps the algorithm precise and efficient.

The multiplication `ones * zeros * mask` can be larger than a 32-bit integer. Python integers automatically grow as needed, so no explicit overflow handling is necessary.

## Worked Examples

For the first sample,

```
4
1 2 1
2 3 4
2 4 2
```

Rooting at vertex (1) gives the following root-XOR values.

| Vertex | Parent | Edge weight | Root XOR |
| --- | --- | --- | --- |
| 1 | none | 0 | 0 |
| 2 | 1 | 1 | 1 |
| 3 | 2 | 4 | 5 |
| 4 | 2 | 2 | 3 |

The pairwise XORs can now be obtained without traversing any path.

| Pair | Root XOR values | Pair XOR |
| --- | --- | --- |
| 1, 2 | (0,1) | 1 |
| 1, 3 | (0,5) | 5 |
| 1, 4 | (0,3) | 3 |
| 2, 3 | (1,5) | 4 |
| 2, 4 | (1,3) | 2 |
| 3, 4 | (5,3) | 6 |

Their sum is

[
1+5+3+4+2+6=21.
]

The bit-counting method produces the same result. For example, at bit (0), the root-XOR values are (0,1,5,3), so three have the bit set and one does not. That bit contributes (3\cdot1\cdot1=3). Repeating this for all relevant bits gives (21).

For a second example, consider the tree

```
3
1 2 1
2 3 2
```

The traversal produces these values.

| Vertex | Parent | Edge weight | Root XOR |
| --- | --- | --- | --- |
| 1 | none | 0 | 0 |
| 2 | 1 | 1 | 1 |
| 3 | 2 | 2 | 3 |

For each bit, we count how many values contain it.

| Bit | Values with bit set | Ones | Zeros | Contribution |
| --- | --- | --- | --- | --- |
| 0 | 1, 3 | 2 | 1 | (2\cdot1\cdot1=2) |
| 1 | 3 | 1 | 2 | (1\cdot2\cdot2=4) |

All higher bits have zero contribution, so the answer is (2+4=6).

The three actual paths have XOR values (1), (2), and (3), whose sum is also (6). This example demonstrates why the method counts unordered pairs correctly: each pair is represented once by one zero-bit value and one one-bit value at every differing bit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N+30N)=O(N)) | The tree is traversed once, then 30 bits are scanned across all (N) vertices. |
| Space | (O(N)) | The adjacency list, parent array, root-XOR array, and traversal stack are all linear in (N). |

For (N=10^5), the algorithm performs roughly a few million simple operations rather than billions or trillions of pairwise path operations. The memory usage is also linear, comfortably within the 256 MB limit. The iterative traversal is particularly useful in Python because it avoids recursion-depth failures on highly unbalanced trees.

## Test Cases

The test harness below exposes the solution through a `solve_case` function so that each assertion can execute independently. The maximum-size case is generated as a chain with (100000) vertices and edge weight (1). Its root-XOR values alternate between (0) and (1), giving (50000) values of each kind and an answer of (2.5\times10^9).

```python
import io
import sys

def solve_case(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        input = sys.stdin.readline

        n = int(input())
        graph = [[] for _ in range(n)]

        for _ in range(n - 1):
            u, v, w = map(int, input().split())
            u -= 1
            v -= 1
            graph[u].append((v, w))
            graph[v].append((u, w))

        xor_value = [0] * n
        parent = [-1] * n
        parent[0] = 0

        stack = [0]

        while stack:
            u = stack.pop()

            for v, w in graph[u]:
                if v == parent[u]:
                    continue

                parent[v] = u
                xor_value[v] = xor_value[u] ^ w
                stack.append(v)

        answer = 0

        for bit in range(30):
            mask = 1 << bit
            ones = 0

            for value in xor_value:
                if value & mask:
                    ones += 1

            zeros = n - ones
            answer += ones * zeros * mask

        print(answer)
        return sys.stdout.getvalue().strip()

    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert solve_case(
    """4
1 2 1
2 3 4
2 4 2
"""
) == "21", "sample 1"

# Minimum-size tree
assert solve_case(
    """1
"""
) == "0", "single vertex"

# Maximum edge weight
assert solve_case(
    """2
1 2 1000000000
"""
) == "1000000000", "maximum edge weight"

# Three vertices, different edge weights
assert solve_case(
    """3
1 2 1
2 3 2
"""
) == "6", "different XOR values"

# All equal edge weights
assert solve_case(
    """4
1 2 7
1 3 7
1 4 7
"""
) == "21", "equal edge weights"

# Maximum-size chain, all edge weights equal to 1.
# Root XOR values alternate 0, 1, 0, 1, ...
n = 100000
lines = [str(n)]
for i in range(1, n):
    lines.append(f"{i} {i + 1} 1")

large_case = "\n".join(lines) + "\n"

# There are 50000 zero-valued and 50000 one-valued root XORs.
# Every zero/one pair contributes 1.
assert solve_case(large_case) == "2500000000", "maximum-size chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `0` | No pairs exist, so the empty sum must be zero. |
| `2 / 1 2 1000000000` | `1000000000` | Maximum edge value and exactly one unordered pair. |
| `3 / 1 2 1 / 2 3 2` | `6` | Different edge values and multi-edge path XOR. |
| `4 / 1 2 7 / 1 3 7 / 1 4 7` | `21` | Equal edge weights and leaf-to-leaf XOR cancellation. |
| Chain of (100000) vertices with weight (1) | `2500000000` | Maximum (N), deep tree, iterative traversal, and large answer. |

## Edge Cases

For a single vertex,

```
1
```

the adjacency list is empty, the traversal leaves `xor_value[0]` equal to zero, and every bit has zero ones. The answer remains zero. There is no attempt to access a nonexistent edge or pair.

For the maximum edge weight,

```
2
1 2 1000000000
```

the root XOR values are (0) and (1000000000). For every set bit of (1000000000), there is exactly one zero-valued vertex and one one-valued vertex, so each such bit contributes its power of two. Their sum reconstructs exactly (1000000000). This confirms that the algorithm does not depend on small edge values.

For equal edge weights,

```
4
1 2 7
1 3 7
1 4 7
```

the root XOR values are (0,7,7,7). At every bit contained in (7), there are three ones and one zero, producing (3) contributing pairs. Since (7) contains three bits, the total is (3+6+12=21). Pairs between two leaves do not contribute because (7\oplus7=0). This is exactly the cancellation behavior used in the proof.

For a deep tree, the maximum-size chain has (100000) vertices. A recursive DFS would need to recurse through almost all (100000) vertices, which is unsafe in Python. The iterative stack visits the same vertices without recursion. With every edge equal to (1), the root-XOR values alternate between (0) and (1). There are (50000) of each, so the only relevant bit contributes

[
50000\cdot50000=2500000000.
]

The implementation obtains that result without ever enumerating the roughly (5\times10^9) vertex pairs.

For the path

```
3
1 2 1
2 3 2
```

the root-XOR values are (0,1,3). The pairwise values are (0\oplus1=1), (0\oplus3=3), and (1\oplus3=2), giving (6). The traversal invariant is visible directly here: XORing the values of two endpoints removes the common prefix from the root and leaves precisely the XOR of their connecting path.
