---
title: "CF 104992D - \u0421\u043a\u043e\u043b\u044c\u043a\u043e \u043e\u0448\u0438\u0431\u043e\u043a?"
description: "The training process produces a sequence of exercises. Each exercise has a “correct answer” provided by the owl and a response written by Grisha. The same exercise may appear multiple times, because if Grisha’s answer is not accepted, the owl repeats that exercise later."
date: "2026-06-28T04:27:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104992
codeforces_index: "D"
codeforces_contest_name: "qual VKOSHP Junior 24"
rating: 0
weight: 104992
solve_time_s: 61
verified: false
draft: false
---

[CF 104992D - \u0421\u043a\u043e\u043b\u044c\u043a\u043e \u043e\u0448\u0438\u0431\u043e\u043a?](https://codeforces.com/problemset/problem/104992/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** no  

## Solution
## Problem Understanding

The training process produces a sequence of exercises. Each exercise has a “correct answer” provided by the owl and a response written by Grisha. The same exercise may appear multiple times, because if Grisha’s answer is not accepted, the owl repeats that exercise later.

For every appearance, we are given two strings: Grisha’s answer first, then the correct answer. Even though the strings may differ slightly in formatting, the acceptance rule is lenient: differences in letter case, punctuation, and word order are ignored, and minor spelling variations are treated as irrelevant according to the same normalization idea. In practice, this means two answers should be considered equivalent if they consist of the same set of words after removing punctuation and case differences, and word order no longer matters.

The task is not to count mismatches per attempt. Instead, we must count how many distinct exercises Grisha failed on the very first time they appeared. Once an exercise is answered correctly for the first time, any later repetitions of that same exercise are irrelevant for the answer.

The key observation is that the identity of an exercise is determined by its correct answer after normalization, because the same task always comes with the same correct solution string. Therefore, we only care about the first time each normalized correct answer appears and whether Grisha’s normalized response matches it.

The constraints allow up to 40,000 attempts and total input size up to 200,000 characters. This rules out any solution that repeatedly compares strings in quadratic fashion. A linear or near-linear preprocessing per string is sufficient, but repeated sorting of large structures without care would still pass due to small total length, as long as we aggregate correctly.

A subtle edge case arises when the same exercise appears multiple times and is first answered incorrectly, then later correctly. For example, if an exercise “A” appears as incorrect first, then later appears again, we must still count it only once. Another edge case is that two strings that look different superficially may actually represent the same answer under normalization, so direct string comparison would incorrectly count errors.

## Approaches

A brute-force interpretation would treat every pair independently and directly compare the two strings under a custom equivalence rule. For each of the n pairs, we would normalize both strings by lowercasing, stripping punctuation, splitting into words, sorting them, and then comparing. This is already acceptable in terms of complexity because total input size is small, but a naive implementation might accidentally reprocess the same correct answer multiple times or attempt repeated normalization in a nested way, leading to unnecessary overhead.

The key structural insight is that each exercise is uniquely identified by its correct answer after normalization. Since repeated occurrences of the same task always reuse the same correct string, we can group attempts by that identifier. We only need to know whether the first occurrence for each identifier was correct or not.

This reduces the problem to maintaining a dictionary keyed by normalized correct answers. For each new pair, we compute a canonical representation of both strings and compare them. If the task has not been seen before, we decide whether to increment the answer based on correctness and then mark it as seen. Later occurrences are ignored.

| Approach | Time Complexity | Space Complexity | Verdict |

|---|---|---|

| Brute Force per pair comparison only | O(total length log words) | O(1) extra | Accepted |

| Hash by normalized correct answer | O(total length log words) | O(total words) | Accepted |

## Algorithm Walkthrough

1. Read the number of attempts n, then process 2n lines as n pairs of (Grisha’s answer, correct answer). Each pair corresponds to one submission attempt.
2. For each string, convert it into a canonical form by extracting words, converting them to lowercase, and sorting the resulting list of words. This transformation removes sensitivity to punctuation, capitalization, and word order.
3. Construct a key for the correct answer using this canonical form. This key represents the identity of the exercise.
4. Maintain a dictionary that stores whether we have already processed this exercise and whether its first appearance was correct or not.
5. When encountering a new exercise key for the first time, compare the canonical forms of Grisha’s answer and the correct answer. If they differ, increment the error counter.
6. Mark the exercise as seen so future repetitions are ignored.

The core idea is that the first occurrence is the only one that can contribute to the answer. Any later repetition cannot affect the count because the exercise is already resolved.

### Why it works

The canonical representation collapses all equivalent answers into identical strings. Since all repetitions of the same exercise share the same correct answer, they share the same canonical key. The dictionary ensures that only the first occurrence of each key is evaluated, so each exercise contributes at most one decision to the final count. This guarantees correctness because the problem asks about first-attempt correctness per distinct exercise, not per appearance.

## Python Solution

```python
import sys
import re
input = sys.stdin.readline

def normalize(s: str):
    words = re.findall(r"[a-zA-Z]+", s.lower())
    words.sort()
    return " ".join(words)

n = int(input())
seen = {}
errors = 0

for _ in range(n):
    grisha = input().rstrip("\n")
    correct = input().rstrip("\n")

    key = normalize(correct)
    if key not in seen:
        if normalize(grisha) != key:
            errors += 1
        seen[key] = True

print(errors)
```

The solution builds a canonical representation for both the student’s answer and the correct answer using the same normalization routine. The regular expression extracts words while ignoring punctuation and spacing artifacts. Sorting ensures that word order differences do not affect equality. A dictionary tracks whether we have already processed a given exercise, ensuring only the first occurrence contributes to the answer.

A common mistake is to compare raw strings or only lowercase versions, which fails when word order changes or punctuation is inserted. Another is forgetting to deduplicate repeated tasks, which would overcount errors.

## Worked Examples

### Example trace

Input consists of four attempts forming two exercises, where one repeats after failure.

| Step | Grisha | Correct | Normalized Correct | First seen? | Match? | Errors |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Who possted this photo | Who posted this photo | this photo posted who | yes | no | 1 |
| 2 | You are welcome | You are welcome | are you welcome | yes | yes | 1 |
| 3 | Who posted this foto | Who posted this photo | this photo posted who | no | ignored | 1 |
| 4 | Who posted this phota | Who posted this photo | this photo posted who | no | ignored | 1 |

This trace shows that only the first occurrence of the first exercise matters. Even though later appearances are incorrect or corrected, they do not affect the final count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total length log k) | Each string is tokenized and sorted by words, and total characters across all strings is bounded by 200k |
| Space | O(total words) | Storage for normalization and tracking seen exercises |

The complexity fits comfortably within limits because both n and total input size are small, and each string is processed independently with lightweight transformations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    import re

    def norm(s):
        w = re.findall(r"[a-zA-Z]+", s.lower())
        w.sort()
        return " ".join(w)

    seen = {}
    ans = 0

    for _ in range(n):
        g = input().rstrip("\n")
        c = input().rstrip("\n")
        k = norm(c)
        if k not in seen:
```
