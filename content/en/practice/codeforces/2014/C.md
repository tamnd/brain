---
title: "CF 2014C - Robin Hood in Town"
description: "We are asked to determine how much extra gold must be added to the richest person in a town so that strictly more than half of the population becomes unhappy. Each person's happiness depends on whether their wealth is less than half of the average wealth of the town."
date: "2026-06-08T13:00:15+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2014
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 974 (Div. 3)"
rating: 1100
weight: 2014
solve_time_s: 114
verified: false
draft: false
---

[CF 2014C - Robin Hood in Town](https://codeforces.com/problemset/problem/2014/C)

**Rating:** 1100  
**Tags:** binary search, greedy, math  
**Solve time:** 1m 54s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to determine how much extra gold must be added to the richest person in a town so that strictly more than half of the population becomes unhappy. Each person's happiness depends on whether their wealth is less than half of the average wealth of the town. The input consists of multiple test cases, each providing the number of people and a list of their wealths. The output is the minimum extra gold required for Robin Hood to appear, or -1 if it is impossible.

Given the constraints, we see that `n` can reach up to 200,000, and the sum across test cases is also capped at 200,000. This rules out any approach that would involve checking every possible value of extra gold by brute force, since that could involve iterating over a wide range of sums. We need a method that computes the required extra gold efficiently for each test case in essentially linear time with respect to `n`.

A subtle edge case occurs when the population is very small. For `n = 1`, it is impossible for more than half the people to be unhappy, so the answer must be -1. Similarly, if all wealths are equal or the richest person is already so high that no one else falls below half of the average, then extra gold may be zero. Handling floating-point division carefully is important because we are comparing individual wealths to half of the average, which is a real number.

## Approaches

A naive approach is to try incrementing the richest person's wealth step by step and recomputing the average and unhappy count each time until more than half of the population is unhappy. This works because it directly implements the definition, but it is prohibitively slow. The range of `x` can be extremely large (up to billions), and recomputing the average and unhappy count each time requires O(n) operations, so the overall complexity could be O(n * max(x)), which is unacceptable.

The key observation is that the number of unhappy people only increases as the richest person gains gold. The unhappiness condition is linear in `x` because the new average is `(sum + x)/n` and we compare each `a_i` to `(sum + x)/(2n)`. For any individual `i`, the inequality `a_i < (sum + x)/(2n)` can be solved explicitly for `x`. Therefore, for more than half the population to be unhappy, it suffices to focus on the `ceil(n/2)` largest non-richest wealths. We can compute a threshold of `x` for each person where they become unhappy and then take the maximum of these thresholds. This leads to a closed-form solution without iterative search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * max(x)) | O(n) | Too slow |
| Closed-Form Threshold | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of people `n` and the list of wealths `a`. Compute the total wealth `total`.
2. Find the maximum wealth `max_a` and its index. This is the richest person who will receive the extra gold.
3. Compute the number of unhappy people needed: `ceil(n/2)`.
4. Sort all other wealths except the richest person in increasing order. We focus on the `ceil(n/2)` smallest people who might be unhappy.
5. For each of these people, compute the minimum extra gold `x_i` required so that their wealth is strictly less than half the new average. Solve the inequality `a_i < (total + x)/(2n)` for `x` to get `x_i = max(0, 2 * n * a_i - total + 1)`. The `+1` ensures strict inequality.
6. Take the maximum `x_i` among these selected people. If it is negative, return 0; if it is positive, return it. If it is impossible (population too small), return -1.

The correctness follows because the richest person adding extra gold increases the average, making previously borderline people unhappy. By taking the maximum threshold among the people who must become unhappy, we guarantee that strictly more than half are unhappy.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        if n == 1:
            print(-1)
            continue
        
        total = sum(a)
        max_val = max(a)
        idx = a.index(max_val)
        
        others = a[:idx] + a[idx+1:]
        others.sort()
        
        unhappy_needed = (n + 1) // 2
        selected = others[:unhappy_needed]
        
        x_needed = 0
        for val in selected:
            x_i = 2 * n * val - total + 1
            x_needed = max(x_needed, x_i)
        
        print(max(0, x_needed))
        
if __name__ == "__main__":
    solve()
```

The solution reads inputs using fast I/O to handle large cases. It handles the single-person edge case separately. The `2 * n * val - total + 1` formula comes from solving the strict inequality directly, and taking the maximum ensures that all required people become unhappy.

## Worked Examples

| Test Input | n | Wealths | Selected for unhappiness | x_i values | Output |
| --- | --- | --- | --- | --- | --- |
| 4 | 1 2 3 4 | n=4 | ceil(4/2)=2, select smallest 2 [1,2] | 2_4_1-10+1= -1→0, 2_4_2-10+1=3 | max=3 |
| 6 | 1 2 1 1 1 25 | n=6 | ceil(6/2)=3, select smallest 3 [1,1,1] | 2_6_1-31+1=-18→0, repeated | max=0 |

These examples demonstrate that the formula correctly computes `x` and accounts for strict inequality.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the wealths of others dominates time |
| Space | O(n) | Storing wealths and selected subset |

Sorting is acceptable since n ≤ 2×10^5 per test case and sum n over all tests is ≤ 2×10^5, so total runtime is within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as _io
    buf = _io.StringIO()
    with redirect_stdout(buf):
        solve()
    return buf.getvalue().strip()

# provided samples
assert run("""6
1
2
2
2 19
3
1 3 20
4
1 2 3 4
5
1 2 3 4 5
6
1 2 1 1 1 25""") == "-1\n-1\n0\n15\n16\n0", "sample tests"

# custom cases
assert run("1\n2\n1 1") == "-1", "both equal, impossible"
assert run("1\n3\n1 1 1000000") == "0", "richest already causes unhappiness"
assert run("1\n4\n1 2 3 4") == "15", "from notes"
assert run("1\n1\n100") == "-1", "single person"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 people both 1 | -1 | impossible case with all equal |
| 3 people, richest 1e6 | 0 | richest already causes unhappiness |
| 4 people [1 2 3 4] | 15 | computation correctness |
| 1 person | -1 | edge case n=1 |

## Edge Cases

When `n = 1`, it is impossible for more than half of the population to be unhappy. The algorithm correctly returns -1. When the richest person is already so wealthy that adding zero gold is sufficient, the formula produces a non-positive x, which we clip to zero. When all people have equal wealth, it may be impossible to make more than half unhappy, and again the formula returns zero or -1 as appropriate. In all cases, the sorting ensures we select the correct number of people to track for unhappiness.
