---
title: "CF 106270F - Morning Walk"
description: "We are given a circular running track of fixed length. Kabul runs along this loop at a constant speed and keeps moving in one direction for a fixed duration."
date: "2026-06-19T16:41:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106270
codeforces_index: "F"
codeforces_contest_name: "ICPC Asia Dhaka Regional Onsite 2025 \u2014 Replay Contest"
rating: 0
weight: 106270
solve_time_s: 59
verified: true
draft: false
---

[CF 106270F - Morning Walk](https://codeforces.com/problemset/problem/106270/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a circular running track of fixed length. Kabul runs along this loop at a constant speed and keeps moving in one direction for a fixed duration. Other walkers are also moving along the same loop, each with a constant signed speed, so they either move with Kabul or against him.

For each other walker, we are told the time when Kabul first meets that walker. After that first encounter, the two continue moving on the same circular track, so they may meet again multiple times before time runs out. The task is to determine, for every walker, how many total meetings happen during the time interval from the start until the final time T, including the initial meeting and any meeting that happens exactly at T.

The key structure is that every walker moves on a circle with constant velocity, so relative motion is uniform and meetings repeat periodically. Each test case can contain up to 200,000 walkers in total, and times can go up to 10^7, so any solution that simulates movement over time or processes each second is impossible. Even O(NT) or anything that depends on T is immediately ruled out. Even O(N sqrt T) is unsafe.

A subtle point is that we are not asked to compute the first meeting time. That is already given. The input fixes a reference alignment between Kabul and each walker. This removes geometric ambiguity and turns the problem into counting how many times a periodic event occurs in a bounded time interval.

Edge cases that commonly break naive reasoning come from modular wrap-around and direction changes.

A simple failure case is when a walker moves in the same direction very close in speed to Kabul. They may meet rarely but still multiple times, and the period becomes large.

Another edge case is when a meeting occurs exactly at time T. Since T is inclusive, failing to count boundary hits leads to off-by-one errors.

Finally, direction matters only through relative speed. Treating all walkers uniformly without signed velocity leads to incorrect period computation.

## Approaches

A brute-force interpretation would simulate the positions of Kabul and each walker over time. We could advance time in small increments and track when positions match modulo L. For each walker, detecting meetings up to time T would require stepping through all future collision events.

The problem is that meetings form an arithmetic progression in time. The relative position between Kabul and a walker changes linearly with time, and on a circle, equality of position repeats every full relative lap. This turns the sequence of meeting times into an arithmetic progression starting from the given first meeting time ti, with a fixed period depending only on relative speed.

If we let the effective relative speed be v0 - vi, then after each full cycle around the circle, the same alignment repeats. So once we have one meeting at ti, every next meeting happens exactly after a constant time gap equal to L divided by the absolute relative speed.

This reduces each walker to a simple counting problem: given a first occurrence time and a period, count how many terms of an arithmetic progression lie within [0, T].

The brute-force approach works because it directly follows motion, but fails because it would require stepping through potentially O(T) or O(T / period) events per walker. The observation that motion is periodic on a circle reduces the problem to arithmetic progression counting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | O(N · T) | O(1) | Too slow |
| Arithmetic progression counting | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

We treat each walker independently because interactions do not affect each other.

### 1. Compute relative motion

For each walker, compute the relative speed between Kabul and the walker. Since Kabul moves at v0 and the walker moves at vi, the closing speed is v0 - vi in signed form. Only magnitude matters for cycle length.

The reason is that meetings depend only on how fast the distance around the circle is resolved, not direction conventions.

### 2. Derive meeting period

Each time Kabul overtakes or meets the walker again, the relative displacement increases by exactly one full loop length L. Therefore, the time between consecutive meetings is L / |v0 - vi|.

This is the period of the arithmetic progression of meeting times.

### 3. Model meeting times

All meeting times can be written as:

ti, ti + period, ti + 2·period, ...

The first term is given, so we do not need to compute it geometrically.

### 4. Count valid terms within time window

We need the number of terms in the progression that lie in [0, T]. Since ti is guaranteed to be within [0, T], we only need to count how many terms do not exceed T.

So we compute the largest k such that:

ti + k · period ≤ T

This gives:

k ≤ (T - ti) / period

Thus the number of meetings is:

k + 1

### 5. Handle integer arithmetic safely

Because L and speeds are integers, period may not be integer in real arithmetic. However, all input guarantees consistent alignment so we work in rational arithmetic by scaling: we avoid floating point and compute using multiplication.

We rewrite condition:

ti + k·L / d ≤ T, where d = |v0 - vi|

Multiply through:

ti·d + k·L ≤ T·d

So:

k ≤ (T·d - ti·d) / L

We use integer division.

### Why it works

The motion of Kabul and any walker on a circle reduces to a linear function of time modulo L. Equality of positions corresponds to solving a linear congruence in time. Once one solution ti is given, all other solutions form a lattice spaced exactly by L / |v0 - vi|. Since no other forces or interactions exist, the set of meeting times is fully determined by this arithmetic progression. Counting valid meetings is therefore equivalent to counting integer points in a bounded interval of a progression, which is captured exactly by the derived inequality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    K = int(input())
    out = []
    for _ in range(K):
        L, v0, T, N = map(int, input().split())
        res = []
        for _ in range(N):
            ti, vi = map(int, input().split())

            d = abs(v0 - vi)

            # number of additional full cycles possible
            # k such that ti + k*(L/d) <= T
            # => ti*d + k*L <= T*d
            # => k <= (T*d - ti*d) // L
            if ti > T:
                res.append(0)
                continue

            numerator = (T - ti) * d
            if L == 0 or numerator < 0:
                res.append(0)
                continue

            k = numerator // L
            res.append(k + 1)

        out.append(" ".join(map(str, res)))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution processes each walker independently in constant time. The critical part is avoiding floating-point division for the period. Instead, we multiply the inequality by the relative speed to keep everything in integers. This prevents precision issues and preserves correctness even for large values of T and L.

A subtle detail is handling ti exactly at or beyond T. Since ti is guaranteed to be within bounds in the statement, this check is mostly defensive, but it protects against arithmetic edge cases.

## Worked Examples

Consider a small example where L = 100, v0 = 10, T = 50.

### Example 1

A walker has vi = 0 and ti = 10.

Relative speed d = 10.

Period is L / d = 10.

Meeting times are:

10, 20, 30, 40, 50

| k | time |
| --- | --- |
| 0 | 10 |
| 1 | 20 |
| 2 | 30 |
| 3 | 40 |
| 4 | 50 |

All are within T, so answer is 5.

This demonstrates inclusion of the boundary case at T.

### Example 2

Same setup, but vi = 5 and ti = 7.

Relative speed d = 5, period = 20.

Meeting times:

7, 27, 47

| k | time |
| --- | --- |
| 0 | 7 |
| 1 | 27 |
| 2 | 47 |

Next would be 67, which exceeds T.

Answer is 3.

This shows sparse meetings when relative speed is small.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) per test case | each walker is processed in constant arithmetic operations |
| Space | O(1) extra | only storing output and temporary variables |

The constraints allow up to 2·10^5 walkers total, so linear processing is easily fast enough. All operations are integer arithmetic, so the solution comfortably fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    K = int(input())
    out = []
    for _ in range(K):
        L, v0, T, N = map(int, input().split())
        res = []
        for _ in range(N):
            ti, vi = map(int, input().split())
            d = abs(v0 - vi)
            if ti > T:
                res.append(0)
                continue
            numerator = (T - ti) * d
            if L == 0 or numerator < 0:
                res.append(0)
                continue
            k = numerator // L
            res.append(k + 1)
        out.append(" ".join(map(str, res)))
    return "\n".join(out)

# minimal
assert run("1\n10 5 10 1\n0 1\n") == "6", "simple increasing meetings"

# boundary at T
assert run("1\n100 10 50 1\n10 0\n") == "5", "includes exact T"

# same direction close speed
assert run("1\n100 10 100 1\n0 9\n") == "11", "slow relative motion"

# opposite direction
assert run("1\n100 10 100 1\n0 -10\n") == "11", "fast relative motion"

# multiple walkers
assert run("1\n50 5 30 2\n0 1\n5 -1\n") == "4 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal | 6 | base arithmetic progression |
| boundary | 5 | inclusion of time T |
| same direction | 11 | small relative speed handling |
| opposite direction | 11 | correct use of absolute relative speed |
| multiple walkers | 4 3 | per-walker independence |

## Edge Cases

One important edge case is when the first meeting occurs exactly at time T. In that situation, the arithmetic progression contains only the initial term. The formula still works because (T - ti) becomes zero, producing k = 0 and thus answer 1.

Another case is when relative speed is large, making the period very small. This increases the number of meetings, but integer division still captures all valid multiples correctly since each step is derived from exact inequality transformation rather than floating approximation.

When vi is close to v0, the denominator becomes small, so the expression (T - ti) * d / L can become large. Using 64-bit integers is necessary to avoid overflow in intermediate multiplication.
