---
title: "CF 133B - Unary"
description: "We are given a short Brainfuck program consisting of characters like +, -, , <, and so on. Each command corresponds to a fixed 4-bit binary string. After replacing every character with its binary code, we concatenate all those 4-bit chunks into one long binary number."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 133
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 96 (Div. 2)"
rating: 1200
weight: 133
solve_time_s: 90
verified: true
draft: false
---

[CF 133B - Unary](https://codeforces.com/problemset/problem/133/B)

**Rating:** 1200  
**Tags:** implementation  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a short Brainfuck program consisting of characters like `+`, `-`, `>`, `<`, and so on. Each command corresponds to a fixed 4-bit binary string. After replacing every character with its binary code, we concatenate all those 4-bit chunks into one long binary number.

The task is to interpret that binary string as a base-2 integer and print its value modulo `1000003`.

The wording about unary representation can look distracting at first. The size of the unary representation of a number is just the number itself, because unary writes a number `n` using `n` copies of `1`. So we do not actually need to construct any unary string. We only need the decimal value of the binary number.

The input length is at most 100 characters. Every character contributes exactly 4 binary digits, so the final binary number has at most 400 bits. Languages like Python can technically store such integers directly, but the problem explicitly asks for the result modulo `1000003`, so modular arithmetic is the cleanest approach.

A naive implementation mistake is trying to build the huge binary string and convert it afterward. That still works for these constraints, but it misses the core observation that the number can be built incrementally exactly like base conversion.

Another common mistake is misunderstanding what "size of the unary program" means. Consider the input:

```
,.
```

The mapping becomes:

```
, -> 1101
. -> 1100
```

The concatenated binary number is:

```
11011100
```

That equals `220` in decimal, so the answer is `220`, not the length of the binary string and not the number of unary digits explicitly written out.

A subtler edge case appears when the binary representation begins with `1` and contains many zeros afterward. For example:

```
>
```

maps to:

```
1000
```

which equals `8`. A careless implementation that strips leading zeros incorrectly or treats chunks independently could produce the wrong value.

Another easy bug comes from forgetting modular reduction during construction. A 400-bit integer still fits in Python, but in languages with fixed-width integers this would overflow quickly. Using modulo after every step avoids that issue cleanly.

## Approaches

The brute-force approach follows the statement literally. We create a dictionary from Brainfuck commands to 4-bit strings, concatenate all binary chunks into one large binary string, then convert that binary string into a decimal integer.

For a maximum input length of 100, the binary string length is only 400, so even direct conversion is fast enough. The complexity is linear in the number of produced bits.

The more interesting approach avoids ever storing the whole binary number. Suppose we already processed some prefix and its numeric value is `x`. When we append another 4-bit block `b`, the new value becomes:

```
x * 16 + value(b)
```

because appending 4 binary digits is the same as shifting left by 4 bits, which multiplies by `2^4 = 16`.

This transforms the problem into standard positional-number construction. We scan the program from left to right, repeatedly multiplying the current answer by 16 and adding the numeric value of the next command.

Since the final answer is needed modulo `1000003`, we can take modulo after every operation:

```
ans = (ans * 16 + value) % MOD
```

This keeps the numbers small throughout the computation.

The brute-force works because the total input is tiny, but the incremental method is cleaner, uses constant extra memory, and directly mirrors how binary numbers are formed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(n) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Create a mapping from each Brainfuck command to its decimal value after binary conversion.

For example, `">"` maps to binary `1000`, which equals decimal `8`. Similarly, `"["` maps to `1110`, which equals `14`.
2. Initialize `ans = 0`.

This variable stores the value of the binary number formed so far.
3. Process the input string from left to right.

Each command contributes exactly 4 binary digits.
4. For each character `c`, update:

```
ans = (ans * 16 + value[c]) % 1000003
```

Multiplying by 16 shifts the current binary number left by 4 bits. Adding `value[c]` appends the new 4-bit block.
5. After processing all characters, print `ans`.

### Why it works

After processing the first `k` commands, `ans` equals the decimal value of the concatenation of their corresponding 4-bit binary codes, taken modulo `1000003`.

Initially, before processing anything, the binary string is empty and its value is `0`, so the invariant holds.

When a new 4-bit block is appended, the existing binary number shifts left by 4 positions, which multiplies it by 16. Adding the value of the new block produces exactly the numeric value of the extended binary string. Since modular arithmetic preserves addition and multiplication, taking modulo after every update keeps the invariant true.

At the end, all commands have been processed, so `ans` is exactly the required result modulo `1000003`.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000003

values = {
    '>': 8,   # 1000
    '<': 9,   # 1001
    '+': 10,  # 1010
    '-': 11,  # 1011
    '.': 12,  # 1100
    ',': 13,  # 1101
    '[': 14,  # 1110
    ']': 15   # 1111
}

def solve():
    s = input().strip()

    ans = 0

    for ch in s:
        ans = (ans * 16 + values[ch]) % MOD

    print(ans)

solve()
```

The dictionary stores the decimal value of each 4-bit code instead of the binary string itself. This avoids repeated binary parsing.

The core update:

```
ans = (ans * 16 + values[ch]) % MOD
```

matches the mathematical construction exactly. Multiplying by 16 shifts the existing binary number by 4 bits, and adding the new value appends the next command block.

Applying modulo during every iteration keeps the intermediate values small. Python could handle the full integer anyway, but this pattern is safer and directly matches the problem requirement.

Using `strip()` is important because `input()` includes the trailing newline character. Without removing it, dictionary lookup would fail on `'\n'`.

## Worked Examples

### Example 1

Input:

```
,.
```

Mappings:

```
, -> 1101 -> 13
. -> 1100 -> 12
```

| Step | Character | Value | Previous ans | New ans |
| --- | --- | --- | --- | --- |
| 1 | `,` | 13 | 0 | 13 |
| 2 | `.` | 12 | 13 | 220 |

The final answer is `220`.

This trace shows how appending a 4-bit block corresponds to multiplying by 16. After processing `,`, we have binary `1101`. Appending `1100` produces `11011100`, which equals `13 * 16 + 12 = 220`.

### Example 2

Input:

```
[]
```

Mappings:

```
[ -> 1110 -> 14
] -> 1111 -> 15
```

| Step | Character | Value | Previous ans | New ans |
| --- | --- | --- | --- | --- |
| 1 | `[` | 14 | 0 | 14 |
| 2 | `]` | 15 | 14 | 239 |

The final binary number is:

```
11101111
```

which equals `239`.

This example demonstrates that the algorithm works uniformly for every command. The meaning of the Brainfuck operations never matters, only their assigned binary codes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once |
| Space | O(1) | Only a few variables and a fixed-size dictionary are stored |

With at most 100 characters, the running time is tiny. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

MOD = 1000003

values = {
    '>': 8,
    '<': 9,
    '+': 10,
    '-': 11,
    '.': 12,
    ',': 13,
    '[': 14,
    ']': 15
}

def solve():
    s = input().strip()

    ans = 0

    for ch in s:
        ans = (ans * 16 + values[ch]) % MOD

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    return sys.stdout.getvalue().strip()

# provided sample
assert run(",.\n") == "220", "sample 1"

# minimum size input
assert run(">\n") == "8", "single character"

# another single character
assert run("]\n") == "15", "maximum 4-bit value"

# two-character construction
assert run("[]\n") == "239", "binary concatenation"

# long repeated input
expected = 0
for _ in range(100):
    expected = (expected * 16 + 10) % MOD
assert run("+" * 100 + "\n") == str(expected), "maximum length"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `,.` | `220` | Provided sample |
| `>` | `8` | Minimum-size input |
| `]` | `15` | Largest single block |
| `[]` | `239` | Correct binary concatenation |
| `++++...` (100 times) | Computed modulo result | Maximum input length and modular updates |

## Edge Cases

Consider the smallest possible input:

```
>
```

The mapping is:

```
1000
```

which equals `8`.

The algorithm starts with `ans = 0` and performs:

```
ans = 0 * 16 + 8 = 8
```

The final output is correct.

Now consider a case with the largest possible 4-bit value:

```
]
```

Its binary code is:

```
1111
```

which equals `15`.

The algorithm computes:

```
ans = 0 * 16 + 15 = 15
```

No special handling is needed for values near the upper end of the mapping.

Finally, consider a long input such as 100 copies of `+`. Each `+` contributes binary `1010`, or decimal `10`. The intermediate number grows extremely quickly. A solution that stores everything in a fixed-width integer would overflow. Our implementation applies modulo after every update:

```
ans = (ans * 16 + 10) % 1000003
```

so the value always remains below `1000003`, regardless of input length.
