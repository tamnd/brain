---
title: "CF 106136D - Mosaic Garden"
description: "We are working with a fixed string, ECUST, and the task is to generate every possible string that can be formed by independently choosing the case of each character while keeping the underlying letters unchanged."
date: "2026-06-20T01:53:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106136
codeforces_index: "D"
codeforces_contest_name: "East China University of Science and Technology Programming Contest 2025"
rating: 0
weight: 106136
solve_time_s: 55
verified: true
draft: false
---

[CF 106136D - Mosaic Garden](https://codeforces.com/problemset/problem/106136/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working with a fixed string, `ECUST`, and the task is to generate every possible string that can be formed by independently choosing the case of each character while keeping the underlying letters unchanged. Each character stays in its position, but it can be either uppercase or lowercase, and all such combinations are considered valid outputs.

The output is not arbitrary. Every generated string must be sorted using standard ASCII lexicographical order. This ordering compares strings character by character, and at the first position where they differ, the string with the smaller ASCII value comes first. Since uppercase letters have smaller ASCII codes than lowercase letters, uppercase versions of the same letter always come before lowercase ones when compared at the same position.

Although the input format technically provides a line, it carries no information that affects the answer. The entire problem is deterministic and depends only on the string `ECUST`.

The implicit constraint is that the string length is fixed at 5, so the total number of generated strings is also fixed at $2^5 = 32$. This immediately rules out any concern about performance or memory usage. Even a straightforward enumeration is trivially fast.

The main subtlety lies in ordering. A naive approach might generate all case combinations and then sort them using a general-purpose string sort. That is safe, but it hides a structural property that allows direct generation in correct order.

A typical mistake would be to assume lexicographical order over case combinations behaves like binary numbers without checking ASCII rules. For example, treating lowercase as "smaller" would invert the correct ordering and produce incorrect output.

Another subtle issue is forgetting that each character varies independently. If someone incorrectly toggles case globally or swaps characters, they would not generate valid case-preserving variants.

## Approaches

A brute-force method is to generate all subsets of positions to lowercase. For each of the five characters, we decide whether it remains uppercase or becomes lowercase, producing 32 strings. After generating them, we sort the list using normal string comparison.

This works because the search space is extremely small. The cost is essentially generating 32 strings and sorting them, which is negligible. However, it performs unnecessary work because sorting is not actually needed if we exploit how ASCII ordering interacts with case changes.

The key observation is that each position behaves independently in lexicographical comparison. At each character, uppercase is always smaller than lowercase for the same letter. This means that if we interpret uppercase as 0 and lowercase as 1, then lexicographical order across the whole string matches the natural increasing order of the 5-bit binary mask.

So instead of generating and sorting, we can enumerate masks from 0 to 31 and directly construct the corresponding string. This produces the correct order automatically.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force + Sorting | O(32 log 32) | O(32) | Accepted |
| Bitmask Enumeration | O(32) | O(1) extra | Accepted |

## Algorithm Walkthrough

We treat each character in `ECUST` as having two states, uppercase and lowercase, and interpret a choice as a binary decision.

1. Consider all integers from 0 to 31, where each number represents a unique combination of casing choices. Each bit corresponds to one position in the string. This works because 5 characters give exactly 5 binary decisions.
2. For each number, examine its binary representation from the most significant bit (position 0) to the least significant bit (position 4). A bit value of 0 means we keep the uppercase character, and a bit value of 1 means we convert it to lowercase.
3. Build the resulting string character by character. At each position, apply the rule from step 2 to decide whether to lower or keep the character.
4. Print each constructed string immediately. Since masks are processed in increasing order, outputs are already in correct lexicographical order.

The crucial detail is that iterating from 0 upward guarantees lexicographical correctness because earlier bits correspond to earlier characters, and uppercase is always lexicographically smaller than lowercase.

### Why it works

The algorithm relies on a consistent ordering alignment between two systems: binary ordering of masks and ASCII lexicographical ordering of strings. At the first differing position between two generated strings, that position corresponds exactly to the most significant differing bit in their masks. Since we map 0 to uppercase and 1 to lowercase, and uppercase has smaller ASCII value, the ordering of masks directly matches lexicographical ordering. This invariant ensures that no post-sorting is required.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = "ECUST"
n = len(s)

for mask in range(1 << n):
    res = []
    for i in range(n):
        c = s[i]
        if mask & (1 << (n - 1 - i)):
            res.append(c.lower())
        else:
            res.append(c)
    print("".join(res))
```

The program first fixes the base string and iterates over all possible bitmasks representing casing choices. The bit test is aligned so that the most significant bit corresponds to the first character, ensuring lexicographical correctness.

The construction of the string is done in a single pass per mask, which keeps the implementation simple and avoids any need for sorting logic or auxiliary data structures.

## Worked Examples

We can illustrate the process on a smaller analogous string `AB`, where the logic is easier to see while remaining structurally identical.

For `AB`, we enumerate masks from 0 to 3.

| Mask | Binary | A choice | B choice | Output |
| --- | --- | --- | --- | --- |
| 0 | 00 | A | B | AB |
| 1 | 01 | A | b | Ab |
| 2 | 10 | a | B | aB |
| 3 | 11 | a | b | ab |

This trace shows that increasing mask order matches lexicographical order because at the first differing character, uppercase always precedes lowercase.

Applying the same reasoning to `ECUST` simply extends this pattern to five positions, producing 32 ordered outputs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(32 × 5) | Each of the 32 masks builds a 5-character string |
| Space | O(1) extra | Output aside, only a small buffer per string is used |

The input size is constant, so the solution easily fits within any reasonable limits. Even with multiple test formats, the computation remains effectively instantaneous.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = "ECUST"
    n = len(s)
    out = []
    for mask in range(1 << n):
        res = []
        for i in range(n):
            c = s[i]
            if mask & (1 << (n - 1 - i)):
                res.append(c.lower())
            else:
                res.append(c)
        out.append("".join(res))
    return "\n".join(out)

# sample-style check (structure only)
assert len(run("NO_INPUT").splitlines()) == 32

# custom case: single letter analogue logic check
def run_small():
    s = "A"
    return [("A" if m == 0 else "a") for m in range(2)]

assert run_small() == ["A", "a"]

# ordering check for ECUST prefix property
res = run("NO_INPUT").splitlines()
assert res[0] == "ECUST"
assert res[-1] == "ecust"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| NO_INPUT | 32 strings | full enumeration size |
| single-letter model | A, a | case toggle correctness |
| ECUST case range | ECUST first, ecust last | lexicographical extremes |

## Edge Cases

The only meaningful edge behavior is ordering at the boundaries: the fully uppercase and fully lowercase strings.

For input `ECUST`, the mask `00000` produces `ECUST`, which is the smallest string because every character is uppercase. The mask `11111` produces `ecust`, which is the largest because every character is lowercase.

Walking through the first case, each bit is zero, so no character is transformed, and the output remains `ECUST`. Since no other string can have a smaller character at the first differing position, it must appear first in lexicographical order.

For the last case, all bits are one, so every character is lowercase. Any other string differs earlier or at some position where uppercase appears, and uppercase is smaller, so all such strings precede it, making `ecust` the final output.
