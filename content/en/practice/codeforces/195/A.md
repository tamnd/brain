---
title: "CF 195A - Let's Watch Football"
description: "The video lasts for c seconds. Watching one second of video consumes a units of data, while the internet connection downloads only b units per second. Since a b, starting immediately is impossible because data would be consumed faster than it arrives."
date: "2026-06-05T00:48:30+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 195
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 123 (Div. 2)"
rating: 1000
weight: 195
solve_time_s: 99
verified: true
draft: false
---

[CF 195A - Let's Watch Football](https://codeforces.com/problemset/problem/195/A)

**Rating:** 1000  
**Tags:** binary search, brute force, math  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

The video lasts for `c` seconds. Watching one second of video consumes `a` units of data, while the internet connection downloads only `b` units per second. Since `a > b`, starting immediately is impossible because data would be consumed faster than it arrives.

Suppose the viewers wait `t` seconds before pressing play. By that time they have already downloaded `b · t` units of data. After playback starts, downloading continues at the same rate. The goal is to find the smallest integer `t` such that at every moment during playback, the amount of downloaded data is at least as large as the amount of data already consumed by watching.

The constraints are very small. All three values are at most 1000. Even an algorithm that checks many candidate waiting times would run comfortably within the limits. The challenge is not performance, but expressing the condition correctly.

A common mistake is to check only whether the entire video can be downloaded by the end of playback. Consider:

```
4 1 1
```

If we wait 2 seconds, then by the end of playback we have downloaded `1·(2+1)=3` units, which is still insufficient. Waiting 3 seconds gives 4 units exactly. The answer is 3.

Another subtle case is when the bottleneck occurs at the very end rather than near the start. For example:

```
2 1 10
```

Waiting 4 seconds seems close, because playback can start smoothly. However, by the end of the second watched second only 18 units have been downloaded, while 20 units are required. The correct answer is 5.

A careless simulation that only checks the start of playback would incorrectly accept such cases.

## Approaches

A direct brute-force strategy is to try waiting times `t = 0, 1, 2, ...` and test whether playback is possible.

For a fixed `t`, let `x` be the number of seconds already watched. At that point, downloaded data equals

```
b · (t + x)
```

and consumed data equals

```
a · x
```

Playback is valid if

```
b · (t + x) ≥ a · x
```

for every `x` from `0` to `c`.

Checking all `c + 1` moments for every candidate `t` works because the limits are tiny. Even trying 1000 waiting times and checking 1000 moments each is only about one million operations.

The key observation is that the inequality can be simplified:

```
b·t + b·x ≥ a·x
b·t ≥ (a-b)·x
```

Since `a > b`, the right-hand side increases as `x` increases. The hardest moment to satisfy is the largest possible value of `x`, namely `x = c`.

So instead of checking every moment, it is enough to require

```
b·t ≥ (a-b)·c
```

The answer is the smallest integer `t` satisfying this inequality:

```
t = ceil((a-b)·c / b)
```

This reduces the entire problem to a single arithmetic computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(c · answer) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `a`, `b`, and `c`.
2. Rewrite the playback condition at a watched time `x`:

```
b·(t+x) ≥ a·x
```
3. Rearrange it:

```
b·t ≥ (a-b)·x
```

The left side is constant, while the right side grows with `x`.
4. Since `a > b`, the largest value of the right side occurs at `x = c`.
5. Require:

```
b·t ≥ (a-b)·c
```
6. Compute the smallest integer satisfying the inequality:

```
t = ceil((a-b)·c / b)
```
7. Output `t`.

### Why it works

For any watched duration `x`, playback is feasible exactly when

```
b·t ≥ (a-b)·x.
```

Because `a-b` is positive, the right-hand side increases monotonically with `x`. If the inequality holds for the largest possible value `x = c`, it automatically holds for every smaller value of `x`. Thus checking the end of the video is sufficient and necessary. The smallest integer waiting time satisfying that final inequality is precisely

```
ceil((a-b)·c / b).
```

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b, c = map(int, input().split())

need = (a - b) * c
answer = (need + b - 1) // b

print(answer)
```

The variable `need` stores the total deficit that must be covered before playback starts. During each second of watching, consumption exceeds downloading by exactly `a - b` units. Over `c` seconds, that deficit accumulates to `(a - b) · c`.

Waiting `t` seconds downloads `b · t` units beforehand. We need:

```
b·t ≥ need
```

The expression

```
(need + b - 1) // b
```

computes the ceiling of `need / b` using integer arithmetic. This avoids floating-point calculations and eliminates any rounding concerns.

The constraints are tiny, but using integer math is both cleaner and mathematically exact.

## Worked Examples

### Sample 1

Input:

```
4 1 1
```

Compute the required values.

| Variable | Value |
| --- | --- |
| a | 4 |
| b | 1 |
| c | 1 |
| need = (a-b)·c | 3 |
| answer = ceil(3/1) | 3 |

Output:

```
3
```

The viewers must accumulate 3 extra units before starting. During the one second of playback, another unit arrives, giving the required 4 units total.

### Sample 2

Input:

```
2 1 10
```

| Variable | Value |
| --- | --- |
| a | 2 |
| b | 1 |
| c | 10 |
| need = (a-b)·c | 10 |
| answer = ceil(10/1) | 10 |

Output:

```
10
```

Here the connection falls behind by 1 unit every second of playback. Over 10 seconds the deficit is 10 units, so exactly 10 units must be buffered before playback starts.

This trace highlights the central invariant: the entire problem reduces to covering the cumulative deficit `(a-b)·c`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | A constant number of arithmetic operations |
| Space | O(1) | Only a few integer variables are stored |

The solution performs no loops and no auxiliary storage. It easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    a, b, c = map(int, input().split())
    need = (a - b) * c
    return str((need + b - 1) // b)

# provided sample
assert run("4 1 1\n") == "3", "sample 1"

# minimum-size values
assert run("2 1 1\n") == "1", "minimum case"

# exact divisibility
assert run("5 2 4\n") == "6", "exact division"

# ceiling required
assert run("5 3 2\n") == "2", "ceiling division"

# maximum values
assert run("1000 1 1000\n") == "999000", "maximum bounds"

# off-by-one boundary
assert run("3 2 1\n") == "1", "single unit deficit"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 1` | `1` | Smallest meaningful instance |
| `5 2 4` | `6` | Exact division case |
| `5 3 2` | `2` | Ceiling division correctness |
| `1000 1 1000` | `999000` | Largest values |
| `3 2 1` | `1` | Common off-by-one boundary |

## Edge Cases

Consider:

```
3 2 1
```

The deficit accumulated during playback is:

```
(3-2)·1 = 1
```

The algorithm computes:

```
ceil(1/2) = 1
```

Waiting 0 seconds would fail immediately because consumption begins faster than downloading. Waiting 1 second provides enough buffer.

Now consider:

```
5 2 4
```

The deficit is:

```
(5-2)·4 = 12
```

Since

```
12 / 2 = 6
```

is already an integer, the answer is exactly 6. This case verifies that the ceiling formula does not accidentally add an extra second when division is exact.

Finally, consider the largest possible values:

```
1000 1 1000
```

The deficit becomes:

```
(1000-1)·1000 = 999000
```

and the answer is

```
999000
```

All arithmetic comfortably fits inside standard integer types, and the formula still works without any special handling.
