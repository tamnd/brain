---
title: "CF 1705C - Mark and His Unfinished Essay"
description: "Two constructions are proposed for generating a random variable $X$ with a nontrivial distribution on $[-1,1]$. The first maps a single uniform deviate through a trigonometric transformation."
date: "2026-06-09T21:23:39+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1705
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 807 (Div. 2)"
rating: 1400
weight: 1705
solve_time_s: 162
verified: false
draft: false
---

[CF 1705C - Mark and His Unfinished Essay](https://codeforces.com/problemset/problem/1705/C)

**Rating:** 1400  
**Tags:** brute force, implementation  
**Solve time:** 2m 42s  
**Verified:** no  

## Solution
## Solution

Two constructions are proposed for generating a random variable $X$ with a nontrivial distribution on $[-1,1]$. The first maps a single uniform deviate through a trigonometric transformation. The second uses rejection sampling in the unit disk and then applies a rational transformation of the accepted point.

The question is whether these two procedures induce the same distribution for $X$.

Let $U$ be uniformly distributed on $[0,1]$. Method 1 defines

$$X = \sin\!\left(\frac{\pi}{2}U\right).$$

Since $U$ is uniform, the variable $T = \frac{\pi}{2}U$ is uniform on $\left[0, \frac{\pi}{2}\right]$. The transformation $X = \sin T$ is monotone increasing on this interval, hence the distribution of $X$ is determined by inversion of the mapping.

For $-1 \le x \le 1$, the event $X \le x$ is equivalent to

$$\sin T \le x \quad \Longleftrightarrow \quad T \le \arcsin x,$$

since $\sin T$ is increasing. Therefore

$$\Pr(X \le x) = \Pr\!\left(T \le \arcsin x\right) = \frac{2}{\pi}\arcsin x.$$

Thus Method 1 produces the distribution function

$$F_1(x) = \frac{2}{\pi}\arcsin x.$$

Method 2 generates independent uniform $U, V$ on $[-1,1]$ conditioned on $U^2 + V^2 < 1$. This is the uniform distribution over the unit disk. The joint density is constant over the disk, so the accepted point is radially symmetric. We define

$$X = \frac{U^2 - V^2}{U^2 + V^2}.$$

Introduce polar coordinates on the disk. Let

$$U = R\cos\Theta, \quad V = R\sin\Theta,$$

where $R \in [0,1]$ and $\Theta \in [0,2\pi)$, with $\Theta$ uniform and independent of $R^2$ in the sense induced by area measure. Then

$$X = \frac{R^2\cos^2\Theta - R^2\sin^2\Theta}{R^2\cos^2\Theta + R^2\sin^2\Theta}
= \frac{\cos^2\Theta - \sin^2\Theta}{1}
= \cos(2\Theta).$$

The radial variable cancels completely. The distribution of $X$ is therefore determined solely by $\Theta$, which is uniform on $[0,2\pi)$.

Let $T = 2\Theta$, so $T$ is uniform on $[0,4\pi)$. Since $\cos T$ has period $2\pi$, restricting to one period gives an equivalent representation with $T$ uniform on $[0,2\pi)$. Hence we can compute the distribution of $X = \cos T$ with $T \sim \mathrm{Unif}[0,2\pi)$.

For $-1 \le x \le 1$,

$$\Pr(X \le x) = \Pr(\cos T \le x).$$

On $[0,2\pi)$, the set ${\cos T \le x}$ consists of two symmetric arcs whose total length is $2\pi - 2\arccos x$. Therefore

$$F_2(x) = 1 - \frac{1}{\pi}\arccos x.$$

Using the identity $\arccos x = \frac{\pi}{2} - \arcsin x$, we obtain

$$F_2(x) = 1 - \frac{1}{\pi}\left(\frac{\pi}{2} - \arcsin x\right)
= \frac{1}{2} + \frac{1}{\pi}\arcsin x.$$

Now compare the two distribution functions.

Method 1 gives

$$F_1(x) = \frac{2}{\pi}\arcsin x,$$

while Method 2 gives

$$F_2(x) = \frac{1}{2} + \frac{1}{\pi}\arcsin x.$$

These functions are not equal. For instance, at $x=0$,

$$F_1(0) = 0, \qquad F_2(0) = \frac{1}{2}.$$

Since the distribution functions differ at a point in their support, the induced distributions are not the same.

This completes the solution. ∎
