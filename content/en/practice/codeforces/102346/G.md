---
title: "CF 102346G - Getting Confidence"
description: "We have an (N times N) matrix. Row (i) represents ornament (i), and column (j) represents shelf position (j). The value (a{i,j}) measures how confident Fulano is that ornament (i) originally occupied position (j)."
date: "2026-08-14T02:04:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102346
codeforces_index: "G"
codeforces_contest_name: "2019-2020 ACM-ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 102346
solve_time_s: 104
verified: true
draft: false
---

[CF 102346G - Getting Confidence](https://codeforces.com/problemset/problem/102346/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an (N \times N) matrix. Row (i) represents ornament (i), and column (j) represents shelf position (j). The value (a_{i,j}) measures how confident Fulano is that ornament (i) originally occupied position (j).

We must place every ornament into exactly one position, so every row and every column is used exactly once. If ornament (i) is assigned to position (p_i), the score of the complete arrangement is

[
\prod_{i=1}^{N} a_{i,p_i}.
]

The task is to output the ornament occupying each position, with any arrangement achieving the maximum product being valid.

This is a maximum-product version of the assignment problem. The official problem archive gives (N \le 100), with a 1 second time limit and 256 MB memory limit.

The bound (N \le 100) immediately rules out enumerating permutations. There are (N!) possible arrangements, and even evaluating one arrangement costs (O(N)), giving (O(N \cdot N!)) time. At (N=100), this is roughly (100 \cdot 100! \approx 9.3 \times 10^{159}) elementary operations. A polynomial algorithm is required.

The first edge case is (N=1). For example,

```
1
100
```

has only one possible answer, `1`. An implementation that assumes there are at least two rows or columns can fail when constructing its matching arrays.

Another common mistake is allowing two ornaments to use the same position. Consider

```
2
10 9
10 1
```

The best valid arrangement is `2 1`, giving (9 \cdot 10 = 90). A greedy procedure that takes the largest value in each row independently chooses position 1 for both ornaments, which is not a valid permutation. The assignment constraint must be handled globally.

Ties also occur naturally. For

```
2
5 5
5 5
```

every permutation has product (25), so both `1 2` and `2 1` are correct. Code must not assume that the optimum is unique.

The values can also be as large as 100. For (N=100), a product can be as large as (100^{100}), far beyond fixed-width integer types in languages such as C++. We never compute this product directly. The transformation used by the solution avoids the overflow completely.

## Approaches

The direct approach is to enumerate every permutation of the (N) ornaments. For each permutation, we multiply the (N) selected matrix entries and keep the best arrangement. This is correct because every possible valid arrangement is represented by exactly one permutation, so eventually the optimum is examined. Its cost is (O(N \cdot N!)), which becomes unusable long before (N=100).

The structure of the problem gives us a better route. Every valid arrangement chooses exactly one cell from every row and every column, which is precisely a perfect matching in a complete bipartite graph. The only unusual part is that the matching weight is a product rather than a sum.

The logarithm removes that difference. Since every matrix value is positive,

\sum_i \log(a_{i,p_i}).
]

The logarithm is strictly increasing, so the arrangement with the largest product is exactly the arrangement with the largest sum of logarithms. We have converted the problem into a standard maximum-weight assignment problem.

We can equivalently minimize the costs

[
c_{i,j}=-\log(a_{i,j}).
]

The Hungarian algorithm solves this assignment problem in (O(N^3)) time. Its potential-based implementation maintains a partial matching and repeatedly finds an augmenting path for the next row. The standard implementation uses the arrays `u`, `v`, `p`, `way`, and `minv` to maintain the dual potentials and reconstruct each augmenting path.

Because all input values are between 1 and 100, the logarithms are small finite numbers. The intended competitive-programming implementation uses floating-point logarithms, as does the known solution approach for this problem.

The comparison is therefore:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N \cdot N!)) | (O(N)) | Too slow |
| Optimal | (O(N^3)) | (O(N^2)) | Accepted |

## Algorithm Walkthrough

1. Read the confidence matrix and replace every value (a_{i,j}) by the cost (-\log(a_{i,j})). We use a negative sign because the Hungarian implementation below is written for minimum-cost assignment, while we need to maximize the logarithmic score.

Since

\arg\min \sum_i -\log(a_{i,p_i}),
]

the optimal permutation is unchanged.
2. Maintain `p[j]`, where `p[j]` is the row currently assigned to column (j). Column zero is a virtual column used as the starting point of every augmentation.
3. Process the rows one at a time. When row (i) is introduced, temporarily attach it to the virtual column and search for an augmenting path leading to an unused real column.

The existing matching is already optimal for all previously processed rows. The new augmenting path is the mechanism that lets row (i) enter the matching while possibly moving some previously assigned rows to different columns.
4. During the search, maintain `minv[j]`, the smallest reduced cost currently known for reaching column (j), and `way[j]`, the previous column on that path.

The reduced cost is

[
c_{i,j}-u_i-v_j.
]

The potentials `u` and `v` make the reduced costs nonnegative in the maintained dual solution, allowing the shortest augmenting path to be expanded efficiently.
5. Choose the unused column with the smallest `minv` value. Let that value be `delta`. Update the potentials for the currently reachable part of the alternating tree and subtract `delta` from the remaining `minv` values.

This preserves the feasibility of the dual potentials while making at least one new column reachable at zero reduced cost.
6. Continue until an unused column is reached. At that point, follow `way` backwards from that column. Reverse the assignments along the resulting alternating path.

The new matching contains one more row than before, while every processed row still has exactly one column and every used column still has exactly one row.
7. After all (N) rows have been processed, every column has exactly one assigned row. The array `p[1], p[2], ..., p[N]` is already in the format required by the output: for each shelf position (j), `p[j]` is the ornament placed there.

### Why it works

The logarithm transformation preserves the ordering of all possible products, so solving the transformed additive assignment problem is equivalent to solving the original problem. The Hungarian algorithm maintains a valid matching for the processed rows together with dual potentials whose reduced costs are compatible with that matching. Each augmentation adds exactly one new row without breaking the assignment constraints, and the shortest augmenting path gives the minimum possible additional transformed cost. By induction, after processing row (i), the matching is optimal among all assignments of the first (i) rows to distinct columns. After the (N)-th augmentation, every row and column is included, so the resulting perfect matching is globally optimal.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve(data):
    it = iter(data.split())
    n = int(next(it))

    # cost[i][j] = -log(confidence)
    cost = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            x = int(next(it))
            cost[i][j] = -math.log(x)

    # Hungarian algorithm for minimum-cost assignment.
    #
    # p[j] = row currently assigned to column j.
    # way[j] = previous column in the augmenting path.
    u = [0.0] * (n + 1)
    v = [0.0] * (n + 1)
    p = [0] * (n + 1)
    way = [0] * (n + 1)

    for i in range(1, n + 1):
        p[0] = i
        j0 = 0

        minv = [float("inf")] * (n + 1)
        used = [False] * (n + 1)

        while True:
            used[j0] = True
            i0 = p[j0]

            delta = float("inf")
            j1 = 0

            for j in range(1, n + 1):
                if used[j]:
                    continue

                cur = cost[i0 - 1][j - 1] - u[i0] - v[j]

                if cur < minv[j]:
                    minv[j] = cur
                    way[j] = j0

                if minv[j] < delta:
                    delta = minv[j]
                    j1 = j

            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta

            j0 = j1

            if p[j0] == 0:
                break

        while j0 != 0:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1

    return " ".join(map(str, p[1:]))

def main():
    data = sys.stdin.buffer.read()
    if data:
        print(solve(data))

if __name__ == "__main__":
    main()
```

The input is read as one byte string and split once. This keeps parsing overhead small, which matters because the matrix contains up to 10,000 values.

The matrix is converted immediately to negative logarithmic costs. The `-1` indexing adjustment in `cost[i0 - 1][j - 1]` is necessary because the Hungarian arrays use one-based indexing, while Python lists use zero-based indexing.

The arrays `u` and `v` are the row and column potentials. `p` stores the current matching, while `way` stores enough predecessor information to reconstruct an augmenting path without storing the entire path explicitly. This is the standard (O(N^3)) potential formulation of Hungarian.

The virtual column `0` is not a real shelf position. Setting `p[0] = i` starts the augmentation from the currently processed ornament. It must never appear in the final answer, which is why the result uses `p[1:]`.

The update

```
u[p[j]] += delta
v[j] -= delta
```

is paired with

```
minv[j] -= delta
```

for unused columns. Omitting either part breaks the reduced-cost invariant and can produce an invalid or non-optimal matching.

There is no integer overflow because the code never forms the original product. The largest value passed to `math.log` is only 100, and the Hungarian potentials operate on sums of logarithms whose magnitudes are small.

## Worked Examples

### Sample 1

The matrix is

```
1 15 37
42 8 25
77 2 1
```

The Hungarian algorithm processes ornaments as rows. The matching `p` is indexed by shelf position, so after each augmentation it directly tells us which ornament currently occupies each position.

| Step | Added ornament | Current assignment by position | Interpretation |
| --- | --- | --- | --- |
| 1 | 1 | `[1, 0, 0]` | Ornament 1 takes position 1 in the current partial matching |
| 2 | 2 | `[2, 0, 1]` | Ornament 2 takes position 1 and ornament 1 moves to position 3 |
| 3 | 3 | `[3, 1, 2]` | The final augmenting path gives positions 1, 2, 3 to ornaments 3, 1, 2 |

The final arrangement is `3 1 2`. Its product is

[
77 \cdot 15 \cdot 25 = 28875.
]

The last augmentation is the interesting part. Ornament 3 strongly prefers position 1, but ornament 2 was already using that position. Instead of greedily rejecting the conflict, the augmenting path moves ornament 2 to position 3, which in turn moves ornament 1 to position 2. This is exactly the global reassignment that a greedy algorithm cannot perform.

### Sample 2

The matrix is

```
15 1
33 42
```

The algorithm proceeds as follows.

| Step | Added ornament | Current assignment by position | Interpretation |
| --- | --- | --- | --- |
| 1 | 1 | `[1, 0]` | Ornament 1 takes position 1 |
| 2 | 2 | `[1, 2]` | Ornament 2 takes the remaining position 2 |

The resulting output is `1 2`, with product

[
15 \cdot 42 = 630.
]

There is no conflict requiring an augmenting path longer than one edge in this example. It demonstrates the base case of the matching process and confirms that the output is indexed by positions rather than by ornaments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N^3)) | There are (N) augmentation phases, and each phase performs (O(N^2)) work in the worst case |
| Space | (O(N^2)) | The transformed confidence matrix uses (O(N^2)) memory, while the Hungarian arrays use (O(N)) |

For (N=100), (O(N^3)) means roughly one million inner-loop iterations, compared with the factorial number of arrangements in brute force. The matrix itself contains only 10,000 entries, so the memory requirement is comfortably within the 256 MB limit. The archived contest statement specifies a 1 second time limit and 256 MB memory limit.

## Test Cases

The following harness embeds the same `solve` implementation so the tests can be executed directly. Since multiple optimal permutations are possible, the custom cases are chosen so that the expected arrangement is uniquely determined whenever an exact output assertion is used.

```python
import sys
import io
import math

def solve(data):
    it = iter(data.split())
    n = int(next(it))

    cost = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            x = int(next(it))
            cost[i][j] = -math.log(x)

    u = [0.0] * (n + 1)
    v = [0.0] * (n + 1)
    p = [0] * (n + 1)
    way = [0] * (n + 1)

    for i in range(1, n + 1):
        p[0] = i
        j0 = 0

        minv = [float("inf")] * (n + 1)
        used = [False] * (n + 1)

        while True:
            used[j0] = True
            i0 = p[j0]

            delta = float("inf")
            j1 = 0

            for j in range(1, n + 1):
                if used[j]:
                    continue

                cur = cost[i0 - 1][j - 1] - u[i0] - v[j]

                if cur < minv[j]:
                    minv[j] = cur
                    way[j] = j0

                if minv[j] < delta:
                    delta = minv[j]
                    j1 = j

            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta

            j0 = j1

            if p[j0] == 0:
                break

        while j0 != 0:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1

    return " ".join(map(str, p[1:]))

def run(inp: str) -> str:
    return solve(inp.encode()).strip()

# Provided sample 1
assert run(
    """3
1 15 37
42 8 25
77 2 1
"""
) == "3 1 2", "sample 1"

# Provided sample 2
assert run(
    """2
15 1
33 42
"""
) == "1 2", "sample 2"

# Minimum size
assert run(
    """1
100
"""
) == "1", "minimum-size case"

# All values equal, the deterministic Hungarian implementation returns identity
assert run(
    """3
7 7 7
7 7 7
7 7 7
"""
) == "1 2 3", "all-equal values"

# Greedy trap: row 1 and row 2 both prefer position 1,
# but the optimal valid permutation is 2 1.
assert run(
    """2
10 9
10 1
"""
) == "2 1", "greedy trap"

# Boundary values and a unique optimum
assert run(
    """2
100 1
1 100
"""
) == "1 2", "boundary values"

# Maximum-size case with a unique optimum.
# Diagonal entries are 100, all other entries are 1.
n = 100
rows = []
for i in range(n):
    row = ["1"] * n
    row[i] = "100"
    rows.append(" ".join(row))

max_case = str(n) + "\n" + "\n".join(rows) + "\n"
expected = " ".join(str(i) for i in range(1, n + 1))

assert run(max_case) == expected, "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 100` | `1` | Minimum size and one-based indexing |
| A (3 \times 3) matrix filled with `7` | `1 2 3` | Ties and deterministic matching |
| `2 / 10 9 / 10 1` | `2 1` | Global assignment and failure of greedy selection |
| `2 / 100 1 / 1 100` | `1 2` | Maximum input value and unique optimum |
| (100 \times 100), diagonal `100`, elsewhere `1` | `1 2 ... 100` | Maximum (N), performance, and boundary indexing |

## Edge Cases

For (N=1), the input

```
1
100
```

starts the only augmentation with row 1. Column 1 is immediately free, so the path contains only that column and `p[1]` becomes 1. The returned output is `1`. There is no special-case branch in the algorithm, which is useful because the general matching invariant already handles the smallest instance.

For the greedy-conflict case

```
2
10 9
10 1
```

the first row initially takes position 1 because (10 > 9). When row 2 is processed, its best position is also position 1. The augmenting-path search does not simply reject that choice. It considers moving row 1 to position 2, producing the assignment row 1 to position 2 and row 2 to position 1. The output is `2 1`, whose product is (9 \cdot 10 = 90), compared with (10 \cdot 1 = 10) for the other valid assignment.

For equal values,

```
3
7 7 7
7 7 7
7 7 7
```

every valid permutation has the same product (7^3). During each augmentation, the first available column is selected consistently, giving `1 2 3`. The problem allows any optimal permutation, so this deterministic tie behavior is valid.

For the maximum value boundary,

```
2
100 1
1 100
```

the logarithmic costs are finite because every value is positive. The diagonal assignment has product (10000), while the other assignment has product (1). The transformed costs preserve this ordering, so the algorithm returns `1 2`.

For (N=100), the product of the selected values could be (100^{100}), but the implementation never stores that number. Each matrix entry becomes `-math.log(100)` or another small floating-point value, and the Hungarian algorithm only adds and subtracts these logarithmic costs. The assignment arrays remain linear in (N), while the matrix occupies (O(N^2)) memory. This is exactly the scale for which the (O(N^3)) assignment algorithm is appropriate.
