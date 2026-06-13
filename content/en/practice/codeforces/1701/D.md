---
title: "CF 1701D - Permutation Restoration"
description: "We are given an array $b$ that was produced from an unknown permutation $a$ of the numbers $1$ through $n$. For every position $i$, $$bi=leftlfloor frac{i}{ai}rightrfloor." date: "2026-06-09T21:47:53+07:00" tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "greedy", "math", "sortings", "two-pointers"] categories: ["algorithms"] codeforces_contest: 1701 codeforces_index: "D" codeforces_contest_name: "Educational Codeforces Round 131 (Rated for Div. 2)" rating: 1900 weight: 1701 solve_time_s: 62 verified: false draft: false --- [CF 1701D - Permutation Restoration](https://codeforces.com/problemset/problem/1701/D) **Rating:** 1900   **Tags:** binary search, data structures, greedy, math, sortings, two pointers   **Solve time:** 1m 2s   **Verified:** no   ## Solution ## Problem Understanding We are given an array $b$ that was produced from an unknown permutation $a$ of the numbers $1$ through $n$. For every position $i$,$$b_i=\left\lfloor \frac{i}{a_i}\right\rfloor.$$
The permutation has been lost, and we must reconstruct any valid permutation that produces the given array $b$.
The interesting part is that we are not directly told anything about the values of $a_i$. Instead, each $b_i$ restricts which values can be placed at position $i$. Since $a$ must be a permutation, every value from $1$ to $n$ must be used exactly once.
The total size over all test cases is at most $5\cdot10^5$. That immediately rules out anything quadratic. An $O(n^2)$ algorithm would require around $2.5\cdot10^{11}$ operations in the worst case, which is completely impossible. We need something close to $O(n\log n)$ over each test case.
The most dangerous part of the problem is that many positions may allow overlapping ranges of values. A greedy assignment that looks locally valid can easily block a future position.
Consider:
```
n = 3
b = [0, 1, 3]
```
A valid answer is:
```
a = [3, 2, 1]
```
because
$$\left\lfloor\frac{1}{3}\right\rfloor=0,\quad
\left\lfloor\frac{2}{2}\right\rfloor=1,\quad
\left\lfloor\frac{3}{1}\right\rfloor=3.$$
If we simply assign the smallest feasible value at every position from left to right, we may consume value $1$ too early and leave no legal choice for the last position.
Another subtle case occurs when $b_i=0$.
Example:
```
n = 4
b = [0,0,0,0]
```
For position $i=1$,
$$\left\lfloor \frac{1}{a_1}\right\rfloor=0$$
means $a_1>1$. The value $1$ is forbidden there. A careless implementation that treats the lower bound as $1$ for every position would generate invalid assignments.
A third trap comes from boundary values.
Example:
```
n = 2
b = [1,1]
```
For position $1$,
$$\left\lfloor \frac{1}{a_1}\right\rfloor=1$$
forces $a_1=1$.
For position $2$,
$$\left\lfloor \frac{2}{a_2}\right\rfloor=1$$
forces $a_2=2$.
The ranges collapse to single points. Any implementation that computes interval endpoints incorrectly by one will fail on such cases.
## Approaches
A brute-force approach would try to reconstruct the permutation directly. For every position we could enumerate all values $1$ through $n$, check whether they satisfy
$$\left\lfloor \frac{i}{a_i}\right\rfloor=b_i,$$
and then search for a perfect assignment of values to positions.
This works conceptually because the condition is easy to test. Unfortunately, each position may accept many values, and finding a permutation consistent with all constraints becomes a matching problem on $n$ vertices. A naive implementation would be far too slow for $n=5\cdot10^5$.
The key observation is that each position does not accept an arbitrary set of values. The floor equation defines a contiguous interval.
Suppose $b_i>0$. Then
$$b_i \le \frac{i}{a_i} < b_i+1.$$
Rearranging gives
$$\frac{i}{b_i+1} < a_i \le \frac{i}{b_i}.$$
Since $a_i$ is an integer,
L_i=\left\lfloor\frac{i}{b_i+1}\right\rfloor+1, \qquad R_i=\left\lfloor\frac{i}{b_
