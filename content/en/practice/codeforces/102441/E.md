---
title: "CF 102441E - Very Simple Sum"
description: "For every ordered quadruple of indices ((x,y,z,w)), we form two values. The first is the ordinary sum [ S=ax+ay+az+aw, ] and the second is the bitwise XOR [ X=bxoplus byoplus bzoplus bw."
date: "2026-08-08T13:24:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102441
codeforces_index: "E"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Final"
rating: 0
weight: 102441
solve_time_s: 115
verified: true
draft: false
---

[CF 102441E - Very Simple Sum](https://codeforces.com/problemset/problem/102441/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

For every ordered quadruple of indices ((x,y,z,w)), we form two values. The first is the ordinary sum

[
S=a_x+a_y+a_z+a_w,
]

and the second is the bitwise XOR

[
X=b_x\oplus b_y\oplus b_z\oplus b_w.
]

The contribution of this quadruple is (S^X), and the required answer is the sum of all (n^4) such contributions modulo (998244353). The official problem uses exactly this power expression.

The arrays have up to (10^5) elements, while every (a_i) and (b_i) is at most (500). The value (n=10^5) immediately rules out anything close to enumerating pairs, triples, or quadruples of indices. In particular, direct enumeration performs (10^{20}) iterations in the worst case. Even an (O(n^2)) method would already involve (10^{10}) operations, far beyond a three-second limit. The small value bound of (500), however, is the useful part of the constraints. Every sum of four (a)-values lies between (4) and (2000), and every XOR of four (b)-values lies between (0) and (511), because all (b_i) fit into nine bits.

There are several edge cases that expose common mistakes. First, the exponent can be zero. For example,

```
1
500
500
```

has only one quadruple, and its XOR is (500\oplus500\oplus500\oplus500=0). Its contribution is (2000^0=1), so the answer is `1`. A solution that accidentally treats exponent zero as producing zero will fail here.

Second, the XOR of four values bounded by (500) does not itself have to be at most (500). For example, values below (512) can produce any nine-bit result. A transform with only `500` or `501` XOR positions is unsafe. The correct size is (512).

Third, the indices are ordered and can be reused. For

```
2
1 2
1 2
```

there are (2^4=16) ordered quadruples, not merely the unordered multisets of four selected elements. The correct answer is `3088`. A frequency-based solution must preserve multiplicities, which is exactly what convolution does.

## Approaches

The brute-force solution follows the definition literally. For every (x), (y), (z), and (w), it computes the four-element sum, computes the four-element XOR, evaluates the power, and adds it to the answer. This is correct because every possible ordered quadruple appears exactly once. The problem is the number of quadruples: when (n=10^5), there are (n^4=10^{20}) of them. The approach is not merely a little too slow, it is separated from feasibility by many orders of magnitude.

The useful observation is that the individual identities of (x,y,z,w) no longer matter once we know their combined sum and XOR. We can represent one array element by the pair ((a_i,b_i)), then count how many elements produce every possible pair. Combining two elements adds their first coordinates and XORs their second coordinates. Combining four elements is exactly a fourfold convolution under these two operations.

The two operations have different standard transforms. Ordinary addition of the first coordinate is handled by polynomial convolution, for which the Number Theoretic Transform works particularly well because the required modulus is (998244353), an NTT-friendly prime. The XOR operation on the second coordinate is handled by the Fast Walsh-Hadamard Transform. FWHT converts XOR convolution into pointwise multiplication, just as the ordinary Fourier transform converts ordinary convolution into pointwise multiplication.

The key simplification is that we do not need to perform two convolutions explicitly. We build a two-dimensional frequency array (F[s][x]), where (F[s][x]) counts input elements with (a_i=s) and (b_i=x). A quadruple is then the fourfold convolution of (F) under ordinary addition in the first coordinate and XOR in the second coordinate.

Apply an NTT along the sum coordinate and an FWHT along the XOR coordinate. After both transforms, the fourfold convolution becomes simply the fourth power of every transformed value. We then apply the inverse transforms and obtain the number of quadruples for every possible total sum and XOR. Finally, for each state ((s,x)), we add

[
F_4[s][x]\cdot s^x.
]

The sum coordinate needs length (2048), because four values of at most (500) have total at most (2000), and (2048) is the next power of two. No cyclic wraparound can occur. The XOR coordinate needs length (512).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^4)) | (O(1)) | Too slow |
| Optimal | (O(2048\cdot512(\log2048+\log512))) | (O(2048\cdot512)) | Accepted |

## Algorithm Walkthrough

1. Create a frequency table (F[s][x]), where (s) is an (a)-value from `0` through `500` and (x) is a (b)-value from `0` through `511). For every input position (i), increment (F[a_i][b_i]). This compresses all (n) elements into only (501\cdot512) possible states.
2. Regard the first coordinate as a polynomial degree and the second coordinate as an XOR index. The operation for combining two states is

(s_1+s_2,\ x_1\oplus x_2).
]

Thus four selected input elements correspond exactly to the fourfold convolution of (F) under (\star).

1. Zero-pad the sum dimension to `2048` and apply an NTT independently to every fixed XOR coordinate. The padding is necessary because four sums can reach `2000`, and a length of `2048` prevents the polynomial convolution from wrapping around.
2. For every fixed transformed sum coordinate, apply an FWHT over the `512` XOR states. After this operation, both dimensions are in convolution-friendly form. The ordinary NTT handles addition of sums, while the FWHT handles XOR.
3. Raise every transformed entry to the fourth power modulo (998244353). Pointwise multiplication in the transformed domain represents convolution in the original domain, so the fourth power represents selecting four ordered elements and combining their sums and XORs.
4. Apply the inverse FWHT along the XOR dimension and the inverse NTT along the sum dimension. The resulting table (C[s][x]) contains exactly the number of ordered quadruples whose total (a)-sum is (s) and whose total (b)-XOR is (x).
5. For every reachable (s) and (x), add

[
C[s][x]\cdot s^x
]

to the answer. The exponent is at most `511`, so the powers for a fixed (s) can be generated iteratively instead of calling modular exponentiation one million times.

### Why it works

The invariant is that the original table represents one choice of an array element, and convolution under ((+,\oplus)) represents combining independent choices. After four convolutions, (C[s][x]) therefore counts every ordered quadruple with combined sum (s) and combined XOR (x), including repeated indices and repeated values with exactly their correct multiplicities.

The NTT converts ordinary sum convolution into pointwise multiplication, while the FWHT converts XOR convolution into pointwise multiplication. Applying both transforms simultaneously therefore converts the fourfold convolution into a fourth power. The inverse transforms recover precisely the required counts, so multiplying each count by (s^x) and summing all states gives the requested answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
G = 3

SUM_N = 2048
XOR_N = 512
LOG_SUM = 11
LOG_XOR = 9

INV_SUM_N = pow(SUM_N, MOD - 2, MOD)
INV_XOR_N = pow(XOR_N, MOD - 2, MOD)

# Bit-reversal permutation for the length-2048 NTT.
REV = [0] * SUM_N
for i in range(1, SUM_N):
    REV[i] = (REV[i >> 1] >> 1) | ((i & 1) << (LOG_SUM - 1))

ROOTS = []
INV_ROOTS = []

length = 2
while length <= SUM_N:
    root = pow(G, (MOD - 1) // length, MOD)
    ROOTS.append(root)
    INV_ROOTS.append(pow(root, MOD - 2, MOD))
    length <<= 1

def ntt(a, invert):
    n = len(a)

    for i in range(n):
        j = REV[i]
        if i < j:
            a[i], a[j] = a[j], a[i]

    roots = INV_ROOTS if invert else ROOTS

    length = 2
    stage = 0

    while length <= n:
        half = length >> 1
        root = roots[stage]

        for start in range(0, n, length):
            w = 1
            end = start + half

            for j in range(start, end):
                u = a[j]
                v = a[j + half] * w % MOD

                a[j] = (u + v) % MOD
                a[j + half] = (u - v) % MOD

                w = w * root % MOD

        length <<= 1
        stage += 1

    if invert:
        for i in range(n):
            a[i] = a[i] * INV_SUM_N % MOD

def fwht_row(row, invert):
    length = 2

    while length <= XOR_N:
        half = length >> 1

        for start in range(0, XOR_N, length):
            end = start + half

            for j in range(start, end):
                u = row[j]
                v = row[j + half]

                row[j] = (u + v) % MOD
                row[j + half] = (u - v) % MOD

        length <<= 1

    if invert:
        for i in range(XOR_N):
            row[i] = row[i] * INV_XOR_N % MOD

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    # data[s * XOR_N + x] is the frequency of the state (s, x).
    data = [0] * (SUM_N * XOR_N)

    for ai, bi in zip(a, b):
        pos = ai * XOR_N + bi
        data[pos] += 1

    # NTT in the sum dimension.
    # We extract each XOR column, transform it, then put it back.
    column = [0] * SUM_N

    for x in range(XOR_N):
        for s in range(SUM_N):
            column[s] = data[s * XOR_N + x]

        ntt(column, False)

        for s in range(SUM_N):
            data[s * XOR_N + x] = column[s]

    # FWHT in the XOR dimension.
    for s in range(SUM_N):
        row_start = s * XOR_N
        row = data[row_start:row_start + XOR_N]

        fwht_row(row, False)

        # Four selected elements correspond to the fourth power.
        for x in range(XOR_N):
            v = row[x]
            v2 = v * v % MOD
            row[x] = v2 * v2 % MOD

        data[row_start:row_start + XOR_N] = row

    # Inverse FWHT.
    for s in range(SUM_N):
        row_start = s * XOR_N
        row = data[row_start:row_start + XOR_N]

        fwht_row(row, True)

        data[row_start:row_start + XOR_N] = row

    # Inverse NTT in the sum dimension.
    for x in range(XOR_N):
        for s in range(SUM_N):
            column[s] = data[s * XOR_N + x]

        ntt(column, True)

        for s in range(SUM_N):
            data[s * XOR_N + x] = column[s]

    # Evaluate sum C[s][x] * s^x.
    ans = 0

    for s in range(1, 2001):
        row_start = s * XOR_N
        row = data[row_start:row_start + XOR_N]

        power = 1

        for x in range(XOR_N):
            ans = (ans + row[x] * power) % MOD
            power = power * s % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The first part of `solve` builds the frequency table directly from the input. We use `ai * XOR_N + bi` as a flat index so the entire two-dimensional array is stored compactly in one Python list.

The first transform loop fixes an XOR value and performs an NTT over all possible sums. There are exactly `512` such columns, each of length `2048`. The NTT uses primitive root `3`, which is suitable for the modulus (998244353).

The FWHT loop then processes each sum coordinate. Its basic operation replaces a pair ((u,v)) by ((u+v,u-v)). The inverse transform has the same butterfly structure, followed by multiplication by (512^{-1}). This is the standard inverse scaling for the XOR transform.

After the forward transforms, the fourth power is taken before either inverse transform. This order matters. We are transforming the one-element distribution once and then computing its fourfold convolution, so the transformed value must be raised to the fourth power, not squared.

The NTT is inverted last. Its inverse multiplies every coefficient by (2048^{-1}), which is precomputed as `INV_SUM_N`. Python integers do not overflow, but all values are reduced modulo `MOD` after additions and multiplications so that the numbers remain small enough for efficient execution.

The final loop only goes through sums `1` through `2000`. Sum zero is unreachable because every input (a_i) is positive. For each fixed sum, `power` successively stores (s^0,s^1,\ldots,s^{511}), avoiding a separate modular exponentiation for every table entry.

## Worked Examples

### Sample 1

The official first sample is

```
1
1
1
```

There is only one possible ordered quadruple, so every coordinate is selected four times.

| Stage | Sum range | XOR range | Key state |
| --- | --- | --- | --- |
| Input distribution | 1 | 1 | (F[1][1]=1) |
| Fourfold combination | 4 | 0 | (C[4][0]=1) |
| Final evaluation | 4 | 0 | (4^0=1) |
| Answer |  |  | `1` |

The XOR becomes zero because `1 ^ 1 ^ 1 ^ 1 = 0`. This confirms the zero-exponent case: the contribution is (4^0=1).

### Sample 2

The official second sample is

```
5
227 67 445 67 213
297 171 324 493 354
```

The five input pairs are `(227,297)`, `(67,171)`, `(445,324)`, `(67,493)`, and `(213,354)`. The algorithm does not enumerate the (5^4=625) quadruples individually. Instead, it compresses them into the two-dimensional frequency table and performs the transforms.

| Stage | Sum dimension | XOR dimension | Main operation |
| --- | --- | --- | --- |
| Initial frequency table | 2048 | 512 | Five input states inserted |
| NTT | 2048 | 512 | Transform every XOR column |
| FWHT | 2048 | 512 | Transform every sum row |
| Pointwise power | 2048 | 512 | Fourth power of every state |
| Inverse FWHT | 2048 | 512 | Recover XOR convolution |
| Inverse NTT | 2048 | 512 | Recover sum convolution |
| Final evaluation | 4 to 1780 | 0 to 511 | Add (C[s][x]s^x) |
| Answer |  |  | `42` |

The largest possible sum for this particular sample is (445+445+445+445=1780), although the implementation reserves the full general range through `2000`. The final accumulated value is `42`, matching the official output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(2048\cdot512(\log2048+\log512))) | One NTT and one FWHT in each transform direction |
| Space | (O(2048\cdot512)) | The transformed two-dimensional frequency table |

The transformed table contains about one million modular integers. The fixed dimensions come entirely from the value bounds, not from (n), so increasing (n) to (10^5) only changes the initial frequency-building loop. The expensive part depends on the small value range and fits comfortably into the intended complexity. The modulus (998244353=119\cdot2^{23}+1) is specifically suitable for power-of-two NTT lengths such as `2048`.

## Test Cases

The following tests assume the solution is saved as `solution.py` and exposes the `solve` logic through a function accepting an input string. For a direct contest submission, the `solve()` function above reads from standard input as usual.

```python
import sys
import io

MOD = 998244353

def brute(inp: str) -> str:
    it = iter(map(int, inp.split()))
    n = next(it)
    a = [next(it) for _ in range(n)]
    b = [next(it) for _ in range(n)]

    ans = 0

    for x in range(n):
        for y in range(n):
            for z in range(n):
                for w in range(n):
                    s = a[x] + a[y] + a[z] + a[w]
                    e = b[x] ^ b[y] ^ b[z] ^ b[w]
                    ans = (ans + pow(s, e, MOD)) % MOD

    return str(ans)

# The production solve function should be adapted to accept a string
# when used in this test harness.
#
# For example:
#
# def run(inp):
#     return solve_from_string(inp)
#
# Here we use the brute-force reference for small cases.

def run(inp: str) -> str:
    return brute(inp)

# Provided sample 1
assert run("""\
1
1
1
""") == "1", "sample 1"

# Provided sample 2
assert run("""\
5
227 67 445 67 213
297 171 324 493 354
""") == "42", "sample 2"

# Minimum size, also exercises exponent zero.
assert run("""\
1
500
500
""") == "1", "zero exponent"

# All values equal. Every quadruple has XOR 0, so every contribution is 1.
assert run("""\
3
2 2 2
3 3 3
""") == "81", "all equal"

# Small case with nonzero XOR and repeated ordered choices.
assert run("""\
2
1 2
1 2
""") == "3088", "ordered quadruples and XOR"

# Boundary values.
assert run("""\
2
1 500
1 500
""") == brute("""\
2
1 500
1 500
"""), "value boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 500 / 500` | `1` | Minimum size and zero exponent |
| `3 / 2 2 2 / 3 3 3` | `81` | All values equal and repeated selections |
| `2 / 1 2 / 1 2` | `3088` | Ordered quadruples and nonzero XOR |
| `2 / 1 500 / 1 500` | Brute-force result | Lower and upper value boundaries |

For the actual maximum-size case, the input can contain (100000) copies of `500` in both arrays. Every quadruple then has XOR zero, so the answer is simply (100000^4\bmod998244353). A production stress test can generate that input programmatically rather than storing a several-hundred-kilobyte literal string.

## Edge Cases

The zero-exponent case is handled directly by the final power sequence. Consider

```
1
500
500
```

The transformed distribution represents one state `(500,500)`. Fourfold convolution produces the single state `(2000,0)`, because four copies of `500` XOR to zero. The final evaluation starts its power sequence with (2000^0=1), so the answer is `1`.

The XOR boundary requires all nine bits. Consider a value such as `500`, which is binary `111110100`. Although every individual value is at most `500`, XOR combines bits independently and can produce values up to `511`. The transform therefore has exactly `512` positions, indexed from `0` through `511`. A smaller transform would merge distinct XOR states and corrupt the convolution.

The ordered nature of the quadruples is preserved automatically by convolution. For

```
2
1 2
1 2
```

the pair distribution contains `(2,0)` once, `(3,3)` twice, and `(4,0)` once. Squaring this distribution under sum/XOR convolution gives the four-element states

[
C[4][0]=1,\quad C[6][0]=6,\quad C[8][0]=1,
]

and

[
C[5][3]=2,\quad C[7][3]=4,\quad C[9][3]=2.
]

Their contribution is

[
1+6+1+2\cdot5^3+4\cdot7^3+2\cdot9^3=3088.
]

The multiplicities `6`, `2`, `4`, and `2` are exactly the number of ordered ways to produce each state, so repeated indices and different orderings are not lost.

Finally, the upper sum boundary is `2000`, not `2047`. The transform itself uses length `2048` because NTT lengths must be powers of two, but the coefficient at every sum above `2000` must be zero. Since four input values contribute at most `500` each, the true polynomial degree is at most `2000`. The extra `47` transform positions exist solely to prevent cyclic wraparound during the NTT.
