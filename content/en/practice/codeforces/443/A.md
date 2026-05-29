---
title: "CF 443A - Anton and Letters"
description: "We are given a single formatted string that represents a set of lowercase English letters. The set is written in a very specific textual form: it starts with an opening brace, ends with a closing brace, and inside the braces letters are listed separated by comma and space."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 443
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 253 (Div. 2)"
rating: 800
weight: 443
solve_time_s: 79
verified: true
draft: false
---

[CF 443A - Anton and Letters](https://codeforces.com/problemset/problem/443/A)

**Rating:** 800  
**Tags:** constructive algorithms, implementation  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single formatted string that represents a set of lowercase English letters. The set is written in a very specific textual form: it starts with an opening brace, ends with a closing brace, and inside the braces letters are listed separated by comma and space. The same letter may appear multiple times because Anton may have mistakenly written duplicates, but mathematically the set should only keep distinct elements.

The task is to determine how many unique letters appear inside this representation. The output is a single integer, the size of the set after duplicates are ignored.

The input length is at most 1000 characters, which means any solution that scans the string a constant number of times is easily fast enough. Even a simple linear pass is sufficient, since 1000 operations is negligible. This immediately rules out nothing substantial, but it does tell us that we should prefer straightforward parsing over anything complicated like backtracking or nested parsing logic.

The main subtlety is not performance but correctness of parsing. The input includes punctuation characters such as braces, commas, and spaces. A naive approach that splits incorrectly or forgets to ignore these symbols may accidentally count them or include empty tokens.

One common failure case is treating every character except braces as a letter. For example, in the string "{a, b}", if we iterate blindly, we might accidentally include the comma and space. Another failure case is splitting only on commas but forgetting that tokens contain leading spaces, producing strings like " b" instead of "b". If not stripped properly, such tokens would be treated as distinct strings and inflate the answer.

## Approaches

A brute-force interpretation of the problem would be to manually extract all substrings between commas, clean them, and insert them into a list. For each extracted token, we would compare it against all previously seen tokens to determine uniqueness. This works because the input is small, but it introduces unnecessary quadratic behavior: for k letters, each lookup can cost O(k), leading to O(k^2) behavior in the worst case. While k is bounded by 1000, this is still overkill and unnecessary given that hashing exists.

The key observation is that we do not need ordering or frequency counts, only uniqueness. A set structure directly models this requirement. As we scan the string, every valid letter can be inserted into a hash set, which handles deduplication in expected O(1) time per insertion. The punctuation characters can simply be ignored during the scan.

The structure of the input guarantees that valid letters are always single lowercase characters, so we never need to parse multi-character tokens. This reduces the problem to a single linear traversal with filtering.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force List + Linear Search | O(n^2) | O(n) | Too slow |
| Set-based Single Pass | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string as a single line. The string contains braces, commas, spaces, and lowercase letters.
2. Initialize an empty set to store distinct letters. The set is used because it automatically ignores duplicates.
3. Iterate through each character in the string.
4. If the character is between 'a' and 'z', insert it into the set. Any other character is ignored because it is structural punctuation.
5. After processing all characters, the size of the set is the number of distinct letters.
6. Output this size.

The reason we can safely ignore everything except lowercase letters is that the format guarantees all meaningful elements are single characters in that range. No other characters contribute to the set content.

### Why it works

The algorithm maintains an invariant that at any point in the scan, the set contains exactly the distinct letters seen so far in the string. Each insertion either adds a new letter or does nothing if it is already present. Since every valid letter appears somewhere in the string, it will be processed exactly once per occurrence, and the set ensures multiplicity does not matter. At the end, the set contains precisely the unique letters in the representation, which matches the definition of the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

seen = set()

for ch in s:
    if 'a' <= ch <= 'z':
        seen.add(ch)

print(len(seen))
```

The solution reads the entire input line once and iterates over it character by character. The condition `'a' <= ch <= 'z'` ensures we only process actual letters and ignore braces, commas, and spaces. The set `seen` accumulates distinct characters efficiently.

A subtle implementation detail is the use of `strip()` when reading input. This removes the trailing newline without affecting internal spaces, which are irrelevant anyway. No splitting is needed, which avoids tokenization pitfalls entirely.

## Worked Examples

### Example 1

Input:

```
{a, b, c}
```

We scan each character and maintain a set.

| Character | Action | Set state |
| --- | --- | --- |
| { | ignore | {} |
| a | add | {a} |
| , | ignore | {a} |
|  | ignore | {a} |
| b | add | {a, b} |
| , | ignore | {a, b} |
|  | ignore | {a, b} |
| c | add | {a, b, c} |
| } | ignore | {a, b, c} |

Final set size is 3.

This trace shows that punctuation never influences the state, and only letters contribute to uniqueness.

### Example 2

Input:

```
{a, a, b, a}
```

| Character | Action | Set state |
| --- | --- | --- |
| { | ignore | {} |
| a | add | {a} |
| , | ignore | {a} |
|  | ignore | {a} |
| a | already exists | {a} |
| , | ignore | {a} |
|  | ignore | {a} |
| b | add | {a, b} |
| , | ignore | {a, b} |
|  | ignore | {a, b} |
| a | already exists | {a, b} |
| } | ignore | {a, b} |

Final answer is 2.

This confirms that duplicates do not affect the final count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once and set insertion is O(1) on average |
| Space | O(1) | At most 26 lowercase letters can be stored |

The input size is at most 1000, so a single pass solution is well within constraints and runs instantly in both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    s = input().strip()
    seen = set()
    for ch in s:
        if 'a' <= ch <= 'z':
            seen.add(ch)
    return str(len(seen))

# provided sample
assert run("{a, b, c}\n") == "3"

# single element
assert run("{a}\n") == "1"

# duplicates only
assert run("{a, a, a}\n") == "1"

# all letters
assert run("{a, b, c, d, e}\n") == "5"

# alternating duplicates
assert run("{a, b, a, c, b, d}\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| {a} | 1 | minimal valid input |
| {a, a, a} | 1 | duplicate handling |
| {a, b, a, c, b, d} | 4 | mixed duplicates and ordering |

## Edge Cases

One edge case is when all letters are identical, such as "{a, a, a}". The algorithm processes every 'a' and inserts it into the set. After the first insertion, subsequent insertions do nothing, so the final set remains {a}, producing output 1.

Another case is when the set contains only one element "{z}". The scan ignores braces and directly adds 'z', resulting in a single-element set.

A final subtle case is spacing variation inside the braces. Even though every comma is followed by a space, the algorithm never relies on token boundaries, so extra spaces are ignored automatically. Only characters in 'a' to 'z' matter, so formatting variations cannot affect correctness.
