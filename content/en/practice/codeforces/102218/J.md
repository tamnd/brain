---
title: "CF 102218J - Just an easy task"
description: "We need to determine, for every day k from 0 to n - 1, how many ordered pairs (i, j) satisfy i⋅j≡k(modn). Each such pair contributes exactly one unit to day k, so the required output is simply the number of pairs producing each residue modulo n."
date: "2026-08-20T03:33:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102218
codeforces_index: "J"
codeforces_contest_name: "2019, XI Annual Programming Contest by ESCOM-IPN"
rating: 0
weight: 102218
solve_time_s: 440
verified: false
draft: false
---

[CF 102218J - Just an easy task](https://codeforces.com/problemset/problem/102218/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We need to determine, for every day `k` from `0` to `n - 1`, how many ordered pairs `(i, j)` satisfy

i⋅j≡k(modn).

Each such pair contributes exactly one unit to day `k`, so the required output is simply the number of pairs producing each residue modulo `n`.

A direct interpretation gives an `n × n` multiplication table modulo `n`. That observation is useful for understanding the problem, but the constraint `n <= 2.2 × 10^6` makes it impossible to construct that table. There are up to

(2.2×10 6 ) 2 =4.84×10 12

pairs, while the time limit is only 2.5 seconds on the original problem. We need a solution whose work is close to linear in `n`.

The most delicate cases come from the fact that `0` is also a residue and that multiplication modulo a composite number behaves differently from multiplication modulo a prime. For `n = 1`, there is only the pair `(0,0)`, so the answer is `1`. A careless implementation that loops over positive residues only would produce nothing.

For `n = 2`, the pairs are `(0,0)`, `(0,1)`, `(1,0)`, `(1,1)`. Three produce residue `0` and one produces residue `1`, giving

```
31
```

A formula that accidentally assumes every nonzero residue has the same number of representations would fail here.

For `n = 6`, the answer begins with `15` at residue `0`, not `6`. The value at zero counts all pairs whose product is divisible by `6`, and composite moduli create many such pairs. This is exactly the situation where treating the problem like arithmetic modulo a prime gives the wrong result.

## Approaches

The brute-force solution follows the definition directly. Create an array of `n` counters, iterate over every `i` and every `j`, calculate `(i * j) % n`, and increment the corresponding counter. This is correct because every ordered pair is considered exactly once and contributes to exactly the residue specified by the problem.

The problem is the number of operations. In the largest case there are `n² = 4.84 × 10^12` pairs. Even a very small constant per pair would be far beyond the time limit.

The useful observation is to stop fixing both `i` and `j`. Fix `i` and ask when

ij≡k(modn)

has solutions.

Let

g=gcd(i,n).

A standard property of linear congruences says that `ij ≡ k (mod n)` has solutions exactly when `g` divides `k`. When this condition holds, there are exactly `g` different values of `j` modulo `n` satisfying the congruence.

So an `i` contributes `gcd(i,n)` pairs to residue `k` precisely when `gcd(i,n)` divides `k`.

Now group all `i` having the same gcd with `n`. If

gcd(i,n)=d,

write `i = d x`. Then

gcd(x,n/d)=1.

There are exactly

φ(n/d)

such values of `i`, where `φ` is Euler's totient function. Each contributes `d` solutions for `j`, so all `i` with gcd equal to `d` contribute

dφ(n/d)

to every residue `k` divisible by `d`.

Consequently,

c k ​ = d∣n d∣k ​ ∑ ​ dφ(n/d)= d∣gcd(k,n) ∑ ​ dφ(n/d).

This formula changes the problem completely. We only need to consider divisors of `n`. For every divisor `d`, calculate

w d ​ =dφ(n/d)

and add `w_d` to every multiple of `d` among the residues `1,2,\ldots,n-1`. Residue `0` is divisible by every divisor, so it receives every `w_d` separately.

The total number of updates is

d∣n ∑ ​ d n ​ =n d∣n ∑ ​ d 1 ​ ,

which is `O(n log log n)` and is very close to linear for the given bound. We also avoid constructing a full totient sieve up to `n`, because only `φ(n/d)` for divisors of `n` is needed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n²)` | `O(n)` | Too slow |
| Optimal | `O(n log log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Factor `n` into its prime powers. We need the factorization because it lets us enumerate every divisor of `n` and calculate Euler's totient for `n / d` without building a size-`n` totient array.
2. Generate all divisors of `n` from its prime factorization. There are only `τ(n)` of them, which is tiny compared with `n` for `n <= 2.2 × 10^6`.
3. For every divisor `d`, calculate

w=dφ(n/d).

This is the total contribution of all `i` satisfying `gcd(i,n) = d` to every residue divisible by `d`.

1. Add `w` to every positive multiple of `d` below `n`. The loop visits `d, 2d, 3d, ...`, and every one of these residues is divisible by `d`, exactly matching the condition in the formula.
2. Add `w` to `answer[0]` as well. Zero is divisible by every positive integer, but a usual multiples loop beginning at `d` does not visit zero.
3. Output the resulting array. The values can be as large as `n²`, so Python integers naturally provide sufficient precision.

### Why it works

For a fixed `i`, the congruence

ij≡k(modn)

has `gcd(i,n)` solutions for `j` when `gcd(i,n)` divides `k`, and no solutions otherwise. Grouping the values of `i` by `d = gcd(i,n)`, there are `φ(n/d)` values in the group, and each contributes `d` solutions. Thus that group contributes `d φ(n/d)` exactly to the residues divisible by `d`. The algorithm performs precisely those additions for every divisor `d`, including the special residue `0`, so every pair is counted exactly once.

## Python Solution

```python
Pythonimport sysinput = sys.stdin.readline

def factorize(n):    factors = []    x = n    p = 2
    while p * p <= x:        if x % p == 0:            e = 0            while x % p == 0:                x //= p                e += 1            factors.append((p, e))        p += 1 if p == 2 else 2
    if x > 1:        factors.append((x, 1))
    return factors

def get_divisors(factors):    divisors = [1]
    for p, e in factors:        old = divisors[:]        power = 1
        for _ in range(e):            power *= p            for d in old:                divisors.append(d * power)
    return divisors

def phi_from_factorization(x, factors):    result = x
    for p, _ in factors:        if x % p == 0:            result -= result // p
    return result

def compute(n):    factors = factorize(n)    divisors = get_divisors(factors)
    ans = [0] * n
    for d in divisors:        w = d * phi_from_factorization(n // d, factors)
        ans[0] += w
        for k in range(d, n, d):            ans[k] += w
    return ans

def solve():    n = int(input())    ans = compute(n)
    out = sys.stdout.buffer
    # Avoid constructing one enormous output string at once.    chunk = []    for x in ans:        chunk.append(str(x))        if len(chunk) == 100000:            out.write(("\n".join(chunk) + "\n").encode())            chunk.clear()
    if chunk:        out.write(("\n".join(chunk) + "\n").encode())

if __name__ == "__main__":    solve()
```

The factorization starts with `2` and then tests only odd candidates. Since `n` is at most `2.2 × 10^6`, trial division up to `sqrt(n)` is inexpensive.

The divisor generator starts with `{1}`. For each prime power `p^e`, every existing divisor is combined with `p`, `p²`, ..., `p^e`, producing exactly every divisor of `n` once.

For a particular divisor `d`, `n // d` is the modulus appearing inside the totient. Since the prime factors of `n // d` must be among the prime factors of `n`, `phi_from_factorization` can calculate the totient using

φ(x)=x p∣x ∏ ​ (1− p 1 ​ ).

The inner loop starts at `d`, not at zero, because zero is handled explicitly with `ans[0] += w`. Starting at zero would be valid too, but it would require a slightly different loop structure.

The answer array contains ordinary Python integers. No overflow handling is needed, and this matters because the total number of pairs is `n²`, which can be around `4.84 × 10^12`.

The output is written in chunks of 100,000 lines. This keeps the temporary output string bounded instead of constructing a potentially large string containing every answer simultaneously.

## Worked Examples

### Example 1: `n = 6`

The divisors of `6` are `1, 2, 3, 6`. Their contributions are:

1φ(6)=2,
2φ(3)=4,
3φ(2)=3,
6φ(1)=6.

The algorithm adds each contribution to zero and to all positive multiples of its divisor.

| Divisor `d` | `φ(6/d)` | Contribution `dφ(6/d)` | Positive residues updated |
| --- | --- | --- | --- |
| 1 | 2 | 2 | 1, 2, 3, 4, 5 |
| 2 | 2 | 4 | 2, 4 |
| 3 | 1 | 3 | 3 |
| 6 | 1 | 6 | none |

Residue zero receives `2 + 4 + 3 + 6 = 15`.

The resulting array is

```
1526562
```

For example, residue `4` is divisible by `1` and `2`, so it receives `2 + 4 = 6`. It is not divisible by `3` or `6`.

### Example 2: `n = 5`

Since `5` is prime, its only divisors are `1` and `5`.

| Divisor `d` | `φ(5/d)` | Contribution `dφ(5/d)` | Positive residues updated |
| --- | --- | --- | --- |
| 1 | 4 | 4 | 1, 2, 3, 4 |
| 5 | 1 | 5 | none |

Residue zero receives both contributions, giving `9`. Every nonzero residue is divisible only by `1`, so every nonzero answer is `4`.

The output is

```
94444
```

This illustrates why prime moduli have a particularly simple shape, while composite moduli require the full divisor sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log log n)` | For every divisor `d` of `n`, we update approximately `n/d` positions. |
| Space | `O(n)` | The answer array contains `n` integer values. |

The divisor sum satisfies

d∣n ∑ ​ d n ​ =n n σ(n) ​ =O(nloglogn),

so the number of array updates stays close to linear. The factorization and divisor generation take negligible time compared with those updates for the maximum input. The `O(n)` answer array is comfortably within the 256 MB memory limit for this constraint.

## Test Cases

```python
Pythonimport sysimport io
# The functions below are the same computational functions used by the solution.
def factorize(n):    factors = []    x = n    p = 2
    while p * p <= x:        if x % p == 0:            e = 0            while x % p == 0:                x //= p                e += 1            factors.append((p, e))        p += 1 if p == 2 else 2
    if x > 1:        factors.append((x, 1))
    return factors

def get_divisors(factors):    divisors = [1]
    for p, e in factors:        old = divisors[:]        power = 1
        for _ in range(e):            power *= p            for d in old:                divisors.append(d * power)
    return divisors

def phi_from_factorization(x, factors):    result = x
    for p, _ in factors:        if x % p == 0:            result -= result // p
    return result

def compute(n):    factors = factorize(n)    divisors = get_divisors(factors)    ans = [0] * n
    for d in divisors:        w = d * phi_from_factorization(n // d, factors)
        ans[0] += w
        for k in range(d, n, d):            ans[k] += w
    return ans

def run(inp: str) -> str:    n = int(inp.strip())    ans = compute(n)    return "\n".join(map(str, ans)) + "\n"

# Provided sampleassert run("6") == "15\n2\n6\n5\n6\n2\n", "sample 1"
# Minimum sizeassert run("1") == "1\n", "n = 1"
# Small composite numberassert run("4") == "8\n4\n4\n4\n", "n = 4"
# Prime modulus, all nonzero residues have equal valuesassert run("5") == "9\n4\n4\n4\n4\n", "n = 5"
# Another composite case, useful for catching divisor/multiple errorsassert run("8") == "20\n4\n8\n4\n12\n4\n8\n4\n", "n = 8"

# Maximum-size structural test.# We do not materialize a second expected 2.2-million-line string.n = 2_200_000ans = compute(n)
assert len(ans) == n, "maximum n output length"assert sum(ans) == n * n, "every ordered pair must be counted exactly once"assert ans[0] == sum(    d * phi_from_factorization(n // d, factorize(n))    for d in get_divisors(factorize(n))), "zero residue"
```

The maximum-size test deliberately checks structural properties instead of embedding millions of expected output lines. The identity `sum(ans) = n²` is especially useful because every one of the `n²` ordered pairs must contribute to exactly one residue.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Minimum size and handling of residue zero |
| `4` | `8, 4, 4, 4` | Composite modulus and repeated divisor contributions |
| `5` | `9, 4, 4, 4, 4` | Prime modulus and equal nonzero residues |
| `8` | `20, 4, 8, 4, 12, 4, 8, 4` | Several prime-power divisors and multiple boundaries |
| `2_200_000` | Structural checks | Maximum input size, total pair count, and performance |

## Edge Cases

For `n = 1`, the only pair is `(0,0)`. The divisor set contains only `1`, and its contribution is

1⋅φ(1)=1.

The positive-multiple loop performs no updates, while `ans[0]` receives `1`. The output is exactly `1`.

For `n = 2`, the divisors are `1` and `2`. Their contributions are `1·φ(2)=1` and `2·φ(1)=2`. Zero receives `3`, while residue `1` receives only the contribution from divisor `1`, giving `1`. The output is `3,1`, correctly accounting for the three pairs whose product is even.

For `n = 5`, the divisor `1` contributes `φ(5)=4` to every residue, while divisor `5` contributes `5` only to zero. Thus the answer is `9,4,4,4,4`. This catches an easy mistake where the special behavior of residue zero is forgotten.

For `n = 6`, divisor `3` contributes `3` to residues `0` and `3`, while divisor `2` contributes `4` to `0`, `2`, and `4`. Residue `4` consequently receives `2 + 4 = 6`, while residue `5` receives only `2`. This confirms that the algorithm tests divisibility by the divisor rather than merely testing whether the residue shares a prime factor with it.

For the maximum value `n = 2,200,000`, the algorithm never constructs the `n × n` multiplication table. It only processes the divisors of `n` and their multiples, so the amount of work remains near linear in `n`. The output values are still at most the total number of ordered pairs, `n²`, and Python integers handle that range without overflow.
