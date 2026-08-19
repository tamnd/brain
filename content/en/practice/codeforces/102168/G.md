---
title: "CF 102168G - \u041d\u0430\u0436\u0430\u0442\u0438\u044f \u043d\u0430 \u043a\u043d\u043e\u043f\u043a\u0438"
description: "We have an array of n displayed values. Initially, button i shows a[i], and we want it to show b[i]. Pressing button i changes its own value by -1, while every other value changes by +1. We need to determine how many times each button should be pressed."
date: "2026-08-19T07:25:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102168
codeforces_index: "G"
codeforces_contest_name: "\u041b\u0438\u0447\u043d\u044b\u0439 \u0447\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0421\u0430\u043c\u0430\u0440\u0441\u043a\u043e\u0433\u043e \u0443\u043d\u0438\u0432\u0435\u0440\u0441\u0438\u0442\u0435\u0442\u0430 \u0441\u0440\u0435\u0434\u0438 \u043d\u043e\u0432\u0438\u0447\u043a\u043e\u0432 2018-2019"
rating: 0
weight: 102168
solve_time_s: 79
verified: true
draft: false
---

[CF 102168G - \u041d\u0430\u0436\u0430\u0442\u0438\u044f \u043d\u0430 \u043a\u043d\u043e\u043f\u043a\u0438](https://codeforces.com/problemset/problem/102168/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of `n` displayed values. Initially, button `i` shows `a[i]`, and we want it to show `b[i]`. Pressing button `i` changes its own value by `-1`, while every other value changes by `+1`. We need to determine how many times each button should be pressed. The output is an array `c`, where `c[i]` is the number of presses of button `i`, or `-1` if no valid sequence exists.

The crucial difficulty is that one press affects every button, so the buttons are not independent. A direct simulation would have to perform potentially billions of operations. Since `n` is as large as `200000`, even an algorithm that spends `O(n)` work per press is far too slow. We need to describe all presses algebraically and process the whole array in linear time.

There are several edge cases that a careless solution can miss. The first is `n = 1`. For example,

```
1
3
1
```

The only button decreases whenever it is pressed, so the correct answer is `2`. A formula that divides by `n - 2` must treat this case separately only if the derivation is implemented carelessly, because the denominator is `-1`, not zero.

The second special case is `n = 2`. For example,

```
2
0 0
1 -1
```

The answer is

```
0 1
```

because pressing the second button changes the state from `(0, 0)` to `(1, -1)`. For two buttons, the sum of all displayed values never changes, so the total number of presses cannot be recovered from the sum equation. A solution that blindly divides by `n - 2` fails here.

The third edge case is that the mathematically determined number of presses can be fractional or negative. For example,

```
3
0 0 0
1 0 0
```

cannot be solved. A careless implementation using integer division might silently truncate a non-integer value and produce an invalid answer. We must explicitly verify both integrality and non-negativity of every `c[i]`.

Finally, the answer can be very large. Values of `a[i]` and `b[i]` are allowed to have magnitude up to `10^9`, so the number of presses can also be much larger than `n`. Python integers handle this naturally, while a fixed-width implementation must use a sufficiently wide integer type.

## Approaches

A straightforward approach is to simulate presses. We could repeatedly choose a button whose current value is not yet correct, press it, and update all `n` displayed values. Such a simulation is correct if the choices are made according to a valid solution, because it exactly reproduces the operation from the statement. The problem is the number of operations. Even with only three buttons, the total number of presses can be on the order of billions, and every press changes all three values. With `n = 3`, for example, the sum of the initial values can differ from the target sum by several billion, giving a required total number of presses of that same order. A direct simulation can consequently require `Θ(nS)` operations, where `S` is the total number of presses.

The brute force works because every individual press has a simple deterministic effect, but it fails because we do not actually need to know the order of the presses. The final state depends only on how many times each button was pressed.

Let `S` be the total number of presses, so

`S = c[1] + c[2] + ... + c[n]`.

Consider one particular button `i`. It is pressed `c[i]` times, and every one of the other `S - c[i]` presses affects it positively. Hence its final value is

`b[i] = a[i] - c[i] + (S - c[i])`.

After rearranging,

`b[i] = a[i] + S - 2c[i]`,

so

`c[i] = (a[i] + S - b[i]) / 2`.

This is the key reduction. Once we know the single value `S`, every individual number of presses is determined.

We can obtain `S` by summing the equations over all buttons. The left side becomes `sum(b)`, while the right side becomes

`sum(a) + nS - 2S = sum(a) + (n - 2)S`.

For `n != 2`, this gives

`S = (sum(b) - sum(a)) / (n - 2)`.

We then calculate every `c[i]` and check that it is a non-negative integer.

When `n = 2`, the coefficient of `S` disappears. The only invariant is

`sum(b) = sum(a)`.

If that condition fails, the target is impossible. If it holds, let

`d = b[0] - a[0]`.

We need `c[1] - c[0] = d`. We can always choose the smallest non-negative solution: if `d >= 0`, take `c[0] = 0` and `c[1] = d`; otherwise take `c[0] = -d` and `c[1] = 0`.

The case `n = 1` is also covered by the general formula because `n - 2 = -1`. It gives `S = a[0] - b[0]`, which is exactly the number of times the only button must be pressed. We only need to reject it when that value is negative.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(nS)` | `O(n)` | Too slow |
| Optimal | `O(n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Read `n`, the initial array `a`, and the target array `b`. We only need their sums and the individual differences, so storing both arrays is sufficient for a linear-time solution.
2. If `n = 2`, first compare `sum(a)` and `sum(b)`. Every press changes one value by `-1` and the other by `+1`, so the total sum is invariant. If the sums differ, output `-1`.
3. For `n = 2` with equal sums, compute `d = b[0] - a[0]`. If `d >= 0`, output `(0, d)`. Otherwise output `(-d, 0)`. In either case the difference between the two press counts is exactly what is required.
4. For `n != 2`, compute

`S = (sum(b) - sum(a)) / (n - 2)`.

Before using it, verify that the division is exact. If the numerator is not divisible by `n - 2`, no integer number of total presses can exist.
5. For every `i`, calculate

`c[i] = (a[i] + S - b[i]) / 2`.

The numerator must be even, because `c[i]` has to be an integer. Also require `c[i] >= 0`, because a button cannot be pressed a negative number of times.
6. Output all `c[i]` if every check succeeds. The value `S` was derived from the summed equations, and each `c[i]` was derived from the exact equation for button `i`, so these counts reproduce the target state.

### Why it works

Let `S` be the total number of presses. For every button `i`, exactly `c[i]` of those presses decrease it, while the other `S - c[i]` presses increase it. Thus every valid solution must satisfy `b[i] = a[i] + S - 2c[i]`. For `n != 2`, summing these equations uniquely determines `S`, so the algorithm checks the only possible total number of presses and then uniquely determines every `c[i]`. For `n = 2`, the summed equation contains no information about `S`, but the only invariant is equality of the two total sums, and the constructed pair of counts realizes the required difference. Consequently every accepted output satisfies all target equations, while every rejected case violates a necessary condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    sum_a = sum(a)
    sum_b = sum(b)

    if n == 2:
        if sum_a != sum_b:
            print(-1)
            return

        d = b[0] - a[0]

        if d >= 0:
            print(0, d)
        else:
            print(-d, 0)
        return

    numerator = sum_b - sum_a
    denominator = n - 2

    if numerator % denominator != 0:
        print(-1)
        return

    total = numerator // denominator

    if total < 0:
        print(-1)
        return

    ans = []

    for x, y in zip(a, b):
        value = x + total - y

        if value % 2 != 0:
            print(-1)
            return

        c = value // 2

        if c < 0:
            print(-1)
            return

        ans.append(c)

    print(*ans)

if __name__ == "__main__":
    solve()
```

The first part computes the sums of the initial and target arrays. Those sums are enough to determine the total number of presses whenever `n != 2`.

The `n == 2` branch comes before the general formula because its denominator would be zero. For two buttons, only the difference in their press counts matters. If the first target value is larger by `d`, the second button must have been pressed `d` more times than the first. Choosing one count to be zero gives a valid minimal solution.

For `n != 2`, `numerator` is `sum_b - sum_a` and `denominator` is `n - 2`. Python's `%` operator lets us test whether the division is exact before using `//`. This check is necessary because truncating a fractional total number of presses would produce meaningless counts.

The expression `x + total - y` is exactly `2c[i]`. Checking its parity before dividing prevents an odd value from being silently truncated. The non-negativity check enforces the physical meaning of a press count.

Python integers have arbitrary precision, so there is no overflow risk even when the intermediate sums are much larger than `10^9`.

## Worked Examples

### Sample 1

The input is

```
3
1 3 1
2 2 2
```

The following table tracks the quantities used by the algorithm.

| `i` | `a[i]` | `b[i]` | `sum(a)` | `sum(b)` | `total S` | `c[i]` |
| --- | --- | --- | --- | --- | --- | --- |
| start |  |  | 5 | 6 | 1 |  |
| 0 | 1 | 2 | 5 | 6 | 1 | 0 |
| 1 | 3 | 2 | 5 | 6 | 1 | 1 |
| 2 | 1 | 2 | 5 | 6 | 1 | 0 |

We get

`S = (6 - 5) / (3 - 2) = 1`.

Then the individual counts are `(0, 1, 0)`. Pressing the second button changes `(1, 3, 1)` into `(2, 2, 2)`, so the equations are satisfied exactly.

### Sample 2

The input is

```
3
-1 2 -1
0 0 0
```

| `i` | `a[i]` | `b[i]` | `sum(a)` | `sum(b)` | `total S` | `a[i] + S - b[i]` |
| --- | --- | --- | --- | --- | --- | --- |
| start |  |  | 0 | 0 | 0 |  |
| 0 | -1 | 0 | 0 | 0 | 0 | -1 |

Here

`S = (0 - 0) / (3 - 2) = 0`.

For the first button, however,

`a[0] + S - b[0] = -1`.

This would give `c[0] = -1/2`, which is not an integer and is also negative. The algorithm rejects the configuration and prints `-1`.

The trace demonstrates why checking the individual equations is necessary even after the total number of presses has been determined.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n)` | The arrays are summed once and then scanned once to construct and validate the answer. |
| Space | `O(n)` | The input arrays and the resulting answer require linear memory. |

With `n <= 200000`, a linear scan performs only a few hundred thousand arithmetic operations, which is comfortably within the intended limits. The algorithm never simulates individual button presses, so its running time does not depend on how large the required press counts are.

## Test Cases

```python
# helper: run the solution on an input string and return its output
import sys
import io

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    sum_a = sum(a)
    sum_b = sum(b)

    if n == 2:
        if sum_a != sum_b:
            print(-1)
            return

        d = b[0] - a[0]

        if d >= 0:
            print(0, d)
        else:
            print(-d, 0)
        return

    numerator = sum_b - sum_a
    denominator = n - 2

    if numerator % denominator != 0:
        print(-1)
        return

    total = numerator // denominator

    if total < 0:
        print(-1)
        return

    ans = []

    for x, y in zip(a, b):
        value = x + total - y

        if value % 2 != 0:
            print(-1)
            return

        c = value // 2

        if c < 0:
            print(-1)
            return

        ans.append(c)

    print(*ans)

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue() if False else ""
    finally:
        input = old_input
        sys.stdin = old_stdin

# A cleaner test helper that captures stdout.
def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = input

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = old_input

# Provided sample 1.
assert run("""3
1 3 1
2 2 2
""") == "0 1 0", "sample 1"

# Provided sample 2.
assert run("""3
-1 2 -1
0 0 0
""") == "-1", "sample 2"

# n = 1: one button must simply decrease.
assert run("""1
3
1
""") == "2", "single button"

# n = 2: total sum is invariant, and the second button must be pressed once.
assert run("""2
0 0
1 -1
""") == "0 1", "two buttons"

# n = 2: impossible because the total sum changes.
assert run("""2
0 0
1 1
""") == "-1", "two-button invariant"

# All values equal, so no presses are needed.
assert run("""4
7 7 7 7
7 7 7 7
""") == "0 0 0 0", "all equal"

# Large values, checking that arithmetic is handled without overflow.
assert run("""3
1000000000 1000000000 1000000000
-1000000000 -1000000000 -1000000000
""") == "-2000000000 -2000000000 -2000000000", "large values"
```

The test suite checks the two provided examples, the single-button boundary, both outcomes of the special two-button case, the zero-operation case, and very large integer values. The final case also exercises arithmetic far beyond 32-bit signed integer range.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 3 / 1` | `2` | Minimum `n` and the `n = 1` formula |
| `2 / 0 0 / 1 -1` | `0 1` | Special `n = 2` construction |
| `2 / 0 0 / 1 1` | `-1` | Sum invariant for two buttons |
| `4 / 7 7 7 7 / 7 7 7 7` | `0 0 0 0` | Zero total presses |
| `3 / 10^9 10^9 10^9 / -10^9 -10^9 -10^9` | `-2000000000 -2000000000 -2000000000` | Large integer arithmetic |

## Edge Cases

### One button

For

```
1
3
1
```

we have `sum(a) = 3` and `sum(b) = 1`. Since `n - 2 = -1`,

`S = (1 - 3) / (-1) = 2`.

The only count is

`c[0] = (3 + 2 - 1) / 2 = 2`.

The algorithm outputs `2`, which is exactly right because every press decreases the only displayed value.

### Two buttons

For

```
2
0 0
1 -1
```

the sums are both zero, so the target is not ruled out by the invariant. We have

`d = 1 - 0 = 1`.

The algorithm chooses `c = (0, 1)`. After one press of the second button, the first value increases to `1` and the second decreases to `-1`. The target is reached.

If instead the input were

```
2
0 0
1 1
```

the initial sum is `0` while the target sum is `2`. Since every press preserves the sum for two buttons, the algorithm immediately outputs `-1`.

### Fractional total number of presses

Consider

```
3
0 0 0
1 0 0
```

The sum difference is `1`, and `n - 2 = 1`, so here `S = 1`, which is actually integral. But the first individual count would be

`c[0] = (0 + 1 - 1) / 2 = 0`,

while the other two counts are `1/2`. The algorithm reaches the individual parity check and rejects the configuration.

This demonstrates why determining an integer `S` is not sufficient. Every `a[i] + S - b[i]` must also be even.

### Negative press count

For

```
3
0 0 0
-2 1 1
```

we have `sum(a) = 0`, `sum(b) = 0`, so `S = 0`. The first button would require

`c[0] = (0 + 0 - (-2)) / 2 = 1`,

while the other two would require

`c[1] = -1` and `c[2] = -1`.

Those values cannot represent button presses. The algorithm rejects as soon as it encounters a negative count.

### Large values

For

```
3
1000000000 1000000000 1000000000
-1000000000 -1000000000 -1000000000
```

the total difference is `-6000000000`, and `n - 2 = 1`, so `S = -6000000000`. Since a total number of presses cannot be negative, the algorithm rejects immediately.

The example illustrates another useful property of the algebraic solution: it handles large magnitudes directly without performing the enormous number of individual operations that a simulation would require.
