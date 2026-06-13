---
title: "CF 1548C - The Three Little Pigs"
description: "By exercise 20, the hypotheses $$hat q v{n-2}le bhat r+u{n-2}, qquad hat q<b, qquad v{n-1}0$$ imply that $$hat q=q quadtext{or}quad hat q=q-1.$$ Since the present exercise assumes $hat qne q$, necessarily $$hat q=q-1.$$ Let $$r=u-qv=ubmod v ." date: "2026-06-10T13:32:53+07:00" tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "fft", "math"] categories: ["algorithms"] codeforces_contest: 1548 codeforces_index: "C" codeforces_contest_name: "Codeforces Round 736 (Div. 1)" rating: 2500 weight: 1548 solve_time_s: 89 verified: false draft: false --- [CF 1548C - The Three Little Pigs](https://codeforces.com/problemset/problem/1548/C) **Rating:** 2500   **Tags:** combinatorics, dp, fft, math   **Solve time:** 1m 29s   **Verified:** no   ## Solution ## Solution By exercise 20, the hypotheses$$\hat q v_{n-2}\le b\hat r+u_{n-2},
\qquad
\hat q<b,
\qquad
v_{n-1}>0$$
imply that
$$\hat q=q \quad\text{or}\quad \hat q=q-1.$$
Since the present exercise assumes $\hat q\ne q$, necessarily
$$\hat q=q-1.$$
Let
$$r=u-qv=u\bmod v .$$
Since
$$u=\hat q\,v+\hat r\,b^{\,n-1}+u_{n-2}b^{\,n-2}+\cdots,$$
and since $\hat q=q-1$, we have
$$u=qv+\bigl(\hat r\,b^{\,n-1}+u_{n-2}b^{\,n-2}+\cdots-v\bigr).$$
Hence
$$r=\hat r\,b^{\,n-1}+u_{n-2}b^{\,n-2}+\cdots-v.$$
Write
$$T=\hat r\,b+u_{n-2}.$$
Then
$$r
\ge
T\,b^{\,n-2}-v.
\tag{1}$$
The inequality of exercise 19 fails, therefore
$$\hat q v_{n-2}\le b\hat r+u_{n-2}=T.
\tag{2}$$
Since $\hat q=q-1$ and $q\ge1$,
$$\hat q\ge b-2.$$
Indeed, from Theorem A of the division algorithm,
$$q\le \hat q+1,$$
and $\hat q=q-1$ gives equality. Because $q$ is a one place quotient digit, $q\le b-1$, hence $\hat q=b-2$ is the smallest possible value compatible with $\hat q=q-1$.
Using (2),
$$T\ge (b-2)v_{n-2}.
\tag{3}$$
The hypothesis
$$v_{n-1}\ge \left\lfloor \frac b2\right\rfloor$$
implies
$$v
<
(v_{n-1}+1)b^{\,n-1}
\le
\left(\frac b2+1\right)b^{\,n-1}.
\tag{4}$$
Also,
$$v\ge v_{n-1}b^{\,n-1}
\ge \frac{b-1}{2}b^{\,n-1},
\tag{5}$$
and therefore
$$v_{n-2}\le b-1<\frac{2}{b}v\,b^{-(n-2)}.$$
Multiplying by $(b-2)b^{,n-2}$ and using (3),
$$T\,b^{\,n-2}
\ge
\left(1-\frac{2}{b}\right)v.
\tag{6}$$
Substituting (6) into (1) yields
$$r
\ge
\left(1-\frac{2}{b}\right)v.$$
Since $r=u\bmod v$, this is exactly
$$u\bmod v \ge \left(1-\frac{2}{b}\right)v.$$
This completes the proof.
∎
## Notes
The event $\hat q=q-1$ occurs precisely when the trial quotient digit is one too small. The proof shows that this can happen only when the true remainder is already very large, namely within a fraction $2/b$ of the divisor. For machine word bases, $b$ is enormous, so such cases occur with approximate probability $2/b$, which is negligibly small.
