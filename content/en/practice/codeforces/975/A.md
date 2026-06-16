---
title: "CF 975A - Aramic script"
description: "Each word in the input is meant to describe an object, but the language has a normalization rule: two words represent the same object if they contain exactly the same set of distinct letters, ignoring how many times each letter appears and ignoring order."
date: "2026-06-17T01:33:04+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 975
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 478 (Div. 2)"
rating: 900
weight: 975
solve_time_s: 71
verified: true
draft: false
---

[CF 975A - Aramic script](https://codeforces.com/problemset/problem/975/A)

**Rating:** 900  
**Tags:** implementation, strings  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

Each word in the input is meant to describe an object, but the language has a normalization rule: two words represent the same object if they contain exactly the same set of distinct letters, ignoring how many times each letter appears and ignoring order.

So instead of treating words as strings, we are really grouping them by their unique character sets. For example, “a”, “aa”, and “aaaa” all reduce to the same representation because they all contain only the letter “a”. Similarly, “ab”, “baba”, and “aabb” all reduce to the same object because their distinct letters are `{a, b}`.

The task is to count how many distinct such letter-sets appear among all given words.

The constraints are small enough that we can afford to process each word independently and build a representation of its letter set directly. There are at most 1000 words, and each word has length at most 1000, so a straightforward scan over all characters results in at most 10^6 character operations, which is comfortably fast in Python.

A subtle issue arises if we try to use the raw word as the key. Two words like “ab” and “baab” are different strings but represent the same object, so treating strings directly would overcount. Another potential mistake is counting permutations as distinct; for example, “abc”, “cba”, and “bca” are all identical objects under the rules.

The main edge case is heavy repetition of letters. A word like “aaaaaaa” must collapse to a single representative, and if this normalization step is missed, the answer will be inflated.

## Approaches

A brute-force interpretation would compare every word against every other word, checking whether they define the same object. To do this comparison, we would compute the set of characters for each pair and compare them. If there are n words, each comparison costs up to O(26) or O(length), and doing this for all pairs leads to O(n² · k), which is unnecessary but still borderline acceptable at small limits.

The key observation is that equality of objects is equivalence under “set of characters”. This suggests building a canonical form for each word and inserting it into a hash set. The canonical form can be constructed by collecting all distinct letters and encoding them into a sorted string or a bitmask. Since lowercase English letters are fixed in size (26), a compact and collision-free representation is easy to build.

This reduces the problem to computing one signature per word and counting how many unique signatures exist.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pairwise Comparison | O(n² · k) | O(n · k) | Too slow in general form |
| Canonical Set + Hashing | O(n · k) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all words from input. Each word will be processed independently because object identity depends only on its own characters.
2. For each word, construct a representation of the set of characters it contains. A simple and reliable method is to mark which of the 26 lowercase letters appear in the word. This step compresses the word into a structure that ignores frequency and ordering.
3. Convert this structure into a hashable form. One practical approach is to build a string by concatenating all letters that appear in alphabetical order. This ensures that any two words with the same set produce exactly the same string.
4. Insert this canonical representation into a set. The set automatically removes duplicates, so repeated occurrences of the same object are naturally merged.
5. After processing all words, output the size of the set, which corresponds to the number of distinct objects.

### Why it works

The core invariant is that every word is mapped to a unique canonical form determined solely by its set of characters. Two words map to the same canonical form if and only if they contain exactly the same letters. Since the set only stores canonical forms, it groups all equivalent words together and counts each equivalence class exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    words = input().split()

    seen = set()

    for w in words:
        mask = [0] * 26
        for ch in w:
            mask[ord(ch) - 97] = 1

        key = []
        for i in range(26):
            if mask[i]:
                key.append(chr(i + 97))

        seen.add("".join(key))

    print(len(seen))

if __name__ == "__main__":
    solve()
```

The solution reads all words in one pass, then converts each word into a 26-length presence array. This avoids any dependence on word length or character frequency. The alphabetical reconstruction step ensures that permutations like “ab” and “ba” collapse to the same key.

A common implementation pitfall is forgetting to normalize the word at all and inserting raw strings into the set. That would incorrectly treat anagrams as distinct. Another mistake is using a list directly in a set, which is invalid in Python because lists are not hashable.

## Worked Examples

### Example 1

Input:

```
5
a aa aaa ab abb
```

We track the canonical form of each word.

| Word | Character Set | Canonical Key | Seen Set |
| --- | --- | --- | --- |
| a | {a} | a | {a} |
| aa | {a} | a | {a} |
| aaa | {a} | a | {a} |
| ab | {a,b} | ab | {a, ab} |
| abb | {a,b} | ab | {a, ab} |

Final answer is 2.

This confirms that repeated letters and permutations do not affect grouping.

### Example 2

Input:

```
4
abc bca aabb cc
```

| Word | Character Set | Canonical Key | Seen Set |
| --- | --- | --- | --- |
| abc | {a,b,c} | abc | {abc} |
| bca | {a,b,c} | abc | {abc} |
| aabb | {a,b} | ab | {abc, ab} |
| cc | {c} | c | {abc, ab, c} |

Final answer is 3.

This shows how different subsets of letters form distinct objects even when words are permutations or have repetitions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · k) | Each word is scanned once, and each character is processed in constant time |
| Space | O(n) | Each distinct canonical key is stored in a set |

With n ≤ 1000 and total characters ≤ 10^6, the solution easily fits within both time and memory limits. The 26-letter alphabet further ensures constant-factor overhead for normalization.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    words = input().split()

    seen = set()

    for w in words:
        mask = [0] * 26
        for ch in w:
            mask[ord(ch) - 97] = 1

        key = []
        for i in range(26):
            if mask[i]:
                key.append(chr(i + 97))

        seen.add("".join(key))

    return str(len(seen))

# provided sample
assert run("5\na aa aaa ab abb") == "2"

# all identical
assert run("3\na aa aaa") == "1"

# all distinct single letters
assert run("3\na b c") == "3"

# permutations
assert run("3\nab ba ab") == "1"

# mixed case
assert run("4\nabc bca aabb cc") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| a aa aaa | 1 | repetition collapse |
| a b c | 3 | independent single-letter objects |
| ab ba ab | 1 | permutation equivalence |
| abc bca aabb cc | 3 | mixed subsets and grouping |

## Edge Cases

One important edge case is extreme repetition inside a word. For input like “aaaaa”, the algorithm marks only one letter in the mask, so the canonical key becomes “a”. This ensures repeated characters do not inflate the representation.

Another edge case is many anagrams. For example, “abc”, “bca”, and “cab” all produce the same mask and therefore the same key. The set correctly collapses them into one entry because every permutation maps to identical sorted-letter representation.

A final edge case is when all words are identical in structure but differ in length, such as “a”, “aa”, “aaa”, “aaaa”. Each produces the same canonical key “a”, so only one entry remains in the set, producing the correct count of 1.
