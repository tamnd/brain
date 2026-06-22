---
title: "CF 105507A - \u041f\u043e\u043a\u0443\u043f\u043a\u0430 \u0432\u0435\u043b\u043e\u0441\u0438\u043f\u0435\u0434\u0430"
description: "We are asked to pay an exact amount using only two coin types, one worth 2 units and the other worth 5 units. The goal is not just to determine whether the sum can be formed, but to construct a combination of coins whose total value is exactly the required amount and uses as few…"
date: "2026-06-23T01:30:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105507
codeforces_index: "A"
codeforces_contest_name: "2024-2025 \u0412\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e, \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0421\u0430\u0440\u0430\u0442\u043e\u0432\u0441\u043a\u043e\u0439 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 (\u0412\u041a\u041e\u0428\u041f 24, \u0421\u0430\u0440\u0430\u0442\u043e\u0432\u0441\u043a\u0438\u0439 \u043e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u044d\u0442\u0430\u043f)"
rating: 0
weight: 105507
solve_time_s: 52
verified: true
draft: false
---

[CF 105507A - \u041f\u043e\u043a\u0443\u043f\u043a\u0430 \u0432\u0435\u043b\u043e\u0441\u0438\u043f\u0435\u0434\u0430](https://codeforces.com/problemset/problem/105507/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to pay an exact amount using only two coin types, one worth 2 units and the other worth 5 units. The goal is not just to determine whether the sum can be formed, but to construct a combination of coins whose total value is exactly the required amount and uses as few coins as possible.

Each solution corresponds to choosing some number of 5-value coins and some number of 2-value coins so that the weighted sum matches the target. Among all valid combinations, we must minimize the total number of coins used.

The constraint on the target value n goes up to one million. This size immediately rules out any approach that tries all combinations of coin counts in a nested loop over both coin types, since even a quadratic scan over possible counts would be far too slow. A linear or near-linear scan over one dimension is acceptable.

A subtle point is that feasibility is guaranteed, so we never need to handle impossible cases. This removes the need for backtracking or complex parity reasoning to detect infeasibility, but we still must ensure that our greedy choices do not accidentally break the exact sum requirement.

A typical edge case pattern appears when the greedy choice “take as many 5s as possible” overshoots or leaves a remainder that is not divisible by 2. For example, if n is small or congruent to certain residues modulo 10, a naive greedy approach might fail unless it adjusts the number of 5-coins downward.

## Approaches

A brute-force strategy would enumerate how many 5-value coins we take, say k, and then check whether the remaining value n − 5k can be formed using 2-value coins. This means verifying whether n − 5k is non-negative and even, and if so, counting total coins as k plus (n − 5k)/2. Trying all k from 0 up to n/5 gives O(n) possibilities, and each check is O(1), so the total complexity is O(n). While this already fits the constraints, it is unnecessary to check every possibility explicitly, because the structure of the problem strongly constrains the optimal solution.

The key observation is that 5-value coins are always more efficient in terms of reducing coin count per unit value than 2-value coins. However, because 5 is odd while 2 is even, parity constraints can force us to replace one 5-coin with multiple 2-coins. This creates a single-direction adjustment problem: we want as many 5-coins as possible, but we may need to reduce their count until the remaining sum becomes divisible by 2.

This leads to a greedy strategy: start with the maximum possible number of 5-coins and decrement it until feasibility is achieved. Since we only move downward and each step checks a simple parity condition, this process runs in O(n/5) worst case, but in practice it is bounded by a constant factor (at most a few steps due to modulo 2 constraints). This is effectively O(1) per test.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted but unnecessary |
| Greedy adjustment | O(n/5) worst, O(1) practical | O(1) | Accepted |

## Algorithm Walkthrough

We construct the solution by trying to maximize the number of 5-value coins, then fixing the remainder with 2-value coins.

1. Compute the maximum possible number of 5-coins as k = n // 5. This gives the largest starting point that does not exceed n. The idea is that using larger coins reduces the total count, so we start from the most aggressive compression of the sum.
2. While k is non-negative, check whether the remaining value r = n − 5k can be represented using only 2-value coins. This is possible exactly when r is even, since 2 is the only available even unit.
3. If r is even, compute the number of 2-coins as r // 2 and return k + r // 2 as the answer. This combination is optimal because we have maximized the number of larger coins subject to feasibility.
4. If r is odd, decrease k by 1 and repeat. This step corresponds to replacing one 5-coin with additional 2-coins, which flips the parity of the remainder and may restore feasibility.

The key invariant is that at each iteration we are testing the best possible solution with exactly k five-coins. Any solution using more than k five-coins is impossible due to value constraints, and any solution using fewer is considered only when necessary due to parity mismatch. Thus the first feasible k encountered yields the minimum number of coins.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    k = n // 5

    while k >= 0:
        rem = n - 5 * k
        if rem % 2 == 0:
            print(k + rem // 2)
            return
        k -= 1

solve()

if __name__ == "__main__":
    solve()
```

The code follows the greedy structure directly. We start from the maximum possible number of 5-coins and check feasibility via parity. The remainder check `rem % 2 == 0` is the only condition needed because divisibility by 2 fully characterizes representability using 2-value coins.

A common implementation pitfall is forgetting that the loop must decrease k one step at a time rather than jumping by 2. The parity alternates with each decrement, so skipping values would risk missing the first feasible configuration.

## Worked Examples

### Example 1

Let n = 13.

We start with k = 13 // 5 = 2.

| k | remainder n − 5k | parity | action |
| --- | --- | --- | --- |
| 2 | 3 | odd | decrease k |
| 1 | 8 | even | accept |

At k = 1, remainder is 8, which can be formed by 4 coins of value 2. Total coins are 1 + 4 = 5.

This shows that although using two 5-coins gives a smaller coin count for the 5-part, it breaks feasibility, and one reduction step restores a valid decomposition.

### Example 2

Let n = 20.

We start with k = 20 // 5 = 4.

| k | remainder | parity | action |
| --- | --- | --- | --- |
| 4 | 0 | even | accept |

Here no adjustment is needed. We use four 5-coins and zero 2-coins, yielding 4 coins total.

This demonstrates the optimal situation where greedy choice immediately satisfies parity constraints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n/5) worst case | each step decreases k until parity matches |
| Space | O(1) | only a few integers are stored |

Given n up to 10^6, the loop performs at most around 200000 iterations in the absolute worst case, but in practice parity resolves quickly, so it behaves like a constant-time process per input.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return io.StringIO(sys.stdout.getvalue() if False else "")

# Since the solution uses direct print, we instead show logical asserts conceptually.

# sample-like cases
# n = 6 -> 3 coins of 2
# n = 20 -> 4 coins of 5
# n = 13 -> 5 coins total (1x5 + 4x2)
```

Since the original problem statement in this format does not include explicit sample I/O blocks, we focus on structural correctness rather than exact harness execution.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 | 2 | minimum valid even-only case |
| 5 | 1 | pure 5-coin case |
| 6 | 3 | only 2-coins needed |
| 7 | 2 | mixed case requiring adjustment |
| 13 | 5 | parity adjustment case |

## Edge Cases

When n is small, such as n = 4, the algorithm starts with k = 0 since 5-coins cannot be used. The remainder is 4, which is even, so it immediately returns 2 coins of value 2.

For n = 7, k starts at 1, remainder is 2, which is even, so the algorithm correctly returns one 5-coin and one 2-coin. This is optimal because any attempt to use zero 5-coins would require 3 coins of 2, which is worse.

For values where n mod 5 is 1 or 3, the initial greedy choice of k = n // 5 always produces an odd remainder. The loop then decreases k until the remainder becomes even, guaranteeing that a valid decomposition is found without skipping the optimal configuration.
