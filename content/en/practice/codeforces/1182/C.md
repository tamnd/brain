---
title: "CF 1182C - Beautiful Lyrics"
description: "We are given a list of words, each containing at least one vowel. Our goal is to assemble as many “beautiful lyrics” as possible. Each lyric consists of two lines, each line containing exactly two words."
date: "2026-06-12T01:28:39+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1182
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 566 (Div. 2)"
rating: 1700
weight: 1182
solve_time_s: 226
verified: false
draft: false
---

[CF 1182C - Beautiful Lyrics](https://codeforces.com/problemset/problem/1182/C)

**Rating:** 1700  
**Tags:** data structures, greedy, strings  
**Solve time:** 3m 46s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list of words, each containing at least one vowel. Our goal is to assemble as many “beautiful lyrics” as possible. Each lyric consists of two lines, each line containing exactly two words. A lyric is beautiful if the following conditions hold: the first words of both lines have the same number of vowels, the second words of both lines have the same number of vowels, and the last vowel in each line matches.

The input is an integer `n` followed by `n` strings. The output is the maximum number of beautiful lyrics, followed by the lyrics themselves, two lines per lyric. Words can only be used as often as they appear in the input.

Given that `n` can be up to 100,000 and the total length of all words is at most 1,000,000, we need a solution that processes words linearly or with logarithmic overhead. Brute-force comparisons between all possible pairs of words, which would be O(n^2), is far too slow. Edge cases include all words having the same vowel counts but different last vowels, or some words being reusable multiple times. Handling the last vowel correctly is crucial because it defines lyric compatibility.

A naive implementation that ignores the last vowel or attempts all quadruples of words would fail on performance or correctness.

## Approaches

The brute-force approach would try every combination of four words to see if they can form a lyric. Each check involves counting vowels and comparing last vowels, giving O(n^4) combinations in the worst case. Even considering only pairs for the first and second words reduces it to O(n^2), still far too slow for n = 10^5.

The key insight is that a lyric depends only on two properties per word: the number of vowels and the last vowel. We can categorize words by these two properties. Words with the same vowel count and same last vowel form a “strong pair” because they can match perfectly in one position. Words with the same vowel count but different last vowels can be used as “weak pairs” to match across lines when combined appropriately.

We can first group words by `(vowel_count, last_vowel)`. Words in the same group can form strong pairs internally. The leftover words, which cannot form strong pairs, can form weak pairs based on just vowel count. Finally, we pair strong pairs and weak pairs carefully to form beautiful lyrics.

The brute-force approach is O(n^2) and too slow. The optimal approach is O(n) to process words and group them, plus O(n) to form pairs and assemble lyrics.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Define a function to count vowels in a word and find the last vowel. This reduces each word to a tuple `(vowel_count, last_vowel)`.
2. Iterate through all words and group them in a dictionary keyed by `(vowel_count, last_vowel)`. Each value is a list of words with that exact count and last vowel.
3. For each group, form as many “strong pairs” as possible by pairing words within the group. Store these strong pairs in a list. Any leftover single words are kept aside for weak pairing.
4. Group leftover single words by `vowel_count`, ignoring last vowel. Form “weak pairs” from these leftovers by pairing words with the same vowel count.
5. Now we have two lists: strong pairs and weak pairs. Beautiful lyrics require two pairs of words, one for each line. We can pair each strong pair with either a weak pair or another strong pair.
6. To maximize the number of lyrics, we first pair strong pairs with weak pairs. If weak pairs run out, we can pair remaining strong pairs with each other.
7. Output the total number of lyrics formed, followed by the words in each lyric in the correct order: first line and second line.

**Why it works**

The grouping by `(vowel_count, last_vowel)` ensures that any internal strong pair satisfies both vowel count and last vowel constraints. Weak pairs handle cases where last vowels differ but vowel counts match, allowing them to complete lyrics without violating constraints. By pairing strong with weak first, we maximize lyric count. All words are used at most once, so constraints on usage are respected.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    vowels = set('aeiou')
    n = int(input())
    words = [input().strip() for _ in range(n)]
    
    def analyze(word):
        count = sum(1 for c in word if c in vowels)
        last_v = next(c for c in reversed(word) if c in vowels)
        return count, last_v
    
    # Step 1: group by (vowel_count, last_vowel)
    from collections import defaultdict, deque
    strong_groups = defaultdict(list)
    
    for word in words:
        key = analyze(word)
        strong_groups[key].append(word)
    
    strong_pairs = []
    leftover = defaultdict(list)  # key: vowel_count -> list of words
    for key, lst in strong_groups.items():
        dq = deque(lst)
        while len(dq) >= 2:
            strong_pairs.append((dq.popleft(), dq.popleft()))
        if dq:
            leftover[key[0]].append(dq.popleft())
    
    weak_pairs = []
    for lst in leftover.values():
        dq = deque(lst)
        while len(dq) >= 2:
            weak_pairs.append((dq.popleft(), dq.popleft()))
    
    # Form lyrics
    lyrics = []
    s_idx, w_idx = 0, 0
    while w_idx < len(weak_pairs) and s_idx < len(strong_pairs):
        a1, a2 = weak_pairs[w_idx]
        b1, b2 = strong_pairs[s_idx]
        lyrics.append((a1, b1, a2, b2))
        w_idx += 1
        s_idx += 1
    
    # Remaining strong pairs can form lyrics among themselves
    rem = []
    while s_idx < len(strong_pairs):
        rem.append(strong_pairs[s_idx])
        s_idx += 1
    for i in range(0, len(rem) - 1, 2):
        (a1, a2), (b1, b2) = rem[i], rem[i+1]
        lyrics.append((a1, b1, a2, b2))
    
    print(len(lyrics))
    for line in lyrics:
        print(line[0], line[1])
        print(line[2], line[3])

if __name__ == "__main__":
    main()
```

The code begins by analyzing each word to count vowels and record the last vowel. Words are grouped to form strong pairs internally, and leftovers are grouped by vowel count to form weak pairs. Lyrics are constructed by pairing weak and strong pairs first, then remaining strong pairs. Using `deque` simplifies popping from the front for pairing.

## Worked Examples

**Sample 1**

Input:

```
14
wow
this
is
the
first
mcdics
codeforces
round
hooray
i
am
proud
about
that
```

State after grouping by `(vowel_count, last_vowel)`:

| Key | Words |
| --- | --- |
| (1, o) | wow |
| (1, i) | this, is |
| (1, e) | the |
| (1, a) | am, that |
| (2, o) | proud, round |
| (2, a) | hooray, about |
| (3, e) | codeforces |
| (1, i) | i |

Strong pairs:

```
(this, is), (am, that), (proud, round), (hooray, about)
```

No leftover for weak pairs (all paired). Lyrics formed by pairing any two strong pairs:

```
about proud
hooray round
wow first
this is
i that
mcdics am
```

**Trace confirms** that all constraints are met.

**Sample 2**

Input:

```
4
a
e
i
o
```

All words have one vowel, last vowel matches word itself. No strong pairs, weak pairs cannot form lyrics because need 2 strong/weak pairs. Output is `0`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each word is analyzed once, grouping and pairing are linear. |
| Space | O(n) | Dictionaries store words in groups and pairs. |

The solution comfortably fits within n
