---
title: "CF 977A - Wrong Subtraction"
description: "The task describes a very specific way of reducing a positive integer repeatedly. Instead of simply subtracting one in the usual arithmetic sense, the operation depends on the last digit of the number."
date: "2026-06-17T01:26:22+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 977
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 479 (Div. 3)"
rating: 800
weight: 977
solve_time_s: 71
verified: true
draft: false
---

[CF 977A - Wrong Subtraction](https://codeforces.com/problemset/problem/977/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

The task describes a very specific way of reducing a positive integer repeatedly. Instead of simply subtracting one in the usual arithmetic sense, the operation depends on the last digit of the number. If the number ends in a non-zero digit, the number behaves normally and decreases by one. If it ends in zero, the number does not decrease in value directly, but instead drops its last digit entirely, which is equivalent to dividing by ten.

We are given an initial integer n and a number of operations k. Each operation transforms the number according to the rule above, and the goal is to determine the final value after applying exactly k such transformations.

The constraint n ≤ 10^9 implies the number has at most 10 digits. The number of operations k is at most 50, which is extremely small. This immediately rules out any need for optimization beyond straightforward simulation, since even a linear scan over k steps is trivial.

A naive mistake would be to interpret the operation as always subtracting one. For example, starting from 100, a naive approach would produce 99 after one step, but the correct operation removes the trailing zero, producing 10. Another subtle mistake is repeatedly converting between string and integer incorrectly or forgetting that removing a digit changes the magnitude of the number entirely, which affects subsequent steps.

Edge cases appear when the number contains multiple trailing zeros. For instance, starting at 1000 and applying one operation gives 100, not 999. Another edge case is when repeated removal of zeros quickly reduces the number of digits, changing the behavior of future operations significantly.

## Approaches

A brute-force approach directly applies the rule k times. Each step checks the last digit and either subtracts one or divides by ten. Since k is at most 50, this approach is already optimal in practice and requires no further optimization.

The key observation is that there is no hidden structure beyond local digit manipulation. Each operation depends only on the current last digit, and after each transformation the number changes in a way that preserves correctness for the next step. There is no need for precomputation or mathematical shortcuts because the process itself is already bounded by a small k.

Thus the optimal solution is simply simulation of the process exactly as described.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(k) | O(1) | Accepted |
| Optimal Simulation | O(k) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integers n and k from input. The value of n is the current working number, and k is how many transformations will be applied.
2. Repeat the following process exactly k times, since each iteration represents one application of Tanya’s operation.
3. Check the last digit of n using n % 10. This isolates the unit place without affecting the rest of the number.
4. If the last digit is non-zero, subtract one from n. This corresponds to a normal decrement in decimal representation.
5. If the last digit is zero, divide n by 10 using integer division. This removes the last digit entirely, shrinking the number of digits.
6. After completing all k iterations, output the resulting value of n.

### Why it works

At every step, the algorithm mirrors the exact transformation rule applied to the current state of the number. The operation depends only on the last digit, and after each transformation the resulting number becomes the new valid state for the next operation. Since each step is independent and fully determined by the current value, no additional history is required. The sequence of transformations is deterministic, so simulating them in order guarantees the final value matches the required process.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())

for _ in range(k):
    if n % 10 == 0:
        n //= 10
    else:
        n -= 1

print(n)
```

The solution reads the initial number and iteratively applies the k transformations. The condition `n % 10 == 0` directly implements the rule for trailing zeros. Integer division `//= 10` removes the last digit in that case, while subtraction handles all other cases.

The loop runs exactly k times, ensuring correctness without over-processing. Since k is small, no additional optimization is necessary.

## Worked Examples

### Example 1

Input:

```
512 4
```

| Step | Current n | Last digit | Operation | Next n |
| --- | --- | --- | --- | --- |
| 1 | 512 | 2 | subtract 1 | 511 |
| 2 | 511 | 1 | subtract 1 | 510 |
| 3 | 510 | 0 | divide by 10 | 51 |
| 4 | 51 | 1 | subtract 1 | 50 |

Final result is 50.

This trace shows how a single trailing zero causes a structural change in the number rather than a simple decrement, which is why digit-based logic is required.

### Example 2

Input:

```
1000 3
```

| Step | Current n | Last digit | Operation | Next n |
| --- | --- | --- | --- | --- |
| 1 | 1000 | 0 | divide by 10 | 100 |
| 2 | 100 | 0 | divide by 10 | 10 |
| 3 | 10 | 0 | divide by 10 | 1 |

Final result is 1.

This example highlights repeated digit removal, showing how quickly the number shrinks when trailing zeros dominate.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) | Each operation is a constant-time check and update applied k times |
| Space | O(1) | Only a single integer variable is updated in place |

The constraints guarantee k ≤ 50, so the runtime is effectively constant. Even in the worst case, the solution performs at most 50 simple arithmetic operations, which is trivial under the time limit.

## Test Cases

```python
import sys, io

def solve():
    n, k = map(int, sys.stdin.readline().split())
    for _ in range(k):
        if n % 10 == 0:
            n //= 10
        else:
            n -= 1
    print(n)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

# provided sample
assert run("512 4\n") == "50\n", "sample 1"

# minimum case
assert run("10 1\n") == "1\n", "single division"

# all non-zero digits
assert run("999 3\n") == "996\n", "simple decrements"

# multiple trailing zeros
assert run("1000 2\n") == "10\n", "repeated digit removal"

# boundary small number
assert run("2 1\n") == "1\n", "small decrement"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 1 | 1 | single digit removal |
| 999 3 | 996 | normal decrement chain |
| 1000 2 | 10 | repeated zero stripping |
| 2 1 | 1 | minimal decrement case |

## Edge Cases

One edge case occurs when the number ends in multiple zeros. For input `1000` with k = 2, the first operation reduces it to 100 by division, and the second reduces it to 10 by another division. The algorithm handles this naturally because each iteration re-evaluates the last digit after the structure changes.

Another edge case is when the number becomes a single digit early in the process. For example, starting from 10, the first operation produces 1, and subsequent operations continue to subtract or divide safely. The loop does not assume fixed digit length, so it remains correct as the number shrinks dynamically.

A final edge case is when n is just above a power of ten boundary, such as 1001. The subtraction sequence quickly creates a trailing zero, after which division occurs. Since each step always checks the current state, the transition between subtraction and division is always correctly handled without needing special-case logic.
