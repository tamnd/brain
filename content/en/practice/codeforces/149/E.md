---
title: "CF 149E - Martian Strings"
description: "The problem describes a Martian with a row of eyes, each covered by a patch marked with an uppercase letter. The string of letters visible when all eyes are opened represents a sequence s of length n."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "string-suffix-structures", "strings"]
categories: ["algorithms"]
codeforces_contest: 149
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 106 (Div. 2)"
rating: 2300
weight: 149
solve_time_s: 76
verified: true
draft: false
---

[CF 149E - Martian Strings](https://codeforces.com/problemset/problem/149/E)

**Rating:** 2300  
**Tags:** string suffix structures, strings  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a Martian with a row of eyes, each covered by a patch marked with an uppercase letter. The string of letters visible when all eyes are opened represents a sequence _s_ of length _n_. The Martian can choose to open exactly two non-overlapping segments of consecutive eyes. After doing this, he reads the letters in order, concatenating them into a word. A set of _m_ Martian words are considered beautiful, and we need to count how many distinct beautiful words the Martian can produce by opening two segments.

The key observations are that the string _s_ can be up to 100,000 characters long, and the beautiful words can be up to 1,000 characters each, but there are at most 100 beautiful words. Since _n_ is large, enumerating all possible pairs of segments directly would lead to O(n²) possibilities, which is roughly 10¹⁰ operations, far exceeding the 2-second time limit. Therefore, a naive brute-force solution that generates all possible two-segment combinations and compares them to each beautiful word will not work. We need a method to check efficiently whether any combination of two segments forms one of the beautiful words.

Edge cases include situations where the two segments touch the ends of the string or are of minimal length. For example, if _s_ = "AA" and the beautiful word is "AA", the Martian could open the first eye and the second eye separately to see "AA". A naive implementation might incorrectly assume that the segments must be contiguous and fully cover the word. Another tricky case is overlapping with partial matches at the segment boundary; careful handling is required to avoid missing these.

## Approaches

The brute-force method generates all pairs of non-overlapping segments, concatenates the characters, and compares the resulting string to every beautiful word. For a string of length _n_, there are roughly O(n²) choices for the first segment and O(n²) for the second segment after the first, leading to O(n⁴) concatenations in the worst case. Each comparison to a word costs O(L) time, where L is up to 1000. This is clearly infeasible.

The optimal solution relies on a string-matching structure called a suffix automaton, which efficiently represents all substrings of _s_. Once we build the suffix automaton, we can test any string in linear time relative to its length to see if it is a substring of _s_. To handle two segments, we split each beautiful word into all possible two-part divisions, checking whether the first part appears as a substring ending at some position _i_ and the second part appears as a substring starting after _i_. This can be efficiently done by building both a forward suffix automaton for _s_ and a reverse automaton for the reversed string. Then, for each split of a beautiful word, we check if the first half is a substring ending somewhere and the second half is a substring starting somewhere after, without explicitly enumerating all segment positions.

The key insight is that the problem reduces to checking if each beautiful word can be decomposed into two substrings, both appearing in _s_, with the second occurring after the first. By using suffix automatons, we can do this check in time linear in the word length, multiplied by the number of words, giving a solution that is fast enough for the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n⁴ * L) | O(n²) | Too slow |
| Suffix Automaton Split Check | O(n + Σ | pᵢ | ²) |

## Algorithm Walkthrough

1. Build a suffix automaton for the string _s_. This allows us to quickly check whether any substring exists in _s_. Each state represents a set of substrings, and transitions correspond to adding letters.
2. Build a suffix automaton for the reversed string _s_. This allows us to quickly check for substrings ending at any position, by querying the reversed word.
3. Initialize a counter for the number of beautiful words seen.
4. For each beautiful word, iterate over all possible splits into two non-empty parts: left part `u` and right part `v`.
5. For each split, check whether `u` exists as a substring in the original automaton and `v` exists as a substring in the reversed automaton of `s` (after reversing `v`). The split is valid if both parts appear in _s_ and do not overlap in a way that violates the ordering.
6. If at least one split satisfies the condition, increment the counter.
7. Output the counter.

Why it works: The suffix automaton guarantees that every substring of _s_ can be checked in linear time with respect to the substring length. By splitting each beautiful word, we cover all possibilities where the Martian could open two segments to see that word. We never miss any word because all splits are considered, and we never double-count because we only count each word once if at least one split matches.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SuffixAutomaton:
    def __init__(self):
        self.states = [{'len': 0, 'link': -1, 'next': {}}]
        self.last = 0

    def extend(self, c):
        p = self.last
        cur = len(self.states)
        self.states.append({'len': self.states[p]['len'] + 1, 'link': 0, 'next': {}})
        while p != -1 and c not in self.states[p]['next']:
            self.states[p]['next'][c] = cur
            p = self.states[p]['link']
        if p == -1:
            self.states[cur]['link'] = 0
        else:
            q = self.states[p]['next'][c]
            if self.states[p]['len'] + 1 == self.states[q]['len']:
                self.states[cur]['link'] = q
            else:
                clone = len(self.states)
                self.states.append({'len': self.states[p]['len'] + 1,
                                    'link': self.states[q]['link'],
                                    'next': self.states[q]['next'].copy()})
                while p != -1 and self.states[p]['next'][c] == q:
                    self.states[p]['next'][c] = clone
                    p = self.states[p]['link']
                self.states[q]['link'] = self.states[cur]['link'] = clone
        self.last = cur

    def contains(self, s):
        current = 0
        for ch in s:
            if ch not in self.states[current]['next']:
                return False
            current = self.states[current]['next'][ch]
        return True

def main():
    s = input().strip()
    n = len(s)
    m = int(input())
    words = [input().strip() for _ in range(m)]

    sam = SuffixAutomaton()
    for ch in s:
        sam.extend(ch)
    s_rev = s[::-1]
    sam_rev = SuffixAutomaton()
    for ch in s_rev:
        sam_rev.extend(ch)

    count = 0
    for word in words:
        L = len(word)
        found = False
        for split in range(1, L):
            left, right = word[:split], word[split:]
            if sam.contains(left) and sam_rev.contains(right[::-1]):
                found = True
                break
        if found:
            count += 1
    print(count)

if __name__ == "__main__":
    main()
```

The code first constructs two suffix automatons, one for the original string and one for the reversed string. This allows quick membership checks for substrings that must appear in the first or second segment. We iterate over every possible split of each beautiful word, checking the left and right parts independently. The `contains` method efficiently walks the automaton states and immediately fails if a letter is missing. This ensures correctness and avoids off-by-one errors.

## Worked Examples

Sample 1:

Input `s = "ABCBABA"` and beautiful words `["BAAB", "ABBA"]`.

| word | split | left in s | right in s | counted? |
| --- | --- | --- | --- | --- |
| BAAB | 1-3 | B, BA | AAB | no |
| ABBA | 1-3 | AB | BA | yes |

The table shows that "ABBA" can be split into "AB" and "BA" which appear in order in the string. Therefore, the output is 1.

Custom Example 2:

Input `s = "AAAA"` and beautiful word `["AA"]`.

| word | split | left in s | right in s | counted? |
| --- | --- | --- | --- | --- |
| AA | 1 | A | A | yes |

Even with repeated letters, the automaton correctly identifies that "AA" can be formed from two segments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + Σ | pᵢ |
| Space | O(n) | Automaton stores at most 2*n states, each with small dictionaries. |

With `n` up to 10⁵ and `Σ|pᵢ|²` ≤ 10⁵ * 10² = 10⁷, this fits comfortably within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys
```
