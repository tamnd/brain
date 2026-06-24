---
title: "CF 105227A - LLPS"
description: "We are given a single string made of lowercase letters. From this string we may delete characters while preserving order, producing any subsequence."
date: "2026-06-24T16:30:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105227
codeforces_index: "A"
codeforces_contest_name: "CPG Training Contest - 1"
rating: 0
weight: 105227
solve_time_s: 315
verified: false
draft: false
---

[CF 105227A - LLPS](https://codeforces.com/problemset/problem/105227/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a single string made of lowercase letters. From this string we may delete characters while preserving order, producing any subsequence. Among all such subsequences, we want one that is a palindrome and, among all palindromic subsequences, we want the lexicographically largest.

The string length is at most 10, so the input is tiny. That immediately changes the nature of the problem: exponential exploration is already feasible, but we should still aim for a clean structural insight rather than brute forcing all subsequences.

Lexicographic order here follows the standard rule: compare from left to right, and the first position where characters differ decides, or if one is a prefix of the other, the longer string is larger.

A naive pitfall is to assume we need to “build” a palindrome greedily from both ends. That fails because optimal choices depend on global structure, not local matching. Another mistake is to think longer always wins; that is false because a longer subsequence might start with a smaller character, losing lexicographically immediately.

A small edge case appears when all characters are distinct. Then every palindrome subsequence has length 1, and the answer is just the maximum character. Another case is when the best answer is not the longest palindrome, as seen in the sample “codeforces” where the answer is “s”.

## Approaches

The brute-force view is straightforward: enumerate all subsequences of the string, check whether each is a palindrome, and keep the best under lexicographic order. There are at most 2ⁿ subsequences. For each, checking palindrome takes O(n), so total complexity is O(n·2ⁿ). With n ≤ 10, this is at most about 10,240 checks, which is perfectly fine in practice.

However, this brute-force approach is conceptually overkill. The structure of palindromic subsequences in a string has a key simplification: any palindrome has matching first and last characters, and lexicographically larger strings prioritize the first character above everything else. So we should first understand what the first character of the answer must be.

If we pick any character c as the first character of the palindrome, then the last character must also be c, and both must come from occurrences of c in the string. The lexicographically largest palindrome must therefore start with the largest possible character that appears at least once. Once we choose such a character c, we can always form a valid palindrome subsequence consisting only of one occurrence of c, or two occurrences of c if there are at least two.

Now compare possibilities. If c appears at least twice, we can form “cc”. Any longer palindrome that starts with c must also start with c and then continue with something between two chosen occurrences. But any interior part must not introduce a character smaller than c at the front, otherwise lexicographic order would not improve. Since c is already the maximum character in the string, nothing can beat a sequence that starts with c and keeps c’s as much as possible, which collapses to repeating c.

Thus the problem reduces to finding the maximum character in the string and counting how many times it appears. If it appears once, answer is that character. If it appears k times, the best palindrome is that character repeated k times, since we can pick all occurrences as a subsequence and it is trivially a palindrome.

This is the key structural collapse: instead of exploring palindromes, we only need frequency of the maximum character.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·2ⁿ) | O(n) | Accepted but unnecessary |
| Frequency of max char | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the string once to determine the largest character present and how many times it occurs.

1. Scan the string and maintain the maximum character seen so far. This is correct because lexicographic optimality depends first on the leading character, so we must maximize it globally.
2. Count how many times this maximum character appears. This matters because repeating the same maximum character preserves both palindrome structure and lexicographic value.
3. Construct a string consisting of this character repeated as many times as it appears in the input.
4. Output this constructed string directly, since it is a valid subsequence and a palindrome.

The non-obvious part is why we are allowed to take all occurrences of the maximum character. Any subsequence made only of identical characters is always a palindrome, since reversing it changes nothing. Removing any occurrence would only shorten the string without improving lexicographic order, since all characters are equal. So maximality reduces to maximal length among equal-starting candidates.

### Why it works

Any palindromic subsequence has a first character, and lexicographic order is decided immediately by that character unless both candidates share it. Therefore the optimal solution must start with the maximum possible character in the string. Once restricted to that character, no other character can improve lexicographic order, and adding only identical characters preserves both validity and optimality. This forces the answer to be the multiset of all occurrences of the maximum character arranged as a palindrome, which is simply a repetition of that character.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

mx = max(s)
cnt = s.count(mx)

print(mx * cnt)
```

The solution first computes the maximum character using Python’s built-in comparison over characters, which works directly because ASCII order matches lexicographic order. Then it counts occurrences of that character. The output is constructed by repeating the character.

A subtle point is that we do not need to explicitly verify palindromicity, because any string consisting of a single repeated character is always a palindrome. Another subtlety is that we do not need to consider subsequence constraints explicitly: every occurrence of the maximum character can be selected in order, so the repetition is always achievable as a subsequence.

## Worked Examples

Consider “radar”.

We scan and find the maximum character is ‘r’. It appears twice.

| step | max char | count |
| --- | --- | --- |
| r | r | 1 |
| a | r | 1 |
| d | r | 1 |
| a | r | 1 |
| r | r | 2 |

The result is “rr”. This shows that even though “radar” itself is a palindrome, a lexicographically larger subsequence can be formed by focusing only on the dominant character.

Now consider “codeforces”.

The maximum character is ‘s’, appearing once.

| step | max char | count |
| --- | --- | --- |
| c | c | 1 |
| o | o | 1 |
| d | o | 1 |
| e | o | 1 |
| f | o | 1 |
| o | o | 1 |
| r | r | 1 |
| c | r | 1 |
| e | r | 1 |
| s | s | 1 |

The output is “s”, since no repeated character exists to form a longer palindrome.

These traces confirm that the algorithm is purely driven by dominance of the maximum character and ignores all other structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass plus counting occurrences |
| Space | O(1) | only fixed counters and max character |

The input size is at most 10, so even trivial solutions pass easily, but this linear approach generalizes cleanly and avoids any enumeration.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    s = input().strip()
    mx = max(s)
    cnt = s.count(mx)
    return mx * cnt

# provided samples
assert run("radar\n") == "rr"
assert run("bowwowwow\n") == "wwwww"
assert run("codeforces\n") == "s"

# custom cases
assert run("a\n") == "a", "single character"
assert run("abcabc\n") == "cc", "multiple max letters"
assert run("zzxyzz\n") == "zzzz", "all max occurrences used"
assert run("abcd\n") == "d", "strictly increasing letters"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| a | a | minimum length string |
| abcabc | cc | repeated max character selection |
| zzxyzz | zzzz | multiple max occurrences dominate |
| abcd | d | single maximum at end |

## Edge Cases

For a single-character string like “a”, the algorithm identifies ‘a’ as both maximum and only character, producing “a”. The construction still works because repetition count is one, so no special handling is required.

For strings where the maximum character appears many times, such as “zzxyzz”, scanning correctly accumulates all occurrences of ‘z’. Since all are equal, ordering among them does not matter, and the resulting repeated string is always a palindrome and lexicographically maximal among valid subsequences.
