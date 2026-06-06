---
title: "CF 200B - Drinks"
description: "We are given several drinks, and each drink contains some percentage of orange juice. Vasya mixes equal amounts of every drink into a single cocktail. The question is simple: after mixing them, what percentage of the final cocktail is orange juice?"
date: "2026-06-03T16:24:54+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 200
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 126 (Div. 2)"
rating: 800
weight: 200
solve_time_s: 128
verified: false
draft: false
---

[CF 200B - Drinks](https://codeforces.com/problemset/problem/200/B)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 2m 8s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several drinks, and each drink contains some percentage of orange juice. Vasya mixes equal amounts of every drink into a single cocktail.

The question is simple: after mixing them, what percentage of the final cocktail is orange juice?

The input contains the number of drinks and the orange juice percentage of each drink. The output is the orange juice percentage in the mixture.

The constraints are extremely small. There are at most 100 drinks, so any algorithm that processes each percentage once will finish instantly. Even an unnecessarily complicated simulation would still fit comfortably within the limits. This means the challenge is not algorithmic efficiency but correctly understanding how mixing equal quantities affects percentages.

A common mistake is to think about actual volumes and simulate them. The problem does not tell us how many milliliters are taken from each drink. Fortunately, that value does not matter because the same amount is taken from every drink. The final percentage is simply the average of the individual percentages.

Another subtle case occurs when some drinks contain no orange juice at all.

Input:

```
2
0 100
```

Output:

```
50
```

A careless implementation that ignores zero values or divides by the wrong quantity could produce an incorrect result. The mixture contains equal amounts of a pure orange juice drink and a drink with none, so the average is exactly 50%.

Another edge case is when every drink contains 0% orange juice.

Input:

```
3
0 0 0
```

Output:

```
0
```

The answer remains valid because averaging zeros still gives zero.

Similarly, if every drink contains 100% orange juice:

Input:

```
4
100 100 100 100
```

Output:

```
100
```

The mixture remains pure orange juice.

## Approaches

A direct brute-force interpretation is to assume Vasya takes some amount, say 100 milliliters, from every drink. We could compute how many milliliters of orange juice come from each drink, sum those amounts, compute the total volume of the cocktail, and finally divide.

For a drink with percentage `p`, taking 100 milliliters contributes `p` milliliters of orange juice. After processing all drinks, the orange juice percentage is

$$\frac{\text{total orange juice}}{\text{total volume}} \times 100.$$

This approach is correct because it follows the physical mixing process exactly. Its time complexity is $O(n)$, since each drink is processed once.

Looking closely at the formula reveals something simpler. If the same amount is taken from every drink, that amount appears in both the numerator and denominator and cancels out. What remains is just the arithmetic mean of all percentages:

$$\frac{p_1 + p_2 + \cdots + p_n}{n}.$$

The problem immediately becomes an averaging task. We only need the sum of all percentages and then divide by the number of drinks.

The brute-force simulation already runs fast enough for the given constraints, but the averaging observation removes unnecessary calculations and expresses the underlying mathematics directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`, the number of drinks.
2. Read the `n` percentage values.
3. Compute the sum of all percentages.
4. Divide the sum by `n` to obtain the average percentage.
5. Print the result as a floating-point number.

The only mathematical observation is that equal portions are taken from every drink. Because every drink contributes the same volume, the final concentration equals the average of the original concentrations.

### Why it works

Suppose Vasya takes `x` milliliters from each drink.

Drink `i` contributes

$$x \cdot \frac{p_i}{100}$$

milliliters of pure orange juice.

The total orange juice amount is

$$x \cdot \frac{p_1+p_2+\cdots+p_n}{100}.$$

The total cocktail volume is

$$nx.$$

The final percentage is

$$\frac{x \cdot \frac{p_1+p_2+\cdots+p_n}{100}}{nx}\times100 = \frac{p_1+p_2+\cdots+p_n}{n}.$$

The algorithm computes exactly this quantity, so it always returns the correct orange juice percentage.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
p = list(map(int, input().split()))

answer = sum(p) / n
print(answer)
```

The first line reads the number of drinks. The second line reads all percentages into a list.

The expression `sum(p)` computes the total percentage contribution from all drinks. Dividing by `n` gives the arithmetic mean, which is exactly the concentration of orange juice in the final cocktail.

Python automatically performs floating-point division when using `/`, so the result is printed with sufficient precision for the required error tolerance.

There are no tricky boundary conditions. Values may range from 0 to 100, and the maximum sum is only 10,000, which is far below any numeric limit.

## Worked Examples

### Example 1

Input:

```
3
50 50 100
```

| Step | Current Percentage | Running Sum |
| --- | --- | --- |
| Start | - | 0 |
| Read 50 | 50 | 50 |
| Read 50 | 50 | 100 |
| Read 100 | 100 | 200 |

Final computation:

$$200 / 3 = 66.666666666667$$

Output:

```
66.666666666667
```

This example shows that the final concentration is simply the average of all percentages.

### Example 2

Input:

```
2
0 100
```

| Step | Current Percentage | Running Sum |
| --- | --- | --- |
| Start | - | 0 |
| Read 0 | 0 | 0 |
| Read 100 | 100 | 100 |

Final computation:

$$100 / 2 = 50$$

Output:

```
50
```

This example demonstrates that drinks with 0% orange juice are handled naturally by the averaging formula.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each percentage is processed once while computing the sum |
| Space | O(1) | Only a few variables are needed beyond the input data |

With at most 100 drinks, the algorithm performs only a tiny amount of work. Both the time and memory usage are comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    n = int(input())
    p = list(map(int, input().split()))
    print(sum(p) / n)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert abs(float(run("3\n50 50 100\n")) - 66.666666666667) < 1e-6

# minimum size
assert abs(float(run("1\n0\n")) - 0.0) < 1e-6

# all equal values
assert abs(float(run("4\n25 25 25 25\n")) - 25.0) < 1e-6

# all maximum values
assert abs(float(run("5\n100 100 100 100 100\n")) - 100.0) < 1e-6

# mixture of extremes
assert abs(float(run("2\n0 100\n")) - 50.0) < 1e-6

# maximum n
assert abs(float(run("100\n" + " ".join(["100"] * 100) + "\n")) - 100.0) < 1e-6
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0` | `0` | Minimum input size |
| `4 / 25 25 25 25` | `25` | All values equal |
| `5 / 100 100 100 100 100` | `100` | Upper percentage boundary |
| `2 / 0 100` | `50` | Mixing extremes |
| `100` drinks all `100` | `100` | Maximum input size |

## Edge Cases

### Single Drink

Input:

```
1
73
```

Trace:

The sum of percentages is `73`. Dividing by `1` gives `73`.

Output:

```
73
```

With only one drink, the cocktail is identical to the original drink.

### All Percentages Are Zero

Input:

```
3
0 0 0
```

Trace:

The running sum remains `0`.

$$0 / 3 = 0$$

Output:

```
0
```

The algorithm correctly handles the absence of orange juice.

### All Percentages Are One Hundred

Input:

```
4
100 100 100 100
```

Trace:

The sum is `400`.

$$400 / 4 = 100$$

Output:

```
100
```

A mixture of pure orange juice drinks remains pure orange juice.

### Mixture of Extreme Values

Input:

```
2
0 100
```

Trace:

The sum is `100`.

$$100 / 2 = 50$$

Output:

```
50
```

This confirms that averaging percentages correctly models mixing equal amounts of the drinks.
