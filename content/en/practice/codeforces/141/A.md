---
title: "CF 141A - Amusing Joke"
description: "We are given three uppercase strings. The first two strings are the names written on the door, and the third string is the pile of letters found the next morning after somebody mixed everything together."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings", "strings"]
categories: ["algorithms"]
codeforces_contest: 141
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 101 (Div. 2)"
rating: 800
weight: 141
solve_time_s: 91
verified: true
draft: false
---

[CF 141A - Amusing Joke](https://codeforces.com/problemset/problem/141/A)

**Rating:** 800  
**Tags:** implementation, sortings, strings  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three uppercase strings. The first two strings are the names written on the door, and the third string is the pile of letters found the next morning after somebody mixed everything together.

The task is to check whether the third string contains exactly the same letters as the first two strings combined. Every character matters, including how many times it appears. If the combined names contain three `'A'` characters, the pile must also contain exactly three `'A'` characters. No letters can be missing, and no extra letters are allowed.

The maximum length of each string is only 100, so even fairly inefficient operations are completely safe. A quadratic solution would still run instantly. This gives us freedom to choose the clearest implementation instead of worrying about micro-optimizations.

The main danger is forgetting that character frequency matters, not just character existence. A careless solution might only check whether every distinct character appears somewhere in the pile.

Consider this input:

```
AAB
C
ABAC
```

The correct output is:

```
YES
```

The combined names contain two `'A'`, one `'B'`, and one `'C'`. The pile contains exactly the same counts.

Now look at this case:

```
AAB
C
ABC
```

The correct output is:

```
NO
```

A naive presence-based check would incorrectly accept this because all needed letters appear at least once. The problem is that one `'A'` is missing.

Another easy mistake is forgetting to reject extra letters.

```
ABC
DEF
ABCDEFX
```

The correct output is:

```
NO
```

All required letters are present, but the extra `'X'` makes the pile invalid.

A final edge case is when lengths already disagree.

```
AB
CD
ABC
```

The correct output is:

```
NO
```

The combined names need four letters, but the pile only has three. Any correct solution must reject immediately or detect the mismatch through counting.

## Approaches

The brute-force idea is to generate every possible permutation of the combined names and check whether one of them equals the pile string. This works because the problem literally asks whether the pile could be rearranged into the original letters.

If the combined length is `n`, there are `n!` permutations. Even for `n = 20`, this becomes impossibly large, and the actual limit can reach 200 characters. A factorial-time algorithm is completely infeasible.

The key observation is that the order of characters does not matter at all. The pile can be shuffled arbitrarily. Two strings are equivalent under arbitrary reordering if and only if every character appears the same number of times in both.

That reduces the problem to comparing character frequencies.

There are two common ways to do this. One is to count characters using an array or hash map. The other is to sort both strings and compare the sorted results. Since the input size is tiny, either approach is accepted comfortably.

A sorting-based solution is especially concise. We concatenate the first two strings, sort the result, sort the pile string, and compare them directly. If the sorted versions match, the character multisets are identical.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Permutations | O(n!) | O(n) | Too slow |
| Sorting and Compare | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the guest name, the host name, and the pile string.
2. Concatenate the first two strings because together they represent all letters that should exist.
3. Sort the concatenated string. Sorting groups identical letters together, making frequency comparison straightforward.
4. Sort the pile string for the same reason.
5. Compare the two sorted strings.

If they are identical, every character appears the same number of times in both strings, so print `"YES"`.
6. Otherwise, print `"NO"`.

### Why it works

Sorting transforms each string into a canonical form where identical character multisets become identical strings. If two strings contain exactly the same characters with the same frequencies, their sorted versions must match character by character. If even one character count differs, the sorted strings will differ somewhere. This guarantees the comparison is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

guest = input().strip()
host = input().strip()
pile = input().strip()

combined = guest + host

if sorted(combined) == sorted(pile):
    print("YES")
else:
    print("NO")
```

The first step reads the three input strings and removes trailing newline characters using `strip()`.

The variable `combined` stores all letters that should exist if nobody added or removed anything.

The call to `sorted()` converts each string into a sorted list of characters. Python compares lists lexicographically, so equality succeeds only when both lists contain exactly the same characters in the same counts.

One subtle detail is that sorting alone already handles length mismatches automatically. If one string has extra or missing letters, the sorted lists cannot be equal.

The implementation stays short because Python's built-in sorting handles all the heavy lifting efficiently.

## Worked Examples

### Example 1

Input:

```
SANTACLAUS
DEDMOROZ
SANTAMOROZDEDCLAUS
```

| Step | Value |
| --- | --- |
| Guest | `SANTACLAUS` |
| Host | `DEDMOROZ` |
| Combined | `SANTACLAUSDEDMOROZ` |
| Pile | `SANTAMOROZDEDCLAUS` |
| Sorted Combined | `AACDDELMNOORRSSTTUZ` |
| Sorted Pile | `AACDDELMNOORRSSTTUZ` |
| Result | `YES` |

This trace shows the central invariant of the algorithm. Once order is removed through sorting, both strings become identical because they contain exactly the same character frequencies.

### Example 2

Input:

```
AAB
C
ABC
```

| Step | Value |
| --- | --- |
| Guest | `AAB` |
| Host | `C` |
| Combined | `AABC` |
| Pile | `ABC` |
| Sorted Combined | `AABC` |
| Sorted Pile | `ABC` |
| Result | `NO` |

This example demonstrates why frequency matters. The pile contains all required distinct letters, but only one `'A'` instead of two. Sorting exposes the mismatch immediately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the runtime |
| Space | O(n) | Sorted character lists require additional memory |

Here, `n` is the total number of characters involved. Since the maximum possible length is only 200, the runtime is tiny compared to the limits. The solution easily fits within both the time and memory constraints.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    guest = input().strip()
    host = input().strip()
    pile = input().strip()

    combined = guest + host

    if sorted(combined) == sorted(pile):
        print("YES")
    else:
        print("NO")

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
    "SANTACLAUS\nDEDMOROZ\nSANTAMOROZDEDCLAUS\n"
) == "YES\n", "sample 1"

# missing repeated character
assert run(
    "AAB\nC\nABC\n"
) == "NO\n", "missing repeated character"

# extra character
assert run(
    "ABC\nDEF\nABCDEFX\n"
) == "NO\n", "extra character"

# minimum size valid
assert run(
    "A\nB\nAB\n"
) == "YES\n", "minimum valid case"

# all characters equal
assert run(
    "AAA\nAAAA\nAAAAAAA\n"
) == "YES\n", "all equal characters"

# maximum-style boundary case
assert run(
    "A" * 100 + "\n" +
    "B" * 100 + "\n" +
    "A" * 100 + "B" * 100 + "\n"
) == "YES\n", "large boundary case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `AAB / C / ABC` | `NO` | Detects missing duplicate characters |
| `ABC / DEF / ABCDEFX` | `NO` | Rejects extra letters |
| `A / B / AB` | `YES` | Smallest valid input |
| `AAA / AAAA / AAAAAAA` | `YES` | Handles repeated identical characters |
| 100 `'A'` and 100 `'B'` | `YES` | Boundary-sized input |

## Edge Cases

Consider the repeated-character mismatch case:

```
AAB
C
ABC
```

The algorithm concatenates the first two strings into `"AABC"`. After sorting, we get:

```
AABC
```

The pile sorts to:

```
ABC
```

The strings differ because one `'A'` is missing. The algorithm correctly prints `"NO"`.

Now consider the extra-letter case:

```
ABC
DEF
ABCDEFX
```

The combined string sorts to:

```
ABCDEF
```

The pile sorts to:

```
ABCDEFX
```

The extra `'X'` remains visible after sorting, so the comparison fails and the answer is `"NO"`.

Finally, consider a pure length mismatch:

```
AB
CD
ABC
```

The combined names contain four characters, while the pile contains only three. After sorting:

```
Combined: ABCD
Pile:     ABC
```

The sorted strings cannot match because their lengths differ. The algorithm rejects the input automatically without needing any special-case logic.
