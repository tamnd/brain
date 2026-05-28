---
title: "CF 195A - Let's Watch Football"
description: "The video consumes a units of data every second while being watched. The internet connection downloads only b units per second, and a b, so if the users start immediately, the buffer will eventually run out."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 195
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 123 (Div. 2)"
rating: 1000
weight: 195
solve_time_s: 84
verified: true
draft: false
---

[CF 195A - Let's Watch Football](https://codeforces.com/problemset/problem/195/A)

**Rating:** 1000  
**Tags:** binary search, brute force, math  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

The video consumes `a` units of data every second while being watched. The internet connection downloads only `b` units per second, and `a > b`, so if the users start immediately, the buffer will eventually run out.

They can wait for some integer number of seconds before starting playback. During this waiting period, data accumulates in the buffer. After playback begins, downloading continues in parallel with watching. We need the smallest waiting time such that the video never pauses.

Suppose they wait `t` seconds. At any real moment during playback, the total downloaded data must be at least the total consumed data.

If the video length is `c` seconds, then:

- downloaded data after `t + x` seconds is `b(t + x)`
- consumed data after watching `x` seconds is `ax`

The condition becomes:

$$b(t + x) \ge ax$$

for every `0 ≤ x ≤ c`.

The constraints are tiny, all values are at most `1000`, so even a direct simulation would fit comfortably inside the time limit. Still, the problem hides a neat mathematical simplification that turns the whole task into a one-line formula.

A common mistake is checking only the final moment of the video incorrectly. Since playback consumes data continuously, the tightest condition happens at the end of the video.

Consider:

```
a = 2, b = 1, c = 10
```

If we wait `4` seconds, we initially buffer `4` units. During the full video we download `10` more, so total downloaded becomes `14`, but the video needs `20`. Playback must fail before the end.

Another easy off-by-one mistake appears because the answer must be an integer.

Example:

```
a = 4, b = 3, c = 1
```

We need:

$$3(t+1) \ge 4$$

which gives:

$$t \ge \frac{1}{3}$$

The minimum integer answer is `1`, not `0`.

A third pitfall is forgetting that playback starts after waiting. Some incorrect solutions compare only `bt` against `ac`, as if downloading stopped during playback. That overestimates the answer.

For example:

```
a = 5, b = 4, c = 10
```

Naively requiring `bt ≥ ac` gives `t ≥ 13`.

But downloading continues while watching:

$$4(t+10) \ge 50$$

$$t \ge 2.5$$

So the correct answer is `3`.

## Approaches

The brute-force approach is straightforward. We try every waiting time `t` starting from `0`, and check whether playback can finish without interruption.

For a fixed `t`, we verify:

$$b(t+x) \ge ax$$

for all `x` from `0` to `c`.

Since the expression is linear, we could even check every second directly. With constraints up to `1000`, this would still run instantly. The worst case performs roughly one million checks, which is trivial for modern hardware.

The brute-force works because the state of the system is completely determined by downloaded data and consumed data at each moment. If every moment satisfies the inequality, playback succeeds.

The observation that unlocks the optimal solution is that the inequality becomes hardest to satisfy at the end of the video.

Rewrite it:

$$bt + bx \ge ax$$

$$bt \ge (a-b)x$$

Since `a > b`, the right side grows as `x` increases. The maximum value occurs at `x = c`.

So instead of checking every moment, we only need:

$$bt \ge (a-b)c$$

Now we just compute the smallest integer `t` satisfying this inequality:

$$t = \left\lceil \frac{(a-b)c}{b} \right\rceil$$

That removes simulation entirely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(c × answer) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read integers `a`, `b`, and `c`.
2. Compute how much extra data playback consumes compared to downloading each second.

$$a - b$$

This is the rate at which the buffer decreases during playback.

1. Over the whole video of length `c`, the total deficit becomes:

$$(a-b)c$$

This is the amount of data that must already exist in the buffer before playback starts.

1. Since waiting `t` seconds downloads `bt` units, we need:

$$bt \ge (a-b)c$$

1. Compute the smallest integer `t` satisfying the inequality using ceiling division.

$$t = \left\lceil \frac{(a-b)c}{b} \right\rceil$$

In integer arithmetic:

```
((a - b) * c + b - 1) // b
```

1. Print the result.

### Why it works

During playback, the buffer changes by `b - a` units every second. Since `a > b`, the buffer continuously decreases. That means the smallest buffer size occurs at the very end of the video.

If the buffer is still non-negative after `c` seconds of watching, then it was non-negative at every earlier moment as well. So checking only the final moment is sufficient and guarantees uninterrupted playback.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b, c = map(int, input().split())

ans = ((a - b) * c + b - 1) // b

print(ans)
```

The implementation directly follows the mathematical derivation.

The expression `(a - b) * c` computes the total amount of data missing during playback. Since the internet still downloads `b` units every second while watching, only this deficit must be buffered beforehand.

The division must round upward because the answer is restricted to integers. Using ordinary integer division would truncate downward and potentially produce a waiting time that is too small.

The standard ceiling division formula:

```
(x + y - 1) // y
```

computes:

$$\left\lceil \frac{x}{y} \right\rceil$$

without floating-point arithmetic, which avoids precision issues and keeps the solution purely integer-based.

## Worked Examples

### Sample 1

Input:

```
4 1 1
```

We compute the required initial buffer.

| Variable | Value |
| --- | --- |
| `a` | 4 |
| `b` | 1 |
| `c` | 1 |
| `(a-b)c` | 3 |
| Required `t` | `ceil(3/1)` = 3 |

Output:

```
3
```

After waiting `3` seconds, the buffer contains `3` units. During the one second of playback, another `1` unit downloads, so total available data becomes `4`, exactly enough for the video.

This trace demonstrates why downloading during playback matters.

### Sample 2

Input:

```
2 1 10
```

| Variable | Value |
| --- | --- |
| `a` | 2 |
| `b` | 1 |
| `c` | 10 |
| `(a-b)c` | 10 |
| Required `t` | `ceil(10/1)` = 10 |

Output:

```
10
```

After waiting `10` seconds, the users buffer `10` units. While watching the `10`-second video, another `10` units arrive from the internet, giving `20` total units, exactly matching the video's requirement.

This example shows the tight boundary where the final buffer becomes zero exactly at the end.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed |
| Space | O(1) | No extra data structures are used |

The constraints are extremely small, so even simulation would pass comfortably. The mathematical solution is constant time and constant memory, far below the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    a, b, c = map(int, input().split())

    ans = ((a - b) * c + b - 1) // b

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("4 1 1\n") == "3\n", "sample 1"

# custom cases
assert run("2 1 10\n") == "10\n", "long playback"

assert run("4 3 1\n") == "1\n", "ceiling division"

assert run("1000 999 1000\n") == "2\n", "large values"

assert run("5 4 10\n") == "3\n", "downloading continues during watching"

assert run("2 1 1\n") == "1\n", "minimum nonzero wait"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 10` | `10` | Long playback duration |
| `4 3 1` | `1` | Correct ceiling division |
| `1000 999 1000` | `2` | Large boundary values |
| `5 4 10` | `3` | Downloading continues during playback |
| `2 1 1` | `1` | Smallest positive answer |

## Edge Cases

Consider:

```
4 3 1
```

The inequality becomes:

$$3(t+1) \ge 4$$

$$t \ge \frac{1}{3}$$

The algorithm computes:

$$((4-3)\cdot1 + 3 - 1)//3 = 1$$

So it correctly rounds upward. A plain integer division would incorrectly produce `0`.

Now consider:

```
5 4 10
```

A wrong approach might require buffering the entire video beforehand:

$$50 / 4 = 12.5$$

leading to answer `13`.

The algorithm instead computes only the playback deficit:

$$(a-b)c = 10$$

$$\left\lceil \frac{10}{4} \right\rceil = 3$$

After waiting `3` seconds, the users buffer `12` units. During playback, another `40` units download, reaching `52`, which exceeds the required `50`.

Finally, consider the largest boundary case:

```
1000 999 1000
```

The deficit rate is only `1` unit per second:

$$(a-b)c = 1000$$

The answer becomes:

$$\left\lceil \frac{1000}{999} \right\rceil = 2$$

The algorithm handles this directly with integer arithmetic and avoids floating-point precision problems.
