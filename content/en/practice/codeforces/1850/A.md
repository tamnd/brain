---
title: "CF 1850A - To My Critics"
description: "We are asked to work with three digits, call them a, b, and c, each ranging from 0 to 9. The task is to determine if we can pick any two distinct digits among these three so that their sum is at least 10. We repeat this for t independent test cases."
date: "2026-06-09T05:28:54+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1850
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 886 (Div. 4)"
rating: 800
weight: 1850
solve_time_s: 62
verified: true
draft: false
---

[CF 1850A - To My Critics](https://codeforces.com/problemset/problem/1850/A)

**Rating:** 800  
**Tags:** implementation, sortings  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to work with three digits, call them `a`, `b`, and `c`, each ranging from 0 to 9. The task is to determine if we can pick any two distinct digits among these three so that their sum is at least 10. We repeat this for `t` independent test cases. The output should be a simple "YES" if such a pair exists and "NO" if none of the three possible pairs reach a sum of 10.

The constraints are very small: each digit is at most 9, and we have up to 1000 test cases. That means even a solution that checks all possible pairs for each test case will be fast, because for each test case there are only three pairs: `(a, b)`, `(a, c)`, `(b, c)`. Multiplying 3 pairs by 1000 test cases gives only 3000 operations, far below any time limit.

Edge cases worth noticing include cases where all digits are small, for instance `0 0 0`. The correct output is "NO" because no pair sums to 10. Similarly, if all digits are large, for instance `9 9 9`, any pair sums to 18, so the answer is "YES". A subtle edge is when two digits are borderline, like `1 9 0`-here only one pair `(1, 9)` meets the condition. Careless code might miscount the pairs or attempt to sum the same element twice, giving wrong answers.

## Approaches

The brute-force approach is straightforward. For each test case, consider all three possible pairs of digits and check if their sum is at least 10. If any pair meets the criterion, print "YES"; otherwise print "NO". This is correct because it examines all combinations, but in general, checking all pairs can be inefficient if the input set were larger. For three elements, brute-force is trivially fast.

The key insight for a slightly more elegant solution is that we only need to check the sums of the three pairs `(a + b)`, `(a + c)`, `(b + c)`. This works because the condition is symmetric and only depends on pairs, and since there are only three elements, these three sums cover every possibility. There is no need for sorting or more advanced data structures. The check can be performed inline, leading to a very simple and readable implementation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) per test case | O(1) | Accepted |
| Optimal (pair sum check) | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read three integers `a`, `b`, and `c`.
3. Compute the sums of the three possible pairs: `a + b`, `a + c`, and `b + c`.
4. Check if any of these sums is greater than or equal to 10.
5. If at least one sum meets the criterion, output "YES". Otherwise, output "NO".

Why it works: The algorithm checks every pair of distinct digits. Because the problem only asks if **any pair** reaches a sum of 10, covering all three pairs is sufficient. There are no hidden cases beyond these three, so the result is guaranteed correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b, c = map(int, input().split())
    if a + b >= 10 or a + c >= 10 or b + c >= 10:
        print("YES")
    else:
        print("NO")
```

The code directly implements the optimal algorithm. We use `sys.stdin.readline` for fast input, which matters more when `t` is large. Each test case is handled independently, and the condition is evaluated with simple logical OR statements, ensuring all pairs are checked. Using `>= 10` ensures we capture the boundary correctly. There are no loops beyond reading the test cases, so the complexity is minimal.

## Worked Examples

### Example 1

Input: `8 1 2`

| a | b | c | a+b | a+c | b+c | Output |
| --- | --- | --- | --- | --- | --- | --- |
| 8 | 1 | 2 | 9 | 10 | 3 | YES |

The pair `(a, c)` sums to 10, so the output is "YES".

### Example 2

Input: `4 4 5`

| a | b | c | a+b | a+c | b+c | Output |
| --- | --- | --- | --- | --- | --- | --- |
| 4 | 4 | 5 | 8 | 9 | 9 | NO |

No pair reaches a sum of 10, so the output is "NO".

These traces show the algorithm correctly identifies the pair sums and produces the expected result.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case involves 3 sum checks, so for t cases, it's O(3t) → O(t) |
| Space | O(1) | Only a constant number of variables are used per test case |

Given `t <= 1000` and constant work per test case, the solution is extremely fast. Memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        a, b, c = map(int, input().split())
        if a + b >= 10 or a + c >= 10 or b + c >= 10:
            output.append("YES")
        else:
            output.append("NO")
    return "\n".join(output)

# Provided samples
assert run("5\n8 1 2\n4 4 5\n9 9 9\n0 0 0\n8 5 3\n") == "YES\nNO\nYES\nNO\nYES", "sample 1"

# Custom cases
assert run("2\n0 0 0\n9 9 1\n") == "NO\nYES", "edge min and max"
assert run("1\n5 5 5\n") == "YES", "all equal and sum >= 10"
assert run("1\n1 2 3\n") == "NO", "all small numbers"
assert run("1\n0 9 1\n") == "YES", "boundary pair"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 0 | NO | smallest digits, no pair ≥ 10 |
| 9 9 1 | YES | largest digits, one valid pair |
| 5 5 5 | YES | all equal digits ≥ 5, sum ≥ 10 |
| 1 2 3 | NO | all small numbers, sum < 10 |
| 0 9 1 | YES | borderline pair sum 10 |

## Edge Cases

The algorithm handles the edge case where all digits are zero. Input `0 0 0` results in sums 0, 0, 0. None meet the criterion, so output is "NO". For maximum digits `9 9 9`, all sums are 18, producing "YES". For boundary conditions like `1 9 0`, it correctly identifies the `(1, 9)` pair and outputs "YES". Every non-obvious scenario is covered because the algorithm explicitly checks all three possible pairs.
