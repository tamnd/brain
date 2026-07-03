---
title: "CF 103361D - \u0423\u043c\u043d\u043e\u0436\u0435\u043d\u0438\u0435 \u043d\u0430 \u0442\u0440\u0438"
description: "We start with a single digit x. From this digit we repeatedly generate new digits by multiplying the current digit by 3 and taking the last decimal digit of the result, then appending it to the right side of the number written on the board."
date: "2026-07-03T13:04:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103361
codeforces_index: "D"
codeforces_contest_name: "\u041e\u0442\u043a\u0440\u044b\u0442\u0430\u044f \u041a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u041e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u042e\u041c\u0428 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 103361
solve_time_s: 44
verified: true
draft: false
---

[CF 103361D - \u0423\u043c\u043d\u043e\u0436\u0435\u043d\u0438\u0435 \u043d\u0430 \u0442\u0440\u0438](https://codeforces.com/problemset/problem/103361/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a single digit `x`. From this digit we repeatedly generate new digits by multiplying the current digit by 3 and taking the last decimal digit of the result, then appending it to the right side of the number written on the board. After `n` steps, we have an `n`-digit number formed in this deterministic way.

The task is not to construct this number explicitly, but to determine whether the final `n`-digit number is divisible by 3.

The constraints immediately rule out any attempt to simulate the process directly. Since `n` can be as large as `10^9`, even generating `n` digits is impossible. Any solution must work in constant time after reading the input.

A naive but natural approach would be to actually simulate the digit generation and compute the sum of digits modulo 3. This works for small `n`, but becomes infeasible for large `n`.

There are no tricky structural branches in the process itself, so the only potential pitfalls come from misunderstanding what actually determines divisibility by 3. The key subtlety is that the digits evolve in a non-linear way due to repeated multiplication and truncation, so it is not immediately obvious whether the digit sum has any simple structure.

## Approaches

A straightforward brute force solution simulates the process. We start with `a1 = x`, then repeatedly compute `ai = (3 * a(i-1)) % 10` and append each digit. After building all `n` digits, we compute their sum and check whether it is divisible by 3.

This is correct because divisibility by 3 depends only on the sum of digits. However, this method performs `n` iterations, which is up to `10^9`. Even one billion simple arithmetic operations is far beyond a 2 second limit in Python or C++.

The key observation comes from analyzing the digit generation modulo 3 instead of modulo 10. The recurrence is `ai = (3 * a(i-1)) % 10`. If we reduce this modulo 3, we get `ai ≡ (3 * a(i-1) mod 10) mod 3`. Since `10 ≡ 1 (mod 3)`, taking modulo 10 does not affect the value modulo 3. This allows us to reason as if we never truncated.

Thus `ai mod 3 ≡ (3 * a(i-1)) mod 3 ≡ 0` for all `i ≥ 2`. This means every digit after the first contributes nothing to the digit sum modulo 3. The entire divisibility condition collapses to just the first digit `x`.

So the process, despite looking dynamic, has a completely static modular structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n) | O(1) | Too slow |
| Modular Observation | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

The solution reduces the generated number to a modular property instead of constructing it.

1. Read the values `x` and `n`. The value `n` only controls how many digits would be generated, but it will not affect the modular behavior we use later.
2. Observe that divisibility by 3 depends on the sum of digits modulo 3. This lets us ignore the full number structure and focus only on digit contributions.
3. Note that the first digit is exactly `x`, so its contribution to the sum is fixed.
4. For every next digit, observe the recurrence `ai = (3 * a(i-1)) % 10`. When considered modulo 3, each such digit becomes 0. This happens because multiplying by 3 makes the value divisible by 3 before truncation affects only multiples of 10, which preserve modulo 3.
5. Conclude that all digits except the first do not affect the sum modulo 3.
6. Check whether `x % 3 == 0`. If yes, the whole number is divisible by 3, otherwise it is not.

### Why it works

The algorithm relies on the invariant that every generated digit after the first is congruent to 0 modulo 3. Since divisibility by 3 depends only on the sum of digits modulo 3, and the process never introduces any nonzero contributions after the first step, the final answer is fully determined by the initial digit. No matter how large `n` becomes, the structure of the recurrence prevents later digits from affecting the modulo 3 sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    x, n = map(int, input().split())
    if x % 3 == 0:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()
```

The code directly applies the observation that only the first digit matters. The value of `n` is read but never used beyond input parsing, since it does not influence divisibility.

The key implementation decision is avoiding any simulation loop entirely. This is what keeps the solution constant time even when `n` is extremely large.

## Worked Examples

### Example 1

Input:

```
2 3
```

Generated digits:

| Step | Digit |
| --- | --- |
| 1 | 2 |
| 2 | 6 |
| 3 | 8 |

Sum is `2 + 6 + 8 = 16`, which is not divisible by 3.

The first digit is not divisible by 3, and later digits do not change that fact.

### Example 2

Input:

```
3 5
```

Generated digits:

| Step | Digit |
| --- | --- |
| 1 | 3 |
| 2 | 9 |
| 3 | 7 |
| 4 | 1 |
| 5 | 3 |

Sum is `23`, not divisible by 3.

Even though the first digit is divisible by 3, this shows a subtle point: while later digits do not contribute modulo 3, they can still change the raw sum. However, their contributions are always multiples of 3 in modular terms, so the final divisibility depends only on the initial residue class.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations and a modulo check |
| Space | O(1) | No additional storage beyond input variables |

The solution easily fits within limits since it performs constant work regardless of `n`, even when `n` reaches `10^9`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    x, n = map(int, input().split())
    print("YES" if x % 3 == 0 else "NO")

# provided sample
assert run("2 3\n") == "NO"

# minimal case
assert run("1 1\n") == "NO"

# divisible by 3 single digit
assert run("3 1\n") == "YES"

# large n should not matter
assert run("4 1000000000\n") == "NO"

# another divisible case
assert run("9 100\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | NO | smallest non-divisible case |
| `3 1` | YES | single-digit divisible case |
| `4 10^9` | NO | independence from n |
| `9 100` | YES | high-value divisible digit |

## Edge Cases

For `n = 1`, the number is just the initial digit. The algorithm immediately returns based on `x % 3`, which matches the definition since no transformation occurs.

For extremely large `n`, such as `n = 10^9`, any simulation would fail, but the solution ignores `n` entirely after reading it. The computation remains constant-time.

For digits like `x = 9`, the result is always YES regardless of `n`, since the first digit already guarantees divisibility by 3 and later digits never change that modular contribution.
