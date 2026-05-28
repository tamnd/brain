---
title: "CF 132A - Turing Tape"
description: "We are given the final text printed by INTERCAL's strange \"Turing Tape\" output procedure. Each printed character was produced from one integer of an unknown array. The encoding process depends on the previous printed character, so every step is linked to the one before it."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 132
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 96 (Div. 1)"
rating: 1300
weight: 132
solve_time_s: 99
verified: true
draft: false
---

[CF 132A - Turing Tape](https://codeforces.com/problemset/problem/132/A)

**Rating:** 1300  
**Tags:** implementation  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the final text printed by INTERCAL's strange "Turing Tape" output procedure. Each printed character was produced from one integer of an unknown array. The encoding process depends on the previous printed character, so every step is linked to the one before it.

For a single character, the process works like this:

First, take the previous printed character and reverse its 8-bit binary representation. For the very first character, this value is treated as `0`.

Second, subtract the current array value modulo `256`.

Third, reverse the bits again, and interpret the result as the ASCII code of the character that gets printed.

The task is to reconstruct the original array from the printed text.

The input length is at most `100`, which is tiny. Even an inefficient solution would easily fit inside the limits. The real challenge is understanding the transformation correctly and avoiding mistakes with bit reversal and modulo arithmetic.

The most error-prone part is the direction of the formula. The encoding subtracts the array value from the reversed previous character, not the other way around. If we accidentally compute:

```
x = current - previous
```

instead of

```
x = previous - current  (mod 256)
```

the entire sequence becomes wrong.

Another common mistake is reversing only the significant bits instead of exactly 8 bits.

For example, the character `'A'` has ASCII value `65`.

```
65 = 01000001₂
```

Reversing all 8 bits gives:

```
10000010₂ = 130
```

A careless implementation might reverse only `"1000001"` and get `"1000001"` again, incorrectly producing `65`.

Modulo handling is another subtle detail. Suppose the previous reversed value is `0` and the current reversed value is `18`.

The required array element is:

```
(0 - 18) mod 256 = 238
```

If we forget the modulo operation, we would output `-18`, which is invalid because array elements must be unsigned 8-bit integers.

## Approaches

A brute-force approach would try every possible array value from `0` to `255` for each character and simulate the encoding process until the produced character matches the target text.

For one position, we would potentially test `256` candidates, and each test requires reversing bits and checking the resulting character. With at most `100` characters, this becomes roughly `256 × 100 = 25600` attempts, which is still completely fine for the limits.

The brute-force works because the search space is very small. Every array element is an 8-bit value, so there are only `256` possibilities.

The problem is that brute force ignores the algebra hidden inside the transformation. The encoding process is fully reversible. Once we recognize that, guessing becomes unnecessary.

Suppose:

```
p = reverse_bits(previous_character)
c = reverse_bits(current_character)
```

The encoding rule says:

```
c = (p - a[i]) mod 256
```

Rearranging gives:

```
a[i] = (p - c) mod 256
```

Everything on the right side is already known from the text itself. The previous character is known, and the current character is known. That means each array element can be computed directly in constant time.

The key observation is that bit reversal is its own inverse. Reversing twice returns the original number. Because of that, we can simply reverse the ASCII values of the printed characters and reconstruct the exact intermediate states used during encoding.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(256n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string.
2. Maintain a variable `prev`, representing the reversed binary value of the previous printed character. Initialize it to `0`, because the statement defines the first step that way.
3. For each character in the string, compute its ASCII value with `ord()`.
4. Reverse the bits of this ASCII value using exactly 8 bits.

The reversal must preserve leading zeroes. For example:

```
00010010 -> 01001000
```
5. Let this reversed value be `cur`.
6. The encoding rule was:

```
cur = (prev - a[i]) mod 256
```

Rearranging gives:

```
a[i] = (prev - cur) mod 256
```

Compute this value and print it.
7. Update `prev = cur` before processing the next character.

### Why it works

The algorithm reconstructs exactly the same intermediate values used during encoding.

For every character, `cur` equals the result produced after step 2 of the original process, because reversing the printed character restores that intermediate state. Since the encoding equation is:

```
cur = (prev - a[i]) mod 256
```

solving for `a[i]` uniquely determines the original array value. The invariant is that `prev` always stores the reversed representation of the previous printed character, exactly matching the encoder's state before processing the next element.

Because every step is reversible and modulo `256` arithmetic is preserved, the reconstructed array is guaranteed to be correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def reverse_bits(x):
    res = 0

    for i in range(8):
        if x & (1 << i):
            res |= (1 << (7 - i))

    return res

def solve():
    s = input().rstrip("\n")

    prev = 0

    for ch in s:
        cur = reverse_bits(ord(ch))
        value = (prev - cur) % 256
        print(value)
        prev = cur

solve()
```

The `reverse_bits` function performs an exact 8-bit reversal. This detail matters because ASCII characters may contain leading zeroes in binary form. Using string slicing without padding would produce incorrect answers for many characters.

The variable `prev` stores the reversed binary representation of the previous printed character. Initially it is `0`, matching the statement's special rule for the first character.

For each character, the code computes:

```
value = (prev - cur) % 256
```

The modulo operation is essential because the original process uses unsigned 8-bit arithmetic. Python's `% 256` cleanly converts negative differences into the correct range `0..255`.

The update:

```
prev = cur
```

must happen after printing the current answer. Updating too early would shift the entire sequence by one position.

## Worked Examples

### Example 1

Input:

```
Hi
```

Step-by-step trace:

| Character | ASCII | Reversed bits (`cur`) | Previous (`prev`) | Output value |
| --- | --- | --- | --- | --- |
| H | 72 | 18 | 0 | 238 |
| i | 105 | 150 | 18 | 124 |

Output:

```
238
124
```

This trace shows how the state flows from one character to the next. The second computation depends on the reversed form of `'H'`, not on the original ASCII value.

### Example 2

Input:

```
A
```

Step-by-step trace:

| Character | ASCII | Reversed bits (`cur`) | Previous (`prev`) | Output value |
| --- | --- | --- | --- | --- |
| A | 65 | 130 | 0 | 126 |

Output:

```
126
```

This example demonstrates why leading zeroes matter. The 8-bit form of `65` is:

```
01000001
```

Reversing all eight bits gives:

```
10000010 = 130
```

A shorter reversal would produce the wrong answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once, and bit reversal always takes 8 iterations |
| Space | O(1) | Only a few integer variables are used |

With at most `100` characters, the running time is tiny. Even the brute-force approach would pass comfortably, but the direct reconstruction solution is cleaner and mathematically exact.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def reverse_bits(x):
    res = 0

    for i in range(8):
        if x & (1 << i):
            res |= (1 << (7 - i))

    return res

def solve():
    input = sys.stdin.readline

    s = input().rstrip("\n")

    prev = 0
    out = []

    for ch in s:
        cur = reverse_bits(ord(ch))
        out.append(str((prev - cur) % 256))
        prev = cur

    print("\n".join(out))

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

# provided sample
assert run("Hello, World!\n") == (
    "238\n108\n112\n0\n64\n194\n48\n26\n244\n168\n24\n16\n162\n"
), "sample 1"

# minimum size input
assert run("A\n") == "126\n", "single character"

# repeated characters
assert run("AAA\n") == "126\n0\n0\n", "same reversed value repeatedly"

# boundary ASCII values
assert run(" ~\n") == "252\n252\n", "space and tilde"

# alternating pattern
assert run("Hi\n") == "238\n124\n", "state transition correctness"

# maximum size style test
assert len(run(("A" * 100) + "\n").strip().split()) == 100, "length 100"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `A` | `126` | Single-character initialization |
| `AAA` | `126 0 0` | Correct state updates across equal characters |
| ` ~` | `252 252` | Boundary printable ASCII values |
| `Hi` | `238 124` | Dependency on previous character |
| `A` repeated 100 times | 100 outputs | Maximum input size handling |

## Edge Cases

Consider the smallest possible input:

```
A
```

The algorithm starts with:

```
prev = 0
```

The ASCII value of `'A'` is `65`.

Its 8-bit reversal is:

```
01000001 -> 10000010 = 130
```

The output becomes:

```
(0 - 130) mod 256 = 126
```

The algorithm correctly handles the special initialization rule for the first character.

Now consider repeated characters:

```
AAA
```

The reversed value of `'A'` is always `130`.

The computations are:

```
First:  (0 - 130) mod 256 = 126
Second: (130 - 130) mod 256 = 0
Third:  (130 - 130) mod 256 = 0
```

This case confirms that the algorithm updates `prev` correctly after every iteration.

Finally, consider characters whose binary form begins with zeroes:

```
A
```

Its binary form is:

```
01000001
```

If we reversed only significant bits, we would incorrectly get:

```
1000001
```

which is still `65`.

The implementation explicitly processes exactly 8 positions, so the correct reversed value `130` is obtained. This prevents silent errors on many printable ASCII characters.
