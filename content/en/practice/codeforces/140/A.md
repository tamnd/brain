---
title: "CF 140A - New Year Table"
description: "We have a large circular table with radius R and want to place n identical circular plates, each with radius r. Every plate must satisfy three conditions simultaneously. First, the entire plate must stay inside the table. Second, every plate must touch the boundary of the table."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "math"]
categories: ["algorithms"]
codeforces_contest: 140
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 100"
rating: 1700
weight: 140
solve_time_s: 105
verified: true
draft: false
---

[CF 140A - New Year Table](https://codeforces.com/problemset/problem/140/A)

**Rating:** 1700  
**Tags:** geometry, math  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a large circular table with radius `R` and want to place `n` identical circular plates, each with radius `r`.

Every plate must satisfy three conditions simultaneously.

First, the entire plate must stay inside the table.

Second, every plate must touch the boundary of the table.

Third, no two plates may overlap, although touching is allowed.

The task is simply to decide whether such an arrangement exists.

The constraints are tiny. All values are at most 1000, and there is only one test case. This immediately tells us the challenge is not about optimization, but about deriving the correct geometric condition. Any algorithm from constant time up to even quadratic time would fit comfortably within the limits. The real difficulty is avoiding incorrect geometry reasoning and handling corner cases cleanly.

The most dangerous edge cases come from small values of `n`.

Consider this input:

```
1 5 10
```

The correct answer is:

```
NO
```

A single plate must still fit inside the table. Since the plate radius exceeds the table radius, placement is impossible. A careless solution that only checks spacing between plates might incorrectly accept this case because there are no other plates to collide with.

Now look at:

```
2 4 2
```

The correct answer is:

```
YES
```

Each plate has diameter `4`, equal to the table radius. The two plates can sit opposite each other and touch at exactly one point. Implementations using strict inequalities instead of non-strict inequalities often reject this valid configuration.

The trickiest case is:

```
2 2 1
```

The correct answer is:

```
YES
```

The centers of the two plates lie on a circle of radius `R - r = 1`. Opposite points on that circle are distance `2` apart, exactly equal to `2r`, so the plates touch but do not overlap.

Another subtle case is:

```
3 2 1
```

The correct answer is:

```
NO
```

Many incorrect solutions only check whether `2r <= R`, which is true here. But three unit circles cannot all touch the boundary of a radius-2 table without overlapping.

## Approaches

The brute-force way to think about the problem is to imagine placing plate centers on the circle of radius `R - r`, because every plate touching the table boundary forces its center to stay exactly that far from the table center.

If we tried all angular arrangements of `n` points around this circle and checked pairwise distances between plates, we would eventually find a valid arrangement when one exists. This is conceptually correct because the geometry is completely determined by the center positions.

The problem is that continuous geometry has infinitely many configurations. Even discretizing angles finely enough would still be awkward and unnecessary. The constraints are small, but numerical searching is the wrong tool here because the structure is highly symmetric.

The key observation is that the best arrangement is always evenly spaced around the table.

Each plate center lies on the same circle of radius `R - r`. If we distribute the centers uniformly, neighboring centers form equal angles of `2π / n`. The distance between neighboring centers becomes the chord length:

$$2(R-r)\sin\left(\frac{\pi}{n}\right)$$

For the plates not to overlap, this distance must be at least `2r`.

So we need:

$$2(R-r)\sin\left(\frac{\pi}{n}\right) \ge 2r$$

This simplifies to:

$$(R-r)\sin\left(\frac{\pi}{n}\right) \ge r$$

There is an even cleaner way to avoid trigonometry entirely.

When `n >= 2`, the plates can fit iff:

$$R \ge 2r$$

and additionally the circumference arrangement has enough room. Codeforces editorial solutions usually derive the equivalent condition:

$$n \cdot r \le R$$

only for special geometry interpretations, but that is not correct here.

The correct standard derivation is:

For `n = 1`, we only need `r <= R`.

For `n = 2`, two plates fit iff `2r <= R`.

For `n >= 3`, evenly spaced centers form a regular polygon, and the exact condition becomes:

$$\sin\left(\frac{\pi}{n}\right) \ge \frac{r}{R-r}$$

Using direct geometry is the safest approach.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Infinite / impractical | O(1) | Too slow |
| Optimal Geometry | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `R`, and `r`.
2. Handle the case `n == 1`.

A single plate only needs to fit inside the table while touching the boundary. This is possible exactly when `r <= R`.
3. Handle the case `n == 2`.

The two plate centers must lie on opposite sides of the circle of radius `R-r`. The maximum distance between them is the diameter:

$$2(R-r)$$

The plates avoid overlap iff this is at least `2r`.

That simplifies to:

$$R \ge 2r$$
4. Handle the case `n >= 3`.

Place centers evenly around the circle of radius `R-r`.

The angle between neighboring centers is:

$$\frac{2\pi}{n}$$

The chord length between neighbors is:

$$2(R-r)\sin\left(\frac{\pi}{n}\right)$$

The plates fit iff this distance is at least `2r`.
5. Print `"YES"` if the inequality holds, otherwise print `"NO"`.

### Why it works

Every valid plate center must lie exactly on the circle of radius `R-r`, because the plate touches the table boundary internally.

Among all arrangements of `n` points on a circle, the regular polygon maximizes the minimum distance between neighboring points. If even the optimal symmetric arrangement causes overlap, no irregular arrangement can do better.

The algorithm checks exactly this optimal configuration. The distance condition guarantees neighboring plates do not intersect, which automatically guarantees all pairs are non-overlapping because neighboring pairs are the closest.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    n, R, r = map(int, input().split())

    if n == 1:
        print("YES" if r <= R else "NO")
        return

    if R < 2 * r:
        print("NO")
        return

    if n == 2:
        print("YES")
        return

    lhs = (R - r) * math.sin(math.pi / n)

    eps = 1e-12

    if lhs + eps >= r:
        print("YES")
    else:
        print("NO")

solve()
```

The first branch handles the singleton case separately because the geometry changes completely when there is only one plate. Many wrong submissions forget this and incorrectly apply the multi-plate formula.

The next check eliminates impossible configurations early. If `R < 2r`, even two opposite plates cannot fit.

For `n >= 3`, the implementation directly evaluates the geometric inequality derived from the regular polygon arrangement. Floating-point precision matters because valid cases may involve exact equality. The epsilon avoids rejecting configurations due to tiny rounding errors.

The expression:

```
(R - r) * math.sin(math.pi / n)
```

comes from halving the chord-length inequality. This keeps the arithmetic slightly cleaner and avoids unnecessary multiplication by 2.

## Worked Examples

### Example 1

Input:

```
4 10 4
```

| Variable | Value |
| --- | --- |
| n | 4 |
| R | 10 |
| r | 4 |
| R - r | 6 |
| sin(pi / n) | sin(pi / 4) ≈ 0.7071 |
| lhs | 6 × 0.7071 ≈ 4.2426 |
| Compare with r | 4.2426 ≥ 4 |

Output:

```
YES
```

This example shows a standard successful arrangement. The neighboring plate centers are far enough apart for the circles to touch without overlap.

### Example 2

Input:

```
3 2 1
```

| Variable | Value |
| --- | --- |
| n | 3 |
| R | 2 |
| r | 1 |
| R - r | 1 |
| sin(pi / n) | sin(pi / 3) ≈ 0.8660 |
| lhs | 1 × 0.8660 = 0.8660 |
| Compare with r | 0.8660 < 1 |

Output:

```
NO
```

This demonstrates why simply checking `R >= 2r` is insufficient. Two plates fit, but three do not.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed |
| Space | O(1) | No extra data structures are used |

The constraints are extremely small, so performance is never an issue. The solution runs instantly and uses constant memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, R, r = map(int, input().split())

    out = []

    if n == 1:
        out.append("YES" if r <= R else "NO")
    else:
        if R < 2 * r:
            out.append("NO")
        elif n == 2:
            out.append("YES")
        else:
            lhs = (R - r) * math.sin(math.pi / n)
            eps = 1e-12

            if lhs + eps >= r:
                out.append("YES")
            else:
                out.append("NO")

    return "\n".join(out) + "\n"

# provided sample
assert run("4 10 4\n") == "YES\n", "sample 1"

# minimum values
assert run("1 1 1\n") == "YES\n", "single plate exact fit"

# single plate too large
assert run("1 3 4\n") == "NO\n", "single plate impossible"

# boundary case for two plates
assert run("2 2 1\n") == "YES\n", "two touching plates"

# three plates impossible
assert run("3 2 1\n") == "NO\n", "three plates overlap"

# large valid configuration
assert run("6 1000 1\n") == "YES\n", "large table"

# equality edge case
assert run("2 4 2\n") == "YES\n", "exact boundary equality"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `YES` | Single plate exact fit |
| `1 3 4` | `NO` | Plate larger than table |
| `2 2 1` | `YES` | Equality for two touching plates |
| `3 2 1` | `NO` | Multi-plate overlap case |
| `6 1000 1` | `YES` | Large-radius easy configuration |
| `2 4 2` | `YES` | Non-strict inequality handling |

## Edge Cases

Consider the input:

```
1 3 4
```

The algorithm immediately enters the `n == 1` branch. Since `r > R`, the plate cannot fit inside the table even before considering boundary touching. The output becomes:

```
NO
```

This case is important because the general multi-plate geometry formula does not apply cleanly when there is only one plate.

Now examine:

```
2 2 1
```

The algorithm skips the singleton branch. Since `R = 2r`, the early impossibility test passes exactly at equality. Because `n == 2`, the algorithm prints:

```
YES
```

The two plates sit opposite each other and touch at one point. Strict comparisons would incorrectly reject this valid arrangement.

Finally, consider:

```
3 2 1
```

The computation becomes:

$$(R-r)\sin(\pi/3)=1 \times 0.8660$$

Since this value is smaller than `r = 1`, neighboring plates would overlap. The algorithm correctly prints:

```
NO
```

This case proves why checking only `R >= 2r` is insufficient once the number of plates exceeds two.
