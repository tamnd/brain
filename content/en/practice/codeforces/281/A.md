---
title: "CF 281A - Word Capitalization"
description: "The task is to take a single word consisting of English letters and make sure its first character is uppercase. The rest of the letters must remain exactly as they are in the input. For example, given the input \"apple\", the output should be \"Apple\"."
date: "2026-06-05T09:13:28+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 281
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 172 (Div. 2)"
rating: 800
weight: 281
solve_time_s: 283
verified: true
draft: false
---

[CF 281A - Word Capitalization](https://codeforces.com/problemset/problem/281/A)

**Rating:** 800  
**Tags:** implementation, strings  
**Solve time:** 4m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to take a single word consisting of English letters and make sure its first character is uppercase. The rest of the letters must remain exactly as they are in the input. For example, given the input "apple", the output should be "Apple". If the input already begins with an uppercase letter, such as "Apple", the output should remain unchanged. Inputs may mix lowercase and uppercase letters, like "ApPLe", in which case only the first character matters for modification.

The constraints are straightforward: the word is non-empty and no longer than 103 characters. This is a very small input size, so any algorithm that inspects the characters sequentially or performs constant-time string operations will run well within the 2-second limit. There is no need for heavy optimizations; even a naive approach will complete in microseconds.

Edge cases arise when the first character is already uppercase, when the word is a single letter, or when the first character is lowercase and the rest are a mix of uppercase and lowercase letters. For instance, an input of "a" should produce "A". An input of "Zebra" should remain "Zebra". If a careless implementation converts the entire word to uppercase, it would incorrectly transform "aPpLe" into "APPLE" rather than "APpLe".

## Approaches

The simplest way to solve the problem is to manually inspect the first character of the string. If it is lowercase, convert it to uppercase and then concatenate it with the rest of the string unchanged. This works because string indexing and concatenation are constant-time operations for such small lengths. This brute-force approach is both correct and fast for the input size, with only a handful of operations.

A slightly different perspective is using built-in string functions like Python’s `str.capitalize()`. However, `str.capitalize()` converts the first character to uppercase but also forces all other characters to lowercase, which is not acceptable here. This demonstrates why reading documentation carefully matters: a standard library function that seems to do "capitalization" may have side effects that break correctness.

The optimal approach is therefore very simple: convert only the first character to uppercase and leave the rest unchanged. This exploits the small fixed structure of the problem - we only care about one character at a time, and the remainder of the string does not need inspection or modification. No iteration over the entire string is needed, beyond slicing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (check and modify first character manually) | O(1) | O(1) | Accepted |
| Using `str.capitalize()` | O(n) | O(n) | Incorrect for mixed-case inputs |
| Optimal (uppercase first character, concatenate remainder) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input word and remove any trailing newline or whitespace. This ensures we are only working with the actual letters.
2. Extract the first character of the word. This character is the only one that may need modification.
3. Convert the first character to uppercase. In Python, this can be done with the `upper()` method.
4. Concatenate the uppercase first character with the substring consisting of all remaining characters in the word, starting from index 1. This preserves the original casing of the rest of the word.
5. Print the resulting string.

This works because the invariant is simple: the first character is guaranteed to be uppercase, and the remainder of the string remains exactly as in the input. Since string slicing preserves order and content, no information is lost, and the algorithm always produces the correctly capitalized word.

## Python Solution

```python
import sys
input = sys.stdin.readline

word = input().strip()
capitalized = word[0].upper() + word[1:]
print(capitalized)
```

The code first strips any trailing newline using `strip()` to ensure only letters remain. Then it accesses `word[0]` to isolate the first character and applies `upper()`. Concatenation with `word[1:]` preserves all remaining letters exactly as they were. Finally, the result is printed. This implementation handles single-character words correctly because slicing `word[1:]` on a one-character string produces an empty string, so concatenation works without errors.

## Worked Examples

Input: "ApPLe"

| Step | word | first character | remainder | capitalized |
| --- | --- | --- | --- | --- |
| 1 | "ApPLe" | "A" | "pPLe" | "A" + "pPLe" |
| 2 | Output | "ApPLe" |  |  |

This shows that no modification occurs if the first character is already uppercase.

Input: "apple"

| Step | word | first character | remainder | capitalized |
| --- | --- | --- | --- | --- |
| 1 | "apple" | "a" | "pple" | "A" + "pple" |
| 2 | Output | "Apple" |  |  |

This demonstrates converting the first letter while leaving the rest unchanged.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only the first character is modified and the rest is sliced without iteration. Maximum string length is 103. |
| Space | O(1) | No extra space proportional to input; only one new string is created. |

Given the constraints, this solution fits comfortably within the time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    word = input().strip()
    return word[0].upper() + word[1:]

# provided sample
assert run("ApPLe\n") == "ApPLe", "sample 1"

# custom cases
assert run("apple\n") == "Apple", "lowercase first letter"
assert run("z\n") == "Z", "single character lowercase"
assert run("Z\n") == "Z", "single character uppercase"
assert run("aPpLe\n") == "APpLe", "mixed case first letter lowercase"
assert run("AbcDEfG\n") == "AbcDEfG", "already capitalized"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "apple" | "Apple" | lowercase first letter |
| "z" | "Z" | single-character lowercase |
| "Z" | "Z" | single-character uppercase |
| "aPpLe" | "APpLe" | mixed-case first letter lowercase |
| "AbcDEfG" | "AbcDEfG" | already capitalized |

## Edge Cases

For a single-character lowercase word like "z", the algorithm accesses `word[0]`, applies `upper()`, resulting in "Z", and concatenates with `word[1:]`, which is empty. The output is correct.

For a single-character uppercase word like "Z", `word[0].upper()` leaves it as "Z" and concatenation with `word[1:]` (empty) does not change it.

For a mixed-case input like "aPpLe", the first character is converted to "A" while the rest "PpLe" remains unchanged. This confirms that the algorithm does not erroneously lowercase or modify the remaining letters.
