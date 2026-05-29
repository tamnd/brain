---
title: "IMO 2024"
description: "IMO 2024 — 6/6 solved, 1 verified."
tags: ["imo", "mathematics", "olympiad"]
categories: ["mathematics"]
imo_year: 2024
weight: 2024
draft: false
---

# IMO 2024

[Official IMO 2024 problems](https://www.imo-official.org/year_info.aspx?year=2024) &nbsp;·&nbsp; 6/6 solved, 1 verified.

## Problem 1

*✓ verified* · 5m00s · [Solution →](1.md)

Determine all real numbers $\alpha$ such that, for every positive integer $n$, the integer

$$
\lfloor \alpha \rfloor + \lfloor 2\alpha \rfloor + \dots +\lfloor n\alpha \rfloor
$$

is a multiple of $n$. (Note that $\lfloor z \rfloor$ denotes the greatest integer less than or equal to $z$. For example, $\lfloor -\pi \rfloor = -4$ and $\lfloor 2 \rfloor = \lfloor 2.9 \rfloor = 2$.)

---

## Problem 2

*solved* · 8m52s · [Solution →](2.md)

Find all positive integer pairs $(a,b),$ such that there exists positive integers $g,N,$ such that $$
\gcd (a^n+b,b^n+a)=g
$$ holds for all integer $n\ge N$.

---

## Problem 3

*solved* · 8m59s · [Solution →](3.md)

Let $a_1, a_2, a_3, \dots$ be an infinite sequence of positive integers, and let $N$ be a positive integer. Suppose that, for each $n > N$, $a_n$ is equal to the number of times $a_{n-1}$ appears in the list $a_1, a_2, \dots, a_{n-1}$.

Prove that at least one of the sequence $a_1, a_3, a_5, \dots$ and $a_2, a_4, a_6, \dots$ is eventually periodic.

(An infinite sequence $b_1, b_2, b_3, \dots$ is eventually periodic if there exist positive integers $p$ and $M$ such that $b_{m+p} = b_m$ for all $m \ge M$.)

---

## Problem 4

*solved* · 1h06m · [Solution →](4.md)

Let $ABC$ be a triangle with $AB < AC < BC$. Let the incentre and incircle of triangle $ABC$ be $I$ and $\omega$, respectively. Let $X$ be the point on line $BC$ different from $C$ such that the line through $X$ parallel to $AC$ is tangent to $\omega$. Similarly, let $Y$ be the point on line $BC$ different from $B$ such that the line through $Y$ parallel to $AB$ is tangent to $\omega$. Let $AI$ intersect the circumcircle of triangle $ABC$ again at $P  \neq A$. Let $K$ and $L$ be the midpoints of $AC$ and $AB$, respectively. Prove that $\angle KIL + \angle YPX = 180^{\circ}$.

---

## Problem 5

*solved* · 11m42s · [Solution →](5.md)

Turbo the snail plays a game on a board with 2024 rows and 2023 columns. There are hidden monsters in 2022 of the cells. Initially, Turbo does not know where any of the monsters are, but he knows that there is exactly one monster in each row except the first row and the last row, and that each column contains at most one monster.

Turbo makes a series of attempts to go from the first row to the last row. On each attempt, he chooses to start on any cell in the first row, then repeatedly moves to an adjacent cell sharing a common side. (He is allowed to return to a previously visited cell.) If he reaches a cell with a monster, his attempt ends and he is transported back to the first row to start a new attempt. The monsters do not move, and Turbo remembers whether or not each cell he has visited contains a monster. If he reaches any cell in the last row, his attempt ends and the game is over.

Determine the minimum value of $n$ for which Turbo has a strategy that guarantees reaching the last row on the $n^{th}$ attempt or earlier, regardless of the locations of the monsters.

---

## Problem 6

*solved* · 17m40s · [Solution →](6.md)

Let $\mathbb{Q}$ be the set of rational numbers. A function $f: \mathbb{Q} \to \mathbb{Q}$ is called $\emph{aquaesulian}$ if the following property holds: for every $x,y \in \mathbb{Q}$, $$
f(x+f(y)) = f(x) + y \quad \text{or} \quad f(f(x)+y) = x + f(y).
$$Show that there exists an integer $c$ such that for any aquaesulian function $f$ there are at most $c$ different rational numbers of the form $f(r) + f(-r)$ for some rational number $r$, and find the smallest possible value of $c$.

