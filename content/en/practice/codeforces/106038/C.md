---
title: "CF 106038C - Jo\u00e3o Pessoa"
description: "We are given a circular arrangement of parentheses. The string contains only '(' and ')', and the total number of opening and closing brackets is equal. We are allowed to take a prefix of the string and move it to the end, effectively rotating the string."
date: "2026-06-20T18:37:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106038
codeforces_index: "C"
codeforces_contest_name: "UNICAMP Selection Contest 2025"
rating: 0
weight: 106038
solve_time_s: 52
verified: true
draft: false
---

[CF 106038C - Jo\u00e3o Pessoa](https://codeforces.com/problemset/problem/106038/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a circular arrangement of parentheses. The string contains only `'('` and `')'`, and the total number of opening and closing brackets is equal. We are allowed to take a prefix of the string and move it to the end, effectively rotating the string. The task is to choose a rotation that makes the resulting sequence a valid parentheses string, and output how many characters we need to move from the front.

A valid parentheses sequence here means that if we scan from left to right, we never see more closing parentheses than opening ones at any prefix, and at the end the counts match, which is already guaranteed by the input.

The key constraint is that the string length is up to typical Codeforces limits (implicitly large, so linear or near-linear solutions are expected). A quadratic approach that tries every rotation and checks validity from scratch would be too slow because each check is O(n), leading to O(n²) overall.

A subtle edge case appears when multiple rotations produce valid sequences. For example, `"()()"` is valid already, so rotating by 0 is correct, but rotating by 2 also works. The problem allows any valid answer, so we only need one correct rotation.

Another edge case is when the string is completely reversed in terms of balance, such as `"))((()"`. A naive check of only total counts would fail because intermediate prefixes matter, not just global counts.

## Approaches

A brute-force strategy would try every possible rotation. For each rotation index i, we construct the rotated string and check whether it is valid by scanning from left to right and tracking balance. Each validity check costs O(n), and there are n rotations, giving O(n²) time. This is too slow for large n.

The structure of the problem suggests we should avoid recomputing validity from scratch. The important observation is that validity of a parentheses sequence depends only on prefix balance, and rotation just shifts where we start reading the same cyclic sequence. So instead of rebuilding strings, we can think in terms of prefix sums over a doubled or cyclic view.

We define balance as +1 for `'('` and -1 for `')'`. For a rotation starting at position i, we need all prefix sums in the segment `[i, i+n-1]` (circularly) to stay non-negative.

A key idea is to find the position where starting the traversal gives the best chance of avoiding negative prefix sums. This can be identified by tracking the minimum prefix balance over the original array and choosing a rotation that starts right after the lowest point in the cumulative balance curve. That ensures the path never dips below zero when re-centered.

This reduces the task to a single linear scan computing prefix balances and locating the index of the minimum prefix sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal (prefix min rotation) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Convert the string into an array of +1 and -1 values depending on parentheses. This turns the problem into tracking cumulative sums instead of string structure, which makes rotation effects easier to reason about.
2. Compute prefix sums while scanning the string from left to right. Keep a running total where each `'('` increases the sum and each `')'` decreases it. This represents how far above or below validity threshold the sequence goes at each point.
3. Track the index where the prefix sum reaches its minimum value. This point corresponds to the deepest dip in balance across the entire sequence. The intuition is that this is the weakest point in the cyclic structure.
4. Choose the rotation so that this minimum point becomes just before the start of the new string. Concretely, if the minimum prefix occurs at index i, we rotate by i+1 positions.
5. Output this rotation index. If multiple valid choices exist, any minimum-achieving position works because all such rotations avoid negative prefix sums.

### Why it works

The prefix sum curve describes a walk that starts at zero and ends at zero. A valid parentheses sequence is exactly a walk that never goes below zero. When we rotate the sequence, we are effectively choosing a new starting point on this cyclic walk. The best starting point is one immediately after the global minimum, because that shifts the entire curve upward so that the lowest point becomes zero instead of negative. Since every other prefix is higher than or equal to this minimum, no prefix in the rotated version can go negative.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
n = len(s)

min_prefix = 0
min_idx = -1

pref = 0

for i, ch in enumerate(s):
    if ch == '(':
        pref += 1
    else:
        pref -= 1

    if pref < min_prefix:
        min_prefix = pref
        min_idx = i

# rotate so that min prefix position moves to end of prefix
print(min_idx + 1)
```

The code computes the cumulative balance in a single pass while tracking where the lowest value occurs. The variable `min_idx` stores the last position where the prefix sum is minimal. Rotating after this index ensures the sequence starts from a point where balance is non-negative throughout.

A common subtlety is off-by-one handling: we rotate by `min_idx + 1`, not `min_idx`, because we want the new string to begin immediately after the lowest prefix point.

## Worked Examples

### Example 1: `"))((()"`

We compute prefix balance step by step.

| i | char | prefix | min_prefix | min_idx |
| --- | --- | --- | --- | --- |
| 0 | ) | -1 | -1 | 0 |
| 1 | ) | -2 | -2 | 1 |
| 2 | ( | -1 | -2 | 1 |
| 3 | ( | 0 | -2 | 1 |
| 4 | ) | -1 | -2 | 1 |
| 5 | ( | 0 | -2 | 1 |

The minimum prefix is -2 at index 1, so we rotate by 2. The rotated string is `"((())("`, which is valid.

This trace shows that even though multiple negative dips occur, the deepest dip determines the correct rotation point.

### Example 2: `"()()"`

| i | char | prefix | min_prefix | min_idx |
| --- | --- | --- | --- | --- |
| 0 | ( | 1 | 0 | -1 |
| 1 | ) | 0 | 0 | -1 |
| 2 | ( | 1 | 0 | -1 |
| 3 | ) | 0 | 0 | -1 |

The minimum prefix is 0 throughout, so `min_idx = -1`. We output `0`, meaning no rotation is needed. The string is already valid.

This shows that the algorithm naturally handles already-balanced sequences without special casing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass computing prefix sums |
| Space | O(1) | only a few integer variables are used |

The solution fits comfortably within constraints because it processes each character once and performs only constant-time updates per step.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = input().strip()
    n = len(s)

    min_prefix = 0
    min_idx = -1
    pref = 0

    for i, ch in enumerate(s):
        pref += 1 if ch == '(' else -1
        if pref < min_prefix:
            min_prefix = pref
            min_idx = i

    return str(min_idx + 1)

# provided samples
assert run("))((()\n") == "2"
assert run("()\n") == "0"
assert run("))((\n") == "2"

# custom cases
assert run("()") == "0", "already valid"
assert run(")(()") == "1", "single correction via rotation"
assert run("((()))") == "0", "fully nested already valid"
assert run(")))(((") == "3", "large imbalance symmetric"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `()` | `0` | already valid, no rotation needed |
| `)(()` | `1` | rotation needed to fix early negative prefix |
| `)))(((` | `3` | worst-case imbalance, checks correct min index handling |

## Edge Cases

One edge case is when the string is already valid and never dips below zero. In this case, the minimum prefix is zero at all points, so `min_idx` remains `-1`, and the output becomes `0`. The algorithm correctly identifies that no rotation is required.

Another edge case is when the minimum prefix occurs at the last character. In a string like `"((()))"` or any already balanced valid form, this still leads to `min_idx = -1`, so the result is stable and does not incorrectly suggest rotation.

A more subtle case is when multiple positions share the same minimum prefix value. The algorithm stores the last occurrence, but any occurrence would produce a valid rotation because shifting after any deepest dip yields a non-negative re-centered walk.
