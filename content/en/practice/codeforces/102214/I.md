---
title: "CF 102214I - Image"
description: "We have a large grayscale image (I), whose pixels are bytes written as two-digit hexadecimal values, and a smaller template image (T). The template may have been cropped from the large image, but because of lossy compression, its pixels need not match exactly."
date: "2026-08-18T11:35:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102214
codeforces_index: "I"
codeforces_contest_name: "\u041e\u0442\u043a\u0440\u044b\u0442\u043e\u0435 \u043b\u0438\u0447\u043d\u043e\u0435 \u043f\u0435\u0440\u0432\u0435\u043d\u0441\u0442\u0432\u043e \u0418\u041a\u0418\u0422 \u0421\u0424\u0423 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2015"
rating: 0
weight: 102214
solve_time_s: 217
verified: true
draft: false
---

[CF 102214I - Image](https://codeforces.com/problemset/problem/102214/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a large grayscale image (I), whose pixels are bytes written as two-digit hexadecimal values, and a smaller template image (T). The template may have been cropped from the large image, but because of lossy compression, its pixels need not match exactly.

For every possible top-left position ((x,y)) where the template fits, we compare every template pixel (T(i,j)) with the corresponding image pixel (I(x+i,y+j)). The score is the sum of squared differences,

[
SSD(x,y)=\sum_{i=0}^{M-1}\sum_{j=0}^{N-1}
(I(x+j,y+i)-T(j,i))^2.
]

The required output is any position having the minimum score. The coordinates are zero-based, so (0\le x\le W-N) and (0\le y\le H-M). The input pixels are hexadecimal, but after parsing them they are ordinary integers from 0 through 255.

The large image can contain up to (1024\cdot768=786432) pixels, while the template can itself be almost as large. A direct comparison at every possible position can consequently perform tens of billions of pixel operations. A quadratic or quartic algorithm in the image dimensions is not realistic under a 4 second limit. We need to compute all template correlations simultaneously, which is exactly the kind of operation for which convolution and FFT are useful.

There are several boundary cases that a direct implementation can mishandle. If the template has exactly the same dimensions as the image, there is only one legal position. For example,

```
1 1
7
1 1
7
```

has the only possible answer `0 0`. A search that accidentally uses `< W-N` instead of `<= W-N` would find no position.

A one-pixel template is another useful boundary case. For

```
3 1
10 20 30
1 1
1E
```

the template contains hexadecimal `1E`, which is decimal 30, so the answer is `2 0`. Treating the input as decimal rather than hexadecimal would silently change the problem.

Equal-valued images can have many optimal positions. For

```
3 2
07 07 07
07 07 07
2 1
07 07
```

every legal position has SSD zero, so `0 0`, `1 0`, and `0 1` are all correct. The program must not assume that the optimum is unique.

Finally, the bottom-right position is legal and must be inspected. For example,

```
3 3
00 00 00
00 00 00
00 00 2A
1 1
2A
```

has the unique optimum at `2 2`. An incorrect loop stopping at `W-N-1` or `H-M-1` misses it.

## Approaches

The brute-force method follows the definition directly. For every legal top-left position, it visits all (NM) template pixels, computes the difference with the corresponding image pixel, squares it, and adds it to the current score. This is correct because every SSD is evaluated exactly as defined.

The number of positions is

[
(W-N+1)(H-M+1),
]

so the total work is

[
O((W-N+1)(H-M+1)NM).
]

At (W=1024), (H=768), (N=512), and (M=384), there are (513\cdot385=197505) positions and each comparison scans (512\cdot384=196608) pixels. That is about (3.88\times10^{10}) pixel comparisons. The brute-force method is mathematically simple but far beyond what the time limit permits.

The useful observation comes from expanding the square:

[
(I-T)^2=I^2-2IT+T^2.
]

For a fixed position, this gives

\sum I(x+j,y+i)^2
-2\sum I(x+j,y+i)T(j,i)
+\sum T(j,i)^2.
]

The last term is independent of the position, because the template never changes. The first term is a sum of squares over a rectangular window of the large image, so every such value can be obtained in constant time after building a two-dimensional prefix sum of (I^2).

The only difficult part is

[
C(x,y)=
\sum I(x+j,y+i)T(j,i).
]

This is a two-dimensional cross-correlation. If we reverse the template in both dimensions, the correlation becomes an ordinary two-dimensional convolution. The convolution theorem says that this convolution can be computed by transforming both arrays with a two-dimensional FFT, multiplying corresponding frequency coefficients, and transforming the result back. This changes the expensive part from scanning every template pixel at every position to roughly (O(PQ(\log P+\log Q))), where (P) and (Q) are suitable powers of two.

There is also a useful implementation optimization. A straightforward FFT solution would perform one forward transform for the image and another for the reversed template, followed by one inverse transform. Since both inputs are real, we can pack them into one complex array as (I+iT'). From one Fourier transform, the transforms of the real and imaginary parts can be recovered using conjugate symmetry. This leaves only one forward two-dimensional FFT and one inverse two-dimensional FFT.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O((W-N+1)(H-M+1)NM)) | (O(WH)) | Too slow |
| Optimal | (O(PQ(\log P+\log Q))) | (O(PQ)) | Accepted |

## Algorithm Walkthrough

1. Read the image and template, converting every two-digit hexadecimal pixel to an integer from 0 through 255. Store the large image as (I) and the template as (T). The dimensions are kept in width-first form for the output, while the arrays use row-first indexing.
2. Build a two-dimensional prefix sum of (I^2). For any rectangular image window, the sum of squared image pixels can then be obtained with four prefix-sum accesses. This handles the position-dependent (\sum I^2) term without repeatedly visiting all template pixels.
3. Compute (S_T=\sum T^2) once. This is the same for every possible placement, so there is no reason to recompute it.
4. Choose powers of two (P) and (Q) satisfying (P\ge H+M-1) and (Q\ge W+N-1). These dimensions are large enough to hold the complete linear convolution, rather than a cyclic convolution. Padding is essential because an FFT naturally computes cyclic convolution.
5. Create a (P\times Q) complex array. Put the large image (I) into its real part. Put the template reversed in both dimensions into its imaginary part. If (T') is the reversed template, the stored value is conceptually (I+iT').
6. Apply a two-dimensional FFT. A two-dimensional transform is implemented as one-dimensional FFTs across every row, followed by one-dimensional FFTs down every column. After this operation, use the conjugate-symmetry identities to recover the frequency-domain transforms of (I) and (T').
7. Multiply the recovered transforms pointwise. By the convolution theorem, the inverse transform of this product is the convolution (I*T'). Because (T') is the template reversed in both dimensions, the coefficient at ((y+M-1,x+N-1)) is exactly the correlation (C(x,y)) needed by the SSD formula.
8. Apply the inverse two-dimensional FFT to obtain all correlation values in the spatial domain. Floating-point FFT introduces tiny numerical errors, so each correlation is rounded to the nearest integer before it is used in the exact integer SSD formula.
9. Iterate over all legal template positions. For each ((x,y)), obtain the window sum of (I^2) from the prefix sum, obtain the correlation from the convolution result, and calculate

[
SSD(x,y)=windowSquareSum-2C(x,y)+S_T.
]

Keep the position with the smallest value.

1. Print the best position as `x y`. Scanning positions from top to bottom and left to right is sufficient when several positions have the same SSD, because the statement permits any optimal position.

### Why it works

The prefix sum gives the exact value of the first term in the expanded SSD formula, and (S_T) is exactly the constant third term. Reversing the template converts the remaining cross-correlation into a convolution, whose coefficients are recovered by the FFT computation. Consequently, for every legal position, the algorithm reconstructs exactly the three terms that define its SSD, up to negligible floating-point FFT error that is removed by rounding the integer correlation. Since every legal position is examined and the smallest reconstructed SSD is selected, the returned position is optimal.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def next_pow2(x):
    p = 1
    while p < x:
        p <<= 1
    return p

def make_rev(n):
    rev = [0] * n
    half = n >> 1
    j = 0
    for i in range(1, n):
        bit = half
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        rev[i] = j
    return rev

def make_roots(n):
    forward = {}
    inverse = {}

    length = 2
    while length <= n:
        half = length >> 1
        angle = 2.0 * math.pi / length

        wf = []
        wi = []
        for j in range(half):
            a = angle * j
            c = math.cos(a)
            s = math.sin(a)
            wf.append(complex(c, -s))
            wi.append(complex(c, s))

        forward[length] = wf
        inverse[length] = wi
        length <<= 1

    return forward, inverse

def fft1d(a, invert, rev, roots_forward, roots_inverse):
    n = len(a)

    for i in range(n):
        j = rev[i]
        if i < j:
            a[i], a[j] = a[j], a[i]

    length = 2
    roots = roots_inverse if invert else roots_forward

    while length <= n:
        half = length >> 1
        w = roots[length]

        for base in range(0, n, length):
            for j in range(half):
                u = a[base + j]
                v = a[base + j + half] * w[j]
                a[base + j] = u + v
                a[base + j + half] = u - v

        length <<= 1

    if invert:
        inv_n = 1.0 / n
        for i in range(n):
            a[i] *= inv_n

def fft2(mat, invert, rev_p, rev_q, roots_p_f, roots_p_i,
         roots_q_f, roots_q_i):
    p = len(mat)
    q = len(mat[0])

    for r in range(p):
        fft1d(mat[r], invert, rev_q, roots_q_f, roots_q_i)

    col = [0j] * p
    for c in range(q):
        for r in range(p):
            col[r] = mat[r][c]

        fft1d(col, invert, rev_p, roots_p_f, roots_p_i)

        for r in range(p):
            mat[r][c] = col[r]

def build_prefix_square(img):
    h = len(img)
    w = len(img[0])

    pref = [[0] * (w + 1) for _ in range(h + 1)]

    for r in range(h):
        row_sum = 0
        prev = pref[r]
        cur = pref[r + 1]

        for c in range(w):
            v = img[r][c]
            row_sum += v * v
            cur[c + 1] = prev[c + 1] + row_sum

    return pref

def rect_sum(pref, y1, x1, y2, x2):
    return (
        pref[y2][x2]
        - pref[y1][x2]
        - pref[y2][x1]
        + pref[y1][x1]
    )

def solve():
    first = input().split()
    while not first:
        first = input().split()

    W, H = map(int, first)

    image = []
    for _ in range(H):
        row = input().split()
        while not row:
            row = input().split()
        image.append([int(x, 16) for x in row])

    N, M = map(int, input().split())

    template = []
    for _ in range(M):
        row = input().split()
        while not row:
            row = input().split()
        template.append([int(x, 16) for x in row])

    pref = build_prefix_square(image)

    template_square = 0
    for row in template:
        for v in row:
            template_square += v * v

    P = next_pow2(H + M - 1)
    Q = next_pow2(W + N - 1)

    mat = [[0j] * Q for _ in range(P)]

    for r in range(H):
        dst = mat[r]
        src = image[r]
        for c in range(W):
            dst[c] = complex(src[c], 0.0)

    for r in range(M):
        src = template[r]
        dst = mat[M - 1 - r]
        for c in range(N):
            dst[N - 1 - c] += complex(0.0, src[c])

    rev_p = make_rev(P)
    rev_q = make_rev(Q)

    roots_p_f, roots_p_i = make_roots(P)
    roots_q_f, roots_q_i = make_roots(Q)

    fft2(
        mat,
        False,
        rev_p,
        rev_q,
        roots_p_f,
        roots_p_i,
        roots_q_f,
        roots_q_i,
    )

    # Recover FFT(image) * FFT(reversed_template) from
    # one packed transform FFT(image + i * reversed_template).
    #
    # For Z = A + iB:
    # A_k = (Z_k + conj(Z_-k)) / 2
    # B_k = (Z_k - conj(Z_-k)) / (2i)
    #
    # Process conjugate-frequency pairs together so that the
    # original spectrum is never overwritten before it is needed.

    for r in range(P):
        rr = (-r) % P

        for c in range(Q):
            cc = (-c) % Q

            idx = r * Q + c
            ridx = rr * Q + cc

            if idx > ridx:
                continue

            z = mat[r][c]
            zn = mat[rr][cc].conjugate()

            a = (z + zn) * 0.5
            b = (z - zn) * (-0.5j)

            product = a * b

            mat[r][c] = product

            if idx != ridx:
                mat[rr][cc] = product.conjugate()

    fft2(
        mat,
        True,
        rev_p,
        rev_q,
        roots_p_f,
        roots_p_i,
        roots_q_f,
        roots_q_i,
    )

    best_x = 0
    best_y = 0
    best = None

    for y in range(H - M + 1):
        for x in range(W - N + 1):
            window_square = rect_sum(
                pref,
                y,
                x,
                y + M,
                x + N,
            )

            corr = int(round(mat[y + M - 1][x + N - 1].real))

            ssd = window_square - 2 * corr + template_square

            if best is None or ssd < best:
                best = ssd
                best_x = x
                best_y = y

    return f"{best_x} {best_y}"

if __name__ == "__main__":
    print(solve())
```

The input phase converts every hexadecimal token with `int(token, 16)`. This is preferable to manually handling digits and letters, and it also accepts either uppercase or lowercase hexadecimal.

The prefix construction stores one extra row and column. A rectangle with half-open boundaries `[y1, y2) x [x1, x2)` is then recovered with four accesses. Using half-open coordinates avoids special cases at the first row and column.

The FFT dimensions are based on the full convolution size, not merely the original image size. If the padding were too small, the FFT would compute a cyclic convolution and values from one side of the array would wrap around to the other side.

The template is placed at reversed coordinates because convolution uses the kernel in its original direction while correlation requires the kernel to be reversed. The coefficient at row `y + M - 1` and column `x + N - 1` consequently corresponds to the template placed at `(x, y)`.

The packed FFT section is the most delicate part of the implementation. If `Z` is the transform of `A+iB`, then the transform of `A` can be recovered from `Z[k]` and the conjugate of `Z[-k]`. The same pair gives the transform of `B`. Processing both frequency positions together prevents one transformed value from being overwritten before its conjugate partner has been read.

Python's integers do not overflow, so the final SSD expression is safe even though its maximum value is around (255^2\cdot786432), which is more than (2^{32}). The FFT itself uses floating-point complex numbers, but the desired correlation is an integer. Rounding the final real coefficient recovers that integer accurately for the given value range.

## Worked Examples

### Sample 1

The image is

```
00 FF 12
AA BB 34
```

and the template is

```
FF 11
```

There are two possible horizontal positions and only one vertical position.

| x | y | Window | Correlation | Window (\sum I^2) | SSD | Best so far |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | `00 FF` | (0\cdot255+255\cdot17) | (0^2+255^2) | 121669 | `(0,0)` |
| 1 | 0 | `FF 12` | (255\cdot255+18\cdot17) | (255^2+18^2) | 1 | `(1,0)` |

At `(1,0)`, the first pixel matches exactly and the second differs by only one, so the SSD is (1). The algorithm obtains the same correlation from the convolution and selects `1 0`, matching the sample.

### Sample 2

There are six legal positions because the image is (4\times5) and the template is (3\times3).

| x | y | SSD | Best so far |
| --- | --- | --- | --- |
| 0 | 0 | 82038 | `(0,0)` |
| 1 | 0 | 72104 | `(1,0)` |
| 0 | 1 | 85314 | `(1,0)` |
| 1 | 1 | 88380 | `(1,0)` |
| 0 | 2 | 83249 | `(1,0)` |
| 1 | 2 | 105273 | `(1,0)` |

The smallest score is at `(1,0)`. This example demonstrates why maximizing the correlation alone would not be a valid replacement for minimizing SSD. The (\sum I^2) term changes between windows, so both the window energy and the correlation must be included.

## Complexity Analysis

Let

[
P=2^{\lceil\log_2(H+M-1)\rceil}
]

and

[
Q=2^{\lceil\log_2(W+N-1)\rceil}.
]

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(PQ(\log P+\log Q)+WH+NM)) | Two-dimensional FFT plus prefix-sum and input processing |
| Space | (O(PQ+WH)) | Padded complex FFT array and image prefix sums |

With the maximum dimensions, both padded dimensions are at most 2048, so (P Q\le 2048^2). The intended solution fits comfortably in the generous 1024 MB memory limit, while the FFT reduces the correlation computation from billions of direct pixel multiplications to frequency-domain transforms. The published problem gives a 4 second limit, so the implementation needs an iterative FFT rather than a recursive one and benefits substantially from packing the two real inputs into one complex transform.

## Test Cases

The test harness below assumes the `solve()` function from the solution is available. The maximum-size case is generated programmatically instead of embedding hundreds of thousands of input pixels.

```python
# helper: run solution on input string, return output string
import sys
import io

# Assume solve() is imported from the submitted solution.

def run(inp: str) -> str:
    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(inp)
        return solve().strip()
    finally:
        sys.stdin = old_stdin

# Sample 1
sample1 = """\
3 2
00 FF 12
AA BB 34
2 1
FF 11
"""
assert run(sample1) == "1 0", "sample 1"

# Sample 2
sample2 = """\
4 5
89 4E 72 C6
C7 E9 EA 8F
6E B1 FD E4
7C 22 6C D0
93 FB DB E5
3 3
79 C0 51
B9 98 37
BB 64 7F
"""
assert run(sample2) == "1 0", "sample 2"

# Minimum-size input.
minimum = """\
1 1
00
1 1
00
"""
assert run(minimum) == "0 0", "minimum size"

# All positions have the same SSD.
all_equal = """\
3 2
07 07 07
07 07 07
2 1
07 07
"""
assert run(all_equal) == "0 0", "all equal values"

# The unique optimum is the bottom-right position.
bottom_right = """\
3 3
00 00 00
00 00 00
00 00 2A
1 1
2A
"""
assert run(bottom_right) == "2 2", "bottom-right boundary"

# Maximum-size dimensions, all zeros.
# Every position is optimal, and the scan should return 0 0.
W, H = 1024, 768
N, M = 1024, 768

image_rows = "\n".join(
    " ".join(["00"] * W)
    for _ in range(H)
)
template_rows = "\n".join(
    " ".join(["00"] * N)
    for _ in range(M)
)

maximum = (
    f"{W} {H}\n"
    f"{image_rows}\n"
    f"{N} {M}\n"
    f"{template_rows}\n"
)

assert run(maximum) == "0 0", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 00 / 1 1 / 00` | `0 0` | Minimum dimensions and the single legal position |
| A `3 x 2` image filled with `07`, with a `2 x 1` template filled with `07` | `0 0` | Multiple optimal positions and zero SSD |
| A `3 x 3` image with only the bottom-right pixel equal to `2A`, with a `1 x 1` template `2A` | `2 2` | Inclusive right and bottom boundaries |
| `1024 x 768` all-zero image and equally sized all-zero template | `0 0` | Maximum dimensions, memory usage, and large padding |
| Sample 1 | `1 0` | Hexadecimal parsing and a unique optimum |
| Sample 2 | `1 0` | General two-dimensional matching |

## Edge Cases

When the template is the same size as the image, the FFT still works, but there is only one candidate. For

```
1 1
7
1 1
7
```

the padded convolution contains the required correlation at `(0,0)`, the prefix sum gives (7^2), the template square sum gives (7^2), and the SSD becomes zero. The scan has exactly one iteration and prints `0 0`.

For a one-pixel template, the correlation reduces to the product of the template pixel and each image pixel. For

```
3 1
10 20 30
1 1
1E
```

the template value is hexadecimal `1E`, or 30. The three SSD values are (400), (100), and (0), so the algorithm prints `2 0`. No special one-dimensional case is needed because the same convolution formula handles it.

For an all-equal image and template, every legal position can have the same score. With

```
3 2
07 07 07
07 07 07
2 1
07 07
```

the correlation and window-square terms are identical for every position, giving SSD zero everywhere. Since the scan starts at `(0,0)` and only replaces the answer when it finds a strictly smaller score, it prints `0 0`, which is a valid optimum.

For the bottom-right boundary,

```
3 3
00 00 00
00 00 00
00 00 2A
1 1
2A
```

the legal coordinates are `0..2` in both dimensions. The unique zero-SSD position is `(2,2)`. The convolution coefficient used by the algorithm is at row `2 + 1 - 1 = 2` and column `2 + 1 - 1 = 2`, so the boundary position is included exactly once.

For hexadecimal input, values such as `0A`, `FF`, and `e7` must all be accepted. Python's `int(token, 16)` handles all of them, so the algorithm does not need separate parsing logic for digits and letters.

For the maximum dimensions, the image and template can both be (1024\times768). The convolution requires dimensions up to (2047\times1535), which are rounded to (2048\times2048) for the FFT. The implementation deliberately allocates the padded transform at those dimensions rather than attempting to process only the original image area, because insufficient zero padding would turn the required linear convolution into a cyclic one and corrupt the correlation values near the boundaries.
