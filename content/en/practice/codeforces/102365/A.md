---
title: "CF 102365A - Abnormal Words"
description: "We need to transform a lowercase word using a Caesar cipher. The input first tells us whether to encode or decode. Encoding moves every letter forward by a fixed shift s, while decoding moves every letter backward by the same amount."
date: "2026-08-14T02:55:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102365
codeforces_index: "A"
codeforces_contest_name: "UBC Programming Contest 2019 (UBCPC 2019)"
rating: 0
weight: 102365
solve_time_s: 78
verified: true
draft: false
---

[CF 102365A - Abnormal Words](https://codeforces.com/problemset/problem/102365/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to transform a lowercase word using a Caesar cipher. The input first tells us whether to encode or decode. Encoding moves every letter forward by a fixed shift `s`, while decoding moves every letter backward by the same amount. The alphabet is cyclic, so moving past `z` continues from `a`, and moving before `a` continues from `z`.

For example, with shift `4`, the letter `x` becomes `b` during encoding because the four forward positions are `y`, `z`, `a`, `b`. During decoding, `b` becomes `x` for the same reason in reverse.

The first input line is either `E` or `D`, the second contains the shift `s`, and the third contains the word. The word contains between 1 and 100 lowercase letters. Since the word is so short, even a straightforward character-by-character simulation is easily fast enough. The shift is at most 25, so even an implementation that moves one alphabet position at a time would perform at most `100 * 25 = 2500` character movements.

The interesting part is not performance but handling the cyclic alphabet correctly. A direct character comparison such as `ord(c) + s` can produce a value outside the range for lowercase letters when the result passes `z`. Converting the letter to a number from 0 through 25 and using modulo 26 avoids that boundary problem completely.

A single-letter word is a useful minimum-size case. For input `E`, shift `1`, and word `a`, the answer is `b`. An implementation that accidentally processes only words of length greater than one would fail here.

Wrapping at either end is the main boundary case. For example, encoding `z` by `1` gives `a`, not the character after `z` in Unicode. Similarly, decoding `a` by `1` gives `z`. A careless implementation that simply adds or subtracts from the character code without modulo 26 will produce an invalid character.

The shift can also be larger than the distance to the alphabet boundary. With `E`, shift `25`, and word `b`, the result is `a`. Thinking of the shift as an ordinary integer addition without cyclic arithmetic makes these cases easy to mishandle.

## Approaches

A direct brute-force implementation can process each character by repeatedly moving it one position through the alphabet. For every character, we perform the shift one step at a time, wrapping from `z` to `a` or from `a` to `z` as needed. This is correct because applying one valid alphabet transition repeatedly produces exactly the requested Caesar shift.

With at most 100 characters and a shift of at most 25, this performs at most 2500 single-position movements. That is nowhere near the limit for a one-second program, so this approach is actually accepted for the given constraints. Its weakness is that it does unnecessary work and obscures the simple mathematical structure of the operation.

The key observation is that the alphabet has exactly 26 positions and those positions form a cycle. Represent `a` as 0, `b` as 1, through `z` as 25. Encoding then becomes `(value + s) % 26`, while decoding becomes `(value - s) % 26`. Python's modulo operation handles negative values correctly, so decoding `a` with shift `1` naturally produces position 25, which is `z`.

The brute-force method works because repeated one-step moves eventually reach the same destination. The observation that the alphabet is a fixed cycle lets us replace all those individual moves with one modular arithmetic operation. The resulting algorithm needs exactly one transformation per character.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Repeated one-step shifting | O( | w | s) | O( | w | ) | Accepted, but unnecessary work |
| Modular arithmetic | O( | w | ) | O( | w | ) | Accepted |

## Algorithm Walkthrough

1. Read the operation type, the shift `s`, and the word. The operation type determines whether the shift should be added or subtracted from every character.
2. Convert each character into its zero-based alphabet position using `ord(c) - ord('a')`. This maps the alphabet to the convenient numeric range `0` through `25`.
3. If the operation is encoding, add `s` to the position. If the operation is decoding, subtract `s`. The direction directly matches the definition of the two operations.
4. Apply `% 26` to the resulting position. This makes the alphabet cyclic, so values past 25 wrap to the beginning and negative values wrap to the end.
5. Convert the resulting position back to a lowercase character with `chr(position + ord('a'))`, and append it to the answer.
6. Print the transformed word. Each input character has been transformed independently, so processing all characters produces the complete encrypted or decrypted word.

### Why it works

At every iteration, the current answer character represents exactly the Caesar transformation of the corresponding input character. Its zero-based alphabet position is increased by `s` for encoding or decreased by `s` for decoding, and modulo 26 identifies the unique position on the cyclic alphabet after that movement. Since the transformation is correct for every character independently, concatenating all transformed characters gives exactly the required word.

## Python Solution

```python
import sys
input = sys.stdin.readline

operation = input().strip()
s = int(input())
word = input().strip()

result = []

for c in word:
    pos = ord(c) - ord('a')

    if operation == 'E':
        pos = (pos + s) % 26
    else:
        pos = (pos - s) % 26

    result.append(chr(pos + ord('a')))

print(''.join(result))
```

The first three lines read the operation, shift, and word in the same order as the input format. `strip()` removes the newline from each line, while preserving the actual lowercase word.

For each character, `ord(c) - ord('a')` produces a value from 0 to 25. This is preferable to manipulating ASCII values directly because the modulo operation now corresponds exactly to positions in the alphabet.

The encoding branch adds the shift before taking modulo 26. For decoding, subtraction is used instead. Python's `%` operator maps a negative result back into the range from 0 through 25, so `(0 - 1) % 26` is `25`. This handles decoding `a` into `z` without any special boundary condition.

The result is accumulated in a list because strings are immutable in Python. Appending each character and joining once is simple and runs in linear time.

There is no integer overflow concern because the largest position involved is tiny. The main implementation detail that matters is taking modulo 26 after the addition or subtraction, rather than forgetting the wraparound at the alphabet boundaries.

## Worked Examples

### Sample 1

The input requests encoding with shift `3` and the word `hello`.

| Character | Position | Operation | New Position | Output Character |
| --- | --- | --- | --- | --- |
| `h` | 7 | `7 + 3` | 10 | `k` |
| `e` | 4 | `4 + 3` | 7 | `h` |
| `l` | 11 | `11 + 3` | 14 | `o` |
| `l` | 11 | `11 + 3` | 14 | `o` |
| `o` | 14 | `14 + 3` | 17 | `r` |

The resulting word is `khoor`. No character crosses the end of the alphabet, so modulo 26 does not visibly change any of these positions. The trace demonstrates the basic encoding transformation.

### Sample 2

The input requests decoding with shift `3` and the word `jreeohghbjrrn`.

| Character | Position | Operation | New Position | Output Character |
| --- | --- | --- | --- | --- |
| `j` | 9 | `9 - 3` | 6 | `g` |
| `r` | 17 | `17 - 3` | 14 | `o` |
| `e` | 4 | `4 - 3` | 1 | `b` |
| `e` | 4 | `4 - 3` | 1 | `b` |
| `o` | 14 | `14 - 3` | 11 | `l` |
| `h` | 7 | `7 - 3` | 4 | `e` |
| `g` | 6 | `6 - 3` | 3 | `d` |
| `h` | 7 | `7 - 3` | 4 | `e` |
| `b` | 1 | `1 - 3` | 24 | `y` |
| `j` | 9 | `9 - 3` | 6 | `g` |
| `r` | 17 | `17 - 3` | 14 | `o` |
| `r` | 17 | `17 - 3` | 14 | `o` |
| `n` | 13 | `13 - 3` | 10 | `k` |

The result is `gobbledeygook`. The `b` in the ninth position is especially useful because its position becomes `-1` before modulo is applied, and `-1 % 26` gives `25`, which correctly maps to `y`. This demonstrates why modular arithmetic handles the cyclic boundary without a separate special case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | w | ) | Every character is processed once with constant-time arithmetic. |
| Space | O( | w | ) | The transformed characters are stored before joining them. |

The word has at most 100 characters, so the algorithm performs only a few hundred elementary operations in the worst case. It is comfortably within the one-second time limit and uses negligible memory compared with the 256 MB limit.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    operation = input().strip()
    s = int(input())
    word = input().strip()

    result = []

    for c in word:
        pos = ord(c) - ord('a')

        if operation == 'E':
            pos = (pos + s) % 26
        else:
            pos = (pos - s) % 26

        result.append(chr(pos + ord('a')))

    print(''.join(result))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()
    output = sys.stdout.getvalue().strip()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return output

assert run("E\n3\nhello\n") == "khoor", "sample 1"
assert run("D\n3\njreeohghbjrrn\n") == "gobbledeygook", "sample 2"

assert run("E\n1\na\n") == "b", "minimum-size encoding"
assert run("D\n1\na\n") == "z", "minimum-size decoding with wraparound"
assert run("E\n1\nzzzzzzzzzzzzzzzzzzzz\n") == "aaaaaaaaaaaaaaaaaaaa", "all-equal boundary case"
assert run("D\n25\nabcdefghijklmnopqrstuvwxyz\n") == "bcdefghijklmnopqrstuvwxyza", "maximum shift and full alphabet"
assert run("E\n25\nb\n") == "a", "large shift crossing the alphabet boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `E`, `1`, `a` | `b` | Minimum word size and ordinary encoding |
| `D`, `1`, `a` | `z` | Backward wraparound at the start of the alphabet |
| `E`, `1`, repeated `z` | Repeated `a` | Forward wraparound and all-equal characters |
| `D`, `25`, alphabet | `bcdefghijklmnopqrstuvwxyza` | Maximum shift and every alphabet position |
| `E`, `25`, `b` | `a` | Large shift with a boundary crossing |

## Edge Cases

The minimum-size input `E`, shift `1`, word `a` produces `b`. The algorithm converts `a` to position 0, adds 1, and obtains position 1, which converts back to `b`. There is no assumption that the word contains multiple characters.

For forward wraparound, consider `E`, shift `1`, word `z`. The character `z` has position 25. Adding the shift gives 26, and `26 % 26` is 0, so the result is `a`. A direct character-code addition would not have this behavior.

For backward wraparound, consider `D`, shift `1`, word `a`. The position is 0, and subtracting the shift gives `-1`. Python evaluates `-1 % 26` as 25, so the result becomes `z`. This is the main case that distinguishes correct modular arithmetic from an implementation that only handles nonnegative positions.

For a large shift, consider `E`, shift `25`, word `b`. The position of `b` is 1, so the transformed position is `(1 + 25) % 26 = 0`. The output is `a`. This catches implementations that accidentally use a special rule only for shifts close to the alphabet boundary.

Finally, consider a word containing only `z` characters, such as `E`, shift `1`, word `zzzz`. Every character independently maps from position 25 to position 0, producing `aaaa`. The per-character invariant remains valid even when every character exercises the same boundary condition.
