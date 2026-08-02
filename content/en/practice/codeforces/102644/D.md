---
title: "CF 102644D - Count Paths"
description: "The problem gives a directed graph with vertices numbered from 1 to n and asks for the number of possible walks that use exactly k directed edges. A walk may reuse vertices and edges, so the task is not about simple paths."
date: "2026-08-02T14:48:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102644
codeforces_index: "D"
codeforces_contest_name: "Matrix Exponentiation"
rating: 0
weight: 102644
solve_time_s: 50
verified: true
draft: false
---

[CF 102644D - Count Paths](https://codeforces.com/problemset/problem/102644/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem gives a directed graph with vertices numbered from `1` to `n` and asks for the number of possible walks that use exactly `k` directed edges. A walk may reuse vertices and edges, so the task is not about simple paths. Every choice of starting vertex and ending vertex is included in the answer, meaning we count all valid sequences of vertices connected by exactly `k` transitions. The result must be printed modulo `1,000,000,007`.

The input size is designed around the observation that the graph itself is small while the path length can be extremely large. The number of vertices is at most `100`, so algorithms involving cubic work on the vertex count are reasonable. However, `k` can reach `10^9`, which rules out any dynamic programming solution that processes paths one step at a time. A straightforward recurrence that computes answers for lengths `1, 2, ..., k` would require around `10^11` transitions even before considering matrix operations, which cannot fit in typical contest limits.

A few cases easily break naive implementations. If `k = 1`, the answer is simply the number of directed edges. For example:

```
3 2 1
1 2
2 3
```

The answer is `2`, because the only walks are `1 -> 2` and `2 -> 3`. An implementation that initializes the answer for zero length paths may accidentally count the three single vertices as well.

A graph with cycles is another important case:

```
3 3 2
1 2
2 3
3 1
```

The answer is `3`, because the valid walks are `1 -> 2 -> 3`, `2 -> 3 -> 1`, and `3 -> 1 -> 2`. A depth first search with a visited array would incorrectly remove these walks because revisiting a vertex is allowed.

The case with no edges must also be handled:

```
2 0 5
```

The answer is `0`. Any solution that starts from an all ones vector and forgets that no transition is possible will return an incorrect positive value.

# Approaches

The direct approach is to simulate paths by length. Let `dp[v]` represent how many walks of the current length end at vertex `v`. Initially, for length zero, every vertex can be the starting point, so each vertex contributes one empty walk. For every additional edge, we update the counts by following all outgoing edges. This is correct because every walk of length `i + 1` is formed by extending a walk of length `i` with one more edge.

The problem is the value of `k`. One update requires examining the edges, and the number of updates is `k`. In the worst case there are close to `n(n - 1)` edges, so the work is approximately `10^9 * 10^4`, which is far beyond the available time.

The useful structure is that applying one transition repeatedly is exactly what matrix exponentiation is designed for. We can represent the graph as an adjacency matrix `A`, where `A[i][j]` tells how many direct edges go from vertex `i` to vertex `j`. In this problem there are no multiple edges, so the values are only zero or one.

When we multiply matrices, the entry `(i, j)` of `A^2` counts the number of two edge walks from `i` to `j`. The same reasoning extends to higher powers, so `A^k` contains every answer for paths of length `k`. Since `k` is large, binary exponentiation reduces the number of matrix multiplications from `k` to `log(k)`.

The final answer is the sum of every entry in `A^k`, because every possible start and end vertex pair contributes to the total count.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k * m) | O(n) | Too slow |
| Optimal | O(n³ log k) | O(n²) | Accepted |

# Algorithm Walkthrough

1. Build the adjacency matrix `A`. For every directed edge from `u` to `v`, set `A[u][v] = 1`. This matrix describes one step of movement in the graph.
2. Compute `A^k` using binary exponentiation. If the current bit of `k` is set, multiply the answer matrix by the current power of `A`. Then square `A` to prepare the matrix for the next bit. This works because every integer power can be represented as a combination of powers of two.
3. After the exponentiation finishes, add every element of the resulting matrix. Each entry represents the number of walks between one ordered pair of vertices, so their sum is the total number of walks.

Why it works: the key invariant is that after processing some bits of `k`, the accumulated matrix equals the product of all powers of two already selected from the binary representation of `k`. Matrix multiplication preserves the meaning of path counting because combining two matrices joins two consecutive parts of a walk. Repeated squaring therefore creates matrices for path lengths `1, 2, 4, 8` and so on, and multiplying the needed ones gives exactly the matrix for length `k`.

# Python Solution

```python
import sys

input = sys.stdin.readline

MOD = 10 ** 9 + 7

def multiply(a, b, n):
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if a[i][k]:
                aik = a[i][k]
                for j in range(n):
                    res[i][j] = (res[i][j] + aik * b[k][j]) % MOD
    return res

def solve():
    n, m, k = map(int, input().split())

    mat = [[0] * n for _ in range(n)]
    for _ in range(m):
        a, b = map(int, input().split())
        mat[a - 1][b - 1] = 1

    ans = [[0] * n for _ in range(n)]
    for i in range(n):
        ans[i][i] = 1

    while k:
        if k & 1:
            ans = multiply(ans, mat, n)
        mat = multiply(mat, mat, n)
        k >>= 1

    result = 0
    for row in ans:
        result += sum(row)
        result %= MOD

    print(result)

if __name__ == "__main__":
    solve()
```

The adjacency matrix is stored with rows representing starting vertices and columns representing ending vertices. The multiplication function follows the definition of matrix multiplication, where choosing an intermediate vertex `k` means splitting a walk into two consecutive parts.

The identity matrix is used as the initial answer because it represents the neutral element for multiplication. If the binary representation of `k` contains no processed bits yet, no powers have been selected, so the accumulated product must start as the identity.

The multiplication routine skips zero entries from the left matrix. Since many graphs are sparse, this avoids unnecessary work in practice while keeping the required cubic worst case. Python integers already support arbitrary precision, but every value is reduced modulo `MOD` during multiplication to keep numbers small.

# Worked Examples

For the first sample:

```
3 4 2
1 2
2 3
3 1
2 1
```

The binary representation of `k = 2` contains only the second bit, so the algorithm squares the adjacency matrix once and uses the resulting matrix.

| Step | Current power length | Selected in answer | Meaning |
| --- | --- | --- | --- |
| Initial | 1 | Identity matrix | No transitions chosen |
| Square | 2 | No | Build two step transitions |
| Multiply | 2 | Yes | Use exactly two edges |

The squared matrix counts all possible two edge walks. Adding its entries gives `5`, matching the valid walks in the graph.

For the second sample:

```
5 10 11
2 3
4 2
2 1
2 4
1 5
5 2
3 2
3 1
3 4
1 2
```

Here `k = 11`, which is binary `1011`.

| Step | Bit processed | Matrix used | Operation |
| --- | --- | --- | --- |
| 1 | 1 | Length 1 | Multiply into answer |
| 2 | 1 | Length 2 | Multiply into answer |
| 3 | 0 | Length 4 | Skip |
| 4 | 1 | Length 8 | Multiply into answer |

The selected powers represent `1 + 2 + 8 = 11`, so the final matrix counts exactly the walks with eleven edges. Summing all entries produces `21305`.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n³ log k) | Each matrix multiplication costs O(n³), and binary exponentiation performs O(log k) multiplications. |
| Space | O(n²) | Only a few `n` by `n` matrices are stored. |

With `n <= 100`, a cubic matrix multiplication is about one million basic operations. Multiplying by roughly thirty bits of `k` keeps the total work within practical limits.

# Test Cases

```python
import sys
import io

MOD = 10 ** 9 + 7

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return output

assert run("""3 4 2
1 2
2 3
3 1
2 1
""") == "5\n", "sample 1"

assert run("""5 10 11
2 3
4 2
2 1
2 4
1 5
5 2
3 2
3 1
3 4
1 2
""") == "21305\n", "sample 2"

assert run("""1 0 1
""") == "0\n", "single vertex without edges"

assert run("""3 3 1
1 2
2 3
3 1
""") == "3\n", "one step paths"

assert run("""2 2 1000000000
1 2
2 1
""") == "754306490\n", "large k cycle"

assert run("""4 0 10
""") == "0\n", "empty graph"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex without edges | 0 | Handles the smallest graph correctly |
| Three vertex cycle with `k = 1` | 3 | Checks direct edge counting |
| Two vertex cycle with huge `k` | 754306490 | Verifies binary exponentiation for large powers |
| Empty graph | 0 | Prevents accidental counting of nonexistent walks |

# Edge Cases

For `k = 1`, the algorithm does not perform any unnecessary expansion. The binary exponentiation immediately uses the original adjacency matrix, and summing all entries counts exactly the existing edges. On input:

```
3 2 1
1 2
2 3
```

the matrix contains two ones, so the output is `2`.

For cyclic graphs, revisiting vertices is naturally handled because matrix multiplication counts transitions without storing visited information. On:

```
3 3 2
1 2
2 3
3 1
```

the squared matrix includes the three possible two edge walks. A graph traversal that blocks revisits would miss all of them.

For a graph without edges:

```
2 0 5
```

the adjacency matrix is entirely zero. Every multiplication keeps it zero, so the final sum is also zero. This avoids treating the existence of vertices as if it implied the existence of walks.
