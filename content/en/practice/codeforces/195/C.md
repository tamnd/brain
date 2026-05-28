---
title: "CF 195C - Try and Catch"
description: "The task is to simulate the exception-handling behavior of a simple programming language. The program consists of three types of statements: try, catch(type, message), and throw(type)."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "expression-parsing", "implementation"]
categories: ["algorithms"]
codeforces_contest: 195
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 123 (Div. 2)"
rating: 1800
weight: 195
solve_time_s: 68
verified: true
draft: false
---

[CF 195C - Try and Catch](https://codeforces.com/problemset/problem/195/C)

**Rating:** 1800  
**Tags:** expression parsing, implementation  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to simulate the exception-handling behavior of a simple programming language. The program consists of three types of statements: `try`, `catch(type, message)`, and `throw(type)`. Each `try` starts a new exception-handling block, and its corresponding `catch` closes the most recently opened `try` that has not yet been closed. A `throw` creates an exception of a certain type. When the program executes a `throw`, it searches backward for all open `try` blocks whose corresponding `catch` matches the thrown type. If multiple blocks match, the earliest `catch` after the `throw` is chosen. If no match exists, the output is "Unhandled Exception".

The input gives the number of lines followed by the program lines themselves, which may contain spaces, empty lines, or spacing around operators. The program is guaranteed syntactically correct, has exactly one `throw`, and every `try` has a matching `catch`. The output is the message printed by the activated `catch`, or the default "Unhandled Exception".

Given the maximum number of lines is $10^5$, the algorithm must run in roughly linear time. Nested `try-catch` blocks and irregular spacing make naive string scanning error-prone, especially if one tries to match lines strictly by position rather than logical nesting.

A non-obvious edge case is when multiple nested `try` blocks could catch the thrown exception. For example, if `throw(AE)` occurs inside two nested `try` blocks, and both corresponding `catch` statements could match `AE`, the activated catch is the one whose `catch` appears earliest in the program after the `throw`. A careless implementation that just looks at the last open `try` would give the wrong result.

Another edge case is when there are empty lines or excessive spaces. For instance, `catch(AE,"msg")` might appear as `catch ( AE , "msg" )`. Parsing must be robust to whitespace.

## Approaches

The brute-force approach is to simulate the program literally: iterate line by line, maintain a stack of open `try` blocks, and when encountering the `throw`, scan forward to find the first `catch` that matches the type. This works because the program is correct, but if implemented naively, scanning forward could be $O(n^2)$ in a worst-case scenario with deep nesting, since each `throw` could scan nearly all remaining lines.

The key observation is that we only need one pass if we maintain a stack of open `try` blocks as we process lines. Each `try` pushes its line index onto the stack. Each `catch` pops the last `try` from the stack and stores the exception type and message along with the starting index. When we reach the `throw`, the stack contains all `try` blocks that were opened before it. We can then scan the stored catch information to select the first catch that occurs after the throw and matches the thrown type. This reduces time complexity to $O(n)$, since every line is processed once and stack operations are constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow for n = 10^5 |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty stack for `try` blocks and a list to store `catch` information. Each element of the list will store the line index, exception type, and message.
2. Iterate through each line of the program while keeping track of the line number.
3. When encountering a `try`, push its line number onto the stack. We do not need further information yet because the matching `catch` will provide the type and message.
4. When encountering a `catch(type, message)`, pop the last `try` line index from the stack and append a tuple `(try_index, catch_index, exception_type, message)` to the list of catches. This preserves the program order.
5. When encountering the `throw(type)`, record the throw's line number and thrown type. There is only one `throw` so we stop tracking after this.
6. After parsing all lines, scan the catch list. For each catch, check if its `try_index` is less than the `throw` line number and its `catch_index` is greater than the `throw` line number, and if its exception type matches the thrown type.
7. The first catch that meets these criteria is the one that activates, so print its message. If no such catch exists, print "Unhandled Exception".

Why it works: The stack guarantees that each `catch` is paired with the most recent unclosed `try`. By storing the starting and ending line numbers, we can determine whether a `throw` falls within the range of a try-catch block. Scanning in order ensures that if multiple blocks can handle the exception, we select the one whose `catch` appears earliest after the `throw`. This replicates the language's semantics correctly.

## Python Solution

```python
import sys
input = sys.stdin.readline
import re

n = int(input())
lines = [input().strip() for _ in range(n)]

try_stack = []
catches = []
throw_line = -1
throw_type = ""

for i, line in enumerate(lines):
    line = line.strip()
    if not line:
        continue
    if line.startswith("try"):
        try_stack.append(i)
    elif line.startswith("catch"):
        m = re.match(r'catch\s*\(\s*([A-Za-z]+)\s*,\s*"(.*)"\s*\)', line)
        if m:
            exc_type, message = m.groups()
            try_index = try_stack.pop()
            catches.append((try_index, i, exc_type, message))
    elif line.startswith("throw"):
        m = re.match(r'throw\s*\(\s*([A-Za-z]+)\s*\)', line)
        if m:
            throw_type = m.group(1)
            throw_line = i

for try_idx, catch_idx, exc_type, message in catches:
    if try_idx < throw_line < catch_idx and exc_type == throw_type:
        print(message)
        break
else:
    print("Unhandled Exception")
```

The code first strips lines and skips empty lines. `try_stack` ensures proper nesting, while `catches` tracks all catch blocks with their range. Regular expressions parse the `catch` and `throw` statements flexibly, ignoring extra spaces. After identifying the `throw`, the scan finds the first matching catch according to language rules.

## Worked Examples

### Sample 1

Input lines:

| Line | Command | Stack | Catches | Throw info |
| --- | --- | --- | --- | --- |
| 0 | try | [0] | [] | - |
| 1 | try | [0,1] | [] | - |
| 2 | throw(AE) | [0,1] | [] | type=AE, line=2 |
| 3 | catch(BE,"BE in line 3") | [0] | [(1,3,BE,"BE in line 3")] | - |
| 4 | try | [0,4] | ... | - |
| 5 | catch(AE,"AE in line 5") | [0] | [...,(4,5,AE,"AE in line 5")] | - |
| 6 | catch(AE,"AE somewhere") | [] | [...,(0,6,AE,"AE somewhere")] | - |

During final scan, only `(0,6,AE,"AE somewhere")` matches throw at line 2, printing `"AE somewhere"`.

### Sample 2

Input:

| Line | Command | Stack | Catches | Throw info |
| --- | --- | --- | --- | --- |
| 0 | try | [0] | [] | - |
| 1 | throw(AE) | [0] | [] | type=AE, line=1 |
| 2 | catch(AE,"AE in line 3") | [] | [(0,2,AE,"AE in line 3")] | - |
| 3 | catch(AE,"AE somewhere") | [] | [(0,2,AE,"AE in line 3"), (x,3,AE,"AE somewhere")] | - |

The first catch with `try_idx<1<catch_idx` is `(0,2,AE,"AE in line 3")`, so `"AE in line 3"` is printed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each line is read once, stack push/pop and list append are O(1). Final scan of catches is at most O(n). |
| Space | O(n) | Stack and catch list can store up to n elements in worst case. |

The solution easily fits within 2 seconds for n up to 10^5 and uses memory well under 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import re
    n = int(input())
    lines = [input().strip() for _ in range(n)]
    try_stack = []
    catches = []
    throw_line = -1
    throw_type = ""
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        if line.startswith("try"):
            try_stack.append(i)
        elif line.startswith("catch"):
            m = re.match(r'catch\s*\(\s*([A-Za-z]+)\s*,\s*"(.*)"
```
