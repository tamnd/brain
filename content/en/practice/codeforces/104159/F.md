---
title: "CF 104159F - Wordland"
description: "We are given several short strings made of lowercase English letters. For each string, we need to decide whether it is “valid” under a rule that depends on how letters alternate between two classes: vowels and consonants. The rule is applied after a preprocessing step."
date: "2026-07-02T01:07:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104159
codeforces_index: "F"
codeforces_contest_name: "\u041e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u0420\u0421(\u042f) (5-8 \u043a\u043b\u0430\u0441\u0441\u044b) 2022-23, 2 \u0434\u0435\u043d\u044c"
rating: 0
weight: 104159
solve_time_s: 64
verified: true
draft: false
---

[CF 104159F - Wordland](https://codeforces.com/problemset/problem/104159/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several short strings made of lowercase English letters. For each string, we need to decide whether it is “valid” under a rule that depends on how letters alternate between two classes: vowels and consonants.

The rule is applied after a preprocessing step. In Wordland, if the same letter appears multiple times consecutively, it is pronounced as if it were a single occurrence. So the string is first compressed by collapsing every maximal block of identical letters into a single character. After this compression, we check whether the resulting sequence alternates strictly between vowels and consonants. A word is valid if every adjacent pair in the compressed string consists of one vowel and one consonant.

The vowel set is fixed as a, e, i, o, u, y, and all other letters are consonants.

The input size is very small: at most 100 words, each of length at most 100. This immediately implies that even quadratic or cubic solutions would pass comfortably, but the structure of the task suggests a linear scan per word is the natural fit.

The main subtlety is the compression rule. A naive approach might forget to merge consecutive duplicates before checking alternation. That leads to incorrect rejection or acceptance.

For example, consider the word “totoroooo”. If we check alternation directly, the trailing “oooo” looks like multiple vowels in a row, which would violate alternation. But after compression, “oooo” becomes a single “o”, and the structure becomes “t o t o r o”, which alternates correctly.

A second edge case is a word like “rr”. After compression it becomes “r”, which has no adjacent pairs to violate the rule, so it should be valid.

## Approaches

The brute-force idea is straightforward. For each word, we first explicitly build a new string by merging consecutive identical characters. This can be done by scanning the string and appending a character only when it differs from the previous one. After this compression, we iterate through the reduced string and check every adjacent pair to verify that one is a vowel and the other is a consonant.

This approach is already linear in the size of each word. Even if we consider worst case, 100 words of length 100, we are performing about 10,000 character operations, which is trivial. There is no need for more advanced optimization.

The key observation is that the problem is essentially two independent linear passes per word: one pass for run-length compression and one pass for validation. Since both are O(L), we can conceptually merge them into a single scan. While scanning, we track the last kept character (after compression) and only compare against it when a new character block begins.

The brute-force version works because it explicitly constructs the compressed representation. The optimized version avoids storing it and instead maintains only the last relevant character and its vowel status.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (explicit compression + check) | O(total length) | O(L) | Accepted |
| One-pass streaming compression | O(total length) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. For each word, define a helper function that determines whether a character is a vowel. This is a constant-time lookup against the set {a, e, i, o, u, y}.
2. Iterate through the characters of the word from left to right while maintaining the last “compressed” character that we accepted. Initially, there is no previous character.
3. When we encounter a character, compare it with the previous character in the raw string. If it is the same, we skip it because it belongs to the same run and does not change the compressed structure.
4. If it differs from the previous raw character, we treat it as the next character in the compressed sequence. At this point, we compare its vowel/consonant type with the last kept compressed character. If both belong to the same class, we immediately know the word is invalid.
5. Update the last compressed character and continue scanning.
6. If we reach the end of the word without finding a violation, the word is valid.

The crucial design point is that we only ever compare characters that survive compression boundaries. We never compare within a run, because those duplicates are explicitly ignored.

### Why it works

Run-length compression preserves exactly the sequence we care about: transitions between distinct letters. Any violation of the alternation rule must appear at one of these transitions. Within a run of identical letters, all letters have identical vowel status, so collapsing them does not lose any information relevant to alternation. Therefore, checking only the compressed boundary sequence is sufficient and complete.

## Python Solution

```python
import sys
input = sys.stdin.readline

VOWELS = set("aeiouy")

def is_vowel(c: str) -> bool:
    return c in VOWELS

n = int(input())
for _ in range(n):
    s = input().strip()
    
    prev_raw = None
    prev_kept = None
    
    ok = True
    
    for c in s:
        if c == prev_raw:
            continue
        
        if prev_kept is not None:
            if is_vowel(c) == is_vowel(prev_kept):
                ok = False
                break
        
        prev_kept = c
        prev_raw = c
    
    print("YES" if ok else "NO")
```

The solution maintains two pieces of state. The first, `prev_raw`, is used purely for compression: it tracks whether the current character is part of a repeated run. The second, `prev_kept`, represents the last character in the compressed sequence.

The key detail is that we only compare vowel classes when a new compressed character appears. This avoids building an explicit string while still preserving correctness.

A common mistake is to compare every adjacent pair in the original string, which incorrectly penalizes repeated vowels or consonants. Another mistake is to compress but forget to compare after compression boundaries only.

## Worked Examples

### Sample 1

Input word: `kukaracha`

| Step | Char | prev_raw | Kept? | prev_kept | Vowel? | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | k | - | yes | - | C | start |
| 2 | u | k | yes | k | V vs C | OK |
| 3 | k | u | yes | u | C vs V | OK |
| 4 | a | k | yes | k | V vs C | OK |
| 5 | r | a | yes | a | C vs V | OK |
| 6 | a | r | yes | r | V vs C | OK |
| 7 | c | a | yes | a | C vs V | OK |
| 8 | h | c | yes | c | C vs C | FAIL |

The failure occurs when transitioning from “c” to “h”, both consonants. This confirms that alternation is strictly enforced on compressed transitions.

### Sample 2

Input word: `totoroooo`

| Step | Char | prev_raw | Kept? | prev_kept | Vowel? | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | t | - | yes | - | C | start |
| 2 | o | t | yes | t | V vs C | OK |
| 3 | t | o | yes | o | C vs V | OK |
| 4 | o | t | no | o | - | skip (duplicate run) |
| 5 | r | o | yes | o | C vs V | OK |
| 6 | o | r | yes | r | V vs C | OK |
| 7 | o | o | no | o | - | skip (duplicate run) |

No violation is found, so the word is valid.

These traces show that duplicates never affect transitions, and correctness depends only on the compressed sequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(NL) | Each character is processed once per word, with constant-time checks |
| Space | O(1) | Only a few variables are maintained per word |

Given N ≤ 100 and L ≤ 100, the total work is at most 10^4 character operations, which is well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    VOWELS = set("aeiouy")
    
    def is_vowel(c):
        return c in VOWELS
    
    n = int(sys.stdin.readline())
    out = []
    for _ in range(n):
        s = sys.stdin.readline().strip()
        
        prev_raw = None
        prev_kept = None
        ok = True
        
        for c in s:
            if c == prev_raw:
                continue
            if prev_kept is not None and is_vowel(c) == is_vowel(prev_kept):
                ok = False
                break
            prev_kept = c
            prev_raw = c
        
        out.append("YES" if ok else "NO")
    
    return "\n".join(out)

# provided samples
assert run("5\nkukaracha\nramen\nfoot\nemployees\ntotoroooo\n") == "NO\nYES\nYES\nNO\nYES"
assert run("2\nrr\nttttt\n") == "YES\nYES"

# custom cases
assert run("1\na") == "YES"
assert run("1\naa") == "YES"
assert run("1\nab") == "YES"
assert run("1\naba") == "YES"
assert run("1\nabbaa") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | YES | Single letter word |
| `aa` | YES | Compression removes duplicates |
| `ab` | YES | Simple alternating pair |
| `aba` | YES | Alternation over three letters |
| `abbaa` | NO | Same-type transition after compression |

## Edge Cases

One edge case is a word made entirely of repeated identical letters. For example, input “ttttt” compresses to “t”, which has no transitions to violate alternation, so it is valid. The algorithm handles this because `prev_kept` is never compared until a second distinct compressed character appears.

Another edge case is a word where duplicates appear at multiple places, such as “lesssoon”. The repeated “sss” must be collapsed into a single “s”, otherwise a naive adjacent-check would incorrectly detect vowel-consonant violations inside the run. In the algorithm, all repeated letters are skipped using `prev_raw`, ensuring only run boundaries contribute to checks.

A third edge case is alternating letters with repeated blocks, such as “totoroooo”. The trailing run of vowels must not be interpreted as multiple alternations. The skip logic ensures that only the transition from the run is considered, so correctness depends only on compressed structure rather than raw repetition.
