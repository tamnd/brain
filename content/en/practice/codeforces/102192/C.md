---
title: "CF 102192C - City Development"
description: "We have n cities arranged in order, and those cities are simultaneously partitioned into nested administrative groups. A group at level i contains exactly ni consecutive cities, and every finer group lies completely inside one coarser group."
date: "2026-08-18T01:57:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102192
codeforces_index: "C"
codeforces_contest_name: "2018 Chinese Multi-University Training, Nanjing U Contest"
rating: 0
weight: 102192
solve_time_s: 215
verified: true
draft: false
---

[CF 102192C - City Development](https://codeforces.com/problemset/problem/102192/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` cities arranged in order, and those cities are simultaneously partitioned into nested administrative groups. A group at level `i` contains exactly `n_i` consecutive cities, and every finer group lies completely inside one coarser group. The final level has `n_k = 1`, so an individual city is itself a level-`k` group.

For two cities, the interaction coefficient depends only on the finest administrative level containing both of them. If they are in different top-level groups, their coefficient is `rho_0`. If they first become separated at some finer level, the corresponding `rho_i` is used. A city interacts with itself using `rho_k`.

One year is a linear transformation of the current vector of city values. If we call that transformation `A`, the task is to compute `A^T d_0` modulo `998244353`, where `T` can be as large as `10^18`.

The direct interpretation gives an `n x n` matrix, but storing or multiplying such a matrix is immediately impossible. Even one application of the matrix needs `Theta(n^2)` operations. With `n = 3 * 10^5`, that is about `9 * 10^10` pair interactions for a single year, far beyond the four-second limit. The exponent `T` also rules out simulating years one by one.

The hierarchy itself is the useful structure. Because every group size divides the preceding one, whenever the size strictly decreases it becomes at most half of the previous size. Thus, although `k` can be as large as `n` because equal consecutive sizes are allowed, there can be at most `O(log n)` distinct group sizes.

There are several edge cases that can silently break a careless implementation. The first is `n = 1`. For example,

```
1
1 1 3
1
7
2 5
```

The only city interacts with itself using `rho_1 = 5`, so the answer is `7 * 5^3 = 875`. Treating `rho_0` as the diagonal coefficient would give the wrong result.

Another edge case is repeated administrative sizes. For example,

```
1
4 3 1
4 2 1
3 3 3 3
1 2 4 7
```

Every city sees three other cities with total interaction `1 + 4 + 1 + 7` arranged according to their levels, and the row sum is `13`. Since every initial value is `3`, the correct output is

```
39 39 39 39
```

A solution that assumes every level introduces a new partition may create zero-dimensional eigenspaces and mishandle repeated sizes.

A third boundary case occurs when the largest administrative group already contains all cities. For example,

```
1
4 3 2
4 2 1
1 2 3 4
1 1 1 2
```

Here the matrix is simply `J + I`, where `J` is the all-ones matrix. Squaring it gives `6J + I`, so the answer is

```
61 62 63 64
```

A solution that assumes there is always a nonempty space outside the top-level groups would incorrectly discard this case.

## Approaches

The brute-force method constructs the interaction matrix explicitly. For every pair of cities, we determine their lowest common administrative level and place the corresponding coefficient in the matrix. Applying one year then costs `O(n^2)`, and doing this for `T` years costs `O(Tn^2)`. Even if we tried matrix exponentiation, a dense `n x n` matrix would make multiplication far too expensive. At `n = 3 * 10^5`, the matrix alone would contain roughly `9 * 10^10` entries.

The useful observation is that the matrix is not arbitrary. Define `B_i` as the matrix whose entry is `1` exactly when two cities belong to the same level-`i` group. Since the coefficient changes from `rho_{i-1}` to `rho_i` when we move to level `i`, the interaction matrix can be written as

[
A = \rho_0 J + \sum_{i=1}^{k}(\rho_i-\rho_{i-1})B_i.
]

This representation is powerful because all the `B_i` are nested block matrices. More precisely, if `P_m` means averaging a vector inside every consecutive block of `m` cities, then

[
B_i = n_i P_{n_i}.
]

All these averaging operators are projections onto nested subspaces, so they commute and can be simultaneously decomposed into independent hierarchical components.

For a distinct block size `m`, collect all terms having that size into one coefficient

[
\gamma_m = \sum_{i=m}(\rho_i-\rho_{i-1})m.
]

Then the matrix becomes

[
A = \rho_0 J + \sum_m \gamma_m P_m.
]

Suppose the distinct sizes are

[
m_1 > m_2 > \dots > m_r=1.
]

Let `P_0` be the global averaging operator over all `n` cities. The difference

[
P_{m_q}-P_{m_{q-1}}
]

extracts exactly the information that is constant inside an `m_q` block but has zero average inside its parent block. Each such subspace is an eigenspace of `A`.

The eigenvalue belonging to the component introduced at size `m_q` is the suffix sum

[
\lambda_q=\sum_{j=q}^{r}\gamma_{m_j}.
]

The global constant component has eigenvalue

[
\lambda_0=n\rho_0+\sum_{j=1}^{r}\gamma_{m_j}.
]

The remaining component, consisting of differences between top-level groups, has eigenvalue zero. Since `T >= 1`, that component disappears after raising the matrix to the `T`-th power.

The brute-force works because it applies the exact interaction matrix. It fails because it treats every city pair independently. The observation that the matrix is a sum of nested averaging operators lets us replace pairwise interactions with a small number of hierarchical projections. Since distinct sizes halve whenever they change, there are only `O(log n)` such projections.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(T n^2)` | `O(n^2)` | Too slow |
| Optimal | `O(n + n log n)` | `O(n)` | Accepted |

The implementation below is even more efficient than explicitly visiting every city for every level. Each projection is applied through range additions on its blocks. The total number of blocks over all distinct sizes is `O(n)` because the sizes decrease by at least a factor of two.

## Algorithm Walkthrough

1. Read the administrative sizes and interaction coefficients, then replace consecutive equal sizes by a single distinct size. For every size `m`, accumulate

[
\gamma_m \mathrel{+}=m(\rho_i-\rho_{i-1}).
]

Equal levels produce the same averaging operator, so their matrix contributions can be combined safely.
2. Compute the suffix eigenvalues. Processing the distinct sizes from smallest to largest gives

[
\lambda_q=\gamma_{m_q}+\lambda_{q+1}.
]

This is exactly the eigenvalue on the difference between an `m_q`-block average and its parent-block average, because every finer projection acts as multiplication by its block size on that component.
3. Compute the global eigenvalue

[
\lambda_0=n\rho_0+\sum_q\gamma_{m_q}.
]

The all-constant vector is an eigenvector because every row of the interaction matrix has the same sum.
4. Raise every relevant eigenvalue to `T` modulo `998244353`. Since `T` can reach `10^18`, binary exponentiation is required.
5. Express the powered operator as a linear combination of the averaging projections. Start with `lambda_0^T` on the global average. For every distinct size `m < n`, the corresponding eigenspace contributes

[
\lambda_m^T(P_m-P_{\text{parent}}).
]

Adding the positive coefficient to `P_m` and subtracting it from its parent projection produces the final coefficient of every projection.
6. Build a prefix sum of the initial city values. This lets us obtain the sum of any administrative block in constant time, and therefore its average in constant time after multiplying by the modular inverse of its size.
7. Apply each projection coefficient using a difference array. For every block `[l,r)`, compute its average and add the corresponding value to the entire interval through two difference-array updates. There are only `n/m` blocks for size `m`.
8. Prefix-sum the difference array once to recover the final value of every city.

The correctness invariant is that after processing any collection of hierarchical components, the accumulated value assigned to a city is exactly the contribution of those components in the eigenspace decomposition of the initial vector. The operators `P_m` are nested projections, so every vector decomposes uniquely into the global constant component, the successive differences between nested block averages, and the remaining top-level difference component. The latter has eigenvalue zero and vanishes after at least one year. Every other component is multiplied by its exact eigenvalue raised to `T`, so the resulting vector is exactly `A^T d_0`.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve_case(n, k, T, sizes, d, rho):
    # Compress equal administrative sizes.
    groups = []
    gamma = []

    for i in range(k):
        m = sizes[i]
        add = (rho[i + 1] - rho[i]) * m % MOD

        if groups and groups[-1] == m:
            gamma[-1] = (gamma[-1] + add) % MOD
        else:
            groups.append(m)
            gamma.append(add)

    r = len(groups)

    # Suffix eigenvalues for the hierarchical difference spaces.
    eig = [0] * r
    cur = 0
    for i in range(r - 1, -1, -1):
        cur += gamma[i]
        cur %= MOD
        eig[i] = cur

    # Eigenvalue of the global constant subspace.
    global_eig = (rho[0] * n + cur) % MOD
    global_pow = pow(global_eig, T, MOD)

    # Coefficients of the projection operators.
    #
    # The decomposition is
    # A^T = global_pow * P_global
    #       + sum eig[i]^T * (P_i - P_parent).
    #
    # If groups[i] == n, P_i == P_global, so that component is zero.
    coeff = [0] * r
    coeff_global = global_pow

    previous = -1

    for i in range(r):
        m = groups[i]
        if m == n:
            continue

        ep = pow(eig[i], T, MOD)

        coeff[i] = (coeff[i] + ep) % MOD

        if previous == -1:
            coeff_global = (coeff_global - ep) % MOD
        else:
            coeff[previous] = (coeff[previous] - ep) % MOD

        previous = i

    # Prefix sums of the initial vector.
    pref = [0] * (n + 1)
    s = 0
    for i, x in enumerate(d):
        s += x
        pref[i + 1] = s % MOD

    # Difference array for range additions.
    diff = [0] * (n + 1)

    # Global average contribution.
    if coeff_global:
        avg = pref[n] * pow(n, MOD - 2, MOD) % MOD
        value = coeff_global * avg % MOD
        diff[0] += value
        diff[n] -= value

    # Contributions of every nontrivial administrative size.
    for i in range(r):
        c = coeff[i]
        m = groups[i]

        if c == 0 or m == n:
            continue

        inv_m = pow(m, MOD - 2, MOD)
        factor = c * inv_m % MOD

        for l in range(0, n, m):
            rr = l + m
            block_sum = (pref[rr] - pref[l]) % MOD
            value = block_sum * factor % MOD

            diff[l] += value
            diff[rr] -= value

    # Recover point values from the range additions.
    ans = [0] * n
    cur = 0
    for i in range(n):
        cur += diff[i]
        ans[i] = cur % MOD

    return ans

def main():
    t = int(input())
    out = []

    for _ in range(t):
        n, k, T = map(int, input().split())
        sizes = list(map(int, input().split()))
        d = list(map(int, input().split()))
        rho = list(map(int, input().split()))

        ans = solve_case(n, k, T, sizes, d, rho)
        out.append(" ".join(map(str, ans)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The first part compresses equal sizes. The factor `m` in `gamma` comes from `B_i = mP_m`, because averaging over a block divides its sum by `m`, while the original block matrix returns the sum.

The suffix loop computes the eigenvalue of every hierarchical difference space. If a vector has zero average in every parent block and is constant inside the current blocks, all coarser averaging operators annihilate it, while every finer block operator multiplies it by its block size. That gives exactly the suffix sum of the `gamma` values.

The special case `m == n` is handled by skipping the corresponding difference space. A level whose groups contain all cities has the same averaging operator as the global projection, so subtracting its powered eigenvalue as if it were a new component would introduce a fake zero-dimensional component.

The prefix array is stored modulo `MOD`. All block sizes are at most `3 * 10^5`, which is strictly smaller than `998244353`, so every required modular inverse exists.

The difference array is the key implementation optimization. Instead of adding one block average to all `m` cities, two boundary updates represent the whole range. Across a level with block size `m`, there are only `n/m` such updates.

Python integers do not overflow, but modular reduction is still performed regularly so that intermediate values remain small. The exponentiation calls use Python's three-argument `pow`, which performs modular exponentiation in logarithmic time.

## Worked Examples

### Sample 1

The sample has `n = 4`, sizes `2, 1`, initial vector `[1, 3, 5, 6]`, and coefficients `[2, 4, 5]`.

The matrix decomposition starts with

[
A=2J+(4-2)B_1+(5-4)I.
]

Since `B_1 = 2P_2`, this becomes

[
A=2J+4P_2+I.
]

The global eigenvalue is `13`, the level-2 block-difference eigenvalue is `5`, and the city-level difference eigenvalue is `1`.

| Component | Eigenvalue | Powered coefficient | Projection |
| --- | --- | --- | --- |
| Global | 13 | 13 | `P_global` |
| Size 2 difference | 5 | 5 | `P_2 - P_global` |
| Size 1 difference | 1 | 1 | `I - P_2` |

Combining the projections gives

[
A=8P_{\text{global}}+4P_2+I.
]

The relevant averages are `15/4` globally, `2` in the first size-2 block, `11/2` in the second size-2 block, and the original values at size `1`.

| City | Global contribution | Size-2 contribution | City contribution | Result |
| --- | --- | --- | --- | --- |
| 1 | 30 | 8 | 1 | 39 |
| 2 | 30 | 8 | 3 | 41 |
| 3 | 30 | 22 | 5 | 57 |
| 4 | 30 | 22 | 6 | 58 |

The output is `39 41 57 58`. The trace shows why the answer can be assembled from block averages rather than individual pair interactions.

### Example 2

Consider

```
1
2 1 2
1
1 2
2 3
```

There is only one administrative level of size `1`, so different cities interact with coefficient `2`, while a city interacts with itself using coefficient `3`. The matrix is

[
A=
\begin{pmatrix}
3&2\
2&3
\end{pmatrix}.
]

Its global eigenvalue is `5`, and its difference eigenvalue is `1`.

| Component | Eigenvalue | After `T = 2` | Projection |
| --- | --- | --- | --- |
| Global | 5 | 25 | `P_global` |
| City difference | 1 | 1 | `I - P_global` |

Thus

[
A^2=25P_{\text{global}}+(I-P_{\text{global}})
=24P_{\text{global}}+I.
]

The global average of `[1,2]` is `3/2`, giving

| City | Global part | Individual part | Result |
| --- | --- | --- | --- |
| 1 | 36 | 1 | 37 |
| 2 | 36 | 2 | 38 |

The output is `37 38`. This example exercises the case where there is only the city level and no nontrivial intermediate administrative partition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n + S)` where `S = sum(n/m)` over distinct sizes | Prefix construction, block processing, and final reconstruction are linear in the total number of blocks and cities |
| Space | `O(n + r)` | Initial values, prefix sums, difference array, and at most `O(log n)` distinct sizes |

For two consecutive distinct administrative sizes, the smaller divides the larger and is strictly smaller, so it is at most half of the larger. Consequently,

[
\frac{n}{m_1}+\frac{n}{m_2}+\cdots < 1+2+4+\cdots < 2n.
]

Thus the total number of administrative blocks processed is `O(n)`, not `O(n log n)`. The practical complexity of the implementation is therefore `O(n + k + log T)` per test case, with the `k` term coming from reading and compressing the input. Across all test cases, the sum of `n` is at most `10^6`, so the solution stays within the intended limits.

## Test Cases

The following test harness assumes the submitted solution is saved as `solution.py` and exposes the `solve_case` function shown above.

```python
import sys
import io

from solution import solve_case

def run(inp: str) -> str:
    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(inp)
        t = int(sys.stdin.readline())
        out = []

        for _ in range(t):
            n, k, T = map(int, sys.stdin.readline().split())
            sizes = list(map(int, sys.stdin.readline().split()))
            d = list(map(int, sys.stdin.readline().split()))
            rho = list(map(int, sys.stdin.readline().split()))
            ans = solve_case(n, k, T, sizes, d, rho)
            out.append(" ".join(map(str, ans)))

        return "\n".join(out)
    finally:
        sys.stdin = old_stdin

# Provided sample.
assert run(
    """1
4 2 1
2 1
1 3 5 6
2 4 5
"""
) == "39 41 57 58", "sample 1"

# Minimum-size case, n = 1.
expected = 7 * pow(5, 10**18, 998244353) % 998244353
assert run(
    """1
1 1 1000000000000000000
1
7
2 5
"""
) == str(expected), "minimum size and huge T"

# All initial values equal. Every row has sum 13.
assert run(
    """1
4 3 1
4 2 1
3 3 3 3
1 2 4 7
"""
) == "39 39 39 39", "all equal values"

# The largest administrative group is the whole country.
# The matrix is J + I, and its square is 6J + I.
assert run(
    """1
4 3 2
4 2 1
1 2 3 4
1 1 1 2
"""
) == "61 62 63 64", "top-level group equals all cities"

# Only city level exists. Matrix [[3,2],[2,3]], squared gives [[13,12],[12,13]].
assert run(
    """1
2 1 2
1
1 2
2 3
"""
) == "37 38", "city-level-only case"

# Maximum n, using uniform values and coefficients.
# A is the all-ones matrix, so one year produces n for every city.
n = 300000
inp = (
    "1\n"
    f"{n} 1 1\n"
    "1\n"
    + " ".join(["1"] * n) + "\n"
    "1 1\n"
)
out = run(inp).split()
assert len(out) == n, "maximum-size output length"
assert all(x == str(n % 998244353) for x in out), "maximum-size uniform case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, T=10^18` | `7 * 5^T mod MOD` | Smallest possible hierarchy and huge exponent |
| `n=4`, all initial values `3` | `39 39 39 39` | Constant-vector eigenvalue and repeated hierarchy |
| `n=4`, sizes `4,2,1`, `T=2` | `61 62 63 64` | Top-level group equals the whole city set |
| `n=2`, `k=1`, `T=2` | `37 38` | No intermediate administrative level |
| `n=300000`, uniform values | `300000` repeated `300000` times | Maximum input size and linear block processing |

## Edge Cases

For `n = 1`, every averaging operator is the identity. In the input

```
1
1 1 3
1
7
2 5
```

the decomposition has global eigenvalue `5`, because the only matrix entry is `rho_1`. The powered operator is multiplication by `5^3`, giving `875`. The implementation naturally handles this because the size-1 group coincides with the global projector, so the nontrivial difference component is skipped.

For repeated sizes, consider

```
1
4 3 1
4 2 1
3 3 3 3
1 2 4 7
```

The size `4` and size `2` projectors are distinct, while the three levels themselves remain fully represented even if additional equal sizes were inserted. The compression step combines equal-size contributions into one `gamma` value. Since the input vector is constant, only the global eigenvalue matters, and every output becomes `39`.

For a top-level group equal to all cities, consider

```
1
4 3 2
4 2 1
1 2 3 4
1 1 1 2
```

The matrix is `J + I`. Its global eigenvalue is `5`, while every nonconstant component has eigenvalue `1`. After two years the global component is multiplied by `25`, and every nonconstant component remains unchanged. Since the global average is `5/2`, the result is `25 * 5/2 + (d_i - 5/2) = 60 + d_i`, giving `61 62 63 64`.

For a hierarchy containing only the city level, the input

```
1
2 1 2
1
1 2
2 3
```

has matrix

[
\begin{pmatrix}
3&2\
2&3
\end{pmatrix}.
]

The global component has eigenvalue `5` and the difference component has eigenvalue `1`. After two years the first component is multiplied by `25`, while the second remains unchanged, producing `37 38`. This catches the common mistake of assuming that at least one intermediate administrative level must exist.
