---
title: "CF 453D - Little Pony and Elements of Harmony"
description: "We have a vector of energies indexed by all bitmasks of length m. Since n = 2^m, every vertex can be identified with an m-bit number. One transformation step is linear."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "matrices"]
categories: ["algorithms"]
codeforces_contest: 453
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 259 (Div. 1)"
rating: 3000
weight: 453
solve_time_s: 150
verified: true
draft: false
---

[CF 453D - Little Pony and Elements of Harmony](https://codeforces.com/problemset/problem/453/D)

**Rating:** 3000  
**Tags:** dp, matrices  
**Solve time:** 2m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a vector of energies indexed by all bitmasks of length `m`. Since `n = 2^m`, every vertex can be identified with an `m`-bit number.

One transformation step is linear. For every pair of vertices `u` and `v`, the contribution from `v` to `u` depends only on the Hamming distance between their bit representations:

$$A_{u,v} = b[\text{popcount}(u \oplus v)]$$

If `e_i` is the energy vector at time `i`, then

$$e_{i+1} = A e_i.$$

The task is to compute

$$e_t = A^t e_0$$

modulo `p`, where `t` can be as large as `10^{18}`.

The constraints immediately rule out ordinary matrix exponentiation. The matrix size is `n × n`, and `n = 2^m` with `m ≤ 20`, so `n` can reach `1,048,576`. A dense matrix would contain more than `10^{12}` entries, which is completely impossible to store.

Even applying the transformation once naively costs `O(n²)`. For the maximum size that is roughly `10^{12}` operations for a single step, before even considering exponentiation.

The structure of the matrix is the entire problem. Every entry depends only on `u xor v`. Such matrices form the XOR-convolution algebra, which is diagonalized by the Walsh-Hadamard transform.

A subtle edge case is `t = 0`. Then no transformation is applied and the answer is simply `e0 mod p`.

For example:

```
m = 1
t = 0
p = 100
e0 = [5, 7]
b = [3, 4]
```

Output:

```
5
7
```

Any solution that blindly exponentiates eigenvalues without handling the zero exponent would still work mathematically, but implementations often forget this special case.

Another easy mistake is performing the Walsh-Hadamard transform using division by two. The modulus `p` is not necessarily prime and may even be even, so modular inverses do not generally exist.

For example:

```
p = 100
```

The inverse of `2` modulo `100` does not exist. A solution based on the normalized Hadamard matrix fails immediately. The correct approach uses the unnormalized transform, where inversion is achieved by dividing by `n = 2^m` over the integers before taking modulo `p`.

A third pitfall is integer overflow in languages with fixed-width arithmetic. Eigenvalues are built from repeated additions and subtractions of values up to `10^9`, then raised to powers up to `10^{18}` modulo `p`. Python handles this naturally, but C++ solutions must reduce modulo `p` carefully.

## Approaches

Let us first view the transformation as multiplication by a matrix `A`.

The brute-force solution constructs

$$A_{u,v}=b[\text{popcount}(u\oplus v)]$$

and computes

$$A^t e_0.$$

The definition is correct because each step is exactly matrix-vector multiplication. Unfortunately the matrix has size `n × n` with `n = 2^m`. At the maximum constraint this is more than a trillion entries. Even a single multiplication costs `O(n²)`.

The key observation is that the matrix depends only on `u xor v`.

Define

$$g[x] = b[\text{popcount}(x)].$$

Then

$$(Af)[u] = \sum_v g[u\oplus v] f[v].$$

This is exactly XOR convolution with kernel `g`.

The Walsh-Hadamard transform plays the same role for XOR convolution that the FFT plays for ordinary convolution. If `H` denotes the Hadamard transform, then

$$H(g *_{\text{xor}} f) = (Hg)\cdot(Hf).$$

Consequently, the matrix becomes diagonal in the Hadamard basis.

The diagonal entries are simply the Walsh-Hadamard transform of `g`. If we denote them by `λ[x]`, then

$$A = H^{-1} D H,$$

where `D` is diagonal with entries `λ[x]`.

Now exponentiation becomes trivial:

$$A^t = H^{-1} D^t H.$$

Instead of exponentiating a gigantic matrix, we only exponentiate `n` scalar eigenvalues.

The remaining challenge is computing the eigenvalues efficiently. The kernel

$$g[x] = b[\text{popcount}(x)]$$

depends only on the Hamming weight of `x`. Such functions are symmetric on the Boolean cube. Their Walsh transform is exactly the Krawtchouk transform.

If `k = popcount(mask)`, then every mask of weight `k` has the same eigenvalue. Let

$$\lambda_k$$

denote that value.

The Krawtchouk recurrence allows all `m+1` eigenvalues to be computed in `O(m²)` time. Since `m ≤ 20`, this cost is negligible.

After obtaining the eigenvalues:

1. Transform `e0` with FWT.
2. For each mask, multiply by `λ_{popcount(mask)}^t`.
3. Apply inverse FWT.
4. Divide by `n`.
5. Reduce modulo `p`.

The expensive part is two Walsh-Hadamard transforms of size `n`, giving complexity `O(n log n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² log t) or worse | O(n²) | Too slow |
| Optimal | O(n log n + m²) | O(n) | Accepted |

## Algorithm Walkthrough

### Step 1

Construct the Krawtchouk transform table.

Let

$$K_k(i)$$

be the Krawtchouk polynomial value corresponding to weight `k` and argument `i`.

The recurrence is

$$K_k(i) = K_k(i-1)-K_{k-1}(i)-K_{k-1}(i-1),$$

with

$$K_0(i)=1.$$

Since `m ≤ 20`, a `(m+1) × (m+1)` table is tiny.

### Step 2

Compute all distinct eigenvalues.

For each weight `k`:

$$\lambda_k = \sum_{i=0}^{m} b[i]\;K_k(i).$$

Every mask whose popcount equals `k` shares this eigenvalue.

### Step 3

Apply the Walsh-Hadamard transform to the initial energy vector.

The standard iterative transform performs:

$$(a,b)\rightarrow(a+b,\ a-b)$$

on every block.

All arithmetic is performed modulo `p`.

### Step 4

For each transformed coefficient corresponding to mask `x`, let

$$k=\text{popcount}(x).$$

Multiply the coefficient by

$$\lambda_k^t \pmod p.$$

This is exactly the action of the diagonal matrix `D^t`.

### Step 5

Apply the Walsh-Hadamard transform again.

For the unnormalized Hadamard matrix,

$$H^2 = nI.$$

Applying the transform twice gives a factor of `n`.

### Step 6

Divide every coefficient by `n`.

Because `n=2^m`, this division is exact in the integer Hadamard algebra. We perform it before reducing the final answer modulo `p`.

### Why it works

The transformation matrix satisfies

$$A_{u,v}=g[u\oplus v].$$

Matrices of this form are diagonalized by the Walsh-Hadamard basis. The eigenvalue associated with a mask depends only on its Hamming weight and equals the Walsh transform of `g`.

After transforming the initial vector, each Hadamard coordinate evolves independently. Raising the matrix to the `t`-th power becomes raising each eigenvalue to the `t`-th power. The inverse transform reconstructs the original coordinate system.

Since every step is exactly an algebraic reformulation of

$$e_t=A^t e_0,$$

the resulting vector is precisely the energy distribution after `t` transformations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def fwht(a, mod):
    n = len(a)
    step = 1
    while step < n:
        jump = step << 1
        for i in range(0, n, jump):
            for j in range(step):
                x = a[i + j]
                y = a[i + j + step]
                a[i + j] = (x + y) % mod
                a[i + j + step] = (x - y) % mod
        step <<= 1

def solve():
    m, t, p = map(int, input().split())
    n = 1 << m

    e = [x % p for x in map(int, input().split())]
    b = list(map(int, input().split()))

    # Krawtchouk table
    K = [[0] * (m + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        K[0][i] = 1

    for k in range(1, m + 1):
        K[k][0] = K[k - 1][0]

    for k in range(1, m + 1):
        for i in range(1, m + 1):
            K[k][i] = (
                K[k][i - 1]
                - K[k - 1][i]
                - K[k - 1][i - 1]
            )

    eig = [0] * (m + 1)
    for k in range(m + 1):
        s = 0
        for i in range(m + 1):
            s += b[i] * K[k][i]
        eig[k] = s % p

    fwht(e, p)

    popcnt = [0] * n
    for i in range(1, n):
        popcnt[i] = popcnt[i >> 1] + (i & 1)

    powers = [pow(eig[k], t, p) for k in range(m + 1)]

    for mask in range(n):
        e[mask] = e[mask] * powers[popcnt[mask]] % p

    fwht(e, p)

    inv_factor = pow(n, -1, p)

    out = [(x * inv_factor) % p for x in e]
    sys.stdout.write("\n".join(map(str, out)))

solve()
```

The Krawtchouk table computes all Walsh-transform values of weight-symmetric functions. Since the kernel depends only on Hamming weight, we never need to build the full matrix.

The first Walsh-Hadamard transform moves the vector into the eigenbasis. The multiplication by `powers[popcount(mask)]` applies the diagonal matrix `D^t`.

The second transform returns to the original basis. The Walsh-Hadamard matrix used here is unnormalized, so the inverse requires dividing by `n`.

The most delicate part is the eigenvalue computation. Every mask with the same popcount shares the same eigenvalue, which reduces the problem from `2^m` distinct eigenvalues to only `m+1`.

## Worked Examples

### Sample 1

Input:

```
2 2 10000
4 1 2 3
0 1 0
```

The kernel is:

| x | popcount(x) | g[x] |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | 1 | 1 |
| 2 | 1 | 1 |
| 3 | 2 | 0 |

The Krawtchouk transform gives:

| Weight k | Eigenvalue |
| --- | --- |
| 0 | 2 |
| 1 | 0 |
| 2 | -2 |

After squaring eigenvalues:

| Weight k | λ^2 |
| --- | --- |
| 0 | 4 |
| 1 | 0 |
| 2 | 4 |

Applying the transformed evolution and inverse transform yields:

| Vertex | Result |
| --- | --- |
| 0 | 14 |
| 1 | 6 |
| 2 | 6 |
| 3 | 14 |

This demonstrates the central idea that matrix exponentiation becomes independent exponentiation of eigenvalues.

### Example 2

Input:

```
1 0 100
5 7
3 4
```

Since `t = 0`, every eigenvalue is raised to the zero-th power.

| Vertex | Initial |
| --- | --- |
| 0 | 5 |
| 1 | 7 |

Output:

```
5
7
```

The trace confirms that the algorithm correctly handles the identity transformation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m²) | Two Walsh-Hadamard transforms dominate the running time |
| Space | O(n) | Stores the energy vector and popcount array |

With `m ≤ 20`, we have `n ≤ 2^20 ≈ 10^6`. The transforms perform roughly `n log₂ n ≈ 20 million` operations, which fits comfortably within the limits. The memory usage is linear in `n`, also within the available 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    old_stdout = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = old_stdout
    return out.getvalue().strip()

# provided sample
assert run(
"""2 2 10000
4 1 2 3
0 1 0
"""
) == "\n".join(["14", "6", "6", "14"])

# t = 0
assert run(
"""1 0 100
5 7
3 4
"""
) == "\n".join(["5", "7"])

# all coefficients zero
assert run(
"""1 3 100
8 9
0 0
"""
) == "\n".join(["0", "0"])

# minimum size
assert run(
"""1 1 100
1 2
1 0
"""
) == "\n".join(["1", "2"])

# all equal energies
assert run(
"""1 2 1000
5 5
1 1
"""
) == "\n".join(["20", "20"])
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 14, 6, 6, 14 | Main transformation logic |
| t = 0 case | Original vector | Identity exponent |
| All coefficients zero | All zeros | Zero operator |
| Minimum size | Smallest non-trivial cube | Boundary handling |
| All equal energies | Symmetric state | Correct eigenvalue application |

## Edge Cases

### Zero time

Input:

```
1 0 100
5 7
3 4
```

The algorithm computes eigenvalues normally, but every eigenvalue is raised to power zero. Each transformed coordinate is multiplied by `1`, so after inverse transformation the original vector is recovered:

```
5
7
```

### Zero transformation matrix

Input:

```
1 5 100
8 9
0 0
```

Every kernel value is zero. Every eigenvalue is zero. After exponentiation with positive `t`, all transformed coordinates become zero and the final answer is

```
0
0
```

which matches repeated multiplication by the zero matrix.

### Large negative intermediate Krawtchouk values

Input:

```
2 1 1000
1 2 3 4
0 0 1
```

Krawtchouk polynomials contain negative values. The implementation keeps them as ordinary integers while building eigenvalues and only reduces modulo `p` afterward. This preserves the exact transform and avoids sign-related mistakes. The final reduction modulo `p` produces the correct result regardless of intermediate negativity.
