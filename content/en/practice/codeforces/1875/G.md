---
title: "CF 1875G - Jellyfish and Miku"
description: "Algorithm C begins with $d=3$, so each segment ends at the first position where all three values $0$, $1$, and $2$ have appeared at least once. The sequence is $$11012210221202020121220101020121." date: "2026-06-09T01:00:52+07:00" tags: ["codeforces", "competitive-programming", "dp", "math", "probabilities"] categories: ["algorithms"] codeforces_contest: 1875 codeforces_index: "G" codeforces_contest_name: "Codeforces Round 901 (Div. 2)" rating: 2800 weight: 1875 solve_time_s: 56 verified: false draft: false --- [CF 1875G - Jellyfish and Miku](https://codeforces.com/problemset/problem/1875/G) **Rating:** 2800   **Tags:** dp, math, probabilities   **Solve time:** 56s   **Verified:** no   ## Solution ## Solution Algorithm C begins with $d=3$, so each segment ends at the first position where all three values $0$, $1$, and $2$ have appeared at least once. The sequence is$$11012210221202020121220101020121.$$
For the first segment, starting at the first symbol,
$$1,1,0,1$$
contains only the values $0$ and $1$. The next symbol is $2$, giving the complete set ${0,1,2}$. Hence the first segment is
$$11012,$$
with length $5$.
The second segment begins immediately afterward:
$$2,2,1$$
contains only ${1,2}$. The next symbol is $0$, completing the set. Hence the second segment is
$$2210,$$
with length $4$.
The third segment begins at the next position:
$$2,2,1,2$$
contains only ${1,2}$. The next symbol is $0$, completing the set. Hence the third segment is
$$22120,$$
with length $5$.
The fourth segment begins next:
$$2,0,2,0$$
contains only ${0,2}$. The next symbol is $1$, completing the set. Hence the fourth segment is
$$20201,$$
with length $5$.
The fifth segment begins next:
$$2,1,2,2$$
contains only ${1,2}$. The next symbol is $0$, completing the set. Hence the fifth segment is
$$21220,$$
with length $5$.
The sixth segment begins next:
$$1,0,1,0$$
contains only ${0,1}$. The next symbol is $2$, completing the set. Hence the sixth segment is
$$10102,$$
with length $5$.
The seventh segment begins next:
$$0,1,2$$
already contains all three values. Hence the seventh segment is
$$012,$$
with length $3$.
Thus Algorithm C partitions the sequence as
$$11012 \mid 2210 \mid 22120 \mid 20201 \mid 21220 \mid 10102 \mid 012,$$
and the seven recorded lengths are
$$5,\ 4,\ 5,\ 5,\ 5,\ 5,\ 3.$$
Therefore the answer is
$$\boxed{5,\ 4,\ 5,\ 5,\ 5,\ 5,\ 3}.$$
