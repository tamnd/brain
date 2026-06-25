---
title: "CF 105809O - Obfuscation technique"
description: "This is an output-only problem. There is no input at all. The statement gives a sequence of hexadecimal byte values. Interpreting each pair of hexadecimal digits as an ASCII character reveals a hidden message."
date: "2026-06-25T15:30:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105809
codeforces_index: "O"
codeforces_contest_name: "Code Rush 2025"
rating: 0
weight: 105809
solve_time_s: 38
verified: true
draft: false
---

[CF 105809O - Obfuscation technique](https://codeforces.com/problemset/problem/105809/O)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

This is an output-only problem. There is no input at all.

The statement gives a sequence of hexadecimal byte values. Interpreting each pair of hexadecimal digits as an ASCII character reveals a hidden message. The task is simply to determine what that message is asking for and print the requested output.

Since there is no input and no computation depending on test cases, complexity is irrelevant. The entire challenge is recognizing that the provided text is hexadecimal ASCII encoding and decoding it correctly.

A common mistake is to print the decoded sentence itself instead of the value requested by the sentence.

For example, decoding

```
45 4C
```

gives

```
EL
```

but the full message decodes to:

```
EL CODIGO DE DESACTIVACION ES: "CODE:RUSH:TEC"
```

The sentence says that the deactivation code is `CODE:RUSH:TEC`, so that is the required output.

## Approaches

The brute-force approach is to manually decode every hexadecimal byte into its ASCII character and reconstruct the sentence. Since the message is fixed, this immediately gives the answer. The amount of work is constant.

There is no need for any algorithmic optimization because the input never changes. Once the hexadecimal string is decoded, the hidden message explicitly reveals the required output.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Manual hexadecimal decoding | O(1) | O(1) | Accepted |
| Directly print the discovered answer | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Observe that the provided text consists of hexadecimal byte values.
2. Convert each hexadecimal value to its ASCII character.
3. Reconstruct the message.
4. Read the decoded sentence:

`EL CODIGO DE DESACTIVACION ES: "CODE:RUSH:TEC"`.
5. Print the deactivation code requested by the message:

`CODE:RUSH:TEC`.

### Why it works

The hexadecimal sequence is a fixed encoding of an ASCII sentence. Decoding it uniquely determines the hidden message, and the message explicitly identifies the required output. Since there is no input, printing that discovered value is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

print("CODE:RUSH:TEC")
```

The solution does not read any input because the problem specifies that none exists.

The hexadecimal text in the statement is constant. After decoding it once, we know the required output is always the same string. Printing that string directly is the simplest and most reliable solution.

## Worked Examples

Since the problem has no input, every execution behaves identically.

### Execution Trace

| Step | Action | Result |
| --- | --- | --- |
| 1 | Decode hexadecimal text | `EL CODIGO DE DESACTIVACION ES: "CODE:RUSH:TEC"` |
| 2 | Extract requested code | `CODE:RUSH:TEC` |
| 3 | Print answer | `CODE:RUSH:TEC` |

This trace shows that the decoded sentence directly contains the value that must be printed.

### Another Execution

| Step | Action | Result |
| --- | --- | --- |
| 1 | Run program | No input required |
| 2 | Execute print statement | `CODE:RUSH:TEC` |

Because there is no input, every run produces the same correct output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a single fixed string is printed |
| Space | O(1) | No data structures are used |

The program performs a constant amount of work and uses constant memory, which easily satisfies any reasonable limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    print("CODE:RUSH:TEC")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue()

assert run("") == "CODE:RUSH:TEC\n", "empty input"
assert run("\n") == "CODE:RUSH:TEC\n", "extra newline"
assert run("anything\n") == "CODE:RUSH:TEC\n", "ignored data"
assert run("123 456\n789\n") == "CODE:RUSH:TEC\n", "still constant output"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty input | `CODE:RUSH:TEC` | Official behavior |
| single newline | `CODE:RUSH:TEC` | No input processing required |
| arbitrary text | `CODE:RUSH:TEC` | Output is constant |
| multiple lines | `CODE:RUSH:TEC` | Output-only nature of the problem |

## Edge Cases

The main non-obvious pitfall is printing the entire decoded sentence instead of the requested code.

If the decoded text is:

```
EL CODIGO DE DESACTIVACION ES: "CODE:RUSH:TEC"
```

the correct output is:

```
CODE:RUSH:TEC
```

The algorithm handles this because it interprets the sentence and prints only the code identified by the message.

Another possible mistake is including the quotation marks.

Correct output:

```
CODE:RUSH:TEC
```

Incorrect output:

```
"CODE:RUSH:TEC"
```

The required answer is the code itself, without surrounding quotes. The provided solution prints exactly that string.
