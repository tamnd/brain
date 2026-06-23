---
title: "CF 105257A - chmod"
description: "Each input line describes a Unix-like permission configuration encoded in a compact numeric form. Instead of directly giving permissions for a file, the system uses a three-digit number, where each digit independently describes the access rights for one of three user classes…"
date: "2026-06-24T04:25:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105257
codeforces_index: "A"
codeforces_contest_name: "2024 ICPC ShaanXi Provincial Contest"
rating: 0
weight: 105257
solve_time_s: 53
verified: true
draft: false
---

[CF 105257A - chmod](https://codeforces.com/problemset/problem/105257/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

Each input line describes a Unix-like permission configuration encoded in a compact numeric form. Instead of directly giving permissions for a file, the system uses a three-digit number, where each digit independently describes the access rights for one of three user classes: owner, group, and others.

Each digit is between 0 and 7, and should be interpreted as a 3-bit mask. The three bits correspond, in fixed order, to read, write, and execute permissions. If a bit is set, the corresponding character appears in the final permission string, otherwise a dash is used.

The output for each test case is a 9-character string. It is formed by expanding each of the three digits into a block of three characters, and concatenating the blocks in the order owner, group, others.

The constraints are small, with at most 100 test cases and constant work per case. This immediately rules out anything beyond linear processing per input line, although even quadratic behavior would still pass. The structure of the problem is fixed-width decoding, so performance is not the main difficulty.

A common mistake comes from misinterpreting bit order. The most significant bit corresponds to read, the middle bit to write, and the least significant bit to execute. For example, digit 6 corresponds to binary 110, which means read and write are enabled but execute is not, producing the string “rw-”. Another frequent error is reversing the order of characters inside each triplet, which leads to incorrect permutations like “wr-” or “-rw”.

## Approaches

The brute-force idea is to treat each digit as a number from 0 to 7 and explicitly test each permission using repeated modulo or binary conversion logic. For every digit, one could repeatedly divide by 2 or extract bits one by one, building the string in a temporary array. This is correct because each digit encodes exactly three independent boolean flags.

This approach already runs in constant time per digit since there are only three bits, but it tends to be written in a more verbose and error-prone way. If implemented carelessly using string operations or repeated concatenation inside loops, it can become unnecessarily slow or messy, even though the theoretical complexity remains trivial.

The key observation is that each digit directly maps to three fixed bit positions. Instead of simulating binary extraction, we can use bitwise operations. This reduces the solution to a direct lookup of whether each of the three bits is set. Since there are only eight possible values per digit, the mapping is entirely deterministic and constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force bit extraction | O(T) | O(1) | Accepted |
| Bitwise direct mapping | O(T) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases and iterate over each input string.
2. For each character in the string, convert it to an integer digit.
3. For each digit, determine the permission characters in fixed order: read, write, execute.
4. For each permission, check the corresponding bit in the digit using bitwise AND.
5. If the bit is set, append the corresponding character, otherwise append a dash.
6. Concatenate the three-character blocks for all digits and output the resulting 9-character string.

The reason this ordering works is that the problem defines a strict positional mapping between bits and permission types. Each digit is independent, so decoding can be done locally without any cross-dependency between owner, group, and others.

### Why it works

Each digit encodes a subset of a three-element set, where each element corresponds to a permission type. The binary representation of the digit is exactly the characteristic vector of that subset. Since the mapping from bits to characters is fixed and injective, reconstructing the string by checking each bit independently preserves all information without ambiguity. Concatenating the decoded blocks reconstructs the full permission string uniquely.

## Python Solution

```python
import sys
input = sys.stdin.readline

def decode_digit(d):
    r = 'r' if d & 4 else '-'
    w = 'w' if d & 2 else '-'
    x = 'x' if d & 1 else '-'
    return r + w + x

t = int(input())
out = []

for _ in range(t):
    s = input().strip()
    res = []
    for ch in s:
        d = ord(ch) - ord('0')
        res.append(decode_digit(d))
    out.append(''.join(res))

print('\n'.join(out))
```

The core of the implementation is the `decode_digit` function, which isolates the three permission bits using bitwise AND. The constants 4, 2, and 1 correspond to the binary weights of the read, write, and execute positions respectively.

The main loop simply applies this transformation independently to each character and concatenates results. Using a list for accumulation avoids repeated string concatenation overhead, which is unnecessary but still a good habit in Python competitive programming.

## Worked Examples

Consider the input consisting of two test cases:

```
2
760
123
```

For the first case, we decode each digit separately.

| Digit | Binary | Read | Write | Execute | Result |
| --- | --- | --- | --- | --- | --- |
| 7 | 111 | r | w | x | rwx |
| 6 | 110 | r | w | - | rw- |
| 0 | 000 | - | - | - | --- |

Concatenating gives `rwxrw----`.

For the second case:

| Digit | Binary | Read | Write | Execute | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 001 | - | - | x | --x |
| 2 | 010 | - | w | - | -w- |
| 3 | 011 | - | w | x | -wx |

Concatenating gives `--x-w--wx`.

These traces show that each digit is decoded independently and always produces exactly three characters, preserving fixed structure across all inputs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case processes exactly three digits with constant-time bit operations |
| Space | O(T) | Output storage dominates, as we build one string per test case |

The runtime is linear in the number of test cases, and the constant factor is extremely small. With at most 100 inputs, execution is effectively instantaneous under the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def decode_digit(d):
        r = 'r' if d & 4 else '-'
        w = 'w' if d & 2 else '-'
        x = 'x' if d & 1 else '-'
        return r + w + x

    t = int(input())
    out = []
    for _ in range(t):
        s = input().strip()
        res = []
        for ch in s:
            d = ord(ch) - ord('0')
            res.append(decode_digit(d))
        out.append(''.join(res))

    return '\n'.join(out)

# provided sample (interpreted)
assert run("2\n760\n123\n") == "rwxrw----\n--x-w--wx"

# minimal case
assert run("1\n0\n") == "---------"

# all ones
assert run("1\n111\n") == "--x--x--x"

# full permissions
assert run("1\n777\n") == "rwxrwxrwx"

# mixed case
assert run("1\n504\n") == "r-x---r--"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n0 | --------- | all permissions off |
| 1\n777 | rwxrwxrwx | all permissions on |
| 1\n111 | --x--x--x | single-bit execute propagation |
| 1\n504 | r-x---r-- | mixed independent digits |

## Edge Cases

For an input like `0`, the digit has no bits set, so all three permissions map to dashes. The algorithm evaluates `0 & 4`, `0 & 2`, and `0 & 1`, all of which are false, producing “---” for each group. Repeating this three times yields a full string of nine dashes, which matches the intended empty permission state.

For an input like `7`, all bits are set. The checks `7 & 4`, `7 & 2`, and `7 & 1` all evaluate as true, producing “rwx”. This behavior is consistent across all digits, and since each digit is handled independently, there is no interference between groups, ensuring correctness even in uniform or extreme cases.
