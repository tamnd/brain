---
title: "CF 16C - Monitor"
description: "We start with a monitor whose dimensions are a × b. Both values are integers. We want to shrink this monitor so that the"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 16
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 16 (Div. 2 Only)"
rating: 1800
weight: 16
solve_time_s: 97
verified: true
draft: false
---

[CF 16C - Monitor](https://codeforces.com/problemset/problem/16/C)

**Rating:** 1800  
**Tags:** binary search, number theory  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a monitor whose dimensions are `a × b`. Both values are integers. We want to shrink this monitor so that the new dimensions keep the exact aspect ratio `x : y`.

The new monitor must satisfy three conditions at the same time.

First, both dimensions must remain integers.

Second, the new width cannot exceed `a`, and the new height cannot exceed `b`, because we are only allowed to reduce the monitor size.

Third, among all valid reduced monitors with ratio `x : y`, we want the one with the largest possible area.

The aspect ratio condition means the final dimensions must look like:

$$(k \cdot x,\ k \cdot y)$$

for some positive integer `k`.

The constraints go up to `2 · 10^9`, which immediately rules out any approach that iterates through all possible widths, heights, or scaling factors one by one. A loop running billions of times is impossible within competitive programming limits. We need a constant-time or logarithmic-time solution.

The tricky part is that the ratio may not already be reduced. For example, if `x = 6` and `y = 4`, then the ratio is actually equivalent to `3 : 2`. If we forget to simplify first, we may incorrectly conclude that some valid answers are impossible.

Consider this example:

```
a = 10
b = 10
x = 6
y = 4
```

If we use `(6k, 4k)` directly, the largest valid `k` is `1`, giving `(6, 4)` with area `24`.

But after reducing the ratio to `3 : 2`, we can use `k = 3`, giving `(9, 6)` with area `54`, which is much larger.

Another edge case appears when one dimension becomes the limiting factor.

```
a = 8
b = 5
x = 4
y = 3
```

A careless implementation might maximize width first and try `(8, 6)`, which exceeds the height limit.

The correct approach recognizes that both dimensions must fit simultaneously. The largest valid scaling factor is:

$$k = \min\left(\left\lfloor \frac{a}{x} \right\rfloor,\ \left\lfloor \frac{b}{y} \right\rfloor\right)$$

after reducing the ratio.

One more subtle case is when no valid positive monitor exists.

```
a = 1
b = 1
x = 2
y = 3
```

Even the smallest ratio-preserving monitor would need dimensions `(2, 3)`, which do not fit. The correct output is:

```
0 0
```

A buggy implementation might accidentally output negative values, fractional values, or `(2, 3)` without checking bounds carefully.

## Approaches

A brute-force approach would try every possible scaling factor `k` and check whether `(k·x, k·y)` fits inside `(a, b)`. Among all valid choices, we would keep the one with the largest area.

This works because every valid monitor with ratio `x : y` must be some integer multiple of `(x, y)`. The issue is the search space size. If `a = b = 2 · 10^9` and `x = y = 1`, then `k` can be as large as `2 · 10^9`. Iterating through billions of candidates is far too slow.

The key observation is that the area grows monotonically with `k`.

The area equals:

$$(kx)(ky) = k^2xy$$

Since `x` and `y` are fixed positive numbers, maximizing area is exactly the same as maximizing `k`.

So instead of testing every candidate, we only need the largest integer `k` satisfying:

$$kx \le a$$

$$ky \le b$$

That gives:

$$k \le \left\lfloor \frac{a}{x} \right\rfloor$$

$$k \le \left\lfloor \frac{b}{y} \right\rfloor$$

The largest valid value is simply the smaller of those two limits.

There is still one essential detail. Before computing `k`, we must reduce the ratio `(x, y)` by their greatest common divisor. Otherwise we artificially force the monitor dimensions to be larger than necessary.

For example, ratio `100 : 50` is really `2 : 1`. Using the unreduced version severely restricts the possible scaling factor.

After dividing both numbers by `gcd(x, y)`, the algorithm becomes a few arithmetic operations and one gcd computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(min(a/x, b/y)) | O(1) | Too slow |
| Optimal | O(log(min(x, y))) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the four integers `a`, `b`, `x`, and `y`.

`a` and `b` are the monitor limits, while `x : y` is the required aspect ratio.
2. Compute `g = gcd(x, y)`.

The ratio may not be reduced. Dividing by the gcd gives the smallest equivalent ratio.
3. Replace:

$$x \leftarrow \frac{x}{g}$$

$$y \leftarrow \frac{y}{g}$$

After this step, `x` and `y` are coprime.
4. Compute the maximum possible scaling factor:

$$k = \min\left(\left\lfloor \frac{a}{x} \right\rfloor,\ \left\lfloor \frac{b}{y} \right\rfloor\right)$$

Any larger value would violate at least one dimension limit.
5. Output:

$$(k \cdot x,\ k \cdot y)$$

If `k = 0`, this automatically becomes `0 0`, meaning no valid reduced monitor exists.

### Why it works

After reducing the ratio, every valid monitor with aspect ratio `x : y` has the form `(kx, ky)` for some integer `k ≥ 0`.

The monitor constraints require both dimensions to fit:

$$kx \le a$$

$$ky \le b$$

So every valid `k` must satisfy:

$$k \le \left\lfloor \frac{a}{x} \right\rfloor$$

and

$$k \le \left\lfloor \frac{b}{y} \right\rfloor$$

Taking the minimum gives the largest feasible scaling factor.

Since the area equals:

$$(kx)(ky) = k^2xy$$

and `x`, `y` are fixed positive integers, the area strictly increases as `k` increases. The largest valid `k` always produces the maximum possible area.

Reducing the ratio first is necessary because all equivalent aspect ratios should represent the same family of monitors. Using unreduced values would skip valid candidates.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

a, b, x, y = map(int, input().split())

g = gcd(x, y)

x //= g
y //= g

k = min(a // x, b // y)

print(k * x, k * y)
```

The solution follows the mathematical derivation directly.

The first important step is reducing the ratio using `gcd`. Without this, the algorithm may produce a smaller-than-optimal monitor. Since `x` and `y` can be as large as `2 · 10^9`, using Euclid's algorithm is ideal because it runs in logarithmic time.

After normalization, the code computes the largest possible scaling factor `k`. Integer division is essential here. We need the largest integer multiplier that still fits inside the monitor bounds.

The order of operations matters. We reduce the ratio before computing the divisions. If we compute limits using unreduced values, we may underestimate the valid scaling factor.

Python integers automatically avoid overflow, but this logic is also safe in 64-bit languages because the largest possible product is:

$$2 \cdot 10^9$$

which comfortably fits inside signed 64-bit integers.

The implementation naturally handles impossible cases. If either `a // x` or `b // y` equals zero, then `k = 0`, and the printed result becomes `0 0`.

## Worked Examples

### Example 1

Input:

```
800 600 4 3
```

The ratio is already reduced.

| Step | a | b | x | y | gcd | k |
| --- | --- | --- | --- | --- | --- | --- |
| Initial values | 800 | 600 | 4 | 3 | - | - |
| Compute gcd | 800 | 600 | 4 | 3 | 1 | - |
| Reduce ratio | 800 | 600 | 4 | 3 | 1 | - |
| Compute k | 800 | 600 | 4 | 3 | 1 | 200 |
| Final answer | 800 | 600 | 4 | 3 | 1 | 200 |

The resulting monitor is `(800, 600)`. This example shows that the original monitor may already satisfy the required aspect ratio.

### Example 2

Input:

```
10 10 6 4
```

The ratio is not reduced.

| Step | a | b | x | y | gcd | k |
| --- | --- | --- | --- | --- | --- | --- |
| Initial values | 10 | 10 | 6 | 4 | - | - |
| Compute gcd | 10 | 10 | 6 | 4 | 2 | - |
| Reduce ratio | 10 | 10 | 3 | 2 | 2 | - |
| Compute k | 10 | 10 | 3 | 2 | 2 | 3 |
| Final answer | 9 | 6 | 3 | 2 | 2 | 3 |

The answer becomes `(9, 6)`.

This trace demonstrates why ratio reduction is mandatory. If we skipped the gcd step, we would incorrectly get `(6, 4)` instead of the larger valid monitor.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log(min(x, y))) | Euclid's gcd algorithm dominates the runtime |
| Space | O(1) | Only a few integer variables are stored |

The constraints are extremely large, so any iterative search would fail. This solution performs only a gcd computation and a handful of arithmetic operations, which easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from math import gcd

def solve():
    input = sys.stdin.readline

    a, b, x, y = map(int, input().split())

    g = gcd(x, y)

    x //= g
    y //= g

    k = min(a // x, b // y)

    print(k * x, k * y)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
assert run("800 600 4 3\n") == "800 600", "sample 1"

# minimum valid case
assert run("1 1 1 1\n") == "1 1", "minimum case"

# impossible case
assert run("1 1 2 3\n") == "0 0", "no valid monitor"

# ratio reduction required
assert run("10 10 6 4\n") == "9 6", "must reduce ratio"

# maximum values
assert run("2000000000 2000000000 1 1\n") == "2000000000 2000000000", "large values"

# one dimension limiting
assert run("8 5 4 3\n") == "4 3", "height constraint dominates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1` | `1 1` | Smallest valid monitor |
| `1 1 2 3` | `0 0` | Impossible configuration |
| `10 10 6 4` | `9 6` | Correct gcd reduction |
| `2000000000 2000000000 1 1` | `2000000000 2000000000` | Large integer handling |
| `8 5 4 3` | `4 3` | Proper minimum bound selection |

## Edge Cases

Consider the unreduced ratio case:

```
10 10 6 4
```

The algorithm computes:

$$gcd(6,4)=2$$

so the ratio becomes `(3,2)`.

Then:

$$k = \min(10//3,\ 10//2)=\min(3,5)=3$$

The final monitor is:

```
9 6
```

If we skipped reduction, we would only get `(6,4)`, which has much smaller area.

Now examine an impossible configuration:

```
1 1 2 3
```

The ratio is already reduced. The scaling factor becomes:

$$k = \min(1//2,\ 1//3)=\min(0,0)=0$$

The algorithm outputs:

```
0 0
```

which correctly indicates that no positive monitor can satisfy the ratio.

Finally, consider a case where one dimension is the bottleneck:

```
8 5 4 3
```

We compute:

$$k = \min(8//4,\ 5//3)=\min(2,1)=1$$

The result becomes:

```
4 3
```

Even though width allows scaling by `2`, height does not. Taking the minimum of the two limits guarantees both dimensions remain valid simultaneously.
