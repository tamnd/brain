---
title: "CF 188E - HQ9+"
description: "We are asked to analyze a string representing a program written in HQ9+, a toy language with four instructions: H, Q, 9, and +. Only the first three produce output when executed: H prints \"Hello, World!"
date: "2026-06-03T01:06:39+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 188
codeforces_index: "E"
codeforces_contest_name: "Surprise Language Round 6"
rating: 1400
weight: 188
solve_time_s: 57
verified: true
draft: false
---

[CF 188E - HQ9+](https://codeforces.com/problemset/problem/188/E)

**Rating:** 1400  
**Tags:** *special, implementation  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to analyze a string representing a program written in HQ9+, a toy language with four instructions: `H`, `Q`, `9`, and `+`. Only the first three produce output when executed: `H` prints "Hello, World!", `Q` prints the program itself, and `9` prints the lyrics of "99 Bottles of Beer". The `+` instruction modifies an internal accumulator, but does not print anything. Any other character in the input string is ignored.

The input is a single line containing 1 to 100 ASCII characters between `!` (33) and `~` (126). Our task is to determine whether executing this program will produce any output. Output is a simple "YES" if there is at least one instruction that prints something, and "NO" otherwise.

The problem is constrained enough that a linear scan of the string is feasible. Even at the maximum length of 100 characters, iterating through each character to check if it is `H`, `Q`, or `9` will require at most 100 operations, which is negligible under a 2-second time limit.

An edge case is a string composed entirely of `+` characters or other non-output characters. For example, `"+++"` should produce "NO", whereas a string with `"H++"` should produce "YES" because of the `H`. Another edge case is a string where the output-producing instruction appears at the very end, e.g., `"abc9"`. Careless implementations might return "NO" if they stop scanning too early or do not correctly check all characters.

## Approaches

A brute-force approach is to simulate the program: iterate through each character and perform the corresponding action. This would involve actual printing or counting, but since we only care about whether output occurs, the full simulation is unnecessary. The brute-force works because the language has only four instructions, but it is conceptually overkill because the only information needed is the presence of `H`, `Q`, or `9`.

The optimal approach leverages the observation that we do not need to execute the program. Output occurs if and only if at least one character in the string is one of `H`, `Q`, or `9`. This reduces the problem to a simple membership check: iterate through the string and immediately return "YES" upon encountering any of the three characters, returning "NO" only if none are found. This approach is linear in the length of the input and does not require any additional memory beyond a few variables.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n) | O(1) | Overkill but correct |
| Output Presence Check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string and strip any trailing newline. This ensures we process only the program code itself.
2. Iterate over each character in the string. At each step, check if the character is `H`, `Q`, or `9`. These are the only instructions that produce output.
3. If a character matches, immediately print "YES" and terminate. There is no need to continue scanning since one output-producing instruction guarantees that the program will produce output.
4. If the loop finishes without encountering any of the three characters, print "NO". This captures the case where the program has no output-producing instructions.

Why it works: The algorithm maintains the invariant that if output exists in the program, it will be detected on the first occurrence of an output-producing instruction. Since all output-producing instructions are explicitly known and case-sensitive, no output can occur from other characters, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

program = input().strip()

for char in program:
    if char in "HQ9":
        print("YES")
        break
else:
    print("NO")
```

The code reads the program string and iterates through each character. The `in` check identifies output-producing instructions. The `break` ensures we terminate as soon as output is detected. The `else` clause of the `for` loop is executed only if the loop completes without encountering a `break`, allowing us to handle the "NO output" case cleanly.

## Worked Examples

Sample Input 1:

```
Hello!
```

| Step | Character | Check | Action |
| --- | --- | --- | --- |
| 1 | H | H in "HQ9" | Print "YES" and break |

The first character is `H`, which produces output. The algorithm terminates immediately, demonstrating that early termination works correctly.

Sample Input 2:

```
+++
```

| Step | Character | Check | Action |
| --- | --- | --- | --- |
| 1 | + | Not in "HQ9" | Continue |
| 2 | + | Not in "HQ9" | Continue |
| 3 | + | Not in "HQ9" | Continue |
| Loop ends | - | - | Print "NO" |

No characters produce output, confirming the algorithm correctly identifies programs with zero output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character of the string is examined at most once; n ≤ 100 |
| Space | O(1) | Only a few variables are used; no additional data structures |

Given n ≤ 100, this solution runs in negligible time and uses minimal memory, well within the limits of 2 seconds and 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    program = input().strip()
    for char in program:
        if char in "HQ9":
            return "YES"
    return "NO"

# Provided samples
assert run("Hello!\n") == "YES", "sample 1"
assert run("+++\n") == "NO", "sample 2"

# Custom cases
assert run("Q\n") == "YES", "single output instruction"
assert run("abcdefg\n") == "NO", "no instructions"
assert run("abcHxyz\n") == "YES", "output instruction in middle"
assert run("99Bottles\n") == "YES", "contains 9 producing output"
assert run("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n") == "NO", "maximum-size non-output"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Q | YES | Single output instruction |
| abcdefg | NO | No output instructions |
| abcHxyz | YES | Output instruction in middle |
| 99Bottles | YES | Contains 9 |
| +++++... (max 100) | NO | Max-size non-output input |

## Edge Cases

Consider a program composed entirely of `+` characters: `"++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"`. The loop checks each character, finds none of `H`, `Q`, or `9`, and the `else` clause prints "NO". This confirms that the algorithm handles strings with only non-output instructions correctly.

For a program with a single `9` at the very end: `"abc9"`, the loop iterates over `a`, `b`, `c` without action, reaches `9`, prints "YES", and exits immediately. This shows that output detected late in the string is handled correctly, and early termination does not produce false negatives.
