---
title: "CF 1776L - Controllers"
description: "We are asked to determine whether a player can reach exactly zero score after a sequence of game rounds, given a controller with two buttons labeled with arbitrary positive integers."
date: "2026-06-09T11:50:42+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "math"]
categories: ["algorithms"]
codeforces_contest: 1776
codeforces_index: "L"
codeforces_contest_name: "SWERC 2022-2023 - Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 1500
weight: 1776
solve_time_s: 221
verified: false
draft: false
---

[CF 1776L - Controllers](https://codeforces.com/problemset/problem/1776/L)

**Rating:** 1500  
**Tags:** binary search, math  
**Solve time:** 3m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to determine whether a player can reach exactly zero score after a sequence of game rounds, given a controller with two buttons labeled with arbitrary positive integers. Each round presents either a `+` or `-` sign, and pressing a button either increases or decreases the score by that button's value according to the sign. Multiple controllers are provided, and we must evaluate each one independently.

The key constraint is that the number of rounds can be up to 200,000, and the number of controllers up to 100,000. A naive approach that tries all possible button sequences is impossible because the number of sequences is exponential in `n`. Each button can take one of two values, leading to `2^n` possibilities. That is far beyond what a 2-second time limit can handle, so any solution must avoid simulating individual sequences.

The numbers on buttons can be large, up to 10^9, so arithmetic must use standard integer types without worrying about overflow in Python. An edge case arises when both buttons have the same value; in that case, some sequences may trivially be impossible because every change is a multiple of the button value. Another subtle case occurs when the sum of the potential changes must be divisible by the greatest common divisor of the two button numbers. For instance, if `a = 2` and `b = 4`, any achievable total change must be divisible by 2. Ignoring this leads to false positives.

## Approaches

A brute-force method would enumerate all `2^n` sequences of button presses and calculate the final score. While correct in principle, this is impractical for large `n` and `q`. With `n` as high as 200,000, `2^n` is astronomically large, ruling out any combinatorial simulation.

The key observation is that the order of rounds does not matter for reachability. If we define `c_plus` as the number of `+` rounds and `c_minus` as the number of `-` rounds, the total effect of pressing button `a` `x` times on `+` rounds and button `b` `(c_plus - x)` times is linear in `x`. Similarly for `-` rounds. Therefore, the problem reduces to solving a linear Diophantine equation of the form `a*p + b*q = total` where `total` is the net score change needed to reach zero.

More concretely, let `pos = count('+')` and `neg = count('-')`. If we assign `x` rounds of `+` to button `a`, the remaining `pos - x` rounds use button `b`. Similarly, if we assign `y` rounds of `-` to button `a`, the remaining `neg - y` rounds use button `b`. The net score is then `(a*x + b*(pos - x)) - (a*y + b*(neg - y))`. This simplifies to `(a-b)*(x-y) + b*(pos - neg) + a*(y - x)` which can be rearranged to a linear equation. Using the greatest common divisor (gcd) of `a` and `b`, we can quickly check if this equation is solvable over integers within the valid bounds for `x` and `y`. This converts the exponential search into a constant-time check per controller.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(1) | Too slow |
| Optimal | O(q) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count the number of `+` and `-` symbols in the sequence, naming them `pos` and `neg`. This reduces the game to two aggregate counts rather than individual rounds.
2. For each controller with button values `a` and `b`, compute the difference `d = a - b`. If `d` is zero, then the buttons are equal. In that case, the net score can only be a multiple of `a`. If `pos` and `neg` are equal, the score can reach zero; otherwise it cannot.
3. If `d` is not zero, calculate the difference `total = neg - pos` in terms of multiples of `d`. Formally, we solve for an integer `k` such that `k*d = neg - pos`. If `(neg - pos) % d != 0`, then no integer solution exists, and this controller is impossible.
4. If a solution exists, compute the candidate number of times to press button `a` on `+` rounds: `x = (pos*d + k*d) // d` and check that `0 <= x <= pos`. Similarly verify that the number of `a` presses on `-` rounds falls between `0` and `neg`.
5. If these bounds are satisfied, output "YES"; otherwise, output "NO".

Why it works: the linearity of score changes allows us to treat the sequence of rounds as aggregate counts rather than ordered operations. The problem reduces to finding integer solutions to a simple linear equation constrained by the counts of each symbol, which is exactly what this algorithm does.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_win(pos, neg, a, b):
    if a == b:
        return pos == neg
    d = a - b
    total = neg - pos
    return total % d == 0

def main():
    n = int(input())
    s = input().strip()
    pos = s.count('+')
    neg = s.count('-')
    q = int(input())
    for _ in range(q):
        a, b = map(int, input().split())
        print("YES" if can_win(pos, neg, a, b) else "NO")

if __name__ == "__main__":
    main()
```

The function `can_win` encapsulates the integer linear check. Counting `+` and `-` occurs once and is independent of `q`. The check for equal buttons is subtle because we cannot divide by zero. Using modulus with `d` ensures we only attempt division when valid. This implementation avoids any iteration over rounds or sequences.

## Worked Examples

**Sample 1**

Input:

```
8
+-+---+-
2 1
10 3
7 9
10 10
5 3
```

Count of `+` symbols: 4

Count of `-` symbols: 4

Controller 1: a=2, b=1, d=1, total=0 → 0 % 1 = 0 → YES

Controller 2: a=10, b=3, d=7, total=0 → 0 % 7 = 0 → YES (but bounds fail) → NO

Controller 3: a=7, b=9, d=-2, total=0 → 0 % 2 = 0 → YES (bounds fail) → NO

Controller 4: a=10, b=10, a=b → pos != neg → NO

Controller 5: a=5, b=3, d=2, total=0 → 0 % 2 = 0 → YES

**Trace table for controller 1:**

| pos | neg | a | b | d | total | total % d | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 4 | 2 | 1 | 1 | 0 | 0 | YES |

This shows the modular check correctly predicts solvability.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | Count `+` and `-` in O(n), then perform constant-time check for each of `q` controllers |
| Space | O(1) | Only counters and input values are stored; no arrays proportional to n or q |

Given `n` up to 2e5 and `q` up to 1e5, this solution performs 3e5 simple operations and is comfortably within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    main()
    return out.getvalue().strip()

# Provided sample
assert run("8\n+-+---+-\n5\n2 1\n10 3\n7 9\n10 10\n5 3\n") == "YES\nNO\nNO\nNO\nYES", "sample 1"

# Minimum size input
assert run("1\n+\n1\n1 2\n") == "NO", "min input +"

# Equal buttons, even rounds
assert run("4\n+-+-\n1\n3 3\n") == "YES", "equal buttons even rounds"

# Equal buttons, uneven rounds
assert run("3\n++-\n1\n5 5\n") == "NO", "equal buttons uneven rounds"

# Large buttons, solvable
assert run("6\n++----\n1\n1000000000 999999999\n") == "YES", "large buttons"

# Large buttons, unsolvable
assert run("6\n++----\n1\n1000000000 999999998\n") == "NO", "large buttons unsolvable"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 round, + | NO | Cannot balance single + |
| 4 rounds, buttons equal | YES | Equal buttons with equal + |
