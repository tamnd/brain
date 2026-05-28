---
title: "CF 81A - Plug-in"
description: "We are given a lowercase string that may contain accidental repeated keystrokes. Whenever two equal characters become adjacent, both characters must be deleted. After removing one pair, new adjacent equal pairs may appear, and those must also be removed."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 81
codeforces_index: "A"
codeforces_contest_name: "Yandex.Algorithm Open 2011: Qualification 1"
rating: 1400
weight: 81
solve_time_s: 96
verified: true
draft: false
---

[CF 81A - Plug-in](https://codeforces.com/problemset/problem/81/A)

**Rating:** 1400  
**Tags:** implementation  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a lowercase string that may contain accidental repeated keystrokes. Whenever two equal characters become adjacent, both characters must be deleted. After removing one pair, new adjacent equal pairs may appear, and those must also be removed.

The process continues until no adjacent equal characters remain. The final remaining string must be printed.

For example, consider the string `abccba`.

First, the pair `cc` disappears:

```
abccba -> abba
```

Now a new pair `bb` becomes adjacent:

```
abba -> aa
```

Finally:

```
aa -> ""
```

The important detail is that removals can trigger more removals later. A solution that only deletes the pairs visible in the original string would be wrong.

The input length can reach `2 * 10^5`, which immediately rules out repeatedly rebuilding the string from scratch. Any algorithm that scans the whole string many times can become quadratic. With 200,000 characters, an `O(n^2)` approach may require tens of billions of operations, far beyond the time limit.

A linear or near-linear solution is needed.

Several edge cases are easy to mishandle.

Consider:

```
aaaa
```

A careless implementation might remove only the first pair and stop:

```
aaaa -> aa
```

But the remaining `aa` must also disappear, so the correct result is the empty string.

Another tricky case is:

```
abccba
```

The equal characters that finally cancel are not adjacent in the original string. They only become adjacent after earlier deletions. Any approach that processes pairs independently without accounting for chain reactions will fail here.

A third important scenario is alternating characters:

```
abababab
```

No adjacent equal pair ever exists, so the output must remain unchanged. The algorithm must avoid deleting non-adjacent equal letters.

Finally, boundary behavior matters. For input:

```
aaab
```

The first two `a` characters disappear:

```
aaab -> ab
```

The remaining single `a` must stay. Incorrect index movement after deletion often causes bugs here.

## Approaches

The most direct solution is to repeatedly scan the string looking for adjacent equal characters. Whenever one is found, remove that pair and restart the scan.

For example:

```
abbaca
```

becomes:

```
aaca
```

then:

```
ca
```

This approach is correct because it exactly simulates the problem statement.

The problem is efficiency. Removing characters from the middle of a string is expensive, and restarting scans repeatedly makes things worse. In the worst case, each deletion may require shifting almost the entire string.

Suppose the input length is `n`. We may perform `O(n)` deletions, and each deletion may cost `O(n)` time due to copying or rebuilding strings. The total complexity becomes `O(n^2)`.

With `n = 200000`, quadratic behavior is far too slow.

The key observation is that only the most recent surviving character matters when processing a new character.

Imagine building the final string from left to right.

If the current character is different from the last surviving character, it must remain for now.

If it matches the last surviving character, those two characters immediately cancel each other.

This behavior is exactly what a stack provides.

We maintain a stack containing the characters that currently survive after processing the prefix of the string.

When reading a new character:

If it matches the stack top, we pop the top because the pair disappears.

Otherwise, we push the character.

Every character is pushed at most once and popped at most once, giving linear complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal Stack Solution | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create an empty stack.
2. Process the string from left to right, one character at a time.
3. For the current character, check whether the stack is non-empty and whether its top element equals the current character.
4. If they are equal, remove the top element from the stack.

This models deleting a consecutive equal pair.
5. Otherwise, push the current character onto the stack.

This character currently survives and may interact with future characters.
6. After processing all characters, the stack contains exactly the remaining string.
7. Join the stack characters together and print the result.

### Why it works

The stack always stores the fully processed result for the prefix seen so far.

Suppose we have already processed the first `i` characters correctly. When character `i + 1` arrives, only one new adjacent pair can possibly form, between this character and the current last surviving character.

If they are equal, both disappear, so popping is correct.

If they differ, no deletion involving the new character is possible yet, so pushing is correct.

Because every step preserves the correct processed form of the prefix, the final stack is exactly the fully reduced string.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()

    stack = []

    for ch in s:
        if stack and stack[-1] == ch:
            stack.pop()
        else:
            stack.append(ch)

    print("".join(stack))

solve()
```

The solution follows the stack idea directly.

The `stack` list stores the surviving characters after processing the current prefix.

For every character `ch`, we compare it with the stack top.

If both are equal, they form an adjacent equal pair in the current reduced string, so we remove the top with `pop()`.

Otherwise, the character survives for now, so we append it.

At the end, the stack already contains the final answer in order, so `"".join(stack)` constructs the resulting string efficiently.

Using a Python list as a stack is important. Appending and popping from the end are both `O(1)` operations.

A common mistake is repeatedly concatenating strings during processing. Since Python strings are immutable, repeated concatenation creates new strings repeatedly and can degrade to quadratic complexity.

Another subtle detail is using `strip()` when reading input. The input line ends with a newline character, and we do not want that newline processed as part of the string.

## Worked Examples

### Example 1

Input:

```
hhoowaaaareyyoouu
```

| Current Character | Stack Before | Action | Stack After |
| --- | --- | --- | --- |
| h | "" | push | h |
| h | h | pop | "" |
| o | "" | push | o |
| o | o | pop | "" |
| w | "" | push | w |
| a | w | push | wa |
| a | wa | pop | w |
| a | w | push | wa |
| a | wa | pop | w |
| r | w | push | wr |
| e | wr | push | wre |
| y | wre | push | wrey |
| y | wrey | pop | wre |
| o | wre | push | wreo |
| o | wreo | pop | wre |
| u | wre | push | wreu |
| u | wreu | pop | wre |

Final output:

```
wre
```

This example demonstrates repeated chain reactions. Several pairs disappear immediately, and later characters continue interacting with the updated stack state.

### Example 2

Input:

```
abccba
```

| Current Character | Stack Before | Action | Stack After |
| --- | --- | --- | --- |
| a | "" | push | a |
| b | a | push | ab |
| c | ab | push | abc |
| c | abc | pop | ab |
| b | ab | pop | a |
| a | a | pop | "" |

Final output:

```
""
```

This trace shows why chain reactions matter. The first deletion creates a new adjacent pair, which creates another one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is pushed once and popped at most once |
| Space | O(n) | The stack may store the entire string in the worst case |

With at most 200,000 characters, linear complexity easily fits within the limits. The stack operations are constant time, so the implementation runs efficiently even on the largest inputs.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    s = input().strip()

    stack = []

    for ch in s:
        if stack and stack[-1] == ch:
            stack.pop()
        else:
            stack.append(ch)

    print("".join(stack))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("hhoowaaaareyyoouu\n") == "wre", "sample 1"

# minimum size
assert run("a\n") == "a", "single character"

# all equal
assert run("aaaaaa\n") == "", "all characters removed"

# chain reactions
assert run("abccba\n") == "", "multiple cascading removals"

# no removals
assert run("abababab\n") == "abababab", "alternating characters"

# boundary behavior
assert run("aaab\n") == "ab", "remaining character after deletion"

# large-style pattern
assert run("aabbccddeeff\n") == "", "repeated adjacent pairs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `a` | Minimum input size |
| `aaaaaa` | `""` | Repeated cascading deletions |
| `abccba` | `""` | Chain reactions after intermediate removals |
| `abababab` | `abababab` | No deletions occur |
| `aaab` | `ab` | Correct handling after partial deletion |
| `aabbccddeeff` | `""` | Multiple independent adjacent pairs |

## Edge Cases

Consider the input:

```
aaaa
```

Execution:

```
stack = []
read 'a' -> push -> [a]
read 'a' -> pop  -> []
read 'a' -> push -> [a]
read 'a' -> pop  -> []
```

Final output:

```
""
```

This confirms that the algorithm naturally handles repeated cascading deletions without rescanning the string.

Now consider:

```
abccba
```

Execution:

```
[a]
[a, b]
[a, b, c]
[a, b]
[a]
[]
```

The important detail is that the second `b` cancels only after the `cc` pair disappears. The stack automatically captures this new adjacency.

Finally, consider:

```
aaab
```

Execution:

```
[a]
[]
[a]
[a, b]
```

Final output:

```
ab
```

This verifies correct handling when an odd number of identical characters appears consecutively. Only complete pairs disappear, and the remaining unmatched character survives.
