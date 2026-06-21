---
title: "CF 105962A - Neymar at Santos"
description: "We are looking at a simplified financial model tied to football performance. There are $P$ teachers, each earning a fixed monthly salary $R$."
date: "2026-06-21T21:55:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105962
codeforces_index: "A"
codeforces_contest_name: "UNICAMP Freshman Contest 2025"
rating: 0
weight: 105962
solve_time_s: 56
verified: true
draft: false
---

[CF 105962A - Neymar at Santos](https://codeforces.com/problemset/problem/105962/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are looking at a simplified financial model tied to football performance. There are $P$ teachers, each earning a fixed monthly salary $R$. Neymar scores $G$ goals in a month, and for each goal, a fixed amount $X$ is supposed to be deducted from each teacher’s salary and transferred to Neymar.

The key restriction is that no teacher’s salary can become negative. If repeated deductions would reduce a teacher below zero, the deduction is capped so that the salary stops at zero.

The task is to compute the total amount Neymar receives after all $G$ goals, aggregated over all teachers.

From the constraints, $P$ can be as large as $10^8$, while $R$ is at most $3000$, $G$ at most $40$, and $X$ at most $2000$. This immediately suggests that any approach iterating over teachers is impossible, since $P$ alone makes $O(P)$ operations infeasible.

The important structure is that every teacher is identical in behavior. Each one contributes independently, so the answer is $P$ times the contribution of a single teacher.

A naive mistake happens when we ignore the cap at zero. For example, if $R = 10$, $G = 5$, and $X = 3$, then naive multiplication gives $15$ deducted per teacher, but the salary only allows $10$ to be taken. The correct per-teacher contribution is therefore $10$, not $15$.

Another subtle failure occurs when capping is applied per goal incorrectly. For instance, with $R = 10$, $G = 2$, $X = 7$, a naive approach might subtract $7$ twice for a total of $14$, then cap at $10$, which is fine here, but conceptually the correct reasoning is that the total deduction is $G \cdot X = 14$, then capped to $R$.

## Approaches

A brute-force interpretation would simulate each goal for each teacher, decrementing salaries step by step and stopping when a salary reaches zero. This is conceptually straightforward because it directly follows the rules of repeated deduction with a lower bound. However, this requires iterating over all $P$ teachers and all $G$ goals, leading to $P \cdot G$ operations. In the worst case this is $10^8 \cdot 40 = 4 \cdot 10^9$ updates, which is far beyond feasible limits.

The key observation is that all teachers are identical and independent. Instead of simulating, we can compute the total deduction per teacher in closed form. Each teacher loses $X$ per goal, so over $G$ goals the intended total is $G \cdot X$. However, the maximum possible loss is bounded by $R$, since salary cannot go below zero. Therefore, each teacher contributes exactly $\min(R, G \cdot X)$. Multiplying by $P$ gives the final answer.

This reduces the problem to constant-time arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(P · G) | O(1) | Too slow |
| Direct Formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the values $P$, $R$, $G$, and $X$. These define the number of identical contributors, their salary cap, the number of events, and the per-event deduction.
2. Compute the total intended deduction per teacher as $G \cdot X$. This represents what would happen if there were no salary restriction.
3. Compare this value with $R$, since no teacher can contribute more than their full salary. Take $\min(R, G \cdot X)$.
4. Multiply the per-teacher contribution by $P$ to obtain the total amount Neymar receives.
5. Output the result.

The core reasoning is that each teacher behaves independently and identically, so once the per-teacher contribution is known, scaling to the full population is linear and exact.

### Why it works

Each teacher’s salary evolution depends only on their own deductions and never interacts with others. Over $G$ identical operations, the total attempted deduction is additive. The only constraint is a hard upper bound of $R$, which truncates the total contribution per teacher. This makes the per-teacher contribution fully determined by a single min operation, and summing over all teachers preserves correctness because there are no cross-dependencies.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    P = int(input())
    R = int(input())
    G = int(input())
    X = int(input())

    per_teacher = min(R, G * X)
    print(P * per_teacher)

if __name__ == "__main__":
    solve()
```

The implementation follows the derived formula directly. The only subtle point is ensuring the multiplication $G \cdot X$ happens before the min, since the cap applies to the total accumulated deduction, not per goal. Python’s large integer support makes overflow a non-issue even when $P$ is large.

## Worked Examples

Consider an input where $P = 3$, $R = 10$, $G = 2$, $X = 3$. The intended deduction per teacher is $G \cdot X = 6$, which is below the salary cap.

| Step | Value |
| --- | --- |
| P | 3 |
| R | 10 |
| G · X | 6 |
| per teacher | min(10, 6) = 6 |
| total | 18 |

This shows the unrestricted case where no salary cap is triggered.

Now consider $P = 2$, $R = 8$, $G = 3$, $X = 5$. The total intended deduction per teacher is $15$, but salary limits it.

| Step | Value |
| --- | --- |
| P | 2 |
| R | 8 |
| G · X | 15 |
| per teacher | min(8, 15) = 8 |
| total | 16 |

This demonstrates the saturation behavior when the salary cap is binding.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations and comparisons are performed |
| Space | O(1) | No auxiliary data structures are used |

The solution easily fits within limits even for the maximum value of $P = 10^8$, since it avoids any per-teacher iteration entirely.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    P = int(sys.stdin.readline())
    R = int(sys.stdin.readline())
    G = int(sys.stdin.readline())
    X = int(sys.stdin.readline())

    per_teacher = min(R, G * X)
    return str(P * per_teacher)

# simple cases
assert run("1\n10\n1\n5\n") == "5"
assert run("1\n10\n2\n6\n") == "10"

# cap not reached
assert run("3\n10\n2\n3\n") == "18"

# cap reached
assert run("2\n8\n3\n5\n") == "16"

# zero effective cap scenario
assert run("100\n5\n10\n1\n") == "500"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1,10,1,5 | 5 | basic single teacher case |
| 1,10,2,6 | 10 | cap triggered |
| 3,10,2,3 | 18 | multi-teacher scaling |
| 2,8,3,5 | 16 | saturation behavior |
| 100,5,10,1 | 500 | large P with tight cap |

## Edge Cases

One important edge case is when the intended deduction is smaller than the salary. For example, with $P = 5$, $R = 100$, $G = 2$, $X = 10$, the total per teacher is $20$. The algorithm computes $\min(100, 20) = 20$, and multiplying gives $100$. No cap is triggered, and all teachers fully contribute the computed amount.

Another edge case is when the intended deduction exceeds salary by a large margin. For instance, $P = 4$, $R = 7$, $G = 3$, $X = 10$ gives $G \cdot X = 30$, but each teacher is capped at $7$. The result becomes $28$. The algorithm correctly collapses repeated overflows into a single cap operation.

A final edge case is when $P$ is extremely large, such as $10^8$. Since the computation reduces to a single multiplication after the min operation, there is no iteration over teachers, and the result remains exact and efficient.
