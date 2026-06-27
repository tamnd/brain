---
title: "CF 105048A - To be, or not to be?"
description: "We are given a single line of text that may contain uppercase and lowercase English letters mixed with spaces. The task is to determine whether the contiguous sequence of characters “be” appears anywhere in this text when we ignore capitalization."
date: "2026-06-28T05:41:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105048
codeforces_index: "A"
codeforces_contest_name: "UTPC Contest 03-22-24 Div. 2 (Beginner)"
rating: 0
weight: 105048
solve_time_s: 72
verified: true
draft: false
---

[CF 105048A - To be, or not to be?](https://codeforces.com/problemset/problem/105048/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single line of text that may contain uppercase and lowercase English letters mixed with spaces. The task is to determine whether the contiguous sequence of characters “be” appears anywhere in this text when we ignore capitalization.

The key transformation is that case does not matter, so every character should be treated as if it were lowercase before we search. Spaces are just normal characters in the input, but they cannot be part of the target substring because we are specifically looking for two consecutive letters forming “be”.

The input size is at most 1000 characters, which is extremely small by competitive programming standards. This immediately rules out any concern about efficiency beyond linear scanning. Even a naive approach that checks every possible substring is already sufficient within limits.

The main subtlety is handling case normalization and ensuring we only consider consecutive letters. A common mistake is to search for “be” in the original string without converting case, which fails on inputs like “BE” or “Be”. Another mistake is incorrectly skipping spaces in a way that breaks adjacency logic. For example, “b e” should not match because the characters are not consecutive in the original string.

Edge cases include strings with no letters forming the pattern even though letters appear near each other, such as “b e”, and strings where the match spans different cases like “bE” or “BE”. A single-character string like “b” or “e” must also correctly return “no”.

## Approaches

A straightforward approach is to normalize the string into a uniform case, then scan it from left to right checking every adjacent pair of characters. If any pair equals “be”, we immediately conclude the answer is positive.

A brute-force variant would explicitly test every substring of length 2 and compare it to “be” after converting to lowercase. For a string of length n, this checks n - 1 substrings, each in constant time, giving linear complexity. Even more naive methods like generating all substrings would be unnecessary but still pass given the constraint.

The key observation is that the problem reduces to a simple pattern search of fixed length 2. There is no need for advanced string algorithms like KMP because the pattern is constant-sized. This collapses the task into a single pass over the string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all substrings) | O(n) | O(1) | Accepted |
| Optimal (single scan) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string as a single line. This string may include spaces, which we will not remove, only ignore for matching purposes indirectly through character comparison.
2. Convert the entire string to lowercase. This ensures that comparisons are uniform and eliminates case-based branching later.
3. Iterate through the string from index 0 to n - 2. We stop at n - 2 because we are always checking a pair of consecutive characters.
4. For each position i, check whether s[i] is 'b' and s[i + 1] is 'e'. This directly tests whether the substring starting at i matches the target pattern.
5. If any such pair is found, immediately output “yes” and terminate the program.
6. If the loop finishes without finding a match, output “no”.

### Why it works

The algorithm relies on the invariant that every occurrence of the substring “be” in the original string must appear as two consecutive characters in some index pair (i, i + 1). Lowercasing preserves equality relationships between letters, so any valid match in the original string corresponds exactly to a match in the transformed string. Since we check all adjacent pairs, no valid occurrence can be missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().rstrip("\n")
s = s.lower()

found = False
for i in range(len(s) - 1):
    if s[i] == 'b' and s[i + 1] == 'e':
        found = True
        break

print("YES" if found else "NO")
```

The solution reads the input efficiently and immediately normalizes it using `.lower()`. The loop is carefully bounded to avoid indexing out of range when accessing `i + 1`. The early exit ensures we stop as soon as the pattern is found, though even without early exit the complexity remains linear.

A common implementation pitfall is forgetting that spaces remain in the string. This code handles that correctly because spaces will never match either 'b' or 'e', so they naturally fail comparisons without needing special handling.

## Worked Examples

### Example 1

Input:

```
To Be or Not to BE that is the QUESTION
```

After lowercasing:

```
to be or not to be that is the question
```

| i | s[i] | s[i+1] | Match |
| --- | --- | --- | --- |
| 0 | t | o | no |
| 1 | o |  | no |
| 2 |  | b | no |
| 3 | b | e | yes |

At index 3, we encounter the pair “be”, so the algorithm stops immediately and outputs YES. This confirms that case normalization allows detection of both “Be” and “BE” uniformly.

### Example 2

Input:

```
To b or not to b that is the question
```

After lowercasing:

```
to b or not to b that is the question
```

| i | s[i] | s[i+1] | Match |
| --- | --- | --- | --- |
| 0 | t | o | no |
| 1 | o |  | no |
| 2 |  | b | no |
| 3 | b |  | no |
| 4 |  | o | no |
| ... | ... | ... | ... |

No adjacent pair forms “be”, so the loop completes without setting the flag. The output is NO, which confirms that isolated letters do not incorrectly combine across spaces.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan each adjacent pair of characters once |
| Space | O(1) | Only a few variables are used besides the input string |

The maximum input length is 1000, so even a linear scan is effectively constant-time in practice. Memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    s = sys.stdin.readline().rstrip("\n").lower()
    for i in range(len(s) - 1):
        if s[i] == 'b' and s[i + 1] == 'e':
            return "YES"
    return "NO"

# provided samples
assert run("To Be or Not to BE that is the QUESTION\n") == "YES"
assert run("To b or not to b that is the question\n") == "NO"

# custom cases
assert run("be\n") == "YES"
assert run("Be\n") == "YES"
assert run("b e\n") == "NO"
assert run("bbbbbeeeee\n") == "YES"
assert run("xyz\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "be" | YES | minimal match |
| "b e" | NO | space breaks adjacency |
| "BBBB" | NO | no false positives under case normalization |
| "xyz" | NO | non-matching letters |

## Edge Cases

A key edge case is when the substring appears with mixed capitalization. For input like “bE”, the algorithm first converts it to “be”, then the adjacent check detects it at index 0 and returns YES immediately. This confirms that normalization correctly unifies all case variants.

Another edge case is the presence of spaces between letters that would otherwise form the pattern. For example, “b e” becomes “b e” after normalization. The loop checks only adjacent indices, so it never combines characters across the space, and correctly returns NO.

A final edge case is very short strings such as “b” or “e”. After lowercasing, the loop range becomes empty since length minus one is zero or negative, so no iteration occurs and the function correctly returns NO.
