---
title: "CF 104443C - Morco-Feely Palindromes"
description: "We are given a single string consisting only of digits, with length at most 100. The task is to decide whether this string satisfies a very specific symmetry condition and output a simple yes or no verdict."
date: "2026-06-30T18:45:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104443
codeforces_index: "C"
codeforces_contest_name: "TheForces Round #18 (JuneIsApril-Forces)"
rating: 0
weight: 104443
solve_time_s: 68
verified: true
draft: false
---

[CF 104443C - Morco-Feely Palindromes](https://codeforces.com/problemset/problem/104443/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single string consisting only of digits, with length at most 100. The task is to decide whether this string satisfies a very specific symmetry condition and output a simple yes or no verdict.

The structure we are looking for is purely about how the characters read from left to right compare with the characters read from right to left. There is no arithmetic interpretation of the digits, no need to parse numbers or perform transformations. The entire problem reduces to reasoning about the sequence of characters as a static object.

Because the maximum length is only 100, any solution that inspects characters directly is already efficient enough. Even an approach that repeatedly scans the string would still run in constant time relative to typical competitive programming limits. This immediately rules out concerns about performance optimization and shifts focus entirely onto correctness and handling boundary cases.

The main subtlety lies in recognizing edge behavior on very small inputs. A single character string behaves differently from multi-character strings because symmetry becomes trivial, while two-character strings may or may not satisfy the required condition depending on whether both ends match.

A naive mistake here would be to assume a property based on partial observation, such as checking only the first and last characters without verifying the full structure. For example, input `343` would incorrectly pass a first-last check, but a full verification is still required to ensure full symmetry.

## Approaches

The straightforward approach is to check whether the string reads the same forward and backward. This means comparing symmetric positions: the first character with the last, the second with the second last, and so on until the middle is reached.

A brute-force way to think about this is to reverse the string and compare it with the original. This works because reversing encodes all symmetry constraints into a single object comparison. The cost is linear in the string length, since constructing the reversed string and comparing it both take O(n) time.

Given the constraint of length at most 100, even repeated comparisons or naive scans are negligible. However, if we generalize the idea, the key structural insight is that palindrome checking does not require storing the entire reversed string. Instead, we can directly compare mirrored indices, which avoids extra allocation and makes the logic clearer.

The brute-force works because it explicitly constructs the reversed representation and checks equality. It becomes unnecessary overhead when we realize that the comparison is pairwise independent, allowing early termination as soon as a mismatch is found.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Reverse and compare | O(n) | O(n) | Accepted |
| Two-pointer check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We focus on the two-pointer method, since it expresses the structure of the problem most directly.

1. Start with two indices, one at the beginning of the string and one at the end. These represent the characters that must match for the string to remain symmetric. If at any point they differ, symmetry is broken immediately.
2. Compare the characters at the two indices. If they are not equal, we can stop and conclude the string is not symmetric. This early exit is valid because a single mismatch violates the global condition.
3. If they match, move both pointers inward, advancing the left index forward and the right index backward. This ensures we progressively verify all mirrored positions without repetition.
4. Repeat this process until the pointers cross or meet. If we complete all comparisons without finding a mismatch, the string satisfies the symmetry requirement.

The reasoning behind this process is that every valid symmetric string must satisfy equality at all mirrored positions simultaneously. Checking them independently guarantees completeness because each comparison enforces one necessary condition of the global structure.

### Why it works

The algorithm maintains the invariant that all character pairs outside the current pointer range have already been verified to match. Each step reduces the unverified portion of the string while preserving correctness. If a mismatch exists anywhere, it must occur in some mirrored pair, and that pair will eventually be checked directly. Therefore, the algorithm cannot miss a violation, and if it finishes without finding one, the string must be symmetric.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

i, j = 0, len(s) - 1
ok = True

while i < j:
    if s[i] != s[j]:
        ok = False
        break
    i += 1
    j -= 1

print("YES" if ok else "NO")
```

The code reads the input string and initializes two pointers at its extremes. The loop enforces the mirrored comparison logic described earlier. The moment a mismatch is found, we exit early because further checks cannot repair symmetry.

A subtle implementation detail is the use of `strip()` to ensure no trailing newline interferes with indexing. Another important point is handling the case where the string has length 1, in which case the loop never runs and the result correctly defaults to `YES`.

## Worked Examples

### Example 1

Input: `5`

| i | j | s[i] | s[j] | Action |
| --- | --- | --- | --- | --- |
| 0 | 0 | 5 | 5 | pointers meet, stop |

Since there are no mismatches, the string is symmetric by definition.

This confirms the behavior on the minimal input size, where symmetry is vacuously true.

### Example 2

Input: `43`

| i | j | s[i] | s[j] | Action |
| --- | --- | --- | --- | --- |
| 0 | 1 | 4 | 3 | mismatch found |

The first comparison already violates symmetry, so the process stops immediately.

This demonstrates early termination in non-symmetric strings, where no further computation is needed once a contradiction is found.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is compared at most once via mirrored pairing |
| Space | O(1) | Only two pointers are used, no extra data structures |

The input size is bounded by 100, so the algorithm runs in constant time in practice. Even in a much larger setting, the linear scan remains efficient and easily within typical constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    s = input().strip()
    i, j = 0, len(s) - 1
    ok = True
    while i < j:
        if s[i] != s[j]:
            ok = False
            break
        i += 1
        j -= 1
    return "YES" if ok else "NO"

# provided samples
assert run("5\n") == "YES"
assert run("43\n") == "NO"
assert run("76\n") == "NO"

# custom cases
assert run("1\n") == "YES"
assert run("11\n") == "YES"
assert run("12321\n") == "YES"
assert run("12345\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | YES | single character symmetry |
| 11 | YES | even-length palindrome |
| 12321 | YES | longer odd-length palindrome |
| 12345 | NO | clearly non-symmetric sequence |

## Edge Cases

A single digit input like `7` is the simplest scenario. The algorithm sets `i = 0` and `j = 0`, so the loop does not execute. The result remains `YES`, which is correct because any single character string is symmetric by definition.

For a two-character mismatch such as `90`, the first comparison `s[0]` vs `s[1]` fails immediately. The algorithm correctly outputs `NO` without unnecessary checks.

For a longer symmetric input like `1221`, comparisons proceed as `(1,1)` and `(2,2)` in mirrored positions. All checks succeed, confirming that the algorithm correctly aggregates local equality into global symmetry.
