---
title: "CF 106102L - Texting"
description: "We are given several text messages. A message is considered a \"battle\" if it contains a run of at least three consecutive letters a, ignoring case. That means sequences such as aaa, AaA, aAA, and AAA all qualify."
date: "2026-06-25T11:50:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106102
codeforces_index: "L"
codeforces_contest_name: "AGM 2025, Final Round, Day 1"
rating: 0
weight: 106102
solve_time_s: 36
verified: true
draft: false
---

[CF 106102L - Texting](https://codeforces.com/problemset/problem/106102/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several text messages. A message is considered a "battle" if it contains a run of at least three consecutive letters `a`, ignoring case. That means sequences such as `aaa`, `AaA`, `aAA`, and `AAA` all qualify.

For each message, we must determine whether such a run exists anywhere inside the text.

If a qualifying run appears, we print:

```
Love is war!
```

Otherwise we print:

```
Just friends <3
```

The messages may contain spaces and other characters, so each entire line must be read as a complete string.

The constraints are small. Each message is at most 100 characters long, so even a straightforward scan of every character is easily fast enough. If there are `n` messages, the total work is proportional to the total number of characters across all messages.

The main implementation detail that causes mistakes is case-insensitive matching. A sequence like:

```
AAa
```

must be treated exactly the same as:

```
aaa
```

Another easy mistake is resetting the consecutive count incorrectly when encountering a non-`a` character.

Consider the message:

```
aabaa
```

The longest consecutive run of `a` has length 2, so the correct output is:

```
Just friends <3
```

A solution that only counts the total number of `a` characters would incorrectly classify this as a battle.

As another example:

```
xAAAy
```

contains three consecutive `a` letters after converting to lowercase, so the correct output is:

```
Love is war!
```

A case-sensitive implementation would miss this.

## Approaches

The brute-force idea is to examine every possible substring of length at least three and check whether all characters in that substring are the letter `a` under case-insensitive comparison.

For a message of length `m`, there are O(m²) substrings, and checking each one may take additional time. Although the limits here are tiny and this would still pass, it performs much more work than necessary.

The structure of the problem gives a simpler observation. We do not actually care where a run starts or ends. We only need to know whether any consecutive run of `a` reaches length 3.

That suggests scanning the message once while maintaining the current length of the ongoing run of `a` characters. When we see an `a` (after converting the character to lowercase), we increase the run length. Any other character breaks the run and resets the counter to zero.

The moment the counter reaches 3, we already know the answer for that message.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m²) | O(1) | Unnecessary |
| Optimal | O(m) | O(1) | Accepted |

Here `m` denotes the length of a single message.

## Algorithm Walkthrough

1. Read the integer `n`.
2. Repeat `n` times, reading one complete message line each time.
3. Initialize a counter `run = 0`.
4. Scan the message character by character.
5. Convert the current character to lowercase.
6. If the character is `'a'`, increase `run` by 1. Otherwise set `run = 0`.
7. If `run` becomes at least 3, mark the message as a battle and stop scanning that message.
8. Output `"Love is war!"` if a battle was found. Otherwise output `"Just friends <3"`.

### Why it works

The variable `run` always stores the length of the current suffix consisting entirely of consecutive `a` characters, ignoring case.

Whenever a non-`a` character appears, any consecutive sequence ending at the previous position is broken, so resetting `run` to zero is correct.

A message contains a valid battle exactly when some consecutive run of `a` reaches length at least three. The algorithm detects that event the first time `run >= 3`, and if it never happens, no qualifying run exists anywhere in the message.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

for _ in range(n):
    s = input().rstrip("\n")

    run = 0
    battle = False

    for ch in s:
        if ch.lower() == 'a':
            run += 1
            if run >= 3:
                battle = True
                break
        else:
            run = 0

    if battle:
        print("Love is war!")
    else:
        print("Just friends <3")
```

The first line reads the number of messages. Each subsequent line is processed independently.

The counter `run` tracks the current consecutive sequence of `a` characters. Using `ch.lower()` guarantees that uppercase and lowercase versions are treated identically.

The early `break` is not required for correctness, but it avoids extra work once the answer is already known.

Using `rstrip("\n")` removes only the trailing newline produced by input, while preserving any spaces that are part of the message itself.

## Worked Examples

### Example 1

Input message:

```
THIS MEANS WAAAAAARRRRRRRRRR
```

| Character | Lowercase | run |
| --- | --- | --- |
| W | w | 0 |
| A | a | 1 |
| A | a | 2 |
| A | a | 3 |

At the third consecutive `a`, the condition is satisfied and the answer becomes:

```
Love is war!
```

This example shows that uppercase letters must be treated the same as lowercase letters.

### Example 2

Input message:

```
what is a aardvark
```

| Character | Lowercase | run |
| --- | --- | --- |
| a | a | 1 |
| space | space | 0 |
| a | a | 1 |
| a | a | 2 |
| r | r | 0 |

The longest consecutive run has length 2, so no battle exists.

Output:

```
Just friends <3
```

This example demonstrates why counting total occurrences of `a` is insufficient. Only consecutive occurrences matter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m) | Each character is examined once |
| Space | O(1) | Only a few variables are stored |

Since each message is scanned exactly once and messages are short, the solution easily fits within any reasonable contest limits.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())

    out = []

    for _ in range(n):
        s = input().rstrip("\n")

        run = 0
        battle = False

        for ch in s:
            if ch.lower() == 'a':
                run += 1
                if run >= 3:
                    battle = True
                    break
            else:
                run = 0

        out.append("Love is war!" if battle else "Just friends <3")

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return result

# sample-style cases
assert run(
"""5
How are you doing Kaguya?
THIS MEANS WAAAAAARRRRRRRRRR
oops sorry wrong person
LlLmmAAaOoo that's soooo funnnyyy
what is a aardvark
"""
) == (
"""Just friends <3
Love is war!
Just friends <3
Love is war!
Just friends <3"""
)

# minimum size
assert run("1\na\n") == "Just friends <3"

# exactly three consecutive letters
assert run("1\naaa\n") == "Love is war!"

# mixed case
assert run("1\nAaA\n") == "Love is war!"

# separated runs
assert run("1\naa baa aa\n") == "Just friends <3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `Just friends <3` | Minimum-size message |
| `aaa` | `Love is war!` | Exact threshold of 3 |
| `AaA` | `Love is war!` | Case-insensitive matching |
| `aa baa aa` | `Just friends <3` | Runs separated by non-`a` characters |

## Edge Cases

Consider the message:

```
AaA
```

The algorithm converts each character to lowercase while scanning.

The values of `run` become:

```
1 -> 2 -> 3
```

As soon as `run` reaches 3, the algorithm outputs:

```
Love is war!
```

This correctly handles mixed capitalization.

Now consider:

```
aabaa
```

The scan proceeds as:

```
a -> run = 1
a -> run = 2
b -> run = 0
a -> run = 1
a -> run = 2
```

The counter never reaches 3, so the result is:

```
Just friends <3
```

This confirms that only consecutive occurrences matter.

Finally, consider:

```
aaaa
```

The counter evolves as:

```
1 -> 2 -> 3
```

The algorithm immediately recognizes a battle and stops scanning. Longer runs are automatically handled because any run of length 4, 5, or more necessarily passes through length 3 first.
