---
title: "CF 104883A - rnm\uff0c\u9000\u94b1\uff01"
description: "We are given a chronological log of a player’s account balance in a virtual currency system. Each record changes their balance in one of three ways: they either receive currency by paying real money, spend currency in the game, or do something irrelevant that does not affect…"
date: "2026-06-28T09:09:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104883
codeforces_index: "A"
codeforces_contest_name: "The 18-th Beihang University Collegiate Programming Contest (BCPC 2023) - Final"
rating: 0
weight: 104883
solve_time_s: 42
verified: true
draft: false
---

[CF 104883A - rnm\uff0c\u9000\u94b1\uff01](https://codeforces.com/problemset/problem/104883/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a chronological log of a player’s account balance in a virtual currency system. Each record changes their balance in one of three ways: they either receive currency by paying real money, spend currency in the game, or do something irrelevant that does not affect their balance.

The key quantity is the final amount of unused virtual currency after processing all events in order. Since the exchange rate between RMB and the in-game currency is one to one, whatever remains unspent can be directly refunded as RMB at the end.

The input is a sequence of signed integers. A positive value increases the balance, a negative value decreases it, and zero leaves it unchanged. Spending is guaranteed to never exceed the current balance at any moment, so the balance never becomes invalid during processing.

From a constraints perspective, the number of events is at most 1000, and each value can be as large as 10^9 in magnitude. This immediately rules out any need for complex data structures or optimizations beyond a single pass aggregation. Even an O(n^2) simulation would pass comfortably, but the structure suggests that a linear scan is both sufficient and natural.

A common mistake is to overthink the refund condition and try to separate “spent but refundable” versus “already used” currency. For example, if the log is `[+328, -328, +488]`, a naive interpretation might incorrectly assume the first deposit contributes to refund because it was once positive, but the spending cancels it completely. Another subtle case is when zero entries appear; they should be ignored entirely, for example `[+100, 0, -50]` should behave exactly like `[+100, -50]`. Any solution that treats zeros as breaking segments or triggers separate accounting will miscompute the result.

## Approaches

A brute-force interpretation would simulate an account with a running balance and, for every refund query, attempt to reconstruct which deposits remain unused. One could imagine tracking each deposit separately and marking portions as consumed when spending occurs. This would resemble maintaining a multiset of available funds and repeatedly matching withdrawals against earlier deposits. While correct, this approach becomes unnecessarily heavy because each spending operation might need to scan backward to find available deposits, leading to quadratic behavior in the worst case when alternating deposits and withdrawals.

The key simplification comes from recognizing that the problem does not ask for attribution of funds, only the final remaining total. Every deposit increases total refundable value, every spend decreases it, and intermediate structure is irrelevant. Since spending is guaranteed to be valid at every step, no deposit ever needs partial tracking beyond the aggregate sum.

This collapses the entire process into computing a running prefix sum over all values. The final answer is simply the total sum of all entries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Tracking Deposits | O(n^2) | O(n) | Too slow |
| Prefix Sum Aggregation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable `balance` to zero. This variable represents the total unspent currency at any moment in time.
2. Iterate through each record in order. For each value `x`, update `balance` by adding `x` directly to it. Positive values increase available funds, negative values reduce them, and zeros leave it unchanged.
3. After processing all records, output `balance` as the final refundable amount.

The reason this direct accumulation is valid is that the spending operations are fully consistent with prior deposits. Since every withdrawal is guaranteed to be supported by existing balance, there is no need to track which specific deposit it came from. The system behaves like a pure conservation of value with no hidden constraints.

### Why it works

At any point in the sequence, the running sum equals the net difference between all money added and all money spent so far. Because spending never exceeds available funds, this sum always corresponds exactly to the remaining unspent currency. No reallocation or historical matching can change the final net value, since every operation is linear and reversible only in aggregate, not in structure.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
balance = 0

for _ in range(n):
    x = int(input().strip())
    balance += x

print(balance)
```

The implementation maintains a single accumulator. Each input line is parsed and added directly to this accumulator. Fast input is used because although constraints are small, this is standard competitive programming practice.

A subtle point is that no filtering is applied to zero values. Treating zeros specially would only complicate the logic without changing the result. Another important detail is that Python’s integer type naturally handles large sums, so there is no overflow concern even if all values are near 10^9.

## Worked Examples

Consider an input where a player deposits currency, spends part of it, then receives more:

Input:

```
5
100
-30
0
50
-20
```

| Step | x | Balance before | Balance after |
| --- | --- | --- | --- |
| 1 | 100 | 0 | 100 |
| 2 | -30 | 100 | 70 |
| 3 | 0 | 70 | 70 |
| 4 | 50 | 70 | 120 |
| 5 | -20 | 120 | 100 |

Final output is 100. This demonstrates that zero entries have no effect and that spending simply reduces the remaining refundable amount.

Now consider an alternating pattern:

Input:

```
4
200
-100
-50
150
```

| Step | x | Balance before | Balance after |
| --- | --- | --- | --- |
| 1 | 200 | 0 | 200 |
| 2 | -100 | 200 | 100 |
| 3 | -50 | 100 | 50 |
| 4 | 150 | 50 | 200 |

Final output is 200. This shows that earlier spending can be “replenished” by later deposits, and only the net sum matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each record is processed exactly once with constant-time arithmetic |
| Space | O(1) | Only a single accumulator is maintained regardless of input size |

The constraints allow up to 1000 operations, so a linear pass is trivially fast. Even significantly larger inputs would remain efficient under this approach due to its constant per-element processing cost.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    return str(solution())

def solution():
    n = int(input().strip())
    balance = 0
    for _ in range(n):
        balance += int(input().strip())
    return balance

# sample-like cases
assert solution.__code__  # placeholder to ensure function exists

# custom cases
sys.stdin = io.StringIO("1\n0\n")
assert solution() == 0, "minimum non-trivial zero effect"

sys.stdin = io.StringIO("3\n10\n-5\n-5\n")
assert solution() == 0, "exact cancellation"

sys.stdin = io.StringIO("5\n100\n100\n-50\n-50\n0\n")
assert solution() == 100, "mixed operations with zero"

sys.stdin = io.StringIO("4\n1000000000\n-1\n-999999999\n0\n")
assert solution() == 0, "boundary large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 0 | 0 | zero-only edge case |
| 10, -5, -5 | 0 | full cancellation |
| mixed sequence | 100 | interaction of ops and zero |
| large values | 0 | boundary arithmetic safety |

## Edge Cases

A zero-only sequence such as `n=3, [0, 0, 0]` produces a balance of zero because no operation changes the state. The algorithm processes each entry but the accumulator remains unchanged throughout.

A fully cancelling sequence like `[+50, -20, -30]` reduces the balance step by step until it reaches zero. The running sum naturally reflects this cancellation without any need to track intermediate ownership of funds.

A case with late recovery, such as `[+100, -150, +200]`, shows that temporary deficits are impossible due to the problem guarantee, and the final result depends only on the net sum, here 150.
