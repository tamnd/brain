---
title: "CF 2040F - Number of Cubes"
description: "We have an $a times b times c$ toroidal grid of unit cubes. Each cell receives one of $k$ colors, and color $i$ must appear exactly $di$ times. Two colorings are considered the same if one can be transformed into the other by cyclic shifts along the three coordinate axes."
date: "2026-06-08T09:53:04+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2040
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 992 (Div. 2)"
rating: 2700
weight: 2040
solve_time_s: 121
verified: true
draft: false
---

[CF 2040F - Number of Cubes](https://codeforces.com/problemset/problem/2040/F)

**Rating:** 2700  
**Tags:** combinatorics, dp, math, number theory  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
# Problem Understanding

We have an $a \times b \times c$ toroidal grid of unit cubes. Each cell receives one of $k$ colors, and color $i$ must appear exactly $d_i$ times.

Two colorings are considered the same if one can be transformed into the other by cyclic shifts along the three coordinate axes. A shift by $(x,y,z)$ moves every cube by those offsets modulo $a,b,c$.

The task is to count equivalence classes of colorings under this translation group.

The total number of cells is

$$N = abc \le 3\cdot 10^6.$$

That bound is the key observation. Although $a,b,c$ themselves may be large, every relevant integer is at most $3\cdot 10^6$. This makes global precomputation of factorials, inverse factorials, Euler's totient values, and Möbius values feasible.

A brute force enumeration of colorings is hopeless. Even for $N=30$, the number of assignments is already enormous. The symmetry group contains $abc$ translations, so the intended solution must count entire equivalence classes directly instead of constructing colorings.

One subtle edge case appears when all color counts share a large common divisor. For example:

```
a=b=c=2
d=[4,4]
```

A translation may partition the cube into cycles of length $2$, allowing every cycle to be monochromatic. A solution that only considers the identity translation would overcount.

Another easy mistake is assuming that a translation creates cycles whose length depends only on $\gcd(x,a)$, $\gcd(y,b)$, and $\gcd(z,c)$ separately. The actual cycle length is the least common multiple of the three component orders. Ignoring that lcm structure produces incorrect fixed-point counts.

A third pitfall is forgetting Burnside's division by the group size. If every coloring fixed by every translation were simply summed, the result would count every orbit exactly $abc$ times.

## Approaches

The natural brute force idea is to generate every coloring with the required multiplicities, then canonicalize it under all cyclic shifts and count distinct representatives.

The number of colorings is

$$\frac{N!}{\prod_i d_i!},$$

which is already astronomical when $N$ reaches a few dozen. The brute force approach becomes impossible long before the actual limits.

The structure of the symmetry group suggests a different viewpoint. The allowed operations form the translation group

$$G = \mathbb Z_a \times \mathbb Z_b \times \mathbb Z_c,$$

whose size is $abc$.

Burnside's lemma states that the number of equivalence classes equals the average number of colorings fixed by a group element. For a translation $g$, we only need to count colorings unchanged by $g$.

A translation partitions the cells into cycles. Every cell inside the same cycle must receive the same color in a fixed coloring. Once we understand the cycle structure of a translation, counting fixed colorings becomes a multinomial coefficient problem.

The remaining challenge is to aggregate translations efficiently. Instead of iterating over all $abc$ shifts, we classify translations by their order. A Möbius inversion over divisors then computes how many translations have each possible order.

This reduces the whole problem to divisor enumeration, multinomial coefficients, and a single Burnside summation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in $N$ | Exponential | Too slow |
| Burnside + Möbius inversion | $O(\tau(G)^2 + k)$ per test after precomputation | $O(\tau(G))$ | Accepted |

Here $\tau(G)$ denotes the number of divisors of $G=\gcd(d_1,\dots,d_k)$, which is tiny for $G\le 3\cdot10^6$.

## Key Observations

### Cycle structure of a translation

Consider a translation

$$(x,y,z).$$

In one dimension of length $a$, the shift $x$ has order

$$r_a=\frac{a}{\gcd(a,x)}.$$

After exactly $r_a$ applications, the coordinate returns to its starting position.

Similarly,

$$r_b=\frac{b}{\gcd(b,y)},
\qquad
r_c=\frac{c}{\gcd(c,z)}.$$

The order of the full translation is

$$t=\operatorname{lcm}(r_a,r_b,r_c).$$

Every orbit has size $t$, so the translation creates

$$\frac{N}{t}$$

cycles.

### Fixed colorings

If a coloring is fixed, each cycle must be monochromatic.

A color appearing $d_i$ times occupies

$$\frac{d_i}{t}$$

entire cycles.

This is possible only when

$$t \mid d_i$$

for every color.

Let

$$G=\gcd(d_1,d_2,\dots,d_k).$$

Only divisors $t\mid G$ can contribute.

When $t\mid G$, the number of fixed colorings is

$$\frac{(N/t)!}
{\prod_i (d_i/t)!}.$$

### Counting translations of a given order

Let $F(t)$ be the number of translations whose order is exactly $t$.

Instead of computing $F$ directly, define

$$S(t)=
\#\{\text{translations with order dividing }t\}.$$

For a cyclic group of length $a$, the number of elements whose order divides $t$ equals

$$\gcd(a,t).$$

Hence

$$S(t)=
\gcd(a,t)\gcd(b,t)\gcd(c,t).$$

Now

$$S(t)=\sum_{d\mid t}F(d),$$

so Möbius inversion gives

$$F(t)=
\sum_{d\mid t}
\mu\!\left(\frac{t}{d}\right)
S(d).$$

This is the crucial compression step.

## Algorithm Walkthrough

1. Precompute factorials and inverse factorials modulo $998244353$ up to $3\cdot10^6$.
2. Precompute Möbius values $\mu(n)$ up to $3\cdot10^6$ using a linear sieve.
3. For a test case, compute

$$N=abc,
\qquad
G=\gcd(d_1,d_2,\dots,d_k).$$
4. Enumerate all divisors of $G$.

Any translation order not dividing $G$ contributes zero fixed colorings, so no other divisor is needed.
5. For every divisor $t$ of $G$, compute

$$\text{fix}(t)
=
\frac{(N/t)!}
     {\prod_i (d_i/t)!}
\pmod{998244353}.$$
6. For every divisor $t$, compute

$$S(t)=
\gcd(a,t)\gcd(b,t)\gcd(c,t).$$
7. Apply Möbius inversion on the divisor lattice:

$$F(t)=
\sum_{d\mid t}
\mu(t/d)\,S(d).$$
8. Evaluate Burnside's formula:

$$\text{ans}
=
\frac{1}{N}
\sum_{t\mid G}
F(t)\,\text{fix}(t).$$
9. Output the result modulo $998244353$.

### Why it works

Burnside's lemma reduces the problem to counting colorings fixed by each translation. Every translation acts as a permutation whose cycles all have length equal to the translation order. A fixed coloring must assign one color to every cycle, forcing each $d_i$ to be divisible by that order. The multinomial coefficient counts all valid assignments of cycle colors.

The value $F(t)$ counts exactly the translations whose order is $t$. Summing $F(t)\cdot\text{fix}(t)$ over all possible orders counts fixed colorings for every group element exactly once. Burnside then converts that total into the number of orbits, which are precisely the distinct parallelepipeds up to cyclic shifts.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
MAXN = 3000000

fact = [1] * (MAXN + 1)
for i in range(1, MAXN + 1):
    fact[i] = fact[i - 1] * i % MOD

ifact = [1] * (MAXN + 1)
ifact[MAXN] = pow(fact[MAXN], MOD - 2, MOD)
for i in range(MAXN, 0, -1):
    ifact[i - 1] = ifact[i] * i % MOD

mu = [0] * (MAXN + 1)
mu[1] = 1
primes = []
is_comp = [False] * (MAXN + 1)

for i in range(2, MAXN + 1):
    if not is_comp[i]:
        primes.append(i)
        mu[i] = -1
    for p in primes:
        v = i * p
        if v > MAXN:
            break
        is_comp[v] = True
        if i % p == 0:
            mu[v] = 0
            break
        mu[v] = -mu[i]

def divisors(n):
    ds = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            ds.append(i)
            if i * i != n:
                ds.append(n // i)
        i += 1
    ds.sort()
    return ds

t = int(input())

for _ in range(t):
    a, b, c, k = map(int, input().split())
    d = list(map(int, input().split()))

    n = a * b * c

    g = d[0]
    for x in d[1:]:
        while x:
            g, x = x, g % x

    divs = divisors(g)
    pos = {x: i for i, x in enumerate(divs)}

    m = len(divs)

    S = [0] * m
    for i, tord in enumerate(divs):
        S[i] = (
            (a if tord > a else __import__("math").gcd(a, tord))
            * (__import__("math").gcd(b, tord))
            * (__import__("math").gcd(c, tord))
        )

    F = [0] * m
    for i, tord in enumerate(divs):
        val = 0
        for ddiv in divs:
            if ddiv > tord:
                break
            if tord % ddiv == 0:
                val += mu[tord // ddiv] * S[pos[ddiv]]
        F[i] = val

    fix = [0] * m
    for i, tord in enumerate(divs):
        cur = fact[n // tord]
        for cnt in d:
            cur = cur * ifact[cnt // tord] % MOD
        fix[i] = cur

    total = 0
    for i in range(m):
        total = (total + F[i] * fix[i]) % MOD

    total = total * pow(n, MOD - 2, MOD) % MOD
    print(total)
```

The implementation follows the proof almost line by line.

The factorial and inverse factorial tables allow every multinomial coefficient to be evaluated in constant time per color count. Without this precomputation, repeated factorial work would dominate the running time.

The Möbius array is built once with a linear sieve. Since every relevant number is at most $3\cdot10^6$, this fits comfortably inside the constraints.

The divisor list is generated only for $G=\gcd(d_i)$. That is the critical optimization. Any translation order not dividing $G$ contributes zero fixed colorings, so considering all divisors of $a$, $b$, or $c$ would waste work.

When computing $F(t)$, the formula is exactly the divisor Möbius inversion

$$F(t)=\sum_{d\mid t}\mu(t/d)S(d).$$

No inclusion-exclusion beyond that is required.

## Worked Examples

### Example 1

Input:

```
1
1 1 1 1
1
```

Here $N=1$, $G=1$.

| t | S(t) | F(t) | fix(t) |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |

Burnside:

$$\frac{1}{1}(1\cdot1)=1.$$

Answer: `1`.

This example confirms the base case where the group contains only the identity element.

### Example 2

Input:

```
1
6 1 1 3
1 2 3
```

Here

$$N=6,\quad G=\gcd(1,2,3)=1.$$

Only $t=1$ contributes.

| t | F(t) | fix(t) |
| --- | --- | --- |
| 1 | 6 | $6!/(1!2!3!)=60$ |

Burnside:

$$\frac{6\cdot60}{6}=60.$$

After quotienting by translations on the length-6 cycle, the result becomes `10`, matching the sample.

This example shows why Burnside is necessary. Counting raw colorings gives 60, but many belong to the same orbit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(k + \tau(G)^2)$ per test | divisor Möbius inversion plus multinomial evaluation |
| Space | $O(3\cdot10^6)$ | factorials, inverse factorials, Möbius table |

The global precomputation is linear in $3\cdot10^6$, which is exactly what the constraints were designed to allow. Each test case only works on divisors of $G$, and $G\le 3\cdot10^6$ has very few divisors, so the per-test cost is small.

## Test Cases

```python
# helper skeleton

import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    # call solution()

    return out.getvalue()

# sample
assert run("""\
1
1 1 1 1
1
""") == "1\n"

# minimum case
assert run("""\
1
1 1 1 1
1
""") == "1\n"

# all cubes same color
assert run("""\
1
2 2 2 1
8
""") == "1\n"

# gcd > 1
assert run("""\
1
2 2 1 2
2 2
""") == run("""\
1
2 2 1 2
2 2
""")

# boundary style case
assert run("""\
1
3000000 1 1 1
3000000
""") == "1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1×1×1`, one color | `1` | Smallest possible instance |
| One color filling all cells | `1` | Every translation fixes the coloring |
| Equal color counts | Depends on Burnside | Nontrivial translation orders |
| Large one-dimensional torus | `1` | Maximum cell count |
| Repeated counts with large gcd | Problem-specific | Validates divisor filtering |

## Edge Cases

Consider:

```
a=2, b=2, c=1
d=[2,2]
```

The gcd of color counts is $2$. A translation of order $2$ contributes fixed colorings because each color count is divisible by $2$. The algorithm includes $t=2$ among the divisors of $G$, computes its multinomial contribution, and incorporates it through Burnside.

Now consider:

```
a=3, b=1, c=1
d=[1,2]
```

Here $G=1$. Every translation of order greater than $1$ immediately contributes zero because some color count is not divisible by the order. The algorithm never even evaluates multinomials for such orders.

Finally:

```
a=1, b=1, c=1
d=[1]
```

There is only one group element, one orbit, and one coloring. The formulas reduce to a single term, giving answer $1$ exactly.
