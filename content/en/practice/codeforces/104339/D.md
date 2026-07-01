---
title: "CF 104339D - base64 encoding"
description: "We are given a stream of bytes, already provided as hexadecimal values, and we need to convert that raw binary data into a Base64-encoded string using the standard alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/."
date: "2026-07-01T18:38:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104339
codeforces_index: "D"
codeforces_contest_name: "FAMCS Olympiad for scholars, Qualification (copy)"
rating: 0
weight: 104339
solve_time_s: 62
verified: true
draft: false
---

[CF 104339D - base64 encoding](https://codeforces.com/problemset/problem/104339/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a stream of bytes, already provided as hexadecimal values, and we need to convert that raw binary data into a Base64-encoded string using the standard alphabet `ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/`.

The encoding works by grouping the input bytes into chunks of three. Each group of three bytes forms a 24-bit integer. That 24-bit block is then split into four 6-bit segments, and each segment is used as an index into the Base64 alphabet to produce four characters. If the last group has fewer than three bytes, we still conceptually build the 24-bit block by padding missing bytes with zero bits, but the output is truncated and padded with `=` so that the final length becomes a multiple of 4 characters.

The output is a single continuous Base64 string representing the entire input.

The constraints allow up to 50,000 bytes. A direct per-byte or per-bit simulation is perfectly fine because the work is linear in the input size. Anything worse than O(n) would be unnecessary, since even a few million primitive operations are easily fast enough in Python.

A subtle edge case appears when the input length is not divisible by three. For example, a single byte input like `0F` must produce two Base64 characters followed by `==`, not four computed characters with incorrect interpretation of padding bits. A careless implementation often forgets to suppress extra output or mishandles padding shifting.

Another issue is byte grouping at boundaries. For instance, with two bytes, the algorithm still forms a 24-bit block by shifting in zeros, but only three Base64 characters are valid before padding. Incorrect masking or failing to distinguish “real” vs “padded” bytes leads to incorrect trailing symbols.

## Approaches

A brute-force interpretation would directly simulate bit operations for every byte, concatenating bits into a growing string or integer, then slicing it into 6-bit chunks. This works because Base64 is fundamentally a bit-packing transformation. However, building and slicing strings of bits repeatedly introduces overhead proportional to the total number of bits with a large constant factor, and naive string concatenation in loops can degrade performance significantly for 50,000 bytes.

The key observation is that Base64 operates in fixed-size blocks. Every 3 bytes independently produce 4 characters. This allows us to process input in chunks without maintaining a growing bit buffer. Instead of simulating bits explicitly, we directly compute the 24-bit integer using shifts and bitwise OR operations, then extract the four 6-bit indices using shifts.

For the final partial block, we still compute the 24-bit value in the same way, but we only emit the first 2 or 3 characters depending on whether we had 1 or 2 bytes, followed by the required padding.

This reduces the problem to a simple linear scan over the byte array with constant-time processing per block.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force bit string construction | O(n) with high constant | O(n) | Too slow in practice |
| Block-wise bit manipulation | O(n) | O(1) extra | Accepted |

## Algorithm Walkthrough

We process the input bytes in groups of three.

1. Read all bytes as integers from hexadecimal strings. This gives us direct numeric values, avoiding repeated parsing later.
2. Iterate over the byte array in steps of three. For each full group:

We construct a 24-bit integer by shifting the first byte left by 16 bits, the second by 8 bits, and adding the third as-is. This preserves their original order in a single packed value.
3. From this 24-bit integer, extract four 6-bit segments. We do this by shifting right by 18, 12, 6, and 0 bits respectively, then masking with `63` to isolate the last 6 bits. Each value indexes into the Base64 alphabet.
4. Append the four characters to the output string.
5. When fewer than three bytes remain, construct the same 24-bit buffer but treat missing bytes as zero. If only one byte remains, we generate two valid Base64 characters and append `==`. If two bytes remain, we generate three characters and append `=`.

### Why it works

The correctness comes from the fact that Base64 is a bijection between 24-bit blocks and four 6-bit symbols. Every full group of three bytes contributes exactly 24 bits, and splitting them into fixed 6-bit windows preserves the original binary structure without overlap. Padding does not alter the encoded prefix because missing bits are zero-filled consistently in both encoding definition and implementation.

## Python Solution

```python
import sys
input = sys.stdin.readline

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def encode_base64(n, data):
    out = []

    i = 0
    while i < n:
        b1 = data[i]
        i += 1

        b2 = data[i] if i < n else None
        i += 1 if i < n else 0

        b3 = data[i] if i < n else None
        i += 1 if i < n else 0

        # build 24-bit buffer
        x = b1 << 16
        if b2 is not None:
            x |= b2 << 8
        if b3 is not None:
            x |= b3

        # always compute full 4 indices
        c1 = ALPHABET[(x >> 18) & 63]
        c2 = ALPHABET[(x >> 12) & 63]
        c3 = ALPHABET[(x >> 6) & 63]
        c4 = ALPHABET[x & 63]

        if b2 is None:
            out.append(c1 + c2 + "==")
        elif b3 is None:
            out.append(c1 + c2 + c3 + "=")
        else:
            out.append(c1 + c2 + c3 + c4)

    return "".join(out)

def main():
    n = int(input().strip())
    data = list(map(lambda x: int(x, 16), input().split()))
    print(encode_base64(n, data))

if __name__ == "__main__":
    main()
```

The implementation keeps processing strictly in blocks of up to three bytes. The bit packing step using shifts ensures we never need to explicitly manage binary strings. The masking with `& 63` guarantees that each extracted segment is a valid Base64 index.

Care must be taken in handling the last block. The logic explicitly checks whether the second or third byte exists and decides padding based on that. A common mistake is to always output four characters and then append padding, which produces incorrect encodings for short final blocks.

## Worked Examples

### Example 1

Input:

```
3
43 61 74
```

| Step | Bytes | 24-bit value | Indices (6-bit chunks) | Output chunk |
| --- | --- | --- | --- | --- |
| 1 | 43 61 74 | packed full block | 16, 34, 25, 52 | Q2F0 |

This example is a full block of three bytes, so no padding occurs. The algorithm produces four characters directly.

The trace shows a clean mapping from 24-bit packing to four Base64 symbols, confirming correctness for complete blocks.

### Example 2

Input:

```
4
0F DD A4 12
```

| Step | Bytes | 24-bit value | Indices | Output chunk |
| --- | --- | --- | --- | --- |
| 1 | 0F DD A4 | full block | 3, 61, 40, 36 | D92k |
| 2 | 12 | partial block | 4, 18, 0, 0 | Eg== |

The first group behaves like a normal full encoding. The second group only has one byte, so the remaining two bytes are treated as zero padding. Only the first two Base64 characters are meaningful, and the output ends with `==`.

This trace highlights how padding suppresses excess encoded characters while still computing the full 6-bit decomposition internally.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each byte is processed exactly once in constant-time bit operations |
| Space | O(n) | Output string stores a constant expansion of input size |

The algorithm scales linearly with input size, which is optimal for a transformation that must read every byte at least once. With 50,000 bytes, the total operations remain well within Python’s limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    return io.StringIO(sys.stdout.getvalue() if hasattr(sys.stdout, "getvalue") else "")

# helper redefinition for clean runs
def run(inp: str) -> str:
    import sys, io
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    try:
        main()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = backup_stdin
        sys.stdout = backup_stdout

assert run("3\n43 61 74\n") == "Q2F0"
assert run("4\n0F DD A4 12\n") == "D92kEg=="

# single byte
assert run("1\n00\n") == "AA=="

# two bytes
assert run("2\nFF FF\n") == "//8="

# all equal pattern
assert run("3\n00 00 00\n") == "AAAA"

# maximum small repeat pattern
assert run("6\n41 42 43 44 45 46\n") == "QUJDREVG"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 byte zero | AA== | single-byte padding |
| 2 bytes FF FF | //8= | two-byte boundary case |
| 3 zero bytes | AAAA | full block correctness |
| ABCDEF bytes | QUJDREVG | multiple full blocks |

## Edge Cases

A single-byte input like `00` exercises the padding logic directly. The algorithm builds a 24-bit block `0x000000`, extracts indices all equal to zero, producing `AAAA`, and then truncates to `AA==`. This confirms that suppression of extra characters happens after extraction, not before it.

A two-byte input like `FF FF` produces a full 24-bit value `0xFFFF00`. The first three Base64 characters are valid, but the fourth is discarded and replaced with `=`. The shift-and-mask approach ensures we still compute the correct intermediate value without special-casing the bit math, only the output length differs.
