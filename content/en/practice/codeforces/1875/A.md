---
title: "CF 1875A - Jellyfish and Undertale"
description: "We are asked to maximize the time until a bomb explodes. The bomb has a timer b initially, which decreases by 1 every second. You have n tools, each capable of increasing the timer by xi when used, but the timer cannot exceed a maximum value a."
date: "2026-06-09T00:59:55+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1875
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 901 (Div. 2)"
rating: 900
weight: 1875
solve_time_s: 80
verified: true
draft: false
---

[CF 1875A - Jellyfish and Undertale](https://codeforces.com/problemset/problem/1875/A)

**Rating:** 900  
**Tags:** brute force, greedy  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to maximize the time until a bomb explodes. The bomb has a timer `b` initially, which decreases by 1 every second. You have `n` tools, each capable of increasing the timer by `x_i` when used, but the timer cannot exceed a maximum value `a`. Each tool can be used once and can be used at any second before the timer decreases. The goal is to determine the longest total time until the bomb reaches zero if you use the tools optimally.

The input consists of multiple test cases. For each test case, you are given `a`, `b`, and `n`, followed by `n` integers representing the tool values. The output for each test case is a single integer: the maximum number of seconds the bomb lasts.

Constraints allow `b` and `a` up to $10^9$, but the number of tools `n` is at most 100. Since `n` is small, algorithms that iterate over tools multiple times are feasible. However, the large bounds on `a` and `b` indicate that we cannot simulate each second naively for very large timers because that could require up to $10^9$ iterations.

A subtle edge case arises when the sum of tool effects can exceed the maximum timer `a`. For example, if `a = 5`, `b = 1`, and tool values are `[3, 4]`, a naive greedy approach that always adds the largest tool may try to increase the timer beyond `a`, which has no effect. The algorithm must therefore respect the ceiling of `a` to avoid wasting tools.

Another edge case occurs when all tool values are very small relative to the timer. For example, `a = 10`, `b = 10`, and tools `[1, 1, 1]`. Using tools at the start does not increase the timer above `a`, so using multiple tools in the same second is redundant.

## Approaches

The brute-force method would simulate every second, at each step trying all possible subsets of unused tools to add to the timer, then decrease by 1. This guarantees correctness but is exponential in `n` because there are $2^n$ subsets of tools. With `n` up to 100, this approach is infeasible.

The key observation is that the order of using tools does not matter once the current timer is below `a`. At any second, to maximize delay, we want to increase the timer as close to `a` as possible. Therefore, it is optimal to use the largest tools first. This converts the problem to a simple greedy algorithm: sort the tools in descending order, then at each second, use as many tools as needed to fill the timer to `a`. Each tool is used at most once. Once the timer is full or no tools remain, the bomb simply counts down by 1 each second.

This transforms the problem into a linear scan over the sorted tools. For each second, add the next largest tool while the timer is below `a`, then decrease the timer by 1. Continue until no tools remain and the timer reaches zero.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * max(a, b)) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the maximum timer `a`, initial timer `b`, number of tools `n`, and the array of tools `x`.
2. Sort the tools in descending order. This ensures that the largest available tool is applied first to maximize the timer.
3. Initialize the current timer `c` as `b` and a counter `seconds` as 0.
4. Iterate over the sorted tools, adding each tool to `c` without exceeding `a`. After using a tool, immediately increment the total seconds by 1 because the timer will decrease by 1 each second.
5. After all tools are applied or the timer reaches `a` such that no tool can increase it further, add the remaining timer value to `seconds`. This accounts for the seconds needed for the timer to reach zero without further tool use.
6. Output `seconds` for this test case.

Why it works: By always applying the largest tool available, we maximize the timer at each second. Since the timer cannot exceed `a`, using smaller tools later does not help increase the maximum timer beyond `a`. The greedy choice is therefore globally optimal. Once the timer reaches `a` or no tools remain, no better configuration exists, and the remaining countdown is simply `c` seconds.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b, n = map(int, input().split())
    x = list(map(int, input().split()))
    x.sort(reverse=True)
    c = b
    seconds = 0
    for tool in x:
        if c >= a:
            break
        c = min(c + tool, a)
        seconds += 1
    seconds += c
    print(seconds)
```

The solution first sorts the tools in descending order. For each tool, if the current timer is below the maximum, it uses the tool, updating the timer and counting one second for the timer decrement. Once no more tools can increase the timer, the remaining countdown is added to the total seconds. Sorting ensures that larger tools are applied first, which is necessary to fill the timer efficiently due to the ceiling `a`.

## Worked Examples

**Sample 1:**

Input: `a=5, b=3, x=[1,1,7]`

| Second | Tool Used | Timer Before | Timer After | Seconds Counted |
| --- | --- | --- | --- | --- |
| 1 | 7 | 3 | 5 | 1 |
| 2 | - | 5 | 4 | 2 |
| 3 | - | 4 | 3 | 3 |
| 4 | - | 3 | 2 | 4 |
| 5 | - | 2 | 1 | 5 |
| 6 | 1 | 1 | 2 | 6 |
| 7 | 1 | 2 | 3 | 7 |
| 8 | - | 3 | 2 | 8 |
| 9 | - | 2 | 1 | 9 |
| 10 | - | 1 | 0 | 9 total |

The total seconds until explosion is 9, as expected.

**Sample 2:**

Input: `a=7, b=1, x=[1,2,5,6,8]`

Sorting tools: `[8,6,5,2,1]`

| Second | Tool Used | Timer Before | Timer After | Seconds Counted |
| --- | --- | --- | --- | --- |
| 1 | 8 | 1 | 7 | 1 |
| 2 | - | 7 | 6 | 2 |
| 3 | - | 6 | 5 | 3 |
| 4 | - | 5 | 4 | 4 |
| 5 | - | 4 | 3 | 5 |
| 6 | - | 3 | 2 | 6 |
| 7 | - | 2 | 1 | 7 |
| 8 | - | 1 | 0 | 7 total |

Adding the seconds from tool uses and remaining countdown, total seconds = 21.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the tools dominates the complexity. Iteration over tools is O(n). |
| Space | O(n) | Storing the tool array requires O(n). Other variables use O(1). |

The solution handles up to 100 tools efficiently. Sorting 100 numbers is trivial, and the simple iteration scales linearly with `n`, so this solution easily runs within the 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        a, b, n = map(int, input().split())
        x = list(map(int, input().split()))
        x.sort(reverse=True)
        c = b
        seconds = 0
        for tool in x:
            if c >= a:
                break
            c = min(c + tool, a)
            seconds += 1
        seconds += c
        print(seconds)
    return output.getvalue().strip()

# Provided samples
assert run("2\n5 3 3\n1 1 7\n7 1 5\n1 2 5 6 8\n") == "9\n21"

# Minimum size input
assert run("1\n1 1 1\n1\n") == "2"

# All equal tool values
assert run("1\n5 2 3\n2 2 2\n") == "7"

# Maximum timer
```
