---
title: "CF 102218H - Heartbreaker Radio Station"
description: "We have several sinusoidal waves, all oscillating with the same angular frequency. The only things that differ between waves are their amplitudes and phases. We need to replace their sum with one sinusoid having that same frequency, and report its amplitude and phase."
date: "2026-08-20T03:26:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102218
codeforces_index: "H"
codeforces_contest_name: "2019, XI Annual Programming Contest by ESCOM-IPN"
rating: 0
weight: 102218
solve_time_s: 111
verified: false
draft: false
---

[CF 102218H - Heartbreaker Radio Station](https://codeforces.com/problemset/problem/102218/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 51s  
**Verified:** no  

## Solution
## Problem Understanding

We have several sinusoidal waves, all oscillating with the same angular frequency. The only things that differ between waves are their amplitudes and phases. We need to replace their sum with one sinusoid having that same frequency, and report its amplitude and phase.

For wave (i),

[
f_i(t)=A_i\sin(\omega t+\phi_i).
]

The complete signal is

[
f(t)=\sum_{i=1}^{n} A_i\sin(\omega t+\phi_i),
]

and we want values (A\ge 0) and (0\le\phi<2\pi) such that

[
f(t)=A\sin(\omega t+\phi)
]

for every (t).

The frequency (\omega) is actually irrelevant to the computation once we recognize that every wave has the same frequency. The challenge is to combine the amplitudes and phases efficiently.

With (n\le 10^5), an (O(n)) algorithm is comfortably within the intended range for a 2-second limit. An (O(n^2)) method would require around (10^{10}) elementary operations at the largest input size, which is far beyond what can fit in the time limit. The input amplitudes and phases are real numbers, so the implementation also has to use floating-point arithmetic and respect the required (10^{-6}) precision.

There are three edge cases that commonly cause otherwise reasonable implementations to fail. The first is cancellation. Consider

```
2 1
1 0
1 3.141592653589793
```

The two waves are opposites, so their sum is exactly zero. The correct result is

```
0 0
```

because when (A=0), the phase has no effect and (0) is a valid choice. A careless implementation may call `atan2(0, 0)` and obtain an implementation-dependent interpretation, or may produce a tiny numerical amplitude and an arbitrary phase.

The second issue is the quadrant of the phase. For

```
1 1
1 4.71238898038469
```

the answer is the same amplitude and phase, approximately

```
1 4.71238898038469
```

Since `atan2` returns values in ([-\pi,\pi]), it may return (-\pi/2) instead of (3\pi/2). The mathematical phase is equivalent, but the required output range is specifically ([0,2\pi)), so negative angles must be normalized.

The third issue is cancellation in the two accumulated components. For example,

```
2 1
100 0
100 3.141592653589793
```

should again produce zero. The intermediate sine and cosine components can be very small because large positive and negative contributions cancel. The solution should not make decisions based on exact equality of floating-point values except where the final amplitude is effectively zero.

## Approaches

A direct but unnecessarily expensive way to think about the problem is to evaluate the complete signal at many different times. For every chosen time (t), we would compute all (n) waves and add them. If we use (n) sample times, this takes (n) evaluations of (n) waves, giving (O(n^2)) work. At (n=10^5), that is about (10^{10}) wave evaluations, which is much too slow.

The brute-force approach is correct because every individual wave is evaluated exactly according to its definition, so the computed samples really are samples of the desired sum. The problem is that the common frequency gives us much more structure than arbitrary samples require.

The key observation is the angle-addition identity

[
\sin(x+\phi)=\sin x\cos\phi+\cos x\sin\phi.
]

Applying it to every wave gives

A_i\cos\phi_i\sin(\omega t)
+
A_i\sin\phi_i\cos(\omega t).
]

All waves are now expressed using the same two basis functions, (\sin(\omega t)) and (\cos(\omega t)). We only need to add their coefficients.

Define

[
C=\sum_{i=1}^{n} A_i\cos\phi_i
]

and

[
S=\sum_{i=1}^{n} A_i\sin\phi_i.
]

Then the complete signal becomes

[
f(t)=C\sin(\omega t)+S\cos(\omega t).
]

Now expand the desired single wave:

A\cos\phi\sin(\omega t)
+
A\sin\phi\cos(\omega t).
]

Matching the two coefficients gives

[
A\cos\phi=C,
\qquad
A\sin\phi=S.
]

These two equations describe a vector with coordinates ((C,S)). Its length is the resulting amplitude,

[
A=\sqrt{C^2+S^2},
]

and its direction is the resulting phase,

[
\phi=\operatorname{atan2}(S,C).
]

So the entire problem reduces to one pass over the input, accumulating two real numbers.

The same insight can also be viewed as vector addition. Each sinusoid (A_i\sin(\omega t+\phi_i)) corresponds to a vector of length (A_i) and angle (\phi_i). Adding the waves means adding these vectors. The resulting vector's length is (A), while its direction is (\phi).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(1)) | Too slow |
| Optimal | (O(n)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Initialize two accumulators, (C=0) and (S=0). They will store the coefficients of (\sin(\omega t)) and (\cos(\omega t)), respectively.
2. For every input wave, compute (A_i\cos\phi_i) and add it to (C). Compute (A_i\sin\phi_i) and add it to (S).

This is the central transformation. We never need to evaluate the waves at any actual time (t), because their common frequency means every wave uses the same two basis functions.
3. After all waves have been processed, calculate

[
A=\sqrt{C^2+S^2}.
]

The values (C) and (S) are exactly (A\cos\phi) and (A\sin\phi), so their Euclidean length must be the amplitude.

1. If (A) is effectively zero, output (0) and phase (0).

A zero-amplitude sinusoid is identically zero regardless of its phase, so phase (0) is a valid canonical choice. This also avoids asking for the direction of a zero vector.
2. Otherwise calculate

[
\phi=\operatorname{atan2}(S,C).
]

`atan2` is required instead of ordinary `atan(S/C)` because it knows the signs of both components and consequently determines the correct quadrant.

1. If the phase is negative, add (2\pi) to it. Then print (A) and (\phi) with enough decimal digits to satisfy the (10^{-6}) error requirement.

### Why it works

After processing every wave, the accumulators satisfy

[
C=\sum_i A_i\cos\phi_i
]

and

[
S=\sum_i A_i\sin\phi_i.
]

By the angle-addition identity, the original sum is consequently

[
f(t)=C\sin(\omega t)+S\cos(\omega t).
]

The computed amplitude and phase satisfy

[
A\cos\phi=C
]

and

[
A\sin\phi=S.
]

Substituting those two equalities into

[
A\sin(\omega t+\phi)
]

produces exactly (C\sin(\omega t)+S\cos(\omega t)), which is the original sum. Thus the resulting sinusoid is equivalent for every possible value of (t), not merely at selected sample points.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

n, omega = input().split()
n = int(n)
omega = float(omega)

c = 0.0
s = 0.0

for _ in range(n):
    a, phi = map(float, input().split())
    c += a * math.cos(phi)
    s += a * math.sin(phi)

amplitude = math.hypot(c, s)

if amplitude < 1e-12:
    phase = 0.0
else:
    phase = math.atan2(s, c)
    if phase < 0.0:
        phase += 2.0 * math.pi

print(f"{amplitude:.12f} {phase:.12f}")
```

The first line reads `n` and `omega`. The value of `omega` is parsed because it is part of the input format, but it does not appear later in the computation. Once every wave has the same frequency, only its amplitude and phase determine the coefficient vector that must be added.

The variables `c` and `s` correspond directly to the two coefficients derived in the algorithm. For each wave, the code computes its horizontal component (A_i\cos\phi_i) and vertical component (A_i\sin\phi_i), then adds them to the respective accumulators.

`math.hypot(c, s)` computes (\sqrt{c^2+s^2}). It is preferable to writing the expression manually because `hypot` is designed to calculate vector lengths robustly.

The zero check uses a very small tolerance rather than checking `amplitude == 0`. Floating-point cancellation can leave a mathematically zero result represented by a tiny residual value. Any phase is valid when the amplitude is zero, so choosing phase (0) gives a stable and valid output.

For a nonzero result, `atan2(s, c)` returns the angle of the vector ((c,s)). Its result lies in ([-\pi,\pi]), while the problem requires ([0,2\pi)). Adding (2\pi) to a negative result converts it into the required range. A result of exactly (2\pi) does not occur from `atan2`, and adding (2\pi) is only performed for negative values, so the upper boundary remains valid.

The frequency never needs to be multiplied into any expression. Doing so would actually be a conceptual mistake because the required output phase is the constant (\phi) in (A\sin(\omega t+\phi)), not the time-dependent angle (\omega t+\phi).

## Worked Examples

There is no second official sample in the supplied statement, so the second trace below uses a small constructed input.

For Sample 1, the important state is the pair ((C,S)). The following table shows the accumulated values after each wave, rounded for readability.

| Wave | (A_i) | (\phi_i) | (C) after wave | (S) after wave |
| --- | --- | --- | --- | --- |
| 1 | 93.22 | 5.53 | 65.75 | -66.07 |
| 2 | 48.58 | 0.86 | 97.49 | -28.99 |
| 3 | 15.31 | 5.39 | 107.13 | -40.89 |
| 4 | 5.66 | 4.12 | 104.07 | -44.76 |
| 5 | 48.53 | 6.09 | 152.43 | -54.13 |
| 6 | 6.60 | 1.42 | 153.42 | -47.61 |
| 7 | 21.15 | 0.06 | 174.50 | -46.34 |
| 8 | 4.27 | 5.47 | 177.49 | -49.20 |

The rounded table hides some precision, but the full-precision accumulators give approximately

[
A=185.184472750
]

and

[
\phi=6.019915094.
]

The resulting vector lies in the fourth quadrant because (C>0) and (S<0). `atan2` correctly produces a negative equivalent angle first, then the normalization step adds (2\pi), giving the required phase near (6.02).

For the constructed cancellation example

```
2 1
3 0
3 3.141592653589793
```

the two waves have equal amplitudes and phases separated by (\pi).

| Wave | (A_i) | (\phi_i) | (C) after wave | (S) after wave |
| --- | --- | --- | --- | --- |
| 1 | 3 | 0 | 3 | 0 |
| 2 | 3 | (\pi) | 0 | approximately 0 |

The final vector is the zero vector, so its amplitude is zero. The algorithm chooses phase (0), producing

```
0.000000000000 0.000000000000
```

Any other phase would represent the same zero signal. This trace demonstrates why the algorithm must explicitly handle the zero-vector case instead of trying to interpret its direction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Each wave requires one sine, one cosine, and constant additional arithmetic. |
| Space | (O(1)) | Only the two accumulated components and a few scalar variables are stored. |

For (n=10^5), the algorithm performs one pass over the input and stores no array of waves. Its (O(n)) running time is appropriate for the 2-second limit, while its constant memory usage is far below the 256 MB limit. Python's trigonometric function calls dominate the constant factor, but there are only (10^5) of each, which is practical.

## Test Cases

Because floating-point output cannot safely be compared as an exact string, the test harness below parses the two output values and checks them against the expected values with a tolerance.

```python
import sys
import io
import math

def solve():
    input = sys.stdin.readline

    n, omega = input().split()
    n = int(n)
    omega = float(omega)

    c = 0.0
    s = 0.0

    for _ in range(n):
        a, phi = map(float, input().split())
        c += a * math.cos(phi)
        s += a * math.sin(phi)

    amplitude = math.hypot(c, s)

    if amplitude < 1e-12:
        phase = 0.0
    else:
        phase = math.atan2(s, c)
        if phase < 0.0:
            phase += 2.0 * math.pi

    print(f"{amplitude:.12f} {phase:.12f}")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def check(inp: str, expected_a: float, expected_phi: float, message: str):
    out = run(inp).split()
    actual_a = float(out[0])
    actual_phi = float(out[1])

    assert math.isclose(actual_a, expected_a, rel_tol=1e-6, abs_tol=1e-6), message
    assert math.isclose(actual_phi, expected_phi, rel_tol=1e-6, abs_tol=1e-6), message

# Provided sample.
sample1 = """\
8 66.82
93.22 5.53
48.58 0.86
15.31 5.39
5.66 4.12
48.53 6.09
6.60 1.42
21.15 0.06
4.27 5.47
"""
check(
    sample1,
    185.184472750,
    6.019915094,
    "sample 1"
)

# Minimum-size input, a single wave must remain unchanged.
check(
    """\
1 1
7 1.2
""",
    7.0,
    1.2,
    "single wave"
)

# Exact cancellation.
check(
    """\
2 10
5 0
5 3.141592653589793
""",
    0.0,
    0.0,
    "complete cancellation"
)

# Phase in the fourth quadrant. This catches atan2 without normalization.
check(
    """\
1 2
4 4.71238898038469
""",
    4.0,
    1.5 * math.pi,
    "negative atan2 result must be normalized"
)

# Equal phases. The amplitudes simply add.
check(
    """\
4 50
1.5 0.75
2.5 0.75
3.0 0.75
4.0 0.75
""",
    11.0,
    0.75,
    "equal amplitudes direction"
)

# Large input, exercising linear processing and accumulation.
large_n = 100000
large_input = f"{large_n} 1\n" + ("1 0\n" * large_n)
large_out = run(large_input).split()
assert math.isclose(float(large_out[0]), 100000.0, rel_tol=1e-6, abs_tol=1e-6)
assert math.isclose(float(large_out[1]), 0.0, rel_tol=1e-6, abs_tol=1e-6)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | (185.184472750,\ 6.019915094) | Full official example and general accumulation |
| `1 1 / 7 1.2` | (7,\ 1.2) | Minimum input and single-wave behavior |
| `2 10 / 5 0 / 5 π` | (0,\ 0) | Complete cancellation and zero amplitude |
| `1 2 / 4 3π/2` | (4,\ 3π/2) | `atan2` quadrant handling and phase normalization |
| Four waves with phase (0.75) | (11,\ 0.75) | Equal phase, where amplitudes add directly |
| (10^5) waves with amplitude (1), phase (0) | (100000,\ 0) | Maximum input size and linear complexity |

## Edge Cases

Complete cancellation is handled by the zero-amplitude branch. For

```
2 1
1 0
1 3.141592653589793
```

the first wave contributes ((C,S)=(1,0)). The second contributes ((-1,0)), so the final vector is ((0,0)). Its amplitude is zero and the algorithm outputs phase zero. The frequency does not change this conclusion because both waves have the same frequency.

A phase in the fourth quadrant exposes a common mistake with `atan2`. For

```
1 1
1 4.71238898038469
```

the accumulated components are approximately

[
C=0,\qquad S=-1.
]

`atan2(-1,0)` returns (-\pi/2). Since the required phase must be nonnegative, the algorithm adds (2\pi), obtaining (3\pi/2), which is exactly the original phase.

Floating-point cancellation is also handled safely. Consider

```
2 1
100 0
100 3.141592653589793
```

Mathematically the vector contributions are ((100,0)) and ((-100,0)). In floating-point arithmetic the second sine is not necessarily represented as exactly zero, so the final vector may contain a tiny residual. The `1e-12` threshold treats such a residual as the zero vector. Since the required numerical tolerance is (10^{-6}), this does not discard any meaningful nonzero result.

Finally, the phase boundary itself does not require special handling beyond the normalization step. A phase approaching (2\pi) has a vector pointing just below the positive (C)-axis, while a phase just above zero points just above it. `atan2` distinguishes these signs correctly. The normalization only changes negative representations into their equivalent values in ([0,2\pi)), without changing the represented sinusoid.
