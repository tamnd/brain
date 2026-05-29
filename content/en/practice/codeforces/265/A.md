---
title: "CF 265A - Colorful Stones (Simplified Edition)"
description: "The problem describes a row of stones, each colored red, green, or blue, represented by a string s of characters 'R', 'G', and 'B'. Squirrel Liss starts on the first stone and executes a sequence of color-based instructions, given by a second string t."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 265
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 162 (Div. 2)"
rating: 800
weight: 265
solve_time_s: 77
verified: false
draft: false
---

[CF 265A - Colorful Stones (Simplified Edition)](https://codeforces.com/problemset/problem/265/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 17s  
**Verified:** no  

## Solution
## Problem Understanding

The problem describes a row of stones, each colored red, green, or blue, represented by a string `s` of characters 'R', 'G', and 'B'. Squirrel Liss starts on the first stone and executes a sequence of color-based instructions, given by a second string `t`. Each instruction corresponds to a color: if the stone Liss is currently on matches the instruction's color, she moves forward by one stone. Otherwise, she stays put. We are asked to compute Liss's final position after executing all instructions, with positions numbered starting from one.

The strings are short, up to 50 characters each, which allows for a direct simulation of the instructions without worrying about time limits. Each instruction requires only a single comparison and, if applicable, an increment. With 50 instructions and 50 stones, this leads to at most 50 operations, which is negligible under a 2-second time limit.

A subtle edge case arises when multiple instructions do not match the current stone color. For example, if `s = "RGB"` and `t = "GGG"`, Liss will never move from stone 1. Another potential pitfall is handling the 1-based indexing properly; naive zero-based array handling could lead to off-by-one errors.

## Approaches

A brute-force approach directly simulates Liss's movements. We start with a variable `pos = 0` for the first stone (zero-based for internal computation). For each instruction, we check if `s[pos]` matches the instruction. If it does, we increment `pos`. This correctly models the rules and is simple to implement. The number of comparisons equals the length of `t`, so in the worst case, we perform 50 operations, which is acceptable.

There is no need for a more complex algorithm because the input size is extremely small. The key insight is that this is a pure simulation problem; no precomputation, data structures, or greedy strategies improve performance. The optimal solution is the same as the brute-force simulation but must carefully handle 1-based output.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force / Simulation | O( | t | ) |
| Optimized | O( | t | ) |

## Algorithm Walkthrough

1. Initialize a variable `pos = 0` representing Liss's current stone index (zero-based). This choice simplifies string indexing in Python.
2. Iterate over each character `instruction` in the string `t`. Each character represents a color instruction.
3. For each `instruction`, check if `s[pos]` matches it. This models the rule that Liss moves only if the instruction matches the stone color.
4. If there is a match, increment `pos` by one. Otherwise, do nothing and proceed to the next instruction.
5. After processing all instructions, output `pos + 1` to convert from zero-based to one-based position.

Why it works: The algorithm maintains the invariant that `pos` always represents the current stone index of Liss. Each instruction is applied in order, and movement occurs only when allowed. Because we iterate through the instructions sequentially, no movement is skipped or repeated incorrectly. The final output correctly translates from internal zero-based indexing to the problem's one-based numbering.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
t = input().strip()

pos = 0  # zero-based index

for instruction in t:
    if s[pos] == instruction:
        pos += 1

print(pos + 1)
```

The solution first reads and strips both strings to remove any trailing newline. The `pos` variable tracks the current position, starting from 0. The for-loop iterates over each instruction, performing a single equality check and optional increment. Finally, the result is printed as a 1-based index. Care is taken to increment only on matching instructions, which avoids off-by-one errors.

## Worked Examples

### Sample 1

Input:

```
s = "RGB"
t = "RRR"
```

| Step | pos | instruction | s[pos] == instruction? | Action |
| --- | --- | --- | --- | --- |
| 1 | 0 | R | R == R | pos += 1 → pos = 1 |
| 2 | 1 | R | G == R | no move |
| 3 | 1 | R | G == R | no move |

Final output: 1-based `pos + 1 = 2`.

This trace shows that repeated instructions that do not match the current stone color are correctly ignored.

### Sample 2

Input:

```
s = "RGBB"
t = "RGBB"
```

| Step | pos | instruction | s[pos] == instruction? | Action |
| --- | --- | --- | --- | --- |
| 1 | 0 | R | R == R | pos = 1 |
| 2 | 1 | G | G == G | pos = 2 |
| 3 | 2 | B | B == B | pos = 3 |
| 4 | 3 | B | B == B | pos = 4 |

Final output: 1-based `pos + 1 = 5`, which is correct. This confirms proper increment at every match.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | t |
| Space | O(1) | Only a single index variable `pos` is needed; strings are input only. |

Given the constraints (maximum 50 stones and 50 instructions), this algorithm runs in microseconds, well within the 2-second limit, and uses negligible memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = input().strip()
    t = input().strip()
    pos = 0
    for instruction in t:
        if s[pos] == instruction:
            pos += 1
    return str(pos + 1)

# Provided sample
assert run("RGB\nRRR\n") == "2", "sample 1"

# Custom cases
assert run("R\nR\n") =
```
