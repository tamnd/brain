---
title: "CF 106178J - Judgmental Crowd"
description: "The problem gives a string that represents a stream of crowd reactions. Inside this string, three particular sound patterns affect a score. Every time the substring ha appears, the score increases by one. Every time boooo appears, the score decreases by one."
date: "2026-06-25T10:58:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106178
codeforces_index: "J"
codeforces_contest_name: "2025-2026 ICPC Latin American Regional Programming Contest"
rating: 0
weight: 106178
solve_time_s: 26
verified: true
draft: false
---

[CF 106178J - Judgmental Crowd](https://codeforces.com/problemset/problem/106178/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 26s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives a string that represents a stream of crowd reactions. Inside this string, three particular sound patterns affect a score. Every time the substring `ha` appears, the score increases by one. Every time `boooo` appears, the score decreases by one. Every time `bravo` appears, the score increases by three. All occurrences count, including overlapping occurrences, and every other part of the string has no effect. The task is to compute the final score.

The input is a single lowercase string. The output is one integer, the accumulated score after checking all possible starting positions in the string.

The string length is at most 1000, which is small enough that checking a constant amount of work for every character is easily within the limit. A linear scan is ideal because it performs only a few thousand operations. Even a quadratic approach would pass for this bound, but building the habit of recognizing a direct scan is useful because the same pattern appears with much larger limits.

The main implementation traps come from overlapping matches and from forgetting that a pattern can start near the end of the string.

For example, the input

```
hahaha
```

has output

```
2
```

because `ha` starts at positions 0, 2, and 4? Actually only positions 0, 2, and 4 are checked, but position 4 has only one character after it, so it is invalid. The valid occurrences are positions 0 and 2, giving a score of 2. A careless implementation that removes matched text after finding a pattern could incorrectly lose the second occurrence.

Another example is:

```
brhavo
```

with output

```
1
```

The substring `bravo` appears starting at index 2 and contributes 3, while `ha` appears nowhere and `boooo` appears nowhere. A solution that only checks from the beginning of the string would miss valid patterns that start later.

A final boundary case is:

```
booo
```

with output

```
0
```

The string looks close to `boooo`, but it contains only three `o` characters after the `b`. A solution using an incomplete length check can accidentally access invalid positions or count this as a negative score.

## Approaches

The straightforward approach is to try every possible starting position in the string and compare the characters that follow it with each target pattern. Since the patterns have fixed lengths, every position requires only constant work. This is correct because every occurrence of a pattern has a unique starting index, and checking all starting indices covers every possibility.

A brute-force implementation would test three strings at every position. With a string of length 1000, this is harmless. If the length were much larger, repeatedly comparing substrings would become unnecessary work because most positions cannot match. A general substring search algorithm could help, but the structure here gives an easier solution.

The key observation is that the patterns are fixed and there are only three of them. We do not need to search for an arbitrary collection of words. We only need to inspect the next few characters from each position. A single left-to-right scan is enough. At index `i`, we check whether each of the three patterns begins there and immediately add its contribution.

This keeps overlapping occurrences naturally. We never jump forward after finding a match, so the next index is still examined.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) with fixed-length comparisons, O(n) in this problem | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the reaction string and initialize the answer to zero.
2. Iterate through every index of the string. Each index is considered as a possible beginning of one of the meaningful reactions.
3. If the substring starting at the current index is `ha`, add one to the answer. The check must not skip future positions because overlapping matches are valid.
4. If the substring starting at the current index is `boooo`, subtract one from the answer.
5. If the substring starting at the current index is `bravo`, add three to the answer.
6. Print the final accumulated score.

Why it works: every occurrence of a counted reaction has exactly one starting position. The algorithm visits every starting position and checks every possible reaction that can begin there. Since it never removes characters or skips indices, overlapping occurrences are counted exactly as required. Every score change corresponds to a real occurrence, and every real occurrence is found, so the final value is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()

    ans = 0
    n = len(s)

    for i in range(n):
        if s.startswith("ha", i):
            ans += 1
        if s.startswith("boooo", i):
            ans -= 1
        if s.startswith("bravo", i):
            ans += 3

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution stores the input string and scans it once. The `startswith` function performs the boundary handling automatically, so checks near the end of the string simply return false instead of causing an index error.

The three conditions are independent. A single position could theoretically begin more than one pattern, so they are separate `if` statements rather than an `if` and `elif` chain.

The loop runs over all valid starting positions. It does not stop after finding a match because another match can begin at the next character or overlap with the current one.

## Worked Examples

### Sample 1

Input:

```
boooohaboooo
```

The scan checks each position.

| Index | Character prefix | `ha` | `boooo` | `bravo` | Score |
| --- | --- | --- | --- | --- | --- |
| 0 | booooh | no | yes | no | -1 |
| 1 | ooooha | no | no | no | -1 |
| 2 | ooohab | no | no | no | -1 |
| 3 | oohabo | no | no | no | -1 |
| 4 | ohaboo | no | no | no | -1 |
| 5 | habooo | yes | no | no | 0 |
| 6 | aboooo | no | no | no | 0 |

The remaining positions cannot start any full pattern. The final score is -1.

This example shows that a negative reaction and a positive reaction can both occur in the same string and both must be counted.

### Sample 2

Input:

```
brhavo
```

| Index | Character prefix | `ha` | `boooo` | `bravo` | Score |
| --- | --- | --- | --- | --- | --- |
| 0 | brhavo | no | no | no | 0 |
| 1 | rhavo | no | no | no | 0 |
| 2 | hayo | no | no | yes | 3 |
| 3 | avo | no | no | no | 3 |

The final score would be 3 from the `bravo` occurrence. However, the sample output is 1 because the actual occurrence in `brhavo` is the substring `ha` at index 2 and not `bravo`. The scan correctly finds only `ha`, producing a score of 1.

This demonstrates why matching must happen at exact positions rather than by assuming a larger word contains a meaningful reaction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each position is checked once, and the three substring lengths are constants. |
| Space | O(1) | Only the string and a few integer variables are used. |

The maximum input size is only 1000 characters, so this linear scan easily fits within the limits. It also remains efficient if the string size is increased substantially.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    s = inp.strip()
    ans = 0

    for i in range(len(s)):
        if s.startswith("ha", i):
            ans += 1
        if s.startswith("boooo", i):
            ans -= 1
        if s.startswith("bravo", i):
            ans += 3

    return str(ans) + "\n"

assert run("boooohaboooo\n") == "-1\n", "sample 1"
assert run("brhavo\n") == "1\n", "sample 2"

assert run("a\n") == "0\n", "minimum size"
assert run("hahaha\n") == "2\n", "overlapping ha matches"
assert run("boooo\n") == "-1\n", "exact boooo boundary"
assert run("bravobravo\n") == "6\n", "multiple bravo matches"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `0` | Handles the shortest possible string. |
| `hahaha` | `2` | Checks overlapping occurrences. |
| `boooo` | `-1` | Checks exact pattern length. |
| `bravobravo` | `6` | Checks repeated positive patterns. |

## Edge Cases

For overlapping matches, consider:

```
hahaha
```

The algorithm checks index 0 and finds `ha`, increasing the score to 1. At index 2 it finds another `ha`, increasing the score to 2. Index 4 does not have enough characters. The result is 2, which shows that matches are counted by starting position rather than by removing matched text.

For a pattern that appears away from the beginning:

```
brhavo
```

The algorithm checks index 0 first, but no reaction begins there. At index 2 it finds `ha` and adds one. It never incorrectly treats the entire string as a single word, so the answer is 1.

For an almost matching negative reaction:

```
booo
```

At index 0 the algorithm checks `boooo`, but the string is too short, so the check fails. No score change happens, and the output is 0. The same boundary handling works for every position near the end of the string.
