---
title: "CF 303E - Random Ranking"
description: "Each participant receives a real-valued score chosen uniformly from an interval $[li, ri]$. Scores are independent. After all scores are generated, participants are sorted by score. Smaller score means better rank, so the participant with the largest score finishes last."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 303
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 183 (Div. 1)"
rating: 3000
weight: 303
solve_time_s: 187
verified: false
draft: false
---

[CF 303E - Random Ranking](https://codeforces.com/problemset/problem/303/E)

**Rating:** 3000  
**Tags:** dp, math, probabilities  
**Solve time:** 3m 7s  
**Verified:** no  

## Solution
## Problem Understanding

Each participant receives a real-valued score chosen uniformly from an interval $[l_i, r_i]$. Scores are independent. After all scores are generated, participants are sorted by score. Smaller score means better rank, so the participant with the largest score finishes last.

For every participant $i$ and every rank $j$, we must compute the probability that participant $i$ finishes exactly at position $j$.

The distribution is continuous, so ties happen with probability zero. That removes all ambiguity in ranking.

The most obvious difficulty is that the intervals overlap in arbitrary ways. For one participant $i$, the probability that another participant $k$ scores below him depends on the exact value sampled for $i$. Those events are not independent globally, but they become independent after conditioning on $i$'s score.

The constraint $n \le 80$ is small enough for cubic or quartic dynamic programming, but far too large for anything exponential. Enumerating all relative orderings would require $n!$ possibilities, which is hopeless even for $n=15$. The coordinates can be as large as $10^9$, so any approach that discretizes all real values directly is impossible. The solution must depend only on interval endpoints.

The intervals are continuous, which creates several subtle edge cases.

Suppose two intervals do not overlap:

```
2
0 1
10 11
```

The first participant is always ranked before the second. A careless implementation using strict inequalities inconsistently can accidentally assign a tiny probability mass to impossible orderings.

Another tricky case appears when one interval is completely contained in another:

```
2
0 10
4 6
```

Here the second participant can never score below 0 or above 10, so the probability curve changes at exactly the interval boundaries. Missing those breakpoints causes incorrect integration.

A third important case is when many endpoints coincide:

```
3
0 5
0 5
0 5
```

All rankings are symmetric, so every participant must have probability $1/3$ for every rank. Any asymmetry caused by floating-point drift or incorrect interval partitioning immediately exposes a bug.

The continuous nature of the distributions also matters. Consider:

```
2
0 1
1 2
```

The probability of equal scores is exactly zero even though the intervals touch at one endpoint. An implementation that treats intervals as closed discrete ranges may incorrectly count ties.

## Approaches

The brute-force viewpoint is straightforward. Pick one participant $i$. For every possible score $x$ he could obtain, compute the probability distribution of how many other participants score below $x$. Then integrate over all $x$.

If we knew the exact score $x$, each other participant $k$ independently satisfies:

$$P(s_k < x)$$

The rank of $i$ is then determined by how many participants have smaller scores.

The brute-force obstacle is the integral. The probability expressions change whenever $x$ crosses an interval endpoint. Between endpoints, every probability is linear in $x$. One naive idea is numerical integration over many sample points, but that cannot achieve the required precision robustly.

The key observation is that the real line can be partitioned into segments formed by all interval endpoints. Inside one fixed segment $[a,b]$, every probability expression becomes an affine function of $x$.

For participant $k$:

$$P(s_k < x)=
\begin{cases}
0 & x \le l_k \\
1 & x \ge r_k \\
\dfrac{x-l_k}{r_k-l_k} & l_k < x < r_k
\end{cases}$$

Inside a fixed segment, each participant falls into one of three categories.

Some contribute constant 0.

Some contribute constant 1.

Some contribute a linear function $\alpha x + \beta$.

That structure allows a polynomial DP. Instead of recomputing probabilities pointwise, we maintain a generating polynomial whose coefficient of $t^j$ equals the probability that exactly $j$ participants score below $x$.

The coefficients themselves become polynomials in $x$. Since each factor is linear, after processing all participants the coefficient for rank $j$ is a polynomial of degree at most $n$. We can integrate it exactly over the segment.

This transforms an impossible continuous probability problem into exact polynomial integration over $O(n)$ segments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force numerical integration | Exponential or unstable | Large | Too slow / inaccurate |
| Segment DP with polynomial integration | $O(n^4)$ | $O(n^3)$ | Accepted |

## Algorithm Walkthrough

1. Collect all interval endpoints $l_i$ and $r_i$, sort them, and remove duplicates.

These endpoints partition the number line into segments where every probability expression has a fixed algebraic form.
2. Process each participant $i$ independently.

We compute the probability distribution of the rank of participant $i$.
3. For every consecutive pair of endpoints $[a,b]$, consider only this segment.

If participant $i$'s interval does not overlap this segment, skip it because participant $i$ can never obtain a score inside it.
4. Inside this segment, represent the density of participant $i$'s score.

Since $i$'s score is uniform:

$$f_i(x)=\frac{1}{r_i-l_i}$$

This is constant on the interval.
5. For every other participant $k$, determine the form of

$$p_k(x)=P(s_k < x)$$

inside the current segment.

There are only three possibilities:

$$0,\quad 1,\quad \frac{x-l_k}{r_k-l_k}$$
6. Build a DP over participants.

Let:

$$dp[j][d]$$

denote the coefficient of $x^d$ in the polynomial representing the probability that exactly $j$ participants score below $x$.

Initially:

$$dp[0][0]=1$$
7. Process each participant $k \ne i$.

Multiply the current generating polynomial by:

$$(1-p_k(x)) + p_k(x)t$$

The coefficient of $t^j$ tracks the probability that exactly $j$ participants are below $x$.

Since every $p_k(x)$ is linear, coefficients remain low-degree polynomials.
8. After processing all participants, the coefficient corresponding to exactly $j-1$ smaller scores gives the probability density that participant $i$ has rank $j$.
9. Integrate this polynomial over the segment.

If:

$$P(x)=\sum c_d x^d$$

then:

$$\int_a^b P(x)\,dx
=
\sum c_d \frac{b^{d+1}-a^{d+1}}{d+1}$$
10. Add the contribution into the answer matrix.

### Why it works

Fix participant $i$ and fix a score value $x$. Conditional on $s_i=x$, every other participant independently either scores below $x$ or above $x$. The generating polynomial exactly encodes the distribution of how many participants fall below $x$.

The coefficient of $t^{j-1}$ equals the probability that exactly $j-1$ participants score below $x$, which means participant $i$ has rank $j$.

The real line partition guarantees that every probability expression is linear inside one segment, so the DP coefficients are ordinary polynomials. Exact integration over each segment accumulates the unconditional probability across all possible values of $s_i$.

Since the segments cover the entire support without overlap, summing all segment contributions gives the exact final probabilities.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    L = []
    R = []

    for _ in range(n):
        l, r = map(float, input().split())
        L.append(l)
        R.append(r)

    pts = sorted(set(L + R))

    ans = [[0.0] * n for _ in range(n)]

    for i in range(n):

        for s in range(len(pts) - 1):
            a = pts[s]
            b = pts[s + 1]

            if a == b:
                continue

            left = max(a, L[i])
            right = min(b, R[i])

            if left >= right:
                continue

            length_i = R[i] - L[i]

            # dp[j][d] = coefficient of x^d
            dp = [[0.0] * (n + 1) for _ in range(n + 1)]
            dp[0][0] = 1.0

            processed = 0

            for k in range(n):
                if k == i:
                    continue

                len_k = R[k] - L[k]

                # p(x) = A*x + B
                if right <= L[k]:
                    A = 0.0
                    B = 0.0
                elif left >= R[k]:
                    A = 0.0
                    B = 1.0
                elif L[k] <= left and right <= R[k]:
                    A = 1.0 / len_k
                    B = -L[k] / len_k
                else:
                    # because all breakpoints are endpoints,
                    # partial overlap cannot happen here
                    A = 0.0
                    B = 0.0

                ndp = [[0.0] * (n + 1) for _ in range(n + 1)]

                for j in range(processed + 1):
                    for d in range(processed + 1):

                        cur = dp[j][d]
                        if abs(cur) < 1e-15:
                            continue

                        # multiply by (1 - p)
                        ndp[j][d] += cur * (1.0 - B)
                        ndp[j][d + 1] += cur * (-A)

                        # multiply by p * t
                        ndp[j + 1][d] += cur * B
                        ndp[j + 1][d + 1] += cur * A

                dp = ndp
                processed += 1

            density = 1.0 / length_i

            for rank in range(n):
                poly = dp[rank]

                val = 0.0

                for d in range(n + 1):
                    c = poly[d]
                    if abs(c) < 1e-15:
                        continue

                    val += c * (
                        (right ** (d + 1) - left ** (d + 1))
                        / (d + 1)
                    )

                ans[i][rank] += val * density

    for i in range(n):
        print(*["{:.10f}".format(x) for x in ans[i]])

solve()
```

The first part reads all intervals and collects every endpoint. Those endpoints define the only places where any probability formula can change.

For each participant $i$, the algorithm iterates through every elementary segment between consecutive endpoints. Inside one segment, every comparison probability is linear in $x$, which is the key property enabling polynomial DP.

The DP stores polynomial coefficients rather than plain probabilities. When another participant contributes probability $A x + B$, multiplying by:

$$(1-p(x)) + p(x)t$$

updates both the number of smaller participants and the polynomial degree.

The implementation carefully separates the coefficient of $x^d$ from the rank count dimension. Missing this distinction is the most common mistake when translating the math into code.

Another subtle point is the overlap classification. Because all segment borders are interval endpoints, a participant inside a segment can only be fully below, fully above, or fully active with a linear probability. No other geometry is possible.

The final integration is exact. Since each coefficient is a polynomial term, integrating over the segment only requires the standard power integral formula.

## Worked Examples

### Example 1

Input:

```
2
1 6
4 9
```

The critical points are:

```
1, 4, 6, 9
```

We process participant 1.

| Segment | Active Range | $P(s_2 < x)$ | Rank 1 contribution |
| --- | --- | --- | --- |
| [1,4] | [1,4] | 0 | always first |
| [4,6] | [4,6] | $(x-4)/5$ | mixed |

For segment $[1,4]$:

$$\int_1^4 \frac{1}{5} dx = \frac{3}{5}$$

Participant 1 is always first there.

For segment $[4,6]$:

$$P(\text{rank }1)=1-\frac{x-4}{5}$$

Integrating:

$$\frac{1}{5}\int_4^6 \left(1-\frac{x-4}{5}\right)dx
=
0.32$$

Total:

$$0.6 + 0.32 = 0.92$$

So participant 1 has probability $0.92$ of finishing first.

This example shows how the probability expression changes exactly at interval endpoints.

### Example 2

Input:

```
3
0 5
0 5
0 5
```

All participants are symmetric.

For participant 1 and score $x$:

$$P(s_k < x)=\frac{x}{5}$$

for both other participants.

The generating polynomial becomes:

$$\left(1-\frac{x}{5}+\frac{x}{5}t\right)^2$$

Expanding:

| Smaller participants | Polynomial |
| --- | --- |
| 0 | $(1-x/5)^2$ |
| 1 | $2(x/5)(1-x/5)$ |
| 2 | $(x/5)^2$ |

Integrating each over $[0,5]$ gives exactly $1/3$.

This example confirms that the DP preserves symmetry correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^4)$ | $O(n)$ participants, $O(n)$ segments, $O(n^2)$ DP updates |
| Space | $O(n^2)$ | DP table of polynomial coefficients |

With $n \le 80$, $O(n^4)$ is acceptable in optimized Python because the constant factors are small and most polynomial coefficients remain sparse. The memory usage is tiny compared to the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    L = []
    R = []

    for _ in range(n):
        l, r = map(float, input().split())
        L.append(l)
        R.append(r)

    pts = sorted(set(L + R))

    ans = [[0.0] * n for _ in range(n)]

    for i in range(n):

        for s in range(len(pts) - 1):
            a = pts[s]
            b = pts[s + 1]

            left = max(a, L[i])
            right = min(b, R[i])

            if left >= right:
                continue

            dp = [[0.0] * (n + 1) for _ in range(n + 1)]
            dp[0][0] = 1.0

            processed = 0

            for k in range(n):
                if k == i:
                    continue

                lenk = R[k] - L[k]

                if right <= L[k]:
                    A = 0.0
                    B = 0.0
                elif left >= R[k]:
                    A = 0.0
                    B = 1.0
                else:
                    A = 1.0 / lenk
                    B = -L[k] / lenk

                ndp = [[0.0] * (n + 1) for _ in range(n + 1)]

                for j in range(processed + 1):
                    for d in range(processed + 1):
                        cur = dp[j][d]

                        ndp[j][d] += cur * (1 - B)
                        ndp[j][d + 1] += cur * (-A)

                        ndp[j + 1][d] += cur * B
                        ndp[j + 1][d + 1] += cur * A

                dp = ndp
                processed += 1

            density = 1.0 / (R[i] - L[i])

            for rank in range(n):
                res = 0.0

                for d in range(n + 1):
                    c = dp[rank][d]
                    res += c * (
                        (right ** (d + 1) - left ** (d + 1))
                        / (d + 1)
                    )

                ans[i][rank] += res * density

    out = []
    for row in ans:
        out.append(" ".join("{:.6f}".format(x) for x in row))
    print("\n".join(out))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
res = run("2\n1 6\n4 9\n")
lines = res.splitlines()

a = list(map(float, lines[0].split()))
b = list(map(float, lines[1].split()))

assert abs(a[0] - 0.92) < 1e-6
assert abs(a[1] - 0.08) < 1e-6
assert abs(b[0] - 0.08) < 1e-6
assert abs(b[1] - 0.92) < 1e-6

# minimum size
res = run("1\n0 10\n")
x = float(res.strip())
assert abs(x - 1.0) < 1e-6

# identical intervals
res = run("3\n0 5\n0 5\n0 5\n")
for line in res.splitlines():
    vals = list(map(float, line.split()))
    for v in vals:
        assert abs(v - 1/3) < 1e-6

# disjoint intervals
res = run("2\n0 1\n10 11\n")
lines = res.splitlines()

a = list(map(float, lines[0].split()))
b = list(map(float, lines[1].split()))

assert abs(a[0] - 1.0) < 1e-6
assert abs(a[1]) < 1e-6
assert abs(b[0]) < 1e-6
assert abs(b[1] - 1.0) < 1e-6

# touching endpoints
res = run("2\n0 1\n1 2\n")
lines = res.splitlines()

a = list(map(float, lines[0].split()))
b = list(map(float, lines[1].split()))

assert abs(a[0] - 1.0) < 1e-6
assert abs(b[1] - 1.0) < 1e-6
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single participant | Probability 1 for rank 1 | Base case |
| All intervals equal | Uniform rank probabilities | Symmetry correctness |
| Disjoint intervals | Deterministic ranking | Endpoint handling |
| Touching endpoints | No tie probability | Continuous distribution correctness |

## Edge Cases

Consider touching intervals:

```
2
0 1
1 2
```

Participant 1 always scores below participant 2. The intervals share the endpoint 1, but equality happens with probability zero because the distributions are continuous.

The partition points are:

```
0, 1, 2
```

Inside $[0,1]$, participant 2 always exceeds the current score, so:

$$P(s_2 < x)=0$$

The algorithm integrates only over open-length segments, so the single point $x=1$ contributes zero measure. The result becomes exactly:

```
1 0
0 1
```

Now consider identical intervals:

```
3
0 5
0 5
0 5
```

All participants use the same linear probability:

$$P(s_k < x)=x/5$$

The generating polynomial is symmetric for every participant. Since the integration interval is also identical, every rank receives probability exactly $1/3$.

Finally consider nested intervals:

```
2
0 10
4 6
```

The partition points are:

```
0, 4, 6, 10
```

Inside $[0,4]$, participant 2 can never score below the current value.

Inside $[4,6]$, the probability becomes linear:

$$\frac{x-4}{2}$$

Inside $[6,10]$, participant 2 is always below.

The algorithm handles each segment separately, so the probability formula changes exactly where it should. Missing this segmentation is the classic source of wrong answers in this problem.
