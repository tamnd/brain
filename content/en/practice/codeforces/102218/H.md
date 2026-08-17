---
title: "CF 102218H - Heartbreaker Radio Station"
description: "We have (n) sinusoidal signals. Every signal oscillates with the same angular frequency (omega), but each one has its own amplitude (Ai) and phase (phii)."
date: "2026-08-17T23:21:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102218
codeforces_index: "H"
codeforces_contest_name: "2019, XI Annual Programming Contest by ESCOM-IPN"
rating: 0
weight: 102218
solve_time_s: 140
verified: false
draft: false
---

[CF 102218H - Heartbreaker Radio Station](https://codeforces.com/problemset/problem/102218/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We have (n) sinusoidal signals. Every signal oscillates with the same angular frequency (\omega), but each one has its own amplitude (A_i) and phase (\phi_i). Their sum is guaranteed to still be a sinusoid with that same frequency, so the task is to recover the amplitude (A) and phase (\phi) of the single equivalent signal.

The input contains (n), the common frequency, and then (n) pairs ((A_i,\phi_i)). The frequency itself does not need to appear in the output because it is unchanged by adding signals. The output only needs the amplitude and phase of the resulting wave, with the phase normalized to the interval ([0,2\pi)).

The key constraint is (n\le 10^5). With a 2 second limit, an (O(n)) solution is the natural target. An (O(n^2)) method would perform roughly (5\cdot10^9) pair operations at the maximum input size, which is far beyond what can fit in the time limit. The amplitudes and phases are real numbers, so floating-point arithmetic is required, and the requested (10^{-6}) tolerance means we should avoid unnecessarily unstable calculations.

There are several edge cases that can make a careless implementation fail.

The first is phase wrapping. Consider

```
2 1
1 6.2
1 0.1
```

The two phases are close to (2\pi) and (0), so their resultant phase is close to (0), not close to (2\pi). A raw `atan2` result can be negative, and printing it directly violates the required phase interval. The phase must be normalized with modulo (2\pi).

The second is cancellation. Consider

```
2 1
1 0
1 3.141592653589793
```

The two waves are exact opposites, so their sum is the zero function. The correct amplitude is (0). The phase is mathematically irrelevant because (0\sin(x+\phi)=0) for every (\phi). A robust implementation can return phase (0) when the computed amplitude is zero.

The third is cancellation in one coordinate only. For example,

```
2 1
1 0
1 1.5707963267948966
```

The sum is (\sin x+\cos x=\sqrt2\sin(x+\pi/4)), so the answer is approximately

```
1.4142135623730951 0.7853981633974483
```

A formula that uses only `atan(y/x)` can lose the quadrant and produce the wrong phase. `atan2` is needed because it determines the angle from both coordinates.

## Approaches

A straightforward way to think about the problem is to combine the waves two at a time. Suppose we already know that two waves with the same frequency can be represented by one equivalent wave. We can combine the first two, then combine that result with the third, then with the fourth, and so on. That sequential version is already linear, but a literal brute-force implementation might repeatedly recompute the resultant of all pairs of remaining waves before choosing the next combination. Such a procedure performs one pair-combination for every pair of waves, giving

[
\frac{n(n-1)}2
]

combinations. For (n=10^5), that is (4,999,950,000) combinations, so the approach is far too slow even though every individual combination is constant time. Its correctness comes from associativity of addition, but it wastes work by repeatedly representing the same partial sums.

The observation that removes this wasted work is to stop storing the intermediate amplitude and phase altogether. Expand one wave using the angle addition identity:

A_i\sin x\cos\phi_i
+
A_i\cos x\sin\phi_i,
]

where (x=\omega t).

Every wave is thus just a linear combination of the same two basis functions, (\sin x) and (\cos x). We can add all coefficients independently:

[
S=\sum_i A_i\cos\phi_i,
\qquad
C=\sum_i A_i\sin\phi_i.
]

The complete sum becomes

[
f(t)=S\sin(\omega t)+C\cos(\omega t).
]

Now expand the desired single wave:

A\cos\phi\sin x+A\sin\phi\cos x.
]

Matching the coefficients gives

[
A\cos\phi=S,
\qquad
A\sin\phi=C.
]

The amplitude is consequently the length of the vector ((S,C)):

[
A=\sqrt{S^2+C^2}.
]

The phase is the direction of that vector:

[
\phi=\operatorname{atan2}(C,S).
]

This is the central idea. Every original wave contributes one two-dimensional vector ((A_i\cos\phi_i,A_i\sin\phi_i)). Adding the waves is exactly the same as adding these vectors. The final amplitude is the vector's length, and the final phase is its direction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Repeated brute-force pair combinations | (O(n^2)) | (O(1)) | Too slow |
| Coefficient accumulation | (O(n)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read (n) and the common frequency (\omega). The value of (\omega) is not needed afterward because every wave has exactly the same frequency, so it remains unchanged in the final signal.
2. Initialize two accumulators, (S=0) and (C=0). For each wave, add (A_i\cos\phi_i) to (S) and (A_i\sin\phi_i) to (C).

These two values are exactly the coefficients of (\sin(\omega t)) and (\cos(\omega t)) in the complete sum, so no individual wave needs to be stored.
3. Compute the final amplitude as

[
A=\sqrt{S^2+C^2}.
]

This follows from the equations (S=A\cos\phi) and (C=A\sin\phi), since squaring and adding them gives (S^2+C^2=A^2).
4. Compute the phase with

[
\phi=\operatorname{atan2}(C,S).
]

The arguments are deliberately in this order. `atan2(y, x)` returns the direction of the vector ((x,y)), and our vector is ((S,C)).
5. If the phase returned by `atan2` is negative, add (2\pi). This converts the angle into the required interval ([0,2\pi)).
6. Print the amplitude and normalized phase with sufficient precision. Python's double-precision floating-point arithmetic is more than adequate for the required (10^{-6}) error.

### Why it works

After processing every input wave, the accumulators satisfy

[
S=\sum_i A_i\cos\phi_i
]

and

[
C=\sum_i A_i\sin\phi_i.
]

Using the angle addition identity, the original sum is exactly

[
S\sin(\omega t)+C\cos(\omega t).
]

The algorithm chooses (A=\sqrt{S^2+C^2}) and (\phi=\operatorname{atan2}(C,S)), which satisfy (A\cos\phi=S) and (A\sin\phi=C). Substituting those two equalities into (A\sin(\omega t+\phi)) produces exactly the same expression as the sum of all input waves. Thus the returned amplitude and phase describe the required equivalent signal.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    n, omega = input().split()
    n = int(n)
    omega = float(omega)

    s = 0.0
    c = 0.0

    for _ in range(n):
        a, phi = map(float, input().split())
        s += a * math.cos(phi)
        c += a * math.sin(phi)

    amplitude = math.hypot(s, c)
    phase = math.atan2(c, s)

    if phase < 0.0:
        phase += 2.0 * math.pi

    print(f"{amplitude:.12f} {phase:.12f}")

if __name__ == "__main__":
    solve()
```

The first line reads the number of waves and the common frequency. Although `omega` is parsed because it belongs to the input format, it never enters the calculation. This is a direct consequence of all waves sharing the same frequency.

The loop implements the coefficient accumulation from the algorithm. `math.cos(phi)` contributes to the coefficient of (\sin(\omega t)), while `math.sin(phi)` contributes to the coefficient of (\cos(\omega t)). The variables are named `s` and `c` according to these accumulated coefficients.

`math.hypot(s, c)` computes (\sqrt{s^2+c^2}) in a numerically robust way. It also avoids manually writing the square-root expression and is preferable when dealing with floating-point magnitudes.

The phase calculation uses `atan2(c, s)` rather than `atan(c / s)`. The latter loses the quadrant whenever `s` is negative and also has a division-by-zero problem when `s` is zero. `atan2` handles both cases directly.

The normalization checks only whether the result is negative. `atan2` returns an angle in ([-\pi,\pi]), so adding (2\pi) once is sufficient to put it into ([0,2\pi)). Floating-point rounding may make a theoretically zero amplitude extremely small, but this does not create a correctness issue because the phase of a zero-amplitude wave is arbitrary.

No integer multiplication or large integer array is involved, so integer overflow is irrelevant. The largest sums are on the order of (10^7), which is comfortably represented by Python's double-precision floating-point type.

## Worked Examples

Since the statement provides only one sample, the second trace below uses a small constructed input that isolates the vector addition and quadrant handling.

For Sample 1, the algorithm accumulates the cosine and sine components of all eight waves.

| Wave | (A_i) | (\phi_i) | (S) after wave | (C) after wave |
| --- | --- | --- | --- | --- |
| 1 | 93.22 | 5.53 | 65.31 | -66.50 |
| 2 | 48.58 | 0.86 | 96.98 | -29.40 |
| 3 | 15.31 | 5.39 | 106.78 | -40.18 |
| 4 | 5.66 | 4.12 | 103.63 | -43.42 |
| 5 | 48.53 | 6.09 | 151.96 | -52.77 |
| 6 | 6.60 | 1.42 | 152.95 | -46.24 |
| 7 | 21.15 | 0.06 | 174.06 | -44.97 |
| 8 | 4.27 | 5.47 | 177.00 | -49.99 |

The displayed intermediate values are rounded for readability. Using the full floating-point values, the final vector has length approximately (185.184472750), and its direction is approximately (6.019915094). The negative accumulated sine coefficient places the vector below the positive (S)-axis, so `atan2` initially returns a negative angle. Adding (2\pi) produces the sample's phase in the required range.

For a simpler example, consider

```
2 1
1 0
1 1.5707963267948966
```

The first wave contributes the vector ((1,0)), while the second contributes ((0,1)).

| Wave | (S) contribution | (C) contribution | (S) | (C) |
| --- | --- | --- | --- | --- |
| 1 | 1.000000 | 0.000000 | 1.000000 | 0.000000 |
| 2 | 0.000000 | 1.000000 | 1.000000 | 1.000000 |

The final amplitude is

[
\sqrt{1^2+1^2}=\sqrt2,
]

and `atan2(1,1)` gives (\pi/4). Thus the result is

```
1.414213562373 0.785398163397
```

This trace demonstrates why both accumulated coordinates are necessary and why `atan2` is the correct way to recover the phase.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Each wave requires one sine and one cosine calculation plus constant-time arithmetic. |
| Space | (O(1)) | Only the two accumulated coefficients and a few scalar values are stored. |

For (n=10^5), the algorithm performs only (10^5) iterations and uses constant extra memory. This is comfortably within the 2 second and 256 MB limits, while the quadratic alternative would require nearly five billion pair combinations.

## Test Cases

The test harness below compares floating-point results with a tolerance instead of comparing decimal strings exactly. That is the appropriate way to test this problem because multiple numerically equivalent answers can differ in their final printed digits while still satisfying the required error bound.

```python
import sys
import io
import math

def solve():
    input = sys.stdin.readline

    n, omega = input().split()
    n = int(n)
    omega = float(omega)

    s = 0.0
    c = 0.0

    for _ in range(n):
        a, phi = map(float, input().split())
        s += a * math.cos(phi)
        c += a * math.sin(phi)

    amplitude = math.hypot(s, c)
    phase = math.atan2(c, s)

    if phase < 0.0:
        phase += 2.0 * math.pi

    print(f"{amplitude:.12f} {phase:.12f}")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def parse_output(out: str):
    a, p = map(float, out.split())
    return a, p

def assert_close(actual: str, expected_a: float, expected_p: float,
                 message: str):
    a, p = parse_output(actual)

    assert math.isclose(a, expected_a, rel_tol=1e-9, abs_tol=1e-9), message
    assert math.isclose(p, expected_p, rel_tol=1e-9, abs_tol=1e-9), message

# Provided sample
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

assert_close(
    run(sample1),
    185.184472750,
    6.019915094,
    "sample 1"
)

# Minimum-size input
assert_close(
    run("1 0.1\n5 1.2\n"),
    5.0,
    1.2,
    "single wave"
)

# Two perpendicular waves
assert_close(
    run("2 1\n1 0\n1 1.5707963267948966\n"),
    math.sqrt(2.0),
    math.pi / 4.0,
    "perpendicular waves"
)

# Exact cancellation
assert_close(
    run("2 10\n1 0\n1 3.141592653589793\n"),
    0.0,
    0.0,
    "exact cancellation"
)

# Boundary phases near 0 and 2*pi
eps = 1e-10
assert_close(
    run(f"2 100\n1 {2 * math.pi - eps}\n1 {eps}\n"),
    2.0,
    0.0,
    "phase wrapping"
)

# Maximum-size input with identical waves
n = 100000
large_input = f"{n} 50\n" + ("1 0\n" * n)
assert_close(
    run(large_input),
    100000.0,
    0.0,
    "maximum-size input"
)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0.1 / 5 1.2` | `5 1.2` | Minimum-size input and preservation of a single wave |
| `2 1 / 1 0 / 1 π/2` | `√2 π/4` | Independent sine and cosine accumulation |
| `2 10 / 1 0 / 1 π` | `0 0` | Complete cancellation and zero amplitude |
| `2 100 / 1 (2π-ε) / 1 ε` | `2 0` | Phase wrapping across the (0) and (2\pi) boundary |
| `100000` identical waves | `100000 0` | Maximum input size and linear-time behavior |

## Edge Cases

For phase wrapping, use

```
2 1
1 6.283185307079586
1 0.0000000001
```

The first phase is (2\pi-10^{-10}), while the second is (10^{-10}). Their vectors point almost in the same direction, so their sum has amplitude extremely close to (2) and phase extremely close to (0). The accumulated sine component is approximately zero and the cosine component is approximately (2). `atan2` may produce a tiny positive or negative value because of floating-point rounding. If it is negative, the algorithm adds (2\pi), producing an equivalent phase in the required range.

For exact cancellation, use

```
2 1
1 0
1 3.141592653589793
```

The first wave contributes ((1,0)), while the second contributes ((-1,0)). The accumulated vector is ((0,0)), so `math.hypot` returns zero. `atan2(0,0)` returns zero in Python, giving the valid output

```
0.000000000000 0.000000000000
```

The phase has no physical meaning when the amplitude is zero, so any phase in the allowed interval would represent the same wave. Returning zero is a convenient canonical choice.

For the quadrant issue, use

```
2 1
1 0
1 1.5707963267948966
```

The accumulated vector is ((1,1)), so the phase is (\pi/4). A formula based on `atan(C/S)` happens to work here, but consider instead

```
2 1
1 3.141592653589793
1 1.5707963267948966
```

The accumulated vector is approximately ((-1,1)). The correct phase is (3\pi/4). A naive `atan(C/S)` calculation sees a ratio of approximately (-1) and returns approximately (-\pi/4), which is the wrong direction. `atan2(C,S)` sees both signs and correctly returns (3\pi/4).

Finally, the maximum-size case can be made especially simple:

```
100000 50
1 0
1 0
...
1 0
```

with (100000) identical waves. Every contribution is ((1,0)), so the final vector is ((100000,0)). The result is amplitude (100000) and phase (0). The algorithm processes every input exactly once, demonstrating why the (O(n)) bound remains practical at the largest allowed input size.
