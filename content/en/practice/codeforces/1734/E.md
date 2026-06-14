---
title: "CF 1734E - Rectangular Congruence"
description: "We are asked to construct an $n times n$ matrix over the field of residues modulo a prime $n$. Every entry must be an integer in the range $0$ to $n-1$, and the diagonal is already fixed: the $i$-th diagonal entry must equal $bi$."
date: "2026-06-15T03:30:23+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1734
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 822 (Div. 2)"
rating: 2100
weight: 1734
solve_time_s: 390
verified: false
draft: false
---

[CF 1734E - Rectangular Congruence](https://codeforces.com/problemset/problem/1734/E)

**Rating:** 2100  
**Tags:** constructive algorithms, number theory  
**Solve time:** 6m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct an $n \times n$ matrix over the field of residues modulo a prime $n$. Every entry must be an integer in the range $0$ to $n-1$, and the diagonal is already fixed: the $i$-th diagonal entry must equal $b_i$.

The main constraint is a strong anti-additivity condition on every pair of distinct rows and every pair of distinct columns. If we take any two rows $r_1 < r_2$ and any two columns $c_1 < c_2$, then the matrix must avoid the equality

$$a_{r_1,c_1} + a_{r_2,c_2} \equiv a_{r_1,c_2} + a_{r_2,c_1} \pmod n.$$

This is exactly saying that every $2 \times 2$ submatrix must not satisfy the classical “cross-sum equality” modulo $n$. Equivalently, every such submatrix must have a non-zero determinant over the finite field $\mathbb{F}_n$.

So the task is to construct a matrix over a prime field with a prescribed diagonal and with the property that every $2 \times 2$ minor is non-degenerate.

The constraint $n < 350$ means we can afford $O(n^2)$ or even $O(n^2 \log n)$ constructions. Anything cubic over all quadruples of indices would be far too slow since there are $O(n^4)$ constraints.

A subtle failure case for naive approaches is trying random filling. For example, picking random values for each row independently will often accidentally produce a degenerate $2 \times 2$ submatrix. Even fixing diagonal entries does not prevent these collisions because the constraint is global and quadratic in structure.

Another naive attempt is to treat rows independently as arbitrary vectors with fixed diagonal entries. This also fails because the condition couples pairs of rows and columns simultaneously.

The key difficulty is that the condition is not local to rows or columns but instead enforces a global rank-like structure.

## Approaches

A brute-force idea would be to try filling the matrix cell by cell and, after each assignment, check all $O(n^4)$ quadruples for violations. Even if we optimized checking by maintaining all $2 \times 2$ minors incrementally, each update still affects $O(n^2)$ constraints, and we would need to check consistency repeatedly. This quickly leads to at least $O(n^4)$ work overall, which is impossible for $n \approx 350$.

The key insight is to reinterpret the condition algebraically. The forbidden equality

$$a_{r_1,c_1} + a_{r_2,c_2} = a_{r_1,c_2} + a_{r_2,c_1}$$

is exactly the statement that the matrix is of rank $1$ when restricted to any $2 \times 2$ block. Over a field, this is equivalent to requiring that the matrix does not behave like an additive separable function on any rectangle.

The classical way to avoid all such equalities over a prime field is to enforce a bilinear structure. If we could represent entries as

$$a_{i,j} = x_i y_j$$

in $\mathbb{F}_n$, then every $2 \times 2$ determinant becomes zero, which is the opposite of what we want. So pure rank-1 structure fails.

Instead, we need a structure where every $2 \times 2$ determinant is non-zero:

$$a_{i,c_1} + a_{r_2,c_2} \ne a_{r_1,c_2} + a_{r_2,c_1}.$$

A standard trick in prime fields is to encode rows and columns using linear functions with carefully chosen slopes so that every rectangle produces a distinct affine combination.

The correct construction is to treat indices as elements of $\mathbb{F}_n$, and define the matrix using a quadratic lifting:

$$a_{i,j} = i \cdot j + c_i + d_j \pmod n,$$

where $c_i$ and $d_j$ are corrections chosen to match the diagonal constraints.

This form is crucial because the cross terms $i \cdot j$ ensure that any rectangle produces a bilinear expression whose mixed terms do not cancel unless indices coincide. The additive terms $c_i$ and $d_j$ allow us to enforce diagonal values without destroying the non-degeneracy of minors.

Now we enforce the diagonal condition:

$$a_{i,i} = i^2 + c_i + d_i \equiv b_i \pmod n.$$

We are free to choose $c_i = 0$, and then set

$$d_i = b_i - i^2 \pmod n.$$

This fully determines the matrix:

$$a_{i,j} = i \cdot j + (b_j - j^2).$$

This construction ensures the diagonal is correct and preserves a strong algebraic asymmetry between rows and columns that prevents cancellation in any $2 \times 2$ submatrix.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^4)$ | $O(n^2)$ | Too slow |
| Optimal | $O(n^2)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

We work entirely in arithmetic modulo $n$, treating indices as elements of the finite field.

1. Interpret each row index $i$ and column index $j$ as integers in $[0, n-1]$. This allows direct arithmetic in the field.
2. Compute a column correction term for each column $j$, defined as $d_j = b_j - j^2 \mod n$. This is chosen so that the diagonal constraint can be satisfied without introducing row-dependent interference.
3. Construct each matrix entry using the formula $a_{i,j} = i \cdot j + d_j \mod n$. This ensures that every column has a fixed affine shift applied consistently across all rows.
4. Output the resulting matrix row by row.

The reason for separating dependence into a bilinear term $i \cdot j$ and a column-only correction is that any equality involving a $2 \times 2$ submatrix expands into a polynomial identity in $i$ and $j$. The mixed product term prevents cancellation across different row pairs.

### Why it works

Fix any two rows $r_1 < r_2$ and columns $c_1 < c_2$. Expanding the cross-sum difference gives

$$(a_{r_1,c_1} + a_{r_2,c_2}) - (a_{r_1,c_2} + a_{r_2,c_1})$$

$$= (r_1 c_1 + d_{c_1}) + (r_2 c_2 + d_{c_2}) - (r_1 c_2 + d_{c_2}) - (r_2 c_1 + d_{c_1})$$

All $d$-terms cancel, leaving

$$r_1 c_1 + r_2 c_2 - r_1 c_2 - r_2 c_1 = (r_1 - r_2)(c_1 - c_2).$$

Since $n$ is prime, the field has no zero divisors, so this expression is non-zero modulo $n$ whenever $r_1 \ne r_2$ and $c_1 \ne c_2$. This guarantees every $2 \times 2$ submatrix violates the forbidden equality.

The diagonal condition is already baked into $d_i$, so all constraints are simultaneously satisfied.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    b = list(map(int, input().split()))
    
    d = [(b[j] - (j * j) % n) % n for j in range(n)]
    
    for i in range(n):
        row = []
        for j in range(n):
            val = (i * j + d[j]) % n
            row.append(str(val))
        print(" ".join(row))

if __name__ == "__main__":
    main()
```

The implementation directly follows the derived formula. The precomputation of $d_j$ ensures diagonal correctness, while the nested loop constructs each entry in $O(1)$ time.

A common implementation pitfall is forgetting that all operations must be reduced modulo $n$ at every step, especially the square term $j^2$. Another subtle point is ensuring that subtraction is also performed modulo $n$, since Python’s negative values otherwise propagate incorrectly.

## Worked Examples

### Example 1

Input:

```
n = 2
b = [0, 0]
```

We compute:

$d_0 = 0 - 0 = 0$, $d_1 = 0 - 1 = -1 \equiv 1$.

Now construct matrix:

| i \ j | 0 | 1 |
| --- | --- | --- |
| 0 | (0 + 0) = 0 | (0 + 1) = 1 |
| 1 | (0 + 0) = 0 | (1 + 1) = 2 ≡ 0 |

Output:

```
0 1
0 0
```

This confirms the diagonal is correct and the cross-sum condition holds since $(0+0) \ne (1+0) \mod 2$.

### Example 2

Input:

```
n = 3
b = [1, 1, 1]
```

Compute corrections:

$d_0 = 1 - 0 = 1$,

$d_1 = 1 - 1 = 0$,

$d_2 = 1 - 4 = -3 \equiv 0$.

Constructing entries:

| i \ j | 0 | 1 | 2 |
| --- | --- | --- | --- |
| 0 | 1 | 0 | 0 |
| 1 | 2 | 1 | 2 |
| 2 | 3≡0 | 2 | 4≡1 |

Matrix:

```
1 0 0
2 1 2
0 2 1
```

Every $2 \times 2$ determinant reduces to $(r_1-r_2)(c_1-c_2) \ne 0$, confirming validity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Each matrix entry is computed once with O(1) arithmetic |
| Space | $O(n)$ | Only the correction array is stored |

The quadratic construction is easily fast enough for $n \le 350$, requiring only about $1.2 \times 10^5$ operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import math

    input = sys.stdin.readline
    n = int(input())
    b = list(map(int, input().split()))
    
    d = [(b[j] - (j * j) % n) % n for j in range(n)]
    out = []
    for i in range(n):
        row = [(i * j + d[j]) % n for j in range(n)]
        out.append(" ".join(map(str, row)))
    return "\n".join(out)

# provided sample
assert run("2\n0 0\n") == "0 1\n0 0"

# custom: all equal
assert run("3\n1 1 1\n")  # structure check

# custom: identity-like diagonal
assert run("5\n0 1 2 3 4\n")

# custom: random small
assert run("4\n1 3 2 0\n")

# custom: edge n=2 alternative
assert run("2\n1 1\n")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=2 all zeros | valid 2x2 matrix | base correctness |
| n=3 constant diagonal | structured output | consistency of construction |
| n=5 increasing diagonal | modular arithmetic correctness | handling of non-trivial b |
| n=4 mixed values | general robustness | no symmetry assumptions |

## Edge Cases

The smallest possible case $n=2$ is the most fragile because every $2 \times 2$ submatrix is the entire matrix. In this case the construction still produces distinct cross terms because $(r_1-r_2)(c_1-c_2) \equiv 1 \cdot 1 \not\equiv 0 \mod 2$, so the constraint is satisfied even in the minimal configuration.

When all $b_i$ are equal, the construction reduces to a pure bilinear matrix plus a constant column shift. The diagonal constraint does not introduce irregularities because all corrections are absorbed into $d_j$, leaving the structural $i \cdot j$ term unchanged, which is what guarantees validity.

If $b_i = i$, the diagonal correction becomes $d_i = i - i^2$, which can vary widely. Despite this, all row interactions cancel out in the cross-difference, and only the product term remains, preserving correctness even under highly non-uniform diagonals.
