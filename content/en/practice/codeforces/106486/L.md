---
title: "CF 106486L - \u7528\u6237\u540d\u957f\u5ea6\u5e94\u5728 5 \u4f4d\u5230 12 \u4f4d\u4e4b\u95f4"
description: "The task is centered around validating a username based purely on its length. We are given a single identifier, and the only requirement is to check whether its length falls within a fixed inclusive range."
date: "2026-06-19T15:15:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106486
codeforces_index: "L"
codeforces_contest_name: "Dalian University of Technology, Software College 2025 Freshman Contest"
rating: 0
weight: 106486
solve_time_s: 42
verified: true
draft: false
---

[CF 106486L - \u7528\u6237\u540d\u957f\u5ea6\u5e94\u5728 5 \u4f4d\u5230 12 \u4f4d\u4e4b\u95f4](https://codeforces.com/problemset/problem/106486/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is centered around validating a username based purely on its length. We are given a single identifier, and the only requirement is to check whether its length falls within a fixed inclusive range. If the length satisfies the constraint, we accept it, otherwise we reject it.

From a data perspective, the input is just a string representing a username. There are no additional parameters, no multiple test cases, and no hidden structure such as graphs or arrays. The output is a simple judgment based on whether the string length is within the allowed bounds.

The constraints are extremely small in computational terms. Even if we assume the input string can be up to a few million characters, a single linear scan over the string is sufficient. That means any solution running in O(n) time is already optimal, since we must at least read the input once. Anything more complex than that would be unnecessary overhead.

The main edge cases are all about boundary length behavior. A username of length exactly 5 should be accepted, and a username of length exactly 12 should also be accepted. A string shorter than 5, such as "abc" with length 3, must be rejected. Similarly, a string longer than 12, such as "abcdefghijklmnop", must be rejected.

A subtle pitfall comes from input formatting. If the input contains trailing newline characters or spaces, a naive length check without stripping could miscount the effective username length. For example, reading raw input and forgetting to remove the newline can shift a valid length by one character.

## Approaches

The brute-force approach in this setting is indistinguishable from the optimal approach because the problem has no structure beyond a single measurement. We simply compute the length of the string and compare it against the allowed range. The correctness comes from the definition of the task itself: validity is entirely determined by whether the length lies in a fixed interval.

A more naive misunderstanding might involve iterating through the string and performing unnecessary checks per character, or attempting to simulate validation rules character by character. That would still be O(n), but it introduces no benefit since no character-level constraints exist.

The key observation is that the entire problem reduces to a single scalar property of the input. Once that is recognized, the solution becomes a direct comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (character-by-character validation) | O(n) | O(1) | Accepted |
| Optimal (direct length check) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

### Optimal approach

1. Read the input string representing the username. The string may include a trailing newline depending on input handling, so it is important to treat it consistently.
2. Remove trailing newline or whitespace characters if they are not part of the actual username. This ensures the measured length corresponds exactly to the logical username.
3. Compute the length of the cleaned string.
4. Compare the length against the valid range [5, 12].
5. Output "YES" if the length lies within the range, otherwise output "NO".

### Why it works

The validity condition depends only on a single numerical attribute of the input, its length. No other property of the string influences the result. Because length is invariant under any rearrangement of characters and independent of content, checking it directly is both necessary and sufficient. Any correct solution must compute or infer this length, and once it is known, the decision is deterministic.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().rstrip("\n")

if 5 <= len(s) <= 12:
    print("YES")
else:
    print("NO")
```

The implementation reads the username in a single operation and immediately normalizes it by removing the trailing newline. This avoids a common off-by-one error where the newline character is accidentally counted as part of the username.

The decision logic is a direct interval check. The bounds are inclusive, so both endpoints 5 and 12 are explicitly allowed.

## Worked Examples

### Example 1

Input:

```
abcde
```

| Step | String | Length | Condition |
| --- | --- | --- | --- |
| Read input | abcde | - | - |
| Strip newline | abcde | - | - |
| Compute length | abcde | 5 | - |
| Check range | - | 5 | 5 ≤ 5 ≤ 12 true |

Output:

```
YES
```

This case demonstrates the lower boundary being accepted. A string of exactly five characters is valid.

### Example 2

Input:

```
abcdefghijklmn
```

| Step | String | Length | Condition |
| --- | --- | --- | --- |
| Read input | abcdefghijklmn | - | - |
| Strip newline | abcdefghijklmn | - | - |
| Compute length | abcdefghijklmn | 14 | - |
| Check range | - | 14 | 5 ≤ 14 ≤ 12 false |

Output:

```
NO
```

This case demonstrates rejection when the length exceeds the upper bound. Even though the input is otherwise well-formed, length alone determines invalidity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Reading the input requires scanning all characters once |
| Space | O(1) | Only a single string is stored |

The time complexity is optimal because any solution must read the entire input at least once. The memory usage is constant beyond storing the input string itself, which is unavoidable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import builtins
    input = sys.stdin.readline

    s = input().rstrip("\n")
    if 5 <= len(s) <= 12:
        return "YES"
    else:
        return "NO"

# boundary cases
assert run("abcde\n") == "YES", "lower bound"
assert run("abcd\n") == "NO", "below lower bound"
assert run("abcdefghijkl\n") == "YES", "upper bound"
assert run("abcdefghijklm\n") == "NO", "above upper bound"

# minimal and empty-like cases
assert run("\n") == "NO", "empty string"

# typical case
assert run("hello123\n") == "YES", "valid middle case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "abcde" | YES | Lower boundary acceptance |
| "abcd" | NO | Just below minimum length |
| "abcdefghijkl" | YES | Upper boundary acceptance |
| "abcdefghijklm" | NO | Just above maximum length |
| "" | NO | Empty input handling |
| "hello123" | YES | Typical valid username |

## Edge Cases

One important edge case is when the input includes only a newline character. In that situation, the raw input string might appear empty after stripping, resulting in a length of zero. The algorithm correctly rejects it because zero is outside the valid interval [5, 12].

Another edge case is when the username is exactly at a boundary. For example, "abcde" has length 5. The algorithm computes length as 5 and directly compares it to the lower bound, correctly accepting it without any special casing.

A third case is overly long usernames. For instance, "abcdefghijklmnop" has length 16. After computing the length, the comparison fails against the upper bound 12, and the algorithm rejects it immediately. No additional logic is needed because the condition fully captures validity.
