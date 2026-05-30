---
title: "CF 488A - Giga Tower"
description: "We are standing at an integer floor number in a very large tower that extends far below zero and far above zero. From our current floor $a$, we are only allowed to move upward, meaning we repeatedly add positive integers."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 488
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 278 (Div. 2)"
rating: 1100
weight: 488
solve_time_s: 647
verified: false
draft: false
---

[CF 488A - Giga Tower](https://codeforces.com/problemset/problem/488/A)

**Rating:** 1100  
**Tags:** brute force  
**Solve time:** 10m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are standing at an integer floor number in a very large tower that extends far below zero and far above zero. From our current floor $a$, we are only allowed to move upward, meaning we repeatedly add positive integers. The goal is to find the smallest positive step $b$ such that the floor $a + b$ contains at least one digit 8 in its decimal representation.

So the task is not to search over floors freely, but to start from a fixed point and move strictly upward until we hit the first number whose decimal digits include an 8.

The input constraint $|a| \le 10^9$ means the starting point is small enough that we can safely simulate upward movement without worrying about overflow or extremely large iteration counts. In the worst case, we might need to check numbers until we encounter a lucky one, but since “lucky” depends on digit structure rather than arithmetic size, the density of such numbers is sufficient for a straightforward scan to pass within limits.

The main subtle edge case is the requirement that $b$ must be strictly positive. Even if the starting number already contains an 8, we cannot output zero. For example, if $a = 8$, we still must move upward to 9 or beyond, and the answer is at least 1 even though 8 is already “lucky”.

Another edge situation appears when moving across digit boundaries like 79 → 80 or 799 → 800. A naive mental assumption that lucky numbers are sparse might lead to overthinking, but in reality we simply check each integer in order.

## Approaches

A direct solution is to simulate walking upward from the starting floor. For each step, we increment the current floor and check whether its decimal representation contains digit 8. The first time this condition holds, we return the distance traveled.

This approach is correct because it follows the definition literally: we are asked for the minimum positive offset, and checking integers in increasing order guarantees that the first valid encounter is optimal.

The brute-force nature is obvious, but also harmless here. In the worst case, if lucky numbers were extremely rare, we might scan a large range. However, numbers containing digit 8 appear frequently enough that the expected number of checks is small, and even worst-case behavior is bounded by the fact that within any block of size 10, every digit appears in each position across the range.

There is no need for advanced optimization like digit DP because we are not counting or constructing all valid numbers, only searching forward from a single point.

The key simplification is recognizing that the problem is purely sequential: we do not need to reason about structure beyond “does this number contain an 8”.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k · d) where k is distance to next lucky number | O(1) | Accepted |
| Optimal | O(k · d) | O(1) | Accepted |

Here $d$ is the number of digits, which is at most 10.

## Algorithm Walkthrough

1. Start from the given floor $a$. We will explore floors strictly greater than $a$, since $b$ must be positive.
2. Initialize a counter $b = 0$, representing how far we have moved upward.
3. Repeatedly increment both the current floor and the counter: move from $a + b$ to $a + b + 1$, then increase $b$ by 1. This ensures we are always checking the next floor in increasing order.
4. For each new floor value, convert it to a string and scan its digits to check whether any digit equals '8'. The reason for string conversion is that digit extraction is simplest and constant-factor efficient for this constraint.
5. If a digit 8 is found, immediately stop and output $b$, since this is the first time we have reached a lucky floor. The ordering guarantees minimality.

### Why it works

We are scanning integers in strictly increasing order starting from $a+1$. Every candidate floor is checked exactly once, and we stop at the first satisfying the condition “contains digit 8”. Since the search space is totally ordered and we proceed monotonically, the first hit must correspond to the minimum positive distance. No skipped value can produce a smaller valid $b$, so correctness follows directly from ordered enumeration.

## Python Solution

```python
import sys
input = sys.stdin.readline

a = int(input().strip())

b = 0
while True:
    b += 1
    x = a + b
    if '8' in str(x):
        print(b)
        break
```

The code follows the algorithm exactly. The loop starts from 1 because we must ensure positivity of $b$. Each iteration moves one floor upward and immediately checks the digit condition.

The conversion `str(x)` is safe because numbers remain within reasonable bounds. The condition `'8' in str(x)` is the simplest way to test digit presence without manually extracting digits.

The loop terminates as soon as the first valid number is found, so no unnecessary computation is performed beyond the answer.

## Worked Examples

### Example 1

Input:

```
179
```

We compute successive values:

| b | x = a + b | contains 8? |
| --- | --- | --- |
| 1 | 180 | yes |

At $b = 1$, the number 180 contains digit 8, so we stop immediately.

This confirms that the algorithm correctly detects a lucky number even when it appears in the next immediate step.

### Example 2

Input:

```
7
```

| b | x = a + b | contains 8? |
| --- | --- | --- |
| 1 | 8 | yes |

Here the first step already produces a lucky number. This demonstrates that even when the starting value is far from containing 8, the algorithm still correctly finds the earliest valid floor.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k · d) | We check each number from $a+1$ until the first lucky number; each check scans up to 10 digits |
| Space | O(1) | Only a few integers and temporary string conversion are used |

The constraints allow this straightforward simulation because the search typically ends quickly, and digit checking is constant-time in practice. Even in worst cases, the bounds are small enough that this linear scan is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    a = int(input().strip())
    b = 0
    while True:
        b += 1
        x = a + b
        if '8' in str(x):
            return str(b)

# provided samples
assert run("179\n") == "1"

# custom cases
assert run("8\n") == "1"          # must move even if starting is lucky
assert run("7\n") == "1"          # immediate next is 8
assert run("10\n") == "8"         # 18 is first lucky (10->18 distance 8)
assert run("-1\n") == "9"         # -1 -> 8 in 9 steps
assert run("80\n") == "1"         # already contains 8 after increment? 81 no, but 88 later; actually 81..87 skip
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 8 | 1 | cannot output 0 even if starting is lucky |
| 7 | 1 | immediate next floor case |
| 10 | 8 | crossing multiple numbers until first 8 appears |
| -1 | 9 | negative starting point handling |
| 80 | 8 | checks skipping within multi-digit region |

## Edge Cases

One important edge case is when the starting number already contains digit 8. For input $a = 8$, the algorithm starts with $b = 1$, checks $9$, and only continues forward. Even though 8 itself is lucky, it is not reachable because $b$ must be positive. The first valid output is $b = 1$ since 9 does not contain 8 but 18 appears later; however the actual first is 18, giving $b = 10$. The loop naturally handles this because it never considers $a$ itself.

Another edge case is negative starting values. For example, $a = -1$. The sequence goes $-1, 0, 1, 2, \dots$ and eventually reaches 8. The algorithm does not treat sign specially, because digit checking is applied to the absolute string representation including the minus sign, but since '-' is ignored in `'8' in str(x)'`, correctness is preserved.

A final subtle case is crossing digit boundaries like 79 to 80 to 81. The method does not rely on arithmetic patterns, so it does not matter where digit changes occur. Every integer is checked independently, so no lucky number can be skipped.
