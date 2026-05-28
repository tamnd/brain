---
title: "CF 81B - Sequence Formatting"
description: "We are given a messy textual representation of a sequence. The string may contain positive integers, commas, spaces, and the special token .... Spaces may appear in the wrong places or appear multiple times. The task is purely formatting."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 81
codeforces_index: "B"
codeforces_contest_name: "Yandex.Algorithm Open 2011: Qualification 1"
rating: 1700
weight: 81
solve_time_s: 103
verified: true
draft: false
---

[CF 81B - Sequence Formatting](https://codeforces.com/problemset/problem/81/B)

**Rating:** 1700  
**Tags:** implementation, strings  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a messy textual representation of a sequence. The string may contain positive integers, commas, spaces, and the special token `...`. Spaces may appear in the wrong places or appear multiple times.

The task is purely formatting. We must rewrite the string so that every token follows a precise spacing policy.

A comma must be followed by exactly one space unless it is the last character of the string. The token `...` must have exactly one space before it unless it appears at the beginning. Spaces between two numbers collapse into a single space. Every other space must disappear.

The input length is at most 255 characters, which is tiny. Even quadratic processing would pass comfortably. The real difficulty is not performance, it is correctly understanding which spaces are legal and which are not.

The most dangerous part of the problem is that spaces are not handled uniformly. A space after a comma is required, while a space before a comma is forbidden. A space before `...` is required, while a space after `...` is forbidden unless another rule introduces it. Spaces between two numbers are allowed but must collapse to one.

Several edge cases silently break naive implementations.

Consider:

```
1 ,2
```

The correct output is:

```
1, 2
```

A careless solution that only inserts missing spaces after commas might leave the illegal space before the comma unchanged.

Another tricky case is:

```
...1
```

The correct output is:

```
...1
```

There must not be a space after `...`. The rule only talks about a space before it.

Now consider:

```
1     2
```

The correct output is:

```
1 2
```

Spaces between numbers collapse to exactly one. If we globally delete all spaces and then rebuild formatting around commas, this valid separator disappears.

One more subtle case:

```
1,...,2
```

The correct output is:

```
1, ..., 2
```

The token `...` behaves differently from numbers. It needs a leading space, and the comma after it still requires a trailing space.

The safest way to solve the problem is to stop thinking about individual characters and instead think in terms of tokens.

## Approaches

A brute-force strategy would repeatedly scan the string and locally repair violations. One pass could remove duplicate spaces, another could insert missing spaces after commas, another could delete spaces before commas, and so on.

This works because every formatting rule is local. Each mistake can be corrected by inspecting only nearby characters.

The problem with this approach is not asymptotic complexity. With only 255 characters, even many scans are fast enough. The real issue is interaction between rules. One repair step can accidentally create a new violation for another rule. For example, deleting spaces aggressively can remove the required space before `...`. The implementation becomes fragile because every transformation depends on the order of previous transformations.

A much cleaner observation is that the input is already composed of well-defined tokens. Every meaningful piece is either:

```
number
comma
...
```

Spaces are never semantically important on their own. They only describe formatting relationships between neighboring tokens.

Once we tokenize the string, formatting becomes deterministic. We can rebuild the answer from scratch while deciding exactly which spaces belong between adjacent tokens.

This completely avoids complicated cleanup logic.

The reconstruction rules become simple:

If the current token is a comma, append it directly with no preceding space.

If the current token is `...`, add one leading space unless it starts the string.

If two consecutive tokens are numbers, place exactly one space between them.

If the previous token is a comma, place exactly one space before the current non-comma token.

Everything else gets no space.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force repeated string fixes | O(n²) | O(n) | Accepted but fragile |
| Tokenize and rebuild | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Scan the input string from left to right and extract tokens.

Ignore spaces completely during tokenization. Whenever we encounter digits, consume the entire number. Whenever we encounter `...`, treat all three dots as one token. Commas become standalone tokens.
2. Store all extracted tokens in order.

After this step, the original messy spacing no longer matters. We only preserve the semantic structure of the sequence.
3. Rebuild the answer token by token.

For each token, decide whether a space is needed before appending it.
4. If the token is a comma, append it immediately.

Commas never have spaces before them.
5. If the previous token was a comma, insert exactly one space before the current token.

This enforces the rule about commas.
6. If the current token is `...` and it is not the first token, insert exactly one space before it.

This enforces the special rule for suspension points.
7. If both the previous token and current token are numbers, insert exactly one space.

This handles sequences where numbers were separated only by spaces.
8. Append the current token.
9. Print the reconstructed string.

### Why it works

The algorithm separates parsing from formatting.

During tokenization, every meaningful token is preserved exactly once and every original space is discarded. This guarantees that no incorrect spacing survives into the reconstruction phase.

During rebuilding, every legal space is introduced explicitly from the formatting rules. Since each rule depends only on neighboring tokens, every boundary between tokens is handled exactly once.

The reconstruction rules are mutually exclusive and complete. Every required space is added, and every forbidden space is omitted. Because the final string is built only from these controlled decisions, the output always satisfies all formatting requirements.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_number(token):
    return token[0].isdigit()

s = input().rstrip()

tokens = []
n = len(s)
i = 0

while i < n:
    if s[i] == ' ':
        i += 1

    elif s[i].isdigit():
        j = i
        while j < n and s[j].isdigit():
            j += 1
        tokens.append(s[i:j])
        i = j

    elif s[i] == ',':
        tokens.append(',')
        i += 1

    else:
        tokens.append('...')
        i += 3

ans = []

for idx, token in enumerate(tokens):
    if idx > 0:
        prev = tokens[idx - 1]

        need_space = False

        if prev == ',':
            need_space = True
        elif token == '...':
            need_space = True
        elif is_number(prev) and is_number(token):
            need_space = True

        if need_space:
            ans.append(' ')

    ans.append(token)

print(''.join(ans))
```

The first phase extracts tokens while completely ignoring spaces. This is the key simplification. Once spaces disappear, the remaining structure becomes unambiguous.

The digit parsing loop is important because numbers may contain multiple digits. Reading only one character at a time would incorrectly split `123` into three tokens.

The `...` token must be consumed as a single unit. Advancing by three characters guarantees that we never interpret the dots individually.

The reconstruction phase only examines neighboring tokens. The variable `need_space` centralizes all spacing logic into one place, which makes it easier to verify correctness.

The order of checks matters conceptually, although the conditions themselves are mutually compatible. A comma rule overrides everything because commas never receive a leading space. The implementation handles this naturally by only deciding whether to insert a space before the current token.

One subtle point is that `...` always gets a leading space unless it is the first token. This matches the statement exactly.

## Worked Examples

### Example 1

Input:

```
1,2 ,3,...,     10
```

Tokenization produces:

| Position | Extracted token |
| --- | --- |
| 0 | 1 |
| 1 | , |
| 2 | 2 |
| 3 | , |
| 4 | 3 |
| 5 | , |
| 6 | ... |
| 7 | , |
| 8 | 10 |

Reconstruction:

| Current token | Previous token | Insert space? | Current output |
| --- | --- | --- | --- |
| 1 | none | No | 1 |
| , | 1 | No | 1, |
| 2 | , | Yes | 1, 2 |
| , | 2 | No | 1, 2, |
| 3 | , | Yes | 1, 2, 3 |
| , | 3 | No | 1, 2, 3, |
| ... | , | Yes | 1, 2, 3, ... |
| , | ... | No | 1, 2, 3, ..., |
| 10 | , | Yes | 1, 2, 3, ..., 10 |

Final output:

```
1, 2, 3, ..., 10
```

This example demonstrates that all original spaces can safely be discarded. The correct formatting emerges entirely from token relationships.

### Example 2

Input:

```
12     34...56
```

Tokenization:

| Position | Extracted token |
| --- | --- |
| 0 | 12 |
| 1 | 34 |
| 2 | ... |
| 3 | 56 |

Reconstruction:

| Current token | Previous token | Insert space? | Current output |
| --- | --- | --- | --- |
| 12 | none | No | 12 |
| 34 | 12 | Yes | 12 34 |
| ... | 34 | Yes | 12 34 ... |
| 56 | ... | No | 12 34 ...56 |

Final output:

```
12 34 ...56
```

This trace shows that spaces are only inserted where rules explicitly require them. There is no automatic space after `...`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is scanned a constant number of times |
| Space | O(n) | Tokens and output string both store at most O(n) characters |

The input size is extremely small, but the linear solution is still preferable because it keeps the logic clean and predictable. The algorithm comfortably fits within all limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    import sys
    input = sys.stdin.readline

    def is_number(token):
        return token[0].isdigit()

    s = input().rstrip()

    tokens = []
    n = len(s)
    i = 0

    while i < n:
        if s[i] == ' ':
            i += 1

        elif s[i].isdigit():
            j = i
            while j < n and s[j].isdigit():
                j += 1
            tokens.append(s[i:j])
            i = j

        elif s[i] == ',':
            tokens.append(',')
            i += 1

        else:
            tokens.append('...')
            i += 3

    ans = []

    for idx, token in enumerate(tokens):
        if idx > 0:
            prev = tokens[idx - 1]

            need_space = False

            if prev == ',':
                need_space = True
            elif token == '...':
                need_space = True
            elif is_number(prev) and is_number(token):
                need_space = True

            if need_space:
                ans.append(' ')

        ans.append(token)

    print(''.join(ans))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue().strip()

# provided sample
assert run("1,2 ,3,...,     10\n") == "1, 2, 3, ..., 10", "sample 1"

# minimum size
assert run("7\n") == "7", "single token"

# spaces between numbers
assert run("12     34\n") == "12 34", "collapse spaces"

# comma formatting
assert run("1 ,2,3\n") == "1, 2, 3", "remove spaces before commas"

# dots formatting
assert run("1,...,2\n") == "1, ..., 2", "space before dots"

# no space after dots unless required elsewhere
assert run("...123\n") == "...123", "dots at beginning"

# larger mixed case
assert run("10,20   30,...40\n") == "10, 20 30, ...40", "mixed formatting"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `7` | `7` | Minimum valid input |
| `12     34` | `12 34` | Collapsing spaces between numbers |
| `1 ,2,3` | `1, 2, 3` | Removing illegal spaces before commas |
| `1,...,2` | `1, ..., 2` | Correct handling of `...` |
| `...123` | `...123` | No forced space after dots |
| `10,20   30,...40` | `10, 20 30, ...40` | Multiple formatting rules interacting |

## Edge Cases

Consider the input:

```
1 ,2
```

Tokenization ignores spaces entirely and produces:

```
["1", ",", "2"]
```

During reconstruction, the comma is appended directly after `1`, and `2` receives exactly one leading space because it follows a comma.

The output becomes:

```
1, 2
```

This correctly removes the illegal space before the comma.

Now consider:

```
...1
```

The tokens are:

```
["...", "1"]
```

The first token never receives a leading space because it starts the string. The number `1` does not receive a leading space either because the previous token is neither a comma nor another number.

The final result is:

```
...1
```

This confirms that the algorithm does not incorrectly invent spaces after `...`.

Next, examine:

```
1     2
```

The tokens become:

```
["1", "2"]
```

Since both adjacent tokens are numbers, reconstruction inserts exactly one space between them.

The output is:

```
1 2
```

All extra spaces disappear while preserving the required separator.

Finally, consider:

```
1,...,2
```

The token sequence is:

```
["1", ",", "...", ",", "2"]
```

The `...` token receives a leading space because it is not the first token. The number `2` receives a leading space because it follows a comma.

The reconstructed string becomes:

```
1, ..., 2
```

This demonstrates that commas and suspension points interact correctly even when no spaces existed in the original input.
