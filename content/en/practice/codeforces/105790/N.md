---
title: "CF 105790N - Shield Navigation"
description: "We have an $N times M$ grid. Each time a shield is built at position $(x,y)$, it protects every cell in row $x$ and every cell in column $y$. A cell is usable if it is protected by at least one shield. There are two types of operations. A type 1 operation builds a new shield."
date: "2026-06-26T03:51:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105790
codeforces_index: "N"
codeforces_contest_name: "UDESC Selection Contest 2024-1"
rating: 0
weight: 105790
solve_time_s: 51
verified: true
draft: false
---

[CF 105790N - Shield Navigation](https://codeforces.com/problemset/problem/105790/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an $N \times M$ grid. Each time a shield is built at position $(x,y)$, it protects every cell in row $x$ and every cell in column $y$. A cell is usable if it is protected by at least one shield.

There are two types of operations.

A type 1 operation builds a new shield.

A type 2 operation asks whether an Almeiding starting at $(x_i,y_i)$ can reach $(x_f,y_f)$ using only protected cells and moving one step at a time in the four cardinal directions.

The grid itself can contain up to $10^6$ cells, while the number of queries is as large as $2 \cdot 10^5$. Any solution that tries to maintain the state of every protected cell or perform a graph search for each query is immediately too slow. Even a single BFS over a grid of size $10^6$ would already be expensive, and doing that repeatedly is impossible. We need an $O(1)$ or $O(\log N)$ answer per query.

The main danger is misunderstanding the connectivity structure created by the shields.

Consider this input:

```
3 3 2
1 2 2
2 2 1 2 3
```

The shield activates row 2 and column 2. Both cells $(2,1)$ and $(2,3)$ lie on the protected row, so the answer is:

```
SIM
```

A naive implementation that only checks whether the endpoints lie on the same protected row or column would fail on more general cases.

Another interesting case is:

```
3 3 2
1 2 2
2 1 2 3 2
```

The start and end cells are both protected because they belong to column 2. The correct answer is:

```
SIM
```

Even though the cells are in different rows, the entire column is protected.

Finally:

```
3 3 2
1 2 2
2 1 1 3 3
```

Neither endpoint is protected. The correct answer is:

```
NAO
```

A path cannot even start or end on an unprotected cell.

## Approaches

A brute-force solution would explicitly mark every protected cell and, for each type 2 query, run BFS or DFS between the two endpoints. This is correct because it directly simulates movement in the protected region.

The problem is scale. A single shield can affect an entire row and an entire column. With up to $10^6$ cells and $2 \cdot 10^5$ queries, repeatedly exploring the grid is far beyond the limit.

The key observation comes from understanding what a shield actually creates.

When a shield is built at $(x,y)$, row $x$ becomes fully protected and column $y$ becomes fully protected. Their intersection cell $(x,y)$ connects the row and the column together.

Since every shield always activates both one row and one column, every protected structure contains at least one row-column intersection. Any protected cell belongs either to an activated row or to an activated column. From such a cell, we can move to an intersection, and from there to any other protected row or column activated by shields. As a result, all protected cells belong to a single connected component.

That completely changes the problem.

A type 2 query does not require checking connectivity at all. We only need to verify that both endpoints are protected. If both are protected, they automatically belong to the unique protected component and are reachable from each other. If either endpoint is unprotected, the answer is impossible.

We can maintain two boolean arrays:

One array records which rows have ever appeared as a shield center.

The other records which columns have ever appeared as a shield center.

A cell $(r,c)$ is protected exactly when row $r$ is active or column $c$ is active.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force BFS per query | O(Q · N · M) worst case | O(N · M) | Too slow |
| Optimal row/column tracking | O(Q) | O(N + M) | Accepted |

## Algorithm Walkthrough

1. Create a boolean array `row` of size `N` and a boolean array `col` of size `M`.
2. For a type 1 query `(x, y)`, mark `row[x] = True` and `col[y] = True`.
3. For a type 2 query, determine whether the start cell is protected.

A cell `(r, c)` is protected if `row[r]` is active or `col[c]` is active.
4. Determine whether the destination cell is protected using the same rule.
5. If both cells are protected, print `"SIM"`.

Every protected cell belongs to the same connected protected region.
6. Otherwise print `"NAO"`.

### Why it works

Every shield activates an entire row and an entire column. Those two structures intersect at the shield center, creating a connection between them.

Any protected cell lies either on an active row or on an active column. From that cell, we can move along its row or column to a shield intersection. Through intersections, every protected row and protected column becomes part of one connected structure. Thus, all protected cells are mutually reachable.

The only reason a query can fail is that the start or destination cell is not protected. That is exactly what the algorithm checks.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, q = map(int, input().split())

rows = [False] * n
cols = [False] * m

ans = []

for _ in range(q):
    data = list(map(int, input().split()))

    if data[0] == 1:
        _, x, y = data
        rows[x - 1] = True
        cols[y - 1] = True
    else:
        _, xi, yi, xf, yf = data

        start_ok = rows[xi - 1] or cols[yi - 1]
        finish_ok = rows[xf - 1] or cols[yf - 1]

        ans.append("SIM" if start_ok and finish_ok else "NAO")

sys.stdout.write("\n".join(ans))
```

The two arrays are the entire state of the problem.

When a shield is created, we do not mark all cells in its row or column. Doing that would be too expensive. Instead, we only remember that the row and column are active.

For a query cell `(r,c)`, the protection condition is exactly:

```
rows[r] or cols[c]
```

This directly matches the definition of protection.

The implementation uses zero-based indexing internally, so every coordinate read from input is decreased by one before accessing the arrays.

No graph construction, BFS, DFS, or union-find structure is needed because connectivity is already implied by the geometry of the shields.

## Worked Examples

### Example 1

Input:

```
3 3 3
1 2 2
2 2 1 2 3
2 1 1 3 3
```

State evolution:

| Step | Operation | Active Rows | Active Cols | Result |
| --- | --- | --- | --- | --- |
| 1 | Build (2,2) | {2} | {2} | - |
| 2 | Query (2,1) → (2,3) | {2} | {2} | SIM |
| 3 | Query (1,1) → (3,3) | {2} | {2} | NAO |

For the first query, both cells lie on row 2, which is active. For the second query, neither endpoint is protected.

### Example 2

Input:

```
3 3 4
2 1 1 3 3
1 1 1
2 1 1 3 3
2 3 1 1 3
```

State evolution:

| Step | Operation | Active Rows | Active Cols | Result |
| --- | --- | --- | --- | --- |
| 1 | Query (1,1) → (3,3) | {} | {} | NAO |
| 2 | Build (1,1) | {1} | {1} | - |
| 3 | Query (1,1) → (3,3) | {1} | {1} | NAO |
| 4 | Query (3,1) → (1,3) | {1} | {1} | SIM |

The last query succeeds because both cells belong to active column 1 or active row 1, placing them inside the protected component.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(Q) | Each query performs only a few array accesses |
| Space | O(N + M) | One boolean array for rows and one for columns |

Since $Q \le 2 \cdot 10^5$ and $N \cdot M \le 10^6$, linear processing of the queries is easily fast enough. No operation depends on the size of the grid itself beyond the two arrays.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m, q = map(int, input().split())
    rows = [False] * n
    cols = [False] * m

    out = []

    for _ in range(q):
        a = list(map(int, input().split()))

        if a[0] == 1:
            rows[a[1] - 1] = True
            cols[a[2] - 1] = True
        else:
            s = rows[a[1] - 1] or cols[a[2] - 1]
            t = rows[a[3] - 1] or cols[a[4] - 1]
            out.append("SIM" if s and t else "NAO")

    return "\n".join(out)

# sample 1
assert run(
"""3 3 3
1 2 2
2 2 1 2 3
2 1 1 3 3
"""
) == "SIM\nNAO"

# sample 2
assert run(
"""3 3 4
2 1 1 3 3
1 1 1
2 1 1 3 3
2 3 1 1 3
"""
) == "NAO\nNAO\nSIM"

# minimum grid, no shield
assert run(
"""1 1 1
2 1 1 1 1
"""
) == "NAO"

# single shield, same cell
assert run(
"""1 1 2
1 1 1
2 1 1 1 1
"""
) == "SIM"

# protected through row
assert run(
"""4 4 2
1 3 2
2 3 1 3 4
"""
) == "SIM"

# one endpoint protected, one not
assert run(
"""4 4 2
1 2 2
2 2 1 4 4
"""
) == "NAO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 grid, no shield | NAO | Unprotected start/end |
| 1×1 grid, shield present | SIM | Smallest positive case |
| Same active row | SIM | Row protection logic |
| One protected endpoint | NAO | Both endpoints must be protected |
| Sample 1 | SIM, NAO | Official behavior |
| Sample 2 | NAO, NAO, SIM | Connectivity after activation |

## Edge Cases

Consider:

```
1 1 1
2 1 1 1 1
```

No shield has been built. The row is inactive and the column is inactive. The algorithm evaluates:

```
rows[1] OR cols[1] = false
```

for both endpoints, producing:

```
NAO
```

which is correct because the only cell is unprotected.

Now consider:

```
3 3 2
1 2 2
2 1 2 3 2
```

After building the shield, row 2 and column 2 become active. Both endpoints lie on column 2, so both are protected. The algorithm returns:

```
SIM
```

Even though the rows differ, movement along the active column is possible.

Finally:

```
4 4 2
1 2 2
2 2 1 4 4
```

The start cell `(2,1)` is protected because row 2 is active. The destination `(4,4)` is not protected because neither row 4 nor column 4 is active. The algorithm detects this immediately and prints:

```
NAO
```

No path can end on an unprotected cell, so the answer is correct.
