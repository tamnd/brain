---
title: "CF 1977A - Little Nikita"
description: "Nikita has a tower that starts empty, and he can perform exactly one of two operations per move: either place one cube on top or remove one cube from the top. The problem asks whether, after performing exactly n moves, the tower can have exactly m cubes."
date: "2026-06-08T17:15:08+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1977
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 948 (Div. 2)"
rating: 800
weight: 1977
solve_time_s: 92
verified: true
draft: false
---

[CF 1977A - Little Nikita](https://codeforces.com/problemset/problem/1977/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

Nikita has a tower that starts empty, and he can perform exactly one of two operations per move: either place one cube on top or remove one cube from the top. The problem asks whether, after performing exactly `n` moves, the tower can have exactly `m` cubes. Each test case provides the number of moves `n` and the desired height `m`. The output is "Yes" if this is possible, and "No" otherwise.

The constraints are small: both `n` and `m` are at most 100, and there are at most 100 test cases. This means any algorithm with complexity roughly `O(n)` per test case will run comfortably within the time limit. The problem is essentially about parity and reachability rather than exhaustive simulation.

Non-obvious edge cases occur when `m` is greater than `n` or when `m` and `n` have different parity. For example, if `n = 2` and `m = 3`, there is no way to reach three cubes in only two moves. Similarly, if `n = 3` and `m = 2`, the moves must leave the tower at height 2 after three operations, but since each move changes the height by exactly 1, the parity of `n` and `m` must match for it to be possible.

## Approaches

A brute-force approach would attempt to simulate all sequences of adding and removing cubes. For each move, you could recursively try adding or removing a cube and check whether the final height matches `m`. This works for very small inputs but has exponential complexity: each of `n` moves has two choices, so there are `2^n` possible sequences. Even with `n = 100`, this is infeasible.

The key insight is that the only factors limiting the final tower height are the total number of moves `n` and the parity of `m`. Every move changes the tower height by exactly one, so after `n` moves, the height difference from the starting point (zero) must be a number of the same parity as `n`. Additionally, the maximum height achievable is `n` if Nikita only adds cubes. Therefore, the conditions for reaching exactly `m` cubes are that `m` is at most `n` and `m` has the same parity as `n`. This reduces the problem to a simple check without simulation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read the integers `n` and `m`.
3. Check if `m` is less than or equal to `n`. If not, output "No" and continue.
4. Check if the parity of `n` and `m` matches, meaning `(n - m) % 2 == 0`. If it does, output "Yes"; otherwise, output "No".

The reason this works is that each move changes the tower height by exactly 1, so the difference between `n` and `m` must be an even number to reach exactly `m` after `n` moves. The condition `m <= n` ensures that Nikita does not need more moves than allowed to reach the desired height.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    if m <= n and (n - m) % 2 == 0:
        print("Yes")
    else:
        print("No")
```

The code reads input efficiently using `sys.stdin.readline`. For each test case, it immediately checks the two conditions: `m <= n` ensures we have enough moves to reach the height, and `(n - m) % 2 == 0` ensures that the number of up and down moves can be arranged to reach exactly `m`. This avoids unnecessary loops or recursion.

## Worked Examples

**Example 1:** `n = 3, m = 3`

| n | m | n - m | parity check | Result |
| --- | --- | --- | --- | --- |
| 3 | 3 | 0 | 0 % 2 == 0 | Yes |

The difference is zero, even, and `m <= n`, so reaching 3 cubes is possible by adding a cube on each move.

**Example 2:** `n = 2, m = 4`

| n | m | n - m | parity check | Result |
| --- | --- | --- | --- | --- |
| 2 | 4 | -2 | -2 % 2 == 0 | No |

Although the parity check is satisfied, `m > n` makes it impossible to reach height 4 in only 2 moves.

These traces show that both conditions are necessary and sufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is evaluated in constant time. |
| Space | O(1) | No additional memory beyond input storage. |

With `t` up to 100 and `n, m` up to 100, the solution runs comfortably in under 1 second and uses negligible memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        if m <= n and (n - m) % 2 == 0:
            print("Yes")
        else:
            print("No")
    return out.getvalue().strip()

# provided samples
assert run("3\n3 3\n2 4\n5 3\n") == "Yes\nNo\nYes", "sample 1"

# custom cases
assert run("4\n1 1\n2 2\n2 1\n100 100\n") == "Yes\nYes\nNo\nYes", "edge and max"
assert run("2\n1 2\n3 0\n") == "No\nYes", "parity and zero"
assert run("3\n10 10\n10 0\n10 5\n") == "Yes\nYes\nNo", "all-even, all-zero, mismatched parity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1, 2 2, 2 1, 100 100 | Yes, Yes, No, Yes | Minimum size, exact matches, impossible height, maximum size |
| 1 2, 3 0 | No, Yes | Parity mismatch, reaching zero cubes |
| 10 10, 10 0, 10 5 | Yes, Yes, No | Even maximum, zero, and impossible parity |

## Edge Cases

When `m = 0` and `n` is even, the algorithm correctly outputs "Yes" because Nikita can add and remove cubes alternately to end with an empty tower. For example, `n = 4, m = 0` results in `(n - m) % 2 = 0` and `m <= n`, so the output is "Yes".

When `m > n`, the algorithm immediately outputs "No", avoiding incorrect assumptions about negative moves. For example, `n = 3, m = 5` produces "No" even though the parity matches, because the height is unreachable.

When `n` and `m` differ in parity, the algorithm outputs "No", catching the subtle case where a sequence of ±1 moves cannot reach the target due to parity mismatch, such as `n = 5, m = 2`.
