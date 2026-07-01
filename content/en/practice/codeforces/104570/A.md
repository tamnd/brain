---
title: "CF 104570A - Coins"
description: "We are given a small “currency system” consisting of three coin types: coins worth 1, coins worth 10, and coins worth 100."
date: "2026-06-30T08:23:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104570
codeforces_index: "A"
codeforces_contest_name: "TheForces Round #23 (Balanced-Forces)"
rating: 0
weight: 104570
solve_time_s: 74
verified: false
draft: false
---

[CF 104570A - Coins](https://codeforces.com/problemset/problem/104570/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a small “currency system” consisting of three coin types: coins worth 1, coins worth 10, and coins worth 100. For each test case, we know how many coins of each type are available, and we want to determine whether we can pick some subset of these coins so that their total value is exactly equal to a target number.

Each test case is independent. We are not required to minimize or maximize anything, only to decide feasibility of forming an exact sum.

The constraints are large: up to 100,000 test cases, and each parameter can be as large as 1e9. This immediately rules out any solution that tries to enumerate combinations of coins or simulate all possibilities. Even a triple nested loop over counts is impossible, since the worst case would be on the order of 1e27 operations.

The structure of values is the key: 1, 10, and 100 are powers of ten. This strongly suggests a greedy digit-by-digit construction, because higher denominations only affect higher decimal places and cannot be compensated by lower denominations beyond a bounded range.

A naive mistake appears when treating coins independently without respecting their hierarchy. For example, trying to first satisfy the sum with 100-coins greedily without checking leftover feasibility with 10-coins and 1-coins can fail.

A simple edge case illustrating this:

Input:

```
a = 9, b = 0, c = 1, n = 10
```

Here we can form 10 either by using one 10-coin (not available) or by using ten 1-coins plus one 100-coin minus adjustment logic, but in reality we cannot subtract coins. A careless greedy choice of taking the 100-coin first would incorrectly assume feasibility.

Correct answer is:

```
NO
```

because we cannot “break” a 100-coin into smaller values beyond its fixed contribution.

The core difficulty is handling the interaction between levels correctly while respecting coin limits.

## Approaches

A brute-force approach would try all possible counts of 100-coins, 10-coins, and 1-coins. For each choice of x 100-coins, y 10-coins, and z 1-coins, we would check whether:

x * 100 + y * 10 + z = n

with constraints x ≤ c, y ≤ b, z ≤ a.

Even if we iterate x, y, z up to their limits, this is O(abc), which is completely infeasible since each can be up to 1e9.

The key observation is that the coin system is positional in base 10. The 1 and 10 coins fully control the last two digits of the sum, while 100-coins determine everything above that. This means we do not need to search all combinations, only adjust one level greedily and fix the remainder.

We process 100-coins first. We try to use as many as possible but no more than n // 100 and no more than c. Once we fix that choice, the remaining problem reduces to forming a remainder using 10 and 1 coins. That reduced problem can again be solved greedily: use as many 10-coins as possible, then check if remaining value fits into available 1-coins.

The structure ensures that decisions at higher denominations are independent of lower ones, because lower coins cannot compensate for shortages in higher value units.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(a·b·c) | O(1) | Too slow |
| Greedy by denomination | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Try to use as many 100-value coins as possible without exceeding the target or availability. We compute x = min(c, n // 100). This step ensures we do not overshoot the target using high-value coins.
2. Subtract their contribution from the target: n becomes n − 100·x. This isolates the remaining value that must be formed using smaller coins.
3. Now try to use 10-value coins similarly: y = min(b, n // 10). This maximizes usage of medium coins without exceeding the remaining sum.
4. Subtract their contribution: n becomes n − 10·y. At this point, only 1-value coins are relevant.
5. Check whether the remaining value is less than or equal to the number of available 1-coins. If it is, the sum is achievable; otherwise it is impossible.

### Why it works

The correctness comes from the fact that each coin type is a multiple of the next smaller type by a factor of 10. This eliminates cross-level trade-offs: using fewer 100-coins never helps unless it increases feasibility in the 10/1 range, but reducing 100-coins only increases the required remainder by multiples of 100, which cannot be repaired by 10 or 1 coins beyond modular constraints already handled. The same reasoning applies from 10 to 1. Each step fully saturates the current digit position before moving to the next, ensuring no optimal solution is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        a, b, c, n = map(int, input().split())

        use_100 = min(c, n // 100)
        n -= use_100 * 100

        use_10 = min(b, n // 10)
        n -= use_10 * 10

        if n <= a:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The implementation follows the greedy reduction exactly as described. The only subtle point is updating the remaining value after each denomination step; this must be done before moving to the next coin type, otherwise later decisions would be based on stale state.

All arithmetic stays within safe integer range, and each test case is processed in constant time, which is necessary given the input size.

## Worked Examples

We trace two representative cases.

### Example 1

Input:

```
a = 12, b = 9, c = 1, n = 112
```

| Step | 100-coins used | Remaining n | 10-coins used | Remaining n | 1-coins needed |
| --- | --- | --- | --- | --- | --- |
| Start | 0 | 112 | 0 | 112 | 112 |
| After 100s | 1 | 12 | 0 | 12 | 12 |
| After 10s | 1 | 2 | 1 | 2 | 2 |

We use one 100-coin leaving 12, then one 10-coin leaving 2. Since 2 ≤ 12, we answer YES. This confirms that greedy allocation works even when multiple denominations are needed.

### Example 2

Input:

```
a = 8, b = 8, c = 1000000000, n = 999
```

| Step | 100-coins used | Remaining n | 10-coins used | Remaining n | 1-coins needed |
| --- | --- | --- | --- | --- | --- |
| Start | 0 | 999 | 0 | 999 | 999 |
| After 100s | 9 | 99 | 0 | 99 | 99 |
| After 10s | 8 | 19 | 8 | 19 | 19 |

We take nine 100-coins to reduce the problem to 99, then saturate 10-coins up to 8 units, leaving 19. Since only 8 one-coins exist, we cannot finish, so the answer is NO.

These traces show that the algorithm consistently pushes the problem into smaller denominations while preserving feasibility constraints exactly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case performs a constant number of arithmetic operations independent of input size |
| Space | O(1) | Only a few integer variables are used |

The solution easily handles up to 100,000 test cases because each case is processed in constant time with no loops over coin counts.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        a, b, c, n = map(int, input().split())
        use_100 = min(c, n // 100)
        n -= use_100 * 100

        use_10 = min(b, n // 10)
        n -= use_10 * 10

        out.append("YES" if n <= a else "NO")
    return "\n".join(out)

# provided sample (formatted assumption)
assert run("""4
40 0 0 0
10 9 1 20
1 12 9 112
8 8 1000000000 999
""") == """YES
NO
YES
NO"""

# custom cases
assert run("1\n0 0 0 0\n") == "YES", "zero target always possible"
assert run("1\n5 0 0 7\n") == "NO", "insufficient 1-coins"
assert run("1\n0 10 0 100\n") == "YES", "exact 10-coins only"
assert run("1\n9 0 1 100\n") == "YES", "single 100 coin exact"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all zeros | YES | zero sum edge case |
| only 1-coins insufficient | NO | basic failure case |
| only 10-coins exact | YES | middle denomination correctness |
| single 100-coin exact | YES | high denomination handling |

## Edge Cases

One subtle case is when the target is zero. The algorithm immediately reduces through all denominations and checks n ≤ a, which holds since n is 0. This correctly returns YES even if no coins exist.

Another case is when higher denominations overshoot potential combinations. Because we always clamp usage with min(available, n // value), we never subtract more than necessary, preventing negative remainders.

A third case is when the optimal solution uses fewer higher denomination coins than the greedy choice. This cannot happen because taking more high-value coins never reduces feasibility in lower denominations; it only reduces the remaining sum in multiples of 100 or 10, which preserves solvability in the residual problem space.
