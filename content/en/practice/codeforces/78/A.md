---
title: "CF 78A - Haiku"
description: "We are given three lines representing the three phrases of a poem. A valid haiku must contain exactly 5 vowel letters in the first phrase, 7 in the second, and 5 in the third. For this problem, syllables are simplified into vowel counts."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 78
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 70 (Div. 2)"
rating: 800
weight: 78
solve_time_s: 210
verified: true
draft: false
---

[CF 78A - Haiku](https://codeforces.com/problemset/problem/78/A)

**Rating:** 800  
**Tags:** implementation, strings  
**Solve time:** 3m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three lines representing the three phrases of a poem. A valid haiku must contain exactly 5 vowel letters in the first phrase, 7 in the second, and 5 in the third.

For this problem, syllables are simplified into vowel counts. Only the lowercase letters `a`, `e`, `i`, `o`, and `u` are considered vowels. Spaces do not matter, and words may be separated by multiple spaces. Leading and trailing spaces are also allowed.

The task is simply to count vowels in each of the three lines and check whether the counts match the required `5-7-5` pattern.

The constraints are tiny. Each line has length at most 100, so the total input size is at most 300 characters. Even an inefficient solution would easily fit within the time limit. A single pass through each string is more than enough.

The main difficulty is not performance, it is handling formatting correctly. Multiple spaces can appear between words, and there may be spaces at the beginning or end of a line. A solution that tries to split words carelessly may accidentally ignore valid characters or mishandle empty tokens.

Consider this input:

```
on  codeforces  
beta round is running
   a rustling of keys
```

The first line contains multiple spaces and trailing spaces. The correct output is `YES` because spaces do not affect vowel counting.

Another easy mistake is forgetting that only lowercase vowels count. For example:

```
bcdfg
aeiouuu
hello
```

The vowel counts are `0`, `7`, and `2`, so the answer is `NO`.

A careless implementation might also count distinct vowels instead of total vowel occurrences. For example:

```
aaaaa
aeiouae
eeeee
```

The counts are `5`, `7`, and `5`. Every vowel occurrence matters, not just unique letters.

## Approaches

The most direct approach is to process each line character by character and count how many characters belong to the vowel set `{a, e, i, o, u}`. After computing the counts for all three lines, we compare them with `[5, 7, 5]`.

Even a brute-force interpretation works comfortably here because the input is extremely small. Suppose we repeatedly scan each string for every vowel separately. Each line has length at most 100, so that would still be only a few hundred operations.

The cleaner observation is that we never need word boundaries at all. Spaces are irrelevant, and every consonant can simply be ignored. The whole problem reduces to counting matching characters in each line.

That insight gives a very compact linear solution. We scan each line once, count vowels, and compare the result against the required pattern.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(5 × n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

Here, `n` is the total number of characters across the three lines.

## Algorithm Walkthrough

1. Read the three input lines exactly as they appear.
2. Store the required vowel counts as `[5, 7, 5]`.
3. For each line, scan every character and count how many belong to the vowel set `{a, e, i, o, u}``.
4. Compare the count of the current line with the expected value for that position.

The first line must have 5 vowels, the second must have 7, and the third must have 5.
5. If any line fails the comparison, print `NO` immediately.
6. If all three lines match their required counts, print `YES`.

### Why it works

The definition of a valid haiku in this problem depends only on the number of vowel letters in each phrase. The algorithm counts exactly those characters and ignores everything else. Since every character is checked once and every vowel occurrence contributes exactly one to the count, the computed totals are correct. Comparing these totals with `5-7-5` directly matches the problem definition, so the algorithm cannot accept an invalid poem or reject a valid one.

## Python Solution

```python
import sys
input = sys.stdin.readline

# solution

vowels = set("aeiou")
target = [5, 7, 5]

lines = [input().rstrip('\n') for _ in range(3)]

for i in range(3):
    count = 0

    for ch in lines[i]:
        if ch in vowels:
            count += 1

    if count != target[i]:
        print("NO")
        sys.exit()

print("YES")
```

The solution begins by storing all vowels inside a set. Membership checks in a set are constant time, which keeps the implementation clean and efficient.

The three lines are read exactly as given. We remove only the trailing newline character with `rstrip('\n')`. Using plain `strip()` would also remove leading and trailing spaces, which is unnecessary. Even though spaces do not affect correctness here, preserving the original input format is safer.

For each line, we iterate through every character and increment the counter whenever the character is a vowel.

After counting vowels for a line, we immediately compare the result with the required value. If the counts differ, there is no need to continue checking the remaining lines, so we print `NO` and terminate early.

If all three lines satisfy the required counts, the poem matches the haiku structure and we print `YES`.

## Worked Examples

### Example 1

Input:

```
on  codeforces  
beta round is running
   a rustling of keys
```

| Line | Text | Vowel Count | Expected |
| --- | --- | --- | --- |
| 1 | `on  codeforces` | 5 | 5 |
| 2 | `beta round is running` | 7 | 7 |
| 3 | `a rustling of keys` | 5 | 5 |

Since all three counts match the required pattern, the output is:

```
YES
```

This example demonstrates that multiple spaces and leading spaces do not matter. Only vowel occurrences are counted.

### Example 2

Input:

```
hello
aeiouae
world
```

| Line | Text | Vowel Count | Expected |
| --- | --- | --- | --- |
| 1 | `hello` | 2 | 5 |
| 2 | `aeiouae` | 7 | 7 |
| 3 | `world` | 1 | 5 |

The first line already fails the requirement, so the correct output is:

```
NO
```

This trace shows that a single mismatch is enough to reject the poem.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is scanned once |
| Space | O(1) | Only a few counters and small fixed structures are used |

The maximum total input size is only 300 characters, so the solution runs essentially instantly. Memory usage is constant and far below the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    vowels = set("aeiou")
    target = [5, 7, 5]

    lines = [input().rstrip('\n') for _ in range(3)]

    for i in range(3):
        count = 0

        for ch in lines[i]:
            if ch in vowels:
                count += 1

        if count != target[i]:
            print("NO")
            return

    print("YES")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run(
    "on  codeforces  \n"
    "beta round is running\n"
    "   a rustling of keys\n"
) == "YES\n", "sample 1"

# minimum-size invalid case
assert run(
    "a\n"
    "a\n"
    "a\n"
) == "NO\n", "minimum-size case"

# exact 5-7-5 using repeated vowels
assert run(
    "aaaaa\n"
    "aeiouae\n"
    "eeeee\n"
) == "YES\n", "exact vowel counts"

# spaces everywhere
assert run(
    "   aeiou   \n"
    " aeiouae \n"
    "  eeeee\n"
) == "YES\n", "leading and trailing spaces"

# consonants only
assert run(
    "bcdfg\n"
    "hjklmnp\n"
    "qrst\n"
) == "NO\n", "zero vowels"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a / a / a` | `NO` | Minimum-size invalid input |
| Repeated vowels with exact counts | `YES` | Total occurrences matter |
| Inputs with many spaces | `YES` | Spaces must be ignored |
| Consonants only | `NO` | Zero-vowel handling |

## Edge Cases

A common tricky case is multiple spaces between words and around the sentence.

Input:

```
   aeiou   
 aeiouae 
  eeeee
```

The algorithm scans every character. Spaces are ignored because they are not vowels. The counts become `5`, `7`, and `5`, so the output is:

```
YES
```

Another edge case is lines with no vowels at all.

Input:

```
bcdfg
hjklmnp
qrst
```

The vowel counts are `0`, `0`, and `0`. The first line already fails the required count of `5`, so the algorithm immediately prints:

```
NO
```

A subtle mistake is counting distinct vowels instead of all occurrences.

Input:

```
aaaaa
aeiouae
eeeee
```

The first line contains five copies of the same vowel. The algorithm correctly counts every occurrence separately, producing counts `5`, `7`, and `5`. The output is:

```
YES
```
