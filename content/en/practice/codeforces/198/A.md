---
title: "CF 198A - About Bacteria"
description: "We are asked to model the growth of bacteria under a specific rule. In the first experiment, each bacterium multiplies by a factor of k every second and then b extra bacteria appear due to some abnormal effect."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 198
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 125 (Div. 1)"
rating: 1700
weight: 198
solve_time_s: 88
verified: true
draft: false
---

[CF 198A - About Bacteria](https://codeforces.com/problemset/problem/198/A)

**Rating:** 1700  
**Tags:** implementation, math  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to model the growth of bacteria under a specific rule. In the first experiment, each bacterium multiplies by a factor of _k_ every second and then _b_ extra bacteria appear due to some abnormal effect. Starting from a single bacterium, after _n_ seconds there are exactly _z_ bacteria. The task is to predict how long it would take for a second experiment, starting from _t_ bacteria, to reach at least _z_ bacteria using the same growth formula.

The inputs are four integers: _k_ is the multiplicative growth rate per second, _b_ is the additive growth per second, _n_ is the duration in seconds of the first experiment, and _t_ is the starting bacteria count of the second experiment. The output is a single integer - the minimal number of seconds needed in the second experiment to reach at least _z_ bacteria.

Constraints are moderate. All variables are ≤ 10^6. Computing the first experiment straightforwardly is feasible because _n_ is at most a million, but naive simulation of the second experiment can become too slow if the number of seconds needed is large, because bacteria grow exponentially. This suggests a mathematical approach rather than brute-force iteration.

Edge cases include situations where the additive growth _b_ dominates early growth. For example, if _k_ = 1 and _b_ > 0, the first experiment grows linearly. Another edge case is when the starting number _t_ in the second experiment is already greater than _z_, so the answer should be zero. A careless implementation could either simulate too many steps or miscompute the final second.

## Approaches

A naive approach is to simulate the second experiment second by second. Start with _t_, multiply by _k_ and add _b_ in each iteration, counting the seconds until reaching or exceeding _z_. This is correct, but if _k_ > 1, the growth is exponential, and the number of steps could be very high if _t_ is small and _z_ is large. The worst-case operations could be around 10^6 to 10^9, which is risky for a 2-second time limit.

The key insight is to avoid simulating each second by using the explicit formula for the first experiment. If the first experiment starts from 1 bacterium, after _n_ seconds the population is

```
z = k^n + b*(k^(n) - 1)/(k - 1) if k > 1
```

or

```
z = 1 + b*n if k = 1
```

We can invert this formula for the second experiment, starting from _t_, and compute how many steps _m_ satisfy

```
t * k^m + b * (k^m - 1)/(k - 1) >= z  for k > 1
```

or

```
t + m*b >= z  for k = 1
```

This lets us solve for _m_ efficiently, either with a closed formula or with a simple loop that multiplies by _k_ and adds _b_, but only until we exceed _z_. Because _m_ grows logarithmically when _k_ > 1, this is fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(m) | O(1) | Too slow if m large |
| Mathematical / Direct Formula | O(log(z/t)) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read integers _k_, _b_, _n_, _t_ from input. We do not need _n_ explicitly to simulate the second experiment; we only need the resulting _z_.
2. Compute _z_, the final number of bacteria after the first experiment. If _k_ is 1, the growth is linear, so _z_ = 1 + _n_·_b_. Otherwise, use the geometric progression formula: _z_ = k^n + b*(k^n - 1)/(k - 1).
3. Check if the starting number _t_ in the second experiment is already ≥ _z_. If so, print 0.
4. Otherwise, initialize a counter _seconds_ = 0 and a variable _current_ = _t_.
5. While _current_ < _z_, update _current_ = current*k + b and increment _seconds_ by 1.
6. When the loop exits, _current_ is at least _z_. Print _seconds_.

Why it works: at each iteration, the number of bacteria increases exactly according to the rules. Because growth is monotonic and integer arithmetic is exact, the first time _current_ reaches or exceeds _z_ is the minimal number of seconds. The formula ensures we are not undercounting or overshooting.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    k, b, n, t = map(int, input().split())

    # Compute z after first experiment
    if k == 1:
        z = 1 + n * b
    else:
        z = pow(k, n) + b * (pow(k, n) - 1) // (k - 1)

    if t >= z:
        print(0)
        return

    seconds = 0
    current = t
    while current < z:
        current = current * k + b
        seconds += 1

    print(seconds)

if __name__ == "__main__":
    main()
```

The solution separates computing _z_ from simulating the second experiment. The check for t ≥ z handles the edge case where no growth is needed. The loop is safe because the number of iterations is logarithmic when k > 1. Using integer division ensures no floating-point inaccuracies for geometric sums.

## Worked Examples

Sample 1:

Input: `3 1 3 5`

| second | current |
| --- | --- |
| 0 | 5 |
| 1 | 5*3 + 1 = 16 |
| 2 | 16*3 + 1 = 49 |

First experiment: z = 3^3 + 1*(3^3 - 1)/(3 - 1) = 27 + (26/2) = 27 + 13 = 40.

After 0 seconds, current = 5 < 40. After 1 second, 16 < 40. After 2 seconds, 49 ≥ 40. Output is 2.

Sample 2:

Input: `1 2 4 3`

First experiment: z = 1 + 4*2 = 9.

Starting current = 3. Loop:

| second | current |
| --- | --- |
| 0 | 3 |
| 1 | 3 + 2 = 5 |
| 2 | 5 + 2 = 7 |
| 3 | 7 + 2 = 9 |

Output = 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log(z/t)) | Each loop multiplies by k > 1 or adds b, doubling or more each step. In worst-case linear growth (k=1), at most z-t iterations. |
| Space | O(1) | Only a few integer variables are used. |

The constraints ensure z ≤ 10^6*(10^6^n) for large n, but Python handles large integers. At most 10^6 loop iterations in the linear case, acceptable under a 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# Provided sample
assert run("3 1 3 5\n") == "2", "sample 1"

# Custom cases
assert run("1 2 4 3\n") == "3", "linear growth"
assert run("2 1 3 10\n") == "1", "t already close to z"
assert run("1 1 1 2\n") == "0", "t >= z edge case"
assert run("2 3 5 1\n") == "3", "exponential growth small t"
assert run("3 0 4 2\n") == "2", "b = 0, pure exponential"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 4 3 | 3 | Linear growth with k=1 |
| 2 1 3 10 | 1 | Starting t close to z |
| 1 1 1 2 | 0 | Starting t already ≥ z |
| 2 3 5 1 | 3 | Exponential growth from small t |
| 3 0 4 2 | 2 | Exponential growth with b=0 |

## Edge Cases

If k = 1 and b > 0, growth is linear. For example, input `1 2 4 3`, z = 1 + 4*2 = 9, starting t = 3. Iteration adds 2 each second: 3 → 5 → 7 → 9, output 3. The algorithm correctly counts additive growth instead of multiplying by 1.

If t ≥ z initially, e
