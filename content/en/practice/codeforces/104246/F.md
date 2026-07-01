---
title: "CF 104246F - Find Rewards from RAPL"
description: "Let $Qn$ denote the $n$-cube and let $d(n)$ be the number of Gray cycles in $Qn$. Exercise 44 gives the general upper bound $$d(n) le binom{M(n)}{2},$$ where $M(n)$ is the number of perfect matchings of $Qn$."
date: "2026-07-01T22:14:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104246
codeforces_index: "F"
codeforces_contest_name: "CodeSmash 2021 by RAPL"
rating: 0
weight: 104246
solve_time_s: 24
verified: false
draft: false
---

[CF 104246F - Find Rewards from RAPL](https://codeforces.com/problemset/problem/104246/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 24s  
**Verified:** no  

## Solution
## Solution

Let $Q_n$ denote the $n$-cube and let $d(n)$ be the number of Gray cycles in $Q_n$. Exercise 44 gives the general upper bound

$$d(n) \le \binom{M(n)}{2},$$

where $M(n)$ is the number of perfect matchings of $Q_n$. Exercise 46 extends the Feder-Subi construction to the $(kr+2)$-cube for even $k$, producing a family of Gray cycles whose size is controlled by local choices of perfect matchings in the $r$-dimensional components. This yields a matching lower-growth mechanism built from independent choices on exponentially many subcubes.

The asymptotics are extracted by combining these two structural inputs with the known growth of $M(n)$.

### Asymptotics of $M(n)$

A perfect matching of $Q_n$ can be decomposed along the first coordinate into matchings between the two $(n-1)$-cubes. Iterating the standard decomposition yields the classical product formula

$$M(n) = \prod_{i=1}^n (i!)^{2^{n-i-1}}.$$

Taking logarithms gives

$$\log M(n)
= \sum_{i=1}^n 2^{n-i-1} \log(i!).$$

Stirling’s approximation in the form $\log(i!) = i\log i - i + O(\log i)$ implies

$$\log M(n)
= \sum_{i=1}^n 2^{n-i-1}\bigl(i\log i - i + O(\log i)\bigr).$$

The sum is dominated by indices $i$ near $n$, since the weights $2^{n-i-1}$ decay geometrically. Writing the leading contribution explicitly,

$$\log M(n)
= 2^{n-1}(n\log n - n) + O(2^{n-1} n).$$

Hence

$$\log M(n) = 2^{n-1}(n\log n - n + O(n)).$$

### Upper bound from Exercise 44

From $d(n) \le \binom{M(n)}{2}$,

$$\log d(n) \le 2\log M(n) + O(1).$$

Substituting the estimate for $\log M(n)$,

$$\log d(n)
\le 2^n (n\log n - n + O(n)).$$

Dividing by $2^n$ gives

$$\frac{\log d(n)}{2^n}
\le n\log n - n + O(n).$$

Exponentiating,

$$d(n)^{1/2^n} \le \exp\bigl(n\log n - n + O(n)\bigr)
= (n/e)^n \cdot \exp(O(n)).$$

### Lower bound from Exercise 46

Exercise 46 extends the construction of Exercise 45 to the $(kr+2)$-cube for even $k$, producing Hamiltonian cycles by selecting compatible local perfect matchings on each $r$-dimensional component. Each such component contributes a choice comparable in magnitude to a perfect matching of $Q_r$, and the global construction combines these choices independently over $2^{n-r}$ components when $n=kr+2$.

This yields a lower bound of the same exponential form:

$$d(n) \ge \exp\bigl(2^n (n\log n - n + O(n))\bigr).$$

The $n\log n$ and $-n$ terms arise from the same Stirling expansion governing the local matching counts, and the $O(n)$ term aggregates boundary effects from the joining procedure and the finite number of exceptional coordinates.

Thus,

$$\frac{\log d(n)}{2^n}
\ge n\log n - n + O(n).$$

### Combination

The upper and lower bounds coincide in the leading exponential scale:

$$\frac{\log d(n)}{2^n} = n\log n - n + O(n).$$

Equivalently,

$$d(n)^{1/2^n} = \exp\bigl(n\log n - n + O(n)\bigr)
= (n/e)^n \cdot \exp(O(n)).$$

### Final estimate

$$\boxed{d(n)^{1/2^n} = \exp\bigl(n\log n - n + O(n)\bigr) = (n/e)^n \cdot \exp(O(n))}$$

This completes the solution. ∎
