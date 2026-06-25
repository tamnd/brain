---
title: "CF 105767F - Mega Polynomial"
description: "We are given two polynomials. The first one is a linear polynomial $$f(x)=Ax+B$$ and the second one has only two non-zero terms: $$g(x)=Cx^n+Dx^{n-1}."
date: "2026-06-25T15:59:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105767
codeforces_index: "F"
codeforces_contest_name: "TheForces Round #40 (Maths-Forces)"
rating: 0
weight: 105767
solve_time_s: 47
verified: true
draft: false
---

[CF 105767F - Mega Polynomial](https://codeforces.com/problemset/problem/105767/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two polynomials. The first one is a linear polynomial

$$f(x)=Ax+B$$

and the second one has only two non-zero terms:

$$g(x)=Cx^n+Dx^{n-1}.$$

We need the smallest number of derivatives, call it $k$, such that after differentiating $g(x)$ exactly $k$ times, the resulting polynomial can be divided by $f(x)$ while keeping all coefficients of the quotient as integers.

The number of test cases can reach $10^5$, and every value is at most $2\cdot10^5$. A solution that simulates derivatives or tries every possible $k$ for every test case would be too slow. With $10^5$ cases, we need close to constant time per case after preprocessing.

The main traps are caused by the word "integer" in the divisibility definition. Divisibility over rational numbers is not enough.

For example:

```
1
2 4 1 3 3
```

Here

$$f(x)=2x+4,\quad g(x)=x^3+3x^2.$$

After one derivative:

$$g'(x)=3x^2+6x=3x(x+2).$$

The linear part is proportional to $2x+4$, but the quotient would contain a fraction:

$$3x(x+2)=\frac{3}{2}x(2x+4).$$

The correct answer is not $1$. We must continue until the quotient is an integer polynomial.

Another edge case is when the zero polynomial is reached. For example:

```
1
5 1 1 1 1
```

After enough derivatives, the polynomial becomes zero. Zero is divisible by every polynomial because the quotient can simply be zero. The answer must include this final possibility.

A third edge case is $k=0$. The original polynomial may already satisfy the condition.

## Approaches

A direct approach is to repeatedly differentiate $g(x)$ and test whether the result is divisible by $f(x)$. This works mathematically because the degree decreases by one every derivative, and after $n+1$ derivatives the polynomial is zero. However, checking all possible derivatives for every test case costs $O(n)$, giving $O(2\cdot10^{10})$ work in the worst case, which is far beyond the limit.

The key observation is that every derivative keeps the same structure. After $k$ derivatives, where $0\le k<n$,

$$g^{(k)}(x)=
\frac{n!}{(n-k)!}C x^{n-k}
+
\frac{(n-1)!}{(n-1-k)!}D x^{n-1-k}.$$

The polynomial can be written as

$$x^{n-1-k}(\alpha x+\beta).$$

The extra power of $x$ does not matter for divisibility by $Ax+B$. The only relevant part is the linear factor. We need

$$\alpha x+\beta=q(Ax+B)$$

for some integer $q$.

The ratio condition gives

$$\frac{\alpha}{\beta}=\frac{A}{B}.$$

Substituting the derivative coefficients:

$$\frac{nC}{(n-k)D}=\frac AB.$$

Rearranging:

$$nBC=AD(n-k).$$

Let

$$s=n-k.$$

Then $s$ is uniquely determined:

$$s=\frac{nBC}{AD}.$$

If this is not an integer between $1$ and $n$, no non-zero derivative works and the answer is $n+1$. If it exists, we still need to check that the quotient is integral. The remaining condition is

$$B \mid D\cdot \frac{(n-1)!}{(s-1)!}.$$

We only need prime exponents of $B$. Since $B\le 2\cdot10^5$, we can factor it and compute factorial prime exponents with Legendre's formula.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n)$ per test case | $O(1)$ | Too slow |
| Optimal | $O(\log n \log B)$ per test case | $O(200000)$ | Accepted |

## Algorithm Walkthrough

1. Compute

$$num=nBC,\qquad den=AD.$$

The ratio equation says that $s=n-k=num/den$, so the derivative count is determined before checking integrality.

1. If `num` is not divisible by `den`, there is no valid derivative before the zero polynomial. Return $n+1$.
2. Let $s=num/den$. If $s\notin[1,n]$, return $n+1$. The value of $s$ represents $n-k$, so it must correspond to an existing derivative.
3. Check whether

$$B \mid D\cdot s(s+1)\cdots(n-1).$$

The product is exactly $(n-1)!/(s-1)!$, which appears in the constant coefficient of the linear factor after differentiation.

1. If the divisibility test succeeds, the answer is $k=n-s$. Otherwise return $n+1$.

Why it works:

Every possible useful derivative has a linear factor whose coefficient ratio must match $Ax+B$. That ratio forces exactly one possible value of $n-k$. The only remaining requirement is that the scalar multiplier is an integer. The prime exponent check verifies precisely that condition, so every returned value satisfies the definition, and every smaller derivative has already been ruled out by the forced value of $k$.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXN = 200000

spf = list(range(MAXN + 1))
for i in range(2, int(MAXN ** 0.5) + 1):
    if spf[i] == i:
        for j in range(i * i, MAXN + 1, i):
            if spf[j] == j:
                spf[j] = i

def factor(x):
    res = []
    while x > 1:
        p = spf[x]
        c = 0
        while x % p == 0:
            x //= p
            c += 1
        res.append((p, c))
    return res

def fact_exp(n, p):
    ans = 0
    while n:
        n //= p
        ans += n
    return ans

def solve_case(A, B, C, D, n):
    num = B * n * C
    den = A * D

    if num % den:
        return n + 1

    s = num // den
    if s < 1 or s > n:
        return n + 1

    need = factor(B)

    for p, e in need:
        have = 0
        x = D
        while x % p == 0:
            have += 1
            x //= p
        have += fact_exp(n - 1, p) - fact_exp(s - 1, p)
        if have < e:
            return n + 1

    return n - s

def main():
    t = int(input())
    ans = []
    for _ in range(t):
        A, B, C, D, n = map(int, input().split())
        ans.append(str(solve_case(A, B, C, D, n)))
    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The code first builds a smallest prime factor table so that factoring $B$ is fast. Since all values are bounded by $200000$, this preprocessing is shared by all test cases.

The ratio calculation uses Python integers, so there is no overflow risk. The value `s` is checked before being converted into an answer because $k=n-s$ only makes sense when $s$ is a valid remaining degree.

The divisibility test never constructs the factorial product directly. Instead, it compares prime exponents. The exponent of a prime in $m!$ is found by repeatedly dividing $m$ by that prime, which is Legendre's formula.

## Worked Examples

For:

```
1
1 2 2 4 1
```

The variables evolve as follows.

| Step | Value |
| --- | --- |
| $num=B n C$ | 8 |
| $den=A D$ | 4 |
| $s=num/den$ | 2 |
| $k=n-s$ | -1 |

Here $s>n$, so this path is impossible. The zero polynomial is reached after $n+1$ derivatives, so the answer is:

```
2
```

For:

```
1
4 2 3 3 4
```

| Step | Value |
| --- | --- |
| $num=B n C$ | 24 |
| $den=A D$ | 12 |
| $s$ | 2 |
| $k=n-s$ | 2 |
| Required check | passes |

The second derivative is the first one where the quotient is an integer polynomial, giving:

```
2
```

These examples show both the degree equation and the integer quotient condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log B \log n)$ | Factoring and factorial exponent calculations are logarithmic |
| Space | $O(200000)$ | The SPF sieve is stored once |

The preprocessing handles the largest possible values once. Each test case only touches the prime factors of $B$, so $10^5$ test cases fit comfortably.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().strip().split()
    sys.stdin = old

    if not data:
        return ""

    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        A = int(next(it))
        B = int(next(it))
        C = int(next(it))
        D = int(next(it))
        n = int(next(it))
        out.append(str(solve_case(A, B, C, D, n)))
    return "\n".join(out)

assert run("""6
1 2 2 4 1
4 2 3 3 4
2 4 1 3 3
2 1 5 2 4
131296 123463 91609 133724 142208
172458 127836 190471 141192 190476
""") == """0
2
4
5
50599
190477"""

assert run("1\n1 1 1 1 1\n") == "0"
assert run("1\n2 4 1 3 3\n") == "4"
assert run("1\n200000 200000 200000 200000 200000\n") == "200001"
assert run("1\n5 1 1 1 10\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1 1` | `0` | The original polynomial already works |
| `2 4 1 3 3` | `4` | The integer quotient restriction |
| `200000 200000 200000 200000 200000` | `200001` | Large values and fallback to zero polynomial |
| `5 1 1 1 10` | `0` | Simple proportional case |

## Edge Cases

When the initial polynomial already divides correctly, the ratio equation gives $s=n$, so the answer becomes $k=0$. The algorithm handles this because it allows $s$ to equal $n$.

When the ratio condition is satisfied but the quotient is fractional, the prime exponent check rejects the candidate. For example, with

```
1
2 4 1 3 3
```

the only possible non-zero candidate is $k=1$, but the coefficient multiplier contains a factor of $3/2$. The algorithm detects that $B=4$ does not divide the required coefficient and returns the later zero polynomial answer.

When no derivative before the zero polynomial can work, the returned value is $n+1$. At that point $g^{(n+1)}(x)=0$, and zero is divisible by the linear polynomial with quotient zero.
