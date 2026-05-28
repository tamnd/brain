---
title: "CF 130G - CAPS LOCK ON"
description: "We are given a single string containing printable ASCII characters. Some characters may be lowercase English letters, some may already be uppercase letters, and others may be symbols or digits."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 130
codeforces_index: "G"
codeforces_contest_name: "Unknown Language Round 4"
rating: 1700
weight: 130
solve_time_s: 88
verified: true
draft: false
---

[CF 130G - CAPS LOCK ON](https://codeforces.com/problemset/problem/130/G)

**Rating:** 1700  
**Tags:** *special  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single string containing printable ASCII characters. Some characters may be lowercase English letters, some may already be uppercase letters, and others may be symbols or digits. The task is to transform only the lowercase letters into their uppercase versions while leaving every other character unchanged.

For example, the string `cOdEfOrCeS` becomes `CODEFORCES`. The lowercase letters `c`, `d`, `f`, `r`, and `e` are converted, while the characters already in uppercase stay exactly the same.

The input length is at most 100 characters, which is extremely small. Even an inefficient solution would comfortably fit within the limits. A linear scan over the string is more than enough, since processing 100 characters takes essentially no time. Memory usage is also trivial because we only need to store the resulting string.

The tricky part is not performance but correctness. A careless implementation can accidentally modify characters that are not lowercase letters.

Consider this input:

```
abc123!?
```

The correct output is:

```
ABC123!?
```

Digits and punctuation must stay unchanged. An implementation that blindly shifts every character code by a fixed amount would corrupt non-letter characters.

Another edge case is a string that is already uppercase:

```
HELLO
```

The output must remain:

```
HELLO
```

A buggy implementation that assumes every letter is lowercase could incorrectly transform uppercase characters into unrelated ASCII symbols.

One more important case is mixed symbols:

```
a-z_
```

The correct output is:

```
A-Z_
```

Only the lowercase letters `a` and `z` should change. The dash and underscore must remain untouched.

## Approaches

The most direct brute-force approach is to examine every character one by one. For each character, we check whether it is a lowercase English letter. If it is, we replace it with its uppercase counterpart. Otherwise, we copy it unchanged into the result.

This already works efficiently because the string length is at most 100. The worst case performs only 100 character checks and transformations, which is negligible.

One way to implement this brute-force method manually is through ASCII arithmetic. Lowercase letters `'a'` through `'z'` are exactly 32 positions after uppercase letters `'A'` through `'Z'` in the ASCII table. So if a character lies in the lowercase range, we can subtract 32 from its ASCII value.

The language already provides a cleaner solution through the built-in `upper()` method. This method internally performs the same conversion logic and keeps non-letter characters unchanged. Since the problem only asks for uppercase conversion, using the built-in method gives the simplest and safest implementation.

The brute-force idea and the optimal solution are effectively the same here because the input is tiny and every valid approach scans the string once. The main improvement is not asymptotic speed but code simplicity and reliability.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Manual character conversion | O(n) | O(n) | Accepted |
| Using built-in `upper()` | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input string from standard input.
2. Convert the string to uppercase using Python's `upper()` method.

This method transforms every lowercase English letter into its uppercase version while leaving digits, punctuation, and already-uppercase letters unchanged.
3. Print the transformed string.

### Why it works

The algorithm processes every character independently. For each character, the uppercase conversion follows standard ASCII letter mapping rules. Lowercase letters are converted to uppercase, while all other characters remain identical. Since every position is handled correctly and independently, the final string is exactly the required uppercase transformation of the input.

## Python Solution

```python
import sys
input = sys.stdin.readline

# solution
s = input().strip()
print(s.upper())
```

The program starts by reading the string from input. Since the input consists of a single line, `strip()` safely removes the trailing newline character added by standard input.

The call to `upper()` performs the entire conversion. Python automatically converts lowercase English letters to uppercase and leaves all other printable ASCII characters unchanged. This behavior matches the problem requirements exactly.

The implementation avoids manual ASCII manipulation, which reduces the chance of mistakes involving punctuation or already-uppercase letters.

## Worked Examples

### Example 1

Input:

```
cOdEfOrCeS
```

| Position | Character | After `upper()` |
| --- | --- | --- |
| 0 | c | C |
| 1 | O | O |
| 2 | d | D |
| 3 | E | E |
| 4 | f | F |
| 5 | O | O |
| 6 | r | R |
| 7 | C | C |
| 8 | e | E |
| 9 | S | S |

Final output:

```
CODEFORCES
```

This example shows that lowercase and uppercase letters can appear in any order. The algorithm treats each character independently and converts only lowercase ones.

### Example 2

Input:

```
a-z_123
```

| Position | Character | After `upper()` |
| --- | --- | --- |
| 0 | a | A |
| 1 | - | - |
| 2 | z | Z |
| 3 | _ | _ |
| 4 | 1 | 1 |
| 5 | 2 | 2 |
| 6 | 3 | 3 |

Final output:

```
A-Z_123
```

This trace confirms that symbols and digits remain unchanged. Only lowercase letters are modified.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The string is scanned once |
| Space | O(n) | A new uppercase string is created |

Here, `n` is the length of the string. Since the maximum length is only 100, the solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    s = input().strip()
    print(s.upper())

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

# provided samples
assert run("cOdEfOrCeS\n") == "CODEFORCES\n", "sample 1"

# custom cases
assert run("a\n") == "A\n", "single lowercase letter"
assert run("Z\n") == "Z\n", "single uppercase letter"
assert run("123!@#\n") == "123!@#\n", "symbols and digits unchanged"
assert run("abcxyz\n") == "ABCXYZ\n", "all lowercase letters"
assert run("a-z_123\n") == "A-Z_123\n", "mixed symbols and letters"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `A` | Minimum-size lowercase input |
| `Z` | `Z` | Already-uppercase character remains unchanged |
| `123!@#` | `123!@#` | Digits and symbols are preserved |
| `abcxyz` | `ABCXYZ` | All lowercase letters convert correctly |
| `a-z_123` | `A-Z_123` | Mixed characters are handled safely |

## Edge Cases

Consider the input:

```
123!@#
```

The algorithm applies `upper()` to the entire string. Since none of the characters are lowercase letters, every character stays unchanged. The output becomes:

```
123!@#
```

This case confirms that punctuation and digits are preserved correctly.

Now consider:

```
HELLO
```

Each character is already uppercase. The conversion leaves the string untouched, producing:

```
HELLO
```

This verifies that the algorithm does not accidentally modify uppercase letters.

Finally, consider:

```
a-z_
```

The algorithm processes the characters one by one internally:

| Character | Result |
| --- | --- |
| a | A |
| - | - |
| z | Z |
| _ | _ |

The final output is:

```
A-Z_
```

This demonstrates that lowercase letters are converted correctly even when surrounded by non-letter symbols.
