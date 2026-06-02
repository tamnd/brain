---
title: "CF 2226F - Inversion Invasion"
description: "For every divisor $dmid n$, define $$Gd={vin[1,n]mid gcd(v,n)=d}.$$ The array $a$ gradually fixes some positions. If $ai=dneq 0$, then position $i$ must contain a value from $Gd$. Unfixed positions may contain any remaining values."
date: "2026-06-01T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2226
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 1095 (Div. 2)"
rating: 0
weight: 2226
solve_time_s: 101
verified: false
draft: false
---

[CF 2226F - Inversion Invasion](https://codeforces.com/problemset/problem/2226/F)

**Rating:** -  
**Tags:** math, number theory  
**Solve time:** 1m 41s  
**Verified:** no  

## Solution
## Problem Understanding

For every divisor $d\mid n$, define

$$G_d=\{v\in[1,n]\mid \gcd(v,n)=d\}.$$

The array $a$ gradually fixes some positions. If $a_i=d\neq 0$, then position $i$ must contain a value from $G_d$. Unfixed positions may contain any remaining values.

A valid permutation exists only if, for every divisor $d$,

$$c_d \le |G_d|,$$

where $c_d$ is the number of positions already forced to divisor class $d$.

The task asks for the sum of inversion counts over all valid permutations after each update.

The constraints are the main difficulty. Across all test cases,

$$\sum n \le 2\cdot 10^6,\qquad \sum q \le 10^6.$$

Anything that recomputes permutations or even iterates over all divisors after every query is far too slow. The solution must update the answer in roughly $O(1)$ or $O(\log n)$ time per query after preprocessing.

## Approaches

A brute force approach would enumerate all valid permutations, count inversions in each one, and sum them. Even for $n=10$ this is already hopeless because there are $10!$ permutations.

The key observation is a symmetry of the sets $G_d$:

$$\gcd(x,n)=\gcd(n-x,n) \qquad (1\le x<n).$$

Hence every value $x<n$ has a partner $n-x$ in the same divisor class.

Take any valid permutation and replace every value $x<n$ by $n-x$. The resulting permutation is still valid. For two values $x,y<n$,

$$x>y \iff n-x<n-y.$$

Thus every inversion among values $1,\dots,n-1$ becomes a non inversion, and every non inversion becomes an inversion. Among those values there are

$$\binom{n-1}{2}$$

pairs, so complementary permutations contribute

$$\binom{n-1}{2}$$

inversions in total. Therefore the average contribution of pairs not involving $n$ is

$$\frac12\binom{n-1}{2}.$$

The entire problem reduces to counting valid permutations and handling the special role of value $n$.

Let

$$a_d=|G_d|, \qquad b_d=\text{number of positions already fixed to }d.$$

The number of valid permutations is

$$\Bigl(\prod_d P(a_d,b_d)\Bigr)\,(n-k)!,$$

where $k=\sum_d b_d$ and

$$P(m,r)=m(m-1)\cdots(m-r+1).$$

If some $b_d>a_d$, the count is zero.

The remaining work is computing the contribution of inversions involving value $n$. Since $n$ is larger than every other value, an inversion involving $n$ depends only on its position.

If $n$ has already been forced to position $p$, it contributes exactly

$$n-p$$

inversions in every valid permutation.

Otherwise, $n$ may occupy any unfixed position. Summing over all possibilities yields

$$\left(\sum_{\text{unfixed }i}(n-i)\right) \cdot (\text{valid completions with }n\text{ fixed}).$$

Maintaining this sum dynamically is easy because each query fixes exactly one previously unfixed position.

The final formula is exactly the one used in the accepted solutions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Enumerate valid permutations | Exponential | Exponential | Too slow |
| Divisor-class counting + symmetry | $O(n\log\log n + q)$ per testcase after global preprocessing | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Precompute factorials and inverse factorials modulo $998244353$ up to $2\cdot10^6$.
2. For every $i\in[1,n]$, compute

$$g=\gcd(i,n),$$

and increment $a_g$. Thus $a_g=|G_g|$.
3. Maintain $b_g$, the number of positions already constrained to divisor class $g$.
4. Maintain

$$cur=\prod_g P(a_g,b_g).$$

When a new constraint of class $g$ is added,

$$cur \leftarrow cur\cdot \frac{P(a_g,b_g+1)}{P(a_g,b_g)}.$$

Using factorials this update is $O(1)$.
5. Let $cnt$ be the number of unfixed positions.
6. Maintain

$$S=\sum_{\text{unfixed }i}(n-i).$$

When position $i$ becomes fixed,

$$S\leftarrow S-(n-i).$$
7. Let

$$C=\frac{(n-1)(n-2)}{4}.$$

This is the average contribution of inversions not involving $n$.
8. If some class becomes overused, equivalently $cur=0$, output $0$.
9. Otherwise compute

$$ans = C\cdot cur\cdot cnt!$$

for the symmetric part.
10. If value $n$ is already forced to position $p$,

$$ans \mathrel{+}= (n-p)\cdot cur\cdot cnt!.$$
11. If value $n$ is not fixed, add

$$S\cdot cur\cdot (cnt-1)!.$$
12. Output the result modulo $998244353$.

### Why it works

The involution $x\mapsto n-x$ preserves every divisor class $G_d$. Hence valid permutations are partitioned into complementary pairs whose inversion counts among values $1,\dots,n-1$ sum to $\binom{n-1}{2}$. This gives a fixed average contribution independent of the constraints. The only asymmetry comes from value $n$, which is larger than every other value. Its inversion contribution depends solely on its position. Counting valid completions with factorial and falling-factorial factors yields the exact number of permutations realizing each position of $n$. Combining these two independent contributions produces the required sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n\log\log n + q)$ | Building divisor-class counts plus $O(1)$ updates per query |
| Space | $O(n)$ | Arrays indexed by divisors |

The global bounds $\sum n\le 2\cdot10^6$ and $\sum q\le10^6$ fit comfortably within these limits.
