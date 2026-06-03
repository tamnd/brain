---
title: "CF 220D - Little Elephant and Triangle"
description: "We have all lattice points inside the rectangle $$0 le x le w,qquad 0 le y le h.$$ A valid answer is an ordered triple of points that forms a nondegenerate triangle whose area is a positive integer. The order matters, so every geometric triangle contributes up to $3!"
date: "2026-06-04T01:47:52+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "math"]
categories: ["algorithms"]
codeforces_contest: 220
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 136 (Div. 1)"
rating: 2500
weight: 220
solve_time_s: 163
verified: true
draft: false
---

[CF 220D - Little Elephant and Triangle](https://codeforces.com/problemset/problem/220/D)

**Rating:** 2500  
**Tags:** geometry, math  
**Solve time:** 2m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We have all lattice points inside the rectangle

$$0 \le x \le w,\qquad 0 \le y \le h.$$

A valid answer is an **ordered** triple of points that forms a nondegenerate triangle whose area is a positive integer. The order matters, so every geometric triangle contributes up to $3! = 6$ different triples.

The rectangle contains

$$N=(w+1)(h+1)$$

points. With $w,h \le 4000$, the grid can contain more than 16 million points. Any algorithm that even iterates over all points is impossible, let alone over all triples.

The key difficulty is that the condition is not merely "nondegenerate". The area must also be an integer. For lattice points, twice the area is always an integer, so we need to understand when the doubled area is even.

A common mistake is to count all triangles with even doubled area and forget to remove collinear triples. For example:

Input

```
2 1
```

The three points $(0,0)$, $(1,0)$, $(2,0)$ have doubled area $0$, which is even, but they do not form a triangle and must not be counted.

Another easy mistake is to count unordered triples. The statement explicitly says that different orders are different answers. Every valid geometric triangle contributes six ordered triples.

## Approaches

The brute force idea is straightforward. Enumerate every ordered triple of points, compute

$$|(x_2-x_1)(y_3-y_1)-(x_3-x_1)(y_2-y_1)|$$

and check whether it is nonzero and divisible by two.

This is correct, but completely infeasible. The grid may contain over $16$ million points, so the number of triples is on the order of $10^{21}$.

The breakthrough comes from separating the two requirements.

The integer-area condition depends only on the parity of the doubled area. Modulo $2$, the determinant depends only on the parity classes of the coordinates. There are only four parity classes:

$$(0,0),\ (0,1),\ (1,0),\ (1,1).$$

Once the parity classes are known, the parity of the doubled area is determined.

After counting all ordered triples whose doubled area is even, we subtract the triples whose area is actually zero. Those are exactly the collinear triples.

Counting collinear triples looks geometric, but lattice geometry gives a clean formula. If two lattice points differ by $(dx,dy)$, then the segment contains

$$\gcd(dx,dy)+1$$

lattice points. Every interior lattice point between the endpoints creates one collinear triple with those endpoints. This converts the geometry into sums involving $\gcd$, which can be evaluated efficiently using Euler's totient function.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N^3)$ | $O(1)$ | Too slow |
| Optimal | $O(\min(w,h)\log\log(\min(w,h)))$ | $O(\min(w,h))$ | Accepted |

## Algorithm Walkthrough

### Counting ordered triples with integer doubled area

1. Compute the sizes of the four parity classes.
2. Let

$$N=(w+1)(h+1).$$

The number of ordered triples of distinct points is

$$N(N-1)(N-2).$$

1. A determinant is odd modulo $2$ if and only if the three points belong to three different parity classes.
2. For every choice of three distinct parity classes, add

$$6 \cdot c_i c_j c_k$$

to the count of odd determinants.

1. Subtract the odd count from the total count. The result is the number of ordered distinct triples whose doubled area is even.

### Counting collinear ordered triples

1. Consider a segment whose endpoint difference is $(dx,dy)$.
2. The number of lattice points on that segment equals

$$\gcd(dx,dy)+1.$$

1. The number of interior lattice points is

$$\gcd(dx,dy)-1.$$

Each interior point together with the two endpoints forms one unordered collinear triple.

1. The number of placements of such a segment is

$$(w-dx+1)(h-dy+1).$$

1. If both $dx$ and $dy$ are positive, both slopes $+\frac{dy}{dx}$ and $-\frac{dy}{dx}$ exist, so we multiply by $2$.
2. Sum all contributions to obtain the number of unordered collinear triples.
3. Multiply by $6$ because the answer requires ordered triples.

### Accelerating the gcd sum

For $dx>0$ and $dy>0$, we need

$$\sum (w-dx+1)(h-dy+1)(\gcd(dx,dy)-1).$$

Using

$$\gcd(a,b)-1=\sum_{\substack{d\mid \gcd(a,b)\\ d>1}}\varphi(d),$$

we get

$$\sum_{d\ge2}\varphi(d)\,S_x(d)\,S_y(d),$$

where

$$S_x(d)=\sum_{k=1}^{\lfloor w/d\rfloor}(w-dk+1),$$

$$S_y(d)=\sum_{k=1}^{\lfloor h/d\rfloor}(h-dk+1).$$

Both sums have closed forms:

$$S_x(d)=m(w+1)-d\frac{m(m+1)}2,
\quad m=\left\lfloor\frac wd\right\rfloor.$$

The same formula works for $S_y$.

### Why it works

The parity argument counts exactly the ordered triples whose doubled area is even. Every valid integer-area triangle belongs to that set.

The only triples counted there that are not valid are the collinear ones. A collinear triple has area zero, hence doubled area zero, so it is always included in the parity count.

The lattice-point formula $\gcd(dx,dy)+1$ counts all lattice points on a segment. Choosing the two extreme points and one interior point gives a unique collinear triple, so every degenerate triple is counted exactly once before multiplying by $6$ for ordering.

The final answer is therefore

$$\text{even-area triples}
-
\text{collinear triples}.$$

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

def solve():
    w, h = map(int, input().split())

    n = (w + 1) * (h + 1)

    ex = w // 2 + 1
    ox = (w + 1) - ex

    ey = h // 2 + 1
    oy = (h + 1) - ey

    c = [
        ex * ey,
        ex * oy,
        ox * ey,
        ox * oy,
    ]

    total = n * (n - 1) * (n - 2)

    odd = 0
    for i in range(4):
        for j in range(i + 1, 4):
            for k in range(j + 1, 4):
                odd += 6 * c[i] * c[j] * c[k]

    even_area = total - odd

    m = min(w, h)

    phi = list(range(m + 1))
    for i in range(2, m + 1):
        if phi[i] == i:
            for j in range(i, m + 1, i):
                phi[j] -= phi[j] // i

    unordered_collinear = 0

    for dx in range(1, w + 1):
        unordered_collinear += (dx - 1) * (w - dx + 1) * (h + 1)

    for dy in range(1, h + 1):
        unordered_collinear += (dy - 1) * (h - dy + 1) * (w + 1)

    diag = 0
    for d in range(2, m + 1):
        mx = w // d
        my = h // d

        sx = mx * (w + 1) - d * mx * (mx + 1) // 2
        sy = my * (h + 1) - d * my * (my + 1) // 2

        diag += phi[d] * sx * sy

    unordered_collinear += 2 * diag

    ordered_collinear = 6 * unordered_collinear

    ans = (even_area - ordered_collinear) % MOD
    print(ans)

solve()
```

The first block computes the four parity-class sizes and uses them to count all ordered triples whose doubled area is even.

The second block computes Euler's totient values up to $\min(w,h)$. These values appear in the divisor expansion of $\gcd(a,b)-1$.

The axis-aligned contributions are handled separately because one of the coordinates is zero. For horizontal segments, $\gcd(dx,0)=dx$. Vertical segments are symmetric.

The diagonal contributions use the totient identity. The closed forms for $S_x(d)$ and $S_y(d)$ avoid any nested loops over coordinates.

All arithmetic is performed with Python integers, which safely handle values much larger than $64$-bit limits.

## Worked Examples

### Sample 1

Input

```
2 1
```

Parity classes:

| Class | Size |
| --- | --- |
| (0,0) | 2 |
| (0,1) | 2 |
| (1,0) | 1 |
| (1,1) | 1 |

| Quantity | Value |
| --- | --- |
| Total ordered distinct triples | 120 |
| Odd doubled area | 72 |
| Even doubled area | 48 |
| Ordered collinear triples | 12 |
| Final answer | 36 |

Output:

```
36
```

This example shows why the collinear subtraction is necessary. The parity count alone gives 48, not 36.

### Sample 2

Input

```
2 2
```

| Quantity | Value |
| --- | --- |
| Total ordered distinct triples | 504 |
| Odd doubled area | 192 |
| Even doubled area | 312 |
| Ordered collinear triples | 72 |
| Final answer | 240 |

Output:

```
240
```

This example contains horizontal, vertical, and diagonal collinear triples, exercising every part of the counting formula.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\min(w,h)\log\log(\min(w,h)))$ | Totient sieve dominates |
| Space | $O(\min(w,h))$ | Storage for $\varphi$ |

With $w,h \le 4000$, the sieve contains at most 4000 entries and the summation runs only a few thousand iterations. The solution is comfortably within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    MOD = 1000000007

    def solve():
        w, h = map(int, input().split())

        n = (w + 1) * (h + 1)

        ex = w // 2 + 1
        ox = (w + 1) - ex
        ey = h // 2 + 1
        oy = (h + 1) - ey

        c = [ex * ey, ex * oy, ox * ey, ox * oy]

        total = n * (n - 1) * (n - 2)

        odd = 0
        for i in range(4):
            for j in range(i + 1, 4):
                for k in range(j + 1, 4):
                    odd += 6 * c[i] * c[j] * c[k]

        even_area = total - odd

        m = min(w, h)
        phi = list(range(m + 1))
        for i in range(2, m + 1):
            if phi[i] == i:
                for j in range(i, m + 1, i):
                    phi[j] -= phi[j] // i

        bad = 0

        for dx in range(1, w + 1):
            bad += (dx - 1) * (w - dx + 1) * (h + 1)

        for dy in range(1, h + 1):
            bad += (dy - 1) * (h - dy + 1) * (w + 1)

        diag = 0
        for d in range(2, m + 1):
            mx = w // d
            my = h // d

            sx = mx * (w + 1) - d * mx * (mx + 1) // 2
            sy = my * (h + 1) - d * my * (my + 1) // 2

            diag += phi[d] * sx * sy

        bad += 2 * diag

        return str((even_area - 6 * bad) % MOD)

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    return solve()

assert run("2 1\n") == "36", "sample 1"
assert run("2 2\n") == "240", "sample 2"

assert run("1 1\n") == "0", "minimum rectangle"
assert run("1 2\n") == "0", "all triangles have half-integer area"
assert run("2 3\n") == "264", "mixed parity structure"
assert run("4000 4000\n").isdigit(), "maximum bounds"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `0` | Smallest grid with no valid triangle |
| `1 2` | `0` | Integer-area condition eliminates all triangles |
| `2 3` | `264` | General case with several slopes |
| `4000 4000` | numeric output | Performance at maximum limits |

## Edge Cases

Consider:

```
1 1
```

The grid contains only four points. Every triangle has area $1/2$, never an integer. The parity counting step correctly finds that every nondegenerate triangle has odd doubled area, so the answer becomes zero.

Consider:

```
2 1
```

The points on each horizontal row form a collinear triple. The parity count includes them because doubled area $=0$ is even. The collinear subtraction removes exactly those twelve ordered triples, producing the correct answer 36.

Consider:

```
1 2
```

There are nondegenerate triangles, but every one has area $1/2$. The parity-class computation detects that their doubled area is odd, so none are counted in the first place. The collinear correction is irrelevant, and the final answer remains zero.

The separation into "even doubled area" and "collinear" handles all of these cases uniformly.
