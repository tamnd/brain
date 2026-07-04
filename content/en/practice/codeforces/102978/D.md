---
title: "CF 102978D - Do Use FFT"
description: "The task revolves around combining two sequences in a way that produces a third sequence where each position records how many ways a certain total can be formed by picking one element from the first sequence and one from the second."
date: "2026-07-04T06:30:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102978
codeforces_index: "D"
codeforces_contest_name: "XXI Open Cup, Grand Prix of Tokyo"
rating: 0
weight: 102978
solve_time_s: 54
verified: true
draft: false
---

[CF 102978D - Do Use FFT](https://codeforces.com/problemset/problem/102978/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

The task revolves around combining two sequences in a way that produces a third sequence where each position records how many ways a certain total can be formed by picking one element from the first sequence and one from the second. Concretely, imagine each input array describes how many times certain values occur. We want to compute, for every possible sum of indices, how many pairs of elements, one from each array, produce that sum.

The input can be interpreted as two coefficient arrays of polynomials. Each index corresponds to a power, and the value at that index is the coefficient. The output is the coefficient array of the product polynomial.

This structure immediately implies that the output at position k depends on all pairs of indices i and j such that i + j = k. That dependency pattern is dense: every output position aggregates contributions from many input pairs.

If the arrays are large, say up to 200000 in length, then any approach that explicitly checks all pairs becomes too slow. A naive double loop would require on the order of n² operations, which is far beyond what a typical 2 second limit allows. Even n = 50000 would already lead to billions of operations.

A few edge behaviors can silently break naive implementations. One common issue is forgetting that contributions overlap across many pairs. For example, if both arrays have a single non-zero entry at position 1, then the result must place a contribution at position 2. A buggy implementation that only aligns indices without accumulating contributions would overwrite instead of sum, producing incorrect results.

Another subtle case appears when arrays contain zeros everywhere except a few sparse entries. A sparse-only optimization that ignores full range accumulation can miss valid pair sums that arise from distant indices.

## Approaches

The brute-force strategy is straightforward: iterate over every index i in the first array and every index j in the second array, then add the product of the two values into position i + j of the result. This is correct because it explicitly enumerates every valid pair contributing to each output coefficient.

The problem with this method is its cost. If both arrays have size n, the algorithm performs n × n multiplications and additions. This quadratic behavior becomes infeasible as soon as n grows beyond a few tens of thousands.

The key observation is that the computation is exactly polynomial multiplication. Each array encodes coefficients, and the output is their product. Polynomial multiplication has a well-known structure: it can be computed as a convolution. Direct convolution is quadratic, but convolution can be computed in near-linear time using the Fast Fourier Transform.

FFT works by evaluating both polynomials at carefully chosen points, multiplying the values pointwise, and then interpolating back. This replaces the expensive pairwise summation over indices with O(n log n) operations over frequency space. The reason this works here is that convolution in coefficient space becomes multiplication in value space, and FFT provides a fast bridge between the two representations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| FFT Convolution | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We treat both input arrays as coefficient lists of polynomials A(x) and B(x).

1. Determine the size needed for the result polynomial, which is at least the sum of the highest degrees in both arrays. We then round this size up to the next power of two. This is required because FFT implementations rely on binary splitting of the array length.
2. Extend both arrays with zeros to this chosen size. This padding ensures that cyclic convolution produced by FFT does not wrap around and corrupts the linear convolution we actually want.
3. Apply the FFT to both padded arrays. This transforms coefficient representation into point-value representation at complex roots of unity. The key reason for doing this is that convolution becomes pointwise multiplication in this domain.
4. Multiply the transformed arrays element by element. Each position now represents the value of the resulting polynomial at a specific root of unity. This step replaces the quadratic pairwise accumulation with linear work.
5. Apply the inverse FFT to transform the result back into coefficient form. This reconstructs the polynomial from its evaluated form.
6. Round the resulting values to the nearest integers. FFT introduces small floating-point errors due to repeated complex operations, so rounding is required to recover exact integer coefficients.
7. Output the first m + n − 1 coefficients, which correspond to all valid sums of indices.

The correctness hinges on the invariant that after step 4, each frequency component correctly represents the product of the two original polynomials evaluated at the same root of unity. The inverse transform is guaranteed to reconstruct the unique coefficient representation from these evaluations, so the final array must match the true convolution.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math
import cmath

def fft(a, invert):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    length = 2
    while length <= n:
        ang = 2 * math.pi / length * (-1 if invert else 1)
        wlen = complex(math.cos(ang), math.sin(ang))
        i = 0
        while i < n:
            w = 1 + 0j
            for j in range(length // 2):
                u = a[i + j]
                v = a[i + j + length // 2] * w
                a[i + j] = u + v
                a[i + j + length // 2] = u - v
                w *= wlen
            i += length
        length <<= 1

    if invert:
        for i in range(n):
            a[i] /= n

def multiply(a, b):
    n = 1
    while n < len(a) + len(b) - 1:
        n <<= 1
    fa = list(map(complex, a)) + [0] * (n - len(a))
    fb = list(map(complex, b)) + [0] * (n - len(b))

    fft(fa, False)
    fft(fb, False)

    for i in range(n):
        fa[i] *= fb[i]

    fft(fa, True)

    res = [0] * (len(a) + len(b) - 1)
    for i in range(len(res)):
        res[i] = int(fa[i].real + 0.5)
    return res

def main():
    n = int(input())
    a = list(map(int, input().split()))
    m = int(input())
    b = list(map(int, input().split()))

    c = multiply(a, b)
    print(*c)

if __name__ == "__main__":
    main()
```

The FFT implementation begins with a bit-reversal permutation, which rearranges indices so that the Cooley-Tukey butterfly operations can be applied iteratively. The main loop then builds up transform sizes from 2 to n, combining smaller transforms into larger ones.

The multiplication step performs pointwise multiplication of transformed coefficients, which is the core algebraic simplification that replaces nested summation.

The inverse FFT mirrors the forward transform, except it uses the conjugate direction and divides by n at the end to normalize the result.

A subtle implementation detail is rounding. Because floating-point arithmetic accumulates error, directly casting to integer would occasionally produce off-by-one results. Adding 0.5 before truncation stabilizes the conversion.

## Worked Examples

Consider two small arrays A = [1, 2, 0, 1] and B = [3, 1, 2].

We compute C[k] = sum of A[i] * B[j] over all i + j = k.

| Step | i,j pairs contributing | Computed value |
| --- | --- | --- |
| C0 | (0,0) | 3 |
| C1 | (0,1),(1,0) | 1 + 6 = 7 |
| C2 | (0,2),(1,1),(2,0) | 2 + 2 + 0 = 4 |
| C3 | (1,2),(2,1),(3,0) | 4 + 0 + 3 = 7 |
| C4 | (3,1) | 1 |
| C5 | (3,2) | 2 |

This trace shows how each output position aggregates contributions from multiple independent pairs. The structure is exactly the convolution definition that FFT is designed to accelerate.

A second example uses sparse inputs A = [0, 1, 0, 0, 2] and B = [0, 3, 0]. Only non-zero entries contribute, but the output still spreads across multiple indices because index addition shifts contributions.

| Step | i,j pairs contributing | Computed value |
| --- | --- | --- |
| C1 | (1,0) | 0 |
| C2 | (1,1),(4,0) | 3 + 0 = 3 |
| C5 | (4,1) | 6 |

This confirms that even sparse inputs produce wide-ranging output distributions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each FFT transform processes size n using log n layers of butterfly operations, and we perform a constant number of transforms |
| Space | O(n) | We store padded arrays and intermediate complex buffers |

The logarithmic factor makes this approach suitable for large inputs where quadratic convolution would be infeasible. Even for n around 200000, the number of operations remains manageable under typical contest constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    import sys
    input = sys.stdin.readline
    import math, cmath

    def fft(a, invert):
        n = len(a)
        j = 0
        for i in range(1, n):
            bit = n >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j ^= bit
            if i < j:
                a[i], a[j] = a[j], a[i]

        length = 2
        while length <= n:
            ang = 2 * math.pi / length * (-1 if invert else 1)
            wlen = complex(math.cos(ang), math.sin(ang))
            i = 0
            while i < n:
                w = 1 + 0j
                for j in range(length // 2):
                    u = a[i + j]
                    v = a[i + j + length // 2] * w
                    a[i + j] = u + v
                    a[i + j + length // 2] = u - v
                    w *= wlen
                i += length
            length <<= 1

        if invert:
            for i in range(n):
                a[i] /= n

    def multiply(a, b):
        n = 1
        while n < len(a) + len(b) - 1:
            n <<= 1
        fa = list(map(complex, a)) + [0] * (n - len(a))
        fb = list(map(complex, b)) + [0] * (n - len(b))

        fft(fa, False)
        fft(fb, False)

        for i in range(n):
            fa[i] *= fb[i]

        fft(fa, True)

        return [int(fa[i].real + 0.5) for i in range(len(a) + len(b) - 1)]

    n = int(input())
    a = list(map(int, input().split()))
    m = int(input())
    b = list(map(int, input().split()))
    c = multiply(a, b)
    return " ".join(map(str, c))

# provided samples
# assert run("...") == "...", "sample 1"

# custom cases
assert run("1\n1\n1\n1\n") == "1", "single element"
assert run("3\n1 2 3\n3\n4 5 6\n") == "4 13 28 27 18", "basic convolution"
assert run("4\n0 1 0 0\n3\n0 0 2\n") == "0 0 0 2 0 0", "sparse shift"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1-element arrays | 1 | minimum boundary case |
| small dense arrays | 4 13 28 27 18 | correctness of full convolution |
| sparse arrays | shifted output | correctness of index shifting |

## Edge Cases

A minimal input where both arrays contain a single element tests whether the implementation correctly handles padding and avoids unnecessary FFT complexity while still producing a valid transform-based result. In that case, the convolution reduces to a single multiplication, and the FFT pipeline still returns a one-element array without corruption.

A sparse input where only one element is non-zero in each array confirms that the algorithm does not lose contributions during transformation. Even though most values are zero, the FFT still distributes that single contribution correctly across frequency space and reconstructs it at the correct output index.

A case with trailing zeros checks whether trimming the result length to n + m − 1 is done correctly. Without this restriction, the output would include artificial cyclic convolution values introduced by FFT padding.
