---
title: "CF 104380J - No 7"
description: "We are given a single positive integer x, and we need to move strictly downward to find the closest smaller integer that avoids a specific digit constraint: none of its decimal digits may be 7."
date: "2026-07-01T17:08:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104380
codeforces_index: "J"
codeforces_contest_name: "The Andover Computing Open (TACO) 2023"
rating: 0
weight: 104380
solve_time_s: 62
verified: true
draft: false
---

[CF 104380J - No 7](https://codeforces.com/problemset/problem/104380/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single positive integer `x`, and we need to move strictly downward to find the closest smaller integer that avoids a specific digit constraint: none of its decimal digits may be `7`. Among all integers less than `x`, we want the largest one that satisfies this restriction.

The task is fundamentally a search over integers below a given bound, but with a filter that excludes any number containing the digit `7`. The output is not just any valid number, but the maximum valid number under the constraint, which makes this a “closest valid predecessor” problem.

The constraint `x ≤ 10^4` means the search space is tiny. Even a linear scan from `x - 1` down to `1` performs at most ten thousand checks, and each check only inspects a few digits. This immediately rules out the need for any sophisticated digit DP or greedy reconstruction; even naive iteration fits comfortably within time limits.

Edge cases appear when `x` itself is just above a forbidden region. For example, if `x = 7000`, then numbers like `6999`, `6998`, and so on must be examined carefully until a valid one appears. A careless mistake is to decrement once and assume the result is valid, which fails immediately for inputs like `x = 70`, where `69` is valid but `69` is not always found if only a single step is taken. Another subtle case is when the answer crosses multiple digit boundaries, such as `x = 100`, where the answer is `99`, not `99` or something involving digit replacement logic.

## Approaches

The most direct strategy is to start from `x - 1` and repeatedly decrement until we find a number whose decimal representation does not contain the digit `7`. Each candidate is checked by converting it to a string and scanning its characters. This is correct because we explore all integers in descending order, guaranteeing that the first valid number encountered is the maximum valid one below `x`.

The inefficiency concern arises only if the forbidden digit causes long chains of invalid numbers. In the worst case, we might skip numbers like `70, 71, 72, ..., 79`, or larger patterns like `7000` downwards, but even then the total number of checks is bounded by `10^4`. Each check costs O(log x), so the total work is negligible.

The key observation is that there is no structural constraint linking digits except the exclusion of `7`. That removes any need for combinatorial reasoning over digits. A greedy decrement-and-test loop fully captures the solution space.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (decrement + check) | O(x · log x) | O(1) | Accepted |
| Optimal (same as brute, simplified reasoning) | O(x · log x) | O(1) | Accepted |

In this problem, the “optimal” solution is essentially the brute force solution justified by constraints.

## Algorithm Walkthrough

1. Start from the integer immediately below `x`. This is the largest possible candidate and ensures we search downward in correct order.
2. For each candidate number, check whether it contains the digit `7` by converting it to a string and scanning all characters. This step enforces the constraint directly without needing arithmetic digit extraction.
3. If the number contains no `7`, return it immediately. Because we are scanning downward, the first valid number is guaranteed to be the largest valid answer.
4. Otherwise, decrement the candidate by one and repeat the check.

The loop continues until a valid number is found. Since the domain is bounded by `x ≤ 10^4`, termination is guaranteed.

### Why it works

The algorithm maintains the invariant that every number greater than the current candidate and less than `x` has already been considered and rejected. Because we only move downward and never skip values, the first number that passes the digit filter must be the maximum valid number under `x`. There is no possibility of missing a better answer since all larger candidates are tested earlier in the sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def has_seven(n: int) -> bool:
    return '7' in str(n)

def solve():
    x = int(input().strip())
    cur = x - 1
    
    while cur > 0:
        if not has_seven(cur):
            print(cur)
            return
        cur -= 1
    
    print(0)

if __name__ == "__main__":
    solve()
```

The function `has_seven` isolates the digit-checking logic, making the main loop clearer and less error-prone. The loop begins at `x - 1` because the problem explicitly requires a strictly smaller number.

A subtle point is handling the case where no valid number exists above zero. Since `1 ≤ x ≤ 10^4`, and `0` does not contain a `7`, the loop will always terminate safely, but the guard ensures correctness even in degenerate reasoning.

## Worked Examples

### Example 1

Input: `8`

| cur | contains '7'? | action |
| --- | --- | --- |
| 7 | yes | skip |
| 6 | no | output |

The algorithm skips `7` because it violates the constraint and immediately returns `6`. This confirms that the scan correctly bypasses invalid single-digit values.

### Example 2

Input: `777`

| cur | contains '7'? | action |
| --- | --- | --- |
| 776 | yes | skip |
| 775 | yes | skip |
| ... | ... | continue |
| 700 | yes | skip |
| 699 | no | output |

This trace shows a long sequence of invalid candidates due to repeated digit `7`. The algorithm still finds the correct answer because it systematically checks every number downward without assumptions about digit structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(x · log x) | At most x decrements, each digit check costs O(log x) due to string conversion |
| Space | O(1) | Only a few integers and temporary string representation |

The constraints cap `x` at 10,000, so the worst-case number of iterations is tiny. Even a straightforward loop executes comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    x = int(sys.stdin.readline().strip())
    cur = x - 1
    
    while cur > 0:
        if '7' not in str(cur):
            print(cur)
            return
        cur -= 1
    
    print(0)

# provided samples
assert run("8\n") == "6"
assert run("777\n") == "699"

# custom cases
assert run("7\n") == "6", "single forbidden number"
assert run("10\n") == "9", "simple boundary"
assert run("100\n") == "99", "two-digit collapse"
assert run("71\n") == "69", "skipping across forbidden digit"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 7 | 6 | single forbidden value boundary |
| 10 | 9 | simple decrement case |
| 100 | 99 | digit boundary transition |
| 71 | 69 | skipping range containing forbidden digit |

## Edge Cases

For input `x = 7`, the algorithm sets `cur = 6`. The check `'7' in str(6)` is false immediately, so it outputs `6`. This confirms correct handling when the forbidden digit is exactly at the boundary.

For input `x = 70`, the algorithm starts at `69`. Since `69` contains no `7`, it is returned immediately. The sequence never evaluates `70` itself because the strict inequality is enforced at initialization.

For input `x = 100`, the algorithm evaluates `99` directly. Since neither digit is `7`, the output is `99`, demonstrating correct handling of carry-like digit transitions without explicit numeric reasoning.
