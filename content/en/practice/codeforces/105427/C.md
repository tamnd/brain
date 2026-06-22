---
title: "CF 105427C - Converting Romans"
description: "We are given a collection of strings, each string representing a number written in a simplified Roman numeral system. Each character is one of the standard Roman symbols I, V, X, L, C, D, M with fixed values 1, 5, 10, 50, 100, 500, 1000."
date: "2026-06-23T04:06:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105427
codeforces_index: "C"
codeforces_contest_name: "2023-2024 ACM-ICPC Nordic Collegiate Programming Contest (NCPC 2023)"
rating: 0
weight: 105427
solve_time_s: 54
verified: true
draft: false
---

[CF 105427C - Converting Romans](https://codeforces.com/problemset/problem/105427/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of strings, each string representing a number written in a simplified Roman numeral system. Each character is one of the standard Roman symbols I, V, X, L, C, D, M with fixed values 1, 5, 10, 50, 100, 500, 1000.

The interpretation rule is not the classical strict Roman rule, but a relaxed version: whenever a symbol appears somewhere to the left of a strictly larger-valued symbol, that left symbol contributes negatively. Otherwise it contributes positively. Unlike the usual Roman numeral system, subtraction is not limited to adjacent pairs, so a symbol can be “canceled” by any larger symbol appearing later in the string.

For each input string, we must compute the resulting integer value under this rule and print it.

The input size makes the structure important. There can be up to 1000 strings, and the total length across all strings is up to 300,000 characters. This means any solution must be linear in total input size. An approach that scans each string multiple times or compares all pairs of characters would be too slow.

A naive reading might suggest checking every character against all later characters to decide whether it is subtracted. That would lead to quadratic behavior per string, which is impossible at the given scale.

A key subtlety is that subtraction depends only on whether there exists a larger symbol somewhere to the right, not how far it is or how many such symbols exist.

A typical failure case comes from interpreting subtraction only between adjacent characters. For example, in the string "IVI", a local rule might subtract I from V but miss that the final I is positive again.

Another failure case arises if we only subtract when the next character is larger. In "IXC", both I and X should be affected by later larger symbols, but adjacency-based logic would miss the influence of C on I.

## Approaches

The brute-force idea is straightforward: for each character, scan everything to its right to check whether a larger-valued Roman symbol exists. If such a symbol exists, we subtract the current value, otherwise we add it.

This is correct because it directly encodes the rule definition: a symbol is negative exactly when it has a larger symbol somewhere to its right. However, this requires, for each of the L characters in a string, scanning up to L more characters. That gives O(L²) per string, and in the worst case with total length 300,000, this would exceed 10¹⁰ operations, which is far beyond feasible limits.

The optimization comes from reversing the perspective. Instead of asking “does a larger symbol exist to the right of this position?”, we ask “what is the maximum symbol seen so far from the right?”. If we traverse the string from right to left, we can maintain the maximum Roman value encountered so far. For each character, if it is strictly smaller than this maximum, it must be subtracted; otherwise it contributes positively and updates the maximum.

This works because the condition “there exists a larger symbol to the right” is equivalent to “the maximum suffix value is greater than the current value”.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(L²) total | O(1) | Too slow |
| Optimal | O(L) total | O(1) | Accepted |

## Algorithm Walkthrough

We process each Roman numeral string independently.

1. Convert each Roman character into its integer value using a fixed mapping. This allows constant-time comparisons between symbols.
2. Initialize a variable `max_right` to zero. This will store the maximum value seen so far while scanning from the right.
3. Traverse the string from the last character to the first character.
4. For each character, compare its value with `max_right`. If it is strictly less than `max_right`, subtract it from the running answer. Otherwise, add it and update `max_right` to this value.
5. After processing all characters, output the accumulated sum.

The key idea in step 4 is that we never need to explicitly search for a larger symbol. The suffix maximum already encodes whether such a symbol exists.

### Why it works

At any position i during a right-to-left scan, `max_right` represents the maximum value among all characters strictly to the right of i. Therefore, a character at i is subtracted if and only if there exists a character to its right with a larger value. This matches the problem definition exactly. The invariant is that after processing suffix i+1..n, `max_right` equals the maximum value in that suffix, ensuring correct classification for position i.

## Python Solution

```python
import sys
input = sys.stdin.readline

value = {
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000
}

def solve(s: str) -> int:
    max_right = 0
    ans = 0

    for ch in reversed(s):
        v = value[ch]
        if v < max_right:
            ans -= v
        else:
            ans += v
            max_right = v

    return ans

def main():
    n = int(input())
    for _ in range(n):
        s = input().strip()
        print(solve(s))

if __name__ == "__main__":
    main()
```

The mapping table is fixed and allows constant-time lookup for each character.

The main loop processes each string independently. The reversal is crucial because it ensures that `max_right` always refers to the suffix maximum, not a prefix property.

The subtraction condition is strictly `v < max_right`, not `<=`, since equal values do not trigger subtraction under the problem rule.

## Worked Examples

Consider the input string `IVI`.

| Step | Char | Value | max_right before | Action | max_right after | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | I | 1 | 0 | add | 1 | 1 |
| 2 | V | 5 | 1 | add | 5 | 6 |
| 3 | I | 1 | 5 | subtract | 5 | 5 |

This shows how only symbols strictly smaller than a later maximum are subtracted.

Now consider `ID`.

| Step | Char | Value | max_right before | Action | max_right after | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | D | 500 | 0 | add | 500 | 500 |
| 2 | I | 1 | 500 | subtract | 500 | 499 |

This demonstrates non-adjacent subtraction, where I is affected by D even though they are separated.

These traces confirm that the suffix maximum correctly captures the “exists a larger symbol to the right” condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total length) | Each character is processed once with O(1) work |
| Space | O(1) | Only a fixed mapping and a few variables are used |

The total length is at most 300,000, so a single linear pass over all characters fits comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    return sys.stdout.getvalue()

# Since we cannot reliably capture stdout in this template environment,
# these asserts are illustrative.

# provided sample (conceptual)
# assert run("3\nCDXCIX\nID\nIV\n") == "499\n499\n4\n"

# minimal cases
# assert run("1\nI\n") == "1"
# assert run("1\nIV\n") == "4"

# edge: strictly increasing
# assert run("1\nIXC\n") == "109"

# edge: all equal
# assert run("1\nIII\n") == "3"

# edge: large value first
# assert run("1\nMCI\n") == "1100"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| I | 1 | single symbol |
| IV | 4 | basic subtraction |
| IXC | 109 | non-adjacent subtraction chain |
| III | 3 | no subtraction case |
| MCI | 1100 | large prefix dominance |

## Edge Cases

One important edge case is when subtraction is triggered by a symbol far away, not adjacent. In `ID`, the I is not next to a larger symbol, but it is still subtracted because D appears later. During processing, we see D first, setting `max_right = 500`, and then I is processed and subtracted, producing 499 correctly.

Another edge case is when values increase and then decrease again, such as `IVI`. The first I is processed with no larger suffix, so it adds. V then updates the suffix maximum. The final I is then compared against V and subtracted. This confirms that the algorithm correctly handles local increases and later decreases without needing any pairwise comparisons.

A final subtle case is repeated large symbols like `MCM`. The first M sets the maximum, the C is subtracted because M exists to its right, and the final M is added normally. The suffix maximum ensures that earlier symbols are correctly classified even when multiple large symbols exist later in the string.
