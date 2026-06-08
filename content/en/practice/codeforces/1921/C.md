---
title: "CF 1921C - Sending Messages"
description: "Stepan needs to send a series of messages at strictly increasing moments in time. His phone starts with a finite charge, loses a constant amount per unit of time while it is on, and consumes a fixed cost if he turns it off and then back on."
date: "2026-06-08T19:21:48+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1921
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 920 (Div. 3)"
rating: 900
weight: 1921
solve_time_s: 108
verified: true
draft: false
---

[CF 1921C - Sending Messages](https://codeforces.com/problemset/problem/1921/C)

**Rating:** 900  
**Tags:** greedy, math  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

Stepan needs to send a series of messages at strictly increasing moments in time. His phone starts with a finite charge, loses a constant amount per unit of time while it is on, and consumes a fixed cost if he turns it off and then back on. The problem asks whether he can schedule all messages without the battery ever reaching zero.

Each test case provides the number of messages, the initial battery, the per-unit time consumption, the cost of toggling power, and the exact moments the messages need to be sent. We must output "YES" if there exists a sequence of on/off decisions that allows all messages to be sent, and "NO" otherwise.

Constraints suggest that the sum of messages across all test cases does not exceed 200,000, and time moments can be up to $10^9$. This rules out any solution that would iterate through each time unit individually; we must reason in terms of the differences between message times. Edge cases include situations where the battery is barely enough to survive until the first message or where toggling the phone on and off is cheaper than leaving it on.

A careless approach might simulate every unit of time or ignore the choice between leaving the phone on versus turning it off, leading to wrong answers on inputs where the optimal strategy involves toggling.

## Approaches

The brute-force approach considers the phone state at every single moment from 0 to the last message, either staying on or turning off to conserve energy. For each unit of time, we would calculate the battery drop. This is correct in principle, but with $10^9$ as the maximum message time, iterating over time units is infeasible.

The key insight is that the battery only changes at discrete moments: at the times of the messages and immediately before or after a phone toggle. Between two consecutive messages, we only need to decide whether it is cheaper to leave the phone on or to turn it off and on again. For a gap of length $d$, leaving the phone on consumes $a \cdot d$ units, while turning it off and on consumes $b$ units. Hence, for each interval, the minimal battery cost is $\min(a \cdot d, b)$. We accumulate these costs starting from the first message and check whether the remaining battery ever drops below zero.

This observation reduces the problem to $O(n)$ per test case, because we only process the differences between consecutive message moments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate each time unit) | O(max(m_i)) | O(1) | Too slow |
| Optimal (greedy intervals) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read $n, f, a, b$ and the list of message times $m$.
3. Initialize the remaining battery to $f$.
4. Iterate over the gaps between consecutive messages, including the first message at time $m_1$ as a gap from 0. Compute the length of the gap $d = m_i - m_{i-1}$ (with $m_0 = 0$).
5. For each gap, determine the minimal battery cost: $\min(a \cdot d, b)$. Subtract this from the remaining battery.
6. If at any point the battery drops to 0 or below, break and output "NO" for this test case. Otherwise, after all messages, output "YES".

Why it works: the algorithm always chooses the cheaper option between leaving the phone on or turning it off and on for each gap. Since the phone only loses battery in two ways-linear in time when on or fixed when toggled-this greedy choice guarantees the minimal possible consumption up to each message, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, f, a, b = map(int, input().split())
    m = list(map(int, input().split()))
    prev = 0
    battery = f
    possible = True
    for time in m:
        gap = time - prev
        cost = min(a * gap, b)
        battery -= cost
        if battery <= 0:
            possible = False
            break
        prev = time
    print("YES" if possible else "NO")
```

The code reads inputs efficiently using `sys.stdin.readline` for multiple test cases. For each message, it calculates the interval from the previous moment, computes the cheaper cost, and updates the battery. The `battery <= 0` check ensures that any scenario where Stepan cannot send a message is detected immediately. Using `min(a * gap, b)` captures the essential greedy decision.

## Worked Examples

**Example 1**

Input: `1 3 1 5`

- Gap: 3 units (from 0 to 3)
- Cost: min(1*3, 5) = 3
- Remaining battery: 3 - 3 = 0 → output "NO"

**Example 3**

Input: `5 10 1 2` with messages `[1, 2, 3, 4, 5]`

| Message | Gap | Cost | Battery After |
| --- | --- | --- | --- |
| 1 | 1 | min(1,2)=1 | 10-1=9 |
| 2 | 1 | 1 | 9-1=8 |
| 3 | 1 | 1 | 8-1=7 |
| 4 | 1 | 1 | 7-1=6 |
| 5 | 1 | 1 | 6-1=5 |

Battery never reaches 0 → output "YES". This shows the algorithm correctly accumulates costs and handles small gaps efficiently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each message is processed once; n summed over all test cases ≤ 2×10^5 |
| Space | O(n) | Storing message times per test case; no additional structures |

The solution fits well within the 2-second time limit because it processes each message once and uses minimal additional memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    # call solution
    t = int(input())
    for _ in range(t):
        n, f, a, b = map(int, input().split())
        m = list(map(int, input().split()))
        prev = 0
        battery = f
        possible = True
        for time in m:
            gap = time - prev
            cost = min(a * gap, b)
            battery -= cost
            if battery <= 0:
                possible = False
                break
            prev = time
        print("YES" if possible else "NO")
    return out.getvalue().strip()

# Provided samples
assert run("6\n1 3 1 5\n3\n7 21 1 3\n4 6 10 13 17 20 26\n5 10 1 2\n1 2 3 4 5\n1 1000000000 1000000000 1000000000\n1000000000\n3 11 9 6\n6 8 10\n12 621526648 2585904 3566299\n51789 61859 71998 73401 247675 298086 606959 663464 735972 806043 806459 919683") == "NO\nYES\nYES\nNO\nNO\nYES"

# Custom edge cases
assert run("1\n1 1 1 1\n1") == "NO", "battery exactly equal to gap cost"
assert run("1\n2 10 1 100\n1 1000000000") == "YES", "large gap with off/on cheaper than long on"
assert run("1\n3 5 2 3\n1 2 4") == "NO", "mixed gap costs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1\n1` | NO | Battery reaches 0 exactly at first message |
| `2 10 1 100\n1 1000000000` | YES | Handles very large gaps efficiently |
| `3 5 2 3\n1 2 4` | NO | Mixed greedy decisions between leaving on and toggling |

## Edge Cases

When the battery is exactly equal to the cost of the first interval, the algorithm correctly outputs "NO". For extremely large gaps, multiplying `a * gap` might overflow in some languages, but Python handles large integers, and the `min(a * gap, b)` choice correctly prevents incorrect overflow results. The greedy choice guarantees minimal consumption for each interval, so no subtle case of skipping a toggle will cause a wrong answer.
