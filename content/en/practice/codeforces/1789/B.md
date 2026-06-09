---
title: "CF 1789B - Serval and Inversion Magic"
description: "We are given a binary string consisting only of 0s and 1s. The task is to determine whether we can make it a palindrome by flipping exactly one contiguous segment of the string. Flipping a segment means changing every 0 in that segment to 1 and every 1 to 0."
date: "2026-06-09T10:42:03+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "strings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1789
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 853 (Div. 2)"
rating: 800
weight: 1789
solve_time_s: 90
verified: true
draft: false
---

[CF 1789B - Serval and Inversion Magic](https://codeforces.com/problemset/problem/1789/B)

**Rating:** 800  
**Tags:** brute force, implementation, strings, two pointers  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string consisting only of 0s and 1s. The task is to determine whether we can make it a palindrome by flipping exactly one contiguous segment of the string. Flipping a segment means changing every 0 in that segment to 1 and every 1 to 0.

For example, for a string `10010`, flipping the first three characters produces `01110`, which is a palindrome. The string length can be up to 100,000, and there can be up to 10,000 test cases. Since the total sum of lengths does not exceed 200,000, we need a solution that runs linearly with respect to the string length per test case. Quadratic solutions that try all possible segments would result in around 10^10 operations, which is infeasible.

The tricky part is that we are allowed **exactly one flip**, not multiple. This introduces several edge cases. If the string is already a palindrome, we cannot do nothing - we must still flip one segment, potentially the smallest segment. For instance, `11` is a palindrome, but flipping either character produces `01` or `10`, both of which are not palindromes. This highlights the importance of checking the ability to flip some segment to achieve the palindrome, not just whether the string is currently a palindrome.

Another subtle scenario occurs with strings of length three, such as `010`. If we flip the middle character, it remains a palindrome. If we flip the outer two, it is still a palindrome. These small cases illustrate that the exact segment selection is crucial, and we must account for overlaps between the left and right mismatches in the string.

## Approaches

A brute-force approach would iterate over all possible segments `[l, r]` and flip them to see whether the resulting string is a palindrome. The number of segments is O(n^2), and checking for a palindrome costs O(n). This gives a worst-case complexity of O(n^3), which is far too slow for `n` up to 10^5.

The key insight is to focus on **mismatched positions**. For a string to become a palindrome, every character at index `i` must match the character at index `n-i-1`. If they already match, we can ignore them. If they differ, flipping a segment must cover one of the characters but not the other, effectively inverting one to match the other.

By counting the number of mismatched pairs, we can reason:

- If there are **0 mismatches**, the string is already a palindrome. Flipping any segment of length one will create exactly one mismatch pair, but flipping a single character in an even-length string can still produce a valid palindrome. In practice, a length check and whether the string length allows a segment flip is enough.
- If there is **exactly 1 mismatch pair**, flipping a segment covering one of the mismatched characters will fix it. This is possible if the segment includes one of the pair and optionally more characters without creating additional mismatches elsewhere.
- If there are **more than 1 mismatch pairs**, we need to check whether these mismatches are consecutive or can be covered by a single contiguous flip. A mismatch pattern like `0110` has mismatches at positions 0-3 and 1-2; a single flip of the middle two fixes it. If mismatches are non-adjacent in a pattern that cannot be covered by one segment, it is impossible.

A simpler way to implement is to iterate with two pointers from left and right toward the center. Count the positions where `s[left] == s[right]` versus `s[left] != s[right]`. If the count of mismatches is zero, we can flip any single character. If the count is one or the mismatches form a contiguous block, the answer is yes. Otherwise, the answer is no. This reduces the problem to a linear scan, O(n) per test case, which is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Two-Pointer Mismatch Counting | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize two pointers: `l = 0` and `r = n - 1`.
2. Move the pointers toward the center. For each pair `(s[l], s[r])`, check if they are equal. If equal, no action is required, move `l` forward and `r` backward.
3. If they are not equal, mark this as a mismatch. Store the first and last mismatch positions. Increment `l` and decrement `r`.
4. After the scan, count the total number of mismatches. If there are zero mismatches, the string is already a palindrome. Flipping any single character (or the middle character if odd length) will maintain palindrome structure. Return "Yes".
5. If mismatches exist, check whether all mismatch indices form a contiguous block. This can be determined by verifying that the distance between the first and last mismatch equals the number of mismatches. If so, a single flip covering this segment will resolve all mismatches. Return "Yes".
6. If mismatches are non-contiguous, no single segment can fix the string. Return "No".

The reason this works is that each mismatch requires exactly one inversion on one of the two positions. A contiguous flip can invert multiple positions at once. If all mismatches lie in one contiguous segment, flipping that segment aligns all mismatched pairs simultaneously. Non-contiguous mismatches require multiple separate flips, which violates the constraint of exactly one operation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = input().strip()
        
        l, r = 0, n - 1
        mismatches = []
        while l < r:
            if s[l] != s[r]:
                mismatches.append(l)
            l += 1
            r -= 1
        
        if not mismatches:
            print("Yes")
            continue
        
        first, last = mismatches[0], mismatches[-1]
        if last - first + 1 == len(mismatches):
            print("Yes")
        else:
            print("No")

if __name__ == "__main__":
    solve()
```

The code initializes pointers and collects mismatch indices. If the mismatch indices are contiguous, a single flip fixes all differences. If there are no mismatches, flipping any minimal segment keeps the string a palindrome. Edge conditions, like odd-length strings, are naturally handled by the pointer iteration.

## Worked Examples

### Example 1

Input: `1001`

| l | r | s[l] | s[r] | mismatch list |
| --- | --- | --- | --- | --- |
| 0 | 3 | 1 | 1 | [] |
| 1 | 2 | 0 | 0 | [] |

No mismatches, we can flip the entire string to get `0110`, which is a palindrome. Output: Yes.

### Example 2

Input: `10010`

| l | r | s[l] | s[r] | mismatch list |
| --- | --- | --- | --- | --- |
| 0 | 4 | 1 | 0 | [0] |
| 1 | 3 | 0 | 1 | [0,1] |

Mismatches are contiguous positions 0 and 1. Flipping segment `[0,1]` gives `01110`, a palindrome. Output: Yes.

### Example 3

Input: `0111011`

| l | r | s[l] | s[r] | mismatch list |
| --- | --- | --- | --- | --- |
| 0 | 6 | 0 | 1 | [0] |
| 1 | 5 | 1 | 1 | [0] |
| 2 | 4 | 1 | 0 | [0,2] |

Mismatches are non-contiguous (positions 0 and 2). No single flip can fix all mismatches. Output: No.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case, O(total n) overall | We scan the string once with two pointers. Sum of n ≤ 2⋅10^5. |
| Space | O(n) in worst case for mismatch indices | At most n/2 mismatches stored. Could be optimized to O(1) with just first and last mismatch. |

The algorithm fits comfortably within the 1-second time limit and 256 MB memory constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("3\n4\n1001\n5\n10010\n7\n0111011\n") == "Yes\nYes\nNo", "samples"

# minimum-size inputs
assert run("2\n2\n01\n2\n11\n") == "Yes\nYes", "2-char strings"

# all-equal values
assert run("2\n5\n00000\n5\n11111\n") == "Yes\nYes", "all same"

# single mismatch in middle
assert run("1\n3\n010\n") == "Yes", "odd-length single
```
