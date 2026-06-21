---
title: "CF 106084A - Take It or Double It"
description: "We are given a simple interactive story that reduces to a decision about whether a value should be accepted immediately or allowed to “grow” once more. A starting amount of money $x$ is offered to the first person."
date: "2026-06-21T16:03:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106084
codeforces_index: "A"
codeforces_contest_name: "2025 ICPC Asia Taiwan Online Programming Contest"
rating: 0
weight: 106084
solve_time_s: 44
verified: true
draft: false
---

[CF 106084A - Take It or Double It](https://codeforces.com/problemset/problem/106084/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a simple interactive story that reduces to a decision about whether a value should be accepted immediately or allowed to “grow” once more.

A starting amount of money $x$ is offered to the first person. Each person in a chain can either accept the current amount, ending the process, or refuse it and force the amount to double for the next person. However, there is a global constraint: the host has only $d$ dollars available. If doubling the current amount would exceed $d$, the host is not allowed to let that happen and must force the current person to accept the money immediately.

The task is to determine, at the very first encounter with amount $x$, whether the person will say “take it” or “double it”, assuming all people prefer doubling whenever they are allowed to do so.

The key observation from the constraints is that both $x$ and $d$ are up to $10^9$. This is small enough that repeated doubling cannot continue for many steps, because each step grows the value exponentially. In fact, after at most 30 doublings, values already exceed the limit of 32-bit integers, and after around 30 to 31 steps they surpass $10^9$.

A naive simulation that repeatedly doubles until a stopping condition is still safe here, since the number of steps is logarithmic in $d$. However, the real problem is even simpler: we only need to decide whether one more doubling is allowed at the current state.

The main edge case is misunderstanding whether the decision depends on future steps or just the immediate next action. Another potential mistake is simulating multiple people unnecessarily, while the problem only asks for the first decision in the chain.

For example, if $x = 123$ and $d = 246$, doubling gives exactly 246, which is valid, so the answer is “double it”. If $x = 345$ and $d = 678$, doubling gives 690, which exceeds the limit, so the person must be forced to take the money immediately.

The entire process collapses into checking a single inequality.

## Approaches

The brute-force interpretation follows the story literally. We start at value $x$, and repeatedly simulate people in sequence. At each step, we check whether doubling the current value would exceed $d$. If it does, we stop and force acceptance. Otherwise, we double and continue. We repeat until someone takes the money.

This works because the process is deterministic: every person always chooses to double unless forced otherwise. However, the number of iterations is proportional to how many times we can double before exceeding $d$, which is at most $O(\log d)$. While this is already small, it is still unnecessary work given the problem only asks for the very first decision.

The key insight is that the behavior of all future participants is irrelevant to the current decision. The only question is whether the current amount can legally be doubled once. If $2x > d$, then doubling is impossible immediately, so the answer is forced acceptance. If $2x \le d$, then doubling is allowed, and the person will always choose it.

This reduces the entire process to a constant-time comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulation of full process | $O(\log d)$ | $O(1)$ | Accepted |
| Direct check $2x \le d$ | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We only need to determine whether the first person is allowed to pass the money forward.

1. Read the values $x$ and $d$. These represent the current offer and the maximum allowed budget.
2. Compute $2x$. This represents what the next offer would become if the person chooses to double.
3. Compare $2x$ with $d$. If $2x$ is strictly greater than $d$, then doubling is not allowed, so the person must accept immediately.
4. Otherwise, if $2x \le d$, the person follows their preference and chooses to double.

The decision is entirely determined at this single step, so no further simulation is needed.

### Why it works

At any point in the process, the only constraint that restricts behavior is whether doubling violates the budget. The participants have no reason to take early unless forced, so the only blocking condition is $2 \cdot \text{current} > d$. Since we are asked only about the initial state, the entire system reduces to checking whether the first doubling is valid. Any future chain does not affect this local feasibility condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

x, d = map(int, input().split())

if 2 * x > d:
    print("take it")
else:
    print("double it")
```

The solution reads the two integers and performs a single arithmetic comparison. The only subtlety is ensuring multiplication happens before comparison, which is safe in Python due to arbitrary precision integers.

The decision logic directly mirrors the algorithm: we test whether the next state after doubling is valid under the constraint.

## Worked Examples

### Example 1

Input: `123 246`

We compute whether doubling is allowed.

| Step | Current x | 2x | d | Decision |
| --- | --- | --- | --- | --- |
| 1 | 123 | 246 | 246 | double it |

Since $2x = d$, doubling is valid, so the correct output is “double it”.

This confirms that equality is allowed and only strict overflow blocks doubling.

### Example 2

Input: `345 678`

| Step | Current x | 2x | d | Decision |
| --- | --- | --- | --- | --- |
| 1 | 345 | 690 | 678 | take it |

Here $2x > d$, so doubling is impossible. The person must accept immediately.

This validates that the comparison is strict and not inclusive.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only one multiplication and one comparison are performed |
| Space | $O(1)$ | No additional data structures are used |

The constraints allow up to $10^9$, but the algorithm performs constant-time arithmetic, which is trivially within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    x, d = map(int, sys.stdin.readline().split())
    return "double it" if 2 * x <= d else "take it"

# provided samples
assert run("123 246\n") == "double it"
assert run("345 678\n") == "take it"

# custom cases
assert run("1 1\n") == "take it", "doubling exceeds even smallest bound"
assert run("1 2\n") == "double it", "exact boundary case"
assert run("500000000 1000000000\n") == "double it", "max boundary valid"
assert run("500000001 1000000000\n") == "take it", "just over half boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | take it | minimum edge where doubling fails |
| 1 2 | double it | smallest valid doubling case |
| 500000000 1000000000 | double it | large boundary where equality holds |
| 500000001 1000000000 | take it | off-by-one around half of d |

## Edge Cases

The main edge case is when $2x = d$. For input `123 246`, the algorithm computes $2x = 246$, which is not greater than $d$, so it correctly outputs “double it”. This confirms that equality does not trigger forced acceptance.

Another edge case is when $x = d$. For input `100 100`, we compute $2x = 200$, which exceeds $d$, so the output is “take it”. This shows that even when the initial offer is fully affordable, doubling may already be invalid.

A third case is when $x$ is just below half of $d$, such as `499999999 1000000000`. Doubling is still valid, so the process continues. But if we increase $x$ by one, the decision flips immediately. This highlights that the solution is entirely boundary-driven and sensitive only to the single inequality $2x \le d$.
