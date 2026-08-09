---
title: "CF 102439B - Varvara and matrix"
description: "We have an (n times m) matrix whose entries are integers from (0) to (k). A zero marks an unknown cell, and the special condition is that every row and every column contains at most one zero. We must replace every zero independently by either (A) or (B)."
date: "2026-08-10T06:41:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102439
codeforces_index: "B"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Semifinal"
rating: 0
weight: 102439
solve_time_s: 364
verified: true
draft: false
---

[CF 102439B - Varvara and matrix](https://codeforces.com/problemset/problem/102439/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an (n \times m) matrix whose entries are integers from (0) to (k). A zero marks an unknown cell, and the special condition is that every row and every column contains at most one zero. We must replace every zero independently by either (A) or (B).

The beauty of the matrix counts pairs of rows and pairs of columns whose four intersection cells all contain the same value. We are not asked to preserve the actual set of beautiful rectangles, only its total count. The key consequence is that every rectangle containing a zero was not beautiful before the replacement, because four zero corners are impossible under the one-zero-per-row and one-zero-per-column condition. Thus the only possible change is that some previously non-beautiful rectangle becomes beautiful after zeros are filled. The task is exactly to prevent every such new rectangle.

The dimensions are at most (1000), so scanning the entire matrix, or doing a constant amount of work per cell, is practical. In contrast, enumerating all pairs of rows and all pairs of columns already gives

249,500,250,000
]

rectangles in the largest square case. That immediately rules out algorithms that inspect every rectangle. The number of zeros is also at most (1000), because zeros form a matching between rows and columns. This small number of unknown cells is what makes a Boolean constraint formulation possible.

The value (k) can be as large as (nm), but its magnitude does not affect the algorithm. We only care whether a fixed cell equals (A), equals (B), or equals neither.

There are several edge cases that a direct approach can mishandle. First, a single zero may be forbidden from taking one of the two values. For example,

```
2 2
2
1 2
0 1
1 1
```

The zero cannot become (1), because that would create an all-(1) rectangle. It can become (2), so the correct result is `Yes`, for example with

```
2 1
1 1
```

A careless algorithm that treats every zero as freely assignable could accidentally create the rectangle.

A more subtle case is when one zero is forbidden from taking both values. Consider

```
3 3
2
1 2
1 1 1
1 0 2
1 2 2
```

If the center becomes (1), the upper-left (2\times2) rectangle becomes all (1). If it becomes (2), the lower-right (2\times2) rectangle becomes all (2). No replacement exists, so the answer is `No`. The two restrictions come from different rectangles and have to be combined.

Another edge case involves two zeros. Consider

```
2 2
2
1 2
0 1
1 0
```

The two zeros are opposite corners and the other two corners are (1). They cannot both be replaced by (1), because that would create an all-(1) rectangle. They can, however, receive different values, so the answer is `Yes`. Handling only constraints involving one zero would miss this condition.

These are exactly the types of restrictions captured by the 2-SAT formulation used below. The original statement and constraints are available in the official Codeforces Gym archive.

## Approaches

A direct brute-force solution would try all (2^z) replacements, where (z) is the number of zeros, and calculate the beauty after every replacement. For each assignment, enumerating every rectangle takes

[
O(n^2m^2)
]

time. In the worst case (n=m=1000), there are exactly (249,500,250,000) rectangles, so the brute-force work is roughly

[
249,500,250,000 \cdot 2^{1000}
]

rectangle checks. Even checking every rectangle once is already far beyond the limit.

The next observation is that we do not actually need to calculate the beauty. Every rectangle that was beautiful before contains no zero, and its four values remain unchanged. Hence the original beautiful rectangles are automatically preserved. We only have to forbid rectangles that become beautiful after replacing their zero corners.

Because every row and column has at most one zero, a rectangle contains at most two zeros. If it contains exactly one zero, the other three corners are fixed. The zero must not receive their common value. If it contains two zeros, they must occupy opposite corners, and the other two corners are fixed. If those two fixed corners both equal (A), the two zeros cannot both receive (A). The same applies to (B).

This gives only two kinds of logical restrictions. A zero may be forbidden from taking (A) or (B), or two zeros may be forbidden from simultaneously taking (A) or simultaneously taking (B). Both are clauses involving at most two Boolean variables, so the entire problem becomes 2-SAT.

The remaining difficulty is finding all one-zero restrictions quickly. For a zero at ((x,y)), suppose we want to know whether assigning it (A) would create an all-(A) rectangle. We need another row (r) and another column (c) satisfying

[
a_{x,c}=A,\qquad
a_{r,c}=A,\qquad
a_{r,y}=A.
]

For every row (x), build a bitset containing all rows (r) that have an (A) somewhere in a column where row (x) also has (A). Then intersect it with the bitset of rows having (A) in column (y). A nonempty intersection means that the required rectangle exists.

The same construction is done for (B). This is the bitset optimization used in standard solutions to this problem.

For two-zero rectangles, there are at most (1000) zeros, so checking all pairs directly costs only (O(z^2)). We then solve the resulting 2-SAT instance with strongly connected components.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^z n^2m^2)) | (O(nm)) | Too slow |
| Rectangle enumeration | (O(n^2m^2)) | (O(nm)) | Too slow |
| Optimal | (O(nm\lceil n/w\rceil + z^2 + E)) | (O(nm + E)) | Accepted |

Here (z\le\min(n,m)), (w) is the machine word size used by the bitset representation, and (E=O(zn+z^2)) is the number of implication edges. For (n,m\le1000), the bitset operations are small enough to fit comfortably within the intended approach.

## Algorithm Walkthrough

1. Read the matrix and record every zero as a Boolean variable. For variable (i), let `A_i` mean that its zero is replaced by (A), and let `B_i` mean that it is replaced by (B). Since each zero must receive exactly one value, `A_i` and `B_i` are complementary literals.
2. Build bitsets for the positions containing (A) and (B). For every row, store the columns containing (A), and separately the columns containing (B). For every column, store the rows containing (A), and separately the rows containing (B).
3. For every row (x), construct `coverA[x]`. Its set bits are exactly the rows (r) for which there exists some column (c) with both (a_{x,c}=A) and (a_{r,c}=A). Construct `coverB` in the same way.

This turns the search for a one-zero rectangle into one bitset intersection instead of scanning every possible pair of a row and a column.
4. For every zero at ((x,y)), check whether `colA[y] & coverA[x]` is nonempty. If it is, there is a row (r) and a column (c) such that the other three corners of the rectangle are all (A). Consequently this zero cannot be assigned (A), so add the implication

[
A_i \rightarrow B_i.
]

Perform the analogous check for (B). If it succeeds, add

[
B_i \rightarrow A_i.
]
5. Consider every pair of distinct zeros (i=(x,y)) and (j=(r,c)). Since every row and column contains at most one zero, their rows and columns are automatically different. The only rectangle containing both zeros has them at opposite corners.

If (a_{x,c}=A) and (a_{r,y}=A), assigning (A) to both zeros would create a new beautiful rectangle. Thus the clause is

[
\neg(A_i\land A_j),
]

which becomes the two implications

[
A_i\rightarrow B_j,
\qquad
A_j\rightarrow B_i.
]

If the two fixed corners are both (B), add the symmetric restrictions

[
B_i\rightarrow A_j,
\qquad
B_j\rightarrow A_i.
]
6. The implication graph now represents every assignment that would create a new beautiful rectangle. Run a strongly connected component algorithm on it. A 2-SAT instance is impossible exactly when a variable and its complement belong to the same strongly connected component.
7. If some zero has `A_i` and `B_i` in the same component, print `No`. Otherwise choose a value according to the component ordering, replace every zero, and print the resulting matrix.

### Why it works

Every rectangle that was beautiful before the replacement contains no zero, so its four corners never change. Thus beauty can decrease only if an old rectangle changes, which cannot happen, and it can increase only when a rectangle containing one or two zeros becomes monochromatic.

A rectangle contains at most two zeros because no row or column contains two zeros. With one zero, the other three corners are fixed, so the only restriction is that the zero cannot take their common value. With two zeros, they are opposite corners and the other two corners are fixed, so the only restriction occurs when those fixed corners agree with (A) or (B), forbidding both zeros from taking that value.

The algorithm creates exactly these restrictions and no others. Every implication in the graph represents a necessary condition for avoiding a new beautiful rectangle, and every possible new beautiful rectangle produces one of these implications. A satisfying assignment of the 2-SAT instance therefore corresponds exactly to a valid replacement of all zeros. The SCC test is the standard satisfiability criterion for 2-SAT.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline
sys.setrecursionlimit(1_000_000)

def solve():
    n, m = map(int, input().split())
    k = int(input())
    A, B = map(int, input().split())

    matrix = []
    row_a = [0] * n
    row_b = [0] * n
    col_a = [0] * m
    col_b = [0] * m
    zeros = []

    for i in range(n):
        row = list(map(int, input().split()))
        matrix.append(array('I', row))

        ma = 0
        mb = 0

        for j, value in enumerate(row):
            if value == 0:
                zeros.append((i, j))
            elif value == A:
                ma |= 1 << j
                col_a[j] |= 1 << i
            elif value == B:
                mb |= 1 << j
                col_b[j] |= 1 << i

        row_a[i] = ma
        row_b[i] = mb

    z = len(zeros)

    if z == 0:
        out = ["Yes"]
        out.extend(" ".join(map(str, row)) for row in matrix)
        sys.stdout.write("\n".join(out))
        return

    # cover_a[x] contains every row r that shares an A-column
    # with row x. cover_b is analogous.
    cover_a = [0] * n
    cover_b = [0] * n

    for i in range(n):
        bits = row_a[i]
        cur = 0
        while bits:
            low = bits & -bits
            c = low.bit_length() - 1
            cur |= col_a[c]
            bits -= low
        cover_a[i] = cur

        bits = row_b[i]
        cur = 0
        while bits:
            low = bits & -bits
            c = low.bit_length() - 1
            cur |= col_b[c]
            bits -= low
        cover_b[i] = cur

    nodes = 2 * z

    # Forward-star representation of the implication graph.
    head = [-1] * nodes
    to = array('i')
    nxt = array('i')

    def add_edge(u, v):
        e = len(to)
        to.append(v)
        nxt.append(head[u])
        head[u] = e

    # Literal encoding:
    # 2*i     = zero i is assigned A
    # 2*i + 1 = zero i is assigned B
    #
    # The complement of a literal is literal ^ 1.

    # Restrictions involving exactly one zero.
    for i, (x, y) in enumerate(zeros):
        a_lit = 2 * i
        b_lit = a_lit + 1

        if col_a[y] & cover_a[x]:
            # A_i is forbidden: A_i -> B_i
            add_edge(a_lit, b_lit)

        if col_b[y] & cover_b[x]:
            # B_i is forbidden: B_i -> A_i
            add_edge(b_lit, a_lit)

    # Restrictions involving two zeros.
    for i in range(z):
        x, y = zeros[i]
        ai = 2 * i
        bi = ai + 1

        for j in range(i + 1, z):
            r, c = zeros[j]
            aj = 2 * j
            bj = aj + 1

            if matrix[x][c] == A and matrix[r][y] == A:
                # Not (A_i and A_j).
                add_edge(ai, bj)
                add_edge(aj, bi)

            if matrix[x][c] == B and matrix[r][y] == B:
                # Not (B_i and B_j).
                add_edge(bi, aj)
                add_edge(bj, ai)

    # Tarjan SCC.
    index = [-1] * nodes
    low = [0] * nodes
    on_stack = [False] * nodes
    stack = []
    component = [-1] * nodes
    timer = 0
    comp_id = 0

    def dfs(v):
        nonlocal timer, comp_id

        index[v] = timer
        low[v] = timer
        timer += 1

        stack.append(v)
        on_stack[v] = True

        e = head[v]
        while e != -1:
            w = to[e]

            if index[w] == -1:
                dfs(w)
                if low[w] < low[v]:
                    low[v] = low[w]
            elif on_stack[w] and index[w] < low[v]:
                low[v] = index[w]

            e = nxt[e]

        if low[v] == index[v]:
            while True:
                w = stack.pop()
                on_stack[w] = False
                component[w] = comp_id
                if w == v:
                    break
            comp_id += 1

    for v in range(nodes):
        if index[v] == -1:
            dfs(v)

    # A variable and its complement in the same SCC means
    # that the 2-SAT instance is unsatisfiable.
    for i in range(z):
        if component[2 * i] == component[2 * i + 1]:
            sys.stdout.write("No\n")
            return

    # Tarjan numbers SCCs in reverse topological order of the
    # condensation graph, so the larger component id is chosen.
    for i, (x, y) in enumerate(zeros):
        if component[2 * i] > component[2 * i + 1]:
            matrix[x][y] = A
        else:
            matrix[x][y] = B

    out = ["Yes"]
    out.extend(" ".join(map(str, row)) for row in matrix)
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input phase stores the matrix in compact integer arrays rather than ordinary nested Python integer lists. This matters because a (1000\times1000) Python list of Python integers has considerably more overhead than the actual (4) MB of 32-bit values needed by the matrix.

`row_a` and `row_b` are integer bitsets whose bit (j) says whether column (j) contains the corresponding value in that row. `col_a` and `col_b` use the same idea in the other direction. Python integers make these bitsets especially convenient because `&`, `|`, and bit shifts operate on many bits at once in native code.

The `cover_a` construction deserves attention. Suppose row (x) contains (A) in columns (c_1,c_2,\ldots). For each such column, `col_a[c]` contains every row having (A) in that column. Taking their union gives every row that shares at least one (A)-column with row (x). Intersecting this with `col_a[y]` then asks whether such a row also has (A) at column (y), exactly matching the three fixed corners required by a rectangle around zero ((x,y)).

The implication graph uses two nodes per zero. Node `2*i` represents choosing (A), and node `2*i+1` represents choosing (B). A forbidden value becomes a one-way implication to the opposite value. A two-zero prohibition becomes the standard pair of implications for a two-literal clause.

The pair loop uses `i + 1` rather than all ordered pairs. The condition is symmetric, so checking both orders would only duplicate the same clauses. The matrix access `matrix[x][c]` and `matrix[r][y]` is safe because the zeros are in different rows and different columns.

Tarjan's algorithm avoids storing a second reverse graph. With up to about (4) million implication edges in the theoretical worst case, this is a useful memory optimization in Python. The recursion depth is bounded by the (2z\le2000) graph vertices, and the recursion limit is raised well above that bound.

The final assignment uses the SCC component ordering. If the two literals of a variable have different components, exactly one can be selected according to the usual 2-SAT topological ordering. No integer overflow is possible because all graph indices and matrix values are at most polynomial in the input dimensions.

## Worked Examples

### Sample 1

The input has three zeros:

[
z_0=(1,3),\qquad z_1=(2,1),\qquad z_2=(4,4),
]

using one-based coordinates. Here (A=3) and (B=5).

| Step | Zero | Single-zero restriction | Pair restriction | Resulting choice |
| --- | --- | --- | --- | --- |
| 1 | (z_0=(1,3)) | None | (z_0,z_2) cannot both be (3) | (5) |
| 2 | (z_1=(2,1)) | None | No restriction with the other zeros | (5) |
| 3 | (z_2=(4,4)) | None | (z_0,z_2) cannot both be (3) | (3) |
| 4 | All variables | SCCs are consistent | No variable conflicts with its complement | `Yes` |

The only relevant new rectangle is formed by the first and fourth zeros together with two fixed (3)'s. Consequently those two zeros cannot both become (3). The assignment (z_0=5,z_1=5,z_2=3) satisfies the restriction and matches the sample's valid construction.

### Sample 2

Here (A=1) and (B=2), with zeros at ((2,2)) and ((3,3)).

| Step | Zero | (A) restriction | (B) restriction | Result |
| --- | --- | --- | --- | --- |
| 1 | ((2,2)) | Forbidden by an all-(1) rectangle | Allowed | Must be (2) |
| 2 | ((3,3)) | Forbidden by the corresponding constraints | Restricted by another rectangle | Forced conflict |
| 3 | Both variables | Implications propagate | (A_i) and (B_i) reach each other | Same SCC |
| 4 | Formula | Variable equals its complement | Unsatisfiable | `No` |

The first zero already receives a restriction from a rectangle whose other three corners are (1). The second zero contributes additional implications, and the resulting implication graph puts both possible literals of a variable into the same strongly connected component. The 2-SAT instance is unsatisfiable, so no replacement can preserve the beauty.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(nm\lceil n/w\rceil + z^2 + E)) | Bitset construction plus all zero pairs and SCC edges |
| Space | (O(nm + E)) | Matrix, bitsets, and implication graph |
| Number of variables | (z\le\min(n,m)) | At most one zero per row and column |
| Number of graph edges | (E=O(zn+z^2)) | One-zero and two-zero restrictions |

For (n,m\le1000), there are at most (1000) Boolean variables. The bitset work operates on at most (1000) bits at a time, while the pair enumeration contains at most about (500,000) zero pairs. The SCC graph has only (2000) vertices. This is fundamentally different from enumerating the roughly (2.5\times10^{11}) possible rectangles in a (1000\times1000) matrix.

The standard C++ formulation describes the bitset part as (O(n^3/w)) for square-sized dimensions, which is the same word-parallel idea used here.

## Test Cases

The following test harness runs the same `solve()` function, validates `Yes` answers by recomputing beauty for small matrices, checks `No` answers directly, and includes a (1000\times1000) boundary case without attempting an (O(n^2m^2)) beauty computation.

```python
import sys
import io
from array import array

# Paste the solve() implementation from the solution above here.

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

def parse_input(inp: str):
    lines = inp.strip().splitlines()
    n, m = map(int, lines[0].split())
    k = int(lines[1])
    A, B = map(int, lines[2].split())
    mat = [list(map(int, lines[3 + i].split())) for i in range(n)]
    return n, m, A, B, mat

def beauty(mat):
    n = len(mat)
    m = len(mat[0])
    ans = 0

    for r1 in range(n):
        for r2 in range(r1 + 1, n):
            for c1 in range(m):
                x = mat[r1][c1]
                for c2 in range(c1 + 1, m):
                    if (
                        x != 0
                        and x == mat[r1][c2]
                        and x == mat[r2][c1]
                        and x == mat[r2][c2]
                    ):
                        ans += 1

    return ans

def validate_yes(inp, out):
    n, m, A, B, original = parse_input(inp)
    lines = out.strip().splitlines()

    assert lines[0] == "Yes"
    assert len(lines) == n + 1

    result = [list(map(int, lines[i + 1].split())) for i in range(n)]

    assert all(len(row) == m for row in result)

    for i in range(n):
        for j in range(m):
            if original[i][j] == 0:
                assert result[i][j] in (A, B)
            else:
                assert result[i][j] == original[i][j]

    assert beauty(original) == beauty(result)

def validate_no(inp, out):
    assert out.strip() == "No"

# Provided sample 1.
sample1 = """\
4 4
5
3 5
1 1 0 3
0 5 4 5
1 1 4 4
2 5 3 0
"""

out = run(sample1)
validate_yes(sample1, out)

# Provided sample 2.
sample2 = """\
4 4
4
1 2
1 1 3 3
1 0 2 3
1 2 0 3
1 3 1 3
"""

out = run(sample2)
validate_no(sample2, out)

# Custom 1: minimum-size matrix, all equal, no zeros.
case1 = """\
2 2
2
1 2
1 1
1 1
"""

out = run(case1)
validate_yes(case1, out)

# Custom 2: two opposite zeros. They cannot both become A,
# but assigning different values is valid.
case2 = """\
2 2
2
1 2
0 1
1 0
"""

out = run(case2)
validate_yes(case2, out)

# Custom 3: one zero is forbidden from both A and B.
case3 = """\
3 3
2
1 2
1 1 1
1 0 2
1 2 2
"""

out = run(case3)
validate_no(case3, out)

# Custom 4: maximum-size boundary case.
# There are no zeros, so the matrix must simply remain unchanged.
n = 1000
row = "7 " * 999 + "7"
case4 = f"{n} {n}\n1000\n1 2\n" + "\n".join([row] * n) + "\n"

out = run(case4)
lines = out.strip().splitlines()

assert lines[0] == "Yes"
assert len(lines) == n + 1
assert lines[1] == row
assert lines[-1] == row
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 x 2`, all entries equal | `Yes` | Minimum dimensions and no-zero case |
| `2 x 2` with opposite zeros | `Yes` | Two-zero clause |
| `3 x 3` with one zero | `No` | A single variable forbidden from both values |
| `1000 x 1000`, no zeros | `Yes` | Maximum matrix dimensions and boundary memory usage |
| Provided sample 1 | `Yes` | Normal satisfiable instance |
| Provided sample 2 | `No` | SCC contradiction |

## Edge Cases

The one-zero case

```
2 2
2
1 2
0 1
1 1
```

has the zero at ((1,1)). Its row contains (1) in column (2), and its column contains (1) in row (2). The remaining corner is also (1), so assigning the zero to (1) would create a new beautiful rectangle. The algorithm detects `col_a[y] & cover_a[x]` as nonempty and adds (A_i\rightarrow B_i). There is no corresponding restriction for (B), so the SCC solver chooses (B=2). The output can be

```
Yes
2 1
1 1
```

The two-zero case

```
2 2
2
1 2
0 1
1 0
```

has zeros at opposite corners. If both became (1), all four corners would be (1), so the algorithm adds

[
A_0\rightarrow B_1
]

and

[
A_1\rightarrow B_0.
]

The assignment (A_0=B), (A_1=A) satisfies both implications, giving

```
Yes
2 1
1 2
```

A zero can also be simultaneously forbidden from both values:

```
3 3
2
1 2
1 1 1
1 0 2
1 2 2
```

For the center zero, the upper-left rectangle has three fixed (1)'s, so the center cannot become (1). The lower-right rectangle has three fixed (2)'s, so it cannot become (2). The graph consequently contains both implications (A_0\rightarrow B_0) and (B_0\rightarrow A_0), placing the two literals in the same SCC. The solver prints `No`.

If there are no zeros, there are no Boolean variables and no implications. Every rectangle keeps exactly the same four corners, so the beauty is unchanged automatically. The algorithm immediately prints `Yes` and the original matrix.

If (A) or (B) does not occur anywhere in the original matrix, the corresponding bitsets simply remain empty. A zero can still be assigned that value, and there cannot be a new rectangle whose fixed corners use that absent value. The bitset intersection naturally produces no restriction for that value.

The one-zero-per-row and one-zero-per-column condition is also essential. It guarantees that a rectangle contains at most two zeros. Without that property, a rectangle could contain three or four zeros and the two kinds of clauses used by this solution would no longer cover every possible new beautiful rectangle.
