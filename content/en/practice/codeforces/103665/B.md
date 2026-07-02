---
title: "CF 103665B - \u041f\u0435\u0440\u0435\u0432\u043e\u0434\u0447\u0438\u043a"
description: "We are given a word that belongs to exactly one of two alien alphabets. One alphabet uses only the letters A and B, while the other uses only the digits 0 and 1."
date: "2026-07-03T02:06:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103665
codeforces_index: "B"
codeforces_contest_name: "\u0422\u0443\u0440\u043d\u0438\u0440 \u0410\u0440\u0445\u0438\u043c\u0435\u0434\u0430 2018"
rating: 0
weight: 103665
solve_time_s: 43
verified: true
draft: false
---

[CF 103665B - \u041f\u0435\u0440\u0435\u0432\u043e\u0434\u0447\u0438\u043a](https://codeforces.com/problemset/problem/103665/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a word that belongs to exactly one of two alien alphabets. One alphabet uses only the letters `A` and `B`, while the other uses only the digits `0` and `1`. The task is to determine which alphabet the input word belongs to, and then convert it into the other alphabet using a fixed character-by-character mapping.

The mapping is completely deterministic. Every `A` becomes `0`, every `B` becomes `1`, and conversely every `0` becomes `A`, every `1` becomes `B`. There is no structure beyond independent character substitution, so the word length stays unchanged and each position can be processed without context.

The input size constraint is small, with the word length up to 100 characters. This immediately implies that even the most straightforward linear scan is trivially fast, since at most we perform 100 character checks and replacements. Anything up to O(n²) would still be fine, but there is no reason to go beyond O(n).

Edge cases are minimal, but there are a few subtle ones worth stating explicitly. The word length could be 1, for example input `A`, which should become `0`. Similarly, `1` should become `B`. Another case is when the entire string is already in binary form, such as `0101`, which must be converted fully to letters. A careless implementation might incorrectly assume one alphabet without checking, but the guarantee says the input belongs entirely to one alphabet, so a single scan is enough to decide.

## Approaches

A brute-force interpretation would treat this as a general translation problem: first attempt to detect the alphabet, then repeatedly apply replacements or build intermediate strings while scanning multiple times. One could imagine replacing characters using repeated string operations or using nested loops that repeatedly scan and replace characters until no changes remain. This would still work because the transformation is simple and local, but it is unnecessary overhead.

The key observation is that the input is guaranteed to be homogeneous. Either all characters are from `{A, B}` or all are from `{0, 1}`. That means we do not need any complex detection or validation logic beyond inspecting characters as we scan. A single pass is sufficient: we can map each character directly to its counterpart and construct the result in one sweep.

This reduces the problem to a direct character substitution problem, where each position is transformed independently in O(1), giving a total O(n) solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (repeated scanning/rebuilding) | O(n²) | O(n) | Accepted but unnecessary |
| Optimal single-pass mapping | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`, which tells us how many characters are in the word. We do not actually need it for processing, but it ensures input consistency.
2. Read the string `s` of length `n`.
3. Inspect the first character of the string to determine the direction of translation. If it is `A` or `B`, then we are translating from the letter alphabet to binary. Otherwise, it must be `0` or `1`, meaning we translate from binary to letters. This works because the problem guarantees the string is fully consistent.
4. Create an empty list or buffer to build the output efficiently. Using a list avoids repeated string concatenation, which would be slower in Python.
5. Iterate through each character in the string. For each character, apply the mapping:

If we are in letter-to-binary mode, replace `A → 0` and `B → 1`.

If we are in binary-to-letter mode, replace `0 → A` and `1 → B`.

Append the converted character to the output buffer.
6. Join the buffer into a final string and print it.

### Why it works

Each character is independent of all others, and the translation rule is a bijection between the two alphabets. This means every valid input string maps to exactly one valid output string with no ambiguity. Since we determine the mode once and apply a fixed per-character transformation, the algorithm preserves correctness position by position. No character ever depends on context, so there is no opportunity for cascading errors or state corruption.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    s = input().strip()

    # detect alphabet from first character
    if s[0] in "AB":
        # Dobos -> Femos
        mp = {'A': '0', 'B': '1'}
    else:
        # Femos -> Dobos
        mp = {'0': 'A', '1': 'B'}

    res = []
    for c in s:
        res.append(mp[c])

    print("".join(res))

if __name__ == "__main__":
    solve()
```

The implementation follows the algorithm exactly. The dictionary `mp` encodes the translation rule, so each character lookup is constant time. The result is accumulated in a list to avoid quadratic behavior from string concatenation. The decision about direction is made once based on the first character, which is safe due to the guarantee that the entire string belongs to one alphabet.

## Worked Examples

### Example 1

Input:

```
n = 5
s = ABAAB
```

We first detect that `A` is a letter, so we are translating letters to binary.

| Step | Character | Mapping | Output so far |
| --- | --- | --- | --- |
| 1 | A | 0 | 0 |
| 2 | B | 1 | 01 |
| 3 | A | 0 | 010 |
| 4 | A | 0 | 0100 |
| 5 | B | 1 | 01001 |

Output:

```
01001
```

This confirms that each character is independently mapped and no structural transformation is needed.

### Example 2

Input:

```
n = 2
s = 11
```

We detect digits, so we translate binary to letters.

| Step | Character | Mapping | Output so far |
| --- | --- | --- | --- |
| 1 | 1 | B | B |
| 2 | 1 | B | BB |

Output:

```
BB
```

This shows the reverse direction behaves symmetrically and uses the same per-character logic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once with O(1) lookup |
| Space | O(n) | Output string stored explicitly |

The constraint n ≤ 100 makes this complexity far below any practical limit. Even with overhead from Python I/O, the solution runs instantly.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    input = sys.stdin.readline

    n = int(input().strip())
    s = input().strip()

    if s[0] in "AB":
        mp = {'A': '0', 'B': '1'}
    else:
        mp = {'0': 'A', '1': 'B'}

    return "".join(mp[c] for c in s)

# provided samples
assert run("5\nABAAB\n") == "01001"
assert run("2\n11\n") == "BB"

# custom cases
assert run("1\nA\n") == "0"
assert run("1\n1\n") == "B"
assert run("4\nABAB\n") == "0101"
assert run("4\n0101\n") == "ABAB"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 A` | `0` | minimum length, letter to binary |
| `1 1` | `B` | minimum length, binary to letter |
| `ABAB` | `0101` | alternating pattern consistency |
| `0101` | `ABAB` | reverse mapping consistency |

## Edge Cases

For single-character inputs, the algorithm still correctly identifies the alphabet from that one character and applies the mapping once. For example, input `A` sets the mapping `{A → 0}`, and the loop runs once producing `0`.

For binary single-character input `1`, the mapping is `{1 → B}`, and the output is `B`. There is no ambiguity because the detection step relies only on membership in the fixed alphabets, and those alphabets are disjoint.

For alternating strings like `ABAB`, the algorithm does not assume structure, it simply applies the mapping per index. Each position is independent, so no interaction between positions affects correctness.
