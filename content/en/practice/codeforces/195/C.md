---
title: "CF 195C - Try and Catch"
description: "We are given the source code of a tiny language that contains only three kinds of statements: try, catch(type, message), and exactly one throw(type). Each try is paired with a later catch, forming a try-catch block."
date: "2026-06-05T00:36:58+07:00"
tags: ["codeforces", "competitive-programming", "expression-parsing", "implementation"]
categories: ["algorithms"]
codeforces_contest: 195
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 123 (Div. 2)"
rating: 1800
weight: 195
solve_time_s: 143
verified: true
draft: false
---

[CF 195C - Try and Catch](https://codeforces.com/problemset/problem/195/C)

**Rating:** 1800  
**Tags:** expression parsing, implementation  
**Solve time:** 2m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the source code of a tiny language that contains only three kinds of statements: `try`, `catch(type, message)`, and exactly one `throw(type)`.

Each `try` is paired with a later `catch`, forming a try-catch block. The input is guaranteed to be syntactically correct, so these blocks are properly nested.

When an exception is thrown, we must determine which catch block handles it. A catch block can handle the exception if three conditions hold:

1. Its corresponding `try` appears before the `throw`.
2. Its `catch` appears after the `throw`.
3. Its exception type matches the thrown type.

Among all such blocks, the language chooses the one whose `catch` statement appears earliest after the throw. We must print that catch block's message. If no block matches, we print:

```
Unhandled Exception
```

The program contains at most $10^5$ lines. This immediately rules out any solution that repeatedly scans large portions of the program. A quadratic algorithm would require roughly $10^{10}$ operations in the worst case, which is far beyond the limit. We need a linear or near-linear solution.

The parsing itself is also part of the challenge. Lines may contain arbitrary spaces around keywords, parentheses, commas, and quotes. A solution that relies on exact formatting will fail.

One subtle point is that the selected handler is not necessarily the innermost surrounding `try`. The language chooses the matching block whose `catch` occurs first after the throw.

Consider:

```
try
    try
        throw(AE)
    catch(BE,"x")
catch(AE,"y")
```

The inner block surrounds the throw, but its exception type does not match. The correct output is:

```
y
```

Another easy mistake is to search only among blocks that are still "open" when the throw is reached. The language's definition depends on the relative positions of `try`, `throw`, and `catch`, not on simulating execution.

For example:

```
try
    throw(AE)
catch(AE,"first")
try
catch(AE,"second")
```

The correct output is:

```
first
```

because the first matching catch after the throw is chosen.

A third edge case occurs when no handler matches:

```
try
    throw(AE)
catch(BE,"wrong")
```

The output must be:

```
Unhandled Exception
```

even though the throw lies inside a try-catch block.

## Approaches

A brute-force solution would first reconstruct all try-catch blocks. Then, after locating the throw, it could examine every block and check whether:

- the block's `try` is before the throw,
- the block's `catch` is after the throw,
- the exception types match.

Among all qualifying blocks, we would choose the one with the smallest catch position.

This approach is correct because it directly implements the specification. If there are $m$ blocks, the work is $O(m)$, which is already acceptable. The real difficulty is reconstructing the blocks efficiently while parsing.

A less careful implementation might repeatedly search for matching catches or repeatedly traverse nesting structures, leading to $O(n^2)$ behavior on deeply nested input.

The key observation is that the program structure is perfectly nested. Every `catch` closes the most recent unmatched `try`. This is exactly the behavior of a stack.

While scanning the program once, we can push the line number of every `try`. When a `catch` appears, it closes the topmost `try`, allowing us to immediately construct one complete block.

After collecting all blocks and locating the single throw, determining the answer becomes a simple linear scan over the blocks.

The entire solution runs in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with repeated searches | O(n²) | O(n) | Too slow |
| Stack-based parsing + one scan | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all program lines.
2. For every line, remove leading and trailing whitespace.
3. Detect which statement the line contains.
4. When a `try` is found, push its line index onto a stack.

The most recent unmatched `try` must be the one closed next.
5. When a `catch(type,message)` is found, pop the stack.

The popped position is the matching `try` for this catch. Store a record containing:

- try position
- catch position
- exception type
- message
6. When a `throw(type)` is found, store:

- throw position
- thrown exception type
7. After parsing the whole program, examine every recorded block.
8. A block can handle the exception if:

- `try_position < throw_position`
- `catch_position > throw_position`
- `block_type == thrown_type`
9. Among all matching blocks, choose the one with the smallest catch position.
10. Print its message.
11. If no block qualifies, print:

```
Unhandled Exception
```

### Why it works

The stack reconstruction is correct because the statement guarantees that every `catch` closes the most recently opened unmatched `try`. This is exactly the standard parenthesis-matching property.

Every recorded block therefore contains the correct pair of positions. A block is eligible precisely when its `try` is before the throw and its `catch` is after the throw, matching the language definition. Among eligible blocks, selecting the smallest catch position implements the rule that the earliest catch after the throw is activated. Since every possible block is checked exactly once, the algorithm cannot miss the correct handler.

## Python Solution

```python
import sys
import re

input = sys.stdin.readline

def solve():
    n = int(input())

    stack = []
    blocks = []

    throw_pos = -1
    throw_type = ""

    catch_re = re.compile(
        r'catch\s*\(\s*([A-Za-z]+)\s*,\s*"([^"]+)"\s*\)'
    )
    throw_re = re.compile(
        r'throw\s*\(\s*([A-Za-z]+)\s*\)'
    )

    for i in range(n):
        line = input().strip()

        if not line:
            continue

        if line.startswith("try"):
            stack.append(i)

        elif line.startswith("throw"):
            m = throw_re.match(line)
            throw_type = m.group(1)
            throw_pos = i

        elif line.startswith("catch"):
            m = catch_re.match(line)
            exc_type = m.group(1)
            message = m.group(2)

            try_pos = stack.pop()
            blocks.append((try_pos, i, exc_type, message))

    answer = None
    best_catch_pos = n + 1

    for try_pos, catch_pos, exc_type, message in blocks:
        if (
            try_pos < throw_pos < catch_pos
            and exc_type == throw_type
        ):
            if catch_pos < best_catch_pos:
                best_catch_pos = catch_pos
                answer = message

    if answer is None:
        print("Unhandled Exception")
    else:
        print(answer)

solve()
```

The first part of the code parses the program while reconstructing try-catch blocks. The stack stores unmatched `try` positions. Whenever a `catch` appears, the top of the stack is the only valid matching `try`, so we immediately create a complete block record.

Regular expressions handle arbitrary spacing. This avoids many parsing bugs caused by inputs such as:

```
catch ( AE , "msg" )
```

or

```
throw( AE )
```

The second phase evaluates every block against the thrown exception. The condition

```
try_pos < throw_pos < catch_pos
```

exactly matches the statement's requirement that the throw lies inside the block.

The final tie-breaking uses the smallest catch position, because the language chooses the matching catch that appears first after the throw.

## Worked Examples

### Example 1

Input:

```
try
    try
        throw(AE)
    catch(BE,"BE in line 3")

    try
    catch(AE,"AE in line 5")
catch(AE,"AE somewhere")
```

| Event | Stack After Event | Recorded Blocks |
| --- | --- | --- |
| try at 0 | [0] | - |
| try at 1 | [0,1] | - |
| throw(AE) at 2 | [0,1] | - |
| catch(BE) at 3 | [0] | (1,3,BE) |
| try at 5 | [0,5] | previous |
| catch(AE) at 6 | [0] | (5,6,AE) |
| catch(AE) at 7 | [] | (0,7,AE) |

Checking the blocks:

| Block | Contains Throw? | Type Match? | Eligible? |
| --- | --- | --- | --- |
| (1,3,BE) | Yes | No | No |
| (5,6,AE) | No | Yes | No |
| (0,7,AE) | Yes | Yes | Yes |

The selected message is:

```
AE somewhere
```

This example shows that a matching type is not enough. The throw must also lie between the corresponding try and catch.

### Example 2

```
try
    try
        throw(AE)
    catch(AE,"inner")
catch(AE,"outer")
```

| Block | Try Position | Catch Position | Type |
| --- | --- | --- | --- |
| Inner | 1 | 3 | AE |
| Outer | 0 | 4 | AE |

Both blocks contain the throw and both types match.

| Block | Catch Position |
| --- | --- |
| Inner | 3 |
| Outer | 4 |

The earliest catch is position 3, so the answer is:

```
inner
```

This demonstrates the tie-breaking rule.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to parse, one pass over blocks |
| Space | O(n) | Stack and stored block information |

With at most $10^5$ lines, linear processing is easily fast enough. Memory usage is also linear and comfortably fits within the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
import re

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())

    stack = []
    blocks = []

    throw_pos = -1
    throw_type = ""

    catch_re = re.compile(
        r'catch\s*\(\s*([A-Za-z]+)\s*,\s*"([^"]+)"\s*\)'
    )
    throw_re = re.compile(
        r'throw\s*\(\s*([A-Za-z]+)\s*\)'
    )

    for i in range(n):
        line = input().strip()

        if not line:
            continue

        if line.startswith("try"):
            stack.append(i)

        elif line.startswith("throw"):
            m = throw_re.match(line)
            throw_type = m.group(1)
            throw_pos = i

        elif line.startswith("catch"):
            m = catch_re.match(line)
            exc_type = m.group(1)
            message = m.group(2)

            blocks.append((stack.pop(), i, exc_type, message))

    ans = None
    best = n + 1

    for l, r, typ, msg in blocks:
        if l < throw_pos < r and typ == throw_type:
            if r < best:
                best = r
                ans = msg

    return (ans if ans is not None else "Unhandled Exception") + "\n"

# provided sample
assert run(
"""8
try
    try
        throw ( AE )
    catch ( BE, "BE in line 3" )

    try
    catch(AE, "AE in line 5")
catch(AE,"AE somewhere")
"""
) == "AE somewhere\n"

# minimum size
assert run(
"""3
try
throw(AE)
catch(AE,"ok")
"""
) == "ok\n"

# no matching handler
assert run(
"""3
try
throw(AE)
catch(BE,"x")
"""
) == "Unhandled Exception\n"

# earliest catch wins
assert run(
"""5
try
try
throw(AE)
catch(AE,"inner")
catch(AE,"outer")
"""
) == "inner\n"

# spaces everywhere
assert run(
"""3
try
 throw (  ABC  )
 catch ( ABC , "works" )
"""
) == "works\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single try-catch around throw | `ok` | Smallest valid instance |
| Mismatched exception type | `Unhandled Exception` | No handler found |
| Nested matching handlers | `inner` | Earliest catch selection |
| Heavy whitespace variation | `works` | Robust parsing |
| Official sample | `AE somewhere` | Full specification |

## Edge Cases

### Matching outer block, non-matching inner block

Input:

```
3
try
throw(AE)
catch(BE,"x")
```

The only block contains the throw, but its type is `BE` while the thrown type is `AE`.

The algorithm records one block:

| Try | Catch | Type |
| --- | --- | --- |
| 0 | 2 | BE |

The type comparison fails, so no candidate is selected and the output becomes:

```
Unhandled Exception
```

### Multiple matching handlers

Input:

```
5
try
try
throw(AE)
catch(AE,"inner")
catch(AE,"outer")
```

Recorded blocks:

| Try | Catch | Type |
| --- | --- | --- |
| 1 | 3 | AE |
| 0 | 4 | AE |

Both contain the throw and both match the type. The algorithm chooses the smaller catch position, namely `3`, producing:

```
inner
```

### Handler after throw but try starts after throw

Input:

```
5
throw(AE)
try
catch(AE,"later")
try
catch(AE,"another")
```

Neither block satisfies:

```
try_position < throw_position
```

so neither can handle the exception.

The algorithm rejects both blocks and prints:

```
Unhandled Exception
```

which matches the language definition.
