---
title: "CF 162E - HQ9+"
description: "The problem asks whether a program written in the joke language HQ9+ will produce any output. The program is a string containing between 1 and 100 printable ASCII characters. Only four instructions matter: \"H\", \"Q\", \"9\", and \"+\"."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 162
codeforces_index: "E"
codeforces_contest_name: "VK Cup 2012 Wild-card Round 1"
rating: 1800
weight: 162
solve_time_s: 69
verified: true
draft: false
---

[CF 162E - HQ9+](https://codeforces.com/problemset/problem/162/E)

**Rating:** 1800  
**Tags:** *special  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks whether a program written in the joke language HQ9+ will produce any output. The program is a string containing between 1 and 100 printable ASCII characters. Only four instructions matter: "H", "Q", "9", and "+". The "+" instruction manipulates an internal accumulator but does not produce any output, so it can be ignored for the purpose of this problem. All other characters, including lowercase letters and punctuation, are also ignored. The task is to detect whether the program contains at least one of "H", "Q", or "9", in which case running the program will produce output.

The constraints are small, with a maximum input length of 100 characters. This means we can afford simple linear scans through the string, and there is no need for optimization beyond O(n). Non-obvious edge cases include strings that contain only ignored characters or strings with mixed case. For example, a program `"hello"` contains only lowercase letters, which are ignored, so the correct output is "NO". Conversely, `"H"` produces output, so the answer is "YES". A careless approach might check for any occurrence of 'h' instead of 'H', giving a wrong answer.

## Approaches

A brute-force approach is straightforward: iterate through each character of the string and check if it matches "H", "Q", or "9". If any match is found, immediately output "YES"; otherwise, output "NO" at the end. This works because the problem only requires detecting a single instruction that produces output, and each character can be checked independently. Given the maximum length of 100, this method requires at most 100 comparisons, which is negligible in terms of computational cost.

The optimal approach is effectively the same as the brute-force approach in this case. The key insight is recognizing that we do not need to simulate the program or handle the accumulator at all. The problem reduces to a membership test in a set of three characters. Using a set for comparison makes the code concise and clear, and a single pass through the string guarantees correctness.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string representing the HQ9+ program.
2. Initialize a set containing the characters `'H'`, `'Q'`, and `'9'`. This set represents instructions that produce output.
3. Iterate over each character in the input string. For each character, check if it is a member of the set of output-producing instructions.
4. If any character is found in the set, immediately print "YES" and terminate the algorithm. This ensures we do not waste time scanning the rest of the string unnecessarily.
5. If the loop completes without finding any character in the set, print "NO". At this point, we know the program produces no output.

Why it works: The invariant is that the program produces output if and only if it contains at least one of "H", "Q", or "9". By scanning the string once and checking membership in a set, we guarantee that any output-producing instruction will be detected and that we never produce a false positive for ignored characters.

## Python Solution

```python
import sys
input = sys.stdin.readline

program = input().strip()
output_instructions = {'H', 'Q', '9'}

for char in program:
    if char in output_instructions:
        print("YES")
        break
else:
    print("NO")
```

The solution reads the program from standard input and removes trailing newline characters with `strip()`. The set `output_instructions` allows constant-time membership checks for each character. The `for-else` structure ensures that "NO" is only printed if the loop completes without finding a match. Using a set instead of multiple `or` conditions makes the code scalable and easy to read.

## Worked Examples

Sample 1:

Input: `"Hello!"`

| Step | char | char in set? | Action |
| --- | --- | --- | --- |
| 1 | 'H' | Yes | Print YES, stop |
| 2 | 'e' | - | - |

The algorithm detects 'H' immediately and outputs "YES". Subsequent characters are not checked, demonstrating early termination.

Sample 2:

Input: `"hello"`

| Step | char | char in set? | Action |
| --- | --- | --- | --- |
| 1 | 'h' | No | Continue |
| 2 | 'e' | No | Continue |
| 3 | 'l' | No | Continue |
| 4 | 'l' | No | Continue |
| 5 | 'o' | No | Continue |

No characters match 'H', 'Q', or '9', so the loop completes and the algorithm prints "NO". This confirms that lowercase letters are ignored.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan each character once and perform a constant-time set membership check. |
| Space | O(1) | The set of instructions has a fixed size of three elements, independent of input size. |

Given that n ≤ 100, the solution performs at most 100 operations and uses minimal memory, well within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as io_module
    out = io_module.StringIO()
    with redirect_stdout(out):
        program = input().strip()
        output_instructions = {'H', 'Q', '9'}
        for char in program:
            if char in output_instructions:
                print("YES")
                break
        else:
            print("NO")
    return out.getvalue().strip()

# provided samples
assert run("Hello!\n") == "YES", "sample 1"
assert run("hello\n") == "NO", "sample 2"

# custom cases
assert run("H\n") == "YES", "single instruction H"
assert run("+++\n") == "NO", "only non-output instructions"
assert run("9abc\n") == "YES", "9 instruction at start"
assert run("abcdQ\n") == "YES", "Q instruction at end"
assert run("!@#$\n") == "NO", "symbols only, no instructions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "H" | YES | Single output instruction |
| "+++" | NO | Only accumulator increments produce no output |
| "9abc" | YES | Output instruction at start of string |
| "abcdQ" | YES | Output instruction at end of string |
| "!@#$" | NO | Non-instruction symbols ignored correctly |

## Edge Cases

A string containing only lowercase letters or symbols such as `"hello!"` correctly produces "NO". The algorithm checks each character individually and only triggers "YES" for uppercase "H", "Q", or the digit "9". A program like `"H9+Q"` produces "YES" immediately upon encountering 'H', demonstrating that early termination works. A single-character program `"+"` produces "NO" because '+' does not generate output. The handling of these edge cases confirms the solution is robust and aligns with the problem requirements.
