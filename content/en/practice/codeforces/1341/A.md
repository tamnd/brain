---
title: "CF 1341A - Nastya and Rice"
description: "We are given several independent scenarios about a bag of rice grains. In each scenario, there are two layers of uncertainty: the weight of each individual grain and the total weight of all grains together."
date: "2026-06-15T04:39:36+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1341
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 637 (Div. 2) - Thanks, Ivan Belonogov!"
rating: 900
weight: 1341
solve_time_s: 77
verified: true
draft: false
---

[CF 1341A - Nastya and Rice](https://codeforces.com/problemset/problem/1341/A)

**Rating:** 900  
**Tags:** math  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent scenarios about a bag of rice grains. In each scenario, there are two layers of uncertainty: the weight of each individual grain and the total weight of all grains together.

Each grain is known to have an integer weight lying in a symmetric interval around some average value. Separately, the total weight of all grains is also constrained to lie in another symmetric interval. The question is whether there exists any assignment of integer weights to all grains such that every grain respects its own allowed range and the sum of all grains lands inside the allowed total range.

We are not asked to construct the weights, only to decide whether such a configuration is logically possible.

The constraints are small per test case, with up to 1000 grains and up to 1000 test cases. This immediately suggests that any solution must be constant time per test case, since even linear scanning per case would already reach about 10^6 operations, which is still fine, but anything involving nested reasoning over distributions would be unnecessary and overkill.

A subtle pitfall comes from thinking only about averages. A naive idea is to compare the average grain weight range with the average implied by the total interval. This is incorrect because the total constraint is on the sum, not on per-grain averages, and the extremal configurations matter.

Another potential mistake is treating bounds independently without scaling. The total range scales with n, but a careless implementation might forget to multiply per-grain bounds, leading to incorrect feasibility checks.

## Approaches

The brute-force interpretation would be to try all possible assignments of grain weights within their allowed ranges and check whether any assignment produces a sum within the required interval. Even for a single test case, each grain has up to a range of roughly 2001 possible values, so the number of combinations is on the order of $(2001)^n$, which is completely infeasible even for very small n. The structure of the problem suggests we do not need to examine individual assignments.

The key observation is that we do not care about the exact distribution of weights, only the possible range of the sum. Since each grain is independent and contributes additively, the minimum possible total sum is achieved when every grain takes its minimum value, and the maximum possible total sum is achieved when every grain takes its maximum value. This turns the entire problem into checking whether two intervals overlap: the achievable sum interval and the required total interval.

Once we compute the achievable sum range, feasibility reduces to checking whether these two intervals intersect.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Interval reasoning | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

For each test case, we proceed in a small number of deterministic steps.

1. Compute the minimum possible weight of a single grain as $a - b$. This is the smallest allowed value per grain.
2. Compute the maximum possible weight of a single grain as $a + b$. This is the largest allowed value per grain.
3. Multiply both by $n$ to get the minimum and maximum possible total weights: $S_{\min} = n(a - b)$ and $S_{\max} = n(a + b)$. This step is justified because each grain contributes independently and we can choose each grain at its extreme to push the sum.
4. Compute the allowed total weight interval from the input as $[c - d, c + d]$.
5. Check whether these two intervals intersect. Concretely, we verify that the maximum achievable sum is at least the minimum allowed total, and the minimum achievable sum is at most the maximum allowed total.
6. If both conditions hold, output "Yes"; otherwise output "No".

### Why it works

The sum of independent bounded variables always attains its extrema by pushing every variable to its own extremum. Any deviation from choosing all minimums increases the sum, and any deviation from choosing all maximums decreases the sum, so no intermediate configuration can expand the reachable interval beyond $[n(a-b), n(a+b)]$. Therefore the problem reduces exactly to checking whether this reachable interval overlaps the required interval, which is both necessary and sufficient for feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, a, b, c, d = map(int, input().split())
    
    min_sum = n * (a - b)
    max_sum = n * (a + b)
    
    low = c - d
    high = c + d
    
    if max_sum >= low and min_sum <= high:
        print("Yes")
    else:
        print("No")
```

The implementation directly follows the derived interval reasoning. The key detail is correctly scaling both endpoints of the per-grain interval by n. A frequent mistake is to compare $a-b$ and $a+b$ directly with the total bounds without multiplying, which ignores aggregation.

The overlap condition is symmetric: either endpoint can validate feasibility, but both must be checked to ensure the intervals intersect rather than one strictly containing the other.

## Worked Examples

We trace two sample cases to see how the interval comparison behaves.

### Example 1

Input: `7 20 3 101 18`

| Step | min grain | max grain | min sum | max sum | total interval | result |
| --- | --- | --- | --- | --- | --- | --- |
| Compute | 17 | 23 | 119 | 161 | [83, 119] | Yes |

The achievable sum range is [119, 161], while the required range is [83, 119]. The intervals touch at 119, so feasibility holds exactly at the boundary case where all grains take the minimum value.

### Example 2

Input: `11 11 10 234 2`

| Step | min grain | max grain | min sum | max sum | total interval | result |
| --- | --- | --- | --- | --- | --- | --- |
| Compute | 1 | 21 | 11 | 231 | [232, 236] | No |

Here the maximum possible sum is 231, but the required interval starts at 232. Even the most favorable configuration cannot reach the required total.

These examples show that boundary touching is valid and strict separation causes failure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case uses constant arithmetic operations |
| Space | O(1) | No auxiliary structures proportional to input size |

The solution comfortably fits the constraints since even 1000 test cases only require a few arithmetic operations each.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    
    t = int(input())
    out = []
    for _ in range(t):
        n, a, b, c, d = map(int, input().split())
        min_sum = n * (a - b)
        max_sum = n * (a + b)
        low = c - d
        high = c + d
        out.append("Yes" if (max_sum >= low and min_sum <= high) else "No")
    return "\n".join(out)

# provided samples
assert run("""5
7 20 3 101 18
11 11 10 234 2
8 9 7 250 122
19 41 21 321 10
3 10 8 6 1
""") == """Yes
No
Yes
No
Yes"""

# minimum case
assert run("1\n1 2 1 1 0\n") == "Yes"

# impossible small case
assert run("1\n1 10 1 5 0\n") == "No"

# tight boundary overlap
assert run("1\n2 5 1 9 1\n") == "Yes"

# large n edge
assert run("1\n1000 1000 0 1000000 0\n") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single grain overlap | Yes | minimum boundary correctness |
| single grain impossible | No | non-overlap detection |
| tight overlap | Yes | boundary intersection handling |
| large n | Yes | scaling correctness |

## Edge Cases

One important edge case occurs when the intervals touch exactly at one point. For example, if the maximum achievable sum equals the minimum required sum, the correct answer is still "Yes". The algorithm handles this because the condition uses non-strict inequalities, ensuring boundary feasibility is accepted.

Another case is when n equals 1. The problem reduces to checking whether two intervals overlap directly, and the scaling step still works correctly since multiplying by 1 preserves the interval.

A third case is when b equals 0 or d equals 0. This collapses one or both intervals into single points. The algorithm still works because the intersection check naturally handles degenerate intervals without special casing.
