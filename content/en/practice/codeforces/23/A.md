---
title: "CF 23A - You're Given a String..."
description: "We are given a string of lowercase letters, and the task is to find the length of the longest substring that occurs at least twice in the string. The repeated occurrences may overlap. The input is a single string of at most 100 characters."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 23
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 23"
rating: 1200
weight: 23
solve_time_s: 115
verified: true
draft: false
---
[CF 23A - You're Given a String...](https://codeforces.com/problemset/problem/23/A)

**Rating:** 1200  
**Tags:** brute force, greedy  
**Solve time:** 1m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string of lowercase letters, and the task is to find the length of the longest substring that occurs at least twice in the string. The repeated occurrences may overlap. The input is a single string of at most 100 characters. The output is a single integer representing the maximum length of such a repeating substring.

Because the string length is small, up to 100, we can afford algorithms that are quadratic in the length of the string. This makes approaches that compare all pairs of substrings feasible. The problem’s edge cases are situations where either no substring repeats, where all characters are the same, or where substrings overlap exactly. For example, the string `aaaa` has a longest repeated substring of length 3 (`aaa`), which can occur overlapping: positions 0-2 and 1-3. A naive approach might fail to handle this overlap correctly if it only considers non-overlapping positions.

Another subtle case is a string with entirely unique letters, such as `abcd`. Here, the correct answer is `0` because no substring repeats, not even single letters.

## Approaches

The simplest approach is brute force. We can generate all possible substrings of the input and count how many times each occurs. For each substring, we slide a window over the string and compare substrings of the same length. If we find a substring that appears at least twice, we record its length and update the maximum. This method is correct because it explicitly examines every candidate substring, but its complexity is O(n³) in the worst case: O(n²) for generating all substrings and O(n) to check occurrences. For n = 100, this is about 1,000,000 operations, which is acceptable given modern CPU speeds, but it is on the slower side and can be optimized.

The key insight is that we do not need to check every substring individually. Instead, we can iterate over possible lengths in decreasing order and check if any substring of that length repeats. Once we find a length that works, we can stop. Checking all substrings of a fixed length can be done in O(n²) time using a set or dictionary to track seen substrings. This reduces the overall complexity to O(n³) in the worst case, but in practice, it is faster because we stop early once the longest repeated substring is found.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Accepted for n ≤ 100 |
| Length-based Set Check | O(n³) worst-case, faster on average | O(n²) | Accepted, simpler to implement |

## Algorithm Walkthrough

1. Determine the length of the input string `n`. Initialize a variable `max_len` to 0. This will store the longest repeating substring length found so far.
2. Loop over candidate substring lengths `l` from 1 to `n-1`. We do not need to check length `n` because a substring of length `n` can only appear once.
3. For each length `l`, initialize an empty set `seen`. This will track all substrings of length `l` we encounter.
4. Slide a window of length `l` over the string from index 0 to `n-l`. Extract the substring at each position.
5. If the substring is already in `seen`, update `max_len` to `l` if `l` is larger than the current `max_len`. Break out of this inner loop because we already found a repeated substring of this length.
6. If the substring is not in `seen`, add it to the set and continue.
7. After all lengths are checked, output `max_len`.

Why it works: The algorithm maintains an invariant that `max_len` is the largest length for which a repeated substring has been found. By checking shorter substrings first, we ensure no valid longer substring is missed. The use of a set guarantees that duplicate substrings are detected efficiently.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
n = len(s)
max_len = 0

for l in range(1, n):
    seen = set()
    for i in range(n - l + 1):
        sub = s[i:i+l]
        if sub in seen:
            max_len = l
            break
        seen.add(sub)

print(max_len)
```

The solution reads the string and iterates over possible substring lengths. The inner loop constructs each substring using slicing. Using a set ensures duplicates are detected in average O(1) time per check. Breaking the inner loop once a repeated substring is found avoids unnecessary work.

## Worked Examples

For `abcd`:

| l | Substrings checked | Seen set | max_len |
| --- | --- | --- | --- |
| 1 | 'a','b','c','d' | {'a','b','c','d'} | 0 |
| 2 | 'ab','bc','cd' | {'ab','bc','cd'} | 0 |
| 3 | 'abc','bcd' | {'abc','bcd'} | 0 |

No substring repeats, so the output is `0`.

For `aaaa`:

| l | Substrings checked | Seen set | max_len |
| --- | --- | --- | --- |
| 1 | 'a','a' | {'a'} | 1 |
| 2 | 'aa','aa' | {'aa'} | 2 |
| 3 | 'aaa','aaa' | {'aaa'} | 3 |

Here the longest repeated substring is `aaa` with overlapping occurrences, giving `max_len = 3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n³) worst-case | Outer loop over lengths O(n), inner loop over positions O(n), substring slicing O(n) |
| Space | O(n²) | Set stores up to n substrings of length n in worst case |

Given n ≤ 100, the solution performs at most 1,000,000 substring checks and fits well within the 2-second limit. Memory usage remains minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = input().strip()
    n = len(s)
    max_len = 0
    for l in range(1, n):
        seen = set()
        for i in range(n - l + 1):
            sub = s[i:i+l]
            if sub in seen:
                max_len = l
                break
            seen.add(sub)
    return str(max_len)

# provided samples
assert run("abcd\n") == "0", "sample 1"
assert run("aaaa\n") == "3", "overlapping repeats"

# custom cases
assert run("abcabc\n") == "3", "entire repeated sequence"
assert run("a\n") == "0", "single character string"
assert run("ababab\n") == "4", "overlapping pattern abab"
assert run("abcdefg\n") == "0", "all unique letters"
assert run("aaaaa\n") == "4", "all same letters, max overlap"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| abcabc | 3 | repeated substring equal to half the string |
| a | 0 | minimum input size |
| ababab | 4 | overlapping repeats |
| abcdefg | 0 | no repeats |
| aaaaa | 4 | maximum overlap |

## Edge Cases

A single-character string like `a` produces `0` because no substring can repeat. The algorithm correctly iterates over lengths starting from 1 and finds no repeated substrings.

For a string like `aaaaa`, the algorithm finds overlapping repeats by checking substrings of increasing length. It correctly detects `aaaa` as the longest repeated substring because `aaaa` occurs at positions 0-3 and 1-4. The set ensures duplicates are caught, and breaking the loop once a repeat is found avoids missing longer substrings.
