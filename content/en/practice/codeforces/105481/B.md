---
title: "CF 105481B - \u6bd4\u5206\u5e7b\u672f"
description: "We are given a scoreboard written in the form A-B, where A represents Alex’s score and B represents the opponent’s score. Both values are single digits from 0 to 9. The system applies a “score illusion” operation that simply swaps the two values."
date: "2026-06-23T01:58:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105481
codeforces_index: "B"
codeforces_contest_name: "2024 CCPC Liaoning Provincial Contest"
rating: 0
weight: 105481
solve_time_s: 44
verified: true
draft: false
---

[CF 105481B - \u6bd4\u5206\u5e7b\u672f](https://codeforces.com/problemset/problem/105481/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a scoreboard written in the form `A-B`, where `A` represents Alex’s score and `B` represents the opponent’s score. Both values are single digits from 0 to 9.

The system applies a “score illusion” operation that simply swaps the two values. After the transformation, Alex’s score becomes what the opponent had, and the opponent’s score becomes what Alex had. The output must again be printed in the same `A-B` format, but with the swapped values.

The constraints are extremely small since each value is a single digit encoded directly in the input string. This means there is no need for parsing integers beyond reading characters or splitting the string. Any solution that runs in constant time per input is trivially sufficient.

The main subtlety is purely syntactic: correctly extracting the two numbers and preserving formatting. A careless implementation might accidentally treat the entire string as a number, or split incorrectly when formatting variations appear.

A concrete edge case is `0-0`. The correct output is still `0-0`. Another is `9-0`, which must become `0-9`. Any parsing that drops leading zeros or assumes multi-digit arithmetic would still need to preserve exact digits.

## Approaches

A brute-force interpretation would treat A and B as numbers, simulate swapping by converting them to integers, and reconstruct the string. This works correctly because swapping is independent of numeric structure, but it is unnecessary overhead for such small fixed-size input.

The real simplification comes from noticing that the input format is rigid: exactly one character, then a hyphen, then one character. There is no ambiguity, no multi-digit parsing, and no whitespace handling. The “computation” is only a character rearrangement problem.

Thus the solution reduces to reading the string and swapping the characters around the hyphen. No arithmetic is required at all.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (parse integers, swap, format) | O(1) | O(1) | Accepted |
| Direct string swap | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string `s`, which has the form `A-B`. The structure guarantees exactly three meaningful characters plus a newline.
2. Identify the first character `s[0]` as Alex’s original score and the last character `s[2]` as the opponent’s score. The middle character is always the separator `-`.
3. Construct the result by placing `s[2]`, then `-`, then `s[0]`. This directly implements the “illusion” without converting types or modifying values.
4. Output the constructed string.

### Why it works

The problem defines the transformation as a pure swap of two independent scalar values embedded in fixed positions. Since the format is invariant and each score occupies a single character position, swapping characters at positions 0 and 2 preserves all semantic meaning. There is no dependency between digits and no carry or arithmetic effect, so character permutation exactly matches the required transformation.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
print(f"{s[2]}-{s[0]}")
```

The implementation relies entirely on positional indexing. The `.strip()` ensures that newline characters do not interfere with indexing. Since the format is guaranteed to be `digit-digits`, indexing `s[0]` and `s[2]` is always safe.

A common mistake is attempting to split by `-` and forgetting to reconstruct formatting correctly. While `split('-')` also works, direct indexing is simpler and avoids intermediate string allocations.

## Worked Examples

### Example 1

Input: `2-3`

| Step | A (original) | B (original) | Action | Result |
| --- | --- | --- | --- | --- |
| 1 | 2 | 3 | Read string | "2-3" |
| 2 | 2 | 3 | Extract positions | s[0]=2, s[2]=3 |
| 3 | 2 | 3 | Swap | "3-2" |

Output: `3-2`

This confirms the operation is purely positional and independent of numeric interpretation.

### Example 2

Input: `9-0`

| Step | A (original) | B (original) | Action | Result |
| --- | --- | --- | --- | --- |
| 1 | 9 | 0 | Read string | "9-0" |
| 2 | 9 | 0 | Extract positions | s[0]=9, s[2]=0 |
| 3 | 9 | 0 | Swap | "0-9" |

Output: `0-9`

This highlights that leading zeros are preserved automatically because we never convert to integers.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only constant-time character access and formatting |
| Space | O(1) | No auxiliary data structures beyond the input string |

The solution fits easily within constraints because it performs a fixed number of operations regardless of input.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import *
    s = _sys.stdin.readline().strip()
    return f"{s[2]}-{s[0]}"

# provided samples
assert run("2-3\n") == "3-2", "sample 1"

# custom cases
assert run("0-0\n") == "0-0", "all equal"
assert run("9-0\n") == "0-9", "boundary swap"
assert run("1-9\n") == "9-1", "max digits"
assert run("5-2\n") == "2-5", "general case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0-0 | 0-0 | identical values |
| 9-0 | 0-9 | boundary digits |
| 1-9 | 9-1 | max-range swap |
| 5-2 | 2-5 | general correctness |

## Edge Cases

The input `0-0` demonstrates that swapping identical values must preserve the same string. The algorithm reads `s[0]=0` and `s[2]=0`, then constructs `0-0`, which matches expectation.

For `9-0`, the algorithm extracts `9` and `0` and outputs `0-9`. No special handling is needed because the output format is purely positional, not numeric.

Since every valid input is exactly three meaningful characters, there are no structural edge cases beyond digit identity, which the algorithm handles inherently through indexing.
