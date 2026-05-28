---
title: "CF 162D - Remove digits"
description: "We are given a single string containing printable ASCII characters. Some of those characters may be digits from '0' to '9'. The task is to remove every digit and print the remaining characters in their original order."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 162
codeforces_index: "D"
codeforces_contest_name: "VK Cup 2012 Wild-card Round 1"
rating: 1900
weight: 162
solve_time_s: 75
verified: true
draft: false
---

[CF 162D - Remove digits](https://codeforces.com/problemset/problem/162/D)

**Rating:** 1900  
**Tags:** *special  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single string containing printable ASCII characters. Some of those characters may be digits from `'0'` to `'9'`. The task is to remove every digit and print the remaining characters in their original order.

The statement mentions that characters shift left after removal, but that detail only describes how string deletion works conceptually. We do not actually need to simulate repeated deletions. The final result is simply the subsequence of non-digit characters.

The input length is at most 100 characters, which is extremely small. Even inefficient approaches would fit comfortably within the limits. A quadratic solution with repeated deletions would perform at most around 10,000 character operations, which is trivial for a 3 second limit. Still, the cleanest solution scans the string once and builds the answer directly.

There are several edge cases that can quietly break careless implementations.

A string containing only digits should produce an empty line.

Input:

```
12345
```

Correct output:

```

```

A buggy implementation might accidentally print spaces or fail to print a newline.

Digits may appear anywhere, not only at the ends.

Input:

```
a1b2c3
```

Correct output:

```
abc
```

An incorrect solution that removes only the first digit or stops early would fail here.

The string may contain symbols that are not letters or digits.

Input:

```
VK-Cup-2012!
```

Correct output:

```
VK-Cup-!
```

The hyphens and exclamation mark must stay. Only numeric characters are removed.

## Approaches

The most direct brute-force idea is to repeatedly search for a digit and erase it from the string. Since strings are immutable in Python, every deletion creates a new string, so removing one character costs linear time. If the string has length `n`, and we remove digits one by one, the total complexity becomes `O(n^2)` in the worst case.

For this problem, even that approach is fast enough because `n ≤ 100`. Still, it does unnecessary work. Every deletion shifts characters left, which means the same characters may be copied many times.

The better observation is that we never need to physically delete characters. The final answer consists exactly of the characters that are not digits. Instead of modifying the original string, we can scan it once from left to right and append every non-digit character to the result.

This reduces the work to a single pass over the string. Each character is checked once, and appended at most once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input string.
2. Create an empty list that will store the characters we want to keep.
3. Iterate through the string character by character.
4. For each character, check whether it is a digit.

In Python, `ch.isdigit()` returns `True` for numeric characters and `False` otherwise.
5. If the character is not a digit, append it to the result list.

We keep all letters, punctuation marks, and symbols unchanged.
6. After processing the entire string, join the collected characters into one final string.
7. Print the result.

### Why it works

The algorithm processes every character exactly once. During the scan, it preserves the relative order of all non-digit characters because they are appended in the same order they appear in the input. Every digit is skipped, so no digit can appear in the output. Since every character is either skipped or appended exactly once, the produced string is precisely the original string with all digits removed.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

result = []

for ch in s:
    if not ch.isdigit():
        result.append(ch)

print("".join(result))
```

The program starts by reading the input string. Using `strip()` removes the trailing newline from input.

The `result` list stores all characters that survive the filtering step. Using a list is efficient because appending characters is `O(1)`, while repeatedly concatenating strings would create many temporary strings.

The loop examines each character independently. If `isdigit()` returns `False`, the character is added to the answer. Digits are ignored completely.

Finally, `"".join(result)` converts the collected characters into the final string. If every character was a digit, the list remains empty and `join` correctly produces an empty string.

## Worked Examples

### Example 1

Input:

```
VK-Cup-2012!
```

| Current character | Digit? | Result so far |
| --- | --- | --- |
| V | No | V |
| K | No | VK |
| - | No | VK- |
| C | No | VK-C |
| u | No | VK-Cu |
| p | No | VK-Cup |
| - | No | VK-Cup- |
| 2 | Yes | VK-Cup- |
| 0 | Yes | VK-Cup- |
| 1 | Yes | VK-Cup- |
| 2 | Yes | VK-Cup- |
| ! | No | VK-Cup-! |

Final output:

```
VK-Cup-!
```

This trace shows that symbols are preserved exactly as they appear. Only numeric characters are skipped.

### Example 2

Input:

```
a1b2c3
```

| Current character | Digit? | Result so far |
| --- | --- | --- |
| a | No | a |
| 1 | Yes | a |
| b | No | ab |
| 2 | Yes | ab |
| c | No | abc |
| 3 | Yes | abc |

Final output:

```
abc
```

This example demonstrates that digits can appear between normal characters and are removed independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once |
| Space | O(n) | The result may store all characters |

With `n ≤ 100`, the algorithm easily fits within the limits. Even much slower approaches would pass, but the linear scan is both simpler and more efficient.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    s = input().strip()

    result = []

    for ch in s:
        if not ch.isdigit():
            result.append(ch)

    print("".join(result))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run("VK-Cup-2012!\n") == "VK-Cup-!\n", "sample 1"

# custom cases
assert run("12345\n") == "\n", "all digits"
assert run("abc\n") == "abc\n", "no digits"
assert run("a1b2c3\n") == "abc\n", "digits between letters"
assert run("9\n") == "\n", "minimum size, single digit"
assert run("!@#456$%^789&*\n") == "!@#$%^&*\n", "symbols preserved"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `12345` | empty string | Handles all-digit input |
| `abc` | `abc` | Leaves digit-free strings unchanged |
| `a1b2c3` | `abc` | Removes digits in the middle |
| `9` | empty string | Minimum-size edge case |
| `!@#456$%^789&*` | `!@#$%^&*` | Preserves punctuation and symbols |

## Edge Cases

Consider the input:

```
12345
```

The algorithm scans every character. Since all characters are digits, none are appended to `result`.

| Character | Action | Result |
| --- | --- | --- |
| 1 | Skip | "" |
| 2 | Skip | "" |
| 3 | Skip | "" |
| 4 | Skip | "" |
| 5 | Skip | "" |

At the end, `join(result)` produces an empty string, which is exactly the required output.

Now consider:

```
a0!
```

The scan proceeds as follows:

| Character | Action | Result |
| --- | --- | --- |
| a | Append | a |
| 0 | Skip | a |
| ! | Append | a! |

The digit is removed, while the punctuation mark remains untouched.

Finally, consider:

```
007bond
```

| Character | Action | Result |
| --- | --- | --- |
| 0 | Skip | "" |
| 0 | Skip | "" |
| 7 | Skip | "" |
| b | Append | b |
| o | Append | bo |
| n | Append | bon |
| d | Append | bond |

Leading digits are handled naturally because the algorithm does not rely on positions or indices. It simply filters characters based on whether they are digits.
