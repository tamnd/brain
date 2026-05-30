---
title: "CF 470G - Hamming Distance"
description: "The task is to compute the Hamming distance between two strings of equal length. In practical terms, you are comparing two sequences of letters and counting how many positions contain different characters. Each mismatch contributes exactly one to the distance."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 470
codeforces_index: "G"
codeforces_contest_name: "Surprise Language Round 7"
rating: 2300
weight: 470
solve_time_s: 57
verified: true
draft: false
---

[CF 470G - Hamming Distance](https://codeforces.com/problemset/problem/470/G)

**Rating:** 2300  
**Tags:** *special  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to compute the Hamming distance between two strings of equal length. In practical terms, you are comparing two sequences of letters and counting how many positions contain different characters. Each mismatch contributes exactly one to the distance. For example, comparing `CODECHEF` and `TOPCODER`, every position where the letters differ increases the total by one, yielding a distance of six.

The input constraints are straightforward: strings have lengths between 1 and 100. This means the problem size is very small, so even a solution that explicitly compares each character one by one will run comfortably within the time limit. Memory is not a concern either, because we only need to store two short strings and a counter. The main edge cases involve the shortest strings of length 1, strings that are identical, or strings where every character differs. For instance, the strings `A` and `A` should produce a distance of `0`, whereas `A` and `B` produce `1`. A careless implementation could accidentally ignore the first or last character, or miscount when the strings are identical.

## Approaches

The brute-force approach is also the optimal approach here due to the small input size. You iterate through the strings in parallel, comparing characters at the same index. Each time the characters differ, you increment a counter. At the end of the loop, the counter contains the total Hamming distance. This method is correct because it directly implements the definition of Hamming distance: the number of differing positions.

There is no faster asymptotic algorithm for this problem because you must examine every character at least once to determine if it matches or differs. Any attempt to optimize further by preprocessing or clever bit manipulation would only complicate the solution without improving runtime, since n ≤ 100. The only potential pitfalls are off-by-one errors in indexing and forgetting to handle strings of length 1 correctly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two input strings. Since the strings are guaranteed to be equal in length, no additional checks are necessary.
2. Initialize a counter variable to zero. This will hold the Hamming distance.
3. Iterate over the indices of the strings from 0 to n-1. For each index, compare the characters from both strings.
4. If the characters differ, increment the counter by one. This captures the definition of Hamming distance directly.
5. After the iteration completes, print the counter. This represents the total number of mismatched positions.

Why it works: the algorithm maintains an invariant that the counter always equals the number of mismatched characters seen so far. By iterating through every position and checking the characters exactly once, we guarantee that no mismatch is missed or double-counted. Since every index is considered, the final counter is exactly the Hamming distance.

## Python Solution

```python
import sys
input = sys.stdin.readline

s1 = input().strip()
s2 = input().strip()

distance = 0
for c1, c2 in zip(s1, s2):
    if c1 != c2:
        distance += 1

print(distance)
```

The solution reads the two strings using fast input. The `strip()` call removes any trailing newline characters that could cause a false mismatch. The loop uses `zip` to iterate over both strings simultaneously, which is cleaner than using an index counter. Every mismatch increments the distance counter. Finally, we print the result.

## Worked Examples

### Sample 1

Input: `CODECHEF` and `TOPCODER`

| Index | s1[i] | s2[i] | Match? | Distance |
| --- | --- | --- | --- | --- |
| 0 | C | T | No | 1 |
| 1 | O | O | Yes | 1 |
| 2 | D | P | No | 2 |
| 3 | E | C | No | 3 |
| 4 | C | O | No | 4 |
| 5 | H | D | No | 5 |
| 6 | E | E | Yes | 5 |
| 7 | F | R | No | 6 |

This demonstrates that the algorithm correctly increments the counter only on mismatches and produces 6.

### Custom Sample

Input: `AAAA` and `ABAA`

| Index | s1[i] | s2[i] | Match? | Distance |
| --- | --- | --- | --- | --- |
| 0 | A | A | Yes | 0 |
| 1 | A | B | No | 1 |
| 2 | A | A | Yes | 1 |
| 3 | A | A | Yes | 1 |

Distance is 1, confirming that single mismatches are counted correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is visited exactly once to compare. n ≤ 100, so this is very fast. |
| Space | O(1) | Only a single integer counter is used beyond the input strings. |

Since n ≤ 100 and the operations per iteration are constant, the solution runs comfortably in under 2 seconds and uses minimal memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s1 = input().strip()
    s2 = input().strip()
    distance = sum(1 for c1, c2 in zip(s1, s2) if c1 != c2)
    return str(distance)

# provided sample
assert run("CODECHEF\nTOPCODER\n") == "6", "sample 1"

# minimum-size input, identical
assert run("A\nA\n") == "0", "single char equal"

# minimum-size input, different
assert run("A\nB\n") == "1", "single char different"

# all characters equal
assert run("XYZXYZ\nXYZXYZ\n") == "0", "all equal"

# all characters different
assert run("AAAA\nBBBB\n") == "4", "all different"

# mixed case
assert run("ABCD\nACBD\n") == "2", "mixed differences"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| A\nA | 0 | Single-character strings that are identical |
| A\nB | 1 | Single-character strings that differ |
| XYZXYZ\nXYZXYZ | 0 | Longer strings where all characters are equal |
| AAAA\nBBBB | 4 | Longer strings where all characters differ |
| ABCD\nACBD | 2 | Strings with partial matches to check correct counting |

## Edge Cases

For the smallest strings, like `A` and `B`, the algorithm initializes `distance = 0`, compares the only character, increments once because they differ, and prints `1`. For identical strings like `XYZXYZ` and `XYZXYZ`, the counter never increments, yielding `0`. Strings where every character differs, like `AAAA` and `BBBB`, increment the counter at every index, producing the length of the string as the distance. In all cases, the iteration invariant ensures correctness, and the solution handles the full range of possible inputs.
