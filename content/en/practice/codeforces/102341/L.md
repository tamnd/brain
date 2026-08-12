---
title: "CF 102341L - Lati@s"
description: "The game looks enormous because one move replaces a single tuple by up to (2^n-1) new tuples, and the initial position already contains (n!) tuples. The useful way to look at it is not as a simulation, but as an impartial game whose positions have Sprague-Grundy values."
date: "2026-08-13T03:26:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102341
codeforces_index: "L"
codeforces_contest_name: "Radewoosh+mnbvmar Contest (supported by AIM Tech)"
rating: 0
weight: 102341
solve_time_s: 161
verified: true
draft: false
---

[CF 102341L - Lati@s](https://codeforces.com/problemset/problem/102341/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

The game looks enormous because one move replaces a single tuple by up to (2^n-1) new tuples, and the initial position already contains (n!) tuples. The useful way to look at it is not as a simulation, but as an impartial game whose positions have Sprague-Grundy values.

A tuple (A=(A_1,\ldots,A_n)) can be played only when every coordinate is positive. A move chooses an arbitrary tuple (B) with (0\le B_i<A_i), removes (A), and inserts every tuple obtained by independently choosing, in each coordinate, either (A_i) or (B_i), except that the original tuple (A) itself is not inserted. The whole position is a disjoint sum of these tuple games, so the Grundy values of all tuples are XORed.

The input gives an (n\times n) matrix (M). For every permutation of its columns, we take one entry from every row using distinct columns and obtain one initial tuple. Thus the initial position contains the (n!) products associated with all permutation selections from the matrix. The required output is simply whether the XOR of their Grundy values is zero. A zero value means the second player wins, while a nonzero value means the first player wins.

The bound (n\le150) rules out anything exponential in (n), including explicitly generating the (n!) tuples. Even for (n=20), (n!) is already about (2.4\cdot10^{18}), and for (n=150) it is far beyond any practical representation. The matrix has only (n^2\le22500) entries, which strongly suggests that the permutation sum must be rewritten algebraically. The matrix entries are below (2^{64}), so ordinary signed 64-bit arithmetic is unsafe, and the required multiplication is not ordinary integer multiplication anyway.

There are several small cases that easily fool an implementation which treats the game like ordinary arithmetic. For example,

```
1
0
```

has output `Second`. The only tuple is ((0)), so it has no legal move. An implementation that treats every tuple as a positive heap would incorrectly declare a first-player win.

For

```
1
18446744073709551615
```

the output is `First`. With one coordinate, the game is exactly an ordinary Nim heap of that size, so every positive value is winning. A signed 64-bit parser would already fail on this input because (2^{64}-1) is larger than (2^{63}-1).

Another subtle case is repeated rows. For example,

```
2
1 1
1 1
```

has output `Second`. There are two identical permutation tuples, namely ((1,1)) twice. Their Grundy values cancel by XOR. An implementation that converts the permutation sum into an ordinary integer sum would miss this characteristic-two cancellation.

Finally, the second sample,

```
2
1 2
2 3
```

also gives `Second`. The determinant-like expression is (1\otimes3\oplus2\otimes2=3\oplus3=0), where (\otimes) is nimber multiplication. Using ordinary multiplication would give (3+4=7), which has nothing to do with the game's Grundy value.

## Approaches

A direct approach would enumerate every permutation, build its tuple, compute the Grundy value of that tuple, and XOR all those values. This is already impossible because there are (n!) permutations. For a worst-case matrix with every entry equal to (2^{64}-1), there are (n!) initial tuples, and if we tried to enumerate all legal choices of (B) from one such tuple, there are ((2^{64}-1)^n) choices for (B), with (2^n-1) generated tuples for every choice. Thus even enumerating the first layer of the game tree would involve (n!(2^{64}-1)^n(2^n-1)) combinations. The brute force is conceptually correct, but it fails before the actual game analysis even becomes relevant.

The key observation is that the Grundy value of a tuple has a remarkably algebraic form. A one-coordinate tuple containing (a) has Grundy value (a). For several coordinates, the move replaces (A) by all nonempty combinations of (A_i) and (B_i). Because Grundy values of independent components are XORed, the XOR of the generated tuples expands exactly like a product over characteristic two.

This is precisely the recursive game interpretation of nimber multiplication. If a tuple is (A=(A_1,\ldots,A_n)), its Grundy value is

[
g(A)=A_1\otimes A_2\otimes\cdots\otimes A_n.
]

The reason is that the move from (A) with a chosen (B) creates the same three-corner, four-corner, and higher-dimensional structure used in the standard recursive definition of nimber multiplication. The XOR over all nonempty subsets is the corresponding product expansion, and the mex characterization of nimber multiplication gives exactly the required Grundy recurrence. This is the (n)-dimensional version of Conway's diminishing-rectangle game.

The starting position is consequently the XOR of

[
\bigotimes_{i=1}^{n} M_{i,\sigma(i)}
]

over every permutation (\sigma). Nimber addition is XOR, and nimber multiplication is distributive over XOR. Expanding the determinant over a field of characteristic two gives exactly this permutation sum. The usual determinant sign disappears because (1=-1) in characteristic two. Thus the entire game reduces to computing

[
\det(M)
]

where every addition is XOR and every multiplication is nimber multiplication. This reduction is also the central observation of the published solution discussion for this problem.

The remaining challenge is implementing nimber multiplication fast enough. Values below (2^{64}) form the finite field (\mathrm{GF}(2^{64})) under nimber addition and multiplication. A naive recursive multiplication is too expensive inside (O(n^3)) Gaussian elimination. We instead split 64-bit nimbers into 16-bit pieces and precompute a logarithm/exponent representation of the 16-bit nimber field. A 64-bit product can then be assembled using only a constant number of 16-bit field products. This is the same divide-and-conquer construction used by established nimber libraries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n!(2^{64})^n2^n)) already for the first move layer | Astronomical | Too slow |
| Optimal | (O(n^3+2^{16})) | (O(n^2+2^{16})) | Accepted |

## Algorithm Walkthrough

1. Interpret every matrix entry as a 64-bit nimber. Addition of nimbers is ordinary bitwise XOR, while multiplication is the special nimber product.
2. Regard each initial tuple as an independent impartial game. The Grundy value of a tuple (A) is

[
A_1\otimes A_2\otimes\cdots\otimes A_n.
]

The multidimensional move rule is exactly the recursive construction whose Grundy value is nimber multiplication, so we never need to simulate the descendants of a tuple.

1. XOR the Grundy values of all permutation tuples. By distributivity, this becomes

[
\bigoplus_{\sigma}
\left(
M_{1,\sigma(1)}
\otimes\cdots\otimes
M_{n,\sigma(n)}
\right).
]

This is the determinant of (M) over the field of 64-bit nimbers. Since the field has characteristic two, there is no separate sign for odd permutations.

1. Compute this determinant with Gaussian elimination. For column (k), find a row (p\ge k) with a nonzero entry in that column. If none exists, the determinant is zero and the answer is immediately `Second`.
2. Swap row (p) with row (k). In an ordinary field a row swap negates the determinant, but in characteristic two the negation of a value is itself, so the determinant does not change.
3. Multiply the determinant accumulator by the pivot (A_{k,k}). Then compute its multiplicative inverse and use it to eliminate the entries below the pivot. For a row (i>k), the required factor is

[
f=A_{i,k}\otimes A_{k,k}^{-1}.
]

For every (j>k), replace

[
A_{i,j}
\leftarrow
A_{i,j}\oplus(f\otimes A_{k,j}).
]

The entry in column (k) can then be set directly to zero.

1. Compute inverses using the field identity

[
x^{-1}=x^{2^{64}-2}
]

for nonzero (x). Binary exponentiation needs only 64 nimber multiplications per pivot, which is negligible compared with the (O(n^3)) elimination updates. The finite-field inverse identity is also the one used in published solutions.

1. After all columns have been processed, the determinant accumulator is the Grundy value of the entire starting position. Print `First` when it is nonzero and `Second` otherwise.

### Why it works

The invariant is that the XOR of the Grundy values of all currently represented tuple games is the nim-sum of their individual game values. For one tuple, the move rule is exactly the multidimensional diminishing-rectangle game, whose Grundy value is the nimber product of its coordinates. Consequently the initial position has value equal to the XOR of the nimber products selected by all permutations. Distributivity turns that permutation XOR into the determinant of (M) over the nimber field. Gaussian elimination preserves that determinant while reducing the matrix to triangular form, and the product of its pivots is the determinant. A zero determinant means a zero Grundy value, which is precisely a losing position for the first player.

## Python Solution

```python
import sys
input = sys.stdin.readline

MASK16 = 65535
ORDER = 65535
PROOT = 10279
PPOLY = 92191

def build_small_table():
    dp = [[0] * 256 for _ in range(256)]
    dp[1][1] = 1

    for e in range(1, 4):
        p = 1 << e
        q = p >> 1
        ep = 1 << p
        eq = 1 << q
        mask = eq - 1

        for i in range(ep):
            for j in range(i, ep):
                if i < eq and j < eq:
                    continue

                if min(i, j) <= 1:
                    v = i * j
                else:
                    iu = i >> q
                    il = i & mask
                    ju = j >> q
                    jl = j & mask

                    u = dp[iu][ju]
                    l = dp[il][jl]
                    ul = dp[iu ^ il][ju ^ jl]
                    uq = dp[u][eq >> 1]

                    v = ((ul ^ l) << q) ^ uq ^ l

                dp[i][j] = v
                dp[j][i] = v

    return dp

SMALL = build_small_table()

def nim16_direct(a, b):
    if a == 0 or b == 0:
        return 0
    if min(a, b) <= 1:
        return a * b

    iu = a >> 8
    il = a & 255
    ju = b >> 8
    jl = b & 255

    u = SMALL[iu][ju]
    l = SMALL[il][jl]
    ul = SMALL[iu ^ il][ju ^ jl]
    uq = SMALL[u][128]

    return ((ul ^ l) << 8) ^ uq ^ l

def build_field_tables():
    base = [1] * 16
    for i in range(1, 16):
        base[i] = nim16_direct(base[i - 1], PROOT)

    raw_exp = [0] * ORDER
    raw_exp[0] = 1

    for i in range(1, ORDER):
        x = raw_exp[i - 1]
        raw_exp[i] = (x << 1) ^ (PPOLY if x & 32768 else 0)

    pre = [0] * 65536
    for bit in range(16):
        start = 1 << bit
        end = start << 1
        value = base[bit]
        for x in range(start, end):
            pre[x] = pre[x - start] ^ value

    exp = [0] * ORDER
    log = [0] * 65536

    for i in range(ORDER):
        value = pre[raw_exp[i]]
        exp[i] = value
        log[value] = i

    return exp, log

EXP16, LOG16 = build_field_tables()

def mul16(a, b):
    if a == 0 or b == 0:
        return 0
    return EXP16[(LOG16[a] + LOG16[b]) % ORDER]

def h16(a, shift):
    if a == 0:
        return 0
    return EXP16[(LOG16[a] + shift) % ORDER]

def mul32(a, b):
    ah = a >> 16
    al = a & MASK16
    bh = b >> 16
    bl = b & MASK16

    low = mul16(al, bl)
    cross = mul16(ah ^ al, bh ^ bl)
    high = h16(mul16(ah, bh), 3)

    return ((cross ^ low) << 16) ^ high ^ low

def mul64(a, b):
    if a == 0 or b == 0:
        return 0

    ah = a >> 32
    al = a & 0xffffffff
    bh = b >> 32
    bl = b & 0xffffffff

    low = mul32(al, bl)
    cross = mul32(ah ^ al, bh ^ bl)

    high_part = mul32(ah, bh)
    h_high = (
        (h16((high_part >> 16) ^ (high_part & MASK16), 3) << 16)
        ^ h16(high_part >> 16, 6)
    )

    return ((cross ^ low) << 32) ^ h_high ^ low

def nim_pow(a, e):
    result = 1
    while e:
        if e & 1:
            result = mul64(result, a)
        a = mul64(a, a)
        e >>= 1
    return result

def nim_inverse(a):
    return nim_pow(a, (1 << 64) - 2)

def determinant(mat):
    n = len(mat)
    det = 1

    for col in range(n):
        pivot = col
        while pivot < n and mat[pivot][col] == 0:
            pivot += 1

        if pivot == n:
            return 0

        if pivot != col:
            mat[pivot], mat[col] = mat[col], mat[pivot]

        p = mat[col][col]
        det = mul64(det, p)
        inv = nim_inverse(p)

        pivot_row = mat[col]

        for i in range(col + 1, n):
            value = mat[i][col]
            if value == 0:
                continue

            factor = mul64(value, inv)
            row = mat[i]

            row[col] = 0
            for j in range(col + 1, n):
                row[j] ^= mul64(factor, pivot_row[j])

    return det

def solve():
    n = int(input())
    mat = [list(map(int, input().split())) for _ in range(n)]

    ans = determinant(mat)
    print("First" if ans else "Second")

if __name__ == "__main__":
    solve()
```

The first preprocessing stage builds multiplication for all nimbers below (256). The recurrence splits an 8-bit value into two halves and uses the recursive definition of nimber multiplication. This table contains only (256^2) entries.

The next stage constructs a representation of the field with 65536 elements. The value `PPOLY = 92191` describes the irreducible polynomial used for the polynomial representation, while `PROOT = 10279` provides a primitive element in the nimber representation. The exponent table converts powers of that primitive element into actual 16-bit nimbers, and `LOG16` performs the reverse mapping. This construction is the 16-bit version of the standard fast nimber implementation.

A 16-bit nimber product is then just two table lookups and an index operation. The 32-bit and 64-bit products use the Karatsuba-style identity from the nimber field. In particular, `mul32` requires three 16-bit products, and `mul64` requires three 32-bit products. The shift represented by `h16` corresponds to multiplication by (2^{15}) in the 16-bit field decomposition.

The determinant routine performs ordinary Gaussian elimination with XOR replacing addition. Since the field has characteristic two, row swaps do not introduce a sign change. The pivot itself is multiplied into `det` before the row is used for elimination, so the final value remains the determinant even though the elimination rows are not normalized.

The inverse exponent is `(1 << 64) - 2`, which is exactly (2^{64}-2). Python integers have arbitrary precision, so there is no overflow while constructing that exponent or while parsing the input values. The matrix entries themselves remain below (2^{64}), and every nimber operation returns another 64-bit field element.

The order of operations during elimination matters. The factor must be computed using the inverse of the current pivot before the pivot row is modified. In this implementation the pivot row is never normalized, so its original entries remain available for every row update.

## Worked Examples

### Sample 1

The matrix is

```
0 1 2
1 2 3
1 2 1
```

The elimination trace is:

| Column | Pivot row | Pivot | Row updates | Determinant |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | (R_1\leftrightarrow R_0), then (R_2\leftarrow R_2\oplus R_0) | 1 |
| 1 | 1 | 1 | No nonzero entry below pivot | 1 |
| 2 | 2 | 2 | No rows below | 2 |

After the first swap the matrix is

```
1 2 3
0 1 2
1 2 1
```

The factor for the third row is (1\otimes1^{-1}=1), so the third row becomes

```
0 0 2
```

The triangular pivots are therefore (1,1,2), and the determinant is

[
1\otimes1\otimes2=2.
]

The determinant is nonzero, so the initial game has nonzero Grundy value and the answer is `First`.

This trace also demonstrates why ordinary multiplication must not be substituted into the determinant. The same matrix is being evaluated in the nimber field, where, for example, (2\otimes2=3).

### Sample 2

The matrix is

```
1 2
2 3
```

The trace is:

| Column | Pivot | Inverse | Row factor | Updated row | Determinant |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 2 | ([0,,3\oplus(2\otimes2)]=[0,0]) | 1 |
| 1 | 0 | unavailable | none | none | 0 |

Since (2\otimes2=3), the second entry becomes

[
3\oplus3=0.
]

The second pivot does not exist, so the determinant is zero and the answer is `Second`.

This example exercises the exact situation where the matrix becomes singular because nimber multiplication differs from ordinary integer multiplication.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^3+2^{16})) | Gaussian elimination performs (O(n^3)) field operations, while the 16-bit tables require (O(2^{16})) preprocessing |
| Space | (O(n^2+2^{16})) | The matrix needs (O(n^2)) storage and the exponent/logarithm tables need (O(2^{16})) storage |

For (n\le150), Gaussian elimination has only about a few million matrix-level operations, and each nimber multiplication reduces to a constant number of 16-bit table accesses. The preprocessing is independent of (n), so the solution fits the intended polynomial bound rather than the factorial size of the original permutation set.

## Test Cases

The following harness assumes the submitted implementation is saved as `solution.py` and exposes the `solve()` function. The maximum-size case is generated programmatically so the test file itself remains readable.

```python
# test_solution.py
import sys
import io
from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run(
    """3
0 1 2
1 2 3
1 2 1
"""
) == "First", "sample 1"

# Provided sample 2
assert run(
    """2
1 2
2 3
"""
) == "Second", "sample 2"

# Minimum size, zero tuple is immediately losing.
assert run(
    """1
0
"""
) == "Second", "single zero"

# Minimum size, largest allowed input value is positive.
MAX64 = (1 << 64) - 1
assert run(
    f"""1
{MAX64}
"""
) == "First", "single maximum value"

# Identity matrix has determinant 1.
assert run(
    """2
1 0
0 1
"""
) == "First", "identity matrix"

# Equal rows make the determinant zero.
assert run(
    """2
1 1
1 1
"""
) == "Second", "equal rows"

# Boundary value combined with a zero entry.
assert run(
    f"""2
{MAX64} 0
0 1
"""
) == "First", "maximum boundary value"

# Maximum n, all rows equal, so determinant is zero.
max_case = "150\n" + "\n".join(["7 " * 149 + "7"] * 150) + "\n"
assert run(max_case) == "Second", "maximum n with equal rows"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0` | `Second` | A tuple containing zero has no move |
| `1 / 2^64-1` | `First` | 64-bit unsigned boundary and the one-dimensional game |
| `2 / identity` | `First` | A nonzero determinant with zero off-diagonal entries |
| `2 / equal rows` | `Second` | Characteristic-two cancellation and singular matrices |
| `2 / [[2^64-1,0],[0,1]]` | `First` | Maximum input value without signed overflow |
| `150 / all 7` | `Second` | Maximum matrix dimension and immediate zero determinant |

## Edge Cases

The zero tuple case is handled before any inverse or elimination is attempted. For

```
1
0
```

the determinant is the single entry (0), so the algorithm returns zero and prints `Second`. This matches the game because a tuple containing zero cannot be selected.

For the largest possible value,

```
1
18446744073709551615
```

the determinant is that same nonzero nimber. The one-dimensional game is an ordinary Nim heap, so its Grundy value is the heap size itself. The algorithm never converts the value to a signed type, and the nonzero determinant produces `First`.

Repeated tuples are handled automatically by XOR. With

```
2
1 1
1 1
```

both permutations produce exactly the same tuple ((1,1)). Its Grundy value is (1\otimes1=1), and the two copies contribute (1\oplus1=0). The determinant is also zero because the two rows are equal, so the algorithm prints `Second`.

A zero pivot does not imply a zero determinant until the algorithm has searched all rows below it. For example,

```
2
0 1
1 0
```

starts with a zero in the first pivot position, but the second row supplies the nonzero pivot. After swapping the rows, the pivots are (1) and (1), giving determinant (1) and output `First`. An implementation that simply checks `matrix[k][k] == 0` without searching for another row would incorrectly return `Second`.

The second sample exposes the difference between ordinary arithmetic and nimber arithmetic. For

```
2
1 2
2 3
```

the elimination factor is (2), and the lower-right value becomes

[
3\oplus(2\otimes2)=3\oplus3=0.
]

The determinant is zero, so the result is `Second`. Ordinary integer elimination would instead use (2\cdot2=4) and obtain (3-4=-1), which is unrelated to the game's algebra.

At the maximum dimension, consider a (150\times150) matrix in which every entry is (7). The first pivot can be chosen, but every other row is identical to it, so elimination makes all later pivot columns vanish. Equivalently, the determinant has two equal rows and is zero. The algorithm terminates with `Second` without ever constructing the (150!) initial tuples.
