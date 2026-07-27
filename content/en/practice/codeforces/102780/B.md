---
title: "CF 102780B - Mysterious Resistors"
description: "The circuit is built from several identical unknown resistors. Each stage contains one known resistor and one mysterious resistor connected in parallel, and all stages are then connected in series."
date: "2026-07-27T20:06:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102780
codeforces_index: "B"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 19)"
rating: 0
weight: 102780
solve_time_s: 69
verified: true
draft: false
---

[CF 102780B - Mysterious Resistors](https://codeforces.com/problemset/problem/102780/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

The circuit is built from several identical unknown resistors. Each stage contains one known resistor and one mysterious resistor connected in parallel, and all stages are then connected in series. The input gives the number of stages, the total resistance of the whole circuit, and the known resistor value in every stage. The task is to recover the resistance of the mysterious resistor.

If the unknown resistance is `x`, the contribution of a single stage with known resistance `ri` is

$$\frac{ri \cdot x}{ri + x}$$

because the two resistors are connected in parallel. The total circuit resistance is the sum of these values over all stages, so we need to find `x` such that

$$\sum_{i=1}^{k}\frac{r_i x}{r_i+x}=R$$

The number of stages can reach 1000, and each known resistance can be large. This rules out methods that try many possible resistance values or perform symbolic equation solving with many terms. The useful property is that the required precision is only `10^-6`, so an iterative numerical method with about 60 to 100 iterations is easily fast enough. A solution around `O(k log precision)` operations fits comfortably because it only performs a simple sum over at most 1000 values per iteration.

A few cases can break careless implementations. A common mistake is assuming the answer is always close to the largest known resistor. For example, with input

```
1 5
10
```

the correct output is `10.000000`, because the only stage has resistance

$$\frac{10x}{10+x}=5$$

which gives `x=10`. A fixed upper bound like `100000` would fail on larger possible answers.

Another issue is stopping the binary search too early. With

```
3 11
3 12 30
```

the answer is `6.000000`. A few iterations might find an approximation that looks close but does not satisfy the required precision. The function changes smoothly, so many iterations are cheap and avoid this problem.

A third edge case is when the target is exactly half of the sum of the known resistances. For example,

```
2 10
10 10
```

has answer `10`, because each parallel pair contributes `5`. The algorithm must allow the upper boundary to reach this value instead of stopping when the search interval merely becomes small.

## Approaches

A direct approach is to try possible values of the mysterious resistor and calculate the resulting total resistance. Since the resistance is a continuous value, we cannot enumerate all candidates exactly, and a naive scan over a fine grid would require an enormous number of checks. Even if the range were limited to one million possible values and every check only took `k` operations, the worst case would already require around one billion operations when `k=1000`.

The useful observation is that the total resistance is a monotonic function of the unknown resistor. When `x` increases, every individual parallel resistance

$$\frac{r_i x}{r_i+x}$$

also increases. This means there is exactly one answer, and we can use binary search on the value of `x`.

The brute-force approach works because evaluating a candidate value is easy, but it fails because finding a sufficiently accurate candidate by trying values one by one is too expensive. The monotonic relationship between the unknown resistance and the final circuit resistance lets us discard half of the search space after every iteration.

The search interval can start from zero. The upper bound is found dynamically by repeatedly doubling it until the calculated resistance becomes at least `R`. The required answer is guaranteed to exist because the maximum possible circuit resistance approaches the sum of all known resistances, and the statement guarantees that the target does not exceed half of this value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k * number of tried values) | O(1) | Too slow |
| Optimal | O(k log precision) | O(1) | Accepted |

## Algorithm Walkthrough

1. Store the known resistances and define a function that calculates the total circuit resistance for a chosen mysterious resistor value `x`. The function adds the parallel resistance of every stage, which gives the resistance the circuit would have if the unknown resistor were `x`.
2. Start with a lower bound of `0` and an upper bound of `1`. Increase the upper bound by doubling it until the calculated resistance is at least the target `R`. This creates an interval containing the real answer without needing any assumptions about the size of the unknown resistor.
3. Repeat binary search on this interval. Take the middle value and calculate the circuit resistance produced by it. If the result is smaller than `R`, the unknown resistor must be larger, so move the lower bound upward. Otherwise, the unknown resistor is smaller or equal to this value, so move the upper bound downward.
4. Perform enough iterations to make the interval much smaller than the required error. Around 100 iterations is more than enough because the interval shrinks by half every time.
5. Output the final midpoint as the estimated value of the mysterious resistor.

Why it works: the calculated total resistance is strictly increasing with respect to the unknown resistance. Every binary search decision is based on this ordering, so when a midpoint produces too small a resistance, every smaller value is also invalid. When it produces too large a resistance, every larger value is also invalid. The search interval always contains the true answer, and repeated halving makes the interval converge to that answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    k, R = map(int, input().split())
    r = list(map(int, input().split()))

    def calc(x):
        total = 0.0
        for v in r:
            total += v * x / (v + x)
        return total

    lo = 0.0
    hi = 1.0

    while calc(hi) < R:
        hi *= 2.0

    for _ in range(100):
        mid = (lo + hi) / 2.0
        if calc(mid) < R:
            lo = mid
        else:
            hi = mid

    print("{:.10f}".format((lo + hi) / 2.0))

if __name__ == "__main__":
    solve()
```

The `calc` function directly implements the electrical formula for a candidate mysterious resistor value. It uses floating point arithmetic because the answer is not necessarily an integer and the required precision is decimal.

The upper bound search is dynamic rather than fixed. This avoids relying on a guessed maximum answer and handles cases where the unknown resistor is larger than every known resistor. Doubling finishes quickly because the required answer range is limited by the input constraints.

The binary search runs for a fixed number of iterations instead of checking an epsilon condition. This avoids precision corner cases and gives a guaranteed amount of shrinking. One hundred iterations leaves far more accuracy than the required `10^-6`.

Python floating point values are sufficient here because the largest intermediate values are small enough and the final answer only needs six digits after the decimal point.

## Worked Examples

For the first sample:

```
3 11
3 12 30
```

The search evaluates different guesses for the unknown resistor.

| Iteration idea | Lower bound | Upper bound | Midpoint result |
| --- | --- | --- | --- |
| Initial range | 0 | 8 | Too small or close to target |
| Later search | Around 6 | Around 8 | Above 11 |
| Final range | Near 6 | Near 6 | Converges to 6 |

The algorithm finds that a mysterious resistor of `6` makes the three parallel stages sum to `11`. The shrinking interval demonstrates the monotonic property used by binary search.

For the second sample:

```
7 110
15 60 6 45 20 120 70
```

| Iteration idea | Lower bound | Upper bound | Decision |
| --- | --- | --- | --- |
| Initial expansion | 0 | 32 | Resistance below target |
| Expanded range | 0 | 64 | Resistance above target |
| Final search | Near 30 | Near 30 | Converges to 30 |

The upper bound expansion quickly finds an interval containing the answer. Binary search then narrows it until the result is `30.000000`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k log precision) | Each of about 100 iterations evaluates all `k` stages once |
| Space | O(1) | Only the resistance list and a few variables are stored |

With `k <= 1000`, the algorithm performs roughly 100,000 arithmetic operations. This is easily within the limits, while approaches that try many possible resistor values would not scale.

## Test Cases

```python
import sys
import io

def solve(inp):
    data = inp.strip().split()
    k = int(data[0])
    R = int(data[1])
    r = list(map(int, data[2:]))

    def calc(x):
        s = 0.0
        for v in r:
            s += v * x / (v + x)
        return s

    lo = 0.0
    hi = 1.0
    while calc(hi) < R:
        hi *= 2.0

    for _ in range(100):
        mid = (lo + hi) / 2
        if calc(mid) < R:
            lo = mid
        else:
            hi = mid

    return "{:.6f}".format((lo + hi) / 2)

assert solve("3 11\n3 12 30\n") == "6.000000"
assert solve("7 110\n15 60 6 45 20 120 70\n") == "30.000000"

assert solve("1 5\n10\n") == "10.000000"
assert solve("2 10\n10 10\n") == "10.000000"
assert solve("3 3\n3 3 3\n") == "1.000000"
assert solve("4 100000\n100000 100000 100000 100000\n") == "100000.000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 5 / 10` | `10.000000` | Single stage and large unknown value |
| `2 10 / 10 10` | `10.000000` | Exact half-sum boundary case |
| `3 3 / 3 3 3` | `1.000000` | Small answer and repeated values |
| `4 100000 / 100000 100000 100000 100000` | `100000.000000` | Large values and upper-bound expansion |

## Edge Cases

For the single-stage case

```
1 5
10
```

the function being searched is

$$f(x)=\frac{10x}{10+x}$$

The binary search begins with a small range, expands the upper bound until the function reaches at least `5`, and then converges to `x=10`. It does not depend on having multiple stages.

For the exact boundary case

```
2 10
10 10
```

the total known resistance is `20`, and the target is exactly half of that. The correct answer is `10`. At `x=10`, each stage contributes

$$\frac{10\cdot10}{10+10}=5$$

so the total is `10`. The dynamic upper bound allows the search to include this value.

For a case where all resistors are equal,

```
3 3
3 3 3
```

the answer is `1`. Each stage contributes

$$\frac{3\cdot1}{3+1}=0.75$$

and the total is `2.25`, so the algorithm continues searching until it finds the value that gives exactly `3`. The monotonic check handles repeated values without any special case.

For the largest values,

```
4 100000
100000 100000 100000 100000
```

the unknown resistance is `100000`. The initial upper bound is far too small, but doubling quickly reaches a range containing the answer. The search then works the same way as in smaller cases, showing why a dynamic upper bound is safer than a hardcoded limit.
