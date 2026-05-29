---
title: "CF 245A - System Administrator"
description: "Polycarpus is running a simple monitoring routine for two servers, which we can call server a and server b. Each \"ping\" command sends exactly ten packets to one of the servers."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 245
codeforces_index: "A"
codeforces_contest_name: "CROC-MBTU 2012, Elimination Round (ACM-ICPC)"
rating: 800
weight: 245
solve_time_s: 207
verified: true
draft: false
---

[CF 245A - System Administrator](https://codeforces.com/problemset/problem/245/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 3m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

Polycarpus is running a simple monitoring routine for two servers, which we can call server _a_ and server _b_. Each "ping" command sends exactly ten packets to one of the servers. The input tells us, for each ping, how many packets successfully reached the server and how many were lost. The goal is to determine whether each server is "alive" or "dead" at the end of the day. A server is "alive" if at least half of all packets sent to it during the day successfully reached it; otherwise, it is "dead".

The input gives the number of ping commands executed, followed by a list of results for each command. Each line indicates which server was pinged and how many packets succeeded and failed. Because the number of ping commands is at most 1000, we can process all commands linearly. Each ping only involves simple arithmetic (summing packet successes), so we do not need advanced data structures or algorithms.

A subtle edge case arises when the total number of successful packets is exactly half of all packets sent. For instance, if server _a_ received two pings of 5 successful packets each, the total is 10 out of 20, which qualifies as "alive". A careless implementation might check for strictly greater than half, producing an incorrect "dead" answer. Another case to watch is when one server receives far more pings than the other, which should not affect the independent calculation for each server.

## Approaches

The naive approach is actually optimal here. We could, in principle, simulate each packet individually, but since each ping always sends ten packets, it is enough to keep track of total successful packets and total sent packets for each server. This is equivalent to accumulating the number of successes and comparing against half of total packets sent. The brute-force method of listing each individual packet would take O(n*10) operations, which is still feasible for n = 1000, but unnecessary.

The key insight is that we do not care about individual pings beyond counting the successes. All we need is two accumulators, one for each server, to sum successes, and then compare each to half the total packets sent to that server. This reduces the problem to O(n) time and O(1) space.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate packets) | O(n*10) | O(n*10) | Accepted but overkill |
| Optimal (sum successes) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize two counters for successful packets: `success_a` and `success_b`, and two counters for total packets sent: `total_a` and `total_b`. Each server starts with zero successes and zero packets sent.
2. Iterate through all ping commands. For each command, read the server type `t`, number of successes `x`, and number of lost packets `y`.
3. If `t` is 1 (server _a_), add `x` to `success_a` and add `x + y` (which is always 10) to `total_a`. If `t` is 2 (server _b_), add `x` to `success_b` and add `x + y` to `total_b`. This accumulates the total successes and total packets sent for each server.
4. After processing all commands, compare `success_a` with `total_a // 2`. If it is greater than or equal to half of `total_a`, server _a_ is "LIVE"; otherwise, it is "DEAD". Do the same for server _b_ using `success_b` and `total_b // 2`.

Why it works: Each server is evaluated independently based on the total number of packets sent and the total successes. Summing the successes and totals maintains the exact ratio required to check if at least half the packets were successful. No information is lost by accumulating totals rather than tracking individual pings.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
success_a = 0
success_b = 0
total_a = 0
total_b = 0

for _ in range(n):
    t, x, y = map(int, input().split())
    if t == 1:
        success_a += x
        total_a += x + y
    else:
        success_b += x
        total_b += x + y

print("LIVE" if success_a * 2 >= total_a else "DEAD")
print("LIVE" if success_b * 2 >= total_b else "DEAD")
```

The solution initializes counters for each server and iterates through each ping command. The multiplication by 2 in the comparison avoids floating-point division and correctly handles the case when the number of successful packets is exactly half of the total. The code ensures that every ping is accounted for and that the decision logic matches the problem requirement.

## Worked Examples

Sample 1:

| t | x | y | success_a | total_a | success_b | total_b |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 5 | 5 | 5 | 10 | 0 | 0 |
| 2 | 6 | 4 | 5 | 10 | 6 | 10 |

After processing, success_a_2 = 10 >= total_a=10 → LIVE, success_b_2 = 12 >= total_b=10 → LIVE. Both servers are alive.

Sample 2:

| t | x | y | success_a | total_a | success_b | total_b |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 10 | 10 | 10 | 20 | 0 | 0 |
| 2 | 0 | 10 | 10 | 20 | 0 | 10 |

success_a_2 = 20 >= total_a=20 → LIVE, success_b_2 = 0 < total_b=10 → DEAD. Server a is alive, server b is dead.

This trace demonstrates that the algorithm correctly handles exact half and zero-success cases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each of the n commands is processed exactly once, performing constant work per command. |
| Space | O(1) | Only four counters are maintained regardless of n. |

Since n ≤ 1000, the O(n) solution easily fits within the 2-second time limit. Memory usage is negligible, far below the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    success_a = 0
    success_b = 0
    total_a = 0
    total_b = 0
    for _ in range(n):
        t, x, y = map(int, input().split())
        if t == 1:
            success_a += x
            total_a += x + y
        else:
            success_b += x
            total_b += x + y
    return f"{'LIVE' if success_a*2 >= total_a else 'DEAD'}\n{'LIVE' if success_b*2 >= total_b else 'DEAD'}"

# Provided samples
assert run("2\n1 5 5\n2 6 4\n") == "LIVE\nLIVE", "sample 1"
assert run("2\n1 10 10\n2 0 10\n") == "LIVE\nDEAD", "sample 2"

# Custom cases
assert run("2\n1 5 5\n2 5 5\n") == "LIVE\nLIVE", "half-success boundary"
assert run("2\n1 4 6\n2 5 5\n") == "DEAD\nLIVE", "a fails, b passes"
assert run("4\n1 10 0\n1 0 10\n2 5 5\n2 0 10\n") == "LIVE\nDEAD", "multiple pings with mixed results"
assert run("2\n1 0 10\n2 0 10\n") == "DEAD\nDEAD", "all failures"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n1 5 5\n2 5 5 | LIVE\nLIVE | exactly half success case |
| 2\n1 4 6\n2 5 5 | DEAD\nLIVE | one server fails, one passes |
| 4\n1 10 0\n1 0 10\n2 5 5\n2 0 10 | LIVE\nDEAD | multiple pings with mixed successes |
| 2\n1 0 10\n2 0 10 | DEAD\nDEAD | zero-success case |

## Edge Cases

For the half-success boundary, input `2\n1 5 5\n2 5 5\n` results in `success_a=5, total_a=10` and `success_b=5, total_b=10`. The condition `success*2 >= total` evaluates as `10 >= 10` → True, so both servers are LIVE. This confirms the algorithm handles exactly 50% success correctly.

For the all-failures case `2\n1 0 10\n2 0 10`, the counters `success_a=0, total_a=10
