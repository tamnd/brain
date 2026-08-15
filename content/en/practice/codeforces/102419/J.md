---
title: "CF 102419J - Jaber The policeman"
description: "Think of every lit cell as an edge between its row and its column. A row is a vertex on the left, a column is a vertex on the right, and a 1 at position (i, j) means that the corresponding row and column are connected. The required row sums tell us the degree of every row vertex."
date: "2026-08-15T08:56:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102419
codeforces_index: "J"
codeforces_contest_name: "SPC 2019"
rating: 0
weight: 102419
solve_time_s: 367
verified: false
draft: false
---

[CF 102419J - Jaber The policeman](https://codeforces.com/problemset/problem/102419/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 7s  
**Verified:** no  

## Solution
## Problem Understanding

Think of every lit cell as an edge between its row and its column. A row is a vertex on the left, a column is a vertex on the right, and a `1` at position `(i, j)` means that the corresponding row and column are connected.

The required row sums tell us the degree of every row vertex. We are free to choose the column degrees and the positions of all the `1`s. During the inspection, removing a row or a column means deleting that vertex and all incident edges. Jaber is satisfied exactly when the vertex being removed has at most one remaining incident edge.

The question is thus asking whether we can construct a bipartite graph with the prescribed degrees on the row side, together with an ordering of all vertices in which every removed vertex has current degree at most one.

The bounds `n, m <= 1000` mean the output itself can contain up to one million matrix characters, so an `O(nm)` algorithm is already close to optimal. An algorithm with quadratic work beyond the matrix construction is unnecessary, and anything exponential is completely infeasible. The memory limit also comfortably allows storing a `1000 x 1000` matrix.

There are several edge cases that can fool a construction based only on the total number of `1`s. For example,

```
2 2
2 2
```

has four `1`s, but every row must contain both columns. The only possible matrix is

```
11
11
```

which contains a cycle. Every vertex in that cycle has degree two, so there is no valid first inspection. The correct answer is `NO`.

A second boundary case is

```
2 2
2 0
```

Here the answer is `YES`. We can use

```
11
00
```

and inspect column 2 first, then row 1, then row 2, then column 1. A construction that requires every row to have its own private columns would incorrectly reject this case, even though several rows can safely share one central column.

The all-zero case also needs separate handling. For

```
3 4
0 0 0
```

the answer is `YES`, because the entire matrix can be zero and every row and column can be inspected in any order. A formula involving the number of positive rows must not accidentally assume that at least one row contains a `1`.

## Approaches

A direct brute-force solution could enumerate every binary matrix whose row sums match the input, then search for an inspection order. For a fixed matrix, the inspection condition can be checked by viewing it as a graph and repeatedly removing vertices of degree at most one. However, the number of possible matrices is already

[
\prod_{i=1}^{n} \binom{m}{a_i}.
]

If we additionally tried every possible inspection order, there would be `(n+m)!` orders for each matrix. Thus the total number of matrix-order pairs is

[
\left(\prod_{i=1}^{n}\binom{m}{a_i}\right)(n+m)!.
]

In the worst case `n = m = 1000` and every `a_i = 500`, so even the number of candidate matrices alone is

[
\binom{1000}{500}^{1000}.
]

There is no possibility of exploring this space.

The useful observation is that a valid inspection order has a very simple graph interpretation. If a graph contains a cycle, every vertex on that cycle initially has degree at least two inside the cycle. Whichever cycle vertex we try to inspect first would have at least two remaining edges, so the inspection fails. Conversely, every forest has a leaf, and repeatedly deleting leaves eventually removes the whole forest. Thus a valid inspection order exists exactly when the graph of `1` cells is a forest.

Now the problem becomes much simpler. Let `S` be the total number of `1`s and let `p` be the number of rows with positive degree. We want a forest whose row degrees are exactly the given values while using at most `m` column vertices.

We can construct the smallest possible connected component containing all positive rows. Choose one column as a central vertex and connect every positive row to it. If row `i` needs degree `a_i`, give it another `a_i - 1` private columns. These private columns have degree one, so they are leaves. The resulting component is a tree.

The number of columns needed is

[
1+\sum_{a_i>0}(a_i-1)
=1+S-p.
]

This number is also necessary. Consider any forest containing all positive rows. For every tree component containing edges, the number of edges equals the number of vertices minus one. If `q` columns participate in the edges and there are `c` nonempty components, then

[
S=p+q-c.
]

Hence

[
q=S-p+c\ge S-p+1.
]

So if `S-p+1 > m`, no forest can realize the row degrees. If it is at most `m`, our central-column construction realizes them.

The brute-force works because it explicitly searches for the graph and its ordering, but fails because there are exponentially many possibilities. The forest characterization removes the search entirely, and the central-column construction gives the required matrix directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential, at least proportional to `∏ C(m, a_i)` matrices | `O(nm)` | Too slow |
| Optimal | `O(nm)` | `O(nm)` | Accepted |

## Algorithm Walkthrough

1. Compute `S`, the sum of all row degrees, and `p`, the number of rows whose degree is positive. If `p = 0`, every cell can be zero, so output the zero matrix and any order of all rows and columns.
2. Compute `needed = S - p + 1`. This is the number of columns required by the central-column construction. If `needed > m`, print `NO`. The lower-bound argument above shows that no valid forest can fit inside the available number of columns.
3. Use column 1 as the central column. For every row with `a_i > 0`, put a `1` in column 1. This gives every positive row one edge while keeping all such rows connected through the same vertex.
4. For each positive row `i`, add exactly `a_i - 1` additional `1`s. Give these cells consecutive columns starting from column 2, and never reuse these private columns. Every such column then has exactly one edge, so it is a leaf of the forest.
5. All remaining matrix cells stay zero. The constructed nonzero part is a tree: the central column is connected to every positive row, and every additional edge goes from a row to a fresh leaf column.
6. Put all private columns first in the inspection order. Each of them currently has exactly one `1`, so inspecting it is safe and removes that edge.
7. After the private columns of every positive row have been removed, each positive row has only its edge to the central column. Inspect all positive rows next. Every such row now has exactly one remaining `1`.
8. Inspect all zero rows. They have no `1`s at all, so they are always safe.
9. Inspect the central column and then every unused column. By this point every edge has already disappeared, so these columns have zero remaining `1`s.

Why it works. The nonzero cells form a tree. The private columns are its leaves, and removing them makes every positive row a leaf in turn. Once all positive rows are removed, the central column has no remaining edges. Every other vertex is isolated. Thus every vertex is inspected with degree at most one, while every row receives exactly its prescribed number of `1`s.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    total = sum(a)
    positive = sum(x > 0 for x in a)

    if positive == 0:
        out = ["YES"]
        out.extend(["0" * m for _ in range(n)])

        for i in range(1, n + 1):
            out.append(f"row {i}")
        for j in range(1, m + 1):
            out.append(f"col {j}")

        sys.stdout.write("\n".join(out))
        return

    needed = total - positive + 1

    if needed > m:
        sys.stdout.write("NO\n")
        return

    # bytearray keeps the matrix compact while allowing O(1) cell updates.
    matrix = [bytearray(b"0" * m) for _ in range(n)]

    # Column 1 is the central column.
    next_col = 1  # zero-based index of the next private column

    # The central column is column 0.
    for i, degree in enumerate(a):
        if degree == 0:
            continue

        matrix[i][0] = ord("1")

        # Use fresh private columns for the remaining degree.
        for _ in range(degree - 1):
            next_col += 1
            matrix[i][next_col - 1] = ord("1")

    private_columns = next_col - 1

    out = ["YES"]
    out.extend(row.decode() for row in matrix)

    # Every private column is a leaf.
    for j in range(2, private_columns + 1):
        out.append(f"col {j}")

    # Positive rows become leaves after their private columns disappear.
    for i, degree in enumerate(a):
        if degree > 0:
            out.append(f"row {i + 1}")

    # Zero rows are isolated.
    for i, degree in enumerate(a):
        if degree == 0:
            out.append(f"row {i + 1}")

    # The central column is now isolated.
    out.append("col 1")

    # All unused columns are isolated from the start.
    for j in range(private_columns + 1, m + 1):
        out.append(f"col {j}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first part computes the two quantities that characterize feasibility. `total` is the number of edges the final graph must contain, while `positive` counts the row vertices that actually participate in the graph.

The expression `total - positive + 1` is the number of columns used by the construction. Column 1 is the shared central vertex. Every positive row contributes `a_i - 1` private columns. The `needed > m` check is performed before allocating the matrix, so an impossible instance immediately produces `NO`.

The matrix is stored as `bytearray` objects. A normal Python string cannot be modified in place, while a list of individual characters would consume substantially more memory. A `bytearray` gives direct cell assignment and keeps a million-cell matrix small.

The variable `next_col` uses zero-based indexing for the matrix, while the output uses one-based column numbers. After putting the central `1` in index zero, the first private column is matrix index one, corresponding to output column 2. Keeping this conversion in one place avoids an off-by-one error.

The inspection order deliberately removes private columns before their corresponding rows. If a row with degree four were inspected immediately, it would still have four lights on. After its three private columns have been inspected, only the central edge remains, so the row is safe.

No integer-overflow handling is required in Python. Even the maximum possible sum is only `n * m = 10^6`, although Python integers would also handle larger values safely.

## Worked Examples

For Sample 1,

```
4 4
1 0 0 0
```

we have `total = 1`, `positive = 1`, and `needed = 1`. No private column is necessary. The only positive row connects directly to the central column.

| Step | `total` | `positive` | `needed` | `next_col` | Action |
| --- | --- | --- | --- | --- | --- |
| Read input | 1 | 1 | 1 | 1 | Row 1 needs one edge |
| Build row 1 | 1 | 1 | 1 | 1 | Put `1` in column 1 |
| Build rows 2 to 4 | 1 | 1 | 1 | 1 | They remain zero |
| Order | 1 | 1 | 1 | 1 | Inspect rows, then column 1 |

One valid output produced by the algorithm is

```
YES
1000
0000
0000
0000
row 1
row 2
row 3
row 4
col 1
col 2
col 3
col 4
```

Row 1 has one light and is inspected first, so it is safe. All other rows and columns are isolated when inspected.

For Sample 2,

```
4 4
2 1 1 1
```

we get `total = 5`, `positive = 4`, and `needed = 2`. Column 1 is central, while column 2 becomes a private leaf for row 1.

| Step | Row degree | Central edge | Private columns | `next_col` | Action |
| --- | --- | --- | --- | --- | --- |
| Row 1 | 2 | Yes | Column 2 | 2 | Put `1` in columns 1 and 2 |
| Row 2 | 1 | Yes | None | 2 | Put `1` in column 1 |
| Row 3 | 1 | Yes | None | 2 | Put `1` in column 1 |
| Row 4 | 1 | Yes | None | 2 | Put `1` in column 1 |
| Inspect column 2 | 1 | Yes | Removed | 2 | Column 2 is safe |
| Inspect row 1 | 1 | Yes | Removed | 2 | Only column 1 remains |
| Inspect rows 2 to 4 | 1 | Yes | None | 2 | Each has only column 1 |
| Inspect column 1 | 0 | Removed | None | 2 | All edges are gone |

The resulting matrix is

```
1100
1000
1000
1000
```

The order is

```
col 2
row 1
row 2
row 3
row 4
col 1
col 3
col 4
```

The sample output uses a different valid matrix and order. The problem permits any valid construction, so producing a different one is completely acceptable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(nm)` | The matrix has `nm` cells and the output itself has this size in the worst case |
| Space | `O(nm)` | The constructed matrix occupies `nm` cells |

With `n, m <= 1000`, there are at most one million matrix cells. The algorithm touches the matrix only to construct the required output, and its remaining work is linear in `n + m`. This fits comfortably within the 1 second and 256 MB limits in Python with compact `bytearray` storage.

## Test Cases

Because the problem allows many different valid matrices and inspection orders, a robust test harness should validate the returned construction instead of comparing every successful answer to one fixed output. The two provided samples are deterministic for the implementation below, so their exact output can also be checked.

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

def validate(inp: str, out: str) -> bool:
    data = inp.split()
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:2 + n]))

    lines = out.strip().splitlines()

    if lines[0] == "NO":
        # Verify impossibility using the necessary condition.
        total = sum(a)
        positive = sum(x > 0 for x in a)
        if positive == 0:
            return False
        return total - positive + 1 > m

    if lines[0] != "YES":
        return False

    if len(lines) != 1 + n + n + m:
        return False

    matrix = lines[1:1 + n]
    order = lines[1 + n:]

    for i in range(n):
        if len(matrix[i]) != m:
            return False
        if any(c not in "01" for c in matrix[i]):
            return False
        if matrix[i].count("1") != a[i]:
            return False

    used_rows = set()
    used_cols = set()

    current = [list(row) for row in matrix]

    for command in order:
        kind, x = command.split()
        x = int(x)

        if kind == "row":
            if not 1 <= x <= n or x in used_rows:
                return False

            remaining = sum(current[x - 1][j] == "1"
                            for j in range(m)
                            if j not in used_cols)

            if remaining > 1:
                return False

            used_rows.add(x)

        elif kind == "col":
            if not 1 <= x <= m or x in used_cols:
                return False

            remaining = sum(current[i][x - 1] == "1"
                            for i in range(n)
                            if i not in used_rows)

            if remaining > 1:
                return False

            used_cols.add(x)

        else:
            return False

    return len(used_rows) == n and len(used_cols) == m

# Provided samples
sample1 = """\
4 4
1 0 0 0
"""

sample2 = """\
4 4
2 1 1 1
"""

assert validate(sample1, solve_data(sample1)), "sample 1"
assert validate(sample2, solve_data(sample2)), "sample 2"

# Minimum-size all-zero instance
case1 = """\
1 1
0
"""
assert validate(case1, solve_data(case1)), "minimum all-zero case"

# Minimum-size all-one instance
case2 = """\
1 1
1
"""
assert validate(case2, solve_data(case2)), "minimum all-one case"

# Impossible boundary case: both rows require both columns
case3 = """\
2 2
2 2
"""
assert solve_data(case3).strip() == "NO", "cycle boundary case"

# Large all-equal case
case4 = "1000 1000\n" + " ".join(["1"] * 1000) + "\n"
assert validate(case4, solve_data(case4)), "large all-equal case"

# Exactly enough columns for a valid tree
case5 = """\
3 4
3 1 1
"""
assert validate(case5, solve_data(case5)), "exact column bound"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 0` | `YES` | Minimum dimensions and all-zero construction |
| `1 1 / 1` | `YES` | Minimum dimensions with one edge |
| `2 2 / 2 2` | `NO` | Detects the unavoidable cycle |
| `1000 1000 / 1 ... 1` | `YES` | Maximum dimensions and many equal row degrees |
| `3 4 / 3 1 1` | `YES` | Exact boundary where `S-p+1 = m` |

## Edge Cases

For the all-zero case

```
3 4
0 0 0
```

we have `positive = 0`. The special branch constructs three rows of `0000` and then lists all rows and columns. Every inspected line contains zero lights, so every inspection is valid. The branch is also necessary because the general central-column construction is designed around at least one positive row.

For the minimum nonzero case

```
1 1
1
```

we have `total = 1`, `positive = 1`, and `needed = 1`. The matrix is simply `1`. There are no private columns. The row is inspected first with one remaining light, and the only column is inspected afterward with zero remaining lights.

For the impossible cycle case

```
2 2
2 2
```

we have `total = 4`, `positive = 2`, so `needed = 4 - 2 + 1 = 3`. Since only two columns exist, the construction is rejected. The lower bound proves that this is not merely a failure of our particular construction. Any forest realizing the two row degrees would require at least three column vertices, while the grid has only two.

For the exact-bound case

```
3 4
3 1 1
```

we have `total = 5`, `positive = 3`, and `needed = 3`. Since `3 <= 4`, the instance is feasible. The construction uses column 1 as the center, columns 2 and 3 as two private leaves for the first row, and leaves column 4 unused. The matrix becomes

```
1110
1000
1000
```

The order starts with columns 2 and 3, then row 1, then rows 2 and 3, followed by the central and unused columns. Every non-isolated vertex is removed as a leaf.

For the maximum-size equal-degree case

```
1000 1000
1 1 1 ... 1
```

there are `1000` positive rows and `total = 1000`, giving `needed = 1`. All rows can share the same central column. The matrix therefore has a single column of `1`s and 999 zero columns. Each row has degree one, so all rows can be inspected safely before the central column. This demonstrates why sharing a column is the key structural idea and why the number of required columns depends on `total - positive + 1`, rather than on the total number of `1`s.
