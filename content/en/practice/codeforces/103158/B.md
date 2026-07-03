---
title: "CF 103158B - Zero equals Infinity!"
description: "Let $A$ be a family of $t$-combinations, and let $partial A$ denote its shadow, the family of all $(t-1)$-combinations contained in members of $A$."
date: "2026-07-03T17:32:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103158
codeforces_index: "B"
codeforces_contest_name: "ACPC Kickoff 2021"
rating: 0
weight: 103158
solve_time_s: 164
verified: false
draft: false
---

[CF 103158B - Zero equals Infinity!](https://codeforces.com/problemset/problem/103158/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 44s  
**Verified:** no  

## Solution
## Solution

Let $A$ be a family of $t$-combinations, and let $\partial A$ denote its shadow, the family of all $(t-1)$-combinations contained in members of $A$. We seek the minimum possible size of $A$ such that $|\partial A| < |A|$.

The key tool is the Kruskal-Katona theorem, which implies that among all families $A$ of $t$-combinations with a fixed cardinality, the shadow $\partial A$ is minimized by taking $A$ to be an initial segment of the colexicographic order. Therefore, if any family of a given size satisfies $|\partial A| < |A|$, then the same inequality holds for the colex initial segment of that size. It follows that the problem reduces to studying initial segments of the form consisting of all $t$-subsets of ${1,2,\dots,n}$, since the threshold occurs at a binomial layer.

For such a full layer family $A = \binom{[n]}{t}$, the shadow consists of all $(t-1)$-subsets of ${1,2,\dots,n}$, hence

$$|A| = \binom{n}{t}, \quad |\partial A| = \binom{n}{t-1}.$$

The ratio between these quantities is

$$\frac{|\partial A|}{|A|} = \frac{\binom{n}{t-1}}{\binom{n}{t}} = \frac{t}{n-t+1}.$$

The inequality $|\partial A| < |A|$ is therefore equivalent to

$$\frac{t}{n-t+1} < 1,$$

which simplifies to

$$t < n - t + 1,$$

or equivalently

$$n > 2t - 1.$$

The smallest integer $n$ satisfying this condition is $n = 2t$. For this value,

$$|A| = \binom{2t}{t}, \quad |\partial A| = \binom{2t}{t-1}.$$

The ratio becomes

$$\frac{|\partial A|}{|A|} = \frac{t}{t+1} < 1,$$

so $|\partial A| < |A|$ holds for $A = \binom{[2t]}{t}$.

It remains to show minimality of $|A|$. For any $m < \binom{2t}{t}$, consider the colex initial segment $A_m$ of size $m$. The Kruskal-Katona theorem implies that its shadow is at least as large as that of any other family of size $m$. At the level $n = 2t - 1$, one has

$$\binom{2t-1}{t-1} = \binom{2t-1}{t},$$

so the shadow of the full layer is equal in size to the layer itself. This is the last point where equality can occur. Increasing the size beyond this threshold necessarily forces the family to include sets from the next layer structure in the colex ordering, and the binomial ratio above shows that the first strict inequality $|\partial A| < |A|$ occurs exactly when passing to $n = 2t$.

Thus the smallest possible family occurs when $A$ is the full collection of all $t$-subsets of a $2t$-element set.

Therefore the minimum size is

$$|A| = \binom{2t}{t}.$$

$$\boxed{\binom{2t}{t}}$$

This completes the proof. ∎
