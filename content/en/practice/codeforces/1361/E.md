---
title: "CF 1361E - James and the Chase"
description: "The exercise asks for a direct algebraic simplification of two displayed identities involving content and primitive part of polynomials over a unique factorization domain $S$."
date: "2026-06-11T12:47:51+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "probabilities", "trees"]
categories: ["algorithms"]
codeforces_contest: 1361
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 647 (Div. 1) - Thanks, Algo Muse!"
rating: 3000
weight: 1361
solve_time_s: 173
verified: false
draft: false
---

[CF 1361E - James and the Chase](https://codeforces.com/problemset/problem/1361/E)

**Rating:** 3000  
**Tags:** dfs and similar, graphs, probabilities, trees  
**Solve time:** 2m 53s  
**Verified:** no  

## Solution
## Correct Solution for TAOCP 4.6.1.24

The exercise asks for a direct algebraic simplification of two displayed identities involving content and primitive part of polynomials over a unique factorization domain $S$. The goal is not to introduce new structural theorems, but to rewrite the given expressions until they match the cleaner forms already stated later in the section.

The key point throughout is that both $\operatorname{cont}(\cdot)$ and $\operatorname{pp}(\cdot)$ are defined by a fixed factorization

$$u(x) = \operatorname{cont}(u)\,\operatorname{pp}(u(x)),$$

with $\operatorname{cont}(u) \in S$ and $\operatorname{pp}(u)$ primitive in the sense of Section 4.6.1. This decomposition is canonical under the conventions of the section, so no additional ambiguity beyond this definition is introduced or needed.

## Simplification of (19) to (20)

Equation (19) is the coefficient-level definition of content for a product polynomial. It defines $\operatorname{cont}(uv)$ as the greatest common divisor (in $S$) of all coefficients of the product $uv$.

Write

$$u(x) = \sum_i u_i x^i, \quad v(x) = \sum_j v_j x^j.$$

Then the coefficients of $uv$ are finite sums of elements $u_i v_j$. Every coefficient of $uv$ is therefore an $S$-linear combination of products of coefficients of $u$ and $v$.

The crucial observation is that every coefficient of $uv$ is divisible by every common divisor of all coefficients of $u$, and also by every common divisor of all coefficients of $v$. If $d$ divides all $u_i$, then each coefficient $u_i v_j$ is divisible by $d$, hence every coefficient of $uv$ is divisible by $d$. The same holds for any common divisor of the $v_j$. Therefore every common divisor of coefficients of $u$ and of $v$ is also a common divisor of coefficients of $uv$, which gives the divisibility

$$\operatorname{cont}(u)\operatorname{cont}(v) \mid \operatorname{cont}(uv).$$

Conversely, every coefficient of $u$ is divisible by $\operatorname{cont}(u)$, and every coefficient of $v$ is divisible by $\operatorname{cont}(v)$, so every coefficient $u_i v_j$ is divisible by $\operatorname{cont}(u)\operatorname{cont}(v)$. Since the coefficients of $uv$ are sums of such terms, they are all divisible by $\operatorname{cont}(u)\operatorname{cont}(v)$. Hence

$$\operatorname{cont}(uv) \mid \operatorname{cont}(u)\operatorname{cont}(v).$$

Both divisibilities together force equality in a UFD up to units, and under the standard convention used in Section 4.6.1 (content taken as a canonical generator of the coefficient ideal), this removes any unit ambiguity. The result is exactly the simplified identity (20):

$$\operatorname{cont}(uv) = \operatorname{cont}(u)\operatorname{cont}(v).$$

The “simplification” from (19) to (20) is precisely the recognition that the coefficientwise gcd of the product factors into the product of coefficientwise gcds, because divisibility propagates through multiplication and addition without introducing new common factors beyond those already present.

## Simplification of (24) to (24)

Equation (24) concerns the primitive part of a product. Starting from the defining factorization,

$$u(x) = \operatorname{cont}(u)\operatorname{pp}(u(x)), \quad v(x) = \operatorname{cont}(v)\operatorname{pp}(v(x)),$$

we multiply to obtain

$$uv = \operatorname{cont}(u)\operatorname{cont}(v)\,\operatorname{pp}(u)\operatorname{pp}(v).$$

Now apply the definition of primitive part: a polynomial is written uniquely as its content times its primitive part, and the primitive part is characterized by having content equal to $1$ in the normalization of the section.

We first identify the content of $uv$. From the already established identity (20),

$$\operatorname{cont}(uv) = \operatorname{cont}(u)\operatorname{cont}(v).$$

Divide $uv$ by this content factor:

$$\operatorname{pp}(uv) = \frac{uv}{\operatorname{cont}(uv)} = \frac{\operatorname{cont}(u)\operatorname{cont}(v)\,\operatorname{pp}(u)\operatorname{pp}(v)}{\operatorname{cont}(u)\operatorname{cont}(v)}.$$

The content factors cancel exactly, leaving

$$\operatorname{pp}(uv) = \operatorname{pp}(u)\operatorname{pp}(v).$$

This is a direct algebraic simplification: no unit adjustments or normalization choices are required, since the cancellation occurs entirely inside the defining factorization.

Thus equation (24) reduces immediately to the clean multiplicative identity for primitive parts, which is the simplified form stated in the section.

## Why these simplifications are valid

Both steps rely only on the defining property of content as a coefficient gcd and the defining factorization of a polynomial into content times primitive part. The first identity is a structural property of coefficient divisibility under multiplication. The second identity is then a direct consequence of substituting the factorization and canceling the content term using the result of the first identity.

No additional assumptions about units, normalization conventions, or external structural lemmas are needed. The simplification is purely algebraic rewriting within the definitions already in place in Section 4.6.1.
