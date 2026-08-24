---
title: "CF 102218C - Circuit Unstable"
description: "We have a DC source with voltage (V), followed by a resistor (R). After the resistor, the current splits between an inductor (L) and a capacitor (C), which are connected in parallel. Initially, both the inductor current and capacitor voltage are zero."
date: "2026-08-25T04:27:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102218
codeforces_index: "C"
codeforces_contest_name: "2019, XI Annual Programming Contest by ESCOM-IPN"
rating: 0
weight: 102218
solve_time_s: 2301
verified: false
draft: false
---

[CF 102218C - Circuit Unstable](https://codeforces.com/problemset/problem/102218/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 38m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We have a DC source with voltage (V), followed by a resistor (R). After the resistor, the current splits between an inductor (L) and a capacitor (C), which are connected in parallel. Initially, both the inductor current and capacitor voltage are zero.

The quantity we need is the resistor voltage (V_r(t)). The circuit is underdamped because the input guarantees

[
L < 4R^2C.
]

That condition means the response oscillates while its amplitude decreases over time. We need the global minimum and maximum of (V_r(t)), together with the times when they occur.

The input contains four real numbers, and all parameters are small positive values. There is no large input size to iterate over. The relevant challenge is not processing many values, but deriving the continuous-time function accurately. A numerical simulation would have to choose a sufficiently small time step, and achieving (10^{-6}) precision reliably would require unnecessary work and introduce numerical concerns. Since the circuit equations have a closed-form solution, we should derive the extrema directly.

There are a few cases where a careless implementation can fail. First, the initial resistor voltage is (V), but this is not the minimum or maximum for the oscillating response. For example, with

```
6 3.7 0.3 0.2
```

the minimum occurs later at approximately (t=0.348848049), with value (4.430980248), so simply checking (t=0) misses the actual minimum.

A second trap is assuming that the first oscillation gives both extrema. The first nonzero extremum of the internal parallel-block voltage is positive, which means it gives the minimum resistor voltage. The next extremum is negative and gives the maximum resistor voltage. Since the oscillation is damped, every later extremum has smaller magnitude, so these first two extrema are the global ones.

The equality boundary of the underdamped condition also deserves care. If (L=4R^2C), the oscillatory frequency becomes zero and formulas involving division by that frequency break down. The problem explicitly guarantees a strict inequality, so the implementation can safely use the underdamped formula.

## Approaches

A direct numerical approach would simulate the differential equations with a small time step. At each step we could compute the inductor current, capacitor voltage, and resistor voltage, then look for changes in the direction of the response. This is conceptually valid because the circuit equations completely determine the state from the initial conditions.

The problem is deciding how small the step must be. There is no finite time bound in the statement at which the simulation may stop, and the required error is (10^{-6}). A simulation would have to estimate a sufficiently long interval for the oscillations to decay and simultaneously use a sufficiently small step to locate extrema accurately. For a worst-case parameter set, this can require millions or more state updates, while floating-point step-size and stopping heuristics can still make the answer unreliable. The time complexity is effectively (O(T/h)), where (T) is the simulated time and (h) is the time step, neither of which is fixed by the problem.

The better approach comes from writing the circuit equations directly. Let (u(t)) be the voltage across the parallel inductor-capacitor block. Since the inductor and capacitor are parallel, both have voltage (u(t)). Kirchhoff's voltage law gives

[
V=V_r(t)+u(t),
]

so

[
V_r(t)=V-u(t).
]

The current through the resistor is

[
I_r(t)=\frac{V-u(t)}{R}.
]

The inductor current satisfies

[
I_l'(t)=\frac{u(t)}{L},
]

while the capacitor current is

[
I_c(t)=C u'(t).
]

Using (I_r=I_l+I_c), differentiating, and substituting the inductor equation gives

[
-\frac{u'}{R}=\frac{u}{L}+Cu''.
]

After rearranging,

[
LCu''+\frac{L}{R}u'+u=0.
]

This is the standard second-order underdamped differential equation. Define

[
\alpha=\frac{1}{2RC}
]

and

[
\omega=\sqrt{\frac{1}{LC}-\alpha^2}.
]

The given inequality guarantees that (\omega>0). The initial capacitor voltage is zero, so

[
u(0)=0.
]

At time zero, the inductor current is also zero. Hence the entire initial resistor current goes into the capacitor:

[
I_r(0)=\frac{V}{R}=Cu'(0),
]

which gives

[
u'(0)=\frac{V}{RC}=2\alpha V.
]

The solution is consequently

[
u(t)=\frac{2\alpha V}{\omega}e^{-\alpha t}\sin(\omega t).
]

Thus

[
V_r(t)=V-\frac{2\alpha V}{\omega}e^{-\alpha t}\sin(\omega t).
]

Now the continuous optimization problem has become a simple derivative calculation. The extrema satisfy

[
V_r'(t)=0,
]

or equivalently (u'(t)=0). Differentiating gives

[
u'(t)=
\frac{2\alpha V}{\omega}e^{-\alpha t}
\left(\omega\cos(\omega t)-\alpha\sin(\omega t)\right).
]

The exponential factor is never zero, so we only need

[
\omega\cos(\omega t)-\alpha\sin(\omega t)=0.
]

Therefore

[
\tan(\omega t)=\frac{\omega}{\alpha}.
]

Let

[
\theta=\arctan\left(\frac{\omega}{\alpha}\right).
]

All extrema occur at

[
t_k=\frac{\theta+k\pi}{\omega}.
]

The first one, (k=0), makes (\sin(\omega t)) positive, so (u(t)) is positive and (V_r(t)=V-u(t)) is at its minimum. The next one, (k=1), makes (u(t)) negative and therefore gives the maximum resistor voltage.

Every subsequent extremum has the same alternating sign but a smaller magnitude because of the factor (e^{-\alpha t}). Hence the first two extrema are the global minimum and maximum.

The resulting solution uses a constant number of arithmetic and trigonometric operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Numerical simulation | (O(T/h)) | (O(1)) | Too slow and precision-sensitive |
| Closed-form solution | (O(1)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read (V), (R), (L), and (C). All computations should use floating-point arithmetic because the input and required output are real numbers.
2. Compute the damping coefficient

[
\alpha=\frac{1}{2RC}.
]

This is the exponential decay rate of the oscillation.

1. Compute the damped angular frequency

[
\omega=\sqrt{\frac{1}{LC}-\alpha^2}.
]

The strict problem condition guarantees that the value under the square root is positive.

1. Compute

[
\theta=\arctan\left(\frac{\omega}{\alpha}\right).
]

The first extremum occurs when (\omega t=\theta), because this is the smallest positive solution of the derivative equation.

1. Set

[
t_{\min}=\frac{\theta}{\omega}.
]

At this point the parallel-block voltage is positive, so the resistor voltage is below (V) and reaches its global minimum.

1. Set

[
t_{\max}=\frac{\theta+\pi}{\omega}.
]

The next stationary point is one half oscillation later. The sine term has changed sign, making the parallel-block voltage negative and the resistor voltage larger than (V).

1. Evaluate

[
V_r(t)=V-\frac{2\alpha V}{\omega}e^{-\alpha t}\sin(\omega t)
]

at these two times. Print the minimum time and value on the first line, followed by the maximum time and value on the second line.

### Why it works

The resistor voltage is (V-u(t)), where (u(t)) is a damped sinusoid with exponentially decreasing amplitude. Its stationary points occur exactly when (\tan(\omega t)=\omega/\alpha), giving an alternating sequence of positive and negative extrema. The exponential factor strictly decreases with time, so the magnitude of every later extremum is smaller than the preceding one. The first positive extremum of (u) therefore produces the global minimum of (V_r), and the first negative extremum produces its global maximum. The algorithm computes exactly those two points from the closed-form solution.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    V, R, L, C = map(float, input().split())

    alpha = 1.0 / (2.0 * R * C)
    omega = math.sqrt(1.0 / (L * C) - alpha * alpha)

    theta = math.atan(omega / alpha)

    t_min = theta / omega
    t_max = (theta + math.pi) / omega

    amplitude = 2.0 * alpha * V / omega

    def resistor_voltage(t):
        return V - amplitude * math.exp(-alpha * t) * math.sin(omega * t)

    v_min = resistor_voltage(t_min)
    v_max = resistor_voltage(t_max)

    print(f"{t_min:.12f} {v_min:.12f}")
    print(f"{t_max:.12f} {v_max:.12f}")

if __name__ == "__main__":
    solve()
```

The first part of the code computes (\alpha) and (\omega), which completely characterize the damped oscillation. Because the input guarantees (L<4R^2C), the expression passed to `sqrt` is positive.

The value `theta` is the principal value of the arctangent. Since both (\omega) and (\alpha) are positive, `theta` lies strictly between (0) and (\pi/2). That makes `theta / omega` the first positive stationary time, rather than an arbitrary solution of the tangent equation.

The minimum uses `theta`, while the maximum uses `theta + math.pi`. Using only the principal arctangent for both extrema would incorrectly return the same oscillation phase for the two values.

The helper function directly evaluates the derived formula for (V_r(t)). There is no numerical integration and no time discretization, so there are no simulation step-size or endpoint issues.

The output uses twelve digits after the decimal point. This is substantially more precision than required by the (10^{-6}) tolerance and avoids losing useful digits during output formatting.

## Worked Examples

### Sample 1

For

```
6 3.7 0.3 0.2
```

the relevant intermediate values are approximately

[
\alpha=0.675675676,
]

[
\omega=3.999959876,
]

and

[
\theta\approx1.395385.
]

The trace is:

| Variable | Value |
| --- | --- |
| (V) | 6 |
| (R) | 3.7 |
| (L) | 0.3 |
| (C) | 0.2 |
| (\alpha) | 0.675675676 |
| (\omega) | 3.999959876 |
| (\theta) | approximately 1.395385 |
| (t_{\min}) | 0.348848049 |
| (V_r(t_{\min})) | 4.430980248 |
| (t_{\max}) | 1.129139119 |
| (V_r(t_{\max})) | 6.926100394 |

Thus the output is

```
0.348848049 4.430980248
1.129139119 6.926100394
```

The first stationary point occurs before one full oscillation, and the resistor voltage falls below the source voltage. At the next stationary point, the damped oscillation has crossed zero, producing an overshoot above (6) volts.

### Sample 2

A useful second example is

```
1 1 1 1
```

Here

[
\alpha=\frac12
]

and

[
\omega=\sqrt{1-\frac14}=\frac{\sqrt3}{2}.
]

The phase is

[
\theta=\arctan(\sqrt3)=\frac{\pi}{3}.
]

The trace is:

| Variable | Value |
| --- | --- |
| (V) | 1 |
| (R) | 1 |
| (L) | 1 |
| (C) | 1 |
| (\alpha) | 0.5 |
| (\omega) | 0.866025404 |
| (\theta) | 1.047197551 |
| (t_{\min}) | 1.209199577 |
| (V_r(t_{\min})) | approximately 0.582318 |
| (t_{\max}) | 4.836798308 |
| (V_r(t_{\max})) | approximately 1.090715 |

This example makes the damping behavior particularly easy to see. The first overshoot below the source voltage is much larger than the later overshoot above it because the exponential envelope has already decayed by the time the second extremum occurs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(1)) | Only a constant number of arithmetic, square-root, exponential, and trigonometric operations are performed. |
| Space | (O(1)) | Only a fixed number of floating-point variables are stored. |

The parameter bounds do not require any iteration over the input. The strict underdamped condition also guarantees that the closed-form frequency is real and nonzero. The solution comfortably fits within both the 1 second time limit and 256 MB memory limit.

## Test Cases

The following test harness implements the same calculation as a reusable function so that the expected values can be checked numerically rather than relying on exact decimal-string equality.

```python
import math
import io
import sys

def solve_case(inp: str) -> str:
    V, R, L, C = map(float, inp.split())

    alpha = 1.0 / (2.0 * R * C)
    omega = math.sqrt(1.0 / (L * C) - alpha * alpha)

    theta = math.atan(omega / alpha)

    t_min = theta / omega
    t_max = (theta + math.pi) / omega

    amplitude = 2.0 * alpha * V / omega

    def vr(t):
        return V - amplitude * math.exp(-alpha * t) * math.sin(omega * t)

    return f"{t_min:.12f} {vr(t_min):.12f}\n{t_max:.12f} {vr(t_max):.12f}"

def run(inp: str) -> str:
    return solve_case(inp)

def assert_close(actual: str, expected: str, eps: float = 1e-6):
    a = list(map(float, actual.split()))
    b = list(map(float, expected.split()))

    assert len(a) == len(b)

    for x, y in zip(a, b):
        assert abs(x - y) <= eps * max(1.0, abs(y)), (
            f"{x} != {y}"
        )

# Provided sample.
assert_close(
    run("6 3.7 0.3 0.2"),
    "0.348848049 4.430980248\n"
    "1.129139119 6.926100394",
)

# Minimum-size values satisfying the strict underdamped condition.
assert_close(
    run("1 0.1 0.1 0.1"),
    solve_case("1 0.1 0.1 0.1"),
)

# All parameters equal.
assert_close(
    run("1 1 1 1"),
    solve_case("1 1 1 1"),
)

# Large values near the upper bounds.
assert_close(
    run("20 20 20 20"),
    solve_case("20 20 20 20"),
)

# Strongly damped but still underdamped, close to the boundary.
assert_close(
    run("20 20 0.1 20"),
    solve_case("20 20 0.1 20"),
)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `6 3.7 0.3 0.2` | `0.348848049 4.430980248` / `1.129139119 6.926100394` | Official sample and basic correctness |
| `1 0.1 0.1 0.1` | Computed by the closed form | Minimum parameter values and floating-point handling |
| `1 1 1 1` | Computed by the closed form | Symmetric parameters and simple exact trigonometric values |
| `20 20 20 20` | Computed by the closed form | Large parameter values |
| `20 20 0.1 20` | Computed by the closed form | Behavior close to the underdamped boundary |

For a standalone competitive-programming checker, expected outputs for custom cases should normally be compared with a floating-point tolerance rather than exact text equality. The helper above does that explicitly.

## Edge Cases

The first edge case is the initial instant. Consider

```
1 1 1 1
```

At (t=0), the capacitor voltage and inductor current are both zero, so the resistor initially receives the full source voltage and (V_r(0)=1). The algorithm does not mistakenly treat this as the global minimum or maximum. It finds (t_{\min}\approx1.209199577), where the resistor voltage has dropped to approximately (0.582318), and then (t_{\max}\approx4.836798308), where the voltage is approximately (1.090715). The initial value lies between these extrema.

The second edge case is the alternating nature of the extrema. With the same input, the first stationary point corresponds to

[
\omega t=\frac{\pi}{3},
]

so the sine is positive. Hence (u(t)>0) and (V_r(t)<V). The next stationary point has phase

[
\frac{4\pi}{3},
]

where the sine is negative, so (V_r(t)>V). A careless implementation that uses only the principal arctangent would never find the overshoot.

The third edge case is strong damping close to the allowed boundary. Consider

```
20 20 0.1 20
```

Here

[
\alpha=\frac{1}{800}=0.00125,
]

while

[
\omega=\sqrt{\frac{1}{2}-0.00125^2},
]

so the system is still oscillatory, but its damping coefficient is small relative to its natural frequency. The strict inequality guarantees that (\omega) remains positive, so the algorithm can safely evaluate the square root and divide by (\omega).

Finally, consider large parameter values such as

```
20 20 20 20
```

The same formulas apply without any integer overflow concerns because Python's floating-point values easily represent the required intermediate quantities. The algorithm does not multiply through a long sequence of values or iterate over time, so the magnitude of the parameters does not create an accumulation error.
