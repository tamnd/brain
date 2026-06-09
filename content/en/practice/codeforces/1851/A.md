---
title: "CF 1851A - Escalator Conversations"
description: "We are given a fixed escalator structure and a set of people with known heights. Vlad also has a height. The escalator has equally spaced steps, and each step increases in height by a constant value."
date: "2026-06-09T05:24:31+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1851
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 888 (Div. 3)"
rating: 800
weight: 1851
solve_time_s: 78
verified: true
draft: false
---

[CF 1851A - Escalator Conversations](https://codeforces.com/problemset/problem/1851/A)

**Rating:** 800  
**Tags:** brute force, constructive algorithms, math  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed escalator structure and a set of people with known heights. Vlad also has a height. The escalator has equally spaced steps, and each step increases in height by a constant value. The question is not about physical movement but about whether two people can be placed on two different steps so that the vertical distance between them matches the difference in their heights exactly.

For each person in the input, we need to decide independently whether there exists a pair of steps for Vlad and that person such that both the step difference constraint and the height difference constraint align perfectly. If such a placement exists, we count that person.

The key observation is that step differences are always multiples of a fixed value, since each step increases height by exactly `k`. This immediately turns the problem into checking whether a given height difference can be expressed as `d * k` for some integer `d` that fits within the escalator bounds.

The constraints are small: at most 1000 test cases and at most 50 people per test case. This guarantees that an O(n) per test case solution is sufficient, and even a simple arithmetic check per person is enough.

A common edge case arises when the height difference is zero or when it is not divisible by `k`. Another subtle case is when the required step difference exceeds the available number of steps, even if divisibility holds. Both conditions must be enforced simultaneously.

A naive mistake is to try to simulate all step pairs for each person, which is unnecessary and risks overlooking the fact that only the difference matters, not absolute positions.

## Approaches

A brute-force solution would try every pair of steps for Vlad and every person, checking whether there exists a valid alignment of step differences and height differences. For each person, this would require iterating over all `m * m` step pairs, leading to O(n m^2) per test case. While still technically small under constraints, it is conceptually inefficient and obscures the structure of the problem.

The key simplification is recognizing that the only thing that matters is the absolute height difference between Vlad and another person. Once this difference is fixed, the only question is whether we can realize it using the escalator geometry. Since each step contributes exactly `k` height difference, we are checking whether the difference is divisible by `k` and whether the implied step distance fits within `[1, m-1]`.

This reduces the problem to a direct arithmetic condition per person, eliminating all combinatorial reasoning.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n m^2) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the absolute height difference between Vlad and each person. This represents the total vertical gap that must be explained using escalator steps.
2. Check whether this difference is divisible by `k`. If it is not, then no sequence of step movements can match the height gap exactly, because each step contributes exactly `k` units.
3. If divisible, compute the required step distance as `diff // k`.
4. Verify that this step distance is strictly between 1 and `m - 1`. We require two different steps, so zero is invalid, and we cannot exceed the escalator range.
5. Count all people satisfying both conditions.

### Why it works

The escalator induces a discrete linear metric where valid height differences are exactly integer multiples of `k`. Any valid conversation corresponds to choosing two distinct steps whose index difference matches the quotient of the height difference divided by `k`. Since steps are bounded between 1 and `m`, the maximum achievable index difference is `m - 1`. This fully characterizes all valid configurations, so checking divisibility and bounds is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m, k, H = map(int, input().split())
    h = list(map(int, input().split()))
    
    ans = 0
    
    for x in h:
        diff = abs(x - H)
        
        if diff == 0:
            continue
        
        if diff % k != 0:
            continue
        
        d = diff // k
        
        if 1 <= d <= m - 1:
            ans += 1
    
    print(ans)
```

After reading the input, we iterate through each person and compute their absolute height difference with Vlad. We immediately discard cases where the difference is zero since two different steps are required. Then we enforce the divisibility condition by `k`, ensuring the escalator step size can represent the height gap. Finally, we check that the implied step distance fits inside the escalator range. Each valid person increments the answer.

The implementation is intentionally minimal because all structure is captured by these arithmetic constraints.

## Worked Examples

### Example 1

Input:

```
n = 5, m = 3, k = 3, H = 11
h = [5, 4, 14, 18, 2]
```

| Person | Height diff | diff % k | step distance | valid |
| --- | --- | --- | --- | --- |
| 5 | 6 | 0 | 2 | yes |
| 4 | 7 | - | - | no |
| 14 | 3 | 0 | 1 | yes |
| 18 | 7 | - | - | no |
| 2 | 9 | 0 | 3 | no |

We count two valid people.

### Example 2

Input:

```
n = 3, m = 1, k = 4, H = 10
h = [18, 6, 14]
```

| Person | Height diff | diff % k | step distance | valid |
| --- | --- | --- | --- | --- |
| 18 | 8 | 0 | 2 | no |
| 6 | 4 | 0 | 1 | no |
| 14 | 4 | 0 | 1 | no |

No valid pairs exist because only one step is available.

These examples confirm that both divisibility and step-range constraints must be enforced simultaneously.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each person is processed once with constant work |
| Space | O(1) | Only counters and input storage are used |

The constraints allow up to 1000 test cases and 50 elements each, so a linear scan per test case is easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, m, k, H = map(int, input().split())
        h = list(map(int, input().split()))
        ans = 0
        for x in h:
            diff = abs(x - H)
            if diff == 0:
                continue
            if diff % k == 0 and 1 <= diff // k <= m - 1:
                ans += 1
        out.append(str(ans))
    return "\n".join(out)

# provided sample
assert run("""7
5 3 3 11
5 4 14 18 2
2 9 5 6
11 9
10 50 3 11
43 44 74 98 62 60 99 4 11 73
4 8 8 49
68 58 82 73
7 1 4 66
18 66 39 83 48 99 79
9 1 1 13
26 23 84 6 60 87 40 41 25
6 13 3 28
30 70 85 13 1 55""") == """2
1
4
1
0
0
3"""

# custom cases
assert run("""1
1 10 2 5
7""") == "1", "single valid match"
assert run("""1
3 2 5 10
1 2 3""") == "0", "no divisibility case"
assert run("""1
4 3 1 10
11 9 8 10""") == "3", "k=1 dense reachability"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element near match | 1 | basic divisibility case |
| no matches | 0 | impossibility due to k constraint |
| k = 1 case | 3 | full reachability edge case |

## Edge Cases

When all heights equal Vlad’s height, every difference is zero, and none are counted because the problem requires two different steps, making self-matching invalid.

When `k` is large relative to all height differences, most differences fail the divisibility check, leading to zero valid conversations even if raw differences seem close.

When `m = 1`, no pair of distinct steps exists, so the answer is always zero regardless of height values, since the step distance constraint cannot be satisfied.
