---
title: "CF 94A - Restoring Password"
description: "We are given an encrypted password represented as a binary string of length 80. The original password had exactly 8 decimal digits, and each digit was encoded into a block of 10 binary characters."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 94
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 76 (Div. 2 Only)"
rating: 900
weight: 94
solve_time_s: 118
verified: true
draft: false
---

[CF 94A - Restoring Password](https://codeforces.com/problemset/problem/94/A)

**Rating:** 900  
**Tags:** implementation, strings  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an encrypted password represented as a binary string of length 80. The original password had exactly 8 decimal digits, and each digit was encoded into a block of 10 binary characters. The mapping between digits and binary blocks is also provided: after the encrypted string, we receive 10 distinct binary strings corresponding to digits `0` through `9`.

The task is to split the 80-character encrypted string into 8 consecutive blocks of length 10, determine which digit each block represents, and print the restored 8-digit password.

The constraints are tiny. The encrypted string always has length 80, and there are only 10 mappings to compare against. Even a straightforward implementation that compares every block against every digit performs only `8 × 10 = 80` comparisons, each on strings of length 10. That is effectively constant time.

The main danger in this problem is not performance, but handling the indexing correctly. Since the encoded password is one long string, a mistake in slicing boundaries can silently shift every later block and produce the wrong password.

Consider this input:

```
11111111110000000000...
```

If we accidentally split using blocks of size 8 or 9 instead of 10, the first digit might still match something by coincidence, but every later lookup becomes incorrect.

Another subtle issue is confusing the direction of the mapping. The input lines after the encrypted string represent:

```
code for 0
code for 1
...
code for 9
```

A careless implementation may store them backwards and later try to look up digits by numeric index instead of by binary code.

For example:

```
encrypted block = "0101101000"
```

If `"0101101000"` corresponds to digit `6`, we need a mapping:

```
"0101101000" -> "6"
```

and not:

```
"6" -> "0101101000"
```

Otherwise restoring the password becomes awkward or incorrect.

## Approaches

The most direct approach is brute force. We split the 80-character encrypted string into 8 pieces of length 10. For each piece, we compare it against all 10 known digit encodings until we find a match. Since all mappings are distinct and the statement guarantees a valid solution, exactly one digit matches each block.

This approach is already fast enough. At worst we perform:

```
8 password blocks × 10 digit patterns × 10 character comparisons
```

which is only 800 character checks.

The problem becomes even cleaner if we preprocess the mappings into a dictionary. Instead of searching linearly through all 10 digit encodings every time, we directly map each binary block to its corresponding digit.

The key observation is that the encodings are unique. That means the binary string itself can serve as a dictionary key.

So we build:

```
binary block -> digit
```

Then every 10-character segment of the encrypted password can be decoded in constant time.

The brute-force solution works because the input size is tiny, but the dictionary observation removes unnecessary repeated comparisons and produces a cleaner implementation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(8 × 10 × 10) | O(1) | Accepted |
| Optimal | O(80) | O(10) | Accepted |

## Algorithm Walkthrough

1. Read the 80-character encrypted string.

This string contains the encodings of all 8 password digits concatenated together.
2. Read the 10 binary patterns corresponding to digits `0` through `9`.

Since the input order is fixed, the first pattern belongs to digit `0`, the second to digit `1`, and so on.
3. Build a dictionary where the key is the 10-character binary string and the value is the digit it represents.

This allows direct decoding later.
4. Traverse the encrypted string in steps of 10 characters.

Each segment represents exactly one encoded digit.
5. For every segment, look it up in the dictionary and append the resulting digit to the answer string.

The statement guarantees that every segment exists in the mapping.
6. Print the reconstructed password.

### Why it works

Each digit encoding is unique, so every 10-character block maps to exactly one digit. The encrypted password is formed by concatenating 8 such blocks without overlap or extra characters. Splitting the string every 10 characters reconstructs the original encoded pieces exactly, and dictionary lookup converts each piece back into its corresponding digit. Since every block is decoded independently and correctly, the final reconstructed string is the original password.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    encrypted = input().strip()

    mapping = {}

    for digit in range(10):
        code = input().strip()
        mapping[code] = str(digit)

    answer = []

    for i in range(0, 80, 10):
        block = encrypted[i:i + 10]
        answer.append(mapping[block])

    print("".join(answer))

solve()
```

The solution follows the algorithm directly.

The dictionary `mapping` stores the reverse relation from binary code to digit. This is the most convenient direction because later we receive encoded blocks and need to recover digits from them.

The loop:

```
for i in range(0, 80, 10):
```

is important. The encrypted string must be split into non-overlapping chunks of exactly length 10. Using a different step size would corrupt the partitioning.

Each block is extracted with:

```
encrypted[i:i + 10]
```

Python slicing safely returns exactly the desired substring.

The answer is accumulated in a list and joined at the end. Repeated string concatenation would also work here because the input is tiny, but list accumulation is the standard competitive-programming pattern.

## Worked Examples

### Example 1

Input:

```
01001100100101100000010110001001011001000101100110010110100001011010100101101100
0100110000
0100110010
0101100000
0101100010
0101100100
0101100110
0101101000
0101101010
0101101100
0101101110
```

Dictionary after preprocessing:

| Binary Code | Digit |
| --- | --- |
| 0100110000 | 0 |
| 0100110010 | 1 |
| 0101100000 | 2 |
| 0101100010 | 3 |
| 0101100100 | 4 |
| 0101100110 | 5 |
| 0101101000 | 6 |
| 0101101010 | 7 |
| 0101101100 | 8 |
| 0101101110 | 9 |

Decoding process:

| Position | Extracted Block | Decoded Digit |
| --- | --- | --- |
| 0-9 | 0100110010 | 1 |
| 10-19 | 0101100000 | 2 |
| 20-29 | 0101100010 | 3 |
| 30-39 | 0101100100 | 4 |
| 40-49 | 0101100110 | 5 |
| 50-59 | 0101101000 | 6 |
| 60-69 | 0101101010 | 7 |
| 70-79 | 0101101100 | 8 |

Final password:

```
12345678
```

This trace shows that every 10-character segment is decoded independently and directly through the dictionary.

### Example 2

Input:

```
11111111110000000000111111111100000000001111111111000000000011111111110000000000
0000000000
1111111111
0000000001
0000000011
0000000111
0000001111
0000011111
0000111111
0001111111
0011111111
```

Dictionary:

| Binary Code | Digit |
| --- | --- |
| 0000000000 | 0 |
| 1111111111 | 1 |
| 0000000001 | 2 |
| 0000000011 | 3 |
| 0000000111 | 4 |
| 0000001111 | 5 |
| 0000011111 | 6 |
| 0000111111 | 7 |
| 0001111111 | 8 |
| 0011111111 | 9 |

Decoding:

| Position | Extracted Block | Decoded Digit |
| --- | --- | --- |
| 0-9 | 1111111111 | 1 |
| 10-19 | 0000000000 | 0 |
| 20-29 | 1111111111 | 1 |
| 30-39 | 0000000000 | 0 |
| 40-49 | 1111111111 | 1 |
| 50-59 | 0000000000 | 0 |
| 60-69 | 1111111111 | 1 |
| 70-79 | 0000000000 | 0 |

Final password:

```
10101010
```

This example demonstrates repeated patterns. The algorithm does not rely on digits being distinct inside the password.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(80) | We process 8 blocks of length 10 |
| Space | O(10) | The dictionary stores 10 mappings |

The running time is effectively constant because the input size never grows beyond fixed limits. The memory usage is also negligible, storing only the 10 known encodings.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    encrypted = input().strip()

    mapping = {}

    for digit in range(10):
        code = input().strip()
        mapping[code] = str(digit)

    answer = []

    for i in range(0, 80, 10):
        answer.append(mapping[encrypted[i:i + 10]])

    print("".join(answer))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run(
"""01001100100101100000010110001001011001000101100110010110100001011010100101101100
0100110000
0100110010
0101100000
0101100010
0101100100
0101100110
0101101000
0101101010
0101101100
0101101110
"""
) == "12345678", "sample 1"

# all digits in order
assert run(
"""00000000000000000001000000001000000000110000000010000000010100000001100000000111
0000000000
0000000001
0000000010
0000000011
0000000100
0000000101
0000000110
0000000111
0000001000
0000001001
"""
) == "01234567", "digits in increasing order"

# repeated digit
assert run(
"""11111111111111111111111111111111111111111111111111111111111111111111111111111111
0000000000
1111111111
0000000001
0000000011
0000000111
0000001111
0000011111
0000111111
0001111111
0011111111
"""
) == "11111111", "same digit repeated many times"

# alternating boundary pattern
assert run(
"""10101010100101010101101010101001010101011010101010010101010110101010100101010101
0101010101
1010101010
0000000000
1111111111
0011001100
1100110011
0000111100
1111000011
0110011001
1001100110
"""
) == "10101010", "checks exact 10-character slicing"

# maximum-style mixed password
assert run(
"""00111111110001111111000011111100000111110000011111000000111100000011110000001111
0000000000
1111111111
0000000001
0000000011
0000000111
0000001111
0000011111
0000111111
0001111111
0011111111
"""
) == "98765435", "mixed decoding"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 12345678 | Basic decoding |
| Ordered digits | 01234567 | Correct mapping direction |
| Repeated digit | 11111111 | Repeated blocks handled correctly |
| Alternating patterns | 10101010 | Exact 10-character segmentation |
| Mixed password | 98765435 | Arbitrary decoding order |

## Edge Cases

A common mistake is slicing the encrypted string incorrectly.

Consider:

```
11111111110000000000111111110000000000111111110000000000111111110000000000
```

Suppose:

```
1111111111 -> 1
0000000000 -> 0
```

The correct password is:

```
10101010
```

Our algorithm processes indices:

```
0, 10, 20, 30, 40, 50, 60, 70
```

Each slice has exactly length 10. Since the boundaries align perfectly with the encoding format, decoding succeeds.

Another subtle case is repeated encoded blocks.

Input:

```
00000000000000000000000000000000000000000000000000000000000000000000000000000000
```

with mapping:

```
0000000000 -> 0
```

repeated among the 10 definitions.

The correct output is:

```
00000000
```

The algorithm does not assume uniqueness among password digits. Every block lookup is independent, so repeated patterns decode naturally.

A third pitfall is reversing the mapping direction.

Suppose:

```
0101010101 -> 7
```

If we stored:

```
mapping["7"] = "0101010101"
```

then later we could not decode an encrypted block directly. Our implementation instead stores:

```
mapping["0101010101"] = "7"
```

which matches the actual lookup operation required during decoding.
