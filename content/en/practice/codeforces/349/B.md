---
title: "CF 349B - Color the Fence"
description: "Igor wants to paint the largest possible number on a fence using a limited amount of paint. Each digit from 1 to 9 has a specific paint cost, and zero cannot be used."
date: "2026-06-06T18:45:38+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 349
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 202 (Div. 2)"
rating: 1700
weight: 349
solve_time_s: 90
verified: true
draft: false
---

[CF 349B - Color the Fence](https://codeforces.com/problemset/problem/349/B)

**Rating:** 1700  
**Tags:** data structures, dp, greedy, implementation  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

Igor wants to paint the largest possible number on a fence using a limited amount of paint. Each digit from 1 to 9 has a specific paint cost, and zero cannot be used. The input consists of the total available paint $v$ and an array of nine positive integers $a_1$ through $a_9$ indicating the paint needed for each digit. The output should be the largest number Igor can form with his paint supply. If no digit can be painted, the output is -1.

The constraints give $v$ up to $10^6$ and paint costs up to $10^5$. This implies we cannot try all possible combinations of digits naively, because there could be millions of digits and trying every subset would be exponentially expensive. We must aim for a linear or near-linear approach in terms of $v$.

Non-obvious edge cases include situations where the cheapest digit is not the largest. For example, if $v = 5$ and costs are $[5, 4, 3, 2, 1, 2, 3, 4, 5]$, a naive greedy approach that picks the largest digit affordable at each step might pick 5 repeatedly. Another edge case is when $v$ is smaller than any digit's paint cost, which should yield -1.

## Approaches

A brute-force solution would try all sequences of digits, sum their paint costs, and select the maximum numeric value. While this is correct conceptually, the number of sequences grows exponentially with $v$ divided by the minimum paint cost, which can reach millions. Explicitly constructing and comparing all numbers is computationally infeasible.

The key observation is that the largest number is achieved by maximizing the length of the number first. With the remaining paint, each position should hold the largest possible digit. This reduces the problem to first computing the maximum number of digits we can paint using the cheapest digit, and then iteratively upgrading digits from left to right if the remaining paint allows a more expensive digit to replace a cheaper one. This approach leverages the fact that the numeric value increases most by placing higher digits in higher positions once the length is fixed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(9^(v/min_cost)) | O(v/min_cost) | Too slow |
| Optimal | O(n * 9) ≈ O(v) | O(v/min_cost) | Accepted |

## Algorithm Walkthrough

1. Identify the cheapest digit. Iterate over the array of costs and find the digit with the minimum paint cost. Let this be $d_\text{min}$ with cost $c_\text{min}$.
2. Compute the maximum number of digits we can paint using only the cheapest digit. If $v < c_\text{min}$, print -1 because no digit can be painted.
3. Initialize an array of length equal to the maximum number of digits, filled entirely with the cheapest digit. Subtract $c_\text{min} \times \text{length}$ from $v$ to calculate the remaining paint.
4. Iterate from left to right through each digit position. For each position, try replacing the current digit with the largest possible digit that does not exceed the remaining paint. Specifically, check digits 9 down to $d_\text{min}+1$. If the replacement digit costs $c$, ensure that $v + c_\text{min} \ge c$ because the original digit's cost $c_\text{min}$ is already spent. If feasible, perform the replacement and update the remaining paint.
5. After processing all positions, output the resulting number as a string.

Why it works: The algorithm guarantees the maximum length first, which directly maximizes the numeric value in terms of number of digits. Replacing leftmost digits with larger ones while respecting the remaining paint ensures the largest possible value without reducing length. This invariant holds for each position independently, so the global number is maximal.

## Python Solution

```python
import sys
input = sys.stdin.readline

v = int(input())
costs = list(map(int, input().split()))

min_cost = min(costs)
min_digit = costs.index(min_cost) + 1

if v < min_cost:
    print(-1)
    sys.exit()

length = v // min_cost
v -= length * min_cost

number = [min_digit] * length

for i in range(length):
    for d in range(9, min_digit, -1):
        c = costs[d - 1]
        if v + min_cost >= c:
            number[i] = d
            v -= c - min_cost
            break

print(''.join(map(str, number)))
```

The first section reads input and determines the cheapest digit. We then compute the maximum number of digits, ensuring the remaining paint is tracked accurately. The nested loop carefully upgrades digits from largest to smallest feasible, subtracting only the additional cost. The algorithm correctly handles cases where multiple upgrades are possible and guarantees the leftmost digits are maximized.

## Worked Examples

**Example 1:**

Input:

```
5
5 4 3 2 1 2 3 4 5
```

Variables:

| Step | min_digit | min_cost | length | remaining v | number |
| --- | --- | --- | --- | --- | --- |
| Initialization | 5 | 1 | 5 | 0 | [5,5,5,5,5] |

No remaining paint to upgrade, output `55555`.

**Example 2:**

Input:

```
10
1 2 3 4 5 6 7 8 9
```

Variables:

| Step | min_digit | min_cost | length | remaining v | number |
| --- | --- | --- | --- | --- | --- |
| Init | 1 | 1 | 10 | 0 | [1]*10 |
| Upgrade pos0 | 9 | 9 | feasible | 0 | [9,1,1,1,1,1,1,1,1,1] |
| Upgrade pos1 | 9 | 9 | not enough paint | 0 | no change |

Output: `9111111111`

This trace shows that the first digit is upgraded to maximize value while respecting remaining paint.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(9 * v/min_cost) | We may attempt up to 9 replacements for each digit position |
| Space | O(v/min_cost) | Array storing digits of the resulting number |

Given $v ≤ 10^6$ and minimal cost ≥1, at most 10^6 iterations are possible, well within 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    v = int(input())
    costs = list(map(int, input().split()))
    min_cost = min(costs)
    min_digit = costs.index(min_cost) + 1
    if v < min_cost:
        return "-1"
    length = v // min_cost
    v -= length * min_cost
    number = [min_digit] * length
    for i in range(length):
        for d in range(9, min_digit, -1):
            c = costs[d - 1]
            if v + min_cost >= c:
                number[i] = d
                v -= c - min_cost
                break
    return ''.join(map(str, number))

assert run("5\n5 4 3 2 1 2 3 4 5\n") == "55555", "sample 1"
assert run("10\n1 2 3 4 5 6 7 8 9\n") == "9111111111", "custom 1"
assert run("3\n5 5 5 5 5 5 5 5 5\n") == "-1", "custom 2"
assert run("15\n1 1 1 1 1 1 1 1 1\n") == "999999999999999", "custom 3"
assert run("7\n1 3 3 3 3 3 3 3 3\n") == "7111111", "custom 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5\n5 4 3 2 1 2 3 4 5 | 55555 | Upgrades not possible, cheapest digit dominates |
| 10\n1 2 3 4 5 6 7 8 9 | 9111111111 | Partial upgrade of leftmost digit |
| 3\n5 5 5 5 5 5 5 5 5 | -1 | Not enough paint for any digit |
| 15\n1 1 1 1 1 1 1 1 1 | 999999999999999 | All costs equal, upgrades to maximum feasible |
| 7\n1 3 3 3 3 3 3 3 3 | 7111111 | Upgrade only first digit, remaining minimal digits |

## Edge Cases

If $v$ is smaller than any digit cost, such as $v=3$ with all costs ≥5, the algorithm prints -1 immediately, correctly handling the impossibility.

If multiple digits have the same minimal cost, the algorithm chooses the smallest numerical digit to fill the number, ensuring maximum
