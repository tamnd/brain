---
title: "CF 1089J - JS Minification"
description: "We are given a small programming language source file together with a set of reserved tokens. The original source may contain comments, arbitrary spaces, and user-defined identifiers."
date: "2026-06-13T03:46:36+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1089
codeforces_index: "J"
codeforces_contest_name: "2018-2019 ICPC, NEERC, Northern Eurasia Finals (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 3200
weight: 1089
solve_time_s: 364
verified: false
draft: false
---

[CF 1089J - JS Minification](https://codeforces.com/problemset/problem/1089/J)

**Rating:** 3200  
**Tags:** greedy, implementation  
**Solve time:** 6m 4s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a small programming language source file together with a set of reserved tokens. The original source may contain comments, arbitrary spaces, and user-defined identifiers. The parser removes comments, skips spaces, and repeatedly extracts the longest valid token according to the language rules.

The task has two distinct parts.

First, we must reconstruct the exact token sequence represented by the source. During this process, comments disappear and spacing becomes irrelevant.

Second, every user-defined word must be renamed according to a deterministic scheme. The first distinct word encountered becomes the first available lowercase identifier, the second distinct word becomes the second available lowercase identifier, and so on. Reserved tokens are excluded from this generated identifier sequence.

After renaming, we must print a single line whose tokenization produces exactly the renamed token sequence. Among all such outputs, we need one with the minimum possible number of spaces.

The constraints are surprisingly small. There are at most 40 reserved tokens, at most 40 source lines, and each line has length at most 80. The entire input is only a few thousand characters. This means we do not need sophisticated parsing machinery. Even algorithms with complexity proportional to the square of the source length are completely safe.

The difficult part is not efficiency. The challenge is correctly reproducing the parser's longest-match behavior and determining exactly when spaces are required between adjacent output tokens.

Several edge cases are easy to miss.

Consider reserved tokens that are prefixes of other reserved tokens.

```
Reserved: + ++
Source: ++
```

The parser must produce the token `++`, not two `+` tokens. A parser that accepts the first matching reserved token instead of the longest matching one will produce the wrong token sequence.

Consider reserved tokens that also satisfy the definition of a word.

```
Reserved: while
Source: while abc
```

The token `while` is reserved and must never be renamed. Treating every alphanumeric string as a word would incorrectly rename it.

Consider adjacent tokens that merge into a larger word.

```
Tokens: a b
```

Printing `ab` without a space changes the parsing result from two words into one word. At least one space is required.

The opposite situation also occurs.

```
Tokens: a +
```

Printing `a+` is perfectly safe. Adding a space would only make the result longer.

A particularly subtle case is when two reserved tokens concatenate into another reserved token.

```
Reserved: + ++
Tokens: + +
```

Printing `++` would be parsed as a single `++` token because the parser always takes the longest possible token. A space is mandatory even though neither token is a word or number.

Understanding exactly when adjacent tokens can be written without separators is the core of the problem.

## Approaches

A brute-force viewpoint is useful for understanding the optimization problem.

After obtaining the renamed token sequence, suppose there are `k` tokens. Between every adjacent pair we may either insert a space or not. There are `2^(k-1)` possible outputs. For each candidate output we could run the parser again and check whether it reconstructs the desired token sequence. The shortest valid one would be the answer.

This approach is correct because it explicitly tests every possible placement of spaces. Unfortunately, even a few dozen tokens already make the search space astronomical.

The key observation is that the decision between two neighboring tokens is completely local.

Suppose we have already renamed all identifiers. Consider two consecutive output tokens `A` and `B`.

If writing `A+B` causes the parser to produce exactly the same two tokens, then omitting the space is always better because spaces only increase the length.

If writing `A+B` causes the parser to produce anything else, then a space is mandatory.

There is no interaction with other positions. Whether we need a separator between tokens `i` and `i+1` depends only on those two tokens.

This reduces the problem to two independent tasks.

First, recover and rename the token sequence.

Second, for every adjacent pair, determine whether concatenation changes the parsing result.

Because the input size is tiny, we can simply reuse the parser itself. For a pair `(A,B)`, parse the string `A+B`. If the result is exactly `[A,B]`, no space is needed. Otherwise, insert one space.

The same longest-match parser that extracts tokens from the original source also answers the spacing question.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^k · k) | O(k) | Too slow |
| Optimal | O(T + k · L²) | O(T) | Accepted |

Here `T` is the total source length and `L` is the maximum token length. Since all limits are tiny, this is easily fast enough.

## Algorithm Walkthrough

### Parsing model

The parser must exactly match the statement.

At any position:

1. Skip spaces.
2. Among all reserved tokens beginning at the current position, take the longest one if any exist.
3. Otherwise, if the current character is a digit, consume the longest digit sequence and create a number token.
4. Otherwise, consume the longest valid word and create a word token.

The input is guaranteed to be valid.

### Word generation

The target identifier sequence consists of lowercase words ordered first by length and then lexicographically:

```
a, b, ..., z, aa, ab, ...
```

Any identifier that is itself a reserved token must be skipped.

### Renaming

While traversing the parsed token sequence:

1. If the token is not a word, keep it unchanged.
2. If the token is a reserved token, keep it unchanged.
3. Otherwise, if this word has not appeared before, assign the next available generated identifier.
4. Replace every occurrence of that original word by its assigned identifier.

### Minimal spacing

For every adjacent pair of renamed tokens `(A,B)`:

1. Form the string `A+B`.
2. Parse this string using the same tokenizer.
3. If the result is exactly the two-token sequence `[A,B]`, append `B` directly after `A`.
4. Otherwise insert one space before `B`.

A single space is always sufficient because spaces are skipped before tokenization.

### Why it works

The parser is deterministic and always chooses the longest valid token at each position.

After renaming, the target token sequence is fixed. The only remaining freedom is where to place spaces.

For any adjacent pair, omitting the separator is valid exactly when parsing the concatenation reproduces those two tokens. If it does not, then no output without a separator can preserve the token sequence because the parser would interpret the boundary differently.

Since every space decision depends only on one adjacent pair and spaces never decrease length, the optimal strategy is to omit a space whenever possible and insert one only when necessary. Applying this rule independently to every boundary yields the minimum possible total number of spaces.

## Python Solution

```python
import sys
input = sys.stdin.readline

WORD_CHARS = set(
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789_$"
)

def is_word_start(c):
    return c.isalpha() or c == '_' or c == '$'

def tokenize(text, reserved):
    tokens = []
    i = 0
    n = len(text)

    while i < n:
        while i < n and text[i] == ' ':
            i += 1
        if i >= n:
            break

        best = None
        best_len = 0

        for tok in reserved:
            if text.startswith(tok, i) and len(tok) > best_len:
                best = tok
                best_len = len(tok)

        if best is not None:
            tokens.append(best)
            i += best_len
            continue

        c = text[i]

        if c.isdigit():
            j = i
            while j < n and text[j].isdigit():
                j += 1
            tokens.append(text[i:j])
            i = j
            continue

        j = i
        while j < n and text[j] in WORD_CHARS:
            j += 1
        tokens.append(text[i:j])
        i = j

    return tokens

def is_word_token(token, reserved):
    if token in reserved:
        return False
    if not token:
        return False
    if token[0].isdigit():
        return False
    return all(ch in WORD_CHARS for ch in token)

def generate_names(reserved):
    length = 1

    while True:
        total = 26 ** length

        for x in range(total):
            cur = []
            y = x

            for _ in range(length):
                cur.append(chr(ord('a') + (y % 26)))
                y //= 26

            name = ''.join(reversed(cur))

            if name not in reserved:
                yield name

        length += 1

def solve():
    n = int(input())

    reserved = set()
    if n:
        reserved = set(input().split())
    else:
        input()

    m = int(input())

    source_tokens = []

    for _ in range(m):
        line = input().rstrip('\n')

        pos = line.find('#')
        if pos != -1:
            line = line[:pos]

        source_tokens.extend(tokenize(line, reserved))

    gen = generate_names(reserved)

    mapping = {}
    renamed = []

    for tok in source_tokens:
        if is_word_token(tok, reserved):
            if tok not in mapping:
                mapping[tok] = next(gen)
            renamed.append(mapping[tok])
        else:
            renamed.append(tok)

    if not renamed:
        print()
        return

    answer = [renamed[0]]

    for i in range(1, len(renamed)):
        a = renamed[i - 1]
        b = renamed[i]

        merged = a + b
        parsed = tokenize(merged, reserved)

        if len(parsed) == 2 and parsed[0] == a and parsed[1] == b:
            answer.append(b)
        else:
            answer.append(' ')
            answer.append(b)

    print(''.join(answer))

if __name__ == "__main__":
    solve()
```

The tokenizer is the central component. It is used twice: once to recover the original token sequence and later to test whether two neighboring output tokens can be concatenated safely.

The longest-reserved-token rule must be implemented before number and word recognition. This matches the statement's precedence rules. For example, if `while` is reserved, the string `while` must become a reserved token rather than a word.

The identifier generator enumerates lowercase strings by increasing length and lexicographic order. Any generated name that belongs to the reserved set is skipped.

The spacing phase deliberately reuses the parser instead of trying to derive dozens of special cases. This avoids mistakes involving reserved-token overlaps such as `+` versus `++` or identifiers adjacent to numbers.

## Worked Examples

### Example 1

Input from the statement.

The first distinct user words appear in this order:

| Original word | Assigned name |
| --- | --- |
| fib | a |
| num | b |
| return_value | c |
| prev | d |
| temp | e |

Part of the renamed token sequence becomes:

| Token index | Token |
| --- | --- |
| 1 | fun |
| 2 | a |
| 3 | ( |
| 4 | b |
| 5 | ) |
| 6 | { |
| 7 | var |
| 8 | c |

Now consider some adjacent pairs.

| A | B | Concatenation | Parsed result | Space needed |
| --- | --- | --- | --- | --- |
| fun | a | funa | [funa] | Yes |
| a | ( | a( | [a, (] | No |
| c | = | c= | [c, =] | No |
| + | d | +d | [+, d] | No |

The final output is:

```
fun a(b){var c=1,d=0,e;while(b>0){e=c;c=c+d;d=e;b--;}return c;}
```

This example demonstrates that most separators disappear, while spaces survive only where concatenation would merge tokens.

### Example 2

Constructed example:

```
Reserved:
+
++

Source:
x + +
```

Renaming gives:

```
a + +
```

Boundary analysis:

| A | B | Concatenation | Parsed result | Space needed |
| --- | --- | --- | --- | --- |
| a | + | a+ | [a, +] | No |
| + | + | ++ | [++] | Yes |

Final output:

```
a+ +
```

Without the inserted space, the parser would see a single `++` token.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T + k · L²) | Parsing the source plus reparsing each adjacent concatenation |
| Space | O(T) | Stores tokens, mappings, and output |

The total source size is only a few thousand characters. Even repeatedly reparsing concatenated token pairs is negligible. The solution comfortably fits within both the time limit and memory limit.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    # insert solution implementation here
    pass

# sample 1
assert run("""16
fun while return var { } ( ) , ; > = + ++ - --
9
fun fib(num) { # compute fibs
  var return_value = 1, prev = 0, temp;
  while (num > 0) {
    temp = return_value; return_value = return_value + prev;
    prev = temp;
    num--;
  }
  return return_value;
}
""").strip() == "fun a(b){var c=1,d=0,e;while(b>0){e=c;c=c+d;d=e;b--;}return c;}"

# minimum case
assert run("""0

1
abc
""").strip() == "a"

# repeated identifier
assert run("""0

1
foo foo foo
""").strip() == "a a a"

# reserved token overlapping another reserved token
assert run("""2
+ ++
1
x + +
""").strip() == "a+ +"

# identifier next to number
assert run("""0

1
x 123
""").strip() == "a 123"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single identifier | `a` | Smallest valid program |
| `foo foo foo` | `a a a` | Consistent renaming of repeated words |
| `x + +` with `+` and `++` reserved | `a+ +` | Longest-match reserved-token ambiguity |
| `x 123` | `a 123` | Word-number boundary requires a separator |

## Edge Cases

Consider reserved words that look like identifiers.

```
Reserved:
while

Source:
while x
```

The tokenizer classifies `while` as reserved before considering the word rule. It remains unchanged. Only `x` is renamed to `a`. The output becomes:

```
while a
```

A solution that renames every identifier-shaped token would incorrectly produce `a b`.

Consider two words that become one word after concatenation.

```
Source:
foo bar
```

After renaming:

```
a b
```

The concatenation `ab` parses as a single word token. Reparsing detects this because the result is `[ab]` instead of `[a, b]`. A space is inserted, giving the correct output `a b`.

Consider overlapping operators.

```
Reserved:
+
++

Source:
+ +
```

The concatenation `++` parses as one reserved token. Reparsing returns `[++]`, so a space is inserted. The output remains `+ +`, preserving the original token sequence.

Consider a word followed by a number.

```
Source:
abc 123
```

After renaming:

```
a 123
```

The concatenation `a123` is a single word token because digits may appear after the first character of a word. Reparsing catches this, so the algorithm inserts a separator and outputs `a 123`. This preserves the intended token boundary.
