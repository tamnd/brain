---
title: "CF 102426A - \u81ea\u7136\u8bed\u8a00\u5904\u7406"
description: "Each text has already been converted into a frequency vector. So the string processing part is completely gone. For one test case, we only need to examine a collection of (n) vectors, each having (m) integer coordinates, and decide whether those vectors are linearly dependent."
date: "2026-08-12T19:20:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102426
codeforces_index: "A"
codeforces_contest_name: "The 7-th BIT Campus Programming Contest for Junior Grade Group"
rating: 0
weight: 102426
solve_time_s: 336
verified: true
draft: false
---

[CF 102426A - \u81ea\u7136\u8bed\u8a00\u5904\u7406](https://codeforces.com/problemset/problem/102426/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

Each text has already been converted into a frequency vector. So the string processing part is completely gone. For one test case, we only need to examine a collection of (n) vectors, each having (m) integer coordinates, and decide whether those vectors are linearly dependent.

The question is equivalent to asking whether there exist coefficients (c_1,c_2,\ldots,c_n), not all zero, such that

[
c_1A_1+c_2A_2+\cdots+c_nA_n=0.
]

If such coefficients exist, the vectors are linearly dependent and the answer is `YES`. Otherwise they are linearly independent and the answer is `NO`.

The dimensions are very small. There are at most 10 vectors, and every vector has at most 4 coordinates. This immediately gives a useful necessary condition: in an (m)-dimensional vector space, no more than (m) vectors can be linearly independent. Thus, whenever (n>m), the answer is automatically `YES`.

Even when (n\le m), we still need to determine whether the vectors actually have full rank. Since (m\le4), Gaussian elimination is more than fast enough. There are at most (10\times4=40) input numbers per case, so even algorithms with considerably worse asymptotic complexity would fit the stated limits. The small bounds are useful for implementation choices, but they do not change the underlying mathematical problem: we need to compute the rank of a matrix.

There are two input-format details worth handling carefully. First, zero vectors immediately make a vector group linearly dependent. For example,

```
1 2
0 0
```

has answer `YES`, because the coefficient of the zero vector can be chosen as 1. A rank implementation that only looks for duplicate rows could incorrectly report independence.

Second, duplicate or proportional vectors also create dependence. For example,

```
2 2
1 2
2 4
```

has answer `YES`, because the second vector is twice the first. Checking whether the rows are merely different is not enough. What matters is whether one row can be expressed as a linear combination of the others.

The supplied statement says that the first input value is (T), while the displayed sample starts directly with `n m`. These two pieces are inconsistent. The solution below accepts the formal multi-test-case format and also recognizes the displayed sample format, so the algorithm itself is unaffected by this formatting discrepancy.

## Approaches

A direct brute-force idea is to enumerate every nonempty subset of the vectors and test whether that subset is linearly dependent. If any subset is dependent, the entire vector group is dependent. For every subset, we can run Gaussian elimination on its rows.

This approach is correct because a vector family is linearly dependent exactly when it contains a nonempty linearly dependent subfamily. Its worst-case complexity is (O(2^n m^3)), since there are (2^n-1) nonempty subsets and a rank computation costs (O(m^3)). With the actual maximum (n=10) and (m=4), this is at most roughly (1024\cdot64=65536) elementary elimination-scale operations per test case, so even this brute-force approach would pass comfortably.

The problem with that approach is not the given limits, but the unnecessary exponential dependence on (n). If the same task allowed thousands or hundreds of thousands of vectors, enumerating subsets would immediately become impossible. The structure of linear dependence gives us a much cleaner route: all vectors can be placed into one matrix, and the number of independent vectors is exactly the matrix rank.

The key observation is that Gaussian elimination computes this rank directly. Each successful pivot identifies one independent direction. If we find exactly (n) pivots, every one of the (n) vectors contributes a new independent direction, so the vectors are independent. If fewer than (n) pivots exist, some vector is a combination of the previous independent directions, so the family is dependent.

Since (m) is the number of columns, the rank can never exceed (m). This also explains the immediate (n>m) case: there cannot possibly be (n) pivots in only (m) columns.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^n m^3)) | (O(nm)) | Accepted here, but unnecessarily exponential |
| Optimal | (O(nm^2)) | (O(nm)) | Accepted |

## Algorithm Walkthrough

1. Read (n), (m), and the (n) vectors, treating the vectors as the rows of an (n\times m) matrix. This turns the original question directly into a matrix-rank problem.
2. If (n>m), immediately output `YES`. An (m)-dimensional vector space cannot contain more than (m) linearly independent vectors, so dependence is guaranteed.
3. Maintain a current pivot row. Initially it is row 0. For each column, search the remaining rows for one whose value in this column is nonzero. If no such row exists, this column cannot provide another independent direction, so move to the next column.
4. When a nonzero pivot is found, swap that row into the current pivot position. We can divide the pivot row by its pivot value, making the pivot equal to 1. Exact rational arithmetic is used here so that the result does not depend on floating-point precision.
5. Eliminate the current pivot column from every other row. After elimination, every previously processed pivot column has zeros outside its pivot row. This gives a row-echelon-style representation in which every successful pivot corresponds to one independent dimension.
6. Increase the rank and move the pivot row to the next position. Once all columns have been processed, the number of successful pivots is the matrix rank.
7. Compare the rank with (n). If `rank == n`, all (n) vectors are linearly independent, so output `NO`. Otherwise, the rank is smaller than the number of vectors, so output `YES`.

### Why it works

The central invariant is that after each successful pivot, the processed pivot rows represent mutually independent directions, and every processed column has been eliminated from the other rows. A new pivot can exist only if there is still a row containing information that cannot be produced by the previous pivot rows.

Consequently, every pivot increases the rank by exactly one. Gaussian elimination finishes with exactly as many pivots as the dimension of the span of the input vectors. A vector family of size (n) is linearly independent exactly when its span has dimension (n), so `rank == n` is precisely the condition for the required `NO` answer.

## Python Solution

```python
import sys
from fractions import Fraction

input = sys.stdin.readline

def independent(vectors, m):
    n = len(vectors)

    if n > m:
        return False

    a = [[Fraction(x) for x in row] for row in vectors]

    rank = 0

    for col in range(m):
        pivot = -1

        for row in range(rank, n):
            if a[row][col] != 0:
                pivot = row
                break

        if pivot == -1:
            continue

        a[rank], a[pivot] = a[pivot], a[rank]

        pivot_value = a[rank][col]
        for j in range(col, m):
            a[rank][j] /= pivot_value

        for row in range(n):
            if row == rank:
                continue

            factor = a[row][col]
            if factor == 0:
                continue

            for j in range(col, m):
                a[row][j] -= factor * a[rank][j]

        rank += 1

        if rank == n:
            return True

    return False

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    # The formal statement uses T test cases.
    # The displayed sample omits T and starts directly with n m.
    # Detect both formats from the first input line.
    lines = sys.stdin.buffer.read().splitlines()

    # Re-read using the raw data above if possible.
    # For the formal format, the first line contains only T.
    first_line = lines[0].split()

    if len(first_line) == 1:
        t = int(first_line[0])
        pos = 1

        answers = []

        for _ in range(t):
            n = int(data[pos])
            m = int(data[pos + 1])
            pos += 2

            vectors = []
            for _ in range(n):
                vectors.append(list(map(int, data[pos:pos + m])))
                pos += m

            answers.append("NO" if independent(vectors, m) else "YES")

        sys.stdout.write("\n".join(answers))
    else:
        # Format used by the displayed sample: n m followed by n vectors.
        pos = 0
        n = int(data[pos])
        m = int(data[pos + 1])
        pos += 2

        vectors = []
        for _ in range(n):
            vectors.append(list(map(int, data[pos:pos + m])))
            pos += m

        sys.stdout.write("NO\n" if independent(vectors, m) else "YES\n")

if __name__ == "__main__":
    solve()
```

The `independent` function first handles the dimension argument. When (n>m), it returns `False` because the vectors cannot be independent. This is the same mathematical shortcut used in the walkthrough.

The matrix is converted to `Fraction` values before elimination. Although the input consists only of integers, division during Gaussian elimination can create rational values. Using floating-point numbers would normally work for these tiny bounds, but exact arithmetic makes the dependence test mathematically robust and avoids choosing an arbitrary epsilon for deciding whether a value is zero.

The outer loop processes each column as a possible pivot position. The search begins at `rank`, because rows above that position already contain established pivots. Once a nonzero value is found, the corresponding row is swapped into place.

The pivot row is normalized to make the pivot equal to 1. The implementation then eliminates the pivot column from every other row. Eliminating both above and below the pivot is slightly more work than the minimum needed for ordinary row-echelon form, but it keeps the matrix in reduced form and makes the rank invariant especially straightforward.

The early `rank == n` return is safe because rank can only increase. Once there are already (n) pivots, all (n) vectors are independent and no later column can change that conclusion.

The parser contains a small compatibility layer because the supplied statement and displayed sample disagree about whether (T) is present. If the first line contains one integer, it is treated as (T). If it contains two integers, they are treated as (n,m), matching the displayed sample. The actual linear algebra is identical in either format.

## Worked Examples

### Sample 1

The displayed sample contains two vectors:

```
2 2
1 1
0 1
```

The matrix is

[
\begin{pmatrix}
1&1\
0&1
\end{pmatrix}.
]

The elimination proceeds as follows.

| Column | Pivot row | Matrix state | Rank |
| --- | --- | --- | --- |
| 0 | 0 | (\begin{pmatrix}1&1\0&1\end{pmatrix}) | 1 |
| 1 | 1 | (\begin{pmatrix}1&0\0&1\end{pmatrix}) | 2 |

The final rank is 2, which equals the number of vectors. Thus the vectors are linearly independent and the answer is `NO`.

This example demonstrates the basic invariant: every successful pivot contributes one independent direction. The second vector is not a multiple of the first, so a second pivot exists.

### Sample 2

Consider two proportional vectors:

```
1
2 2
1 2
2 4
```

The matrix is

[
\begin{pmatrix}
1&2\
2&4
\end{pmatrix}.
]

| Column | Pivot row | Matrix state | Rank |
| --- | --- | --- | --- |
| 0 | 0 | (\begin{pmatrix}1&2\2&4\end{pmatrix}) | 1 |
| 1 | none | (\begin{pmatrix}1&2\0&0\end{pmatrix}) | 1 |

Only one pivot is found. The second row becomes zero because it is twice the first row. The rank is therefore 1, smaller than (n=2), so the answer is `YES`.

This trace exercises the case where the vectors are distinct but still linearly dependent. Merely checking whether two rows are equal would miss this example, while rank detects it immediately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(nm^2)) | At most (m) pivot columns are processed, and eliminating a pivot touches (O(nm)) matrix entries |
| Space | (O(nm)) | The matrix stores all (n) vectors |

With (n\le10) and (m\le4), the matrix contains at most 40 entries. Even exact `Fraction` arithmetic is easily fast enough for these limits, and the memory usage is negligible compared with the 64 MB limit.

The asymptotic bound is also appropriate beyond these tiny constraints. The solution avoids enumerating subsets and computes the entire rank in one elimination pass.

## Test Cases

```python
import sys
import io
from fractions import Fraction

def independent(vectors, m):
    n = len(vectors)

    if n > m:
        return False

    a = [[Fraction(x) for x in row] for row in vectors]
    rank = 0

    for col in range(m):
        pivot = -1

        for row in range(rank, n):
            if a[row][col] != 0:
                pivot = row
                break

        if pivot == -1:
            continue

        a[rank], a[pivot] = a[pivot], a[rank]

        p = a[rank][col]
        for j in range(col, m):
            a[rank][j] /= p

        for row in range(n):
            if row == rank:
                continue

            factor = a[row][col]
            if factor == 0:
                continue

            for j in range(col, m):
                a[row][j] -= factor * a[rank][j]

        rank += 1

        if rank == n:
            return True

    return False

def run(inp: str) -> str:
    lines = inp.strip().splitlines()
    data = inp.split()

    if not data:
        return ""

    first_line = lines[0].split()

    if len(first_line) == 1:
        t = int(first_line[0])
        pos = 1
        out = []

        for _ in range(t):
            n = int(data[pos])
            m = int(data[pos + 1])
            pos += 2

            vectors = []
            for _ in range(n):
                vectors.append(list(map(int, data[pos:pos + m])))
                pos += m

            out.append("NO" if independent(vectors, m) else "YES")

        return "\n".join(out) + "\n"

    n = int(data[0])
    m = int(data[1])
    pos = 2

    vectors = []
    for _ in range(n):
        vectors.append(list(map(int, data[pos:pos + m])))
        pos += m

    return ("NO\n" if independent(vectors, m) else "YES\n")

# Provided sample, whose displayed format omits T.
assert run("""\
2 2
1 1
0 1
""") == "NO\n", "sample 1"

# Minimum-size case: one nonzero vector is independent.
assert run("""\
1
1 1
7
""") == "NO\n", "minimum nonzero vector"

# Zero vector is always dependent.
assert run("""\
1
1 3
0 0 0
""") == "YES\n", "zero vector"

# Two proportional vectors are dependent.
assert run("""\
1
2 2
1 2
2 4
""") == "YES\n", "proportional vectors"

# Maximum dimensions, with four independent vectors.
assert run("""\
1
4 4
1 0 0 0
0 1 0 0
0 0 1 0
0 0 0 100
""") == "NO\n", "maximum-size independent case"

# More vectors than dimensions must be dependent.
assert run("""\
1
5 4
1 0 0 0
0 1 0 0
0 0 1 0
0 0 0 1
1 1 1 1
""") == "YES\n", "n greater than m"

# Several test cases in the formal format.
assert run("""\
3
2 2
1 1
0 1
2 2
1 2
2 4
3 2
1 0
0 1
1 1
""") == "NO\nYES\nYES\n", "multiple test cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1 / 7` | `NO` | Minimum-size case with one nonzero vector |
| `1 / 1 3 / 0 0 0` | `YES` | Zero vector |
| `1 / 2 2 / 1 2 / 2 4` | `YES` | Proportional vectors |
| `1 / 4 4 / ...` | `NO` | Maximum dimension with four independent vectors |
| `1 / 5 4 / ...` | `YES` | Boundary condition (n>m) |
| Three formal test cases | `NO YES YES` | Multiple test-case parsing and mixed dependence results |

## Edge Cases

The first edge case is a zero vector. Consider

```
1
1 3
0 0 0
```

The algorithm starts with rank 0. In column 0 there is no nonzero entry, and the same happens in columns 1 and 2. No pivot is found, so the final rank remains 0. Since (0<1), the vectors are dependent and the output is `YES`. This works without any special zero-vector check because Gaussian elimination naturally treats a zero row as contributing no rank.

The second edge case is a pair of different but proportional vectors:

```
1
2 2
1 2
2 4
```

The first row supplies a pivot in column 0, increasing the rank to 1. Eliminating column 0 from the second row changes it from `(2, 4)` to `(0, 0)`. The second column has no remaining nonzero candidate, so the rank stays 1. Since there are two vectors but only one independent direction, the answer is `YES`.

The third edge case occurs when there are more vectors than coordinates:

```
1
5 4
1 0 0 0
0 1 0 0
0 0 1 0
0 0 0 1
1 1 1 1
```

The algorithm returns `YES` immediately because (5>4). No elimination is necessary. There are only four coordinate directions available, so five vectors cannot be independent.

The fourth edge case is a full-rank square matrix:

```
1
4 4
1 0 0 0
0 1 0 0
0 0 1 0
0 0 0 100
```

The algorithm finds one pivot in every column. The rank reaches 4, which equals the number of vectors, so it returns `NO`. The value 100 causes no special handling because the elimination uses exact rational arithmetic.

These cases cover the main ways a superficial solution can fail: confusing distinct vectors with independent vectors, overlooking the zero vector, forgetting the (n>m) dimension bound, or using approximate arithmetic without considering exact zero detection.
