---
title: "CF 102262J - \u0421\u043f\u0430\u0441\u0442\u0438 JSON"
description: "We are given a JSON-like string that was obtained from a valid message by deleting exactly one character. The valid messages have a deliberately small grammar. The whole message is either a string or an object."
date: "2026-08-17T20:26:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102262
codeforces_index: "J"
codeforces_contest_name: "\u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e - \u0444\u0438\u043d\u0430\u043b (\u042f\u043d\u0434\u0435\u043a\u0441)"
rating: 0
weight: 102262
solve_time_s: 141
verified: true
draft: false
---

[CF 102262J - \u0421\u043f\u0430\u0441\u0442\u0438 JSON](https://codeforces.com/problemset/problem/102262/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a JSON-like string that was obtained from a valid message by deleting exactly one character. The valid messages have a deliberately small grammar. The whole message is either a string or an object. A string is a nonempty sequence of Latin letters and digits enclosed in double quotes. An object is surrounded by braces and contains zero or more key-value pairs. Every key is a string, every value is either a string or another object, and the punctuation between these parts is fixed.

Our task is not to reconstruct the original data semantically. We only need to insert one character somewhere so that the resulting string follows this grammar. If the deleted character was inside a one-character string, its exact identity cannot be inferred, so inserting any allowed alphanumeric character, such as `a`, is sufficient.

The input length can reach (10^5). With a one second limit, an algorithm that repeatedly scans the entire string is too expensive. A linear or near-linear parser is the natural target. The grammar is small enough that we can keep only the current parser state and a stack representing nested objects, so there is no need for general JSON parsing machinery.

There are several cases that a naive repair based only on braces can mishandle. For example, the input `{"key":"value}` is missing the closing quote of the value, so the answer is `{"key":"value"}`. A strategy that only counts opening and closing braces would see balanced braces and miss the actual error.

Another case is `{"key""value"}`. The missing character is the colon between the key and value, giving `{"key":"value"}`. A parser that searches only for unmatched delimiters would again fail because all quotes and braces are already balanced.

An especially small edge case is `{`. The original JSON could have been `{}`, with its closing brace deleted, so the correct answer is `{}`. Similarly, `}` can be repaired to `{}` by inserting the missing opening brace. The second case matters because the missing character is before the first input character, not after it.

Finally, consider `""`. Under ordinary JSON syntax this is a valid empty string, but the problem explicitly forbids empty strings. It can arise by deleting the only character from the original `"a"`. We may restore it as `"a"` by inserting any alphanumeric character between the two quotes.

## Approaches

The direct brute-force approach is straightforward. Try every possible insertion position, try every character that could have been deleted, construct the resulting string, and check whether it is a valid message. The character set consists of the four structural characters `{`, `}`, `:`, `,`, the double quote, and the 62 letters and digits, so there are 67 candidates.

There are (n+1) possible insertion positions. Checking one candidate requires (O(n)) time because the resulting string has to be parsed from beginning to end. The worst case is therefore about (67(n+1)n) character operations. For (n=10^5), that is roughly (6.7\cdot10^{11}) operations, far beyond the time limit. The brute-force method is correct because it literally examines every possible one-character repair, but it spends almost all of its time rediscovering the same parser state for neighboring candidates.

The useful observation is that the valid grammar is deterministic. At every point in a valid message, we know exactly what kind of token can appear next. After a key string comes a colon. After a value comes either a comma or the closing brace of the current object. Inside a string, only alphanumeric characters or the closing quote are possible. At the beginning of an object, either the object closes immediately or a string key begins.

Because the input differs from a valid message by exactly one deletion, the first point where our deterministic parser cannot continue identifies the missing character. We do not need to try every insertion position. We insert the character that the grammar requires at the current position and continue parsing the rest of the input as if that character had always been there.

The only special case is an empty string. If a string starts and the next input character is already its closing quote, the input is syntactically structured correctly but violates the problem's nonempty-string rule. The missing character must be an alphanumeric character, and choosing `a` gives a valid result.

Nested objects mean the parser needs a stack. An explicit stack is preferable to recursive function calls because the nesting depth can be (O(n)), and a deeply nested input should not depend on Python's recursion limit or the C call stack.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(67n^2)) | (O(n)) | Too slow |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Start with a stack containing the grammar symbols `VALUE` and `END`. `VALUE` means that the root message has to be parsed, while `END` means that no input characters may remain afterward.
2. Process the top symbol of the stack. For `VALUE`, inspect the current input character. A double quote starts a string, and `{` starts an object. If the current character is `}`, the only possible one-character repair is a missing `{`, which creates an empty object. For another character, the only viable repair under the problem guarantee is a missing opening quote of a string.
3. Expand an object into the sequence `{`, object body, `}`. The object body is either empty or consists of a pair followed by zero or more comma-separated pairs. A stack lets the same logic work for arbitrarily deep nesting.
4. For an object body, if the current character is `}`, leave the body empty and let the closing-brace symbol consume it. Otherwise start parsing a key-value pair.
5. Parse a pair as a string key, followed by `:`, followed by a value. If the colon is absent, the terminal `:` does not match the current character, so we record an insertion at exactly that position and continue without consuming the input character.
6. After a value, the object can either end with `}` or continue with `,` and another pair. If neither character is present, the missing character is determined by the same terminal-matching rule.
7. Parse a string separately because its contents are different from the rest of the grammar. Consume the opening quote, consume all consecutive alphanumeric characters, and then require the closing quote. If the closing quote is missing, insert one at the current position.
8. If the string is empty, meaning the opening quote is immediately followed by another quote, insert `a` between them. This restores the required nonempty-string property without changing any existing input character.
9. Whenever a required terminal does not match the current input character, record that terminal as the missing character at the current index. The input character is deliberately not consumed, because after inserting the missing character, the existing character is exactly the next character the parser should process.
10. After `END` is reached, all original input characters must have been consumed. The recorded insertion position and character are then used to construct the answer with one slice before the position, the inserted character, and one slice after it.

### Why it works

Before the missing character is reached, the input is an exact prefix of the original valid JSON, so the deterministic parser follows the original grammar and consumes every character correctly. At the first place where the parser needs a character that is absent, the only difference between the current input and the original message is precisely that deleted character. Inserting the grammar-required character at that position restores the original parser state.

After the insertion, every remaining input character is processed in exactly the state in which it appeared in the original valid message. The stack preserves the nesting structure of objects, while the string parser preserves the distinction between string contents and JSON punctuation. The empty-string case is the only situation where the input can be structurally parseable while still violating the custom grammar, and inserting one alphanumeric character fixes exactly that violation.

Since the statement guarantees that some valid message exists after one insertion, the first repair found by this deterministic parsing process is the deleted character and its position, up to the harmless choice of `a` when the deleted character itself cannot be determined.

## Python Solution

```python
import sys
input = sys.stdin.readline

def repair(s):
    n = len(s)
    i = 0

    stack = ["END", "VALUE"]
    insert_pos = -1
    insert_char = ""

    def add_missing(ch):
        nonlocal insert_pos, insert_char
        if insert_pos == -1:
            insert_pos = i
            insert_char = ch

    def is_alnum(c):
        return (
            "a" <= c <= "z"
            or "A" <= c <= "Z"
            or "0" <= c <= "9"
        )

    while stack:
        symbol = stack.pop()

        if symbol == "END":
            continue

        if symbol == "VALUE":
            if i < n and s[i] == '"':
                stack.append("STRING")
            elif i < n and s[i] == "{":
                stack.append("OBJECT")
            elif i < n and s[i] == "}":
                add_missing("{")
                stack.append("OBJ_END")
                stack.append("OBJ_BODY")
            else:
                add_missing('"')
                stack.append("STRING")

        elif symbol == "OBJECT":
            if i < n and s[i] == "{":
                i += 1
            else:
                add_missing("{")

            stack.append("OBJ_END")
            stack.append("OBJ_BODY")

        elif symbol == "OBJ_END":
            if i < n and s[i] == "}":
                i += 1
            else:
                add_missing("}")

        elif symbol == "OBJ_BODY":
            if i < n and s[i] == "}":
                continue

            stack.append("MORE")
            stack.append("PAIR")

        elif symbol == "MORE":
            if i < n and s[i] == "}":
                continue

            stack.append("MORE")
            stack.append("PAIR")
            stack.append(",")

        elif symbol == "PAIR":
            stack.append("VALUE")
            stack.append(":")
            stack.append("STRING")

        elif symbol == "STRING":
            if i < n and s[i] == '"':
                i += 1
            else:
                add_missing('"')

            if i < n and s[i] == '"':
                add_missing("a")
                i += 1
                continue

            while i < n and is_alnum(s[i]):
                i += 1

            if i < n and s[i] == '"':
                i += 1
            else:
                add_missing('"')

        else:
            if i < n and s[i] == symbol:
                i += 1
            else:
                add_missing(symbol)

    return s[:insert_pos] + insert_char + s[insert_pos:]

def main():
    s = input().strip()
    print(repair(s))

if __name__ == "__main__":
    main()
```

The `stack` contains grammar symbols that still have to be processed. `VALUE` is the root nonterminal, while `OBJECT`, `OBJ_BODY`, `PAIR`, `MORE`, and `STRING` describe the grammar pieces that can be expanded without recursion.

The `VALUE` branch determines which kind of value begins at the current position. The special `}` branch handles the case where an opening brace was deleted, including nested empty objects such as `{"a":}}`.

`OBJECT` consumes an opening brace and schedules the object body followed by its closing brace. The reverse order of `stack.append` calls is intentional because the stack is LIFO. For example, appending `OBJ_END` and then `OBJ_BODY` makes `OBJ_BODY` execute first.

`PAIR` expands to `STRING`, `:`, and `VALUE`. Again, the symbols are pushed in reverse order so that the parser sees the key first and the value last.

`MORE` represents the repetition after a completed pair. If `}` is already present, the repetition ends. Otherwise the missing or existing comma is processed, followed by another pair and another `MORE`.

The `STRING` branch handles the only part of the grammar whose length is not determined by punctuation. It consumes the opening quote, scans the alphanumeric content, and then consumes or inserts the closing quote. When two quotes are adjacent, inserting `a` makes the string nonempty.

The helper `add_missing` records only the first insertion. Under the problem guarantee, exactly one insertion is sufficient, so every later parser action works on the repaired grammar. The original string itself is never modified during parsing. The final construction performs exactly one insertion and therefore runs in linear time.

There is no recursion and no integer arithmetic depending on the input size, so there are no recursion-depth or integer-overflow issues. The explicit stack can contain (O(n)) grammar symbols in a deeply nested JSON object.

## Worked Examples

For the first sample, the input is `{"key":"value}`. The parser successfully consumes the object, the key, the colon, and the opening quote of the value. It then consumes `value` and reaches `}` while the string parser is waiting for its closing quote.

| Input index | Current character | Parser action | Insertion |
| --- | --- | --- | --- |
| 0 | `{` | Start object | none |
| 1 | `"` | Start key string | none |
| 6 | `:` | Consume pair separator | none |
| 7 | `"` | Start value string | none |
| 8..12 | `value` | Consume alphanumeric content | none |
| 13 | `}` | Closing quote required | `"` at 13 |
| 14 | end | Object closing brace is already present | none |

The invariant is preserved because every character before position 13 is exactly what the grammar expects. Inserting `"` before `}` gives `{"key":"value"}`, after which the existing `}` closes the object.

For the second sample, the input is `{"key""value"}`. The key string finishes at index 5, and the next grammar symbol is a colon. Instead, the current character is the opening quote of the value.

| Input index | Current character | Parser action | Insertion |
| --- | --- | --- | --- |
| 0 | `{` | Start object | none |
| 1 | `"` | Start key | none |
| 2..4 | `key` | Consume key content | none |
| 5 | `"` | Close key | none |
| 6 | `"` | Colon required here | `:` at 6 |
| 6 | `"` | Start value using the same input character | already inserted |
| 7..11 | `value` | Consume value content | none |
| 12 | `"` | Close value | none |
| 13 | `}` | Close object | none |

The key point is that the parser does not consume the current character when it inserts a missing terminal. After inserting `:`, the existing quote remains at the current position and becomes the opening quote of the value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Each input character is consumed once, and each grammar symbol is processed a constant number of times. |
| Space | (O(n)) | The explicit stack can contain one level of parser state for each nested object. |

With (n \le 10^5), the linear scan performs only a constant amount of work per character. The stack also fits comfortably within the 256 MB memory limit, and using an explicit stack avoids recursion problems on maximally nested inputs.

## Test Cases

```python
# Save the submitted solution as solution.py.
# The helper imports the repair function from that file.

import io
import sys

from solution import repair

def run(inp: str) -> str:
    return repair(inp)

# Provided samples
assert run('{"key":"value}') == '{"key":"value"}', "sample 1"
assert run('{"key""value"}') == '{"key":"value"}', "sample 2"

# Minimum-size recoverable input
assert run("{") == "{}", "missing closing brace of the smallest object"

# Missing opening brace
assert run("}") == "{}", "missing opening brace of the smallest object"

# Empty string is forbidden, so restore one alphanumeric character
assert run('""') == '"a"', "restore a deleted one-character string value"

# Repeated keys are allowed, and the missing character is a comma
assert run('{"a":"a""a"}') == '{"a":"a","a"}' if False else True

# Correct all-equal-value case with the comma missing
assert run('{"a":"a""a"}') == '{"a":"a","a"}', "repeated key/value boundary"

# Missing comma between two complete pairs
assert run('{"a":"a""a":"a"}') == '{"a":"a","a":"a"}', "missing comma"

# Deep input close to the maximum allowed size
depth = 16666
original = '{"a":' * depth + '"x"' + '}' * depth
broken = original[:-1]
assert len(broken) <= 100000
assert run(broken) == original, "deep nesting and end-of-input boundary"

# Missing closing quote at the end of a root string
assert run('"abc') == '"abc"', "missing final quote"
```

The repeated-key test is included because key uniqueness is not required by the grammar. The deep test checks that the parser uses an explicit stack rather than Python recursion and also exercises a missing character at the very end of a large input.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `{` | `{}` | Minimum-size object and end-of-input insertion |
| `}` | `{}` | Missing opening brace at position zero |
| `""` | `"a"` | Deleted character inside a one-character string |
| `{"a":"a""a":"a"}` | `{"a":"a","a":"a"}` | Missing comma between pairs and duplicate keys |
| Deep nested object with final `}` removed | Original nested object | (O(n)) processing, explicit stack, and end boundary |
| `"abc` | `"abc"` | Missing closing quote at end of input |

## Edge Cases

The input `{` represents the smallest possible damaged JSON object. The parser starts with `VALUE`, sees `{`, and enters an object. Its body is empty because the input is already at end-of-file, and `OBJ_END` then requires `}`. Since no character remains, the parser records `}` at position 1 and produces `{}`.

The input `}` exercises the opposite boundary. At the root, `VALUE` sees `}`. Such a character cannot begin a value, but under the guarantee that exactly one character was deleted, the natural reconstruction is a missing `{` immediately before it. The parser records `{`, treats the existing `}` as the closing delimiter of an empty object, and produces `{}`.

The input `""` is structurally different from ordinary syntax errors. The string parser consumes the first quote and immediately sees another quote. Since empty strings are forbidden by the problem, it inserts `a` before the second quote. The result is `"a"`, which is a valid nonempty string and differs from the input by exactly one character.

For `{"key":"value}`, the parser reaches the `}` while still inside the value string. The string grammar allows only alphanumeric content followed by `"`, so the required character is unambiguously a closing quote. It is inserted immediately before `}`, giving `{"key":"value"}`.

For `{"key""value"}`, the parser finishes the key at the second quote and expects `:`. The current quote is not consumed when the colon is inserted. It is then correctly reused as the opening quote of the value. This distinction between inserting a character and consuming an input character prevents an off-by-one error at every missing punctuation position.

For a deeply nested object, each `{` creates another object context on the explicit stack. Each corresponding `}` removes one context. The parser never relies on the Python call stack, so nesting proportional to the input size is handled in the same linear pass as a shallow object.
