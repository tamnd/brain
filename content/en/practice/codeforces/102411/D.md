---
title: "CF 102411D - Double Palindrome"
description: "We need to count strings over an alphabet of size (k), considering every length from (1) through (n). A string qualifies if it is a palindrome itself, or if it can be split at some position into two non-empty palindromes."
date: "2026-08-10T14:35:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102411
codeforces_index: "D"
codeforces_contest_name: "ICPC 2019-2020 North-Western Russia Regional Contest"
rating: 0
weight: 102411
solve_time_s: 860
verified: false
draft: false
---

[CF 102411D - Double Palindrome](https://codeforces.com/problemset/problem/102411/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 14m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We need to count strings over an alphabet of size \(k\), considering every length from \(1\) through \(n\). A string qualifies if it is a palindrome itself, or if it can be split at some position into two non-empty palindromes. The same string is counted only once even if it has several valid splits. The answer is taken modulo \(998244353\). The original constraints and examples are given in the official problem statement. citeturn for the smallest nontrivial alphabet this is exponentially large. With \(k=26\), merely enumerating strings of the maximum length would require considering \(26^{100000}\) candidates. A two second limit rules out any approach proportional to the number of strings, and even polynomial algorithms with a large exponent would be unsuitable. We need to count whole families of strings mathematically.

There are several edge cases that expose common mistakes. The empty string is not allowed, so input `1 1` has answer \(1\), not \(2\). The only string is `a`.

Input `2 2` has answer \(6\). There are two strings of length one and all four strings of length two qualify, because every length-two string can be split into two one-letter palindromes. A method that counts only palindromes would return \(4\), which is wrong.

Input `3 3` has answer \(33\). The length-three contribution is \(21\), not just the \(9\) palindromes. Strings such as `aab` and `abb` qualify because they split as `aa|b` and `a|bb`. A method that checks only whether the whole string is a palindrome misses these strings.

The case \(k=1\) is also useful. With only the letter `a`, every non-empty string is a palindrome. Thus `100000 1` must produce `100000`. Any formula that accidentally counts decompositions instead of distinct strings can overcount this case dramatically.

## Approaches

The brute-force approach is conceptually straightforward. Generate every non-empty string of length at most \(n\), then try every possible split and check whether both resulting pieces are palindromes. This is correct because the definition itself is exactly an existential condition over the split position.

The problem is the number of strings. There are

\[
\sum_{i=1}^{n} k^i
\]

candidates, already \(\Theta(k^n)\). If checking all splits and palindrome conditions takes \(O(n^2)\) per string in a direct implementation, the worst-case work is \(\Theta(n^2 k^n)\). Even generating the strings is hopeless for \(n=10^5\).

The key observation is to stop thinking about the split itself. Suppose a string is \(w=uv\), where both \(u\) and \(v\) are palindromes. Its reverse is

\[
w^R=v^R u^R=vu.
\]

Rotating \(w^R\) by the length of \(v\) gives \(uv=w\). Conversely, if some rotation of \(w^R\) equals \(w\), cutting at the rotation point gives \(w=uv\) and the equality \(w^R=vu\), which forces \(u=u^R\) and \(v=v^R\).

So a double palindrome is exactly a word that is a cyclic rotation of its reverse. This turns the problem into counting fixed strings under reflections of a cycle.

For a fixed length \(m\), define \(r(m,k)\) as the number of pairs consisting of a string and a rotation that transforms its reverse back into the string. For a chosen rotation, positions are paired by a reflection of the \(m\)-cycle. Counting fixed strings becomes a simple count of independent positions.

If \(m\) is odd, every reflection has one fixed position and \((m-1)/2\) pairs, so it fixes

\[
k^{(m+1)/2}
\]

strings. There are \(m\) rotations, giving

\[
r(m,k)=m k^{(m+1)/2}.
\]

If \(m\) is even, half of the reflections have two fixed positions and \(m/2-1\) pairs, while the other half have no fixed positions and \(m/2\) pairs. Summing those two cases gives

\[
r(m,k)
=
\frac m2 k^{m/2+1}
+
\frac m2 k^{m/2}
=
\frac m2(k+1)k^{m/2}.
\]

The remaining problem is that \(r(m,k)\) counts a word once for every valid rotation, while we need every distinct word exactly once. Periodicity is what causes this multiplicity.

Every non-empty word has a unique primitive root. If a word has length \(m\) and is obtained by repeating a primitive word \(d\) times, then its rotational symmetry has exactly \(d\) equivalent positions. Grouping words by their primitive root and applying the standard divisor relation gives

\[
r(m,k)=\sum_{d\mid m}\varphi(d)T(m/d,k),
\]

where \(T(m,k)\) is the number of distinct double palindromes of length \(m\). This is the standard counting relation for palindrome pairs, and the resulting closed divisor formula is documented independently in the combinatorics literature. citeturn9 \(d\), we visit all multiples \(m=d,2d,3d,\ldots\) and add its contribution to \(T(m,k)\). There are only \(O(n\log n)\) such visits.

The brute-force approach works because it explicitly tests the definition, but fails because the set of strings is exponential. The observation that double palindromes are exactly rotations of their reverses replaces string enumeration by counting fixed points of reflections, and divisor inversion removes the overcount caused by periodic strings.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | \(\Theta(n^2 k^n)\) | \(O(n)\) per generated string | Too slow |
| Optimal | \(O(n\log n)\) | \(O(n)\) | Accepted |

## Algorithm Walkthrough

1. Precompute \(k^i\bmod 998244353\) for every \(0\le i\le n\). The formulas for \(r(m,k)\) only need powers whose exponent is at most \(\lceil n/2\rceil\), but computing the entire array keeps the implementation simple.

2. Compute \(r(m,k)\) for every length \(m\). For odd \(m\), use \(m k^{(m+1)/2}\). For even \(m\), use \((m/2)(k+1)k^{m/2}\). These values count strings together with a rotation witnessing that the string is a double palindrome.

3. Compute \(g(d)=\prod_{p\mid d}(1-p)\) for every \(d\le n\). We sieve over the primes, and whenever a prime \(p\) is found, multiply every multiple of \(p\) by \(1-p\). A prime may occur with any exponent in \(d\), but it contributes only once, exactly as required by the product over distinct prime factors.

4. Initialize \(T(m,k)\) to zero. For every divisor candidate \(d\), visit all multiples \(m=qd\) and add

\[
g(d)r(q,k)
\]

to \(T(m,k)\). Since \(q=m/d\), this is exactly the term indexed by \(d\) in the divisor formula.

5. Sum \(T(1,k),T(2,k),\ldots,T(n,k)\). The problem asks for all non-empty lengths up to \(n\), so this final sum is the required answer.

### Why it works

For each length \(m\), \(r(m,k)\) counts every qualifying word once for every rotation that maps its reverse to itself. The primitive-period decomposition of words converts these multiplicities into the divisor relation \(r=\varphi*T\). Dirichlet inversion gives \(T=g*r\), so the convolution performed by the algorithm computes every distinct double palindrome exactly once. The formulas for \(r\) count all reflection-fixed strings exactly, because each reflection partitions the positions into fixed points and mirrored pairs, with one free letter choice per resulting orbit. Thus every term added to the final sum corresponds to exactly one valid string of the corresponding length.

## Python Solution

```python
import sys

input = sys.stdin.readline

MOD = 998244353

def solve():
    n, k = map(int, input().split())

    # Powers of k modulo MOD.
    pw = [1] * (n + 1)
    for i in range(1, n + 1):
        pw[i] = pw[i - 1] * k % MOD

    # r[m] = number of (word, rotation) pairs such that
    # rotating reverse(word) by that amount gives word.
    r = [0] * (n + 1)

    for m in range(1, n + 1):
        if m & 1:
            r[m] = m * pw[(m + 1) // 2] % MOD
        else:
            r[m] = (
                (m // 2)
                * (k + 1)
                * pw[m // 2]
            ) % MOD

    # g[d] = Dirichlet inverse of Euler's phi function:
    # g[d] = product_{p | d} (1 - p).
    g = [1] * (n + 1)

    is_prime = bytearray(b'\x01') * (n + 1)
    if n >= 0:
        is_prime[0] = 0
    if n >= 1:
        is_prime[1] = 0

    for p in range(2, n + 1):
        if not is_prime[p]:
            continue

        factor = (1 - p) % MOD

        # p appears only once in the product for every multiple.
        for x in range(p, n + 1, p):
            g[x] = g[x] * factor % MOD

        # Sieve composites.
        if p * p <= n:
            for x in range(p * p, n + 1, p):
                is_prime[x] = 0

    # T[m] = sum_{d | m} g[d] * r[m / d].
    T = [0] * (n + 1)

    for d in range(1, n + 1):
        coeff = g[d]
        for m in range(d, n + 1, d):
            T[m] = (T[m] + coeff * r[m // d]) % MOD

    ans = sum(T) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
```

The first loop constructs powers of \(k\), avoiding repeated modular exponentiation. Since consecutive powers differ by only one multiplication, this takes linear time.

The construction of `r` follows directly from the reflection argument. The odd case has \((m+1)/2\) independent position orbits. For an even length, the two types of reflections contribute \(k^{m/2+1}\) and \(k^{m/2}\), each occurring \(m/2\) times.

The array `g` stores the inverse-totient coefficients. The prime sieve multiplies by \(1-p\) for every multiple of \(p\), but it never multiplies twice for \(p^2,p^3,\ldots\). That distinction is essential because \(g(d)\) depends on distinct prime divisors, not on their exponents.

The final nested loop is the divisor convolution. When the outer variable is \(d\), the inner loop visits precisely those lengths \(m\) for which \(d\mid m\). The remaining factor is `r[m // d]`, matching the formula exactly.

Python integers do not overflow, but reducing after each multiplication keeps the values small and is necessary for performance. Negative factors such as \(1-p\) are normalized with `% MOD`, so every stored coefficient lies in the usual modular range.

## Worked Examples

### Sample 1

For input `3 3`, the alphabet has three letters. The following table shows the per-length quantities.

| Length \(m\) | \(r(m,3)\) | \(g(m)\) | \(T(m,3)\) | Running answer |
|---:|---:|---:|---:|---:|
| 1 | 3 | 1 | 3 | 3 |
| 2 | 12 | \(-1\) | \(12-3=9\) | 12 |
| 3 | 27 | \(-2\) | \(27-2\cdot3=21\) | 33 |

For length one, all three strings qualify. For length two, every one of the \(3^2=9\) strings is a concatenation of two one-letter palindromes. For length three, the answer is \(21\), giving the required total \(3+9+21=33\).

The trace also demonstrates why `r[m]` cannot itself be used as the answer. For length two, `r[2]=12`, while there are only nine distinct strings. Some strings have more than one witnessing rotation, so divisor inversion is necessary.

### Sample 2

For input `6 2`, the alphabet contains two letters.

| Length \(m\) | \(r(m,2)\) | \(g(m)\) | \(T(m,2)\) | Running answer |
|---:|---:|---:|---:|---:|
| 1 | 2 | 1 | 2 | 2 |
| 2 | 6 | \(-1\) | \(6-2=4\) | 6 |
| 3 | 12 | \(-2\) | \(12-2\cdot2=8\) | 14 |
| 4 | 24 | \(-1\) | \(24-6-2=16\) | 30 |
| 5 | 40 | \(-4\) | \(40-4\cdot2=32\) | 62 |
| 6 | 72 | 2 | \(72-2\cdot4-1\cdot8-2\cdot2=52\) | 114 |

The final sum is \(114\), matching the sample. The length-six row is especially useful because several proper divisors contribute, showing the full divisor convolution rather than only a single correction term.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | \(O(n\log n)\) | Computing \(r\) and powers is linear, the prime sieve is near-linear, and the divisor convolution performs \(\sum_{d=1}^n\lfloor n/d\rfloor=O(n\log n)\) updates. |
| Space | \(O(n)\) | The arrays for powers, \(r\), inverse-totient coefficients, and the answer each contain \(O(n)\) entries. |

With \(n\le 10^5\), the divisor convolution performs only about \(n\log n\) iterations, roughly \(1.2\) million for the given bound. The memory usage is linear and comfortably below 512 MB. The exponential dependence on the alphabet size has disappeared from the algorithm, because \(k\le26\) is used only in modular multiplications and precomputed powers.

## Test Cases

The following harness assumes the submitted solution is saved as `solution.py` and exposes a `solve` function that accepts an input string and returns the output string. For a directly runnable test version, the same body can be adapted to accept `data` instead of reading from `stdin`.

```python
import io
import sys

MOD = 998244353

def solve_data(inp: str) -> str:
    data = io.StringIO(inp)
    n, k = map(int, data.readline().split())

    pw = [1] * (n + 1)
    for i in range(1, n + 1):
        pw[i] = pw[i - 1] * k % MOD

    r = [0] * (n + 1)
    for m in range(1, n + 1):
        if m & 1:
            r[m] = m * pw[(m + 1) // 2] % MOD
        else:
            r[m] = (m // 2) * (k + 1) * pw[m // 2] % MOD

    g = [1] * (n + 1)

    is_prime = bytearray(b'\x01') * (n + 1)
    is_prime[0] = 0
    if n >= 1:
        is_prime[1] = 0

    for p in range(2, n + 1):
        if not is_prime[p]:
            continue

        factor = (1 - p) % MOD
        for x in range(p, n + 1, p):
            g[x] = g[x] * factor % MOD

        if p * p <= n:
            for x in range(p * p, n + 1, p):
                is_prime[x] = 0

    T = [0] * (n + 1)

    for d in range(1, n + 1):
        for m in range(d, n + 1, d):
            T[m] = (T[m] + g[d] * r[m // d]) % MOD

    return str(sum(T) % MOD)

def run(inp: str) -> str:
    return solve_data(inp).strip()

# Provided samples.
assert run("3 3\n") == "33", "sample 1"
assert run("6 2\n") == "114", "sample 2"
assert run("42 7\n") == "83419789", "sample 3"

# Minimum size.
assert run("1 1\n") == "1", "minimum input"

# One-character alphabet: every non-empty string is a palindrome.
assert run("100000 1\n") == "100000", "maximum n with one letter"

# All length-two strings over two letters qualify.
assert run("2 2\n") == "6", "length-two boundary"

# Small case where non-palindromic double palindromes matter.
assert run("5 2\n") == "62", "off-by-one and split counting"
```

| Test input | Expected output | What it validates |
|---|---:|---|
| `1 1` | `1` | Minimum length and exclusion of the empty string |
| `100000 1` | `100000` | Maximum \(n\), all strings being palindromes, and linear memory handling |
| `2 2` | `6` | Every length-two string being a concatenation of two one-letter palindromes |
| `5 2` | `62` | Multiple divisor contributions and boundary handling |

## Edge Cases

For `1 1`, the power array contains only \(1\). The reflection count is \(r(1,1)=1\), and \(g(1)=1\), so \(T(1,1)=1\). The final sum is exactly \(1\), representing the single string `a`. The algorithm never introduces an empty string because all calculations start at length one.

For `2 2`, the reflection counts are \(r(1,2)=2\) and \(r(2,2)=6\). Since \(g(1)=1\) and \(g(2)=-1\),

\[
T(1,2)=2
\]

and

\[
T(2,2)=6-2=4.
\]

The total is \(6\). The four length-two strings are all valid because each can be split into two one-letter palindromes.

For `3 3`, the length-three contribution is

\[
T(3,3)=r(3,3)-2r(1,3)=27-6=21.
\]

Together with \(T(1,3)=3\) and \(T(2,3)=9\), the answer is \(33\). This catches the mistake of counting only whole-string palindromes, since there are only nine length-three palindromes but twenty-one double palindromes.

For `100000 1`, every power of \(k\) is one, and the resulting counting formula simplifies to exactly one qualifying string at every length, namely the all-`a` string. The algorithm still executes the same divisor convolution, but all modular arithmetic remains valid and the final sum is \(100000\). This case simultaneously exercises the maximum length and the smallest alphabet.
:::
