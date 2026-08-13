---
title: "CF 102282I - \u041f\u0440\u043e\u0438\u0437\u0432\u0435\u0434\u0435\u043d\u0438\u044f"
description: "We have an (n times n) grid. Some cells contain positive integers and the rest contain zero. Every row and every column must contain exactly two nonzero cells."
date: "2026-08-13T09:15:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102282
codeforces_index: "I"
codeforces_contest_name: "2011, \u041e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u043a\u043e\u043d\u0442\u0435\u0441\u0442 \u0421\u0413\u0410\u0423 \u043d\u0430 \u0447\u0435\u0442\u0432\u0435\u0440\u0442\u044c\u0444\u0438\u043d\u0430\u043b ACM ICPC"
rating: 0
weight: 102282
solve_time_s: 204
verified: true
draft: false
---

[CF 102282I - \u041f\u0440\u043e\u0438\u0437\u0432\u0435\u0434\u0435\u043d\u0438\u044f](https://codeforces.com/problemset/problem/102282/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an (n \times n) grid. Some cells contain positive integers and the rest contain zero. Every row and every column must contain exactly two nonzero cells. The product of the two numbers in row (i) must equal (y_i), while the product of the two numbers in column (j) must equal (x_j). Every number written into the grid must be different from every other written number.

The input consists of (n), the (n) required column products (x_0,\ldots,x_{n-1}), and the (n) required row products (y_0,\ldots,y_{n-1}). The statement guarantees that at least one valid grid exists, so we only have to construct one.

A useful way to view the grid is as a bipartite graph. Create one vertex for every row and one vertex for every column. A nonzero cell becomes an edge between its row and its column, and the number in the cell becomes the edge label. Since every row and column contains exactly two numbers, every vertex has degree two. Thus the selected cells form a collection of even cycles. The product of the labels incident to each row or column is prescribed.

The bound (n \le 10) is the main signal about the intended approach. There are only (2n \le 20) numbers to place, but their positions and values interact through both rows and columns. A brute force over arbitrary cells is far too large, while a carefully pruned backtracking search over the forced multiplicative structure is small enough.

The products are at most (1000). This is especially useful because every number placed in the table divides the product of the row containing it and also divides the product of its column. Consequently, all candidate values are among the divisors of numbers from (1) through (1000), and a target has very few possible factorizations into two distinct positive integers.

There are several edge cases that a careless implementation can miss. The number (1) is allowed as a cell value, and it may be essential. For example,

```
2
2 12
3 8
```

has the valid output

```
1 3
2 4
```

The first row uses (1) and (3), so rejecting (1) as a useless factor would incorrectly eliminate the solution.

A row product can also be a square without its two cell values being equal. For example,

```
2
20 63
36 35
```

can be solved by

```
4 9
5 7
```

The first row has product (4 \cdot 9 = 36). A solver that only considers the pair ((6,6)) for the square (36) would fail, even though equal values are forbidden.

The order of the two factors matters because they have to go into different columns. For example,

```
2
10 21
6 35
```

has the solution

```
2 3
5 7
```

The factors (2) and (3) both belong to the row product (6), but only (2) fits the first column product (10), while (3) fits the second column product (21). Treating an unordered factor pair as if its orientation did not matter loses valid placements.

## Approaches

The most direct brute force chooses two cells in every row, then chooses two values whose product is the required row product. For (n=10), even choosing only the positions already gives

[
\binom{100}{2}^{10}=4950^{10}
]

possible choices before considering the values, column constraints, or the requirement that all values be distinct. That is roughly (8.7\cdot10^{36}) possibilities, so a cell-by-cell enumeration is completely impractical.

The useful observation is that a row product does not allow arbitrary values. If the remaining product of a row is (p), its two values must be a factor pair (a,b) with (ab=p). Since (p\le1000), there are very few such pairs. The same observation applies to columns.

We can go one step further and represent every row and column by its remaining product and its remaining degree. Initially every vertex has degree two and its remaining product is its original target. Whenever we place a value (v) on an edge, we divide the remaining product of both endpoints by (v), and decrease both endpoint degrees by one.

The search always chooses the currently most constrained row or column. If a vertex has only one remaining edge, its next value is completely determined by its remaining product. We only have to decide which opposite vertex receives it. If a vertex has two remaining edges, we enumerate its factor pairs and two possible opposite vertices.

This is much smaller than searching over cells. More importantly, once we choose a degree-two vertex and connect it to two neighbors, those neighbors become degree one. The search then propagates forced values through the resulting cycle. The same process repeats for another component if the solution consists of several cycles.

For a product not exceeding (1000), there are at most 32 divisors, so there are at most 16 unordered factor pairs. A degree-two vertex has at most (n(n-1)) ordered choices of two distinct neighbors, giving at most (16\cdot10\cdot9=1440) local candidates before divisibility and uniqueness pruning. In practice the candidate count is dramatically smaller because every candidate must also divide the remaining product of its two chosen neighbors.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O\left(\binom{n^2}{2}^n\right)) before choosing values | (O(n^2)) | Too slow |
| Constraint Backtracking | (O(B^{2n})) worst case, (B\le1440), with strong divisibility pruning | (O(n^2)) apart from the search stack and memoization | Accepted |

The exponential worst-case bound is deliberately loose. The practical search is controlled by (n\le10), the small divisor count of numbers up to (1000), the degree-two structure, and the fact that every failed partial assignment is rejected as soon as one endpoint can no longer be completed.

## Algorithm Walkthrough

1. Treat the (n) rows and (n) columns as (2n) vertices. For each vertex store its remaining product and its remaining degree. Initially every degree is two and the remaining product is the corresponding input value.
2. Maintain the set of already used cell values. A value can be placed only if it has not appeared anywhere else in the grid. Also maintain which row-column cells have already been occupied, because the graph must be simple and the same cell cannot be selected twice.
3. For a vertex whose remaining degree is one, its next edge value is forced. It must equal the vertex's remaining product. We enumerate the opposite vertices where that value divides the opposite remaining product and where the connecting cell has not already been used.
4. For a vertex whose remaining degree is two, enumerate every factorization (a\cdot b=p) of its remaining product into two distinct values. For each factor pair, choose two distinct available opposite vertices. Both orientations, (a) on the first vertex and (b) on the second, and the reverse, are considered because the opposite products may accept only one orientation.
5. Before accepting a candidate, check the immediate consequences on both endpoints. If an endpoint becomes degree zero, its remaining product must become one. If it becomes degree one, its remaining product must be a value that can still be used. If it remains degree two, its remaining product must still have a factorization into two distinct unused values. These checks discard impossible branches before recursion.
6. Among all vertices that still have incident edges, choose the one with the fewest currently feasible candidates. This is the standard minimum-remaining-values idea. A forced degree-one vertex is especially valuable because its value is already known, so it usually has only a few possible neighbors.
7. Apply the chosen candidate by writing its value into the corresponding cells, dividing the remaining products, decreasing the degrees, and marking the values and cells as used.
8. Recurse until every vertex has degree zero. At that point every row and column has exactly two values, all remaining products are one, and all cell values are distinct. The constructed grid is the answer.

### Why it works

The invariant is that every partial assignment represents a valid set of already chosen edges, and for every vertex its stored remaining product is exactly the product still required from its unassigned incident edges. A candidate is considered only when its value divides both endpoint products, respects the remaining degrees, uses an empty cell, and is globally unused. Thus every recursive state can still correspond to a valid completion. Conversely, for any valid completion of a state, the next chosen vertex must use either its forced remaining value when its degree is one, or one of its valid factor pairs when its degree is two, connected to two of its actual neighbors. The search enumerates all such possibilities, so it cannot discard the only valid solution. Since the input guarantees that a solution exists, some branch reaches the state where all degrees are zero.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXV = 1000

factor_pairs = [[] for _ in range(MAXV + 1)]
for p in range(1, MAXV + 1):
    d = 1
    while d * d <= p:
        if p % d == 0:
            e = p // d
            if d != e:
                factor_pairs[p].append((d, e))
        d += 1

def solve(data: str) -> str:
    it = iter(data.split())
    n = int(next(it))
    x = [int(next(it)) for _ in range(n)]
    y = [int(next(it)) for _ in range(n)]

    if prod(x) != prod(y):
        return ""

    m = 2 * n

    rem = x[:] + y[:]
    deg = [2] * m

    ans = [[0] * n for _ in range(n)]
    used_mask = 0
    edge_mask = 0

    def edge_bit(v, u):
        if v < n:
            r, c = v, u - n
        else:
            r, c = u, v - n
        return 1 << (r * n + c)

    def neighbors(v):
        if v < n:
            return range(n, 2 * n)
        return range(n)

    def cell_coords(v, u):
        if v < n:
            return v, u - n
        return u, v - n

    def value_unused(v, mask):
        return (mask >> v) & 1 == 0

    def future_possible(u, value, mask, emask):
        if deg[u] <= 0:
            return False

        if rem[u] % value != 0:
            return False

        nr = rem[u] // value
        nd = deg[u] - 1

        if nd == 0:
            return nr == 1

        if value_unused(value, mask):
            pass

        if nd == 1:
            if nr <= 0 or nr > MAXV:
                return False
            if not value_unused(nr, mask):
                return False

            for w in neighbors(u):
                if deg[w] == 0:
                    continue
                bit = edge_bit(u, w)
                if emask & bit:
                    continue
                if rem[w] % nr == 0:
                    return True
            return False

        if nr <= 0 or nr > MAXV:
            return False

        for a, b in factor_pairs[nr]:
            if not value_unused(a, mask) or not value_unused(b, mask):
                continue
            for w1 in neighbors(u):
                if deg[w1] == 0:
                    continue
                bit1 = edge_bit(u, w1)
                if emask & bit1:
                    continue
                if rem[w1] % a != 0:
                    continue
                for w2 in neighbors(u):
                    if w2 == w1 or deg[w2] == 0:
                        continue
                    bit2 = edge_bit(u, w2)
                    if emask & bit2:
                        continue
                    if rem[w2] % b == 0:
                        return True
        return False

    def candidates(v, mask, emask):
        result = []

        if deg[v] == 0:
            return result

        if deg[v] == 1:
            value = rem[v]

            if value <= 0 or value > MAXV:
                return result
            if not value_unused(value, mask):
                return result

            for u in neighbors(v):
                if deg[u] == 0:
                    continue

                bit = edge_bit(v, u)
                if emask & bit:
                    continue

                if rem[u] % value != 0:
                    continue

                new_mask = mask | (1 << value)
                if not future_possible(u, value, new_mask, emask | bit):
                    continue

                result.append((u, value))
            return result

        for a, b in factor_pairs[rem[v]]:
            if not value_unused(a, mask) or not value_unused(b, mask):
                continue

            for u in neighbors(v):
                if deg[u] == 0:
                    continue
                bit_u = edge_bit(v, u)
                if emask & bit_u:
                    continue
                if rem[u] % a != 0:
                    continue

                for w in neighbors(v):
                    if w == u or deg[w] == 0:
                        continue
                    bit_w = edge_bit(v, w)
                    if emask & bit_w:
                        continue
                    if rem[w] % b != 0:
                        continue

                    new_mask = mask | (1 << a) | (1 << b)
                    new_emask = emask | bit_u | bit_w

                    if not future_possible(u, a, new_mask, new_emask):
                        continue
                    if not future_possible(w, b, new_mask, new_emask):
                        continue

                    result.append((u, a, w, b))

        return result

    failed = set()

    def dfs(mask, emask):
        if all(d == 0 for d in deg):
            return True

        key = (
            tuple(rem),
            tuple(deg),
            mask,
            emask,
        )
        if key in failed:
            return False

        best_v = -1
        best_candidates = None

        for v in range(m):
            if deg[v] == 0:
                continue

            cand = candidates(v, mask, emask)

            if not cand:
                failed.add(key)
                return False

            if best_candidates is None or len(cand) < len(best_candidates):
                best_v = v
                best_candidates = cand

                if len(best_candidates) == 1:
                    break

        v = best_v

        for cand in best_candidates:
            if deg[v] == 1:
                u, value = cand

                r, c = cell_coords(v, u)
                ans[r][c] = value

                old_rem_v = rem[v]
                old_rem_u = rem[u]
                old_deg_v = deg[v]
                old_deg_u = deg[u]

                rem[v] //= value
                rem[u] //= value
                deg[v] -= 1
                deg[u] -= 1

                bit = edge_bit(v, u)
                if dfs(mask | (1 << value), emask | bit):
                    return True

                rem[v] = old_rem_v
                rem[u] = old_rem_u
                deg[v] = old_deg_v
                deg[u] = old_deg_u
                ans[r][c] = 0

            else:
                u, a, w, b = cand

                r1, c1 = cell_coords(v, u)
                r2, c2 = cell_coords(v, w)

                ans[r1][c1] = a
                ans[r2][c2] = b

                old = (
                    rem[v], rem[u], rem[w],
                    deg[v], deg[u], deg[w]
                )

                rem[v] //= a
                rem[u] //= a
                deg[v] -= 1
                deg[u] -= 1

                rem[v] //= b
                rem[w] //= b
                deg[v] -= 1
                deg[w] -= 1

                bit1 = edge_bit(v, u)
                bit2 = edge_bit(v, w)

                if dfs(
                    mask | (1 << a) | (1 << b),
                    emask | bit1 | bit2
                ):
                    return True

                rem[v], rem[u], rem[w] = old[:3]
                deg[v], deg[u], deg[w] = old[3:]
                ans[r1][c1] = 0
                ans[r2][c2] = 0

        failed.add(key)
        return False

    dfs(used_mask, edge_mask)

    return "\n".join(" ".join(map(str, row)) for row in ans)

def prod(a):
    result = 1
    for v in a:
        result *= v
    return result

if __name__ == "__main__":
    data = sys.stdin.read()
    sys.stdout.write(solve(data))
```

The factor-pair table is precomputed once. For every product up to (1000), it stores only pairs of distinct factors, because using the same value twice would violate the global uniqueness condition.

The arrays `rem` and `deg` contain both sides of the bipartite graph. Vertices `0` through `n-1` represent rows, while vertices `n` through `2*n-1` represent columns. Dividing `rem` and decrementing `deg` after placing an edge directly mirrors the mathematical invariant from the algorithm.

The `edge_mask` is necessary in addition to the degree information. Two vertices may both still have unused degree while their connecting cell has already been occupied by an earlier decision. Without remembering occupied cells, the search could accidentally create a parallel edge between the same row and column.

The `used_mask` stores all used values as bits. Since every value is at most (1000), a Python integer is an efficient representation. Testing whether a value has already appeared becomes a single bit operation.

`future_possible` performs local forward checking. It does not prove that the remaining instance is solvable, but it detects several immediate impossibilities. In particular, a vertex that becomes degree zero must have remaining product one, and a vertex that becomes degree one must have a remaining value that can actually be connected somewhere.

The recursive search uses minimum remaining values. It generates candidates for every unfinished vertex and selects the vertex with the smallest candidate list. A degree-one vertex is often nearly forced, so after the first degree-two decision the search usually propagates through an entire cycle with very little branching.

The memoization key contains the remaining products, remaining degrees, used values, and occupied cells. All of these are needed because two states with identical products can still differ in which cells are already occupied or which values have already been consumed.

Python integers do not overflow, so products and bit masks are safe. The input has only one test case, exactly as specified by the statement, so there is no test-case loop.

## Worked Examples

### Sample 1

The input is

```
2
2 12
3 8
```

The first row must contain two distinct factors of (3), so the only possibility is (1) and (3). The first column has target (2), so (1) must go there. The second column receives (3). The remaining row then has target (8), and its only possible placement is (2) in the first column and (4) in the second.

| Step | Chosen vertex | Assignment | Remaining products |
| --- | --- | --- | --- |
| 0 | Row 0 | none | Rows: 3, 8; Columns: 2, 12 |
| 1 | Row 0 | (r_0c_0=1,\ r_0c_1=3) | Rows: 1, 8; Columns: 2, 4 |
| 2 | Column 0 | (r_1c_0=2) | Rows: 1, 4; Columns: 1, 4 |
| 3 | Column 1 | (r_1c_1=4) | Rows: 1, 1; Columns: 1, 1 |

The final grid is

```
1 3
2 4
```

Every row and column has exactly two entries, and the four values are distinct. The table also illustrates why degree-one vertices are powerful: after the first row is fixed, each column has exactly one remaining edge, so its value is forced.

### Sample 2

The input is

```
3
5 8 18
2 30 12
```

The most constrained initial vertex is column zero. Its target is (5), and its two factors must be (1) and (5). The only compatible row products are row zero for (1) and row one for (5).

| Step | Chosen vertex | Assignment | Remaining products |
| --- | --- | --- | --- |
| 0 | Column 0 | none | Rows: 2, 30, 12; Columns: 5, 8, 18 |
| 1 | Column 0 | (r_0c_0=1,\ r_1c_0=5) | Rows: 2, 6, 12; Columns: 1, 8, 18 |
| 2 | Row 1 | (r_1c_2=6) | Rows: 2, 1, 12; Columns: 1, 8, 3 |
| 3 | Column 2 | (r_2c_2=3) | Rows: 2, 1, 4; Columns: 1, 8, 1 |
| 4 | Row 0 | (r_0c_1=2) | Rows: 1, 1, 4; Columns: 1, 6, 1 |
| 5 | Row 2 | (r_2c_1=4) | Rows: 1, 1, 1; Columns: 1, 1, 1 |

The resulting grid is

```
1 2 0
5 0 6
0 4 3
```

The trace demonstrates the cycle propagation. Once column zero is fixed, row one has only one remaining factor, which fixes column two, which then fixes row two's factor in that column. The last two placements become forced.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(B^{2n})) in the loose worst case, (B\le1440) | Each recursive decision assigns at least one edge, and every degree-two decision considers only factor pairs and pairs of opposite vertices |
| Space | (O(n^2 + S)) | The grid, masks, recursion state, and memoized failed states require storage proportional to the search |

The theoretical exponential bound is intentionally conservative. With (n\le10), there are only 20 vertices and 20 occupied cells in a complete solution. The divisor restriction makes each local factor choice tiny, while the minimum-candidate heuristic and forward checking eliminate most branches immediately. This is the structure that makes the search practical under the given (1) second limit.

## Test Cases

The test harness below assumes the `solve` function from the solution is available in the same file or imported from it. Since the problem allows any valid answer, the samples are checked exactly, while the custom cases are checked with a validator that verifies every requirement of the problem.

```python
import io
import sys

def run(inp: str) -> str:
    return solve(inp).strip()

def validate(inp: str, out: str) -> bool:
    data = list(map(int, inp.split()))
    n = data[0]
    x = data[1:1 + n]
    y = data[1 + n:1 + 2 * n]

    lines = out.strip().splitlines()
    if len(lines) != n:
        return False

    a = []
    for line in lines:
        row = list(map(int, line.split()))
        if len(row) != n:
            return False
        a.append(row)

    used = set()

    for i in range(n):
        values = [a[i][j] for j in range(n) if a[i][j] != 0]
        if len(values) != 2:
            return False
        if values[0] in used or values[1] in used:
            return False
        if values[0] <= 0 or values[1] <= 0:
            return False
        if values[0] * values[1] != y[i]:
            return False
        used.update(values)

    for j in range(n):
        values = [a[i][j] for i in range(n) if a[i][j] != 0]
        if len(values) != 2:
            return False
        if values[0] * values[1] != x[j]:
            return False

    return True

sample1 = """\
2
2 12
3 8
"""

sample2 = """\
3
5 8 18
2 30 12
"""

assert run(sample1) == "1 3\n2 4", "sample 1"
assert run(sample2) == "1 2 0\n5 0 6\n0 4 3", "sample 2"

case_min = """\
2
10 21
6 35
"""
assert validate(case_min, run(case_min)), "minimum size and forced orientation"

case_boundary = """\
2
600 500
1000 300
"""
assert validate(case_boundary, run(case_boundary)), "product 1000 boundary"

case_equal_rows = """\
4
15 120 90 80
60 60 60 60
"""
assert validate(case_equal_rows, run(case_equal_rows)), "equal row products"

case_max = """\
10
11 40 57 72 85 96 105 112 117 120
20 38 54 68 80 90 98 104 108 110
"""
assert validate(case_max, run(case_max)), "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 10 21 / 6 35` | Any valid (2\times2) grid | Minimum size and factor orientation |
| `2 / 600 500 / 1000 300` | Any valid (2\times2) grid | Boundary product (1000), plus large factors |
| `4 / 15 120 90 80 / 60 60 60 60` | Any valid (4\times4) grid | Many equal target products |
| `10 / 11 40 57 72 85 96 105 112 117 120 / 20 38 54 68 80 90 98 104 108 110` | Any valid (10\times10) grid | Maximum (n) and the full backtracking search |

The maximum-size case comes from a ten-cycle using the distinct values (1) through (20). Its row pairs are ((1,20),(2,19),\ldots,(10,11)), and the column products are chosen from the adjacent values around the cycle. Every required product stays below (1000), while all twenty cell values remain distinct.

## Edge Cases

The value (1) is handled exactly like every other positive integer. In the first sample, row zero has product (3), so the factor pair is (1,3). The column products (2) and (12) force (1) into the first column and (3) into the second. The solver never treats (1) as special, and its bit is recorded in `used_mask`, so a second (1) cannot be introduced later.

For a square product such as (36), the factor-pair generator enumerates every divisor (d) up to (\sqrt{36}), then stores the distinct pair ((d,36/d)). Thus ((4,9)) is considered even though (36) is a square. The pair ((6,6)) is deliberately excluded because the two cell values must be different.

For the orientation-sensitive case

```
2
10 21
6 35
```

row zero has factors (2) and (3). The first column accepts (2), while the second accepts (3). After placing them, the remaining row has product (35), and (5) and (7) are forced into the remaining cells. The reverse orientation would leave a column with an incompatible remaining product, so forward checking rejects it immediately or on the next recursive step.

The product boundary case

```
2
600 500
1000 300
```

has a valid grid

```
20 50
30 10
```

because the row products are (20\cdot50=1000) and (30\cdot10=300), while the column products are (20\cdot30=600) and (50\cdot10=500). The solver uses ordinary integer division for the remaining products, so values at the upper bound cause no special arithmetic case.

Finally, equal target products do not imply equal cell values. In the (4\times4) case with all row products equal to (60), different rows can use different factor pairs of (60). The global uniqueness check concerns the numbers placed in cells, not the required row and column products, so repeated target values are perfectly valid when the corresponding factor pairs can remain distinct.
