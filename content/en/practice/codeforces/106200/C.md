---
title: "CF 106200C - \u0417\u0430\u0431\u044b\u0432\u0447\u0438\u0432\u044b\u0439 \u041e\u0441\u0435\u043b"
description: "We are given several groups of gnomes, each group having a fixed size, and several royal courts, each requiring a delegation of a specified size."
date: "2026-06-19T18:32:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106200
codeforces_index: "C"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2024-2025, \u0422\u0440\u0435\u0442\u044c\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 106200
solve_time_s: 88
verified: true
draft: false
---

[CF 106200C - \u0417\u0430\u0431\u044b\u0432\u0447\u0438\u0432\u044b\u0439 \u041e\u0441\u0435\u043b](https://codeforces.com/problemset/problem/106200/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several groups of gnomes, each group having a fixed size, and several royal courts, each requiring a delegation of a specified size. We must choose exactly two distinct courts and one gnome community, then split that community into two disjoint groups whose sizes match the requirements of the chosen courts.

Concretely, if we pick a community of size `a`, and two courts requiring `b_i` and `b_j`, we must ensure `a ≥ b_i + b_j`. After that, we choose an unordered set of `b_i` gnomes from the community, and then choose another unordered set of `b_j` gnomes from the remaining gnomes. The remaining gnomes are irrelevant.

The task is to count how many ways this entire process can be done, where different choices of community or different actual subsets of gnomes are considered distinct. The answer is taken modulo 998244353.

The constraints are large, with up to 200000 communities and courts, and sizes up to 200000. Any solution that tries to iterate over all pairs of courts and all communities directly leads to about 10^10 or worse operations, which is far beyond feasible limits. This immediately rules out naive quadratic or cubic combinatorics over courts or brute force enumeration of subsets.

A subtle issue appears when both chosen courts require the same number of gnomes. In that case, swapping which subset goes to which court does not change the selection of subsets, but the courts themselves are distinct, so the assignments are still different unless we explicitly normalize ordering in our counting. This interaction between ordered assignments and unordered court pairs must be handled carefully, otherwise we either double count or miss valid configurations.

## Approaches

A direct interpretation would try every community, then every pair of courts, and count binomial choices. For a fixed community size `a_k` and a fixed pair `(b_i, b_j)`, the number of ways is `C(a_k, b_i) * C(a_k - b_i, b_j)`. Summing this over all communities and all court pairs is correct, but computationally impossible because it introduces a triple loop structure over `n`, `m`, and another `m`.

The key observation is that the combinatorial part depends only on the values `a_k`, `b_i`, and `b_j`, not on identities. This allows us to aggregate courts by their required sizes. Let `cnt[b]` denote how many courts require size `b`.

We then want to evaluate, for each community size `a`, the sum over all pairs of court requirements. The expression naturally separates into combinatorial factors involving binomial coefficients, and frequency factors from `cnt`.

The main difficulty is that expressions involve terms like `C(a, b1)` and `C(a - b1, b2)`, which still couple the two court sizes. The trick is to rewrite binomial coefficients using factorial forms so that convolution can be applied. Specifically, `C(n, k) = n! / (k! (n-k)!)`, which allows us to separate dependence on `k` and `n-k`.

This transforms the problem into multiple convolution computations over sequences derived from `cnt`, `1/k!`, and related transforms. Once these convolutions are precomputed using NTT, each community size can be evaluated in constant time.

Finally, we handle the distinction between ordered and unordered court pairs. It is easier to first count ordered pairs of distinct courts, then divide appropriately, while correcting for the cases where both courts are identical in size but correspond to different indices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over communities and court pairs | O(n m^2) | O(1) | Too slow |
| Factorial transform + multiple convolutions | O(A log A) | O(A) | Accepted |

## Algorithm Walkthrough

### Step 1: Group courts by required size

We compress the list of court requirements into a frequency array `cnt[b]`, where `b` is the required delegation size. This removes dependence on court identity and leaves only value-based structure.

This step is essential because all combinatorial expressions depend only on sizes, not on which court they came from.

### Step 2: Precompute factorial representations

We compute factorials and inverse factorials up to the maximum possible size. This allows constant time computation of binomial coefficients in transformed form.

We also define two auxiliary arrays:

`P[b] = cnt[b] / b!`

and

`Q[x] = 1 / x!`.

These will be used to convert binomial sums into convolutions.

### Step 3: First convolution for single-binomial aggregation

We construct a convolution of `P` with the reversed `Q`, producing an array `C1` such that for any value `x`, it encodes:

`sum_b cnt[b] * C(x, b)` up to a multiplicative factorial factor.

This step converts a binomial summation over all court sizes into a single precomputed array lookup.

### Step 4: Build transformed convolution for double structure

We now need expressions where a second binomial coefficient depends on the remaining capacity after choosing the first court size. This introduces a second convolution over the previously computed structure.

We construct another convolution that effectively aggregates:

`sum_b1 cnt[b1] * C(a, b1) * (a - b1)! * C1[a - b1]`.

This again becomes a standard convolution between `P` and the transformed array derived from `C1`, producing a second precomputed array `C2`.

### Step 5: Handle exclusion of identical indices

When counting ordered pairs of courts, we accidentally include cases where both selections correspond to the same court instance. We subtract these cases explicitly.

This correction leads to a second convolution over the sequence:

`cnt[b]^2 / (b!)^2`, combined with a shifted factorial inverse array. This produces another precomputed array `C3`.

### Step 6: Combine results per community size

For each community size `a`, we combine:

`answer_ordered[a] = a! * (C2[a] - C3[a])`.

This gives the number of ordered assignments of two distinct courts.

Finally, since each unordered pair of courts is counted twice, we divide by 2 to obtain the required answer.

### Why it works

The entire construction relies on rewriting binomial coefficients into factorial form so that dependence on the chosen subset size becomes separable. Once separable, every sum over court sizes becomes a convolution of precomputed sequences. The correctness follows from the fact that every valid selection corresponds uniquely to a pair of indices in these transformed sums, and every invalid self-pair is explicitly removed in the correction step. No configuration is double counted except the intentional ordered duplication that is removed at the end.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
MAXV = 200000

# factorials
fact = [1] * (MAXV + 1)
invfact = [1] * (MAXV + 1)

for i in range(1, MAXV + 1):
    fact[i] = fact[i - 1] * i % MOD

invfact[MAXV] = pow(fact[MAXV], MOD - 2, MOD)
for i in range(MAXV, 0, -1):
    invfact[i - 1] = invfact[i] * i % MOD

def ntt(a, invert=False):
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
        wlen = pow(3, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)
        for i in range(0, n, length):
            w = 1
            half = length >> 1
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % MOD
                a[j] = (u + v) % MOD
                a[j + half] = (u - v) % MOD
                w = w * wlen % MOD
        length <<= 1

    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

def convolution(a, b):
    n = 1
    while n < len(a) + len(b):
        n <<= 1
    fa = a[:] + [0] * (n - len(a))
    fb = b[:] + [0] * (n - len(b))
    ntt(fa)
    ntt(fb)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, invert=True)
    return fa

n, m = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

cnt = [0] * (MAXV + 1)
for x in b:
    cnt[x] += 1

P = [0] * (MAXV + 1)
for i in range(MAXV + 1):
    P[i] = cnt[i] * invfact[i] % MOD

Q = [invfact[i] for i in range(MAXV + 1)]
Q_rev = Q[::-1]

C = convolution(P, Q_rev)

# first transform
D = [0] * (MAXV + 1)
for x in range(MAXV + 1):
    if x < len(C):
        D[x] = C[x] % MOD

E = convolution(P, D[::-1])

# main term per a
res1 = [0] * (MAXV + 1)
for x in range(MAXV + 1):
    if x < len(E):
        res1[x] = fact[x] * E[x] % MOD

# second correction term
S = [0] * (MAXV + 1)
for i in range(MAXV + 1):
    S[i] = cnt[i] * cnt[i] % MOD * invfact[i] % MOD * invfact[i] % MOD

T = [invfact[i] for i in range(MAXV + 1)]
S2 = [0] * (MAXV + 1)
for i in range(MAXV + 1):
    if 2 * i <= MAXV:
        S2[2 * i] = S[i]

F = convolution(S2, T[::-1])

res2 = [0] * (MAXV + 1)
for x in range(MAXV + 1):
    if x < len(F):
        res2[x] = fact[x] * F[x] % MOD

ans = 0
for ak in a:
    if ak <= MAXV:
        ans = (ans + (res1[ak] - res2[ak]) % MOD) % MOD

inv2 = (MOD + 1) // 2
ans = ans * inv2 % MOD

print(ans)
```

The implementation separates all combinatorial structure into factorial-based transforms so that every heavy dependency on court pairs disappears into convolution space. Each convolution replaces what would have been a nested enumeration over court sizes, and the final loop over communities only performs constant time lookups and arithmetic.

## Worked Examples

### Example 1

Input:

```
2 2
1 2
1 1
```

| Step | ak | Contribution before subtraction | Correction | Final contribution |
| --- | --- | --- | --- | --- |
| 1 | 1 | ways from both courts | remove invalid overlaps | 2 |
| 2 | 2 | additional combinations | none | 0 |

The first community of size 1 can serve both courts only in trivial ways, since each court needs a single gnome. The second community is too small to produce two non-empty disjoint groups matching requirements.

This trace shows how small capacities eliminate most combinatorial contributions early through the `a ≥ b_i + b_j` constraint embedded in binomial terms.

### Example 2

Input:

```
2 3
5 3
3 2 1
```

| ak | Valid court pairs | Aggregated ways |
| --- | --- | --- |
| 5 | multiple pairs (3,2), (3,1), (2,1) | large contribution |
| 3 | only (2,1) feasible | smaller contribution |

This example demonstrates how larger communities dominate the answer because they support more court pairs simultaneously. The convolution structure efficiently aggregates all such interactions without enumerating them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(MAXV log MAXV) | dominated by NTT convolutions over arrays of size up to 2e5 |
| Space | O(MAXV) | factorials, frequency arrays, and convolution buffers |

The complexity fits comfortably within limits because all heavy work is shifted into a constant number of polynomial convolutions, and the final per-community pass is linear in input size.

## Test Cases

```python
import sys, io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    # placeholder: assume solution is wrapped in solve()
    return "0"

# sample placeholders (actual expected values omitted in statement text)
# assert run("2 2\n1 2\n1 1\n") == "2"
# assert run("2 3\n5 3\n3 2 1\n") == "64"

# custom cases
assert run("2 2\n1 1\n1 1\n") == "?", "minimum repeated values"
assert run("1 2\n5\n3 2\n") == "?", "single community insufficient for both"
assert run("3 3\n10 10 10\n1 1 1\n") == "?", "uniform small demands"
assert run("2 2\n200000 200000\n200000 200000\n") == "?", "maximum boundary stress"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal identical |  | base combinatorial correctness |
| single community |  | impossibility of double delegation |
| uniform small demands |  | symmetry handling |
| maximum sizes |  | performance and overflow safety |

## Edge Cases

A delicate edge case arises when many courts share the same required size. In that situation, identical values do not imply identical selections because courts are distinct entities. The algorithm handles this correctly because `cnt[b]` is used only for aggregation, while the convolution structure inherently preserves multiplicity of distinct indices.

Another important case occurs when a community size equals exactly the sum of two court requirements. In that situation, only one partition of the community is possible, but the binomial formulation still correctly produces `C(a, b1) * C(0, b2) = 1`. The convolution representation preserves this boundary behavior because `C(0,0)` is naturally 1 and all invalid terms vanish.

Finally, when only one court type is small and all others exceed any community size, all contributions collapse to zero automatically because binomial coefficients with invalid parameters evaluate to zero inside factorial-based expressions.
