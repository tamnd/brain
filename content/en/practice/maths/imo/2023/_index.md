---
title: "IMO 2023"
description: "IMO 2023 — 6/6 solved."
tags: ["imo", "mathematics", "olympiad"]
categories: ["mathematics"]
imo_year: 2023
weight: 2023
draft: false
---

# IMO 2023

[Official IMO 2023 problems](https://www.imo-official.org/year_info.aspx?year=2023) &nbsp;·&nbsp; 6/6 solved.

| # | Status | Time |
|---|--------|------|
| [1](1.md) | solved | 1m14s |
| [2](2.md) | solved | 1m11s |
| [3](3.md) | solved | 1m49s |
| [4](4.md) | solved | 1m50s |
| [5](5.md) | solved | 43s |
| [6](6.md) | solved | 1m23s |

**Problem 1** &nbsp; *solved* · 1m14s · [Solution →](1.md)

Determine all composite integers $n>1$ that satisfy the following property: if $d_1,d_2,\dots,d_k$ are all the positive divisors of $n$ with $1=d_1<d_2<\dots<d_k=n$, then $d_i$ divides $d_{i+1}+d_{i+2}$ for every $1\le i \le k-2$.

**Problem 2** &nbsp; *solved* · 1m11s · [Solution →](2.md)

Let $ABC$ be an acute-angled triangle with $AB < AC$. Let $\Omega$ be the circumcircle of $ABC$. Let $S$ be the midpoint of the arc $CB$ of $\Omega$ containing $A$. The perpendicular from $A$ to $BC$ meets $BS$ at $D$ and meets $\Omega$ again at $E \neq A$. The line through $D$ parallel to $BC$ meets line $BE$ at $L$. Denote the circumcircle of triangle $BDL$ by $\omega$. Let $\omega$ meet $\Omega$ again at $P \neq B$. Prove that the line tangent to $\omega$ at $P$ meets line $BS$ on the internal angle bisector of $\angle BAC$.

**Problem 3** &nbsp; *solved* · 1m49s · [Solution →](3.md)

For each integer $k \geqslant 2$, determine all infinite sequences of positive integers $a_1, a_2, \ldots$ for which there exists a polynomial $P$ of the form $P(x)=x^k+c_{k-1} x^{k-1}+\cdots+c_1 x+c_0$, where $c_0, c_1, \ldots, c_{k-1}$ are non-negative integers, such that
$$
P\left(a_n\right)=a_{n+1} a_{n+2} \cdots a_{n+k}
$$
for every integer $n \geqslant 1$.

**Problem 4** &nbsp; *solved* · 1m50s · [Solution →](4.md)

Let $x_1, x_2, \cdots , x_{2023}$ be pairwise different positive real numbers such that
$$
a_n = \sqrt{(x_1+x_2+ \text{···} +x_n)(\frac1{x_1} + \frac1{x_2} + \text{···} +\frac1{x_n})}
$$
is an integer for every $n = 1,2,\cdots,2023$. Prove that $a_{2023} \ge 3034$.

**Problem 5** &nbsp; *solved* · 43s · [Solution →](5.md)

Let $n$ be a positive integer. A Japanese triangle consists of $1 + 2 + \dots + n$ circles arranged in an equilateral triangular shape such that for each $i = 1$, $2$, $\dots$, $n$, the $i^{th}$ row contains exactly $i$ circles, exactly one of which is coloured red. A ninja path in a Japanese triangle is a sequence of $n$ circles obtained by starting in the top row, then repeatedly going from a circle to one of the two circles immediately below it and finishing in the bottom row. Here is an example of a Japanese triangle with $n = 6$, along with a ninja path in that triangle containing two red circles.

![[asy] // credit to vEnhance for the diagram (which was better than my original asy): size(4cm);   pair X = dir(240); pair Y = dir(0);   path c = scale(0.5)*unitcircle;   int[] t = {0,0,2,2,3,0};   for (int i=0; i<=5; ++i) {     for (int j=0; j<=i; ++j) {       filldraw(shift(i*X+j*Y)*c, (t[i]==j) ? lightred : white);       draw(shift(i*X+j*Y)*c);     }   }   draw((0,0)--(X+Y)--(2*X+Y)--(3*X+2*Y)--(4*X+2*Y)--(5*X+2*Y),linewidth(1.5));   path q = (3,-3sqrt(3))--(-3,-3sqrt(3));   draw(q,Arrows(TeXHead, 1));   label("$n = 6$", q, S); label("$n = 6$", q, S); [/asy]](//latex.artofproblemsolving.com/f/b/a/fba6b5fd48bca54a3103c12a3fd27b464a32abf2.png)

In terms of $n$, find the greatest $k$ such that in each Japanese triangle there is a ninja path containing at least $k$ red circles.

- A clear setup and notation.
- Rigorous logical arguments.
- Explicit justification of all nontrivial steps.
- Standard IMO-level presentation and structure.
- A concise concluding statement.

Once you send the problem, I'll produce the full solution.

**Problem 6** &nbsp; *solved* · 1m23s · [Solution →](6.md)

Let $ABC$ be an equilateral triangle. Let $A_1,B_1,C_1$ be interior points of $ABC$ such that $BA_1=A_1C$, $CB_1=B_1A$, $AC_1=C_1B$, and
$$
\angle BA_1C+\angle CB_1A+\angle AC_1B=480^\circ
$$Let $BC_1$ and $CB_1$ meet at $A_2,$ let $CA_1$ and $AC_1$ meet at $B_2,$ and let $AB_1$ and $BA_1$ meet at $C_2.$

Prove that if triangle $A_1B_1C_1$ is scalene, then the three circumcircles of triangles $AA_1A_2, BB_1B_2$ and $CC_1C_2$ all pass through two common points.
