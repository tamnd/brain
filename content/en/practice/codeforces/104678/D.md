---
title: "CF 104678D - Basic examination"
description: "We are given a string made only of opening and closing parentheses. The task is to decide whether this sequence could arise from some valid arithmetic expression after stripping away everything except parentheses."
date: "2026-06-29T09:06:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104678
codeforces_index: "D"
codeforces_contest_name: "October come back. Together training"
rating: 0
weight: 104678
solve_time_s: 52
verified: true
draft: false
---

[CF 104678D - Basic examination](https://codeforces.com/problemset/problem/104678/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string made only of opening and closing parentheses. The task is to decide whether this sequence could arise from some valid arithmetic expression after stripping away everything except parentheses.

A key observation is that any arithmetic expression, once numbers and operators are removed, leaves only the structure imposed by parentheses. That structure is valid exactly when every closing bracket matches a previously opened one, and no prefix ever closes more brackets than have been opened.

So the input is simply a candidate bracket structure, and the output is a binary decision: whether this structure could correspond to a correctly formed expression.

The constraint n up to 200000 immediately rules out any quadratic simulation or repeated rescanning. Any solution that tries to match pairs by searching or repeatedly modifying the string will be too slow. A linear scan is the only realistic option.

A few edge situations expose common mistakes.

If the string starts with a closing bracket, such as input `")("`, it is impossible to interpret it as coming from any valid expression, because there is no earlier context that could supply a matching opening bracket. The correct output is `NO`.

If the string has correct total counts but invalid ordering, such as `"())("`, the total number of opens equals closes, yet at some prefix the sequence becomes invalid. The correct output is still `NO`, which shows that balance alone is not sufficient.

If the string is perfectly balanced like `"(())()"`, both ordering and counts align, and the answer is `YES`.

## Approaches

A brute-force way to validate the structure is to repeatedly search for adjacent matching pairs `"()"` and remove them until no more removals are possible. If the string becomes empty, it is valid.

This works because every valid bracket pair must eventually be matched and removed. However, each removal potentially shifts the string and forces rescanning. In the worst case, such as `"((((....))))"`, each removal scans almost the entire string again. With n up to 200000, this leads to roughly O(n^2) operations, which is far too slow.

The key structural insight is that validity depends only on whether we ever encounter more closing brackets than available openings when reading left to right. Instead of simulating removals, we maintain a counter representing how many unmatched opening brackets exist at each step.

Whenever we see `'('`, we increase the counter. Whenever we see `')'`, we must have at least one unmatched `'('` available; otherwise the sequence is invalid immediately. At the end, the sequence is valid only if no unmatched openings remain.

This transforms the problem into a single pass with constant work per character.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force removal simulation | O(n²) | O(n) | Too slow |
| Single-pass counter | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We scan the string from left to right while tracking a single integer representing the number of currently open but unmatched parentheses.

1. Initialize a counter `balance = 0`. This represents how many `'('` have been seen that are not yet matched by a `')'`.
2. Iterate through each character in the string.
3. If the character is `'('`, increment `balance` by one. This reflects introducing a new unmatched opening bracket.
4. If the character is `')'`, decrement `balance` by one. Before or after decrementing, we must ensure that `balance` is not already zero, because that would mean we are trying to close a bracket that does not exist. If this happens, the sequence cannot correspond to any valid expression.
5. If at any point `balance` becomes negative, immediately conclude the sequence is invalid.
6. After processing the entire string, check whether `balance` equals zero. If it does, every opening bracket has been matched; otherwise some remain unmatched and the sequence is invalid.

The correctness hinges on the fact that at any prefix, the number of closing brackets cannot exceed the number of opening brackets in any valid expression.

### Why it works

The algorithm maintains an invariant: after processing each prefix, `balance` equals the number of unmatched opening brackets in that prefix, assuming the prefix is valid so far. Each `'('` introduces a new unmatched requirement, and each `')'` removes exactly one such requirement. If a closing bracket appears when no requirement exists, it violates the fundamental pairing constraint of well-formed parentheses, making the entire sequence impossible to derive from any valid expression.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    s = input().strip()

    balance = 0

    for ch in s:
        if ch == '(':
            balance += 1
        else:
            balance -= 1
            if balance < 0:
                print("NO")
                return

    print("YES" if balance == 0 else "NO")

if __name__ == "__main__":
    solve()
```

The implementation mirrors the linear scan described earlier. The early exit when `balance` becomes negative is crucial, because continuing further cannot repair an already invalid prefix. The final equality check ensures that no unmatched opening brackets remain.

A subtle point is that we never need to explicitly store the positions of brackets or attempt pairing. The counter fully encodes the necessary structure.

## Worked Examples

### Example 1

Input: `(())()`

| Step | Character | Balance | Valid prefix |
| --- | --- | --- | --- |
| 1 | ( | 1 | yes |
| 2 | ( | 2 | yes |
| 3 | ) | 1 | yes |
| 4 | ) | 0 | yes |
| 5 | ( | 1 | yes |
| 6 | ) | 0 | yes |

The balance never goes negative and ends at zero, so the sequence is valid.

This confirms the invariant that every prefix maintains at least as many opens as closes.

### Example 2

Input: `())`

| Step | Character | Balance | Valid prefix |
| --- | --- | --- | --- |
| 1 | ( | 1 | yes |
| 2 | ) | 0 | yes |
| 3 | ) | -1 | no |

At step 3, the algorithm detects an invalid prefix because a closing bracket appears without a matching opening one. The process stops immediately.

This demonstrates how early termination catches invalid structures efficiently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed exactly once with constant work |
| Space | O(1) | Only a single counter is maintained |

With n up to 200000, a linear scan comfortably fits within time limits, and constant memory ensures no overhead from auxiliary structures.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("6\n(())()\n") == "YES"
assert run("3\n())\n") == "NO"
assert run("4\n)(()\n") == "NO"

# minimum size valid
assert run("2\n()\n") == "YES"

# minimum invalid
assert run("2\n)\n(") == "NO"

# all opens
assert run("5\n(((((") == "NO"

# balanced but wrong order
assert run("4\n())(") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `()` | YES | smallest valid sequence |
| `)(` | NO | early invalid prefix |
| `(((((` | NO | unmatched opens remain |
| `())(` | NO | balance correct but prefix violation |

## Edge Cases

One important edge case is when the sequence starts with a closing bracket. For input `")("`, the algorithm immediately decreases the balance below zero at the first character. Since no opening bracket has been seen, this reflects an impossible structure, and the output is correctly `NO`.

Another case is when the total number of opening and closing brackets is equal, but ordering is invalid, such as `"())("`. The balance returns to zero midway, but later drops below zero. The algorithm detects the violation at the exact point it occurs, rather than relying on final counts.

A third case is a long sequence of only opening brackets like `"((((("`. The balance never becomes negative, but it remains positive at the end. This shows that validity requires both prefix correctness and complete matching, and the final zero-check captures this requirement.
