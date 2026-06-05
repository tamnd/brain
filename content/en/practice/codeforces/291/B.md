---
title: "CF 291B - Command Line Arguments"
description: "We are given a single command-line string written in the fictional Pindows operating system. A command line consists of lexemes, which are the tokens passed to a program. There are two ways a lexeme can appear. A normal lexeme is a maximal sequence of non-space characters."
date: "2026-06-05T16:51:38+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 291
codeforces_index: "B"
codeforces_contest_name: "Croc Champ 2013 - Qualification Round"
rating: 1300
weight: 291
solve_time_s: 137
verified: false
draft: false
---

[CF 291B - Command Line Arguments](https://codeforces.com/problemset/problem/291/B)

**Rating:** 1300  
**Tags:** *special, implementation, strings  
**Solve time:** 2m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a single command-line string written in the fictional Pindows operating system. A command line consists of lexemes, which are the tokens passed to a program.

There are two ways a lexeme can appear.

A normal lexeme is a maximal sequence of non-space characters. For example, in:

```
run.exe one two
```

the lexemes are `run.exe`, `one`, and `two`.

A quoted lexeme begins with `"` and ends with the matching `"`. Everything between those quotes belongs to one lexeme, including spaces. The contents may even be empty. For example:

```
"a b" ""
```

contains two lexemes: `a b` and the empty string.

The input is guaranteed to be a valid command line. Quotes are never ambiguous, quoted blocks are properly closed, and every lexeme is separated from neighboring lexemes by spaces or by the ends of the string.

Our task is simply to parse the command line and print every lexeme on its own line, surrounded by `<` and `>`.

The string length is at most $10^5$. This immediately rules out any approach that repeatedly copies large substrings or rescans parts of the input. A linear scan is the natural target because we only need to identify token boundaries once.

Several edge cases deserve attention.

Consider an empty quoted argument:

```
""
```

The correct output is:

```
<>
```

A parser that assumes every token contains at least one character would accidentally discard this argument.

Consider a quoted argument containing spaces:

```
"a b c"
```

The correct output is:

```
<a b c>
```

Splitting the input by spaces would incorrectly produce three separate pieces.

Consider a quoted argument consisting of a single space:

```
" "
```

The correct output is:

```
< >
```

This is different from an empty argument, so we must preserve every character inside the quotes exactly.

Finally, consider adjacent punctuation:

```
run.exe one, two!
```

The correct output is:

```
<run.exe>
<one,>
<two!>
```

Punctuation is part of the lexeme. Only spaces and quotes have special meaning.

## Approaches

The most direct idea is to process the string character by character and build the current lexeme. Whenever we encounter a space outside quotes, we finish the current lexeme. Whenever we encounter a quote, we find the matching closing quote and treat everything between them as one token.

A brute-force implementation might repeatedly search forward for matching quotes and repeatedly create new substrings. Since each search may traverse a large part of the string, the worst-case complexity can degrade toward $O(n^2)$. With $n = 10^5$, that becomes too expensive.

The structure of the input gives us a much better option. Every character belongs to exactly one of three categories:

1. A separator space outside quotes.
2. A character inside a quoted lexeme.
3. A character of an unquoted lexeme.

Once a character has been processed, we never need to look at it again. This suggests a single left-to-right scan.

The key observation is that quoted lexemes always begin with `"`, and the statement guarantees the command line is valid. As soon as we see an opening quote, we can keep advancing until the corresponding closing quote. The contents between them form one complete lexeme. For unquoted lexemes, we advance until the next space.

Each character is visited a constant number of times, giving a linear solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the entire input line.
2. Maintain an index `i` pointing to the current position.
3. If `s[i]` is a space, advance `i`.

Spaces outside lexemes are only separators, so they do not belong to any token.
4. If `s[i]` is a double quote, start parsing a quoted lexeme.

Advance past the opening quote, remember the starting position, and continue until the matching closing quote. The substring between those quotes is one lexeme.
5. Store that lexeme and advance past the closing quote.
6. Otherwise, start parsing an unquoted lexeme.

Continue moving forward until reaching a space or the end of the string. The characters traversed form one lexeme.
7. Store the lexeme.
8. Repeat until the entire string has been processed.
9. Print each stored lexeme surrounded by `<` and `>`.

### Why it works

At every position, the parser is either outside a lexeme or inside exactly one lexeme. The input guarantees that quotes are properly matched and that lexemes are separated by spaces or string boundaries.

When a quote is encountered, every character up to the matching quote belongs to the same lexeme by definition. When a non-quote, non-space character is encountered, the lexeme extends until the next separator space. These are exactly the rules used by the command-line specification.

Since every lexeme is extracted according to its defining boundary conditions, and every character belongs to exactly one processed region, the algorithm outputs precisely the lexemes represented by the command line.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().rstrip('\n')

    n = len(s)
    i = 0
    tokens = []

    while i < n:
        if s[i] == ' ':
            i += 1
            continue

        if s[i] == '"':
            i += 1
            start = i

            while i < n and s[i] != '"':
                i += 1

            tokens.append(s[start:i])
            i += 1  # skip closing quote
        else:
            start = i

            while i < n and s[i] != ' ':
                i += 1

            tokens.append(s[start:i])

    sys.stdout.write('\n'.join(f'<{token}>' for token in tokens))

if __name__ == "__main__":
    solve()
```

The implementation follows the parsing logic directly.

The outer loop always points to the first unprocessed character. Spaces are skipped immediately because they never belong to a lexeme.

When a quote is encountered, the code records the position immediately after the opening quote and advances until the closing quote. The slice `s[start:i]` contains exactly the quoted contents. This naturally handles empty strings because if the quotes are adjacent, `start == i` and the slice is empty.

For ordinary lexemes, the parser advances until the next space. Since quotes cannot appear inside an unquoted lexeme in a valid input, no additional checks are required.

A common mistake is using `split()` on the input. That destroys information about quoted sections and cannot represent empty arguments. Another subtle point is preserving spaces inside quoted lexemes. The substring extraction does this automatically because only the outer quote characters are removed.

## Worked Examples

### Example 1

Input:

```
"RUn.exe O" "" "   2ne, " two! . " "
```

| Step | Position Type | Extracted Lexeme |
| --- | --- | --- |
| 1 | Quoted | `RUn.exe O` |
| 2 | Quoted | `` |
| 3 | Quoted | `  2ne,` |
| 4 | Unquoted | `two!` |
| 5 | Unquoted | `.` |
| 6 | Quoted | ` ` |

Output:

```
<RUn.exe O>
<>
<   2ne, >
<two!>
<.>
< >
```

This example demonstrates all special cases simultaneously: spaces inside quotes, an empty argument, normal arguments, and a quoted argument consisting of one space.

### Example 2

Input:

```
run.exe one two
```

| Step | Position Type | Extracted Lexeme |
| --- | --- | --- |
| 1 | Unquoted | `run.exe` |
| 2 | Unquoted | `one` |
| 3 | Unquoted | `two` |

Output:

```
<run.exe>
<one>
<two>
```

This trace shows the simpler case where every lexeme is unquoted and spaces act purely as separators.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is examined at most a constant number of times |
| Space | O(n) | Stored lexemes together contain at most n characters |

With an input length of at most $10^5$, a linear scan easily fits within the time limit. The memory usage is also linear in the input size and well within the available limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    s = inp.rstrip('\n')

    n = len(s)
    i = 0
    tokens = []

    while i < n:
        if s[i] == ' ':
            i += 1
            continue

        if s[i] == '"':
            i += 1
            start = i

            while i < n and s[i] != '"':
                i += 1

            tokens.append(s[start:i])
            i += 1
        else:
            start = i

            while i < n and s[i] != ' ':
                i += 1

            tokens.append(s[start:i])

    return '\n'.join(f'<{x}>' for x in tokens)

# provided sample
assert run('"RUn.exe O" "" "   2ne, " two! . " "') == (
    "<RUn.exe O>\n"
    "<>\n"
    "<   2ne, >\n"
    "<two!>\n"
    "<.>\n"
    "< >"
), "sample 1"

# custom cases
assert run('""') == "<>", "empty quoted argument"

assert run('"a b c"') == "<a b c>", "spaces inside quoted token"

assert run('abc') == "<abc>", "single unquoted token"

assert run('one two three') == (
    "<one>\n<two>\n<three>"
), "multiple ordinary tokens"

assert run('" " "."') == (
    "< >\n<.>"
), "space token and punctuation token"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `""` | `<>` | Empty quoted lexeme |
| `"a b c"` | `<a b c>` | Spaces preserved inside quotes |
| `abc` | `<abc>` | Smallest ordinary command |
| `one two three` | Three separate lexemes | Standard separator handling |
| `" " "."` | `< >`, `<.>` | Distinguishes space from empty string |

## Edge Cases

Consider the input:

```
""
```

The parser sees an opening quote, advances to the next quote immediately, and extracts the substring between them. That substring has length zero, so the stored lexeme is the empty string. The output becomes:

```
<>
```

No special-case code is required.

Consider:

```
" "
```

After entering quoted mode, the parser collects the single space between the quotes. The extracted substring is `" "` rather than `""`, producing:

```
< >
```

This confirms that spaces inside quotes are data, not separators.

Consider:

```
"a b" c
```

The first lexeme is parsed entirely inside quotes, yielding `a b`. After the closing quote, the parser skips the separating space and parses the unquoted lexeme `c`. The output is:

```
<a b>
<c>
```

The internal space remains part of the first argument because quoted mode ignores separator semantics until the matching closing quote is reached.

Consider:

```
run.exe one, two!
```

The parser never treats punctuation specially. It only stops unquoted parsing when it reaches a space. The extracted lexemes are:

```
<run.exe>
<one,>
<two!>
```

This verifies that punctuation belongs to the token exactly as it appears in the input.
