---
title: "CF 102218H - Heartbreaker Radio Station"
description: "We have (n) sinusoidal waves. Every wave oscillates with the same angular frequency (omega), but each has its own amplitude (Ai) and phase (phii)."
date: "2026-08-18T12:52:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102218
codeforces_index: "H"
codeforces_contest_name: "2019, XI Annual Programming Contest by ESCOM-IPN"
rating: 0
weight: 102218
solve_time_s: 147
verified: false
draft: false
---

[CF 102218H - Heartbreaker Radio Station](https://codeforces.com/problemset/problem/102218/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We have (n) sinusoidal waves. Every wave oscillates with the same angular frequency (\omega), but each has its own amplitude (A_i) and phase (\phi_i). Their sum is guaranteed to be representable as one more sinusoid with that same frequency, and we need to recover its amplitude (A) and phase (\phi).

The input gives (n), the common frequency, and then (n) pairs ((A_i,\phi_i)). The output is a pair ((A,\phi)) such that

A\sin(\omega t+\phi)
]

for every (t), with (A\ge 0) and (0\le\phi<2\pi).

The frequency itself does not affect the calculation. Since every term has exactly the same (\omega), we only need to combine their amplitudes and phases.

The value (n) can reach (10^5). A solution that compares every wave with every other wave would perform roughly (10^{10}) pairwise operations in the worst case, which is far beyond a two-second time limit. We need a linear or near-linear algorithm. The amplitudes are at most (100), so the accumulated coefficients are at most about (10^7), comfortably inside ordinary floating-point range. The phase values are already given in radians and lie in one full revolution.

There are several numerical edge cases that can make a seemingly reasonable implementation wrong. Consider a single wave:

```
1 1
5 0
```

The result is exactly (5) with phase (0). A solution that unnecessarily modifies the phase or uses a formula involving division by one trigonometric component can fail when that component is zero.

A second case is a wave pointing in the opposite direction:

```
1 1
5 3.141592653589793
```

The result has amplitude (5) and phase (\pi). Computing the phase with `atan(y / x)` is unsafe because (x) can be zero and, more importantly, the signs of (x) and (y) determine the quadrant. `atan2` is designed for exactly this situation.

Finally, complete cancellation is possible:

```
2 1
1 0
1 3.141592653589793
```

The two waves are negatives of each other, so the result is the zero function. Its amplitude is (0), and its phase is mathematically irrelevant because (0\sin(\omega t+\phi)=0) for every (\phi). A floating-point implementation may leave a tiny residual instead of exact zero, which is harmless within the required error tolerance.

There is also a boundary case around (2\pi). For example,

```
2 1
1 0
1 6.283185307079586
```

has a resultant phase extremely close to (2\pi), not a negative angle. Since `atan2` returns angles in ([-\pi,\pi]), negative results must be shifted by (2\pi).

## Approaches

A direct approach would try to evaluate the sum as a function of (t), perhaps at several points, and then recover the amplitude and phase from those values. That is unnecessary, and evaluating many points for every wave would only add work. A more algebraic brute-force approach could repeatedly combine two sinusoids using trigonometric identities. Although each individual combination is correct, repeatedly manipulating the expressions can still introduce unnecessary work and numerical complexity. If every pair of waves is considered, the worst case is on the order of (n^2=10^{10}) operations.

The useful observation is that the phase shift can be expanded before doing any summation. For one wave,

A_i\sin(\omega t)\cos\phi_i
+
A_i\cos(\omega t)\sin\phi_i.
]

Every wave is thus just a linear combination of the same two functions, (\sin(\omega t)) and (\cos(\omega t)). We can add their coefficients independently.

Define

[
X=\sum_{i=1}^{n} A_i\cos\phi_i
]

and

[
Y=\sum_{i=1}^{n} A_i\sin\phi_i.
]

Then the complete sum becomes

[
f(t)=X\sin(\omega t)+Y\cos(\omega t).
]

Now expand the desired single wave:

A\cos\phi\sin(\omega t)
+
A\sin\phi\cos(\omega t).
]

Matching coefficients gives

[
A\cos\phi=X,
\qquad
A\sin\phi=Y.
]

The pair ((X,Y)) can be viewed as a two-dimensional vector. Its length is the resulting amplitude,

[
A=\sqrt{X^2+Y^2},
]

and its direction is the resulting phase,

[
\phi=\operatorname{atan2}(Y,X).
]

This reduces the entire problem to one pass through the input. The brute-force works because sinusoidal waves can be combined algebraically, but it fails to exploit the fact that every wave uses the same two basis functions. The observation that all terms reduce to coefficients of (\sin(\omega t)) and (\cos(\omega t)) lets us replace the whole collection of waves by one accumulated two-dimensional vector.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(1)) | Too slow |
| Optimal | (O(n)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read (n) and (\omega). The value of (\omega) is not needed afterward because it is identical for every wave, so all the work can be done using the amplitudes and phases.
2. Initialize two accumulators, (X=0) and (Y=0). They will store the coefficients of (\sin(\omega t)) and (\cos(\omega t)) in the complete sum.
3. For every wave ((A_i,\phi_i)), add (A_i\cos\phi_i) to (X) and (A_i\sin\phi_i) to (Y). This follows directly from expanding (\sin(\omega t+\phi_i)).
4. Compute the resulting amplitude with

[
A=\operatorname{hypot}(X,Y).
]

This is the Euclidean length of the coefficient vector and is numerically preferable to manually writing (\sqrt{X^2+Y^2}).
5. Compute the phase with

[
\phi=\operatorname{atan2}(Y,X).
]

`atan2` uses both coordinates, so it chooses the correct quadrant. Python's `math.atan2` returns an angle in the range from (-\pi) to (\pi).
6. If the phase is negative, add (2\pi). The required output interval is ([0,2\pi)), so this converts the `atan2` convention to the convention required by the problem.
7. Print (A) and (\phi) with enough decimal digits. Printing twelve digits after the decimal point gives much more precision than the required (10^{-6}).

### Why it works

After processing any prefix of the waves, (X) is exactly the coefficient contributed by that prefix to (\sin(\omega t)), while (Y) is exactly its coefficient for (\cos(\omega t)). Adding another wave updates these coefficients by precisely (A_i\cos\phi_i) and (A_i\sin\phi_i), so the invariant remains true for every input line.

After all waves have been processed, the complete function is

[
X\sin(\omega t)+Y\cos(\omega t).
]

Choosing (A=\sqrt{X^2+Y^2}) and (\phi=\operatorname{atan2}(Y,X)) gives (A\cos\phi=X) and (A\sin\phi=Y). Substituting those identities into (A\sin(\omega t+\phi)) reproduces the accumulated function exactly, apart from floating-point rounding. The phase normalization only adds a full revolution, which does not change a sinusoid.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    n, omega = input().split()
    n = int(n)

    x = 0.0
    y = 0.0

    for _ in range(n):
        a, phi = map(float, input().split())
        x += a * math.cos(phi)
        y += a * math.sin(phi)

    amplitude = math.hypot(x, y)
    phase = math.atan2(y, x)

    if phase < 0.0:
        phase += 2.0 * math.pi

    print(f"{amplitude:.12f} {phase:.12f}")

if __name__ == "__main__":
    solve()
```

The first line reads `omega`, but the implementation deliberately does not use it. The common frequency is already present in every term and never changes during the coefficient matching.

The variables `x` and `y` correspond directly to the two coefficients derived in the algorithm. Each input wave contributes one vector of length (A_i) at angle (\phi_i), so accumulating these two components is equivalent to vector addition.

`math.hypot(x, y)` computes the length of that accumulated vector. Python documents `hypot` as the Euclidean norm of its arguments, which is exactly the amplitude calculation required here.

`math.atan2(y, x)` is used instead of `math.atan(y / x)`. Besides avoiding division by zero, it preserves the signs of both coordinates and consequently selects the correct quadrant.

The negative-phase adjustment is deliberately performed after `atan2`. Adding (2\pi) only when the result is negative maps the returned angle into the required interval without changing its sine or cosine.

No integer arithmetic is involved in the trigonometric calculations, so integer overflow is not an issue. The largest possible accumulated coordinate is around (10^7), which is easily represented by a double-precision floating-point number.

## Worked Examples

### Sample 1

For the first sample, each wave contributes a vector

[
(A_i\cos\phi_i,\ A_i\sin\phi_i).
]

The following table shows the accumulated vector after each input line. Values are rounded here for readability; the program keeps full floating-point precision.

| Wave | (A_i) | (\phi_i) | (X) after wave | (Y) after wave |
| --- | --- | --- | --- | --- |
| 1 | 93.22 | 5.53 | 67.96 | -63.80 |
| 2 | 48.58 | 0.86 | 99.65 | -26.99 |
| 3 | 15.31 | 5.39 | 109.24 | -38.93 |
| 4 | 5.66 | 4.12 | 106.08 | -43.63 |
| 5 | 48.53 | 6.09 | 153.71 | -52.95 |
| 6 | 6.60 | 1.42 | 154.70 | -46.43 |
| 7 | 21.15 | 0.06 | 175.81 | -45.16 |
| 8 | 4.27 | 5.47 | 178.74 | -48.26 |

The final vector points slightly below the positive (X)-axis, so `atan2` returns a small negative angle. Adding (2\pi) moves it into the required range. Using the unrounded internal values gives approximately

[
A=185.184472750,
\qquad
\phi=6.019915094,
]

matching the sample output.

The trace demonstrates the main invariant: regardless of how many waves have already been processed, the two accumulated values completely describe their sum at the common frequency.

### Constructed Example

Consider

```
2 1
1 0
1 1.5707963267948966
```

The first wave is (\sin(t)). The second is (\sin(t+\pi/2)=\cos(t)).

| Wave | (A_i) | (\phi_i) | (X) after wave | (Y) after wave |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1.000000 | 0.000000 |
| 2 | 1 | (\pi/2) | 1.000000 | 1.000000 |

The final amplitude is

[
A=\sqrt{1^2+1^2}=\sqrt2,
]

and the phase is

[
\phi=\operatorname{atan2}(1,1)=\frac{\pi}{4}.
]

Thus the result is

```
1.414213562373 0.785398163397
```

This example makes the coefficient matching especially visible because the two original waves contribute directly to different basis functions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Each of the (n) waves requires one sine, one cosine, and constant-time arithmetic. |
| Space | (O(1)) | Only the two accumulated coefficients and a few scalar values are stored. |

With (n\le 10^5), the algorithm performs only one pass over the input and never stores the wave list. Its memory usage is constant, and its time grows linearly with the number of waves, which comfortably fits the stated limits.

## Test Cases

The test harness below checks numerical answers rather than comparing formatted strings. This is necessary because many different decimal representations can satisfy the problem's error tolerance.

```python
import math
import io
import sys

def solve_text(inp: str) -> str:
    data = inp.strip().split()
    it = iter(data)

    n = int(next(it))
    omega = float(next(it))

    x = 0.0
    y = 0.0

    for _ in range(n):
        a = float(next(it))
        phi = float(next(it))
        x += a * math.cos(phi)
        y += a * math.sin(phi)

    amplitude = math.hypot(x, y)
    phase = math.atan2(y, x)

    if phase < 0.0:
        phase += 2.0 * math.pi

    return f"{amplitude:.12f} {phase:.12f}"

def run(inp: str):
    out = solve_text(inp)
    a, p = map(float, out.split())
    return a, p

def phase_distance(a, b):
    d = abs(a - b) % (2.0 * math.pi)
    return min(d, 2.0 * math.pi - d)

# Provided sample
a, p = run(
    """8 66.82
93.22 5.53
48.58 0.86
15.31 5.39
5.66 4.12
48.53 6.09
6.60 1.42
21.15 0.06
4.27 5.47
"""
)
assert abs(a - 185.184472750) <= 1e-6
assert phase_distance(p, 6.019915094) <= 1e-6

# Minimum-size input
a, p = run(
    """1 0.1
5 0
"""
)
assert abs(a - 5.0) <= 1e-9
assert phase_distance(p, 0.0) <= 1e-9

# All waves identical
a, p = run(
    """3 2
2 2.0943951023931953
2 2.0943951023931953
2 2.0943951023931953
"""
)
assert abs(a - 6.0) <= 1e-9
assert phase_distance(p, 2.0943951023931953) <= 1e-9

# Exact cancellation
a, p = run(
    """2 1
1 0
1 3.141592653589793
"""
)
assert abs(a) <= 1e-9

# Phase near the 2*pi boundary
a, p = run(
    """2 1
1 0
1 6.283185207179586
"""
)
assert abs(a - 2.0) <= 1e-7
assert phase_distance(p, 2.0 * math.pi - 5e-8) <= 1e-7

# Maximum-size input
n = 100000
maximum_input = str(n) + " 100\n" + ("100 0\n" * n)
a, p = run(maximum_input)
assert abs(a - 10000000.0) <= 1e-5
assert phase_distance(p, 0.0) <= 1e-9
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0.1 / 5 0` | (5,0) | Minimum input and a phase of exactly zero |
| Three identical waves with phase (2\pi/3) | (6,2\pi/3) | Linear accumulation of equal vectors |
| `1 0 / 1 π` | (0), arbitrary phase | Complete cancellation and floating-point residuals |
| Two phases near (0) and (2\pi) | Amplitude near (2), phase near (2\pi) | Correct circular phase handling |
| (100000) identical waves | (10^7,0) | Maximum (n), linear complexity, and accumulated magnitude |

## Edge Cases

A single wave with phase zero,

```
1 0.1
5 0
```

produces (X=5) and (Y=0). The amplitude is (5), and `atan2(0,5)` gives phase zero. There is no division by (X) or (Y), so the axis case is handled naturally.

A phase of (\pi),

```
1 1
5 3.141592653589793
```

produces (X=-5) and (Y) very close to zero. `atan2` sees the negative (X) coordinate and returns an angle near (\pi), whereas a plain `atan(Y/X)` approach could lose the quadrant information.

For complete cancellation,

```
2 1
1 0
1 3.141592653589793
```

the mathematical vector sum is ((0,0)). Python's floating-point evaluation of (\sin(\pi)) may leave a tiny value instead of exact zero, but `hypot` still produces an amplitude on the order of machine precision. That is far below the required (10^{-6}) absolute error, so the computed result represents the zero function correctly.

For a phase close to (2\pi),

```
2 1
1 0
1 6.283185207179586
```

the second vector is almost identical to the first, but points infinitesimally below the positive (X)-axis. `atan2` consequently returns a tiny negative phase. The explicit addition of (2\pi) converts it to a value just below (2\pi), which satisfies the required output range.

The maximum-size case consists of (100000) identical waves with amplitude (100) and phase zero. Every vector contributes ((100,0)), so the final vector is ((10^7,0)), giving amplitude (10^7) and phase zero. The algorithm still performs exactly one constant amount of work per wave, so the input size changes the running time linearly rather than quadratically.
