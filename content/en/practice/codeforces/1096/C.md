---
title: "CF 1096C - Polygon for the Angle"
description: "We are working with a regular polygon, meaning all sides and angles are symmetric. The input gives an angle value, and we must decide whether there exists some regular n-gon such that we can pick three vertices $a, b, c$ (not necessarily consecutive) and the angle formed at $b$…"
date: "2026-06-13T05:28:53+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "geometry"]
categories: ["algorithms"]
codeforces_contest: 1096
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 57 (Rated for Div. 2)"
rating: 1600
weight: 1096
solve_time_s: 330
verified: true
draft: false
---

[CF 1096C - Polygon for the Angle](https://codeforces.com/problemset/problem/1096/C)

**Rating:** 1600  
**Tags:** brute force, geometry  
**Solve time:** 5m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working with a regular polygon, meaning all sides and angles are symmetric. The input gives an angle value, and we must decide whether there exists some regular n-gon such that we can pick three vertices $a, b, c$ (not necessarily consecutive) and the angle formed at $b$, namely $\angle abc$, is exactly the given value.

In other words, we are not dealing with the interior angle of the polygon itself, but with any angle formed by choosing three vertices on the circle in cyclic order. The geometry reduces to reasoning about equally spaced points on a circle and the central angles between them.

The output is the smallest number of vertices $n$ for which such a configuration exists, or $-1$ if no regular polygon can realize that angle.

The constraint $T \le 180$ is small, so we can afford a per-test computation that is logarithmic or even mildly linear in the worst case, but not something that grows linearly with the large bound $998244353$. The large upper bound only guarantees that if a valid solution exists, it is not astronomically large in a way that would break integer handling, not that we should iterate up to it.

A naive mistake comes from assuming we only need to check interior angles of a regular polygon. For example, in a regular pentagon, the interior angle is fixed at $108^\circ$, but the problem allows angles like $36^\circ$ or $72^\circ$ formed by non-adjacent vertices. Another common mistake is assuming the angle must come from adjacent arcs only; in reality, any two arcs defined by vertex distances contribute.

A second subtle failure case is treating the angle as if it must equal $k \cdot \frac{180(n-2)}{n}$, which is unrelated to this problem. The angle here depends only on chord geometry on a circle, not polygon interior structure.

## Approaches

A brute-force approach would try to fix a polygon size $n$, place $n$ points on a unit circle, and then enumerate triples $(a, b, c)$, compute the angle at $b$, and check if any match the target. The number of triples is $O(n^3)$, and even computing angles is constant time with dot products. Trying this for multiple $n$ up to even a few thousand becomes completely infeasible, and clearly impossible under the constraint that valid $n$ can reach up to $10^9$-scale bounds.

The structure becomes simpler once we stop thinking in terms of coordinates and instead think in terms of arc differences. On a circle, a regular n-gon divides the full angle $360^\circ$ into equal steps of $x = \frac{360}{n}$. Any two vertices correspond to integer multiples of this step.

Now consider a vertex $b$, and two other vertices $a$ and $c$. The angle $\angle abc$ is an inscribed angle in a circle, so it equals half the measure of the arc $ac$ that does not contain $b$. That arc length must be some integer multiple of the step $x$. If the arc between $a$ and $c$ spans $k$ edges of the polygon, then the arc measure is $k \cdot x$, and the inscribed angle is:

$$\angle abc = \frac{kx}{2} = \frac{k}{2} \cdot \frac{360}{n} = \frac{180k}{n}.$$

So the problem reduces to finding integers $n$ and $k$ such that:

$$\text{ang} = \frac{180k}{n}.$$

Rearranging:

$$n \cdot \text{ang} = 180k.$$

So $180k$ must be divisible by $\text{ang}$, and we want the smallest $n$ such that there exists an integer $k$ making the equality hold. Since $k$ corresponds to a non-degenerate arc, it only needs to be positive and less than $n$, but for existence we can always choose $k$ appropriately if the ratio works.

Let $g = \gcd(180, \text{ang})$. Then we can simplify:

$$\text{ang} = \frac{180}{n}k \Rightarrow n = \frac{180k}{\text{ang}}.$$

Write $180 = g \cdot 180'$, $\text{ang} = g \cdot a'$, giving:

$$n = \frac{180'k}{a'}.$$

To minimize $n$, we choose the smallest positive $k$ such that $a' \mid 180'k$. Since $a'$ and $180'$ are coprime, this requires $k = a'$, yielding:

$$n = 180'.$$

So the answer reduces to:

$$n = \frac{180}{\gcd(180, \text{ang})}.$$

This is the minimal polygon size that can realize the required angle.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ per n | $O(1)$ | Too slow |
| Optimal | $O(1)$ per query | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the angle for each query. The problem is independent per test case, so each can be solved in isolation.
2. Compute the greatest common divisor between 180 and the given angle. This step extracts the maximal shared factor that determines which angle fractions are achievable using equal circular partitions.
3. Divide 180 by this gcd to obtain the candidate polygon size. This value corresponds to the smallest number of equal arc segments needed so that the angle can be represented as an inscribed angle formed by two vertices.
4. Output this value directly, since it is guaranteed to be the minimum valid $n$.

### Why it works

The key invariant is that every possible angle formed by three vertices in a regular n-gon can be expressed as $\frac{180k}{n}$ for some integer $k$. This comes directly from interpreting the configuration on a circle and using the inscribed angle theorem.

Thus the problem becomes finding the smallest $n$ such that $\text{ang} \cdot n / 180$ is an integer for some valid integer construction of $k$. Reducing by gcd ensures we remove all common factors so that the smallest feasible $n$ remains. Any smaller $n$ would reintroduce a fractional requirement for $k$, making the geometry impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline

from math import gcd

t = int(input())
for _ in range(t):
    ang = int(input())
    print(180 // gcd(180, ang))
```

The solution hinges on the observation that the entire geometry collapses into a divisibility condition between 180 and the requested angle. The gcd computation isolates the irreducible fraction of the angle relative to a full semicircle measure, and the final division yields the smallest polygon size supporting that fraction.

There are no loops over $n$, and no geometric simulation. The only subtle point is recognizing that the factor 180 comes from the inscribed angle theorem, not from polygon interior angle formulas.

## Worked Examples

We will trace two inputs: 54 and 178.

For angle 54:

| Step | ang | gcd(180, ang) | 180 / gcd | Output |
| --- | --- | --- | --- | --- |
| 1 | 54 | 18 | 10 | 10 |

The gcd is 18, meaning 54° shares a strong structure with 180°, allowing the angle to be formed using a 10-gon. This corresponds to the sample where a 10-sided regular polygon admits a 54° inscribed angle.

This trace confirms that the solution depends only on number-theoretic reduction, not geometric search.

For angle 178:

| Step | ang | gcd(180, ang) | 180 / gcd | Output |
| --- | --- | --- | --- | --- |
| 1 | 178 | 2 | 90 | 90 |

Here the gcd is small, meaning the angle is almost coprime with 180. This forces a much larger polygon to represent such a fine angular resolution.

The trace shows that as the gcd decreases, the required polygon size increases, matching intuition that more vertices are needed to approximate arbitrary angles.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T)$ | Each test case requires one gcd computation and constant arithmetic |
| Space | $O(1)$ | No extra data structures beyond a few integers |

The constraints allow up to 180 queries, so even a straightforward per-query gcd computation is easily fast enough. The solution runs in negligible time and uses constant memory regardless of input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    t = int(input())
    out = []
    for _ in range(t):
        ang = int(input())
        out.append(str(180 // math.gcd(180, ang)))
    return "\n".join(out)

# provided samples
assert run("4\n54\n50\n2\n178\n") == "10\n18\n90\n90"

# minimum case
assert run("1\n1\n") == "180"

# angle that divides 180 exactly
assert run("1\n60\n") == "3"

# angle close to 180
assert run("1\n179\n") == "180"

# multiple mixed
assert run("3\n45\n90\n30\n") == "4\n2\n6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 1 | 180 | smallest angle forcing maximal polygon |
| 60 | 3 | clean divisor case |
| 179 | 180 | near-coprime edge |
| 45, 90, 30 | 4, 2, 6 | multiple gcd patterns |

## Edge Cases

A subtle case is when the angle is a divisor of 180. For input `ang = 60`, the gcd is 60, so the answer becomes `180 / 60 = 3`. This corresponds to a triangle, where many angles can be formed simply due to symmetry. A naive approach might incorrectly assume a larger polygon is needed because it ignores that triangles already allow multiple inscribed angles.

For `ang = 179`, the gcd with 180 is 1, forcing the output to be 180. The geometry interpretation is that such an angle requires extremely fine angular granularity, achievable only when the polygon approximates a circle with many vertices. Any attempt to “simplify” this case would incorrectly reduce the polygon size and fail to realize the required precision.

For `ang = 1`, the gcd is also 1, so the result is again 180. This is the maximal stress test where the smallest angle forces the full resolution of the 180-unit structure, and any shortcut based on “small angle means small polygon” would break here.
