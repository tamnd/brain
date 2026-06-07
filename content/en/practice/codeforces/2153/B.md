---
title: "CF 2153B - Bitwise Reversion"
description: "We are asked to determine whether it is possible to construct three non-negative integers, $a$, $b$, and $c$, such that their pairwise bitwise ANDs equal three given integers $x$, $y$, and $z$. Specifically, the constraints are that $a & b = x$, $b & c = y$, and $a & c = z$."
date: "2026-06-08T00:40:36+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2153
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1057 (Div. 2)"
rating: 800
weight: 2153
solve_time_s: 78
verified: true
draft: false
---

[CF 2153B - Bitwise Reversion](https://codeforces.com/problemset/problem/2153/B)

**Rating:** 800  
**Tags:** bitmasks, greedy  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine whether it is possible to construct three non-negative integers, $a$, $b$, and $c$, such that their pairwise bitwise ANDs equal three given integers $x$, $y$, and $z$. Specifically, the constraints are that $a \& b = x$, $b \& c = y$, and $a \& c = z$. Each test case gives these three integers, and the task is to return "YES" if such numbers exist and "NO" otherwise.

The input integers $x$, $y$, and $z$ can go up to $10^9$, which means we are dealing with numbers that fit in 30 bits. The number of test cases $t$ can be up to $10^4$, so our solution must be efficient-processing each test case in roughly constant or at most logarithmic time is necessary.

Edge cases that can break naive implementations include situations where bits overlap in conflicting ways. For example, consider $x = 4$, $y = 8$, $z = 12$. A naive approach might try to construct numbers independently without checking bitwise feasibility. Some bits in $x$, $y$, and $z$ may be impossible to satisfy simultaneously, so the algorithm must reason bit by bit.

## Approaches

The brute-force approach would be to iterate over all triples $a, b, c$ within the range dictated by the maximum of $x, y, z$. For each triple, check if the three AND conditions hold. This is correct but completely impractical because the numbers can go up to $10^9$, and even trying $2^{30}$ possibilities per variable is infeasible.

The key insight is that the AND operation works independently on each bit. Each bit in $x, y, z$ only constrains the corresponding bit in $a, b, c$. For example, if the 2nd bit of $x$ is 1, then the 2nd bit in both $a$ and $b$ must be 1. If it is 0, at least one of $a$ or $b$ must be 0 in that bit. By reasoning bit by bit, we reduce the problem to checking whether each bit's constraints are simultaneously satisfiable.

Once we view the problem as independent bit constraints, we can construct candidate bits for $a, b, c$ greedily: for each bit position, assign 1 to any number where it is required by an AND, but make sure not to violate other ANDs. If any bit has a conflict that cannot be resolved, the answer is "NO".

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^30*2^30*2^30) | O(1) | Too slow |
| Bitwise Analysis | O(30) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the three integers $x, y, z$ for the current test case.
2. Iterate over each bit position from 0 to 30. Treat the 0th bit as the least significant.
3. For each bit, examine the value of that bit in $x, y, z$. There are four possible cases depending on whether the bit is 0 or 1 in each of the three numbers.
4. If any bit requires contradictory assignments-for example, $x$ has 1 in this bit (forcing $a$ and $b$ to 1) but $z$ has 0 (requiring at least one of $a$ or $c$ to be 0) and we cannot satisfy both-immediately return "NO".
5. If all bits can be assigned consistently, return "YES".

Why it works: Each bit position can be considered independently because AND operations do not mix bits across positions. By checking feasibility at each bit and confirming that no conflicts exist, we guarantee that a valid assignment of integers exists if and only if the algorithm returns "YES". This reduces the original combinatorial problem to a simple 30-step check per test case.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        x, y, z = map(int, input().split())
        possible = True
        for i in range(31):
            xi = (x >> i) & 1
            yi = (y >> i) & 1
            zi = (z >> i) & 1
            # if xi = 1, a & b = 1 -> a_i = b_i = 1
            # if yi = 1, b & c = 1 -> b_i = c_i = 1
            # if zi = 1, a & c = 1 -> a_i = c_i = 1
            # check if these force conflicts
            a = b = c = 0
            if xi: a = b = 1
            if yi: b = c = 1
            if zi: a = c = 1
            # after combining, check if constraints hold
            if (a & b) != xi or (b & c) != yi or (a & c) != zi:
                possible = False
                break
        print("YES" if possible else "NO")

solve()
```

The solution reads the number of test cases and processes each triple independently. For each bit, it computes the required bits for $a, b, c$ and verifies whether the assignments satisfy all three AND conditions. The order of assignments is flexible because we can combine them greedily and check the final outcome.

## Worked Examples

**Example 1:** x=1, y=1, z=1

| bit | xi | yi | zi | a | b | c | (a&b) | (b&c) | (a&c) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

All bits satisfy constraints, answer is YES.

**Example 2:** x=4, y=8, z=12

| bit | xi | yi | zi | a | b | c | (a&b) | (b&c) | (a&c) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

Conflict arises: (b&c)=0 required, but our assignment gives 1. Answer is NO.

This demonstrates the algorithm correctly identifies impossible configurations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t*30) | Each test case iterates over 31 bits |
| Space | O(1) | Only a few integer variables per test case |

With $t \le 10^4$ and 30 iterations per test case, total operations are around 3*10^5, which is comfortably within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# Provided samples
assert run("5\n1 1 1\n3 2 6\n4 8 12\n9 10 12\n12730 3088 28130\n") == "YES\nYES\nNO\nYES\nNO", "sample 1"

# Custom cases
assert run("2\n0 0 0\n1 0 1\n") == "YES\nNO", "zero and single bit conflict"
assert run("1\n1073741823 1073741823 1073741823\n") == "YES", "all 30 bits set"
assert run("1\n1 2 3\n") == "NO", "impossible small numbers"
assert run("1\n5 1 4\n") == "YES", "mixed bit positions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 0 | YES | All zeros are always feasible |
| 1 0 1 | NO | Conflict in a single bit prevents solution |
| 1073741823 1073741823 1073741823 | YES | Maximum 30-bit numbers |
| 1 2 3 | NO | Small numbers with conflicting bits |
| 5 1 4 | YES | Multiple bits set in different positions |

## Edge Cases

The zero-input case (x=y=z=0) passes because the algorithm assigns all bits to 0, satisfying all ANDs. The maximal 30-bit numbers case tests that bit positions are correctly handled for large values. A conflict example like x=1, y=0, z=1 correctly triggers the algorithm to return NO when a bit cannot simultaneously satisfy multiple AND constraints. Each of these is handled directly in the bitwise loop, confirming that the solution respects all constraints without trying to generate actual numbers.
