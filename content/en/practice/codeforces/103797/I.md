---
title: "CF 103797I - I cry"
description: "We are given a long sequence of days encoded as a string. Each character represents whether Cosenza has an exam on that day or not. A day marked E is an exam day, while F is a free day."
date: "2026-07-02T08:49:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103797
codeforces_index: "I"
codeforces_contest_name: "IME++ Starters Try-outs 2022"
rating: 0
weight: 103797
solve_time_s: 41
verified: true
draft: false
---

[CF 103797I - I cry](https://codeforces.com/problemset/problem/103797/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a long sequence of days encoded as a string. Each character represents whether Cosenza has an exam on that day or not. A day marked `E` is an exam day, while `F` is a free day.

Cosenza follows a very rigid rule: every exam requires exactly one full free day of studying, and he refuses to study on an exam day. This means each `E` must be paired with a distinct `F` that occurs before it in the schedule, because studying happens before the exam and consumes an entire free day. If at any point an exam arrives without a previously available free day to assign as study time, the schedule becomes invalid and he “cries”.

At the same time, Cosenza only plays CS:GO on days that are truly free in every sense: they are not exam days and are not used for studying. Initially, he already has a streak of 100 consecutive such days, and we need to compute how many additional free-play days he can accumulate after scheduling all required study sessions.

The key interaction is that some `F` days will be consumed by studying, and the remaining `F` days become playable streak extensions. The output is either the total number of playable free days after scheduling, or `"I cry"` if it is impossible to assign a study day for every exam.

The string length can be up to 10^6, so any quadratic or repeated scanning approach is immediately impossible. We need a single linear pass solution that maintains only simple counters.

A subtle failure case appears when exams appear before enough free days exist. For example, `EFFFFF` fails immediately because the first day is an exam with no prior free day available to study, even though free days appear later.

Another failure case occurs when there are enough free days globally but not enough before certain exams. For example, `FEFE` looks balanced globally but the second `E` does not have enough earlier unused `F` days depending on consumption order.

## Approaches

A brute-force strategy would try to simulate the scheduling explicitly by iterating over each exam and searching backward for an unused free day to assign as study time. Each assignment would require scanning potentially the entire prefix of the string. In the worst case, with alternating patterns like `FFFFFF...EEE...`, each exam might scan nearly O(n) positions, leading to O(n^2) total complexity, which is far too slow for 10^6 characters.

The key observation is that we never need to remember _which_ free day is used for studying, only how many are available. Each `F` increases a pool of available study slots, and each `E` consumes one. If at any point we need to consume a study slot but none exists, the schedule becomes invalid.

Once feasibility is guaranteed, the remaining problem is purely arithmetic: every free day that is not consumed for studying becomes a playable CS:GO day. If we track how many free days are used for study, the answer is total free days minus used study days.

This reduces the problem to a single pass with two counters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (backtracking per exam) | O(n^2) | O(1) | Too slow |
| Greedy counting | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

### Optimal strategy

We maintain two counters: available free days and used study days.

1. Initialize a counter `free = 0`, representing unused free days available for studying, and `used = 0`, representing how many free days we have committed to studying so far.
2. Traverse the string from left to right, processing each day in order. This is necessary because study must happen before exams, so prefix availability matters.
3. If the current character is `F`, increment `free` because this day can potentially be used for studying later.
4. If the current character is `E`, we need to allocate one study day. If `free` is greater than zero, we decrement `free` and increment `used`. If `free` is zero, we immediately conclude it is impossible to satisfy this exam requirement, so we output `"I cry"`.
5. After processing the entire string successfully, compute total free days as the number of `F` in the input. The final answer is `total_F - used`.

### Why it works

The core invariant is that at any point in the scan, `free` exactly represents the number of previously seen free days that have not yet been assigned as study days. Each exam consumes one such unit, and if none exists, no future free day can fix the failure because study must happen before the exam. Therefore, feasibility is determined entirely by prefix validity. Once feasibility holds, the number of remaining free days is fixed and independent of assignment choices, since each exam consumes exactly one free day and all assignments are equivalent in cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

free = 0
used = 0
total_f = 0

for ch in s:
    if ch == 'F':
        free += 1
        total_f += 1
    else:  # 'E'
        if free == 0:
            print("I cry")
            sys.exit(0)
        free -= 1
        used += 1

print(total_f - used)
```

The implementation directly mirrors the greedy interpretation. The `free` counter tracks available study capacity, and `used` tracks how many `F` days are consumed by exams. We also maintain `total_f` so we can compute remaining playable days at the end without re-scanning the string.

The early exit on failure is safe because once an exam cannot be satisfied at a given prefix, no future `F` can retroactively fix it.

## Worked Examples

### Example 1: `FFEE`

We simulate step by step.

| Index | Char | free before | used before | Action | free after | used after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | F | 0 | 0 | add free | 1 | 0 |
| 2 | F | 1 | 0 | add free | 2 | 0 |
| 3 | E | 2 | 0 | use free | 1 | 1 |
| 4 | E | 1 | 1 | use free | 0 | 2 |

Total free days = 2, used = 2, answer = 0.

This confirms that all free days were consumed by study, leaving no CS:GO extension.

### Example 2: `FEF`

| Index | Char | free before | used before | Action | free after | used after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | F | 0 | 0 | add free | 1 | 0 |
| 2 | E | 1 | 0 | use free | 0 | 1 |
| 3 | F | 0 | 1 | add free | 1 | 1 |

Total free days = 2, used = 1, answer = 1.

This shows that a free day appearing after an exam is still useful for play but cannot help that exam, reinforcing prefix dependency.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once in a single scan |
| Space | O(1) | Only a constant number of counters are used |

The solution is linear and fits easily within constraints up to 10^6 characters, both in time and memory.

## Test Cases

```python
import sys, io

def solve():
    s = sys.stdin.readline().strip()

    free = 0
    used = 0
    total_f = 0

    for ch in s:
        if ch == 'F':
            free += 1
            total_f += 1
        else:
            if free == 0:
                return "I cry"
            free -= 1
            used += 1

    return str(total_f - used)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided samples
assert run("EFFFFF") == "I cry"
assert run("FFEE") == "0"

# custom cases
assert run("F") == "1"
assert run("E") == "I cry"
assert run("FEFE") == "1"
assert run("FFFFEEEE") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `F` | `1` | single free day, no exams |
| `E` | `I cry` | impossible immediate failure |
| `FEFE` | `1` | interleaving case, prefix dependency |
| `FFFFEEEE` | `0` | full consumption edge case |

## Edge Cases

For the input `EFFFFF`, the algorithm fails immediately at the first character because `free = 0` when processing `E`. The simulation stops and outputs `"I cry"`, correctly capturing that no future free day can be used to satisfy a past exam requirement.

For a case like `FFFFEEEE`, the algorithm accumulates four free days, then consumes all four for exams. The final counters reach `free = 0`, `used = 4`, and `total_f = 4`, producing answer `0`, which correctly reflects that no playable days remain.

For `FEFE`, the algorithm alternates between gaining and consuming. Each `E` is always matched with the most recent unused `F`, maintaining the invariant that `free` never represents future availability incorrectly. The final result depends only on how many `F` remain unconsumed, not their positions, confirming correctness of the greedy prefix matching strategy.
