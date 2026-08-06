---
title: "CF 102511K - Traffic Blights"
description: "We need analyze a line of traffic lights. A car starts at position zero at a random real-valued time. Since it moves one meter per second, the time it reaches a light is the starting time plus that light's position."
date: "2026-08-06T19:31:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102511
codeforces_index: "K"
codeforces_contest_name: "2019 ICPC World Finals"
rating: 0
weight: 102511
solve_time_s: 73
verified: true
draft: false
---

[CF 102511K - Traffic Blights](https://codeforces.com/problemset/problem/102511/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We need analyze a line of traffic lights. A car starts at position zero at a random real-valued time. Since it moves one meter per second, the time it reaches a light is the starting time plus that light's position. A light is either red or green according to its own repeating cycle, and the car succeeds only if every light is green exactly when it arrives.

The task is to compute two kinds of probabilities. For every light, we need the probability that it is the first light where the car is stopped. We also need the probability that the car passes every light.

The difficulty is that the starting time interval is astronomically large. The value 2019! is chosen because it contains every possible light period as a divisor, so the distribution of starting times is exactly the same as choosing a random time over one complete combined cycle. The combined cycle itself is far too large to enumerate.

The number of lights is only 500, and every period is at most 100. A simulation over time is impossible because even a single period combination can be enormous. The useful bound is the period size, not the length of the time interval. We need a representation that keeps only the possible periodic patterns created by periods up to 100.

A common mistake is to assume that lights are independent. They are not. Two lights with periods 4 and 6, for example, are correlated because the same starting time affects both. Another mistake is treating arrival exactly at the end of a red interval incorrectly. A light is green starting at time `r`, so the interval is half-open.

For example, with one light at position 1 with `r = 1, g = 1`, half of all starting times cause the car to arrive during the red second and half during the green second. The answer is:

```
0.5
0.5
```

A method that samples integer starting times fails here because the starting time is continuous. The boundary points have zero probability and must not be treated as discrete cases.

## Approaches

The direct approach would be to find the complete repeating cycle of all lights, then scan every possible moment in that cycle. It is correct because the traffic system repeats exactly. However, the least common multiple of periods from 1 to 100 is far larger than any feasible data structure, so this approach cannot even build the timeline.

The key observation is that although the common period is huge, every periodic function involved has only a small number of possible frequencies. A light with period `p` can be described by Fourier coefficients with frequencies `k/p`. After combining all possible periods up to 100, the number of distinct reduced fractions `k/p` is only about 3000.

Instead of storing the entire timeline, we store the Fourier representation of the set of start times that are still alive. Multiplying by a light's green function removes cars stopped at that light. Multiplying by a red function and taking the constant Fourier coefficient gives the probability that the current light is the first failure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(LCM of periods) | O(LCM of periods) | Too slow |
| Fourier representation | O(n * 3044 * 100) | O(3044) | Accepted |

## Algorithm Walkthrough

1. Precompute every possible reduced frequency `a/b` where `b <= 100`. Give every such frequency an integer identifier. Also precompute how two frequencies add modulo 1.
2. For each traffic light, build the Fourier coefficients of its red interval and green interval. The interval is shifted by the light position because a car starting at time `t` reaches the light at time `t + x`.
3. Maintain a Fourier map representing the set of starting times that have passed all previous lights. Initially this is the constant function 1.
4. Before updating the current light, multiply the current survivor function by the current light's red function. The coefficient of frequency zero is exactly the fraction of starting times that fail at this light first.
5. Multiply the survivor function by the current light's green function and continue. After all lights, the zero-frequency coefficient is the probability of reaching the end.

The invariant is that after processing the first `i` lights, the Fourier representation is exactly the indicator function of starting times that make it through those `i` lights. The red multiplication extracts the subset that fails at the current light, while the green multiplication keeps only the times that survive. Since Fourier multiplication represents multiplication of periodic functions, every update preserves this meaning.

## Python Solution

```python
import sys
import math
from array import array

input = sys.stdin.readline

freqs = []
freq_id = {}
for d in range(1, 101):
    for a in range(d):
        g = math.gcd(a, d)
        if g == 1:
            key = (a, d)
            freq_id[key] = len(freqs)
            freqs.append(key)
freq_id[(0, 1)] = len(freqs)
freqs.append((0, 1))

m = len(freqs)

add_table = []
for a, b in freqs:
    row = array('H')
    for c, d in freqs:
        num = a * d + c * b
        den = b * d
        num %= den
        if num == 0:
            row.append(freq_id[(0, 1)])
        else:
            g = math.gcd(num, den)
            row.append(freq_id[(num // g, den // g)])
    add_table.append(row)

TWO_PI = 2.0 * math.pi

def make_fourier(x, r, g, red):
    p = r + g
    length = r if red else g
    start = 0 if red else r
    end = start + length
    res = []
    for k in range(p):
        if k == 0:
            val = length / p
        else:
            a = math.cos(-TWO_PI * k * start / p) + 1j * math.sin(-TWO_PI * k * start / p)
            b = math.cos(-TWO_PI * k * end / p) + 1j * math.sin(-TWO_PI * k * end / p)
            val = (a - b) / (2j * math.pi * k)
        if x and k:
            val *= math.cos(TWO_PI * k * x / p) + 1j * math.sin(TWO_PI * k * x / p)
        if abs(val) > 1e-14:
            if k == 0:
                idx = freq_id[(0, 1)]
            else:
                z = k
                d = p
                gg = math.gcd(z, d)
                idx = freq_id[(z // gg, d // gg)]
            res.append((idx, val))
    return res

def multiply(cur, poly):
    nxt = {}
    add = add_table
    for a, va in cur.items():
        row = add[a]
        for b, vb in poly:
            c = row[b]
            nxt[c] = nxt.get(c, 0j) + va * vb
    return nxt

def solve():
    n = int(input())
    lights = []
    for _ in range(n):
        x, r, g = map(int, input().split())
        lights.append((x, r, g))

    cur = {freq_id[(0, 1)]: 1.0 + 0j}
    ans = []
    zero = freq_id[(0, 1)]

    for x, r, g in lights:
        red = make_fourier(x, r, g, True)
        fail = multiply(cur, red)
        ans.append(fail.get(zero, 0).real)
        green = make_fourier(x, r, g, False)
        cur = multiply(cur, green)

    for v in ans:
        print("{:.12f}".format(v))
    print("{:.12f}".format(cur.get(zero, 0).real))

if __name__ == "__main__":
    solve()
```

The preprocessing creates a compact universe of all possible frequencies. The addition table is stored using 16-bit integers because there are fewer than 65536 possible frequencies, which keeps the convolution step fast.

The Fourier construction uses the integral of an interval indicator function. The position shift multiplies each frequency by the corresponding phase factor, matching the fact that the car reaches the light later by exactly `x` seconds.

The multiplication routine is the core of the solution. It combines every existing frequency with every frequency from the current light. Because the second operand has at most 100 entries, the number of operations stays small.

The constant coefficient is the average value of the represented function. Since our functions are indicators, that average is exactly the required probability.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * 3044 * 100) | Each light multiplies the current spectrum by at most 100 frequencies |
| Space | O(3044) | Only the possible Fourier frequencies are stored |

The largest spectrum has only a few thousand entries, so the solution fits comfortably within the given limits.

## Edge Cases

A light with no red time has `r = 0`. Its red Fourier function is empty, so its failure probability is zero. The green function is the constant function one, meaning the light does not affect the survivor distribution.

A light with no green time has `g = 0`. Every surviving car reaching it stops. The red function becomes the full indicator function, and the final survivor probability becomes zero after this update.

A car arriving exactly when a light changes from red to green must continue. The interval integration uses `[0, r)` for red and `[r, r+g)` for green, so boundary points are assigned correctly. These points do not affect the probability, but using closed intervals can introduce incorrect Fourier coefficients.
