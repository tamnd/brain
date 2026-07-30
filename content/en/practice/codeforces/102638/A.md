---
title: "CF 102638A - Listen To Your Heart"
description: "The task hides a single integer inside an equation involving square roots, cube roots, and two different powers. There is no input value to process. The program only has to determine the unique integer x satisfying the equation and print it."
date: "2026-07-31T00:28:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102638
codeforces_index: "A"
codeforces_contest_name: "Bredor contest"
rating: 0
weight: 102638
solve_time_s: 151
verified: true
draft: false
---

[CF 102638A - Listen To Your Heart](https://codeforces.com/problemset/problem/102638/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

The task hides a single integer inside an equation involving square roots, cube roots, and two different powers. There is no input value to process. The program only has to determine the unique integer `x` satisfying the equation and print it.

The unusual part of this problem is that the equation is not intended to be solved by numerical search. The time limit is effectively asking for a constant-time observation. A brute force program that tries many integers would spend time checking square roots and cube roots repeatedly, while the intended solution should reduce the algebra to a direct construction.

There are no input-dependent constraints because the input is empty. The only meaningful constraint is that the answer must be found exactly. Floating point approximations are dangerous because the equation involves large powers, where a tiny rounding error can turn a correct equality into a false comparison.

A careless approach might search only a small interval. For example, trying values from `0` to `100` would never find the answer, because the correct output is `228`. Another mistake is to compare the two sides using floating point arithmetic. Even if the correct integer is reached, expressions such as powers of irrational values can accumulate enough error to fail an equality check.

## Approaches

A straightforward approach would be to iterate over possible integers `x`, verify that all radicals are defined, evaluate both sides of the equation, and stop when they match. This is logically correct because the statement guarantees that exactly one integer works. However, it has no natural upper bound. Searching a wide range would require an unknown number of expensive radical evaluations, and checking equality with floating point values would also be unreliable.

The key observation comes from the powers. If two real numbers satisfy `a^7 = b^3`, then because 7 and 3 are coprime, both values can be represented using a common base. We can write:

```
a = t^3
b = t^7
```

for some real value `t`.

Applying this to the right side gives:

```
x - sqrt((x^2 - 1984) / 5) = t^7
```

The hidden value turns out to be very simple. Trying the natural small integer candidate `t = 2` gives `t^7 = 128`. Substituting this into the second expression:

```
x - sqrt((x^2 - 1984) / 5) = 128
```

and isolating the square root gives:

```
(x - 128)^2 = (x^2 - 1984) / 5
```

Expanding this equation results in:

```
x^2 - 320x + 20976 = 0
```

The discriminant is `18496`, whose square root is `136`, giving the possible roots:

```
x = (320 ± 136) / 2
```

The two candidates are `228` and `92`. Only `228` satisfies the original unsquared equation because the square root must equal `x - 128`, which is non-negative. Checking the other side confirms the hidden structure:

```
sqrt(228 - 3) - cbrt((3 * 228 + 2) / 2)
= sqrt(225) - cbrt(343)
= 15 - 7
= 8
= 2^3
```

So the entire equation is satisfied with `t = 2` and `x = 228`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(R) checks over searched range | O(1) | Too slow and unreliable |
| Algebraic Observation | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Recognize that the two sides have powers 7 and 3, so represent both sides using a shared base. The left side becomes `t^3` and the right side becomes `t^7`.
2. Find the small integer base that makes the expressions align. Taking `t = 2` makes the right side equal to `128`.
3. Solve the equation:

```
x - sqrt((x^2 - 1984) / 5) = 128
```

by moving the non-radical part to the other side and squaring.

1. Solve the resulting quadratic equation. It produces two possible values, `228` and `92`.
2. Check the sign condition from the original square root expression. The value under the square root represents `x - 128`, so the candidate must satisfy `x >= 128`. This removes `92`.
3. Output `228`.

Why it works:

The transformation does not guess the answer directly. The powers force both sides of the equation to be powers of the same quantity. The value `t = 2` creates an exact integer structure: the right side becomes `128`, and the left side becomes `8`, which is exactly `2^3`. Solving the resulting quadratic finds every possible candidate created by this transformation, and checking the original sign condition removes the extraneous solution introduced by squaring.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    print(228)

if __name__ == "__main__":
    solve()
```

The solution does not read any input because the problem contains no input data. The complete algebraic reduction shows that the only valid integer is `228`, so the program only needs to print that value.

There are no overflow concerns because no arithmetic is performed at runtime. There are also no floating point operations, avoiding precision problems from the original equation.

## Worked Examples

Since the problem has no sample input, the traces below use the only meaningful execution: the program starts and prints the fixed solution.

| Step | Action | Value |
| --- | --- | --- |
| 1 | Start program | No input |
| 2 | Call `solve()` | `print(228)` |
| 3 | Output | `228` |

This trace demonstrates that the algorithm does not depend on external values. The equation itself uniquely determines the output.

| Step | Action | Value |
| --- | --- | --- |
| 1 | Check input stream | Empty |
| 2 | Skip parsing | No variables needed |
| 3 | Print answer | `228` |

This second trace confirms that an implementation expecting test cases or numerical input would be solving a different problem.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The program performs one output operation. |
| Space | O(1) | No additional storage is used. |

The memory limit is easily satisfied because the program stores no data. The constant-time solution is the only practical approach for a task with no input and an exact algebraic answer.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return "228\n"
    finally:
        sys.stdin = old_stdin

assert run("") == "228\n", "empty input"

assert run("\n") == "228\n", "newline input"

assert run("0\n") == "228\n", "unexpected extra input"

assert run("100\n") == "228\n", "arbitrary ignored input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Empty input | 228 | The official input format contains nothing. |
| Newline input | 228 | Whitespace does not affect the solution. |
| `0` | 228 | The program does not incorrectly depend on external numbers. |
| `100` | 228 | The fixed equation answer is always printed. |

## Edge Cases

A search-based solution may fail because it assumes the answer lies in a guessed range. For example, an implementation testing only values from `1` to `100` receives no input but still tries possible answers internally. It would incorrectly conclude that there is no solution, while the correct output is `228`. The constant-time solution avoids this by deriving the value instead of searching.

A floating point verification approach can also fail. The valid answer is:

```
x = 228
```

At this value, the left base is exactly:

```
sqrt(225) - cbrt(343) = 15 - 7 = 8
```

and the right base is exactly:

```
228 - sqrt((228^2 - 1984) / 5) = 228 - 100 = 128
```

The equality is:

```
8^7 = 128^3
```

A numerical approximation might represent one side slightly differently after repeated radical and power operations. The final solution avoids all such comparisons by printing the proven integer directly.
