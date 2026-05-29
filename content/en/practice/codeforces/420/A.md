---
title: "CF 420A - Start Up"
description: "We are asked to determine whether a given company name is symmetric with respect to a vertical mirror. In practical terms, we are given a single string consisting of uppercase English letters, and we need to check whether the string would appear identical if reflected in a…"
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 420
codeforces_index: "A"
codeforces_contest_name: "Coder-Strike 2014 - Finals (online edition, Div. 1)"
rating: 1000
weight: 420
solve_time_s: 84
verified: true
draft: false
---

[CF 420A - Start Up](https://codeforces.com/problemset/problem/420/A)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine whether a given company name is symmetric with respect to a vertical mirror. In practical terms, we are given a single string consisting of uppercase English letters, and we need to check whether the string would appear identical if reflected in a mirror placed vertically along its left-right axis. Only certain letters are symmetrical in this way, for example `A`, `H`, `I`, `M`, `O`, `T`, `U`, `V`, `W`, `X`, `Y`. Letters like `B` or `C` will look different when mirrored and thus cannot appear in a valid name.

The input constraint allows a string length of up to 100,000 characters. With a 1-second time limit, this implies that an algorithm must run in linear time, O(n), at worst. Anything quadratic or involving nested iterations over the string will be too slow. Memory is generous at 256 MB, so storing a small set of valid characters or a boolean array of length n is trivial.

The main edge cases to be careful about are empty or single-character strings, although the problem guarantees non-empty input. A single character that is valid (like `A`) should return `YES`. A string with a single invalid character (like `B`) should return `NO`. Another subtle scenario is strings with all valid characters but arranged in an asymmetric way, for example `AHAH` is invalid because its reverse `HAHA` differs.

## Approaches

The naive approach is straightforward: reverse the string and check whether every character is both mirrored and in the allowed set. This works because mirroring is equivalent to reading the string backwards while ensuring each character itself is symmetrical. However, in a naive implementation, one might accidentally try to map every character to its mirrored version, which is unnecessary for uppercase letters since only a specific subset is valid. This could introduce redundant operations but still would be O(n).

The key insight is that the problem reduces to two checks: first, every character must belong to the set of vertically symmetric letters; second, the string must read the same forwards and backwards. By combining these checks in a single pass, we can efficiently solve the problem in O(n) time without extra memory beyond a small constant-sized set of letters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force: reverse + check mirror | O(n) | O(n) | Accepted |
| Optimal: single-pass check against allowed set and symmetry | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Create a set containing all letters that are symmetrical with respect to a vertical mirror: `A, H, I, M, O, T, U, V, W, X, Y`. This allows constant-time membership checks for each character.
2. Initialize two pointers, one at the start of the string and one at the end. We will iterate towards the middle.
3. At each step, check if both characters at the start and end pointers are in the allowed set. If either character is invalid, print `NO` and terminate. This immediately handles cases where a single disallowed character invalidates the entire string.
4. Check if the characters at the start and end pointers are equal. If not, print `NO` and terminate. This ensures that the string reads the same forwards and backwards.
5. Move the start pointer one step forward and the end pointer one step backward, repeating steps 3 and 4 until the pointers meet or cross.
6. If the loop completes without termination, print `YES`. The string satisfies both symmetry and character validity.

Why it works: The invariant is that at each iteration, all characters outside the current pointers have been validated for symmetry and correct placement. The algorithm checks all pairs exactly once. Since only valid letters are allowed and each pair matches, the final string is guaranteed to be identical to its mirror reflection.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
valid_letters = {'A', 'H', 'I', 'M', 'O', 'T', 'U', 'V', 'W', 'X', 'Y'}

left, right = 0, len(s) - 1
while left <= right:
    if s[left] not in valid_letters or s[right] not in valid_letters:
        print("NO")
        sys.exit()
    if s[left] != s[right]:
        print("NO")
        sys.exit()
    left += 1
    right -= 1

print("YES")
```

The code first reads the input string and removes any trailing newline characters. The set of valid mirror letters allows quick membership testing. We then use a two-pointer technique to check symmetry from the outside in. Exiting immediately on failure avoids unnecessary work. This ensures the algorithm runs in O(n) time and uses only O(1) additional space.

## Worked Examples

Sample Input 1:

```
AHA
```

| left | right | s[left] | s[right] | check valid | check equal |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | A | A | yes | yes |
| 1 | 1 | H | H | yes | yes |

The loop completes, so output is `YES`. Both symmetry and validity are satisfied.

Sample Input 2:

```
ABBA
```

| left | right | s[left] | s[right] | check valid | check equal |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | A | A | yes | yes |
| 1 | 2 | B | B | no | - |

Since `B` is not valid, output is `NO`. This demonstrates the character filter correctly rejects non-symmetric letters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is visited exactly once with two pointers moving towards the center. |
| Space | O(1) | The set of valid letters has constant size; no additional storage scales with n. |

The algorithm easily handles strings of length up to 100,000 within 1 second and uses negligible memory, well within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = input().strip()
    valid_letters = {'A', 'H', 'I', 'M', 'O', 'T', 'U', 'V', 'W', 'X', 'Y'}
    left, right = 0, len(s) - 1
    while left <= right:
        if s[left] not in valid_letters or s[right] not in valid_letters:
            return "NO"
        if s[left] != s[right]:
            return "NO"
        left += 1
        right -= 1
    return "YES"

# Provided sample
assert run("AHA\n") == "YES", "sample 1"

# Custom cases
assert run("ABBA\n") == "NO", "invalid letters"
assert run("AAA\n") == "YES", "all valid, odd length"
assert run("AHHHA\n") == "YES", "odd length palindrome"
assert run("XYX\n") == "YES", "symmetric X/Y letters"
assert run("XYZ\n") == "NO", "contains invalid Z"
assert run("A\n") == "YES", "single valid letter"
assert run("B\n") == "NO", "single invalid letter"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| ABBA | NO | Invalid letters in the middle |
| AAA | YES | Repeated valid letters, odd length |
| AHHHA | YES | Odd length palindrome with valid letters |
| XYZ | NO | Presence of invalid letters |
| A | YES | Single valid character |
| B | NO | Single invalid character |

## Edge Cases

For a single character `A`, the pointers `left` and `right` both point at index 0. The loop runs once, finds `A` in the valid set, and `s[left] == s[right]`, then exits, returning `YES`. For a single invalid character `B`, the same loop immediately detects that `B` is not in the valid set and returns `NO`. Strings with maximum length and all valid characters will be handled in O(n) time with no extra memory beyond the small set, confirming robustness across constraints.
