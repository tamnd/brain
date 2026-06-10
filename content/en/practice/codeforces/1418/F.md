---
title: "CF 1418F - Equal Product"
description: "Fix a value of $x1$. We need to find two different representations of the same product: $$x1 y1 = x2 y2,$$ with $x2 x1$, $y2 < y1$, and the product lying inside $[l,r]$. The output is required separately for every $x1$ from $1$ to $n$."
date: "2026-06-11T06:52:23+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "math", "number-theory", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1418
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 95 (Rated for Div. 2)"
rating: 3000
weight: 1418
solve_time_s: 122
verified: true
draft: false
---

[CF 1418F - Equal Product](https://codeforces.com/problemset/problem/1418/F)

**Rating:** 3000  
**Tags:** data structures, math, number theory, two pointers  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

Fix a value of $x_1$. We need to find two different representations of the same product:

$$x_1 y_1 = x_2 y_2,$$

with $x_2 > x_1$, $y_2 < y_1$, and the product lying inside $[l,r]$.

The output is required separately for every $x_1$ from $1$ to $n$. For some values of $x_1$ no valid quadruple exists, in which case we print $-1$.

The constraints are what make the problem difficult. Both $n$ and $m$ can reach $2 \cdot 10^5$, so anything quadratic is immediately impossible. Even iterating over all pairs $(x_2,y_2)$ for every $x_1$ would require tens of billions of operations.

The product range constraint can also be misleading. A naive approach might try to iterate over all products in $[l,r]$, but $r$ can be as large as $nm$, which is up to $4 \cdot 10^{10}$.

One subtle edge case appears when the valid range of $y_1$ is empty.

For example:

```
n = 3
m = 5
l = 20
r = 20
```

For $x_1 = 3$,

$$y_1 = \frac{20}{3}$$

is not an integer and no value of $y_1$ satisfies both the product range and $1 \le y_1 \le m$. Any implementation that assumes the interval is nonempty will produce invalid answers.

Another easy mistake is forgetting that $y_2$ must be strictly smaller than $y_1$.

Consider:

```
x1 = 4
y1 = 6
x2 = 8
y2 = 3
```

This is valid because $24 = 24$ and $3 < 6$.

But if $a=b$ in the reduced ratio construction described later, then $y_2=y_1$, which is forbidden. We must always enforce $a>b$.

A third trap is constructing an equal product but allowing $x_2>n$.

For example:

```
n = 5
x1 = 4
```

Using ratio $a/b = 3/2$ gives

$$x_2 = 4 \cdot \frac{3}{2} = 6,$$

which violates the limit on $x_2$. The ratio must satisfy the bound on $x_2$ as well.

## Approaches

Suppose we fix $x_1$.

The valid values of $y_1$ are exactly those satisfying

$$l \le x_1 y_1 \le r,$$

together with $1 \le y_1 \le m$. This gives an interval

$$[y_{\text{low}}, y_{\text{high}}].$$

A brute force solution would try every $y_1$ in that interval and search for another factorization of the same product. Even checking all possible $x_2$ values leads to roughly

$$O(nm)$$

or worse, far beyond the limits.

The key observation is that equal products are really a statement about ratios.

Assume

$$x_1 y_1 = x_2 y_2.$$

Write

$$\frac{x_2}{x_1}=\frac{a}{b}$$

in lowest terms.

Since $x_2>x_1$, we have $a>b$.

Because the fraction is reduced, $b$ must divide $x_1$. Also,

$$\frac{y_1}{y_2}=\frac{a}{b},$$

so $a$ must divide $y_1$.

Thus a solution exists if we can find:

$$b \mid x_1,$$

and some

$$a>b$$

such that:

$$x_1 \cdot \frac{a}{b} \le n,$$

and at least one number inside $[y_{\text{low}},y_{\text{high}}]$ is divisible by $a$.

Now the problem becomes a divisor query problem.

For every interval $[y_{\text{low}},y_{\text{high}}]$, we need to know which values of $a$ have at least one multiple inside that interval. Then for every divisor $b$ of $x_1$, we want the smallest active $a$ satisfying

$$b < a \le \frac{nb}{x_1}.$$

The intervals change with $x_1$, and their endpoints move monotonically. This makes a two pointer sweep possible. We maintain all divisors that currently have a multiple inside the active interval. A segment tree lets us find the first active $a$ in a range.

That reduces the whole problem to roughly $O((n+m)\log^2 n)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nm)$ or worse | $O(1)$ | Too slow |
| Optimal | $O((n+m)\log^2 n)$ | $O(n+m)$ | Accepted |

## Algorithm Walkthrough

1. Precompute all divisors for every number from $1$ to $\max(n,m)$ using a sieve style loop.
2. For every $x$, precompute its divisor list.
3. For each $x$, compute

$$L_x=\max\!\left(1,\left\lceil\frac{l}{x}\right\rceil\right),$$

and

$$R_x=\min\!\left(m,\left\lfloor\frac{r}{x}\right\rfloor\right).$$

These are exactly the valid values of $y_1$.

1. Process $x$ from $n$ down to $1$.
2. Maintain the current interval $[curL,curR]$, initially empty.
3. When the target interval changes from the previous one, move the two pointers. Whenever a value $y$ enters the interval, add all divisors of $y$. Whenever a value $y$ leaves the interval, remove all divisors of $y$.
4. For every divisor $a$, keep a counter equal to the number of multiples of $a$ currently present in the interval.
5. A value $a$ is active if its counter is positive. Store active values in a segment tree.
6. For the current $x$, iterate over all divisors $b$ of $x$.
7. The largest allowed value of $a$ is

$$\text{limit}=\left\lfloor \frac{nb}{x}\right\rfloor.$$

1. Query the segment tree for the first active value in

$$[b+1,\text{limit}].$$

1. If such an $a$ exists, construct

$$y_1=\left\lceil\frac{L_x}{a}\right\rceil a.$$

Because $a$ is active, this multiple is guaranteed to lie inside the interval.

1. Set

$$x_2=x_1\frac{a}{b},
\qquad
y_2=y_1\frac{b}{a}.$$

1. Output the quadruple and stop searching for this $x_1$.
2. If no divisor $b$ produces a valid $a$, output $-1$.

### Why it works

The maintained interval contains exactly the valid values of $y_1$ for the current $x_1$.

A divisor $a$ is active exactly when some valid $y_1$ is divisible by $a$. The segment tree query finds an active $a$ satisfying $a>b$ and $x_1a/b \le n$.

Since $b\mid x_1$ and $a\mid y_1$,

$$x_2=x_1\frac{a}{b}$$

and

$$y_2=y_1\frac{b}{a}$$

are integers.

The inequality $a>b$ guarantees

$$x_2>x_1$$

and

$$y_2<y_1.$$

The equality

$$x_1y_1=x_2y_2$$

follows directly from the construction. Every printed quadruple is valid, and every valid quadruple corresponds to some divisor $b$ and active divisor $a$, so the search cannot miss a solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def first_in_range(seg, size, l, r):
    if l > r:
        return -1

    def dfs(node, nl, nr):
        if nr < l or nl > r or seg[node] == 0:
            return -1
        if nl == nr:
            return nl
        mid = (nl + nr) // 2
        left = dfs(node * 2, nl, mid)
        if left != -1:
            return left
        return dfs(node * 2 + 1, mid + 1, nr)

    return dfs(1, 1, size)

def solve():
    n, m = map(int, input().split())
    l, r = map(int, input().split())

    mx = max(n, m)

    divisors = [[] for _ in range(mx + 1)]
    for d in range(1, mx + 1):
        for v in range(d, mx + 1, d):
            divisors[v].append(d)

    size = 1
    while size < m:
        size <<= 1

    seg = [0] * (2 * size)
    cnt = [0] * (m + 1)

    def activate(a):
        p = a + size - 1
        seg[p] = 1
        p //= 2
        while p:
            seg[p] = seg[p * 2] | seg[p * 2 + 1]
            p //= 2

    def deactivate(a):
        p = a + size - 1
        seg[p] = 0
        p //= 2
        while p:
            seg[p] = seg[p * 2] | seg[p * 2 + 1]
            p //= 2

    def add_y(y):
        for d in divisors[y]:
            cnt[d] += 1
            if cnt[d] == 1:
                activate(d)

    def remove_y(y):
        for d in divisors[y]:
            cnt[d] -= 1
            if cnt[d] == 0:
                deactivate(d)

    ans = [None] * (n + 1)

    curL = 1
    curR = 0

    for x in range(n, 0, -1):
        L = (l + x - 1) // x
        R = r // x

        if L < 1:
            L = 1
        if R > m:
            R = m

        if L > R:
            ans[x] = None
            continue

        while curR < R:
            curR += 1
            add_y(curR)

        while curR > R:
            remove_y(curR)
            curR -= 1

        while curL < L:
            remove_y(curL)
            curL += 1

        while curL > L:
            curL -= 1
            add_y(curL)

        found = None

        for b in divisors[x]:
            limit = (n * b) // x
            if limit <= b:
                continue

            a = first_in_range(seg, size, b + 1, min(limit, m))
            if a == -1:
                continue

            y1 = ((L + a - 1) // a) * a
            x2 = x * a // b
            y2 = y1 * b // a

            found = (x, y1, x2, y2)
            break

        ans[x] = found

    out = []
    for x in range(1, n + 1):
        if ans[x] is None:
            out.append("-1")
        else:
            out.append(" ".join(map(str, ans[x])))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The divisor sieve is the foundation of the solution. It allows every update of a window endpoint to touch only the divisors of the entering or leaving value.

The two pointers maintain the exact interval of valid $y_1$ values for the current $x$. Since we process $x$ from $n$ down to $1$, both interval endpoints move only forward, so every value of $y$ is inserted and removed at most once.

The segment tree stores only whether a divisor is active. The query searches for the first active value inside a range. That is exactly the operation required by the ratio formulation.

The reconstruction step is easy to get wrong. The chosen $y_1$ must be a multiple of $a$ that lies inside the current interval. Taking the first such multiple guarantees this.

## Worked Examples

### Sample 1

Input:

```
8 20
91 100
```

For $x_1=6$:

$$L=\left\lceil\frac{91}{6}\right\rceil=16,
\qquad
R=\left\lfloor\frac{100}{6}\right\rfloor=16.$$

| x | Interval | b | Chosen a | y1 | x2 | y2 |
| --- | --- | --- | --- | --- | --- | --- |
| 6 | [16,16] | 3 | 4 | 16 | 8 | 12 |

We obtain:

$$6 \cdot 16 = 8 \cdot 12 = 96.$$

This demonstrates the ratio construction. The interval contains only one value, yet a valid factorization still exists.

### Sample 2

Input:

```
4 5
1 10
```

For $x_1=1$:

$$L=1,\quad R=5.$$

| x | Interval | b | Chosen a | y1 | x2 | y2 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [1,5] | 1 | 2 | 2 | 2 | 1 |

For $x_1=2$:

| x | Interval | b | Chosen a | y1 | x2 | y2 |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | [1,5] | 2 | 3 | 3 | 3 | 2 |

The trace shows how the algorithm searches through divisors of $x$ and picks the first active $a$ that satisfies the bound on $x_2$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n+m)\log^2 n)$ | Divisor updates plus segment tree queries |
| Space | $O(n+m)$ | Divisor lists, counters, segment tree |

The sum of divisor counts up to $2 \cdot 10^5$ is about $N \log N$, which is easily manageable. The segment tree operations add another logarithmic factor. The solution comfortably fits within the limits.

## Test Cases

```python
# helper skeleton

import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    # real testing would call solve() and capture stdout
    return out.getvalue()

# Sample outputs are not unique for this problem,
# so exact-string assertions are inappropriate.
# Instead, a checker should verify validity.

# Minimum size
inp = """\
1 1
1 1
"""

# No solution possible because x2 > x1 cannot exist.

# Boundary interval with single product
inp2 = """\
2 2
4 4
"""

# Small dense range
inp3 = """\
4 5
1 10
"""

# Large boundary style test
inp4 = f"""\
200000 200000
1 40000000000
"""

# Interval producing many empty y-ranges
inp5 = """\
5 5
24 25
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| $n=m=1$ | All $-1$ | Smallest possible instance |
| Single product interval | Valid or $-1$ per $x$ | Tight interval handling |
| Sample 2 | Valid quadruples | Basic correctness |
| Maximum limits | Finishes quickly | Performance |
| Narrow high range | Mixed answers | Empty interval handling |

## Edge Cases

Consider:

```
3 5
20 20
```

For $x_1=3$,

$$L=\left\lceil\frac{20}{3}\right\rceil=7,
\qquad
R=\left\lfloor\frac{20}{3}\right\rfloor=6.$$

Since $L>R$, the interval is empty. The algorithm immediately prints $-1$.

Now consider:

```
4 6
24 24
```

For $x_1=4$, the only valid value is $y_1=6$. The algorithm activates all divisors present in the interval $[6,6]$. It may choose $b=2$ and $a=3$, yielding

$$x_2=6,$$

which exceeds $n=4$. The bound

$$a \le \frac{nb}{x_1}$$

rejects this candidate before construction.

Finally:

```
4 5
1 10
```

If the algorithm ever selected $a=b$, then

$$y_2=y_1.$$

The query range begins at $b+1$, so this cannot happen. Strict inequality is enforced structurally rather than by a later check.
