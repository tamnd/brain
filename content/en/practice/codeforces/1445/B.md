---
title: "CF 1445B - Elimination"
description: "We are asked to compute the smallest possible cutoff total score for an olympiad elimination stage. Each participant competes in two contests, and the jury only remembers partial information: the 100-th place score in each contest and a lower bound on the other contest's score…"
date: "2026-06-11T04:00:47+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1445
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 680 (Div. 2, based on Moscow Team Olympiad)"
rating: 900
weight: 1445
solve_time_s: 79
verified: true
draft: false
---

[CF 1445B - Elimination](https://codeforces.com/problemset/problem/1445/B)

**Rating:** 900  
**Tags:** greedy, math  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to compute the smallest possible cutoff total score for an olympiad elimination stage. Each participant competes in two contests, and the jury only remembers partial information: the 100-th place score in each contest and a lower bound on the other contest's score for the top 100 participants. Specifically, for the first contest, the 100-th place scored `a`, and all top 100 participants have at least `b` points in the second contest. Similarly, in the second contest, the 100-th place scored `c`, and all top 100 participants have at least `d` points in the first contest. We are to determine the minimum total score of the participant who ends up in 100-th place when ranking by total scores.

Input consists of multiple test cases. Each case is four integers `a, b, c, d` with constraints `0 ≤ a, b, c, d ≤ 9`, `d ≤ a` and `b ≤ c`. The constraints are small, allowing O(1) operations per test case. The main challenge is not efficiency but reasoning about how scores combine to produce the minimum possible cutoff.

A naive solution might try to simulate all participants’ scores, but that quickly becomes impractical, especially since the exact number of participants is unspecified. The edge cases involve situations where the first contest's 100-th place has a lower score than the minimum in the second contest for the top 100, or vice versa. For example, if `a = 0, b = 0, c = 0, d = 0`, the minimum total score is obviously 0. Careless approaches might overlook the fact that we only need to consider the worst-case combination of scores among the top 100, not the full participant list.

## Approaches

The brute-force approach would attempt to enumerate all possible score distributions of participants that respect the given bounds and find the 100-th total score. Each participant could take any value within the constraints, leading to combinatorial explosion. With 100 participants, even with scores 0-9, the operation count would be excessive, though theoretically feasible here due to small bounds.

The key insight is that we do not need to simulate all participants. We are only interested in the 100-th total score. To minimize the cutoff, we can assume that all other participants who could potentially push the cutoff higher are assigned the lowest allowed scores consistent with the given data. Thus, the minimum total score is achieved when we pick the maximum of the sums `a + b` and `c + d`. `a + b` represents the total for the 100-th participant in the first contest if they take the minimum in the second contest, and `c + d` represents the total for the 100-th participant in the second contest if they take the minimum in the first contest. The cutoff cannot be lower than either of these because the 100-th place in each contest must have at least the given scores in the other contest.

This observation collapses the problem into a simple `max(a + b, c + d)` computation per test case, making the solution O(1) per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(100^2) | O(100) | Overkill |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read the integers `a, b, c, d`.
3. Compute the sum of the first contest's 100-th place score and the minimum second contest score among top 100, i.e., `sum1 = a + b`.
4. Compute the sum of the second contest's 100-th place score and the minimum first contest score among top 100, i.e., `sum2 = c + d`.
5. Take the maximum of `sum1` and `sum2`. This represents the smallest total score that the 100-th participant can have without violating the given constraints.
6. Print this maximum.

Why it works: Any hypothetical scenario with a total score lower than `max(a + b, c + d)` would violate the conditions for the 100-th place in at least one contest. `a + b` ensures the 100-th participant in contest 1 meets the minimum for contest 2, and `c + d` ensures the 100-th participant in contest 2 meets the minimum for contest 1. Taking the maximum guarantees all constraints are respected while minimizing the total.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b, c, d = map(int, input().split())
    print(max(a + b, c + d))
```

This code reads the number of test cases and iterates through each one. For each set of four integers, it calculates the two possible total scores for the 100-th place and prints their maximum. Using `sys.stdin.readline` ensures fast I/O for many test cases. The `map(int, input().split())` converts the four values to integers efficiently.

## Worked Examples

### Example 1

Input: `1 2 2 1`

| Variable | Value |
| --- | --- |
| a | 1 |
| b | 2 |
| c | 2 |
| d | 1 |
| a + b | 3 |
| c + d | 3 |
| max(a+b,c+d) | 3 |

The output is 3, matching the sample. Both 100-th participants’ minimum totals coincide.

### Example 2

Input: `4 8 9 2`

| Variable | Value |
| --- | --- |
| a | 4 |
| b | 8 |
| c | 9 |
| d | 2 |
| a + b | 12 |
| c + d | 11 |
| max(a+b,c+d) | 12 |

The output is 12, confirming that the cutoff is dominated by the first contest's 100-th place.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case requires a constant number of operations. |
| Space | O(1) | Only a few variables are stored, independent of input size. |

Given `t ≤ 3025` and minimal operations per test case, this fits comfortably within the 1-second time limit and 512 MB memory constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    t = int(input())
    for _ in range(t):
        a, b, c, d = map(int, input().split())
        print(max(a + b, c + d))
    
    return output.getvalue().strip()

# Provided samples
assert run("2\n1 2 2 1\n4 8 9 2\n") == "3\n12", "sample 1 & 2"

# Custom cases
assert run("1\n0 0 0 0\n") == "0", "all zeros"
assert run("1\n9 9 9 9\n") == "18", "all maximum values"
assert run("1\n5 5 5 5\n") == "10", "all equal"
assert run("1\n3 7 6 2\n") == "10", "mixed values"
assert run("1\n0 9 9 0\n") == "9", "max cross scenario"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 0 0 | 0 | minimum values edge case |
| 9 9 9 9 | 18 | maximum values edge case |
| 5 5 5 5 | 10 | all-equal values scenario |
| 3 7 6 2 | 10 | general mixed scenario |
| 0 9 9 0 | 9 | ensures correct max computation |

## Edge Cases

If `a = d = 0` and `b = c = 9`, then `a + b = 0 + 9 = 9` and `c + d = 9 + 0 = 9`. The maximum is 9, which correctly gives the minimal total score for the 100-th place. The algorithm correctly handles situations where the first contest's minimum combines with the second contest's minimum, regardless of which dominates.
