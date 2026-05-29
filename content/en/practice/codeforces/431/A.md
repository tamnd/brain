---
title: "CF 431A - Black Square"
description: "In \"Black Square,\" Jury must press on one of four vertical strips whenever a black square appears. Each strip has a fixed energy cost, measured in calories, for pressing it."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 431
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 247 (Div. 2)"
rating: 800
weight: 431
solve_time_s: 70
verified: true
draft: false
---

[CF 431A - Black Square](https://codeforces.com/problemset/problem/431/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

In "Black Square," Jury must press on one of four vertical strips whenever a black square appears. Each strip has a fixed energy cost, measured in calories, for pressing it. We are given four integers representing the calories consumed when pressing the first through fourth strips. The game's progression is described by a string where each character is a digit from "1" to "4" indicating which strip has a square at that second. The task is to compute the total calories Jury expends by following this sequence and pressing the corresponding strips.

The input guarantees up to 105 game seconds, so our solution must process each character efficiently, ideally in linear time. Each calorie cost can be zero, meaning pressing a strip might not consume energy. Edge cases include the string being entirely one type of strip, alternating strips, or having the maximum length of 105. A naive solution that repeatedly searches or performs complex operations per character could exceed the time limit.

A subtle edge case arises when all calorie costs are zero. For example, if the input is `0 0 0 0` and `s = "12341"`, the correct output is `0`, but a careless approach that, for example, assumes every press contributes at least one calorie would give the wrong result.

## Approaches

The brute-force approach is to iterate over the string and, for each character, map it to the corresponding calorie cost and add it to a running total. This works because each second is independent; we only need to know the cost for that specific strip. The brute-force is technically already optimal because every character must be examined, giving a worst-case complexity proportional to the string length.

The key observation that confirms this approach is sufficient is that there are no interactions between the strips; calories are additive. No optimization or complex data structure is needed, since each lookup is a constant-time operation. By mapping the character "1"-"4" directly to the corresponding index in the calorie array, we can efficiently accumulate the total calories.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the four integers representing the calories for the first through fourth strips. Store them in a list `calories` for direct indexing.
2. Read the string `s` representing the sequence of black squares.
3. Initialize a variable `total` to zero to accumulate the calorie count.
4. Iterate over each character `c` in the string `s`. Convert `c` to an integer and subtract one to match zero-based indexing, then access `calories` at that index and add the value to `total`.
5. After processing all characters, print the value of `total`.

Why it works: The algorithm maintains the invariant that `total` always equals the sum of calories for all processed strips. Since every character is handled exactly once and mapped directly to its cost, no calories are missed or double-counted. The final `total` is therefore the sum over all seconds, satisfying the problem requirement.

## Python Solution

```python
import sys
input = sys.stdin.readline

# read calorie costs for each strip
calories = list(map(int, input().split()))
s = input().strip()

total = 0
for c in s:
    total += calories[int(c) - 1]

print(total)
```

The first line reads the four calorie values and stores them in a list. Subtracting one from `int(c)` ensures that the mapping from "1"-"4" to the zero-based list indices is correct. The loop directly adds the appropriate calorie value to `total` without any conditional checks or branching. This avoids off-by-one errors. The string is stripped of whitespace to ensure we do not accidentally process a newline character.

## Worked Examples

**Sample 1**

Input:

```
1 2 3 4
123214
```

| Step | Character | Index | Calories Added | Total |
| --- | --- | --- | --- | --- |
| 1 | '1' | 0 | 1 | 1 |
| 2 | '2' | 1 | 2 | 3 |
| 3 | '3' | 2 | 3 | 6 |
| 4 | '2' | 1 | 2 | 8 |
| 5 | '1' | 0 | 1 | 9 |
| 6 | '4' | 3 | 4 | 13 |

This trace confirms the total calories accumulate correctly for each press.

**Sample 2**

Input:

```
5 5 5 5
4441
```

| Step | Character | Index | Calories Added | Total |
| --- | --- | --- | --- | --- |
| 1 | '4' | 3 | 5 | 5 |
| 2 | '4' | 3 | 5 | 10 |
| 3 | '4' | 3 | 5 | 15 |
| 4 | '1' | 0 | 5 | 20 |

This demonstrates handling repeated presses on the same strip.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character in the string is processed once; integer conversion and list lookup are O(1). |
| Space | O(1) | Only a small fixed-size list for calories and a running total are used. |

Given n ≤ 105, this linear approach executes comfortably within 1 second, even on Python, and memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    calories = list(map(int, input().split()))
    s = input().strip()
    total = 0
    for c in s:
        total += calories[int(c) - 1]
    return str(total)

# provided sample
assert run("1 2 3 4\n123214\n") == "13", "sample 1"

# custom cases
assert run("0 0 0 0\n12341\n") == "0", "all zero calories"
assert run("1 1 1 1\n11111\n") == "5", "all same strip"
assert run("1 2 3 4\n4321\n") == "10", "descending order"
assert run("10 20 30 40\n444444\n") == "240", "repeated max strip"
assert run("5 5 5 5\n1\n") == "5", "single element"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 0 0 / 12341 | 0 | Handling zero-calorie strips |
| 1 1 1 1 / 11111 | 5 | Repeated presses on the same strip |
| 1 2 3 4 / 4321 | 10 | Correct index mapping for descending sequence |
| 10 20 30 40 / 444444 | 240 | Multiple presses on the last strip |
| 5 5 5 5 / 1 | 5 | Minimal input size |

## Edge Cases

When all calorie values are zero, `total` remains zero regardless of the sequence. For example, input `0 0 0 0\n12341` produces `0`. The algorithm correctly handles a string of length one, as in `5 5 5 5\n1`, where it simply adds the cost of the first strip once. For repeated presses on a single strip, such as `11111` with all calories 1, the algorithm accumulates the sum correctly, confirming the invariant holds across multiple identical characters.
