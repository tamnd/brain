---
title: "CF 200B - Drinks"
description: "We are given several drinks, and each drink already contains some percentage of orange juice. Vasya mixes the same amount from every drink into one large cocktail. The task is to compute the final percentage of orange juice in the mixture."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 200
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 126 (Div. 2)"
rating: 800
weight: 200
solve_time_s: 93
verified: true
draft: false
---

[CF 200B - Drinks](https://codeforces.com/problemset/problem/200/B)

**Rating:** 800  
**Tags:** implementation, math  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several drinks, and each drink already contains some percentage of orange juice. Vasya mixes the same amount from every drink into one large cocktail. The task is to compute the final percentage of orange juice in the mixture.

If one drink is 50% orange juice and another is 100%, taking equal amounts from both means the final concentration is simply the average of their percentages. The problem asks us to print that average as a floating-point number.

The constraints are very small. There are at most 100 drinks, and each percentage is between 0 and 100. Even an inefficient solution would run comfortably within the time limit, since processing 100 numbers takes almost no time. The real challenge is not performance, it is handling the arithmetic correctly and printing a floating-point result instead of accidentally truncating to an integer.

One easy mistake is using integer division. Consider this input:

```
2
0 100
```

The correct answer is:

```
50
```

If we divide using integer arithmetic in some languages, values like `1 / 2` may become `0`, producing the wrong result.

Another subtle case is when every drink has 0% juice:

```
3
0 0 0
```

The answer must still be:

```
0
```

A careless implementation that divides by the wrong quantity or forgets to initialize the sum properly could fail here.

A similar edge case happens when all drinks are pure juice:

```
4
100 100 100 100
```

The result must remain exactly `100`, because averaging identical values should never change them.

## Approaches

The most direct way to think about the problem is physically simulating the cocktail. Suppose we take `x` milliliters from every drink. If a drink has `p[i]` percent orange juice, then the amount of pure orange juice contributed by that drink is:

$$x \times \frac{p[i]}{100}$$

We could sum the pure juice from all drinks, compute the total volume `n * x`, and divide them to get the final percentage.

That brute-force reasoning is correct, but it introduces an unnecessary variable `x`. Since every drink contributes the same volume, the common factor cancels out. The cocktail percentage becomes simply the arithmetic mean of all percentages:

$$\frac{p_1 + p_2 + \dots + p_n}{n}$$

This observation removes all simulation details. We only need to sum the percentages and divide by the number of drinks.

Even though the constraints are tiny, this simplification matters because it turns the problem into a clean implementation exercise instead of a floating-point modeling problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`, the number of drinks.
2. Read the list of percentages.
3. Compute the sum of all percentages.

This gives the total percentage contribution from every drink before averaging.
4. Divide the sum by `n`.

Since equal amounts of every drink are mixed, the final concentration is exactly the average percentage.
5. Print the result as a floating-point number.

The judge allows a small error tolerance, so standard floating-point output is sufficient.

### Why it works

Every drink contributes the same volume to the cocktail. Because the contribution volumes are equal, each drink affects the final concentration equally. Averaging the percentages is mathematically identical to computing the ratio of total pure juice to total cocktail volume. The algorithm computes exactly that average, so the produced percentage is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
percentages = list(map(int, input().split()))

answer = sum(percentages) / n

print(answer)
```

The program starts by reading the number of drinks and the list of juice percentages.

The key computation is:

```
sum(percentages) / n
```

This calculates the arithmetic mean of the percentages. In Python 3, the `/` operator always performs floating-point division, so we automatically get a decimal answer when necessary.

The solution uses only constant extra memory besides the input list. There are no tricky boundary conditions because the constraints guarantee `n >= 1`, so division by zero cannot occur.

## Worked Examples

### Example 1

Input:

```
3
50 50 100
```

| Step | Current Value | Running Sum |
| --- | --- | --- |
| Start | - | 0 |
| Add first drink | 50 | 50 |
| Add second drink | 50 | 100 |
| Add third drink | 100 | 200 |

Final computation:

$$200 / 3 = 66.666666666667$$

Output:

```
66.666666666667
```

This trace shows that the algorithm simply accumulates all percentages and averages them. Equal mixing means every drink contributes equally to the result.

### Example 2

Input:

```
4
0 25 50 75
```

| Step | Current Value | Running Sum |
| --- | --- | --- |
| Start | - | 0 |
| Add first drink | 0 | 0 |
| Add second drink | 25 | 25 |
| Add third drink | 50 | 75 |
| Add fourth drink | 75 | 150 |

Final computation:

$$150 / 4 = 37.5$$

Output:

```
37.5
```

This example demonstrates that drinks with 0% juice still participate in the average and reduce the final concentration correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We process each drink exactly once |
| Space | O(1) | Only a few variables are used besides the input list |

With at most 100 drinks, the program runs instantly. The memory usage is negligible and easily fits within the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())
    percentages = list(map(int, input().split()))

    print(sum(percentages) / n)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run("3\n50 50 100\n") == "66.66666666666667", "sample 1"

# minimum size
assert run("1\n0\n") == "0.0", "single zero drink"

# all equal values
assert run("4\n25 25 25 25\n") == "25.0", "all equal percentages"

# boundary values
assert run("2\n0 100\n") == "50.0", "mixed extremes"

# maximum percentage
assert run("3\n100 100 100\n") == "100.0", "all pure juice"

# varied values
assert run("5\n10 20 30 40 50\n") == "30.0", "general averaging case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0` | `0.0` | Minimum input size |
| `4 / 25 25 25 25` | `25.0` | Averaging identical values |
| `2 / 0 100` | `50.0` | Correct floating-point averaging |
| `3 / 100 100 100` | `100.0` | Upper boundary percentages |
| `5 / 10 20 30 40 50` | `30.0` | General correctness |

## Edge Cases

Consider the case where every drink contains no orange juice:

```
3
0 0 0
```

The algorithm computes:

| Drink | Percentage | Running Sum |
| --- | --- | --- |
| 1 | 0 | 0 |
| 2 | 0 | 0 |
| 3 | 0 | 0 |

The final result is:

$$0 / 3 = 0$$

So the output is correctly:

```
0.0
```

Now consider the opposite extreme:

```
4
100 100 100 100
```

The running sum becomes `400`, and the algorithm computes:

$$400 / 4 = 100$$

The final cocktail is still pure orange juice, so the correct output is:

```
100.0
```

Finally, consider a case that exposes integer division mistakes:

```
2
0 100
```

The running sum is `100`, and:

$$100 / 2 = 50$$

Python uses floating-point division for `/`, so the program prints:

```
50.0
```

A language or implementation using integer division carelessly could incorrectly truncate intermediate values, but this solution handles the computation safely.
