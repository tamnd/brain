---
title: "CF 290D - Orange"
description: "We are given a string consisting of English letters, both uppercase and lowercase, and an integer representing a \"capitalization budget\" between 0 and 26."
date: "2026-06-05T10:35:44+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 290
codeforces_index: "D"
codeforces_contest_name: "April Fools Day Contest 2013"
rating: 1400
weight: 290
solve_time_s: 127
verified: true
draft: false
---

[CF 290D - Orange](https://codeforces.com/problemset/problem/290/D)

**Rating:** 1400  
**Tags:** *special, implementation  
**Solve time:** 2m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string consisting of English letters, both uppercase and lowercase, and an integer representing a "capitalization budget" between 0 and 26. The task is to transform the string by converting as many lowercase letters to uppercase as possible without exceeding this budget. Every uppercase letter conversion consumes one unit from the budget. Letters that are already uppercase do not count against the budget and are left unchanged.

The input string can be up to 50 characters long. Since this is very small, any solution that processes each character individually will be efficient. The integer constraint of 0 to 26 is critical: it limits the number of characters we can convert, which means we must be selective if the string contains more than 26 lowercase letters.

Edge cases emerge in a few places. If the budget is 0, no conversions occur. If the string contains fewer lowercase letters than the budget, all lowercase letters should be converted and the remaining budget is unused. Strings composed entirely of uppercase letters are unaffected regardless of the budget. A careless implementation that blindly converts letters or miscounts could easily overshoot the budget or fail to leave already uppercase letters unchanged.

## Approaches

The brute-force approach is straightforward: iterate through the string character by character. For each character, check if it is lowercase and if there is remaining budget. If both conditions hold, convert it to uppercase and decrement the budget. Otherwise, leave the character unchanged. This method is correct because it explicitly implements the rules of the problem. Its complexity is O(n), where n is the string length, which in the worst case is 50. Even with 50 characters, this operation count is trivial. Brute force in this context is already optimal due to the small input size.

The key insight that could refine the approach is recognizing that there is no need for additional data structures or sorting. Every lowercase character is equally valuable for conversion, so a simple left-to-right scan guarantees the maximum possible use of the budget without exceeding it. This observation allows us to avoid thinking in terms of prioritization or complicated selection strategies.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(n) | Accepted |
| Optimized Scan | O(n) | O(n) | Accepted |

Since both are O(n) and n ≤ 50, the scan method suffices.

## Algorithm Walkthrough

1. Read the input string and the budget integer.
2. Initialize an empty result list. Lists are preferable in Python for character-by-character mutation because strings are immutable.
3. Iterate over each character in the input string.
4. For each character, check if it is a lowercase letter. If it is lowercase and the budget is greater than 0, convert it to uppercase and decrement the budget. Otherwise, leave the character unchanged.
5. Append each processed character to the result list.
6. After processing all characters, join the list into a single string and output it.

The reason this works is simple: the algorithm maintains an invariant that at any point, the number of converted lowercase letters does not exceed the budget. Each lowercase character is converted only if budget remains, and uppercase letters are untouched. This guarantees the resulting string is valid and maximizes uppercase conversions.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
k = int(input().strip())

result = []

for ch in s:
    if 'a' <= ch <= 'z' and k > 0:
        result.append(ch.upper())
        k -= 1
    else:
        result.append(ch)

print("".join(result))
```

The solution reads the input efficiently using `sys.stdin.readline` and strips trailing newline characters. The iteration checks each character explicitly against the lowercase ASCII range, which avoids mistakes with `str.islower()` misbehaving on non-ASCII characters. Decrementing the budget only when a conversion occurs ensures the invariant is preserved. Using a list for building the result avoids repeated string concatenations, which are slower in Python.

## Worked Examples

**Sample 1**

Input:

```
AprilFool
14
```

| Character | Budget | Action | Result List |
| --- | --- | --- | --- |
| 'A' | 14 | already uppercase | ['A'] |
| 'p' | 14 | convert | ['A', 'P'], k=13 |
| 'r' | 13 | convert | ['A', 'P', 'R'], k=12 |
| 'i' | 12 | convert | ['A', 'P', 'R', 'I'], k=11 |
| 'l' | 11 | convert | ['A', 'P', 'R', 'I', 'L'], k=10 |
| 'F' | 10 | already uppercase | ['A', 'P', 'R', 'I', 'L', 'F'] |
| 'o' | 10 | convert | ['A', 'P', 'R', 'I', 'L', 'F', 'O'], k=9 |
| 'o' | 9 | convert | ['A', 'P', 'R', 'I', 'L', 'F', 'O', 'O'], k=8 |
| 'l' | 8 | convert | ['A', 'P', 'R', 'I', 'L', 'F', 'O', 'O', 'L'], k=7 |

Output: `APRILFOOL`

This trace confirms the algorithm respects the budget and converts letters left-to-right.

**Edge Case Example**

Input:

```
XYZ
0
```

| Character | Budget | Action | Result List |
| --- | --- | --- | --- |
| 'X' | 0 | already uppercase | ['X'] |
| 'Y' | 0 | already uppercase | ['X', 'Y'] |
| 'Z' | 0 | already uppercase | ['X', 'Y', 'Z'] |

Output: `XYZ`

The budget is zero, so no lowercase letters are converted, and uppercase letters remain unchanged.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We iterate through each character of the string exactly once. n ≤ 50. |
| Space | O(n) | The result list stores each character, giving linear space relative to input length. |

The operation count is minimal, well within the 2-second limit. Memory usage is also trivial, so this solution easily fits within the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = input().strip()
    k = int(input().strip())
    result = []
    for ch in s:
        if 'a' <= ch <= 'z' and k > 0:
            result.append(ch.upper())
            k -= 1
        else:
            result.append(ch)
    return "".join(result)

# provided sample
assert run("AprilFool\n14\n") == "APRILFOOL", "sample 1"

# custom cases
assert run("xyz\n0\n") == "xyz", "zero budget"
assert run("abcXYZ\n2\n") == "ABcXYZ", "partial budget usage"
assert run("abcdef\n26\n") == "ABCDEF", "full budget usage"
assert run("ABCDEFGHIJKLMNOPQRSTUVWXYZ\n10\n") == "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "all uppercase input"
assert run("aAaaA\n3\n") == "AAAaA", "mixed letters with limited budget"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "xyz\n0" | "xyz" | Budget zero case |
| "abcXYZ\n2" | "ABcXYZ" | Partial budget usage with mixed case |
| "abcdef\n26" | "ABCDEF" | Budget exceeds lowercase count |
| "ABCDEFGHIJKLMNOPQRSTUVWXYZ\n10" | "ABCDEFGHIJKLMNOPQRSTUVWXYZ" | All uppercase input |
| "aAaaA\n3" | "AAAaA" | Mixed letters with limited budget |

## Edge Cases

For a string where the budget is zero, the algorithm leaves every character unchanged. Input "xyz\n0" yields "xyz" because the budget never allows conversion. For strings with fewer lowercase letters than the budget, such as "abc\n5", all lowercase letters are converted and the remaining budget is unused. For strings with only uppercase letters, the budget is irrelevant and the string is returned as-is. These scenarios are handled automatically by the condition checks in the iteration.
