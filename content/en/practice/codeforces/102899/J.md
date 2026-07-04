---
title: "CF 102899J - KK\u4e0e\u82f1\u8bed"
description: "We are given a single line of text representing a sentence that may contain the word “is” in different contexts. The task is to scan this sentence and replace every occurrence of the lowercase word “is” only when it appears as a standalone token surrounded by spaces on both…"
date: "2026-07-04T08:22:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102899
codeforces_index: "J"
codeforces_contest_name: "The 2nd Hangzhou Normal University Freshman Programming Contest"
rating: 0
weight: 102899
solve_time_s: 38
verified: true
draft: false
---

[CF 102899J - KK\u4e0e\u82f1\u8bed](https://codeforces.com/problemset/problem/102899/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single line of text representing a sentence that may contain the word “is” in different contexts. The task is to scan this sentence and replace every occurrence of the lowercase word “is” only when it appears as a standalone token surrounded by spaces on both sides. Any other form must remain unchanged, including “Is” with a capital letter, “is” at the beginning or end of the line, or “is” attached to punctuation or other characters.

The input size can be up to 100,000 characters, which immediately suggests that any solution involving repeated string concatenation or repeated global replacements on substrings would be risky if implemented naively in a quadratic way. A linear scan is required, since any approach that repeatedly searches or rebuilds strings inefficiently could degrade to O(n²) in the worst case when many replacements occur.

Several edge cases appear naturally from the definition of “surrounded by spaces”. If the string starts with “is”, it should not be replaced because there is no leading space. For example, the input “is a book” must remain unchanged. Similarly, if “is” appears at the end like “this is”, it is replaced only if it is followed by a space on the right, meaning trailing positions are also sensitive. Another subtle case is punctuation adjacency: “is,” or “(is)” must not be replaced because the word is not bounded strictly by spaces.

A naive approach that splits by spaces and rebuilds the sentence also fails if multiple spaces appear between words or if punctuation is attached to tokens, since it risks losing the original formatting.

## Approaches

The brute-force idea is to repeatedly search the string for the substring `" is "` and replace it with `" was "`. This is logically correct because it directly encodes the condition of having spaces on both sides. However, each replacement potentially shifts the string and requires rebuilding it, and if implemented using repeated `find` and slicing, each operation can take O(n). In a worst case where replacements happen frequently, this leads to O(n²) behavior.

A more reliable observation is that we never need to modify the string in place multiple times. Each character can be processed once from left to right while checking local context. At any position, we only need to decide whether the current three-character window forms `" is "` with proper boundaries. If it does, we emit `" was "` instead of copying the original substring. Otherwise, we copy the current character as-is and move forward. This reduces the problem to a single pass with constant-time checks per position.

The key structural property is that the decision for replacing “is” depends only on its immediate neighbors. No global information is required, so streaming construction is sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force String Replacement | O(n²) | O(n) | Too slow |
| One-pass Scan with Window Check | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input string into a variable `s`. We will construct the answer incrementally rather than modifying `s` in place, since strings are immutable in Python.
2. Initialize an empty list `out` to store output characters efficiently. Using a list avoids repeated string concatenation cost.
3. Iterate through the string using an index `i` from `0` to `len(s) - 1`.
4. At each position `i`, check whether a replacement is possible. The condition requires that:

the substring starting at `i` is exactly `"is"`, and there is a space immediately before and after it, meaning `s[i-1] == ' '` and `s[i+2] == ' '`.

This check ensures we only replace isolated words, not parts of other words or punctuation-attached tokens.
5. If the condition holds, append the string `"was"` to the output list, and advance `i` by 2, since we have consumed two characters.
6. If the condition does not hold, append `s[i]` to the output list and advance `i` by 1.
7. After finishing the loop, join the list into a final string and print it.

### Why it works

The correctness comes from the fact that every decision is local and irreversible. Whenever we replace `" is "` with `" was "`, we are guaranteed that no overlapping or partial match can later be affected because replacements only occur when both surrounding characters are spaces. This prevents conflicts between adjacent matches. Every character is examined exactly once as part of either a match or a non-match case, ensuring full coverage without duplication or omission.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().rstrip('\n')
    n = len(s)
    out = []
    i = 0

    while i < n:
        if i > 0 and i + 2 < n:
            if s[i:i+2] == "is" and s[i-1] == ' ' and s[i+2] == ' ':
                out.append("was")
                i += 2
                continue

        out.append(s[i])
        i += 1

    print("".join(out))

if __name__ == "__main__":
    solve()
```

The implementation relies on a sliding window check around each candidate position. The key subtlety is ensuring boundary safety: the condition `i > 0 and i + 2 < n` prevents out-of-range access when checking neighbors. The loop advancement differs depending on whether a replacement occurs, which avoids double-processing characters inside a matched segment.

## Worked Examples

### Example 1

Input:

```
It is my boy friend.
```

| i | s[i:i+2] | left char | right char | action | output |
| --- | --- | --- | --- | --- | --- |
| 0 | It | - | - | copy | I |
| 1 | t | - | - | copy | It |
| 2 | " i" | t | s | copy | It |
| 3 | is | space | space | replace | It was |
| 5 | my... | - | - | copy rest | It was my boy friend. |

This trace shows that only the correctly bounded “is” is replaced, while punctuation and other words remain unaffected.

### Example 2

Input:

```
Is it your pencil?
```

| i | substring | condition | action | output |
| --- | --- | --- | --- | --- |
| 0 | Is | capital I | no replace | I |
| 1 | s | - | copy | Is |
| 2 | space+i | - | copy | Is |
| ... | ... | ... | ... | final unchanged |

The capitalized “Is” is not modified because matching is case-sensitive and requires exact lowercase “is”.

This confirms that boundary rules and case sensitivity are both enforced naturally by the scan logic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is visited once, and each check is constant time |
| Space | O(n) | Output list stores the final transformed string |

The linear scan fits comfortably within the 1-second limit for n up to 100,000, and memory usage remains proportional to the input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    buf = sio.StringIO()
    with redirect_stdout(buf):
        solve()
    return buf.getvalue().strip()

def solve():
    s = sys.stdin.readline().rstrip('\n')
    n = len(s)
    out = []
    i = 0
    while i < n:
        if i > 0 and i + 2 < n and s[i:i+2] == "is" and s[i-1] == ' ' and s[i+2] == ' ':
            out.append("was")
            i += 2
        else:
            out.append(s[i])
            i += 1
    print("".join(out))

assert run("It is my boy friend.") == "It was my boy friend."
assert run("Is it your pencil?") == "Is it your pencil?"
assert run("This is an island.") == "This was an island."
assert run("is") == "is"
assert run("A is B is C") == "A was B was C"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| It is my boy friend. | It was my boy friend. | Basic replacement |
| Is it your pencil? | Is it your pencil? | Case sensitivity |
| is | is | No surrounding spaces |
| A is B is C | A was B was C | Multiple replacements |

## Edge Cases

A key edge case is when “is” appears at the very beginning. For example, input “is here” should remain unchanged because there is no preceding space. During iteration at index 0, the boundary check `i > 0` fails immediately, so the algorithm safely copies the character without attempting a match.

Another case is trailing occurrences like “this is”. When the scan reaches the last valid position, the condition `i + 2 < n` prevents reading beyond the string, so no invalid access occurs and the final “is” is only replaced if followed by a space, which it is not. The output remains correct.

A third case involves punctuation adjacency such as “is,”. Even though the substring starts with “is”, the character following it is a comma, not a space, so the replacement condition fails. The algorithm preserves the original text exactly, demonstrating that strict boundary checks correctly enforce the definition of a standalone word.
