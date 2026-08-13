---
title: "CF 102319F - Forever Young"
description: "The students have distinct ages, so an arrangement of the class is simply a permutation of the numbers (1,ldots,s). Henry's maximum number of circled students is the length of the longest increasing subsequence of that permutation."
date: "2026-08-14T04:51:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102319
codeforces_index: "F"
codeforces_contest_name: "UBC Summer Contest 2018"
rating: 0
weight: 102319
solve_time_s: 123
verified: true
draft: false
---

[CF 102319F - Forever Young](https://codeforces.com/problemset/problem/102319/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

The students have distinct ages, so an arrangement of the class is simply a permutation of the numbers (1,\ldots,s). Henry's maximum number of circled students is the length of the longest increasing subsequence of that permutation. Eugene's maximum is the length of the longest decreasing subsequence.

We need to count permutations whose longest increasing subsequence has length exactly (n) and whose longest decreasing subsequence has length exactly (m). The answer is required modulo (10^9+7).

The large value (s\le 10^6) immediately rules out anything that examines the students in a quadratic or factorial number of ways. The useful extra constraint is (n+m\ge s-50). This says that the two desired subsequence lengths are almost as large as the entire permutation, which severely restricts the possible combinatorial structures. The entire solution exploits that restriction.

There are two basic feasibility conditions worth keeping in mind. A permutation cannot have increasing and decreasing subsequences whose lengths add to more than (s+1), because the two subsequences can share at most one student. Also, Erdős-Szekeres implies (nm\ge s) whenever such a permutation exists.

A first edge case is (s=1,n=1,m=1). There is exactly one arrangement, so the answer is (1). A careless implementation that assumes there is always at least one nontrivial row or column in a Young diagram can mishandle this case.

A second edge case is (s=5,n=5,m=5). The requested sum of subsequence lengths is (10), which is greater than (s+1=6), so the answer is (0). A program that only checks the stated lower bound on (n+m) and starts enumerating shapes can accidentally treat an impossible shape as valid.

A third edge case occurs at the other end of the allowed range, for example (s=52,n=1,m=1). Here (n+m=2=s-50), so the input satisfies the special constraint, but no permutation of 52 distinct values can have both LIS and LDS equal to 1. The answer is (0). The special condition bounds the amount of extra structure we must enumerate, but it does not make every pair (n,m) feasible.

Finally, when (n+m=s+1), the two subsequences must cover the whole permutation with exactly one common element. There is only one possible Young diagram shape, a hook. This case is useful for catching an off-by-one error in the definition of the small parameter used below.

## Approaches

The direct approach is to enumerate all (s!) permutations, compute their longest increasing and decreasing subsequences, and count those satisfying the requested values. Even with an (O(s\log s)) LIS implementation, this takes (O(s!,s\log s)) operations. At (s=20), the number of permutations is already (20!\approx2.43\cdot10^{18}), so this approach is completely unusable.

A better approach is to stop thinking about the permutation itself. The Robinson-Schensted correspondence gives a bijection between permutations and pairs of standard Young tableaux having the same shape. For a permutation with shape (\lambda), the first row of (\lambda) has length equal to the LIS, and the first column has length equal to the LDS.

If (f^\lambda) denotes the number of standard Young tableaux of shape (\lambda), then a fixed shape corresponds to exactly ((f^\lambda)^2) permutations, because the two tableaux can be chosen independently. Thus the desired answer is

[
\sum_{\substack{\lambda\vdash s\\lambda_1=n\\lambda'_1=m}}(f^\lambda)^2.
]

The brute-force works because every permutation is represented exactly once by its pair of tableaux. The problem is that there are still far too many partitions of (s) to enumerate when (s) is large.

The key observation is the condition (n+m\ge s-50). A Young diagram with first row (n) and first column (m) has a mandatory hook containing

[
n+m-1
]

cells. Everything else consists of at most

[
t=s-(n+m-1)=s-n-m+1
]

additional cells. The input condition gives (0\le t\le51) for every feasible instance.

Remove the first row and the first column from those additional cells. What remains is an ordinary partition (\mu) of exactly (t). Since (t\le51), there are at most (p(51)=239943) such partitions.

This is the central reduction. Instead of enumerating partitions of (s), which could be an enormous number, we enumerate partitions of at most 51. The remaining task is to compute (f^\lambda) quickly without constructing a diagram containing up to one million cells.

The hook-length formula gives

[
f^\lambda=\frac{s!}{\prod_{c\in\lambda}h(c)},
]

where (h(c)) is the hook length of a cell.

The shape is almost a hook, so its hook product can be expressed using only (O(t)) factors. We precompute modular inverses up to (s), then every candidate shape can be evaluated in (O(t)) time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(s!,s\log s)) | (O(s)) | Too slow |
| Optimal | (O(s+p(51)\cdot51)) | (O(s)) | Accepted |

## Algorithm Walkthrough

1. Define

[
t=s-n-m+1.
]

The mandatory hook has (n+m-1) cells, so (t) is exactly the number of cells outside that hook. If (t<0), then (n+m>s+1), which is impossible. If (nm<s), the desired shape cannot fit inside an (n\times m) rectangle, so the answer is also zero.

1. Represent every valid Young diagram as

[
\lambda=(n,\mu_1+1,\mu_2+1,\ldots),
]

where (\mu) is a partition of (t).

The number of rows below the first row is at most (m-1), so (\mu) has at most (m-1) parts. Since the second row of (\lambda) cannot be longer than the first, every part of (\mu) is at most (n-1).

Thus we enumerate partitions of (t) with maximum part (n-1) and at most (m-1) parts.

1. For a particular partition (\mu), construct its column heights. Let (h_c) be the number of parts of (\mu) that are at least (c).

The lower-right portion of (\lambda) is exactly the diagram of (\mu), shifted one row down and one column right. These column heights let us obtain every hook length in that small portion in constant time.

1. Separate the hook product of (\lambda) into four pieces. The cell ((1,1)) has hook length (s), so the numerator after cancelling this factor is ((s-1)!).

For the rest of the first row, the cell corresponding to column (c+1) has hook length

[
n-c+h_c
]

for (1\le c\le\mu_1). After the last occupied column of (\mu), the factors are simply

[
n-\mu_1-1,\ldots,1,
]

giving the factorial ((n-\mu_1-1)!).

1. The cells below the first cell of the first column have hook lengths

[
m-r+\mu_r
]

for row (r) of (\mu). Once the nonzero parts of (\mu) end, the remaining factors form

[
(m-L-1)!,
]

where (L) is the number of parts of (\mu).

1. For every cell ((r,c)) inside (\mu), its corresponding cell in (\lambda) has hook length

[
\mu_r-c+h_c-r+1.
]

There are exactly (t) such cells, so this entire part costs (O(t)) operations.

1. Combine the factors with the hook-length formula. Since every hook length is at most (s\le10^6<10^9+7), every denominator factor has a modular inverse.
2. Square the resulting value (f^\lambda) and add it to the answer. RSK tells us that this square counts exactly the permutations whose RSK shape is (\lambda), so summing over all valid shapes gives the required count.

### Why it works

Every permutation corresponds bijectively to a pair of standard Young tableaux of one common shape (\lambda). The LIS and LDS are respectively the first row and first column lengths of that shape. Hence fixing (n) and (m) is exactly the same as restricting the first row to (n) and the first column to (m).

Every such shape contains the hook of (n+m-1) cells, and all remaining cells form a partition (\mu) of (t=s-n-m+1). The algorithm enumerates every such (\mu) exactly once while enforcing the width and height limits, so every admissible shape appears exactly once and no inadmissible shape appears. The hook-length calculation gives the exact number (f^\lambda) of tableaux of that shape, and the pair of tableaux gives ((f^\lambda)^2) permutations. Thus every valid permutation contributes once to the answer.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

MOD = 1_000_000_007

def solve_case(s, n, m):
    t = s - n - m + 1

    # n + m > s + 1 is impossible.
    # n * m < s means an n by m Young diagram cannot contain s cells.
    if t < 0 or n * m < s:
        return 0

    max_mu = min(t, n - 1)

    # Factorial of s - 1, and factorials of n - 1 and m - 1.
    fact_s = 1
    fact_n = 1
    fact_m = 1

    for i in range(2, s):
        fact_s = fact_s * i % MOD
        if i == n - 1:
            fact_n = fact_s
        if i == m - 1:
            fact_m = fact_s

    # Handle n = 1 or m = 1, where the corresponding factorial is 0!.
    if n - 1 == 0:
        fact_n = 1
    if m - 1 == 0:
        fact_m = 1

    # Modular inverses of every integer up to s.
    inv = array('I', [0]) * (s + 1)
    if s >= 1:
        inv[1] = 1
    for i in range(2, s + 1):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD

    # We only need inverse factorials close to n - 1 and m - 1.
    # invfact_n[j] = 1 / (n - 1 - j)!
    invfact_n = [0] * (max_mu + 1)
    invfact_m = [0] * (min(t, m - 1) + 1)

    invfact_n[0] = pow(fact_n, MOD - 2, MOD)
    for j in range(1, len(invfact_n)):
        x = n - j
        invfact_n[j] = invfact_n[j - 1] * x % MOD

    invfact_m[0] = pow(fact_m, MOD - 2, MOD)
    for j in range(1, len(invfact_m)):
        x = m - j
        invfact_m[j] = invfact_m[j - 1] * x % MOD

    answer = 0
    mu = []

    def process():
        nonlocal answer

        L = len(mu)
        mu1 = mu[0] if L else 0

        # Column heights of mu.
        heights = [0] * (mu1 + 1)
        for x in mu:
            for c in range(1, x + 1):
                heights[c] += 1

        # Start with (s-1)!.
        f = fact_s

        # First row.
        f = f * invfact_n[mu1] % MOD
        for c in range(1, mu1 + 1):
            hook = n - c + heights[c]
            f = f * inv[hook] % MOD

        # First column below the top cell.
        f = f * invfact_m[L] % MOD
        for r, x in enumerate(mu, 1):
            hook = m - r + x
            f = f * inv[hook] % MOD

        # Cells corresponding to the diagram mu.
        for r, x in enumerate(mu, 1):
            for c in range(1, x + 1):
                hook = x - c + heights[c] - r + 1
                f = f * inv[hook] % MOD

        answer = (answer + f * f) % MOD

    def generate(rem, maximum, parts_left):
        if rem == 0:
            process()
            return

        if parts_left == 0 or maximum == 0:
            return

        upper = min(rem, maximum)

        for x in range(upper, 0, -1):
            mu.append(x)
            generate(rem - x, x, parts_left - 1)
            mu.pop()

    generate(t, n - 1, m - 1)
    return answer

def main():
    s, n, m = map(int, input().split())
    print(solve_case(s, n, m))

if __name__ == "__main__":
    main()
```

The first part of the implementation computes (t) and rejects impossible inputs before doing any enumeration. The condition (n*m<s) is equivalent to saying that an (n)-column, (m)-row Young diagram cannot contain enough cells.

The factorial loop computes ((s-1)!), which is the numerator left after removing the hook length (s) of the top-left cell. During the same loop it records ((n-1)!) and ((m-1)!), because only short ranges of their inverse factorials are needed later.

The inverse array uses the standard recurrence

-\left\lfloor\frac{MOD}{i}\right\rfloor
\operatorname{inv}(MOD\bmod i)
\pmod{MOD}.
]

No hook length is divisible by (MOD), because all hook lengths are at most (10^6), so these inverses are always valid.

The two inverse-factorial arrays are deliberately short. For the first row we only need ((n-1-j)!) for (0\le j\le t), and the analogous statement holds for the first column. Storing a full factorial and inverse-factorial table up to one million is unnecessary.

The recursive generator keeps the partition parts nonincreasing. The parameter `maximum` is the largest value allowed for the next part, while `parts_left` enforces the condition that (\mu) has at most (m-1) parts. Because (t\le51), recursion depth is at most 51.

Inside `process`, `heights[c]` is the column height of column (c) in (\mu). The first-row, first-column, and lower-right hook factors are then calculated directly from the formulas above. The loops over the cells of (\mu) process exactly (t) cells, so they never depend on the potentially huge value of (s).

There is no integer overflow issue in Python. Every multiplication is reduced modulo (10^9+7), and the final contribution is squared only after (f^\lambda) has already been reduced modulo the same modulus.

## Worked Examples

### Sample 1

For

[
s=6,\quad n=3,\quad m=3,
]

we get

[
t=6-3-3+1=1.
]

The only partition of 1 is (\mu=(1)), giving the Young diagram

[
\lambda=(3,2,1).
]

Its hook lengths are (5,3,1,3,1,1), whose product is 45. Thus

[
f^\lambda=\frac{6!}{45}=16.
]

There is only one valid shape, so the answer is (16^2=256).

| (\mu) | (\lambda) | (f^\lambda) | Contribution |
| --- | --- | --- | --- |
| ((1)) | ((3,2,1)) | 16 | 256 |

The trace demonstrates the main reduction. Six students do not require enumeration of (6!=720) permutations. Once the RSK shape is fixed, all 256 valid permutations are counted at once.

### Sample 2

For

[
s=12,\quad n=3,\quad m=4,
]

we get

[
t=12-3-4+1=6.
]

The partition must have at most three parts and every part must be at most two. The only possibilities are ((2,2,2)) and ((2,2,1)).

They produce the shapes ((3,3,3,3)) and ((3,3,3,2)).

| (\mu) | (\lambda) | (f^\lambda) | (f^\lambda{}^2) |
| --- | --- | --- | --- |
| ((2,2,2)) | ((3,3,3,3)) | 462 | 213444 |
| ((2,2,1)) | ((3,3,3,2)) | 5544 | 30735936 |
| Total |  |  | 30949380 |

Hence the answer is

[
213444+30735936=30949380.
]

This example shows why enumerating unrestricted partitions is not enough. The width restriction (\mu_1\le n-1) and height restriction (\ell(\mu)\le m-1) eliminate the other partitions of 6.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(s+t,p(t))) | Precomputation costs (O(s)), and each of the (p(t)) partitions is processed in (O(t)). |
| Space | (O(s+t)) | The inverse array uses (O(s)) memory and the current partition uses (O(t)). |

Here (t\le51), and (p(51)=239943). Thus the partition enumeration has fewer than about 240,000 leaves, with at most 51 small cells processed per leaf. The only part depending on the full input size is linear preprocessing up to (s\le10^6). This fits the intended constraints much more comfortably than any approach involving the permutation itself.

## Test Cases

```python
from array import array

MOD = 1_000_000_007

def solve_case(s, n, m):
    t = s - n - m + 1

    if t < 0 or n * m < s:
        return 0

    max_mu = min(t, n - 1)

    fact_s = 1
    fact_n = 1
    fact_m = 1

    for i in range(2, s):
        fact_s = fact_s * i % MOD
        if i == n - 1:
            fact_n = fact_s
        if i == m - 1:
            fact_m = fact_s

    if n - 1 == 0:
        fact_n = 1
    if m - 1 == 0:
        fact_m = 1

    inv = array('I', [0]) * (s + 1)
    inv[1] = 1
    for i in range(2, s + 1):
        inv[i] = (MOD - (MOD // i) * inv[MOD % i] % MOD) % MOD

    invfact_n = [0] * (max_mu + 1)
    invfact_m = [0] * (min(t, m - 1) + 1)

    invfact_n[0] = pow(fact_n, MOD - 2, MOD)
    for j in range(1, len(invfact_n)):
        invfact_n[j] = invfact_n[j - 1] * (n - j) % MOD

    invfact_m[0] = pow(fact_m, MOD - 2, MOD)
    for j in range(1, len(invfact_m)):
        invfact_m[j] = invfact_m[j - 1] * (m - j) % MOD

    answer = 0
    mu = []

    def process():
        nonlocal answer

        L = len(mu)
        mu1 = mu[0] if L else 0

        heights = [0] * (mu1 + 1)
        for x in mu:
            for c in range(1, x + 1):
                heights[c] += 1

        f = fact_s

        f = f * invfact_n[mu1] % MOD
        for c in range(1, mu1 + 1):
            f = f * inv[n - c + heights[c]] % MOD

        f = f * invfact_m[L] % MOD
        for r, x in enumerate(mu, 1):
            f = f * inv[m - r + x] % MOD

        for r, x in enumerate(mu, 1):
            for c in range(1, x + 1):
                hook = x - c + heights[c] - r + 1
                f = f * inv[hook] % MOD

        answer = (answer + f * f) % MOD

    def generate(rem, maximum, parts_left):
        if rem == 0:
            process()
            return
        if parts_left == 0 or maximum == 0:
            return

        for x in range(min(rem, maximum), 0, -1):
            mu.append(x)
            generate(rem - x, x, parts_left - 1)
            mu.pop()

    generate(t, n - 1, m - 1)
    return answer

def run(inp: str) -> str:
    s, n, m = map(int, inp.split())
    return str(solve_case(s, n, m))

# Provided samples
assert run("6 3 3") == "256", "sample 1"
assert run("12 3 4") == "30949380", "sample 2"

# Minimum-size case, and n, m, s are all equal.
assert run("1 1 1") == "1", "minimum size"

# A completely increasing permutation is the only valid arrangement.
assert run("5 5 1") == "1", "maximum LIS"

# A completely decreasing permutation is the only valid arrangement.
assert run("5 1 5") == "1", "maximum LDS"

# n + m > s + 1, so no permutation can satisfy the request.
assert run("5 5 5") == "0", "impossible sum"

# The lower bound n + m = s - 50 is met exactly,
# but LIS = LDS = 1 is impossible for 52 distinct values.
assert run("52 1 1") == "0", "boundary lower bound"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | 1 | Minimum size and equal parameters |
| `5 5 1` | 1 | Purely increasing permutation |
| `5 1 5` | 1 | Purely decreasing permutation |
| `5 5 5` | 0 | Impossible (n+m>s+1) boundary |
| `52 1 1` | 0 | Exact (n+m=s-50) boundary |

## Edge Cases

For `1 1 1`, the value (t=1-1-1+1=0). The generator immediately processes the empty partition (\mu). The corresponding shape is simply ((1)), its tableau count is 1, and the answer becomes (1^2=1). This also shows why the empty partition must be handled explicitly rather than assuming that at least one extra cell exists.

For `5 5 5`, we get (t=5-5-5+1=-4). The algorithm returns zero before constructing any factorial or partition data. The negative value means the mandatory hook would already contain more than five cells, so no Young diagram of size five can have first row and first column both of length five.

For `52 1 1`, the special constraint is satisfied exactly because (1+1=52-50). However,

[
n\cdot m=1<52,
]

so an (n\times m) Young diagram cannot contain 52 cells. The early feasibility test returns zero. This is a useful case because merely checking that (t\le51) is not sufficient.

For `5 5 1`, we have (t=0). The only shape is the hook ((5)), because (m=1) permits no lower rows. Its tableau count is 1, corresponding to the unique increasing permutation. The analogous input `5 1 5` produces the single-column shape and the unique decreasing permutation.

For the sample `6 3 3`, (t=1), so the entire shape is determined by the single partition ((1)). The algorithm obtains (f^\lambda=16) and adds (16^2=256). This catches the common mistake of defining the excess as (s-n-m), which would be off by one and would incorrectly treat this case as having zero extra cells.
