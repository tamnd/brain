---
title: "CF 281A - Word Capitalization"
description: "We are given a single English word and need to modify it so that only the first character becomes uppercase. Every other character must stay exactly as it originally appeared. The input contains just one non-empty string."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 281
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 172 (Div. 2)"
rating: 800
weight: 281
solve_time_s: 75
verified: true
draft: false
---

[CF 281A - Word Capitalization](https://codeforces.com/problemset/problem/281/A)

**Rating:** 800  
**Tags:** implementation, strings  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single English word and need to modify it so that only the first character becomes uppercase. Every other character must stay exactly as it originally appeared.

The input contains just one non-empty string. The string may already start with an uppercase letter, or it may start with a lowercase letter. Characters after the first one are not supposed to change, even if they are uppercase or lowercase in unusual combinations.

The maximum length is only 1000 characters, which is extremely small. Even an algorithm that scans the whole string several times would easily fit within the time limit. A linear solution is more than enough.

The tricky part is not performance, it is preserving the rest of the string unchanged. A careless implementation might accidentally convert the entire word to lowercase or uppercase.

Consider this example:

Input:

```
ApPLe
```

Correct output:

```
ApPLe
```

If someone uses a function that capitalizes the string by forcing all remaining letters to lowercase, the result becomes:

```
Apple
```

That is incorrect because the original uppercase `P` letters must remain uppercase.

Another edge case is a single-character word.

Input:

```
z
```

Correct output:

```
Z
```

The algorithm must still work even though there is no remaining substring after the first character.

One more important case is when the first character is already uppercase.

Input:

```
Codeforces
```

Correct output:

```
Codeforces
```

The program should leave the string unchanged in this situation.

## Approaches

A brute-force approach would rebuild the entire string character by character. We could iterate through every index, uppercase the first character manually, and append all remaining characters unchanged.

This works because the problem only asks for a very small transformation on the string. Since the maximum length is 1000, even repeatedly concatenating characters would still run comfortably within limits.

The weakness of a naive implementation is not speed, but correctness. Many programmers instinctively use built-in capitalization helpers such as Python's `capitalize()`. That method changes the first character to uppercase, but it also converts all remaining letters to lowercase. The problem explicitly forbids modifying the remaining characters.

The key observation is that we only need to transform one position in the string, the first character. Every other character should be copied exactly as-is. Once we recognize that, the solution becomes straightforward:

1. Take the first character.
2. Convert it to uppercase.
3. Append the untouched remainder of the string.

This directly matches the definition of the required transformation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(n) | Accepted |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input string.
2. Extract the first character of the string.
3. Convert that first character to uppercase.

This is the only modification required by the problem.
4. Take the substring starting from index 1 until the end.

These characters must remain unchanged.
5. Concatenate the uppercase first character with the untouched suffix.
6. Print the resulting string.

### Why it works

The algorithm changes exactly one character, the first one. Every character after index 0 is copied directly from the original string without modification. Since the problem definition only requires capitalizing the first letter while preserving all remaining letters, the constructed string is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

result = s[0].upper() + s[1:]

print(result)
```

The program begins by reading the word from standard input. The `strip()` call removes the trailing newline character produced by input reading.

The expression `s[0].upper()` converts only the first character into uppercase form. If the character is already uppercase, it remains unchanged.

The slice `s[1:]` returns every character after the first one exactly as it originally appeared. This is the critical detail that avoids the common mistake of modifying the entire word.

Finally, the two parts are concatenated and printed.

The implementation safely handles single-character strings because `s[1:]` becomes an empty string in that case.

## Worked Examples

### Example 1

Input:

```
ApPLe
```

| Step | Value |
| --- | --- |
| Original string | `ApPLe` |
| First character | `A` |
| Uppercase first character | `A` |
| Remaining substring | `pPLe` |
| Final result | `ApPLe` |

This example shows that the algorithm does not alter the remaining letters. The uppercase `P` characters stay uppercase.

### Example 2

Input:

```
codeforces
```

| Step | Value |
| --- | --- |
| Original string | `codeforces` |
| First character | `c` |
| Uppercase first character | `C` |
| Remaining substring | `odeforces` |
| Final result | `Codeforces` |

This trace demonstrates the main transformation. Only the first character changes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Constructing the final string processes all characters once |
| Space | O(n) | A new output string is created |

The input size is at most 1000 characters, so linear complexity is trivial for the given limits. The solution easily fits within both the time and memory constraints.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    import sys
    input = sys.stdin.readline

    s = input().strip()
    print(s[0].upper() + s[1:])

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
assert run("ApPLe\n") == "ApPLe\n", "sample 1"

# custom cases
assert run("z\n") == "Z\n", "single lowercase character"
assert run("Z\n") == "Z\n", "single uppercase character"
assert run("codeforces\n") == "Codeforces\n", "normal lowercase word"
assert run("JAVA\n") == "JAVA\n", "already uppercase"
assert run("hELLO\n") == "HELLO\n", "preserve remaining characters"

# maximum-size style case
long_word = "a" * 1000
expected = "A" + "a" * 999 + "\n"
assert run(long_word + "\n") == expected, "maximum length input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `z` | `Z` | Single-character lowercase word |
| `Z` | `Z` | Single-character uppercase word |
| `codeforces` | `Codeforces` | Standard capitalization |
| `JAVA` | `JAVA` | Already capitalized input |
| `hELLO` | `HELLO` | Remaining characters stay unchanged |
| 1000 `'a'` characters | First character uppercase only | Maximum input size |

## Edge Cases

A single-character word must still work correctly.

Input:

```
z
```

The algorithm takes `z`, converts it to `Z`, and appends the empty suffix `""`. The final answer becomes:

```
Z
```

There is no out-of-bounds issue because Python slicing safely handles empty ranges.

Another subtle case happens when the remaining letters contain uppercase characters that must stay unchanged.

Input:

```
ApPLe
```

The algorithm converts the first character `A` to uppercase, which changes nothing, then appends the untouched substring `pPLe`. The final result is:

```
ApPLe
```

This confirms that the solution does not accidentally lowercase the rest of the word.

Finally, consider a word whose first character is already uppercase.

Input:

```
Codeforces
```

The uppercase conversion leaves `C` unchanged. The suffix `odeforces` is appended directly, producing:

```
Codeforces
```

The algorithm behaves correctly even when no visible transformation is needed.
