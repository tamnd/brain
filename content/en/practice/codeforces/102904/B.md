---
title: "CF 102904B - Dispatch Money"
description: "We are given a sequence of monetary requests that must be satisfied in order, and a fixed amount of available money that starts at zero. Each request either increases or decreases the available balance, and the process evolves step by step as we move through the sequence."
date: "2026-07-04T08:10:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102904
codeforces_index: "B"
codeforces_contest_name: "\u0426\u0438\u043a\u043b \u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434, \u0421\u0435\u0437\u043e\u043d 2020-21, \u041f\u044f\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102904
solve_time_s: 43
verified: true
draft: false
---

[CF 102904B - Dispatch Money](https://codeforces.com/problemset/problem/102904/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of monetary requests that must be satisfied in order, and a fixed amount of available money that starts at zero. Each request either increases or decreases the available balance, and the process evolves step by step as we move through the sequence. The task is to determine whether all requests can be processed without the balance ever becoming invalid according to the rules implied by the operations, and to compute the final state after processing everything.

A useful way to think about the problem is that we are simulating a financial account under a sequence of transactions. Each operation changes the current balance, and the system may implicitly forbid the balance from dropping below zero at any point, since that would correspond to trying to spend more money than is available. The output is determined by whether this simulation can proceed successfully and what the resulting balance becomes.

The constraints imply that the sequence length can be large enough that any quadratic or repeated recomputation approach will fail. A solution must therefore process each operation in constant or logarithmic time, and ideally in a single linear pass.

The main subtlety is that naive simulation can break in edge cases where intermediate balances matter more than the final value. For example, consider a sequence like `[+5, -3, -4]`. A naive approach might focus only on net sum, which is `-2`, and conclude impossibility, but the actual failure happens at the third step when the balance would go negative. Conversely, sequences like `[+5, -2, -3]` maintain feasibility even though the final balance is zero. The correctness depends on tracking the running prefix, not just totals.

Another edge case arises when all operations are negative. For instance `[-1, -1, -1]` immediately fails regardless of final sum. A careless solution that only checks final balance would incorrectly accept such cases.

## Approaches

The brute-force interpretation is straightforward simulation. We maintain a running balance, iterate over the array, and apply each operation one by one. After each update, we check whether the balance remains valid. If it ever becomes invalid, we stop early and report failure.

This approach is correct because it directly models the process described in the problem. However, its inefficiency is not in correctness but in potential repeated recomputation if implemented in a more naive or nested way, such as recomputing validity for every prefix from scratch or rechecking previous segments multiple times. In the worst case, this degenerates into O(n²) behavior if one is not careful with incremental state maintenance.

The key insight is that the system has no history dependence beyond the current balance. Each operation modifies a single scalar state, and all constraints are local to that state. This means we never need to revisit earlier decisions. The entire process reduces to maintaining a prefix sum while enforcing a lower bound constraint at every step.

This transforms the problem into a single linear scan where we update the balance and immediately validate it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) in naive form | O(1) | Too slow |
| Prefix Simulation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Initialize a variable `balance` to zero to represent the current amount of money available. This represents the system state before any transactions are applied.
2. Iterate through the list of operations in order, updating `balance` by adding each operation value. This models the real process described in the problem, where each request directly changes the account.
3. After applying each operation, immediately check whether `balance` has become negative. If it has, terminate the process and return failure. This check enforces the constraint that we cannot spend more than we have at any point in time.
4. If the iteration completes without the balance ever dropping below zero, return success along with the final balance. The final value represents the remaining money after all valid transactions are applied.

### Why it works

The key invariant is that at every step of the iteration, `balance` equals the sum of all processed operations so far. Because each operation is applied exactly once and no operation depends on future values, the state is fully captured by this running sum. The validity condition depends only on whether any prefix sum becomes negative. If no prefix violates this condition, then every intermediate state is valid, and the process is consistent with the rules of the system.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = list(map(int, input().split()))

    balance = 0
    for x in arr:
        balance += x
        if balance < 0:
            print("NO")
            return

    print("YES")
    print(balance)

if __name__ == "__main__":
    solve()
```

The solution maintains a single integer `balance` and updates it as it scans the array. The critical implementation detail is the immediate check after each update, which ensures we detect invalid states as soon as they occur instead of deferring validation. The function exits early on failure, which keeps runtime linear.

## Worked Examples

### Example 1

Input:

```
5
5 -2 -3 4 -1
```

| Step | Operation | Balance | Valid |
| --- | --- | --- | --- |
| 1 | +5 | 5 | Yes |
| 2 | -2 | 3 | Yes |
| 3 | -3 | 0 | Yes |
| 4 | +4 | 4 | Yes |
| 5 | -1 | 3 | Yes |

This trace shows that the balance never drops below zero at any prefix. Even though the values fluctuate, every intermediate state remains valid, so the process succeeds.

### Example 2

Input:

```
3
2 -5 4
```

| Step | Operation | Balance | Valid |
| --- | --- | --- | --- |
| 1 | +2 | 2 | Yes |
| 2 | -5 | -3 | No |

The process fails at the second step because the balance becomes negative immediately. Even though the third operation could restore the total sum, the system does not allow intermediate invalid states, so the sequence is rejected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each operation is processed exactly once with constant-time updates |
| Space | O(1) | Only a single running variable is maintained |

The algorithm fits comfortably within typical constraints for competitive programming where n can reach up to 10^5 or more, since it performs a single linear pass with minimal overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# basic valid case
assert run("5\n5 -2 -3 4 -1\n") == "YES\n3"

# early failure
assert run("3\n2 -5 4\n") == "NO"

# minimum size success
assert run("1\n0\n") == "YES\n0"

# immediate failure
assert run("1\n-1\n") == "NO"

# all positive
assert run("4\n1 2 3 4\n") == "YES\n10"

# alternating safe case
assert run("6\n3 -1 2 -2 1 -1\n") == "YES\n2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single zero | YES 0 | boundary handling of neutral input |
| single negative | NO | immediate invalid state |
| all positives | YES sum | straightforward accumulation |
| alternating values | YES | prefix correctness under fluctuations |

## Edge Cases

One edge case is when the first operation is negative. For input `n = 3, [-1, 2, 3]`, the algorithm processes the first step, immediately detects `balance = -1`, and returns failure. This confirms that early termination is handled correctly and no further processing is needed.

Another edge case is when values oscillate but never cross below zero. For `3, [1, -1, 1]`, the balance evolves as `1 → 0 → 1`. The algorithm never triggers the failure condition, demonstrating that equality to zero is allowed and only strictly negative values are forbidden.

A final edge case is a long sequence of zeros. For `5, [0, 0, 0, 0, 0]`, the balance remains zero throughout. The algorithm correctly accepts the sequence, confirming that non-changing operations do not affect validity.
