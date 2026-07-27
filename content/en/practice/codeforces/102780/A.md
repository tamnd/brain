---
title: "CF 102780A - Green tea"
description: "I will provide the editorial as a complete standalone document. Edit The task is to choose how many spoonfuls of hot water and cold water to put into a mug so that the resulting mixture has a temperature of exactly 80 degrees."
date: "2026-07-28T03:32:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102780
codeforces_index: "A"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 19)"
rating: 0
weight: 102780
solve_time_s: 106
verified: true
draft: false
---

[CF 102780A - Green tea](https://codeforces.com/problemset/problem/102780/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
I will provide the editorial as a complete standalone document.

Edit

# Problem Understanding

The task is to choose how many spoonfuls of hot water and cold water to put into a mug so that the resulting mixture has a temperature of exactly 80 degrees. The hot water has temperature `t1`, the cold water has temperature `t2`, and the required output is the pair of volumes `v1` and `v2`. Among all possible pairs, we need the one using the smallest total number of spoonfuls.

The mixing rule says that the total heat after mixing must match the weighted average of the two temperatures. For this problem, that means:

`t1 * v1 + t2 * v2 = 80 * (v1 + v2)`

The constraints tell us that the hot water temperature is never below 80 and the cold water temperature is always below 80. The values are small enough that even checking many combinations would fit, but the equation has enough structure to solve it directly in constant time. There is no need for simulation or search.

The main edge cases come from temperatures that make one side of the mixture unnecessary or make the ratio very simple. If `t1` is already 80, the hot water alone already gives the required temperature. For input `80 20`, the correct output is `1 0`. A careless solution based only on the general ratio formula could divide by zero because `t1 - 80` becomes zero.

Another edge case is when the temperature differences are not coprime. For input `100 20`, the differences are `20` and `60`. The raw ratio is `v1 : v2 = 60 : 20`, but the smallest valid pair is `3 : 1`. A solution that does not reduce the fraction would output unnecessarily large values.

A third case is when the two temperature differences already have a common divisor larger than one but one side is close to the target. For input `81 79`, the required ratio is `1 : 1`, so the answer is `1 1`. Searching from only one side or using floating point calculations can introduce rounding mistakes here.

# Approaches

A straightforward approach is to try every possible pair of spoon counts. We can iterate over all `v1` and `v2` values from 0 to 1000, check whether the equation is satisfied, and keep the pair with the smallest sum. This is correct because every allowed answer is considered. The worst case checks about one million pairs, since there are roughly `1001 * 1001` combinations.

The brute force approach works for the given limits, but it hides the mathematical structure of the problem. If the allowed spoon counts became much larger, the number of combinations would grow quadratically and quickly become impractical.

The useful observation comes from rearranging the temperature equation:

`t1 * v1 + t2 * v2 = 80 * v1 + 80 * v2`

Moving terms gives:

`(t1 - 80) * v1 = (80 - t2) * v2`

The left side describes how much the hot water raises the temperature above 80, and the right side describes how much the cold water lowers it below 80. The two effects must balance exactly.

This gives a direct ratio between the two volumes. The hot water amount must be proportional to `80 - t2`, while the cold water amount must be proportional to `t1 - 80`. Reducing this ratio by the greatest common divisor gives the smallest possible integer solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1000²) | O(1) | Accepted for the given limits |
| Optimal | O(1) | O(1) | Accepted |

# Algorithm Walkthrough

1. Read the hot and cold water temperatures.
2. Check whether the hot water temperature is exactly 80. In this situation, adding any amount of cold water would only move the temperature away from the target, so one spoon of hot water and zero spoons of cold water is the smallest valid answer.
3. Compute the two temperature differences: `hot_difference = t1 - 80` and `cold_difference = 80 - t2`. These values represent how much each type of water changes the mixture temperature away from the target.
4. Find the greatest common divisor of the two differences. Dividing both values by this divisor reduces the ratio while keeping the balance equation true.
5. Output `cold_difference / gcd` as the amount of hot water and `hot_difference / gcd` as the amount of cold water. The values are placed this way because more cold water is needed when the cold water is far below 80, and more hot water is needed when the hot water is far above 80.

Why it works: Every valid mixture must satisfy the equation `(t1 - 80) * v1 = (80 - t2) * v2`. This means the two volumes must have the same ratio as the opposite temperature differences. The algorithm constructs exactly that ratio and divides by the greatest common divisor, producing the smallest positive integer pair that satisfies the equation. Since any other valid pair would be a multiple of this reduced pair, no smaller total volume can exist.

# Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t1, t2 = map(int, input().split())

    if t1 == 80:
        print(1, 0)
        return

    a = t1 - 80
    b = 80 - t2

    g = __import__("math").gcd(a, b)

    print(b // g, a // g)

if __name__ == "__main__":
    solve()
```

The first part handles the special case where the hot water is already at the target temperature. The general formula assumes that the hot water contributes a positive amount of heat above 80, so this case needs separate handling.

The variables `a` and `b` store the two deviations from the target temperature. The equation says that the hot water volume is connected to the cold water deviation, and the cold water volume is connected to the hot water deviation, which is why the final output uses them in reversed order.

The greatest common divisor is used to reduce the ratio. Without this reduction, the answer would still satisfy the equation but would not have the minimum possible total number of spoons.

All calculations use integers, so there are no floating point precision problems. The values are also far below Python's integer limits, so overflow is not a concern.

# Worked Examples

For the first sample, the input is:

```
100 20
```

The execution can be traced as follows.

| Step | t1 | t2 | hot_difference | cold_difference | gcd | Output |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | 100 | 20 | 20 | 60 |  |  |
| After gcd | 100 | 20 | 20 | 60 | 20 | 3 1 |

The hot water is 20 degrees above the target and the cold water is 60 degrees below it. The hot water needs to appear in the ratio of the cold water difference, giving `60 : 20`, which reduces to `3 : 1`.

For the second sample, the input is:

```
100 30
```

The execution is:

| Step | t1 | t2 | hot_difference | cold_difference | gcd | Output |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | 100 | 30 | 20 | 50 |  |  |
| After gcd | 100 | 30 | 20 | 50 | 10 | 5 2 |

The hot water raises the temperature by 20 degrees per spoon and the cold water lowers it by 50 degrees per spoon. Five spoons of hot water balance two spoons of cold water.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic operations and one greatest common divisor computation are performed. |
| Space | O(1) | The algorithm stores only a few integer variables. |

The constant-time solution easily fits the time limit and memory limit because it avoids any enumeration of possible spoon counts.

# Test Cases

```python
import sys
import io
import math

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    t1, t2 = map(int, sys.stdin.readline().split())

    if t1 == 80:
        ans = "1 0"
    else:
        a = t1 - 80
        b = 80 - t2
        g = math.gcd(a, b)
        ans = f"{b // g} {a // g}"

    sys.stdin = old_stdin
    return ans

assert solve_data("100 20\n") == "3 1", "sample 1"
assert solve_data("100 30\n") == "5 2", "sample 2"

assert solve_data("80 0\n") == "1 0", "target hot water boundary"
assert solve_data("100 79\n") == "1 20", "small cold difference"
assert solve_data("81 79\n") == "1 1", "equal temperature differences"
assert solve_data("100 0\n") == "4 1", "maximum temperature range"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `80 0` | `1 0` | Checks the special case where hot water is already at the target. |
| `100 79` | `1 20` | Checks a case where a large amount of cold water is needed. |
| `81 79` | `1 1` | Checks the smallest non-special balanced ratio. |
| `100 0` | `4 1` | Checks the largest possible temperature difference. |

# Edge Cases

For input `80 20`, the algorithm immediately detects that the hot water temperature equals the desired temperature. It outputs `1 0`, because one spoon of hot water alone creates an 80 degree mixture. A formula-only implementation could fail here because the hot temperature difference is zero.

For input `100 20`, the algorithm computes `hot_difference = 20` and `cold_difference = 60`. The greatest common divisor is 20, so the reduced ratio is `60 / 20 = 3` and `20 / 20 = 1`. The output is `3 1`, which uses the minimum number of spoons.

For input `81 79`, the algorithm computes `hot_difference = 1` and `cold_difference = 1`. Their greatest common divisor is 1, so no reduction is needed. The output `1 1` shows that equal distance from the target requires equal amounts of both waters.

This editorial can also be adapted into a shorter Codeforces-style explanation or expanded into a more formal proof-based version.
