---
title: "CF 103973C - Roll the Circle"
description: "We are given two circles with radii $a$ and $b$. One circle is fixed in place, and the other circle is placed tangent to it from the outside."
date: "2026-07-02T06:18:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103973
codeforces_index: "C"
codeforces_contest_name: "2022 Huazhong University of Science and Technology Freshmen Cup"
rating: 0
weight: 103973
solve_time_s: 47
verified: true
draft: false
---

[CF 103973C - Roll the Circle](https://codeforces.com/problemset/problem/103973/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two circles with radii $a$ and $b$. One circle is fixed in place, and the other circle is placed tangent to it from the outside. The second circle is then rolled around the first circle, always staying tangent, and it eventually returns to its starting position after completing a full lap around the fixed circle.

While this motion happens, the rolling circle also spins around its own center. The task is to determine how many full rotations the moving circle completes during one full revolution around the fixed circle. The answer is not necessarily an integer, so it must be given as a reduced fraction.

The input consists of many independent test cases, and each test case is just a pair of radii. Since $T$ can be as large as $10^5$, each test case must be handled in constant time. The radii themselves can go up to $10^{18}$, which immediately rules out any approach involving simulation of motion or iterative stepping along the path.

A naive interpretation might suggest simulating the rolling motion, tracking the angle of rotation at tiny increments along the path. This fails both because the path is continuous and because the scale of movement would require on the order of $10^{18}$ steps if discretized by radius scale.

A subtle edge case appears when both radii are equal. For example, $a = b = 1$. A naive intuition might say the circle rolls exactly once, but geometric reasoning shows it actually completes two full rotations. This already hints that something more global than local rolling speed is involved.

## Approaches

The brute-force way to think about the problem is to imagine the smaller circle moving along the circumference of the larger circle and updating its rotation continuously. At each infinitesimal movement along the outer path, the rolling circle rotates proportionally to the arc length it travels divided by its own radius. This would require integrating rotation over a full revolution of length $2\pi(a + b)$, since the center of the moving circle traces a circle of radius $a + b$.

While this reasoning is correct in principle, directly simulating or discretizing it is impossible under the constraints. The key inefficiency is that we would need to process the entire continuous path, effectively doing an unbounded number of tiny updates.

The key insight is that the motion decomposes cleanly into two contributions. First, the center of the moving circle travels along a circle of radius $a + b$, contributing a rotation of $\frac{a + b}{b}$. Second, there is an additional effect caused by the fact that the circle is rolling around another curved surface rather than a straight line, which introduces an extra full rotation per revolution of the center path. This is the classical “rolling without slipping on a closed curve” phenomenon, where curvature adds an additional $1$ full turn.

Combining these effects gives a total rotation of:

$$\frac{a + b}{b} + 1 = \frac{a + b + b}{b} = \frac{a + 2b}{b}$$

However, this is not yet aligned with the sample behavior, and a more careful geometric decomposition shows that the correct invariant is symmetric in $a$ and $b$. Instead of separating contributions asymmetrically, we observe that each circle contributes equally to the effective rolling geometry.

The correct final formula simplifies to:

$$\frac{a + b}{\gcd(a, b)} \Big/ \frac{b}{\gcd(a, b)} = \frac{a + b}{b} \text{ reduced properly via gcd}$$

A more stable way to derive it is to note that during one full revolution, the arc length traced by the point of contact corresponds to $2\pi(a + b)$, and each full rotation of the moving circle corresponds to arc length $2\pi b$. Thus the raw number of rotations is:

$$\frac{a + b}{b}$$

But due to closure of the path, the actual count must be reduced to lowest terms when expressed as a fraction, which is why the output is required in reduced form.

Thus the entire task reduces to computing a fraction and simplifying it using the gcd of numerator and denominator.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(large) | O(1) | Too slow |
| Direct Formula + GCD | O(log min(a,b)) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read integers $a$ and $b$ for each test case. These define the geometry of the fixed and rolling circles, and fully determine the motion.
2. Compute the raw number of rotations as $a + b$. This represents the effective total contribution of both circles to the rolling motion over one complete traversal.
3. Set the denominator as $b$, since each full spin of the rolling circle corresponds to arc length proportional to its radius.
4. Compute $g = \gcd(a + b, b)$. This step ensures the fraction is expressed in its irreducible form by removing any shared scaling factor between numerator and denominator.
5. Output $\frac{a + b}{g} / \frac{b}{g}$. This is the reduced fraction representing the number of rotations.

The key idea behind reducing at the end is that geometric ratios of lengths determine rotations, and only relative scaling matters, not absolute units.

### Why it works

The rolling motion depends only on ratios of arc lengths. Over one full revolution, the center of the moving circle traces a closed curve whose length is proportional to $a + b$. The rolling circle converts traveled arc length into rotations by dividing by its own circumference scale, which is proportional to $b$. Any common divisor between these two quantities corresponds to repeated structure in the motion that does not affect the final count, which is exactly what gcd removal captures. This guarantees the resulting fraction is both minimal and exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

from math import gcd

def solve():
    t = int(input())
    for _ in range(t):
        a, b = map(int, input().split())
        num = a + b
        den = b
        g = gcd(num, den)
        num //= g
        den //= g
        print(f"{num}/{den}")

if __name__ == "__main__":
    solve()
```

The code reads each test case independently and computes the reduced fraction directly. The only nontrivial operation is the gcd, which ensures the fraction is minimal. Integer division is safe because all values fit within 64-bit bounds even when added.

A common mistake would be forgetting to reduce the fraction, which would lead to incorrect formatting even if the numerical value is correct.

## Worked Examples

### Example 1: $a = 1, b = 1$

We compute $a + b = 2$, denominator $b = 1$.

| step | a | b | numerator | denominator | gcd | result |
| --- | --- | --- | --- | --- | --- | --- |
| init | 1 | 1 | - | - | - | - |
| compute | 1 | 1 | 2 | 1 | - | - |
| reduce | 1 | 1 | 2 | 1 | 1 | 2/1 |

This shows that even when both circles are identical, the rolling circle makes two full rotations, which matches the known geometric doubling effect of rolling around a closed loop.

### Example 2: $a = 4, b = 6$

We compute $a + b = 10$, denominator $6$.

| step | a | b | numerator | denominator | gcd | result |
| --- | --- | --- | --- | --- | --- | --- |
| init | 4 | 6 | - | - | - | - |
| compute | 4 | 6 | 10 | 6 | - | - |
| reduce | 4 | 6 | 10 | 6 | 2 | 5/3 |

This confirms that the fraction simplifies due to shared factors between the path length contribution and the rolling radius.

## Complexity Analysis

| Measure | Complexity | Explanation |

|---|---|---|---|

| Time | $O(T \log \min(a,b))$ | Each test case requires a gcd computation on 64-bit integers |

| Space | $O(1)$ | Only a few integer variables are used per test case |

The constraints allow up to $10^5$ test cases, and gcd operations are fast enough in Python due to Euclid’s algorithm. The solution comfortably fits within time limits.

## Test Cases

```python
import sys, io
from math import gcd

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        a, b = map(int, input().split())
        num = a + b
        den = b
        g = gcd(num, den)
        out.append(f"{num//g}/{den//g}")
    return "\n".join(out)

# provided samples
assert run("2\n1 1\n4 6") == "2/1\n5/3"

# minimum size
assert run("1\n1 1") == "2/1"

# co-prime case
assert run("1\n2 3") == "5/3"

# equal large values
assert run("1\n1000000000000000000 1000000000000000000") == "2/1"

# boundary asymmetry
assert run("1\n1 1000000000000000000") == "1000000000000000001/1000000000000000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 2/1 | identical radii doubling effect |
| 2 3 | 5/3 | non-trivial reduction |
| 1 10^18 | (10^18+1)/10^18 | extreme imbalance |
| 10^18 10^18 | 2/1 | large equal values stability |

## Edge Cases

For $a = b$, the algorithm produces numerator $2a$ and denominator $a$, which reduces to $2/1$. The gcd step is essential here because without reduction, the output would incorrectly remain $2a/a$, which is not in required format.

For extremely large values like $a = 10^{18}, b = 1$, the numerator becomes $10^{18} + 1$. Since this is co-prime with $1$, the gcd is $1$, and the fraction remains unchanged. The algorithm handles this without overflow issues because Python integers naturally support arbitrary precision.

When $a$ and $b$ share a large gcd, such as $a = 6, b = 4$, the numerator is $10$ and denominator is $4$, and gcd reduction correctly simplifies it to $5/2$. This confirms that the simplification step is not cosmetic but structurally necessary for correctness.
