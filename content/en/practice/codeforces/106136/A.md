---
title: "CF 106136A - Golden Alleyway"
description: "We are given a small ICPC team and a record of how many medals the team wins in a contest. Each gold, silver, and bronze medal corresponds to a fixed prize pool: gold is worth 7500 yuan per team, silver is 3000 yuan per team, and bronze is 1500 yuan per team."
date: "2026-06-20T02:15:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106136
codeforces_index: "A"
codeforces_contest_name: "East China University of Science and Technology Programming Contest 2025"
rating: 0
weight: 106136
solve_time_s: 41
verified: true
draft: false
---

[CF 106136A - Golden Alleyway](https://codeforces.com/problemset/problem/106136/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small ICPC team and a record of how many medals the team wins in a contest. Each gold, silver, and bronze medal corresponds to a fixed prize pool: gold is worth 7500 yuan per team, silver is 3000 yuan per team, and bronze is 1500 yuan per team. The team can have at most three members, and whatever total prize money the team earns is divided equally among all members.

The task is to compute the amount of money one specific member receives, given the team size and the counts of each medal type.

The input contains four integers: the team size, followed by the number of gold, silver, and bronze medals. The output is a single integer representing one member’s share of the total prize money.

The constraints are extremely small. The team size is at most 3, and the total number of medals is at most 7. This immediately rules out any need for optimization techniques or even careful data structures. Every operation is constant-time arithmetic.

Because all values are integers and divisions are exact by construction (the total prize is always divisible by team size in the intended interpretation), the main pitfall is simply implementing the arithmetic correctly without losing precision or mixing up division order.

A few edge cases still deserve attention.

One edge case is when there are no medals at all. For example, input `2 0 0 0` should yield `0`, since the total prize is zero.

Another is the smallest possible team size. For example, `1 1 0 0` should return the full gold prize of 7500, since nothing is split.

A third is when the prize does not divide evenly if computed incorrectly due to premature integer division. For example, if one mistakenly divides each medal prize individually per person before summing, floating-point or truncation errors could appear. The correct approach is to compute total prize first, then divide once.

## Approaches

A brute-force interpretation is almost unnecessary here, but we can still describe it as simulating each medal event and accumulating prize per team member. For each gold medal, we would add 7500 to a running total, each silver adds 3000, and each bronze adds 1500, then finally divide by team size.

Even if we incorrectly thought of distributing each medal reward across members immediately, the worst-case operation count is still bounded by the number of medals, which is at most 7. So even a literal simulation of every medal event is trivial.

The key observation is that the problem is purely additive and linear. The order in which medals are processed does not matter, and there are no interactions between medals. This reduces everything to computing a weighted sum and dividing once at the end.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Simulation | O(g + s + b) | O(1) | Accepted |
| Direct Formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the four integers representing team size and counts of gold, silver, and bronze medals. This establishes all inputs needed for the computation in a single step.
2. Compute the total prize earned by the team as a weighted sum: each gold contributes 7500, each silver contributes 3000, and each bronze contributes 1500. This step collapses the entire contest history into a single scalar value, which is valid because each medal contributes independently.
3. Divide the total prize by the team size. Since the team splits winnings equally, this produces the amount each member receives.
4. Output the result as an integer.

### Why it works

The prize system is linear with respect to medal counts. Each medal contributes a fixed independent amount to the total reward, and the splitting operation is applied once to the final sum. Because division is applied after summation, distributivity ensures the result is equivalent to distributing each medal reward equally among members and then summing. This guarantees that no ordering or grouping effects can change the final answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, g, s, b = map(int, input().split())

total = g * 7500 + s * 3000 + b * 1500
print(total // n)
```

The solution reads the input in one line and immediately unpacks the four integers. The total prize is computed using direct multiplication of counts by their respective values, which avoids any loops.

The division is done at the very end using integer division. This is safe because all prize values are multiples of 500 and the division is intended to be exact under the problem’s definition. Using `//` ensures we remain in integer arithmetic, avoiding floating-point issues.

A common mistake would be to divide each medal contribution separately before summing. That would still work mathematically here, but it introduces unnecessary risk of rounding errors in more general problems and obscures the intended structure.

## Worked Examples

### Example 1

Input: `3 2 1 2`

We compute the total prize step by step.

| Step | Gold | Silver | Bronze | Total calculation | Total |
| --- | --- | --- | --- | --- | --- |
| Init | 2 | 1 | 2 | - | 0 |
| After gold | 2 | 1 | 2 | 2 × 7500 | 15000 |
| After silver | 2 | 1 | 2 | + 1 × 3000 | 18000 |
| After bronze | 2 | 1 | 2 | + 2 × 1500 | 21000 |

Now divide by team size 3: 21000 ÷ 3 = 7000.

This trace confirms that aggregation before division matches the intended equal splitting of total earnings.

### Example 2

Input: `1 0 0 4`

| Step | Gold | Silver | Bronze | Total calculation | Total |
| --- | --- | --- | --- | --- | --- |
| Init | 0 | 0 | 4 | - | 0 |
| After bronze | 0 | 0 | 4 | 4 × 1500 | 6000 |

Divide by team size 1: 6000 ÷ 1 = 6000.

This case confirms that the formula naturally handles single-member teams without any special logic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations regardless of input |
| Space | O(1) | No auxiliary data structures are used |

The constraints are extremely small, so even a more verbose implementation would comfortably fit within limits. The direct formula approach is optimal and executes in constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    n, g, s, b = map(int, input().split())
    total = g * 7500 + s * 3000 + b * 1500
    return str(total // n)

# provided samples
assert run("3 2 1 2") == "7000", "sample 1"
assert run("1 0 0 4") == "6000", "sample 2"

# custom cases
assert run("1 0 0 0") == "0", "no medals"
assert run("3 0 0 0") == "0", "team with no reward"
assert run("2 1 1 1") == str((7500 + 3000 + 1500)//2), "mixed medals"
assert run("3 7 0 0") == str((7*7500)//3), "max gold case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 0 0 | 0 | zero reward edge case |
| 3 0 0 0 | 0 | no medals with team splitting |
| 2 1 1 1 | 6000 | mixed medal aggregation |
| 3 7 0 0 | 17500 | maximum gold boundary |

## Edge Cases

For the input `3 0 0 0`, the algorithm computes total prize as zero and divides by three, producing zero. This confirms that the division step does not introduce artifacts when the numerator is zero.

For `1 0 0 4`, the computation yields 6000 before division. Since team size is one, division leaves the value unchanged, confirming correctness for minimal team size.

For `3 7 0 0`, total prize is `7 × 7500 = 52500`, and division yields `17500`. This demonstrates that the algorithm handles maximum medal counts without overflow concerns in Python and correctly applies integer division at the end.
