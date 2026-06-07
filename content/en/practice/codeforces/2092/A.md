---
title: "CF 2092A - Kamilka and the Sheep"
description: "We are given a list of sheep, each with a distinct beauty level. Kamilka can feed every sheep the same number of extra grass bunches, effectively increasing all beauty levels by the same integer $d ge 0$."
date: "2026-06-08T05:41:54+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "number-theory", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2092
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1014 (Div. 2)"
rating: 800
weight: 2092
solve_time_s: 77
verified: true
draft: false
---

[CF 2092A - Kamilka and the Sheep](https://codeforces.com/problemset/problem/2092/A)

**Rating:** 800  
**Tags:** greedy, math, number theory, sortings  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of sheep, each with a distinct beauty level. Kamilka can feed every sheep the same number of extra grass bunches, effectively increasing all beauty levels by the same integer $d \ge 0$. After this feeding, she must select exactly two sheep, and the pleasure she gets is the greatest common divisor (GCD) of their resulting beauty levels. The task is to maximize this GCD.

The input consists of multiple test cases, each specifying $n$, the number of sheep, followed by $n$ distinct integers representing beauty levels. The output is a single integer per test case - the maximum GCD achievable.

The constraints are moderate: $n$ can be up to 100, beauty levels can be as high as $10^9$, and there are up to 500 test cases. Because $n$ is small, algorithms with $O(n^2)$ time per test case are feasible, but brute-force attempts to test every $d$ up to $10^9$ are impossible.

The key edge cases include scenarios where only two sheep exist, which forces us to consider the difference between them carefully. Another edge case is when beauty levels are already coprime; adding a uniform $d$ might be the only way to increase the GCD. For example, for input `2\n1 3\n`, choosing $d=1$ produces GCD 2, which is optimal. A naive approach that ignores the possibility of adding a uniform $d$ will incorrectly output 1.

## Approaches

The brute-force approach is straightforward: for each possible $d$, compute all resulting beauty levels and check the GCD of every pair. This is correct because it tests all feasible ways of feeding, but it fails completely in practice because $d$ can be extremely large, up to $10^9$, making it infeasible.

The key insight is to consider how GCD behaves under uniform addition. Let the two chosen sheep have beauty levels $x$ and $y$. After adding $d$, their values become $x+d$ and $y+d$, and the GCD of the two is $\gcd(x+d, y+d)$. By the properties of GCD, this simplifies to $\gcd(x+d, y+d) = \gcd(x - y, y + d)$. This means the maximum GCD achievable is always a divisor of some difference $y - x$.

Thus, instead of iterating over $d$, we can iterate over all pairs of sheep and compute the difference of their beauty levels. For each difference $diff = y - x$, all divisors of $diff$ are candidate maximum GCDs. Then, for each candidate divisor, we check if there exists a $d$ such that adding it to all sheep produces two numbers divisible by the divisor. Because we can always shift $d$ to make the larger number divisible by the divisor, the largest divisor of any difference between two sheep is always achievable. Therefore, the optimal strategy reduces to finding the largest difference between any two sheep and taking its divisors.

This leads to a simple and efficient $O(n^2)$ algorithm: iterate over all pairs of sheep, compute their differences, and record the maximum difference. That maximum difference's largest divisor is the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 * max(a_i)) | O(n) | Too slow |
| Optimal | O(n^2) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of sheep $n$ and their beauty levels $a$.
2. Initialize a variable `max_beauty` to the maximum beauty level and `min_beauty` to the minimum. The difference `max_beauty - min_beauty` gives the maximum gap between any two sheep.
3. The maximum pleasure Kamilka can achieve is exactly this difference because we can choose $d = max_beauty - max(a_i)$ to shift numbers and make the GCD equal to the difference.
4. Print this value as the answer for the test case.

Why it works: adding the same $d$ to all numbers does not change the differences between numbers. The GCD of two numbers after adding $d$ can always be maximized by taking the difference between the largest and smallest number. Because the differences of beauty levels determine all possible GCDs, the global maximum is the largest difference itself.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    max_a = max(a)
    min_a = min(a)
    print(max_a - min_a)
```

This solution reads input efficiently using `sys.stdin.readline`, extracts the number of sheep and their beauty levels, computes the maximum and minimum beauty levels, and outputs the difference. This works because the difference captures the maximum achievable GCD after adding a suitable $d$. The solution avoids unnecessary computations and works within all constraints.

## Worked Examples

### Example 1

Input:

```
2
1 3
```

| Step | a | max(a) | min(a) | max - min |
| --- | --- | --- | --- | --- |
| Initial | [1,3] | 3 | 1 | 2 |

Output: 2

Explanation: adding $d=1$ gives numbers 2 and 4, whose GCD is 2, which matches the difference.

### Example 2

Input:

```
5 4 3 2 1
```

| Step | a | max(a) | min(a) | max - min |
| --- | --- | --- | --- | --- |
| Initial | [5,4,3,2,1] | 5 | 1 | 4 |

Output: 4

Explanation: feeding $d=0$ and choosing 1 and 5 gives GCD 4, which is optimal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Only need max and min computation over n elements |
| Space | O(n) | Storing beauty levels |

Since $n \le 100$ and $t \le 500$, the total operations are around 50,000, well within the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = int(input())
    res = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        res.append(str(max(a)-min(a)))
    return "\n".join(res)

# Provided samples
assert run("4\n2\n1 3\n5\n5 4 3 2 1\n3\n5 6 7\n3\n1 11 10\n") == "2\n4\n2\n10"

# Custom cases
assert run("1\n2\n1000000000 1\n") == "999999999", "large difference"
assert run("1\n3\n7 7 7\n") == "0", "all equal"
assert run("1\n2\n1 2\n") == "1", "minimum size"
assert run("1\n4\n10 1 2 3\n") == "9", "non-sorted input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2\n1000000000 1` | 999999999 | Maximum difference near upper limit |
| `3\n7 7 7` | 0 | All sheep equal beauty |
| `2\n1 2` | 1 | Minimum size input |
| `4\n10 1 2 3` | 9 | Algorithm works on unsorted input |

## Edge Cases

If all sheep have the same beauty, the difference is zero. For example, input `3\n7 7 7` produces output `0`. The algorithm correctly identifies this because `max(a) - min(a)` is 0.

If there are only two sheep, input `2\n1 2`, the difference is 1. Adding $d$ does not increase the GCD beyond 1 because the numbers are consecutive; the algorithm handles this by computing `max(a)-min(a)` directly, producing 1.

If beauty levels span the full range, e.g., `2\n1 1000000000`, the algorithm computes `1000000000 - 1 = 999999999` efficiently without overflow, since Python integers handle arbitrarily large values.

This solution is simple, efficient, and directly leverages the mathematical property that GCD maximization under uniform addition is determined by the largest difference.
