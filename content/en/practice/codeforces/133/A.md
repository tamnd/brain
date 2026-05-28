---
title: "CF 133A - HQ9+"
description: "The task is to analyze a program written in the esoteric HQ9+ language and determine whether executing it will produce any visible output. The program is provided as a single string consisting of printable ASCII characters."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 133
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 96 (Div. 2)"
rating: 900
weight: 133
solve_time_s: 64
verified: true
draft: false
---

[CF 133A - HQ9+](https://codeforces.com/problemset/problem/133/A)

**Rating:** 900  
**Tags:** implementation  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to analyze a program written in the esoteric HQ9+ language and determine whether executing it will produce any visible output. The program is provided as a single string consisting of printable ASCII characters. In HQ9+, only four characters have operational meaning: "H" prints "Hello, World!", "Q" prints the program itself, "9" prints the lyrics of "99 Bottles of Beer", and "+" modifies an internal accumulator but does not produce output. Any other characters are ignored.

From the perspective of execution, this means the program will produce output if it contains at least one of "H", "Q", or "9". All other characters, including "+", letters, punctuation, or digits, do not generate visible output. The string length is between 1 and 100, which is small enough that any algorithm that examines each character individually is acceptable. Because the output depends on the presence of specific instructions, we only need a membership test over the string, not any actual simulation of the HQ9+ operations.

Edge cases include strings with only non-output instructions, strings containing multiple output instructions, and strings with output instructions embedded among irrelevant characters. For instance, the input `"Hi!"` contains "H" and should return `"YES"`, while `"+++"` contains only "+", and should return `"NO"`. A careless implementation that checks only the first character or assumes "+" generates output would fail these cases.

## Approaches

A naive approach would be to simulate the entire program, processing each character in order and generating the actual output strings. This works because it faithfully replicates the semantics of HQ9+, but it is overkill for the problem requirement. In the worst case, the string could contain a "9", which theoretically would require generating the full lyrics of "99 Bottles of Beer". That is unnecessary here because we only need a boolean answer, not the actual printed text.

The optimal approach leverages the observation that we do not need the output itself, only whether it exists. Therefore, we can scan the program string once and check whether it contains any of "H", "Q", or "9". If such a character exists, the answer is `"YES"`, otherwise `"NO"`. This reduces the problem to a single linear pass over the string, avoiding unnecessary string generation and ensuring a simple, robust solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(n) | Works but unnecessarily heavy |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string representing the HQ9+ program. We assume it contains only printable ASCII characters and is non-empty.
2. Initialize a set containing the three output-producing instructions: `{'H', 'Q', '9'}`. This allows constant-time membership checks.
3. Iterate through each character of the program string.
4. For each character, check if it exists in the set of output instructions.
5. If any character matches, immediately print `"YES"` and terminate, because we have found a character that produces output.
6. If the loop completes without finding any output-producing characters, print `"NO"`.

Why it works: At each step, the algorithm checks the exact set of characters known to produce visible output. Since any occurrence guarantees output, an early exit is safe. Conversely, if no such character exists in the string, the program cannot produce any output, so returning `"NO"` is correct. This invariant holds regardless of the position or number of other irrelevant characters.

## Python Solution

```python
import sys
input = sys.stdin.readline

program = input().strip()
output_instructions = {'H', 'Q', '9'}

for ch in program:
    if ch in output_instructions:
        print("YES")
        break
else:
    print("NO")
```

The code first trims any trailing newline or spaces. The set `output_instructions` provides O(1) membership checks. The `for` loop scans each character. The `else` clause on the `for` executes only if the loop did not break, meaning no output-producing instruction was found. This is a subtle but standard Python feature that avoids needing an extra flag variable.

## Worked Examples

**Sample Input 1:** `"Hi!"`

| Step | ch | ch in output_instructions? | Action |
| --- | --- | --- | --- |
| 1 | 'H' | Yes | Print "YES", exit |
| - | - | - | Loop terminates early |

This confirms that the program detects output immediately, even if additional characters follow.

**Sample Input 2:** `"+++"`

| Step | ch | ch in output_instructions? | Action |
| --- | --- | --- | --- |
| 1 | '+' | No | Continue |
| 2 | '+' | No | Continue |
| 3 | '+' | No | Continue |
| - | - | - | Loop completes, print "NO" |

This demonstrates correct handling of programs with no visible output instructions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan each character once, and n ≤ 100 |
| Space | O(1) | The set of output instructions has constant size |

Given the constraints, a linear scan of up to 100 characters is trivial in both time and memory. The solution fits comfortably within the 2-second time limit and 256 MB memory bound.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    program = sys.stdin.readline().strip()
    output_instructions = {'H', 'Q', '9'}
    for ch in program:
        if ch in output_instructions:
            return "YES"
    return "NO"

# Provided samples
assert run("Hi!\n") == "YES", "sample 1"
assert run("+++\n") == "NO", "sample 2"

# Custom cases
assert run("9\n") == "YES", "single '9'"
assert run("abcDEF\n") == "NO", "all non-instructions"
assert run("H+Q+9\n") == "YES", "multiple output instructions"
assert run("!\n") == "NO", "minimum ASCII non-instruction"
assert run("!H!Q!9!+\n") == "YES", "mixed characters with output"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "9" | "YES" | Single output instruction |
| "abcDEF" | "NO" | All non-instructions |
| "H+Q+9" | "YES" | Multiple output instructions |
| "!" | "NO" | Minimum ASCII non-instruction |
| "!H!Q!9!+" | "YES" | Mixed irrelevant and output instructions |

## Edge Cases

The program `"+++"` tests a string containing only non-output instructions. The algorithm correctly scans all characters, finds none in `{'H','Q','9'}`, and prints `"NO"`. The input `"!H!Q!9!+"` contains a mix of irrelevant characters and output instructions. The algorithm detects 'H' on the second character, prints `"YES"` immediately, and exits without scanning the remainder. These traces confirm the correctness of both early exit and full scan paths.
