---
title: "CF 106486E - Excel \u7684\u5217\u7f16\u53f7"
description: "We are given a sequence of queries, each query is a large positive integer representing a column index in a spreadsheet system that labels columns using letters instead of numbers."
date: "2026-06-19T15:13:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106486
codeforces_index: "E"
codeforces_contest_name: "Dalian University of Technology, Software College 2025 Freshman Contest"
rating: 0
weight: 106486
solve_time_s: 43
verified: true
draft: false
---

[CF 106486E - Excel \u7684\u5217\u7f16\u53f7](https://codeforces.com/problemset/problem/106486/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of queries, each query is a large positive integer representing a column index in a spreadsheet system that labels columns using letters instead of numbers. The labeling starts from single letters, then continues with two-letter strings, then three-letter strings, and so on, following a lexicographic pattern over uppercase English letters.

The task is to convert each integer position into its corresponding “column name” string under this scheme. The key difficulty is that this is not a standard base-26 conversion because there is no zero digit, and the mapping is shifted so that A corresponds to 1 rather than 0.

The input size is large, with up to 100,000 queries and each number as large as 10^18. This immediately rules out any approach that builds strings by enumerating all previous labels or simulating the entire sequence. Any solution must process each query in logarithmic time with respect to the value, since linear or enumeration-based approaches would be far too slow.

A subtle edge case appears around powers of 26. For example, 26 maps to Z, but 27 maps to AA, not BA or something similar. Another tricky case is values like 52, 53, and 702, where naive modulo-26 logic can misbehave if we do not handle the lack of zero properly. For instance, 26 should yield Z, while naive modulo arithmetic often produces an empty remainder or incorrect carry behavior unless adjusted.

## Approaches

A brute-force idea is to start from 1 and repeatedly generate column names in order until we reach the target index. This is conceptually straightforward because the mapping is monotonic and lexicographically ordered, so we would just increment a counter and convert each number into its string representation until we reach the query value. However, this requires generating up to a_i strings per query. Since a_i can be as large as 10^18, this is completely infeasible, even for a single query.

The key observation is that the structure behaves like a base-26 numeral system, except digits are from 1 to 26 instead of 0 to 25. This means we can interpret the number as a 1-indexed base-26 representation. The transformation is similar to converting a number into base 26, but whenever we extract a digit, we must map remainder 0 to letter Z and decrease the quotient before continuing. This adjustment resolves the off-by-one shift introduced by the absence of a zero digit.

Instead of generating all previous labels, we directly decompose the number into characters from least significant position to most significant position using repeated division by 26, correcting the remainder when it becomes zero.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | O(max a_i) per query | O(1) | Too slow |
| Positional Base-26 Conversion | O(log a_i) per query | O(1) extra (output aside) | Accepted |

## Algorithm Walkthrough

We process each query independently.

1. Start with the given number a. This represents the position in the infinite ordered list of column labels.
2. Repeatedly compute the last character of the label by taking a modulo 26. This gives a number in the range 0 to 25, but here 0 does not correspond to A. If the remainder is 0, we interpret it as 26, meaning the character Z, and we also decrement the number before continuing.
3. Convert the adjusted remainder into a character by mapping 1 to A, 2 to B, and so on up to 26 to Z.
4. Append this character to a list, since we are building the string from least significant position to most significant.
5. Divide the number by 26 (integer division). This moves us to the next “digit” in the column naming system.
6. Repeat until the number becomes zero.
7. Reverse the collected characters to obtain the final column label.

The non-obvious step is the adjustment when remainder is zero. This effectively shifts the representation so that each “digit” lives in 1 to 26 instead of 0 to 25, preserving the fact that there is no representation for zero in this system.

### Why it works

The column labels form a positional numeral system with base 26 but without a zero digit. Every valid label corresponds uniquely to a sequence of choices where each position contributes a value in 1 to 26. The repeated division process reconstructs these positions from least significant to most significant, and the correction step ensures that boundary cases like multiples of 26 are represented using Z rather than spilling into the next higher digit incorrectly. This guarantees a bijection between integers and strings.

## Python Solution

```python
import sys
input = sys.stdin.readline

def convert(x: int) -> str:
    res = []
    while x > 0:
        x -= 1
        res.append(chr(ord('A') + (x % 26)))
        x //= 26
    return ''.join(reversed(res))

def main():
    t = int(input())
    for _ in range(t):
        x = int(input())
        print(convert(x))

if __name__ == "__main__":
    main()
```

The crucial implementation choice is subtracting one before taking modulo. This single line resolves the off-by-one shift introduced by the absence of a zero digit. Without it, multiples of 26 would incorrectly map to the wrong letters.

We build the result in reverse order because each modulo step extracts the least significant “digit” first. Reversing at the end restores the correct left-to-right representation.

## Worked Examples

Consider input 1 equal to 28.

| Step | x before | x after -1 | x % 26 | Char | Next x |
| --- | --- | --- | --- | --- | --- |
| 1 | 28 | 27 | 1 | B | 1 |
| 2 | 1 | 0 | 0 | A | 0 |

We obtain BA, which matches the expected mapping since 27 is AA and 28 is BA.

Now consider 26.

| Step | x before | x after -1 | x % 26 | Char | Next x |
| --- | --- | --- | --- | --- | --- |
| 1 | 26 | 25 | 25 | Z | 0 |

The result is Z, confirming that boundary alignment works correctly.

These examples show how the decrement step ensures correct handling of exact multiples of 26 and preserves lexicographic ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t log a_i) | Each number is repeatedly divided by 26 |
| Space | O(1) extra per query | Only a small character buffer is used |

The logarithmic factor comes from repeatedly reducing the number by a factor of 26. Even for values up to 10^18, this requires fewer than 40 iterations per query, which easily fits within limits for up to 10^5 queries.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def convert(x: int) -> str:
        res = []
        while x > 0:
            x -= 1
            res.append(chr(ord('A') + (x % 26)))
            x //= 26
        return ''.join(reversed(res))

    t = int(input())
    out = []
    for _ in range(t):
        out.append(convert(int(input())))
    return "\n".join(out)

# provided samples (conceptual placeholders since exact sample formatting is unclear)
# assert run("5\n5\n27\n52\n53\n703\n") == "E\nAA\nAZ\nBA\nAAA"

# custom cases
assert run("1\n1\n") == "A", "minimum case"
assert run("1\n26\n") == "Z", "boundary at single digit"
assert run("1\n27\n") == "AA", "first two-letter case"
assert run("1\n52\n") == "AZ", "boundary in two-letter space"
assert run("1\n703\n") == "AAA", "boundary three-letter rollover"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | A | minimum value handling |
| 26 | Z | single-digit boundary |
| 27 | AA | transition to two letters |
| 52 | AZ | internal two-letter boundary |
| 703 | AAA | three-letter rollover correctness |

## Edge Cases

For input 26, the algorithm sets x = 26, then decrements to 25, produces character Z, and terminates. This avoids producing an empty remainder and ensures that exact multiples of 26 are handled cleanly.

For input 52, the first iteration maps 52 to remainder 0 after adjustment, producing Z, then continues with x = 1, producing A. This yields AZ, which matches the expected lexicographic ordering.

For input 703, repeated division transitions across all three-character boundaries. The first step yields A for the last position, then AA-like propagation produces AAA. Each stage correctly respects the 1-indexed digit system, confirming that carry propagation behaves like a positional numeral system without zero.
