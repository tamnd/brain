---
title: "CF 106215A - An Unfortunate Coincidence"
description: "We are given n words. For each word, we must check whether it is exactly the string \"WY\". If a word is exactly \"WY\", we replace it with \"Whitney Young\" in the output. Every other word must be printed unchanged. The input consists of an integer n, followed by n strings."
date: "2026-06-25T06:50:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106215
codeforces_index: "A"
codeforces_contest_name: "2025-2026 Whitney Young Practice Contest 1"
rating: 0
weight: 106215
solve_time_s: 40
verified: true
draft: false
---

[CF 106215A - An Unfortunate Coincidence](https://codeforces.com/problemset/problem/106215/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given `n` words. For each word, we must check whether it is exactly the string `"WY"`.

If a word is exactly `"WY"`, we replace it with `"Whitney Young"` in the output. Every other word must be printed unchanged.

The input consists of an integer `n`, followed by `n` strings. Each string contains only uppercase and lowercase English letters. The output contains exactly `n` lines, one result for each input word.

The constraints are extremely small. There are at most 2025 words, and each word has length at most 67. Even the most direct solution that examines every character of every word performs only a few hundred thousand operations. Any linear scan is easily fast enough.

The main source of mistakes is misunderstanding what counts as a match.

Consider the input:

```
3
WY
wy
WYOMING
```

The correct output is:

```
Whitney Young
wy
WYOMING
```

Only the first word is replaced. The comparison is case-sensitive, so `"wy"` does not match. Also, `"WYOMING"` contains `"WY"` as a prefix, but the entire word is not equal to `"WY"`.

Another easy mistake is attempting substring replacement. For example:

```
2
AWYB
WY
```

The correct output is:

```
AWYB
Whitney Young
```

Only complete-word equality matters.

## Approaches

The most straightforward solution is to process the words one by one.

For each word, compare it with `"WY"`.

If they are equal, print `"Whitney Young"`. Otherwise, print the original word.

A brute-force interpretation might check every character manually. Since each word is at most 67 characters long, this still runs comfortably within the limits. The total work is proportional to the total number of input characters.

The key observation is that the task is not asking for pattern matching inside a string. It only asks whether a word is exactly equal to one specific value. Modern languages already provide string equality operations, making the solution almost trivial.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force character-by-character comparison | O(total input length) | O(1) | Accepted |
| Direct string equality check | O(total input length) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`.
2. Repeat `n` times:

Read the next word.
3. If the word is exactly `"WY"`, print `"Whitney Young"`.
4. Otherwise, print the word unchanged.

### Why it works

For every input word, the problem defines exactly one condition that triggers replacement: the word must be equal to `"WY"`.

The algorithm checks precisely that condition. When the condition is true, it outputs the required replacement text. When the condition is false, it outputs the original word. Since every word is handled independently and according to the problem definition, the produced output is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

for _ in range(n):
    s = input().strip()
    if s == "WY":
        print("Whitney Young")
    else:
        print(s)
```

The program first reads the number of words.

Each subsequent line is read and stripped of its trailing newline. The comparison `s == "WY"` performs an exact, case-sensitive equality check.

When the comparison succeeds, the required replacement text is printed. Otherwise, the original word is printed unchanged.

Using `strip()` is important because input lines contain a trailing newline character. Without removing it, the comparison against `"WY"` would fail.

No additional data structures are needed because each word can be processed immediately after reading it.

## Worked Examples

### Example 1

Input:

```
9
I
miss
WY
Math
Team
and
WY
Coding
Club
```

Trace:

| Word | Equals "WY"? | Output |
| --- | --- | --- |
| I | No | I |
| miss | No | miss |
| WY | Yes | Whitney Young |
| Math | No | Math |
| Team | No | Team |
| and | No | and |
| WY | Yes | Whitney Young |
| Coding | No | Coding |
| Club | No | Club |

Output:

```
I
miss
Whitney Young
Math
Team
and
Whitney Young
Coding
Club
```

This example shows that every occurrence of the exact word `"WY"` is replaced independently.

### Example 2

Input:

```
4
WY
wy
WYOMING
WY
```

Trace:

| Word | Equals "WY"? | Output |
| --- | --- | --- |
| WY | Yes | Whitney Young |
| wy | No | wy |
| WYOMING | No | WYOMING |
| WY | Yes | Whitney Young |

Output:

```
Whitney Young
wy
WYOMING
Whitney Young
```

This demonstrates both case sensitivity and the requirement that the entire word must match.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total input length) | Each word is read once and compared once |
| Space | O(1) | Only one word is stored at a time |

The total input size is tiny, so this solution runs comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())
    for _ in range(n):
        s = input().strip()
        if s == "WY":
            print("Whitney Young")
        else:
            print(s)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run(
"""9
I
miss
WY
Math
Team
and
WY
Coding
Club
"""
) == (
"""I
miss
Whitney Young
Math
Team
and
Whitney Young
Coding
Club
"""
)

# minimum size
assert run(
"""1
WY
"""
) == (
"""Whitney Young
"""
)

# no replacements
assert run(
"""3
abc
DEF
Wy
"""
) == (
"""abc
DEF
Wy
"""
)

# all replacements
assert run(
"""4
WY
WY
WY
WY
"""
) == (
"""Whitney Young
Whitney Young
Whitney Young
Whitney Young
"""
)

# substring but not exact match
assert run(
"""3
AWYB
WYOMING
WY
"""
) == (
"""AWYB
WYOMING
Whitney Young
"""
)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single word `WY` | `Whitney Young` | Minimum input size |
| No word equals `WY` | Original words | No accidental replacements |
| All words equal `WY` | All replaced | Repeated replacements |
| `AWYB`, `WYOMING`, `WY` | Only last replaced | Exact equality, not substring matching |

## Edge Cases

Consider:

```
1
wy
```

The algorithm compares `"wy"` with `"WY"`. Since string comparison is case-sensitive, they are different. The output remains:

```
wy
```

This correctly handles case differences.

Consider:

```
1
WYOMING
```

The algorithm checks whether the entire string equals `"WY"`. It does not, so the output is:

```
WYOMING
```

This avoids the common mistake of replacing words that merely contain `"WY"` as a substring.

Consider:

```
3
WY
WY
WY
```

Each word is processed independently. Every comparison succeeds, producing:

```
Whitney Young
Whitney Young
Whitney Young
```

The algorithm does not stop after the first replacement and correctly handles multiple occurrences.
