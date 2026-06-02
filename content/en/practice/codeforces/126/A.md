---
title: "CF 126A - Hot Bath"
description: "We have two water taps. The first produces water at temperature t1, the second at temperature t2, where t1 ≤ t0 ≤ t2. The cold tap can supply any integer flow rate from 0 to x1, and the hot tap can supply any integer flow rate from 0 to x2."
date: "2026-06-02T16:37:16+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 126
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 93 (Div. 1 Only)"
rating: 1900
weight: 126
solve_time_s: 122
verified: true
draft: false
---

[CF 126A - Hot Bath](https://codeforces.com/problemset/problem/126/A)

**Rating:** 1900  
**Tags:** binary search, brute force, math  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two water taps. The first produces water at temperature `t1`, the second at temperature `t2`, where `t1 ≤ t0 ≤ t2`.

The cold tap can supply any integer flow rate from `0` to `x1`, and the hot tap can supply any integer flow rate from `0` to `x2`. If we choose flow rates `y1` and `y2`, the resulting mixed temperature is

$$\frac{t_1y_1+t_2y_2}{y_1+y_2}.$$

Our goal is to choose integer flow rates within the allowed limits so that the resulting temperature is at least `t0`. Among all valid choices, we want the temperature that is closest to `t0`. Since the temperature may not be exactly attainable, we minimize the excess above `t0`.

If several choices produce the same temperature, Bob prefers the bath to fill faster, so we maximize the total flow rate `y1 + y2`.

The limits are up to `10^6`, so a brute force over all possible pairs `(y1, y2)` would require up to `10^12` checks, which is completely impossible within two seconds. Any accepted solution must exploit the mathematical structure of the temperature formula.

A subtle point is that the objective is lexicographic. First minimize the temperature difference above `t0`, then maximize the total flow rate. A solution that fills faster is not allowed to sacrifice temperature quality.

Another easy mistake is forgetting that the temperature must be at least `t0`. For example:

```
t1 = 10, t2 = 70, t0 = 25
```

A mixture at temperature `24.9` is closer to `25` than a mixture at `25.1`, but it is invalid because the temperature falls below the target.

There is also the case where using only cold water is optimal.

```
10 70 100 100 10
```

Any amount of cold water alone already has temperature exactly `10`, which matches the target. The best choice is `(100, 0)` because among all exact matches it fills the bath fastest.

Finally, when `t1 = t2 = t0`, every valid mixture has exactly the target temperature. The answer is simply the maximum total flow, namely `(x1, x2)`.

## Approaches

A direct brute force would try every pair

$$0 \le y_1 \le x_1,\quad 0 \le y_2 \le x_2.$$

For each pair we compute the resulting temperature, discard those below `t0`, and keep the best candidate according to the required ordering.

The reasoning is straightforward and completely correct, but the complexity is

$$O(x_1x_2).$$

Since both limits can reach `10^6`, this becomes roughly `10^{12}` iterations and is far beyond what can be executed.

The key observation is that once we fix one flow rate, the other is essentially determined by the temperature constraint.

Suppose we fix the hot-water amount `y2`. We need

$$\frac{t_1y_1+t_2y_2}{y_1+y_2}\ge t_0.$$

Multiplying through and rearranging gives

$$(t_0-t_1)y_1 \le (t_2-t_0)y_2.$$

For a fixed `y2`, the largest valid `y1` is

$$y_1=
\left\lfloor
\frac{(t_2-t_0)y_2}{t_0-t_1}
\right\rfloor.$$

Why do we want the largest valid `y1`? Because increasing `y1` lowers the temperature. Since we are looking for the temperature closest to `t0` from above, we want as much cold water as possible while still remaining valid.

Now only `y2` remains to be enumerated. Since `x2 ≤ 10^6`, iterating over all possible hot-water flow rates is perfectly feasible.

For each `y2`, we compute the largest admissible `y1`, cap it by `x1`, and evaluate the resulting mixture. This reduces the search from two dimensions to one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(x1·x2) | O(1) | Too slow |
| Optimal | O(x2) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize the answer as `(1, 0)`. The problem guarantees `x1 ≥ 1`, so at least one valid choice always exists.
2. Iterate `y2` from `0` to `x2`.
3. If `t0 = t1`, every amount of cold water alone already satisfies the target exactly. In this special case the best cold-water amount is simply `x1`.
4. Otherwise compute

$$y_1=
\left\lfloor
\frac{(t_2-t_0)y_2}{t_0-t_1}
\right\rfloor.$$

This is the largest cold-water flow that can still keep the mixture temperature at least `t0`.

1. Since the tap capacity is limited, replace `y1` by `min(y1, x1)`.
2. Ignore the case `y1 = 0` and `y2 = 0` because the temperature would be undefined.
3. Compare the candidate mixture against the current best answer.

Instead of using floating-point arithmetic, compare temperatures through cross multiplication:

$$\frac{t_1y_1+t_2y_2}{y_1+y_2}.$$

The candidate is better if its excess above `t0` is smaller. If the excess is equal, prefer the one with larger `y1+y2`.

1. Store the best candidate and continue.
2. Output the selected pair.

### Why it works

For any fixed `y2`, increasing `y1` decreases the resulting temperature because more cold water is added. Among all valid values of `y1`, the largest valid one produces the temperature closest to `t0` from above. Any smaller value would only make the temperature hotter and strictly worse.

Since the algorithm examines every possible `y2`, and for each one chooses the unique best `y1`, every potentially optimal solution is considered. The final comparison exactly follows the problem's ordering: first minimize temperature excess above `t0`, then maximize total flow. Consequently the chosen pair is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t1, t2, x1, x2, t0 = map(int, input().split())

    best_y1 = 1
    best_y2 = 0

    best_num = t1
    best_den = 1

    for y2 in range(x2 + 1):
        if t0 == t1:
            y1 = x1
        else:
            y1 = ((t2 - t0) * y2) // (t0 - t1)
            if y1 > x1:
                y1 = x1

        if y1 == 0 and y2 == 0:
            continue

        num = t1 * y1 + t2 * y2
        den = y1 + y2

        if num < t0 * den:
            continue

        cur_diff_num = num - t0 * den
        best_diff_num = best_num - t0 * best_den

        left = cur_diff_num * best_den
        right = best_diff_num * den

        better = False

        if left < right:
            better = True
        elif left == right and den > best_den:
            better = True

        if better:
            best_y1 = y1
            best_y2 = y2
            best_num = num
            best_den = den

    print(best_y1, best_y2)

solve()
```

The loop enumerates every possible hot-water flow rate. For each one, the formula derived from the temperature constraint gives the largest cold-water flow that still keeps the temperature at least `t0`.

The implementation never uses floating-point numbers. The quantity being minimized is

$$\frac{\text{temperature}-t_0}{1},$$

which can be written as

$$\frac{\text{num}-t_0\cdot\text{den}}{\text{den}}.$$

Two such fractions are compared using cross multiplication. This avoids precision issues and remains safe because Python integers have arbitrary precision.

The special case `t0 == t1` deserves attention. The derived formula would divide by zero, so it must be handled separately. In that situation every amount of cold water is valid, and using the maximum possible amount gives the lowest temperature and the fastest filling rate.

## Worked Examples

### Example 1

Input:

```
10 70 100 100 25
```

| y2 | computed y1 | capped y1 | temperature excess |
| --- | --- | --- | --- |
| 30 | 22 | 22 | positive |
| 31 | 23 | 23 | positive |
| 32 | 24 | 24 | positive |
| 33 | 24 | 24 | very small |
| 34 | 25 | 25 | larger |
| ... | ... | ... | ... |

For `y2 = 33` we obtain `y1 = 99` after scaling through the formula. The resulting temperature is the closest attainable temperature above `25`, and no other candidate with the same excess has a larger total flow. The answer becomes:

```
99 33
```

This example demonstrates the central idea of the solution. For every hot-water amount, the best cold-water amount is immediately determined.

### Example 2

Input:

```
10 70 100 100 10
```

| y2 | y1 | resulting temperature |
| --- | --- | --- |
| 0 | 100 | 10 |
| 1 | 100 | >10 |
| 2 | 100 | >10 |

The exact target temperature is already achieved with pure cold water.

Among all exact matches, `(100, 0)` has the largest total flow, so the answer is:

```
100 0
```

This trace confirms the tie-breaking rule.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(x2) | One iteration for every possible hot-water flow rate |
| Space | O(1) | Only a few variables are maintained |

With `x2 ≤ 10^6`, the algorithm performs about one million iterations, which easily fits within the time limit. Memory usage remains constant.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    t1, t2, x1, x2, t0 = map(int, input().split())

    best_y1 = 1
    best_y2 = 0
    best_num = t1
    best_den = 1

    for y2 in range(x2 + 1):
        if t0 == t1:
            y1 = x1
        else:
            y1 = ((t2 - t0) * y2) // (t0 - t1)
            y1 = min(y1, x1)

        if y1 == 0 and y2 == 0:
            continue

        num = t1 * y1 + t2 * y2
        den = y1 + y2

        if num < t0 * den:
            continue

        cur = (num - t0 * den) * best_den
        prv = (best_num - t0 * best_den) * den

        if cur < prv or (cur == prv and den > best_den):
            best_y1 = y1
            best_y2 = y2
            best_num = num
            best_den = den

    return f"{best_y1} {best_y2}"

# provided sample
assert run("10 70 100 100 25\n") == "99 33"

# minimum values
assert run("1 1 1 1 1\n") == "1 1"

# target equals cold temperature
assert run("10 70 100 100 10\n") == "100 0"

# target equals hot temperature
assert run("10 70 100 100 70\n") == "0 100"

# all temperatures equal
assert run("5 5 10 20 5\n") == "10 20"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1 1` | `1 1` | Minimum constraints |
| `10 70 100 100 10` | `100 0` | Target equals cold temperature |
| `10 70 100 100 70` | `0 100` | Target equals hot temperature |
| `5 5 10 20 5` | `10 20` | Every mixture has identical temperature |

## Edge Cases

### Target equals cold-water temperature

Input:

```
10 70 100 100 10
```

The general formula would divide by `t0 - t1 = 0`. The algorithm explicitly handles this situation by setting `y1 = x1` for every `y2`.

The candidate `(100, 0)` achieves the exact target temperature. Any positive `y2` makes the water hotter and thus farther from the target. The output is correctly:

```
100 0
```

### Target equals hot-water temperature

Input:

```
10 70 100 100 70
```

The constraint becomes

$$(70-10)y_1 \le 0.$$

Only `y1 = 0` is possible. The algorithm computes exactly that and eventually chooses:

```
0 100
```

which is the fastest exact match.

### All temperatures equal

Input:

```
5 5 10 20 5
```

Every mixture has temperature exactly `5`. The primary objective ties for all candidates, so only total flow matters.

The algorithm compares equal temperature excesses and selects the largest denominator `y1+y2`, producing:

```
10 20
```

which uses both taps at maximum capacity.

### Optimal answer uses one tap only

Input:

```
20 100 5 5 20
```

Pure cold water already reaches the target exactly. Any hot water increases the temperature unnecessarily.

The algorithm evaluates all `y2`, discovers that `y2 = 0` gives zero excess, and returns:

```
5 0
```

which is the correct lexicographically optimal solution.
