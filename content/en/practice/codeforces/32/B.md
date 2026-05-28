---
title: "CF 32B - Borze"
description: "We are given a string written in the Borze encoding system. Every digit of a ternary number is represented by one of three patterns:"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "expression-parsing", "implementation"]
categories: ["algorithms"]
codeforces_contest: 32
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 32 (Div. 2, Codeforces format)"
rating: 800
weight: 32
solve_time_s: 77
verified: true
draft: false
---
[CF 32B - Borze](https://codeforces.com/problemset/problem/32/B)

**Rating:** 800  
**Tags:** expression parsing, implementation  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string written in the Borze encoding system. Every digit of a ternary number is represented by one of three patterns:

- `"."` represents `0`
- `"-."` represents `1`
- `"--"` represents `2`

The task is to decode the entire string and print the resulting ternary number.

The key detail is that the encoding is prefix-safe. A single dot always stands alone as `0`, while a dash must always be paired with the next character. That means whenever we encounter `'-'`, we immediately know the current digit uses two characters.

The input length is at most 200 characters, which is tiny. Even a quadratic solution would fit comfortably within the time limit, since at worst it would process about 40,000 character operations. Still, the structure of the encoding naturally leads to a simple linear scan, so there is no reason to do extra work.

The main source of mistakes is incorrect pointer movement while parsing the string.

Consider the input:

```
--.
```

The correct decoding is:

```
20
```

A careless implementation might read the first `'-'` alone and fail to combine it with the next character. The encoding rules require every dash to consume two characters.

Another easy mistake happens when advancing through the string after decoding a two-character token.

For example:

```
-.--
```

Correct output:

```
12
```

If we decode `"-."` as `1` but only move forward by one position instead of two, the second character `'.'` gets processed again and produces the wrong result.

A final edge case is a string made entirely of dots:

```
...
```

Correct output:

```
000
```

Leading zeroes must be preserved exactly as decoded. Converting the result into an integer would incorrectly collapse it into a single `0`.

## Approaches

The most direct brute-force idea is to repeatedly try matching the current prefix against the three valid Borze symbols. At each position, we check whether the substring starts with `"."`, `"-."`, or `"--"`, append the corresponding digit, and continue.

This works because the encoding rules are unambiguous. No valid symbol can be confused with another once we inspect the current character and, when necessary, the next one.

Even if implemented inefficiently with substring creation at every step, the input is so small that the solution still passes comfortably. With length at most 200, repeatedly slicing strings would still stay well under a few tens of thousands of operations.

The observation that simplifies the problem further is that there are really only two situations:

- If the current character is `'.'`, the answer digit is definitely `0`.
- If the current character is `'-'`, we only need to inspect the next character:

- `"-."` means `1`
- `"--"` means `2`

That lets us process the string in one left-to-right scan using an index pointer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the Borze string.
2. Create an empty result string and initialize an index `i = 0`.
3. While `i` is inside the string:

1. If `s[i]` is `'.'`, append `'0'` to the answer and move `i` forward by 1.
2. Otherwise the current character is `'-'`, so the digit must use two characters.

- If `s[i + 1]` is `'.'`, append `'1'`.
- Otherwise append `'2'`.

Move `i` forward by 2.
4. Print the constructed answer string.

### Why it works

The encoding rules partition the input into non-overlapping valid tokens.

A dot always forms the token `"."`, and a dash always begins either `"-."` or `"--"`. Because of this, the correct token at position `i` is uniquely determined by the current character and possibly the next one.

The algorithm always consumes exactly the characters belonging to the current digit, never skips characters, and never processes a character twice. After each step, every processed prefix has already been decoded correctly. When the scan finishes, the entire string has been decoded.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

ans = []
i = 0

while i < len(s):
    if s[i] == '.':
        ans.append('0')
        i += 1
    else:
        if s[i + 1] == '.':
            ans.append('1')
        else:
            ans.append('2')
        i += 2

print(''.join(ans))
```

The solution keeps a pointer `i` representing the current unread position in the Borze string.

When the current character is `'.'`, the mapping is immediate. We append `'0'` and move one step forward because this token uses exactly one character.

When the current character is `'-'`, we must inspect the next character to distinguish between `"-."` and `"--"`. Both cases consume two characters, so the pointer advances by 2.

The answer is stored in a list instead of repeatedly concatenating strings. For this problem either approach would pass, but list accumulation followed by `''.join()` is the standard efficient pattern in Python.

The boundary access `s[i + 1]` is always safe because the input is guaranteed to be valid. A lone trailing `'-'` can never appear.

## Worked Examples

### Example 1

Input:

```
.-.--
```

| Step | i | Current characters | Decoded digit | Answer |
| --- | --- | --- | --- | --- |
| 1 | 0 | `.` | `0` | `0` |
| 2 | 1 | `-.` | `1` | `01` |
| 3 | 3 | `--` | `2` | `012` |

Final output:

```
012
```

This trace shows how the algorithm switches between one-character and two-character tokens without ambiguity.

### Example 2

Input:

```
--..-.
```

| Step | i | Current characters | Decoded digit | Answer |
| --- | --- | --- | --- | --- |
| 1 | 0 | `--` | `2` | `2` |
| 2 | 2 | `.` | `0` | `20` |
| 3 | 3 | `.` | `0` | `200` |
| 4 | 4 | `-.` | `1` | `2001` |

Final output:

```
2001
```

This example demonstrates consecutive single-character tokens after a two-character token. The pointer movement stays correct because each branch advances by exactly the token length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once |
| Space | O(n) | The decoded answer is stored separately |

With a maximum input length of only 200 characters, the solution easily fits within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    s = input().strip()

    ans = []
    i = 0

    while i < len(s):
        if s[i] == '.':
            ans.append('0')
            i += 1
        else:
            if s[i + 1] == '.':
                ans.append('1')
            else:
                ans.append('2')
            i += 2

    print(''.join(ans))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    return sys.stdout.getvalue().strip()

# provided sample
assert run(".-.--\n") == "012", "sample 1"

# minimum size input
assert run(".\n") == "0", "single dot"

# only two-character tokens
assert run("------\n") == "222", "all twos"

# alternating token sizes
assert run(".--.-.\n") == "021", "mixed parsing"

# leading zeroes preserved
assert run("...\n") == "000", "leading zeroes"

# boundary condition with final two-character token
assert run(".--\n") == "02", "ending with double dash"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `.` | `0` | Minimum valid input |
| `------` | `222` | Consecutive two-character tokens |
| `.--.-.` | `021` | Mixed token lengths |
| `...` | `000` | Leading zero preservation |
| `.--` | `02` | Correct handling of final token |

## Edge Cases

Consider the input:

```
--.
```

The algorithm starts at index `0` and sees `'-'`. It checks the next character and finds another `'-'`, so it appends `2` and advances by 2 positions. Now `i = 2`, where the remaining character is `'.'`, producing `0`.

The final answer is:

```
20
```

This confirms that two-character tokens are consumed together and never partially processed.

Now consider:

```
-.--
```

At `i = 0`, the substring `"-."` becomes `1`, and the pointer jumps directly to `i = 2`. The remaining substring `"--"` becomes `2`.

The output is:

```
12
```

If the pointer advanced by only one position after decoding `"-."`, the second character would be parsed again and corrupt the result.

Finally, consider:

```
...
```

Each dot independently maps to `0`, producing:

```
000
```

The algorithm stores the result as a string, so leading zeroes remain intact. Converting through integers would incorrectly lose information.
