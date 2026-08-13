---
title: "CF 102309J - Jobless Orz Panda"
description: "We are given an (ntimes n) integer matrix (A) and positive integers (b1,ldots,bn). For a vector (x), define (y=Ax). The integral asks for the (n)-dimensional volume of all vectors (x) whose image (y) lies inside the axis-aligned box [ 0le yile bi."
date: "2026-08-13T07:06:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102309
codeforces_index: "J"
codeforces_contest_name: "The 2019 \u201cOrz Panda\u201d Cup Programming Contest"
rating: 0
weight: 102309
solve_time_s: 377
verified: true
draft: false
---

[CF 102309J - Jobless Orz Panda](https://codeforces.com/problemset/problem/102309/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an (n\times n) integer matrix (A) and positive integers (b_1,\ldots,b_n). For a vector (x), define (y=Ax). The integral asks for the (n)-dimensional volume of all vectors (x) whose image (y) lies inside the axis-aligned box

[
0\le y_i\le b_i.
]

The required answer is the square of that volume.

The key geometric question is therefore not really about integration. The set of valid (y) is simply a rectangular box, while (x) is obtained from (y) through the linear transformation (A). If (A) is invertible, the box is transformed back into a parallelotope, whose volume is determined by the determinant of (A). If (A) is singular, some direction in (x)-space is completely invisible to (Ax), so the feasible set extends infinitely far in that direction.

When (A) is invertible,

# \frac{\operatorname{Vol}(y)}{|\det A|}

\frac{\prod_i b_i}{|\det A|}.
]

Consequently, the requested value is

[
\boxed{
\frac{\left(\prod_i b_i\right)^2}{(\det A)^2}
}.
]

The constraints have (n\le300), so an (O(n^3)) algorithm is appropriate. A cubic algorithm performs about (300^3=27) million basic matrix operations, while anything exponential or factorial is completely infeasible. The matrix entries and the (b_i) values are as large as (10^9), so computing the determinant as an ordinary machine integer is also unsafe. Python's arbitrary-precision integers avoid overflow, but modular Gaussian elimination is cleaner because the requested result is itself modulo a prime.

There are two separate failure cases that a careless implementation must distinguish. First, a singular matrix makes the integral infinite. For example,

```
2
1 1
1 1
2 2
```

has determinant zero, and the correct output is `Orz`. The feasible (x)-set contains an unrestricted direction, so treating the determinant as merely a denominator would incorrectly suggest division by zero.

Second, a nonzero integer determinant can itself be divisible by (M=10^9+7). For example,

```
2
1 2
-500000003 1
1 1
```

has determinant

[
1+2\cdot500000003=1000000007=M.
]

The integral is finite, but its reduced denominator still contains (M), because every (b_i\le10^9<M), so (\prod b_i) cannot contain the prime factor (M). The required modular inverse does not exist, so the correct answer is again `Orz`. A solution that only checks whether the determinant is nonzero over the integers but then blindly calls a modular inverse would produce an invalid result.

The sample with

```
2
1 1
1 -1
4 5
```

has determinant (-2). The transformed box has volume (4\cdot5=20), so the feasible (x)-region has volume (20/2=10), and the requested square is (100).

## Approaches

A direct brute-force way to think about the determinant is its Leibniz formula,

[
\det A=\sum_{\pi} \operatorname{sgn}(\pi)
\prod_i A_{i,\pi(i)}.
]

It examines one term for every permutation of (n) columns. That means (n!) products, and roughly (n\cdot n!) scalar operations if the products are formed independently. At (n=300), even (300!) is astronomically larger than anything that can be processed in four seconds. Direct numerical integration is even less useful, since the integration region is an arbitrary high-dimensional polytope in the original coordinates.

The geometric observation removes the integration completely. The constraints are already a box in (y=Ax) coordinates. For an invertible linear map, volume changes by exactly the factor (|\det A|). Thus the entire integral can be expressed using one determinant and the product of the (b_i).

The remaining challenge is computing that determinant efficiently and in a form compatible with modular division. Gaussian elimination computes a determinant in (O(n^3)). Since the modulus (M=1000000007) is prime, every nonzero matrix entry modulo (M) has a modular inverse. We can consequently perform elimination entirely modulo (M).

There is one subtle point about the meaning of a zero determinant modulo (M). A zero determinant over the integers certainly means the matrix is singular, but the converse modulo (M) is slightly different: an integer determinant can be nonzero while divisible by (M). That case still has to produce `Orz`, because the rational answer has a denominator containing (M). Since all (b_i<M), the numerator ((\prod b_i)^2) is not divisible by (M), so no factor (M) can disappear during fraction reduction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force determinant expansion | (O(n\cdot n!)) | (O(n)) | Too slow |
| Optimal modular Gaussian elimination | (O(n^3)) | (O(n^2)) | Accepted |

## Algorithm Walkthrough

1. Read (A) and (b), and reduce every matrix entry modulo (M=1000000007). Negative entries are converted to their equivalent nonnegative residues.
2. Compute (\det A\bmod M) using Gaussian elimination. At column (i), search rows (i,\ldots,n-1) for a nonzero pivot. If none exists, the determinant is zero modulo (M), so output `Orz`.

If the determinant is zero modulo (M), either (A) is genuinely singular or its nonzero integer determinant is divisible by (M). Both cases lead to `Orz`, for different mathematical reasons.
3. When a pivot is found below the current row, swap the two rows. A row swap changes the determinant's sign, so multiply the accumulated determinant by (-1).
4. Multiply the determinant accumulator by the pivot value. Then eliminate the entries below that pivot. If the pivot is (p) and the entry being eliminated is (v), use

[
f=v p^{-1}\pmod M
]

and replace the row by

[
R_j\leftarrow R_j-fR_i.
]

Only columns to the right of the pivot need to be updated because the current column becomes zero.

1. After all columns have been processed, the determinant accumulator is (\det A\bmod M). If it is zero, output `Orz`. Otherwise, compute

[
B=\prod_i b_i\pmod M.
]

1. The required value is

[
\frac{B^2}{(\det A)^2}.
]

Since the determinant is nonzero modulo (M), its modular inverse exists. Compute

[
B^2\cdot(\det A)^{-2}\pmod M.
]

Python's `pow(x, M-2, M)` gives the modular inverse because (M) is prime.

### Why it works

Let (S={x:0\le (Ax)_i\le b_i\text{ for every }i}). If (A) is invertible, the map (x\mapsto Ax) bijectively maps (S) to the box (B=[0,b_1]\times\cdots\times[0,b_n]). Linear changes of variables scale volume by (|\det A|), so

# \frac{\operatorname{Vol}(B)}{|\det A|}

\frac{\prod_i b_i}{|\det A|}.
]

Squaring removes the sign of the determinant and gives the formula used by the algorithm.

If (A) is singular, there exists a nonzero vector (v) with (Av=0). Starting from any feasible point, moving along (v) leaves (Ax) unchanged, so the feasible region contains an unbounded line and has infinite volume. Thus singular matrices must produce `Orz`.

Finally, suppose (\det A\ne0) as an integer but (\det A\equiv0\pmod M). Since (M) is prime and every (b_i<M), the numerator ((\prod b_i)^2) is not divisible by (M). Hence the reduced denominator still contains (M), so its modular inverse does not exist. The same `Orz` decision is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

def determinant_mod(a):
    n = len(a)
    det = 1

    for col in range(n):
        pivot = col
        while pivot < n and a[pivot][col] == 0:
            pivot += 1

        if pivot == n:
            return 0

        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            det = (-det) % MOD

        p = a[col][col]
        det = det * p % MOD

        inv_p = pow(p, MOD - 2, MOD)

        pivot_row = a[col]

        for row in range(col + 1, n):
            value = a[row][col]
            if value == 0:
                continue

            factor = value * inv_p % MOD
            current = a[row]

            for j in range(col + 1, n):
                current[j] = (current[j] - factor * pivot_row[j]) % MOD

            current[col] = 0

    return det

def solve():
    out = []

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        n = int(line)

        a = []
        for _ in range(n):
            row = list(map(int, input().split()))
            a.append([x % MOD for x in row])

        b = list(map(int, input().split()))

        det = determinant_mod(a)

        if det == 0:
            out.append("Orz")
            continue

        product_b = 1
        for x in b:
            product_b = product_b * (x % MOD) % MOD

        inv_det = pow(det, MOD - 2, MOD)
        ans = product_b * product_b % MOD
        ans = ans * inv_det % MOD
        ans = ans * inv_det % MOD

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The determinant routine modifies the matrix in place, which avoids allocating another (n\times n) matrix. Every entry is kept modulo (M), so all arithmetic remains bounded by roughly (M^2) before the modulo operation.

The pivot search is necessary because Gaussian elimination cannot divide by a zero pivot. A row swap changes the determinant sign, which is why `det` is negated when a different pivot row is selected.

The elimination factor is computed as `value * inv_p % MOD`. The current pivot column is then explicitly set to zero. The inner loop starts at `col + 1`, rather than at `col`, because the value at the current column is already known to become zero. This saves work and avoids accidentally modifying the pivot column before it is used by later rows.

The determinant is multiplied by each pivot before elimination. Gaussian elimination preserves the determinant up to row swaps, because subtracting a multiple of one row from another does not change the determinant. Thus the product of the pivots, together with the signs from row swaps, is exactly the determinant modulo (M).

Python does not have fixed-width integer overflow, but the implementation still performs all operations modulo (M) because the mathematical output is modulo (M) and modular Gaussian elimination avoids enormous determinant values.

The two calls to `inv_det` in the final expression correspond to the squared determinant in the denominator. There is no need to calculate an absolute determinant because the square makes its sign irrelevant.

## Worked Examples

### Sample 1

The first sample case is

```
2
1 1
1 -1
4 5
```

The matrix determinant is

[
1\cdot(-1)-1\cdot1=-2.
]

Modulo (M), this is (M-2=1000000005).

| Step | Pivot | Pivot value | Determinant modulo (M) |
| --- | --- | --- | --- |
| Start | none | none | 1 |
| Column 0 | 0 | 1 | 1 |
| Column 1 | 1 | (-2) | (1000000005) |

The product of the box side lengths is (4\cdot5=20). Hence

# \frac{400}{4}

1. 

]

The output is `100`.

This trace demonstrates the ordinary invertible case. The determinant is nonzero, so the feasible region has finite volume, and the modular inverse of the determinant exists.

### Sample 2

The second sample case is

```
2
1 1
1 1
2 2
```

Both rows are identical, so the determinant is zero.

| Step | Pivot column | Pivot found? | Determinant status |
| --- | --- | --- | --- |
| Start | 0 | Yes, value 1 | Nonzero |
| Eliminate row 1 | 0 | Row becomes `0 0` | Still tracking elimination |
| Column 1 | 1 | No | Zero |

At column 1 there is no nonzero pivot. The determinant is zero modulo (M), and in this case it is also zero as an integer. The matrix has a null direction, so the feasible set is unbounded and the integral is infinite.

The output is `Orz`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^3)) | Gaussian elimination updates (O(n^2)) entries for each of (n) pivots |
| Space | (O(n^2)) | The matrix itself occupies (n^2) entries |

For (n=300), the cubic work is about 27 million matrix-entry updates. The matrix requires only (300^2=90000) stored integers, comfortably within 256 MB. No operation depends exponentially on (n), so the algorithm fits the intended scale of the problem.

## Test Cases

```python
import sys
import io

MOD = 1000000007

def determinant_mod(a):
    n = len(a)
    det = 1

    for col in range(n):
        pivot = col
        while pivot < n and a[pivot][col] == 0:
            pivot += 1

        if pivot == n:
            return 0

        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            det = (-det) % MOD

        p = a[col][col]
        det = det * p % MOD
        inv_p = pow(p, MOD - 2, MOD)

        pivot_row = a[col]

        for row in range(col + 1, n):
            value = a[row][col]
            if value == 0:
                continue

            factor = value * inv_p % MOD
            current = a[row]

            for j in range(col + 1, n):
                current[j] = (
                    current[j] - factor * pivot_row[j]
                ) % MOD

            current[col] = 0

    return det

def solve_string(inp: str) -> str:
    data = inp.split()
    pos = 0
    ans = []

    while pos < len(data):
        n = int(data[pos])
        pos += 1

        a = []
        for _ in range(n):
            row = [int(data[pos + j]) % MOD for j in range(n)]
            pos += n
            a.append(row)

        b = [int(data[pos + i]) for i in range(n)]
        pos += n

        det = determinant_mod(a)

        if det == 0:
            ans.append("Orz")
            continue

        prod = 1
        for x in b:
            prod = prod * x % MOD

        inv_det = pow(det, MOD - 2, MOD)
        value = prod * prod % MOD
        value = value * inv_det % MOD
        value = value * inv_det % MOD

        ans.append(str(value))

    return "\n".join(ans)

def run(inp: str) -> str:
    return solve_string(inp)

sample = """\
2
1 1
1 -1
4 5
2
1 1
1 1
2 2
"""
assert run(sample) == "100\nOrz", "provided samples"

assert run("""\
1
1
1
""") == "1", "minimum size"

assert run("""\
2
2 0
0 2
3 3
""") == "81", "diagonal matrix and equal b"

assert run("""\
2
1 1
1 1
7 7
""") == "Orz", "singular all-equal rows"

assert run("""\
2
1 2
-500000003 1
1 1
""") == "Orz", "determinant divisible by MOD"

# Maximum-size structural case: identity matrix of size 300.
n = 300
lines = [str(n)]
for i in range(n):
    row = ["0"] * n
    row[i] = "1"
    lines.append(" ".join(row))
lines.append(" ".join(["1"] * n))
assert run("\n".join(lines)) == "1", "maximum-size identity matrix"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 1` | `1` | Minimum matrix size and the simplest finite integral |
| `[[2,0],[0,2]]`, `b=[3,3]` | `81` | Determinant scaling and equal side lengths |
| `[[1,1],[1,1]]`, `b=[7,7]` | `Orz` | Singular matrix detection |
| `[[1,2],[-500000003,1]]`, `b=[1,1]` | `Orz` | Nonzero integer determinant divisible by (M) |
| (300\times300) identity, all (b_i=1) | `1` | Maximum matrix size and cubic implementation |

## Edge Cases

A singular matrix must be rejected even though the original inequalities themselves may look bounded in every (y_i). For

```
2
1 1
1 1
7 7
```

the vector ((1,-1)^T) belongs to the nullspace of (A). If (x) satisfies the constraints, then (x+t(1,-1)) satisfies exactly the same constraints for every real (t). The feasible region is consequently unbounded. Gaussian elimination turns the second row into zero and finds no pivot in the final column, so the algorithm outputs `Orz`.

A determinant that vanishes modulo (M) also has to be rejected. Consider

```
2
1 2
-500000003 1
1 1
```

The determinant is

[
1\cdot1-2(-500000003)=1000000007=M.
]

The matrix is invertible over the real numbers, so the integral itself is finite. Its value is

[
\frac{1}{M^2}.
]

Because (M) is prime and the numerator is (1), the reduced denominator has no modular inverse modulo (M). The determinant routine obtains zero modulo (M), so the program correctly prints `Orz`.

The smallest case is

```
1
1
1
```

Here (Ax=x), so the allowed interval for (x) is ([0,1]), whose volume is (1). Squaring gives (1). The determinant algorithm has a single pivot equal to (1), and the final formula gives (1^2/1^2=1).

A row swap must also be handled correctly. For example,

```
2
0 1
1 0
2 3
```

has determinant (-1). The first column has no pivot in the first row, so the algorithm swaps the rows and records the sign change. The box volume is (6), hence the required answer is (6^2=36). Forgetting the determinant sign would not hurt this particular final answer because the determinant is squared, but handling row swaps is still necessary for the determinant computation itself and for maintaining a correct general invariant.

Finally, the case where every (b_i) is equal is not mathematically special. For

```
2
2 0
0 2
3 3
```

the transformed box has volume (9), while the determinant has absolute value (4). The feasible region therefore has volume (9/4), and the requested answer is (81/16). Modulo (M), the program computes (81\cdot16^{-1}). This exercises the actual rational-output requirement rather than only cases where the denominator divides the numerator.
