---
title: "CF 102411J - Just the Last Digit"
description: "The hill can be viewed as a directed acyclic graph whose vertices are the spots (1,ldots,n). Every trail goes from a smaller index to a larger index, so the vertex numbering itself gives a topological order."
date: "2026-08-12T00:21:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102411
codeforces_index: "J"
codeforces_contest_name: "ICPC 2019-2020 North-Western Russia Regional Contest"
rating: 0
weight: 102411
solve_time_s: 174
verified: true
draft: false
---

[CF 102411J - Just the Last Digit](https://codeforces.com/problemset/problem/102411/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

The hill can be viewed as a directed acyclic graph whose vertices are the spots (1,\ldots,n). Every trail goes from a smaller index to a larger index, so the vertex numbering itself gives a topological order.

For every pair (i<j), the input gives only the last decimal digit of the number of directed paths from (i) to (j). A trail (i\to j) is itself a path, while longer paths are obtained by passing through intermediate vertices. The task is to recover whether every possible directed edge exists.

The useful distinction is between a path that goes directly from (i) to (j), and paths that first visit some intermediate vertex (k). If we already know all edges (i\to k) for (i<k<j), then the number of indirect paths from (i) to (j) is

[
\sum_{i<k<j} E_{i,k}P_{k,j},
]

where (E_{i,k}) is either (0) or (1), and (P_{k,j}) is the total number of paths from (k) to (j). We only know (P_{k,j}) modulo (10), but that is enough because the final answer also depends only on the value modulo (10).

The bound (n\le 500) is large enough that enumerating all possible paths is completely impossible. Even the much better dynamic recurrence that examines every triple ((i,k,j)) performs

[
\frac{n(n-1)(n-2)}6
]

inner iterations, which is about (20.7) million when (n=500). That is reasonable in optimized C++, but a Python implementation doing millions of nested interpreted operations can be unnecessarily close to the time limit. We will use the fixed decimal alphabet of only ten digits to reduce the expensive part to roughly (10\binom n2) bit operations.

There are several edge cases that can silently break a straightforward implementation. The first is an adjacent pair. For (j=i+1), there is no intermediate vertex, so the indirect-path sum is exactly zero. For example,

```
2
01
00
```

has one path from vertex (1) to vertex (2), so the answer is

```
01
00
```

An implementation that accidentally accesses an invalid intermediate index can fail here.

The second edge case is modular wraparound. A last digit of zero does not necessarily mean that there is no direct edge. There can be nine indirect paths and one direct path, giving ten paths in total. For example, the following valid graph has a direct edge (1\to6), but exactly ten paths from (1) to (6):

```
6
012350
001124
000112
000001
000001
000000
```

Its correct output is

```
011111
001011
000100
000011
000001
000000
```

The input contains zero at position ((1,6)), yet the edge (1\to6) exists. A solution that interprets an input zero as "no edge" without accounting for the nine indirect paths gets this wrong.

The third edge case is that the input matrix contains path counts, not adjacency information. For instance, if (i\to k) exists and there are two paths from (k) to (j), those two paths must contribute to the indirect count from (i) to (j). Using the original input digit as if it directly represented (E_{i,k}) would mix two different quantities.

## Approaches

The direct brute-force approach follows the path decomposition exactly. Process pairs ((i,j)) in increasing distance. For each pair, enumerate every intermediate (k), add (E_{i,k}P_{k,j}), and compare the result with the given last digit. Since all (E_{i,k}) with (k<j) have already been recovered, this is correct.

More precisely, if (S) is the number of indirect paths from (i) to (j), then

[
P_{i,j}\equiv S+E_{i,j}\pmod {10}.
]

Since (E_{i,j}) can only be zero or one, the edge exists exactly when

[
(S+1)\bmod 10=P_{i,j}.
]

The number of innermost iterations is

\frac{n(n-1)(n-2)}6.
]

At (n=500), that is (20,708,500) iterations. The recurrence is mathematically simple and is the standard accepted cubic formulation of the problem.

The brute-force recurrence works because the graph is a DAG. Once all shorter intervals have been processed, every possible first intermediate vertex (k) has an already reconstructed edge (i\to k), while the path count (P_{k,j}) is already present in the input.

The problem with Python is not the mathematics but the cost of performing tens of millions of nested operations. The observation that makes the computation much cheaper is that every (P_{k,j}) is one of only ten digits. For a fixed destination (j) and digit (d), we can store a bitset containing exactly those vertices (k) for which (P_{k,j}=d).

For a fixed source (i), maintain another bitset containing the already reconstructed outgoing edges (i\to k). Then the number of intermediate vertices satisfying both conditions is simply a bit intersection followed by `bit_count()`.

If `edges` contains the known vertices (k) with (E_{i,k}=1), and `mask[j][d]` contains the vertices whose path-count digit to (j) equals (d), then

\sum_{d=0}^{9}
d\cdot
\operatorname{popcount}
\left(
\text{edges}\mathbin{&}\text{mask}[j][d]
\right).
]

Python integers implement arbitrary-length bitsets in optimized native code, so these intersections and population counts are much cheaper than explicitly looping over every (k).

The key structural fact is that while processing (j) from left to right, `edges` contains only vertices smaller than (j). Thus there is no need to explicitly mask the range (i<k<j). The order of reconstruction provides that restriction automatically.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^3)) | (O(n^2)) | Mathematically correct, unnecessarily slow in Python |
| Bitset by digit | (O(10n^2)) | (O(10n^2)) | Accepted |

## Algorithm Walkthrough

1. Read the matrix of last digits and keep it unchanged. It represents (P_{i,j}\bmod 10), not the graph itself, so it must remain available whenever we decide a new edge.
2. Build ten bitmasks for every destination (j). The bit at position (k) is set in `mask[j][d]` exactly when the input says that the number of paths from (k) to (j) ends in digit (d). Only (k<j) needs to be stored.
3. Create an initially empty adjacency matrix and process source vertices (i) from left to right. For each fixed (i), maintain a single integer `edge_mask`. Its (k)-th bit is one precisely when we have already established the direct edge (i\to k).
4. For every destination (j>i), calculate the number of indirect paths from (i) to (j). For each digit (d), intersect `edge_mask` with `mask[j][d]`. The population count gives the number of intermediate vertices (k) for which (i\to k) is an edge and (P_{k,j}) has last digit (d). Multiply that count by (d) and add it to the indirect total.
5. Reduce the indirect total modulo (10). If there is no direct edge, the observed digit must equal this value. If a direct edge exists, the observed digit must equal the indirect value plus one modulo (10). Since a valid input is guaranteed, the edge is present exactly when

[
(\text{indirect}+1)\bmod 10=P_{i,j}.
]

1. If the edge exists, set bit (j) in `edge_mask` immediately after deciding the pair ((i,j)). It must not be inserted before the calculation for (j), because the direct edge (i\to j) is not an intermediate edge for paths from (i) to (j).
2. After processing all destinations for (i), output the corresponding row of the adjacency matrix. Repeat for every source vertex.

The invariant is that immediately before processing a pair ((i,j)), `edge_mask` contains exactly the direct edges (i\to k) for (i<k<j). Consequently, every indirect path from (i) to (j) has a unique first edge (i\to k), and all paths continuing from (k) to (j) are counted by (P_{k,j}). Their sum is exactly the number of paths that do not use the direct edge (i\to j). Adding one accounts for the direct edge, so the comparison with the observed last digit uniquely determines whether that edge exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    p = [input().strip() for _ in range(n)]

    # masks[j][d] has bit k set iff p[k][j] == digit d.
    masks = [[0] * 10 for _ in range(n)]

    for k in range(n):
        bit = 1 << k
        row = p[k]
        for j in range(k + 1, n):
            masks[j][ord(row[j]) - 48] |= bit

    ans = [bytearray(n) for _ in range(n)]

    for i in range(n - 1):
        edge_mask = 0
        row = ans[i]

        for j in range(i + 1, n):
            col_masks = masks[j]

            indirect = 0
            for d in range(1, 10):
                indirect += d * (edge_mask & col_masks[d]).bit_count()

            given = ord(p[i][j]) - 48

            if (indirect + 1) % 10 == given:
                row[j] = 1
                edge_mask |= 1 << j

    sys.stdout.write(
        '\n'.join(''.join('1' if x else '0' for x in row) for row in ans)
    )

if __name__ == "__main__":
    solve()
```

The first loop constructs the digit masks. For a fixed intermediate vertex (k), `bit = 1 << k` is reused for the entire row, avoiding repeated shifting. The loop starts at `k + 1` because entries at or below the diagonal are guaranteed to be zero and can never be intermediate vertices for a forward path.

The second phase reconstructs the graph. `edge_mask` is reset for every source (i), because it represents only edges leaving that source. The destination (j) is processed in increasing order, so every bit already present in `edge_mask` corresponds to a valid intermediate vertex.

The expression

```
(edge_mask & col_masks[d]).bit_count()
```

is the optimized replacement for an entire loop over (k). The intersection keeps exactly those (k) for which both (E_{i,k}=1) and (P_{k,j}\equiv d\pmod{10}).

Digit zero does not need to be processed because its contribution to the sum is zero. The masks for zero are still built because they make the representation complete and keep the construction simple.

The direct edge is inserted into `edge_mask` only after deciding ((i,j)). Moving that operation before the calculation would incorrectly count the direct edge as an intermediate vertex.

There is no integer overflow issue in Python. Even though the indirect sum can exceed ten, only its value modulo ten matters. The implementation keeps the full small sum for simplicity, and at most (9(n-2)) is added for one pair.

## Worked Examples

There is only one official sample, so the second trace uses the modular-wraparound case from the edge discussion.

For Sample 1, the input is

```
5
01113
00012
00001
00001
00000
```

The following table shows the pair-by-pair decisions. The `indirect` column is computed using already reconstructed edges.

| Source (i) | Destination (j) | Given digit | Indirect paths mod 10 | Edge |
| --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 0 | 1 |
| 1 | 3 | 1 | 0 | 1 |
| 1 | 4 | 1 | 1 | 0 |
| 1 | 5 | 3 | 3 | 0 |
| 2 | 3 | 0 | 0 | 0 |
| 2 | 4 | 1 | 0 | 1 |
| 2 | 5 | 2 | 1 | 1 |
| 3 | 4 | 0 | 0 | 0 |
| 3 | 5 | 1 | 0 | 1 |
| 4 | 5 | 1 | 0 | 1 |

For example, when processing (1\to5), the known edges from vertex (1) are (1\to2) and (1\to3). The corresponding path counts are (P_{2,5}=2) and (P_{3,5}=1), giving three indirect paths. Since the observed digit is also three, no direct edge (1\to5) is needed.

The resulting adjacency matrix is

```
01100
00011
00001
00001
00000
```

which matches the sample.

For the modular-wraparound case,

```
6
012350
001124
000112
000001
000001
000000
```

consider source vertex (1). The decisions are:

| (j) | Given digit | Known edge mask before (j) | Indirect paths | Edge (1\to j) |
| --- | --- | --- | --- | --- |
| 2 | 1 | none | 0 | 1 |
| 3 | 2 | (2) | 1 | 1 |
| 4 | 3 | (2,3) | 2 | 1 |
| 5 | 5 | (2,3,4) | 4 | 1 |
| 6 | 0 | (2,3,4,5) | 9 | 1 |

The last row demonstrates the purpose of taking the result modulo ten. Before deciding (1\to6), the four already known edges contribute

# 4+2+2+1

1. 

]

Adding the direct edge gives ten paths, whose last digit is zero. Since

[
(9+1)\bmod 10=0,
]

the algorithm correctly reconstructs the edge even though the input digit is zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(10n^2)) | There are (O(n^2)) pairs, and each pair checks the ten possible digits using native integer bit operations |
| Space | (O(10n^2)) | Ten bitsets are stored for every destination, plus the (n\times n) answer |

For (n=500), there are only (124{,}750) pairs and ten digit classes, so the algorithm performs about (1.25) million `bit_count()` operations. The bitsets themselves contain only 500 relevant bits each. This comfortably fits the 2 second and 512 MB limits while avoiding the roughly 20.7 million explicit Python-level inner iterations of the cubic recurrence.

## Test Cases

```python
import sys
import io

def solve():
    n = int(input())
    p = [input().strip() for _ in range(n)]

    masks = [[0] * 10 for _ in range(n)]

    for k in range(n):
        bit = 1 << k
        row = p[k]
        for j in range(k + 1, n):
            masks[j][ord(row[j]) - 48] |= bit

    ans = [bytearray(n) for _ in range(n)]

    for i in range(n - 1):
        edge_mask = 0
        row = ans[i]

        for j in range(i + 1, n):
            col_masks = masks[j]

            indirect = 0
            for d in range(1, 10):
                indirect += d * (edge_mask & col_masks[d]).bit_count()

            given = ord(p[i][j]) - 48

            if (indirect + 1) % 10 == given:
                row[j] = 1
                edge_mask |= 1 << j

    sys.stdout.write(
        '\n'.join(''.join('1' if x else '0' for x in row) for row in ans)
    )

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    try:
        solve()
        result = sys.stdout.getvalue() if hasattr(sys.stdout, "getvalue") else ""
    finally:
        input = old_input
        sys.stdin = old_stdin

    return result

def run_capture(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = input

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        input = old_input
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run_capture(
    """5
01113
00012
00001
00001
00000
"""
) == """01100
00011
00001
00001
00000
""", "sample 1"

# Minimum-size graph with one edge
assert run_capture(
    """2
01
00
"""
) == """01
00
""", "minimum size"

# Minimum-size graph with no edge
assert run_capture(
    """2
00
00
"""
) == """00
00
""", "minimum size, no edge"

# Complete DAG on four vertices.
# Path counts are:
# 1 -> 2: 1
# 1 -> 3: 2
# 1 -> 4: 4
# 2 -> 3: 1
# 2 -> 4: 2
# 3 -> 4: 1
assert run_capture(
    """4
0114
0012
0001
0000
"""
) == """0111
0011
0001
0000
""", "complete DAG"

# A direct edge whose total path count wraps from 10 to digit 0.
assert run_capture(
    """6
012350
001124
000112
000001
000001
000000
"""
) == """011111
001011
000100
000011
000001
000000
""", "modulo 10 wraparound"

# Maximum-size input.
# The empty graph has zero paths between every distinct pair,
# so the input and output are both 500 zero rows.
n = 500
zero_row = "0" * n
max_input = str(n) + "\n" + "\n".join([zero_row] * n) + "\n"
max_output = "\n".join([zero_row] * n) + "\n"

assert run_capture(max_input) == max_output, "maximum size"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 01 / 00` | `01 / 00` | Minimum size and adjacent-pair handling |
| `2 / 00 / 00` | `00 / 00` | Empty graph and zero path counts |
| `4 / 0114 / 0012 / 0001 / 0000` | Complete upper-triangular adjacency | Multiple indirect paths and correct reconstruction order |
| `6 / 012350 / 001124 / 000112 / 000001 / 000001 / 000000` | `011111 / 001011 / 000100 / 000011 / 000001 / 000000` | Last-digit wraparound, including an existing edge with observed digit zero |
| (500\times500) zero matrix | (500\times500) zero matrix | Maximum (n), memory use, and performance |

## Edge Cases

The adjacent-pair case has no intermediate vertex. For

```
2
01
00
```

the pair ((1,2)) has an indirect sum of zero. The observed digit is one, so

[
(0+1)\bmod10=1,
]

and the algorithm sets the edge (1\to2). There is no attempt to inspect a nonexistent vertex between them.

The empty graph is handled in exactly the same recurrence. For

```
2
00
00
```

the indirect sum is zero and the observed digit is zero. Since

[
(0+1)\bmod10\ne0,
]

the edge is absent. The resulting matrix remains all zeroes.

The most deceptive case is modular wraparound. Consider

```
6
012350
001124
000112
000001
000001
000000
```

For (1\to6), the already reconstructed edges are (1\to2,1\to3,1\to4,1\to5). Their contributions are

[
P_{2,6}=4,\qquad
P_{3,6}=2,\qquad
P_{4,6}=2,\qquad
P_{5,6}=1.
]

The indirect total is (9). The observed digit is zero, but adding a direct edge produces ten paths, so the correct decision is (E_{1,6}=1). The algorithm tests `(9 + 1) % 10 == 0` and recovers that edge correctly.

Finally, reconstruction order is essential. When deciding (E_{i,j}), only edges (E_{i,k}) with (k<j) are allowed to participate in the indirect-path sum. Processing (j) from left to right guarantees that every bit in `edge_mask` represents an already established edge and that the current candidate edge (i\to j) has not accidentally been counted as its own intermediate contribution.
